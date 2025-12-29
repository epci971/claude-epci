"""
Tests for Wave Strategies (F11)

Tests ProgressiveStrategy and SystematicStrategy implementations.
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.strategies import (
    get_strategy,
    Task,
    WaveStrategy,
    ProgressiveStrategy,
    SystematicStrategy,
)
from orchestration.wave_context import Wave, WaveContext, WaveStatus


class TestGetStrategy:
    """Tests for strategy factory function."""

    def test_get_progressive_strategy(self):
        strategy = get_strategy("progressive")
        assert isinstance(strategy, ProgressiveStrategy)
        assert strategy.name == "progressive"

    def test_get_systematic_strategy(self):
        strategy = get_strategy("systematic")
        assert isinstance(strategy, SystematicStrategy)
        assert strategy.name == "systematic"

    def test_get_unknown_strategy(self):
        with pytest.raises(ValueError) as exc_info:
            get_strategy("unknown")
        assert "Unknown strategy" in str(exc_info.value)

    def test_case_insensitive(self):
        strategy = get_strategy("PROGRESSIVE")
        assert isinstance(strategy, ProgressiveStrategy)


class TestTask:
    """Tests for Task dataclass."""

    def test_create_task(self):
        task = Task(
            name="create_user_entity",
            file_path="src/entity/user.py",
            action="create",
            estimated_minutes=10,
        )
        assert task.name == "create_user_entity"
        assert task.file_path == "src/entity/user.py"
        assert task.action == "create"
        assert task.estimated_minutes == 10
        assert task.dependencies == []

    def test_task_with_dependencies(self):
        task = Task(
            name="create_user_service",
            dependencies=["create_user_entity", "create_user_repository"],
        )
        assert len(task.dependencies) == 2


class TestProgressiveStrategy:
    """Tests for ProgressiveStrategy."""

    @pytest.fixture
    def strategy(self):
        return ProgressiveStrategy()

    @pytest.fixture
    def sample_tasks(self):
        return [
            Task(name="create_user_entity", estimated_minutes=10),
            Task(name="create_user_repository", estimated_minutes=10),
            Task(name="create_user_service", estimated_minutes=15),
            Task(name="create_user_handler", estimated_minutes=10),
            Task(name="create_user_controller", estimated_minutes=10),
            Task(name="create_user_api", estimated_minutes=15),
            Task(name="create_user_tests", estimated_minutes=20),
            Task(name="update_documentation", estimated_minutes=10),
        ]

    def test_strategy_properties(self, strategy):
        assert strategy.name == "progressive"
        assert "wave by wave" in strategy.description.lower()

    def test_plan_waves_creates_waves(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        assert len(result.waves) > 0
        assert result.total_tasks == len(sample_tasks)
        assert result.strategy_name == "progressive"

    def test_plan_waves_categorizes_correctly(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        # Find waves by name
        wave_names = {w.name: w for w in result.waves}

        # Entity/Repository should be in Foundations
        if "Foundations" in wave_names:
            foundations = wave_names["Foundations"]
            assert any("entity" in t for t in foundations.tasks)
            assert any("repository" in t for t in foundations.tasks)

        # Service/Handler should be in Core Logic
        if "Core Logic" in wave_names:
            core = wave_names["Core Logic"]
            assert any("service" in t for t in core.tasks)

        # Controller/API should be in Integration
        if "Integration" in wave_names:
            integration = wave_names["Integration"]
            assert any("controller" in t for t in integration.tasks)

    def test_plan_waves_orders_correctly(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        orders = [w.order for w in result.waves]
        assert orders == sorted(orders)  # Should be in ascending order

    def test_plan_waves_estimates_duration(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        expected_duration = sum(t.estimated_minutes for t in sample_tasks)
        assert result.estimated_duration_minutes == expected_duration

    def test_should_continue_after_completed_wave(self, strategy):
        wave = Wave(wave_id="test", name="Test", order=1, status=WaveStatus.COMPLETED)
        context = WaveContext()

        assert strategy.should_continue_after_wave(wave, context) is True

    def test_should_stop_after_failed_wave(self, strategy):
        wave = Wave(wave_id="test", name="Test", order=1, status=WaveStatus.FAILED)
        context = WaveContext()

        assert strategy.should_continue_after_wave(wave, context) is False

    def test_should_stop_on_critical_issues(self, strategy):
        from orchestration.wave_context import Issue

        wave = Wave(wave_id="test", name="Test", order=1, status=WaveStatus.COMPLETED)
        context = WaveContext()
        context.add_issue(Issue(severity="critical", message="Critical error"))

        assert strategy.should_continue_after_wave(wave, context) is False

    def test_empty_tasks_list(self, strategy):
        result = strategy.plan_waves([])

        assert len(result.waves) == 0
        assert result.total_tasks == 0

    def test_unmatched_tasks_go_to_finalization(self, strategy):
        tasks = [
            Task(name="random_task_xyz", estimated_minutes=5),
            Task(name="another_unknown", estimated_minutes=5),
        ]
        result = strategy.plan_waves(tasks)

        # Should have at least one wave
        assert len(result.waves) >= 1

        # All tasks should be assigned
        all_assigned = sum(len(w.tasks) for w in result.waves)
        assert all_assigned == len(tasks)


class TestSystematicStrategy:
    """Tests for SystematicStrategy."""

    @pytest.fixture
    def strategy(self):
        return SystematicStrategy()

    @pytest.fixture
    def sample_tasks(self):
        return [
            Task(name="task1", estimated_minutes=10, dependencies=[]),
            Task(name="task2", estimated_minutes=10, dependencies=["task1"]),
            Task(name="task3", estimated_minutes=10, dependencies=["task1"]),
            Task(name="task4", estimated_minutes=10, dependencies=["task2", "task3"]),
        ]

    def test_strategy_properties(self, strategy):
        assert strategy.name == "systematic"
        assert "analyze" in strategy.description.lower()

    def test_plan_waves_has_analysis_wave(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        # First wave should be analysis
        assert result.waves[0].wave_id == "analysis"
        assert result.waves[0].name == "Analysis"

    def test_plan_waves_has_validation_wave(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        # Last wave should be validation
        assert result.waves[-1].wave_id == "validation"
        assert result.waves[-1].name == "Validation"

    def test_plan_waves_respects_dependencies(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        # Get execution waves (exclude analysis and validation)
        exec_waves = [w for w in result.waves if w.wave_id.startswith("execution")]

        # task1 should be in earlier wave than task4
        task1_wave = None
        task4_wave = None
        for wave in exec_waves:
            if "task1" in wave.tasks:
                task1_wave = wave.order
            if "task4" in wave.tasks:
                task4_wave = wave.order

        if task1_wave and task4_wave:
            assert task1_wave < task4_wave

    def test_plan_waves_metadata(self, strategy, sample_tasks):
        result = strategy.plan_waves(sample_tasks)

        assert result.metadata["analysis_first"] is True
        assert result.metadata["batch_execution"] is True

    def test_should_continue_after_analysis_failure(self, strategy):
        wave = Wave(wave_id="analysis", name="Analysis", order=1, status=WaveStatus.FAILED)
        context = WaveContext()

        # Analysis failure should stop everything
        assert strategy.should_continue_after_wave(wave, context) is False

    def test_should_continue_after_execution_failure_non_critical(self, strategy):
        wave = Wave(wave_id="execution_1", name="Execution", order=2, status=WaveStatus.FAILED)
        context = WaveContext()

        # Non-critical execution failure may continue
        assert strategy.should_continue_after_wave(wave, context) is True

    def test_max_tasks_per_batch(self):
        strategy = SystematicStrategy(max_tasks_per_batch=2)
        tasks = [Task(name=f"task{i}", estimated_minutes=5) for i in range(10)]

        result = strategy.plan_waves(tasks)

        # Execution waves should respect batch size
        exec_waves = [w for w in result.waves if w.wave_id.startswith("execution")]
        for wave in exec_waves:
            assert len(wave.tasks) <= 2


class TestStrategyHelpers:
    """Tests for strategy helper methods."""

    def test_filter_tasks_by_pattern(self):
        strategy = ProgressiveStrategy()
        tasks = [
            Task(name="create_entity"),
            Task(name="update_service"),
            Task(name="entity_validation"),
            Task(name="other_task"),
        ]

        filtered = strategy.filter_tasks_by_pattern(tasks, ["entity"])

        assert len(filtered) == 2
        assert all("entity" in t.name for t in filtered)

    def test_calculate_wave_duration(self):
        strategy = ProgressiveStrategy()
        tasks = [
            Task(name="task1", estimated_minutes=10),
            Task(name="task2", estimated_minutes=15),
            Task(name="task3", estimated_minutes=5),
        ]

        duration = strategy.calculate_wave_duration(tasks)

        assert duration == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
