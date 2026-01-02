#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Calibration Module (F08)

Run with: pytest test_calibration.py -v
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

import pytest

from ..calibration import (
    CalibrationData,
    CalibrationFactor,
    CalibrationEvent,
    CalibrationManager,
    calculate_ema,
    calculate_calibration_ratio,
    calculate_accuracy,
    calculate_confidence,
    determine_trend,
)


class TestEMACalculation:
    """Tests for Exponential Moving Average calculation."""

    def test_ema_with_default_alpha(self):
        """Test EMA with default alpha=0.3."""
        result = calculate_ema(new_value=1.5, old_value=1.0, alpha=0.3)
        # 0.3 * 1.5 + 0.7 * 1.0 = 0.45 + 0.7 = 1.15
        assert abs(result - 1.15) < 0.001

    def test_ema_new_value_higher(self):
        """Test EMA when new value is higher."""
        result = calculate_ema(new_value=2.0, old_value=1.0, alpha=0.3)
        assert result > 1.0  # Should increase
        assert result < 2.0  # But not reach new value

    def test_ema_new_value_lower(self):
        """Test EMA when new value is lower."""
        result = calculate_ema(new_value=0.5, old_value=1.0, alpha=0.3)
        assert result < 1.0  # Should decrease
        assert result > 0.5  # But not reach new value

    def test_ema_alpha_one(self):
        """Test EMA with alpha=1 (use new value only)."""
        result = calculate_ema(new_value=2.0, old_value=1.0, alpha=1.0)
        assert result == 2.0

    def test_ema_alpha_zero(self):
        """Test EMA with alpha=0 (use old value only)."""
        result = calculate_ema(new_value=2.0, old_value=1.0, alpha=0.0)
        assert result == 1.0


class TestCalibrationRatio:
    """Tests for calibration ratio calculation."""

    def test_ratio_equal(self):
        """Test ratio when actual equals estimated."""
        result = calculate_calibration_ratio(estimated=60, actual=60)
        assert result == 1.0

    def test_ratio_under_estimate(self):
        """Test ratio when actual exceeds estimated."""
        result = calculate_calibration_ratio(estimated=60, actual=90)
        assert result == 1.5

    def test_ratio_over_estimate(self):
        """Test ratio when estimated exceeds actual."""
        result = calculate_calibration_ratio(estimated=60, actual=30)
        assert result == 0.5

    def test_ratio_zero_estimated(self):
        """Test ratio with zero estimated (edge case)."""
        result = calculate_calibration_ratio(estimated=0, actual=60)
        assert result == 1.0  # Default to 1.0

    def test_ratio_negative_estimated(self):
        """Test ratio with negative estimated (edge case)."""
        result = calculate_calibration_ratio(estimated=-10, actual=60)
        assert result == 1.0  # Default to 1.0


class TestAccuracyCalculation:
    """Tests for accuracy calculation."""

    def test_accuracy_perfect(self):
        """Test perfect accuracy."""
        result = calculate_accuracy(estimated=60, actual=60)
        assert result == 1.0

    def test_accuracy_under_estimate(self):
        """Test accuracy when under-estimating by 50%."""
        result = calculate_accuracy(estimated=60, actual=90)
        # Error ratio = |90-60|/60 = 0.5
        # Accuracy = 1 - 0.5 = 0.5
        assert result == 0.5

    def test_accuracy_over_estimate(self):
        """Test accuracy when over-estimating by 50%."""
        result = calculate_accuracy(estimated=60, actual=30)
        # Error ratio = |30-60|/60 = 0.5
        # Accuracy = 1 - 0.5 = 0.5
        assert result == 0.5

    def test_accuracy_double_time(self):
        """Test accuracy when actual is double estimated."""
        result = calculate_accuracy(estimated=60, actual=120)
        # Error ratio = |120-60|/60 = 1.0
        # Accuracy = 1 - 1.0 = 0.0
        assert result == 0.0

    def test_accuracy_zero_estimated(self):
        """Test accuracy with zero estimated (edge case)."""
        result = calculate_accuracy(estimated=0, actual=60)
        assert result == 0.5  # Neutral

    def test_accuracy_capped_at_one(self):
        """Test accuracy is capped at 1.0."""
        result = calculate_accuracy(estimated=60, actual=60)
        assert result <= 1.0

    def test_accuracy_capped_at_zero(self):
        """Test accuracy is capped at 0.0."""
        result = calculate_accuracy(estimated=60, actual=600)
        assert result >= 0.0


class TestConfidenceCalculation:
    """Tests for confidence level calculation."""

    def test_confidence_zero_samples(self):
        """Test confidence with zero samples."""
        result = calculate_confidence(samples=0)
        assert result == 0.0

    def test_confidence_full(self):
        """Test full confidence at min_samples."""
        result = calculate_confidence(samples=5, min_samples=5)
        assert result == 1.0

    def test_confidence_above_min(self):
        """Test confidence above min_samples."""
        result = calculate_confidence(samples=10, min_samples=5)
        assert result == 1.0

    def test_confidence_partial(self):
        """Test partial confidence below min_samples."""
        result = calculate_confidence(samples=2, min_samples=5)
        assert 0.0 < result < 1.0

    def test_confidence_one_sample(self):
        """Test confidence with one sample."""
        result = calculate_confidence(samples=1, min_samples=5)
        assert result > 0.0


class TestTrendDetermination:
    """Tests for trend determination."""

    def test_trend_stable_empty(self):
        """Test stable trend with empty history."""
        result = determine_trend([])
        assert result == "stable"

    def test_trend_stable_few_samples(self):
        """Test stable trend with few samples."""
        history = [
            CalibrationEvent("f1", "STANDARD", 60, 60, 1.0, "2025-01-01T00:00:00Z"),
            CalibrationEvent("f2", "STANDARD", 60, 60, 1.0, "2025-01-02T00:00:00Z"),
        ]
        result = determine_trend(history)
        assert result == "stable"

    def test_trend_improving(self):
        """Test improving trend."""
        history = [
            CalibrationEvent("f1", "STANDARD", 60, 120, 2.0, "2025-01-01T00:00:00Z"),  # 0% accuracy
            CalibrationEvent("f2", "STANDARD", 60, 100, 1.67, "2025-01-02T00:00:00Z"),  # 33% accuracy
            CalibrationEvent("f3", "STANDARD", 60, 80, 1.33, "2025-01-03T00:00:00Z"),  # 67% accuracy
            CalibrationEvent("f4", "STANDARD", 60, 65, 1.08, "2025-01-04T00:00:00Z"),  # 92% accuracy
            CalibrationEvent("f5", "STANDARD", 60, 60, 1.0, "2025-01-05T00:00:00Z"),  # 100% accuracy
        ]
        result = determine_trend(history)
        assert result == "improving"


class TestCalibrationDataclass:
    """Tests for CalibrationData dataclass."""

    def test_from_dict_empty(self):
        """Test creating from empty dict."""
        data = CalibrationData.from_dict({})
        assert data.version == "1.0.0"
        assert data.factors == {}
        assert data.history == []

    def test_from_dict_with_factors(self):
        """Test creating from dict with factors."""
        input_data = {
            "version": "1.0.0",
            "factors": {
                "STANDARD": {"factor": 1.2, "samples": 5, "confidence": 1.0}
            }
        }
        data = CalibrationData.from_dict(input_data)
        assert "STANDARD" in data.factors
        assert data.factors["STANDARD"].factor == 1.2

    def test_to_dict_roundtrip(self):
        """Test to_dict produces valid JSON."""
        data = CalibrationData()
        data.factors["TINY"] = CalibrationFactor(factor=0.9, samples=3)

        result = data.to_dict()
        assert isinstance(result, dict)
        assert "factors" in result

        # Should be JSON serializable
        json_str = json.dumps(result)
        assert len(json_str) > 0


class TestCalibrationManager:
    """Tests for CalibrationManager."""

    @pytest.fixture
    def temp_memory_dir(self):
        """Create temporary memory directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory_dir = Path(tmpdir) / ".project-memory"
            (memory_dir / "learning").mkdir(parents=True)
            yield memory_dir

    def test_load_nonexistent(self, temp_memory_dir):
        """Test loading when file doesn't exist."""
        manager = CalibrationManager(temp_memory_dir)
        data = manager.load()
        assert isinstance(data, CalibrationData)
        assert data.factors == {}

    def test_calibrate_first_sample(self, temp_memory_dir):
        """Test calibration with first sample."""
        manager = CalibrationManager(temp_memory_dir)
        factor = manager.calibrate(
            feature_slug="test-feature",
            complexity="STANDARD",
            estimated=60,
            actual=90,
        )

        # First sample uses ratio directly
        assert factor.factor == 1.5  # 90/60
        assert factor.samples == 1

    def test_calibrate_multiple_samples(self, temp_memory_dir):
        """Test calibration with multiple samples."""
        manager = CalibrationManager(temp_memory_dir)

        # First sample
        manager.calibrate("f1", "STANDARD", 60, 90)  # ratio = 1.5

        # Second sample
        factor = manager.calibrate("f2", "STANDARD", 60, 60)  # ratio = 1.0

        # EMA: 0.3 * 1.0 + 0.7 * 1.5 = 0.3 + 1.05 = 1.35
        assert abs(factor.factor - 1.35) < 0.001
        assert factor.samples == 2

    def test_get_calibration_factor(self, temp_memory_dir):
        """Test getting calibration factor."""
        manager = CalibrationManager(temp_memory_dir)
        manager.calibrate("f1", "TINY", 30, 25)

        factor = manager.get_calibration_factor("TINY")
        assert abs(factor - 0.833) < 0.01  # 25/30

    def test_get_calibrated_estimate(self, temp_memory_dir):
        """Test applying calibration to estimate."""
        manager = CalibrationManager(temp_memory_dir)
        manager.calibrate("f1", "SMALL", 60, 90)  # ratio = 1.5

        calibrated = manager.get_calibrated_estimate("SMALL", 60)
        assert calibrated == 90  # 60 * 1.5

    def test_save_and_load(self, temp_memory_dir):
        """Test persistence."""
        manager1 = CalibrationManager(temp_memory_dir)
        manager1.calibrate("f1", "STANDARD", 60, 75)

        # Create new manager, should load saved data
        manager2 = CalibrationManager(temp_memory_dir)
        factor = manager2.get_calibration_factor("STANDARD")
        assert abs(factor - 1.25) < 0.01  # 75/60

    def test_reset(self, temp_memory_dir):
        """Test reset creates backup and clears data."""
        manager = CalibrationManager(temp_memory_dir)
        manager.calibrate("f1", "STANDARD", 60, 75)

        manager.reset(backup=True)

        # Should be empty after reset
        data = manager.load()
        assert data.factors == {}
        assert data.global_stats.total_samples == 0

    def test_get_status(self, temp_memory_dir):
        """Test getting status."""
        manager = CalibrationManager(temp_memory_dir)
        manager.calibrate("f1", "STANDARD", 60, 75)

        status = manager.get_status()
        assert "total_samples" in status
        assert "factors" in status
        assert status["total_samples"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
