#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Pattern Detector (F06)

Tests the code pattern detection for security, performance, and quality issues.
"""

import pytest
import sys
import tempfile
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from detector import PatternDetector, PatternFinding


class TestPatternFinding:
    """Test PatternFinding dataclass."""

    def test_finding_creation(self):
        """Finding should be created with required fields."""
        finding = PatternFinding(
            pattern_id="sql-injection",
            file_path="src/Repository.php",
            line_number=42,
            message="SQL injection detected",
            severity="critical",
        )

        assert finding.pattern_id == "sql-injection"
        assert finding.line_number == 42
        assert finding.severity == "critical"

    def test_finding_defaults(self):
        """Finding should have sensible defaults."""
        finding = PatternFinding(
            pattern_id="test",
            file_path="test.php",
        )

        assert finding.severity == "minor"
        assert finding.source == "detector"
        assert finding.context == {}


class TestPatternDetectorInit:
    """Test PatternDetector initialization."""

    def test_detector_creation(self):
        """Detector should be created with project root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            detector = PatternDetector(Path(tmpdir))
            assert detector.project_root == Path(tmpdir)


class TestSecurityPatternDetection:
    """Test security pattern detection."""

    def test_detect_php_get_superglobal(self):
        """Should detect $_GET usage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.php"
            test_file.write_text('''<?php
$user = $_GET['user'];
echo $user;
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_security(test_file, test_file.read_text())

            assert len(findings) >= 1
            assert any(f.pattern_id == "input-not-validated" for f in findings)

    def test_detect_sql_string_concat(self):
        """Should detect SQL string concatenation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "repo.php"
            test_file.write_text('''<?php
$query = "SELECT * FROM users WHERE id = " + $id;
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_security(test_file, test_file.read_text())

            assert any(f.pattern_id == "sql-injection" for f in findings)

    def test_detect_twig_raw_filter(self):
        """Should detect Twig raw filter (XSS risk)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "template.html.twig"
            test_file.write_text('''
<div>{{ user_content|raw }}</div>
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_security(test_file, test_file.read_text())

            assert any(f.pattern_id == "xss-vulnerability" for f in findings)

    def test_detect_react_dangerous_html(self):
        """Should detect React dangerouslySetInnerHTML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "Component.tsx"
            test_file.write_text('''
function MyComponent({ html }) {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_security(test_file, test_file.read_text())

            assert any(f.pattern_id == "xss-vulnerability" for f in findings)


class TestPerformancePatternDetection:
    """Test performance pattern detection."""

    def test_detect_find_all(self):
        """Should detect findAll() without pagination."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "Service.php"
            test_file.write_text('''<?php
$users = $this->userRepository->findAll();
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_performance(test_file, test_file.read_text())

            assert any(f.pattern_id == "large-payload" for f in findings)

    def test_detect_select_star_without_limit(self):
        """Should detect SELECT * without LIMIT."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "query.py"
            test_file.write_text('''
query = "SELECT * FROM users"
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_performance(test_file, test_file.read_text())

            assert any(f.pattern_id == "large-payload" for f in findings)


class TestQualityPatternDetection:
    """Test quality pattern detection."""

    def test_detect_god_class(self):
        """Should detect class with >500 lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "GodClass.php"
            # Create a file with 600 lines and one class
            content = '''<?php
class GodClass {
''' + '\n'.join([f'    public function method{i}() {{ return {i}; }}' for i in range(600)]) + '''
}
'''
            test_file.write_text(content)

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_quality(test_file, test_file.read_text())

            assert any(f.pattern_id == "god-class" for f in findings)

    def test_detect_long_method(self):
        """Should detect method with >50 lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "Service.php"
            # Create a method with 60 lines
            content = '''<?php
class Service {
    public function longMethod() {
''' + '\n'.join([f'        $x{i} = {i};' for i in range(60)]) + '''
    }
}
'''
            test_file.write_text(content)

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_quality(test_file, test_file.read_text())

            assert any(f.pattern_id == "long-method" for f in findings)

    def test_detect_magic_numbers(self):
        """Should detect magic numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "calc.py"
            test_file.write_text('''
def calculate(x):
    return x * 42 + 1337
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_quality(test_file, test_file.read_text())

            magic_findings = [f for f in findings if f.pattern_id == "magic-numbers"]
            assert len(magic_findings) >= 1

    def test_skip_http_status_codes(self):
        """Should not flag HTTP status codes as magic numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "api.py"
            test_file.write_text('''
def handle():
    if error:
        return response(status=404)
    return response(status=200)
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector._detect_quality(test_file, test_file.read_text())

            # Should not flag 404 or 200
            magic_findings = [f for f in findings if f.pattern_id == "magic-numbers"]
            assert all("404" not in f.message and "200" not in f.message for f in magic_findings)


class TestDetectAll:
    """Test detect_all integration."""

    def test_detect_all_runs_all_detectors(self):
        """Should run security, performance, and quality detectors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with multiple issues
            test_file = Path(tmpdir) / "problematic.php"
            test_file.write_text('''<?php
class Service {
    public function process() {
        $user = $_GET['user'];  // Security issue
        $all = $this->repo->findAll();  // Performance issue
        $magic = 42 * 1337;  // Quality issue
    }
}
''')

            detector = PatternDetector(Path(tmpdir))
            findings = detector.detect_all([test_file])

            pattern_ids = {f.pattern_id for f in findings}
            assert "input-not-validated" in pattern_ids
            assert "large-payload" in pattern_ids
            assert "magic-numbers" in pattern_ids


class TestSubagentIntegration:
    """Test subagent findings conversion."""

    def test_convert_code_reviewer_findings(self):
        """Should convert code-reviewer findings."""
        data = [
            {
                'type': 'long-method',
                'file': 'src/Service.php',
                'line': 100,
                'message': 'Method is too long',
                'severity': 'minor',
            }
        ]

        findings = PatternDetector.from_subagent_findings("code-reviewer", data)

        assert len(findings) == 1
        assert findings[0].pattern_id == "long-method"
        assert findings[0].source == "code-reviewer"

    def test_convert_security_auditor_findings(self):
        """Should convert security-auditor findings."""
        data = [
            {
                'pattern_id': 'sql-injection',
                'file_path': 'src/Repository.php',
                'line_number': 50,
                'description': 'SQL injection vulnerability',
                'severity': 'critical',
            }
        ]

        findings = PatternDetector.from_subagent_findings("security-auditor", data)

        assert len(findings) == 1
        assert findings[0].pattern_id == "sql-injection"
        assert findings[0].severity == "critical"

    def test_handle_missing_fields(self):
        """Should handle findings with missing optional fields."""
        data = [
            {'id': 'custom-issue'}
        ]

        findings = PatternDetector.from_subagent_findings("qa-reviewer", data)

        assert len(findings) == 1
        assert findings[0].pattern_id == "custom-issue"
        assert findings[0].file_path == ""
        assert findings[0].line_number is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
