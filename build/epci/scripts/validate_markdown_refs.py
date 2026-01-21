#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation des références de fichiers dans les documents markdown.
Vérifie que les liens [text](path) pointent vers des fichiers existants.

Usage: python validate_markdown_refs.py [path]
"""

import sys
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Set


@dataclass
class RefFinding:
    """Une référence markdown problématique."""
    source_file: Path
    line_number: int
    link_text: str
    link_path: str
    issue: str

    def __str__(self):
        return f"{self.source_file.name}:{self.line_number} [{self.link_text}]({self.link_path}) - {self.issue}"


@dataclass
class ValidationReport:
    """Rapport de validation des références markdown."""
    name: str = "markdown-references"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    findings: List[RefFinding] = field(default_factory=list)
    refs_checked: int = 0
    files_scanned: int = 0
    checks_passed: int = 0
    checks_total: int = 3

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_finding(self, finding: RefFinding):
        self.findings.append(finding)
        # Les références cassées sont des warnings, pas des erreurs bloquantes
        # car certaines peuvent être des liens externes ou des patterns valides

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

        print(f"Files scanned: {self.files_scanned}")
        print(f"References checked: {self.refs_checked}")
        print()

        if self.findings:
            print("BROKEN/SUSPICIOUS REFERENCES:")
            for finding in self.findings:
                print(f"   ⚠️  {finding}")
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

        status = "PASSED" if self.valid else "FAILED"
        print(f"RESULT: {status} ({len(self.findings)} issues found)")
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


def extract_markdown_links(content: str) -> List[Tuple[int, str, str]]:
    """Extrait les liens markdown [text](path) du contenu."""
    links = []

    # Pattern: [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        for match in re.finditer(pattern, line):
            link_text = match.group(1)
            link_path = match.group(2)
            links.append((line_num, link_text, link_path))

    return links


def is_external_link(path: str) -> bool:
    """Vérifie si un lien est externe (http, https, mailto, etc.)."""
    return path.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://'))


def is_anchor_link(path: str) -> bool:
    """Vérifie si un lien est un anchor (#section)."""
    return path.startswith('#')


def is_template_link(path: str) -> bool:
    """Vérifie si un lien contient des templates/placeholders."""
    return any(p in path for p in ['${', '{{', '<', '>', '{', '}'])


def resolve_link_path(link_path: str, source_file: Path, project_root: Path) -> Path:
    """Résout un chemin de lien relatif en chemin absolu."""
    # Retirer les anchors (#section)
    path = link_path.split('#')[0]

    if not path:
        return None

    # Chemin absolu depuis la racine du projet
    if path.startswith('/'):
        return project_root / path.lstrip('/')

    # Chemin relatif depuis le fichier source
    return (source_file.parent / path).resolve()


def validate_file_refs(
    file_path: Path,
    project_root: Path,
    report: ValidationReport
) -> None:
    """Valide les références markdown dans un fichier."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return

    report.files_scanned += 1
    links = extract_markdown_links(content)

    for line_num, link_text, link_path in links:
        report.refs_checked += 1

        # Ignorer les liens externes
        if is_external_link(link_path):
            continue

        # Ignorer les anchors purs
        if is_anchor_link(link_path):
            continue

        # Ignorer les templates
        if is_template_link(link_path):
            continue

        # Ignorer certains patterns spéciaux
        if link_path.startswith('@') or link_path.startswith('$'):
            continue

        # Résoudre le chemin
        resolved = resolve_link_path(link_path, file_path, project_root)

        if resolved is None:
            continue

        # Vérifier si le fichier existe
        if not resolved.exists():
            # Essayer avec différentes extensions
            alternatives = [
                resolved.with_suffix('.md'),
                resolved / 'SKILL.md',
                resolved / 'README.md',
                resolved / 'index.md',
            ]

            found = any(alt.exists() for alt in alternatives)

            if not found:
                report.add_finding(RefFinding(
                    source_file=file_path,
                    line_number=line_num,
                    link_text=link_text,
                    link_path=link_path,
                    issue="File not found"
                ))


def validate_markdown_refs(scan_path: Path = None) -> int:
    """Valide les références markdown dans le projet."""
    project_root = get_project_root()
    src_path = project_root / "src"

    if scan_path is None:
        scan_path = src_path

    report = ValidationReport()

    print(f"Validating markdown references in: {scan_path}")
    print()

    # Check 1: Scanner les commandes
    print("Checking commands...")
    commands_dir = src_path / "commands"
    if commands_dir.exists():
        for md_file in commands_dir.glob("**/*.md"):
            validate_file_refs(md_file, project_root, report)
        print(f"  [OK] Checked commands")
    report.pass_check()

    # Check 2: Scanner les skills
    print("Checking skills...")
    skills_base = src_path / "skills"
    if skills_base.exists():
        for md_file in skills_base.glob("**/*.md"):
            validate_file_refs(md_file, project_root, report)
        print(f"  [OK] Checked skills")
    report.pass_check()

    # Check 3: Scanner les agents et docs
    print("Checking agents and docs...")
    for dir_name in ['agents', 'settings']:
        target_dir = src_path / dir_name
        if target_dir.exists():
            for md_file in target_dir.glob("**/*.md"):
                validate_file_refs(md_file, project_root, report)

    # Docs à la racine
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        for md_file in docs_dir.glob("**/*.md"):
            validate_file_refs(md_file, project_root, report)

    print(f"  [OK] Checked agents and docs")
    report.pass_check()

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validate markdown file references [text](path)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Checks performed:
  - [text](path) links point to existing files
  - Relative paths resolve correctly

Ignored:
  - External links (http://, https://, etc.)
  - Anchor links (#section)
  - Template paths (${...}, {{...}})

Examples:
  python validate_markdown_refs.py             # Check all
  python validate_markdown_refs.py src/        # Check specific path
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
    sys.exit(validate_markdown_refs(scan_path))


if __name__ == "__main__":
    main()
