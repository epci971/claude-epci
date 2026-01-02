"""
Systematic Wave Strategy (F11)

Performs complete analysis of all tasks first, then executes
in optimized batches. This strategy is ideal for well-defined
features with high confidence.

Wave Structure:
    1. Analysis Wave: Analyze all tasks, dependencies, risks
    2. Execution Waves: Grouped by dependency order
    3. Validation Wave: Final validation and cleanup
"""

from typing import List, Optional, Dict, Set

from .base import WaveStrategy, Task, StrategyResult
from ..wave_context import Wave, WaveContext, WaveStatus


class SystematicStrategy(WaveStrategy):
    """
    Systematic strategy: Analyze all first, then batch execution.

    Features:
        - Comprehensive analysis before any execution
        - Dependency-based task grouping
        - Optimized execution batches
        - Minimal breakpoints (analysis -> execution -> validation)
    """

    def __init__(self, max_tasks_per_batch: int = 5):
        """
        Initialize systematic strategy.

        Args:
            max_tasks_per_batch: Maximum tasks per execution wave
        """
        self.max_tasks_per_batch = max_tasks_per_batch

    @property
    def name(self) -> str:
        return "systematic"

    @property
    def description(self) -> str:
        return "Analyze all waves first, then execute in batches"

    def plan_waves(
        self,
        tasks: List[Task],
        context: Optional[WaveContext] = None,
    ) -> StrategyResult:
        """
        Plan waves using dependency-based batching.

        Creates:
        1. Analysis wave (always first)
        2. Execution waves (grouped by dependencies)
        3. Validation wave (always last)
        """
        waves = []
        total_duration = 0

        # Wave 1: Analysis
        analysis_wave = Wave(
            wave_id="analysis",
            name="Analysis",
            order=1,
            tasks=["analyze_all_tasks", "validate_dependencies", "assess_risks"],
            status=WaveStatus.PENDING,
        )
        waves.append(analysis_wave)
        total_duration += 15  # Fixed analysis time

        # Build dependency graph and create execution waves
        execution_batches = self._build_dependency_batches(tasks)

        for i, batch in enumerate(execution_batches, start=2):
            wave = Wave(
                wave_id=f"execution_{i-1}",
                name=f"Execution Batch {i-1}",
                order=i,
                tasks=[t.name for t in batch],
                status=WaveStatus.PENDING,
            )
            waves.append(wave)
            total_duration += self.calculate_wave_duration(batch)

        # Final wave: Validation
        validation_wave = Wave(
            wave_id="validation",
            name="Validation",
            order=len(waves) + 1,
            tasks=["run_all_tests", "validate_integration", "final_review"],
            status=WaveStatus.PENDING,
        )
        waves.append(validation_wave)
        total_duration += 20  # Fixed validation time

        return StrategyResult(
            waves=waves,
            total_tasks=len(tasks),
            estimated_duration_minutes=total_duration,
            strategy_name=self.name,
            metadata={
                "wave_count": len(waves),
                "analysis_first": True,
                "batch_execution": True,
                "execution_batches": len(execution_batches),
            },
        )

    def _build_dependency_batches(self, tasks: List[Task]) -> List[List[Task]]:
        """
        Build execution batches based on task dependencies.

        Uses topological sorting to ensure dependencies are
        executed before dependents.
        """
        if not tasks:
            return []

        # Build dependency graph
        task_map: Dict[str, Task] = {t.name: t for t in tasks}
        in_degree: Dict[str, int] = {t.name: 0 for t in tasks}
        dependents: Dict[str, List[str]] = {t.name: [] for t in tasks}

        for task in tasks:
            for dep in task.dependencies:
                if dep in task_map:
                    in_degree[task.name] += 1
                    dependents[dep].append(task.name)

        # Topological sort into batches
        batches: List[List[Task]] = []
        remaining: Set[str] = set(t.name for t in tasks)

        while remaining:
            # Find all tasks with no remaining dependencies
            ready = [
                name for name in remaining
                if in_degree[name] == 0
            ]

            if not ready:
                # Circular dependency or isolated tasks - add remaining as single batch
                ready = list(remaining)

            # Create batch (respecting max size)
            batch_tasks = []
            for name in ready[:self.max_tasks_per_batch]:
                batch_tasks.append(task_map[name])
                remaining.remove(name)

                # Update in-degrees for dependents
                for dependent in dependents[name]:
                    if dependent in remaining:
                        in_degree[dependent] -= 1

            batches.append(batch_tasks)

        return batches

    def should_continue_after_wave(
        self,
        wave: Wave,
        context: WaveContext,
    ) -> bool:
        """
        Determine if execution should continue.

        In systematic strategy, we're more lenient:
        - Analysis failure stops everything
        - Execution failure may continue if not critical
        - Validation failure requires review but doesn't stop
        """
        if wave.is_failed:
            # Analysis failure is always critical
            if wave.wave_id == "analysis":
                return False

            # Execution failure - check for critical issues
            critical_issues = context.get_critical_issues()
            if critical_issues:
                return False

            # Non-critical execution failure - continue with warning
            return True

        return True

    def get_analysis_tasks(self) -> List[str]:
        """Get the list of analysis tasks performed in the first wave."""
        return [
            "analyze_all_tasks",
            "validate_dependencies",
            "identify_patterns",
            "assess_risks",
            "estimate_complexity",
        ]

    def get_validation_tasks(self) -> List[str]:
        """Get the list of validation tasks performed in the final wave."""
        return [
            "run_all_tests",
            "validate_integration",
            "check_coverage",
            "final_review",
        ]

    def get_wave_summary(self, result: StrategyResult) -> str:
        """Generate a human-readable summary of planned waves."""
        lines = [
            f"Systematic Strategy: {len(result.waves)} waves planned",
            f"Total tasks: {result.total_tasks}",
            f"Estimated duration: {result.estimated_duration_minutes} minutes",
            "",
            "Wave Structure:",
            f"  1. Analysis (preparation)",
            f"  2-{len(result.waves)-1}. Execution batches ({result.metadata.get('execution_batches', 0)} batches)",
            f"  {len(result.waves)}. Validation (final checks)",
        ]

        return "\n".join(lines)
