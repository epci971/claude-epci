#!/usr/bin/env python3
"""Tests for validate_markdown_refs.py"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_markdown_refs import (
    extract_markdown_links,
    is_external_link,
    is_anchor_link,
    is_template_link,
    resolve_link_path,
    RefFinding,
    ValidationReport
)


class TestExtractMarkdownLinks:
    """Tests for extract_markdown_links function."""

    def test_extract_simple_link(self):
        """Test extracting simple link."""
        content = "See [README](README.md) for details."

        result = extract_markdown_links(content)

        assert len(result) == 1
        line_num, text, path = result[0]
        assert line_num == 1
        assert text == "README"
        assert path == "README.md"

    def test_extract_multiple_links(self):
        """Test extracting multiple links."""
        content = """[Link 1](path1.md)
[Link 2](path2.md)
[Link 3](path3.md)"""

        result = extract_markdown_links(content)

        assert len(result) == 3

    def test_extract_link_with_anchor(self):
        """Test extracting link with anchor."""
        content = "[Section](file.md#section)"

        result = extract_markdown_links(content)

        assert len(result) == 1
        _, _, path = result[0]
        assert path == "file.md#section"

    def test_no_links(self):
        """Test content without links."""
        content = "No links here."

        result = extract_markdown_links(content)

        assert len(result) == 0


class TestIsExternalLink:
    """Tests for is_external_link function."""

    def test_http_link(self):
        """Test HTTP link."""
        assert is_external_link("http://example.com") is True

    def test_https_link(self):
        """Test HTTPS link."""
        assert is_external_link("https://example.com") is True

    def test_mailto_link(self):
        """Test mailto link."""
        assert is_external_link("mailto:test@example.com") is True

    def test_local_link(self):
        """Test local link."""
        assert is_external_link("./path/to/file.md") is False
        assert is_external_link("file.md") is False


class TestIsAnchorLink:
    """Tests for is_anchor_link function."""

    def test_anchor_link(self):
        """Test anchor link."""
        assert is_anchor_link("#section") is True
        assert is_anchor_link("#heading-with-dashes") is True

    def test_not_anchor_link(self):
        """Test non-anchor link."""
        assert is_anchor_link("file.md#section") is False
        assert is_anchor_link("file.md") is False


class TestIsTemplateLink:
    """Tests for is_template_link function."""

    def test_template_with_braces(self):
        """Test template with ${...}."""
        assert is_template_link("${PLUGIN_ROOT}/path") is True

    def test_template_with_double_braces(self):
        """Test template with {{...}}."""
        assert is_template_link("{{variable}}/path") is True

    def test_template_with_angle_brackets(self):
        """Test template with <...>."""
        assert is_template_link("<placeholder>/path") is True

    def test_not_template(self):
        """Test non-template link."""
        assert is_template_link("regular/path.md") is False


class TestResolveLinkPath:
    """Tests for resolve_link_path function."""

    def test_absolute_path(self, tmp_path):
        """Test absolute path resolution."""
        source = tmp_path / "src" / "file.md"

        result = resolve_link_path("/docs/readme.md", source, tmp_path)

        assert result == tmp_path / "docs" / "readme.md"

    def test_relative_path(self, tmp_path):
        """Test relative path resolution."""
        source = tmp_path / "src" / "commands" / "file.md"
        source.parent.mkdir(parents=True)

        result = resolve_link_path("../skills/test.md", source, tmp_path)

        expected = (source.parent / "../skills/test.md").resolve()
        assert result == expected

    def test_anchor_stripped(self, tmp_path):
        """Test anchor is stripped."""
        source = tmp_path / "file.md"

        result = resolve_link_path("other.md#section", source, tmp_path)

        # Should resolve without the anchor
        assert "#section" not in str(result)

    def test_empty_after_anchor(self, tmp_path):
        """Test link that is only anchor."""
        source = tmp_path / "file.md"

        result = resolve_link_path("#section", source, tmp_path)

        assert result is None


class TestRefFinding:
    """Tests for RefFinding dataclass."""

    def test_str_representation(self, tmp_path):
        """Test string representation."""
        finding = RefFinding(
            source_file=tmp_path / "test.md",
            line_number=42,
            link_text="broken link",
            link_path="./missing.md",
            issue="File not found"
        )

        result = str(finding)

        assert "test.md" in result
        assert "42" in result
        assert "broken link" in result
        assert "./missing.md" in result


class TestValidationReport:
    """Tests for ValidationReport dataclass."""

    def test_initial_state(self):
        """Test initial state."""
        report = ValidationReport()
        assert report.valid is True
        assert report.files_scanned == 0
        assert report.refs_checked == 0

    def test_add_finding(self, tmp_path):
        """Test adding finding."""
        report = ValidationReport()
        finding = RefFinding(
            source_file=tmp_path / "test.md",
            line_number=1,
            link_text="text",
            link_path="path.md",
            issue="File not found"
        )

        report.add_finding(finding)

        # Findings are warnings, don't invalidate
        assert report.valid is True
        assert len(report.findings) == 1

    def test_print_report(self, capsys):
        """Test print_report."""
        report = ValidationReport()
        report.files_scanned = 100
        report.refs_checked = 500
        report.pass_check()

        result = report.print_report()

        assert result == 0


class TestIntegration:
    """Integration tests for markdown ref validation."""

    def test_validate_existing_file(self, tmp_path):
        """Test validation with existing referenced file."""
        # Create source file
        source = tmp_path / "source.md"
        source.write_text("[Target](target.md)")

        # Create target file
        target = tmp_path / "target.md"
        target.write_text("# Target")

        # Extract and check
        links = extract_markdown_links(source.read_text())
        _, _, path = links[0]

        resolved = resolve_link_path(path, source, tmp_path)
        assert resolved.exists()

    def test_validate_missing_file(self, tmp_path):
        """Test validation with missing referenced file."""
        source = tmp_path / "source.md"
        source.write_text("[Missing](missing.md)")

        links = extract_markdown_links(source.read_text())
        _, _, path = links[0]

        resolved = resolve_link_path(path, source, tmp_path)
        assert not resolved.exists()
