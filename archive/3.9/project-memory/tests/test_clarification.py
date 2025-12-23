#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Clarification System (F05).

Tests cover:
- Clarification Analyzer (keyword extraction, domain detection)
- Similarity Matcher (Jaccard similarity, feature matching)
- Question Generator (question generation, max 3 constraint)
- Integration (complete flow)
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from project_memory.clarification_analyzer import (
    extract_keywords,
    detect_domain,
    identify_missing_info,
    analyze_brief,
    Domain,
)
from project_memory.similarity_matcher import (
    normalize_text,
    calculate_jaccard_similarity,
    calculate_similarity,
    find_similar_features,
    extract_common_patterns,
)
from project_memory.question_generator import (
    generate_questions,
    adapt_to_persona,
    Question,
    QuestionType,
    MAX_QUESTIONS,
)


# =============================================================================
# ANALYZER TESTS
# =============================================================================

class TestClarificationAnalyzer:
    """Tests for clarification_analyzer.py"""

    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        brief = "Add user authentication with OAuth"
        keywords = extract_keywords(brief)

        assert "authentication" in keywords
        assert "oauth" in keywords
        assert "user" in keywords
        # Stopwords should be filtered
        assert "with" not in keywords
        assert "add" not in keywords

    def test_extract_keywords_french(self):
        """Test keyword extraction from French brief."""
        brief = "Ajouter un système de notifications par email"
        keywords = extract_keywords(brief)

        assert "notifications" in keywords
        assert "email" in keywords
        # French stopwords should be filtered
        assert "un" not in keywords
        assert "de" not in keywords

    def test_extract_keywords_empty(self):
        """Test keyword extraction with empty input."""
        assert extract_keywords("") == []
        assert extract_keywords("   ") == []

    def test_detect_domain_auth(self):
        """Test auth domain detection."""
        keywords = ["authentication", "oauth", "login", "user"]
        domain = detect_domain(keywords)

        assert domain.name == "auth"
        assert domain.confidence > 0.5
        assert len(domain.keywords_matched) >= 2

    def test_detect_domain_notification(self):
        """Test notification domain detection."""
        keywords = ["notification", "email", "push", "alert"]
        domain = detect_domain(keywords)

        assert domain.name == "notification"
        assert domain.confidence > 0.5

    def test_detect_domain_api(self):
        """Test API domain detection."""
        keywords = ["api", "endpoint", "rest", "json"]
        domain = detect_domain(keywords)

        assert domain.name == "api"

    def test_detect_domain_unknown(self):
        """Test unknown domain detection."""
        keywords = ["something", "random", "words"]
        domain = detect_domain(keywords)

        assert domain.name == "unknown"
        assert domain.confidence == 0.0

    def test_detect_domain_empty(self):
        """Test domain detection with empty keywords."""
        domain = detect_domain([])

        assert domain.name == "unknown"
        assert domain.confidence == 0.0

    def test_identify_missing_info_auth(self):
        """Test gap identification for auth domain."""
        brief = "Add authentication"  # Missing method, roles
        gaps = identify_missing_info(brief, "auth")

        categories = [g.category for g in gaps]
        assert "auth_method" in categories

    def test_identify_missing_info_notification(self):
        """Test gap identification for notification domain."""
        brief = "Add notifications"  # Missing channels
        gaps = identify_missing_info(brief, "notification")

        categories = [g.category for g in gaps]
        assert "channels" in categories

    def test_analyze_brief_complete(self):
        """Test complete brief analysis."""
        brief = "Ajouter un système d'authentification OAuth"
        analysis = analyze_brief(brief)

        assert len(analysis.keywords) > 0
        assert analysis.domain.name == "auth"
        assert isinstance(analysis.gaps, list)


# =============================================================================
# SIMILARITY MATCHER TESTS
# =============================================================================

class TestSimilarityMatcher:
    """Tests for similarity_matcher.py"""

    def test_normalize_text(self):
        """Test text normalization."""
        text = "User Authentication with OAuth!"
        normalized = normalize_text(text)

        assert "user" in normalized
        assert "authentication" in normalized
        assert "oauth" in normalized
        assert "with" in normalized  # Not a stopword in matcher

    def test_normalize_text_empty(self):
        """Test normalization of empty text."""
        assert normalize_text("") == set()
        assert normalize_text("   ") == set()

    def test_jaccard_similarity_identical(self):
        """Test Jaccard similarity for identical sets."""
        set1 = {"a", "b", "c"}
        set2 = {"a", "b", "c"}

        score = calculate_jaccard_similarity(set1, set2)
        assert score == 1.0

    def test_jaccard_similarity_disjoint(self):
        """Test Jaccard similarity for disjoint sets."""
        set1 = {"a", "b", "c"}
        set2 = {"d", "e", "f"}

        score = calculate_jaccard_similarity(set1, set2)
        assert score == 0.0

    def test_jaccard_similarity_partial(self):
        """Test Jaccard similarity for overlapping sets."""
        set1 = {"a", "b", "c"}
        set2 = {"b", "c", "d"}

        # Intersection: {b, c} = 2
        # Union: {a, b, c, d} = 4
        # Jaccard = 2/4 = 0.5
        score = calculate_jaccard_similarity(set1, set2)
        assert score == 0.5

    def test_jaccard_similarity_empty(self):
        """Test Jaccard similarity with empty sets."""
        assert calculate_jaccard_similarity(set(), {"a"}) == 0.0
        assert calculate_jaccard_similarity({"a"}, set()) == 0.0
        assert calculate_jaccard_similarity(set(), set()) == 0.0

    def test_calculate_similarity(self):
        """Test feature similarity calculation."""
        keywords = ["authentication", "oauth", "user"]
        title = "User Authentication with OAuth"

        score, matched = calculate_similarity(keywords, title)

        assert score > 0.5
        assert len(matched) >= 2

    def test_find_similar_features(self, sample_features):
        """Test finding similar features."""
        keywords = ["authentication", "oauth", "user"]

        matches = find_similar_features(sample_features, keywords, threshold=0.2)

        assert len(matches) > 0
        # User authentication should be top match
        assert matches[0].slug == "user-authentication"

    def test_find_similar_features_notification(self, sample_features):
        """Test finding similar notification features."""
        keywords = ["notification", "email", "send"]

        matches = find_similar_features(sample_features, keywords, threshold=0.2)

        assert len(matches) > 0
        slugs = [m.slug for m in matches]
        assert "email-notifications" in slugs

    def test_find_similar_features_no_match(self, sample_features):
        """Test when no similar features found."""
        keywords = ["blockchain", "crypto", "nft"]

        matches = find_similar_features(sample_features, keywords, threshold=0.5)

        assert len(matches) == 0

    def test_find_similar_features_empty(self):
        """Test with empty inputs."""
        assert find_similar_features([], ["auth"], 0.3) == []
        assert find_similar_features([{"slug": "test", "title": "Test"}], [], 0.3) == []

    def test_extract_common_patterns(self, sample_features):
        """Test pattern extraction from features."""
        keywords = ["authentication", "service"]
        matches = find_similar_features(sample_features, keywords, threshold=0.2)

        patterns = extract_common_patterns(matches)

        assert isinstance(patterns, list)
        # Should detect Service pattern from files
        assert "Service" in patterns


# =============================================================================
# QUESTION GENERATOR TESTS
# =============================================================================

class TestQuestionGenerator:
    """Tests for question_generator.py"""

    def test_generate_questions_max_3(self, sample_context, sample_gaps):
        """Test that max 3 questions are generated."""
        similar = [
            {"slug": "test", "title": "Test", "score": 0.8, "files_modified": []}
        ]

        result = generate_questions(
            brief="Test brief",
            context=sample_context,
            similar_features=similar,
            gaps=sample_gaps,
        )

        assert len(result.questions) <= MAX_QUESTIONS
        assert len(result.questions) <= 3

    def test_generate_questions_with_similar(self, sample_context):
        """Test question generation with similar feature."""
        similar = [
            {
                "slug": "user-alerts",
                "title": "User Alerts System",
                "score": 0.75,
                "files_modified": ["src/Service/AlertService.php"],
            }
        ]

        result = generate_questions(
            brief="Add notification system",
            context=sample_context,
            similar_features=similar,
            gaps=[],
        )

        # Should have at least one REUSE question
        types = [q.type for q in result.questions]
        assert QuestionType.REUSE in types

    def test_generate_questions_without_similar(self, sample_context, sample_gaps):
        """Test question generation without similar features."""
        result = generate_questions(
            brief="Add notification system",
            context=sample_context,
            similar_features=[],
            gaps=sample_gaps,
        )

        # Should have technical questions from gaps
        types = [q.type for q in result.questions]
        assert QuestionType.TECHNICAL in types

    def test_generate_questions_suggestions(self, sample_context):
        """Test that questions include suggestions."""
        similar = [
            {
                "slug": "alerts",
                "title": "Alerts",
                "score": 0.6,
                "files_modified": [],
            }
        ]

        result = generate_questions(
            brief="Add notifications",
            context=sample_context,
            similar_features=similar,
            gaps=[],
        )

        # At least one question should have a suggestion
        suggestions = [q.suggestion for q in result.questions if q.suggestion]
        assert len(suggestions) > 0

    def test_adapt_to_persona_backend(self):
        """Test persona adaptation for backend."""
        questions = [
            Question(
                type=QuestionType.TECHNICAL,
                text="Test question",
                priority="medium",
            )
        ]

        adapted = adapt_to_persona(questions, "backend", lang="fr")

        # Should add priority question for backend
        assert len(adapted) >= len(questions)

    def test_adapt_to_persona_none(self):
        """Test persona adaptation with no persona."""
        questions = [
            Question(
                type=QuestionType.TECHNICAL,
                text="Test question",
                priority="medium",
            )
        ]

        adapted = adapt_to_persona(questions, None, lang="fr")

        # Should return unchanged
        assert len(adapted) == len(questions)

    def test_question_to_dict(self):
        """Test Question serialization."""
        question = Question(
            type=QuestionType.REUSE,
            text="Test question?",
            suggestion="Yes",
            reason="Test reason",
            source_feature="test-feature",
            priority="high",
        )

        data = question.to_dict()

        assert data["type"] == "reuse"
        assert data["text"] == "Test question?"
        assert data["suggestion"] == "Yes"
        assert data["source_feature"] == "test-feature"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestClarificationIntegration:
    """Integration tests for complete clarification flow."""

    def test_complete_flow_with_history(self, sample_features):
        """Test complete flow: analyze → match → generate."""
        brief = "Ajouter un système de notifications par email"

        # Step 1: Analyze
        analysis = analyze_brief(brief)
        assert analysis.domain.name == "notification"

        # Step 2: Find similar
        matches = find_similar_features(
            sample_features,
            analysis.keywords,
            threshold=0.2
        )
        assert len(matches) > 0

        # Step 3: Generate questions
        context = {
            "domain": analysis.domain.name,
            "patterns": [],
            "keywords": analysis.keywords,
        }
        gaps = [
            {
                "category": g.category,
                "description": g.description,
                "priority": g.priority,
                "example_question": g.example_question,
            }
            for g in analysis.gaps
        ]

        result = generate_questions(
            brief=brief,
            context=context,
            similar_features=[
                {
                    "slug": m.slug,
                    "title": m.title,
                    "score": m.score,
                    "files_modified": m.files_modified,
                }
                for m in matches
            ],
            gaps=gaps,
        )

        # Validate result
        assert len(result.questions) <= 3
        assert result.domain_detected == "notification"
        assert result.similar_features_found > 0

    def test_complete_flow_no_history(self):
        """Test complete flow without feature history."""
        brief = "Ajouter un système d'authentification"

        # Step 1: Analyze
        analysis = analyze_brief(brief)
        assert analysis.domain.name == "auth"

        # Step 2: No similar features (empty history)
        matches = find_similar_features([], analysis.keywords, threshold=0.3)
        assert len(matches) == 0

        # Step 3: Generate questions (graceful degradation)
        context = {
            "domain": analysis.domain.name,
            "patterns": [],
        }

        result = generate_questions(
            brief=brief,
            context=context,
            similar_features=[],
            gaps=[],
        )

        # Should still generate questions
        assert len(result.questions) >= 1
        assert result.similar_features_found == 0

    def test_graceful_degradation(self):
        """Test graceful degradation with invalid inputs."""
        # Empty brief should not crash
        analysis = analyze_brief("")
        assert analysis.domain.name == "unknown"

        # Should still work with minimal context
        result = generate_questions(
            brief="",
            context={},
            similar_features=[],
            gaps=[],
        )
        assert isinstance(result.questions, list)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
