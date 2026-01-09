"""
Orchestrator Module

Main orchestration engine for parallel agent execution using DAG dependencies.
Handles wave execution, error propagation, and result collection.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

from .config import OrchestrationConfig, OrchestrationMode, load_config
from .dag_builder import DAG, DAGBuilder, CycleDetectedError
from .agent_runner import AgentRunner, AgentResult, AgentStatus, AgentExecutor


logger = logging.getLogger(__name__)


class OrchestrationError(Exception):
    """Base exception for orchestration errors."""
    pass


class RequiredAgentFailedError(OrchestrationError):
    """Raised when a required agent fails."""

    def __init__(self, agent_name: str, result: AgentResult):
        self.agent_name = agent_name
        self.result = result
        super().__init__(f"Required agent '{agent_name}' failed: {result.error or result.status.value}")


@dataclass
class OrchestrationResult:
    """Complete result of an orchestration run."""
    success: bool
    results: Dict[str, AgentResult] = field(default_factory=dict)
    duration_seconds: float = 0.0
    waves_executed: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def parallel_agents(self) -> int:
        """Count of agents that ran in parallel (same wave)."""
        return sum(1 for r in self.results.values() if r.status != AgentStatus.SKIPPED)

    @property
    def sequential_time_estimate(self) -> float:
        """Estimated time if agents ran sequentially."""
        return sum(r.duration_seconds for r in self.results.values())

    @property
    def parallel_gain(self) -> float:
        """Percentage time saved by parallel execution."""
        seq_time = self.sequential_time_estimate
        if seq_time == 0:
            return 0.0
        return ((seq_time - self.duration_seconds) / seq_time) * 100

    def get_verdict_summary(self) -> Dict[str, int]:
        """Get count of each verdict type."""
        verdicts: Dict[str, int] = {}
        for result in self.results.values():
            verdict = result.verdict or "UNKNOWN"
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
        return verdicts

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "results": {k: v.to_dict() for k, v in self.results.items()},
            "duration_seconds": self.duration_seconds,
            "waves_executed": self.waves_executed,
            "errors": self.errors,
            "warnings": self.warnings,
            "parallel_gain": f"{self.parallel_gain:.1f}%",
        }


class Orchestrator:
    """
    Main orchestration engine for multi-agent execution.

    Executes agents according to a DAG, running independent agents in parallel
    while respecting dependency ordering.

    Usage:
        config = load_config("config/dag-default.yaml")
        orchestrator = Orchestrator(config)
        result = await orchestrator.execute(context)
    """

    def __init__(
        self,
        config: OrchestrationConfig,
        executor: Optional[AgentExecutor] = None,
        hook_runner: Optional[Callable] = None,
    ):
        """
        Initialize the orchestrator.

        Args:
            config: Orchestration configuration
            executor: Optional function to execute agents
            hook_runner: Optional function to run hooks (pre-agent, post-agent)
        """
        self.config = config
        self.executor = executor
        self.hook_runner = hook_runner

        # Build DAG from config
        self._dag = DAGBuilder.from_config(config)

        # Execution state
        self._results: Dict[str, AgentResult] = {}
        self._completed: Set[str] = set()
        self._skipped: Set[str] = set()
        self._failed_required: bool = False
        self._stop_requested: bool = False

    async def execute(self, context: Dict[str, Any]) -> OrchestrationResult:
        """
        Execute all agents according to the DAG.

        Args:
            context: Execution context (files, feature info, etc.)

        Returns:
            OrchestrationResult with all agent results
        """
        start_time = time.time()
        waves_executed = 0
        errors: List[str] = []
        warnings: List[str] = []

        logger.info(f"Starting orchestration with mode: {self.config.mode.value}")
        logger.info(f"Agents to execute: {list(self._dag.agents.keys())}")

        # Reset state
        self._results = {}
        self._completed = set()
        self._skipped = set()
        self._failed_required = False
        self._stop_requested = False

        try:
            # Execute based on mode
            if self.config.mode == OrchestrationMode.SEQUENTIAL:
                waves_executed = await self._execute_sequential(context)
            elif self.config.mode == OrchestrationMode.PARALLEL:
                waves_executed = await self._execute_parallel(context)
            else:  # DAG mode
                waves_executed = await self._execute_dag(context)

        except RequiredAgentFailedError as e:
            errors.append(str(e))
            logger.error(f"Orchestration stopped: {e}")

        except asyncio.TimeoutError:
            errors.append(f"Global timeout exceeded ({self.config.timeout_global}s)")
            logger.error("Orchestration timed out")

        except Exception as e:
            errors.append(f"Unexpected error: {e}")
            logger.exception("Orchestration failed with unexpected error")

        # Collect warnings from optional agent failures
        for name, result in self._results.items():
            agent_config = self.config.get_agent(name)
            if agent_config and not agent_config.required and result.is_failure:
                warnings.append(f"Optional agent '{name}' failed: {result.error}")

        duration = time.time() - start_time
        success = not self._failed_required and not errors

        # Log summary
        self._log_summary(success, duration, waves_executed)

        return OrchestrationResult(
            success=success,
            results=self._results,
            duration_seconds=duration,
            waves_executed=waves_executed,
            errors=errors,
            warnings=warnings,
        )

    async def _execute_dag(self, context: Dict[str, Any]) -> int:
        """Execute agents following DAG dependencies."""
        return await asyncio.wait_for(
            self._execute_dag_inner(context),
            timeout=self.config.timeout_global,
        )

    async def _execute_dag_inner(self, context: Dict[str, Any]) -> int:
        """Inner DAG execution without timeout wrapper."""
        waves = 0

        while not self._should_stop():
            # Find agents ready to run
            runnable = self._dag.find_runnable(self._completed, self._skipped)

            if not runnable:
                if len(self._completed) + len(self._skipped) < len(self._dag):
                    # Some agents not processed - shouldn't happen with valid DAG
                    logger.error("DAG execution stuck - no runnable agents")
                    break
                break  # All done

            # Execute wave
            logger.info(f"Wave {waves + 1}: executing {runnable}")
            await self._execute_wave(runnable, context)
            waves += 1

        return waves

    async def _execute_sequential(self, context: Dict[str, Any]) -> int:
        """Execute agents one by one in topological order."""
        return await asyncio.wait_for(
            self._execute_sequential_inner(context),
            timeout=self.config.timeout_global,
        )

    async def _execute_sequential_inner(self, context: Dict[str, Any]) -> int:
        """Inner sequential execution without timeout wrapper."""
        order = self._dag.topological_sort()
        waves = 0

        for agent_name in order:
            if self._should_stop():
                break

            logger.info(f"Sequential: executing {agent_name}")
            await self._execute_wave([agent_name], context)
            waves += 1

        return waves

    async def _execute_parallel(self, context: Dict[str, Any]) -> int:
        """Execute all agents in parallel (ignore DAG)."""
        return await asyncio.wait_for(
            self._execute_parallel_inner(context),
            timeout=self.config.timeout_global,
        )

    async def _execute_parallel_inner(self, context: Dict[str, Any]) -> int:
        """Inner parallel execution without timeout wrapper."""
        all_agents = list(self._dag.agents.keys())
        logger.info(f"Parallel: executing all {len(all_agents)} agents")
        await self._execute_wave(all_agents, context)
        return 1  # Single wave

    async def _execute_wave(self, agents: List[str], context: Dict[str, Any]) -> None:
        """
        Execute a wave of agents in parallel.

        Args:
            agents: List of agent names to execute
            context: Execution context
        """
        tasks = []

        for agent_name in agents:
            agent_config = self.config.get_agent(agent_name)
            if not agent_config:
                logger.warning(f"Agent config not found: {agent_name}")
                continue

            # Create runner
            runner = AgentRunner(agent_config, self.executor)

            # Run pre-agent hook
            if self.hook_runner:
                try:
                    await self._run_hook("pre-agent", agent_name, context)
                except Exception as e:
                    logger.warning(f"Pre-agent hook failed for {agent_name}: {e}")

            # Schedule execution
            tasks.append(self._run_agent_with_hook(runner, agent_name, context))

        # Execute all agents in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for agent_name, result in zip(agents, results):
            self._handle_result(agent_name, result)

    async def _run_agent_with_hook(
        self,
        runner: AgentRunner,
        agent_name: str,
        context: Dict[str, Any],
    ) -> AgentResult:
        """Run agent and post-agent hook."""
        result = await runner.run(context)

        # Run post-agent hook
        if self.hook_runner:
            try:
                hook_context = {**context, "agent_result": result.to_dict()}
                await self._run_hook("post-agent", agent_name, hook_context)
            except Exception as e:
                logger.warning(f"Post-agent hook failed for {agent_name}: {e}")

        return result

    async def _run_hook(
        self,
        hook_type: str,
        agent_name: str,
        context: Dict[str, Any],
    ) -> None:
        """Run a hook if hook_runner is configured."""
        if not self.hook_runner:
            return

        hook_context = {
            **context,
            "hook_type": hook_type,
            "agent_name": agent_name,
        }

        if asyncio.iscoroutinefunction(self.hook_runner):
            await self.hook_runner(hook_type, hook_context)
        else:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.hook_runner, hook_type, hook_context)

    def _handle_result(self, agent_name: str, result: Any) -> None:
        """
        Handle the result of an agent execution.

        Args:
            agent_name: Name of the agent
            result: AgentResult or Exception
        """
        # Handle exceptions from gather
        if isinstance(result, Exception):
            result = AgentResult(
                agent_name=agent_name,
                status=AgentStatus.FAILED,
                error=str(result),
            )

        self._results[agent_name] = result
        agent_config = self.config.get_agent(agent_name)

        if result.is_skipped:
            self._skipped.add(agent_name)
            logger.info(f"Agent {agent_name} skipped")

        elif result.is_success:
            self._completed.add(agent_name)
            logger.info(
                f"Agent {agent_name} completed: {result.verdict} "
                f"({result.duration_seconds:.2f}s)"
            )

        elif result.is_failure:
            if agent_config and agent_config.required:
                self._failed_required = True
                logger.error(
                    f"Required agent {agent_name} failed: {result.error}"
                )
                raise RequiredAgentFailedError(agent_name, result)
            else:
                # Optional agent failed - continue with warning
                self._completed.add(agent_name)  # Treat as "done" for DAG
                logger.warning(
                    f"Optional agent {agent_name} failed: {result.error}"
                )

    def _should_stop(self) -> bool:
        """Check if orchestration should stop."""
        return self._failed_required or self._stop_requested

    def stop(self) -> None:
        """Request orchestration to stop after current wave."""
        self._stop_requested = True
        logger.info("Orchestration stop requested")

    def _log_summary(
        self,
        success: bool,
        duration: float,
        waves: int,
    ) -> None:
        """Log orchestration summary."""
        status = "SUCCESS" if success else "FAILED"
        completed = len(self._completed)
        skipped = len(self._skipped)
        total = len(self._dag)

        logger.info(
            f"Orchestration {status}: "
            f"{completed}/{total} completed, {skipped} skipped, "
            f"{waves} waves, {duration:.2f}s"
        )

        # Log verdict summary
        verdicts = {}
        for result in self._results.values():
            v = result.verdict or "UNKNOWN"
            verdicts[v] = verdicts.get(v, 0) + 1

        if verdicts:
            verdict_str = ", ".join(f"{k}: {v}" for k, v in verdicts.items())
            logger.info(f"Verdicts: {verdict_str}")


async def run_orchestration(
    config_path: str,
    context: Dict[str, Any],
    executor: Optional[AgentExecutor] = None,
    hook_runner: Optional[Callable] = None,
) -> OrchestrationResult:
    """
    Convenience function to run orchestration from a config file.

    Args:
        config_path: Path to YAML configuration file
        context: Execution context
        executor: Optional agent executor function
        hook_runner: Optional hook runner function

    Returns:
        OrchestrationResult
    """
    config = load_config(config_path)
    orchestrator = Orchestrator(config, executor, hook_runner)
    return await orchestrator.execute(context)
