"""
MCP Integration Module (F12)

Provides Model Context Protocol integration for EPCI with 4 servers:
- Context7: Library documentation lookup
- Sequential: Multi-step structured reasoning
- Magic: UI component generation (21st.dev)
- Playwright: E2E testing and browser automation

Auto-activation based on F09 persona scoring with graceful fallbacks.
"""

from .config import MCPServerConfig, MCPContext, MCPStatus
from .activation_matrix import PERSONA_MCP_MAPPING, get_mcps_for_persona
from .auto_activation import MCPAutoActivation
from .registry import MCPRegistry
from .fallbacks import get_fallback, FALLBACK_STRATEGIES

__all__ = [
    # Config
    "MCPServerConfig",
    "MCPContext",
    "MCPStatus",
    # Activation
    "PERSONA_MCP_MAPPING",
    "get_mcps_for_persona",
    "MCPAutoActivation",
    # Registry
    "MCPRegistry",
    # Fallbacks
    "get_fallback",
    "FALLBACK_STRATEGIES",
]

__version__ = "1.0.0"
