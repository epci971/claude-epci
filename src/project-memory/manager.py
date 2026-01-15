#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Project Memory Manager

Core module for managing project memory in target projects.
Handles loading, saving, validation, and migration of memory data.

Usage:
    from project_memory import ProjectMemoryManager

    manager = ProjectMemoryManager()
    context = manager.load_context()
    manager.save_feature_history(feature_data)
"""

import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_SCHEMA_VERSION = "1.0.0"
MEMORY_DIR_NAME = ".project-memory"

# Subdirectories in .project-memory/
SUBDIRS = [
    "history/features",
    "history/decisions",
    "patterns",
    "metrics",
    "learning",
]

# Core files
CORE_FILES = [
    "context.json",
    "conventions.json",
    "settings.json",
]


# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class ProjectInfo:
    """Project identification and stack information."""
    name: str = ""
    stack: str = "unknown"
    detected_at: Optional[str] = None
    framework_version: Optional[str] = None
    language_version: Optional[str] = None
    root_path: Optional[str] = None


@dataclass
class TeamInfo:
    """Team and developer information."""
    primary_developer: Optional[str] = None
    code_style: Optional[str] = None


@dataclass
class IntegrationConfig:
    """Integration configuration (GitHub, Notion, etc.)."""
    enabled: bool = False
    repository: Optional[str] = None
    branch_pattern: str = "feature/{slug}"
    workspace_id: Optional[str] = None
    features_database: Optional[str] = None


@dataclass
class EpciInfo:
    """EPCI plugin metadata."""
    plugin_version: str = "5.3.0"
    features_completed: int = 0
    last_session: Optional[str] = None
    initialized_at: Optional[str] = None


@dataclass
class ProjectContext:
    """Complete project context."""
    version: str = CURRENT_SCHEMA_VERSION
    project: ProjectInfo = field(default_factory=ProjectInfo)
    team: TeamInfo = field(default_factory=TeamInfo)
    integrations: Dict[str, Any] = field(default_factory=dict)
    epci: EpciInfo = field(default_factory=EpciInfo)

    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectContext':
        """Create from dictionary with nested object handling."""
        return cls(
            version=data.get('version', CURRENT_SCHEMA_VERSION),
            project=ProjectInfo(**data.get('project', {})),
            team=TeamInfo(**data.get('team', {})),
            integrations=data.get('integrations', {}),
            epci=EpciInfo(**{k: v for k, v in data.get('epci', {}).items()
                            if k in EpciInfo.__dataclass_fields__}),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'project': asdict(self.project),
            'team': asdict(self.team),
            'integrations': self.integrations,
            'epci': asdict(self.epci),
        }


@dataclass
class NamingConventions:
    """Naming conventions for the project."""
    entities: str = "PascalCase"
    services: str = "{Name}Service"
    repositories: str = "{Entity}Repository"
    controllers: str = "{Domain}Controller"
    components: str = "PascalCase"
    hooks: str = "use{Name}"


@dataclass
class StructureConventions:
    """Project structure conventions."""
    src_location: str = "src/"
    tests_location: str = "tests/"
    test_suffix: str = "Test"
    test_pattern: str = "{Name}Test"
    feature_tests_pattern: Optional[str] = None


@dataclass
class CodeStyleConventions:
    """Code formatting conventions."""
    max_line_length: int = 120
    indent: str = "spaces"
    indent_size: int = 4
    quotes: str = "single"
    semicolons: bool = True
    trailing_comma: str = "es5"


@dataclass
class Conventions:
    """Complete conventions configuration."""
    version: str = CURRENT_SCHEMA_VERSION
    naming: NamingConventions = field(default_factory=NamingConventions)
    structure: StructureConventions = field(default_factory=StructureConventions)
    code_style: CodeStyleConventions = field(default_factory=CodeStyleConventions)
    detected_at: Optional[str] = None
    manual_overrides: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'Conventions':
        """Create from dictionary."""
        naming_data = data.get('naming', {})
        structure_data = data.get('structure', {})
        code_style_data = data.get('code_style', {})

        return cls(
            version=data.get('version', CURRENT_SCHEMA_VERSION),
            naming=NamingConventions(**{k: v for k, v in naming_data.items()
                                        if k in NamingConventions.__dataclass_fields__}),
            structure=StructureConventions(**{k: v for k, v in structure_data.items()
                                              if k in StructureConventions.__dataclass_fields__}),
            code_style=CodeStyleConventions(**{k: v for k, v in code_style_data.items()
                                               if k in CodeStyleConventions.__dataclass_fields__}),
            detected_at=data.get('detected_at'),
            manual_overrides=data.get('manual_overrides', []),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'version': self.version,
            'naming': asdict(self.naming),
            'structure': asdict(self.structure),
            'code_style': asdict(self.code_style),
            'detected_at': self.detected_at,
            'manual_overrides': self.manual_overrides,
        }


@dataclass
class FeatureHistory:
    """Feature development history entry."""
    slug: str
    title: str
    created_at: str
    complexity: str
    completed_at: Optional[str] = None
    complexity_score: float = 0.5
    files_modified: List[str] = field(default_factory=list)
    files_created: int = 0
    files_updated: int = 0
    loc_added: int = 0
    loc_removed: int = 0
    tests_created: int = 0
    test_coverage: Optional[float] = None
    estimated_time: Optional[str] = None
    actual_time: Optional[str] = None
    phases: Dict[str, str] = field(default_factory=dict)
    agents_used: List[str] = field(default_factory=list)
    issues_found: Dict[str, int] = field(default_factory=dict)
    related_features: List[str] = field(default_factory=list)
    feature_document: Optional[str] = None
    commit_hash: Optional[str] = None
    branch: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'FeatureHistory':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ComplexityStats:
    """Statistics for a complexity category."""
    count: int = 0
    avg_time: Optional[str] = None
    avg_files: Optional[float] = None
    avg_loc: Optional[float] = None


@dataclass
class VelocityMetrics:
    """Velocity and estimation metrics."""
    version: str = CURRENT_SCHEMA_VERSION
    total_features: int = 0
    avg_time_tiny: Optional[str] = None
    avg_time_small: Optional[str] = None
    avg_time_standard: Optional[str] = None
    avg_time_large: Optional[str] = None
    estimation_accuracy: Optional[float] = None
    by_complexity: Dict[str, ComplexityStats] = field(default_factory=dict)
    last_5_features: List[Dict] = field(default_factory=list)
    velocity_trend: str = "stable"
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'VelocityMetrics':
        """Create from dictionary."""
        summary = data.get('summary', {})
        by_complexity = {}
        for key, value in data.get('by_complexity', {}).items():
            by_complexity[key] = ComplexityStats(**value) if isinstance(value, dict) else value

        return cls(
            version=data.get('version', CURRENT_SCHEMA_VERSION),
            total_features=summary.get('total_features', 0),
            avg_time_tiny=summary.get('avg_time_tiny'),
            avg_time_small=summary.get('avg_time_small'),
            avg_time_standard=summary.get('avg_time_standard'),
            avg_time_large=summary.get('avg_time_large'),
            estimation_accuracy=summary.get('estimation_accuracy'),
            by_complexity=by_complexity,
            last_5_features=data.get('trend', {}).get('last_5_features', []),
            velocity_trend=data.get('trend', {}).get('velocity_trend', 'stable'),
            updated_at=data.get('updated_at'),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary matching schema structure."""
        return {
            'version': self.version,
            'summary': {
                'total_features': self.total_features,
                'avg_time_tiny': self.avg_time_tiny,
                'avg_time_small': self.avg_time_small,
                'avg_time_standard': self.avg_time_standard,
                'avg_time_large': self.avg_time_large,
                'estimation_accuracy': self.estimation_accuracy,
            },
            'by_complexity': {
                k: asdict(v) if isinstance(v, ComplexityStats) else v
                for k, v in self.by_complexity.items()
            },
            'trend': {
                'last_5_features': self.last_5_features,
                'velocity_trend': self.velocity_trend,
            },
            'updated_at': self.updated_at,
        }


@dataclass
class Settings:
    """EPCI settings for the project."""
    version: str = CURRENT_SCHEMA_VERSION
    hooks: Dict[str, Any] = field(default_factory=lambda: {
        'enabled': True,
        'timeout_seconds': 30,
        'fail_on_error': False,
        'active': [],
    })
    breakpoints: Dict[str, Any] = field(default_factory=lambda: {
        'show_metrics': True,
        'show_preview': True,
        'auto_continue_tiny': False,
    })
    flags: Dict[str, Any] = field(default_factory=lambda: {
        'default_thinking': None,
        'auto_safe_for_sensitive': True,
        'auto_uc_threshold': 0.75,
    })
    memory: Dict[str, Any] = field(default_factory=lambda: {
        'auto_save_features': True,
        'track_velocity': True,
        'detect_patterns': True,
        'backup_before_save': True,
    })
    integrations: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'Settings':
        """Create from dictionary."""
        return cls(
            version=data.get('version', CURRENT_SCHEMA_VERSION),
            hooks=data.get('hooks', cls.__dataclass_fields__['hooks'].default_factory()),
            breakpoints=data.get('breakpoints', cls.__dataclass_fields__['breakpoints'].default_factory()),
            flags=data.get('flags', cls.__dataclass_fields__['flags'].default_factory()),
            memory=data.get('memory', cls.__dataclass_fields__['memory'].default_factory()),
            integrations=data.get('integrations', {}),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'version': self.version,
            'hooks': self.hooks,
            'breakpoints': self.breakpoints,
            'flags': self.flags,
            'memory': self.memory,
            'integrations': self.integrations,
        }


# =============================================================================
# MIGRATION SYSTEM
# =============================================================================

# Migration functions: (from_version, to_version) -> migration_func
MIGRATIONS: Dict[tuple, callable] = {
    # Example: ("1.0.0", "1.1.0"): migrate_1_0_to_1_1,
}


def get_migration_path(from_version: str, to_version: str) -> List[tuple]:
    """Get the sequence of migrations needed."""
    # For now, simple direct migration
    # Future: implement full migration graph traversal
    if from_version == to_version:
        return []
    if (from_version, to_version) in MIGRATIONS:
        return [(from_version, to_version)]
    return []


# =============================================================================
# PROJECT MEMORY MANAGER
# =============================================================================

class ProjectMemoryManager:
    """
    Manages project memory in target projects.

    The memory is stored in .project-memory/ directory at the project root.
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the manager.

        Args:
            project_root: Path to project root. Defaults to current directory.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.memory_dir = self.project_root / MEMORY_DIR_NAME
        self._templates_dir = Path(__file__).parent / "templates"

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def is_initialized(self) -> bool:
        """Check if project memory is initialized."""
        return self.memory_dir.exists() and (self.memory_dir / "context.json").exists()

    def init_memory(self, detected_context: Optional[Dict] = None) -> bool:
        """
        Initialize project memory structure.

        Args:
            detected_context: Pre-detected context (stack, conventions) from detector.

        Returns:
            True if initialization successful.
        """
        try:
            # Create main directory
            self.memory_dir.mkdir(exist_ok=True)

            # Create subdirectories
            for subdir in SUBDIRS:
                (self.memory_dir / subdir).mkdir(parents=True, exist_ok=True)

            # Create core files from templates
            now = datetime.utcnow().isoformat() + "Z"

            # Context
            context = self._load_template("context.json")
            context['epci']['initialized_at'] = now
            context['project']['root_path'] = str(self.project_root)

            if detected_context:
                # Merge detected values
                if 'project' in detected_context:
                    context['project'].update(detected_context['project'])
                    context['project']['detected_at'] = now
                if 'team' in detected_context:
                    context['team'].update(detected_context['team'])

            self._atomic_write(self.memory_dir / "context.json", context)

            # Conventions
            conventions = self._load_template("conventions.json")
            if detected_context and 'conventions' in detected_context:
                self._deep_merge(conventions, detected_context['conventions'])
                conventions['detected_at'] = now
            self._atomic_write(self.memory_dir / "conventions.json", conventions)

            # Settings
            settings = self._load_template("settings.json")
            self._atomic_write(self.memory_dir / "settings.json", settings)

            # Velocity (in metrics/)
            velocity = self._load_template("velocity.json")
            self._atomic_write(self.memory_dir / "metrics" / "velocity.json", velocity)

            # Create empty pattern files
            self._atomic_write(self.memory_dir / "patterns" / "detected.json", {"patterns": [], "detected_at": now})
            self._atomic_write(self.memory_dir / "patterns" / "custom.json", {"patterns": []})

            # Create empty learning files
            self._atomic_write(self.memory_dir / "learning" / "corrections.json", {"corrections": []})
            self._atomic_write(self.memory_dir / "learning" / "preferences.json", {"preferences": {}})

            # Create quality metrics placeholder
            self._atomic_write(self.memory_dir / "metrics" / "quality.json", {
                "version": CURRENT_SCHEMA_VERSION,
                "metrics": {},
                "updated_at": None
            })

            return True

        except Exception as e:
            print(f"Error initializing project memory: {e}")
            return False

    # -------------------------------------------------------------------------
    # Loading
    # -------------------------------------------------------------------------

    def load_context(self) -> ProjectContext:
        """Load project context with graceful degradation."""
        return self._load_file("context.json", ProjectContext)

    def load_conventions(self) -> Conventions:
        """Load project conventions with graceful degradation."""
        return self._load_file("conventions.json", Conventions)

    def load_settings(self) -> Settings:
        """Load project settings with graceful degradation."""
        return self._load_file("settings.json", Settings)

    def load_velocity(self) -> VelocityMetrics:
        """Load velocity metrics with graceful degradation."""
        return self._load_file("metrics/velocity.json", VelocityMetrics)

    def load_feature_history(self, slug: str) -> Optional[FeatureHistory]:
        """Load a specific feature's history."""
        file_path = self.memory_dir / "history" / "features" / f"{slug}.json"
        if not file_path.exists():
            return None
        try:
            data = self._read_json(file_path)
            return FeatureHistory.from_dict(data)
        except Exception:
            return None

    def list_features(self) -> List[str]:
        """List all feature slugs in history."""
        features_dir = self.memory_dir / "history" / "features"
        if not features_dir.exists():
            return []
        return [f.stem for f in features_dir.glob("*.json")]

    def get_all_feature_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all features (for similarity matching).

        Returns:
            List of dicts with slug, title, complexity, files_modified.
            Empty list if Project Memory unavailable (graceful degradation).
        """
        try:
            features = []
            for slug in self.list_features():
                feature = self.load_feature_history(slug)
                if feature:
                    features.append({
                        'slug': feature.slug,
                        'title': feature.title,
                        'complexity': feature.complexity,
                        'files_modified': feature.files_modified,
                        'completed_at': feature.completed_at,
                    })
            return features
        except Exception:
            # Graceful degradation
            return []

    def find_similar_features(
        self,
        keywords: List[str],
        threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Find features similar to given keywords.

        Uses Jaccard similarity on feature titles and slugs.

        Args:
            keywords: List of keywords from brief analysis.
            threshold: Minimum similarity score (default 0.3).

        Returns:
            List of similar features with scores.
            Empty list if no matches or Project Memory unavailable.
        """
        try:
            from .similarity_matcher import find_similar_features as _find_similar

            features = self.get_all_feature_metadata()
            if not features:
                return []

            matches = _find_similar(features, keywords, threshold)
            return [
                {
                    'slug': m.slug,
                    'title': m.title,
                    'score': m.score,
                    'matched_keywords': m.matched_keywords,
                    'complexity': m.complexity,
                    'files_modified': m.files_modified,
                }
                for m in matches
            ]
        except Exception:
            # Graceful degradation
            return []

    def get_patterns_for_domain(self, domain: str) -> List[str]:
        """
        Get detected patterns relevant to a domain.

        Args:
            domain: Domain name (auth, api, ui, data, etc.).

        Returns:
            List of pattern names.
            Empty list if unavailable (graceful degradation).
        """
        try:
            patterns_file = self.memory_dir / "patterns" / "detected.json"
            if not patterns_file.exists():
                return []

            data = self._read_json(patterns_file)
            all_patterns = data.get('patterns', [])

            # Domain-pattern mapping
            domain_patterns = {
                'auth': ['mvc', 'service', 'repository'],
                'api': ['mvc', 'rest', 'dto', 'service'],
                'ui': ['component', 'mvc', 'state'],
                'data': ['repository', 'entity', 'ddd'],
                'infra': ['config', 'pipeline'],
                'notification': ['event-driven', 'queue', 'observer'],
                'payment': ['service', 'gateway', 'facade'],
                'search': ['repository', 'index', 'query'],
            }

            relevant = domain_patterns.get(domain, [])
            return [p for p in all_patterns if any(r in p.lower() for r in relevant)]
        except Exception:
            # Graceful degradation
            return []

    def _load_file(self, relative_path: str, dataclass_type):
        """Generic file loader with graceful degradation."""
        file_path = self.memory_dir / relative_path

        if not file_path.exists():
            # Return default instance
            print(f"Warning: {relative_path} not found, using defaults")
            return dataclass_type()

        try:
            data = self._read_json(file_path)

            # Check version and migrate if needed
            file_version = data.get('version', '1.0.0')
            if file_version != CURRENT_SCHEMA_VERSION:
                data = self._migrate(data, file_version, CURRENT_SCHEMA_VERSION)

            return dataclass_type.from_dict(data)

        except json.JSONDecodeError as e:
            print(f"Warning: {relative_path} is corrupted ({e}), using defaults")
            return dataclass_type()
        except Exception as e:
            print(f"Warning: Error loading {relative_path} ({e}), using defaults")
            return dataclass_type()

    # -------------------------------------------------------------------------
    # Saving
    # -------------------------------------------------------------------------

    def save_context(self, context: ProjectContext) -> bool:
        """Save project context."""
        return self._save_file("context.json", context.to_dict())

    def save_conventions(self, conventions: Conventions) -> bool:
        """Save project conventions."""
        return self._save_file("conventions.json", conventions.to_dict())

    def save_settings(self, settings: Settings) -> bool:
        """Save project settings."""
        return self._save_file("settings.json", settings.to_dict())

    def save_velocity(self, velocity: VelocityMetrics) -> bool:
        """Save velocity metrics."""
        velocity.updated_at = datetime.utcnow().isoformat() + "Z"
        return self._save_file("metrics/velocity.json", velocity.to_dict())

    def save_feature_history(self, feature: Union[FeatureHistory, dict]) -> bool:
        """Save a feature's history."""
        if isinstance(feature, dict):
            feature = FeatureHistory.from_dict(feature)

        file_path = self.memory_dir / "history" / "features" / f"{feature.slug}.json"
        return self._atomic_write(file_path, feature.to_dict())

    def _save_file(self, relative_path: str, data: dict) -> bool:
        """Generic file saver with atomic write."""
        file_path = self.memory_dir / relative_path
        return self._atomic_write(file_path, data)

    # -------------------------------------------------------------------------
    # Export / Reset
    # -------------------------------------------------------------------------

    def export_all(self) -> dict:
        """Export all memory data as a single dictionary."""
        return {
            'context': self.load_context().to_dict(),
            'conventions': self.load_conventions().to_dict(),
            'settings': self.load_settings().to_dict(),
            'velocity': self.load_velocity().to_dict(),
            'features': {
                slug: self.load_feature_history(slug).to_dict()
                for slug in self.list_features()
                if self.load_feature_history(slug)
            },
            'exported_at': datetime.utcnow().isoformat() + "Z",
        }

    def reset(self, backup: bool = True) -> bool:
        """
        Reset project memory.

        Args:
            backup: If True, create backup before reset.

        Returns:
            True if reset successful.
        """
        if not self.memory_dir.exists():
            return True

        try:
            if backup:
                backup_path = self.memory_dir.parent / f".project-memory-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                shutil.copytree(self.memory_dir, backup_path)

            shutil.rmtree(self.memory_dir)
            return True
        except Exception as e:
            print(f"Error resetting project memory: {e}")
            return False

    # -------------------------------------------------------------------------
    # Velocity Update
    # -------------------------------------------------------------------------

    def update_velocity_from_feature(self, feature: FeatureHistory) -> bool:
        """Update velocity metrics after feature completion."""
        velocity = self.load_velocity()

        # Increment total
        velocity.total_features += 1

        # Update by_complexity
        complexity = feature.complexity
        if complexity not in velocity.by_complexity:
            velocity.by_complexity[complexity] = ComplexityStats()

        stats = velocity.by_complexity[complexity]
        if isinstance(stats, dict):
            stats = ComplexityStats(**stats)
            velocity.by_complexity[complexity] = stats

        stats.count += 1

        # Update last_5_features
        velocity.last_5_features.append({
            'slug': feature.slug,
            'complexity': feature.complexity,
            'estimated': feature.estimated_time,
            'actual': feature.actual_time,
        })
        velocity.last_5_features = velocity.last_5_features[-5:]  # Keep only last 5

        return self.save_velocity(velocity)

    # -------------------------------------------------------------------------
    # Learning & Calibration (F08)
    # -------------------------------------------------------------------------

    def get_calibration_manager(self):
        """
        Get the CalibrationManager instance.

        Returns:
            CalibrationManager for calibration operations.
        """
        try:
            from .calibration import CalibrationManager
            return CalibrationManager(self.memory_dir)
        except ImportError:
            return None

    def get_learning_analyzer(self):
        """
        Get the LearningAnalyzer instance.

        Returns:
            LearningAnalyzer for learning operations.
        """
        try:
            from .learning_analyzer import LearningAnalyzer
            return LearningAnalyzer(self.memory_dir)
        except ImportError:
            return None

    def trigger_calibration(self, feature: FeatureHistory) -> bool:
        """
        Trigger calibration after feature completion.

        Args:
            feature: Completed feature with estimated/actual times.

        Returns:
            True if calibration successful.
        """
        try:
            calibration = self.get_calibration_manager()
            if not calibration:
                return False

            # Parse times
            estimated = self._parse_time_to_minutes(feature.estimated_time)
            actual = self._parse_time_to_minutes(feature.actual_time)

            if not estimated or not actual:
                return False

            calibration.calibrate(
                feature_slug=feature.slug,
                complexity=feature.complexity,
                estimated=estimated,
                actual=actual,
            )
            return True
        except Exception:
            # Graceful degradation
            return False

    def record_suggestion_feedback(
        self,
        pattern: str,
        action: str
    ) -> bool:
        """
        Record user feedback on a suggestion.

        Args:
            pattern: Pattern identifier (e.g., "test-coverage", "n1-query").
            action: "accepted", "rejected", "ignored", or "disabled"

        Returns:
            True if recorded successfully.
        """
        try:
            analyzer = self.get_learning_analyzer()
            if not analyzer:
                return False

            return analyzer.record_feedback(pattern, action)
        except Exception:
            return False

    def record_correction(self, correction: dict) -> bool:
        """
        Record a correction for pattern detection.

        Args:
            correction: Dict with pattern_id, type, severity, reason, etc.

        Returns:
            True if recorded successfully.
        """
        try:
            analyzer = self.get_learning_analyzer()
            if not analyzer:
                return False

            return analyzer.record_correction(correction)
        except Exception:
            return False

    def get_learning_status(self) -> dict:
        """
        Get combined learning status (calibration + preferences).

        Returns:
            Dictionary with complete learning status.
        """
        status = {
            'calibration': {},
            'learning': {},
            'available': False,
        }

        try:
            calibration = self.get_calibration_manager()
            if calibration:
                status['calibration'] = calibration.get_status()
                status['available'] = True

            analyzer = self.get_learning_analyzer()
            if analyzer:
                status['learning'] = analyzer.get_status()
                status['available'] = True
        except Exception:
            pass

        return status

    def reset_learning(self, backup: bool = True) -> bool:
        """
        Reset all learning data (calibration + preferences).

        Args:
            backup: Whether to create backups.

        Returns:
            True if reset successful.
        """
        success = True

        try:
            calibration = self.get_calibration_manager()
            if calibration:
                success = calibration.reset(backup) and success

            analyzer = self.get_learning_analyzer()
            if analyzer:
                success = analyzer.reset(backup) and success
        except Exception:
            success = False

        return success

    def export_learning(self) -> dict:
        """
        Export all learning data.

        Returns:
            Dictionary with all learning data.
        """
        export = {
            'calibration': {},
            'preferences': {},
            'corrections': {},
            'exported_at': datetime.utcnow().isoformat() + "Z",
        }

        try:
            calibration = self.get_calibration_manager()
            if calibration:
                data = calibration.load()
                export['calibration'] = data.to_dict()

            analyzer = self.get_learning_analyzer()
            if analyzer:
                prefs = analyzer.load_preferences()
                export['preferences'] = prefs.to_dict()

                corrections = analyzer.load_corrections()
                export['corrections'] = corrections.to_dict()
        except Exception:
            pass

        return export

    def _parse_time_to_minutes(self, time_str: Optional[str]) -> Optional[float]:
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

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _load_template(self, filename: str) -> dict:
        """Load a template file."""
        template_path = self._templates_dir / filename
        if template_path.exists():
            return self._read_json(template_path)
        return {}

    def _read_json(self, path: Path) -> dict:
        """Read JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _atomic_write(self, path: Path, data: dict) -> bool:
        """
        Write JSON file atomically to prevent corruption.

        Writes to a temp file first, then moves to target.
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file
            fd, temp_path = tempfile.mkstemp(suffix='.json', dir=path.parent)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Atomic move
                shutil.move(temp_path, path)
                return True
            except Exception:
                # Clean up temp file on error
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise
        except Exception as e:
            print(f"Error writing {path}: {e}")
            return False

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Deep merge two dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def _migrate(self, data: dict, from_version: str, to_version: str) -> dict:
        """Migrate data between schema versions."""
        path = get_migration_path(from_version, to_version)

        for from_v, to_v in path:
            migration_func = MIGRATIONS.get((from_v, to_v))
            if migration_func:
                data = migration_func(data)
                data['version'] = to_v

        return data


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='EPCI Project Memory Manager')
    parser.add_argument('command', choices=['init', 'status', 'export', 'reset'],
                        help='Command to execute')
    parser.add_argument('--project', '-p', type=str, default='.',
                        help='Project root directory')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force operation without confirmation')

    args = parser.parse_args()

    manager = ProjectMemoryManager(Path(args.project))

    if args.command == 'init':
        if manager.is_initialized() and not args.force:
            print("Project memory already initialized. Use --force to reinitialize.")
            return 1
        if manager.init_memory():
            print(f"Project memory initialized at {manager.memory_dir}")
            return 0
        return 1

    elif args.command == 'status':
        if not manager.is_initialized():
            print("Project memory not initialized. Run 'init' first.")
            return 1

        context = manager.load_context()
        velocity = manager.load_velocity()
        features = manager.list_features()

        print(f"Project: {context.project.name or '(unnamed)'}")
        print(f"Stack: {context.project.stack}")
        print(f"Features completed: {velocity.total_features}")
        print(f"Features in history: {len(features)}")
        print(f"Initialized: {context.epci.initialized_at}")
        return 0

    elif args.command == 'export':
        if not manager.is_initialized():
            print("Project memory not initialized.")
            return 1

        data = manager.export_all()
        print(json.dumps(data, indent=2))
        return 0

    elif args.command == 'reset':
        if not manager.is_initialized():
            print("Project memory not initialized.")
            return 0

        if not args.force:
            confirm = input("Are you sure you want to reset project memory? (y/N): ")
            if confirm.lower() != 'y':
                print("Cancelled.")
                return 0

        if manager.reset(backup=True):
            print("Project memory reset. Backup created.")
            return 0
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
