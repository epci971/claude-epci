#!/usr/bin/env python3
"""
Command Inventory Validator

Extracts all flags, agents, skills, hooks, and tools from command files
and compares against a baseline to detect regressions.

Usage:
    python3 validate_command_inventory.py [--baseline] [--compare <baseline.json>]
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def extract_flags(content: str) -> Set[str]:
    """Extract all flags (--flag-name) from content."""
    pattern = r'`--([a-z][a-z0-9-]*)`'
    flags = set(re.findall(pattern, content))
    # Also catch flags in tables without backticks
    pattern2 = r'\|\s*`?--([a-z][a-z0-9-]*)`?\s*\|'
    flags.update(re.findall(pattern2, content))
    return {f'--{f}' for f in flags}


def extract_agents(content: str) -> Set[str]:
    """Extract all agent references (@agent-name) from content."""
    pattern = r'@([A-Za-z][a-z0-9-]*)'
    agents = set(re.findall(pattern, content))
    # Filter out obvious non-agents (decorators, example paths, etc.)
    exclude = {
        'example', 'user', 'path', 'file', 'slug', 'date',
        'dataclass', 'validator', 'property', 'staticmethod', 'classmethod',
        'simple-feature', 'simple', 'name', 'output', 'Plan'  # Plan is @planner
    }
    return {f'@{a}' for a in agents if a.lower() not in exclude and not a[0].isupper() or a in ['Explore']}


def extract_skills(content: str) -> Set[str]:
    """Extract all skill references from content."""
    # Match skill patterns like: skill: X, Skills: X, Skill: `X`
    pattern = r'(?:skill|skills?)[:,]\s*`?([a-z][a-z0-9-]*)`?'
    skills = set(re.findall(pattern, content, re.IGNORECASE))
    # Also match in skill lists with commas
    pattern2 = r'Skills:\s*([^\n]+)'
    match = re.search(pattern2, content)
    if match:
        skill_line = match.group(1)
        # Extract skills from comma-separated or space-separated list
        found = re.findall(r'([a-z][a-z0-9-]+)', skill_line)
        skills.update(found)
    # Filter out non-skills (generic words)
    exclude = {'skill', 'skills', 'name', 'type', 'commands', 'stack'}
    return {s for s in skills if s not in exclude}


def extract_hooks(content: str) -> Set[str]:
    """Extract all hook types from content."""
    pattern = r'(?:pre|post|on)-[a-z0-9-]+'
    hooks = set(re.findall(pattern, content))
    # Filter out example-specific hooks (from decompose examples, etc.)
    exclude = {
        'on-django', 'on-etl', 'on-gardel', 'on-prd', 'on-urgentes',
        'on-intelligente', 'on-by-'  # From example content
    }
    return {h for h in hooks if h not in exclude}


def extract_tools(content: str) -> Set[str]:
    """Extract allowed-tools from frontmatter."""
    pattern = r'allowed-tools:\s*\[(.*?)\]'
    match = re.search(pattern, content)
    if match:
        tools_str = match.group(1)
        tools = re.findall(r'[A-Za-z]+', tools_str)
        return set(tools)
    return set()


def extract_mcp_servers(content: str) -> Set[str]:
    """Extract MCP server references."""
    servers = set()
    mcp_patterns = [
        r'Context7', r'context7',
        r'Sequential', r'sequential',
        r'Magic', r'magic',
        r'Playwright', r'playwright',
    ]
    for pattern in mcp_patterns:
        if re.search(pattern, content):
            servers.add(pattern.lower())
    return servers


def analyze_command(file_path: Path) -> Dict:
    """Analyze a single command file."""
    content = file_path.read_text()
    return {
        'name': file_path.stem,
        'flags': sorted(extract_flags(content)),
        'agents': sorted(extract_agents(content)),
        'skills': sorted(extract_skills(content)),
        'hooks': sorted(extract_hooks(content)),
        'tools': sorted(extract_tools(content)),
        'mcp_servers': sorted(extract_mcp_servers(content)),
    }


def generate_inventory(commands_dir: Path) -> Dict:
    """Generate full inventory from all command files."""
    inventory = {
        'commands': {},
        'all_flags': set(),
        'all_agents': set(),
        'all_skills': set(),
        'all_hooks': set(),
        'all_tools': set(),
        'all_mcp_servers': set(),
    }

    # Scan main command files
    for cmd_file in sorted(commands_dir.glob('*.md')):
        analysis = analyze_command(cmd_file)
        inventory['commands'][analysis['name']] = analysis
        inventory['all_flags'].update(analysis['flags'])
        inventory['all_agents'].update(analysis['agents'])
        inventory['all_skills'].update(analysis['skills'])
        inventory['all_hooks'].update(analysis['hooks'])
        inventory['all_tools'].update(analysis['tools'])
        inventory['all_mcp_servers'].update(analysis['mcp_servers'])

    # Also scan references/ directory for shared content
    refs_dir = commands_dir / 'references'
    if refs_dir.exists():
        for ref_file in sorted(refs_dir.glob('*.md')):
            content = ref_file.read_text()
            inventory['all_flags'].update(extract_flags(content))
            inventory['all_agents'].update(extract_agents(content))
            inventory['all_hooks'].update(extract_hooks(content))

    # Convert sets to sorted lists for JSON
    for key in ['all_flags', 'all_agents', 'all_skills', 'all_hooks', 'all_tools', 'all_mcp_servers']:
        inventory[key] = sorted(inventory[key])

    return inventory


def compare_inventories(baseline: Dict, current: Dict) -> Dict:
    """Compare two inventories and report differences."""
    report = {
        'status': 'PASS',
        'missing': {},
        'added': {},
        'summary': {}
    }

    categories = ['all_flags', 'all_agents', 'all_skills', 'all_hooks', 'all_tools', 'all_mcp_servers']

    for cat in categories:
        baseline_set = set(baseline.get(cat, []))
        current_set = set(current.get(cat, []))

        missing = baseline_set - current_set
        added = current_set - baseline_set

        if missing:
            report['missing'][cat] = sorted(missing)
            report['status'] = 'FAIL'
        if added:
            report['added'][cat] = sorted(added)

        report['summary'][cat] = {
            'baseline': len(baseline_set),
            'current': len(current_set),
            'missing': len(missing),
            'added': len(added)
        }

    return report


def print_report(report: Dict) -> None:
    """Print comparison report."""
    print("\n" + "=" * 60)
    print("COMMAND INVENTORY COMPARISON REPORT")
    print("=" * 60)

    for cat, summary in report['summary'].items():
        cat_name = cat.replace('all_', '').upper()
        status = "✅" if summary['missing'] == 0 else "❌"
        print(f"\n{status} {cat_name}")
        print(f"   Baseline: {summary['baseline']} | Current: {summary['current']}")
        if summary['missing'] > 0:
            print(f"   ⚠️  MISSING: {summary['missing']}")
            for item in report['missing'].get(cat, []):
                print(f"      - {item}")
        if summary['added'] > 0:
            print(f"   ➕ Added: {summary['added']}")
            for item in report['added'].get(cat, []):
                print(f"      + {item}")

    print("\n" + "=" * 60)
    if report['status'] == 'PASS':
        print("✅ VALIDATION PASSED - No functional regression detected")
    else:
        print("❌ VALIDATION FAILED - Missing elements detected!")
    print("=" * 60)


def main():
    commands_dir = Path(__file__).parent.parent / 'commands'

    if not commands_dir.exists():
        print(f"Error: Commands directory not found: {commands_dir}")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == '--baseline':
        # Generate baseline
        inventory = generate_inventory(commands_dir)
        output = Path(__file__).parent.parent.parent / 'docs/audits/command-inventory-baseline.json'
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(inventory, indent=2))
        print(f"✅ Baseline saved to: {output}")
        print(f"\nSummary:")
        print(f"  Commands: {len(inventory['commands'])}")
        print(f"  Flags: {len(inventory['all_flags'])}")
        print(f"  Agents: {len(inventory['all_agents'])}")
        print(f"  Skills: {len(inventory['all_skills'])}")
        print(f"  Hooks: {len(inventory['all_hooks'])}")
        print(f"  Tools: {len(inventory['all_tools'])}")
        print(f"  MCP Servers: {len(inventory['all_mcp_servers'])}")

    elif len(sys.argv) > 2 and sys.argv[1] == '--compare':
        # Compare with baseline
        baseline_path = Path(sys.argv[2])
        if not baseline_path.exists():
            print(f"Error: Baseline file not found: {baseline_path}")
            sys.exit(1)

        baseline = json.loads(baseline_path.read_text())
        current = generate_inventory(commands_dir)
        report = compare_inventories(baseline, current)
        print_report(report)

        sys.exit(0 if report['status'] == 'PASS' else 1)

    else:
        # Just display current inventory
        inventory = generate_inventory(commands_dir)
        print(json.dumps(inventory, indent=2))


if __name__ == '__main__':
    main()
