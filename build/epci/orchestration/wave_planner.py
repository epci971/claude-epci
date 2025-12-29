"""
Wave Planner Module (F11)

Plans wave execution for LARGE features by analyzing tasks
and organizing them into waves using configurable strategies.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import WaveConfig, WaveStrategyType, get_default_wave_config
from .wave_context import Wave, WaveContext
from .strategies import get_strategy, Task, StrategyResult, WaveStrategy


logger = logging.getLogger(__name__)


@dataclass
class PlannerInput:
    """Input for wave planning."""
    feature_slug: str
    tasks: List[Dict[str, Any]]
    complexity: str = "LARGE"
    strategy: str = "progressive"
    safe_mode: bool = False

    def to_task_list(self) -> List[Task]:
        """Convert raw task dictionaries to Task objects."""
        return [
            Task(
                name=t.get("name", f"task_{i}"),
                file_path=t.get("file_path"),
                action=t.get("action", "create"),
                estimated_minutes=t.get("estimated_minutes", 10),
                dependencies=t.get("dependencies", []),
            )
            for i, t in enumerate(self.tasks)
        ]


@dataclass
class WavePlan:
    """Complete wave execution plan."""
    feature_slug: str
    complexity: str
    strategy_name: str
    waves: List[Wave]
    total_tasks: int
    estimated_duration_minutes: int
    safe_mode: bool = False
    config: Optional[WaveConfig] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def wave_count(self) -> int:
        return len(self.waves)

    def get_wave(self, wave_id: str) -> Optional[Wave]:
        """Get wave by ID."""
        return next((w for w in self.waves if w.wave_id == wave_id), None)

    def get_wave_by_order(self, order: int) -> Optional[Wave]:
        """Get wave by execution order."""
        return next((w for w in self.waves if w.order == order), None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary for serialization."""
        return {
            "feature_slug": self.feature_slug,
            "complexity": self.complexity,
            "strategy_name": self.strategy_name,
            "waves": [w.to_dict() for w in self.waves],
            "total_tasks": self.total_tasks,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "wave_count": self.wave_count,
            "safe_mode": self.safe_mode,
            "metadata": self.metadata,
        }

    def summary(self) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"Wave Plan: {self.feature_slug}",
            f"  Strategy: {self.strategy_name}",
            f"  Waves: {self.wave_count}",
            f"  Tasks: {self.total_tasks}",
            f"  Duration: ~{self.estimated_duration_minutes} min",
            f"  Safe mode: {'Yes' if self.safe_mode else 'No'}",
            "",
        ]

        for wave in self.waves:
            lines.append(f"  [{wave.order}] {wave.name}: {len(wave.tasks)} tasks")

        return "\n".join(lines)


class WavePlanner:
    """
    Plans wave execution for features.

    Analyzes tasks and creates an optimal execution plan
    using the configured strategy.

    Usage:
        planner = WavePlanner()
        plan = planner.plan(input_data)
    """

    def __init__(self, config: Optional[WaveConfig] = None):
        """
        Initialize the wave planner.

        Args:
            config: Optional wave configuration. Uses defaults if not provided.
        """
        self.config = config or get_default_wave_config()
        self._strategies: Dict[str, WaveStrategy] = {}

    def get_strategy(self, strategy_name: str) -> WaveStrategy:
        """Get or create a strategy instance."""
        if strategy_name not in self._strategies:
            self._strategies[strategy_name] = get_strategy(strategy_name)
        return self._strategies[strategy_name]

    def plan(self, input_data: PlannerInput) -> WavePlan:
        """
        Create a wave execution plan.

        Args:
            input_data: Planning input with tasks and configuration

        Returns:
            WavePlan ready for execution
        """
        logger.info(f"Planning waves for feature: {input_data.feature_slug}")
        logger.info(f"Strategy: {input_data.strategy}, Tasks: {len(input_data.tasks)}")

        # Get strategy
        strategy = self.get_strategy(input_data.strategy)

        # Convert to Task objects
        tasks = input_data.to_task_list()

        # Create initial context
        context = WaveContext(
            wave_number=0,
            feature_slug=input_data.feature_slug,
            complexity=input_data.complexity,
        )

        # Plan waves using strategy
        result = strategy.plan_waves(tasks, context)

        # Create plan
        plan = WavePlan(
            feature_slug=input_data.feature_slug,
            complexity=input_data.complexity,
            strategy_name=strategy.name,
            waves=result.waves,
            total_tasks=result.total_tasks,
            estimated_duration_minutes=result.estimated_duration_minutes,
            safe_mode=input_data.safe_mode,
            config=self.config,
            metadata=result.metadata,
        )

        logger.info(f"Plan created: {plan.wave_count} waves, ~{plan.estimated_duration_minutes} min")

        return plan

    def plan_from_feature_doc(
        self,
        feature_doc_path: str,
        strategy: str = "progressive",
        safe_mode: bool = False,
    ) -> WavePlan:
        """
        Create a wave plan from a Feature Document.

        Parses the Feature Document to extract tasks from §2.

        Args:
            feature_doc_path: Path to the Feature Document
            strategy: Strategy to use
            safe_mode: Enable breakpoints between waves

        Returns:
            WavePlan ready for execution
        """
        # Parse Feature Document
        tasks = self._parse_feature_document(feature_doc_path)

        # Extract feature slug from path
        import os
        feature_slug = os.path.splitext(os.path.basename(feature_doc_path))[0]

        input_data = PlannerInput(
            feature_slug=feature_slug,
            tasks=tasks,
            complexity="LARGE",  # Waves are typically for LARGE features
            strategy=strategy,
            safe_mode=safe_mode,
        )

        return self.plan(input_data)

    def _parse_feature_document(self, path: str) -> List[Dict[str, Any]]:
        """
        Parse tasks from a Feature Document.

        Looks for task definitions in §2 — Implementation Plan.
        """
        tasks = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Simple parsing - look for task patterns
            # Format: "1. [ ] **Task name** (X min)"
            import re
            task_pattern = r'\d+\.\s*\[[ x]\]\s*\*\*([^*]+)\*\*\s*\((\d+)\s*min\)'

            for match in re.finditer(task_pattern, content, re.IGNORECASE):
                task_name = match.group(1).strip()
                estimated_minutes = int(match.group(2))

                tasks.append({
                    "name": task_name,
                    "estimated_minutes": estimated_minutes,
                })

            logger.info(f"Parsed {len(tasks)} tasks from Feature Document")

        except FileNotFoundError:
            logger.warning(f"Feature Document not found: {path}")
        except Exception as e:
            logger.error(f"Error parsing Feature Document: {e}")

        return tasks

    def suggest_strategy(self, tasks: List[Dict[str, Any]], complexity: str) -> str:
        """
        Suggest the best strategy based on task characteristics.

        Args:
            tasks: List of tasks
            complexity: Feature complexity

        Returns:
            Suggested strategy name
        """
        # Heuristics for strategy selection
        task_count = len(tasks)

        # Check for high dependency interconnection
        has_complex_deps = any(
            len(t.get("dependencies", [])) > 2 for t in tasks
        )

        # Check for uncertainty indicators
        has_uncertainty = any(
            "research" in t.get("name", "").lower() or
            "investigate" in t.get("name", "").lower() or
            "explore" in t.get("name", "").lower()
            for t in tasks
        )

        # Progressive for uncertain or highly interdependent tasks
        if has_uncertainty or has_complex_deps:
            return "progressive"

        # Systematic for well-defined, large task sets
        if task_count > 10 and not has_uncertainty:
            return "systematic"

        # Default to progressive
        return "progressive"


def create_wave_plan(
    feature_slug: str,
    tasks: List[Dict[str, Any]],
    strategy: str = "progressive",
    safe_mode: bool = False,
    config: Optional[WaveConfig] = None,
) -> WavePlan:
    """
    Convenience function to create a wave plan.

    Args:
        feature_slug: Feature identifier
        tasks: List of task dictionaries
        strategy: Strategy name
        safe_mode: Enable breakpoints
        config: Optional wave configuration

    Returns:
        WavePlan ready for execution
    """
    planner = WavePlanner(config)
    input_data = PlannerInput(
        feature_slug=feature_slug,
        tasks=tasks,
        strategy=strategy,
        safe_mode=safe_mode,
    )
    return planner.plan(input_data)
