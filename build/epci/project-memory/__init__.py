"""
EPCI Project Memory Module

Provides persistence for project context, conventions, and feature history.
Data is stored in .project-memory/ directory in target projects.
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

__all__ = [
    'ProjectMemoryManager',
    'ProjectContext',
    'Conventions',
    'FeatureHistory',
    'VelocityMetrics',
    'Settings',
    'CURRENT_SCHEMA_VERSION',
]

__version__ = '1.0.0'
