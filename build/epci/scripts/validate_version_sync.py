#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation de la synchronisation des versions entre les 3 fichiers:
- CLAUDE.md (header Version : X.Y.Z)
- src/.claude-plugin/plugin.json
- build/epci/.claude-plugin/plugin.json

Usage: python validate_version_sync.py [--fix]
"""

import sys
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class ValidationReport:
    """Rapport de validation des versions."""
    name: str = "version-sync"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 4

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

        if self.errors:
            print("ERRORS:")
            for err in self.errors:
                print(f"   ❌ {err}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warn in self.warnings:
                print(f"   ⚠️  {warn}")
            print()

        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")

        return 0 if self.valid else 1


def get_project_root() -> Path:
    """Trouve la racine du projet (contient src/)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "src").exists() and (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


def extract_version_from_claude_md(file_path: Path) -> Optional[str]:
    """Extrait la version depuis CLAUDE.md (format: Version : X.Y.Z)."""
    if not file_path.exists():
        return None

    content = file_path.read_text(encoding='utf-8')
    # Pattern: > **Version** : 5.6.0 ou Version : 5.6.0
    match = re.search(r'[Vv]ersion[^:]*:\s*(\d+\.\d+\.\d+)', content)
    if match:
        return match.group(1)
    return None


def extract_version_from_plugin_json(file_path: Path) -> Optional[str]:
    """Extrait la version depuis plugin.json."""
    if not file_path.exists():
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('version')
    except (json.JSONDecodeError, IOError):
        return None


def update_claude_md_version(file_path: Path, new_version: str) -> bool:
    """Met à jour la version dans CLAUDE.md."""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding='utf-8')
    # Pattern flexible pour remplacer la version
    new_content = re.sub(
        r'([Vv]ersion[^:]*:\s*)(\d+\.\d+\.\d+)',
        f'\\g<1>{new_version}',
        content,
        count=1
    )

    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    return False


def update_plugin_json_version(file_path: Path, new_version: str) -> bool:
    """Met à jour la version dans plugin.json."""
    if not file_path.exists():
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('version') != new_version:
            data['version'] = new_version
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            return True
        return False
    except (json.JSONDecodeError, IOError):
        return False


def validate_version_sync(fix: bool = False) -> int:
    """Valide la synchronisation des versions entre les 3 fichiers."""
    project_root = get_project_root()
    report = ValidationReport()

    # Chemins des fichiers
    claude_md = project_root / "CLAUDE.md"
    src_plugin = project_root / "src" / ".claude-plugin" / "plugin.json"
    build_plugin = project_root / "build" / "epci" / ".claude-plugin" / "plugin.json"

    versions: Dict[str, Optional[str]] = {}

    # Check 1: CLAUDE.md existe et contient une version
    print(f"Checking CLAUDE.md...")
    versions['claude_md'] = extract_version_from_claude_md(claude_md)
    if versions['claude_md']:
        print(f"  [OK] CLAUDE.md version: {versions['claude_md']}")
        report.pass_check()
    else:
        report.add_error(f"CLAUDE.md missing or no version found at {claude_md}")

    # Check 2: src/plugin.json existe et contient une version
    print(f"Checking src/.claude-plugin/plugin.json...")
    versions['src_plugin'] = extract_version_from_plugin_json(src_plugin)
    if versions['src_plugin']:
        print(f"  [OK] src/plugin.json version: {versions['src_plugin']}")
        report.pass_check()
    else:
        report.add_error(f"src/.claude-plugin/plugin.json missing or no version at {src_plugin}")

    # Check 3: build/plugin.json existe et contient une version
    print(f"Checking build/epci/.claude-plugin/plugin.json...")
    versions['build_plugin'] = extract_version_from_plugin_json(build_plugin)
    if versions['build_plugin']:
        print(f"  [OK] build/plugin.json version: {versions['build_plugin']}")
        report.pass_check()
    else:
        report.add_error(f"build/epci/.claude-plugin/plugin.json missing or no version at {build_plugin}")

    # Check 4: Toutes les versions sont identiques
    print(f"Checking version synchronization...")
    valid_versions = {k: v for k, v in versions.items() if v is not None}

    if len(valid_versions) >= 2:
        unique_versions = set(valid_versions.values())

        if len(unique_versions) == 1:
            print(f"  [OK] All versions synchronized: {list(unique_versions)[0]}")
            report.pass_check()
        else:
            report.add_error(f"Version mismatch detected: {dict(valid_versions)}")

            if fix:
                # Trouver la version la plus récente (semver comparison)
                def parse_semver(v):
                    parts = v.split('.')
                    return tuple(int(p) for p in parts)

                latest_version = max(valid_versions.values(), key=parse_semver)
                print(f"  [FIX] Aligning all versions to: {latest_version}")

                fixed = []
                if versions.get('claude_md') != latest_version:
                    if update_claude_md_version(claude_md, latest_version):
                        fixed.append("CLAUDE.md")

                if versions.get('src_plugin') != latest_version:
                    if update_plugin_json_version(src_plugin, latest_version):
                        fixed.append("src/plugin.json")

                if versions.get('build_plugin') != latest_version:
                    if update_plugin_json_version(build_plugin, latest_version):
                        fixed.append("build/plugin.json")

                if fixed:
                    print(f"  [OK] Fixed: {', '.join(fixed)}")
                    report.valid = True
                    report.errors = []
                    report.pass_check()
    else:
        report.add_error("Not enough version files found to compare")

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validate version synchronization across EPCI plugin files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Files checked:
  - CLAUDE.md (Version : X.Y.Z header)
  - src/.claude-plugin/plugin.json
  - build/epci/.claude-plugin/plugin.json

Examples:
  python validate_version_sync.py          # Check only
  python validate_version_sync.py --fix    # Fix mismatches
        """
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix version mismatches (align to latest version)'
    )

    args = parser.parse_args()
    sys.exit(validate_version_sync(fix=args.fix))


if __name__ == "__main__":
    main()
