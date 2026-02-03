"""Tests for PRD Schema v2 validation.

Tests the updated prd-v2.json schema with userStories[] format,
execution tracking, and status fields for Ralph integration.
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "prd-v2.json"


@pytest.fixture
def schema():
    """Load the PRD v2 schema."""
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture
def minimal_valid_userstory():
    """Minimal valid userStory object."""
    return {
        "id": "US1",
        "title": "Test Story",
        "category": "core",
        "type": "feature",
        "complexity": "M",
        "priority": "must-have",
        "status": "pending",
        "passes": False,
        "acceptanceCriteria": [],
        "tasks": [],
        "dependencies": {"depends_on": [], "blocks": []},
        "execution": {
            "attempts": 0,
            "last_error": None,
            "files_modified": [],
            "completed_at": None,
            "iteration": 0,
        },
    }


@pytest.fixture
def minimal_valid_prd(minimal_valid_userstory):
    """Minimal valid PRD document."""
    return {
        "title": "Test PRD",
        "version": "2.0",
        "userStories": [minimal_valid_userstory],
        "meta": {
            "branchName": "feature/test",
            "projectName": "Test Project",
            "generatedAt": "2026-02-02T12:00:00Z",
            "generatedBy": "test",
            "source": "test",
        },
        "config": {
            "max_iterations": 50,
            "test_command": "pytest",
            "lint_command": "flake8",
            "granularity": "standard",
        },
        "metrics": {"total_stories": 1, "completed": 0, "critical_path": ["US1"]},
    }


class TestSchemaStructure:
    """Test AC1: Schema uses userStories[] as main array."""

    def test_userstories_is_required(self, schema, minimal_valid_prd):
        """userStories must be present."""
        del minimal_valid_prd["userStories"]
        with pytest.raises(ValidationError) as exc:
            validate(minimal_valid_prd, schema)
        assert "userStories" in str(exc.value)

    def test_userstories_accepts_array(self, schema, minimal_valid_prd):
        """userStories accepts array of story objects."""
        validate(minimal_valid_prd, schema)

    def test_meta_is_required(self, schema, minimal_valid_prd):
        """meta object must be present."""
        del minimal_valid_prd["meta"]
        with pytest.raises(ValidationError) as exc:
            validate(minimal_valid_prd, schema)
        assert "meta" in str(exc.value)

    def test_config_is_required(self, schema, minimal_valid_prd):
        """config object must be present."""
        del minimal_valid_prd["config"]
        with pytest.raises(ValidationError) as exc:
            validate(minimal_valid_prd, schema)
        assert "config" in str(exc.value)

    def test_metrics_is_required(self, schema, minimal_valid_prd):
        """metrics object must be present."""
        del minimal_valid_prd["metrics"]
        with pytest.raises(ValidationError) as exc:
            validate(minimal_valid_prd, schema)
        assert "metrics" in str(exc.value)


class TestExecutionTracking:
    """Test AC2: execution object with tracking fields."""

    def test_execution_attempts_is_integer(self, schema, minimal_valid_prd):
        """execution.attempts must be integer."""
        minimal_valid_prd["userStories"][0]["execution"]["attempts"] = "not-int"
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)

    def test_execution_files_modified_is_array(self, schema, minimal_valid_prd):
        """execution.files_modified must be array of strings."""
        minimal_valid_prd["userStories"][0]["execution"]["files_modified"] = "not-array"
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)

    def test_execution_last_error_nullable(self, schema, minimal_valid_prd):
        """execution.last_error can be null or string."""
        minimal_valid_prd["userStories"][0]["execution"]["last_error"] = None
        validate(minimal_valid_prd, schema)
        minimal_valid_prd["userStories"][0]["execution"]["last_error"] = "Error message"
        validate(minimal_valid_prd, schema)

    def test_execution_completed_at_nullable(self, schema, minimal_valid_prd):
        """execution.completed_at can be null or ISO-8601 string."""
        minimal_valid_prd["userStories"][0]["execution"]["completed_at"] = None
        validate(minimal_valid_prd, schema)
        minimal_valid_prd["userStories"][0]["execution"]["completed_at"] = "2026-02-02T12:00:00Z"
        validate(minimal_valid_prd, schema)

    def test_execution_iteration_is_integer(self, schema, minimal_valid_prd):
        """execution.iteration must be integer."""
        minimal_valid_prd["userStories"][0]["execution"]["iteration"] = "not-int"
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)


class TestStatusTracking:
    """Test AC3: status enum and passes boolean."""

    def test_status_valid_enum_values(self, schema, minimal_valid_prd):
        """status must be valid enum value."""
        for status in ["pending", "in_progress", "completed", "failed", "blocked"]:
            minimal_valid_prd["userStories"][0]["status"] = status
            validate(minimal_valid_prd, schema)

    def test_status_invalid_value_fails(self, schema, minimal_valid_prd):
        """Invalid status value should fail."""
        minimal_valid_prd["userStories"][0]["status"] = "invalid"
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)

    def test_passes_is_boolean(self, schema, minimal_valid_prd):
        """passes must be boolean."""
        minimal_valid_prd["userStories"][0]["passes"] = "not-bool"
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)

    def test_passes_accepts_true_false(self, schema, minimal_valid_prd):
        """passes accepts true and false."""
        for val in [True, False]:
            minimal_valid_prd["userStories"][0]["passes"] = val
            validate(minimal_valid_prd, schema)


class TestDoneFlags:
    """Test AC4: done boolean on acceptanceCriteria and tasks."""

    def test_acceptance_criteria_done_field(self, schema, minimal_valid_prd):
        """acceptanceCriteria items must have done boolean."""
        minimal_valid_prd["userStories"][0]["acceptanceCriteria"] = [
            {"id": "AC1", "description": "Test AC", "done": False}
        ]
        validate(minimal_valid_prd, schema)

    def test_acceptance_criteria_done_required(self, schema, minimal_valid_prd):
        """acceptanceCriteria.done is required."""
        minimal_valid_prd["userStories"][0]["acceptanceCriteria"] = [
            {"id": "AC1", "description": "Test AC"}
        ]
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)

    def test_task_done_field(self, schema, minimal_valid_prd):
        """task items must have done boolean."""
        minimal_valid_prd["userStories"][0]["tasks"] = [
            {"id": "T1", "description": "Test task", "done": False}
        ]
        validate(minimal_valid_prd, schema)

    def test_task_done_required(self, schema, minimal_valid_prd):
        """task.done is required."""
        minimal_valid_prd["userStories"][0]["tasks"] = [
            {"id": "T1", "description": "Test task"}
        ]
        with pytest.raises(ValidationError):
            validate(minimal_valid_prd, schema)


class TestCompleteValidation:
    """Test complete PRD validation."""

    def test_complete_valid_prd(self, schema, minimal_valid_prd):
        """Complete valid PRD should validate successfully."""
        minimal_valid_prd["userStories"][0]["acceptanceCriteria"] = [
            {"id": "AC1", "description": "First AC", "done": False},
            {"id": "AC2", "description": "Second AC", "done": True},
        ]
        minimal_valid_prd["userStories"][0]["tasks"] = [
            {"id": "T1", "description": "Task 1", "done": True},
        ]
        validate(minimal_valid_prd, schema)

    def test_schema_is_valid_json_schema(self, schema):
        """Verify schema itself is valid JSON Schema."""
        Draft202012Validator.check_schema(schema)
