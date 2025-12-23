"""
EPCI Project Memory Module

Provides persistence for project context, conventions, and feature history.
Data is stored in .project-memory/ directory in target projects.

F08 additions: Calibration and Learning Analyzer for continuous learning.
"""

from .manager import (
    ProjectMemoryManager,
    ProjectContext,
    Conventions,
    FeatureHistory,
    VelocityMetrics,
    Settings,
    CURRENT_SCHEMA_VERSION,
)

from .calibration import (
    CalibrationManager,
    CalibrationData,
    CalibrationFactor,
    calculate_ema,
    calculate_accuracy,
)

from .learning_analyzer import (
    LearningAnalyzer,
    LearningPreferences,
    SuggestionFeedback,
    calculate_suggestion_score,
    calculate_recency_factor,
)

__all__ = [
    # Manager
    'ProjectMemoryManager',
    'ProjectContext',
    'Conventions',
    'FeatureHistory',
    'VelocityMetrics',
    'Settings',
    'CURRENT_SCHEMA_VERSION',
    # Calibration (F08)
    'CalibrationManager',
    'CalibrationData',
    'CalibrationFactor',
    'calculate_ema',
    'calculate_accuracy',
    # Learning (F08)
    'LearningAnalyzer',
    'LearningPreferences',
    'SuggestionFeedback',
    'calculate_suggestion_score',
    'calculate_recency_factor',
]

__version__ = '1.1.0'  # Bumped for F08
