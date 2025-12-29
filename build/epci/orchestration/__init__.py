"""
EPCI Multi-Agent Orchestration Module (F07)

Provides intelligent orchestration for parallel agent execution using DAG.

Usage:
    from orchestration import Orchestrator, load_config

    config = load_config("config/dag-default.yaml")
    orchestrator = Orchestrator(config)
    result = await orchestrator.execute(context)

Components:
    - Orchestrator: Main orchestration engine with DAG execution
    - DAGBuilder: Constructs and validates dependency graphs
    - AgentRunner: Async agent execution with timeout handling
    - load_config: Configuration loader with YAML support

Version: 1.0.0 (EPCI v4.0)
"""

from .config import (
    OrchestrationMode,
    AgentConfig,
    OrchestrationConfig,
    load_config,
    load_config_from_dict,
    merge_with_defaults,
    get_default_config,
)
from .dag_builder import (
    DAG,
    DAGBuilder,
    CycleDetectedError,
)
from .agent_runner import (
    AgentStatus,
    AgentResult,
    AgentRunner,
)
from .orchestrator import (
    Orchestrator,
    OrchestrationResult,
    OrchestrationError,
)

__all__ = [
    # Config
    "OrchestrationMode",
    "AgentConfig",
    "OrchestrationConfig",
    "load_config",
    "load_config_from_dict",
    "merge_with_defaults",
    "get_default_config",
    # DAG
    "DAG",
    "DAGBuilder",
    "CycleDetectedError",
    # Agent
    "AgentStatus",
    "AgentResult",
    "AgentRunner",
    # Orchestrator
    "Orchestrator",
    "OrchestrationResult",
    "OrchestrationError",
]

__version__ = "1.0.0"
