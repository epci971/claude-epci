"""
Progressive Wave Strategy (F11)

Executes waves sequentially with validation between each wave.
This strategy is ideal for uncertain requirements or when
frequent feedback is needed.

Wave Order:
    1. Foundations: Entities, repositories, base classes, config
    2. Core Logic: Services, handlers, business logic
    3. Integration: Controllers, APIs, external integrations
    4. Finalization: Tests, documentation, cleanup
"""

from typing import List, Optional

from .base import WaveStrategy, Task, StrategyResult
from ..wave_context import Wave, WaveContext, WaveStatus


# Default wave definitions for progressive strategy
PROGRESSIVE_WAVES = {
    "foundations": {
        "name": "Foundations",
        "order": 1,
        "patterns": ["entity", "repository", "base", "config", "model", "schema", "interface", "type", "enum"],
    },
    "core": {
        "name": "Core Logic",
        "order": 2,
        "patterns": ["service", "handler", "logic", "processor", "manager", "validator", "factory"],
    },
    "integration": {
        "name": "Integration",
        "order": 3,
        "patterns": ["controller", "api", "integration", "adapter", "client", "gateway", "endpoint"],
    },
    "finalization": {
        "name": "Finalization",
        "order": 4,
        "patterns": ["test", "doc", "migration", "cleanup", "readme", "changelog"],
    },
}


class ProgressiveStrategy(WaveStrategy):
    """
    Progressive strategy: Execute wave by wave with validation.

    Features:
        - Validates output after each wave before proceeding
        - Accumulates context progressively
        - Allows early exit if critical issues are found
        - Supports breakpoints for user validation (with --safe flag)
    """

    def __init__(self, wave_definitions: dict = None):
        """
        Initialize progressive strategy.

        Args:
            wave_definitions: Optional custom wave definitions.
                             Uses PROGRESSIVE_WAVES by default.
        """
        self.wave_definitions = wave_definitions or PROGRESSIVE_WAVES

    @property
    def name(self) -> str:
        return "progressive"

    @property
    def description(self) -> str:
        return "Execute wave by wave with validation between each"

    def plan_waves(
        self,
        tasks: List[Task],
        context: Optional[WaveContext] = None,
    ) -> StrategyResult:
        """
        Plan waves by categorizing tasks into architectural layers.

        Tasks are assigned to waves based on pattern matching:
        - "entity", "repository" -> Foundations
        - "service", "handler" -> Core Logic
        - "controller", "api" -> Integration
        - "test", "doc" -> Finalization

        Tasks not matching any pattern are assigned to Finalization.
        """
        waves = []
        assigned_tasks = set()
        total_duration = 0

        # Create waves in order
        for wave_id, wave_def in sorted(
            self.wave_definitions.items(),
            key=lambda x: x[1]["order"]
        ):
            wave_tasks = self._match_tasks_to_wave(tasks, wave_def["patterns"], assigned_tasks)

            if wave_tasks:  # Only create wave if it has tasks
                wave = Wave(
                    wave_id=wave_id,
                    name=wave_def["name"],
                    order=wave_def["order"],
                    tasks=[t.name for t in wave_tasks],
                    status=WaveStatus.PENDING,
                )
                waves.append(wave)
                assigned_tasks.update(t.name for t in wave_tasks)
                total_duration += self.calculate_wave_duration(wave_tasks)

        # Assign unmatched tasks to finalization wave
        unmatched = [t for t in tasks if t.name not in assigned_tasks]
        if unmatched:
            # Find or create finalization wave
            final_wave = next((w for w in waves if w.wave_id == "finalization"), None)
            if final_wave:
                final_wave.tasks.extend(t.name for t in unmatched)
            else:
                waves.append(Wave(
                    wave_id="finalization",
                    name="Finalization",
                    order=len(waves) + 1,
                    tasks=[t.name for t in unmatched],
                    status=WaveStatus.PENDING,
                ))
            total_duration += self.calculate_wave_duration(unmatched)

        return StrategyResult(
            waves=waves,
            total_tasks=len(tasks),
            estimated_duration_minutes=total_duration,
            strategy_name=self.name,
            metadata={
                "wave_count": len(waves),
                "validation_between_waves": True,
                "context_accumulation": True,
            },
        )

    def _match_tasks_to_wave(
        self,
        tasks: List[Task],
        patterns: List[str],
        already_assigned: set,
    ) -> List[Task]:
        """Match tasks to a wave based on patterns."""
        matched = []
        for task in tasks:
            if task.name in already_assigned:
                continue
            task_lower = task.name.lower()
            if any(pattern in task_lower for pattern in patterns):
                matched.append(task)
        return matched

    def should_continue_after_wave(
        self,
        wave: Wave,
        context: WaveContext,
    ) -> bool:
        """
        Determine if execution should continue after wave completion.

        Stops execution if:
        - Wave failed
        - Critical issues found in context
        - All remaining waves have no tasks

        Args:
            wave: The completed wave
            context: Current accumulated context

        Returns:
            True to continue, False to stop
        """
        # Stop if wave failed
        if wave.is_failed:
            return False

        # Stop if critical issues found
        critical_issues = context.get_critical_issues()
        if critical_issues:
            return False

        return True

    def get_wave_summary(self, result: StrategyResult) -> str:
        """Generate a human-readable summary of planned waves."""
        lines = [
            f"Progressive Strategy: {len(result.waves)} waves planned",
            f"Total tasks: {result.total_tasks}",
            f"Estimated duration: {result.estimated_duration_minutes} minutes",
            "",
        ]

        for wave in result.waves:
            lines.append(f"  Wave {wave.order}: {wave.name}")
            lines.append(f"    Tasks: {len(wave.tasks)}")
            if wave.tasks[:3]:  # Show first 3 tasks
                for task in wave.tasks[:3]:
                    lines.append(f"      - {task}")
                if len(wave.tasks) > 3:
                    lines.append(f"      ... and {len(wave.tasks) - 3} more")

        return "\n".join(lines)
