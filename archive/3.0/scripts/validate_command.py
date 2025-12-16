#!/usr/bin/env python3
"""
Validation automatique des Commandes Claude Code.
Usage: python validate_command.py <path-to-command.md>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    """Rapport de validation d'une commande."""
    command_name: str
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
        print(f"VALIDATION REPORT: {self.command_name}")
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
        report.add_error(f"Command file must be .md: {file_path.suffix}")
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


def validate_allowed_tools(frontmatter: dict, report: ValidationReport) -> bool:
    """Verifie allowed-tools."""
    tools = frontmatter.get('allowed-tools', [])

    valid_tools = [
        'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
        'Task', 'WebFetch', 'LS', 'MultiEdit'
    ]

    if tools:
        for tool in tools:
            if tool not in valid_tools:
                report.add_warning(f"Unknown tool: {tool}")

    print(f"[OK] Allowed-tools: {len(tools)} tools defined")
    report.pass_check()
    return True


def validate_content_structure(content: str, report: ValidationReport) -> bool:
    """Verifie la structure du contenu."""
    # Verifier presence de sections importantes
    has_headers = bool(re.search(r'^#+\s', content, re.MULTILINE))

    if not has_headers:
        report.add_warning("No markdown headers found in content")

    # Estimation tokens
    tokens = len(content) // 4
    if tokens > 5000:
        report.add_warning(f"Content may be too long: ~{tokens} tokens")

    print(f"[OK] Content structure: ~{tokens} tokens")
    report.pass_check()
    return True


def validate_command(command_path_str: str) -> int:
    """Point d'entree principal."""
    command_path = Path(command_path_str).resolve()

    report = ValidationReport(command_name=command_path.name)

    # Validation existence
    if not validate_file_exists(command_path, report):
        return report.print_report()

    content = command_path.read_text(encoding='utf-8')

    # Validations
    frontmatter = validate_yaml_frontmatter(content, report)
    if frontmatter:
        validate_description(frontmatter, report)
        validate_allowed_tools(frontmatter, report)
        validate_content_structure(content, report)

    return report.print_report()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_command.py <path-to-command.md>")
        print("Example: python validate_command.py src/commands/epci-brief.md")
        sys.exit(1)

    sys.exit(validate_command(sys.argv[1]))
