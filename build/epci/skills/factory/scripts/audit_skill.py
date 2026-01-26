#!/usr/bin/env python3
"""
EPCI Skill Auditor - Complete validation of skill compliance.

Validates that an existing skill respects all EPCI best practices:
- Structure (12-point checklist from validate_skill_output.py)
- Breakpoint compliance
- Core skills usage
- Stack skills detection
- Step chain validation

Usage:
    python audit_skill.py <skill_path>
    python audit_skill.py <skill_path> --json

Exit codes:
    0 = All checks pass (or pass with warnings)
    1 = Critical/required check failed
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# Import from sibling module
from validate_skill_output import SkillValidator, ValidationReport


class AuditPhase(Enum):
    """Audit phases."""
    STRUCTURE = 1
    BREAKPOINTS = 2
    CORE_SKILLS = 3
    STACK_SKILLS = 4
    STEP_CHAIN = 5


class Severity(Enum):
    """Audit result severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AuditResult:
    """Result of a single audit check."""
    phase: AuditPhase
    check_id: str
    name: str
    passed: bool
    message: str
    severity: Severity = Severity.ERROR
    suggestion: Optional[str] = None


@dataclass
class PhaseReport:
    """Report for a single phase."""
    phase: AuditPhase
    results: list[AuditResult] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def total_count(self) -> int:
        return len(self.results)

    @property
    def has_errors(self) -> bool:
        return any(not r.passed and r.severity == Severity.ERROR for r in self.results)

    @property
    def has_warnings(self) -> bool:
        return any(not r.passed and r.severity == Severity.WARNING for r in self.results)

    @property
    def status(self) -> str:
        if self.has_errors:
            return "FAIL"
        if self.has_warnings:
            return "WARN"
        return "OK"


@dataclass
class AuditReport:
    """Complete audit report for a skill."""
    skill_name: str
    skill_path: Path
    user_invocable: bool
    phases: dict[AuditPhase, PhaseReport] = field(default_factory=dict)

    @property
    def total_passed(self) -> int:
        return sum(p.passed_count for p in self.phases.values())

    @property
    def total_checks(self) -> int:
        return sum(p.total_count for p in self.phases.values())

    @property
    def has_errors(self) -> bool:
        return any(p.has_errors for p in self.phases.values())

    @property
    def warning_count(self) -> int:
        return sum(
            1 for p in self.phases.values()
            for r in p.results
            if not r.passed and r.severity == Severity.WARNING
        )

    @property
    def overall_status(self) -> str:
        if self.has_errors:
            return "FAIL"
        if self.warning_count > 0:
            return "PASS WITH WARNINGS"
        return "PASS"


class SkillAuditor:
    """Orchestrates complete skill audit across all phases."""

    # Allowed breakpoint types
    ALLOWED_BREAKPOINT_TYPES = [
        "validation", "analysis", "plan-review", "phase-transition",
        "decomposition", "diagnostic", "ems-status", "info-only"
    ]

    # Core skills requirements per user skill
    CORE_SKILLS_REQUIREMENTS = {
        "brainstorm": {
            "required": ["breakpoint-system", "complexity-calculator", "project-memory"],
            "optional": ["clarification-engine", "ems-evaluator"]
        },
        "spec": {
            "required": ["breakpoint-system", "complexity-calculator", "project-memory"],
            "optional": ["clarification-engine"]
        },
        "implement": {
            "required": ["breakpoint-system", "complexity-calculator", "tdd-enforcer",
                        "state-manager", "project-memory"],
            "optional": ["clarification-engine"]
        },
        "quick": {
            "required": ["breakpoint-system", "complexity-calculator", "tdd-enforcer",
                        "state-manager", "project-memory"],
            "optional": []
        },
        "debug": {
            "required": ["breakpoint-system", "project-memory"],
            "optional": ["clarification-engine"]
        },
        "refactor": {
            "required": ["breakpoint-system", "project-memory"],
            "optional": ["tdd-enforcer"]
        },
        "factory": {
            "required": ["breakpoint-system", "complexity-calculator", "project-memory"],
            "optional": ["clarification-engine"]
        },
    }

    # Stack detection patterns
    STACK_PATTERNS = {
        "python-django": {
            "files": ["manage.py", "requirements.txt", "pyproject.toml"],
            "content_patterns": ["django", "Django"]
        },
        "javascript-react": {
            "files": ["package.json"],
            "content_patterns": ["react", "React"]
        },
        "java-springboot": {
            "files": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "content_patterns": ["spring-boot", "springframework"]
        },
        "php-symfony": {
            "files": ["composer.json", "bin/console"],
            "content_patterns": ["symfony"]
        },
        "frontend-editor": {
            "files": ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.cjs"],
            "content_patterns": ["tailwind"]
        }
    }

    def __init__(self, skill_path: Path):
        """
        Initialize auditor.

        Args:
            skill_path: Path to skill directory (containing SKILL.md)
        """
        self.skill_path = Path(skill_path).resolve()
        self.skill_md = self.skill_path / "SKILL.md"
        self.steps_dir = self.skill_path / "steps"
        self.references_dir = self.skill_path / "references"

        # Parsed content
        self._content: str = ""
        self._frontmatter: dict = {}
        self._body: str = ""

        # Report
        self.report: Optional[AuditReport] = None

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
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                if current_key and current_value_lines:
                    self._frontmatter[current_key] = " ".join(current_value_lines).strip()

                key, _, value = line.partition(":")
                current_key = key.strip()
                value = value.strip()

                if value in (">-", "|", ">"):
                    current_value_lines = []
                else:
                    self._frontmatter[current_key] = value
                    current_key = None
                    current_value_lines = []
            elif current_key:
                current_value_lines.append(line.strip())

        if current_key and current_value_lines:
            self._frontmatter[current_key] = " ".join(current_value_lines).strip()

    def _search_pattern(self, pattern: str, include_steps: bool = True) -> list[tuple[Path, str]]:
        """
        Search for a regex pattern in skill files.

        Returns list of (file_path, matched_text) tuples.
        """
        matches = []
        regex = re.compile(pattern, re.IGNORECASE)

        # Search SKILL.md
        for match in regex.finditer(self._content):
            matches.append((self.skill_md, match.group()))

        # Search steps/
        if include_steps and self.steps_dir.exists():
            for step_file in self.steps_dir.glob("*.md"):
                try:
                    content = step_file.read_text(encoding="utf-8")
                    for match in regex.finditer(content):
                        matches.append((step_file, match.group()))
                except (OSError, UnicodeDecodeError):
                    pass

        # Search references/
        if self.references_dir.exists():
            for ref_file in self.references_dir.glob("*.md"):
                try:
                    content = ref_file.read_text(encoding="utf-8")
                    for match in regex.finditer(content):
                        matches.append((ref_file, match.group()))
                except (OSError, UnicodeDecodeError):
                    pass

        return matches

    def audit(self) -> AuditReport:
        """
        Run complete audit across all phases.

        Returns:
            AuditReport with all results
        """
        if not self._load_skill():
            # Create minimal report for missing skill
            self.report = AuditReport(
                skill_name="unknown",
                skill_path=self.skill_path,
                user_invocable=False
            )
            phase_report = PhaseReport(phase=AuditPhase.STRUCTURE)
            phase_report.results.append(AuditResult(
                phase=AuditPhase.STRUCTURE,
                check_id="P1.0",
                name="File exists",
                passed=False,
                message=f"SKILL.md not found at {self.skill_md}",
                severity=Severity.ERROR
            ))
            self.report.phases[AuditPhase.STRUCTURE] = phase_report
            return self.report

        skill_name = self._frontmatter.get("name", self.skill_path.name)
        user_invocable = self._frontmatter.get("user-invocable", "true").lower() == "true"

        self.report = AuditReport(
            skill_name=skill_name,
            skill_path=self.skill_path,
            user_invocable=user_invocable
        )

        # Run all phases
        self.report.phases[AuditPhase.STRUCTURE] = self._run_phase_1_structure()
        self.report.phases[AuditPhase.BREAKPOINTS] = self._run_phase_2_breakpoints()
        self.report.phases[AuditPhase.CORE_SKILLS] = self._run_phase_3_core_skills()
        self.report.phases[AuditPhase.STACK_SKILLS] = self._run_phase_4_stack_skills()
        self.report.phases[AuditPhase.STEP_CHAIN] = self._run_phase_5_step_chain()

        return self.report

    # Name pattern: allows epci: prefix, then lowercase kebab-case
    NAME_PATTERN_WITH_PREFIX = re.compile(r"^(epci:)?[a-z][a-z0-9-]*$")

    def _run_phase_1_structure(self) -> PhaseReport:
        """Phase 1: Structure validation using 12-point checklist."""
        phase_report = PhaseReport(phase=AuditPhase.STRUCTURE)

        # Reuse existing validator
        validator = SkillValidator(self.skill_path)
        validation_report = validator.validate_all(permissive=True)

        # Convert ValidationResult to AuditResult, with special handling for name format
        for result in validation_report.results:
            severity = Severity.WARNING if result.is_warning else Severity.ERROR

            # Special case: name format check should allow epci: prefix
            if result.check_number == 2 and not result.passed:
                name = self._frontmatter.get("name", "")
                if self.NAME_PATTERN_WITH_PREFIX.match(name):
                    # Name is valid with epci: prefix
                    phase_report.results.append(AuditResult(
                        phase=AuditPhase.STRUCTURE,
                        check_id=f"P1.{result.check_number}",
                        name=result.name,
                        passed=True,
                        message=f"Name valid with prefix: {name}",
                        severity=severity
                    ))
                    continue

            # Special case: workflow steps check (P1.9) is not required for core skills
            # Core skills have different structures and may not have numbered workflow steps
            if result.check_number == 9 and not result.passed and not self.report.user_invocable:
                phase_report.results.append(AuditResult(
                    phase=AuditPhase.STRUCTURE,
                    check_id=f"P1.{result.check_number}",
                    name=result.name,
                    passed=True,
                    message="Core skill (numbered workflow steps not required)",
                    severity=Severity.INFO
                ))
                continue

            phase_report.results.append(AuditResult(
                phase=AuditPhase.STRUCTURE,
                check_id=f"P1.{result.check_number}",
                name=result.name,
                passed=result.passed,
                message=result.message,
                severity=severity
            ))

        return phase_report

    def _run_phase_2_breakpoints(self) -> PhaseReport:
        """Phase 2: Breakpoint compliance validation."""
        phase_report = PhaseReport(phase=AuditPhase.BREAKPOINTS)

        # Check 2.1: User-invocable skill should use breakpoint-system
        if self.report.user_invocable:
            uses_breakpoint = bool(self._search_pattern(
                r"@skill:epci:breakpoint-system|epci:breakpoint-system"
            ))
            phase_report.results.append(AuditResult(
                phase=AuditPhase.BREAKPOINTS,
                check_id="P2.1",
                name="Uses breakpoint-system",
                passed=uses_breakpoint,
                message="Uses epci:breakpoint-system" if uses_breakpoint else "Missing breakpoint-system usage",
                severity=Severity.ERROR,
                suggestion=(
                    "Add to Shared Components Used:\n"
                    "  - `epci:breakpoint-system` -- Interactive breakpoints"
                ) if not uses_breakpoint else None
            ))

        # Check 2.2: Breakpoint types in allowed list
        type_matches = self._search_pattern(r"type:\s*[\"']?(\w+(?:-\w+)*)[\"']?")
        found_types = set()
        invalid_types = []

        for _, match_text in type_matches:
            # Extract type value
            type_match = re.search(r"type:\s*[\"']?(\w+(?:-\w+)*)[\"']?", match_text)
            if type_match:
                type_value = type_match.group(1)
                # Skip common non-breakpoint types
                if type_value not in ["string", "number", "boolean", "object", "array"]:
                    found_types.add(type_value)
                    if type_value not in self.ALLOWED_BREAKPOINT_TYPES:
                        invalid_types.append(type_value)

        if self.report.user_invocable and found_types:
            phase_report.results.append(AuditResult(
                phase=AuditPhase.BREAKPOINTS,
                check_id="P2.2",
                name="Breakpoint types valid",
                passed=len(invalid_types) == 0,
                message=(
                    f"All breakpoint types valid: {', '.join(found_types)}"
                    if not invalid_types
                    else f"Invalid breakpoint types: {', '.join(invalid_types)}"
                ),
                severity=Severity.WARNING,
                suggestion=(
                    f"Use allowed types: {', '.join(self.ALLOWED_BREAKPOINT_TYPES)}"
                ) if invalid_types else None
            ))

        # Check 2.3: Breakpoints section in SKILL.md for user skills
        if self.report.user_invocable:
            has_breakpoints_section = bool(re.search(
                r"##\s*Breakpoints?|breakpoint.*types?.*used",
                self._body,
                re.IGNORECASE
            ))
            # Also check Shared Components section for breakpoint mention
            has_in_shared_components = bool(re.search(
                r"Shared Components.*breakpoint-system|breakpoint-system.*Shared Components",
                self._body,
                re.IGNORECASE | re.DOTALL
            ))

            phase_report.results.append(AuditResult(
                phase=AuditPhase.BREAKPOINTS,
                check_id="P2.3",
                name="Breakpoints documented",
                passed=has_breakpoints_section or has_in_shared_components,
                message=(
                    "Breakpoints documented in SKILL.md"
                    if has_breakpoints_section or has_in_shared_components
                    else "Missing Breakpoints section or mention in Shared Components"
                ),
                severity=Severity.WARNING,
                suggestion=(
                    "Add ## Breakpoints section or document in Shared Components Used"
                ) if not (has_breakpoints_section or has_in_shared_components) else None
            ))

        # Check 2.4: No manual ASCII boxes for interactive breakpoints
        ascii_box_patterns = [
            r"\+[-=]+\+.*\n.*\|.*\|.*\n.*\+[-=]+\+",  # +---+ boxes
            r"┌[─┬]+┐.*\n.*│.*│.*\n.*└[─┴]+┘",  # Unicode box drawing
        ]
        manual_boxes = []
        for pattern in ascii_box_patterns:
            if self.steps_dir.exists():
                for step_file in self.steps_dir.glob("*.md"):
                    try:
                        content = step_file.read_text(encoding="utf-8")
                        # Check for boxes that seem to be interactive (have options/choices)
                        if re.search(pattern, content, re.DOTALL):
                            # Check if it's near AskUserQuestion or option patterns
                            if re.search(r"option|choice|select|proceed|cancel", content, re.IGNORECASE):
                                manual_boxes.append(step_file.name)
                    except (OSError, UnicodeDecodeError):
                        pass

        if self.report.user_invocable:
            phase_report.results.append(AuditResult(
                phase=AuditPhase.BREAKPOINTS,
                check_id="P2.4",
                name="No manual interactive boxes",
                passed=len(manual_boxes) == 0,
                message=(
                    "No manual ASCII boxes for interactive breakpoints"
                    if not manual_boxes
                    else f"Potential manual interactive boxes in: {', '.join(manual_boxes)}"
                ),
                severity=Severity.WARNING,
                suggestion=(
                    "Use @skill:epci:breakpoint-system instead of manual ASCII boxes"
                ) if manual_boxes else None
            ))

        return phase_report

    def _run_phase_3_core_skills(self) -> PhaseReport:
        """Phase 3: Core skills usage validation."""
        phase_report = PhaseReport(phase=AuditPhase.CORE_SKILLS)

        # Determine which core skills are required for this skill
        skill_base_name = self._frontmatter.get("name", "").replace("epci:", "")
        requirements = self.CORE_SKILLS_REQUIREMENTS.get(skill_base_name, {})
        required_skills = requirements.get("required", [])
        optional_skills = requirements.get("optional", [])

        if not required_skills and not self.report.user_invocable:
            # Core skills don't have core skill requirements
            phase_report.results.append(AuditResult(
                phase=AuditPhase.CORE_SKILLS,
                check_id="P3.0",
                name="Core skill (no requirements)",
                passed=True,
                message="Core skills don't require other core skills",
                severity=Severity.INFO
            ))
            return phase_report

        if not required_skills:
            # Unknown user skill - check for basic breakpoint-system usage
            required_skills = ["breakpoint-system", "project-memory"]

        # Check required core skills
        for idx, core_skill in enumerate(required_skills, 1):
            found = bool(self._search_pattern(
                rf"epci:{core_skill}|@skill:epci:{core_skill}|`{core_skill}`"
            ))
            phase_report.results.append(AuditResult(
                phase=AuditPhase.CORE_SKILLS,
                check_id=f"P3.{idx}",
                name=f"Uses {core_skill}",
                passed=found,
                message=f"Uses epci:{core_skill}" if found else f"Missing epci:{core_skill}",
                severity=Severity.ERROR,
                suggestion=(
                    f"Add to Shared Components Used:\n"
                    f"  - `epci:{core_skill}` -- [description]"
                ) if not found else None
            ))

        # Check optional core skills (warnings only)
        for idx, core_skill in enumerate(optional_skills, len(required_skills) + 1):
            found = bool(self._search_pattern(
                rf"epci:{core_skill}|@skill:epci:{core_skill}|`{core_skill}`"
            ))
            phase_report.results.append(AuditResult(
                phase=AuditPhase.CORE_SKILLS,
                check_id=f"P3.{idx}",
                name=f"Uses {core_skill}",
                passed=found,
                message=f"Uses epci:{core_skill}" if found else f"Consider adding epci:{core_skill}",
                severity=Severity.INFO,
                suggestion=(
                    f"Consider adding to Shared Components:\n"
                    f"  - `epci:{core_skill}` -- [description]"
                ) if not found else None
            ))

        return phase_report

    def _run_phase_4_stack_skills(self) -> PhaseReport:
        """Phase 4: Stack skills detection and recommendations."""
        phase_report = PhaseReport(phase=AuditPhase.STACK_SKILLS)

        # Check declared stack skills in Shared Components or Subagents
        declared_stacks = []
        for stack_name in self.STACK_PATTERNS:
            if re.search(rf"epci:{stack_name}", self._content, re.IGNORECASE):
                declared_stacks.append(stack_name)

        # Check if skill explicitly mentions auto-detection as a feature IT provides
        # (not just references to stack skills in documentation)
        has_stack_auto_detect = bool(re.search(
            r"auto-detect(?:s|ion)?.*(?:stack|technology|framework)",
            self._content,
            re.IGNORECASE
        )) and bool(re.search(
            r"this skill.*detect|detect.*automatically",
            self._content,
            re.IGNORECASE
        ))

        if declared_stacks:
            # Skill declares stack skills - validate they exist
            for stack_name in declared_stacks:
                phase_report.results.append(AuditResult(
                    phase=AuditPhase.STACK_SKILLS,
                    check_id=f"P4.{list(self.STACK_PATTERNS.keys()).index(stack_name) + 1}",
                    name=f"{stack_name} declared",
                    passed=True,
                    message=f"Stack skill epci:{stack_name} properly declared",
                    severity=Severity.INFO
                ))
        elif has_stack_auto_detect:
            # Skill mentions auto-detection but doesn't declare any stacks
            phase_report.results.append(AuditResult(
                phase=AuditPhase.STACK_SKILLS,
                check_id="P4.0",
                name="Stack auto-detection",
                passed=False,
                message="Skill mentions auto-detection but no stack skills declared",
                severity=Severity.WARNING,
                suggestion=(
                    "Add stack skills to Subagents or Shared Components:\n"
                    "  - epci:python-django, epci:javascript-react, etc."
                )
            ))
        else:
            # Skill is stack-agnostic (doesn't mention stacks)
            phase_report.results.append(AuditResult(
                phase=AuditPhase.STACK_SKILLS,
                check_id="P4.0",
                name="Stack detection",
                passed=True,
                message="Skill is stack-agnostic (no stack skills required)",
                severity=Severity.INFO
            ))

        return phase_report

    def _run_phase_5_step_chain(self) -> PhaseReport:
        """Phase 5: Step chain validation (user skills with steps only)."""
        phase_report = PhaseReport(phase=AuditPhase.STEP_CHAIN)

        # Skip if no steps directory
        if not self.steps_dir.exists():
            if self.report.user_invocable:
                # Check if this might be a --simple skill (acceptable)
                has_workflow_in_skill = bool(re.search(
                    r"##\s*Workflow|##\s*Protocol|##\s*Steps",
                    self._body,
                    re.IGNORECASE
                ))
                phase_report.results.append(AuditResult(
                    phase=AuditPhase.STEP_CHAIN,
                    check_id="P5.0",
                    name="Steps directory",
                    passed=has_workflow_in_skill,
                    message=(
                        "No steps/ directory (simple skill with inline workflow)"
                        if has_workflow_in_skill
                        else "No steps/ directory and no inline workflow"
                    ),
                    severity=Severity.INFO if has_workflow_in_skill else Severity.WARNING,
                    suggestion=(
                        "User-invocable skill should have steps/ directory or inline ## Workflow"
                    ) if not has_workflow_in_skill else None
                ))
            else:
                # Core skill - no steps expected
                phase_report.results.append(AuditResult(
                    phase=AuditPhase.STEP_CHAIN,
                    check_id="P5.0",
                    name="Steps directory",
                    passed=True,
                    message="Core skill (steps/ not required)",
                    severity=Severity.INFO
                ))
            return phase_report

        # Check 5.1: step-00-*.md exists
        step_00_files = list(self.steps_dir.glob("step-00-*.md"))
        phase_report.results.append(AuditResult(
            phase=AuditPhase.STEP_CHAIN,
            check_id="P5.1",
            name="step-00 exists",
            passed=len(step_00_files) > 0,
            message=(
                f"Found init step: {step_00_files[0].name}"
                if step_00_files
                else "Missing step-00-*.md initialization step"
            ),
            severity=Severity.ERROR,
            suggestion="Create steps/step-00-init.md" if not step_00_files else None
        ))

        # Build step graph
        step_graph = self._build_step_graph()
        all_steps = set(step_graph.keys())

        # Find the highest numbered step (likely the final step)
        step_numbers = []
        for step_name in step_graph.keys():
            match = re.match(r"step-(\d{2})", step_name)
            if match:
                step_numbers.append((int(match.group(1)), step_name))
        max_step_name = max(step_numbers, key=lambda x: x[0])[1] if step_numbers else None

        # Check 5.2: Each step has next_step or conditional_next
        steps_without_next = []
        for step_name, step_info in step_graph.items():
            if not step_info["next_step"] and not step_info["conditional_next"]:
                # Allow final steps (step-99, highest numbered step, or explicitly marked as final)
                is_final = (
                    re.match(r"step-99-", step_name) or
                    "final" in step_name.lower() or
                    "generation" in step_name.lower() or
                    "finish" in step_name.lower() or
                    step_name == max_step_name
                )
                if not is_final:
                    steps_without_next.append(step_name)

        phase_report.results.append(AuditResult(
            phase=AuditPhase.STEP_CHAIN,
            check_id="P5.2",
            name="Steps have next_step",
            passed=len(steps_without_next) == 0,
            message=(
                "All steps have next_step or conditional_next"
                if not steps_without_next
                else f"Steps missing next_step: {', '.join(steps_without_next)}"
            ),
            severity=Severity.ERROR,
            suggestion=(
                "Add next_step or conditional_next to each step file"
            ) if steps_without_next else None
        ))

        # Check 5.3: No orphan steps (not referenced by any other step)
        referenced_steps = set()
        for step_info in step_graph.values():
            if step_info["next_step"]:
                referenced_steps.add(step_info["next_step"])
            for cond_next in step_info["conditional_next"]:
                referenced_steps.add(cond_next)

        # step-00 shouldn't be referenced (it's the entry point)
        orphan_steps = []
        for step_name in all_steps:
            if step_name not in referenced_steps and not step_name.startswith("step-00"):
                orphan_steps.append(step_name)

        phase_report.results.append(AuditResult(
            phase=AuditPhase.STEP_CHAIN,
            check_id="P5.3",
            name="No orphan steps",
            passed=len(orphan_steps) == 0,
            message=(
                "All steps are reachable"
                if not orphan_steps
                else f"Orphan steps (not referenced): {', '.join(orphan_steps)}"
            ),
            severity=Severity.WARNING,
            suggestion=(
                "Ensure all steps are referenced by next_step or conditional_next"
            ) if orphan_steps else None
        ))

        # Check 5.4: Chain completeness (can reach from step-00 to a terminal)
        if step_00_files:
            reachable = self._get_reachable_steps(step_graph, step_00_files[0].stem)
            unreachable = all_steps - reachable

            phase_report.results.append(AuditResult(
                phase=AuditPhase.STEP_CHAIN,
                check_id="P5.4",
                name="Chain completeness",
                passed=len(unreachable) == 0,
                message=(
                    f"All {len(all_steps)} steps reachable from step-00"
                    if not unreachable
                    else f"Unreachable steps: {', '.join(unreachable)}"
                ),
                severity=Severity.WARNING,
                suggestion=(
                    "Fix step chain to ensure all steps are reachable"
                ) if unreachable else None
            ))

        # Check 5.5: Step naming convention
        invalid_names = []
        for step_file in self.steps_dir.glob("*.md"):
            if not re.match(r"step-\d{2}[a-z]?-[\w-]+\.md", step_file.name):
                invalid_names.append(step_file.name)

        phase_report.results.append(AuditResult(
            phase=AuditPhase.STEP_CHAIN,
            check_id="P5.5",
            name="Step naming convention",
            passed=len(invalid_names) == 0,
            message=(
                "All steps follow naming convention (step-XX-name.md)"
                if not invalid_names
                else f"Invalid step names: {', '.join(invalid_names)}"
            ),
            severity=Severity.WARNING,
            suggestion=(
                "Use format: step-XX-name.md (e.g., step-01-analysis.md)"
            ) if invalid_names else None
        ))

        return phase_report

    def _build_step_graph(self) -> dict:
        """Build a graph of step transitions."""
        graph = {}

        for step_file in self.steps_dir.glob("step-*.md"):
            try:
                content = step_file.read_text(encoding="utf-8")
                step_name = step_file.stem

                # Find all step references in the file
                all_step_refs = set()

                # Pattern 1: Direct reference → `step-XX-name.md`
                direct_refs = re.findall(r"→\s*`?(step-\d{2}[a-z]?-[\w-]+)", content)
                all_step_refs.update(direct_refs)

                # Pattern 2: Table format | → `step-XX-name.md` |
                table_refs = re.findall(r"\|\s*→?\s*`?(step-\d{2}[a-z]?-[\w-]+)", content)
                all_step_refs.update(table_refs)

                # Pattern 3: next_step: step-XX-name.md
                next_step_refs = re.findall(r"next_step[:\s]+`?(step-\d{2}[a-z]?-[\w-]+)", content, re.IGNORECASE)
                all_step_refs.update(next_step_refs)

                # Pattern 4: Any backtick reference to a step file
                backtick_refs = re.findall(r"`(step-\d{2}[a-z]?-[\w-]+)(?:\.md)?`", content)
                all_step_refs.update(backtick_refs)

                # Determine primary next_step (first direct reference after "## Next Step")
                next_step = None
                next_step_section = re.search(r"##\s*Next\s*Step.*?(?=##|\Z)", content, re.IGNORECASE | re.DOTALL)
                if next_step_section:
                    section_text = next_step_section.group()
                    section_refs = re.findall(r"(step-\d{2}[a-z]?-[\w-]+)", section_text)
                    if section_refs:
                        next_step = section_refs[0]

                # All other references are conditional
                conditional_next = list(all_step_refs - {next_step} if next_step else all_step_refs)

                graph[step_name] = {
                    "next_step": next_step,
                    "conditional_next": conditional_next
                }

            except (OSError, UnicodeDecodeError):
                pass

        return graph

    def _get_reachable_steps(self, graph: dict, start: str) -> set:
        """Get all steps reachable from start using BFS."""
        reachable = set()
        queue = [start]

        while queue:
            current = queue.pop(0)
            if current in reachable:
                continue
            reachable.add(current)

            if current in graph:
                step_info = graph[current]
                if step_info["next_step"] and step_info["next_step"] not in reachable:
                    queue.append(step_info["next_step"])
                for cond_next in step_info["conditional_next"]:
                    if cond_next not in reachable:
                        queue.append(cond_next)

        return reachable


def print_ascii_report(report: AuditReport) -> None:
    """Print audit report in ASCII format."""
    width = 72

    # Header
    print("+" + "-" * (width - 2) + "+")
    title = f"AUDIT SKILL: {report.skill_name}"
    print(f"| {title:<{width - 4}} |")
    print("+" + "-" * (width - 2) + "+")

    # Phase summaries
    phase_names = {
        AuditPhase.STRUCTURE: "Phase 1: Structure (12-point)",
        AuditPhase.BREAKPOINTS: "Phase 2: Breakpoint Compliance",
        AuditPhase.CORE_SKILLS: "Phase 3: Core Skills Usage",
        AuditPhase.STACK_SKILLS: "Phase 4: Stack Skills Detection",
        AuditPhase.STEP_CHAIN: "Phase 5: Step Chain Validation",
    }

    for phase, phase_report in report.phases.items():
        phase_name = phase_names.get(phase, f"Phase {phase.value}")
        status = f"[{phase_report.status}]"
        count = f"{phase_report.passed_count}/{phase_report.total_count}"

        # Color-code status
        if phase_report.status == "OK":
            status_display = f"[OK] {count}"
        elif phase_report.status == "WARN":
            status_display = f"[WARN] {count}"
        else:
            status_display = f"[FAIL] {count}"

        line = f"| {phase_name:<45} {status_display:>22} |"
        print(line)

    print("+" + "-" * (width - 2) + "+")

    # Overall result
    result_line = f"RESULT: {report.overall_status}"
    if report.warning_count > 0 and not report.has_errors:
        result_line += f" ({report.warning_count} warning{'s' if report.warning_count > 1 else ''})"
    print(f"| {result_line:<{width - 4}} |")
    print("+" + "-" * (width - 2) + "+")

    # Suggestions (if any failures or warnings)
    suggestions = []
    for phase_report in report.phases.values():
        for result in phase_report.results:
            if not result.passed and result.suggestion:
                suggestions.append((result.check_id, result.suggestion))

    if suggestions:
        print(f"| {'SUGGESTIONS:':<{width - 4}} |")
        for check_id, suggestion in suggestions[:5]:  # Limit to 5 suggestions
            # Handle multi-line suggestions
            lines = suggestion.split("\n")
            print(f"| [{check_id}] {lines[0]:<{width - 10}} |")
            for line in lines[1:]:
                print(f"|        {line:<{width - 11}} |")
        if len(suggestions) > 5:
            print(f"| ... and {len(suggestions) - 5} more suggestions{' ' * (width - 30)}|")
        print("+" + "-" * (width - 2) + "+")


def print_json_report(report: AuditReport) -> None:
    """Print audit report in JSON format."""
    output = {
        "skill_name": report.skill_name,
        "skill_path": str(report.skill_path),
        "user_invocable": report.user_invocable,
        "overall_status": report.overall_status,
        "total_passed": report.total_passed,
        "total_checks": report.total_checks,
        "warning_count": report.warning_count,
        "phases": {}
    }

    for phase, phase_report in report.phases.items():
        output["phases"][phase.name] = {
            "status": phase_report.status,
            "passed": phase_report.passed_count,
            "total": phase_report.total_count,
            "results": [
                {
                    "check_id": r.check_id,
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity.value,
                    "suggestion": r.suggestion
                }
                for r in phase_report.results
            ]
        }

    print(json.dumps(output, indent=2))


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="EPCI Skill Auditor - Complete validation of skill compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ../brainstorm/              # Audit brainstorm skill
  %(prog)s ../core/state-manager/      # Audit core skill
  %(prog)s ../implement/ --json        # Output as JSON
        """
    )
    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to skill directory (containing SKILL.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report as JSON"
    )

    args = parser.parse_args()

    # Resolve path
    skill_path = args.skill_path.resolve()

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}")
        return 1

    if not skill_path.is_dir():
        print(f"Error: Path is not a directory: {skill_path}")
        return 1

    # Run audit
    auditor = SkillAuditor(skill_path)
    report = auditor.audit()

    # Print report
    if args.json:
        print_json_report(report)
    else:
        print_ascii_report(report)

    # Return exit code
    return 1 if report.has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
