"""
MCP Registry Module (F12)

Provides a singleton registry for MCP server discovery and status tracking.
Handles server availability checking and status management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from threading import Lock
from typing import Any, Callable, Dict, List, Optional

from .config import MCPServerConfig, MCPStatus, load_mcp_configs


class MCPRegistry:
    """
    Singleton registry for MCP server management.

    Handles:
    - Server registration and discovery
    - Status tracking
    - Availability checking with caching
    """

    _instance: Optional["MCPRegistry"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "MCPRegistry":
        """Ensure singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize registry (only once due to singleton)."""
        if self._initialized:
            return

        self._configs: Dict[str, MCPServerConfig] = {}
        self._status: Dict[str, MCPStatus] = {}
        self._last_check: Dict[str, datetime] = {}
        self._availability_cache: Dict[str, bool] = {}
        self._cache_duration = timedelta(minutes=5)
        self._initialized = True

    def reset(self) -> None:
        """Reset registry state (mainly for testing)."""
        self._configs.clear()
        self._status.clear()
        self._last_check.clear()
        self._availability_cache.clear()

    def register(self, config: MCPServerConfig) -> None:
        """
        Register an MCP server configuration.

        Args:
            config: MCPServerConfig to register
        """
        self._configs[config.name] = config
        self._status[config.name] = MCPStatus.PENDING

    def register_from_settings(self, settings: Dict[str, Any]) -> None:
        """
        Register all MCP servers from settings dictionary.

        Args:
            settings: Settings dictionary (from .project-memory/settings.json)
        """
        configs = load_mcp_configs(settings)
        for config in configs.values():
            self.register(config)

    def discover(self) -> List[str]:
        """
        Discover all registered MCP servers.

        Returns:
            List of registered server names
        """
        return list(self._configs.keys())

    def get_config(self, name: str) -> Optional[MCPServerConfig]:
        """
        Get configuration for a specific server.

        Args:
            name: Server name

        Returns:
            MCPServerConfig if registered, None otherwise
        """
        return self._configs.get(name)

    def get_status(self, name: str) -> MCPStatus:
        """
        Get current status of a server.

        Args:
            name: Server name

        Returns:
            MCPStatus (defaults to UNAVAILABLE if not registered)
        """
        return self._status.get(name, MCPStatus.UNAVAILABLE)

    def set_status(self, name: str, status: MCPStatus) -> None:
        """
        Set status for a server.

        Args:
            name: Server name
            status: New status
        """
        self._status[name] = status

    def is_available(self, name: str) -> bool:
        """
        Check if a server is available (cached).

        Uses cached result if within cache duration.

        Args:
            name: Server name

        Returns:
            True if server is available
        """
        if name not in self._configs:
            return False

        config = self._configs[name]
        if not config.enabled:
            return False

        # Check cache
        now = datetime.now()
        if name in self._last_check:
            if now - self._last_check[name] < self._cache_duration:
                return self._availability_cache.get(name, False)

        # For now, assume available if enabled
        # In real implementation, would check actual MCP server
        self._availability_cache[name] = True
        self._last_check[name] = now

        return True

    def check_availability(
        self,
        name: str,
        check_fn: Optional[Callable[[str], bool]] = None,
    ) -> bool:
        """
        Check server availability with optional custom check function.

        Args:
            name: Server name
            check_fn: Optional function to check availability

        Returns:
            True if server is available
        """
        if name not in self._configs:
            return False

        if check_fn:
            available = check_fn(name)
        else:
            # Default: check if enabled
            config = self._configs[name]
            available = config.enabled

        # Update cache
        self._availability_cache[name] = available
        self._last_check[name] = datetime.now()
        self._status[name] = MCPStatus.READY if available else MCPStatus.UNAVAILABLE

        return available

    def get_enabled_servers(self) -> List[str]:
        """
        Get list of enabled server names.

        Returns:
            List of enabled server names
        """
        return [
            name for name, config in self._configs.items()
            if config.enabled
        ]

    def get_auto_activate_servers(self) -> List[str]:
        """
        Get list of servers with auto-activate enabled.

        Returns:
            List of server names with auto-activate
        """
        return [
            name for name, config in self._configs.items()
            if config.enabled and config.auto_activate
        ]

    def summary(self) -> str:
        """
        Generate summary of registry state.

        Returns:
            Human-readable summary
        """
        total = len(self._configs)
        enabled = len(self.get_enabled_servers())
        available = sum(1 for name in self._configs if self.is_available(name))

        status_counts = {}
        for status in self._status.values():
            status_counts[status.value] = status_counts.get(status.value, 0) + 1

        lines = [
            f"MCP Registry:",
            f"  Total servers: {total}",
            f"  Enabled: {enabled}",
            f"  Available: {available}",
            f"  Status:",
        ]
        for status, count in status_counts.items():
            lines.append(f"    {status}: {count}")

        return "\n".join(lines)


# Convenience function to get the singleton instance
def get_registry() -> MCPRegistry:
    """Get the singleton MCPRegistry instance."""
    return MCPRegistry()
