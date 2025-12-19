"""
Agent Runner Module

Provides async execution wrapper for agents with timeout handling
and condition evaluation.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .config import AgentConfig


logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Status of an agent execution."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class AgentResult:
    """Result of an agent execution."""
    agent_name: str
    status: AgentStatus
    verdict: str = ""  # APPROVED, REJECTED, WARNING, N/A
    duration_seconds: float = 0.0
    output: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        """Check if agent completed successfully."""
        return self.status == AgentStatus.SUCCESS

    @property
    def is_failure(self) -> bool:
        """Check if agent failed (including timeout)."""
        return self.status in (AgentStatus.FAILED, AgentStatus.TIMEOUT)

    @property
    def is_skipped(self) -> bool:
        """Check if agent was skipped."""
        return self.status == AgentStatus.SKIPPED

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "agent_name": self.agent_name,
            "status": self.status.value,
            "verdict": self.verdict,
            "duration_seconds": self.duration_seconds,
            "output": self.output,
            "error": self.error,
        }


# Type alias for agent execution function
AgentExecutor = Callable[[str, Dict[str, Any]], Any]


class AgentRunner:
    """
    Async agent execution wrapper with timeout and condition handling.

    Usage:
        runner = AgentRunner(config, executor)
        result = await runner.run(context)
    """

    def __init__(
        self,
        config: AgentConfig,
        executor: Optional[AgentExecutor] = None,
    ):
        """
        Initialize agent runner.

        Args:
            config: Agent configuration
            executor: Optional function to execute the agent.
                      Signature: (agent_name, context) -> result
        """
        self.config = config
        self.executor = executor or self._default_executor
        self._status = AgentStatus.PENDING

    @property
    def status(self) -> AgentStatus:
        """Current agent status."""
        return self._status

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with the given context.

        Args:
            context: Execution context (files, feature info, etc.)

        Returns:
            AgentResult with status and output
        """
        # Check condition first
        if not self.evaluate_condition(context):
            logger.info(f"Agent {self.config.name} skipped: condition not met")
            return AgentResult(
                agent_name=self.config.name,
                status=AgentStatus.SKIPPED,
                verdict="N/A",
                output={"reason": f"Condition not met: {self.config.condition}"},
            )

        return await self.run_with_timeout(context)

    async def run_with_timeout(self, context: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with timeout handling.

        Args:
            context: Execution context

        Returns:
            AgentResult with status and output
        """
        self._status = AgentStatus.RUNNING
        start_time = time.time()

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self._execute(context),
                timeout=self.config.timeout,
            )

            duration = time.time() - start_time
            self._status = AgentStatus.SUCCESS

            return AgentResult(
                agent_name=self.config.name,
                status=AgentStatus.SUCCESS,
                verdict=result.get("verdict", "APPROVED"),
                duration_seconds=duration,
                output=result,
            )

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            self._status = AgentStatus.TIMEOUT
            logger.warning(
                f"Agent {self.config.name} timed out after {self.config.timeout}s"
            )

            return AgentResult(
                agent_name=self.config.name,
                status=AgentStatus.TIMEOUT,
                verdict="TIMEOUT",
                duration_seconds=duration,
                error=f"Execution timed out after {self.config.timeout} seconds",
            )

        except Exception as e:
            duration = time.time() - start_time
            self._status = AgentStatus.FAILED
            logger.error(f"Agent {self.config.name} failed: {e}")

            return AgentResult(
                agent_name=self.config.name,
                status=AgentStatus.FAILED,
                verdict="FAILED",
                duration_seconds=duration,
                error=str(e),
            )

    async def _execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent (internal)."""
        if asyncio.iscoroutinefunction(self.executor):
            return await self.executor(self.config.name, context)
        else:
            # Run sync executor in thread pool
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self.executor, self.config.name, context
            )

    def evaluate_condition(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate if the agent's condition is met.

        Args:
            context: Execution context containing evaluation data

        Returns:
            True if condition is met (or no condition), False otherwise
        """
        if not self.config.condition:
            return True  # No condition = always run

        condition = self.config.condition

        # Evaluate known conditions
        if condition == "has_sensitive_files":
            return self._check_sensitive_files(context)

        if condition.startswith("complexity >="):
            return self._check_complexity(context, condition)

        # Unknown condition - default to True with warning
        logger.warning(f"Unknown condition '{condition}' for agent {self.config.name}")
        return True

    def _check_sensitive_files(self, context: Dict[str, Any]) -> bool:
        """Check if any sensitive files are present."""
        sensitive_patterns = [
            "/auth/", "/security/", "/api/", "/password/",
            "password", "secret", "api_key", "jwt", "oauth",
        ]

        files = context.get("files", [])
        if isinstance(files, list):
            for file_path in files:
                file_str = str(file_path).lower()
                if any(pattern in file_str for pattern in sensitive_patterns):
                    return True

        return False

    def _check_complexity(self, context: Dict[str, Any], condition: str) -> bool:
        """Check if complexity meets threshold."""
        # Parse condition: "complexity >= STANDARD"
        try:
            _, threshold = condition.split(">=")
            threshold = threshold.strip().upper()
        except ValueError:
            return True

        complexity_order = ["TINY", "SMALL", "STANDARD", "LARGE"]
        current = context.get("complexity", "STANDARD").upper()

        try:
            current_idx = complexity_order.index(current)
            threshold_idx = complexity_order.index(threshold)
            return current_idx >= threshold_idx
        except ValueError:
            return True

    @staticmethod
    def _default_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Default executor that simulates agent execution."""
        logger.info(f"Executing agent: {agent_name}")
        return {
            "verdict": "APPROVED",
            "message": f"Agent {agent_name} executed successfully",
        }


class AgentRunnerPool:
    """
    Pool of agent runners for managing multiple agents.

    Provides convenience methods for creating and running multiple agents.
    """

    def __init__(self, executor: Optional[AgentExecutor] = None):
        self.executor = executor
        self._runners: Dict[str, AgentRunner] = {}

    def add_agent(self, config: AgentConfig) -> AgentRunner:
        """Add an agent to the pool."""
        runner = AgentRunner(config, self.executor)
        self._runners[config.name] = runner
        return runner

    def get_runner(self, agent_name: str) -> Optional[AgentRunner]:
        """Get runner for an agent."""
        return self._runners.get(agent_name)

    async def run_agents(
        self,
        agent_names: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, AgentResult]:
        """
        Run multiple agents in parallel.

        Args:
            agent_names: List of agent names to run
            context: Shared execution context

        Returns:
            Dict mapping agent names to results
        """
        tasks = []
        for name in agent_names:
            runner = self._runners.get(name)
            if runner:
                tasks.append(runner.run(context))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        result_dict = {}
        for name, result in zip(agent_names, results):
            if isinstance(result, Exception):
                result_dict[name] = AgentResult(
                    agent_name=name,
                    status=AgentStatus.FAILED,
                    error=str(result),
                )
            else:
                result_dict[name] = result

        return result_dict
