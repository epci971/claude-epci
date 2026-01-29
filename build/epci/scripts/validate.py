#!/usr/bin/env python3
"""
EPCI v6 Comprehensive Validation Script

Validates:
- Plugin structure (plugin.json)
- Skills (SKILL.md) - 12 checks from Factory checklist
- Steps (step-*.md) - 3 checks (breakpoints, invocations, task documentation)
- Agents (*.md) - Basic structure

Usage:
    python validate.py [--verbose] [--json]

Exit codes:
    0: All validations passed (may have warnings)
    1: Validation errors found
"""

import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


# ============ SEVERITY LEVELS ============

class Severity(str, Enum):
    """Validation severity levels."""
    ERROR = "ERROR"      # Blocks validation
    WARNING = "WARNING"  # Warning, doesn't fail
    INFO = "INFO"        # Recommendation


# ============ VALIDATION RESULT ============

@dataclass
class ValidationResult:
    """Result of a single validation check."""
    file: Path
    check: str
    severity: Severity
    message: str
    passed: bool
    line: Optional[int] = None


@dataclass
class ValidationSummary:
    """Summary of all validation results."""
    results: list[ValidationResult] = field(default_factory=list)
    skills_count: int = 0
    steps_count: int = 0
    agents_count: int = 0

    @property
    def errors(self) -> list[ValidationResult]:
        return [r for r in self.results if r.severity == Severity.ERROR and not r.passed]

    @property
    def warnings(self) -> list[ValidationResult]:
        return [r for r in self.results if r.severity == Severity.WARNING and not r.passed]

    @property
    def infos(self) -> list[ValidationResult]:
        return [r for r in self.results if r.severity == Severity.INFO and not r.passed]

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


# ============ VAGUE WORDS FOR DESCRIPTION CHECK ============

# Words that are vague when used alone without context
# Note: "manages", "handles" are OK when describing the skill's main action
VAGUE_WORDS = [
    "various", "different", "multiple", "several", "many", "some",
    "stuff", "things", "etc", "and more", "and so on",
    "deals with",  # Too generic
]

# ============ HELPER FUNCTIONS ============

def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from markdown file.

    Returns dict with frontmatter fields, or empty dict if no frontmatter.
    """
    if not file_path.exists():
        return {}

    content = file_path.read_text()
    if not content.startswith("---"):
        return {}

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}

    frontmatter = {}
    current_key = None
    current_value_lines = []

    for line in lines[1:end_idx]:
        # Handle multi-line values (YAML folded style >-)
        if line.startswith("  ") and current_key:
            current_value_lines.append(line.strip())
            continue

        # Save previous multi-line value
        if current_key and current_value_lines:
            frontmatter[current_key] = " ".join(current_value_lines)
            current_value_lines = []
            current_key = None

        # Parse key: value
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            # Handle multi-line start (>- or > or |)
            if value in (">-", ">", "|"):
                current_key = key
                current_value_lines = []
            # Handle boolean
            elif value.lower() == "true":
                frontmatter[key] = True
            elif value.lower() == "false":
                frontmatter[key] = False
            # Handle list (simplified)
            elif value.startswith("[") and value.endswith("]"):
                # Parse simple list like [Read, Write, Edit]
                items = value[1:-1].split(",")
                frontmatter[key] = [item.strip() for item in items if item.strip()]
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                frontmatter[key] = value[1:-1]
            else:
                frontmatter[key] = value

    # Don't forget last multi-line value
    if current_key and current_value_lines:
        frontmatter[current_key] = " ".join(current_value_lines)

    return frontmatter


def get_content_without_frontmatter(file_path: Path) -> str:
    """Get file content without YAML frontmatter."""
    content = file_path.read_text()
    if not content.startswith("---"):
        return content

    lines = content.split("\n")
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[i + 1:])

    return content


def is_in_code_block(content: str, position: int) -> bool:
    """Check if a position in content is inside a code block."""
    # Count ``` before the position
    before = content[:position]
    code_fence_count = before.count("```")
    return code_fence_count % 2 == 1  # Odd means inside code block


def is_kebab_case(name: str) -> bool:
    """Check if name is in kebab-case (lowercase letters, numbers, hyphens)."""
    return bool(re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$|^[a-z]$', name))


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    return len(file_path.read_text().split("\n"))


# ============ FILE DISCOVERY ============

# Skill directories to exclude from validation (internal/stack skills)
EXCLUDED_SKILL_DIRS = {"core", "stack"}


def find_all_files(src_dir: Path) -> dict:
    """Find all files to validate.

    Only validates business skills (excludes core/ and stack/ directories).
    """
    files = {
        'plugin': src_dir / ".claude-plugin" / "plugin.json",
        'skills': [],
        'steps': [],
        'agents': [],
        'references': [],
    }

    skills_dir = src_dir / "skills"
    if skills_dir.exists():
        # Find SKILL.md files, excluding core/ and stack/ directories
        for skill_md in skills_dir.rglob("SKILL.md"):
            relative = skill_md.relative_to(skills_dir)
            top_dir = relative.parts[0] if relative.parts else ""
            if top_dir not in EXCLUDED_SKILL_DIRS:
                files['skills'].append(skill_md)

        # Steps: only for validated skills
        for skill_path in files['skills']:
            skill_dir = skill_path.parent
            steps_dir = skill_dir / "steps"
            if steps_dir.exists():
                files['steps'].extend(steps_dir.glob("step-*.md"))

        # References: only for validated skills
        for skill_path in files['skills']:
            skill_dir = skill_path.parent
            refs_dir = skill_dir / "references"
            if refs_dir.exists():
                files['references'].extend(refs_dir.glob("*.md"))

    agents_dir = src_dir / "agents"
    if agents_dir.exists():
        files['agents'] = list(agents_dir.glob("*.md"))

    return files


# ============ PLUGIN VALIDATORS ============

def validate_plugin_json(plugin_path: Path) -> list[ValidationResult]:
    """Validate plugin.json structure."""
    results = []

    if not plugin_path.exists():
        results.append(ValidationResult(
            file=plugin_path,
            check="plugin_exists",
            severity=Severity.ERROR,
            message="plugin.json not found",
            passed=False
        ))
        return results

    try:
        with open(plugin_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results.append(ValidationResult(
            file=plugin_path,
            check="plugin_json_valid",
            severity=Severity.ERROR,
            message=f"Invalid JSON: {e}",
            passed=False
        ))
        return results

    # Check required fields
    required_fields = ["name", "version", "description", "skills"]
    for field_name in required_fields:
        if field_name not in data:
            results.append(ValidationResult(
                file=plugin_path,
                check="plugin_required_fields",
                severity=Severity.ERROR,
                message=f"Missing required field: {field_name}",
                passed=False
            ))
        else:
            results.append(ValidationResult(
                file=plugin_path,
                check=f"plugin_field_{field_name}",
                severity=Severity.ERROR,
                message=f"Field '{field_name}' present",
                passed=True
            ))

    # Validate skill paths exist
    if "skills" in data:
        for skill_path in data["skills"]:
            full_path = plugin_path.parent.parent / skill_path
            if not full_path.exists():
                results.append(ValidationResult(
                    file=plugin_path,
                    check="plugin_skill_paths",
                    severity=Severity.ERROR,
                    message=f"Skill file not found: {skill_path}",
                    passed=False
                ))

    return results


# ============ SKILL VALIDATORS (12 checks) ============

def validate_skill_name_uniqueness(skill_path: Path, all_skills: list[Path]) -> ValidationResult:
    """Check that skill names are unique across the project."""
    frontmatter = parse_frontmatter(skill_path)
    name = frontmatter.get("name", "")

    if not name:
        return ValidationResult(
            file=skill_path,
            check="skill_name_uniqueness",
            severity=Severity.ERROR,
            message="Missing 'name' in frontmatter",
            passed=False
        )

    # Count how many skills have this name
    duplicates = []
    for other_skill in all_skills:
        if other_skill == skill_path:
            continue
        other_fm = parse_frontmatter(other_skill)
        if other_fm.get("name") == name:
            duplicates.append(other_skill)

    if duplicates:
        return ValidationResult(
            file=skill_path,
            check="skill_name_uniqueness",
            severity=Severity.ERROR,
            message=f"Duplicate name '{name}' found in: {[str(d) for d in duplicates]}",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_name_uniqueness",
        severity=Severity.ERROR,
        message="Name is unique",
        passed=True
    )


def validate_skill_name_format(skill_path: Path) -> ValidationResult:
    """Check name is kebab-case and <= 64 chars."""
    frontmatter = parse_frontmatter(skill_path)
    name = frontmatter.get("name", "")

    if not name:
        return ValidationResult(
            file=skill_path,
            check="skill_name_format",
            severity=Severity.ERROR,
            message="Missing 'name' in frontmatter",
            passed=False
        )

    # Remove epci: prefix for format check
    clean_name = name.replace("epci:", "")

    issues = []
    if len(clean_name) > 64:
        issues.append(f"name too long ({len(clean_name)} > 64 chars)")

    if not is_kebab_case(clean_name):
        issues.append("name must be kebab-case (lowercase, hyphens)")

    if issues:
        return ValidationResult(
            file=skill_path,
            check="skill_name_format",
            severity=Severity.ERROR,
            message="; ".join(issues),
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_name_format",
        severity=Severity.ERROR,
        message="Name format valid",
        passed=True
    )


def validate_skill_description_specificity(skill_path: Path) -> ValidationResult:
    """Check description doesn't contain vague words."""
    frontmatter = parse_frontmatter(skill_path)
    description = frontmatter.get("description", "")

    if not description:
        return ValidationResult(
            file=skill_path,
            check="skill_description_specificity",
            severity=Severity.ERROR,
            message="Missing 'description' in frontmatter",
            passed=False
        )

    found_vague = []
    desc_lower = description.lower()
    for word in VAGUE_WORDS:
        if word in desc_lower:
            found_vague.append(word)

    if found_vague:
        return ValidationResult(
            file=skill_path,
            check="skill_description_specificity",
            severity=Severity.ERROR,
            message=f"Description contains vague words: {found_vague}",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_description_specificity",
        severity=Severity.ERROR,
        message="Description is specific",
        passed=True
    )


def validate_skill_description_length(skill_path: Path) -> ValidationResult:
    """Check description is < 1024 chars."""
    frontmatter = parse_frontmatter(skill_path)
    description = frontmatter.get("description", "")

    if not description:
        return ValidationResult(
            file=skill_path,
            check="skill_description_length",
            severity=Severity.ERROR,
            message="Missing 'description' in frontmatter",
            passed=False
        )

    if len(description) > 1024:
        return ValidationResult(
            file=skill_path,
            check="skill_description_length",
            severity=Severity.ERROR,
            message=f"Description too long ({len(description)} > 1024 chars)",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_description_length",
        severity=Severity.ERROR,
        message="Description length OK",
        passed=True
    )


def validate_skill_trigger_words(skill_path: Path) -> ValidationResult:
    """Check description has at least 3 trigger words (Use when, Triggers, Not for)."""
    frontmatter = parse_frontmatter(skill_path)
    description = frontmatter.get("description", "")

    if not description:
        return ValidationResult(
            file=skill_path,
            check="skill_trigger_words",
            severity=Severity.WARNING,
            message="Missing 'description' in frontmatter",
            passed=False
        )

    # Look for trigger indicators
    triggers_found = 0
    trigger_patterns = [
        r"Use when:",
        r"Triggers?:",
        r"Not for:",
        r"Do NOT use",
        r"when:.*\b(build|implement|create|fix|debug|refactor)\b",
    ]

    for pattern in trigger_patterns:
        if re.search(pattern, description, re.IGNORECASE):
            triggers_found += 1

    if triggers_found < 2:
        return ValidationResult(
            file=skill_path,
            check="skill_trigger_words",
            severity=Severity.WARNING,
            message=f"Description should have trigger indicators (Use when, Triggers, Not for). Found: {triggers_found}",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_trigger_words",
        severity=Severity.WARNING,
        message="Trigger words present",
        passed=True
    )


def validate_skill_line_count(skill_path: Path) -> ValidationResult:
    """Check SKILL.md is < 500 lines."""
    line_count = count_lines(skill_path)

    if line_count > 500:
        return ValidationResult(
            file=skill_path,
            check="skill_line_count",
            severity=Severity.ERROR,
            message=f"SKILL.md too long ({line_count} > 500 lines)",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_line_count",
        severity=Severity.ERROR,
        message=f"Line count OK ({line_count} lines)",
        passed=True
    )


def validate_skill_references_exist(skill_path: Path) -> ValidationResult:
    """Check that referenced files (@path) actually exist."""
    content = skill_path.read_text()

    # Find @path references (not in code blocks)
    references = []
    for match in re.finditer(r'@(\.\.?/[^\s\)]+)', content):
        ref_path = match.group(1)
        # Check if in code block
        if not is_in_code_block(content, match.start()):
            references.append(ref_path)

    missing = []
    skill_dir = skill_path.parent
    for ref in references:
        full_path = (skill_dir / ref).resolve()
        if not full_path.exists():
            missing.append(ref)

    if missing:
        return ValidationResult(
            file=skill_path,
            check="skill_references_exist",
            severity=Severity.ERROR,
            message=f"Referenced files not found: {missing}",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_references_exist",
        severity=Severity.ERROR,
        message=f"All {len(references)} references exist" if references else "No references to check",
        passed=True
    )


def validate_skill_allowed_tools(skill_path: Path) -> ValidationResult:
    """Check allowed-tools is present and appropriate."""
    frontmatter = parse_frontmatter(skill_path)
    allowed_tools = frontmatter.get("allowed-tools", [])

    # Convert string to list if needed
    if isinstance(allowed_tools, str):
        allowed_tools = [t.strip() for t in allowed_tools.split(",")]

    if not allowed_tools:
        return ValidationResult(
            file=skill_path,
            check="skill_allowed_tools",
            severity=Severity.WARNING,
            message="Missing 'allowed-tools' in frontmatter",
            passed=False
        )

    # Check for common tools that should usually be present
    common_tools = {"Read", "Write", "Edit", "Glob", "Grep", "Bash"}
    has_common = bool(set(allowed_tools) & common_tools)

    if not has_common:
        return ValidationResult(
            file=skill_path,
            check="skill_allowed_tools",
            severity=Severity.WARNING,
            message="allowed-tools missing common tools (Read, Write, etc.)",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_allowed_tools",
        severity=Severity.WARNING,
        message="allowed-tools defined",
        passed=True
    )


def validate_skill_workflow_numbered(skill_path: Path) -> ValidationResult:
    """Check workflow steps are numbered."""
    content = get_content_without_frontmatter(skill_path)

    # Look for numbered lists or workflow sections
    has_workflow = bool(re.search(r'##\s*(Workflow|Steps|EXECUTION)', content, re.IGNORECASE))

    if not has_workflow:
        return ValidationResult(
            file=skill_path,
            check="skill_workflow_numbered",
            severity=Severity.WARNING,
            message="No Workflow/Steps section found",
            passed=False
        )

    # Check for numbered steps
    has_numbered = bool(re.search(r'^\s*\d+\.\s+', content, re.MULTILINE))
    has_step_files = bool(re.search(r'step-\d+', content, re.IGNORECASE))

    if not has_numbered and not has_step_files:
        return ValidationResult(
            file=skill_path,
            check="skill_workflow_numbered",
            severity=Severity.WARNING,
            message="Workflow steps should be numbered or reference step files",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_workflow_numbered",
        severity=Severity.WARNING,
        message="Workflow properly structured",
        passed=True
    )


def validate_skill_examples_present(skill_path: Path) -> ValidationResult:
    """Check examples are included (RECOMMEND)."""
    content = get_content_without_frontmatter(skill_path)

    has_examples = bool(re.search(r'##\s*(Examples?|Quick Start|Usage)', content, re.IGNORECASE))
    has_code_blocks = bool(re.search(r'```', content))

    if not has_examples and not has_code_blocks:
        return ValidationResult(
            file=skill_path,
            check="skill_examples_present",
            severity=Severity.INFO,
            message="Consider adding examples section",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_examples_present",
        severity=Severity.INFO,
        message="Examples present",
        passed=True
    )


def validate_skill_error_handling(skill_path: Path) -> ValidationResult:
    """Check error handling is defined (RECOMMEND)."""
    content = get_content_without_frontmatter(skill_path)

    has_error_section = bool(re.search(r'##\s*(Error|Errors|Error Handling|Failure)', content, re.IGNORECASE))
    has_error_mentions = bool(re.search(r'\b(error|fail|exception|invalid)\b', content, re.IGNORECASE))

    if not has_error_section and not has_error_mentions:
        return ValidationResult(
            file=skill_path,
            check="skill_error_handling",
            severity=Severity.INFO,
            message="Consider documenting error handling",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_error_handling",
        severity=Severity.INFO,
        message="Error handling documented",
        passed=True
    )


def validate_skill_limitations(skill_path: Path) -> ValidationResult:
    """Check limitations are documented (RECOMMEND)."""
    content = get_content_without_frontmatter(skill_path)

    has_limitations = bool(re.search(r'##\s*(Limitations?|Constraints?|Not for|OUT scope)', content, re.IGNORECASE))
    has_not_for = bool(re.search(r'Not for:', content, re.IGNORECASE))

    if not has_limitations and not has_not_for:
        return ValidationResult(
            file=skill_path,
            check="skill_limitations",
            severity=Severity.INFO,
            message="Consider documenting limitations",
            passed=False
        )

    return ValidationResult(
        file=skill_path,
        check="skill_limitations",
        severity=Severity.INFO,
        message="Limitations documented",
        passed=True
    )


def validate_skill_complete(skill_path: Path, all_skills: list[Path]) -> list[ValidationResult]:
    """Run all 12 skill validations."""
    return [
        validate_skill_name_uniqueness(skill_path, all_skills),
        validate_skill_name_format(skill_path),
        validate_skill_description_specificity(skill_path),
        validate_skill_description_length(skill_path),
        validate_skill_trigger_words(skill_path),
        validate_skill_line_count(skill_path),
        validate_skill_references_exist(skill_path),
        validate_skill_allowed_tools(skill_path),
        validate_skill_workflow_numbered(skill_path),
        validate_skill_examples_present(skill_path),
        validate_skill_error_handling(skill_path),
        validate_skill_limitations(skill_path),
    ]


# ============ STEP VALIDATORS (3 checks) ============

def validate_step_task_documentation(step_path: Path) -> list[ValidationResult]:
    """Check Task tool invocations are properly documented."""
    results = []
    content = step_path.read_text()

    # Find Task invocations
    task_patterns = [
        r'Task\s*\(',
        r'LANCE\s+Task\s*\(',
        r'subagent_type:',
    ]

    has_task = any(re.search(p, content) for p in task_patterns)

    if has_task:
        # Check if there's documentation about the task
        has_doc = bool(re.search(r'(###.*invoke|###.*agent|@\w+-\w+)', content, re.IGNORECASE))

        if not has_doc:
            results.append(ValidationResult(
                file=step_path,
                check="step_task_documentation",
                severity=Severity.WARNING,
                message="Task invocation should be documented with section header",
                passed=False
            ))
        else:
            results.append(ValidationResult(
                file=step_path,
                check="step_task_documentation",
                severity=Severity.WARNING,
                message="Task invocations documented",
                passed=True
            ))

    return results


def validate_step_breakpoint_syntax(step_path: Path) -> list[ValidationResult]:
    """
    Validate breakpoints in step files.

    Rules:
    - R1: Header format: ## BREAKPOINT: or ### X. BREAKPOINT:
    - R2: ASCII box present (horizontal lines with corner chars)
    - R3: Box NOT inside code block (``` or 4-space indent)
    - R4: AskUserQuestion present after box
    - R5: ATTENDS marker present
    """
    results = []
    content = step_path.read_text()

    # Find all breakpoint sections
    breakpoint_matches = list(re.finditer(
        r'^(#{2,3})\s+(?:\d+\.\s+)?BREAKPOINT:\s*(.+)$',
        content,
        re.MULTILINE
    ))

    if not breakpoint_matches:
        # No breakpoints in this step, that's OK
        return results

    for match in breakpoint_matches:
        bp_header = match.group(2).strip()
        bp_start = match.end()

        # Find next section header to delimit breakpoint section
        next_section = re.search(r'^#{2,3}\s+[A-Z]', content[bp_start:], re.MULTILINE)
        bp_end = bp_start + next_section.start() if next_section else len(content)
        section = content[bp_start:bp_end]

        # R2: Check ASCII box present (look for box drawing characters)
        has_box_chars = any(c in section for c in ['─', '│', '┌', '┐', '└', '┘', '├', '┤'])
        has_simple_box = '┌─' in section or '+--' in section

        if not has_box_chars and not has_simple_box:
            results.append(ValidationResult(
                file=step_path,
                check="breakpoint_ascii_box",
                severity=Severity.ERROR,
                message=f"Breakpoint '{bp_header}' missing ASCII box",
                passed=False,
                line=content[:match.start()].count('\n') + 1
            ))

        # R3: Check box NOT in code block
        # Find box start position
        box_pos = section.find('┌─')
        if box_pos == -1:
            box_pos = section.find('+--')

        if box_pos != -1:
            # Check if the section before the box has unmatched ```
            section_before_box = section[:box_pos]
            if section_before_box.count('```') % 2 == 1:
                results.append(ValidationResult(
                    file=step_path,
                    check="breakpoint_not_in_codeblock",
                    severity=Severity.ERROR,
                    message=f"Breakpoint '{bp_header}' ASCII box inside code block (won't render)",
                    passed=False,
                    line=content[:match.start()].count('\n') + 1
                ))

        # R4: Check AskUserQuestion present
        has_ask = bool(re.search(
            r'(AskUserQuestion\s*\(|APPELLE\s+AskUserQuestion)',
            section
        ))

        if not has_ask:
            results.append(ValidationResult(
                file=step_path,
                check="breakpoint_askuserquestion",
                severity=Severity.WARNING,
                message=f"Breakpoint '{bp_header}' missing AskUserQuestion call",
                passed=False,
                line=content[:match.start()].count('\n') + 1
            ))

        # R5: Check ATTENDS marker (French: wait)
        has_attends = bool(re.search(
            r'(ATTENDS\s+la\s+r[eé]ponse|ATTENDS|WAIT\s+for)',
            section,
            re.IGNORECASE
        ))

        if not has_attends:
            results.append(ValidationResult(
                file=step_path,
                check="breakpoint_attends_marker",
                severity=Severity.WARNING,
                message=f"Breakpoint '{bp_header}' missing 'ATTENDS la reponse' marker",
                passed=False,
                line=content[:match.start()].count('\n') + 1
            ))

    # If we found breakpoints and no errors were added, add a pass result
    if breakpoint_matches and not any(r.check.startswith("breakpoint_") and not r.passed for r in results):
        results.append(ValidationResult(
            file=step_path,
            check="breakpoint_syntax",
            severity=Severity.ERROR,
            message=f"All {len(breakpoint_matches)} breakpoint(s) valid",
            passed=True
        ))

    return results


def validate_step_no_code_block_invocations(step_path: Path) -> list[ValidationResult]:
    """
    Check that @skill: and @agent: are not in code blocks (won't execute).

    Anti-patterns:
    - @skill:epci:breakpoint-system in code block
    - @agent:ems-evaluator in code block
    """
    results = []
    content = step_path.read_text()

    # Patterns to check
    patterns = [
        (r'@skill:epci:\w+[\w-]*', 'skill invocation'),
        (r'@agent:\w+[\w-]*', 'agent invocation'),
    ]

    for pattern, desc in patterns:
        for match in re.finditer(pattern, content):
            if is_in_code_block(content, match.start()):
                line_num = content[:match.start()].count('\n') + 1
                results.append(ValidationResult(
                    file=step_path,
                    check="no_code_block_invocations",
                    severity=Severity.WARNING,
                    message=f"{desc} '{match.group()}' in code block won't execute (line {line_num})",
                    passed=False,
                    line=line_num
                ))

    return results


def validate_step_complete(step_path: Path) -> list[ValidationResult]:
    """Run all step validations."""
    results = []
    results.extend(validate_step_task_documentation(step_path))
    results.extend(validate_step_breakpoint_syntax(step_path))
    results.extend(validate_step_no_code_block_invocations(step_path))
    return results


# ============ AGENT VALIDATORS ============

def validate_agent(agent_path: Path) -> list[ValidationResult]:
    """Validate agent file structure."""
    results = []

    if not agent_path.exists():
        results.append(ValidationResult(
            file=agent_path,
            check="agent_exists",
            severity=Severity.ERROR,
            message="Agent file not found",
            passed=False
        ))
        return results

    frontmatter = parse_frontmatter(agent_path)

    # Check required fields
    required = ["name", "description"]
    for field_name in required:
        if field_name not in frontmatter:
            results.append(ValidationResult(
                file=agent_path,
                check="agent_required_fields",
                severity=Severity.ERROR,
                message=f"Missing required field: {field_name}",
                passed=False
            ))

    # Check model is specified
    if "model" not in frontmatter:
        results.append(ValidationResult(
            file=agent_path,
            check="agent_model",
            severity=Severity.WARNING,
            message="Missing 'model' field (opus, sonnet, or haiku recommended)",
            passed=False
        ))

    # Check allowed-tools
    if "allowed-tools" not in frontmatter:
        results.append(ValidationResult(
            file=agent_path,
            check="agent_allowed_tools",
            severity=Severity.WARNING,
            message="Missing 'allowed-tools' field",
            passed=False
        ))

    # Check line count (agents should be < 200 lines)
    line_count = count_lines(agent_path)
    if line_count > 200:
        results.append(ValidationResult(
            file=agent_path,
            check="agent_line_count",
            severity=Severity.WARNING,
            message=f"Agent file long ({line_count} > 200 lines recommended)",
            passed=False
        ))

    # If no errors, mark as valid
    if not any(not r.passed and r.severity == Severity.ERROR for r in results):
        results.append(ValidationResult(
            file=agent_path,
            check="agent_valid",
            severity=Severity.ERROR,
            message="Agent structure valid",
            passed=True
        ))

    return results


# ============ MAIN VALIDATION ============

def validate_all(src_dir: Path) -> ValidationSummary:
    """Run all validations on all files."""
    files = find_all_files(src_dir)
    summary = ValidationSummary()

    # 1. Plugin
    summary.results.extend(validate_plugin_json(files['plugin']))

    # 2. Skills (12 checks each)
    summary.skills_count = len(files['skills'])
    for skill in sorted(files['skills']):
        summary.results.extend(validate_skill_complete(skill, files['skills']))

    # 3. Steps (3 checks each)
    summary.steps_count = len(files['steps'])
    for step in sorted(files['steps']):
        summary.results.extend(validate_step_complete(step))

    # 4. Agents
    summary.agents_count = len(files['agents'])
    for agent in sorted(files['agents']):
        summary.results.extend(validate_agent(agent))

    return summary


def print_results(summary: ValidationSummary, verbose: bool = True) -> None:
    """Print validation results in human-readable format."""
    print("\nEPCI v6 Comprehensive Validation")
    print("=" * 60)

    # Group results by file
    files_with_errors = {}
    files_with_warnings = {}
    files_with_infos = {}

    for result in summary.results:
        if not result.passed:
            if result.severity == Severity.ERROR:
                files_with_errors.setdefault(result.file, []).append(result)
            elif result.severity == Severity.WARNING:
                files_with_warnings.setdefault(result.file, []).append(result)
            else:
                files_with_infos.setdefault(result.file, []).append(result)

    # Print errors
    if files_with_errors:
        print(f"\n{'='*60}")
        print("ERRORS (must fix)")
        print("=" * 60)
        for file_path, results in sorted(files_with_errors.items()):
            print(f"\n  {file_path.name}")
            for r in results:
                line_info = f":{r.line}" if r.line else ""
                print(f"    ERROR: {r.message} [{r.check}]{line_info}")

    # Print warnings
    if files_with_warnings and verbose:
        print(f"\n{'='*60}")
        print("WARNINGS (should fix)")
        print("=" * 60)
        for file_path, results in sorted(files_with_warnings.items()):
            print(f"\n  {file_path.name}")
            for r in results:
                line_info = f":{r.line}" if r.line else ""
                print(f"    WARN: {r.message} [{r.check}]{line_info}")

    # Print infos (recommendations)
    if files_with_infos and verbose:
        print(f"\n{'='*60}")
        print("RECOMMENDATIONS")
        print("=" * 60)
        for file_path, results in sorted(files_with_infos.items()):
            print(f"\n  {file_path.name}")
            for r in results:
                print(f"    INFO: {r.message}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("=" * 60)
    print(f"  Skills:  {summary.skills_count} validated")
    print(f"  Steps:   {summary.steps_count} validated")
    print(f"  Agents:  {summary.agents_count} validated")
    print(f"  Errors:  {len(summary.errors)}")
    print(f"  Warnings: {len(summary.warnings)}")
    print(f"  Recommendations: {len(summary.infos)}")
    print()

    if summary.passed:
        status = "PASS"
        if summary.warnings:
            status += f" (with {len(summary.warnings)} warnings)"
        print(f"RESULT: {status}")
    else:
        print(f"RESULT: FAIL ({len(summary.errors)} errors)")


def output_json(summary: ValidationSummary) -> None:
    """Output results as JSON."""
    output = {
        "passed": summary.passed,
        "counts": {
            "skills": summary.skills_count,
            "steps": summary.steps_count,
            "agents": summary.agents_count,
            "errors": len(summary.errors),
            "warnings": len(summary.warnings),
            "infos": len(summary.infos),
        },
        "errors": [
            {
                "file": str(r.file),
                "check": r.check,
                "message": r.message,
                "line": r.line,
            }
            for r in summary.errors
        ],
        "warnings": [
            {
                "file": str(r.file),
                "check": r.check,
                "message": r.message,
                "line": r.line,
            }
            for r in summary.warnings
        ],
    }
    print(json.dumps(output, indent=2))


def main() -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="EPCI v6 Comprehensive Validation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=True,
        help="Show warnings and recommendations (default: True)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show errors"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--src",
        type=Path,
        default=None,
        help="Source directory to validate (default: src/ relative to script)"
    )

    args = parser.parse_args()

    # Determine source directory
    script_dir = Path(__file__).parent
    src_dir = args.src or script_dir.parent

    # Run validation
    summary = validate_all(src_dir)

    # Output results
    if args.json:
        output_json(summary)
    else:
        verbose = not args.quiet
        print_results(summary, verbose=verbose)

    return 0 if summary.passed else 1


if __name__ == "__main__":
    sys.exit(main())
