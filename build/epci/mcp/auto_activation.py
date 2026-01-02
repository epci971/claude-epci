"""
MCP Auto-Activation Module (F12)

Implements auto-activation logic for MCP servers based on:
- F09 persona scoring and preferences
- Keyword triggers in brief content
- File pattern triggers
- Flag triggers
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .activation_matrix import (
    PERSONA_MCP_MAPPING,
    get_auto_activated_mcps,
    get_suggested_mcps,
    check_keyword_triggers,
    check_file_triggers,
    check_flag_triggers,
)
from .config import MCPContext, MCPServerConfig


@dataclass
class PersonaScore:
    """Score for a persona with MCP preferences."""
    name: str
    score: float
    source: str  # "auto", "explicit"
    mcp_primary: Optional[str] = None
    mcp_secondary: Optional[str] = None

    def __post_init__(self):
        if self.name in PERSONA_MCP_MAPPING:
            primary, secondary = PERSONA_MCP_MAPPING[self.name]
            self.mcp_primary = primary
            self.mcp_secondary = secondary


@dataclass
class ActivationResult:
    """Result of MCP auto-activation analysis."""
    auto_activate: List[str] = field(default_factory=list)
    suggested: List[str] = field(default_factory=list)
    sources: Dict[str, str] = field(default_factory=dict)
    scores: Dict[str, float] = field(default_factory=dict)

    def add_auto(self, mcp_name: str, source: str, score: float = 1.0) -> None:
        """Add an MCP to auto-activate list."""
        if mcp_name not in self.auto_activate:
            self.auto_activate.append(mcp_name)
        self.sources[mcp_name] = source
        self.scores[mcp_name] = max(self.scores.get(mcp_name, 0), score)

    def add_suggested(self, mcp_name: str, source: str, score: float = 0.5) -> None:
        """Add an MCP to suggested list (if not already auto)."""
        if mcp_name not in self.auto_activate and mcp_name not in self.suggested:
            self.suggested.append(mcp_name)
        if mcp_name not in self.sources:
            self.sources[mcp_name] = source
            self.scores[mcp_name] = score


class MCPAutoActivation:
    """
    Handles automatic activation of MCP servers based on context.

    Uses F09 persona scoring algorithm adapted for MCP activation:
    - Score > 0.6: Auto-activate
    - Score 0.4-0.6: Suggest
    - Score < 0.4: No activation
    """

    # Thresholds matching F09 persona system
    AUTO_THRESHOLD = 0.6
    SUGGEST_THRESHOLD = 0.4

    def __init__(self, mcp_configs: Optional[Dict[str, MCPServerConfig]] = None):
        """
        Initialize auto-activation handler.

        Args:
            mcp_configs: Optional MCP server configurations
        """
        self.mcp_configs = mcp_configs or {}

    def is_enabled(self, mcp_name: str) -> bool:
        """Check if an MCP server is enabled."""
        if mcp_name not in self.mcp_configs:
            return True  # Default enabled if not configured
        return self.mcp_configs[mcp_name].enabled

    def is_auto_activate_enabled(self, mcp_name: str) -> bool:
        """Check if auto-activation is enabled for an MCP server."""
        if mcp_name not in self.mcp_configs:
            return True  # Default enabled if not configured
        return self.mcp_configs[mcp_name].auto_activate

    def activate_for_personas(
        self,
        personas: List[PersonaScore],
    ) -> ActivationResult:
        """
        Determine MCP activation based on persona scores.

        Args:
            personas: List of PersonaScore objects with scores

        Returns:
            ActivationResult with auto-activate and suggested MCPs
        """
        result = ActivationResult()

        for persona in personas:
            if persona.score >= self.AUTO_THRESHOLD:
                # Auto-activate primary and secondary MCPs
                for mcp_name in get_auto_activated_mcps(persona.name):
                    if self.is_enabled(mcp_name) and self.is_auto_activate_enabled(mcp_name):
                        result.add_auto(
                            mcp_name,
                            f"persona:{persona.name}",
                            persona.score,
                        )
                # Suggest non-auto MCPs
                for mcp_name in get_suggested_mcps(persona.name):
                    if self.is_enabled(mcp_name):
                        result.add_suggested(
                            mcp_name,
                            f"persona:{persona.name}",
                            persona.score * 0.5,
                        )

            elif persona.score >= self.SUGGEST_THRESHOLD:
                # Only suggest MCPs for moderate scores
                if persona.mcp_primary and self.is_enabled(persona.mcp_primary):
                    result.add_suggested(
                        persona.mcp_primary,
                        f"persona:{persona.name}",
                        persona.score,
                    )

        return result

    def activate_for_context(
        self,
        brief_text: str = "",
        file_paths: Optional[List[str]] = None,
        flags: Optional[List[str]] = None,
    ) -> ActivationResult:
        """
        Determine MCP activation based on context analysis.

        Args:
            brief_text: Text content of the brief
            file_paths: List of impacted file paths
            flags: List of active flags

        Returns:
            ActivationResult with auto-activate and suggested MCPs
        """
        result = ActivationResult()
        file_paths = file_paths or []
        flags = flags or []

        # Check keyword triggers
        keyword_scores = check_keyword_triggers(brief_text)
        for mcp_name, score in keyword_scores.items():
            if not self.is_enabled(mcp_name):
                continue

            if score >= self.AUTO_THRESHOLD:
                result.add_auto(mcp_name, "keywords", score)
            elif score >= self.SUGGEST_THRESHOLD:
                result.add_suggested(mcp_name, "keywords", score)

        # Check file triggers
        file_triggers = check_file_triggers(file_paths)
        for mcp_name, triggered in file_triggers.items():
            if triggered and self.is_enabled(mcp_name):
                result.add_auto(mcp_name, "files", 0.8)

        # Check flag triggers
        flag_triggers = check_flag_triggers(flags)
        for mcp_name, triggered in flag_triggers.items():
            if triggered and self.is_enabled(mcp_name):
                result.add_auto(mcp_name, "flags", 1.0)

        return result

    def activate_combined(
        self,
        personas: Optional[List[PersonaScore]] = None,
        brief_text: str = "",
        file_paths: Optional[List[str]] = None,
        flags: Optional[List[str]] = None,
    ) -> ActivationResult:
        """
        Combine persona and context activation.

        Args:
            personas: List of PersonaScore objects
            brief_text: Text content of the brief
            file_paths: List of impacted file paths
            flags: List of active flags

        Returns:
            Combined ActivationResult
        """
        result = ActivationResult()

        # Get persona-based activation
        if personas:
            persona_result = self.activate_for_personas(personas)
            for mcp_name in persona_result.auto_activate:
                result.add_auto(
                    mcp_name,
                    persona_result.sources.get(mcp_name, "persona"),
                    persona_result.scores.get(mcp_name, 0.6),
                )
            for mcp_name in persona_result.suggested:
                result.add_suggested(
                    mcp_name,
                    persona_result.sources.get(mcp_name, "persona"),
                    persona_result.scores.get(mcp_name, 0.4),
                )

        # Get context-based activation
        context_result = self.activate_for_context(brief_text, file_paths, flags)
        for mcp_name in context_result.auto_activate:
            result.add_auto(
                mcp_name,
                context_result.sources.get(mcp_name, "context"),
                context_result.scores.get(mcp_name, 0.6),
            )
        for mcp_name in context_result.suggested:
            result.add_suggested(
                mcp_name,
                context_result.sources.get(mcp_name, "context"),
                context_result.scores.get(mcp_name, 0.4),
            )

        return result

    def create_context(self, result: ActivationResult) -> MCPContext:
        """
        Create MCPContext from activation result.

        Args:
            result: ActivationResult from activation analysis

        Returns:
            MCPContext ready for use in workflow
        """
        context = MCPContext()

        for mcp_name in result.auto_activate:
            source = result.sources.get(mcp_name, "auto")
            context.activate(mcp_name, source)

        return context

    def format_for_display(self, result: ActivationResult) -> str:
        """
        Format activation result for breakpoint display.

        Args:
            result: ActivationResult to format

        Returns:
            Formatted string for FLAGS line
        """
        parts = []

        for mcp_name in result.auto_activate:
            source = result.sources.get(mcp_name, "auto")
            score = result.scores.get(mcp_name, 0)
            flag = f"--{mcp_name[:3] if mcp_name != 'playwright' else 'play'}"
            if "persona:" in source:
                parts.append(f"{flag} (auto: {source.split(':')[1]})")
            else:
                parts.append(f"{flag} (auto: {score:.2f})")

        for mcp_name in result.suggested:
            source = result.sources.get(mcp_name, "suggested")
            flag = f"--{mcp_name[:3] if mcp_name != 'playwright' else 'play'}"
            parts.append(f"{flag} (suggested)")

        return " | ".join(parts)
