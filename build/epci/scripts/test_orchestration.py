#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for EPCI Multi-Agent Orchestration (F07)

Tests cover:
- DAG construction and validation
- Cycle detection
- Parallel vs sequential execution
- Error handling for required/optional agents
- Timeout handling
- Condition evaluation

Run with: pytest src/scripts/test_orchestration.py -v
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

# Add src to path for imports
src_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(src_path))

from orchestration.config import (
    AgentConfig,
    OrchestrationConfig,
    OrchestrationMode,
    load_config,
    load_config_from_dict,
    get_default_config,
    merge_with_defaults,
)
from orchestration.dag_builder import (
    DAG,
    DAGBuilder,
    CycleDetectedError,
    validate_dag_config,
)
from orchestration.agent_runner import (
    AgentRunner,
    AgentResult,
    AgentStatus,
)
from orchestration.orchestrator import (
    Orchestrator,
    OrchestrationResult,
    OrchestrationError,
    RequiredAgentFailedError,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def simple_config():
    """Simple orchestration config with 3 agents."""
    return OrchestrationConfig(
        mode=OrchestrationMode.DAG,
        timeout_global=60,
        agents={
            "agent-a": AgentConfig(name="agent-a", depends_on=[], timeout=10, required=True),
            "agent-b": AgentConfig(name="agent-b", depends_on=["agent-a"], timeout=10, required=True),
            "agent-c": AgentConfig(name="agent-c", depends_on=["agent-a"], timeout=10, required=False),
        }
    )


@pytest.fixture
def epci_config():
    """EPCI-like config matching the default DAG."""
    return get_default_config()


@pytest.fixture
def cyclic_config():
    """Config with a cycle for testing cycle detection."""
    return OrchestrationConfig(
        mode=OrchestrationMode.DAG,
        agents={
            "a": AgentConfig(name="a", depends_on=["c"]),
            "b": AgentConfig(name="b", depends_on=["a"]),
            "c": AgentConfig(name="c", depends_on=["b"]),
        }
    )


def success_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executor that always succeeds."""
    return {"verdict": "APPROVED", "message": f"{agent_name} completed"}


async def async_success_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Async executor that always succeeds with a small delay."""
    await asyncio.sleep(0.1)
    return {"verdict": "APPROVED", "message": f"{agent_name} completed"}


def failure_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executor that always fails."""
    raise RuntimeError(f"{agent_name} failed")


async def slow_executor(agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executor that takes too long (for timeout tests)."""
    await asyncio.sleep(100)
    return {"verdict": "APPROVED"}


# =============================================================================
# CONFIG TESTS
# =============================================================================

class TestConfig:
    """Tests for orchestration configuration."""

    def test_agent_config_defaults(self):
        """Test AgentConfig has correct defaults."""
        config = AgentConfig(name="test")
        assert config.timeout == 60
        assert config.required is True
        assert config.condition is None
        assert config.depends_on == []

    def test_agent_config_validation(self):
        """Test AgentConfig validates timeout."""
        with pytest.raises(ValueError, match="timeout must be positive"):
            AgentConfig(name="test", timeout=0)

        with pytest.raises(ValueError, match="timeout exceeds maximum"):
            AgentConfig(name="test", timeout=500)

    def test_load_config_from_dict(self):
        """Test loading config from dictionary."""
        raw = {
            "orchestration": {
                "default_mode": "sequential",
                "timeout_global": 120,
                "agents": {
                    "test-agent": {
                        "depends_on": [],
                        "timeout": 30,
                        "required": False,
                    }
                }
            }
        }
        config = load_config_from_dict(raw)

        assert config.mode == OrchestrationMode.SEQUENTIAL
        assert config.timeout_global == 120
        assert "test-agent" in config.agents
        assert config.agents["test-agent"].required is False

    def test_get_default_config(self):
        """Test default config matches EPCI structure."""
        config = get_default_config()

        assert "plan-validator" in config.agents
        assert "code-reviewer" in config.agents
        assert "doc-generator" in config.agents
        assert config.mode == OrchestrationMode.DAG

    def test_merge_with_defaults(self):
        """Test merging project config with defaults."""
        project = OrchestrationConfig(
            mode=OrchestrationMode.PARALLEL,
            timeout_global=180,
            agents={
                "custom-agent": AgentConfig(name="custom-agent"),
            }
        )

        merged = merge_with_defaults(project)

        # Project overrides
        assert merged.mode == OrchestrationMode.PARALLEL
        assert merged.timeout_global == 180
        # Custom agent added
        assert "custom-agent" in merged.agents
        # Defaults preserved
        assert "plan-validator" in merged.agents


# =============================================================================
# DAG BUILDER TESTS
# =============================================================================

class TestDAGBuilder:
    """Tests for DAG construction and validation."""

    def test_build_simple_dag(self, simple_config):
        """Test building a simple DAG."""
        dag = DAGBuilder.from_config(simple_config)

        assert len(dag) == 3
        assert "agent-a" in dag
        assert "agent-b" in dag
        assert "agent-c" in dag

    def test_cycle_detection(self, cyclic_config):
        """Test that cycles are detected."""
        with pytest.raises(CycleDetectedError) as exc_info:
            DAGBuilder.from_config(cyclic_config)

        # All agents should be in the cycle
        assert len(exc_info.value.agents) > 0

    def test_topological_sort(self, simple_config):
        """Test topological sorting respects dependencies."""
        dag = DAGBuilder.from_config(simple_config)
        order = dag.topological_sort()

        # agent-a must come before agent-b and agent-c
        a_idx = order.index("agent-a")
        b_idx = order.index("agent-b")
        c_idx = order.index("agent-c")

        assert a_idx < b_idx
        assert a_idx < c_idx

    def test_find_runnable_initial(self, simple_config):
        """Test finding runnable agents at start."""
        dag = DAGBuilder.from_config(simple_config)
        runnable = dag.find_runnable(completed=set())

        # Only agent-a has no dependencies
        assert runnable == ["agent-a"]

    def test_find_runnable_after_completion(self, simple_config):
        """Test finding runnable agents after some complete."""
        dag = DAGBuilder.from_config(simple_config)
        runnable = dag.find_runnable(completed={"agent-a"})

        # Both agent-b and agent-c depend only on agent-a
        assert sorted(runnable) == ["agent-b", "agent-c"]

    def test_find_runnable_with_skipped(self, simple_config):
        """Test skipped agents are treated as completed for dependencies."""
        dag = DAGBuilder.from_config(simple_config)
        runnable = dag.find_runnable(completed=set(), skipped={"agent-a"})

        # Both agent-b and agent-c can run
        assert sorted(runnable) == ["agent-b", "agent-c"]

    def test_validate_dag_config_missing_dependency(self):
        """Test validation catches missing dependencies."""
        config = OrchestrationConfig(
            agents={
                "a": AgentConfig(name="a", depends_on=["nonexistent"]),
            }
        )

        errors = validate_dag_config(config)
        assert len(errors) == 1
        assert "nonexistent" in errors[0]


# =============================================================================
# AGENT RUNNER TESTS
# =============================================================================

class TestAgentRunner:
    """Tests for agent execution."""

    @pytest.mark.asyncio
    async def test_successful_execution(self):
        """Test successful agent execution."""
        config = AgentConfig(name="test", timeout=10)
        runner = AgentRunner(config, success_executor)

        result = await runner.run({})

        assert result.status == AgentStatus.SUCCESS
        assert result.verdict == "APPROVED"
        assert result.duration_seconds > 0

    @pytest.mark.asyncio
    async def test_failed_execution(self):
        """Test failed agent execution."""
        config = AgentConfig(name="test", timeout=10)
        runner = AgentRunner(config, failure_executor)

        result = await runner.run({})

        assert result.status == AgentStatus.FAILED
        assert result.error is not None
        assert "failed" in result.error

    @pytest.mark.asyncio
    async def test_timeout_execution(self):
        """Test agent timeout."""
        config = AgentConfig(name="test", timeout=1)  # 1 second timeout
        runner = AgentRunner(config, slow_executor)

        result = await runner.run({})

        assert result.status == AgentStatus.TIMEOUT
        assert "timed out" in result.error

    @pytest.mark.asyncio
    async def test_condition_not_met(self):
        """Test agent skipped when condition not met."""
        config = AgentConfig(
            name="test",
            condition="has_sensitive_files",
        )
        runner = AgentRunner(config, success_executor)

        # Context without sensitive files
        result = await runner.run({"files": ["src/utils.py"]})

        assert result.status == AgentStatus.SKIPPED
        assert "Condition not met" in result.output.get("reason", "")

    @pytest.mark.asyncio
    async def test_condition_met_sensitive_files(self):
        """Test agent runs when sensitive files detected."""
        config = AgentConfig(
            name="test",
            condition="has_sensitive_files",
        )
        runner = AgentRunner(config, success_executor)

        result = await runner.run({"files": ["src/auth/login.py"]})

        assert result.status == AgentStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_condition_complexity(self):
        """Test complexity condition evaluation."""
        config = AgentConfig(
            name="test",
            condition="complexity >= STANDARD",
        )
        runner = AgentRunner(config, success_executor)

        # SMALL complexity - should skip
        result = await runner.run({"complexity": "SMALL"})
        assert result.status == AgentStatus.SKIPPED

        # STANDARD complexity - should run
        result = await runner.run({"complexity": "STANDARD"})
        assert result.status == AgentStatus.SUCCESS

        # LARGE complexity - should run
        result = await runner.run({"complexity": "LARGE"})
        assert result.status == AgentStatus.SUCCESS


# =============================================================================
# ORCHESTRATOR TESTS
# =============================================================================

class TestOrchestrator:
    """Tests for the main orchestrator."""

    @pytest.mark.asyncio
    async def test_dag_execution_order(self, simple_config):
        """Test DAG execution respects dependencies."""
        execution_order = []

        def tracking_executor(name: str, ctx: Dict) -> Dict:
            execution_order.append(name)
            return {"verdict": "APPROVED"}

        orchestrator = Orchestrator(simple_config, tracking_executor)
        result = await orchestrator.execute({})

        assert result.success
        # agent-a must run before agent-b and agent-c
        assert execution_order.index("agent-a") < execution_order.index("agent-b")
        assert execution_order.index("agent-a") < execution_order.index("agent-c")

    @pytest.mark.asyncio
    async def test_parallel_faster_than_sequential(self, simple_config):
        """Test parallel execution is faster than sequential."""
        async def delayed_executor(name: str, ctx: Dict) -> Dict:
            await asyncio.sleep(0.2)
            return {"verdict": "APPROVED"}

        # DAG mode (parallel where possible)
        simple_config.mode = OrchestrationMode.DAG
        dag_orchestrator = Orchestrator(simple_config, delayed_executor)
        dag_result = await dag_orchestrator.execute({})

        # Sequential mode
        simple_config.mode = OrchestrationMode.SEQUENTIAL
        seq_orchestrator = Orchestrator(simple_config, delayed_executor)
        seq_result = await seq_orchestrator.execute({})

        # DAG should be faster (agent-b and agent-c run in parallel)
        assert dag_result.duration_seconds < seq_result.duration_seconds

    @pytest.mark.asyncio
    async def test_required_agent_failure_stops(self, simple_config):
        """Test that required agent failure stops orchestration."""
        def selective_executor(name: str, ctx: Dict) -> Dict:
            if name == "agent-a":
                raise RuntimeError("Agent A failed")
            return {"verdict": "APPROVED"}

        orchestrator = Orchestrator(simple_config, selective_executor)
        result = await orchestrator.execute({})

        assert not result.success
        assert len(result.errors) > 0
        # agent-b and agent-c should not have run
        assert "agent-b" not in result.results
        assert "agent-c" not in result.results

    @pytest.mark.asyncio
    async def test_optional_agent_failure_continues(self, simple_config):
        """Test that optional agent failure doesn't stop orchestration."""
        def selective_executor(name: str, ctx: Dict) -> Dict:
            if name == "agent-c":  # agent-c is optional
                raise RuntimeError("Agent C failed")
            return {"verdict": "APPROVED"}

        orchestrator = Orchestrator(simple_config, selective_executor)
        result = await orchestrator.execute({})

        assert result.success  # Should still succeed
        assert len(result.warnings) > 0  # But with warnings
        assert result.results["agent-c"].status == AgentStatus.FAILED

    @pytest.mark.asyncio
    async def test_all_agents_complete(self, epci_config):
        """Test all EPCI agents complete successfully."""
        orchestrator = Orchestrator(epci_config, success_executor)
        result = await orchestrator.execute({"complexity": "LARGE"})

        assert result.success
        assert len(result.results) == 5  # All 5 agents
        assert result.waves_executed >= 1

    @pytest.mark.asyncio
    async def test_parallel_gain_calculation(self, simple_config):
        """Test parallel gain is calculated correctly."""
        async def delayed_executor(name: str, ctx: Dict) -> Dict:
            await asyncio.sleep(0.1)
            return {"verdict": "APPROVED"}

        orchestrator = Orchestrator(simple_config, delayed_executor)
        result = await orchestrator.execute({})

        # Sequential time would be ~0.3s, parallel should be ~0.2s
        assert result.parallel_gain > 0

    @pytest.mark.asyncio
    async def test_global_timeout(self):
        """Test global timeout is respected."""
        config = OrchestrationConfig(
            mode=OrchestrationMode.DAG,
            timeout_global=1,  # 1 second global timeout
            agents={
                "slow": AgentConfig(name="slow", timeout=60),
            }
        )

        orchestrator = Orchestrator(config, slow_executor)
        result = await orchestrator.execute({})

        assert not result.success
        assert any("timeout" in err.lower() for err in result.errors)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for the full orchestration flow."""

    @pytest.mark.asyncio
    async def test_full_epci_workflow(self):
        """Test a full EPCI-like workflow."""
        config = get_default_config()

        # Track which agents ran
        agents_run = set()

        def tracking_executor(name: str, ctx: Dict) -> Dict:
            agents_run.add(name)
            return {"verdict": "APPROVED"}

        orchestrator = Orchestrator(config, tracking_executor)
        context = {
            "complexity": "LARGE",
            "files": ["src/auth/login.py"],  # Has sensitive files
        }

        result = await orchestrator.execute(context)

        assert result.success
        # All required agents should run
        assert "plan-validator" in agents_run
        assert "code-reviewer" in agents_run
        assert "doc-generator" in agents_run
        # Optional agents with conditions
        assert "security-auditor" in agents_run  # Because of sensitive files

    @pytest.mark.asyncio
    async def test_result_serialization(self, simple_config):
        """Test OrchestrationResult can be serialized."""
        orchestrator = Orchestrator(simple_config, success_executor)
        result = await orchestrator.execute({})

        result_dict = result.to_dict()

        assert "success" in result_dict
        assert "results" in result_dict
        assert "duration_seconds" in result_dict
        assert "parallel_gain" in result_dict

    def test_config_from_yaml_file(self, tmp_path):
        """Test loading config from YAML file."""
        yaml_content = """
orchestration:
  default_mode: sequential
  timeout_global: 120
  agents:
    test-agent:
      depends_on: []
      timeout: 30
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml_content)

        config = load_config(str(config_file))

        assert config.mode == OrchestrationMode.SEQUENTIAL
        assert "test-agent" in config.agents


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
