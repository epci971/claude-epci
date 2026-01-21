#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation bidirectionnelle de plugin.json:
1. Chaque entry dans plugin.json pointe vers un fichier existant
2. Chaque fichier skill/command/agent est déclaré dans plugin.json
3. Les deux plugin.json (src/ et build/) sont synchronisés

Usage: python validate_plugin_json.py [--fix]
"""

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional


@dataclass
class ValidationReport:
    """Rapport de validation plugin.json."""
    name: str = "plugin-json-sync"
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

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

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

        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")

        return 0 if self.valid else 1


def get_project_root() -> Path:
    """Trouve la racine du projet (contient src/)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "src").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


def load_plugin_json(file_path: Path) -> Optional[dict]:
    """Charge un fichier plugin.json."""
    if not file_path.exists():
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_plugin_json(file_path: Path, data: dict) -> bool:
    """Sauvegarde un fichier plugin.json."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        return True
    except IOError:
        return False


def find_actual_skills(src_path: Path) -> Set[str]:
    """Trouve tous les skills existants (dossiers avec SKILL.md)."""
    skills_base = src_path / "skills"
    if not skills_base.exists():
        return set()

    skills = set()
    for skill_md in skills_base.glob("**/SKILL.md"):
        # Chemin relatif depuis src/
        rel_path = skill_md.relative_to(src_path)
        skills.add(f"./{rel_path}")
    return skills


def find_actual_commands(src_path: Path) -> Set[str]:
    """Trouve toutes les commandes existantes (.md dans commands/)."""
    commands_dir = src_path / "commands"
    if not commands_dir.exists():
        return set()

    commands = set()
    for cmd_md in commands_dir.glob("*.md"):
        rel_path = cmd_md.relative_to(src_path)
        commands.add(f"./{rel_path}")
    return commands


def find_actual_agents(src_path: Path) -> Set[str]:
    """Trouve tous les agents existants (.md dans agents/)."""
    agents_dir = src_path / "agents"
    if not agents_dir.exists():
        return set()

    agents = set()
    for agent_md in agents_dir.glob("*.md"):
        rel_path = agent_md.relative_to(src_path)
        agents.add(f"./{rel_path}")
    return agents


def validate_entries_exist(
    plugin_data: dict,
    src_path: Path,
    entry_type: str,
    report: ValidationReport
) -> List[str]:
    """Vérifie que chaque entry dans plugin.json pointe vers un fichier existant."""
    entries = plugin_data.get(entry_type, [])
    missing = []

    for entry in entries:
        # Convertir ./path en chemin absolu
        entry_path = src_path / entry.lstrip('./')
        if not entry_path.exists():
            missing.append(entry)

    return missing


def validate_all_declared(
    plugin_data: dict,
    actual_files: Set[str],
    entry_type: str
) -> List[str]:
    """Vérifie que tous les fichiers existants sont déclarés dans plugin.json."""
    declared = set(plugin_data.get(entry_type, []))
    undeclared = actual_files - declared
    return list(undeclared)


def validate_plugin_json(fix: bool = False) -> int:
    """Valide la synchronisation bidirectionnelle de plugin.json."""
    project_root = get_project_root()
    src_path = project_root / "src"
    report = ValidationReport()

    src_plugin_path = src_path / ".claude-plugin" / "plugin.json"
    build_plugin_path = project_root / "build" / "epci" / ".claude-plugin" / "plugin.json"

    # Check 1: src/plugin.json existe
    print("Checking src/.claude-plugin/plugin.json...")
    src_plugin = load_plugin_json(src_plugin_path)
    if src_plugin:
        print(f"  [OK] Loaded src/plugin.json")
        report.pass_check()
    else:
        report.add_error(f"Cannot load src/.claude-plugin/plugin.json")
        return report.print_report()

    # Check 2: Toutes les entries pointent vers des fichiers existants
    print("Checking declared files exist...")
    all_missing = []

    for entry_type in ['commands', 'agents', 'skills']:
        missing = validate_entries_exist(src_plugin, src_path, entry_type, report)
        if missing:
            for m in missing:
                report.add_error(f"Missing {entry_type[:-1]} file: {m}")
            all_missing.extend(missing)

    if not all_missing:
        print(f"  [OK] All declared files exist")
        report.pass_check()

    # Check 3: Tous les fichiers existants sont déclarés
    print("Checking all files are declared...")
    actual_skills = find_actual_skills(src_path)
    actual_commands = find_actual_commands(src_path)
    actual_agents = find_actual_agents(src_path)

    undeclared_skills = validate_all_declared(src_plugin, actual_skills, 'skills')
    undeclared_commands = validate_all_declared(src_plugin, actual_commands, 'commands')
    undeclared_agents = validate_all_declared(src_plugin, actual_agents, 'agents')

    all_undeclared = []

    if undeclared_skills:
        for u in undeclared_skills:
            report.add_warning(f"Undeclared skill: {u}")
        all_undeclared.extend(undeclared_skills)

    if undeclared_commands:
        for u in undeclared_commands:
            report.add_warning(f"Undeclared command: {u}")
        all_undeclared.extend(undeclared_commands)

    if undeclared_agents:
        for u in undeclared_agents:
            report.add_warning(f"Undeclared agent: {u}")
        all_undeclared.extend(undeclared_agents)

    if not all_undeclared:
        print(f"  [OK] All files are declared")
        report.pass_check()
    elif fix:
        # Auto-fix: ajouter les fichiers non déclarés
        print(f"  [FIX] Adding undeclared files to plugin.json...")

        if undeclared_skills:
            src_plugin['skills'] = sorted(list(set(src_plugin.get('skills', [])) | set(undeclared_skills)))
        if undeclared_commands:
            src_plugin['commands'] = sorted(list(set(src_plugin.get('commands', [])) | set(undeclared_commands)))
        if undeclared_agents:
            src_plugin['agents'] = sorted(list(set(src_plugin.get('agents', [])) | set(undeclared_agents)))

        if save_plugin_json(src_plugin_path, src_plugin):
            print(f"  [OK] Updated src/plugin.json with {len(all_undeclared)} new entries")
            report.warnings = []  # Clear warnings since we fixed them
            report.pass_check()

    # Check 4: build/plugin.json existe
    print("Checking build/epci/.claude-plugin/plugin.json...")
    build_plugin = load_plugin_json(build_plugin_path)
    if build_plugin:
        print(f"  [OK] Loaded build/plugin.json")
        report.pass_check()
    else:
        report.add_warning(f"Cannot load build/epci/.claude-plugin/plugin.json")
        report.pass_check()  # Not blocking, just warning
        return report.print_report()

    # Check 5: Les deux plugin.json ont les mêmes entries
    print("Checking src/ and build/ synchronization...")

    sync_issues = []
    for entry_type in ['commands', 'agents', 'skills']:
        src_entries = set(src_plugin.get(entry_type, []))
        build_entries = set(build_plugin.get(entry_type, []))

        if src_entries != build_entries:
            only_in_src = src_entries - build_entries
            only_in_build = build_entries - src_entries

            if only_in_src:
                sync_issues.append(f"{entry_type} only in src/: {only_in_src}")
            if only_in_build:
                sync_issues.append(f"{entry_type} only in build/: {only_in_build}")

    if sync_issues:
        for issue in sync_issues:
            report.add_error(issue)

        if fix:
            # Copier src vers build
            print(f"  [FIX] Syncing build/plugin.json from src/...")
            build_plugin['commands'] = src_plugin.get('commands', [])
            build_plugin['agents'] = src_plugin.get('agents', [])
            build_plugin['skills'] = src_plugin.get('skills', [])

            if save_plugin_json(build_plugin_path, build_plugin):
                print(f"  [OK] Synchronized build/plugin.json")
                report.errors = [e for e in report.errors if 'only in' not in e]
                report.valid = len(report.errors) == 0
                report.pass_check()
    else:
        print(f"  [OK] src/ and build/ are synchronized")
        report.pass_check()

    # Check 6: Pas de doublons dans les entries
    print("Checking for duplicates...")
    duplicates = []
    for entry_type in ['commands', 'agents', 'skills']:
        entries = src_plugin.get(entry_type, [])
        seen = set()
        for entry in entries:
            if entry in seen:
                duplicates.append(f"Duplicate {entry_type[:-1]}: {entry}")
            seen.add(entry)

    if duplicates:
        for d in duplicates:
            report.add_error(d)
    else:
        print(f"  [OK] No duplicates found")
        report.pass_check()

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validate plugin.json bidirectional synchronization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks performed:
  1. All entries in plugin.json point to existing files
  2. All existing skills/commands/agents are declared
  3. src/ and build/ plugin.json are synchronized
  4. No duplicate entries

Examples:
  python validate_plugin_json.py          # Check only
  python validate_plugin_json.py --fix    # Auto-add undeclared files
        """
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix: add undeclared files and sync build/'
    )

    args = parser.parse_args()
    sys.exit(validate_plugin_json(fix=args.fix))


if __name__ == "__main__":
    main()
