#!/usr/bin/env python3
"""Tests for validate_cross_refs.py"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_cross_refs import (
    get_available_skills,
    get_available_agents,
    get_available_commands,
    extract_skill_refs,
    extract_agent_refs,
    CrossRefFinding,
    ValidationReport
)


class TestGetAvailableSkills:
    """Tests for get_available_skills function."""

    def test_find_skills(self, tmp_path):
        """Test finding skills."""
        skill_dir = tmp_path / "skills" / "core" / "test-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Test Skill")

        result = get_available_skills(tmp_path)

        assert "test-skill" in result

    def test_empty_directory(self, tmp_path):
        """Test with empty directory."""
        result = get_available_skills(tmp_path)
        assert result == set()

    def test_multiple_skills(self, tmp_path):
        """Test finding multiple skills."""
        for name in ["skill-a", "skill-b", "skill-c"]:
            skill_dir = tmp_path / "skills" / "core" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(f"# {name}")

        result = get_available_skills(tmp_path)

        assert len(result) == 3
        assert "skill-a" in result
        assert "skill-b" in result
        assert "skill-c" in result


class TestGetAvailableAgents:
    """Tests for get_available_agents function."""

    def test_find_agents(self, tmp_path):
        """Test finding agents."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "code-reviewer.md").write_text("# Code Reviewer")

        result = get_available_agents(tmp_path)

        assert "code-reviewer" in result

    def test_empty_directory(self, tmp_path):
        """Test with empty directory."""
        result = get_available_agents(tmp_path)
        assert result == set()


class TestGetAvailableCommands:
    """Tests for get_available_commands function."""

    def test_find_commands(self, tmp_path):
        """Test finding commands."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "brief.md").write_text("# Brief")

        result = get_available_commands(tmp_path)

        assert "brief" in result


class TestExtractSkillRefs:
    """Tests for extract_skill_refs function."""

    def test_extract_at_skill_pattern(self):
        """Test @skill:xxx pattern."""
        content = "Use @skill:breakpoint-display to show..."

        result = extract_skill_refs(content)

        assert len(result) == 1
        assert result[0] == (1, "breakpoint-display")

    def test_extract_skill_braces_pattern(self):
        """Test @skill:{xxx} pattern."""
        content = "Use @skill:{tdd-workflow} for testing..."

        result = extract_skill_refs(content)

        assert len(result) == 1
        assert result[0] == (1, "tdd-workflow")

    def test_extract_skill_backtick_pattern(self):
        """Test skill `xxx` pattern."""
        content = "See documentation of skill `epci-core` for details."

        result = extract_skill_refs(content)

        assert len(result) == 1
        assert result[0] == (1, "epci-core")

    def test_multiple_refs(self):
        """Test multiple skill references."""
        content = """Line 1: @skill:a
Line 2: @skill:b
Line 3: skill `c`"""

        result = extract_skill_refs(content)

        assert len(result) == 3

    def test_no_refs(self):
        """Test content without skill refs."""
        content = "No skill references here."

        result = extract_skill_refs(content)

        assert len(result) == 0


class TestExtractAgentRefs:
    """Tests for extract_agent_refs function."""

    def test_extract_at_agent_pattern(self):
        """Test @agent-name pattern."""
        content = "Submit to @plan-validator for review."

        result = extract_agent_refs(content)

        assert len(result) == 1
        assert result[0] == (1, "plan-validator")

    def test_extract_subagent_backtick(self):
        """Test subagent `name` pattern."""
        content = "Use subagent `code-reviewer` for code review."

        result = extract_agent_refs(content)

        assert len(result) == 1
        assert result[0] == (1, "code-reviewer")

    def test_known_agents_only(self):
        """Test only known agent patterns are extracted."""
        content = "@unknown-thing should not match"

        result = extract_agent_refs(content)

        # Should not match unknown patterns
        assert len(result) == 0


class TestCrossRefFinding:
    """Tests for CrossRefFinding dataclass."""

    def test_str_representation(self, tmp_path):
        """Test string representation."""
        finding = CrossRefFinding(
            source_file=tmp_path / "test.md",
            line_number=42,
            ref_type="skill",
            ref_target="nonexistent",
            issue="Missing skill: nonexistent"
        )

        result = str(finding)

        assert "test.md" in result
        assert "42" in result
        assert "skill" in result
        assert "nonexistent" in result


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_initial_state(self):
        """Test initial state."""
        report = ValidationReport()
        assert report.valid is True
        assert report.refs_checked == 0
        assert len(report.findings) == 0

    def test_add_finding_missing(self, tmp_path):
        """Test adding missing ref finding."""
        report = ValidationReport()
        finding = CrossRefFinding(
            source_file=tmp_path / "test.md",
            line_number=1,
            ref_type="skill",
            ref_target="missing",
            issue="Missing skill: missing"
        )

        report.add_finding(finding)

        assert report.valid is False  # Missing refs invalidate

    def test_add_finding_warning(self, tmp_path):
        """Test adding warning finding."""
        report = ValidationReport()
        finding = CrossRefFinding(
            source_file=tmp_path / "test.md",
            line_number=1,
            ref_type="file",
            ref_target="ref.md",
            issue="Reference file may not exist: ref.md"
        )

        report.add_finding(finding)

        assert report.valid is True  # Warnings don't invalidate

    def test_print_report(self, capsys):
        """Test print_report."""
        report = ValidationReport()
        report.refs_checked = 100
        report.pass_check()

        result = report.print_report()

        assert result == 0
