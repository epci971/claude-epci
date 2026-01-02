"""
Wave Orchestrator Module (F11)

Executes wave plans with context accumulation and optional breakpoints.
Integrates with the existing Orchestrator for agent execution within waves.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .config import WaveConfig, get_default_wave_config
from .wave_context import Wave, WaveContext, WaveStatus, TaskResult, Issue
from .wave_planner import WavePlan
from .strategies import get_strategy


logger = logging.getLogger(__name__)


@dataclass
class WaveExecutionResult:
    """Result of executing a single wave."""
    wave: Wave
    context: WaveContext
    success: bool
    duration_seconds: float = 0.0
    error: Optional[str] = None
    breakpoint_requested: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_id": self.wave.wave_id,
            "wave_name": self.wave.name,
            "success": self.success,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
            "breakpoint_requested": self.breakpoint_requested,
            "context_summary": self.context.summary(),
        }


@dataclass
class WaveOrchestrationResult:
    """Complete result of wave orchestration."""
    success: bool
    plan: WavePlan
    wave_results: List[WaveExecutionResult] = field(default_factory=list)
    final_context: Optional[WaveContext] = None
    total_duration_seconds: float = 0.0
    waves_completed: int = 0
    waves_failed: int = 0
    stopped_at_wave: Optional[str] = None
    stop_reason: Optional[str] = None

    @property
    def waves_total(self) -> int:
        return self.plan.wave_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "feature_slug": self.plan.feature_slug,
            "strategy": self.plan.strategy_name,
            "total_duration_seconds": self.total_duration_seconds,
            "waves_completed": self.waves_completed,
            "waves_failed": self.waves_failed,
            "waves_total": self.waves_total,
            "stopped_at_wave": self.stopped_at_wave,
            "stop_reason": self.stop_reason,
            "wave_results": [r.to_dict() for r in self.wave_results],
            "final_context": self.final_context.to_dict() if self.final_context else None,
        }

    def summary(self) -> str:
        """Generate execution summary."""
        status = "SUCCESS" if self.success else "FAILED"
        lines = [
            f"Wave Orchestration: {status}",
            f"  Feature: {self.plan.feature_slug}",
            f"  Strategy: {self.plan.strategy_name}",
            f"  Duration: {self.total_duration_seconds:.1f}s",
            f"  Waves: {self.waves_completed}/{self.waves_total} completed",
        ]

        if self.stopped_at_wave:
            lines.append(f"  Stopped at: {self.stopped_at_wave}")
            lines.append(f"  Reason: {self.stop_reason}")

        if self.final_context:
            lines.append("")
            lines.append(self.final_context.summary())

        return "\n".join(lines)


# Type for breakpoint callback
BreakpointCallback = Callable[[Wave, WaveContext], bool]

# Type for task executor
TaskExecutor = Callable[[str, WaveContext], TaskResult]


class WaveOrchestrator:
    """
    Executes wave plans with context accumulation.

    Handles:
    - Sequential wave execution
    - Context accumulation between waves
    - Optional breakpoints for user validation
    - Integration with hook system

    Usage:
        orchestrator = WaveOrchestrator()
        result = await orchestrator.execute(plan)
    """

    def __init__(
        self,
        config: Optional[WaveConfig] = None,
        task_executor: Optional[TaskExecutor] = None,
        breakpoint_callback: Optional[BreakpointCallback] = None,
        hook_runner: Optional[Callable] = None,
    ):
        """
        Initialize the wave orchestrator.

        Args:
            config: Wave configuration
            task_executor: Function to execute individual tasks
            breakpoint_callback: Function called at breakpoints, returns True to continue
            hook_runner: Function to execute hooks
        """
        self.config = config or get_default_wave_config()
        self.task_executor = task_executor or self._default_task_executor
        self.breakpoint_callback = breakpoint_callback
        self.hook_runner = hook_runner
        self._stop_requested = False

    async def execute(self, plan: WavePlan) -> WaveOrchestrationResult:
        """
        Execute a wave plan.

        Args:
            plan: The wave plan to execute

        Returns:
            WaveOrchestrationResult with complete execution details
        """
        logger.info(f"Starting wave orchestration: {plan.feature_slug}")
        logger.info(f"Strategy: {plan.strategy_name}, Waves: {plan.wave_count}")

        start_time = time.time()
        wave_results: List[WaveExecutionResult] = []
        context = WaveContext(
            wave_number=0,
            feature_slug=plan.feature_slug,
            complexity=plan.complexity,
            started_at=datetime.now(),
        )

        self._stop_requested = False
        stopped_at = None
        stop_reason = None
        waves_failed = 0

        # Get strategy for continuation decisions
        strategy = get_strategy(plan.strategy_name)

        # Execute waves sequentially
        for wave in plan.waves:
            if self._stop_requested:
                stopped_at = wave.wave_id
                stop_reason = "Stop requested"
                break

            # Execute pre-wave hook
            await self._run_hook("pre-wave", wave, context)

            # Execute wave
            result = await self._execute_wave(wave, context, plan)
            wave_results.append(result)

            if not result.success:
                waves_failed += 1

            # Update context
            context = result.context

            # Execute post-wave hook
            await self._run_hook("post-wave", wave, context)

            # Check if should continue
            if not strategy.should_continue_after_wave(wave, context):
                stopped_at = wave.wave_id
                stop_reason = "Strategy determined stop"
                logger.info(f"Stopping after wave {wave.wave_id}: strategy decision")
                break

            # Handle breakpoint (if safe mode and callback provided)
            if plan.safe_mode and self.breakpoint_callback:
                if not await self._handle_breakpoint(wave, context):
                    stopped_at = wave.wave_id
                    stop_reason = "User cancelled at breakpoint"
                    logger.info(f"User cancelled at breakpoint after wave {wave.wave_id}")
                    break

        total_duration = time.time() - start_time
        waves_completed = len([r for r in wave_results if r.success])
        success = waves_completed == plan.wave_count and waves_failed == 0

        result = WaveOrchestrationResult(
            success=success,
            plan=plan,
            wave_results=wave_results,
            final_context=context,
            total_duration_seconds=total_duration,
            waves_completed=waves_completed,
            waves_failed=waves_failed,
            stopped_at_wave=stopped_at,
            stop_reason=stop_reason,
        )

        logger.info(result.summary())
        return result

    async def _execute_wave(
        self,
        wave: Wave,
        context: WaveContext,
        plan: WavePlan,
    ) -> WaveExecutionResult:
        """Execute a single wave."""
        logger.info(f"Executing wave {wave.order}: {wave.name}")
        start_time = time.time()

        wave.status = WaveStatus.IN_PROGRESS
        wave.started_at = datetime.now()

        # Advance context to new wave
        new_context = context.advance_wave()

        try:
            # Execute with timeout
            timeout = plan.config.timeout_per_wave if plan.config else 300

            await asyncio.wait_for(
                self._execute_wave_tasks(wave, new_context),
                timeout=timeout,
            )

            wave.status = WaveStatus.COMPLETED
            wave.completed_at = datetime.now()
            success = True
            error = None

        except asyncio.TimeoutError:
            wave.status = WaveStatus.FAILED
            wave.completed_at = datetime.now()
            success = False
            error = f"Wave timed out after {timeout}s"
            logger.error(f"Wave {wave.wave_id} timed out")

        except Exception as e:
            wave.status = WaveStatus.FAILED
            wave.completed_at = datetime.now()
            success = False
            error = str(e)
            logger.exception(f"Wave {wave.wave_id} failed: {e}")

        duration = time.time() - start_time
        logger.info(f"Wave {wave.wave_id} {'completed' if success else 'failed'} in {duration:.1f}s")

        return WaveExecutionResult(
            wave=wave,
            context=new_context,
            success=success,
            duration_seconds=duration,
            error=error,
        )

    async def _execute_wave_tasks(
        self,
        wave: Wave,
        context: WaveContext,
    ) -> None:
        """Execute all tasks in a wave."""
        for task_name in wave.tasks:
            logger.debug(f"Executing task: {task_name}")

            # Execute task
            if asyncio.iscoroutinefunction(self.task_executor):
                result = await self.task_executor(task_name, context)
            else:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, self.task_executor, task_name, context
                )

            wave.task_results.append(result)

            # Update context with task results
            for file_path in result.files_created:
                context.add_file_created(file_path)
            for file_path in result.files_modified:
                context.add_file_modified(file_path)

            # Handle task failure
            if result.status == "failed":
                context.add_issue(Issue(
                    severity="important",
                    message=f"Task '{task_name}' failed: {result.error}",
                    source="wave_orchestrator",
                ))

    async def _handle_breakpoint(
        self,
        wave: Wave,
        context: WaveContext,
    ) -> bool:
        """
        Handle breakpoint between waves.

        Returns:
            True to continue, False to stop
        """
        if not self.breakpoint_callback:
            return True

        logger.info(f"Breakpoint after wave {wave.wave_id}")

        try:
            if asyncio.iscoroutinefunction(self.breakpoint_callback):
                return await self.breakpoint_callback(wave, context)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None, self.breakpoint_callback, wave, context
                )
        except Exception as e:
            logger.error(f"Breakpoint callback error: {e}")
            return True  # Continue on error

    async def _run_hook(
        self,
        hook_type: str,
        wave: Wave,
        context: WaveContext,
    ) -> None:
        """Run a hook if configured."""
        if not self.hook_runner:
            return

        hook_context = {
            "hook_type": hook_type,
            "wave_id": wave.wave_id,
            "wave_name": wave.name,
            "wave_order": wave.order,
            "context": context.to_dict(),
        }

        try:
            if asyncio.iscoroutinefunction(self.hook_runner):
                await self.hook_runner(hook_type, hook_context)
            else:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None, self.hook_runner, hook_type, hook_context
                )
        except Exception as e:
            logger.warning(f"Hook {hook_type} failed: {e}")

    def stop(self) -> None:
        """Request orchestration to stop after current wave."""
        self._stop_requested = True
        logger.info("Wave orchestration stop requested")

    @staticmethod
    def _default_task_executor(task_name: str, context: WaveContext) -> TaskResult:
        """Default task executor that simulates task execution."""
        logger.info(f"Executing task: {task_name}")
        return TaskResult(
            task_name=task_name,
            status="completed",
            duration_seconds=1.0,
        )


async def run_wave_orchestration(
    plan: WavePlan,
    task_executor: Optional[TaskExecutor] = None,
    breakpoint_callback: Optional[BreakpointCallback] = None,
) -> WaveOrchestrationResult:
    """
    Convenience function to run wave orchestration.

    Args:
        plan: Wave plan to execute
        task_executor: Optional custom task executor
        breakpoint_callback: Optional breakpoint handler

    Returns:
        WaveOrchestrationResult
    """
    orchestrator = WaveOrchestrator(
        config=plan.config,
        task_executor=task_executor,
        breakpoint_callback=breakpoint_callback,
    )
    return await orchestrator.execute(plan)
