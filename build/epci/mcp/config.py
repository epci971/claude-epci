"""
MCP Configuration Module (F12)

Provides dataclasses for MCP server configuration and context management.
Follows the same pattern as orchestration/config.py for consistency.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class MCPStatus(Enum):
    """Status of an MCP server."""
    READY = "ready"
    PENDING = "pending"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class MCPServerConfig:
    """
    Configuration for a single MCP server.

    Attributes:
        name: Server identifier (context7, sequential, magic, playwright)
        enabled: Whether the server is enabled globally
        auto_activate: Whether to auto-activate based on persona/context
        timeout_seconds: Request timeout (default 15s)
        retry_count: Number of retries on failure (default 2)
        condition: Optional activation condition (e.g., "has_imports")
    """
    name: str
    enabled: bool = True
    auto_activate: bool = True
    timeout_seconds: int = 15
    retry_count: int = 2
    condition: Optional[str] = None

    def __post_init__(self):
        """Validate configuration."""
        valid_names = {"context7", "sequential", "magic", "playwright"}
        if self.name not in valid_names:
            raise ValueError(f"Invalid MCP server name: {self.name}. Must be one of {valid_names}")

        if self.timeout_seconds <= 0:
            raise ValueError(f"MCP {self.name}: timeout must be positive")
        if self.timeout_seconds > 60:
            raise ValueError(f"MCP {self.name}: timeout exceeds maximum (60s)")

        if self.retry_count < 0:
            raise ValueError(f"MCP {self.name}: retry_count must be non-negative")
        if self.retry_count > 5:
            raise ValueError(f"MCP {self.name}: retry_count exceeds maximum (5)")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "auto_activate": self.auto_activate,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "condition": self.condition,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPServerConfig":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            enabled=data.get("enabled", True),
            auto_activate=data.get("auto_activate", True),
            timeout_seconds=data.get("timeout_seconds", 15),
            retry_count=data.get("retry_count", 2),
            condition=data.get("condition"),
        )


@dataclass
class MCPContext:
    """
    Runtime context for MCP servers during workflow execution.

    Tracks which servers are active, their status, and any fallbacks used.
    Integrates with WaveContext for orchestration (F11).

    Attributes:
        active_servers: List of currently active MCP server names
        server_status: Status of each server (ready, pending, error, etc.)
        fallback_used: Map of server name to fallback strategy used
        activation_source: How each server was activated (auto, explicit, persona)
    """
    active_servers: List[str] = field(default_factory=list)
    server_status: Dict[str, MCPStatus] = field(default_factory=dict)
    fallback_used: Dict[str, str] = field(default_factory=dict)
    activation_source: Dict[str, str] = field(default_factory=dict)

    def activate(self, server_name: str, source: str = "auto") -> None:
        """
        Activate an MCP server.

        Args:
            server_name: Name of the MCP server to activate
            source: Activation source (auto, explicit, persona:<name>)
        """
        if server_name not in self.active_servers:
            self.active_servers.append(server_name)
        self.server_status[server_name] = MCPStatus.PENDING
        self.activation_source[server_name] = source

    def deactivate(self, server_name: str) -> None:
        """Deactivate an MCP server."""
        if server_name in self.active_servers:
            self.active_servers.remove(server_name)
        self.server_status[server_name] = MCPStatus.DISABLED

    def set_ready(self, server_name: str) -> None:
        """Mark server as ready."""
        self.server_status[server_name] = MCPStatus.READY

    def set_error(self, server_name: str, fallback: Optional[str] = None) -> None:
        """Mark server as error and record fallback if used."""
        self.server_status[server_name] = MCPStatus.ERROR
        if fallback:
            self.fallback_used[server_name] = fallback

    def is_active(self, server_name: str) -> bool:
        """Check if a server is active."""
        return server_name in self.active_servers

    def is_ready(self, server_name: str) -> bool:
        """Check if a server is ready for use."""
        return self.server_status.get(server_name) == MCPStatus.READY

    def get_active_for_display(self) -> List[Dict[str, str]]:
        """
        Get active servers formatted for breakpoint display.

        Returns list of dicts with name, status, and source.
        """
        result = []
        for name in self.active_servers:
            status = self.server_status.get(name, MCPStatus.PENDING)
            source = self.activation_source.get(name, "unknown")
            result.append({
                "name": name,
                "status": status.value,
                "source": source,
            })
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "active_servers": self.active_servers,
            "server_status": {k: v.value for k, v in self.server_status.items()},
            "fallback_used": self.fallback_used,
            "activation_source": self.activation_source,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPContext":
        """Create from dictionary."""
        return cls(
            active_servers=data.get("active_servers", []),
            server_status={
                k: MCPStatus(v) for k, v in data.get("server_status", {}).items()
            },
            fallback_used=data.get("fallback_used", {}),
            activation_source=data.get("activation_source", {}),
        )

    def summary(self) -> str:
        """Generate human-readable summary."""
        active = len(self.active_servers)
        ready = sum(1 for s in self.server_status.values() if s == MCPStatus.READY)
        errors = sum(1 for s in self.server_status.values() if s == MCPStatus.ERROR)
        fallbacks = len(self.fallback_used)

        return (
            f"MCP Context:\n"
            f"  Active servers: {active}\n"
            f"  Ready: {ready}\n"
            f"  Errors: {errors}\n"
            f"  Fallbacks used: {fallbacks}"
        )


# Default MCP configuration matching CDC-F12
DEFAULT_MCP_CONFIG = {
    "mcp": {
        "enabled": True,
        "default_timeout_seconds": 15,
        "retry_count": 2,
        "servers": {
            "context7": {
                "enabled": True,
                "auto_activate": True,
                "timeout_seconds": 15,
            },
            "sequential": {
                "enabled": True,
                "auto_activate": True,
                "timeout_seconds": 30,
            },
            "magic": {
                "enabled": True,
                "auto_activate": True,
                "timeout_seconds": 20,
            },
            "playwright": {
                "enabled": True,
                "auto_activate": True,
                "timeout_seconds": 20,
            },
        },
    }
}


def load_mcp_configs(settings: Dict[str, Any]) -> Dict[str, MCPServerConfig]:
    """
    Load MCP server configurations from settings dictionary.

    Args:
        settings: Settings dictionary (from .project-memory/settings.json)

    Returns:
        Dictionary mapping server name to MCPServerConfig
    """
    mcp_settings = settings.get("mcp", DEFAULT_MCP_CONFIG["mcp"])

    if not mcp_settings.get("enabled", True):
        return {}

    configs = {}
    servers = mcp_settings.get("servers", {})

    for name, server_data in servers.items():
        if name in {"context7", "sequential", "magic", "playwright"}:
            configs[name] = MCPServerConfig(
                name=name,
                enabled=server_data.get("enabled", True),
                auto_activate=server_data.get("auto_activate", True),
                timeout_seconds=server_data.get(
                    "timeout_seconds",
                    mcp_settings.get("default_timeout_seconds", 15)
                ),
                retry_count=server_data.get(
                    "retry_count",
                    mcp_settings.get("retry_count", 2)
                ),
                condition=server_data.get("condition"),
            )

    return configs
