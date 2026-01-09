#!/usr/bin/env python3
"""
EPCI Component Usage Validator v1.0

Validates that all agents and skills declared in plugin.json are actually
used in commands. Generates a comprehensive usage report.

Usage:
    python validate_usage.py                 # Validate and report
    python validate_usage.py --strict        # Fail if any component unused
    python validate_usage.py --json          # Output as JSON
    python validate_usage.py --fix-readme    # Also fix README references
"""

import json
import re
import sys
from pathlib import Path
from typing import TypedDict
from dataclasses import dataclass, field


@dataclass
class UsageInfo:
    """Information about a component's usage."""
    name: str
    declared_path: str
    used_in_commands: list[str] = field(default_factory=list)
    used_in_skills: list[str] = field(default_factory=list)
    used_in_hooks: list[str] = field(default_factory=list)
    used_in_tests: list[str] = field(default_factory=list)
    is_auto_detected: bool = False

    @property
    def is_used(self) -> bool:
        """Component is considered used if referenced in commands or is auto-detected."""
        return bool(self.used_in_commands) or self.is_auto_detected

    @property
    def usage_score(self) -> int:
        """Score based on how widely the component is used."""
        score = 0
        score += len(self.used_in_commands) * 10
        score += len(self.used_in_skills) * 5
        score += len(self.used_in_hooks) * 3
        score += len(self.used_in_tests) * 2
        return score


class UsageValidator:
    """Validates component usage across the EPCI plugin."""

    # Stack skills that are auto-detected based on project files
    AUTO_DETECTED_SKILLS = {
        'php-symfony',
        'javascript-react',
        'python-django',
        'java-springboot',
        'frontend-editor'
    }

    def __init__(self, plugin_root: Path):
        self.plugin_root = plugin_root
        self.src_dir = plugin_root / 'src'
        self.plugin_json_path = self.src_dir / '.claude-plugin' / 'plugin.json'

        # Load plugin.json
        with open(self.plugin_json_path) as f:
            self.plugin_config = json.load(f)

        self.agents: dict[str, UsageInfo] = {}
        self.skills: dict[str, UsageInfo] = {}

    def _extract_name(self, path: str) -> str:
        """Extract component name from path."""
        # ./agents/plan-validator.md -> plan-validator
        # ./skills/core/epci-core/SKILL.md -> epci-core
        parts = path.split('/')
        if 'agents' in parts:
            return parts[-1].replace('.md', '')
        elif 'skills' in parts:
            # Get the directory name before SKILL.md
            return parts[-2]
        return path

    def _search_in_file(self, file_path: Path, pattern: str) -> bool:
        """Check if pattern exists in file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            return bool(re.search(pattern, content, re.IGNORECASE))
        except Exception:
            return False

    def _get_file_references(self, component_name: str, file_type: str) -> list[str]:
        """Find all files of a type that reference the component."""
        references = []

        # Build search pattern - handle both @name and name formats
        patterns = [
            rf'@{re.escape(component_name)}[^\w-]',
            rf'["\'/]{re.escape(component_name)}["\'/\.]',
            rf'`{re.escape(component_name)}`',
            rf'\b{re.escape(component_name)}\b'
        ]

        # Define search paths based on file type
        search_paths = {
            'commands': self.src_dir / 'commands',
            'skills': self.src_dir / 'skills',
            'hooks': self.src_dir / 'hooks',
            'tests': self.src_dir / 'scripts'
        }

        search_path = search_paths.get(file_type)
        if not search_path or not search_path.exists():
            return references

        # Search through files
        glob_pattern = '**/*.md' if file_type in ('commands', 'skills') else '**/*.py'
        for file_path in search_path.glob(glob_pattern):
            # For commands: include all files (commands SHOULD declare their skills)
            # For skills: skip the skill's own SKILL.md file
            if file_type == 'skills' and component_name in str(file_path) and 'SKILL.md' in str(file_path):
                continue

            for pattern in patterns:
                if self._search_in_file(file_path, pattern):
                    # Get relative path for cleaner output
                    rel_path = file_path.relative_to(self.src_dir)
                    references.append(str(rel_path))
                    break

        return references

    def analyze_agents(self) -> None:
        """Analyze usage of all declared agents."""
        for agent_path in self.plugin_config.get('agents', []):
            name = self._extract_name(agent_path)

            usage = UsageInfo(
                name=name,
                declared_path=agent_path,
                used_in_commands=self._get_file_references(name, 'commands'),
                used_in_skills=self._get_file_references(name, 'skills'),
                used_in_hooks=self._get_file_references(name, 'hooks'),
                used_in_tests=self._get_file_references(name, 'tests')
            )

            self.agents[name] = usage

    def analyze_skills(self) -> None:
        """Analyze usage of all declared skills."""
        for skill_path in self.plugin_config.get('skills', []):
            name = self._extract_name(skill_path)

            usage = UsageInfo(
                name=name,
                declared_path=skill_path,
                used_in_commands=self._get_file_references(name, 'commands'),
                used_in_skills=self._get_file_references(name, 'skills'),
                used_in_hooks=self._get_file_references(name, 'hooks'),
                used_in_tests=self._get_file_references(name, 'tests'),
                is_auto_detected=name in self.AUTO_DETECTED_SKILLS
            )

            self.skills[name] = usage

    def validate(self) -> tuple[bool, dict]:
        """Run full validation and return (success, report)."""
        self.analyze_agents()
        self.analyze_skills()

        # Build report
        report = {
            'version': self.plugin_config.get('version', 'unknown'),
            'agents': {
                'total': len(self.agents),
                'used': sum(1 for a in self.agents.values() if a.is_used),
                'unused': [],
                'details': {}
            },
            'skills': {
                'total': len(self.skills),
                'used': sum(1 for s in self.skills.values() if s.is_used),
                'unused': [],
                'auto_detected': list(self.AUTO_DETECTED_SKILLS),
                'details': {}
            }
        }

        # Populate agent details
        for name, usage in sorted(self.agents.items(), key=lambda x: -x[1].usage_score):
            report['agents']['details'][name] = {
                'commands': usage.used_in_commands,
                'skills': usage.used_in_skills,
                'hooks': usage.used_in_hooks,
                'tests': usage.used_in_tests,
                'score': usage.usage_score,
                'status': 'used' if usage.is_used else 'UNUSED'
            }
            if not usage.is_used:
                report['agents']['unused'].append(name)

        # Populate skill details
        for name, usage in sorted(self.skills.items(), key=lambda x: -x[1].usage_score):
            status = 'auto-detected' if usage.is_auto_detected else ('used' if usage.is_used else 'UNUSED')
            report['skills']['details'][name] = {
                'commands': usage.used_in_commands,
                'skills': usage.used_in_skills,
                'hooks': usage.used_in_hooks,
                'tests': usage.used_in_tests,
                'score': usage.usage_score,
                'status': status
            }
            if not usage.is_used and not usage.is_auto_detected:
                report['skills']['unused'].append(name)

        # Validation passes if no unused components
        success = not report['agents']['unused'] and not report['skills']['unused']

        return success, report

    def print_report(self, report: dict, json_output: bool = False) -> None:
        """Print validation report."""
        if json_output:
            print(json.dumps(report, indent=2))
            return

        print(f"\n{'='*60}")
        print(f"EPCI Component Usage Report v{report['version']}")
        print(f"{'='*60}\n")

        # Agents summary
        agents = report['agents']
        print(f"AGENTS: {agents['used']}/{agents['total']} used")
        print("-" * 40)

        for name, info in agents['details'].items():
            status_icon = "✅" if info['status'] == 'used' else "❌"
            commands = ', '.join(info['commands'][:3]) if info['commands'] else '-'
            if len(info['commands']) > 3:
                commands += f" (+{len(info['commands'])-3})"
            print(f"  {status_icon} @{name}")
            print(f"     Commands: {commands}")
            print(f"     Score: {info['score']}")

        if agents['unused']:
            print(f"\n⚠️  UNUSED AGENTS: {', '.join(agents['unused'])}")

        print()

        # Skills summary
        skills = report['skills']
        print(f"SKILLS: {skills['used']}/{skills['total']} used")
        print("-" * 40)

        for name, info in skills['details'].items():
            if info['status'] == 'auto-detected':
                status_icon = "🔄"
            elif info['status'] == 'used':
                status_icon = "✅"
            else:
                status_icon = "❌"

            commands = ', '.join(info['commands'][:3]) if info['commands'] else '-'
            if len(info['commands']) > 3:
                commands += f" (+{len(info['commands'])-3})"
            print(f"  {status_icon} {name}")
            print(f"     Commands: {commands}")
            print(f"     Score: {info['score']}")

        if skills['unused']:
            print(f"\n⚠️  UNUSED SKILLS: {', '.join(skills['unused'])}")

        print()
        print(f"{'='*60}")

        # Final verdict
        all_used = not agents['unused'] and not skills['unused']
        if all_used:
            print("✅ VALIDATION PASSED: All components are properly used")
        else:
            print("❌ VALIDATION FAILED: Some components are not used")
            print("\nRecommendations:")
            if agents['unused']:
                print(f"  - Remove or use agents: {', '.join(agents['unused'])}")
            if skills['unused']:
                print(f"  - Remove or use skills: {', '.join(skills['unused'])}")

        print(f"{'='*60}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate EPCI component usage')
    parser.add_argument('--strict', action='store_true',
                       help='Exit with error if any component unused')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    parser.add_argument('--root', type=Path, default=Path(__file__).parent.parent.parent,
                       help='Plugin root directory')

    args = parser.parse_args()

    validator = UsageValidator(args.root)
    success, report = validator.validate()

    validator.print_report(report, json_output=args.json)

    if args.strict and not success:
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
