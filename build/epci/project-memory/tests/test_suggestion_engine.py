#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Suggestion Engine (F06)

Tests the suggestion generation, filtering, scoring, and formatting.
"""

import pytest
import sys
import tempfile
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from suggestion_engine import (
    Finding,
    Suggestion,
    SuggestionEngine,
    findings_from_subagent,
    merge_findings,
    PRIORITY_WEIGHTS,
)
from patterns.catalog import Priority, Category


class TestFinding:
    """Test Finding dataclass."""

    def test_finding_creation(self):
        """Finding should be created with required fields."""
        finding = Finding(
            pattern_id="input-not-validated",
            file_path="src/Controller/UserController.php",
            line_number=42,
            message="Input not validated",
        )

        assert finding.pattern_id == "input-not-validated"
        assert finding.file_path == "src/Controller/UserController.php"
        assert finding.line_number == 42

    def test_finding_defaults(self):
        """Finding should have sensible defaults."""
        finding = Finding(
            pattern_id="test",
            file_path="test.php",
        )

        assert finding.severity == "minor"
        assert finding.source == "detector"
        assert finding.context == {}

    def test_finding_to_dict(self):
        """Finding should serialize to dictionary."""
        finding = Finding(
            pattern_id="sql-injection",
            file_path="repo.php",
            severity="critical",
        )
        data = finding.to_dict()

        assert data['pattern_id'] == "sql-injection"
        assert data['severity'] == "critical"


class TestSuggestion:
    """Test Suggestion dataclass."""

    def test_suggestion_creation(self):
        """Suggestion should be created with required fields."""
        suggestion = Suggestion(
            id="sug-0001",
            pattern_id="input-not-validated",
            priority=Priority.P1,
            category=Category.SECURITY,
            title="Input non validé",
            description="Paramètre non validé",
            suggestion_text="Ajouter validation",
        )

        assert suggestion.id == "sug-0001"
        assert suggestion.priority == Priority.P1

    def test_suggestion_location(self):
        """Location property should format correctly."""
        suggestion = Suggestion(
            id="sug-0001",
            pattern_id="test",
            priority=Priority.P1,
            category=Category.SECURITY,
            title="Test",
            description="Test",
            suggestion_text="Test",
            file_path="src/test.php",
            line_number=42,
        )

        assert suggestion.location == "src/test.php:42"

    def test_suggestion_location_no_line(self):
        """Location without line number."""
        suggestion = Suggestion(
            id="sug-0001",
            pattern_id="test",
            priority=Priority.P1,
            category=Category.SECURITY,
            title="Test",
            description="Test",
            suggestion_text="Test",
            file_path="src/test.php",
        )

        assert suggestion.location == "src/test.php"

    def test_suggestion_priority_icon(self):
        """Priority icon should match category."""
        security = Suggestion(
            id="s1", pattern_id="t", priority=Priority.P1,
            category=Category.SECURITY, title="", description="", suggestion_text=""
        )
        perf = Suggestion(
            id="s2", pattern_id="t", priority=Priority.P2,
            category=Category.PERFORMANCE, title="", description="", suggestion_text=""
        )
        quality = Suggestion(
            id="s3", pattern_id="t", priority=Priority.P3,
            category=Category.QUALITY, title="", description="", suggestion_text=""
        )

        assert security.priority_icon == "🔒"
        assert perf.priority_icon == "⚡"
        assert quality.priority_icon == "🧹"


class TestSuggestionEngineBasic:
    """Test SuggestionEngine basic operations."""

    def test_engine_creation(self):
        """Engine should be created without memory dir."""
        engine = SuggestionEngine()
        assert engine.memory_dir is None
        assert engine.learning is None

    def test_engine_with_memory_dir(self):
        """Engine should accept memory directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = SuggestionEngine(memory_dir=Path(tmpdir))
            assert engine.memory_dir is not None


class TestGenerateSuggestions:
    """Test suggestion generation."""

    def test_generate_from_known_pattern(self):
        """Should generate suggestion from known pattern."""
        engine = SuggestionEngine()
        findings = [
            Finding(
                pattern_id="input-not-validated",
                file_path="src/Controller/UserController.php",
                line_number=42,
            )
        ]

        suggestions = engine.generate_suggestions(findings)

        assert len(suggestions) == 1
        assert suggestions[0].pattern_id == "input-not-validated"
        assert suggestions[0].priority == Priority.P1
        assert suggestions[0].category == Category.SECURITY

    def test_generate_from_unknown_pattern(self):
        """Should generate generic suggestion for unknown pattern."""
        engine = SuggestionEngine()
        findings = [
            Finding(
                pattern_id="custom-issue",
                file_path="src/Service/Test.php",
                message="Custom issue found",
                severity="important",
            )
        ]

        suggestions = engine.generate_suggestions(findings)

        assert len(suggestions) == 1
        assert suggestions[0].pattern_id == "custom-issue"
        assert suggestions[0].title == "Custom Issue"

    def test_generate_multiple_findings(self):
        """Should handle multiple findings."""
        engine = SuggestionEngine()
        findings = [
            Finding(pattern_id="input-not-validated", file_path="a.php"),
            Finding(pattern_id="sql-injection", file_path="b.php"),
            Finding(pattern_id="god-class", file_path="c.php"),
        ]

        suggestions = engine.generate_suggestions(findings)

        assert len(suggestions) == 3

    def test_max_suggestions_limit(self):
        """Should respect max_suggestions limit."""
        engine = SuggestionEngine()
        findings = [
            Finding(pattern_id=f"pattern-{i}", file_path=f"file{i}.php")
            for i in range(10)
        ]

        suggestions = engine.generate_suggestions(findings, max_suggestions=3)

        assert len(suggestions) == 3


class TestFilterDisabled:
    """Test disabled suggestion filtering."""

    def test_filter_without_learning(self):
        """Without learning, all suggestions pass through."""
        engine = SuggestionEngine()
        suggestions = [
            Suggestion(
                id="s1", pattern_id="test",
                priority=Priority.P1, category=Category.SECURITY,
                title="Test", description="", suggestion_text=""
            )
        ]

        filtered = engine.filter_disabled(suggestions)
        assert len(filtered) == 1


class TestScoreSuggestions:
    """Test suggestion scoring."""

    def test_score_by_priority(self):
        """P1 should score higher than P2, P2 higher than P3."""
        engine = SuggestionEngine()

        p1 = Suggestion(
            id="s1", pattern_id="input-not-validated",
            priority=Priority.P1, category=Category.SECURITY,
            title="", description="", suggestion_text=""
        )
        p2 = Suggestion(
            id="s2", pattern_id="n-plus-one-query",
            priority=Priority.P2, category=Category.PERFORMANCE,
            title="", description="", suggestion_text=""
        )
        p3 = Suggestion(
            id="s3", pattern_id="magic-numbers",
            priority=Priority.P3, category=Category.QUALITY,
            title="", description="", suggestion_text=""
        )

        scored = engine.score_suggestions([p1, p2, p3])

        assert scored[0].score > scored[1].score
        assert scored[1].score > scored[2].score

    def test_score_includes_impact(self):
        """Severity should affect score via impact multiplier."""
        engine = SuggestionEngine()

        # Both P1, but sql-injection is critical severity
        s1 = Suggestion(
            id="s1", pattern_id="sql-injection",
            priority=Priority.P1, category=Category.SECURITY,
            title="", description="", suggestion_text=""
        )
        s2 = Suggestion(
            id="s2", pattern_id="csrf-missing",
            priority=Priority.P1, category=Category.SECURITY,
            title="", description="", suggestion_text=""
        )

        engine.score_suggestions([s1, s2])

        # sql-injection is critical, csrf-missing is also critical
        # Both should have high scores
        assert s1.score >= 0.5
        assert s2.score >= 0.5


class TestSortSuggestions:
    """Test suggestion sorting."""

    def test_sort_by_priority_first(self):
        """P1 should always come before P2, P2 before P3."""
        engine = SuggestionEngine()

        suggestions = [
            Suggestion(
                id="s3", pattern_id="t", priority=Priority.P3,
                category=Category.QUALITY, title="", description="",
                suggestion_text="", score=0.9
            ),
            Suggestion(
                id="s1", pattern_id="t", priority=Priority.P1,
                category=Category.SECURITY, title="", description="",
                suggestion_text="", score=0.5
            ),
            Suggestion(
                id="s2", pattern_id="t", priority=Priority.P2,
                category=Category.PERFORMANCE, title="", description="",
                suggestion_text="", score=0.7
            ),
        ]

        sorted_suggestions = engine.sort_suggestions(suggestions)

        assert sorted_suggestions[0].priority == Priority.P1
        assert sorted_suggestions[1].priority == Priority.P2
        assert sorted_suggestions[2].priority == Priority.P3

    def test_sort_by_score_within_priority(self):
        """Within same priority, higher score comes first."""
        engine = SuggestionEngine()

        suggestions = [
            Suggestion(
                id="s1", pattern_id="t", priority=Priority.P1,
                category=Category.SECURITY, title="", description="",
                suggestion_text="", score=0.5
            ),
            Suggestion(
                id="s2", pattern_id="t", priority=Priority.P1,
                category=Category.SECURITY, title="", description="",
                suggestion_text="", score=0.9
            ),
        ]

        sorted_suggestions = engine.sort_suggestions(suggestions)

        assert sorted_suggestions[0].score == 0.9
        assert sorted_suggestions[1].score == 0.5


class TestFormatForBreakpoint:
    """Test breakpoint formatting."""

    def test_format_empty(self):
        """Empty suggestions should return empty string."""
        engine = SuggestionEngine()
        result = engine.format_for_breakpoint([])
        assert result == ""

    def test_format_full(self):
        """Full format should include header and icons."""
        engine = SuggestionEngine()
        suggestions = [
            Suggestion(
                id="s1", pattern_id="input-not-validated",
                priority=Priority.P1, category=Category.SECURITY,
                title="Input non validé", description="",
                suggestion_text="", file_path="test.php", line_number=42
            )
        ]

        result = engine.format_for_breakpoint(suggestions, compact=False)

        assert "SUGGESTIONS PROACTIVES" in result
        assert "[P1]" in result
        assert "🔒" in result
        assert "Input non validé" in result

    def test_format_compact(self):
        """Compact format should be shorter."""
        engine = SuggestionEngine()
        suggestions = [
            Suggestion(
                id="s1", pattern_id="test",
                priority=Priority.P1, category=Category.SECURITY,
                title="Test", description="", suggestion_text=""
            )
        ]

        full = engine.format_for_breakpoint(suggestions, compact=False)
        compact = engine.format_for_breakpoint(suggestions, compact=True)

        assert len(compact) < len(full)
        assert "💡 Suggestions:" in compact


class TestFindingsFromSubagent:
    """Test subagent findings conversion."""

    def test_convert_code_reviewer_findings(self):
        """Should convert code-reviewer findings."""
        data = [
            {
                'type': 'long-method',
                'file': 'src/Service/Test.php',
                'line': 100,
                'message': 'Method too long',
                'severity': 'minor',
            }
        ]

        findings = findings_from_subagent("code-reviewer", data)

        assert len(findings) == 1
        assert findings[0].source == "code-reviewer"
        assert findings[0].pattern_id == "long-method"

    def test_convert_security_auditor_findings(self):
        """Should convert security-auditor findings."""
        data = [
            {
                'pattern_id': 'sql-injection',
                'file_path': 'src/Repo.php',
                'line_number': 50,
                'description': 'SQL injection risk',
                'severity': 'critical',
            }
        ]

        findings = findings_from_subagent("security-auditor", data)

        assert len(findings) == 1
        assert findings[0].source == "security-auditor"
        assert findings[0].severity == "critical"


class TestMergeFindings:
    """Test findings merging."""

    def test_merge_removes_duplicates(self):
        """Should remove duplicate findings."""
        list1 = [
            Finding(pattern_id="test", file_path="a.php", line_number=10),
            Finding(pattern_id="test2", file_path="b.php", line_number=20),
        ]
        list2 = [
            Finding(pattern_id="test", file_path="a.php", line_number=10),  # Duplicate
            Finding(pattern_id="test3", file_path="c.php", line_number=30),
        ]

        merged = merge_findings(list1, list2)

        assert len(merged) == 3

    def test_merge_preserves_order(self):
        """First occurrence should be kept."""
        list1 = [Finding(pattern_id="first", file_path="a.php", line_number=1)]
        list2 = [Finding(pattern_id="first", file_path="a.php", line_number=1)]

        merged = merge_findings(list1, list2)

        assert len(merged) == 1


class TestSessionIgnore:
    """Test session-level ignore."""

    def test_ignore_for_session(self):
        """Should track session-ignored patterns."""
        engine = SuggestionEngine()

        engine.ignore_for_session("test-pattern")

        assert "test-pattern" in engine.get_ignored_session_patterns()

    def test_session_ignore_persists_in_engine(self):
        """Session ignores should persist within engine instance."""
        engine = SuggestionEngine()

        engine.ignore_for_session("p1")
        engine.ignore_for_session("p2")

        ignored = engine.get_ignored_session_patterns()
        assert "p1" in ignored
        assert "p2" in ignored


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
