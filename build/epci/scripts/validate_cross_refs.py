#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation des références croisées entre composants EPCI:
- @skill:xxx dans commands/agents pointe vers un skill existant
- @agent-name dans commands pointe vers un agent existant
- Patterns de références internes sont valides

Usage: python validate_cross_refs.py [path]
"""

import sys
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple


@dataclass
class CrossRefFinding:
    """Une référence croisée problématique."""
    source_file: Path
    line_number: int
    ref_type: str
    ref_target: str
    issue: str

    def __str__(self):
        return f"{self.source_file.name}:{self.line_number} [{self.ref_type}] {self.ref_target} - {self.issue}"


@dataclass
class ValidationReport:
    """Rapport de validation des références croisées."""
    name: str = "cross-references"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    findings: List[CrossRefFinding] = field(default_factory=list)
    refs_checked: int = 0
    checks_passed: int = 0
    checks_total: int = 4

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_finding(self, finding: CrossRefFinding):
        self.findings.append(finding)
        if finding.issue.startswith("Missing"):
            self.valid = False

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

        print(f"References checked: {self.refs_checked}")
        print()

        if self.findings:
            errors = [f for f in self.findings if f.issue.startswith("Missing")]
            warnings = [f for f in self.findings if not f.issue.startswith("Missing")]

            if errors:
                print("BROKEN REFERENCES:")
                for finding in errors:
                    print(f"   ❌ {finding}")
                print()

            if warnings:
                print("WARNINGS:")
                for finding in warnings:
                    print(f"   ⚠️  {finding}")
                print()

        if self.errors:
            print("ERRORS:")
            for err in self.errors:
                print(f"   ❌ {err}")
            print()

        status = "PASSED" if self.valid else "FAILED"
        broken_count = len([f for f in self.findings if f.issue.startswith("Missing")])
        print(f"RESULT: {status} ({broken_count} broken references)")
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


def get_available_skills(src_path: Path) -> Set[str]:
    """Récupère la liste des skills disponibles."""
    skills = set()
    skills_base = src_path / "skills"

    if not skills_base.exists():
        return skills

    for skill_md in skills_base.glob("**/SKILL.md"):
        # Nom du skill = nom du dossier parent
        skill_name = skill_md.parent.name
        skills.add(skill_name)

    return skills


def get_available_agents(src_path: Path) -> Set[str]:
    """Récupère la liste des agents disponibles."""
    agents = set()
    agents_dir = src_path / "agents"

    if not agents_dir.exists():
        return agents

    for agent_md in agents_dir.glob("*.md"):
        # Nom de l'agent = nom du fichier sans .md
        agent_name = agent_md.stem
        agents.add(agent_name)

    return agents


def get_available_commands(src_path: Path) -> Set[str]:
    """Récupère la liste des commandes disponibles."""
    commands = set()
    commands_dir = src_path / "commands"

    if not commands_dir.exists():
        return commands

    for cmd_md in commands_dir.glob("*.md"):
        command_name = cmd_md.stem
        commands.add(command_name)

    return commands


def extract_skill_refs(content: str) -> List[Tuple[int, str]]:
    """Extrait les références @skill:xxx du contenu."""
    refs = []

    # Pattern: @skill:skill-name ou @skill:{skill-name}
    patterns = [
        r'@skill:([a-z0-9-]+)',
        r'@skill:\{([a-z0-9-]+)\}',
        r'skill\s+`([a-z0-9-]+)`',  # Mention textuelle: skill `name`
    ]

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                skill_name = match.group(1).lower()
                refs.append((line_num, skill_name))

    return refs


def extract_agent_refs(content: str) -> List[Tuple[int, str]]:
    """Extrait les références @agent-name du contenu."""
    refs = []

    # Pattern: @agent-name, @planner, etc.
    patterns = [
        r'@([a-z]+-[a-z]+(?:-[a-z]+)*)',  # @plan-validator, @code-reviewer
        r'@([a-z]+er)',  # @planner, @clarifier, @implementer
        r'subagent\s+`([a-z0-9-]+)`',  # subagent `name`
    ]

    # Agents connus pour filtrer les faux positifs
    known_agents = {
        'plan-validator', 'code-reviewer', 'security-auditor', 'qa-reviewer',
        'doc-generator', 'decompose-validator', 'rules-validator',
        'clarifier', 'planner', 'implementer',
        'ems-evaluator', 'technique-advisor', 'party-orchestrator',
        'expert-panel', 'rule-clarifier', 'statusline-setup'
    }

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                ref_name = match.group(1).lower()
                # Filtrer pour ne garder que les noms qui ressemblent à des agents
                if ref_name in known_agents or ref_name.endswith('-validator') or ref_name.endswith('-reviewer'):
                    refs.append((line_num, ref_name))

    return refs


def extract_reference_paths(content: str, source_file: Path) -> List[Tuple[int, str]]:
    """Extrait les références à des fichiers locaux (references/, @references/)."""
    refs = []

    # Pattern: @references/path ou references/path.md
    patterns = [
        r'@references/([a-z0-9-/]+\.md)',
        r'references/([a-z0-9-/]+\.md)',
        r'See\s+`?([a-z0-9-/]+\.md)`?',
    ]

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                ref_path = match.group(1)
                refs.append((line_num, ref_path))

    return refs


def validate_file_refs(
    file_path: Path,
    available_skills: Set[str],
    available_agents: Set[str],
    src_path: Path,
    report: ValidationReport
) -> None:
    """Valide les références dans un fichier."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return

    # Vérifier les références aux skills
    skill_refs = extract_skill_refs(content)
    for line_num, skill_name in skill_refs:
        report.refs_checked += 1
        if skill_name not in available_skills:
            report.add_finding(CrossRefFinding(
                source_file=file_path,
                line_number=line_num,
                ref_type="skill",
                ref_target=skill_name,
                issue=f"Missing skill: {skill_name}"
            ))

    # Vérifier les références aux agents
    agent_refs = extract_agent_refs(content)
    for line_num, agent_name in agent_refs:
        report.refs_checked += 1
        if agent_name not in available_agents:
            report.add_finding(CrossRefFinding(
                source_file=file_path,
                line_number=line_num,
                ref_type="agent",
                ref_target=agent_name,
                issue=f"Missing agent: {agent_name}"
            ))

    # Vérifier les références aux fichiers locaux
    ref_paths = extract_reference_paths(content, file_path)
    for line_num, ref_path in ref_paths:
        report.refs_checked += 1

        # Résoudre le chemin relatif
        if file_path.parent.name in ['commands', 'agents']:
            # Pour commands/ et agents/, references/ est dans le même dossier
            base_path = file_path.parent / "references"
        else:
            # Pour skills, references/ est dans le dossier du skill
            base_path = file_path.parent / "references"

        full_path = base_path / ref_path.replace('references/', '')

        # Aussi essayer depuis src/
        alt_path = src_path / "commands" / "references" / ref_path.replace('references/', '')

        if not full_path.exists() and not alt_path.exists():
            # Ne pas traiter comme erreur, juste warning
            report.add_finding(CrossRefFinding(
                source_file=file_path,
                line_number=line_num,
                ref_type="file",
                ref_target=ref_path,
                issue=f"Reference file may not exist: {ref_path}"
            ))


def validate_cross_refs(scan_path: Path = None) -> int:
    """Valide les références croisées dans le projet."""
    project_root = get_project_root()
    src_path = project_root / "src"

    if scan_path is None:
        scan_path = src_path

    report = ValidationReport()

    print(f"Validating cross-references in: {scan_path}")
    print()

    # Check 1: Récupérer la liste des composants disponibles
    print("Loading available components...")
    available_skills = get_available_skills(src_path)
    available_agents = get_available_agents(src_path)
    available_commands = get_available_commands(src_path)

    print(f"  Skills: {len(available_skills)}")
    print(f"  Agents: {len(available_agents)}")
    print(f"  Commands: {len(available_commands)}")
    report.pass_check()

    # Check 2: Valider les références dans les commands
    print("\nChecking commands references...")
    commands_dir = src_path / "commands"
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            validate_file_refs(cmd_file, available_skills, available_agents, src_path, report)
        print(f"  [OK] Checked {len(list(commands_dir.glob('*.md')))} commands")
    report.pass_check()

    # Check 3: Valider les références dans les agents
    print("Checking agents references...")
    agents_dir = src_path / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            validate_file_refs(agent_file, available_skills, available_agents, src_path, report)
        print(f"  [OK] Checked {len(list(agents_dir.glob('*.md')))} agents")
    report.pass_check()

    # Check 4: Valider les références dans les skills
    print("Checking skills references...")
    skills_base = src_path / "skills"
    if skills_base.exists():
        skill_files = list(skills_base.glob("**/SKILL.md"))
        for skill_file in skill_files:
            validate_file_refs(skill_file, available_skills, available_agents, src_path, report)
        print(f"  [OK] Checked {len(skill_files)} skills")
    report.pass_check()

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validate cross-references between EPCI components",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
References checked:
  - @skill:xxx in commands/agents -> skill exists
  - @agent-name in commands -> agent exists
  - references/path.md -> file exists

Examples:
  python validate_cross_refs.py             # Check all
  python validate_cross_refs.py src/        # Check specific path
        """
    )
    parser.add_argument(
        'path',
        nargs='?',
        default=None,
        help='Path to scan (default: src/)'
    )

    args = parser.parse_args()
    scan_path = Path(args.path) if args.path else None
    sys.exit(validate_cross_refs(scan_path))


if __name__ == "__main__":
    main()
