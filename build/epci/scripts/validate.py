#!/usr/bin/env python3
"""
EPCI v6 Validation Script

Validates plugin structure, skills, and components.
"""

import json
import sys
from pathlib import Path


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
    print("=" * 40)

    # Validate plugin.json
    print("\nValidating plugin.json...")
    plugin_path = src_dir / ".claude-plugin" / "plugin.json"
    errors = validate_plugin_json(plugin_path)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} errors)")

    # Validate skills
    print("\nValidating skills...")
    skills_dir = src_dir / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_path = skill_dir / "SKILL.md"
                errors = validate_skill(skill_path)
                all_errors.extend(errors)
                status = "PASS" if not errors else "FAIL"
                print(f"  {status} {skill_dir.name}")

    # Validate components
    print("\nValidating shared components...")
    shared_dir = src_dir / "shared"
    if shared_dir.exists():
        for comp_dir in shared_dir.iterdir():
            if comp_dir.is_dir():
                comp_path = comp_dir / "COMPONENT.md"
                errors = validate_component(comp_path)
                all_errors.extend(errors)
                status = "PASS" if not errors else "FAIL"
                print(f"  {status} {comp_dir.name}")

    # Summary
    print("\n" + "=" * 40)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} errors")
        for error in all_errors:
            print(f"  - {error}")
        return 1
    else:
        print("VALIDATION PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
