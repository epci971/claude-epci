"""
Tests for Wave Planner Module (F11)

Tests WavePlanner and WavePlan functionality.
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.wave_planner import (
    WavePlanner,
    WavePlan,
    PlannerInput,
    create_wave_plan,
)
from orchestration.config import get_default_wave_config


class TestPlannerInput:
    """Tests for PlannerInput dataclass."""

    def test_create_input(self):
        input_data = PlannerInput(
            feature_slug="test-feature",
            tasks=[{"name": "task1"}, {"name": "task2"}],
            complexity="LARGE",
            strategy="progressive",
        )
        assert input_data.feature_slug == "test-feature"
        assert len(input_data.tasks) == 2
        assert input_data.complexity == "LARGE"
        assert input_data.strategy == "progressive"
        assert input_data.safe_mode is False

    def test_to_task_list(self):
        input_data = PlannerInput(
            feature_slug="test",
            tasks=[
                {"name": "create_entity", "file_path": "src/entity.py", "estimated_minutes": 10},
                {"name": "create_service", "action": "modify", "estimated_minutes": 15},
            ],
        )
        tasks = input_data.to_task_list()

        assert len(tasks) == 2
        assert tasks[0].name == "create_entity"
        assert tasks[0].file_path == "src/entity.py"
        assert tasks[0].estimated_minutes == 10
        assert tasks[1].action == "modify"


class TestWavePlan:
    """Tests for WavePlan dataclass."""

    @pytest.fixture
    def sample_plan(self):
        from orchestration.wave_context import Wave, WaveStatus
        return WavePlan(
            feature_slug="test-feature",
            complexity="LARGE",
            strategy_name="progressive",
            waves=[
                Wave(wave_id="w1", name="Wave 1", order=1, tasks=["t1", "t2"]),
                Wave(wave_id="w2", name="Wave 2", order=2, tasks=["t3"]),
            ],
            total_tasks=3,
            estimated_duration_minutes=30,
            safe_mode=True,
        )

    def test_wave_count(self, sample_plan):
        assert sample_plan.wave_count == 2

    def test_get_wave(self, sample_plan):
        wave = sample_plan.get_wave("w1")
        assert wave is not None
        assert wave.name == "Wave 1"

        missing = sample_plan.get_wave("nonexistent")
        assert missing is None

    def test_get_wave_by_order(self, sample_plan):
        wave = sample_plan.get_wave_by_order(2)
        assert wave is not None
        assert wave.wave_id == "w2"

    def test_to_dict(self, sample_plan):
        d = sample_plan.to_dict()
        assert d["feature_slug"] == "test-feature"
        assert d["strategy_name"] == "progressive"
        assert d["wave_count"] == 2
        assert len(d["waves"]) == 2

    def test_summary(self, sample_plan):
        summary = sample_plan.summary()
        assert "test-feature" in summary
        assert "progressive" in summary
        assert "2" in summary  # wave count


class TestWavePlanner:
    """Tests for WavePlanner class."""

    @pytest.fixture
    def planner(self):
        return WavePlanner()

    @pytest.fixture
    def sample_input(self):
        return PlannerInput(
            feature_slug="user-auth",
            tasks=[
                {"name": "create_user_entity", "estimated_minutes": 10},
                {"name": "create_auth_service", "estimated_minutes": 15},
                {"name": "create_login_controller", "estimated_minutes": 10},
                {"name": "create_auth_tests", "estimated_minutes": 20},
            ],
            complexity="LARGE",
            strategy="progressive",
            safe_mode=True,
        )

    def test_plan_creates_wave_plan(self, planner, sample_input):
        plan = planner.plan(sample_input)

        assert isinstance(plan, WavePlan)
        assert plan.feature_slug == "user-auth"
        assert plan.complexity == "LARGE"
        assert plan.strategy_name == "progressive"
        assert plan.safe_mode is True

    def test_plan_assigns_all_tasks(self, planner, sample_input):
        plan = planner.plan(sample_input)

        total_assigned = sum(len(w.tasks) for w in plan.waves)
        assert total_assigned == len(sample_input.tasks)

    def test_plan_estimates_duration(self, planner, sample_input):
        plan = planner.plan(sample_input)

        # Duration should be sum of all task estimates
        expected = 10 + 15 + 10 + 20  # 55 minutes
        assert plan.estimated_duration_minutes == expected

    def test_plan_with_systematic_strategy(self, planner):
        input_data = PlannerInput(
            feature_slug="test",
            tasks=[{"name": "task1"}, {"name": "task2"}],
            strategy="systematic",
        )
        plan = planner.plan(input_data)

        assert plan.strategy_name == "systematic"
        # Systematic should have analysis and validation waves
        wave_ids = [w.wave_id for w in plan.waves]
        assert "analysis" in wave_ids
        assert "validation" in wave_ids

    def test_get_strategy_caches(self, planner):
        strategy1 = planner.get_strategy("progressive")
        strategy2 = planner.get_strategy("progressive")

        assert strategy1 is strategy2  # Same instance

    def test_suggest_strategy_uncertain(self, planner):
        tasks = [
            {"name": "research_auth_options"},
            {"name": "investigate_jwt_library"},
        ]
        suggestion = planner.suggest_strategy(tasks, "LARGE")

        assert suggestion == "progressive"  # Uncertainty -> progressive

    def test_suggest_strategy_complex_deps(self, planner):
        tasks = [
            {"name": "task1", "dependencies": ["dep1", "dep2", "dep3", "dep4"]},
        ]
        suggestion = planner.suggest_strategy(tasks, "LARGE")

        assert suggestion == "progressive"  # Complex deps -> progressive

    def test_suggest_strategy_large_confident(self, planner):
        tasks = [{"name": f"task{i}"} for i in range(15)]
        suggestion = planner.suggest_strategy(tasks, "LARGE")

        assert suggestion == "systematic"  # Large + no uncertainty -> systematic


class TestCreateWavePlan:
    """Tests for create_wave_plan convenience function."""

    def test_create_plan(self):
        tasks = [
            {"name": "task1", "estimated_minutes": 10},
            {"name": "task2", "estimated_minutes": 15},
        ]
        plan = create_wave_plan(
            feature_slug="quick-test",
            tasks=tasks,
            strategy="progressive",
            safe_mode=False,
        )

        assert plan.feature_slug == "quick-test"
        assert plan.total_tasks == 2
        assert plan.safe_mode is False

    def test_create_plan_with_config(self):
        config = get_default_wave_config()
        tasks = [{"name": "task1"}]

        plan = create_wave_plan(
            feature_slug="config-test",
            tasks=tasks,
            config=config,
        )

        assert plan.config is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
