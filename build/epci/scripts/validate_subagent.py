#!/usr/bin/env python3
"""
Validation automatique des Subagents Claude Code.
Usage: python validate_subagent.py <path-to-subagent.md>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    """Rapport de validation d'un subagent."""
    agent_name: str
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 5

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.agent_name}")
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


def validate_file_exists(file_path: Path, report: ValidationReport) -> bool:
    """Verifie que le fichier existe."""
    if not file_path.exists():
        report.add_error(f"File not found: {file_path}")
        return False

    if not file_path.suffix == '.md':
        report.add_error(f"Subagent file must be .md: {file_path.suffix}")
        return False

    print(f"[OK] File exists: {file_path.name}")
    report.pass_check()
    return True


def validate_yaml_frontmatter(content: str, report: ValidationReport) -> dict:
    """Verifie le frontmatter YAML."""
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            report.add_error("YAML frontmatter missing or malformed")
            return None

        frontmatter = yaml.safe_load(match.group(1))
        print("[OK] YAML frontmatter: Valid")
        report.pass_check()
        return frontmatter

    except yaml.YAMLError as e:
        report.add_error(f"YAML syntax error: {e}")
        return None


def validate_name(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie le champ name."""
    name = frontmatter.get('name', '')

    if not name:
        report.add_error("Field 'name' is required for subagents")
        return False

    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        report.add_error(f"Name must be kebab-case: '{name}'")
        return False

    if len(name) > 64:
        report.add_error(f"Name exceeds 64 chars: {len(name)}")
        return False

    print(f"[OK] Name: '{name}'")
    report.pass_check()
    return True


def validate_description(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie la description."""
    desc = frontmatter.get('description', '')

    if not desc:
        report.add_error("Field 'description' is required")
        return False

    if len(desc) < 10:
        report.add_warning("Description seems too short")

    if len(desc) > 500:
        report.add_warning(f"Description is quite long: {len(desc)} chars")

    print(f"[OK] Description: {len(desc)} chars")
    report.pass_check()
    return True


def validate_tools_restriction(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie que les outils sont restrictifs (principe de moindre privilege)."""
    tools = frontmatter.get('allowed-tools', [])

    # Outils dangereux pour un subagent
    dangerous_tools = ['Write', 'Edit', 'Bash']
    read_only_tools = ['Read', 'Grep', 'Glob', 'LS']

    dangerous_count = sum(1 for t in tools if t in dangerous_tools)

    if dangerous_count > 2:
        report.add_warning(
            f"Subagent has many write tools ({dangerous_count}). "
            "Consider restricting to read-only for better isolation."
        )

    if not tools:
        report.add_warning("No allowed-tools specified. Subagent will have default access.")

    print(f"[OK] Tools restriction: {len(tools)} tools")
    report.pass_check()
    return True


def validate_content_focus(content: str, report: ValidationReport) -> bool:
    """Verifie que le contenu est focalis sur une mission."""
    # Estimation tokens
    tokens = len(content) // 4

    if tokens > 2000:
        report.add_warning(
            f"Subagent content is quite long (~{tokens} tokens). "
            "Subagents should be focused on a single mission."
        )

    # Verifier presence instructions claires
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    if len(body.strip()) < 100:
        report.add_warning("Subagent instructions seem very short")

    return True


def validate_subagent(agent_path_str: str) -> int:
    """Point d'entree principal."""
    agent_path = Path(agent_path_str).resolve()

    report = ValidationReport(agent_name=agent_path.name)

    # Validation existence
    if not validate_file_exists(agent_path, report):
        return report.print_report()

    content = agent_path.read_text(encoding='utf-8')

    # Validations
    frontmatter = validate_yaml_frontmatter(content, report)
    if frontmatter:
        validate_name(frontmatter, report)
        validate_description(frontmatter, report)
        validate_tools_restriction(frontmatter, report)
        validate_content_focus(content, report)

    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_subagent.py <path-to-subagent.md>")
        print("Example: python validate_subagent.py src/agents/code-reviewer.md")
        sys.exit(1)

    sys.exit(validate_subagent(sys.argv[1]))
