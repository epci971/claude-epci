"""
EPCI Multi-Agent Orchestration Module (F07 + F11)

Provides intelligent orchestration for parallel agent execution using DAG,
and wave-based orchestration for LARGE features.

Usage (Agent Orchestration - F07):
    from orchestration import Orchestrator, load_config

    config = load_config("config/dag-default.yaml")
    orchestrator = Orchestrator(config)
    result = await orchestrator.execute(context)

Usage (Wave Orchestration - F11):
    from orchestration import WavePlanner, WaveOrchestrator, create_wave_plan

    plan = create_wave_plan("feature-slug", tasks, strategy="progressive")
    orchestrator = WaveOrchestrator()
    result = await orchestrator.execute(plan)

Components:
    - Orchestrator: Main orchestration engine with DAG execution (F07)
    - DAGBuilder: Constructs and validates dependency graphs (F07)
    - AgentRunner: Async agent execution with timeout handling (F07)
    - WavePlanner: Plans wave execution for LARGE features (F11)
    - WaveOrchestrator: Executes waves with context accumulation (F11)
    - WaveContext: Accumulated context across waves (F11)
    - Strategies: Progressive and Systematic wave strategies (F11)

Version: 1.1.0 (EPCI v4.0 - F07 + F11)
"""

from .config import (
    OrchestrationMode,
    AgentConfig,
    OrchestrationConfig,
    load_config,
    load_config_from_dict,
    merge_with_defaults,
    get_default_config,
    # Wave config (F11)
    WaveStrategyType,
    WaveDefinition,
    WaveConfig,
    load_wave_config,
    get_default_wave_config,
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

# Wave Orchestration (F11)
from .wave_context import (
    WaveStatus,
    Wave,
    WaveContext,
    Issue,
    Decision,
    TaskResult,
)
from .wave_planner import (
    WavePlanner,
    WavePlan,
    PlannerInput,
    create_wave_plan,
)
from .wave_orchestrator import (
    WaveOrchestrator,
    WaveOrchestrationResult,
    WaveExecutionResult,
    run_wave_orchestration,
)
from .strategies import (
    WaveStrategy,
    Task,
    StrategyResult,
    ProgressiveStrategy,
    SystematicStrategy,
    get_strategy,
)

__all__ = [
    # Config (F07)
    "OrchestrationMode",
    "AgentConfig",
    "OrchestrationConfig",
    "load_config",
    "load_config_from_dict",
    "merge_with_defaults",
    "get_default_config",
    # Config (F11)
    "WaveStrategyType",
    "WaveDefinition",
    "WaveConfig",
    "load_wave_config",
    "get_default_wave_config",
    # DAG (F07)
    "DAG",
    "DAGBuilder",
    "CycleDetectedError",
    # Agent (F07)
    "AgentStatus",
    "AgentResult",
    "AgentRunner",
    # Orchestrator (F07)
    "Orchestrator",
    "OrchestrationResult",
    "OrchestrationError",
    # Wave Context (F11)
    "WaveStatus",
    "Wave",
    "WaveContext",
    "Issue",
    "Decision",
    "TaskResult",
    # Wave Planner (F11)
    "WavePlanner",
    "WavePlan",
    "PlannerInput",
    "create_wave_plan",
    # Wave Orchestrator (F11)
    "WaveOrchestrator",
    "WaveOrchestrationResult",
    "WaveExecutionResult",
    "run_wave_orchestration",
    # Strategies (F11)
    "WaveStrategy",
    "Task",
    "StrategyResult",
    "ProgressiveStrategy",
    "SystematicStrategy",
    "get_strategy",
]

__version__ = "1.1.0"
