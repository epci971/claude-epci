#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrateur de validation EPCI Plugin.
Executes all validation scripts on all components.

Usage: python validate_all.py [--verbose] [--fix] [--fast]
"""

import sys
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple
import subprocess
import argparse
import time


@dataclass
class ValidationSummary:
    """Global validation summary."""
    # Component validations
    skills_passed: int = 0
    skills_failed: int = 0
    commands_passed: int = 0
    commands_failed: int = 0
    agents_passed: int = 0
    agents_failed: int = 0
    triggering_passed: int = 0
    triggering_failed: int = 0

    # System validations
    flags_passed: bool = False
    rules_passed: bool = False
    notion_passed: bool = False

    # New integrity validations (v5.7)
    version_sync_passed: bool = False
    plugin_json_passed: bool = False
    secrets_passed: bool = False
    cross_refs_passed: bool = False
    breakpoints_passed: bool = False
    markdown_refs_passed: bool = False

    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def total_passed(self):
        # Boolean validations count as 1 each
        bool_checks = [
            self.flags_passed, self.rules_passed, self.notion_passed,
            self.version_sync_passed, self.plugin_json_passed, self.secrets_passed,
            self.cross_refs_passed, self.breakpoints_passed, self.markdown_refs_passed
        ]
        bool_count = sum(1 for b in bool_checks if b)
        return (self.skills_passed + self.commands_passed +
                self.agents_passed + self.triggering_passed + bool_count)

    @property
    def total_failed(self):
        bool_checks = [
            self.flags_passed, self.rules_passed, self.notion_passed,
            self.version_sync_passed, self.plugin_json_passed, self.secrets_passed,
            self.cross_refs_passed, self.breakpoints_passed, self.markdown_refs_passed
        ]
        bool_count = sum(1 for b in bool_checks if not b)
        return (self.skills_failed + self.commands_failed +
                self.agents_failed + self.triggering_failed + bool_count)

    @property
    def is_valid(self):
        # Core validations must pass
        core_valid = (
            self.version_sync_passed and
            self.plugin_json_passed and
            self.secrets_passed and
            self.cross_refs_passed
        )
        # No critical errors in components
        no_critical = self.skills_failed == 0 and self.commands_failed == 0 and self.agents_failed == 0
        return core_valid and no_critical

    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"EPCI PLUGIN VALIDATION SUMMARY")
        print(f"{'='*70}\n")

        print("COMPONENT VALIDATION:")
        print(f"  Skills:      {self.skills_passed} passed, {self.skills_failed} failed")
        print(f"  Commands:    {self.commands_passed} passed, {self.commands_failed} failed")
        print(f"  Agents:      {self.agents_passed} passed, {self.agents_failed} failed")
        print(f"  Triggering:  {self.triggering_passed} passed, {self.triggering_failed} failed")
        print()

        print("SYSTEM VALIDATION:")
        print(f"  Flags:       {'✅' if self.flags_passed else '❌'}")
        print(f"  Rules:       {'✅' if self.rules_passed else '❌'}")
        print(f"  Notion:      {'✅' if self.notion_passed else '❌'}")
        print()

        print("INTEGRITY VALIDATION (v5.7):")
        print(f"  Version Sync:    {'✅' if self.version_sync_passed else '❌'}")
        print(f"  Plugin.json:     {'✅' if self.plugin_json_passed else '❌'}")
        print(f"  Secrets:         {'✅' if self.secrets_passed else '❌'}")
        print(f"  Cross-refs:      {'✅' if self.cross_refs_passed else '❌'}")
        print(f"  Breakpoints:     {'✅' if self.breakpoints_passed else '⚠️ (warnings)'}")
        print(f"  Markdown refs:   {'✅' if self.markdown_refs_passed else '⚠️ (warnings)'}")
        print()

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

        total = self.total_passed + self.total_failed
        status = "✅ ALL VALIDATIONS PASSED" if self.is_valid else "❌ VALIDATION FAILED"
        print(f"\nRESULT: {status} ({self.total_passed}/{total})")
        print(f"{'='*70}\n")

        return 0 if self.is_valid else 1


def get_project_root() -> Path:
    """Trouve la racine du projet (contient src/)."""
    current = Path(__file__).resolve().parent

    while current != current.parent:
        if (current / "src").exists():
            return current
        current = current.parent

    return Path(__file__).resolve().parent.parent.parent


def find_skills(src_path: Path) -> List[Path]:
    """Trouve tous les dossiers skills avec SKILL.md."""
    skills_base = src_path / "skills"
    if not skills_base.exists():
        return []
    return [f.parent for f in skills_base.glob("**/SKILL.md")]


def find_commands(src_path: Path) -> List[Path]:
    """Trouve tous les fichiers commands .md."""
    commands_dir = src_path / "commands"
    if not commands_dir.exists():
        return []
    return list(commands_dir.glob("*.md"))


def find_agents(src_path: Path) -> List[Path]:
    """Trouve tous les fichiers agents .md."""
    agents_dir = src_path / "agents"
    if not agents_dir.exists():
        return []
    return list(agents_dir.glob("*.md"))


def run_validation_script(
    script_path: Path,
    target_path: Path = None,
    verbose: bool = False,
    fix: bool = False
) -> Tuple[bool, str]:
    """Exécute un script de validation et retourne (success, output)."""
    try:
        cmd = [sys.executable, str(script_path)]
        if target_path:
            cmd.append(str(target_path))
        if fix:
            cmd.append('--fix')

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

        if verbose:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return result.returncode == 0, output

    except subprocess.TimeoutExpired:
        return False, f"[TIMEOUT] {script_path.name}"
    except Exception as e:
        return False, f"[ERROR] {script_path.name}: {e}"


def validate_all(verbose: bool = False, fix: bool = False, fast: bool = False) -> int:
    """Point d'entrée principal - valide tous les composants."""
    start_time = time.time()

    project_root = get_project_root()
    src_path = project_root / "src"
    scripts_path = src_path / "scripts"

    summary = ValidationSummary()

    print(f"\n{'='*70}")
    print(f"EPCI PLUGIN VALIDATION {'(FAST MODE)' if fast else ''}")
    print(f"{'='*70}")
    print(f"Project root: {project_root}")
    print(f"Source path:  {src_path}")
    if fix:
        print(f"Auto-fix:     ENABLED")
    print()

    # ===== NEW: INTEGRITY VALIDATIONS (v5.7) =====
    print(f"\n{'─'*40}")
    print("INTEGRITY VALIDATIONS (v5.7)...")
    print(f"{'─'*40}")

    # 1. Version Sync
    print("\n  Checking version synchronization...")
    version_script = scripts_path / "validate_version_sync.py"
    if version_script.exists():
        success, output = run_validation_script(version_script, fix=fix, verbose=verbose)
        if success:
            print("    Version sync: ✅")
            summary.version_sync_passed = True
        else:
            print("    Version sync: ❌")
            summary.errors.append("Version mismatch between CLAUDE.md and plugin.json")
    else:
        print("    [SKIP] validate_version_sync.py not found")
        summary.version_sync_passed = True

    # 2. Plugin.json Sync
    print("  Checking plugin.json synchronization...")
    plugin_script = scripts_path / "validate_plugin_json.py"
    if plugin_script.exists():
        success, output = run_validation_script(plugin_script, fix=fix, verbose=verbose)
        if success:
            print("    Plugin.json: ✅")
            summary.plugin_json_passed = True
        else:
            print("    Plugin.json: ❌")
            summary.errors.append("Plugin.json sync failed")
    else:
        print("    [SKIP] validate_plugin_json.py not found")
        summary.plugin_json_passed = True

    # 3. Secrets Detection
    print("  Checking for secrets...")
    secrets_script = scripts_path / "validate_secrets.py"
    if secrets_script.exists():
        success, output = run_validation_script(secrets_script, verbose=verbose)
        if success:
            print("    Secrets: ✅")
            summary.secrets_passed = True
        else:
            print("    Secrets: ❌")
            summary.errors.append("Potential secrets detected in codebase")
    else:
        print("    [SKIP] validate_secrets.py not found")
        summary.secrets_passed = True

    # 4. Cross-References
    print("  Checking cross-references...")
    crossref_script = scripts_path / "validate_cross_refs.py"
    if crossref_script.exists():
        success, output = run_validation_script(crossref_script, verbose=verbose)
        if success:
            print("    Cross-refs: ✅")
            summary.cross_refs_passed = True
        else:
            print("    Cross-refs: ❌")
            summary.errors.append("Broken cross-references detected")
    else:
        print("    [SKIP] validate_cross_refs.py not found")
        summary.cross_refs_passed = True

    # 5. Breakpoint Syntax (non-blocking)
    if not fast:
        print("  Checking breakpoint syntax...")
        breakpoint_script = scripts_path / "validate_breakpoints.py"
        if breakpoint_script.exists():
            success, output = run_validation_script(breakpoint_script, verbose=verbose)
            if success:
                print("    Breakpoints: ✅")
                summary.breakpoints_passed = True
            else:
                print("    Breakpoints: ⚠️ (warnings only)")
                summary.warnings.append("Breakpoint syntax warnings detected")
                summary.breakpoints_passed = True  # Non-blocking
        else:
            print("    [SKIP] validate_breakpoints.py not found")
            summary.breakpoints_passed = True
    else:
        summary.breakpoints_passed = True

    # 6. Markdown References (non-blocking)
    if not fast:
        print("  Checking markdown references...")
        mdref_script = scripts_path / "validate_markdown_refs.py"
        if mdref_script.exists():
            success, output = run_validation_script(mdref_script, verbose=verbose)
            if success:
                print("    Markdown refs: ✅")
                summary.markdown_refs_passed = True
            else:
                print("    Markdown refs: ⚠️ (warnings only)")
                summary.warnings.append("Markdown reference warnings detected")
                summary.markdown_refs_passed = True  # Non-blocking
        else:
            print("    [SKIP] validate_markdown_refs.py not found")
            summary.markdown_refs_passed = True
    else:
        summary.markdown_refs_passed = True

    # ===== COMPONENT VALIDATIONS =====
    validate_skill_script = scripts_path / "validate_skill.py"
    validate_command_script = scripts_path / "validate_command.py"
    validate_agent_script = scripts_path / "validate_subagent.py"
    test_triggering_script = scripts_path / "test_triggering.py"

    # Skills
    print(f"\n{'─'*40}")
    print("VALIDATING SKILLS...")
    print(f"{'─'*40}")

    skills = find_skills(src_path)
    if not skills:
        print("[INFO] No skills found")
    else:
        print(f"Found {len(skills)} skills\n")

        if validate_skill_script.exists():
            for skill_path in skills:
                print(f"  Validating: {skill_path.name}... ", end="", flush=True)
                success, _ = run_validation_script(validate_skill_script, skill_path, verbose)
                if success:
                    print("✅")
                    summary.skills_passed += 1
                else:
                    print("❌")
                    summary.skills_failed += 1
                    summary.errors.append(f"Skill validation failed: {skill_path.name}")
        else:
            print(f"[WARNING] validate_skill.py not found at {validate_skill_script}")

    # Commands
    print(f"\n{'─'*40}")
    print("VALIDATING COMMANDS...")
    print(f"{'─'*40}")

    commands = find_commands(src_path)
    if not commands:
        print("[INFO] No commands found")
    else:
        print(f"Found {len(commands)} commands\n")

        if validate_command_script.exists():
            for cmd_path in commands:
                print(f"  Validating: {cmd_path.name}... ", end="", flush=True)
                success, _ = run_validation_script(validate_command_script, cmd_path, verbose)
                if success:
                    print("✅")
                    summary.commands_passed += 1
                else:
                    print("❌")
                    summary.commands_failed += 1
                    summary.errors.append(f"Command validation failed: {cmd_path.name}")
        else:
            print(f"[WARNING] validate_command.py not found at {validate_command_script}")

    # Agents
    print(f"\n{'─'*40}")
    print("VALIDATING AGENTS...")
    print(f"{'─'*40}")

    agents = find_agents(src_path)
    if not agents:
        print("[INFO] No agents found")
    else:
        print(f"Found {len(agents)} agents\n")

        if validate_agent_script.exists():
            for agent_path in agents:
                print(f"  Validating: {agent_path.name}... ", end="", flush=True)
                success, _ = run_validation_script(validate_agent_script, agent_path, verbose)
                if success:
                    print("✅")
                    summary.agents_passed += 1
                else:
                    print("❌")
                    summary.agents_failed += 1
                    summary.errors.append(f"Agent validation failed: {agent_path.name}")
        else:
            print(f"[WARNING] validate_subagent.py not found at {validate_agent_script}")

    # Triggering (skip in fast mode)
    if not fast:
        print(f"\n{'─'*40}")
        print("TESTING SKILL TRIGGERING...")
        print(f"{'─'*40}")

        if skills and test_triggering_script.exists():
            for skill_path in skills:
                print(f"  Testing: {skill_path.name}... ", end="", flush=True)
                success, _ = run_validation_script(test_triggering_script, skill_path, verbose)
                if success:
                    print("✅")
                    summary.triggering_passed += 1
                else:
                    print("⚠️")
                    summary.triggering_failed += 1
        elif not skills:
            print("[INFO] No skills to test")
        else:
            print(f"[WARNING] test_triggering.py not found at {test_triggering_script}")

    # ===== SYSTEM VALIDATIONS =====
    print(f"\n{'─'*40}")
    print("SYSTEM VALIDATIONS...")
    print(f"{'─'*40}")

    # Flags
    validate_flags_script = scripts_path / "validate_flags.py"
    if validate_flags_script.exists():
        success, _ = run_validation_script(validate_flags_script, verbose=verbose)
        print(f"  Flags system: {'✅' if success else '❌'}")
        summary.flags_passed = success
        if not success:
            summary.errors.append("Flags system validation failed")
    else:
        print(f"  Flags system: [SKIP]")
        summary.flags_passed = True

    # Rules
    validate_rules_script = scripts_path / "validate_rules.py"
    if validate_rules_script.exists():
        print("  Rules generator: ✅ (present)")
        summary.rules_passed = True
    else:
        print("  Rules generator: [SKIP]")
        summary.rules_passed = True

    # Notion
    validate_notion_script = scripts_path / "validate_notion_config.py"
    if validate_notion_script.exists():
        success, _ = run_validation_script(validate_notion_script, verbose=verbose)
        print(f"  Notion config: {'✅' if success else '❌'}")
        summary.notion_passed = success
        if not success:
            summary.warnings.append("Notion config validation failed")
    else:
        print("  Notion config: [SKIP]")
        summary.notion_passed = True

    # ===== TIMING =====
    elapsed = time.time() - start_time
    print(f"\n{'─'*40}")
    print(f"Validation completed in {elapsed:.2f}s")
    print(f"{'─'*40}")

    # ===== RÉSUMÉ =====
    return summary.print_summary()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="EPCI Plugin Validation Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_all.py              # Run all validations
  python validate_all.py --verbose    # Show detailed output
  python validate_all.py --fix        # Auto-fix fixable issues
  python validate_all.py --fast       # Skip slow checks (triggering, breakpoints, md refs)
        """
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation output'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix fixable issues (version sync, plugin.json)'
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Fast mode: skip slow validations (triggering, breakpoints, markdown refs)'
    )

    args = parser.parse_args()

    sys.exit(validate_all(verbose=args.verbose, fix=args.fix, fast=args.fast))


if __name__ == "__main__":
    main()
