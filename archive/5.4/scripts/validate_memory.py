#!/usr/bin/env python3
"""
Validation script for EPCI Project Memory module.
Validates schemas, templates, and module structure.

Usage: python validate_memory.py [path-to-project-memory]
"""

import sys
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationReport:
    """Validation report for project-memory module."""
    module_name: str = "project-memory"
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks_passed: int = 0
    checks_total: int = 10

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def pass_check(self):
        self.checks_passed += 1

    def print_report(self) -> int:
        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {self.module_name}")
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

        status = "✅ PASSED" if self.valid else "❌ FAILED"
        print(f"RESULT: {status} ({self.checks_passed}/{self.checks_total} checks)")
        print(f"{'='*60}\n")

        return 0 if self.valid else 1


def validate_directory_structure(module_path: Path, report: ValidationReport) -> bool:
    """Validate the module directory structure."""
    required_dirs = ['schemas', 'templates']
    required_files = ['__init__.py', 'manager.py', 'detector.py']

    all_exist = True

    for dirname in required_dirs:
        if not (module_path / dirname).is_dir():
            report.add_error(f"Missing directory: {dirname}/")
            all_exist = False

    for filename in required_files:
        if not (module_path / filename).is_file():
            report.add_error(f"Missing file: {filename}")
            all_exist = False

    if all_exist:
        print("[OK] Directory structure: Valid")
        report.pass_check()

    return all_exist


def validate_schemas(module_path: Path, report: ValidationReport) -> bool:
    """Validate JSON schema files."""
    schemas_dir = module_path / 'schemas'
    required_schemas = [
        'context.schema.json',
        'conventions.schema.json',
        'feature-history.schema.json',
        'velocity.schema.json',
        'version.schema.json',
    ]

    all_valid = True

    for schema_file in required_schemas:
        schema_path = schemas_dir / schema_file
        if not schema_path.exists():
            report.add_error(f"Missing schema: {schema_file}")
            all_valid = False
            continue

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)

            # Validate basic schema structure
            if '$schema' not in schema:
                report.add_warning(f"{schema_file}: Missing $schema declaration")

            if 'type' not in schema:
                report.add_warning(f"{schema_file}: Missing 'type' field")

        except json.JSONDecodeError as e:
            report.add_error(f"{schema_file}: Invalid JSON - {e}")
            all_valid = False

    if all_valid:
        print(f"[OK] Schemas: {len(required_schemas)} valid")
        report.pass_check()

    return all_valid


def validate_templates(module_path: Path, report: ValidationReport) -> bool:
    """Validate template files."""
    templates_dir = module_path / 'templates'
    required_templates = [
        'context.json',
        'conventions.json',
        'settings.json',
        'velocity.json',
    ]

    all_valid = True

    for template_file in required_templates:
        template_path = templates_dir / template_file
        if not template_path.exists():
            report.add_error(f"Missing template: {template_file}")
            all_valid = False
            continue

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)

            # Check for version field
            if 'version' not in template:
                report.add_warning(f"{template_file}: Missing 'version' field")

        except json.JSONDecodeError as e:
            report.add_error(f"{template_file}: Invalid JSON - {e}")
            all_valid = False

    if all_valid:
        print(f"[OK] Templates: {len(required_templates)} valid")
        report.pass_check()

    return all_valid


def validate_manager_module(module_path: Path, report: ValidationReport) -> bool:
    """Validate manager.py module."""
    manager_path = module_path / 'manager.py'

    if not manager_path.exists():
        report.add_error("manager.py not found")
        return False

    content = manager_path.read_text(encoding='utf-8')

    required_classes = [
        'ProjectContext',
        'Conventions',
        'FeatureHistory',
        'VelocityMetrics',
        'Settings',
        'ProjectMemoryManager',
    ]

    required_methods = [
        'init_memory',
        'load_context',
        'save_context',
        'load_feature_history',
        'save_feature_history',
        'export_all',
        'reset',
    ]

    all_found = True

    for cls_name in required_classes:
        if f'class {cls_name}' not in content:
            report.add_error(f"manager.py: Missing class '{cls_name}'")
            all_found = False

    for method_name in required_methods:
        if f'def {method_name}' not in content:
            report.add_error(f"manager.py: Missing method '{method_name}'")
            all_found = False

    # Check for atomic write
    if '_atomic_write' not in content:
        report.add_warning("manager.py: Missing _atomic_write for data safety")

    if all_found:
        print("[OK] manager.py: All classes and methods present")
        report.pass_check()

    return all_found


def validate_detector_module(module_path: Path, report: ValidationReport) -> bool:
    """Validate detector.py module."""
    detector_path = module_path / 'detector.py'

    if not detector_path.exists():
        report.add_error("detector.py not found")
        return False

    content = detector_path.read_text(encoding='utf-8')

    required_items = [
        'STACK_SIGNATURES',
        'CONVENTION_PATTERNS',
        'ARCHITECTURE_PATTERNS',
        'class ProjectDetector',
        'def detect_stack',
        'def detect_conventions',
        'def detect_patterns',
    ]

    all_found = True

    for item in required_items:
        if item not in content:
            report.add_error(f"detector.py: Missing '{item}'")
            all_found = False

    if all_found:
        print("[OK] detector.py: All detection components present")
        report.pass_check()

    return all_found


def validate_init_module(module_path: Path, report: ValidationReport) -> bool:
    """Validate __init__.py exports."""
    init_path = module_path / '__init__.py'

    if not init_path.exists():
        report.add_error("__init__.py not found")
        return False

    content = init_path.read_text(encoding='utf-8')

    required_exports = [
        'ProjectMemoryManager',
        'ProjectContext',
        'Conventions',
        'FeatureHistory',
    ]

    all_found = True

    for export in required_exports:
        if export not in content:
            report.add_error(f"__init__.py: Missing export '{export}'")
            all_found = False

    if all_found:
        print("[OK] __init__.py: All exports present")
        report.pass_check()

    return all_found


def validate_command(commands_path: Path, report: ValidationReport) -> bool:
    """Validate memory.md command."""
    command_path = commands_path / 'memory.md'

    if not command_path.exists():
        report.add_error("memory.md command not found")
        return False

    content = command_path.read_text(encoding='utf-8')

    # Check YAML frontmatter
    if not content.startswith('---'):
        report.add_error("memory.md: Missing YAML frontmatter")
        return False

    required_subcommands = ['status', 'init', 'reset', 'export']

    all_found = True
    for subcmd in required_subcommands:
        if f'`{subcmd}`' not in content and f'/{subcmd}' not in content.lower():
            report.add_warning(f"memory.md: Subcommand '{subcmd}' not documented")

    if all_found:
        print("[OK] memory.md: Command structure valid")
        report.pass_check()

    return True


def validate_skill(skills_path: Path, report: ValidationReport) -> bool:
    """Validate project-memory SKILL.md."""
    skill_path = skills_path / 'core' / 'project-memory' / 'SKILL.md'

    if not skill_path.exists():
        report.add_error("project-memory/SKILL.md not found")
        return False

    content = skill_path.read_text(encoding='utf-8')

    # Check YAML frontmatter
    if not content.startswith('---'):
        report.add_error("SKILL.md: Missing YAML frontmatter")
        return False

    # Check for required sections
    if 'name:' not in content:
        report.add_error("SKILL.md: Missing 'name' in frontmatter")
        return False

    if 'description:' not in content:
        report.add_error("SKILL.md: Missing 'description' in frontmatter")
        return False

    print("[OK] project-memory/SKILL.md: Valid")
    report.pass_check()
    return True


def validate_plugin_json(plugin_path: Path, report: ValidationReport) -> bool:
    """Validate plugin.json includes new components."""
    if not plugin_path.exists():
        report.add_error("plugin.json not found")
        return False

    try:
        with open(plugin_path, 'r', encoding='utf-8') as f:
            plugin = json.load(f)
    except json.JSONDecodeError as e:
        report.add_error(f"plugin.json: Invalid JSON - {e}")
        return False

    # Check for command
    commands = plugin.get('commands', [])
    if not any('memory' in cmd for cmd in commands):
        report.add_error("plugin.json: Missing memory.md in commands")
        return False

    # Check for skill
    core_skills = plugin.get('skills', {}).get('core', [])
    if not any('project-memory' in skill for skill in core_skills):
        report.add_error("plugin.json: Missing project-memory skill")
        return False

    print("[OK] plugin.json: Updated with new components")
    report.pass_check()
    return True


def validate_hooks_extension(hooks_path: Path, report: ValidationReport) -> bool:
    """Validate HookContext extension in runner.py."""
    runner_path = hooks_path / 'runner.py'

    if not runner_path.exists():
        report.add_error("hooks/runner.py not found")
        return False

    content = runner_path.read_text(encoding='utf-8')

    required_fields = [
        'project_memory',
        'detected_stack',
        'detected_conventions',
    ]

    all_found = True

    for field_name in required_fields:
        if field_name not in content:
            report.add_error(f"runner.py: HookContext missing '{field_name}' field")
            all_found = False

    if all_found:
        print("[OK] hooks/runner.py: HookContext extended for project memory")
        report.pass_check()

    return all_found


def validate_project_memory(src_path: Optional[Path] = None) -> int:
    """Main validation entry point."""
    if src_path is None:
        # Try to find src/ from script location
        script_dir = Path(__file__).resolve().parent
        if script_dir.name == 'scripts':
            src_path = script_dir.parent
        else:
            src_path = Path.cwd() / 'src'

    module_path = src_path / 'project-memory'
    commands_path = src_path / 'commands'
    skills_path = src_path / 'skills'
    hooks_path = src_path / 'hooks'
    plugin_path = src_path / '.claude-plugin' / 'plugin.json'

    report = ValidationReport()

    print(f"\nValidating project-memory module at: {module_path}\n")

    # Run all validations
    validate_directory_structure(module_path, report)
    validate_schemas(module_path, report)
    validate_templates(module_path, report)
    validate_manager_module(module_path, report)
    validate_detector_module(module_path, report)
    validate_init_module(module_path, report)
    validate_command(commands_path, report)
    validate_skill(skills_path, report)
    validate_plugin_json(plugin_path, report)
    validate_hooks_extension(hooks_path, report)

    return report.print_report()


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    sys.exit(validate_project_memory(path))
