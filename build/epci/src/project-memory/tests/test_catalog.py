#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Pattern Catalog (F06)

Tests the pattern registry, retrieval, and sorting functions.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from patterns.catalog import (
    PATTERN_CATALOG,
    PatternDefinition,
    Priority,
    Category,
    get_pattern,
    get_patterns_by_category,
    get_patterns_by_priority,
    get_all_patterns,
    get_patterns_for_files,
    get_catalog_stats,
)


class TestPatternCatalog:
    """Test suite for pattern catalog."""

    def test_catalog_not_empty(self):
        """Catalog should contain patterns."""
        assert len(PATTERN_CATALOG) > 0

    def test_catalog_has_minimum_patterns(self):
        """Catalog should have at least 14 patterns (as per CDC)."""
        assert len(PATTERN_CATALOG) >= 14

    def test_all_patterns_have_required_fields(self):
        """All patterns must have required fields."""
        for pattern_id, pattern in PATTERN_CATALOG.items():
            assert pattern.id == pattern_id
            assert pattern.name
            assert pattern.category in Category
            assert pattern.priority in Priority
            assert pattern.description
            assert pattern.suggestion


class TestPatternDefinition:
    """Test PatternDefinition dataclass."""

    def test_pattern_to_dict(self):
        """Pattern should serialize to dictionary."""
        pattern = PatternDefinition(
            id="test-pattern",
            name="Test Pattern",
            category=Category.SECURITY,
            priority=Priority.P1,
            description="Test description",
            detection_hint="Test hint",
            suggestion="Test suggestion",
        )
        data = pattern.to_dict()

        assert data['id'] == "test-pattern"
        assert data['category'] == "security"
        assert data['priority'] == "P1"

    def test_pattern_default_values(self):
        """Pattern should have sensible defaults."""
        pattern = PatternDefinition(
            id="test",
            name="Test",
            category=Category.QUALITY,
            priority=Priority.P3,
            description="Desc",
            detection_hint="Hint",
            suggestion="Suggestion",
        )

        assert pattern.severity == "minor"
        assert pattern.auto_fixable is False
        assert pattern.tags == []
        assert pattern.file_patterns == []


class TestGetPattern:
    """Test get_pattern function."""

    def test_get_existing_pattern(self):
        """Should return pattern when ID exists."""
        pattern = get_pattern("input-not-validated")
        assert pattern is not None
        assert pattern.id == "input-not-validated"
        assert pattern.category == Category.SECURITY

    def test_get_nonexistent_pattern(self):
        """Should return None for unknown ID."""
        pattern = get_pattern("nonexistent-pattern-xyz")
        assert pattern is None


class TestGetPatternsByCategory:
    """Test get_patterns_by_category function."""

    def test_security_patterns(self):
        """Should return security patterns."""
        patterns = get_patterns_by_category(Category.SECURITY)
        assert len(patterns) >= 5  # 5 security patterns in CDC
        assert all(p.category == Category.SECURITY for p in patterns)

    def test_performance_patterns(self):
        """Should return performance patterns."""
        patterns = get_patterns_by_category(Category.PERFORMANCE)
        assert len(patterns) >= 4  # 4 performance patterns in CDC
        assert all(p.category == Category.PERFORMANCE for p in patterns)

    def test_quality_patterns(self):
        """Should return quality patterns."""
        patterns = get_patterns_by_category(Category.QUALITY)
        assert len(patterns) >= 5  # 5 quality patterns in CDC
        assert all(p.category == Category.QUALITY for p in patterns)

    def test_patterns_sorted_by_priority(self):
        """Patterns should be sorted by priority (P1 first)."""
        patterns = get_patterns_by_category(Category.SECURITY)
        priorities = [p.priority.value for p in patterns]
        assert priorities == sorted(priorities)


class TestGetPatternsByPriority:
    """Test get_patterns_by_priority function."""

    def test_p1_patterns(self):
        """Should return P1 (critical) patterns."""
        patterns = get_patterns_by_priority(Priority.P1)
        assert len(patterns) >= 5  # Security patterns are P1
        assert all(p.priority == Priority.P1 for p in patterns)

    def test_p2_patterns(self):
        """Should return P2 (normal) patterns."""
        patterns = get_patterns_by_priority(Priority.P2)
        assert len(patterns) >= 6  # Performance + some quality
        assert all(p.priority == Priority.P2 for p in patterns)

    def test_p3_patterns(self):
        """Should return P3 (low) patterns."""
        patterns = get_patterns_by_priority(Priority.P3)
        assert len(patterns) >= 2  # Some quality patterns
        assert all(p.priority == Priority.P3 for p in patterns)


class TestGetAllPatterns:
    """Test get_all_patterns function."""

    def test_returns_all_patterns(self):
        """Should return all patterns."""
        patterns = get_all_patterns()
        assert len(patterns) == len(PATTERN_CATALOG)

    def test_sorted_by_priority_then_category(self):
        """Patterns should be sorted by priority, then category."""
        patterns = get_all_patterns()
        prev_key = (0, "")
        for p in patterns:
            current_key = (p.priority.value, p.category.value)
            assert current_key >= prev_key
            prev_key = current_key


class TestGetPatternsForFiles:
    """Test get_patterns_for_files function."""

    def test_controller_files(self):
        """Controller files should match relevant patterns."""
        patterns = get_patterns_for_files([
            "src/Controller/UserController.php"
        ])
        pattern_ids = [p.id for p in patterns]

        # Should include controller-relevant patterns
        assert "input-not-validated" in pattern_ids
        assert "auth-missing" in pattern_ids

    def test_repository_files(self):
        """Repository files should match relevant patterns."""
        patterns = get_patterns_for_files([
            "src/Repository/UserRepository.php"
        ])
        pattern_ids = [p.id for p in patterns]

        assert "sql-injection" in pattern_ids

    def test_template_files(self):
        """Template files should match relevant patterns."""
        patterns = get_patterns_for_files([
            "templates/user/profile.html.twig"
        ])
        pattern_ids = [p.id for p in patterns]

        assert "xss-vulnerability" in pattern_ids
        assert "csrf-missing" in pattern_ids


class TestGetCatalogStats:
    """Test get_catalog_stats function."""

    def test_stats_structure(self):
        """Stats should have expected structure."""
        stats = get_catalog_stats()

        assert 'total' in stats
        assert 'by_category' in stats
        assert 'by_priority' in stats

    def test_stats_total_matches_catalog(self):
        """Total should match catalog size."""
        stats = get_catalog_stats()
        assert stats['total'] == len(PATTERN_CATALOG)

    def test_stats_categories_sum_to_total(self):
        """Category counts should sum to total."""
        stats = get_catalog_stats()
        category_sum = sum(stats['by_category'].values())
        assert category_sum == stats['total']

    def test_stats_priorities_sum_to_total(self):
        """Priority counts should sum to total."""
        stats = get_catalog_stats()
        priority_sum = sum(stats['by_priority'].values())
        assert priority_sum == stats['total']


class TestPriorityOrdering:
    """Test that priority ordering is correct (P1 > P2 > P3)."""

    def test_p1_before_p2(self):
        """P1 should sort before P2."""
        assert Priority.P1.value < Priority.P2.value

    def test_p2_before_p3(self):
        """P2 should sort before P3."""
        assert Priority.P2.value < Priority.P3.value

    def test_security_is_p1(self):
        """All security patterns should be P1."""
        security_patterns = get_patterns_by_category(Category.SECURITY)
        assert all(p.priority == Priority.P1 for p in security_patterns)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
