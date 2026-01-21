#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détection de secrets et clés API dans le code source.
Scanne les fichiers du projet pour détecter des patterns de secrets.

Usage: python validate_secrets.py [path]
"""

import sys
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Set


# Patterns de secrets à détecter
SECRET_PATTERNS = [
    # API Keys génériques
    (r'api[_-]?key\s*[:=]\s*["\'][^"\']{10,}["\']', 'API Key'),
    (r'apikey\s*[:=]\s*["\'][^"\']{10,}["\']', 'API Key'),

    # OpenAI
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI API Key'),
    (r'sk-proj-[a-zA-Z0-9]{20,}', 'OpenAI Project Key'),

    # AWS
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*["\'][^"\']{10,}["\']', 'AWS Secret Key'),

    # Google
    (r'AIza[0-9A-Za-z\-_]{35}', 'Google API Key'),

    # GitHub
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Token'),
    (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
    (r'github[_-]?token\s*[:=]\s*["\'][^"\']{10,}["\']', 'GitHub Token'),

    # Anthropic
    (r'sk-ant-[a-zA-Z0-9\-]{20,}', 'Anthropic API Key'),

    # Generic secrets
    (r'password\s*[:=]\s*["\'][^"\']{6,}["\']', 'Password'),
    (r'secret\s*[:=]\s*["\'][^"\']{6,}["\']', 'Secret'),
    (r'token\s*[:=]\s*["\'][^"\']{10,}["\']', 'Token'),
    (r'private[_-]?key\s*[:=]\s*["\'][^"\']{10,}["\']', 'Private Key'),

    # Database
    (r'postgres://[^\s"\']+:[^\s"\']+@', 'PostgreSQL Connection String'),
    (r'mysql://[^\s"\']+:[^\s"\']+@', 'MySQL Connection String'),
    (r'mongodb\+srv://[^\s"\']+:[^\s"\']+@', 'MongoDB Connection String'),

    # Bearer tokens
    (r'[Bb]earer\s+[a-zA-Z0-9\-_.]{20,}', 'Bearer Token'),
]

# Fichiers/dossiers à ignorer
IGNORE_PATTERNS = {
    '.git',
    '__pycache__',
    'node_modules',
    '.venv',
    'venv',
    '.env.example',
    '.env.template',
    '.env.sample',
    'package-lock.json',
    'yarn.lock',
    'poetry.lock',
}

# Extensions à scanner
SCAN_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.json', '.yaml', '.yml', '.toml',
    '.md', '.txt', '.sh', '.bash',
    '.env', '.cfg', '.conf', '.ini',
}


@dataclass
class SecretFinding:
    """Un secret potentiel détecté."""
    file_path: Path
    line_number: int
    pattern_name: str
    matched_text: str

    def __str__(self):
        # Masquer le secret dans l'affichage
        masked = self.matched_text[:10] + '...' if len(self.matched_text) > 10 else self.matched_text
        return f"{self.file_path}:{self.line_number} [{self.pattern_name}] {masked}"


@dataclass
class ValidationReport:
    """Rapport de validation des secrets."""
    name: str = "secrets-detection"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    findings: List[SecretFinding] = field(default_factory=list)
    files_scanned: int = 0
    checks_passed: int = 0
    checks_total: int = 2

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_finding(self, finding: SecretFinding):
        self.findings.append(finding)
        self.valid = False

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.name}")
        print(f"{'='*60}\n")

        print(f"Files scanned: {self.files_scanned}")
        print()

        if self.findings:
            print("POTENTIAL SECRETS DETECTED:")
            for finding in self.findings:
                print(f"   ❌ {finding}")
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
        findings_count = len(self.findings)
        print(f"RESULT: {status} ({findings_count} potential secrets found)")
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


def should_ignore(path: Path) -> bool:
    """Vérifie si un chemin doit être ignoré."""
    parts = path.parts
    for part in parts:
        if part in IGNORE_PATTERNS:
            return True

    # Ignorer les fichiers .example ou .template
    if path.name.endswith('.example') or path.name.endswith('.template'):
        return True

    # Ignorer les fichiers de test (contiennent des exemples de secrets pour les tests)
    if path.name.startswith('test_') or '/tests/' in str(path):
        return True

    return False


def should_scan(path: Path) -> bool:
    """Vérifie si un fichier doit être scanné."""
    if not path.is_file():
        return False

    if should_ignore(path):
        return False

    # Scanner les fichiers sans extension (potentiellement des scripts)
    if path.suffix == '':
        return True

    return path.suffix.lower() in SCAN_EXTENSIONS


def is_false_positive(line: str, match: str, pattern_name: str) -> bool:
    """Détecte les faux positifs courants."""
    line_lower = line.lower()
    match_lower = match.lower()

    # Commentaires TODO/FIXME
    if 'todo' in line_lower or 'fixme' in line_lower:
        return True

    # Placeholders
    placeholders = [
        'your_', 'your-', 'replace', 'example', 'sample',
        'xxx', 'yyy', 'zzz', 'placeholder', 'changeme',
        '<your', '<api', '<secret', '<token',
        '${', '{{', 'env.', 'process.env',
        '%env(', 'getenv(', 'os.environ',
    ]
    for ph in placeholders:
        if ph in match_lower or ph in line_lower:
            return True

    # Documentation / comments
    if line.strip().startswith('#') or line.strip().startswith('//'):
        # Vérifier si c'est un vrai secret ou juste de la doc
        doc_keywords = ['example', 'format', 'looks like', 'pattern', 'e.g.']
        for kw in doc_keywords:
            if kw in line_lower:
                return True

    # Markdown code blocks (documentation examples)
    if '```' in line or line.strip().startswith('|'):
        return True

    # YAML/config examples with environment variable references
    if '%env(' in match or "env(" in match_lower:
        return True

    # Symfony/Laravel style env references
    if match.startswith("'%") or match.startswith('"%'):
        return True

    # Connection string templates
    if 'user:password@' in match_lower or 'username:password@' in match_lower:
        return True

    # Documentation patterns
    doc_patterns = ['user:', 'myuser:', 'dbuser:', 'admin:']
    for dp in doc_patterns:
        if dp in match_lower:
            return True

    # Test fixtures
    if 'test' in match_lower or 'mock' in match_lower:
        return True

    # Security auditor documentation (contains example patterns)
    if 'auditor' in str(match).lower() or 'owasp' in line_lower:
        return True

    # Example API keys in documentation (sk-1234...)
    if re.match(r'sk-[0-9a-f]+$', match) or 'sk-1234' in match:
        return True

    # Docker/CI example connection strings (postgres:postgres@postgres)
    if 'postgres:postgres@' in match or 'user:user@' in match:
        return True

    # Symfony kernel.secret references
    if '%kernel.secret%' in match or 'kernel.secret' in match_lower:
        return True

    return False


def scan_file(file_path: Path) -> List[SecretFinding]:
    """Scanne un fichier pour des secrets potentiels."""
    findings = []

    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return findings

    lines = content.splitlines()

    for line_num, line in enumerate(lines, 1):
        for pattern, pattern_name in SECRET_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                matched_text = match.group(0)

                # Filtrer les faux positifs
                if not is_false_positive(line, matched_text, pattern_name):
                    findings.append(SecretFinding(
                        file_path=file_path,
                        line_number=line_num,
                        pattern_name=pattern_name,
                        matched_text=matched_text
                    ))

    return findings


def validate_secrets(scan_path: Path = None) -> int:
    """Scanne le projet pour des secrets potentiels."""
    if scan_path is None:
        scan_path = get_project_root() / "src"

    report = ValidationReport()

    print(f"Scanning for secrets in: {scan_path}")
    print()

    # Check 1: Le chemin existe
    if not scan_path.exists():
        report.add_error(f"Path not found: {scan_path}")
        return report.print_report()

    report.pass_check()

    # Check 2: Scanner tous les fichiers
    print("Scanning files...")

    if scan_path.is_file():
        files_to_scan = [scan_path] if should_scan(scan_path) else []
    else:
        files_to_scan = [f for f in scan_path.rglob('*') if should_scan(f)]

    for file_path in files_to_scan:
        report.files_scanned += 1
        findings = scan_file(file_path)
        for finding in findings:
            report.add_finding(finding)

    if not report.findings:
        print(f"  [OK] No secrets detected in {report.files_scanned} files")
        report.pass_check()
    else:
        print(f"  [WARNING] {len(report.findings)} potential secrets in {report.files_scanned} files")

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Detect potential secrets and API keys in source code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Patterns detected:
  - API keys (generic, OpenAI, AWS, Google, GitHub, Anthropic)
  - Passwords, secrets, tokens
  - Database connection strings
  - Bearer tokens

Ignored:
  - .env.example, .env.template files
  - Comments with TODO/FIXME
  - Placeholder values (your_key, example, etc.)

Examples:
  python validate_secrets.py                    # Scan src/
  python validate_secrets.py /path/to/scan     # Scan specific path
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
    sys.exit(validate_secrets(scan_path))


if __name__ == "__main__":
    main()
