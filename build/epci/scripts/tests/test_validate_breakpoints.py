#!/usr/bin/env python3
"""Tests for validate_breakpoints.py"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_breakpoints import (
    extract_breakpoint_blocks,
    parse_breakpoint_yaml,
    validate_breakpoint_block,
    BreakpointFinding,
    ValidationReport,
    VALID_BREAKPOINT_TYPES
)


class TestExtractBreakpointBlocks:
    """Tests for extract_breakpoint_blocks function."""

    def test_extract_simple_block(self):
        """Test extracting simple breakpoint block."""
        content = """Some text before
@skill:breakpoint-display
  type: analysis
  title: "Test"

Text after"""

        result = extract_breakpoint_blocks(content)

        assert len(result) == 1
        line_num, yaml_block = result[0]
        assert line_num == 2
        assert "type: analysis" in yaml_block

    def test_extract_multiple_blocks(self):
        """Test extracting multiple breakpoint blocks."""
        content = """@skill:breakpoint-display
  type: analysis
  title: "First"

Some text

@skill:breakpoint-display
  type: validation
  title: "Second"
"""

        result = extract_breakpoint_blocks(content)

        assert len(result) == 2

    def test_no_blocks(self):
        """Test content without breakpoint blocks."""
        content = "No breakpoints here."

        result = extract_breakpoint_blocks(content)

        assert len(result) == 0


class TestParseBreakpointYaml:
    """Tests for parse_breakpoint_yaml function."""

    def test_parse_valid_yaml(self):
        """Test parsing valid YAML."""
        yaml_block = """  type: analysis
  title: "Test Title"
  data:
    key: value"""

        data, error = parse_breakpoint_yaml(yaml_block)

        assert error is None
        assert data["type"] == "analysis"
        assert data["title"] == "Test Title"

    def test_parse_invalid_yaml(self):
        """Test parsing invalid YAML."""
        yaml_block = """  type: [invalid
  title: unclosed"""

        data, error = parse_breakpoint_yaml(yaml_block)

        assert data is None
        assert error is not None


class TestValidateBreakpointBlock:
    """Tests for validate_breakpoint_block function."""

    def test_valid_block(self, tmp_path):
        """Test validating valid block."""
        yaml_data = {
            "type": "analysis",
            "title": "Test Analysis"
        }
        report = ValidationReport()

        validate_breakpoint_block(yaml_data, 1, tmp_path / "test.md", report)

        assert report.valid is True
        assert len(report.findings) == 0

    def test_missing_type(self, tmp_path):
        """Test block missing type field."""
        yaml_data = {
            "title": "Test"
        }
        report = ValidationReport()

        validate_breakpoint_block(yaml_data, 1, tmp_path / "test.md", report)

        assert report.valid is False
        assert any("Missing required field: type" in str(f) for f in report.findings)

    def test_invalid_type(self, tmp_path):
        """Test block with invalid type."""
        yaml_data = {
            "type": "invalid-type",
            "title": "Test"
        }
        report = ValidationReport()

        validate_breakpoint_block(yaml_data, 1, tmp_path / "test.md", report)

        # Unknown types generate warnings, not errors
        assert any("Unknown breakpoint type" in str(f) for f in report.findings)

    def test_non_dict_data(self, tmp_path):
        """Test with non-dict yaml_data."""
        yaml_data = "just a string"
        report = ValidationReport()

        validate_breakpoint_block(yaml_data, 1, tmp_path / "test.md", report)

        assert report.valid is False

    def test_type_not_string(self, tmp_path):
        """Test type field that is not a string."""
        yaml_data = {
            "type": {"nested": "dict"},
            "title": "Test"
        }
        report = ValidationReport()

        validate_breakpoint_block(yaml_data, 1, tmp_path / "test.md", report)

        assert report.valid is False


class TestValidBreakpointTypes:
    """Tests for VALID_BREAKPOINT_TYPES."""

    def test_contains_common_types(self):
        """Test common types are included."""
        assert "analysis" in VALID_BREAKPOINT_TYPES
        assert "plan-review" in VALID_BREAKPOINT_TYPES
        assert "validation" in VALID_BREAKPOINT_TYPES
        assert "checkpoint" in VALID_BREAKPOINT_TYPES


class TestBreakpointFinding:
    """Tests for BreakpointFinding dataclass."""

    def test_str_representation(self, tmp_path):
        """Test string representation."""
        finding = BreakpointFinding(
            source_file=tmp_path / "test.md",
            line_number=42,
            issue="Missing type field",
            severity="error"
        )

        result = str(finding)

        assert "test.md" in result
        assert "42" in result
        assert "Missing type field" in result


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_initial_state(self):
        """Test initial state."""
        report = ValidationReport()
        assert report.valid is True
        assert report.breakpoints_found == 0

    def test_add_error_finding(self, tmp_path):
        """Test adding error finding."""
        report = ValidationReport()
        finding = BreakpointFinding(
            source_file=tmp_path / "test.md",
            line_number=1,
            issue="Error",
            severity="error"
        )

        report.add_finding(finding)

        assert report.valid is False

    def test_add_warning_finding(self, tmp_path):
        """Test adding warning finding."""
        report = ValidationReport()
        finding = BreakpointFinding(
            source_file=tmp_path / "test.md",
            line_number=1,
            issue="Warning",
            severity="warning"
        )

        report.add_finding(finding)

        assert report.valid is True  # Warnings don't invalidate

    def test_print_report(self, capsys):
        """Test print_report."""
        report = ValidationReport()
        report.breakpoints_found = 10
        report.pass_check()

        result = report.print_report()

        assert result == 0
