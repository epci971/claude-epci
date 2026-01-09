"""
DAG Builder Module

Constructs and validates Directed Acyclic Graphs for agent orchestration.
Uses Kahn's algorithm for cycle detection and topological sorting.
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

from .config import AgentConfig, OrchestrationConfig


class CycleDetectedError(Exception):
    """Raised when a cycle is detected in the DAG."""

    def __init__(self, agents: List[str]):
        self.agents = agents
        super().__init__(f"Cycle detected in DAG involving agents: {', '.join(agents)}")


@dataclass
class DAG:
    """
    Directed Acyclic Graph for agent dependencies.

    Provides methods for validation, topological sorting, and finding
    agents ready for execution.
    """

    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    _adjacency: Dict[str, List[str]] = field(default_factory=dict)
    _reverse_adjacency: Dict[str, List[str]] = field(default_factory=dict)
    _validated: bool = False

    def add_agent(self, config: AgentConfig) -> None:
        """Add an agent to the DAG."""
        self.agents[config.name] = config
        self._adjacency[config.name] = list(config.depends_on)

        # Build reverse adjacency (who depends on this agent)
        if config.name not in self._reverse_adjacency:
            self._reverse_adjacency[config.name] = []

        for dep in config.depends_on:
            if dep not in self._reverse_adjacency:
                self._reverse_adjacency[dep] = []
            self._reverse_adjacency[dep].append(config.name)

        self._validated = False

    def validate(self) -> bool:
        """
        Validate the DAG has no cycles using Kahn's algorithm.

        Returns:
            True if DAG is valid (no cycles)

        Raises:
            CycleDetectedError: If a cycle is detected
        """
        if self._validated:
            return True

        # Calculate in-degrees
        in_degree: Dict[str, int] = {agent: 0 for agent in self.agents}
        for agent, deps in self._adjacency.items():
            for dep in deps:
                if dep in self.agents:
                    # dep is a dependency, increment in-degree of agent
                    pass
            in_degree[agent] = len([d for d in deps if d in self.agents])

        # Initialize queue with agents having no dependencies
        queue = deque([agent for agent, degree in in_degree.items() if degree == 0])
        processed = []

        while queue:
            current = queue.popleft()
            processed.append(current)

            # For each agent that depends on current
            for dependent in self._reverse_adjacency.get(current, []):
                if dependent in in_degree:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        # If we couldn't process all agents, there's a cycle
        if len(processed) != len(self.agents):
            remaining = [a for a in self.agents if a not in processed]
            raise CycleDetectedError(remaining)

        self._validated = True
        return True

    def topological_sort(self) -> List[str]:
        """
        Return agents in topological order (dependencies first).

        Returns:
            List of agent names in execution order

        Raises:
            CycleDetectedError: If DAG contains cycles
        """
        self.validate()

        # Calculate in-degrees
        in_degree: Dict[str, int] = {agent: 0 for agent in self.agents}
        for agent, deps in self._adjacency.items():
            in_degree[agent] = len([d for d in deps if d in self.agents])

        # Kahn's algorithm
        queue = deque([agent for agent, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for dependent in self._reverse_adjacency.get(current, []):
                if dependent in in_degree:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        return result

    def find_runnable(self, completed: Set[str], skipped: Optional[Set[str]] = None) -> List[str]:
        """
        Find agents whose dependencies are all satisfied.

        Args:
            completed: Set of agent names that have completed
            skipped: Set of agent names that were skipped (treated as completed)

        Returns:
            List of agent names ready to run
        """
        if skipped is None:
            skipped = set()

        satisfied = completed | skipped
        runnable = []

        for agent_name, config in self.agents.items():
            if agent_name in satisfied:
                continue  # Already done

            # Check if all dependencies are satisfied
            deps_satisfied = all(
                dep in satisfied or dep not in self.agents
                for dep in config.depends_on
            )

            if deps_satisfied:
                runnable.append(agent_name)

        return runnable

    def get_dependencies(self, agent: str) -> List[str]:
        """Get direct dependencies of an agent."""
        if agent not in self.agents:
            return []
        return list(self.agents[agent].depends_on)

    def get_dependents(self, agent: str) -> List[str]:
        """Get agents that depend on this agent."""
        return self._reverse_adjacency.get(agent, [])

    def get_agent_config(self, agent: str) -> Optional[AgentConfig]:
        """Get configuration for an agent."""
        return self.agents.get(agent)

    def __len__(self) -> int:
        return len(self.agents)

    def __contains__(self, agent: str) -> bool:
        return agent in self.agents


class DAGBuilder:
    """
    Builder for constructing DAGs from configuration.

    Usage:
        builder = DAGBuilder()
        builder.add_agent(AgentConfig(...))
        builder.add_agent(AgentConfig(...))
        dag = builder.build()
    """

    def __init__(self):
        self._dag = DAG()

    def add_agent(self, config: AgentConfig) -> "DAGBuilder":
        """Add an agent configuration. Returns self for chaining."""
        self._dag.add_agent(config)
        return self

    def add_agents(self, configs: List[AgentConfig]) -> "DAGBuilder":
        """Add multiple agent configurations. Returns self for chaining."""
        for config in configs:
            self._dag.add_agent(config)
        return self

    def build(self, validate: bool = True) -> DAG:
        """
        Build and return the DAG.

        Args:
            validate: If True, validate the DAG before returning

        Returns:
            The constructed DAG

        Raises:
            CycleDetectedError: If validate=True and DAG has cycles
        """
        if validate:
            self._dag.validate()
        return self._dag

    @classmethod
    def from_config(cls, config: OrchestrationConfig) -> DAG:
        """
        Build a DAG from an OrchestrationConfig.

        Args:
            config: OrchestrationConfig containing agent definitions

        Returns:
            Validated DAG
        """
        builder = cls()
        for agent_config in config.agents.values():
            builder.add_agent(agent_config)
        return builder.build()


def validate_dag_config(config: OrchestrationConfig) -> List[str]:
    """
    Validate a DAG configuration and return any errors.

    Args:
        config: OrchestrationConfig to validate

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check for undefined dependencies
    agent_names = set(config.agents.keys())
    for agent_name, agent_config in config.agents.items():
        for dep in agent_config.depends_on:
            if dep not in agent_names:
                errors.append(
                    f"Agent '{agent_name}' depends on undefined agent '{dep}'"
                )

    # Check for cycles
    if not errors:
        try:
            DAGBuilder.from_config(config)
        except CycleDetectedError as e:
            errors.append(str(e))

    return errors
