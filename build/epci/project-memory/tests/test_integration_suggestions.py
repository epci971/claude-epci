#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests for Proactive Suggestions (F06)

End-to-end tests for the complete suggestion pipeline.
"""

import pytest
import sys
import tempfile
import json
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from patterns.catalog import (
    PATTERN_CATALOG,
    get_pattern,
    get_patterns_by_priority,
    get_catalog_stats,
    Priority,
    Category,
)
from suggestion_engine import (
    SuggestionEngine,
    Finding,
    Suggestion,
    findings_from_subagent,
    merge_findings,
)
from detector import PatternDetector, PatternFinding


class TestEndToEndPipeline:
    """Test the complete suggestion pipeline."""

    def test_detector_to_engine_pipeline(self):
        """Test flow from PatternDetector to SuggestionEngine."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file with issues
            test_file = Path(tmpdir) / "controller.php"
            test_file.write_text('''<?php
class UserController {
    public function create() {
        $email = $_GET['email'];
        $repo->findAll();
        return $x * 42;
    }
}
''')

            # Run pattern detection
            detector = PatternDetector(Path(tmpdir))
            pattern_findings = detector.detect_all([test_file])

            # Convert to suggestions
            engine = SuggestionEngine()
            findings = [
                Finding(
                    pattern_id=pf.pattern_id,
                    file_path=pf.file_path,
                    line_number=pf.line_number,
                    message=pf.message,
                    severity=pf.severity,
                )
                for pf in pattern_findings
            ]

            suggestions = engine.generate_suggestions(findings)

            # Verify pipeline produced results
            assert len(suggestions) >= 1

            # Verify prioritization (P1 before P2 before P3)
            priorities = [s.priority.value for s in suggestions]
            assert priorities == sorted(priorities)

    def test_subagent_findings_integration(self):
        """Test integration with subagent findings."""
        # Simulate code-reviewer findings
        code_reviewer_findings = [
            {
                'type': 'long-method',
                'file': 'src/Service.php',
                'line': 50,
                'message': 'Method exceeds 50 lines',
                'severity': 'minor',
            }
        ]

        # Simulate security-auditor findings
        security_findings = [
            {
                'pattern_id': 'sql-injection',
                'file_path': 'src/Repository.php',
                'line_number': 25,
                'description': 'SQL injection risk',
                'severity': 'critical',
            }
        ]

        # Convert and merge
        cr_findings = findings_from_subagent('code-reviewer', code_reviewer_findings)
        sa_findings = findings_from_subagent('security-auditor', security_findings)
        all_findings = merge_findings(cr_findings, sa_findings)

        # Generate suggestions
        engine = SuggestionEngine()
        suggestions = engine.generate_suggestions(all_findings)

        assert len(suggestions) == 2

        # P1 (security) should come first
        assert suggestions[0].priority == Priority.P1
        assert suggestions[0].source == 'security-auditor'


class TestLearningIntegration:
    """Test integration with learning system (F08)."""

    def test_suggestions_with_memory(self):
        """Test suggestions with project memory enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory_dir = Path(tmpdir) / '.project-memory'
            memory_dir.mkdir()
            (memory_dir / 'learning').mkdir()

            # Create preferences file
            preferences = {
                'version': '1.0.0',
                'suggestion_feedback': {},
                'disabled_suggestions': ['magic-numbers'],
                'preferred_patterns': [],
                'settings': {
                    'learning_enabled': True,
                    'suggestion_threshold': 0.3,
                    'max_suggestions_per_breakpoint': 5,
                },
            }
            (memory_dir / 'learning' / 'preferences.json').write_text(
                json.dumps(preferences)
            )

            # Create engine with memory
            engine = SuggestionEngine(memory_dir=memory_dir)

            findings = [
                Finding(pattern_id='magic-numbers', file_path='a.php'),  # Disabled
                Finding(pattern_id='input-not-validated', file_path='b.php'),  # Active
            ]

            suggestions = engine.generate_suggestions(findings)

            # magic-numbers should be filtered out
            assert len(suggestions) == 1
            assert suggestions[0].pattern_id == 'input-not-validated'

    def test_record_feedback(self):
        """Test feedback recording."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory_dir = Path(tmpdir) / '.project-memory'
            memory_dir.mkdir()
            (memory_dir / 'learning').mkdir()

            engine = SuggestionEngine(memory_dir=memory_dir)

            # Record some feedback
            engine.record_feedback('sug-001', 'input-not-validated', 'accepted')
            engine.record_feedback('sug-002', 'sql-injection', 'rejected')

            # Verify persistence
            prefs_file = memory_dir / 'learning' / 'preferences.json'
            assert prefs_file.exists()

            prefs = json.loads(prefs_file.read_text())
            assert 'input-not-validated' in prefs['suggestion_feedback']


class TestBreakpointFormatting:
    """Test breakpoint output formatting."""

    def test_full_format(self):
        """Test full breakpoint format."""
        engine = SuggestionEngine()

        suggestions = [
            Suggestion(
                id='s1',
                pattern_id='input-not-validated',
                priority=Priority.P1,
                category=Category.SECURITY,
                title='Input non validé',
                description='Test',
                suggestion_text='Add validation',
                file_path='controller.php',
                line_number=42,
            ),
            Suggestion(
                id='s2',
                pattern_id='n-plus-one-query',
                priority=Priority.P2,
                category=Category.PERFORMANCE,
                title='N+1 Query',
                description='Test',
                suggestion_text='Use JOIN',
                file_path='service.php',
            ),
        ]

        output = engine.format_for_breakpoint(suggestions, compact=False)

        assert 'SUGGESTIONS PROACTIVES' in output
        assert '[P1]' in output
        assert '🔒' in output
        assert 'Input non validé' in output
        assert '[P2]' in output
        assert '⚡' in output

    def test_compact_format(self):
        """Test compact breakpoint format."""
        engine = SuggestionEngine()

        suggestions = [
            Suggestion(
                id='s1',
                pattern_id='test',
                priority=Priority.P1,
                category=Category.SECURITY,
                title='Test Issue',
                description='',
                suggestion_text='',
            ),
        ]

        output = engine.format_for_breakpoint(suggestions, compact=True)

        assert '💡 Suggestions:' in output
        assert len(output) < 200  # Compact should be short


class TestCatalogCoverage:
    """Test pattern catalog coverage."""

    def test_minimum_patterns(self):
        """Catalog should have at least 14 patterns (CDC requirement)."""
        stats = get_catalog_stats()
        assert stats['total'] >= 14

    def test_security_coverage(self):
        """Should have 5 security patterns."""
        security = get_patterns_by_priority(Priority.P1)
        assert len(security) >= 5

    def test_all_categories_covered(self):
        """All categories should be covered."""
        stats = get_catalog_stats()
        assert stats['by_category']['security'] >= 5
        assert stats['by_category']['performance'] >= 4
        assert stats['by_category']['quality'] >= 5


class TestAcceptanceCriteria:
    """Test F06 acceptance criteria."""

    def test_ac2_priority_ordering(self):
        """F06-AC2: P1 before P2 before P3."""
        engine = SuggestionEngine()

        findings = [
            Finding(pattern_id='magic-numbers', file_path='a.php'),  # P3
            Finding(pattern_id='input-not-validated', file_path='b.php'),  # P1
            Finding(pattern_id='n-plus-one-query', file_path='c.php'),  # P2
        ]

        suggestions = engine.generate_suggestions(findings)

        assert suggestions[0].priority == Priority.P1
        assert suggestions[1].priority == Priority.P2
        assert suggestions[2].priority == Priority.P3

    def test_ac3_ignore_action(self):
        """F06-AC3: Ignore action works for session."""
        engine = SuggestionEngine()

        engine.ignore_for_session('test-pattern')
        ignored = engine.get_ignored_session_patterns()

        assert 'test-pattern' in ignored

    def test_ac7_catalog_complete(self):
        """F06-AC7: Catalog has 14+ patterns."""
        assert len(PATTERN_CATALOG) >= 14


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
