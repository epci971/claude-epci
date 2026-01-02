#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Learning Analyzer Module (F08)

Run with: pytest test_learning.py -v
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

import pytest

from ..learning_analyzer import (
    SuggestionFeedback,
    RecurringPattern,
    LearningPreferences,
    CorrectionsData,
    LearningAnalyzer,
    calculate_recency_factor,
    calculate_relevance_factor,
    calculate_suggestion_score,
    detect_recurring_patterns,
)


class TestRecencyFactor:
    """Tests for recency factor calculation."""

    def test_recency_recent(self):
        """Test recency for very recent timestamp."""
        now = datetime.utcnow().isoformat() + "Z"
        result = calculate_recency_factor(now)
        assert result > 0.99  # Should be very close to 1.0

    def test_recency_old(self):
        """Test recency for old timestamp."""
        old = (datetime.utcnow() - timedelta(days=60)).isoformat() + "Z"
        result = calculate_recency_factor(old, decay_days=30)
        assert result < 0.2  # Should be significantly decayed

    def test_recency_none(self):
        """Test recency with no timestamp."""
        result = calculate_recency_factor(None)
        assert result == 0.5  # Neutral

    def test_recency_invalid(self):
        """Test recency with invalid timestamp."""
        result = calculate_recency_factor("invalid-date")
        assert result == 0.5  # Neutral fallback

    def test_recency_at_decay_days(self):
        """Test recency at exactly decay_days."""
        old = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
        result = calculate_recency_factor(old, decay_days=30)
        # e^(-1) ≈ 0.368
        assert 0.3 < result < 0.4


class TestRelevanceFactor:
    """Tests for relevance factor calculation."""

    def test_relevance_default(self):
        """Test default relevance."""
        result = calculate_relevance_factor("some-pattern", {})
        assert result == 0.5

    def test_relevance_domain_match(self):
        """Test relevance with domain match."""
        result = calculate_relevance_factor(
            "input-validation",
            {"domain": "auth"}
        )
        assert result > 0.5

    def test_relevance_preferred_pattern(self):
        """Test relevance with preferred pattern."""
        result = calculate_relevance_factor(
            "repository-pattern",
            {},
            preferred_patterns=["repository-pattern"]
        )
        assert result > 0.7

    def test_relevance_capped(self):
        """Test relevance is capped at 1.0."""
        result = calculate_relevance_factor(
            "security-validation",
            {"domain": "auth", "file_types": ["auth"]},
            preferred_patterns=["security-validation"]
        )
        assert result <= 1.0


class TestSuggestionScore:
    """Tests for suggestion score calculation."""

    def test_score_disabled_pattern(self):
        """Test score is 0 for disabled pattern."""
        result = calculate_suggestion_score(
            pattern="nitpick",
            feedback=None,
            context={},
            disabled_patterns=["nitpick"]
        )
        assert result == 0.0

    def test_score_high_acceptance(self):
        """Test score with high acceptance rate."""
        feedback = SuggestionFeedback(
            accepted=9,
            rejected=1,
            acceptance_rate=0.9,
            last_seen=datetime.utcnow().isoformat() + "Z"
        )
        result = calculate_suggestion_score(
            pattern="test-coverage",
            feedback=feedback,
            context={"domain": "test"}
        )
        assert result > 0.5

    def test_score_no_feedback(self):
        """Test score with no prior feedback."""
        result = calculate_suggestion_score(
            pattern="new-pattern",
            feedback=None,
            context={}
        )
        # Uses defaults: 0.5 * 0.5 * 0.5 = 0.125
        assert 0.0 < result < 0.5

    def test_score_old_feedback(self):
        """Test score with old feedback decays."""
        feedback = SuggestionFeedback(
            accepted=5,
            rejected=0,
            acceptance_rate=1.0,
            last_seen=(datetime.utcnow() - timedelta(days=90)).isoformat() + "Z"
        )
        result = calculate_suggestion_score(
            pattern="old-pattern",
            feedback=feedback,
            context={}
        )
        # High acceptance but old, should decay
        assert result < 0.5


class TestPatternDetection:
    """Tests for recurring pattern detection."""

    def test_detect_no_patterns(self):
        """Test with no corrections."""
        result = detect_recurring_patterns([])
        assert result == []

    def test_detect_below_threshold(self):
        """Test patterns below threshold."""
        corrections = [
            {"pattern_id": "test-pattern", "type": "quality"},
            {"pattern_id": "test-pattern", "type": "quality"},
        ]
        result = detect_recurring_patterns(corrections, threshold=3)
        assert result == []

    def test_detect_at_threshold(self):
        """Test patterns at threshold."""
        corrections = [
            {"pattern_id": "input-validation", "type": "security", "severity": "important"},
            {"pattern_id": "input-validation", "type": "security", "severity": "important"},
            {"pattern_id": "input-validation", "type": "security", "severity": "important"},
        ]
        result = detect_recurring_patterns(corrections, threshold=3)
        assert len(result) == 1
        assert result[0].pattern_id == "input-validation"
        assert result[0].auto_suggest is True
        assert result[0].occurrences == 3

    def test_detect_multiple_patterns(self):
        """Test detecting multiple patterns."""
        corrections = [
            {"pattern_id": "pattern-a", "type": "quality"},
            {"pattern_id": "pattern-a", "type": "quality"},
            {"pattern_id": "pattern-a", "type": "quality"},
            {"pattern_id": "pattern-b", "type": "security"},
            {"pattern_id": "pattern-b", "type": "security"},
            {"pattern_id": "pattern-b", "type": "security"},
            {"pattern_id": "pattern-b", "type": "security"},
        ]
        result = detect_recurring_patterns(corrections, threshold=3)
        assert len(result) == 2
        # Should be sorted by occurrences (most first)
        assert result[0].pattern_id == "pattern-b"
        assert result[0].occurrences == 4


class TestSuggestionFeedback:
    """Tests for SuggestionFeedback dataclass."""

    def test_record_accepted(self):
        """Test recording accepted feedback."""
        feedback = SuggestionFeedback()
        feedback.record_feedback("accepted")

        assert feedback.accepted == 1
        assert feedback.rejected == 0
        assert feedback.acceptance_rate == 1.0
        assert feedback.last_action == "accepted"

    def test_record_rejected(self):
        """Test recording rejected feedback."""
        feedback = SuggestionFeedback()
        feedback.record_feedback("rejected")

        assert feedback.accepted == 0
        assert feedback.rejected == 1
        assert feedback.acceptance_rate == 0.0
        assert feedback.last_action == "rejected"

    def test_record_ignored(self):
        """Test recording ignored feedback."""
        feedback = SuggestionFeedback()
        feedback.record_feedback("ignored")

        assert feedback.accepted == 0
        assert feedback.rejected == 0
        assert feedback.acceptance_rate == 0.5  # Unchanged
        assert feedback.last_action == "ignored"

    def test_acceptance_rate_calculation(self):
        """Test acceptance rate is calculated correctly."""
        feedback = SuggestionFeedback()
        feedback.record_feedback("accepted")
        feedback.record_feedback("accepted")
        feedback.record_feedback("rejected")

        # 2 accepted / 3 total = 0.667
        assert abs(feedback.acceptance_rate - 0.667) < 0.01


class TestLearningPreferences:
    """Tests for LearningPreferences dataclass."""

    def test_from_dict_empty(self):
        """Test creating from empty dict."""
        prefs = LearningPreferences.from_dict({})
        assert prefs.version == "1.0.0"
        assert prefs.suggestion_feedback == {}
        assert prefs.disabled_suggestions == []

    def test_from_dict_with_feedback(self):
        """Test creating from dict with feedback."""
        data = {
            "suggestion_feedback": {
                "test-pattern": {"accepted": 5, "rejected": 1, "acceptance_rate": 0.83}
            }
        }
        prefs = LearningPreferences.from_dict(data)
        assert "test-pattern" in prefs.suggestion_feedback

    def test_to_dict_roundtrip(self):
        """Test to_dict produces valid JSON."""
        prefs = LearningPreferences()
        prefs.suggestion_feedback["test"] = SuggestionFeedback(accepted=3)

        result = prefs.to_dict()
        assert isinstance(result, dict)

        # Should be JSON serializable
        json_str = json.dumps(result)
        assert len(json_str) > 0


class TestLearningAnalyzer:
    """Tests for LearningAnalyzer."""

    @pytest.fixture
    def temp_memory_dir(self):
        """Create temporary memory directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory_dir = Path(tmpdir) / ".project-memory"
            (memory_dir / "learning").mkdir(parents=True)
            yield memory_dir

    def test_load_nonexistent(self, temp_memory_dir):
        """Test loading when files don't exist."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        prefs = analyzer.load_preferences()
        assert isinstance(prefs, LearningPreferences)

    def test_record_feedback(self, temp_memory_dir):
        """Test recording feedback."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        result = analyzer.record_feedback("test-pattern", "accepted")
        assert result is True

        # Verify persistence
        prefs = analyzer.load_preferences()
        assert "test-pattern" in prefs.suggestion_feedback

    def test_record_disabled(self, temp_memory_dir):
        """Test recording disabled pattern."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        analyzer.record_feedback("annoying-pattern", "disabled")

        prefs = analyzer.load_preferences()
        assert "annoying-pattern" in prefs.disabled_suggestions

    def test_record_correction(self, temp_memory_dir):
        """Test recording correction."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        correction = {
            "pattern_id": "input-validation",
            "type": "security",
            "severity": "important",
            "reason": "Missing input validation"
        }
        result = analyzer.record_correction(correction)
        assert result is True

        # Verify persistence
        data = analyzer.load_corrections()
        assert len(data.corrections) == 1

    def test_get_suggestion_score(self, temp_memory_dir):
        """Test getting suggestion score."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        analyzer.record_feedback("good-pattern", "accepted")
        analyzer.record_feedback("good-pattern", "accepted")

        score = analyzer.get_suggestion_score("good-pattern", {"domain": "test"})
        assert score > 0

    def test_get_recurring_patterns(self, temp_memory_dir):
        """Test getting recurring patterns."""
        analyzer = LearningAnalyzer(temp_memory_dir)

        # Record 3 corrections for same pattern
        for i in range(3):
            analyzer.record_correction({
                "pattern_id": "n1-query",
                "type": "performance"
            })

        patterns = analyzer.get_recurring_patterns()
        assert len(patterns) == 1
        assert patterns[0].pattern_id == "n1-query"

    def test_get_status(self, temp_memory_dir):
        """Test getting status."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        analyzer.record_feedback("pattern-1", "accepted")
        analyzer.record_correction({"pattern_id": "correction-1", "type": "quality"})

        status = analyzer.get_status()
        assert "patterns_tracked" in status
        assert "total_corrections" in status
        assert status["patterns_tracked"] == 1
        assert status["total_corrections"] == 1

    def test_reset(self, temp_memory_dir):
        """Test reset with backup."""
        analyzer = LearningAnalyzer(temp_memory_dir)
        analyzer.record_feedback("pattern", "accepted")
        analyzer.record_correction({"pattern_id": "corr", "type": "quality"})

        result = analyzer.reset(backup=True)
        assert result is True

        # Data should be cleared
        prefs = analyzer.load_preferences()
        assert prefs.suggestion_feedback == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
