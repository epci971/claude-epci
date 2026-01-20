#!/usr/bin/env python3
"""
Validation de la configuration Notion pour Promptor.
Vérifie que tous les champs MANDATORY sont présents et valides.

Usage: python validate_notion_config.py [--settings-path PATH]
"""

import json
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    """Rapport de validation config Notion."""
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 5

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print("NOTION CONFIG VALIDATION")
        print(f"{'='*60}\n")

        if self.errors:
            print("⛔ ERRORS (BLOCKING):")
            for err in self.errors:
                print(f"   - {err}")
            print()

        if self.warnings:
            print("⚠️ WARNINGS:")
            for warn in self.warnings:
                print(f"   - {warn}")
            print()

        status = "✅ PASSED" if self.valid else "❌ FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")

        if not self.valid:
            print("\n📋 Action requise:")
            print("   Configurer .claude/settings.local.json avec:")
            print('   {')
            print('     "notion": {')
            print('       "token": "ntn_xxx",')
            print('       "tasks_database_id": "xxx",')
            print('       "default_project_id": "xxx"')
            print('     }')
            print('   }')

        print(f"{'='*60}\n")
        return 0 if self.valid else 1


def get_project_root() -> Path:
    """Trouve la racine du projet."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "src").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


def validate_settings_file(settings_path: Path, report: ValidationReport) -> dict:
    """Vérifie que le fichier settings existe et est valide JSON."""
    if not settings_path.exists():
        report.add_error(f"Fichier non trouvé: {settings_path}")
        return None

    try:
        content = settings_path.read_text(encoding='utf-8')
        data = json.loads(content)
        print(f"[OK] Fichier settings: {settings_path.name}")
        report.pass_check()
        return data
    except json.JSONDecodeError as e:
        report.add_error(f"JSON invalide: {e}")
        return None


def validate_notion_section(data: dict, report: ValidationReport) -> dict:
    """Vérifie la présence de la section notion."""
    if 'notion' not in data:
        report.add_error("Section 'notion' manquante dans settings")
        return None

    notion = data['notion']
    if not isinstance(notion, dict):
        report.add_error("Section 'notion' doit être un objet")
        return None

    print("[OK] Section 'notion': présente")
    report.pass_check()
    return notion


def validate_token(notion: dict, report: ValidationReport) -> bool:
    """Vérifie le token Notion (MANDATORY)."""
    token = notion.get('token', '')

    if not token:
        report.add_error("MANDATORY: 'token' absent ou vide")
        return False

    if not token.startswith('ntn_'):
        report.add_warning(f"Token ne commence pas par 'ntn_': {token[:10]}...")

    if len(token) < 20:
        report.add_error(f"Token trop court ({len(token)} chars)")
        return False

    print(f"[OK] Token: ntn_***{token[-4:]}")
    report.pass_check()
    return True


def validate_database_id(notion: dict, report: ValidationReport) -> bool:
    """Vérifie le tasks_database_id (MANDATORY)."""
    db_id = notion.get('tasks_database_id', '')

    if not db_id:
        report.add_error("MANDATORY: 'tasks_database_id' absent ou vide")
        return False

    # UUID Notion: 32 chars hex (sans tirets) ou 36 avec tirets
    clean_id = db_id.replace('-', '')
    if not re.match(r'^[a-f0-9]{32}$', clean_id):
        report.add_error(f"tasks_database_id invalide (format UUID attendu): {db_id[:16]}...")
        return False

    print(f"[OK] Database ID: {db_id[:8]}...{db_id[-4:]}")
    report.pass_check()
    return True


def validate_project_id(notion: dict, report: ValidationReport) -> bool:
    """Vérifie le default_project_id (MANDATORY - critique pour rangement)."""
    project_id = notion.get('default_project_id', '')

    if not project_id:
        report.add_error("⛔ MANDATORY: 'default_project_id' absent ou vide")
        report.add_error("   → Les tâches seront ORPHELINES sans projet!")
        report.add_error("   → Export Notion BLOQUÉ tant que non configuré")
        return False

    # UUID Notion
    clean_id = project_id.replace('-', '')
    if not re.match(r'^[a-f0-9]{32}$', clean_id):
        report.add_error(f"default_project_id invalide (format UUID attendu): {project_id[:16]}...")
        return False

    print(f"[OK] Project ID: {project_id[:8]}...{project_id[-4:]} (MANDATORY ✓)")
    report.pass_check()
    return True


def validate_notion_config(settings_path: Path = None) -> int:
    """Point d'entrée principal."""
    report = ValidationReport()

    if settings_path is None:
        project_root = get_project_root()
        settings_path = project_root / ".claude" / "settings.local.json"

    print(f"\nValidation config Notion: {settings_path}\n")

    # 1. Vérifier le fichier
    data = validate_settings_file(settings_path, report)
    if data is None:
        return report.print_report()

    # 2. Vérifier section notion
    notion = validate_notion_section(data, report)
    if notion is None:
        return report.print_report()

    # 3. Valider chaque champ MANDATORY
    validate_token(notion, report)
    validate_database_id(notion, report)
    validate_project_id(notion, report)

    return report.print_report()


def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="Validation config Notion pour Promptor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vérifie que .claude/settings.local.json contient:
  - notion.token (MANDATORY)
  - notion.tasks_database_id (MANDATORY)
  - notion.default_project_id (MANDATORY - critique pour rangement)

Examples:
  python validate_notion_config.py
  python validate_notion_config.py --settings-path /path/to/settings.json
        """
    )
    parser.add_argument(
        '--settings-path',
        type=Path,
        help='Chemin vers settings.local.json (défaut: .claude/settings.local.json)'
    )

    args = parser.parse_args()
    sys.exit(validate_notion_config(args.settings_path))


if __name__ == "__main__":
    main()
