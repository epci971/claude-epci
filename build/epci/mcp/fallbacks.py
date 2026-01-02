"""
MCP Fallback Strategies (F12)

Defines fallback behavior when MCP servers are unavailable.
Each MCP has a specific fallback strategy per CDC-F12 Section 7.2.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .config import MCPStatus


class FallbackStrategy(Enum):
    """Available fallback strategies."""
    WEB_SEARCH = "web_search"
    NATIVE_REASONING = "native_reasoning"
    BASIC_GENERATION = "basic_generation"
    MANUAL_SUGGESTION = "manual_suggestion"
    SKIP = "skip"


# Fallback strategies from CDC-F12 Section 7.2
FALLBACK_STRATEGIES: Dict[str, FallbackStrategy] = {
    "context7": FallbackStrategy.WEB_SEARCH,
    "sequential": FallbackStrategy.NATIVE_REASONING,
    "magic": FallbackStrategy.BASIC_GENERATION,
    "playwright": FallbackStrategy.MANUAL_SUGGESTION,
}


# Human-readable fallback descriptions
FALLBACK_DESCRIPTIONS: Dict[str, str] = {
    "context7": "Using web search for documentation",
    "sequential": "Using native Claude reasoning",
    "magic": "Using basic component generation without 21st.dev",
    "playwright": "Suggesting manual test steps",
}


# Warning messages from CDC-F12 Section 7.1
FALLBACK_MESSAGES: Dict[str, str] = {
    "context7": "Context7 unreachable, continuing without",
    "sequential": "Sequential error, fallback to standard",
    "magic": "Magic unavailable, using basic generation",
    "playwright": "Playwright unavailable, manual testing suggested",
}


@dataclass
class FallbackResult:
    """Result of a fallback execution."""
    success: bool
    strategy: FallbackStrategy
    message: str
    data: Optional[Any] = None


def get_fallback(mcp_name: str) -> FallbackStrategy:
    """
    Get fallback strategy for an MCP server.

    Args:
        mcp_name: Name of the MCP server

    Returns:
        FallbackStrategy for the server
    """
    return FALLBACK_STRATEGIES.get(mcp_name, FallbackStrategy.SKIP)


def get_fallback_message(mcp_name: str) -> str:
    """
    Get fallback warning message for an MCP server.

    Args:
        mcp_name: Name of the MCP server

    Returns:
        Warning message to display
    """
    return FALLBACK_MESSAGES.get(mcp_name, f"{mcp_name} unavailable")


def get_fallback_description(mcp_name: str) -> str:
    """
    Get human-readable fallback description.

    Args:
        mcp_name: Name of the MCP server

    Returns:
        Description of what fallback does
    """
    return FALLBACK_DESCRIPTIONS.get(mcp_name, "Fallback active")


T = TypeVar("T")


def execute_with_fallback(
    mcp_name: str,
    primary_action: Callable[[], T],
    fallback_action: Optional[Callable[[], T]] = None,
    max_retries: int = 2,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
    on_fallback: Optional[Callable[[str], None]] = None,
) -> FallbackResult:
    """
    Execute an MCP action with automatic fallback on failure.

    Implements retry logic per CDC-F12 Section 7.1:
    - Retry up to max_retries times
    - If still failing, execute fallback
    - Log/notify at each step

    Args:
        mcp_name: Name of the MCP server
        primary_action: Primary action to attempt
        fallback_action: Fallback action if primary fails
        max_retries: Number of retries before fallback (default: 2)
        on_retry: Callback on each retry (retry_count, exception)
        on_fallback: Callback when switching to fallback

    Returns:
        FallbackResult with success status and data
    """
    strategy = get_fallback(mcp_name)
    last_error: Optional[Exception] = None

    # Try primary action with retries
    for attempt in range(max_retries + 1):
        try:
            result = primary_action()
            return FallbackResult(
                success=True,
                strategy=strategy,
                message=f"{mcp_name} action completed",
                data=result,
            )
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                if on_retry:
                    on_retry(attempt + 1, e)

    # Primary failed, try fallback
    if on_fallback:
        on_fallback(get_fallback_message(mcp_name))

    if fallback_action:
        try:
            result = fallback_action()
            return FallbackResult(
                success=True,
                strategy=strategy,
                message=get_fallback_description(mcp_name),
                data=result,
            )
        except Exception as e:
            return FallbackResult(
                success=False,
                strategy=strategy,
                message=f"Fallback also failed: {e}",
                data=None,
            )

    # No fallback action provided
    return FallbackResult(
        success=False,
        strategy=strategy,
        message=f"{mcp_name} failed after {max_retries} retries: {last_error}",
        data=None,
    )


class FallbackHandler:
    """
    Handler for MCP fallback operations.

    Provides a higher-level interface for managing fallbacks
    with logging and metrics collection.
    """

    def __init__(self):
        """Initialize fallback handler."""
        self.fallback_count: Dict[str, int] = {}
        self.error_log: List[Dict[str, Any]] = []

    def record_fallback(self, mcp_name: str, reason: str) -> None:
        """
        Record a fallback occurrence.

        Args:
            mcp_name: MCP server name
            reason: Reason for fallback
        """
        self.fallback_count[mcp_name] = self.fallback_count.get(mcp_name, 0) + 1
        self.error_log.append({
            "mcp": mcp_name,
            "reason": reason,
            "strategy": get_fallback(mcp_name).value,
        })

    def get_fallback_stats(self) -> Dict[str, int]:
        """Get fallback statistics."""
        return self.fallback_count.copy()

    def format_warning(self, mcp_name: str) -> str:
        """
        Format a warning message for display.

        Args:
            mcp_name: MCP server name

        Returns:
            Formatted warning string
        """
        return f"[MCP] {get_fallback_message(mcp_name)}"

    def format_status(self, mcp_name: str, status: MCPStatus) -> str:
        """
        Format status for breakpoint display.

        Args:
            mcp_name: MCP server name
            status: Current status

        Returns:
            Formatted status string with icon
        """
        icons = {
            MCPStatus.READY: "",
            MCPStatus.PENDING: "",
            MCPStatus.ERROR: "",
            MCPStatus.UNAVAILABLE: "",
            MCPStatus.DISABLED: "",
        }
        icon = icons.get(status, "")
        return f"{icon} {mcp_name} ({status.value})"
