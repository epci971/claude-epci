#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Pattern Catalog

Declarative registry of detectable code patterns for proactive suggestions.
Part of F06 Proactive Suggestions feature.

Usage:
    from project_memory.patterns import get_pattern, get_patterns_by_priority

    pattern = get_pattern("input-not-validated")
    p1_patterns = get_patterns_by_priority(Priority.P1)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


# =============================================================================
# ENUMS
# =============================================================================

class Priority(Enum):
    """Suggestion priority levels."""
    P1 = 1  # Critical - Security, bugs
    P2 = 2  # Normal - Quality, performance
    P3 = 3  # Low - Style, optimization


class Category(Enum):
    """Pattern categories."""
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"


# =============================================================================
# PATTERN DEFINITION
# =============================================================================

@dataclass
class PatternDefinition:
    """Definition of a detectable code pattern."""
    id: str
    name: str
    category: Category
    priority: Priority
    description: str
    detection_hint: str
    suggestion: str
    file_patterns: List[str] = field(default_factory=list)
    code_patterns: List[str] = field(default_factory=list)
    severity: str = "minor"  # critical, important, minor
    auto_fixable: bool = False
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'priority': self.priority.name,
            'description': self.description,
            'detection_hint': self.detection_hint,
            'suggestion': self.suggestion,
            'file_patterns': self.file_patterns,
            'code_patterns': self.code_patterns,
            'severity': self.severity,
            'auto_fixable': self.auto_fixable,
            'tags': self.tags,
        }


# =============================================================================
# PATTERN CATALOG
# =============================================================================

PATTERN_CATALOG: Dict[str, PatternDefinition] = {}

def _register(pattern: PatternDefinition) -> PatternDefinition:
    """Register a pattern in the catalog."""
    PATTERN_CATALOG[pattern.id] = pattern
    return pattern


# -----------------------------------------------------------------------------
# SECURITY PATTERNS (P1)
# -----------------------------------------------------------------------------

_register(PatternDefinition(
    id="input-not-validated",
    name="Input non validé",
    category=Category.SECURITY,
    priority=Priority.P1,
    description="Paramètre utilisateur utilisé sans validation",
    detection_hint="Paramètre de requête ou formulaire utilisé directement sans Assert/Validator",
    suggestion="Ajouter validation avec Assert\\NotBlank, Assert\\Email, ou validator custom",
    file_patterns=["**/Controller/**", "**/Api/**", "**/Handler/**"],
    code_patterns=[
        r"\$request->get\(",
        r"\$_GET\[",
        r"\$_POST\[",
        r"request\.form\[",
        r"request\.args\[",
    ],
    severity="critical",
    auto_fixable=False,
    tags=["security", "validation", "input"],
))

_register(PatternDefinition(
    id="sql-injection",
    name="SQL Injection potentielle",
    category=Category.SECURITY,
    priority=Priority.P1,
    description="Requête SQL construite par concaténation de strings",
    detection_hint="Variables interpolées directement dans une query SQL",
    suggestion="Utiliser des paramètres préparés ou un ORM",
    file_patterns=["**/Repository/**", "**/Service/**", "**/Model/**"],
    code_patterns=[
        r"\"SELECT.*\+.*\"",
        r"'SELECT.*\+.*'",
        r"f\"SELECT.*\{",
        r"\.query\(.*\+",
        r"\.execute\(.*%",
    ],
    severity="critical",
    auto_fixable=False,
    tags=["security", "sql", "injection"],
))

_register(PatternDefinition(
    id="xss-vulnerability",
    name="XSS Vulnerability",
    category=Category.SECURITY,
    priority=Priority.P1,
    description="Output non échappé pouvant permettre XSS",
    detection_hint="Variable affichée sans échappement dans template ou response",
    suggestion="Échapper avec htmlspecialchars() ou utiliser |escape dans Twig",
    file_patterns=["**/templates/**", "**/views/**", "**/*.html", "**/*.twig"],
    code_patterns=[
        r"\{\{.*\|raw\}\}",
        r"echo\s+\$",
        r"print\s+\$",
        r"innerHTML\s*=",
        r"v-html=",
    ],
    severity="critical",
    auto_fixable=False,
    tags=["security", "xss", "output"],
))

_register(PatternDefinition(
    id="csrf-missing",
    name="CSRF Token manquant",
    category=Category.SECURITY,
    priority=Priority.P1,
    description="Formulaire POST sans protection CSRF",
    detection_hint="Formulaire avec method POST sans csrf_token",
    suggestion="Ajouter {{ csrf_token() }} ou @csrf dans le formulaire",
    file_patterns=["**/templates/**", "**/views/**", "**/*.html", "**/*.blade.php"],
    code_patterns=[
        r"<form[^>]*method=[\"']post[\"'][^>]*>(?!.*csrf)",
        r"method=\"POST\"(?!.*_token)",
    ],
    severity="critical",
    auto_fixable=True,
    tags=["security", "csrf", "form"],
))

_register(PatternDefinition(
    id="auth-missing",
    name="Authentification manquante",
    category=Category.SECURITY,
    priority=Priority.P1,
    description="Endpoint/Controller sans contrôle d'accès",
    detection_hint="Controller ou route sans annotation/middleware d'authentification",
    suggestion="Ajouter @IsGranted, @Security, ou middleware auth",
    file_patterns=["**/Controller/**", "**/routes/**", "**/api/**"],
    code_patterns=[
        r"class\s+\w+Controller(?!.*@IsGranted)",
        r"@Route(?!.*@Security)",
        r"def\s+\w+\(.*request(?!.*@login_required)",
    ],
    severity="critical",
    auto_fixable=False,
    tags=["security", "auth", "access-control"],
))


# -----------------------------------------------------------------------------
# PERFORMANCE PATTERNS (P2)
# -----------------------------------------------------------------------------

_register(PatternDefinition(
    id="n-plus-one-query",
    name="N+1 Query",
    category=Category.PERFORMANCE,
    priority=Priority.P2,
    description="Requête exécutée dans une boucle (N+1 problem)",
    detection_hint="Appel repository/query dans un foreach/for/map",
    suggestion="Utiliser JOIN FETCH, eager loading, ou batch query",
    file_patterns=["**/Service/**", "**/Controller/**", "**/Handler/**"],
    code_patterns=[
        r"foreach.*\{[^}]*->find\(",
        r"for\s*\([^)]*\)[^}]*\.query\(",
        r"\.map\([^)]*=>.*\.find\(",
        r"for.*in.*:.*\.get\(",
    ],
    severity="important",
    auto_fixable=False,
    tags=["performance", "database", "query"],
))

_register(PatternDefinition(
    id="missing-index",
    name="Index manquant probable",
    category=Category.PERFORMANCE,
    priority=Priority.P2,
    description="Query sur colonne probablement non indexée",
    detection_hint="WHERE/ORDER BY sur colonne sans annotation @Index",
    suggestion="Ajouter @Index sur la colonne ou créer migration",
    file_patterns=["**/Entity/**", "**/Model/**", "**/Repository/**"],
    code_patterns=[
        r"findBy\w+\(",
        r"WHERE\s+\w+\s*=",
        r"ORDER BY\s+\w+",
        r"\.filter\(\w+__",
    ],
    severity="minor",
    auto_fixable=False,
    tags=["performance", "database", "index"],
))

_register(PatternDefinition(
    id="large-payload",
    name="Payload volumineux",
    category=Category.PERFORMANCE,
    priority=Priority.P2,
    description="Response potentiellement > 1MB sans pagination",
    detection_hint="findAll() ou SELECT * sans LIMIT/pagination",
    suggestion="Implémenter pagination ou streaming",
    file_patterns=["**/Controller/**", "**/Api/**", "**/Service/**"],
    code_patterns=[
        r"->findAll\(\)",
        r"SELECT \* FROM",
        r"\.all\(\)(?!.*paginate)",
        r"\.find\(\{\}\)",
    ],
    severity="minor",
    auto_fixable=False,
    tags=["performance", "api", "pagination"],
))

_register(PatternDefinition(
    id="no-cache",
    name="Cache manquant",
    category=Category.PERFORMANCE,
    priority=Priority.P2,
    description="Query répétitive sans mise en cache",
    detection_hint="Même query appelée plusieurs fois sans cache",
    suggestion="Ajouter @Cache, Redis, ou cache applicatif",
    file_patterns=["**/Service/**", "**/Repository/**"],
    code_patterns=[
        r"->find\(\d+\)",
        r"->getConfiguration\(",
        r"->getSettings\(",
        r"Config::get\(",
    ],
    severity="minor",
    auto_fixable=False,
    tags=["performance", "cache", "optimization"],
))


# -----------------------------------------------------------------------------
# QUALITY PATTERNS (P2-P3)
# -----------------------------------------------------------------------------

_register(PatternDefinition(
    id="god-class",
    name="God Class",
    category=Category.QUALITY,
    priority=Priority.P2,
    description="Classe dépassant 500 lignes de code",
    detection_hint="Fichier > 500 LOC avec une seule classe",
    suggestion="Découper en classes plus petites par responsabilité",
    file_patterns=["**/*.php", "**/*.py", "**/*.java", "**/*.ts"],
    code_patterns=[],  # Detection by LOC count
    severity="important",
    auto_fixable=False,
    tags=["quality", "solid", "srp"],
))

_register(PatternDefinition(
    id="long-method",
    name="Méthode trop longue",
    category=Category.QUALITY,
    priority=Priority.P2,
    description="Méthode dépassant 50 lignes de code",
    detection_hint="Fonction/méthode > 50 LOC",
    suggestion="Extraire en sous-méthodes avec noms explicites",
    file_patterns=["**/*.php", "**/*.py", "**/*.java", "**/*.ts", "**/*.js"],
    code_patterns=[],  # Detection by LOC count
    severity="minor",
    auto_fixable=False,
    tags=["quality", "readability", "refactoring"],
))

_register(PatternDefinition(
    id="magic-numbers",
    name="Magic Numbers",
    category=Category.QUALITY,
    priority=Priority.P3,
    description="Constantes numériques en dur dans le code",
    detection_hint="Nombres littéraux autres que 0, 1, -1 dans la logique",
    suggestion="Extraire en constantes nommées",
    file_patterns=["**/*.php", "**/*.py", "**/*.java", "**/*.ts", "**/*.js"],
    code_patterns=[
        r"(?<![\d.])[2-9]\d*(?![\d.])",
        r"==\s*\d{2,}",
        r">\s*\d{2,}",
        r"<\s*\d{2,}",
    ],
    severity="minor",
    auto_fixable=False,
    tags=["quality", "readability", "constants"],
))

_register(PatternDefinition(
    id="dead-code",
    name="Code mort",
    category=Category.QUALITY,
    priority=Priority.P3,
    description="Code jamais exécuté ou commenté",
    detection_hint="Return avant fin de fonction, code après throw, blocs commentés",
    suggestion="Supprimer le code mort",
    file_patterns=["**/*.php", "**/*.py", "**/*.java", "**/*.ts", "**/*.js"],
    code_patterns=[
        r"return.*;\s*\n\s*[^}]",
        r"throw.*;\s*\n\s*[^}]",
        r"//.*\n//.*\n//",
        r"#.*\n#.*\n#",
    ],
    severity="minor",
    auto_fixable=True,
    tags=["quality", "cleanup", "dead-code"],
))

_register(PatternDefinition(
    id="duplicate-code",
    name="Code dupliqué",
    category=Category.QUALITY,
    priority=Priority.P2,
    description="Blocs de code similaires > 20 lignes",
    detection_hint="Patterns répétitifs détectés par analyse de similarité",
    suggestion="Extraire méthode commune ou créer abstraction",
    file_patterns=["**/*.php", "**/*.py", "**/*.java", "**/*.ts", "**/*.js"],
    code_patterns=[],  # Detection by similarity analysis
    severity="important",
    auto_fixable=False,
    tags=["quality", "dry", "refactoring"],
))


# =============================================================================
# CATALOG ACCESS FUNCTIONS
# =============================================================================

def get_pattern(pattern_id: str) -> Optional[PatternDefinition]:
    """
    Get a pattern by ID.

    Args:
        pattern_id: Pattern identifier.

    Returns:
        PatternDefinition or None if not found.
    """
    return PATTERN_CATALOG.get(pattern_id)


def get_patterns_by_category(category: Category) -> List[PatternDefinition]:
    """
    Get all patterns in a category.

    Args:
        category: Category enum value.

    Returns:
        List of patterns in the category, sorted by priority.
    """
    patterns = [p for p in PATTERN_CATALOG.values() if p.category == category]
    return sorted(patterns, key=lambda p: p.priority.value)


def get_patterns_by_priority(priority: Priority) -> List[PatternDefinition]:
    """
    Get all patterns with a specific priority.

    Args:
        priority: Priority enum value.

    Returns:
        List of patterns with the priority.
    """
    return [p for p in PATTERN_CATALOG.values() if p.priority == priority]


def get_all_patterns() -> List[PatternDefinition]:
    """
    Get all patterns sorted by priority then category.

    Returns:
        List of all patterns.
    """
    return sorted(
        PATTERN_CATALOG.values(),
        key=lambda p: (p.priority.value, p.category.value)
    )


def get_patterns_for_files(file_paths: List[str]) -> List[PatternDefinition]:
    """
    Get patterns relevant to given file paths.

    Args:
        file_paths: List of file paths to check.

    Returns:
        List of patterns that could apply to these files.
    """
    import fnmatch

    relevant = set()
    for pattern in PATTERN_CATALOG.values():
        for file_path in file_paths:
            for file_pattern in pattern.file_patterns:
                if fnmatch.fnmatch(file_path, file_pattern):
                    relevant.add(pattern.id)
                    break

    return [PATTERN_CATALOG[pid] for pid in relevant]


# =============================================================================
# CATALOG STATS
# =============================================================================

def get_catalog_stats() -> dict:
    """
    Get statistics about the pattern catalog.

    Returns:
        Dictionary with counts by category and priority.
    """
    stats = {
        'total': len(PATTERN_CATALOG),
        'by_category': {},
        'by_priority': {},
    }

    for category in Category:
        count = len(get_patterns_by_category(category))
        stats['by_category'][category.value] = count

    for priority in Priority:
        count = len(get_patterns_by_priority(priority))
        stats['by_priority'][priority.name] = count

    return stats


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'Priority',
    'Category',
    'PatternDefinition',
    'PATTERN_CATALOG',
    'get_pattern',
    'get_patterns_by_category',
    'get_patterns_by_priority',
    'get_all_patterns',
    'get_patterns_for_files',
    'get_catalog_stats',
]
