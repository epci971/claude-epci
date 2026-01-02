"""
Wave Strategy Base Module (F11)

Defines the abstract base class for wave execution strategies.
Strategies determine how tasks are grouped into waves and executed.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..wave_context import Wave, WaveContext


@dataclass
class Task:
    """Represents a task to be executed in a wave."""
    name: str
    file_path: Optional[str] = None
    action: str = "create"  # create, modify, delete
    estimated_minutes: int = 10
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class StrategyResult:
    """Result of wave planning by a strategy."""
    waves: List[Wave]
    total_tasks: int
    estimated_duration_minutes: int
    strategy_name: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class WaveStrategy(ABC):
    """
    Abstract base class for wave execution strategies.

    Strategies determine how tasks are organized into waves
    and how execution flows between waves.

    Implementations:
        - ProgressiveStrategy: Wave-by-wave with validation between each
        - SystematicStrategy: Analyze all first, then batch execution
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the strategy name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of the strategy."""
        pass

    @abstractmethod
    def plan_waves(
        self,
        tasks: List[Task],
        context: Optional[WaveContext] = None,
    ) -> StrategyResult:
        """
        Plan how to organize tasks into waves.

        Args:
            tasks: List of tasks to be organized
            context: Optional existing context from previous execution

        Returns:
            StrategyResult containing planned waves
        """
        pass

    @abstractmethod
    def should_continue_after_wave(
        self,
        wave: Wave,
        context: WaveContext,
    ) -> bool:
        """
        Determine if execution should continue after a wave completes.

        Args:
            wave: The completed wave
            context: Current accumulated context

        Returns:
            True if execution should continue, False to stop
        """
        pass

    def filter_tasks_by_pattern(
        self,
        tasks: List[Task],
        patterns: List[str],
    ) -> List[Task]:
        """
        Filter tasks that match any of the given patterns.

        Args:
            tasks: List of tasks to filter
            patterns: Patterns to match against task names

        Returns:
            Filtered list of tasks
        """
        return [
            task for task in tasks
            if any(pattern in task.name.lower() for pattern in patterns)
        ]

    def calculate_wave_duration(self, tasks: List[Task]) -> int:
        """Calculate total estimated duration for tasks in minutes."""
        return sum(task.estimated_minutes for task in tasks)
