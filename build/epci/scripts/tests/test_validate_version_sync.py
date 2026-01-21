#!/usr/bin/env python3
"""Tests for validate_version_sync.py"""

import pytest
import tempfile
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_version_sync import (
    extract_version_from_claude_md,
    extract_version_from_plugin_json,
    update_claude_md_version,
    update_plugin_json_version,
    ValidationReport
)


class TestExtractVersionFromClaudeMd:
    """Tests for extract_version_from_claude_md function."""

    def test_extract_standard_format(self, tmp_path):
        """Test extraction from standard format."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("> **Version** : 5.6.3 | **Date** : Janvier 2025\n")

        result = extract_version_from_claude_md(md_file)
        assert result == "5.6.3"

    def test_extract_simple_format(self, tmp_path):
        """Test extraction from simple format."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("Version : 1.2.3\n")

        result = extract_version_from_claude_md(md_file)
        assert result == "1.2.3"

    def test_extract_lowercase(self, tmp_path):
        """Test case-insensitive extraction."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("version : 2.0.0\n")

        result = extract_version_from_claude_md(md_file)
        assert result == "2.0.0"

    def test_file_not_found(self, tmp_path):
        """Test with non-existent file."""
        result = extract_version_from_claude_md(tmp_path / "nonexistent.md")
        assert result is None

    def test_no_version_in_file(self, tmp_path):
        """Test with file without version."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("# Some content without version\n")

        result = extract_version_from_claude_md(md_file)
        assert result is None


class TestExtractVersionFromPluginJson:
    """Tests for extract_version_from_plugin_json function."""

    def test_extract_valid_json(self, tmp_path):
        """Test extraction from valid JSON."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text(json.dumps({"version": "5.6.3", "name": "epci"}))

        result = extract_version_from_plugin_json(json_file)
        assert result == "5.6.3"

    def test_file_not_found(self, tmp_path):
        """Test with non-existent file."""
        result = extract_version_from_plugin_json(tmp_path / "nonexistent.json")
        assert result is None

    def test_invalid_json(self, tmp_path):
        """Test with invalid JSON."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text("not valid json")

        result = extract_version_from_plugin_json(json_file)
        assert result is None

    def test_missing_version_key(self, tmp_path):
        """Test with JSON missing version key."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text(json.dumps({"name": "epci"}))

        result = extract_version_from_plugin_json(json_file)
        assert result is None


class TestUpdateClaudeMdVersion:
    """Tests for update_claude_md_version function."""

    def test_update_version(self, tmp_path):
        """Test updating version."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("> **Version** : 5.6.0 | **Date** : Janvier 2025\n")

        result = update_claude_md_version(md_file, "5.6.3")

        assert result is True
        content = md_file.read_text()
        assert "5.6.3" in content
        assert "5.6.0" not in content

    def test_no_change_needed(self, tmp_path):
        """Test when version is already correct."""
        md_file = tmp_path / "CLAUDE.md"
        md_file.write_text("> **Version** : 5.6.3 | **Date** : Janvier 2025\n")

        result = update_claude_md_version(md_file, "5.6.3")

        # No change made
        assert result is False

    def test_file_not_found(self, tmp_path):
        """Test with non-existent file."""
        result = update_claude_md_version(tmp_path / "nonexistent.md", "1.0.0")
        assert result is False


class TestUpdatePluginJsonVersion:
    """Tests for update_plugin_json_version function."""

    def test_update_version(self, tmp_path):
        """Test updating version."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text(json.dumps({"version": "5.6.0", "name": "epci"}))

        result = update_plugin_json_version(json_file, "5.6.3")

        assert result is True
        data = json.loads(json_file.read_text())
        assert data["version"] == "5.6.3"

    def test_no_change_needed(self, tmp_path):
        """Test when version is already correct."""
        json_file = tmp_path / "plugin.json"
        json_file.write_text(json.dumps({"version": "5.6.3", "name": "epci"}))

        result = update_plugin_json_version(json_file, "5.6.3")

        assert result is False

    def test_file_not_found(self, tmp_path):
        """Test with non-existent file."""
        result = update_plugin_json_version(tmp_path / "nonexistent.json", "1.0.0")
        assert result is False


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_initial_state(self):
        """Test initial report state."""
        report = ValidationReport()
        assert report.valid is True
        assert report.errors == []
        assert report.checks_passed == 0

    def test_add_error(self):
        """Test adding error."""
        report = ValidationReport()
        report.add_error("Test error")

        assert report.valid is False
        assert "Test error" in report.errors

    def test_add_warning(self):
        """Test adding warning."""
        report = ValidationReport()
        report.add_warning("Test warning")

        assert report.valid is True  # Warnings don't invalidate
        assert "Test warning" in report.warnings

    def test_pass_check(self):
        """Test passing check."""
        report = ValidationReport()
        report.pass_check()

        assert report.checks_passed == 1
