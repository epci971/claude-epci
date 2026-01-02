"""
Tests for MCP Auto-Activation Module (F12)

Tests persona-based activation, context triggers, and threshold behavior.
"""

import pytest
from typing import List

from ..auto_activation import (
    MCPAutoActivation,
    PersonaScore,
    ActivationResult,
)
from ..config import MCPServerConfig


class TestPersonaScore:
    """Tests for PersonaScore dataclass."""

    def test_persona_score_with_mapping(self):
        """Test PersonaScore loads MCP preferences from mapping."""
        score = PersonaScore(name="architect", score=0.72, source="auto")

        assert score.name == "architect"
        assert score.score == 0.72
        assert score.mcp_primary == "context7"
        assert score.mcp_secondary == "sequential"

    def test_persona_score_frontend(self):
        """Test frontend persona MCP preferences."""
        score = PersonaScore(name="frontend", score=0.65, source="explicit")

        assert score.mcp_primary == "magic"
        assert score.mcp_secondary == "playwright"

    def test_persona_score_unknown(self):
        """Test unknown persona has no MCP preferences."""
        score = PersonaScore(name="unknown", score=0.5, source="auto")

        assert score.mcp_primary is None
        assert score.mcp_secondary is None


class TestMCPAutoActivation:
    """Tests for MCPAutoActivation class."""

    @pytest.fixture
    def activator(self):
        """Create default activator."""
        return MCPAutoActivation()

    @pytest.fixture
    def activator_with_config(self):
        """Create activator with custom config."""
        configs = {
            "context7": MCPServerConfig(name="context7", enabled=True),
            "sequential": MCPServerConfig(name="sequential", enabled=True),
            "magic": MCPServerConfig(name="magic", enabled=False),  # Disabled
            "playwright": MCPServerConfig(name="playwright", enabled=True),
        }
        return MCPAutoActivation(mcp_configs=configs)

    # Tests for activate_for_personas

    def test_activate_architect_persona(self, activator):
        """Test architect persona activates context7 and sequential."""
        personas = [PersonaScore(name="architect", score=0.72, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "context7" in result.auto_activate
        assert "sequential" in result.auto_activate
        assert result.sources["context7"] == "persona:architect"

    def test_activate_frontend_persona(self, activator):
        """Test frontend persona activates magic and playwright."""
        personas = [PersonaScore(name="frontend", score=0.65, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "magic" in result.auto_activate
        assert "playwright" in result.auto_activate

    def test_activate_security_persona(self, activator):
        """Test security persona activates only sequential."""
        personas = [PersonaScore(name="security", score=0.70, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "sequential" in result.auto_activate
        assert "context7" not in result.auto_activate
        assert "magic" not in result.auto_activate

    def test_activate_qa_persona(self, activator):
        """Test QA persona activates only playwright."""
        personas = [PersonaScore(name="qa", score=0.68, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "playwright" in result.auto_activate
        assert "context7" not in result.auto_activate
        assert "sequential" not in result.auto_activate

    # Tests for threshold behavior

    def test_threshold_auto_activate(self, activator):
        """Test score > 0.6 triggers auto-activation."""
        personas = [PersonaScore(name="backend", score=0.61, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "context7" in result.auto_activate
        assert "sequential" in result.auto_activate

    def test_threshold_suggest(self, activator):
        """Test score 0.4-0.6 triggers suggestion."""
        personas = [PersonaScore(name="backend", score=0.55, source="auto")]
        result = activator.activate_for_personas(personas)

        assert "context7" in result.suggested
        assert "context7" not in result.auto_activate

    def test_threshold_no_action(self, activator):
        """Test score < 0.4 triggers no action."""
        personas = [PersonaScore(name="backend", score=0.35, source="auto")]
        result = activator.activate_for_personas(personas)

        assert len(result.auto_activate) == 0
        assert len(result.suggested) == 0

    # Tests for disabled MCP

    def test_disabled_mcp_not_activated(self, activator_with_config):
        """Test disabled MCP is not activated even with high score."""
        personas = [PersonaScore(name="frontend", score=0.72, source="auto")]
        result = activator_with_config.activate_for_personas(personas)

        # magic is disabled in config
        assert "magic" not in result.auto_activate
        assert "playwright" in result.auto_activate

    # Tests for multiple personas

    def test_multiple_personas(self, activator):
        """Test multiple personas combine their MCPs."""
        personas = [
            PersonaScore(name="backend", score=0.65, source="auto"),
            PersonaScore(name="security", score=0.61, source="auto"),
        ]
        result = activator.activate_for_personas(personas)

        # Backend: context7, sequential
        # Security: sequential
        assert "context7" in result.auto_activate
        assert "sequential" in result.auto_activate

    # Tests for context-based activation

    def test_keyword_triggers_context7(self, activator):
        """Test import keywords trigger context7."""
        result = activator.activate_for_context(
            brief_text="We need to import the react library for this component"
        )

        assert "context7" in result.auto_activate

    def test_keyword_triggers_sequential(self, activator):
        """Test debug keywords trigger sequential."""
        result = activator.activate_for_context(
            brief_text="We need to analyze and investigate this complex issue"
        )

        assert "sequential" in result.auto_activate

    def test_flag_triggers_sequential(self, activator):
        """Test --think-hard flag triggers sequential."""
        result = activator.activate_for_context(
            flags=["--think-hard"]
        )

        assert "sequential" in result.auto_activate
        assert result.sources["sequential"] == "flags"

    def test_file_triggers_magic(self, activator):
        """Test .tsx files trigger magic."""
        result = activator.activate_for_context(
            file_paths=["src/components/Button.tsx", "src/App.tsx"]
        )

        assert "magic" in result.auto_activate
        assert result.sources["magic"] == "files"

    def test_file_triggers_playwright(self, activator):
        """Test .spec.ts files trigger playwright."""
        result = activator.activate_for_context(
            file_paths=["tests/e2e/login.spec.ts"]
        )

        assert "playwright" in result.auto_activate

    # Tests for combined activation

    def test_combined_activation(self, activator):
        """Test combined persona and context activation."""
        personas = [PersonaScore(name="architect", score=0.65, source="auto")]
        result = activator.activate_combined(
            personas=personas,
            brief_text="Add component UI",
            flags=["--think-hard"],
        )

        # From architect: context7, sequential
        # From --think-hard: sequential
        # From "component": magic (if score high enough)
        assert "context7" in result.auto_activate
        assert "sequential" in result.auto_activate

    # Tests for display formatting

    def test_format_for_display(self, activator):
        """Test display formatting for FLAGS line."""
        result = ActivationResult()
        result.add_auto("context7", "persona:architect", 0.72)
        result.add_auto("sequential", "flags", 1.0)
        result.add_suggested("magic", "keywords", 0.45)

        display = activator.format_for_display(result)

        assert "--c7" in display or "--con" in display
        assert "--seq" in display
        assert "suggested" in display


class TestActivationResult:
    """Tests for ActivationResult dataclass."""

    def test_add_auto(self):
        """Test adding auto-activate MCP."""
        result = ActivationResult()
        result.add_auto("context7", "persona:architect", 0.72)

        assert "context7" in result.auto_activate
        assert result.sources["context7"] == "persona:architect"
        assert result.scores["context7"] == 0.72

    def test_add_suggested(self):
        """Test adding suggested MCP."""
        result = ActivationResult()
        result.add_suggested("magic", "keywords", 0.45)

        assert "magic" in result.suggested
        assert "magic" not in result.auto_activate

    def test_auto_takes_precedence(self):
        """Test auto-activate takes precedence over suggested."""
        result = ActivationResult()
        result.add_auto("context7", "persona:architect", 0.72)
        result.add_suggested("context7", "keywords", 0.45)

        # Should still be in auto, not suggested
        assert "context7" in result.auto_activate
        assert "context7" not in result.suggested

    def test_higher_score_wins(self):
        """Test higher score overwrites lower."""
        result = ActivationResult()
        result.add_auto("context7", "keywords", 0.5)
        result.add_auto("context7", "persona:architect", 0.72)

        assert result.scores["context7"] == 0.72
