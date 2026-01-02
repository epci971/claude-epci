#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Question Generator

Generates intelligent clarification questions based on brief analysis,
similar features, and project context.

Used by the intelligent clarification system (F05).

Usage:
    from project_memory.question_generator import generate_questions

    questions = generate_questions(
        brief="Add notification system",
        context={"stack": "symfony", "patterns": ["event-driven"]},
        similar_features=[{"slug": "user-alerts", "title": "User Alerts", "score": 0.8}]
    )
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


# =============================================================================
# CONSTANTS
# =============================================================================

class QuestionType(Enum):
    """Types of clarification questions."""
    REUSE = "reuse"           # Suggest reusing similar feature
    TECHNICAL = "technical"   # Technical implementation question
    SCOPE = "scope"           # Scope/boundary question
    INTEGRATION = "integration"  # Integration with existing systems
    PRIORITY = "priority"     # Priority/urgency question


# Maximum questions per iteration (CDC requirement)
MAX_QUESTIONS = 3


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class Question:
    """A clarification question with metadata."""
    type: QuestionType
    text: str
    suggestion: Optional[str] = None
    reason: Optional[str] = None
    source_feature: Optional[str] = None  # Slug of related feature
    priority: str = "medium"  # high, medium, low

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'type': self.type.value,
            'text': self.text,
            'suggestion': self.suggestion,
            'reason': self.reason,
            'source_feature': self.source_feature,
            'priority': self.priority,
        }


@dataclass
class ClarificationResult:
    """Result of question generation."""
    questions: List[Question]
    similar_features_found: int
    domain_detected: str
    patterns_available: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'questions': [q.to_dict() for q in self.questions],
            'similar_features_found': self.similar_features_found,
            'domain_detected': self.domain_detected,
            'patterns_available': self.patterns_available,
        }


# =============================================================================
# QUESTION TEMPLATES
# =============================================================================

REUSE_TEMPLATES = {
    'fr': "La feature `{feature_slug}` ({feature_title}) utilise {pattern}. Voulez-vous réutiliser cette approche ?",
    'en': "Feature `{feature_slug}` ({feature_title}) uses {pattern}. Would you like to reuse this approach?",
}

TECHNICAL_TEMPLATES = {
    'auth': {
        'fr': "Quelle méthode d'authentification souhaitez-vous : OAuth, JWT, session-based ?",
        'en': "Which authentication method do you prefer: OAuth, JWT, or session-based?",
        'suggestion': "JWT",
    },
    'api': {
        'fr': "Quelles opérations CRUD sont nécessaires pour cette API ?",
        'en': "Which CRUD operations are needed for this API?",
        'suggestion': "GET, POST, PUT, DELETE",
    },
    'notification': {
        'fr': "Quels canaux de notification : email, push, in-app, SMS ?",
        'en': "Which notification channels: email, push, in-app, SMS?",
        'suggestion': "email + in-app",
    },
    'data': {
        'fr': "Quelles sont les entités principales et leurs relations ?",
        'en': "What are the main entities and their relationships?",
        'suggestion': None,
    },
    'ui': {
        'fr': "Quelles sont les cibles : desktop, mobile, les deux ?",
        'en': "What are the targets: desktop, mobile, or both?",
        'suggestion': "responsive (both)",
    },
    'payment': {
        'fr': "Quel fournisseur de paiement : Stripe, PayPal, autre ?",
        'en': "Which payment provider: Stripe, PayPal, or other?",
        'suggestion': "Stripe",
    },
    'search': {
        'fr': "Sur quelles entités et champs la recherche doit-elle porter ?",
        'en': "Which entities and fields should be searchable?",
        'suggestion': None,
    },
    'infra': {
        'fr': "Quel environnement cible : production, staging, développement ?",
        'en': "Which target environment: production, staging, or development?",
        'suggestion': "all environments",
    },
}

SCOPE_TEMPLATES = {
    'fr': "Quel est le périmètre exact ? Qu'est-ce qui est inclus/exclu ?",
    'en': "What is the exact scope? What is included/excluded?",
}

INTEGRATION_TEMPLATES = {
    'fr': "Comment cette feature s'intègre-t-elle avec {component} existant ?",
    'en': "How does this feature integrate with the existing {component}?",
}

PRIORITY_TEMPLATES = {
    'backend': {
        'fr': "Quelle garantie de fiabilité est requise (retry, idempotence) ?",
        'en': "What reliability guarantee is required (retry, idempotence)?",
    },
    'frontend': {
        'fr': "Quelles sont les exigences UX et d'accessibilité ?",
        'en': "What are the UX and accessibility requirements?",
    },
    'security': {
        'fr': "Quelles données sensibles sont manipulées (PII, credentials) ?",
        'en': "What sensitive data is handled (PII, credentials)?",
    },
}


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def generate_questions(
    brief: str,
    context: Dict[str, Any],
    similar_features: List[Dict[str, Any]],
    gaps: Optional[List[Dict[str, Any]]] = None,
    persona: Optional[str] = None,
    lang: str = 'fr'
) -> ClarificationResult:
    """
    Generate intelligent clarification questions.

    Algorithm (from CDC §3.3):
    1. If similar feature found → generate reuse question
    2. Generate technical gap questions (max 2)
    3. Adapt to persona
    4. Return max 3 questions

    Args:
        brief: The raw brief text.
        context: Project context with stack, patterns, etc.
        similar_features: List of similar features from similarity matcher.
        gaps: List of gaps from clarification analyzer.
        persona: Active persona (backend, frontend, security, etc.).
        lang: Language for questions ('fr' or 'en').

    Returns:
        ClarificationResult with max 3 questions.
    """
    questions: List[Question] = []
    domain = context.get('domain', 'unknown')
    patterns = context.get('patterns', [])

    # 1. Reuse question if similar feature found
    if similar_features:
        best_match = similar_features[0]
        if best_match.get('score', 0) >= 0.5:  # Only suggest if good match
            reuse_q = _generate_reuse_question(best_match, patterns, lang)
            if reuse_q:
                questions.append(reuse_q)

    # 2. Technical gap questions (max 2)
    if gaps:
        for gap in gaps[:2]:  # Max 2 gap questions
            if len(questions) >= MAX_QUESTIONS:
                break
            tech_q = _generate_gap_question(gap, domain, lang)
            if tech_q:
                questions.append(tech_q)
    else:
        # No gaps provided, use domain-based technical question
        if len(questions) < MAX_QUESTIONS:
            tech_q = _generate_technical_question(domain, lang)
            if tech_q:
                questions.append(tech_q)

    # 3. Scope question if still room
    if len(questions) < MAX_QUESTIONS and _needs_scope_clarification(brief):
        scope_q = _generate_scope_question(lang)
        questions.append(scope_q)

    # 4. Adapt to persona
    questions = adapt_to_persona(questions, persona, lang)

    # Ensure max 3 questions
    questions = questions[:MAX_QUESTIONS]

    return ClarificationResult(
        questions=questions,
        similar_features_found=len(similar_features),
        domain_detected=domain,
        patterns_available=patterns,
    )


def adapt_to_persona(
    questions: List[Question],
    persona: Optional[str],
    lang: str = 'fr'
) -> List[Question]:
    """
    Adapt questions to the active persona.

    F09 Integration Point: When personas are implemented, this function
    will modify questions based on persona focus:
    - backend: Focus on reliability, performance, queues, data integrity
    - frontend: Focus on UX, accessibility, animations, responsiveness
    - security: Focus on auth, validation, OWASP, compliance
    - architect: Focus on patterns, scalability, design decisions
    - qa: Focus on testability, edge cases, coverage
    - doc: Focus on clarity, examples, maintenance

    Args:
        questions: List of questions to adapt.
        persona: Active persona name (or None).
        lang: Language for questions.

    Returns:
        Adapted questions (currently unchanged until F09 ready).
    """
    if not persona:
        return questions

    # Stub: Add persona-specific question if room
    if len(questions) < MAX_QUESTIONS and persona in PRIORITY_TEMPLATES:
        template = PRIORITY_TEMPLATES[persona]
        questions.append(Question(
            type=QuestionType.PRIORITY,
            text=template.get(lang, template.get('fr', '')),
            priority="medium",
            reason=f"Question adaptée à la persona {persona}",
        ))

    return questions


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _generate_reuse_question(
    feature: Dict[str, Any],
    patterns: List[str],
    lang: str
) -> Optional[Question]:
    """Generate a reuse suggestion question."""
    template = REUSE_TEMPLATES.get(lang, REUSE_TEMPLATES['fr'])

    # Detect pattern from files
    pattern_detected = "un pattern similaire"
    files = feature.get('files_modified', [])
    for f in files:
        f_lower = f.lower()
        if 'service' in f_lower:
            pattern_detected = "le pattern Service"
            break
        elif 'repository' in f_lower:
            pattern_detected = "le pattern Repository"
            break
        elif 'event' in f_lower or 'listener' in f_lower:
            pattern_detected = "le pattern Event-driven"
            break
        elif 'controller' in f_lower:
            pattern_detected = "le pattern MVC"
            break

    text = template.format(
        feature_slug=feature.get('slug', ''),
        feature_title=feature.get('title', feature.get('slug', '')),
        pattern=pattern_detected,
    )

    return Question(
        type=QuestionType.REUSE,
        text=text,
        suggestion="Oui" if lang == 'fr' else "Yes",
        source_feature=feature.get('slug'),
        priority="high",
        reason=f"Feature similaire trouvée (score: {feature.get('score', 0):.0%})",
    )


def _generate_technical_question(domain: str, lang: str) -> Optional[Question]:
    """Generate domain-specific technical question."""
    templates = TECHNICAL_TEMPLATES.get(domain)
    if not templates:
        return None

    text = templates.get(lang, templates.get('fr', ''))
    if not text:
        return None

    return Question(
        type=QuestionType.TECHNICAL,
        text=text,
        suggestion=templates.get('suggestion'),
        priority="high",
        reason=f"Question technique pour le domaine {domain}",
    )


def _generate_gap_question(gap: Dict[str, Any], domain: str, lang: str) -> Optional[Question]:
    """Generate question from a gap analysis result."""
    # Use the example question from the gap
    example_question = gap.get('example_question', '')
    if not example_question:
        return None

    return Question(
        type=QuestionType.TECHNICAL,
        text=example_question,
        priority=gap.get('priority', 'medium'),
        reason=f"Information manquante: {gap.get('description', '')}",
    )


def _generate_scope_question(lang: str) -> Question:
    """Generate scope clarification question."""
    template = SCOPE_TEMPLATES.get(lang, SCOPE_TEMPLATES['fr'])
    return Question(
        type=QuestionType.SCOPE,
        text=template,
        priority="medium",
        reason="Périmètre à clarifier",
    )


def _needs_scope_clarification(brief: str) -> bool:
    """Check if brief needs scope clarification."""
    brief_lower = brief.lower()

    # Scope indicators that suggest clarity
    clear_indicators = [
        'uniquement', 'seulement', 'only', 'just',
        'inclus', 'exclu', 'include', 'exclude',
        'limité à', 'limited to',
    ]

    # If any clear indicator present, scope is likely defined
    if any(ind in brief_lower for ind in clear_indicators):
        return False

    # Vague indicators that suggest need for clarification
    vague_indicators = [
        'système', 'system', 'module', 'feature',
        'améliorer', 'improve', 'ajouter', 'add',
    ]

    # Short briefs with vague terms need clarification
    word_count = len(brief.split())
    has_vague = any(ind in brief_lower for ind in vague_indicators)

    return word_count < 20 and has_vague


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def generate_clarification(
    brief: str,
    manager: Any,  # ProjectMemoryManager
    persona: Optional[str] = None,
    lang: str = 'fr'
) -> ClarificationResult:
    """
    High-level function to generate clarification from a brief.

    Combines analyzer, matcher, and generator.

    Args:
        brief: Raw brief text.
        manager: ProjectMemoryManager instance.
        persona: Active persona (optional).
        lang: Language ('fr' or 'en').

    Returns:
        ClarificationResult with intelligent questions.
    """
    try:
        from .clarification_analyzer import analyze_brief

        # Analyze brief
        analysis = analyze_brief(brief)

        # Find similar features
        similar = manager.find_similar_features(
            analysis.keywords,
            threshold=0.3
        )

        # Get patterns for domain
        patterns = manager.get_patterns_for_domain(analysis.domain.name)

        # Build context
        context = {
            'domain': analysis.domain.name,
            'patterns': patterns,
            'keywords': analysis.keywords,
        }

        # Convert gaps to dict format
        gaps = [
            {
                'category': g.category,
                'description': g.description,
                'priority': g.priority,
                'example_question': g.example_question,
            }
            for g in analysis.gaps
        ]

        # Generate questions
        return generate_questions(
            brief=brief,
            context=context,
            similar_features=similar,
            gaps=gaps,
            persona=persona,
            lang=lang,
        )

    except Exception as e:
        # Graceful degradation: return generic questions
        return ClarificationResult(
            questions=[
                Question(
                    type=QuestionType.SCOPE,
                    text=SCOPE_TEMPLATES.get(lang, SCOPE_TEMPLATES['fr']),
                    priority="high",
                    reason="Clarification générique (erreur système)",
                )
            ],
            similar_features_found=0,
            domain_detected='unknown',
            patterns_available=[],
        )


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python question_generator.py '<brief>'")
        print("Example: python question_generator.py 'Ajouter un système de notifications'")
        return 1

    brief = ' '.join(sys.argv[1:])

    # Mock context and similar features for testing
    context = {
        'domain': 'notification',
        'patterns': ['event-driven', 'service'],
    }

    similar_features = [
        {
            'slug': 'user-alerts',
            'title': 'User Alerts System',
            'score': 0.75,
            'files_modified': ['src/Service/AlertService.php', 'src/Event/UserAlert.php'],
        }
    ]

    result = generate_questions(
        brief=brief,
        context=context,
        similar_features=similar_features,
        lang='fr',
    )

    print(f"Brief: {brief}")
    print(f"Domain: {result.domain_detected}")
    print(f"Similar features: {result.similar_features_found}")
    print(f"\nQuestions ({len(result.questions)}):")

    for i, q in enumerate(result.questions, 1):
        print(f"\n{i}. [{q.type.value}] {q.text}")
        if q.suggestion:
            print(f"   Suggestion: {q.suggestion}")
        if q.reason:
            print(f"   Raison: {q.reason}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
