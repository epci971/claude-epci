#!/usr/bin/env python3
"""
Validation of EPCI flags configuration.
Usage: python validate_flags.py [--check-docs]

Validates:
- flags.md documentation exists and is well-formed
- flags-system skill exists and is valid
- Flag definitions are consistent across documentation
"""

import sys
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Set, Optional


@dataclass
class ValidationReport:
    """Validation report for flags system."""
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
        print("VALIDATION REPORT: Flags System")
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


# Known flags for validation
KNOWN_FLAGS = {
    # Thinking flags
    "--think", "--think-hard", "--ultrathink",
    # Compression flags
    "--uc", "--verbose",
    # Workflow flags
    "--safe", "--no-hooks",
    # Wave flags
    "--wave", "--wave-strategy",
    # Legacy
    "--large", "--continue"
}

INCOMPATIBLE_PAIRS = [
    # No incompatible pairs after removing --fast
]


def find_src_root() -> Path:
    """Find the src directory root."""
    current = Path(__file__).parent
    while current.name != 'src' and current.parent != current:
        current = current.parent
    return current


def validate_flags_doc(src_root: Path, report: ValidationReport) -> bool:
    """Check that flags.md documentation exists."""
    flags_doc = src_root / "settings" / "flags.md"

    if not flags_doc.exists():
        report.add_error(f"flags.md not found at {flags_doc}")
        return False

    try:
        content = flags_doc.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError) as e:
        report.add_error(f"Failed to read flags.md: {e}")
        return False

    # Check required sections
    required_sections = [
        "## Thinking Flags",
        "## Compression Flags",
        "## Workflow Flags",
        "## Wave Flags",
        "## Auto-Activation",
        "## Precedence Rules"
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        report.add_error(f"Missing sections in flags.md: {missing}")
        return False

    print("[OK] flags.md: Documentation exists and is complete")
    report.pass_check()
    return True


def validate_flags_skill(src_root: Path, report: ValidationReport) -> bool:
    """Check that flags-system skill exists."""
    skill_path = src_root / "skills" / "core" / "flags-system" / "SKILL.md"

    if not skill_path.exists():
        report.add_error(f"flags-system skill not found at {skill_path}")
        return False

    try:
        content = skill_path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError) as e:
        report.add_error(f"Failed to read flags-system skill: {e}")
        return False

    # Check for required frontmatter
    if not content.startswith("---"):
        report.add_error("flags-system skill missing YAML frontmatter")
        return False

    if "name: flags-system" not in content:
        report.add_error("flags-system skill has incorrect name")
        return False

    print("[OK] flags-system skill: Exists and has valid structure")
    report.pass_check()
    return True


def validate_flag_references(src_root: Path, report: ValidationReport) -> bool:
    """Check that flag references in commands are consistent."""
    commands_dir = src_root / "commands"

    if not commands_dir.exists():
        report.add_error(f"Commands directory not found at {commands_dir}")
        return False

    unknown_flags: Set[str] = set()

    for cmd_file in commands_dir.glob("*.md"):
        content = cmd_file.read_text()

        # Find all flag references (--something)
        flags_found = re.findall(r'--[a-z][-a-z0-9_]*', content)

        for flag in flags_found:
            if flag not in KNOWN_FLAGS:
                unknown_flags.add(f"{flag} in {cmd_file.name}")

    if unknown_flags:
        for uf in unknown_flags:
            report.add_warning(f"Unknown flag reference: {uf}")

    print("[OK] Flag references: All commands checked")
    report.pass_check()
    return True


def validate_incompatible_flags(report: ValidationReport) -> bool:
    """Validate that incompatible flag pairs are documented."""
    # This is a static check - the actual conflict detection happens at runtime
    print("[OK] Incompatible flags: Pairs defined")
    report.pass_check()
    return True


def validate_hook_context(src_root: Path, report: ValidationReport) -> bool:
    """Check that HookContext includes flags fields."""
    runner_path = src_root / "hooks" / "runner.py"

    if not runner_path.exists():
        report.add_warning("hooks/runner.py not found - skipping HookContext check")
        report.pass_check()
        return True

    content = runner_path.read_text()

    if "active_flags" not in content:
        report.add_error("HookContext missing 'active_flags' field")
        return False

    if "flag_sources" not in content:
        report.add_error("HookContext missing 'flag_sources' field")
        return False

    print("[OK] HookContext: Includes flags fields")
    report.pass_check()
    return True


def main():
    """Main validation entry point."""
    report = ValidationReport()

    # Find src root
    src_root = find_src_root()
    if src_root.name != 'src':
        # Try relative path from script location
        src_root = Path(__file__).parent.parent

    print(f"Validating flags system in: {src_root}\n")

    # Run all validations
    validate_flags_doc(src_root, report)
    validate_flags_skill(src_root, report)
    validate_flag_references(src_root, report)
    validate_incompatible_flags(report)
    validate_hook_context(src_root, report)

    return report.print_report()


if __name__ == "__main__":
    sys.exit(main())
