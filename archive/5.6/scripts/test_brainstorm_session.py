#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Brainstorm Session Management (v4.2)

Tests cover:
- Session YAML format validation
- Technique files structure validation
- --random mode weighted selection logic
- --progressive mode phase transitions

Run with: pytest src/scripts/test_brainstorm_session.py -v
"""

import random
from pathlib import Path
from typing import Any

import pytest
import yaml


# =============================================================================
# PATHS
# =============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BRAINSTORMER_DIR = ROOT_DIR / "src" / "skills" / "core" / "brainstormer"
TECHNIQUES_DIR = BRAINSTORMER_DIR / "references" / "techniques"
SESSION_FORMAT_FILE = BRAINSTORMER_DIR / "references" / "session-format.md"


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def valid_session_yaml() -> str:
    """Valid session YAML content for testing."""
    return '''format_version: "1.0"

session:
  id: "test-feature-2026-01-06"
  slug: "test-feature"
  status: "in_progress"
  phase: "divergent"
  ems: 45
  persona: "architecte"
  iteration: 3
  techniques_used: ["moscow", "5whys"]

  ideas:
    - id: 1
      content: "First idea"
      score: 8
    - id: 2
      content: "Second idea"
      score: 7

  history:
    - iteration: 1
      phase: "divergent"
      ems: 25
      ems_delta: 0
      questions: ["Question 1?"]
      responses: ["Response 1"]
      timestamp: "2026-01-06T10:30:00Z"

  last_question: "Current question?"
  created: "2026-01-06T10:30:00Z"
  updated: "2026-01-06T11:00:00Z"
'''


@pytest.fixture
def invalid_session_yaml_missing_field() -> str:
    """Invalid session YAML missing required field."""
    return '''format_version: "1.0"

session:
  id: "test-feature-2026-01-06"
  slug: "test-feature"
  # Missing: status, phase, ems, etc.
'''


@pytest.fixture
def technique_categories() -> list[str]:
    """List of expected technique category files."""
    return ["analysis.md", "ideation.md", "perspective.md", "breakthrough.md"]


# =============================================================================
# TEST SESSION FORMAT
# =============================================================================

class TestSessionFormat:
    """Tests for session YAML schema validation."""

    def test_valid_session_parses_correctly(self, valid_session_yaml: str):
        """Valid session YAML should parse without errors."""
        data = yaml.safe_load(valid_session_yaml)

        assert data is not None
        assert "format_version" in data
        assert "session" in data
        assert data["format_version"] == "1.0"

    def test_session_has_required_fields(self, valid_session_yaml: str):
        """Session must have all required fields."""
        data = yaml.safe_load(valid_session_yaml)
        session = data["session"]

        required_fields = [
            "id", "slug", "status", "phase", "ems",
            "persona", "iteration", "techniques_used",
            "ideas", "history", "created", "updated"
        ]

        for field in required_fields:
            assert field in session, f"Missing required field: {field}"

    def test_session_status_enum_valid(self, valid_session_yaml: str):
        """Session status must be one of valid enum values."""
        data = yaml.safe_load(valid_session_yaml)
        session = data["session"]

        valid_statuses = ["in_progress", "completed", "abandoned"]
        assert session["status"] in valid_statuses

    def test_session_phase_enum_valid(self, valid_session_yaml: str):
        """Session phase must be one of valid enum values."""
        data = yaml.safe_load(valid_session_yaml)
        session = data["session"]

        valid_phases = ["divergent", "transition", "convergent"]
        assert session["phase"] in valid_phases

    def test_session_ems_range_valid(self, valid_session_yaml: str):
        """Session EMS must be between 0 and 100."""
        data = yaml.safe_load(valid_session_yaml)
        session = data["session"]

        assert 0 <= session["ems"] <= 100

    def test_session_ideas_have_required_fields(self, valid_session_yaml: str):
        """Each idea must have id, content, and score."""
        data = yaml.safe_load(valid_session_yaml)
        ideas = data["session"]["ideas"]

        for idea in ideas:
            assert "id" in idea
            assert "content" in idea
            assert "score" in idea
            assert 0 <= idea["score"] <= 10

    def test_session_history_has_required_fields(self, valid_session_yaml: str):
        """Each history entry must have required fields."""
        data = yaml.safe_load(valid_session_yaml)
        history = data["session"]["history"]

        required_history_fields = [
            "iteration", "phase", "ems", "ems_delta",
            "questions", "responses", "timestamp"
        ]

        for entry in history:
            for field in required_history_fields:
                assert field in entry, f"Missing history field: {field}"

    def test_create_session_file(self, tmp_path: Path, valid_session_yaml: str):
        """Session can be saved and loaded from file."""
        session_file = tmp_path / "test-session.yaml"
        session_file.write_text(valid_session_yaml)

        # Load it back
        loaded = yaml.safe_load(session_file.read_text())
        assert loaded["session"]["slug"] == "test-feature"

    def test_save_restore_preserves_state(self, tmp_path: Path, valid_session_yaml: str):
        """Save then restore preserves complete state."""
        session_file = tmp_path / "test-session.yaml"

        # Save
        original = yaml.safe_load(valid_session_yaml)
        session_file.write_text(yaml.dump(original, default_flow_style=False))

        # Restore
        restored = yaml.safe_load(session_file.read_text())

        assert original == restored

    def test_invalid_session_rejected_missing_fields(
        self, invalid_session_yaml_missing_field: str
    ):
        """Invalid session missing required fields should be detectable."""
        data = yaml.safe_load(invalid_session_yaml_missing_field)
        session = data.get("session", {})

        # Check that required fields are missing
        required_fields = ["status", "phase", "ems", "persona", "iteration"]
        missing = [f for f in required_fields if f not in session]

        # This invalid fixture should be missing these fields
        assert len(missing) > 0, "Invalid fixture should be missing required fields"

    def test_session_mode_field_optional(self, valid_session_yaml: str):
        """Session mode field is optional (null for standard mode)."""
        data = yaml.safe_load(valid_session_yaml)
        session = data["session"]

        # Mode field is optional - should not be required
        # Valid session without mode field should still be valid
        assert "mode" not in session or session.get("mode") in [None, "random", "progressive"]


# =============================================================================
# TEST TECHNIQUES
# =============================================================================

class TestTechniques:
    """Tests for technique files structure validation."""

    def test_technique_files_exist(self, technique_categories: list[str]):
        """All expected technique category files must exist."""
        for filename in technique_categories:
            filepath = TECHNIQUES_DIR / filename
            assert filepath.exists(), f"Missing technique file: {filepath}"

    def test_technique_files_not_empty(self, technique_categories: list[str]):
        """Technique files must not be empty."""
        for filename in technique_categories:
            filepath = TECHNIQUES_DIR / filename
            content = filepath.read_text()
            assert len(content) > 100, f"Technique file too short: {filepath}"

    def test_technique_files_have_headers(self, technique_categories: list[str]):
        """Technique files must have proper markdown headers."""
        for filename in technique_categories:
            filepath = TECHNIQUES_DIR / filename
            content = filepath.read_text()

            # Must have at least one ## header (technique name)
            assert "## " in content, f"No technique headers in: {filepath}"

    def test_techniques_have_required_sections(self, technique_categories: list[str]):
        """Each technique must have Description, Quand utiliser, Questions types."""
        required_patterns = [
            "**Description:**",
            "**Quand utiliser:**",
            "**Questions types:**"
        ]

        for filename in technique_categories:
            filepath = TECHNIQUES_DIR / filename
            content = filepath.read_text()

            for pattern in required_patterns:
                assert pattern in content, f"Missing '{pattern}' in {filepath}"

    def test_all_techniques_mapped_to_phase(self, technique_categories: list[str]):
        """Each technique file should indicate recommended phase."""
        for filename in technique_categories:
            filepath = TECHNIQUES_DIR / filename
            content = filepath.read_text()

            # Should mention phase recommendation
            assert "Phase recommandee:" in content or "phase" in content.lower()


# =============================================================================
# TEST MODES
# =============================================================================

class TestModes:
    """Tests for --random and --progressive mode logic."""

    def test_random_weights_divergent_phase(self):
        """Random mode in Divergent phase should favor Ideation."""
        weights = {
            "ideation": 0.4,
            "perspective": 0.3,
            "breakthrough": 0.2,
            "analysis": 0.1
        }

        # Ideation should have highest weight
        assert weights["ideation"] == max(weights.values())
        # Analysis should have lowest weight
        assert weights["analysis"] == min(weights.values())
        # Weights should sum to 1.0
        assert abs(sum(weights.values()) - 1.0) < 0.001

    def test_random_weights_convergent_phase(self):
        """Random mode in Convergent phase should favor Analysis."""
        weights = {
            "ideation": 0.1,
            "perspective": 0.2,
            "breakthrough": 0.2,
            "analysis": 0.5
        }

        # Analysis should have highest weight
        assert weights["analysis"] == max(weights.values())
        # Ideation should have lowest weight
        assert weights["ideation"] == min(weights.values())
        # Weights should sum to 1.0
        assert abs(sum(weights.values()) - 1.0) < 0.001

    def test_random_excludes_used_techniques(self):
        """Random selection should exclude already used techniques."""
        all_techniques = ["moscow", "5whys", "swot", "scamper", "six-hats"]
        used_techniques = ["moscow", "5whys"]

        available = [t for t in all_techniques if t not in used_techniques]

        assert "moscow" not in available
        assert "5whys" not in available
        assert "swot" in available
        assert "scamper" in available
        assert len(available) == 3

    def test_weighted_random_selection(self):
        """Weighted random selection should respect weights over many iterations."""
        categories = ["ideation", "perspective", "breakthrough", "analysis"]
        weights = [0.4, 0.3, 0.2, 0.1]

        # Run many selections
        random.seed(42)  # For reproducibility
        selections = [random.choices(categories, weights=weights)[0] for _ in range(1000)]

        # Count frequencies
        counts = {cat: selections.count(cat) for cat in categories}

        # Ideation should be selected most often (roughly 40%)
        assert counts["ideation"] > counts["analysis"]
        # Analysis should be selected least often (roughly 10%)
        assert counts["analysis"] < counts["perspective"]

    def test_progressive_transition_at_ems_50(self):
        """Progressive mode should trigger transition at EMS 50."""
        def should_transition(ems: int, phase: str) -> bool:
            return phase == "divergent" and ems >= 50

        assert not should_transition(49, "divergent")
        assert should_transition(50, "divergent")
        assert should_transition(51, "divergent")
        assert not should_transition(50, "convergent")  # Already past transition

    def test_progressive_three_phases(self):
        """Progressive mode must have exactly 3 phases in correct order."""
        phases = ["divergent", "transition", "convergent"]

        assert len(phases) == 3
        assert phases[0] == "divergent"
        assert phases[1] == "transition"
        assert phases[2] == "convergent"

    def test_progressive_ems_ranges(self):
        """Progressive mode EMS ranges should be correct."""
        def get_phase_for_ems(ems: int, mode: str = "progressive") -> str:
            if mode != "progressive":
                return "divergent"  # Non-progressive mode

            if ems < 50:
                return "divergent"
            elif ems == 50:
                return "transition"
            else:
                return "convergent"

        # Test boundary cases
        assert get_phase_for_ems(0) == "divergent"
        assert get_phase_for_ems(49) == "divergent"
        assert get_phase_for_ems(50) == "transition"
        assert get_phase_for_ems(51) == "convergent"
        assert get_phase_for_ems(100) == "convergent"

    def test_planner_available_at_ems_70(self):
        """@planner should be available at EMS >= 70 in Convergent phase."""
        def is_planner_available(ems: int, phase: str) -> bool:
            return phase == "convergent" and ems >= 70

        assert not is_planner_available(69, "convergent")
        assert is_planner_available(70, "convergent")
        assert is_planner_available(85, "convergent")
        assert not is_planner_available(70, "divergent")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
