#!/usr/bin/env python3
"""
Test de triggering des Skills Claude Code.
Usage: python test_triggering.py <path-to-skill-folder>
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class TriggeringReport:
    """Rapport de tests de triggering."""
    skill_name: str
    positive_triggers: list = field(default_factory=list)
    negative_triggers: list = field(default_factory=list)
    passed: int = 0
    failed: int = 0

    def add_pass(self):
        self.passed += 1

    def add_fail(self):
        self.failed += 1

    @property
    def total(self):
        return self.passed + self.failed

    def print_report(self):
        print(f"\n{'='*60}")
        print(f"TRIGGERING TESTS: {self.skill_name}")
        print(f"{'='*60}\n")

        if self.positive_triggers:
            print("POSITIVE TRIGGERS (should match):")
            for trigger, matched in self.positive_triggers:
                status = "✅ TRIGGERED" if matched else "❌ NOT TRIGGERED"
                print(f'   "{trigger}" → {status}')
            print()

        if self.negative_triggers:
            print("NEGATIVE TRIGGERS (should NOT match):")
            for trigger, not_matched in self.negative_triggers:
                status = "✅ NOT TRIGGERED" if not_matched else "❌ TRIGGERED (unexpected)"
                print(f'   "{trigger}" → {status}')
            print()

        status = "PASSED" if self.failed == 0 else "FAILED"
        print(f"RESULT: {status} ({self.passed}/{self.total} tests)")
        print(f"{'='*60}\n")

        return 0 if self.failed == 0 else 1


def load_skill_description(skill_path: Path) -> Optional[str]:
    """Charge la description d'un skill."""
    skill_file = skill_path / "SKILL.md"

    if not skill_file.exists():
        return None

    content = skill_file.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)

    if not match:
        return None

    frontmatter = yaml.safe_load(match.group(1))
    return frontmatter.get('description', '')


def extract_triggers(description: str) -> Tuple[List[str], List[str]]:
    """Extrait les triggers positifs et négatifs de la description."""
    positive = []
    negative = []

    # Extraire "Use when:" patterns
    use_when_match = re.search(r'Use when[:\s]+([^.]+)', description, re.IGNORECASE)
    if use_when_match:
        triggers = use_when_match.group(1).split(',')
        positive = [t.strip() for t in triggers if t.strip()]

    # Extraire "Auto-invoke when:" patterns (alternative)
    auto_invoke_match = re.search(r'Auto-invoke when[:\s]+([^.]+)', description, re.IGNORECASE)
    if auto_invoke_match and not positive:
        triggers = auto_invoke_match.group(1).split(',')
        positive = [t.strip() for t in triggers if t.strip()]

    # Extraire "Not for:" patterns
    not_for_match = re.search(r'Not for[:\s]+([^.]+)', description, re.IGNORECASE)
    if not_for_match:
        exclusions = not_for_match.group(1).split(',')
        negative = [e.strip() for e in exclusions if e.strip()]

    # Extraire "Do NOT load for:" patterns (alternative)
    do_not_match = re.search(r'Do NOT load for[:\s]+([^.]+)', description, re.IGNORECASE)
    if do_not_match and not negative:
        exclusions = do_not_match.group(1).split(',')
        negative = [e.strip() for e in exclusions if e.strip()]

    return positive, negative


def should_trigger(query: str, description: str) -> bool:
    """Détermine si une requête devrait déclencher le skill."""
    query_lower = query.lower()
    desc_lower = description.lower()

    # Extraire mots-clés significatifs de la description (4+ lettres)
    keywords = set(re.findall(r'\b[a-z]{4,}\b', desc_lower))

    # Filtrer les mots communs non-significatifs
    stop_words = {
        'when', 'with', 'that', 'this', 'from', 'have', 'been',
        'will', 'your', 'they', 'more', 'some', 'about', 'which',
        'their', 'would', 'make', 'like', 'just', 'into', 'over',
        'such', 'only', 'also', 'after', 'most', 'than', 'them',
        'should', 'could', 'other', 'load', 'invoke', 'auto'
    }
    keywords = keywords - stop_words

    # Vérifier combien de mots-clés apparaissent dans la requête
    matches = sum(1 for kw in keywords if kw in query_lower)

    # Seuil: au moins 2 mots-clés correspondants
    return matches >= 2


def generate_test_queries(positive_triggers: List[str], negative_triggers: List[str]) -> Tuple[List[str], List[str]]:
    """Génère des requêtes de test à partir des triggers."""
    # Requêtes positives basées sur les triggers
    positive_queries = []
    for trigger in positive_triggers[:3]:  # Max 3
        # Transformer le trigger en requête simulée
        query = f"Help me with {trigger}"
        positive_queries.append(query)

    # Requêtes négatives basées sur les exclusions
    negative_queries = []
    for exclusion in negative_triggers[:2]:  # Max 2
        query = f"I need to work on {exclusion}"
        negative_queries.append(query)

    return positive_queries, negative_queries


def test_skill_triggering(skill_path_str: str) -> int:
    """Teste le triggering d'un skill."""
    skill_path = Path(skill_path_str).resolve()

    # Si c'est un fichier, prendre le dossier parent
    if skill_path.is_file():
        skill_path = skill_path.parent

    if not skill_path.exists():
        print(f"[ERROR] Path not found: {skill_path}")
        return 1

    description = load_skill_description(skill_path)

    if not description:
        print(f"[ERROR] Could not load skill description from: {skill_path}")
        return 1

    report = TriggeringReport(skill_name=skill_path.name)

    positive_triggers, negative_triggers = extract_triggers(description)

    if not positive_triggers and not negative_triggers:
        print(f"[WARNING] No triggers found in description")
        print(f"Description: {description[:200]}...")
        print("\nTip: Description should contain 'Use when:' and 'Not for:' patterns")
        return 0

    # Générer et exécuter les tests
    positive_queries, negative_queries = generate_test_queries(positive_triggers, negative_triggers)

    # Tests positifs (doivent trigger)
    for i, query in enumerate(positive_queries):
        trigger_text = positive_triggers[i] if i < len(positive_triggers) else query
        result = should_trigger(query, description)
        report.positive_triggers.append((trigger_text, result))
        if result:
            report.add_pass()
        else:
            report.add_fail()

    # Tests négatifs (ne doivent pas trigger)
    for i, query in enumerate(negative_queries):
        exclusion_text = negative_triggers[i] if i < len(negative_triggers) else query
        result = not should_trigger(query, description)
        report.negative_triggers.append((exclusion_text, result))
        if result:
            report.add_pass()
        else:
            report.add_fail()

    return report.print_report()


def test_all_skills(base_path: str = "src/skills") -> int:
    """Teste le triggering de tous les skills."""
    base = Path(base_path).resolve()

    if not base.exists():
        print(f"[ERROR] Base path not found: {base}")
        return 1

    # Trouver tous les SKILL.md
    skill_files = list(base.glob("**/SKILL.md"))

    if not skill_files:
        print(f"[WARNING] No SKILL.md files found in: {base}")
        return 0

    print(f"\n{'='*60}")
    print(f"BATCH TRIGGERING TESTS")
    print(f"Found {len(skill_files)} skills")
    print(f"{'='*60}\n")

    failed = 0
    passed = 0

    for skill_file in skill_files:
        skill_path = skill_file.parent
        result = test_skill_triggering(str(skill_path))
        if result == 0:
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"BATCH RESULT: {passed}/{passed + failed} skills passed")
    print(f"{'='*60}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Sans argument, tester tous les skills
        sys.exit(test_all_skills())
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-h', '--help']:
            print("Usage: python test_triggering.py [path-to-skill-folder]")
            print("       python test_triggering.py              # Test all skills")
            print("       python test_triggering.py src/skills/core/epci-core/")
            sys.exit(0)
        sys.exit(test_skill_triggering(sys.argv[1]))
    else:
        print("Usage: python test_triggering.py [path-to-skill-folder]")
        sys.exit(1)
