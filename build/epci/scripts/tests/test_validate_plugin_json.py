#!/usr/bin/env python3
"""Tests for validate_plugin_json.py"""

import pytest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_plugin_json import (
    load_plugin_json,
    save_plugin_json,
    find_actual_skills,
    find_actual_commands,
    find_actual_agents,
    validate_entries_exist,
    validate_all_declared,
    ValidationReport
)


class TestLoadPluginJson:
    """Tests for load_plugin_json function."""

    def test_load_valid_json(self, tmp_path):
        """Test loading valid JSON."""
        json_file = tmp_path / "plugin.json"
        data = {"version": "1.0.0", "commands": [], "agents": [], "skills": []}
        json_file.write_text(json.dumps(data))

        result = load_plugin_json(json_file)
        assert result == data

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading non-existent file."""
        result = load_plugin_json(tmp_path / "nonexistent.json")
        assert result is None

    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text("not valid json")

        result = load_plugin_json(json_file)
        assert result is None


class TestSavePluginJson:
    """Tests for save_plugin_json function."""

    def test_save_valid_data(self, tmp_path):
        """Test saving valid data."""
        json_file = tmp_path / "plugin.json"
        data = {"version": "1.0.0", "commands": []}

        result = save_plugin_json(json_file, data)

        assert result is True
        loaded = json.loads(json_file.read_text())
        assert loaded == data


class TestFindActualComponents:
    """Tests for find_actual_* functions."""

    def test_find_actual_skills(self, tmp_path):
        """Test finding actual skills."""
        skills_dir = tmp_path / "skills" / "core" / "test-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text("# Test Skill")

        result = find_actual_skills(tmp_path)

        assert len(result) == 1
        assert "./skills/core/test-skill/SKILL.md" in result

    def test_find_actual_commands(self, tmp_path):
        """Test finding actual commands."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "test.md").write_text("# Test Command")

        result = find_actual_commands(tmp_path)

        assert len(result) == 1
        assert "./commands/test.md" in result

    def test_find_actual_agents(self, tmp_path):
        """Test finding actual agents."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "test-agent.md").write_text("# Test Agent")

        result = find_actual_agents(tmp_path)

        assert len(result) == 1
        assert "./agents/test-agent.md" in result

    def test_find_empty_directory(self, tmp_path):
        """Test finding in empty directory."""
        assert find_actual_skills(tmp_path) == set()
        assert find_actual_commands(tmp_path) == set()
        assert find_actual_agents(tmp_path) == set()


class TestValidateEntriesExist:
    """Tests for validate_entries_exist function."""

    def test_all_entries_exist(self, tmp_path):
        """Test when all entries exist."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "test.md").write_text("# Test")

        plugin_data = {"commands": ["./commands/test.md"]}
        report = ValidationReport()

        missing = validate_entries_exist(plugin_data, tmp_path, "commands", report)

        assert missing == []

    def test_missing_entry(self, tmp_path):
        """Test when entry is missing."""
        plugin_data = {"commands": ["./commands/missing.md"]}
        report = ValidationReport()

        missing = validate_entries_exist(plugin_data, tmp_path, "commands", report)

        assert "./commands/missing.md" in missing


class TestValidateAllDeclared:
    """Tests for validate_all_declared function."""

    def test_all_declared(self):
        """Test when all files are declared."""
        plugin_data = {"commands": ["./commands/test.md"]}
        actual_files = {"./commands/test.md"}

        undeclared = validate_all_declared(plugin_data, actual_files, "commands")

        assert undeclared == []

    def test_undeclared_file(self):
        """Test when file is not declared."""
        plugin_data = {"commands": []}
        actual_files = {"./commands/test.md"}

        undeclared = validate_all_declared(plugin_data, actual_files, "commands")

        assert "./commands/test.md" in undeclared


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_initial_state(self):
        """Test initial report state."""
        report = ValidationReport()
        assert report.valid is True
        assert report.checks_total == 6

    def test_print_report_returns_correct_code(self, capsys):
        """Test print_report return code."""
        report = ValidationReport()
        report.pass_check()
        report.pass_check()

        result = report.print_report()

        assert result == 0  # Valid report

    def test_print_report_with_errors(self, capsys):
        """Test print_report with errors."""
        report = ValidationReport()
        report.add_error("Test error")

        result = report.print_report()

        assert result == 1  # Invalid report
