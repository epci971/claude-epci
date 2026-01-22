#!/usr/bin/env python3
"""
EPCI v6 Validation Script

Validates plugin structure, skills, commands, and component synchronization.

Usage:
    python validate.py           # Validate only (detect issues)
    python validate.py --fix     # Auto-fix command/skill sync issues
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


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


def find_skill_for_command(command_path: Path, skills_dir: Path) -> Optional[Path]:
    """Find the matching skill for a command.

    Convention: command 'factory.md' -> skill 'skills/factory/SKILL.md'
    """
    command_name = command_path.stem

    # Check direct skill path
    skill_path = skills_dir / command_name / "SKILL.md"
    if skill_path.exists():
        return skill_path

    # Check core skills path
    core_skill_path = skills_dir / "core" / command_name / "SKILL.md"
    if core_skill_path.exists():
        return core_skill_path

    return None


def update_command_frontmatter(command_path: Path, updates: dict) -> bool:
    """Update frontmatter fields in a command file.

    Returns True if file was modified.
    """
    content = command_path.read_text()
    if not content.startswith("---"):
        return False

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return False

    frontmatter_lines = lines[1:end_idx]
    body_lines = lines[end_idx:]

    modified = False

    for key, value in updates.items():
        # Check if key already exists
        key_exists = False
        for i, line in enumerate(frontmatter_lines):
            if line.startswith(f"{key}:"):
                # Update existing key
                frontmatter_lines[i] = f'{key}: "{value}"'
                key_exists = True
                modified = True
                break

        if not key_exists:
            # Add new key before the last line (usually disable-model-invocation)
            # Find the best position (after description)
            insert_idx = len(frontmatter_lines)
            for i, line in enumerate(frontmatter_lines):
                if line.startswith("disable-model-invocation:"):
                    insert_idx = i
                    break
            frontmatter_lines.insert(insert_idx, f'{key}: "{value}"')
            modified = True

    if modified:
        new_content = "---\n" + "\n".join(frontmatter_lines) + "\n" + "\n".join(body_lines)
        command_path.write_text(new_content)

    return modified


# Fields that should be synchronized from skill to command
SYNC_FIELDS = ["argument-hint", "allowed-tools"]


def validate_command_skill_sync(src_dir: Path) -> list[str]:
    """Validate that commands have the same sync fields as their skills.

    Returns list of error messages.
    """
    errors = []
    commands_dir = src_dir / "commands"
    skills_dir = src_dir / "skills"

    if not commands_dir.exists():
        return errors

    for cmd_path in sorted(commands_dir.glob("*.md")):
        skill_path = find_skill_for_command(cmd_path, skills_dir)
        if not skill_path:
            continue

        skill_fm = parse_frontmatter(skill_path)
        cmd_fm = parse_frontmatter(cmd_path)

        # Only check user-invocable skills
        if not skill_fm.get("user-invocable", False):
            continue

        for field in SYNC_FIELDS:
            skill_value = skill_fm.get(field)
            cmd_value = cmd_fm.get(field)

            if skill_value and cmd_value != skill_value:
                if cmd_value:
                    errors.append(
                        f"{cmd_path.name}: {field} mismatch "
                        f"(command='{cmd_value}', skill='{skill_value}')"
                    )
                else:
                    errors.append(
                        f"{cmd_path.name}: missing {field} "
                        f"(should be '{skill_value}')"
                    )

    return errors


def sync_command_skill_fields(src_dir: Path, dry_run: bool = True) -> tuple[int, list[str]]:
    """Synchronize fields from skills to commands.

    Args:
        src_dir: Source directory containing commands/ and skills/
        dry_run: If True, only report what would be changed

    Returns:
        Tuple of (count of files modified/would be modified, list of change descriptions)
    """
    commands_dir = src_dir / "commands"
    skills_dir = src_dir / "skills"

    changes = []
    modified_count = 0

    if not commands_dir.exists():
        return 0, []

    for cmd_path in sorted(commands_dir.glob("*.md")):
        skill_path = find_skill_for_command(cmd_path, skills_dir)
        if not skill_path:
            continue

        skill_fm = parse_frontmatter(skill_path)
        cmd_fm = parse_frontmatter(cmd_path)

        # Only sync user-invocable skills
        if not skill_fm.get("user-invocable", False):
            continue

        updates = {}
        for field in SYNC_FIELDS:
            skill_value = skill_fm.get(field)
            cmd_value = cmd_fm.get(field)

            if skill_value and cmd_value != skill_value:
                updates[field] = skill_value
                changes.append(f"  {cmd_path.name}: set {field} = '{skill_value}'")

        if updates:
            if not dry_run:
                update_command_frontmatter(cmd_path, updates)
            modified_count += 1

    return modified_count, changes


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
    parser = argparse.ArgumentParser(
        description="EPCI v6 Validation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate.py           # Validate only
    python validate.py --fix     # Auto-fix sync issues
        """
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix command/skill synchronization issues"
    )
    args = parser.parse_args()

    src_dir = Path(__file__).parent.parent
    all_errors = []

    print("EPCI v6 Validation")
    print("=" * 50)

    # Validate plugin.json
    print("\n[1/4] Validating plugin.json...")
    plugin_path = src_dir / ".claude-plugin" / "plugin.json"
    errors = validate_plugin_json(plugin_path)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} errors)")

    # Validate skills
    print("\n[2/4] Validating skills...")
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
    print("\n[3/4] Validating shared components...")
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

    # Validate command/skill synchronization
    print("\n[4/4] Validating command/skill sync...")
    sync_errors = validate_command_skill_sync(src_dir)

    if args.fix and sync_errors:
        print("  Running --fix mode...")
        count, changes = sync_command_skill_fields(src_dir, dry_run=False)
        print(f"  Fixed {count} command(s):")
        for change in changes:
            print(change)
        # Re-validate to confirm fixes
        sync_errors = validate_command_skill_sync(src_dir)

    all_errors.extend(sync_errors)
    if sync_errors:
        print(f"  FAIL ({len(sync_errors)} sync errors)")
        for err in sync_errors:
            print(f"    - {err}")
    else:
        print("  PASS")

    # Summary
    print("\n" + "=" * 50)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} errors")
        if not args.fix and sync_errors:
            print("\nTip: Run with --fix to auto-fix command/skill sync issues")
        return 1
    else:
        print("VALIDATION PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
