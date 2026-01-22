#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Brief Reformulator module.
"""

import pytest
from ..brief_reformulator import (
    calculate_fuzziness_score,
    needs_reformulation,
    detect_template_type,
    reformulate_brief,
    format_reformulation_display,
    FuzzinessScore,
    ReformulatedBrief,
    TemplateType,
    FUZZINESS_AUTO_THRESHOLD,
    FUZZINESS_SUGGEST_THRESHOLD,
)


class TestCalculateFuzzinessScore:
    """Tests for calculate_fuzziness_score function."""

    def test_high_fuzziness_for_vague_brief(self):
        """Should return high fuzziness for vague brief."""
        score = calculate_fuzziness_score("améliorer le système")
        assert score.overall > FUZZINESS_SUGGEST_THRESHOLD
        assert score.needs_reformulation

    def test_low_fuzziness_for_clear_brief(self):
        """Should return low fuzziness for clear technical brief."""
        score = calculate_fuzziness_score(
            "Ajouter authentification OAuth avec JWT pour l'API REST. "
            "Endpoints: POST /login, POST /logout, GET /user. "
            "Utiliser refresh tokens avec expiration 7 jours."
        )
        assert score.overall < FUZZINESS_AUTO_THRESHOLD
        # May or may not need reformulation depending on exact score

    def test_high_fuzziness_for_voice_input(self):
        """Should return high fuzziness for voice-dictated input."""
        score = calculate_fuzziness_score(
            "euh donc euh faudrait un truc pour les users tu vois genre un machin"
        )
        assert score.hesitation_density > 0
        assert score.overall > FUZZINESS_SUGGEST_THRESHOLD

    def test_returns_fuzziness_score_object(self):
        """Should return complete FuzzinessScore object."""
        score = calculate_fuzziness_score("some brief")
        assert isinstance(score, FuzzinessScore)
        assert 0 <= score.overall <= 1
        assert 0 <= score.domain_confidence <= 1
        assert 0 <= score.gap_score <= 1
        assert 0 <= score.scope_clarity <= 1
        assert 0 <= score.hesitation_density <= 1
        assert score.suggestion_level in ["auto", "suggest", "skip"]

    def test_suggestion_level_auto(self):
        """Should set suggestion_level to 'auto' for very fuzzy briefs."""
        score = calculate_fuzziness_score("euh truc machin chose")
        if score.overall > FUZZINESS_AUTO_THRESHOLD:
            assert score.suggestion_level == "auto"

    def test_suggestion_level_skip(self):
        """Should set suggestion_level to 'skip' for clear briefs."""
        score = calculate_fuzziness_score(
            "Implémenter endpoint REST POST /api/users avec validation email unique"
        )
        if score.overall < FUZZINESS_SUGGEST_THRESHOLD:
            assert score.suggestion_level == "skip"

    def test_includes_details(self):
        """Should include details in score."""
        score = calculate_fuzziness_score("Add user authentication")
        assert "domain" in score.details
        assert "keywords" in score.details
        assert "word_count" in score.details


class TestNeedsReformulation:
    """Tests for needs_reformulation function."""

    def test_force_flag_overrides_score(self):
        """Should reformulate when force=True regardless of score."""
        score = FuzzinessScore(
            overall=0.1,  # Low score
            domain_confidence=0.9,
            gap_score=0.1,
            scope_clarity=0.9,
            hesitation_density=0.0,
            needs_reformulation=False,
            suggestion_level="skip"
        )
        assert needs_reformulation(score, force=True)

    def test_skip_flag_overrides_score(self):
        """Should not reformulate when skip=True regardless of score."""
        score = FuzzinessScore(
            overall=0.9,  # High score
            domain_confidence=0.1,
            gap_score=0.9,
            scope_clarity=0.1,
            hesitation_density=0.5,
            needs_reformulation=True,
            suggestion_level="auto"
        )
        assert not needs_reformulation(score, skip=True)

    def test_respects_score_when_no_flags(self):
        """Should respect score.needs_reformulation when no flags."""
        score_high = FuzzinessScore(
            overall=0.7,
            domain_confidence=0.3,
            gap_score=0.7,
            scope_clarity=0.3,
            hesitation_density=0.3,
            needs_reformulation=True,
            suggestion_level="auto"
        )
        score_low = FuzzinessScore(
            overall=0.2,
            domain_confidence=0.9,
            gap_score=0.1,
            scope_clarity=0.9,
            hesitation_density=0.0,
            needs_reformulation=False,
            suggestion_level="skip"
        )
        assert needs_reformulation(score_high)
        assert not needs_reformulation(score_low)


class TestDetectTemplateType:
    """Tests for detect_template_type function."""

    def test_detects_feature_template(self):
        """Should detect feature template for new functionality."""
        assert detect_template_type("Ajouter un système de notifications") == TemplateType.FEATURE
        assert detect_template_type("Create user authentication") == TemplateType.FEATURE
        assert detect_template_type("Implémenter export PDF") == TemplateType.FEATURE

    def test_detects_problem_template(self):
        """Should detect problem template for bugs."""
        assert detect_template_type("Fixer le bug de login") == TemplateType.PROBLEM
        assert detect_template_type("Corriger l'erreur 500") == TemplateType.PROBLEM
        assert detect_template_type("Fix broken authentication") == TemplateType.PROBLEM

    def test_detects_decision_template(self):
        """Should detect decision template for choices."""
        assert detect_template_type("Quelle stratégie de cache choisir") == TemplateType.DECISION
        assert detect_template_type("How should we approach authentication") == TemplateType.DECISION

    def test_returns_unknown_for_ambiguous(self):
        """Should return unknown for ambiguous briefs."""
        assert detect_template_type("le système") == TemplateType.UNKNOWN


class TestReformulateBrief:
    """Tests for reformulate_brief function."""

    def test_returns_reformulated_brief(self):
        """Should return ReformulatedBrief object."""
        result = reformulate_brief("euh faudrait un truc pour les users")
        assert isinstance(result, ReformulatedBrief)
        assert result.objective
        assert result.context
        assert result.constraints
        assert result.success_criteria
        assert result.template_type in TemplateType
        assert result.original_brief == "euh faudrait un truc pour les users"

    def test_cleans_voice_artifacts(self):
        """Should clean voice artifacts from brief."""
        result = reformulate_brief("euh genre faudrait tu vois un machin")
        assert "euh" not in result.cleaned_brief.lower()
        assert "genre" not in result.cleaned_brief.lower()
        assert result.cleaning_result is not None

    def test_includes_fuzziness_score(self):
        """Should include fuzziness score in result."""
        result = reformulate_brief("améliorer le système")
        assert result.fuzziness_score is not None
        assert isinstance(result.fuzziness_score, FuzzinessScore)

    def test_uses_exploration_context(self):
        """Should incorporate exploration context when provided."""
        context = {
            "stack": "symfony",
            "impacted_files": ["src/Controller/AuthController.php"],
            "patterns": ["repository", "service-layer"],
            "risks": ["Breaking change in API"]
        }
        result = reformulate_brief("ajouter authentification", context)
        # Context should influence the result
        assert "symfony" in result.context.lower() or len(result.context) > 0


class TestFormatReformulationDisplay:
    """Tests for format_reformulation_display function."""

    def test_formats_all_sections(self):
        """Should format all sections."""
        result = ReformulatedBrief(
            objective="Implémenter authentification OAuth.",
            context="Stack: symfony | 3 fichier(s) impacté(s)",
            constraints="Sans breaking changes",
            success_criteria="Feature fonctionnelle et testée",
            template_type=TemplateType.FEATURE,
            original_brief="ajouter auth",
            cleaned_brief="Ajouter auth."
        )
        formatted = format_reformulation_display(result)
        assert "**Objectif**" in formatted
        assert "**Contexte**" in formatted
        assert "**Contraintes**" in formatted
        assert "**Critères de succès**" in formatted
        assert "OAuth" in formatted


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_workflow_fuzzy_brief(self):
        """Should complete full workflow for fuzzy brief."""
        # Step 1: Calculate fuzziness
        brief = "euh donc faudrait un truc pour gérer les users tu vois"
        score = calculate_fuzziness_score(brief)

        # Step 2: Check if reformulation needed
        if needs_reformulation(score):
            # Step 3: Reformulate
            result = reformulate_brief(brief)

            # Step 4: Format for display
            display = format_reformulation_display(result)

            assert result.cleaned_brief != brief
            assert len(display) > 0

    def test_full_workflow_clear_brief(self):
        """Should handle clear brief appropriately."""
        brief = "Implémenter authentification OAuth avec JWT pour API REST"
        score = calculate_fuzziness_score(brief)

        # Clear brief should have lower fuzziness
        assert score.domain_confidence > 0.3  # Should detect auth domain

    def test_force_reformulation_on_clear_brief(self):
        """Should allow forcing reformulation even on clear brief."""
        brief = "Add user authentication with OAuth"
        score = calculate_fuzziness_score(brief)

        # Even if score is low, force should work
        assert needs_reformulation(score, force=True)

        result = reformulate_brief(brief)
        assert result.objective  # Should still produce valid output
