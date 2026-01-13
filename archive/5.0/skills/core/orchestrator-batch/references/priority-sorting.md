# Priority Sorting

## Overview

When multiple specs have no dependencies on each other (same DAG level),
they are sorted by priority to optimize execution order.

## Sorting Algorithm

```python
def sort_specs_at_level(specs):
    """
    Sort specs at the same DAG level.

    Priority order:
    1. Priority field (1-99, lower = higher priority)
    2. Effort (TINY < SMALL < STANDARD < LARGE)
    3. Alphabetical ID (tiebreaker)
    """
    EFFORT_ORDER = {'TINY': 0, 'SMALL': 1, 'STANDARD': 2, 'LARGE': 3}

    def sort_key(spec):
        priority = spec.get('priority', 50)  # Default middle priority
        effort = EFFORT_ORDER.get(spec['effort'], 2)
        return (priority, effort, spec['id'])

    return sorted(specs, key=sort_key)
```

## Priority Field

The `priority` field in INDEX.md is optional:
- Range: 1-99
- 1 = Highest priority (execute first)
- 99 = Lowest priority
- Empty = Default (50)

**Example INDEX.md:**
```markdown
| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| S01 | Core | 4h | - | - |
| S02 | Quick fix | 2h | 1 | - |
| S03 | Integration | 3h | - | S01, S02 |
```

Here, S02 executes before S01 because priority 1 < default 50.

## Priority Propagation

When a high-priority spec depends on lower-priority specs, the priority
propagates upward to ensure dependencies execute first.

**Algorithm:**
```python
def propagate_priorities(specs, dag):
    """
    Propagate priority from dependents to dependencies.
    If S03 (priority 1) depends on S01 (priority 5),
    then S01 inherits priority 1.
    """
    # Reverse topological order (dependents first)
    for spec_id in reversed(dag.topological_sort()):
        spec = specs[spec_id]
        for dep_id in spec.get('dependencies', []):
            dep = specs[dep_id]
            if spec['priority'] < dep['priority']:
                dep['priority'] = spec['priority']
                dep['priority_inherited_from'] = spec_id
```

**Visual example:**
```
Before propagation:
S01 (priority: 5) ← S03 (priority: 1)

After propagation:
S01 (priority: 1*) ← S03 (priority: 1)
* Inherited from S03
```

## Effort-Based Sorting

When priorities are equal, sort by effort (quick wins first):

| Effort | Order | Rationale |
|--------|-------|-----------|
| TINY | 1 | Fast feedback, build momentum |
| SMALL | 2 | Quick wins accumulate |
| STANDARD | 3 | Main work |
| LARGE | 4 | Most complex, do last |

This maximizes the number of completed specs early in the run.
