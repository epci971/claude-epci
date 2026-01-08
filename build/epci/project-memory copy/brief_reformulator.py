#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Brief Reformulator

Detects fuzzy/voice-dictated briefs and reformulates them into structured format.
Integrates with clarification_analyzer for domain detection and voice_cleaner
for artifact removal.

Usage:
    from project_memory.brief_reformulator import (
        calculate_fuzziness_score,
        reformulate_brief,
        needs_reformulation
    )

    score = calculate_fuzziness_score("euh faudrait un truc pour les users")
    if needs_reformulation(score):
        result = reformulate_brief(brief, exploration_context)
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

try:
    from .clarification_analyzer import (
        analyze_brief,
        BriefAnalysis,
        extract_keywords
    )
    from .voice_cleaner import (
        clean_voice_transcript,
        calculate_hesitation_density,
        VoiceCleaningResult
    )
except ImportError:
    # Fallback for direct execution
    from clarification_analyzer import (
        analyze_brief,
        BriefAnalysis,
        extract_keywords
    )
    from voice_cleaner import (
        clean_voice_transcript,
        calculate_hesitation_density,
        VoiceCleaningResult
    )


# =============================================================================
# CONSTANTS
# =============================================================================

# Fuzziness thresholds
FUZZINESS_AUTO_THRESHOLD = 0.6    # Auto-trigger reformulation
FUZZINESS_SUGGEST_THRESHOLD = 0.4  # Suggest reformulation

# Fuzziness score weights
WEIGHT_DOMAIN_CONFIDENCE = 0.35
WEIGHT_GAP_COUNT = 0.25
WEIGHT_SCOPE_CLARITY = 0.20
WEIGHT_HESITATION_DENSITY = 0.20

# Maximum gaps to consider (for normalization)
MAX_GAPS = 8

# Vague indicators that suggest unclear brief
VAGUE_INDICATORS: List[str] = [
    "système", "system", "module", "feature",
    "améliorer", "improve", "ajouter", "add",
    "truc", "chose", "thing", "stuff",
    "quelque chose", "something", "machin"
]

# Clear scope indicators
CLEAR_SCOPE_INDICATORS: List[str] = [
    "uniquement", "seulement", "only", "just",
    "inclus", "exclu", "include", "exclude",
    "limité à", "limited to", "specifically"
]


class TemplateType(Enum):
    """Types of brief templates."""
    FEATURE = "feature"      # New functionality
    PROBLEM = "problem"      # Bug fix / issue
    DECISION = "decision"    # Technical decision needed
    UNKNOWN = "unknown"


# Template detection keywords
TEMPLATE_KEYWORDS: Dict[TemplateType, List[str]] = {
    TemplateType.FEATURE: [
        "ajouter", "créer", "implémenter", "développer", "nouveau",
        "add", "create", "implement", "develop", "new", "build"
    ],
    TemplateType.PROBLEM: [
        "bug", "erreur", "fixer", "corriger", "problème", "cassé",
        "error", "fix", "broken", "issue", "fail", "crash", "ne marche pas"
    ],
    TemplateType.DECISION: [
        "choisir", "décider", "quelle", "comment", "stratégie",
        "choose", "decide", "which", "how", "strategy", "approach", "should"
    ],
}


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class FuzzinessScore:
    """Fuzziness analysis result."""
    overall: float
    domain_confidence: float
    gap_score: float
    scope_clarity: float
    hesitation_density: float
    needs_reformulation: bool
    suggestion_level: str  # "auto", "suggest", "skip"
    details: Dict[str, any] = field(default_factory=dict)


@dataclass
class ReformulatedBrief:
    """Structured reformulated brief."""
    objective: str
    context: str
    constraints: str
    success_criteria: str
    template_type: TemplateType
    original_brief: str
    cleaned_brief: str
    cleaning_result: Optional[VoiceCleaningResult] = None
    fuzziness_score: Optional[FuzzinessScore] = None


# =============================================================================
# FUNCTIONS
# =============================================================================

def calculate_fuzziness_score(brief: str) -> FuzzinessScore:
    """
    Calculate how fuzzy/unclear a brief is.

    Components:
    - Domain confidence: Lower = more fuzzy (weight: 35%)
    - Gap count: More gaps = more fuzzy (weight: 25%)
    - Scope clarity: No indicators = more fuzzy (weight: 20%)
    - Hesitation density: Higher = more fuzzy (weight: 20%)

    Args:
        brief: Raw brief text.

    Returns:
        FuzzinessScore with overall score and components.
    """
    # Analyze brief with existing system
    analysis = analyze_brief(brief)

    # Calculate domain confidence component (inverted: low confidence = high fuzziness)
    domain_confidence = analysis.domain.confidence
    domain_component = 1 - domain_confidence

    # Calculate gap score (normalized)
    gap_count = len([g for g in analysis.gaps if g.priority == "high"])
    gap_score = min(gap_count / MAX_GAPS, 1.0)

    # Calculate scope clarity
    scope_clarity = _calculate_scope_clarity(brief, analysis.scope_indicators)
    scope_component = 1 - scope_clarity

    # Calculate hesitation density
    density = calculate_hesitation_density(brief)
    hesitation_component = density.density

    # Weighted overall score
    overall = (
        domain_component * WEIGHT_DOMAIN_CONFIDENCE +
        gap_score * WEIGHT_GAP_COUNT +
        scope_component * WEIGHT_SCOPE_CLARITY +
        hesitation_component * WEIGHT_HESITATION_DENSITY
    )

    # Determine suggestion level
    if overall >= FUZZINESS_AUTO_THRESHOLD:
        suggestion_level = "auto"
        needs_reformat = True
    elif overall >= FUZZINESS_SUGGEST_THRESHOLD:
        suggestion_level = "suggest"
        needs_reformat = True
    else:
        suggestion_level = "skip"
        needs_reformat = False

    return FuzzinessScore(
        overall=round(overall, 3),
        domain_confidence=round(domain_confidence, 3),
        gap_score=round(gap_score, 3),
        scope_clarity=round(scope_clarity, 3),
        hesitation_density=round(hesitation_component, 3),
        needs_reformulation=needs_reformat,
        suggestion_level=suggestion_level,
        details={
            "domain": analysis.domain.name,
            "keywords": analysis.keywords,
            "high_priority_gaps": gap_count,
            "total_gaps": len(analysis.gaps),
            "hesitation_count": density.hesitation_count,
            "filler_count": density.filler_count,
            "word_count": density.total_words
        }
    )


def needs_reformulation(score: FuzzinessScore, force: bool = False, skip: bool = False) -> bool:
    """
    Determine if brief needs reformulation based on score and flags.

    Args:
        score: Calculated fuzziness score.
        force: --rephrase flag (force reformulation).
        skip: --no-rephrase flag (skip reformulation).

    Returns:
        True if reformulation should be triggered.
    """
    if skip:
        return False
    if force:
        return True
    return score.needs_reformulation


def detect_template_type(brief: str) -> TemplateType:
    """
    Detect the type of brief (feature, problem, decision).

    Args:
        brief: Brief text.

    Returns:
        Detected TemplateType.
    """
    brief_lower = brief.lower()

    scores = {template: 0 for template in TemplateType if template != TemplateType.UNKNOWN}

    for template_type, keywords in TEMPLATE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in brief_lower:
                scores[template_type] += 1

    if not any(scores.values()):
        return TemplateType.UNKNOWN

    return max(scores, key=scores.get)


def reformulate_brief(
    brief: str,
    exploration_context: Optional[Dict] = None
) -> ReformulatedBrief:
    """
    Reformulate a fuzzy brief into structured format.

    Steps:
    1. Clean voice artifacts
    2. Detect template type
    3. Extract objective, context, constraints
    4. Generate success criteria

    Args:
        brief: Raw brief text.
        exploration_context: Optional context from @Explore (files, patterns).

    Returns:
        ReformulatedBrief with structured content.
    """
    # Step 1: Clean voice artifacts
    cleaning_result = clean_voice_transcript(brief)
    cleaned = cleaning_result.cleaned_text

    # Step 2: Calculate fuzziness (for reference)
    fuzziness = calculate_fuzziness_score(brief)

    # Step 3: Detect template type
    template_type = detect_template_type(cleaned)

    # Step 4: Extract components based on template
    objective = _extract_objective(cleaned, template_type)
    context = _extract_context(cleaned, exploration_context)
    constraints = _extract_constraints(cleaned, exploration_context)
    success_criteria = _generate_success_criteria(cleaned, template_type)

    return ReformulatedBrief(
        objective=objective,
        context=context,
        constraints=constraints,
        success_criteria=success_criteria,
        template_type=template_type,
        original_brief=brief,
        cleaned_brief=cleaned,
        cleaning_result=cleaning_result,
        fuzziness_score=fuzziness
    )


def format_reformulation_display(result: ReformulatedBrief) -> str:
    """
    Format reformulated brief for breakpoint display.

    Args:
        result: ReformulatedBrief to format.

    Returns:
        Formatted string for display.
    """
    lines = []
    lines.append(f"**Objectif**: {result.objective}")
    lines.append(f"**Contexte**: {result.context}")
    lines.append(f"**Contraintes**: {result.constraints}")
    lines.append(f"**Critères de succès**: {result.success_criteria}")

    return "\n".join(lines)


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _calculate_scope_clarity(brief: str, scope_indicators: List[str]) -> float:
    """Calculate scope clarity score."""
    brief_lower = brief.lower()
    word_count = len(brief.split())

    # Check for clear scope indicators
    has_clear_indicator = any(ind in brief_lower for ind in CLEAR_SCOPE_INDICATORS)
    if has_clear_indicator:
        return 1.0

    # Check for vague indicators
    has_vague = any(ind in brief_lower for ind in VAGUE_INDICATORS)

    # Short brief with vague terms = unclear scope
    if word_count < 20 and has_vague:
        return 0.2

    # Has scope indicators from analysis
    if scope_indicators:
        return 0.8

    # Moderate length without clear indicators
    if word_count >= 20:
        return 0.5

    return 0.3


def _extract_objective(brief: str, template_type: TemplateType) -> str:
    """Extract or generate objective from brief."""
    # Clean and format
    objective = brief.strip()

    # Template-specific prefixes
    prefixes = {
        TemplateType.FEATURE: "Implémenter",
        TemplateType.PROBLEM: "Corriger",
        TemplateType.DECISION: "Définir",
        TemplateType.UNKNOWN: "Réaliser"
    }

    # If brief doesn't start with a verb, add prefix
    first_word = objective.split()[0].lower() if objective else ""
    action_verbs = ["ajouter", "créer", "implémenter", "corriger", "fixer", "add", "create", "fix"]

    if first_word not in action_verbs:
        prefix = prefixes.get(template_type, "Réaliser")
        # Extract core subject
        keywords = extract_keywords(brief)
        if keywords:
            core = " ".join(keywords[:3])
            objective = f"{prefix} {core}"
        else:
            objective = f"{prefix}: {brief[:100]}"

    # Ensure ends with period
    if objective and not objective.endswith('.'):
        objective += '.'

    return objective


def _extract_context(brief: str, exploration_context: Optional[Dict]) -> str:
    """Extract context from brief and exploration."""
    context_parts = []

    # From exploration context
    if exploration_context:
        if "stack" in exploration_context:
            context_parts.append(f"Stack: {exploration_context['stack']}")
        if "impacted_files" in exploration_context:
            count = len(exploration_context["impacted_files"])
            context_parts.append(f"{count} fichier(s) impacté(s)")
        if "patterns" in exploration_context:
            context_parts.append(f"Patterns: {', '.join(exploration_context['patterns'][:3])}")

    # If no exploration context, provide generic
    if not context_parts:
        analysis = analyze_brief(brief)
        if analysis.domain.name != "unknown":
            context_parts.append(f"Domaine: {analysis.domain.name}")
        if analysis.keywords:
            context_parts.append(f"Concepts: {', '.join(analysis.keywords[:5])}")

    return " | ".join(context_parts) if context_parts else "À déterminer lors de l'exploration."


def _extract_constraints(brief: str, exploration_context: Optional[Dict]) -> str:
    """Extract constraints from brief and exploration."""
    constraints = []

    brief_lower = brief.lower()

    # Look for explicit constraints
    constraint_patterns = [
        (r"sans\s+(\w+)", "Sans {}"),
        (r"without\s+(\w+)", "Sans {}"),
        (r"pas de\s+(\w+)", "Pas de {}"),
        (r"no\s+(\w+)", "Pas de {}"),
        (r"doit être\s+(\w+)", "Doit être {}"),
        (r"must be\s+(\w+)", "Doit être {}"),
    ]

    for pattern, template in constraint_patterns:
        matches = re.findall(pattern, brief_lower)
        for match in matches:
            constraints.append(template.format(match))

    # From exploration context
    if exploration_context and "risks" in exploration_context:
        for risk in exploration_context["risks"][:2]:
            constraints.append(f"Attention: {risk}")

    return " | ".join(constraints) if constraints else "Aucune contrainte explicite identifiée."


def _generate_success_criteria(brief: str, template_type: TemplateType) -> str:
    """Generate success criteria based on template type."""
    criteria = {
        TemplateType.FEATURE: "Feature fonctionnelle et testée",
        TemplateType.PROBLEM: "Bug corrigé, pas de régression",
        TemplateType.DECISION: "Décision documentée avec justification",
        TemplateType.UNKNOWN: "Objectif atteint et validé"
    }

    base = criteria.get(template_type, criteria[TemplateType.UNKNOWN])

    # Add domain-specific criteria
    analysis = analyze_brief(brief)
    domain = analysis.domain.name

    domain_criteria = {
        "auth": " | Sécurité validée",
        "api": " | Contrat API documenté",
        "ui": " | UX conforme aux maquettes",
        "data": " | Migrations réversibles",
        "payment": " | Conformité PCI-DSS"
    }

    if domain in domain_criteria:
        base += domain_criteria[domain]

    return base


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python brief_reformulator.py '<brief>'")
        print("Example: python brief_reformulator.py 'euh faudrait un truc pour les users'")
        return 1

    brief = ' '.join(sys.argv[1:])

    # Calculate fuzziness
    score = calculate_fuzziness_score(brief)
    print("=" * 60)
    print("FUZZINESS ANALYSIS")
    print("=" * 60)
    print(f"Overall score: {score.overall:.1%}")
    print(f"  Domain confidence: {score.domain_confidence:.1%}")
    print(f"  Gap score: {score.gap_score:.1%}")
    print(f"  Scope clarity: {score.scope_clarity:.1%}")
    print(f"  Hesitation density: {score.hesitation_density:.1%}")
    print(f"Suggestion level: {score.suggestion_level}")
    print(f"Needs reformulation: {score.needs_reformulation}")

    if score.needs_reformulation:
        print("\n" + "=" * 60)
        print("REFORMULATION")
        print("=" * 60)
        result = reformulate_brief(brief)
        print(f"Template type: {result.template_type.value}")
        print(f"\nCleaned brief: {result.cleaned_brief}")
        print(f"\n{format_reformulation_display(result)}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
