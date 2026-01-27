#!/usr/bin/env python3
"""
Validate EPCI skill output against best practices.

Part of factory skill - runs during Phase 5 (preview) and Phase 6 (post-generation).
Implements the 12-point checklist from references/checklist-validation.md.

Usage:
    python validate_skill_output.py <skill_path>
    python validate_skill_output.py <skill_path> --permissive

Exit codes:
    0 = All checks pass
    1 = Required check failed (or recommended in strict mode)
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_number: int
    name: str
    passed: bool
    message: str
    is_warning: bool = False


@dataclass
class ValidationReport:
    """Complete validation report for a skill."""
    skill_name: str
    skill_path: Path
    results: list[ValidationResult] = field(default_factory=list)

    def add(self, result: ValidationResult) -> None:
        self.results.append(result)

    @property
    def required_passed(self) -> bool:
        return all(r.passed for r in self.results if r.check_number <= 9)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def warning_count(self) -> int:
        return sum(1 for r in self.results if r.is_warning and not r.passed)


class SkillValidator:
    """Validates EPCI skills against best practices."""

    # Vague terms that indicate poor description
    VAGUE_TERMS = ["helper", "utility", "tool", "misc", "various", "general", "stuff"]

    # Limits from best-practices-synthesis.md
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_CHARS = 1024
    MIN_DESCRIPTION_WORDS = 10  # Relaxed from 50 for practical use
    MAX_SKILL_LINES = 500
    MIN_WORKFLOW_STEPS = 3

    # Name pattern: lowercase, hyphens allowed, starts with letter
    NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")

    def __init__(self, skill_path: Path, skills_root: Optional[Path] = None):
        """
        Initialize validator.

        Args:
            skill_path: Path to skill directory (containing SKILL.md)
            skills_root: Root directory for uniqueness check (default: auto-detect)
        """
        self.skill_path = Path(skill_path).resolve()
        self.skill_md = self.skill_path / "SKILL.md"
        self.skills_root = skills_root or self._find_skills_root()
        self.report: Optional[ValidationReport] = None

        # Cached content
        self._content: Optional[str] = None
        self._frontmatter: dict = {}
        self._body: str = ""

    def _find_skills_root(self) -> Path:
        """Find the skills/ directory by walking up from skill_path."""
        current = self.skill_path
        while current.parent != current:
            if current.name == "skills":
                return current
            # Check if parent contains skills/
            if (current.parent / "skills").is_dir():
                return current.parent / "skills"
            current = current.parent
        return self.skill_path.parent

    def _load_skill(self) -> bool:
        """Load and parse SKILL.md. Returns False if file doesn't exist."""
        if not self.skill_md.exists():
            return False

        self._content = self.skill_md.read_text(encoding="utf-8")

        # Parse frontmatter
        if self._content.startswith("---"):
            parts = self._content.split("---", 2)
            if len(parts) >= 3:
                self._parse_frontmatter(parts[1])
                self._body = parts[2]
            else:
                self._body = self._content
        else:
            self._body = self._content

        return True

    def _parse_frontmatter(self, frontmatter_text: str) -> None:
        """Parse YAML frontmatter into dict."""
        self._frontmatter = {}
        current_key = None
        current_value_lines = []

        for line in frontmatter_text.strip().split("\n"):
            # Check for new key
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                # Save previous key if any
                if current_key and current_value_lines:
                    self._frontmatter[current_key] = " ".join(current_value_lines).strip()

                key, _, value = line.partition(":")
                current_key = key.strip()
                value = value.strip()

                # Handle multiline indicator
                if value in (">-", "|", ">"):
                    current_value_lines = []
                else:
                    self._frontmatter[current_key] = value
                    current_key = None
                    current_value_lines = []
            elif current_key:
                # Continuation of multiline value
                current_value_lines.append(line.strip())

        # Save last key
        if current_key and current_value_lines:
            self._frontmatter[current_key] = " ".join(current_value_lines).strip()

    def validate_all(self, permissive: bool = False) -> ValidationReport:
        """
        Run all validations.

        Args:
            permissive: If True, recommended checks become warnings (non-blocking)

        Returns:
            ValidationReport with all results
        """
        skill_name = self._frontmatter.get("name", self.skill_path.name)
        self.report = ValidationReport(skill_name=skill_name, skill_path=self.skill_path)

        # Load skill first
        if not self._load_skill():
            self.report.add(ValidationResult(
                check_number=0,
                name="File exists",
                passed=False,
                message=f"SKILL.md not found at {self.skill_md}"
            ))
            return self.report

        # Required checks (1-9)
        self._validate_name_format()
        self._validate_name_unique()
        self._validate_description_specificity()
        self._validate_description_length()
        self._validate_trigger_words()
        self._validate_line_count()
        self._validate_references()
        self._validate_allowed_tools()
        self._validate_workflow_steps()

        # Recommended checks (10-13) - warnings if permissive
        self._check_examples(is_warning=permissive)
        self._check_error_handling(is_warning=permissive)
        self._check_limitations(is_warning=permissive)
        self._check_task_tool_documentation(is_warning=permissive)

        return self.report

    def _validate_name_format(self) -> None:
        """Check 1-2: Name format (kebab-case, lowercase, ≤64 chars)."""
        name = self._frontmatter.get("name", "")

        if not name:
            self.report.add(ValidationResult(
                check_number=1,
                name="Name exists",
                passed=False,
                message="Missing 'name' field in frontmatter"
            ))
            return

        # Check format
        if not self.NAME_PATTERN.match(name):
            self.report.add(ValidationResult(
                check_number=2,
                name="Name format",
                passed=False,
                message=f"Name '{name}' must be lowercase with hyphens only (kebab-case)"
            ))
        elif len(name) > self.MAX_NAME_LENGTH:
            self.report.add(ValidationResult(
                check_number=2,
                name="Name length",
                passed=False,
                message=f"Name '{name}' exceeds {self.MAX_NAME_LENGTH} chars ({len(name)} chars)"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=2,
                name="Name format",
                passed=True,
                message=f"Name valid: {name} ({len(name)} chars)"
            ))

    def _validate_name_unique(self) -> None:
        """Check 1: Name is unique across skills/."""
        name = self._frontmatter.get("name", "")
        if not name:
            return  # Already reported in format check

        duplicates = []

        # Search for other skills with same name
        if self.skills_root.exists():
            for skill_dir in self.skills_root.rglob("SKILL.md"):
                if skill_dir.resolve() == self.skill_md.resolve():
                    continue  # Skip self

                try:
                    content = skill_dir.read_text(encoding="utf-8")
                    if f"name: {name}" in content or f"name: {name}\n" in content:
                        duplicates.append(skill_dir.parent.relative_to(self.skills_root))
                except (OSError, UnicodeDecodeError):
                    pass

        if duplicates:
            self.report.add(ValidationResult(
                check_number=1,
                name="Name unique",
                passed=False,
                message=f"Name '{name}' already exists in: {', '.join(str(d) for d in duplicates)}"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=1,
                name="Name unique",
                passed=True,
                message=f"Name '{name}' is unique"
            ))

    def _validate_description_specificity(self) -> None:
        """Check 3: Description is specific (no vague terms)."""
        description = self._frontmatter.get("description", "").lower()

        if not description:
            self.report.add(ValidationResult(
                check_number=3,
                name="Description exists",
                passed=False,
                message="Missing 'description' field in frontmatter"
            ))
            return

        found_vague = [term for term in self.VAGUE_TERMS if term in description.split()]

        if found_vague:
            self.report.add(ValidationResult(
                check_number=3,
                name="Description specific",
                passed=False,
                message=f"Description contains vague terms: {', '.join(found_vague)}"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=3,
                name="Description specific",
                passed=True,
                message="Description is specific (no vague terms)"
            ))

    def _validate_description_length(self) -> None:
        """Check 4: Description length < 1024 chars."""
        description = self._frontmatter.get("description", "")

        if not description:
            return  # Already reported

        char_count = len(description)
        word_count = len(description.split())

        if char_count >= self.MAX_DESCRIPTION_CHARS:
            self.report.add(ValidationResult(
                check_number=4,
                name="Description length",
                passed=False,
                message=f"Description exceeds {self.MAX_DESCRIPTION_CHARS} chars ({char_count} chars)"
            ))
        elif word_count < self.MIN_DESCRIPTION_WORDS:
            self.report.add(ValidationResult(
                check_number=4,
                name="Description length",
                passed=False,
                message=f"Description too short ({word_count} words, min {self.MIN_DESCRIPTION_WORDS})"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=4,
                name="Description length",
                passed=True,
                message=f"Description length OK ({word_count} words, {char_count} chars)"
            ))

    def _validate_trigger_words(self) -> None:
        """Check 5: Description has trigger words."""
        description = self._frontmatter.get("description", "").lower()

        if not description:
            return  # Already reported

        # Look for trigger patterns
        trigger_patterns = [
            r"use when[:\s]",
            r"trigger[s]?[:\s]",
            r"invoke when",
            r"for[:\s]",
            r"when[:\s]",
        ]

        found_triggers = sum(1 for p in trigger_patterns if re.search(p, description))

        # Also count action verbs at start
        action_verbs = ["create", "generate", "analyze", "validate", "transform",
                        "extract", "build", "debug", "improve", "refactor", "manage"]
        starts_with_action = any(description.startswith(v) for v in action_verbs)

        if found_triggers >= 1 or starts_with_action:
            self.report.add(ValidationResult(
                check_number=5,
                name="Trigger words",
                passed=True,
                message="Description has trigger words/patterns"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=5,
                name="Trigger words",
                passed=False,
                message="Description lacks trigger words (add 'Use when:', 'Triggers:', etc.)"
            ))

    def _validate_line_count(self) -> None:
        """Check 6: SKILL.md < 500 lines."""
        line_count = len(self._content.split("\n"))

        if line_count >= self.MAX_SKILL_LINES:
            self.report.add(ValidationResult(
                check_number=6,
                name="Line count",
                passed=False,
                message=f"SKILL.md exceeds {self.MAX_SKILL_LINES} lines ({line_count} lines)"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=6,
                name="Line count",
                passed=True,
                message=f"SKILL.md lines OK ({line_count} < {self.MAX_SKILL_LINES})"
            ))

    def _validate_references(self) -> None:
        """Check 7: All referenced files exist."""
        # Find markdown links in body
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        missing = []

        for match in link_pattern.finditer(self._body):
            link_text, link_path = match.groups()

            # Skip URLs and anchors
            if link_path.startswith(("http://", "https://", "#", "mailto:")):
                continue

            # Resolve relative path from SKILL.md location
            full_path = (self.skill_path / link_path).resolve()

            if not full_path.exists():
                missing.append(link_path)

        if missing:
            self.report.add(ValidationResult(
                check_number=7,
                name="References exist",
                passed=False,
                message=f"Missing referenced files: {', '.join(missing)}"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=7,
                name="References exist",
                passed=True,
                message="All referenced files exist"
            ))

    def _validate_allowed_tools(self) -> None:
        """Check 8: allowed-tools is appropriate."""
        allowed_tools = self._frontmatter.get("allowed-tools", "")

        if not allowed_tools:
            # allowed-tools is optional, default is inherit
            self.report.add(ValidationResult(
                check_number=8,
                name="Allowed tools",
                passed=True,
                message="allowed-tools not specified (inherits default)"
            ))
            return

        # Check for common issues
        valid_tools = ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "AskUserQuestion",
                       "Task", "WebFetch", "WebSearch", "TodoWrite"]

        tools_list = [t.strip() for t in allowed_tools.replace(",", " ").split()]
        # Handle Bash restrictions like Bash(git:*)
        tools_list = [t.split("(")[0] for t in tools_list]

        unknown = [t for t in tools_list if t not in valid_tools and t]

        if unknown:
            self.report.add(ValidationResult(
                check_number=8,
                name="Allowed tools",
                passed=False,
                message=f"Unknown tools in allowed-tools: {', '.join(unknown)}"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=8,
                name="Allowed tools",
                passed=True,
                message=f"allowed-tools valid: {allowed_tools}"
            ))

    def _validate_workflow_steps(self) -> None:
        """Check 9: Workflow steps are numbered (≥3)."""
        # Look for numbered steps pattern: "1. ", "2. ", etc.
        step_pattern = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)
        steps = step_pattern.findall(self._body)

        if len(steps) >= self.MIN_WORKFLOW_STEPS:
            self.report.add(ValidationResult(
                check_number=9,
                name="Workflow steps",
                passed=True,
                message=f"Workflow has {len(steps)} numbered steps"
            ))
        else:
            self.report.add(ValidationResult(
                check_number=9,
                name="Workflow steps",
                passed=False,
                message=f"Workflow needs ≥{self.MIN_WORKFLOW_STEPS} numbered steps (found {len(steps)})"
            ))

    def _check_examples(self, is_warning: bool = False) -> None:
        """Check 10: Examples included."""
        body_lower = self._body.lower()

        has_examples = (
            "## example" in body_lower or
            "### example" in body_lower or
            "### input" in body_lower or
            "### output" in body_lower or
            "## quick start" in body_lower
        )

        self.report.add(ValidationResult(
            check_number=10,
            name="Examples",
            passed=has_examples,
            message="Examples section found" if has_examples else "No examples section found",
            is_warning=is_warning
        ))

    def _check_error_handling(self, is_warning: bool = False) -> None:
        """Check 11: Error handling defined."""
        body_lower = self._body.lower()

        has_error_handling = (
            "error" in body_lower or
            "fail" in body_lower or
            "invalid" in body_lower or
            "## error" in body_lower
        )

        self.report.add(ValidationResult(
            check_number=11,
            name="Error handling",
            passed=has_error_handling,
            message="Error handling mentioned" if has_error_handling else "No error handling section found",
            is_warning=is_warning
        ))

    def _check_limitations(self, is_warning: bool = False) -> None:
        """Check 12: Limitations documented."""
        body_lower = self._body.lower()

        has_limitations = (
            "## limitation" in body_lower or
            "does not" in body_lower or
            "not for" in body_lower or
            "out of scope" in body_lower
        )

        self.report.add(ValidationResult(
            check_number=12,
            name="Limitations",
            passed=has_limitations,
            message="Limitations documented" if has_limitations else "No limitations section found",
            is_warning=is_warning
        ))

    def _check_task_tool_documentation(self, is_warning: bool = False) -> None:
        """Check 13: Task tool documentation for complex workflows with agent delegation."""
        steps_dir = self.skill_path / "steps"

        # Skip if no steps directory (simple skill)
        if not steps_dir.exists():
            self.report.add(ValidationResult(
                check_number=13,
                name="Task tool docs",
                passed=True,
                message="Simple skill (no steps/, no Task tool needed)",
                is_warning=is_warning
            ))
            return

        # Count steps to determine complexity
        step_files = list(steps_dir.glob("step-*.md"))

        # Only check for complex skills (4+ steps)
        if len(step_files) < 4:
            self.report.add(ValidationResult(
                check_number=13,
                name="Task tool docs",
                passed=True,
                message=f"Simple workflow ({len(step_files)} steps, Task tool optional)",
                is_warning=is_warning
            ))
            return

        # For complex skills, check if any delegable agents are referenced
        delegable_agents = ["@planner", "@plan-validator", "@code-reviewer", "@security-auditor"]
        uses_delegable = False
        has_task_doc = False

        for step_file in step_files:
            try:
                content = step_file.read_text(encoding="utf-8")
                for agent in delegable_agents:
                    if agent in content:
                        uses_delegable = True
                        # Check for Task invocation syntax
                        if "subagent_type:" in content or "subagent_type=" in content:
                            has_task_doc = True
                            break
                if has_task_doc:
                    break
            except (OSError, UnicodeDecodeError):
                pass

        if not uses_delegable:
            self.report.add(ValidationResult(
                check_number=13,
                name="Task tool docs",
                passed=True,
                message="No delegable agents used",
                is_warning=is_warning
            ))
        elif has_task_doc:
            self.report.add(ValidationResult(
                check_number=13,
                name="Task tool docs",
                passed=True,
                message="Task tool invocations documented",
                is_warning=is_warning
            ))
        else:
            self.report.add(ValidationResult(
                check_number=13,
                name="Task tool docs",
                passed=False,
                message="Delegable agents referenced but no Task invocation found",
                is_warning=is_warning
            ))


def print_report(report: ValidationReport, permissive: bool = False) -> int:
    """
    Print validation report and return exit code.

    Args:
        report: ValidationReport to print
        permissive: If True, warnings don't cause failure

    Returns:
        0 if all checks pass, 1 if any required check fails
    """
    print(f"\n🔍 Validating skill: {report.skill_name}")
    print(f"   Path: {report.skill_path}\n")

    # Group results
    required = [r for r in report.results if r.check_number <= 9]
    recommended = [r for r in report.results if r.check_number > 9]

    print("Required Checks:")
    for r in required:
        icon = "✅" if r.passed else "❌"
        print(f"  {icon} {r.check_number}. {r.name}: {r.message}")

    print("\nRecommended Checks:")
    for r in recommended:
        if r.passed:
            icon = "✅"
        elif r.is_warning:
            icon = "⚠️ "
        else:
            icon = "❌"
        print(f"  {icon} {r.check_number}. {r.name}: {r.message}")

    print("\n" + "─" * 50)

    # Determine result
    required_ok = all(r.passed for r in required)
    recommended_ok = all(r.passed for r in recommended)

    if required_ok and recommended_ok:
        print("Result: ✅ PASS (all checks passed)")
        return 0
    elif required_ok and permissive:
        warnings = sum(1 for r in recommended if not r.passed)
        print(f"Result: ✅ PASS ({warnings} warning{'s' if warnings > 1 else ''})")
        return 0
    elif required_ok:
        failures = sum(1 for r in recommended if not r.passed)
        print(f"Result: ❌ FAIL ({failures} recommended check{'s' if failures > 1 else ''} failed)")
        print("   Tip: Use --permissive to treat recommended checks as warnings")
        return 1
    else:
        failures = sum(1 for r in required if not r.passed)
        print(f"Result: ❌ FAIL ({failures} required check{'s' if failures > 1 else ''} failed)")
        return 1


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate EPCI skill output against best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ../brainstorm/              # Validate skill
  %(prog)s ../core/state-manager/      # Validate core skill
  %(prog)s ./my-skill/ --permissive    # Warnings only for recommended
        """
    )
    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to skill directory (containing SKILL.md)"
    )
    parser.add_argument(
        "--permissive",
        action="store_true",
        help="Treat recommended checks as warnings (non-blocking)"
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=None,
        help="Root skills/ directory for uniqueness check (auto-detected if not specified)"
    )

    args = parser.parse_args()

    # Resolve path
    skill_path = args.skill_path.resolve()

    if not skill_path.exists():
        print(f"❌ Error: Path does not exist: {skill_path}")
        return 1

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return 1

    # Run validation
    validator = SkillValidator(skill_path, skills_root=args.skills_root)
    report = validator.validate_all(permissive=args.permissive)

    return print_report(report, permissive=args.permissive)


if __name__ == "__main__":
    sys.exit(main())
