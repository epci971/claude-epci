#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Voice Cleaner module.
"""

import pytest
from ..voice_cleaner import (
    clean_voice_transcript,
    calculate_hesitation_density,
    is_voice_dictated,
    VoiceCleaningResult,
    HesitationDensity,
)


class TestCleanVoiceTranscript:
    """Tests for clean_voice_transcript function."""

    def test_removes_french_hesitations(self):
        """Should remove French hesitation sounds."""
        result = clean_voice_transcript("euh faudrait fixer le bug hum")
        assert "euh" not in result.cleaned_text.lower()
        assert "hum" not in result.cleaned_text.lower()
        assert result.artifacts_removed >= 2

    def test_removes_english_hesitations(self):
        """Should remove English hesitation sounds."""
        result = clean_voice_transcript("um we need to uh fix this")
        assert "um" not in result.cleaned_text.lower()
        assert "uh" not in result.cleaned_text.lower()

    def test_removes_french_fillers(self):
        """Should remove French filler phrases."""
        result = clean_voice_transcript("tu vois genre faudrait faire ça quoi")
        assert "tu vois" not in result.cleaned_text.lower()
        assert "genre" not in result.cleaned_text.lower()
        assert "quoi" not in result.cleaned_text.lower()

    def test_removes_english_fillers(self):
        """Should remove English filler phrases."""
        result = clean_voice_transcript("you know we actually need to like fix this")
        assert "you know" not in result.cleaned_text.lower()
        assert "like" not in result.cleaned_text.lower()

    def test_preserves_rupture_markers(self):
        """Should preserve rupture markers for multi-task detection."""
        result = clean_voice_transcript("fixer le login et puis aussi ajouter l'export")
        # "et puis" and "aussi" should be preserved
        cleaned_lower = result.cleaned_text.lower()
        assert "aussi" in cleaned_lower or "et puis" in cleaned_lower
        assert "aussi" in result.rupture_markers_preserved or "et puis" in result.rupture_markers_preserved

    def test_handles_self_corrections(self):
        """Should keep corrected version for self-corrections."""
        result = clean_voice_transcript("export CSV non pardon JSON")
        assert "json" in result.cleaned_text.lower()
        # CSV should be removed (corrected away)
        assert result.corrections_applied >= 1

    def test_normalizes_tense(self):
        """Should normalize spoken tense to written form."""
        result = clean_voice_transcript("faudrait que le système fasse ça")
        # "faudrait que" should become "doit"
        assert result.normalizations_applied >= 1

    def test_normalizes_voice(self):
        """Should normalize first person to system-centric."""
        result = clean_voice_transcript("je veux un bouton de logout")
        # Should not contain "je veux" after normalization
        assert "je veux" not in result.cleaned_text.lower()
        assert result.normalizations_applied >= 1

    def test_preserves_technical_terms(self):
        """Should preserve technical jargon exactly."""
        result = clean_voice_transcript("euh faudrait une API REST avec OAuth")
        assert "api" in result.cleaned_text.lower()
        assert "rest" in result.cleaned_text.lower()
        assert "oauth" in result.cleaned_text.lower()

    def test_handles_empty_input(self):
        """Should handle empty input gracefully."""
        result = clean_voice_transcript("")
        assert result.cleaned_text == ""
        assert result.artifacts_removed == 0

    def test_cleans_up_whitespace(self):
        """Should normalize multiple spaces and punctuation."""
        result = clean_voice_transcript("euh   fixer   le   bug")
        assert "  " not in result.cleaned_text

    def test_capitalizes_first_letter(self):
        """Should capitalize first letter of result."""
        result = clean_voice_transcript("fixer le bug")
        assert result.cleaned_text[0].isupper()

    def test_ensures_ending_punctuation(self):
        """Should ensure result ends with punctuation."""
        result = clean_voice_transcript("fixer le bug")
        assert result.cleaned_text[-1] in ".!?"

    def test_returns_complete_result_object(self):
        """Should return complete VoiceCleaningResult."""
        result = clean_voice_transcript("euh genre faudrait fixer ça tu vois")
        assert isinstance(result, VoiceCleaningResult)
        assert result.original_text == "euh genre faudrait fixer ça tu vois"
        assert isinstance(result.hesitations_found, list)
        assert isinstance(result.fillers_found, list)


class TestCalculateHesitationDensity:
    """Tests for calculate_hesitation_density function."""

    def test_high_density_for_voice_input(self):
        """Should return high density for voice-dictated input."""
        density = calculate_hesitation_density("euh donc euh faudrait euh fixer le truc")
        assert density.density > 0.1
        assert density.hesitation_count >= 3

    def test_low_density_for_clean_input(self):
        """Should return low density for clean written input."""
        density = calculate_hesitation_density("Add user authentication with OAuth")
        assert density.density < 0.1
        assert density.hesitation_count == 0

    def test_counts_fillers(self):
        """Should count filler phrases."""
        density = calculate_hesitation_density("tu vois genre faudrait faire ça quoi")
        assert density.filler_count >= 2

    def test_handles_empty_input(self):
        """Should handle empty input gracefully."""
        density = calculate_hesitation_density("")
        assert density.total_words == 0
        assert density.density == 0.0

    def test_returns_density_object(self):
        """Should return HesitationDensity object."""
        density = calculate_hesitation_density("some text here")
        assert isinstance(density, HesitationDensity)
        assert density.total_words == 3


class TestIsVoiceDictated:
    """Tests for is_voice_dictated function."""

    def test_detects_voice_input(self):
        """Should detect voice-dictated input."""
        assert is_voice_dictated("euh donc euh faudrait euh fixer le truc")

    def test_rejects_clean_input(self):
        """Should not flag clean written input."""
        assert not is_voice_dictated("Add user authentication with OAuth")

    def test_custom_threshold(self):
        """Should respect custom threshold."""
        text = "euh faudrait fixer ça"
        # With high threshold, should not be flagged
        assert not is_voice_dictated(text, threshold=0.5)
        # With low threshold, might be flagged
        # (depends on actual density)


class TestEdgeCases:
    """Tests for edge cases and complex scenarios."""

    def test_mixed_french_english(self):
        """Should handle mixed French/English input."""
        result = clean_voice_transcript("euh je veux uh add a feature")
        assert "euh" not in result.cleaned_text.lower()
        assert "uh" not in result.cleaned_text.lower()

    def test_multiple_corrections(self):
        """Should handle multiple self-corrections."""
        result = clean_voice_transcript("CSV non JSON non plutôt XML")
        # Should keep final correction
        assert result.corrections_applied >= 1

    def test_long_input(self):
        """Should handle longer inputs."""
        long_input = "euh " * 50 + "fixer le bug"
        result = clean_voice_transcript(long_input)
        assert result.artifacts_removed >= 40

    def test_only_hesitations(self):
        """Should handle input that is mostly hesitations."""
        result = clean_voice_transcript("euh hum bah ben")
        # Result should be minimal or empty after cleaning
        assert len(result.cleaned_text) < len("euh hum bah ben")
