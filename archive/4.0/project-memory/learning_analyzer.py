#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Learning Analyzer Module

Implements suggestion scoring and pattern detection for continuous learning.
Part of the F08 Continuous Learning feature.

Usage:
    from project_memory.learning_analyzer import LearningAnalyzer

    analyzer = LearningAnalyzer(memory_dir)
    score = analyzer.calculate_suggestion_score("pattern-extraction", context)
    patterns = analyzer.detect_recurring_patterns()
"""

import json
import math
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set


# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_VERSION = "1.0.0"
DEFAULT_ACCEPTANCE_RATE = 0.5  # Neutral default
RECENCY_DECAY_DAYS = 30  # Days for recency to decay to 50%
RECURRENCE_THRESHOLD = 3  # Minimum occurrences for auto-suggest
MIN_SCORE_THRESHOLD = 0.3  # Minimum score to show suggestion


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class SuggestionFeedback:
    """Feedback statistics for a suggestion pattern."""
    accepted: int = 0
    rejected: int = 0
    acceptance_rate: float = DEFAULT_ACCEPTANCE_RATE
    last_seen: Optional[str] = None
    last_action: Optional[str] = None  # "accepted", "rejected", "ignored"

    @classmethod
    def from_dict(cls, data: dict) -> 'SuggestionFeedback':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def record_feedback(self, action: str) -> None:
        """
        Record user feedback on a suggestion.

        Args:
            action: "accepted", "rejected", or "ignored"
        """
        self.last_action = action
        self.last_seen = datetime.utcnow().isoformat() + "Z"

        if action == "accepted":
            self.accepted += 1
        elif action == "rejected":
            self.rejected += 1
        # "ignored" doesn't change counts

        # Recalculate acceptance rate
        total = self.accepted + self.rejected
        if total > 0:
            self.acceptance_rate = self.accepted / total
        else:
            self.acceptance_rate = DEFAULT_ACCEPTANCE_RATE


@dataclass
class RecurringPattern:
    """A detected recurring pattern."""
    pattern_id: str
    occurrences: int
    auto_suggest: bool
    last_seen: Optional[str] = None
    severity: str = "minor"  # critical, important, minor
    category: str = "quality"  # security, performance, quality, test

    @classmethod
    def from_dict(cls, data: dict) -> 'RecurringPattern':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class LearningPreferences:
    """Complete learning preferences structure."""
    version: str = CURRENT_VERSION
    suggestion_feedback: Dict[str, SuggestionFeedback] = field(default_factory=dict)
    disabled_suggestions: List[str] = field(default_factory=list)
    preferred_patterns: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=lambda: {
        'learning_enabled': True,
        'suggestion_threshold': MIN_SCORE_THRESHOLD,
        'max_suggestions_per_breakpoint': 5,
    })
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'LearningPreferences':
        """Create from dictionary with nested object handling."""
        feedback = {}
        for key, value in data.get('suggestion_feedback', {}).items():
            if isinstance(value, dict):
                feedback[key] = SuggestionFeedback.from_dict(value)
            else:
                feedback[key] = value

        return cls(
            version=data.get('version', CURRENT_VERSION),
            suggestion_feedback=feedback,
            disabled_suggestions=data.get('disabled_suggestions', []),
            preferred_patterns=data.get('preferred_patterns', []),
            settings=data.get('settings', cls.__dataclass_fields__['settings'].default_factory()),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'suggestion_feedback': {
                k: v.to_dict() if isinstance(v, SuggestionFeedback) else v
                for k, v in self.suggestion_feedback.items()
            },
            'disabled_suggestions': self.disabled_suggestions,
            'preferred_patterns': self.preferred_patterns,
            'settings': self.settings,
            'updated_at': self.updated_at,
        }


@dataclass
class CorrectionsData:
    """Corrections history structure."""
    version: str = CURRENT_VERSION
    corrections: List[dict] = field(default_factory=list)
    patterns: Dict[str, RecurringPattern] = field(default_factory=dict)
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CorrectionsData':
        """Create from dictionary."""
        patterns = {}
        for key, value in data.get('patterns', {}).items():
            if isinstance(value, dict):
                patterns[key] = RecurringPattern.from_dict({'pattern_id': key, **value})

        return cls(
            version=data.get('version', CURRENT_VERSION),
            corrections=data.get('corrections', []),
            patterns=patterns,
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'corrections': self.corrections,
            'patterns': {
                k: {kk: vv for kk, vv in v.to_dict().items() if kk != 'pattern_id'}
                for k, v in self.patterns.items()
            },
            'updated_at': self.updated_at,
        }


# =============================================================================
# SCORING ALGORITHMS
# =============================================================================

def calculate_recency_factor(
    last_seen: Optional[str],
    decay_days: float = RECENCY_DECAY_DAYS
) -> float:
    """
    Calculate recency factor based on time since last seen.

    Uses exponential decay: factor = e^(-t/decay_days)
    Recent = 1.0, older approaches 0.

    Args:
        last_seen: ISO timestamp of last occurrence.
        decay_days: Days for factor to decay to ~37% (e^-1).

    Returns:
        Recency factor between 0 and 1.
    """
    if not last_seen:
        return 0.5  # Neutral for unknown

    try:
        # Parse ISO timestamp, handling various formats
        clean_ts = last_seen.replace('Z', '').replace('+00:00', '')
        # Handle microseconds if present
        if '.' in clean_ts:
            last_dt = datetime.fromisoformat(clean_ts)
        else:
            last_dt = datetime.fromisoformat(clean_ts)

        now = datetime.utcnow()
        days_ago = (now - last_dt).days

        if days_ago < 0:
            days_ago = 0

        # Exponential decay
        return math.exp(-days_ago / decay_days)
    except (ValueError, AttributeError, TypeError):
        return 0.5


def calculate_relevance_factor(
    pattern: str,
    context: dict,
    preferred_patterns: Optional[List[str]] = None
) -> float:
    """
    Calculate relevance factor based on current context.

    Considers:
    - Domain match (auth, api, ui, etc.)
    - File type match
    - User preferences

    Args:
        pattern: Pattern identifier.
        context: Current context with domain, file_types, etc.
        preferred_patterns: User's preferred patterns (boosted).

    Returns:
        Relevance factor between 0 and 1.
    """
    base_relevance = 0.5  # Neutral default

    # Domain relevance
    domain = context.get('domain', '').lower()
    pattern_lower = pattern.lower()

    domain_patterns = {
        'auth': ['security', 'validation', 'input', 'password', 'token'],
        'api': ['rest', 'endpoint', 'validation', 'serialization'],
        'ui': ['component', 'state', 'render', 'hook'],
        'data': ['repository', 'entity', 'query', 'n1'],
        'test': ['coverage', 'mock', 'assertion', 'fixture'],
    }

    for domain_key, patterns in domain_patterns.items():
        if domain_key in domain or domain_key in pattern_lower:
            if any(p in pattern_lower for p in patterns):
                base_relevance += 0.2
                break

    # File type relevance
    file_types = context.get('file_types', [])
    pattern_file_hints = {
        'test': ['test', 'spec'],
        'security': ['auth', 'login', 'password'],
        'performance': ['query', 'cache', 'index'],
    }

    for category, hints in pattern_file_hints.items():
        if category in pattern_lower:
            if any(hint in str(file_types).lower() for hint in hints):
                base_relevance += 0.1

    # User preference boost
    if preferred_patterns and pattern in preferred_patterns:
        base_relevance += 0.3

    return min(1.0, max(0.0, base_relevance))


def calculate_suggestion_score(
    pattern: str,
    feedback: Optional[SuggestionFeedback],
    context: dict,
    preferred_patterns: Optional[List[str]] = None,
    disabled_patterns: Optional[List[str]] = None
) -> float:
    """
    Calculate overall suggestion score.

    Formula: acceptance_rate * recency_factor * relevance_factor

    Args:
        pattern: Pattern identifier.
        feedback: Historical feedback for this pattern.
        context: Current context.
        preferred_patterns: User's preferred patterns.
        disabled_patterns: User's disabled patterns.

    Returns:
        Score between 0 and 1.
    """
    # Disabled patterns always score 0
    if disabled_patterns and pattern in disabled_patterns:
        return 0.0

    # Get acceptance rate
    if feedback:
        acceptance_rate = feedback.acceptance_rate
        last_seen = feedback.last_seen
    else:
        acceptance_rate = DEFAULT_ACCEPTANCE_RATE
        last_seen = None

    # Calculate factors
    recency = calculate_recency_factor(last_seen)
    relevance = calculate_relevance_factor(pattern, context, preferred_patterns)

    # Combined score
    score = acceptance_rate * recency * relevance

    return score


def detect_recurring_patterns(
    corrections: List[dict],
    threshold: int = RECURRENCE_THRESHOLD
) -> List[RecurringPattern]:
    """
    Detect patterns that occur frequently enough to auto-suggest.

    Args:
        corrections: List of correction records.
        threshold: Minimum occurrences to flag as recurring.

    Returns:
        List of recurring patterns.
    """
    pattern_counts: Dict[str, dict] = {}

    for correction in corrections:
        pattern_id = correction.get('pattern_id')
        if not pattern_id:
            continue

        if pattern_id not in pattern_counts:
            pattern_counts[pattern_id] = {
                'count': 0,
                'last_seen': None,
                'severity': correction.get('severity', 'minor'),
                'type': correction.get('type', 'quality'),
            }

        pattern_counts[pattern_id]['count'] += 1
        timestamp = correction.get('timestamp')
        if timestamp:
            current_last = pattern_counts[pattern_id]['last_seen']
            if not current_last or timestamp > current_last:
                pattern_counts[pattern_id]['last_seen'] = timestamp

    # Filter by threshold and create RecurringPattern objects
    recurring = []
    for pattern_id, data in pattern_counts.items():
        if data['count'] >= threshold:
            recurring.append(RecurringPattern(
                pattern_id=pattern_id,
                occurrences=data['count'],
                auto_suggest=True,
                last_seen=data['last_seen'],
                severity=data['severity'],
                category=data['type'],
            ))

    # Sort by occurrences (most frequent first)
    recurring.sort(key=lambda x: x.occurrences, reverse=True)

    return recurring


# =============================================================================
# LEARNING ANALYZER
# =============================================================================

class LearningAnalyzer:
    """
    Analyzes learning data to provide improved suggestions.

    Handles preference tracking, pattern detection, and scoring.
    """

    def __init__(self, memory_dir: Path):
        """
        Initialize the learning analyzer.

        Args:
            memory_dir: Path to .project-memory directory.
        """
        self.memory_dir = Path(memory_dir)
        self.preferences_file = self.memory_dir / "learning" / "preferences.json"
        self.corrections_file = self.memory_dir / "learning" / "corrections.json"
        self._preferences: Optional[LearningPreferences] = None
        self._corrections: Optional[CorrectionsData] = None

    def load_preferences(self) -> LearningPreferences:
        """Load learning preferences from file."""
        if self._preferences is not None:
            return self._preferences

        if not self.preferences_file.exists():
            self._preferences = LearningPreferences()
            return self._preferences

        try:
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._preferences = LearningPreferences.from_dict(data)
            return self._preferences
        except (json.JSONDecodeError, Exception):
            self._preferences = LearningPreferences()
            return self._preferences

    def save_preferences(self) -> bool:
        """Save learning preferences to file."""
        if self._preferences is None:
            return True

        try:
            self._preferences.updated_at = datetime.utcnow().isoformat() + "Z"
            self.preferences_file.parent.mkdir(parents=True, exist_ok=True)

            temp_file = self.preferences_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._preferences.to_dict(), f, indent=2, ensure_ascii=False)

            temp_file.replace(self.preferences_file)
            return True
        except Exception:
            return False

    def load_corrections(self) -> CorrectionsData:
        """Load corrections history from file."""
        if self._corrections is not None:
            return self._corrections

        if not self.corrections_file.exists():
            self._corrections = CorrectionsData()
            return self._corrections

        try:
            with open(self.corrections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._corrections = CorrectionsData.from_dict(data)
            return self._corrections
        except (json.JSONDecodeError, Exception):
            self._corrections = CorrectionsData()
            return self._corrections

    def save_corrections(self) -> bool:
        """Save corrections to file."""
        if self._corrections is None:
            return True

        try:
            self._corrections.updated_at = datetime.utcnow().isoformat() + "Z"
            self.corrections_file.parent.mkdir(parents=True, exist_ok=True)

            temp_file = self.corrections_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._corrections.to_dict(), f, indent=2, ensure_ascii=False)

            temp_file.replace(self.corrections_file)
            return True
        except Exception:
            return False

    def record_feedback(self, pattern: str, action: str) -> bool:
        """
        Record user feedback on a suggestion.

        Args:
            pattern: Pattern identifier.
            action: "accepted", "rejected", "ignored", or "disabled"

        Returns:
            True if recorded successfully.
        """
        prefs = self.load_preferences()

        if action == "disabled":
            # Add to disabled list
            if pattern not in prefs.disabled_suggestions:
                prefs.disabled_suggestions.append(pattern)
            return self.save_preferences()

        # Get or create feedback entry
        if pattern not in prefs.suggestion_feedback:
            prefs.suggestion_feedback[pattern] = SuggestionFeedback()

        # Ensure we have a proper SuggestionFeedback object (not dict)
        current_feedback = prefs.suggestion_feedback[pattern]
        if isinstance(current_feedback, dict):
            # Convert dict to SuggestionFeedback and store back
            current_feedback = SuggestionFeedback.from_dict(current_feedback)

        # Record the feedback action
        current_feedback.record_feedback(action)

        # Always assign back to ensure consistency
        prefs.suggestion_feedback[pattern] = current_feedback
        return self.save_preferences()

    def record_correction(self, correction: dict) -> bool:
        """
        Record a correction for pattern detection.

        Args:
            correction: Correction data with pattern_id, type, severity, etc.

        Returns:
            True if recorded successfully.
        """
        data = self.load_corrections()

        # Add correction to list
        correction['timestamp'] = correction.get('timestamp', datetime.utcnow().isoformat() + "Z")
        correction['id'] = correction.get('id', f"corr-{len(data.corrections) + 1:04d}")
        data.corrections.append(correction)

        # Update pattern stats
        pattern_id = correction.get('pattern_id')
        if pattern_id:
            if pattern_id not in data.patterns:
                data.patterns[pattern_id] = RecurringPattern(
                    pattern_id=pattern_id,
                    occurrences=0,
                    auto_suggest=False,
                    severity=correction.get('severity', 'minor'),
                    category=correction.get('type', 'quality'),
                )

            pattern = data.patterns[pattern_id]
            pattern.occurrences += 1
            pattern.last_seen = correction['timestamp']
            pattern.auto_suggest = pattern.occurrences >= RECURRENCE_THRESHOLD

        return self.save_corrections()

    def get_suggestion_score(self, pattern: str, context: dict) -> float:
        """
        Get the score for a suggestion pattern.

        Args:
            pattern: Pattern identifier.
            context: Current context.

        Returns:
            Score between 0 and 1.
        """
        prefs = self.load_preferences()

        feedback = prefs.suggestion_feedback.get(pattern)
        if isinstance(feedback, dict):
            feedback = SuggestionFeedback.from_dict(feedback)

        return calculate_suggestion_score(
            pattern=pattern,
            feedback=feedback,
            context=context,
            preferred_patterns=prefs.preferred_patterns,
            disabled_patterns=prefs.disabled_suggestions,
        )

    def get_recurring_patterns(self) -> List[RecurringPattern]:
        """
        Get all recurring patterns that should be auto-suggested.

        Returns:
            List of RecurringPattern objects.
        """
        data = self.load_corrections()
        return detect_recurring_patterns(data.corrections)

    def get_status(self) -> dict:
        """
        Get current learning status for display.

        Returns:
            Dictionary with status information.
        """
        prefs = self.load_preferences()
        corrections = self.load_corrections()
        recurring = self.get_recurring_patterns()

        # Calculate top patterns by acceptance
        top_patterns = sorted(
            [
                (k, v.acceptance_rate if isinstance(v, SuggestionFeedback) else v.get('acceptance_rate', 0.5))
                for k, v in prefs.suggestion_feedback.items()
            ],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'learning_enabled': prefs.settings.get('learning_enabled', True),
            'patterns_tracked': len(prefs.suggestion_feedback),
            'disabled_patterns': len(prefs.disabled_suggestions),
            'preferred_patterns': len(prefs.preferred_patterns),
            'total_corrections': len(corrections.corrections),
            'recurring_patterns': len(recurring),
            'top_patterns': [
                {'pattern': p[0], 'acceptance_rate': f"{p[1]:.0%}"}
                for p in top_patterns
            ],
            'last_updated': prefs.updated_at,
        }

    def reset(self, backup: bool = True) -> bool:
        """
        Reset learning data.

        Args:
            backup: Whether to create backups before reset.

        Returns:
            True if reset successful.
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Backup and reset preferences
        if backup and self.preferences_file.exists():
            backup_path = self.preferences_file.with_suffix(f'.backup-{timestamp}.json')
            try:
                self.preferences_file.rename(backup_path)
            except Exception:
                pass

        # Backup and reset corrections
        if backup and self.corrections_file.exists():
            backup_path = self.corrections_file.with_suffix(f'.backup-{timestamp}.json')
            try:
                self.corrections_file.rename(backup_path)
            except Exception:
                pass

        self._preferences = LearningPreferences()
        self._corrections = CorrectionsData()

        return self.save_preferences() and self.save_corrections()


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'SuggestionFeedback',
    'RecurringPattern',
    'LearningPreferences',
    'CorrectionsData',
    'LearningAnalyzer',
    'calculate_recency_factor',
    'calculate_relevance_factor',
    'calculate_suggestion_score',
    'detect_recurring_patterns',
]
