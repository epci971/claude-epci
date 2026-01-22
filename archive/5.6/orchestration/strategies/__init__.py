"""
Wave Strategies Package (F11)

Provides strategy implementations for wave-based orchestration.

Strategies:
    - ProgressiveStrategy: Execute wave by wave with validation between each
    - SystematicStrategy: Analyze all waves first, then execute in batches

Usage:
    from orchestration.strategies import ProgressiveStrategy, get_strategy

    strategy = get_strategy("progressive")
    result = strategy.plan_waves(tasks)
"""

from .base import WaveStrategy, Task, StrategyResult
from .progressive import ProgressiveStrategy
from .systematic import SystematicStrategy


def get_strategy(strategy_name: str) -> WaveStrategy:
    """
    Get a strategy instance by name.

    Args:
        strategy_name: Name of the strategy ("progressive" or "systematic")

    Returns:
        WaveStrategy instance

    Raises:
        ValueError: If strategy name is unknown
    """
    strategies = {
        "progressive": ProgressiveStrategy,
        "systematic": SystematicStrategy,
    }

    if strategy_name.lower() not in strategies:
        raise ValueError(
            f"Unknown strategy: {strategy_name}. "
            f"Available: {list(strategies.keys())}"
        )

    return strategies[strategy_name.lower()]()


__all__ = [
    "WaveStrategy",
    "Task",
    "StrategyResult",
    "ProgressiveStrategy",
    "SystematicStrategy",
    "get_strategy",
]
