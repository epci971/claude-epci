#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Calibration Module

Implements Exponential Moving Average (EMA) calibration for estimation accuracy.
Part of the F08 Continuous Learning feature.

Usage:
    from project_memory.calibration import CalibrationManager

    manager = CalibrationManager(memory_dir)
    manager.calibrate(complexity="STANDARD", estimated=180, actual=210)
    factor = manager.get_calibration_factor("STANDARD")
"""

import json
import math
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_VERSION = "1.0.0"
DEFAULT_ALPHA = 0.3  # EMA smoothing factor (weight of new data)
MIN_SAMPLES_FOR_CONFIDENCE = 5  # Minimum samples for high confidence
MAX_HISTORY_SIZE = 20  # Maximum calibration history entries


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class CalibrationFactor:
    """Calibration factor for a complexity category."""
    factor: float = 1.0
    samples: int = 0
    confidence: float = 0.0
    last_updated: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CalibrationFactor':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CalibrationEvent:
    """A single calibration event."""
    feature_slug: str
    complexity: str
    estimated: float  # in minutes
    actual: float  # in minutes
    ratio: float
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict) -> 'CalibrationEvent':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GlobalCalibration:
    """Global calibration metrics."""
    total_samples: int = 0
    overall_accuracy: float = 0.5
    trend: str = "stable"

    @classmethod
    def from_dict(cls, data: dict) -> 'GlobalCalibration':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CalibrationData:
    """Complete calibration data structure."""
    version: str = CURRENT_VERSION
    factors: Dict[str, CalibrationFactor] = field(default_factory=dict)
    global_stats: GlobalCalibration = field(default_factory=GlobalCalibration)
    history: List[CalibrationEvent] = field(default_factory=list)
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CalibrationData':
        """Create from dictionary with nested object handling."""
        factors = {}
        for key, value in data.get('factors', {}).items():
            if isinstance(value, dict):
                factors[key] = CalibrationFactor.from_dict(value)
            else:
                factors[key] = value

        global_data = data.get('global', data.get('global_stats', {}))
        global_stats = GlobalCalibration.from_dict(global_data) if global_data else GlobalCalibration()

        history = []
        for event in data.get('history', []):
            if isinstance(event, dict):
                history.append(CalibrationEvent.from_dict(event))

        return cls(
            version=data.get('version', CURRENT_VERSION),
            factors=factors,
            global_stats=global_stats,
            history=history,
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'factors': {
                k: v.to_dict() if isinstance(v, CalibrationFactor) else v
                for k, v in self.factors.items()
            },
            'global': self.global_stats.to_dict() if isinstance(self.global_stats, GlobalCalibration) else self.global_stats,
            'history': [
                e.to_dict() if isinstance(e, CalibrationEvent) else e
                for e in self.history
            ],
            'updated_at': self.updated_at,
        }


# =============================================================================
# CALIBRATION ALGORITHMS
# =============================================================================

def calculate_ema(
    new_value: float,
    old_value: float,
    alpha: float = DEFAULT_ALPHA
) -> float:
    """
    Calculate Exponential Moving Average.

    Formula: EMA = alpha * new_value + (1 - alpha) * old_value

    Args:
        new_value: The new observation.
        old_value: The previous EMA value.
        alpha: Smoothing factor (0-1). Higher = more weight to new data.

    Returns:
        New EMA value.
    """
    return alpha * new_value + (1 - alpha) * old_value


def calculate_calibration_ratio(estimated: float, actual: float) -> float:
    """
    Calculate the ratio between actual and estimated time.

    Args:
        estimated: Estimated time (must be > 0).
        actual: Actual time taken.

    Returns:
        Ratio (actual / estimated). Returns 1.0 if estimated is 0.
    """
    if estimated <= 0:
        return 1.0
    return actual / estimated


def calculate_accuracy(estimated: float, actual: float) -> float:
    """
    Calculate estimation accuracy as a 0-1 score.

    Accuracy = 1 - |error_ratio|, capped at 0-1

    Where error_ratio = (actual - estimated) / estimated

    Args:
        estimated: Estimated time.
        actual: Actual time taken.

    Returns:
        Accuracy score between 0 and 1.
    """
    # Guard against division by zero (including floating-point near-zero)
    if estimated <= 0 or abs(estimated) < 1e-10:
        return 0.5  # Neutral accuracy for invalid input

    error_ratio = abs(actual - estimated) / estimated
    accuracy = max(0.0, 1.0 - error_ratio)
    return min(1.0, accuracy)


def calculate_confidence(samples: int, min_samples: int = MIN_SAMPLES_FOR_CONFIDENCE) -> float:
    """
    Calculate confidence level based on sample count.

    Uses a logarithmic scale that approaches 1.0 asymptotically.

    Args:
        samples: Number of samples collected.
        min_samples: Minimum samples for full confidence.

    Returns:
        Confidence score between 0 and 1.
    """
    if samples <= 0:
        return 0.0
    if samples >= min_samples:
        return 1.0

    # Logarithmic growth towards 1.0
    return min(1.0, math.log(samples + 1) / math.log(min_samples + 1))


def determine_trend(history: List[CalibrationEvent], window: int = 5) -> str:
    """
    Determine accuracy trend from recent history.

    Args:
        history: List of calibration events (most recent last).
        window: Number of recent events to consider.

    Returns:
        "improving", "stable", or "declining"
    """
    if len(history) < 3:
        return "stable"

    recent = history[-window:] if len(history) >= window else history

    # Calculate accuracies for first and second half
    mid = len(recent) // 2
    first_half = recent[:mid]
    second_half = recent[mid:]

    if not first_half or not second_half:
        return "stable"

    first_avg = sum(calculate_accuracy(e.estimated, e.actual) for e in first_half) / len(first_half)
    second_avg = sum(calculate_accuracy(e.estimated, e.actual) for e in second_half) / len(second_half)

    diff = second_avg - first_avg

    if diff > 0.1:
        return "improving"
    elif diff < -0.1:
        return "declining"
    return "stable"


# =============================================================================
# CALIBRATION MANAGER
# =============================================================================

class CalibrationManager:
    """
    Manages calibration data for EPCI continuous learning.

    Handles loading, saving, and updating calibration factors
    based on actual vs estimated time measurements.
    """

    def __init__(self, memory_dir: Path, alpha: float = DEFAULT_ALPHA):
        """
        Initialize the calibration manager.

        Args:
            memory_dir: Path to .project-memory directory.
            alpha: EMA smoothing factor.
        """
        self.memory_dir = Path(memory_dir)
        self.calibration_file = self.memory_dir / "learning" / "calibration.json"
        self.alpha = alpha
        self._data: Optional[CalibrationData] = None

    def load(self) -> CalibrationData:
        """
        Load calibration data from file.

        Returns:
            CalibrationData instance (default if file doesn't exist).
        """
        if self._data is not None:
            return self._data

        if not self.calibration_file.exists():
            self._data = CalibrationData()
            return self._data

        try:
            with open(self.calibration_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._data = CalibrationData.from_dict(data)
            return self._data
        except (json.JSONDecodeError, Exception):
            # Graceful degradation
            self._data = CalibrationData()
            return self._data

    def save(self) -> bool:
        """
        Save calibration data to file.

        Returns:
            True if save successful.
        """
        if self._data is None:
            return True  # Nothing to save

        try:
            self._data.updated_at = datetime.utcnow().isoformat() + "Z"

            # Ensure directory exists
            self.calibration_file.parent.mkdir(parents=True, exist_ok=True)

            # Atomic write
            temp_file = self.calibration_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._data.to_dict(), f, indent=2, ensure_ascii=False)

            temp_file.replace(self.calibration_file)
            return True
        except Exception:
            return False

    # Valid complexity categories
    VALID_COMPLEXITIES = {'TINY', 'SMALL', 'STANDARD', 'LARGE'}

    def calibrate(
        self,
        feature_slug: str,
        complexity: str,
        estimated: float,
        actual: float
    ) -> CalibrationFactor:
        """
        Update calibration based on new measurement.

        Uses EMA to smooth the calibration factor over time.

        Args:
            feature_slug: Identifier of the completed feature.
            complexity: Complexity category (TINY, SMALL, STANDARD, LARGE).
            estimated: Estimated time in minutes.
            actual: Actual time in minutes.

        Returns:
            Updated CalibrationFactor for the complexity category.

        Raises:
            ValueError: If inputs are invalid.
        """
        # Input validation
        if not feature_slug or not isinstance(feature_slug, str):
            raise ValueError("feature_slug must be a non-empty string")

        if complexity not in self.VALID_COMPLEXITIES:
            raise ValueError(f"complexity must be one of {self.VALID_COMPLEXITIES}, got '{complexity}'")

        if not isinstance(estimated, (int, float)) or estimated <= 0:
            raise ValueError(f"estimated must be a positive number, got {estimated}")

        if not isinstance(actual, (int, float)) or actual <= 0:
            raise ValueError(f"actual must be a positive number, got {actual}")

        data = self.load()
        now = datetime.utcnow().isoformat() + "Z"

        # Calculate ratio
        ratio = calculate_calibration_ratio(estimated, actual)

        # Get or create factor for this complexity
        if complexity not in data.factors:
            data.factors[complexity] = CalibrationFactor()

        factor = data.factors[complexity]

        # Apply EMA
        if factor.samples == 0:
            # First sample: use ratio directly
            factor.factor = ratio
        else:
            # Apply EMA smoothing
            factor.factor = calculate_ema(ratio, factor.factor, self.alpha)

        # Update metadata
        factor.samples += 1
        factor.confidence = calculate_confidence(factor.samples)
        factor.last_updated = now

        # Add to history
        event = CalibrationEvent(
            feature_slug=feature_slug,
            complexity=complexity,
            estimated=estimated,
            actual=actual,
            ratio=ratio,
            timestamp=now,
        )
        data.history.append(event)

        # Trim history to max size
        if len(data.history) > MAX_HISTORY_SIZE:
            data.history = data.history[-MAX_HISTORY_SIZE:]

        # Update global stats
        data.global_stats.total_samples += 1
        accuracy = calculate_accuracy(estimated, actual)
        data.global_stats.overall_accuracy = calculate_ema(
            accuracy,
            data.global_stats.overall_accuracy,
            self.alpha
        )
        data.global_stats.trend = determine_trend(data.history)

        # Save changes
        self.save()

        return factor

    def get_calibration_factor(self, complexity: str) -> float:
        """
        Get the calibration factor for a complexity category.

        Args:
            complexity: Complexity category.

        Returns:
            Calibration factor (1.0 if no data).
        """
        data = self.load()

        if complexity in data.factors:
            factor = data.factors[complexity]
            if isinstance(factor, CalibrationFactor):
                return factor.factor
            elif isinstance(factor, dict):
                return factor.get('factor', 1.0)

        return 1.0

    def get_calibrated_estimate(self, complexity: str, base_estimate: float) -> float:
        """
        Apply calibration to a base estimate.

        Args:
            complexity: Complexity category.
            base_estimate: Original time estimate in minutes.

        Returns:
            Calibrated estimate.
        """
        factor = self.get_calibration_factor(complexity)
        return base_estimate * factor

    def get_status(self) -> dict:
        """
        Get current calibration status for display.

        Returns:
            Dictionary with status information.
        """
        data = self.load()

        return {
            'total_samples': data.global_stats.total_samples,
            'overall_accuracy': f"{data.global_stats.overall_accuracy:.1%}",
            'trend': data.global_stats.trend,
            'factors': {
                k: {
                    'factor': f"{v.factor:.2f}x" if isinstance(v, CalibrationFactor) else f"{v.get('factor', 1.0):.2f}x",
                    'samples': v.samples if isinstance(v, CalibrationFactor) else v.get('samples', 0),
                    'confidence': f"{(v.confidence if isinstance(v, CalibrationFactor) else v.get('confidence', 0)):.0%}",
                }
                for k, v in data.factors.items()
            },
            'last_updated': data.updated_at,
        }

    def reset(self, backup: bool = True) -> bool:
        """
        Reset calibration data.

        Args:
            backup: Whether to create backup before reset.

        Returns:
            True if reset successful.
        """
        if backup and self.calibration_file.exists():
            backup_path = self.calibration_file.with_suffix(
                f'.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
            )
            try:
                self.calibration_file.rename(backup_path)
            except Exception:
                pass

        self._data = CalibrationData()
        return self.save()

    def recalibrate_from_history(self, features: List[dict]) -> bool:
        """
        Recalibrate from feature history (manual recalibration).

        Args:
            features: List of feature dicts with estimated_time, actual_time, complexity.

        Returns:
            True if recalibration successful.
        """
        # Reset to fresh state
        self._data = CalibrationData()

        for feature in features:
            slug = feature.get('slug', 'unknown')
            complexity = feature.get('complexity', 'STANDARD')
            estimated = self._parse_time(feature.get('estimated_time'))
            actual = self._parse_time(feature.get('actual_time'))

            if estimated and actual:
                self.calibrate(slug, complexity, estimated, actual)

        return True

    @staticmethod
    def _parse_time(time_str: Optional[str]) -> Optional[float]:
        """Parse time string to minutes.

        Supported formats:
        - "30min", "30m", "30" → 30 minutes
        - "1h", "1h 30m", "1h30min" → 60, 90, 90 minutes
        - "1.5h" → 90 minutes
        """
        if not time_str:
            return None

        try:
            # Normalize common formats
            time_str = time_str.lower().strip()
            time_str = time_str.replace('min', 'm').replace('hr', 'h').replace('hour', 'h')

            # Handle "Xh Ym" format
            if 'h' in time_str:
                parts = time_str.replace('h', ' ').replace('m', '').split()
                hours = float(parts[0])
                minutes = float(parts[1]) if len(parts) > 1 else 0
                return hours * 60 + minutes
            elif 'm' in time_str:
                return float(time_str.replace('m', '').strip())
            else:
                return float(time_str)
        except (ValueError, IndexError):
            return None


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'CalibrationData',
    'CalibrationFactor',
    'CalibrationEvent',
    'CalibrationManager',
    'calculate_ema',
    'calculate_accuracy',
    'calculate_calibration_ratio',
    'calculate_confidence',
    'determine_trend',
]
