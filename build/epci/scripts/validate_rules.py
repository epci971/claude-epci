#!/usr/bin/env python3
"""
Validate .claude/rules/ structure and content.

Usage:
    python validate_rules.py <rules_directory>
    python validate_rules.py .claude/rules/
    python validate_rules.py --help

Validates:
    - YAML frontmatter syntax
    - paths patterns validity
    - Required sections presence
    - Token limits
"""

import sys
import re
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationReport:
    """Validation report for a single rules file."""
    name: str
    path: str
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough: 1 token ~ 4 chars)."""
    return len(text) // 4


def validate_yaml_frontmatter(content: str) -> tuple[bool, list, dict]:
    """
    Validate YAML frontmatter.
    Returns: (valid, errors, parsed_data)
    """
    errors = []
    data = {}

    # Check for frontmatter markers
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        errors.append("Missing YAML frontmatter (---...---)")
        return False, errors, data

    frontmatter = match.group(1)

    # Simple YAML parsing (avoid external dependency)
    try:
        lines = frontmatter.strip().split('\n')
        current_key = None
        current_list = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Key: value or Key:
            key_match = re.match(r'^(\w+):\s*(.*)?$', line)
            if key_match and not line.startswith(' ') and not line.startswith('-'):
                if current_key and current_list:
                    data[current_key] = current_list
                    current_list = []
                current_key = key_match.group(1)
                value = key_match.group(2)
                if value:
                    data[current_key] = value.strip()
                continue

            # List item
            list_match = re.match(r'^\s*-\s*(.+)$', line)
            if list_match and current_key:
                item = list_match.group(1).strip()
                # Remove quotes if present
                if item.startswith('"') and item.endswith('"'):
                    item = item[1:-1]
                elif item.startswith("'") and item.endswith("'"):
                    item = item[1:-1]
                current_list.append(item)

        if current_key and current_list:
            data[current_key] = current_list

    except Exception as e:
        errors.append(f"YAML parse error: {e}")
        return False, errors, data

    # Validate required fields
    if 'paths' not in data:
        # paths is optional for _global rules
        pass
    elif not isinstance(data.get('paths'), list):
        if data.get('paths'):
            data['paths'] = [data['paths']]

    return len(errors) == 0, errors, data


def validate_paths_patterns(paths: list) -> tuple[bool, list]:
    """Validate glob patterns in paths."""
    errors = []

    if not paths:
        return True, errors

    for pattern in paths:
        # Check for common issues
        if not isinstance(pattern, str):
            errors.append(f"Invalid path type: {type(pattern)}")
            continue

        # Negation patterns must start with !
        if pattern.startswith('!'):
            pattern = pattern[1:]

        # Check for invalid characters
        invalid_chars = ['<', '>', '|', '\0']
        for char in invalid_chars:
            if char in pattern:
                errors.append(f"Invalid character '{char}' in path: {pattern}")

        # Warn about potentially problematic patterns
        if pattern == '**':
            errors.append(f"Pattern '**' matches everything - too broad")

    return len(errors) == 0, errors


def validate_content_structure(content: str) -> tuple[bool, list, list]:
    """
    Validate markdown content structure.
    Returns: (valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Remove frontmatter for content analysis
    content_body = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)

    # Must have title
    if not re.search(r'^# .+', content_body, re.MULTILINE):
        errors.append("Missing title (# heading)")

    # Check for severity levels
    levels = {
        '🔴': 'CRITICAL',
        '🟡': 'CONVENTIONS',
        '🟢': 'PREFERENCES'
    }

    found_levels = []
    for emoji, name in levels.items():
        if emoji in content_body:
            found_levels.append(name)

    if not found_levels:
        errors.append("Must have at least one section (🔴 CRITICAL, 🟡 CONVENTIONS, or 🟢 PREFERENCES)")

    # Recommended sections (warnings only)
    recommended = ['Quick Reference', 'Anti-pattern', 'Example']
    for section in recommended:
        if section.lower() not in content_body.lower():
            warnings.append(f"Missing recommended section: {section}")

    return len(errors) == 0, errors, warnings


def validate_token_limit(content: str, limit: int = 2000) -> tuple[bool, list]:
    """Check if content exceeds token limit."""
    errors = []
    tokens = estimate_tokens(content)

    if tokens > limit:
        errors.append(f"Token count ({tokens}) exceeds limit ({limit})")

    return len(errors) == 0, errors


def validate_rules_file(file_path: Path) -> ValidationReport:
    """Validate a single rules file."""
    report = ValidationReport(
        name=file_path.name,
        path=str(file_path)
    )

    if not file_path.exists():
        report.valid = False
        report.errors.append(f"File not found: {file_path}")
        return report

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        report.valid = False
        report.errors.append(f"Cannot read file: {e}")
        return report

    # 1. Validate YAML frontmatter
    yaml_valid, yaml_errors, yaml_data = validate_yaml_frontmatter(content)
    if not yaml_valid:
        report.errors.extend(yaml_errors)

    # 2. Validate paths patterns (if present)
    if 'paths' in yaml_data and yaml_data['paths']:
        paths_valid, paths_errors = validate_paths_patterns(yaml_data['paths'])
        if not paths_valid:
            report.errors.extend(paths_errors)

    # 3. Validate content structure
    content_valid, content_errors, content_warnings = validate_content_structure(content)
    if not content_valid:
        report.errors.extend(content_errors)
    report.warnings.extend(content_warnings)

    # 4. Validate token limit
    token_valid, token_errors = validate_token_limit(content)
    if not token_valid:
        report.warnings.extend(token_errors)  # Warning, not error

    report.valid = len(report.errors) == 0
    return report


def validate_rules_directory(rules_dir: Path) -> list[ValidationReport]:
    """Validate all rules files in a directory."""
    reports = []

    if not rules_dir.exists():
        report = ValidationReport(
            name=str(rules_dir),
            path=str(rules_dir),
            valid=False,
            errors=[f"Directory not found: {rules_dir}"]
        )
        return [report]

    # Find all .md files
    md_files = list(rules_dir.glob('**/*.md'))

    if not md_files:
        report = ValidationReport(
            name=str(rules_dir),
            path=str(rules_dir),
            valid=False,
            errors=["No .md files found in directory"]
        )
        return [report]

    for md_file in md_files:
        report = validate_rules_file(md_file)
        reports.append(report)

    return reports


def validate_claude_md(claude_md_path: Path) -> ValidationReport:
    """Validate CLAUDE.md file (different rules than rule files)."""
    report = ValidationReport(
        name="CLAUDE.md",
        path=str(claude_md_path)
    )

    if not claude_md_path.exists():
        report.valid = False
        report.errors.append(f"File not found: {claude_md_path}")
        return report

    try:
        content = claude_md_path.read_text(encoding='utf-8')
    except Exception as e:
        report.valid = False
        report.errors.append(f"Cannot read file: {e}")
        return report

    # CLAUDE.md should have a title
    if not re.search(r'^# .+', content, re.MULTILINE):
        report.errors.append("Missing project title (# heading)")

    # Should have key sections
    required_sections = ['Stack', 'Commande', 'Convention']
    for section in required_sections:
        if section.lower() not in content.lower():
            report.warnings.append(f"Missing recommended section: {section}")

    # Token limit for CLAUDE.md is higher (500)
    tokens = estimate_tokens(content)
    if tokens > 500:
        report.warnings.append(f"CLAUDE.md is large ({tokens} tokens). Consider moving details to rules/")

    report.valid = len(report.errors) == 0
    return report


def print_report(report: ValidationReport) -> None:
    """Print a single validation report."""
    status = "✓" if report.valid else "✗"
    print(f"\n{status} {report.name}")
    print(f"  Path: {report.path}")

    if report.errors:
        print("  Errors:")
        for error in report.errors:
            print(f"    ✗ {error}")

    if report.warnings:
        print("  Warnings:")
        for warning in report.warnings:
            print(f"    ⚠ {warning}")

    if report.valid and not report.warnings:
        print("  All checks passed")


def main(path_str: str) -> int:
    """Main validation entry point."""
    path = Path(path_str)

    print(f"Validating: {path}")
    print("=" * 60)

    reports = []

    if path.is_file():
        # Single file validation
        if path.name == "CLAUDE.md":
            reports.append(validate_claude_md(path))
        else:
            reports.append(validate_rules_file(path))
    elif path.is_dir():
        # Directory validation
        # Check for CLAUDE.md
        claude_md = path / "CLAUDE.md"
        if claude_md.exists():
            reports.append(validate_claude_md(claude_md))

        # Check for rules/ subdirectory
        rules_dir = path / "rules" if (path / "rules").exists() else path
        reports.extend(validate_rules_directory(rules_dir))
    else:
        print(f"Error: Path not found: {path}")
        return 1

    # Print reports
    for report in reports:
        print_report(report)

    # Summary
    print("\n" + "=" * 60)
    total = len(reports)
    passed = sum(1 for r in reports if r.valid)
    warnings = sum(len(r.warnings) for r in reports)

    print(f"Summary: {passed}/{total} files valid")
    if warnings:
        print(f"         {warnings} warning(s)")

    if passed == total:
        print("\n✓ All validations passed")
        return 0
    else:
        print(f"\n✗ {total - passed} file(s) failed validation")
        return 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'path',
        help='Path to .claude/ directory or specific rules file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation output including parsed YAML'
    )

    args = parser.parse_args()

    # Store verbose flag globally for use in validation functions
    if args.verbose:
        print(f"Verbose mode enabled")
        print(f"Validating path: {args.path}")

    sys.exit(main(args.path))
