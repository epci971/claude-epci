#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Suggestion Engine

Core engine for generating and managing proactive suggestions.
Part of F06 Proactive Suggestions feature.

Usage:
    from project_memory.suggestion_engine import SuggestionEngine

    engine = SuggestionEngine(memory_dir)
    suggestions = engine.generate_suggestions(findings, context)
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

try:
    from .patterns.catalog import (
        PATTERN_CATALOG,
        PatternDefinition,
        Priority,
        Category,
        get_pattern,
    )
    from .learning_analyzer import LearningAnalyzer, MIN_SCORE_THRESHOLD
except ImportError:
    from patterns.catalog import (
        PATTERN_CATALOG,
        PatternDefinition,
        Priority,
        Category,
        get_pattern,
    )
    from learning_analyzer import LearningAnalyzer, MIN_SCORE_THRESHOLD


# =============================================================================
# CONSTANTS
# =============================================================================

MAX_SUGGESTIONS_DEFAULT = 5
PRIORITY_WEIGHTS = {
    Priority.P1: 100,
    Priority.P2: 70,
    Priority.P3: 50,
}
IMPACT_MULTIPLIERS = {
    "critical": 1.5,
    "important": 1.2,
    "moderate": 1.0,
    "minor": 0.7,
}


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class Finding:
    """A detected issue or pattern in code."""
    pattern_id: str
    file_path: str
    line_number: Optional[int] = None
    message: str = ""
    severity: str = "minor"
    context: Dict[str, Any] = field(default_factory=dict)
    source: str = "detector"  # detector, code-reviewer, security-auditor, qa-reviewer

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'pattern_id': self.pattern_id,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'message': self.message,
            'severity': self.severity,
            'context': self.context,
            'source': self.source,
        }


@dataclass
class Suggestion:
    """A proactive suggestion to present to the user."""
    id: str
    pattern_id: str
    priority: Priority
    category: Category
    title: str
    description: str
    suggestion_text: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    score: float = 0.5
    auto_fixable: bool = False
    source: str = "detector"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'pattern_id': self.pattern_id,
            'priority': self.priority.name,
            'category': self.category.value,
            'title': self.title,
            'description': self.description,
            'suggestion_text': self.suggestion_text,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'score': self.score,
            'auto_fixable': self.auto_fixable,
            'source': self.source,
            'created_at': self.created_at,
        }

    @property
    def location(self) -> str:
        """Get formatted location string."""
        if self.file_path:
            if self.line_number:
                return f"{self.file_path}:{self.line_number}"
            return self.file_path
        return ""

    @property
    def priority_icon(self) -> str:
        """Get icon for priority/category."""
        icons = {
            Category.SECURITY: "🔒",
            Category.PERFORMANCE: "⚡",
            Category.QUALITY: "🧹",
        }
        return icons.get(self.category, "💡")


# =============================================================================
# SUGGESTION ENGINE
# =============================================================================

class SuggestionEngine:
    """
    Engine for generating and managing proactive suggestions.

    Converts detected findings into prioritized, scored suggestions
    with learning-based personalization.
    """

    def __init__(self, memory_dir: Optional[Path] = None):
        """
        Initialize the suggestion engine.

        Args:
            memory_dir: Path to .project-memory directory.
                       If None, learning features are disabled.
        """
        self.memory_dir = Path(memory_dir) if memory_dir else None
        self._learning: Optional[LearningAnalyzer] = None
        self._suggestion_counter = 0

    @property
    def learning(self) -> Optional[LearningAnalyzer]:
        """Get learning analyzer (lazy load)."""
        if self._learning is None and self.memory_dir:
            self._learning = LearningAnalyzer(self.memory_dir)
        return self._learning

    def generate_suggestions(
        self,
        findings: List[Finding],
        context: Optional[Dict[str, Any]] = None,
        max_suggestions: int = MAX_SUGGESTIONS_DEFAULT,
    ) -> List[Suggestion]:
        """
        Generate suggestions from findings.

        Args:
            findings: List of detected findings.
            context: Current context for relevance scoring.
            max_suggestions: Maximum suggestions to return.

        Returns:
            List of suggestions sorted by priority and score.
        """
        context = context or {}
        suggestions = []

        for finding in findings:
            suggestion = self._finding_to_suggestion(finding)
            if suggestion:
                suggestions.append(suggestion)

        # Filter disabled suggestions
        suggestions = self.filter_disabled(suggestions)

        # Score suggestions
        suggestions = self.score_suggestions(suggestions, context)

        # Filter by minimum score
        threshold = MIN_SCORE_THRESHOLD
        if self.learning:
            prefs = self.learning.load_preferences()
            threshold = prefs.settings.get('suggestion_threshold', MIN_SCORE_THRESHOLD)

        suggestions = [s for s in suggestions if s.score >= threshold]

        # Sort by priority then score
        suggestions = self.sort_suggestions(suggestions)

        # Limit to max
        return suggestions[:max_suggestions]

    def _finding_to_suggestion(self, finding: Finding) -> Optional[Suggestion]:
        """
        Convert a finding to a suggestion.

        Args:
            finding: The finding to convert.

        Returns:
            Suggestion or None if pattern not found.
        """
        pattern = get_pattern(finding.pattern_id)
        if not pattern:
            # Unknown pattern - create generic suggestion
            return self._create_generic_suggestion(finding)

        self._suggestion_counter += 1
        suggestion_id = f"sug-{self._suggestion_counter:04d}"

        return Suggestion(
            id=suggestion_id,
            pattern_id=finding.pattern_id,
            priority=pattern.priority,
            category=pattern.category,
            title=pattern.name,
            description=finding.message or pattern.description,
            suggestion_text=pattern.suggestion,
            file_path=finding.file_path,
            line_number=finding.line_number,
            auto_fixable=pattern.auto_fixable,
            source=finding.source,
        )

    def _create_generic_suggestion(self, finding: Finding) -> Suggestion:
        """Create a generic suggestion for unknown patterns."""
        self._suggestion_counter += 1
        suggestion_id = f"sug-{self._suggestion_counter:04d}"

        # Infer priority from severity
        severity_to_priority = {
            "critical": Priority.P1,
            "important": Priority.P2,
            "moderate": Priority.P2,
            "minor": Priority.P3,
        }
        priority = severity_to_priority.get(finding.severity, Priority.P3)

        # Infer category from source
        source_to_category = {
            "security-auditor": Category.SECURITY,
            "code-reviewer": Category.QUALITY,
            "qa-reviewer": Category.QUALITY,
            "detector": Category.QUALITY,
        }
        category = source_to_category.get(finding.source, Category.QUALITY)

        return Suggestion(
            id=suggestion_id,
            pattern_id=finding.pattern_id,
            priority=priority,
            category=category,
            title=finding.pattern_id.replace("-", " ").title(),
            description=finding.message,
            suggestion_text="Review and address this issue",
            file_path=finding.file_path,
            line_number=finding.line_number,
            source=finding.source,
        )

    def filter_disabled(self, suggestions: List[Suggestion]) -> List[Suggestion]:
        """
        Filter out disabled suggestions.

        Args:
            suggestions: List of suggestions.

        Returns:
            Filtered list without disabled patterns.
        """
        if not self.learning:
            return suggestions

        prefs = self.learning.load_preferences()
        disabled = set(prefs.disabled_suggestions)

        return [s for s in suggestions if s.pattern_id not in disabled]

    def score_suggestions(
        self,
        suggestions: List[Suggestion],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Suggestion]:
        """
        Calculate scores for suggestions.

        Uses the CDC formula:
        score = base_score * impact_multiplier * preference_multiplier

        Args:
            suggestions: List of suggestions.
            context: Current context for relevance.

        Returns:
            Suggestions with updated scores.
        """
        context = context or {}

        for suggestion in suggestions:
            # Base score from priority
            base_score = PRIORITY_WEIGHTS.get(suggestion.priority, 50) / 100.0

            # Impact multiplier from severity (inferred from pattern)
            pattern = get_pattern(suggestion.pattern_id)
            severity = pattern.severity if pattern else "minor"
            impact = IMPACT_MULTIPLIERS.get(severity, 1.0)

            # Learning-based preference multiplier
            if self.learning:
                learning_score = self.learning.get_suggestion_score(
                    suggestion.pattern_id, context
                ) or 0.5  # Default if None
                # Blend base score with learning score
                preference = 0.5 + (learning_score * 0.5)  # Range: 0.5 to 1.0
            else:
                preference = 1.0

            # Final score
            suggestion.score = base_score * impact * preference

        return suggestions

    def sort_suggestions(self, suggestions: List[Suggestion]) -> List[Suggestion]:
        """
        Sort suggestions by priority then score.

        P1 always before P2 before P3, then by score descending.

        Args:
            suggestions: List of suggestions.

        Returns:
            Sorted list.
        """
        return sorted(
            suggestions,
            key=lambda s: (s.priority.value, -s.score)
        )

    def record_feedback(
        self,
        suggestion_id: str,
        pattern_id: str,
        action: str,
    ) -> bool:
        """
        Record user feedback on a suggestion.

        Args:
            suggestion_id: Suggestion ID (for logging).
            pattern_id: Pattern ID (for learning).
            action: "accepted", "rejected", "ignored", or "disabled"

        Returns:
            True if recorded successfully.
        """
        if not self.learning:
            return False

        return self.learning.record_feedback(pattern_id, action)

    def get_ignored_session_patterns(self) -> set:
        """
        Get patterns ignored in current session.

        Returns:
            Set of pattern IDs ignored this session.
        """
        # Session-level ignores (not persisted)
        if not hasattr(self, '_session_ignored'):
            self._session_ignored = set()
        return self._session_ignored

    def ignore_for_session(self, pattern_id: str) -> None:
        """
        Ignore a pattern for the current session only.

        Args:
            pattern_id: Pattern to ignore.
        """
        self.get_ignored_session_patterns().add(pattern_id)

    def format_for_breakpoint(
        self,
        suggestions: List[Suggestion],
        compact: bool = False,
    ) -> str:
        """
        Format suggestions for breakpoint display.

        Args:
            suggestions: List of suggestions to display.
            compact: Use compact format (for token optimization).

        Returns:
            Formatted string for breakpoint.
        """
        if not suggestions:
            return ""

        if compact:
            return self._format_compact(suggestions)
        return self._format_full(suggestions)

    def _format_full(self, suggestions: List[Suggestion]) -> str:
        """Full format for breakpoint."""
        lines = [
            "│ 💡 SUGGESTIONS PROACTIVES                                          │",
        ]

        for i, sug in enumerate(suggestions[:5]):
            prefix = "├──" if i < len(suggestions) - 1 else "└──"
            lines.append(
                f"│ {prefix} [{sug.priority.name}] {sug.priority_icon} {sug.title}"
            )
            if sug.location:
                lines.append(f"│     └── {sug.location}")

        if suggestions:
            lines.append(
                "│     └── Actions: [Accepter tout] [Voir détails] [Ignorer]         │"
            )

        return "\n".join(lines)

    def _format_compact(self, suggestions: List[Suggestion]) -> str:
        """Compact format for token optimization."""
        items = []
        for sug in suggestions[:3]:
            loc = f" ({sug.file_path})" if sug.file_path else ""
            items.append(f"[{sug.priority.name}] {sug.priority_icon} {sug.title}{loc}")

        return "💡 Suggestions: " + " | ".join(items)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def findings_from_subagent(
    subagent: str,
    findings_data: List[Dict[str, Any]],
) -> List[Finding]:
    """
    Convert subagent findings to Finding objects.

    Args:
        subagent: Subagent name (code-reviewer, security-auditor, qa-reviewer).
        findings_data: List of finding dictionaries from subagent.

    Returns:
        List of Finding objects.
    """
    findings = []
    for data in findings_data:
        finding = Finding(
            pattern_id=data.get('pattern_id', data.get('type', 'unknown')),
            file_path=data.get('file', data.get('file_path', '')),
            line_number=data.get('line', data.get('line_number')),
            message=data.get('message', data.get('description', '')),
            severity=data.get('severity', 'minor'),
            context=data.get('context', {}),
            source=subagent,
        )
        findings.append(finding)

    return findings


def merge_findings(
    *finding_lists: List[Finding],
) -> List[Finding]:
    """
    Merge multiple finding lists, deduplicating by pattern+file.

    Args:
        finding_lists: Variable number of finding lists.

    Returns:
        Merged and deduplicated list.
    """
    seen = set()
    merged = []

    for findings in finding_lists:
        for finding in findings:
            key = (finding.pattern_id, finding.file_path, finding.line_number)
            if key not in seen:
                seen.add(key)
                merged.append(finding)

    return merged


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'Finding',
    'Suggestion',
    'SuggestionEngine',
    'findings_from_subagent',
    'merge_findings',
    'MAX_SUGGESTIONS_DEFAULT',
    'PRIORITY_WEIGHTS',
]
