#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation de la syntaxe des invocations @skill:breakpoint-display.
Vérifie que le format YAML est correct et les champs obligatoires présents.

Usage: python validate_breakpoints.py [path]
"""

import sys
import re
import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict


@dataclass
class BreakpointFinding:
    """Un problème de syntaxe breakpoint."""
    source_file: Path
    line_number: int
    issue: str
    severity: str = "warning"  # "error" ou "warning"

    def __str__(self):
        return f"{self.source_file.name}:{self.line_number} - {self.issue}"


@dataclass
class ValidationReport:
    """Rapport de validation des breakpoints."""
    name: str = "breakpoint-syntax"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    findings: List[BreakpointFinding] = field(default_factory=list)
    breakpoints_found: int = 0
    checks_passed: int = 0
    checks_total: int = 3

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_finding(self, finding: BreakpointFinding):
        self.findings.append(finding)
        if finding.severity == "error":
            self.valid = False

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

        print(f"Breakpoint invocations found: {self.breakpoints_found}")
        print()

        if self.findings:
            errors = [f for f in self.findings if f.severity == "error"]
            warnings = [f for f in self.findings if f.severity == "warning"]

            if errors:
                print("ERRORS:")
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
        error_count = len([f for f in self.findings if f.severity == "error"])
        print(f"RESULT: {status} ({error_count} errors found)")
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


# Types de breakpoints valides
VALID_BREAKPOINT_TYPES = {
    # Core types
    'analysis', 'plan-review', 'implementation', 'validation',
    'checkpoint', 'decision', 'error', 'warning', 'info',
    # Extended types (from SKILL.md documentation)
    'clarification-input', 'decomposition', 'diagnostic',
    'ems-status', 'info-only', 'interactive-plan',
    'lightweight', 'research-prompt'
}

# Champs obligatoires par type
REQUIRED_FIELDS = {
    'analysis': ['type', 'title'],
    'plan-review': ['type', 'title', 'data'],
    'implementation': ['type', 'title'],
    'validation': ['type', 'title'],
    'checkpoint': ['type', 'title'],
    'decision': ['type', 'title', 'ask'],
    'error': ['type', 'title'],
    'warning': ['type', 'title'],
    'info': ['type', 'title'],
}


def extract_breakpoint_blocks(content: str) -> List[Tuple[int, str]]:
    """Extrait les blocs @skill:breakpoint-display du contenu.

    Exclut les blocs qui sont dans:
    - Code fences markdown (``` ou ~~~) - documentation/exemples
    - YAML frontmatter (entre --- délimiteurs) - métadonnées fichier
    """
    blocks = []
    lines = content.splitlines()
    in_code_fence = False
    in_frontmatter = False
    frontmatter_line_count = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track YAML frontmatter (only at start of file, between --- markers)
        if stripped == '---':
            if i == 0 or (in_frontmatter and frontmatter_line_count > 0):
                in_frontmatter = not in_frontmatter
                frontmatter_line_count = 0
                i += 1
                continue
        if in_frontmatter:
            frontmatter_line_count += 1
            i += 1
            continue

        # Track code fence state (``` or ~~~)
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_code_fence = not in_code_fence
            i += 1
            continue

        # Skip breakpoints inside code fences (documentation examples)
        if in_code_fence:
            i += 1
            continue

        # Detect breakpoint invocation
        if '@skill:breakpoint-display' in line:
            line_number = i + 1  # 1-indexed
            yaml_lines = []
            i += 1

            # Capture indented YAML lines following the invocation
            while i < len(lines):
                next_line = lines[i]
                # Check for code fence inside YAML block (shouldn't happen but safety)
                if next_line.strip().startswith('```') or next_line.strip().startswith('~~~'):
                    break
                # YAML block continues while lines are indented
                if next_line and (next_line[0] == ' ' or next_line[0] == '\t'):
                    yaml_lines.append(next_line)
                    i += 1
                elif not next_line.strip():
                    # Empty line might be part of YAML or end of block
                    # Check if next non-empty line is still indented
                    break
                else:
                    # Non-indented line = end of YAML block
                    break

            if yaml_lines:
                yaml_block = '\n'.join(yaml_lines)
                blocks.append((line_number, yaml_block))
            continue

        i += 1

    return blocks


def parse_breakpoint_yaml(yaml_block: str) -> Tuple[Optional[Dict], Optional[str]]:
    """Parse un bloc YAML de breakpoint et retourne les données ou une erreur."""
    # Nettoyer l'indentation
    lines = yaml_block.splitlines()

    # Trouver l'indentation minimale
    min_indent = float('inf')
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)

    # Retirer l'indentation commune
    if min_indent < float('inf'):
        lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]

    cleaned_yaml = '\n'.join(lines)

    try:
        data = yaml.safe_load(cleaned_yaml)
        return data, None
    except yaml.YAMLError as e:
        return None, str(e)


def validate_breakpoint_block(
    yaml_data: Dict,
    line_number: int,
    source_file: Path,
    report: ValidationReport
) -> None:
    """Valide un bloc breakpoint parsé."""

    # Vérifier que yaml_data est bien un dict
    if not isinstance(yaml_data, dict):
        report.add_finding(BreakpointFinding(
            source_file=source_file,
            line_number=line_number,
            issue="Breakpoint block should be a YAML mapping",
            severity="error"
        ))
        return

    # Vérifier le champ type
    bp_type = yaml_data.get('type')
    if not bp_type:
        report.add_finding(BreakpointFinding(
            source_file=source_file,
            line_number=line_number,
            issue="Missing required field: type",
            severity="error"
        ))
        return

    # Vérifier que bp_type est une string
    if not isinstance(bp_type, str):
        report.add_finding(BreakpointFinding(
            source_file=source_file,
            line_number=line_number,
            issue=f"Field 'type' should be a string, got {type(bp_type).__name__}",
            severity="error"
        ))
        return

    if bp_type not in VALID_BREAKPOINT_TYPES:
        report.add_finding(BreakpointFinding(
            source_file=source_file,
            line_number=line_number,
            issue=f"Unknown breakpoint type: {bp_type}",
            severity="warning"
        ))

    # Vérifier les champs obligatoires selon le type
    required = REQUIRED_FIELDS.get(bp_type, ['type', 'title'])
    for field in required:
        if field not in yaml_data:
            report.add_finding(BreakpointFinding(
                source_file=source_file,
                line_number=line_number,
                issue=f"Missing required field for type '{bp_type}': {field}",
                severity="warning"
            ))

    # Vérifier la structure de 'ask' si présent
    if 'ask' in yaml_data:
        ask = yaml_data['ask']
        if isinstance(ask, dict):
            if 'question' not in ask:
                report.add_finding(BreakpointFinding(
                    source_file=source_file,
                    line_number=line_number,
                    issue="ask block missing 'question' field",
                    severity="warning"
                ))
            if 'options' not in ask:
                report.add_finding(BreakpointFinding(
                    source_file=source_file,
                    line_number=line_number,
                    issue="ask block missing 'options' field",
                    severity="warning"
                ))

    # Vérifier la structure de 'data' si présent
    if 'data' in yaml_data:
        data = yaml_data['data']
        if not isinstance(data, dict):
            report.add_finding(BreakpointFinding(
                source_file=source_file,
                line_number=line_number,
                issue="'data' field should be an object/dict",
                severity="warning"
            ))


def validate_file_breakpoints(
    file_path: Path,
    report: ValidationReport
) -> None:
    """Valide les breakpoints dans un fichier."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return

    # Extraire les blocs breakpoint
    blocks = extract_breakpoint_blocks(content)

    for line_number, yaml_block in blocks:
        report.breakpoints_found += 1

        # Parser le YAML
        yaml_data, error = parse_breakpoint_yaml(yaml_block)

        if error:
            report.add_finding(BreakpointFinding(
                source_file=file_path,
                line_number=line_number,
                issue=f"YAML syntax error: {error}",
                severity="error"
            ))
            continue

        if yaml_data:
            validate_breakpoint_block(yaml_data, line_number, file_path, report)


def validate_breakpoints(scan_path: Path = None) -> int:
    """Valide la syntaxe des breakpoints dans le projet."""
    project_root = get_project_root()
    src_path = project_root / "src"

    if scan_path is None:
        scan_path = src_path

    report = ValidationReport()

    print(f"Validating breakpoint syntax in: {scan_path}")
    print()

    # Check 1: Scanner les commands
    print("Checking commands...")
    commands_dir = src_path / "commands"
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            validate_file_breakpoints(cmd_file, report)
        # Aussi vérifier dans references/
        for ref_file in commands_dir.glob("references/**/*.md"):
            validate_file_breakpoints(ref_file, report)
        print(f"  [OK] Checked commands")
    report.pass_check()

    # Check 2: Scanner les skills
    print("Checking skills...")
    skills_base = src_path / "skills"
    if skills_base.exists():
        for skill_file in skills_base.glob("**/SKILL.md"):
            validate_file_breakpoints(skill_file, report)
        for ref_file in skills_base.glob("**/references/**/*.md"):
            validate_file_breakpoints(ref_file, report)
        print(f"  [OK] Checked skills")
    report.pass_check()

    # Check 3: Scanner les agents
    print("Checking agents...")
    agents_dir = src_path / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            validate_file_breakpoints(agent_file, report)
        print(f"  [OK] Checked agents")
    report.pass_check()

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validate @skill:breakpoint-display syntax",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks performed:
  - YAML syntax in breakpoint blocks
  - Required fields (type, title, etc.)
  - Valid breakpoint types
  - Structure of ask and data blocks

Valid types: analysis, plan-review, implementation, validation,
             checkpoint, decision, error, warning, info

Examples:
  python validate_breakpoints.py             # Check all
  python validate_breakpoints.py src/        # Check specific path
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
    sys.exit(validate_breakpoints(scan_path))


if __name__ == "__main__":
    main()
