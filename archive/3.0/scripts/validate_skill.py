#!/usr/bin/env python3
"""
Validation automatique des Skills Claude Code.
Usage: python validate_skill.py <path-to-skill-folder>
"""

import sys
import os
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationReport:
    """Rapport de validation d'un skill."""
    skill_name: str
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 6

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.skill_name}")
        print(f"{'='*60}\n")

        if self.errors:
            print("ERRORS:")
            for err in self.errors:
                print(f"   - {err}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warn in self.warnings:
                print(f"   - {warn}")
            print()

        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")

        return 0 if self.valid else 1


def validate_yaml_syntax(content: str, report: ValidationReport) -> dict:
    """Verifie la syntaxe du frontmatter YAML."""
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed")
            return None

        frontmatter = yaml.safe_load(match.group(1))
        print("[OK] YAML syntax: Valid")
        report.pass_check()
        return frontmatter

    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_name(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie le champ name."""
    name = frontmatter.get('name', '')

    if not name:
        report.add_error("Field 'name' is required")
        return False

    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Name must be kebab-case: '{name}'")
        return False

    if len(name) > 64:
        report.add_error(f"Name exceeds 64 chars: {len(name)}")
        return False

    print(f"[OK] Name format: '{name}' ({len(name)} chars)")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie la description."""
    desc = frontmatter.get('description', '')

    if not desc:
        report.add_error("Field 'description' is required")
        return False

    if len(desc) > 1024:
        report.add_error(f"Description exceeds 1024 chars: {len(desc)}")
        return False

    has_use_when = 'use when' in desc.lower()
    has_not_for = 'not for' in desc.lower()

    if not has_use_when:
        report.add_warning("Description should contain 'Use when:'")
    if not has_not_for:
        report.add_warning("Description should contain 'Not for:'")

    print(f"[OK] Description: {len(desc)} chars")
    report.pass_check()
    return True


def estimate_tokens(text: str) -> int:
    """Estimation grossiere du nombre de tokens."""
    return len(text) // 4


def validate_token_count(content: str, report: ValidationReport) -> bool:
    """Verifie que le contenu ne depasse pas 5000 tokens."""
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    tokens = estimate_tokens(body)

    if tokens > 5000:
        report.add_error(f"Content exceeds 5000 tokens: ~{tokens}")
        return False

    print(f"[OK] Token count: ~{tokens} tokens")
    report.pass_check()
    return True


def validate_references(skill_path: Path, content: str, report: ValidationReport) -> bool:
    """Verifie que les fichiers references existent."""
    ref_dir = skill_path / "references"

    # Chercher les references dans le contenu
    refs_mentioned = re.findall(r'references/([a-z0-9-]+\.md)', content)

    missing = []
    for ref in refs_mentioned:
        if ref_dir.exists() and not (ref_dir / ref).exists():
            missing.append(ref)

    if missing:
        report.add_warning(f"Referenced files not found: {', '.join(missing)}")

    print(f"[OK] References: Checked")
    report.pass_check()
    return True


def validate_structure(skill_path: Path, report: ValidationReport) -> bool:
    """Verifie la structure du skill."""
    skill_file = skill_path / "SKILL.md"

    if not skill_file.exists():
        report.add_error(f"SKILL.md not found in {skill_path}")
        return False

    # Verifier que le dossier est kebab-case
    folder_name = skill_path.name
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', folder_name):
        report.add_warning(f"Folder name should be kebab-case: '{folder_name}'")

    print(f"[OK] Structure: Valid")
    report.pass_check()
    return True


def validate_skill(skill_path_str: str) -> int:
    """Point d'entree principal."""
    skill_path = Path(skill_path_str).resolve()

    if not skill_path.exists():
        print(f"[ERROR] Path not found: {skill_path}")
        return 1

    # Si c'est un fichier, prendre le dossier parent
    if skill_path.is_file():
        skill_path = skill_path.parent

    skill_file = skill_path / "SKILL.md"

    if not skill_file.exists():
        print(f"[ERROR] SKILL.md not found in: {skill_path}")
        return 1

    report = ValidationReport(skill_name=skill_path.name)
    content = skill_file.read_text(encoding='utf-8')

    # Validations
    validate_structure(skill_path, report)
    frontmatter = validate_yaml_syntax(content, report)
    if frontmatter:
        validate_name(frontmatter, report)
        validate_description(frontmatter, report)
        validate_token_count(content, report)
        validate_references(skill_path, content, report)

    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <path-to-skill-folder>")
        print("Example: python validate_skill.py src/skills/core/epci-core/")
        sys.exit(1)

    sys.exit(validate_skill(sys.argv[1]))
