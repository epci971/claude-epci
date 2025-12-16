#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPCI Project Detector

Auto-detects project stack, conventions, and patterns.
Used during project memory initialization.

Usage:
    from project_memory.detector import ProjectDetector

    detector = ProjectDetector(project_root)
    context = detector.detect_all()
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


# =============================================================================
# STACK SIGNATURES
# =============================================================================

STACK_SIGNATURES = {
    'php-symfony': {
        'files': ['composer.json', 'symfony.lock'],
        'patterns': [
            ('composer.json', r'"symfony/framework-bundle"'),
            ('composer.json', r'"symfony/symfony"'),
        ],
        'dirs': ['src/Controller', 'src/Entity', 'config/packages'],
    },
    'php-laravel': {
        'files': ['composer.json', 'artisan'],
        'patterns': [
            ('composer.json', r'"laravel/framework"'),
        ],
        'dirs': ['app/Http/Controllers', 'app/Models', 'routes'],
    },
    'javascript-react': {
        'files': ['package.json'],
        'patterns': [
            ('package.json', r'"react":\s*"'),
            ('package.json', r'"react-dom":\s*"'),
        ],
        'dirs': ['src/components', 'src/hooks'],
    },
    'javascript-vue': {
        'files': ['package.json'],
        'patterns': [
            ('package.json', r'"vue":\s*"'),
        ],
        'dirs': ['src/components', 'src/views'],
    },
    'python-django': {
        'files': ['manage.py', 'requirements.txt', 'pyproject.toml'],
        'patterns': [
            ('requirements.txt', r'django[>=<]'),
            ('pyproject.toml', r'django'),
            ('manage.py', r'django'),
        ],
        'dirs': ['templates', 'static'],
    },
    'python-fastapi': {
        'files': ['requirements.txt', 'pyproject.toml'],
        'patterns': [
            ('requirements.txt', r'fastapi'),
            ('pyproject.toml', r'fastapi'),
        ],
        'dirs': ['app', 'routers'],
    },
    'java-springboot': {
        'files': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
        'patterns': [
            ('pom.xml', r'spring-boot'),
            ('build.gradle', r'org\.springframework\.boot'),
            ('build.gradle.kts', r'org\.springframework\.boot'),
        ],
        'dirs': ['src/main/java', 'src/main/resources'],
    },
}


# =============================================================================
# CONVENTION PATTERNS
# =============================================================================

CONVENTION_PATTERNS = {
    'naming': {
        'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
        'camelCase': r'^[a-z][a-zA-Z0-9]*$',
        'snake_case': r'^[a-z][a-z0-9_]*$',
        'kebab-case': r'^[a-z][a-z0-9-]*$',
    },
    'test_patterns': {
        'php': [
            ('tests/', r'Test\.php$'),
            ('tests/Unit/', r'Test\.php$'),
            ('tests/Feature/', r'Test\.php$'),
        ],
        'javascript': [
            ('__tests__/', r'\.(test|spec)\.(js|ts|jsx|tsx)$'),
            ('src/', r'\.(test|spec)\.(js|ts|jsx|tsx)$'),
            ('tests/', r'\.(test|spec)\.(js|ts|jsx|tsx)$'),
        ],
        'python': [
            ('tests/', r'test_.*\.py$'),
            ('tests/', r'.*_test\.py$'),
        ],
        'java': [
            ('src/test/java/', r'Test\.java$'),
            ('src/test/java/', r'.*Tests\.java$'),
        ],
    },
    'code_style': {
        'php': {
            'psr12': ['phpcs.xml', 'phpcs.xml.dist', '.php-cs-fixer.php'],
            'symfony': ['ecs.php', '.ecs.php'],
        },
        'javascript': {
            'eslint': ['.eslintrc', '.eslintrc.js', '.eslintrc.json', 'eslint.config.js'],
            'prettier': ['.prettierrc', '.prettierrc.js', '.prettierrc.json', 'prettier.config.js'],
        },
        'python': {
            'black': ['pyproject.toml', '.black'],
            'flake8': ['.flake8', 'setup.cfg'],
            'ruff': ['ruff.toml', 'pyproject.toml'],
        },
    },
}


# =============================================================================
# ARCHITECTURE PATTERNS
# =============================================================================

ARCHITECTURE_PATTERNS = {
    'mvc': {
        'indicators': ['Controller', 'Model', 'View'],
        'dirs': ['controllers', 'models', 'views'],
    },
    'hexagonal': {
        'indicators': ['Domain', 'Application', 'Infrastructure'],
        'dirs': ['Domain', 'Application', 'Infrastructure'],
    },
    'ddd': {
        'indicators': ['Entity', 'ValueObject', 'Repository', 'Aggregate'],
        'dirs': ['Entity', 'ValueObject', 'Repository'],
    },
    'clean_architecture': {
        'indicators': ['UseCase', 'Entity', 'Gateway', 'Presenter'],
        'dirs': ['usecases', 'entities', 'gateways'],
    },
    'cqrs': {
        'indicators': ['Command', 'Query', 'Handler'],
        'dirs': ['Command', 'Query'],
    },
}


# =============================================================================
# DETECTOR CLASS
# =============================================================================

@dataclass
class DetectionResult:
    """Result of project detection."""
    stack: str
    stack_confidence: float
    framework_version: Optional[str]
    language_version: Optional[str]
    conventions: Dict[str, Any]
    patterns: List[str]
    code_style: Optional[str]


class ProjectDetector:
    """
    Detects project stack, conventions, and patterns.
    """

    def __init__(self, project_root: Path):
        """
        Initialize detector.

        Args:
            project_root: Path to project root directory.
        """
        self.project_root = Path(project_root)
        self._file_cache: Dict[str, str] = {}

    def detect_all(self) -> Dict[str, Any]:
        """
        Detect all project characteristics.

        Returns:
            Dictionary with 'project', 'conventions', 'patterns' keys.
        """
        stack, confidence = self.detect_stack()
        conventions = self.detect_conventions(stack)
        patterns = self.detect_patterns()

        return {
            'project': {
                'name': self._detect_project_name(),
                'stack': stack,
                'framework_version': self._detect_framework_version(stack),
                'language_version': self._detect_language_version(stack),
            },
            'conventions': conventions,
            'patterns': patterns,
        }

    # -------------------------------------------------------------------------
    # Stack Detection
    # -------------------------------------------------------------------------

    def detect_stack(self) -> Tuple[str, float]:
        """
        Detect the project's technology stack.

        Returns:
            Tuple of (stack_name, confidence_score)
        """
        scores: Dict[str, float] = {}

        for stack_name, signature in STACK_SIGNATURES.items():
            score = 0.0
            max_score = 0.0

            # Check for files
            for filename in signature.get('files', []):
                max_score += 1.0
                if (self.project_root / filename).exists():
                    score += 1.0

            # Check for patterns in files
            for filename, pattern in signature.get('patterns', []):
                max_score += 2.0
                content = self._read_file(filename)
                if content and re.search(pattern, content, re.IGNORECASE):
                    score += 2.0

            # Check for directories
            for dirname in signature.get('dirs', []):
                max_score += 0.5
                if (self.project_root / dirname).exists():
                    score += 0.5

            if max_score > 0:
                scores[stack_name] = score / max_score

        if not scores:
            return 'unknown', 0.0

        best_stack = max(scores, key=scores.get)
        return best_stack, scores[best_stack]

    # -------------------------------------------------------------------------
    # Convention Detection
    # -------------------------------------------------------------------------

    def detect_conventions(self, stack: str) -> Dict[str, Any]:
        """
        Detect project conventions based on stack.

        Args:
            stack: Detected stack name.

        Returns:
            Dictionary of detected conventions.
        """
        conventions = {
            'naming': self._detect_naming_conventions(stack),
            'structure': self._detect_structure_conventions(stack),
            'code_style': self._detect_code_style(stack),
        }
        return conventions

    def _detect_naming_conventions(self, stack: str) -> Dict[str, str]:
        """Detect naming conventions from code samples."""
        conventions = {}

        # Sample entity/model names
        entity_dirs = self._find_entity_dirs(stack)
        if entity_dirs:
            samples = self._sample_file_names(entity_dirs)
            conventions['entities'] = self._infer_naming_style(samples)

        # Sample service names
        service_dirs = self._find_service_dirs(stack)
        if service_dirs:
            samples = self._sample_file_names(service_dirs)
            pattern = self._detect_suffix_pattern(samples, 'Service')
            conventions['services'] = pattern or '{Name}Service'

        # Sample controller names
        controller_dirs = self._find_controller_dirs(stack)
        if controller_dirs:
            samples = self._sample_file_names(controller_dirs)
            pattern = self._detect_suffix_pattern(samples, 'Controller')
            conventions['controllers'] = pattern or '{Name}Controller'

        return conventions

    def _detect_structure_conventions(self, stack: str) -> Dict[str, Any]:
        """Detect project structure conventions."""
        structure = {}

        # Detect source location
        for src_dir in ['src', 'app', 'lib', 'source']:
            if (self.project_root / src_dir).is_dir():
                structure['src_location'] = f"{src_dir}/"
                break

        # Detect test location and patterns
        lang = self._get_language_from_stack(stack)
        for test_dir, pattern in CONVENTION_PATTERNS['test_patterns'].get(lang, []):
            if (self.project_root / test_dir.rstrip('/')).exists():
                structure['tests_location'] = test_dir
                # Extract suffix from pattern
                if r'Test\.' in pattern:
                    structure['test_suffix'] = 'Test'
                elif r'\.test\.' in pattern or r'\.spec\.' in pattern:
                    structure['test_suffix'] = '.test'
                break

        return structure

    def _detect_code_style(self, stack: str) -> Dict[str, Any]:
        """Detect code style configuration."""
        lang = self._get_language_from_stack(stack)
        style_patterns = CONVENTION_PATTERNS['code_style'].get(lang, {})

        detected = {}
        for style_name, config_files in style_patterns.items():
            for config_file in config_files:
                if (self.project_root / config_file).exists():
                    detected['standard'] = style_name
                    detected['config_file'] = config_file
                    break
            if 'standard' in detected:
                break

        # Try to extract specific settings from config
        if detected.get('config_file'):
            detected.update(self._parse_style_config(detected['config_file']))

        return detected

    # -------------------------------------------------------------------------
    # Pattern Detection
    # -------------------------------------------------------------------------

    def detect_patterns(self) -> List[str]:
        """
        Detect architecture patterns used in the project.

        Returns:
            List of detected pattern names.
        """
        detected = []

        for pattern_name, signature in ARCHITECTURE_PATTERNS.items():
            score = 0

            # Check for indicator terms in file/dir names
            for indicator in signature.get('indicators', []):
                if self._find_files_matching(f"*{indicator}*"):
                    score += 1

            # Check for pattern directories
            for dirname in signature.get('dirs', []):
                matches = list(self.project_root.rglob(f"**/{dirname}"))
                if matches:
                    score += 1

            # Threshold: at least 2 matches
            if score >= 2:
                detected.append(pattern_name)

        return detected

    # -------------------------------------------------------------------------
    # Version Detection
    # -------------------------------------------------------------------------

    def _detect_project_name(self) -> str:
        """Detect project name from config files."""
        # Try package.json
        package_json = self._read_file('package.json')
        if package_json:
            try:
                data = json.loads(package_json)
                if 'name' in data:
                    return data['name']
            except json.JSONDecodeError:
                pass

        # Try composer.json
        composer_json = self._read_file('composer.json')
        if composer_json:
            try:
                data = json.loads(composer_json)
                if 'name' in data:
                    return data['name'].split('/')[-1]
            except json.JSONDecodeError:
                pass

        # Try pyproject.toml
        pyproject = self._read_file('pyproject.toml')
        if pyproject:
            match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', pyproject)
            if match:
                return match.group(1)

        # Fallback to directory name
        return self.project_root.name

    def _detect_framework_version(self, stack: str) -> Optional[str]:
        """Detect framework version."""
        if 'symfony' in stack:
            return self._extract_version_from_composer('symfony/framework-bundle')
        elif 'laravel' in stack:
            return self._extract_version_from_composer('laravel/framework')
        elif 'react' in stack:
            return self._extract_version_from_package('react')
        elif 'vue' in stack:
            return self._extract_version_from_package('vue')
        elif 'django' in stack:
            return self._extract_version_from_requirements('django')
        elif 'springboot' in stack:
            return self._extract_spring_version()
        return None

    def _detect_language_version(self, stack: str) -> Optional[str]:
        """Detect language version."""
        if 'php' in stack:
            composer = self._read_file('composer.json')
            if composer:
                try:
                    data = json.loads(composer)
                    php_version = data.get('require', {}).get('php', '')
                    return php_version.lstrip('^~>=<')
                except json.JSONDecodeError:
                    pass
        elif 'javascript' in stack or 'typescript' in stack:
            # Check for .nvmrc or package.json engines
            nvmrc = self._read_file('.nvmrc')
            if nvmrc:
                return nvmrc.strip()
        elif 'python' in stack:
            # Check pyproject.toml or setup.py
            pyproject = self._read_file('pyproject.toml')
            if pyproject:
                match = re.search(r'python\s*=\s*["\']([^"\']+)["\']', pyproject)
                if match:
                    return match.group(1).lstrip('^~>=<')
        return None

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def _read_file(self, filename: str) -> Optional[str]:
        """Read file content with caching."""
        if filename in self._file_cache:
            return self._file_cache[filename]

        filepath = self.project_root / filename
        if not filepath.exists():
            self._file_cache[filename] = None
            return None

        try:
            content = filepath.read_text(encoding='utf-8')
            self._file_cache[filename] = content
            return content
        except Exception:
            self._file_cache[filename] = None
            return None

    def _get_language_from_stack(self, stack: str) -> str:
        """Extract language from stack name."""
        if 'php' in stack:
            return 'php'
        elif 'javascript' in stack or 'typescript' in stack:
            return 'javascript'
        elif 'python' in stack:
            return 'python'
        elif 'java' in stack:
            return 'java'
        return 'unknown'

    def _find_entity_dirs(self, stack: str) -> List[Path]:
        """Find entity/model directories."""
        patterns = {
            'php-symfony': ['src/Entity'],
            'php-laravel': ['app/Models'],
            'javascript-react': ['src/models', 'src/types'],
            'python-django': ['*/models'],
            'java-springboot': ['src/main/java/**/entity', 'src/main/java/**/model'],
        }
        return self._find_matching_dirs(patterns.get(stack, []))

    def _find_service_dirs(self, stack: str) -> List[Path]:
        """Find service directories."""
        patterns = {
            'php-symfony': ['src/Service'],
            'php-laravel': ['app/Services'],
            'javascript-react': ['src/services', 'src/api'],
            'python-django': ['*/services'],
            'java-springboot': ['src/main/java/**/service'],
        }
        return self._find_matching_dirs(patterns.get(stack, []))

    def _find_controller_dirs(self, stack: str) -> List[Path]:
        """Find controller directories."""
        patterns = {
            'php-symfony': ['src/Controller'],
            'php-laravel': ['app/Http/Controllers'],
            'python-django': ['*/views'],
            'java-springboot': ['src/main/java/**/controller'],
        }
        return self._find_matching_dirs(patterns.get(stack, []))

    def _find_matching_dirs(self, patterns: List[str]) -> List[Path]:
        """Find directories matching patterns."""
        result = []
        for pattern in patterns:
            if '*' in pattern:
                matches = list(self.project_root.glob(pattern))
            else:
                path = self.project_root / pattern
                if path.exists():
                    matches = [path]
                else:
                    matches = []
            result.extend([m for m in matches if m.is_dir()])
        return result

    def _sample_file_names(self, dirs: List[Path], limit: int = 10) -> List[str]:
        """Sample file names from directories."""
        names = []
        for d in dirs:
            for f in d.iterdir():
                if f.is_file() and not f.name.startswith('.'):
                    names.append(f.stem)
                    if len(names) >= limit:
                        return names
        return names

    def _infer_naming_style(self, samples: List[str]) -> str:
        """Infer naming style from samples."""
        if not samples:
            return 'PascalCase'

        pascal_count = sum(1 for s in samples if re.match(r'^[A-Z][a-zA-Z0-9]*$', s))
        camel_count = sum(1 for s in samples if re.match(r'^[a-z][a-zA-Z0-9]*$', s))
        snake_count = sum(1 for s in samples if re.match(r'^[a-z][a-z0-9_]*$', s))

        if pascal_count >= len(samples) * 0.6:
            return 'PascalCase'
        elif camel_count >= len(samples) * 0.6:
            return 'camelCase'
        elif snake_count >= len(samples) * 0.6:
            return 'snake_case'
        return 'PascalCase'

    def _detect_suffix_pattern(self, samples: List[str], suffix: str) -> Optional[str]:
        """Detect naming pattern with suffix."""
        with_suffix = [s for s in samples if s.endswith(suffix)]
        if len(with_suffix) >= len(samples) * 0.5:
            return '{Name}' + suffix
        return None

    def _find_files_matching(self, pattern: str) -> List[Path]:
        """Find files matching glob pattern."""
        return list(self.project_root.rglob(pattern))[:10]  # Limit for performance

    def _extract_version_from_composer(self, package: str) -> Optional[str]:
        """Extract version from composer.json or composer.lock."""
        # Try composer.lock first (exact version)
        lock_content = self._read_file('composer.lock')
        if lock_content:
            try:
                data = json.loads(lock_content)
                for pkg in data.get('packages', []):
                    if pkg.get('name') == package:
                        return pkg.get('version', '').lstrip('v')
            except json.JSONDecodeError:
                pass

        # Fall back to composer.json (constraint)
        composer = self._read_file('composer.json')
        if composer:
            try:
                data = json.loads(composer)
                version = data.get('require', {}).get(package, '')
                return version.lstrip('^~>=<')
            except json.JSONDecodeError:
                pass
        return None

    def _extract_version_from_package(self, package: str) -> Optional[str]:
        """Extract version from package.json or package-lock.json."""
        # Try package-lock.json first
        lock_content = self._read_file('package-lock.json')
        if lock_content:
            try:
                data = json.loads(lock_content)
                pkg_data = data.get('packages', {}).get(f'node_modules/{package}', {})
                if 'version' in pkg_data:
                    return pkg_data['version']
            except json.JSONDecodeError:
                pass

        # Fall back to package.json
        package_json = self._read_file('package.json')
        if package_json:
            try:
                data = json.loads(package_json)
                version = data.get('dependencies', {}).get(package, '')
                return version.lstrip('^~>=<')
            except json.JSONDecodeError:
                pass
        return None

    def _extract_version_from_requirements(self, package: str) -> Optional[str]:
        """Extract version from requirements.txt."""
        content = self._read_file('requirements.txt')
        if content:
            for line in content.splitlines():
                line = line.strip().lower()
                if line.startswith(package.lower()):
                    match = re.search(r'[>=<]+\s*([\d.]+)', line)
                    if match:
                        return match.group(1)
        return None

    def _extract_spring_version(self) -> Optional[str]:
        """Extract Spring Boot version from pom.xml or build.gradle."""
        pom = self._read_file('pom.xml')
        if pom:
            match = re.search(r'<spring-boot\.version>([^<]+)</spring-boot\.version>', pom)
            if match:
                return match.group(1)
            match = re.search(r'<version>([^<]+)</version>.*spring-boot', pom, re.DOTALL)
            if match:
                return match.group(1)

        gradle = self._read_file('build.gradle') or self._read_file('build.gradle.kts')
        if gradle:
            match = re.search(r"springBootVersion\s*=\s*['\"]([^'\"]+)['\"]", gradle)
            if match:
                return match.group(1)
        return None

    def _parse_style_config(self, config_file: str) -> Dict[str, Any]:
        """Parse style configuration file for specific settings."""
        content = self._read_file(config_file)
        if not content:
            return {}

        result = {}

        # Try to extract common settings
        if config_file.endswith('.json') or 'prettierrc' in config_file.lower():
            try:
                data = json.loads(content)
                if 'tabWidth' in data:
                    result['indent_size'] = data['tabWidth']
                if 'useTabs' in data:
                    result['indent'] = 'tabs' if data['useTabs'] else 'spaces'
                if 'singleQuote' in data:
                    result['quotes'] = 'single' if data['singleQuote'] else 'double'
                if 'semi' in data:
                    result['semicolons'] = data['semi']
                if 'printWidth' in data:
                    result['max_line_length'] = data['printWidth']
            except json.JSONDecodeError:
                pass

        return result


# =============================================================================
# CLI (for testing)
# =============================================================================

def main():
    """CLI entry point for testing."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='EPCI Project Detector')
    parser.add_argument('--project', '-p', type=str, default='.',
                        help='Project root directory')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output as JSON')

    args = parser.parse_args()

    detector = ProjectDetector(Path(args.project))
    result = detector.detect_all()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Project: {result['project']['name']}")
        print(f"Stack: {result['project']['stack']}")
        print(f"Framework: {result['project']['framework_version']}")
        print(f"Language: {result['project']['language_version']}")
        print(f"Patterns: {', '.join(result['patterns']) or 'none detected'}")
        print(f"Conventions: {json.dumps(result['conventions'], indent=2)}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
