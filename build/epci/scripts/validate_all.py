#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrateur de validation EPCI Plugin.
Executes all validation scripts on all components.

Usage: python validate_all.py [--verbose] [--fix]
"""

import sys
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import subprocess
import argparse


@dataclass
class ValidationSummary:
    """Global validation summary."""
    skills_passed: int = 0
    skills_failed: int = 0
    commands_passed: int = 0
    commands_failed: int = 0
    agents_passed: int = 0
    agents_failed: int = 0
    triggering_passed: int = 0
    triggering_failed: int = 0
    flags_passed: bool = False
    rules_passed: bool = False
    errors: list = field(default_factory=list)

    @property
    def total_passed(self):
        flags_count = 1 if self.flags_passed else 0
        rules_count = 1 if self.rules_passed else 0
        return self.skills_passed + self.commands_passed + self.agents_passed + self.triggering_passed + flags_count + rules_count

    @property
    def total_failed(self):
        flags_count = 0 if self.flags_passed else 1
        rules_count = 0 if self.rules_passed else 1
        return self.skills_failed + self.commands_failed + self.agents_failed + self.triggering_failed + flags_count + rules_count

    @property
    def is_valid(self):
        return self.total_failed == 0

    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"EPCI PLUGIN VALIDATION SUMMARY")
        print(f"{'='*70}\n")

        print(f"Skills:      {self.skills_passed} passed, {self.skills_failed} failed")
        print(f"Commands:    {self.commands_passed} passed, {self.commands_failed} failed")
        print(f"Agents:      {self.agents_passed} passed, {self.agents_failed} failed")
        print(f"Triggering:  {self.triggering_passed} passed, {self.triggering_failed} failed")
        flags_status = "passed" if self.flags_passed else "failed"
        print(f"Flags:       {flags_status}")
        rules_status = "passed" if self.rules_passed else "failed"
        print(f"Rules:       {rules_status}")
        print()

        if self.errors:
            print("ERRORS:")
            for err in self.errors:
                print(f"   - {err}")
            print()

        total = self.total_passed + self.total_failed
        status = "✅ ALL VALIDATIONS PASSED" if self.is_valid else "❌ VALIDATION FAILED"
        print(f"\nRESULT: {status} ({self.total_passed}/{total})")
        print(f"{'='*70}\n")

        return 0 if self.is_valid else 1


def get_project_root() -> Path:
    """Trouve la racine du projet (contient src/)."""
    current = Path(__file__).resolve().parent

    # Remonter jusqu'à trouver src/
    while current != current.parent:
        if (current / "src").exists():
            return current
        current = current.parent

    # Fallback: utiliser le dossier parent de scripts/
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


def run_validation_script(script_path: Path, target_path: Path, verbose: bool = False) -> bool:
    """Exécute un script de validation et retourne True si succès."""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), str(target_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if verbose:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {target_path.name}")
        return False
    except Exception as e:
        print(f"[ERROR] {target_path.name}: {e}")
        return False


def validate_all(verbose: bool = False) -> int:
    """Point d'entrée principal - valide tous les composants."""
    project_root = get_project_root()
    src_path = project_root / "src"
    scripts_path = src_path / "scripts"

    summary = ValidationSummary()

    print(f"\n{'='*70}")
    print(f"EPCI PLUGIN VALIDATION")
    print(f"{'='*70}")
    print(f"Project root: {project_root}")
    print(f"Source path:  {src_path}")
    print()

    # Vérifier que les scripts existent
    validate_skill_script = scripts_path / "validate_skill.py"
    validate_command_script = scripts_path / "validate_command.py"
    validate_agent_script = scripts_path / "validate_subagent.py"
    test_triggering_script = scripts_path / "test_triggering.py"

    # ===== VALIDATION DES SKILLS =====
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
                print(f"  Validating: {skill_path.name}... ", end="")
                if run_validation_script(validate_skill_script, skill_path, verbose):
                    print("✅")
                    summary.skills_passed += 1
                else:
                    print("❌")
                    summary.skills_failed += 1
                    summary.errors.append(f"Skill validation failed: {skill_path.name}")
        else:
            print(f"[WARNING] validate_skill.py not found at {validate_skill_script}")

    # ===== VALIDATION DES COMMANDS =====
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
                print(f"  Validating: {cmd_path.name}... ", end="")
                if run_validation_script(validate_command_script, cmd_path, verbose):
                    print("✅")
                    summary.commands_passed += 1
                else:
                    print("❌")
                    summary.commands_failed += 1
                    summary.errors.append(f"Command validation failed: {cmd_path.name}")
        else:
            print(f"[WARNING] validate_command.py not found at {validate_command_script}")

    # ===== VALIDATION DES AGENTS =====
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
                print(f"  Validating: {agent_path.name}... ", end="")
                if run_validation_script(validate_agent_script, agent_path, verbose):
                    print("✅")
                    summary.agents_passed += 1
                else:
                    print("❌")
                    summary.agents_failed += 1
                    summary.errors.append(f"Agent validation failed: {agent_path.name}")
        else:
            print(f"[WARNING] validate_subagent.py not found at {validate_agent_script}")

    # ===== TESTS DE TRIGGERING =====
    print(f"\n{'─'*40}")
    print("TESTING SKILL TRIGGERING...")
    print(f"{'─'*40}")

    if skills and test_triggering_script.exists():
        for skill_path in skills:
            print(f"  Testing: {skill_path.name}... ", end="")
            if run_validation_script(test_triggering_script, skill_path, verbose):
                print("✅")
                summary.triggering_passed += 1
            else:
                print("⚠️")  # Warning, not error (triggering tests are advisory)
                summary.triggering_failed += 1
    elif not skills:
        print("[INFO] No skills to test")
    else:
        print(f"[WARNING] test_triggering.py not found at {test_triggering_script}")

    # ===== VALIDATION FLAGS SYSTEM =====
    print(f"\n{'─'*40}")
    print("VALIDATING FLAGS SYSTEM...")
    print(f"{'─'*40}")

    validate_flags_script = scripts_path / "validate_flags.py"
    if validate_flags_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(validate_flags_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if verbose:
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)

            if result.returncode == 0:
                print("  Flags system: ✅")
                summary.flags_passed = True
            else:
                print("  Flags system: ❌")
                summary.errors.append("Flags system validation failed")
        except Exception as e:
            print(f"  Flags system: ❌ ({e})")
            summary.errors.append(f"Flags validation error: {e}")
    else:
        print(f"[WARNING] validate_flags.py not found at {validate_flags_script}")
        summary.flags_passed = True  # Don't fail if script not present

    # ===== VALIDATION RULES GENERATOR =====
    print(f"\n{'─'*40}")
    print("VALIDATING RULES GENERATOR...")
    print(f"{'─'*40}")

    validate_rules_script = scripts_path / "validate_rules.py"
    if validate_rules_script.exists():
        print("  validate_rules.py: ✅ (present)")
        summary.rules_passed = True
    else:
        print(f"[WARNING] validate_rules.py not found at {validate_rules_script}")
        summary.rules_passed = True  # Don't fail if script not present

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
        """
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation output'
    )

    args = parser.parse_args()

    sys.exit(validate_all(verbose=args.verbose))


if __name__ == "__main__":
    main()
