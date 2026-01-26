#!/usr/bin/env python3
"""
EPCI v6 Validation Script

Validates plugin structure and skills.

Usage:
    python validate.py
"""

import json
import sys
from pathlib import Path


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from markdown file.

    Returns dict with frontmatter fields, or empty dict if no frontmatter.
    """
    if not file_path.exists():
        return {}

    content = file_path.read_text()
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}

    frontmatter = {}
    current_key = None
    current_value_lines = []

    for line in lines[1:end_idx]:
        # Handle multi-line values (YAML folded style >-)
        if line.startswith("  ") and current_key:
            current_value_lines.append(line.strip())
            continue

        # Save previous multi-line value
        if current_key and current_value_lines:
            frontmatter[current_key] = " ".join(current_value_lines)
            current_value_lines = []
            current_key = None

        # Parse key: value
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            # Handle multi-line start (>- or >)
            if value in (">-", ">", "|"):
                current_key = key
                current_value_lines = []
            # Handle boolean
            elif value.lower() == "true":
                frontmatter[key] = True
            elif value.lower() == "false":
                frontmatter[key] = False
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                frontmatter[key] = value[1:-1]
            else:
                frontmatter[key] = value

    # Don't forget last multi-line value
    if current_key and current_value_lines:
        frontmatter[current_key] = " ".join(current_value_lines)

    return frontmatter


def validate_plugin_json(plugin_path: Path) -> list[str]:
    """Validate plugin.json structure."""
    errors = []

    if not plugin_path.exists():
        errors.append(f"plugin.json not found at {plugin_path}")
        return errors

    try:
        with open(plugin_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in plugin.json: {e}")
        return errors

    required_fields = ["name", "version", "description", "skills"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field in plugin.json: {field}")

    # Validate skill paths exist
    if "skills" in data:
        for skill_path in data["skills"]:
            full_path = plugin_path.parent.parent / skill_path
            if not full_path.exists():
                errors.append(f"Skill file not found: {skill_path}")

    return errors


def validate_skill(skill_path: Path) -> list[str]:
    """Validate a SKILL.md file."""
    errors = []

    if not skill_path.exists():
        errors.append(f"SKILL.md not found: {skill_path}")
        return errors

    content = skill_path.read_text()

    # Check for frontmatter
    if not content.startswith("---"):
        errors.append(f"Missing frontmatter in {skill_path}")

    # Check required frontmatter fields
    required_fields = ["name", "description", "user-invocable"]
    for field in required_fields:
        if f"{field}:" not in content:
            errors.append(f"Missing frontmatter field '{field}' in {skill_path}")

    return errors


def validate_component(component_path: Path) -> list[str]:
    """Validate a COMPONENT.md file."""
    errors = []

    if not component_path.exists():
        errors.append(f"COMPONENT.md not found: {component_path}")
        return errors

    content = component_path.read_text()

    # Check for frontmatter
    if not content.startswith("---"):
        errors.append(f"Missing frontmatter in {component_path}")

    # Check that user-invocable is false
    if "user-invocable: true" in content:
        errors.append(f"Component should have user-invocable: false in {component_path}")

    return errors


def main():
    """Run all validations."""
    src_dir = Path(__file__).parent.parent
    all_errors = []

    print("EPCI v6 Validation")
    print("=" * 50)

    # Validate plugin.json
    print("\n[1/3] Validating plugin.json...")
    plugin_path = src_dir / ".claude-plugin" / "plugin.json"
    errors = validate_plugin_json(plugin_path)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} errors)")

    # Validate skills
    print("\n[2/3] Validating skills...")
    skills_dir = src_dir / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_path = skill_dir / "SKILL.md"
                if skill_path.exists():
                    errors = validate_skill(skill_path)
                    all_errors.extend(errors)
                    status = "PASS" if not errors else "FAIL"
                    print(f"  {status} {skill_dir.name}")
                # Check core skills
                if skill_dir.name == "core":
                    for core_skill_dir in sorted(skill_dir.iterdir()):
                        if core_skill_dir.is_dir():
                            core_skill_path = core_skill_dir / "SKILL.md"
                            if core_skill_path.exists():
                                errors = validate_skill(core_skill_path)
                                all_errors.extend(errors)
                                status = "PASS" if not errors else "FAIL"
                                print(f"  {status} core/{core_skill_dir.name}")

    # Validate components
    print("\n[3/3] Validating shared components...")
    shared_dir = src_dir / "shared"
    if shared_dir.exists():
        for comp_dir in sorted(shared_dir.iterdir()):
            if comp_dir.is_dir():
                comp_path = comp_dir / "COMPONENT.md"
                errors = validate_component(comp_path)
                all_errors.extend(errors)
                status = "PASS" if not errors else "FAIL"
                print(f"  {status} {comp_dir.name}")
    else:
        print("  (no shared directory)")

    # Summary
    print("\n" + "=" * 50)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} errors")
        return 1
    else:
        print("VALIDATION PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
