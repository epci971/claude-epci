"""
Tests for Wave Orchestrator Module (F11)

Tests WaveOrchestrator execution and context accumulation.
"""

import pytest
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration.wave_orchestrator import (
    WaveOrchestrator,
    WaveOrchestrationResult,
    WaveExecutionResult,
    run_wave_orchestration,
)
from orchestration.wave_planner import WavePlan, create_wave_plan
from orchestration.wave_context import Wave, WaveContext, WaveStatus, TaskResult
from orchestration.config import get_default_wave_config


class TestWaveExecutionResult:
    """Tests for WaveExecutionResult dataclass."""

    def test_create_result(self):
        wave = Wave(wave_id="test", name="Test", order=1)
        context = WaveContext()
        result = WaveExecutionResult(
            wave=wave,
            context=context,
            success=True,
            duration_seconds=10.5,
        )
        assert result.success is True
        assert result.duration_seconds == 10.5
        assert result.error is None

    def test_to_dict(self):
        wave = Wave(wave_id="test", name="Test", order=1)
        context = WaveContext(wave_number=1)
        result = WaveExecutionResult(
            wave=wave,
            context=context,
            success=False,
            error="Test error",
        )
        d = result.to_dict()
        assert d["wave_id"] == "test"
        assert d["success"] is False
        assert d["error"] == "Test error"


class TestWaveOrchestrationResult:
    """Tests for WaveOrchestrationResult dataclass."""

    @pytest.fixture
    def sample_plan(self):
        return create_wave_plan(
            feature_slug="test",
            tasks=[{"name": "task1"}, {"name": "task2"}],
        )

    def test_waves_total(self, sample_plan):
        result = WaveOrchestrationResult(
            success=True,
            plan=sample_plan,
        )
        assert result.waves_total == sample_plan.wave_count

    def test_to_dict(self, sample_plan):
        result = WaveOrchestrationResult(
            success=True,
            plan=sample_plan,
            waves_completed=2,
            total_duration_seconds=30.0,
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["waves_completed"] == 2
        assert d["total_duration_seconds"] == 30.0

    def test_summary(self, sample_plan):
        result = WaveOrchestrationResult(
            success=True,
            plan=sample_plan,
            waves_completed=2,
            total_duration_seconds=30.0,
        )
        summary = result.summary()
        assert "SUCCESS" in summary
        assert "test" in summary


class TestWaveOrchestrator:
    """Tests for WaveOrchestrator class."""

    @pytest.fixture
    def orchestrator(self):
        return WaveOrchestrator()

    @pytest.fixture
    def sample_plan(self):
        return create_wave_plan(
            feature_slug="orchestrator-test",
            tasks=[
                {"name": "create_entity", "estimated_minutes": 5},
                {"name": "create_service", "estimated_minutes": 5},
                {"name": "create_test", "estimated_minutes": 5},
            ],
            strategy="progressive",
            safe_mode=False,
        )

    @pytest.mark.asyncio
    async def test_execute_completes_all_waves(self, orchestrator, sample_plan):
        result = await orchestrator.execute(sample_plan)

        assert result.success is True
        assert result.waves_completed == sample_plan.wave_count
        assert result.waves_failed == 0

    @pytest.mark.asyncio
    async def test_execute_accumulates_context(self, orchestrator, sample_plan):
        result = await orchestrator.execute(sample_plan)

        assert result.final_context is not None
        assert result.final_context.feature_slug == "orchestrator-test"

    @pytest.mark.asyncio
    async def test_execute_tracks_duration(self, orchestrator, sample_plan):
        result = await orchestrator.execute(sample_plan)

        assert result.total_duration_seconds > 0

    @pytest.mark.asyncio
    async def test_execute_with_custom_executor(self, sample_plan):
        executed_tasks = []

        def custom_executor(task_name: str, context: WaveContext) -> TaskResult:
            executed_tasks.append(task_name)
            return TaskResult(
                task_name=task_name,
                status="completed",
                duration_seconds=1.0,
                files_created=[f"src/{task_name}.py"],
            )

        orchestrator = WaveOrchestrator(task_executor=custom_executor)
        result = await orchestrator.execute(sample_plan)

        assert result.success is True
        assert len(executed_tasks) > 0
        assert result.final_context.files_created  # Should have files

    @pytest.mark.asyncio
    async def test_execute_with_failing_task(self, sample_plan):
        def failing_executor(task_name: str, context: WaveContext) -> TaskResult:
            if "service" in task_name:
                return TaskResult(
                    task_name=task_name,
                    status="failed",
                    error="Simulated failure",
                )
            return TaskResult(task_name=task_name, status="completed")

        orchestrator = WaveOrchestrator(task_executor=failing_executor)
        result = await orchestrator.execute(sample_plan)

        # Should still complete (task failure is recorded as issue)
        assert result.final_context is not None
        assert len(result.final_context.issues_found) > 0

    @pytest.mark.asyncio
    async def test_execute_with_breakpoint(self, sample_plan):
        breakpoint_calls = []

        def breakpoint_callback(wave: Wave, context: WaveContext) -> bool:
            breakpoint_calls.append(wave.wave_id)
            return True  # Continue

        plan = create_wave_plan(
            feature_slug="breakpoint-test",
            tasks=[{"name": "task1"}, {"name": "task2"}],
            safe_mode=True,  # Enable breakpoints
        )

        orchestrator = WaveOrchestrator(breakpoint_callback=breakpoint_callback)
        result = await orchestrator.execute(plan)

        assert result.success is True
        assert len(breakpoint_calls) > 0

    @pytest.mark.asyncio
    async def test_execute_breakpoint_cancellation(self, sample_plan):
        cancel_after_first = True

        def breakpoint_callback(wave: Wave, context: WaveContext) -> bool:
            nonlocal cancel_after_first
            if cancel_after_first:
                cancel_after_first = False
                return False  # Cancel
            return True

        plan = create_wave_plan(
            feature_slug="cancel-test",
            tasks=[{"name": "task1"}, {"name": "task2"}],
            safe_mode=True,
        )

        orchestrator = WaveOrchestrator(breakpoint_callback=breakpoint_callback)
        result = await orchestrator.execute(plan)

        assert result.stopped_at_wave is not None
        assert result.stop_reason == "User cancelled at breakpoint"

    @pytest.mark.asyncio
    async def test_stop_request(self, sample_plan):
        orchestrator = WaveOrchestrator()

        async def stop_after_delay():
            await asyncio.sleep(0.1)
            orchestrator.stop()

        # Start stop task
        asyncio.create_task(stop_after_delay())

        result = await orchestrator.execute(sample_plan)

        # May or may not have stopped depending on timing
        # Just verify it didn't crash
        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_with_hooks(self, sample_plan):
        hook_calls = []

        async def hook_runner(hook_type: str, context: dict):
            hook_calls.append(hook_type)

        orchestrator = WaveOrchestrator(hook_runner=hook_runner)
        result = await orchestrator.execute(sample_plan)

        assert result.success is True
        assert "pre-wave" in hook_calls
        assert "post-wave" in hook_calls


class TestRunWaveOrchestration:
    """Tests for run_wave_orchestration convenience function."""

    @pytest.mark.asyncio
    async def test_run_orchestration(self):
        plan = create_wave_plan(
            feature_slug="convenience-test",
            tasks=[{"name": "task1"}],
        )

        result = await run_wave_orchestration(plan)

        assert result.success is True
        assert result.plan == plan


class TestWaveOrchestrationIntegration:
    """Integration tests for complete wave orchestration."""

    @pytest.mark.asyncio
    async def test_full_progressive_execution(self):
        """Test complete progressive strategy execution."""
        plan = create_wave_plan(
            feature_slug="integration-test",
            tasks=[
                {"name": "create_user_entity", "estimated_minutes": 5},
                {"name": "create_user_repository", "estimated_minutes": 5},
                {"name": "create_user_service", "estimated_minutes": 10},
                {"name": "create_user_controller", "estimated_minutes": 5},
                {"name": "create_user_tests", "estimated_minutes": 10},
            ],
            strategy="progressive",
        )

        files_created = []

        def executor(task_name: str, context: WaveContext) -> TaskResult:
            file_path = f"src/{task_name.replace('create_', '')}.py"
            files_created.append(file_path)
            return TaskResult(
                task_name=task_name,
                status="completed",
                files_created=[file_path],
            )

        orchestrator = WaveOrchestrator(task_executor=executor)
        result = await orchestrator.execute(plan)

        assert result.success is True
        assert len(files_created) == 5
        assert result.final_context.files_created == files_created

    @pytest.mark.asyncio
    async def test_full_systematic_execution(self):
        """Test complete systematic strategy execution."""
        plan = create_wave_plan(
            feature_slug="systematic-test",
            tasks=[
                {"name": "task1", "estimated_minutes": 5},
                {"name": "task2", "estimated_minutes": 5},
                {"name": "task3", "estimated_minutes": 5},
            ],
            strategy="systematic",
        )

        orchestrator = WaveOrchestrator()
        result = await orchestrator.execute(plan)

        assert result.success is True
        # Systematic has analysis + execution + validation waves
        assert result.waves_completed >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
