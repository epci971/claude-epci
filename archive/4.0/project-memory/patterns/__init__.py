#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Patterns Package

Pattern catalog and detection for proactive suggestions.
Part of F06 Proactive Suggestions feature.
"""

from .catalog import (
    PATTERN_CATALOG,
    PatternDefinition,
    Priority,
    Category,
    get_pattern,
    get_patterns_by_category,
    get_patterns_by_priority,
    get_all_patterns,
)

__all__ = [
    'PATTERN_CATALOG',
    'PatternDefinition',
    'Priority',
    'Category',
    'get_pattern',
    'get_patterns_by_category',
    'get_patterns_by_priority',
    'get_all_patterns',
]
