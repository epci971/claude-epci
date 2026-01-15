# DAG Building

## Overview

The orchestrator uses a Directed Acyclic Graph (DAG) to manage spec dependencies.
This ensures specs execute in the correct order and detects circular dependencies.

## API Reference

The `dag_builder.py` module provides:

```python
from src.orchestration.dag_builder import DAG, CycleDetectedError
from src.orchestration.config import AgentConfig

# Build DAG
dag = DAG()
for spec in specs:
    dag.add_agent(AgentConfig(
        name=spec['id'],
        depends_on=spec.get('dependencies', [])
    ))

# Validate (checks for cycles)
try:
    dag.validate()
except CycleDetectedError as e:
    print(f"Cycle detected: {e.agents}")
    abort()

# Get execution order
order = dag.topological_sort()  # ['S01', 'S02', 'S03', ...]

# Find runnable specs (dependencies satisfied)
runnable = dag.find_runnable(
    completed={'S01'},
    skipped=set()
)
```

## Cycle Detection

Uses Kahn's algorithm for topological sorting. If a cycle exists,
`CycleDetectedError` is raised with the cycle path.

**Example cycle:**
```
S01 → S02 → S03 → S01  (cycle!)
```

**Error display:**
```
╔══════════════════════════════════════════════════════════════╗
║ ❌ ERROR: Circular Dependency Detected                       ║
╠══════════════════════════════════════════════════════════════╣
║ Cycle: S01 → S02 → S03 → S01                                ║
║                                                              ║
║ → Remove one dependency to break the cycle                   ║
╚══════════════════════════════════════════════════════════════╝
```

## Dependency Resolution

Before executing a spec, check all dependencies are resolved:

```python
def can_execute(spec_id, completed, failed, skipped):
    deps = dag.get_dependencies(spec_id)
    for dep in deps:
        if dep in failed or dep in skipped:
            return False, f"Dependency {dep} not available"
        if dep not in completed:
            return False, f"Waiting for {dep}"
    return True, None
```

## DAG-Aware Skip

If a spec fails and cannot be retried:
1. Mark spec as FAILED
2. Find all transitive dependents
3. Mark dependents as SKIPPED
4. Continue with independent specs

```python
def skip_dependents(failed_spec_id):
    dependents = dag.get_all_dependents(failed_spec_id)
    for dep in dependents:
        mark_skipped(dep, reason=f"Depends on failed {failed_spec_id}")
```
