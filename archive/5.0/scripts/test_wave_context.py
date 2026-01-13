"""
Tests for Wave Context Module (F11)

Tests WaveContext, Wave, Issue, Decision dataclasses
and context accumulation functionality.
"""

import pytest
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.wave_context import (
    WaveContext,
    Wave,
    WaveStatus,
    Issue,
    Decision,
    TaskResult,
)


class TestWaveStatus:
    """Tests for WaveStatus enum."""

    def test_all_statuses_exist(self):
        assert WaveStatus.PENDING.value == "pending"
        assert WaveStatus.IN_PROGRESS.value == "in_progress"
        assert WaveStatus.COMPLETED.value == "completed"
        assert WaveStatus.FAILED.value == "failed"
        assert WaveStatus.SKIPPED.value == "skipped"


class TestIssue:
    """Tests for Issue dataclass."""

    def test_create_issue(self):
        issue = Issue(
            severity="critical",
            message="Test failure",
            file_path="src/test.py",
            line_number=42,
            source="test_runner",
        )
        assert issue.severity == "critical"
        assert issue.message == "Test failure"
        assert issue.file_path == "src/test.py"
        assert issue.line_number == 42
        assert issue.source == "test_runner"

    def test_issue_to_dict(self):
        issue = Issue(severity="minor", message="Warning")
        d = issue.to_dict()
        assert d["severity"] == "minor"
        assert d["message"] == "Warning"
        assert d["file_path"] is None


class TestDecision:
    """Tests for Decision dataclass."""

    def test_create_decision(self):
        decision = Decision(
            description="Use Repository pattern",
            rationale="Better separation of concerns",
            wave_number=1,
        )
        assert decision.description == "Use Repository pattern"
        assert decision.rationale == "Better separation of concerns"
        assert decision.wave_number == 1
        assert isinstance(decision.timestamp, datetime)

    def test_decision_to_dict(self):
        decision = Decision(
            description="Test",
            rationale="Test rationale",
            wave_number=2,
        )
        d = decision.to_dict()
        assert d["description"] == "Test"
        assert d["wave_number"] == 2
        assert "timestamp" in d


class TestTaskResult:
    """Tests for TaskResult dataclass."""

    def test_create_task_result(self):
        result = TaskResult(
            task_name="create_entity",
            status="completed",
            duration_seconds=5.0,
            files_created=["src/entity.py"],
        )
        assert result.task_name == "create_entity"
        assert result.status == "completed"
        assert result.duration_seconds == 5.0
        assert "src/entity.py" in result.files_created

    def test_failed_task_result(self):
        result = TaskResult(
            task_name="failing_task",
            status="failed",
            error="Import error",
        )
        assert result.status == "failed"
        assert result.error == "Import error"


class TestWave:
    """Tests for Wave dataclass."""

    def test_create_wave(self):
        wave = Wave(
            wave_id="foundations",
            name="Foundations",
            order=1,
            tasks=["task1", "task2"],
        )
        assert wave.wave_id == "foundations"
        assert wave.name == "Foundations"
        assert wave.order == 1
        assert len(wave.tasks) == 2
        assert wave.status == WaveStatus.PENDING

    def test_wave_is_complete(self):
        wave = Wave(wave_id="test", name="Test", order=1)
        assert not wave.is_complete

        wave.status = WaveStatus.COMPLETED
        assert wave.is_complete

    def test_wave_is_failed(self):
        wave = Wave(wave_id="test", name="Test", order=1)
        assert not wave.is_failed

        wave.status = WaveStatus.FAILED
        assert wave.is_failed

    def test_wave_duration(self):
        wave = Wave(wave_id="test", name="Test", order=1)
        wave.started_at = datetime(2025, 1, 1, 10, 0, 0)
        wave.completed_at = datetime(2025, 1, 1, 10, 5, 0)

        assert wave.duration_seconds == 300.0  # 5 minutes

    def test_wave_to_dict(self):
        wave = Wave(
            wave_id="test",
            name="Test Wave",
            order=1,
            tasks=["task1"],
        )
        d = wave.to_dict()
        assert d["wave_id"] == "test"
        assert d["name"] == "Test Wave"
        assert d["status"] == "pending"


class TestWaveContext:
    """Tests for WaveContext dataclass."""

    def test_create_context(self):
        context = WaveContext(
            wave_number=1,
            feature_slug="test-feature",
            complexity="LARGE",
        )
        assert context.wave_number == 1
        assert context.feature_slug == "test-feature"
        assert context.complexity == "LARGE"
        assert context.files_created == []
        assert context.files_modified == []

    def test_add_file_created(self):
        context = WaveContext()
        context.add_file_created("src/entity.py")
        context.add_file_created("src/service.py")
        context.add_file_created("src/entity.py")  # Duplicate

        assert len(context.files_created) == 2
        assert "src/entity.py" in context.files_created
        assert "src/service.py" in context.files_created

    def test_add_file_modified(self):
        context = WaveContext()
        context.add_file_modified("src/config.py")

        assert len(context.files_modified) == 1
        assert "src/config.py" in context.files_modified

    def test_add_pattern(self):
        context = WaveContext()
        context.add_pattern("Repository")
        context.add_pattern("Service Layer")
        context.add_pattern("Repository")  # Duplicate

        assert len(context.patterns_used) == 2

    def test_add_issue(self):
        context = WaveContext()
        issue = Issue(severity="critical", message="Test error")
        context.add_issue(issue)

        assert len(context.issues_found) == 1
        assert context.issues_found[0].severity == "critical"

    def test_add_decision(self):
        context = WaveContext(wave_number=1)
        context.add_decision("Use DDD", "Better domain modeling")

        assert len(context.decisions_made) == 1
        assert context.decisions_made[0].description == "Use DDD"
        assert context.decisions_made[0].wave_number == 1

    def test_get_critical_issues(self):
        context = WaveContext()
        context.add_issue(Issue(severity="critical", message="Critical"))
        context.add_issue(Issue(severity="minor", message="Minor"))
        context.add_issue(Issue(severity="critical", message="Another critical"))

        critical = context.get_critical_issues()
        assert len(critical) == 2

    def test_get_important_issues(self):
        context = WaveContext()
        context.add_issue(Issue(severity="important", message="Important"))
        context.add_issue(Issue(severity="minor", message="Minor"))

        important = context.get_important_issues()
        assert len(important) == 1

    def test_advance_wave(self):
        context = WaveContext(
            wave_number=1,
            feature_slug="test",
            files_created=["file1.py"],
            patterns_used=["Pattern1"],
        )
        context.add_decision("Decision 1", "Rationale")

        new_context = context.advance_wave()

        assert new_context.wave_number == 2
        assert new_context.feature_slug == "test"
        assert "file1.py" in new_context.files_created
        assert "Pattern1" in new_context.patterns_used
        assert len(new_context.decisions_made) == 1

        # Verify independence
        new_context.add_file_created("file2.py")
        assert "file2.py" not in context.files_created

    def test_to_dict(self):
        context = WaveContext(
            wave_number=1,
            feature_slug="test-feature",
            complexity="STANDARD",
        )
        context.add_file_created("test.py")

        d = context.to_dict()
        assert d["wave_number"] == 1
        assert d["feature_slug"] == "test-feature"
        assert "test.py" in d["files_created"]

    def test_from_dict(self):
        data = {
            "wave_number": 2,
            "feature_slug": "restored-feature",
            "files_created": ["file1.py", "file2.py"],
            "files_modified": [],
            "patterns_used": ["Pattern"],
            "tests_status": {"test1": "passed"},
            "issues_found": [{"severity": "minor", "message": "Warning"}],
            "decisions_made": [
                {"description": "Dec", "rationale": "Rat", "wave_number": 1}
            ],
            "agent_results": {},
            "complexity": "LARGE",
        }

        context = WaveContext.from_dict(data)

        assert context.wave_number == 2
        assert context.feature_slug == "restored-feature"
        assert len(context.files_created) == 2
        assert len(context.issues_found) == 1
        assert len(context.decisions_made) == 1

    def test_summary(self):
        context = WaveContext(wave_number=1)
        context.add_file_created("file.py")
        context.update_test_status("test1", "passed")
        context.add_issue(Issue(severity="critical", message="Error"))

        summary = context.summary()

        assert "Wave 1 Context" in summary
        assert "Files created: 1" in summary
        assert "1 critical" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
