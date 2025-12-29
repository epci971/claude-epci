"""
Orchestration Configuration Module

Handles loading and merging of orchestration configurations from YAML files.
Supports per-agent timeouts, conditions, and orchestration modes.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


class OrchestrationMode(Enum):
    """Orchestration execution modes."""
    SEQUENTIAL = "sequential"  # One agent after another
    PARALLEL = "parallel"      # All agents simultaneously (ignore DAG)
    DAG = "dag"               # Respect dependency graph


@dataclass
class AgentConfig:
    """Configuration for a single agent in the orchestration."""
    name: str
    depends_on: List[str] = field(default_factory=list)
    timeout: int = 60  # seconds
    required: bool = True
    condition: Optional[str] = None  # e.g., "has_sensitive_files"

    def __post_init__(self):
        if self.timeout <= 0:
            raise ValueError(f"Agent {self.name}: timeout must be positive")
        if self.timeout > 300:
            raise ValueError(f"Agent {self.name}: timeout exceeds maximum (300s)")


@dataclass
class OrchestrationConfig:
    """Complete orchestration configuration."""
    mode: OrchestrationMode = OrchestrationMode.DAG
    timeout_global: int = 300  # 5 minutes max
    agents: Dict[str, AgentConfig] = field(default_factory=dict)

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get agent configuration by name."""
        return self.agents.get(name)

    def get_required_agents(self) -> List[str]:
        """Get list of required agent names."""
        return [name for name, cfg in self.agents.items() if cfg.required]

    def get_optional_agents(self) -> List[str]:
        """Get list of optional agent names."""
        return [name for name, cfg in self.agents.items() if not cfg.required]


# Default configuration matching CDC-F07
DEFAULT_CONFIG = {
    "orchestration": {
        "default_mode": "dag",
        "timeout_global": 300,
        "agents": {
            "plan-validator": {
                "depends_on": [],
                "timeout": 60,
                "required": True,
            },
            "code-reviewer": {
                "depends_on": ["plan-validator"],
                "timeout": 90,
                "required": True,
            },
            "security-auditor": {
                "depends_on": ["plan-validator"],
                "timeout": 60,
                "required": False,
                "condition": "has_sensitive_files",
            },
            "qa-reviewer": {
                "depends_on": ["plan-validator"],
                "timeout": 60,
                "required": False,
                "condition": "complexity >= STANDARD",
            },
            "doc-generator": {
                "depends_on": ["code-reviewer", "security-auditor", "qa-reviewer"],
                "timeout": 60,
                "required": True,
            },
        },
    }
}


def load_config(path: str) -> OrchestrationConfig:
    """
    Load orchestration configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file

    Returns:
        OrchestrationConfig instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    return _parse_config(raw_config)


def load_config_from_dict(raw_config: Dict[str, Any]) -> OrchestrationConfig:
    """
    Load orchestration configuration from a dictionary.

    Args:
        raw_config: Raw configuration dictionary

    Returns:
        OrchestrationConfig instance
    """
    return _parse_config(raw_config)


def _parse_config(raw_config: Dict[str, Any]) -> OrchestrationConfig:
    """Parse raw configuration dictionary into OrchestrationConfig."""
    if not raw_config or "orchestration" not in raw_config:
        raise ValueError("Invalid config: missing 'orchestration' key")

    orch_config = raw_config["orchestration"]

    # Parse mode
    mode_str = orch_config.get("default_mode", "dag")
    try:
        mode = OrchestrationMode(mode_str)
    except ValueError:
        raise ValueError(f"Invalid orchestration mode: {mode_str}")

    # Parse global timeout
    timeout_global = orch_config.get("timeout_global", 300)
    if timeout_global <= 0 or timeout_global > 600:
        raise ValueError(f"Invalid global timeout: {timeout_global} (must be 1-600)")

    # Parse agents
    agents = {}
    raw_agents = orch_config.get("agents", {})

    for name, agent_data in raw_agents.items():
        agents[name] = AgentConfig(
            name=name,
            depends_on=agent_data.get("depends_on", []),
            timeout=agent_data.get("timeout", 60),
            required=agent_data.get("required", True),
            condition=agent_data.get("condition"),
        )

    return OrchestrationConfig(
        mode=mode,
        timeout_global=timeout_global,
        agents=agents,
    )


def merge_with_defaults(
    project_config: Optional[OrchestrationConfig],
    defaults: Optional[OrchestrationConfig] = None,
) -> OrchestrationConfig:
    """
    Merge project-specific configuration with defaults.

    Project config takes precedence over defaults.

    Args:
        project_config: Project-specific configuration (or None)
        defaults: Default configuration (or None to use built-in defaults)

    Returns:
        Merged OrchestrationConfig
    """
    if defaults is None:
        defaults = _parse_config(DEFAULT_CONFIG)

    if project_config is None:
        return defaults

    # Merge agents: project overrides defaults
    merged_agents = dict(defaults.agents)
    merged_agents.update(project_config.agents)

    return OrchestrationConfig(
        mode=project_config.mode,
        timeout_global=project_config.timeout_global,
        agents=merged_agents,
    )


def get_default_config() -> OrchestrationConfig:
    """Get the built-in default configuration."""
    return _parse_config(DEFAULT_CONFIG)
