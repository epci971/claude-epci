# Circuit Breaker Rules

> 3-level protection against token-burning in autonomous mode.

## Overview

```
Level 1: COMPONENT (retry)
  |
  v
Level 2: TASK (abort)
  |
  v
Level 3: TIMEOUT (external, orchestrator)
```

## Level 1: Component Circuit Breaker

Protects individual components from infinite retry loops.

| Parameter | Value |
|-----------|-------|
| Max retries | 2 |
| Trigger | GREEN attempt fails (test still fails after implementation) |
| Action on trigger | Mark component FAILED, skip to next |
| Status impact | PARTIAL (if other components succeed) |

### Logic

```
FOR each component in plan:
  attempts = 0
  WHILE attempts < 2:
    Execute TDD cycle (RED -> GREEN)
    IF tests pass:
      Mark SUCCESS
      BREAK
    ELSE:
      attempts += 1
      IF attempts < 2:
        Log retry attempt
        Analyze failure, try different approach
  IF attempts >= 2:
    Mark component FAILED
    Log error in JSON output
    Check dependent components -> mark SKIPPED
```

### What Counts as a Retry

| Scenario | Counts as retry? |
|----------|-----------------|
| Test fails after GREEN attempt | YES |
| Syntax error in implementation | YES |
| Import/dependency error | YES |
| Test fails in RED phase (expected) | NO |
| Refactor breaks test | YES (revert + retry) |

## Level 2: Task Circuit Breaker

Protects the entire task from cascading failures.

| Parameter | Value |
|-----------|-------|
| Consecutive failures | 3 |
| Total failure rate | > 50% of components |
| Action on trigger | ABORT entire task |
| Status impact | FAILED |

### Logic

```
consecutive_failures = 0
total_failed = 0
total_attempted = 0

FOR each component:
  total_attempted += 1
  result = execute_component()

  IF result == FAILED:
    consecutive_failures += 1
    total_failed += 1

    IF consecutive_failures >= 3:
      ABORT task
      exit_reason = "circuit_breaker_consecutive"
      BREAK

    IF total_failed / total_attempted > 0.5 AND total_attempted >= 4:
      ABORT task
      exit_reason = "circuit_breaker_rate"
      BREAK

  ELSE:
    consecutive_failures = 0  # Reset on success
```

## Level 3: Timeout (External)

Managed by the orchestrator (not the skill).

| Parameter | Value |
|-----------|-------|
| Responsibility | Pipeline runner (OpenClaw) |
| Mechanism | Process kill after timeout |
| Recovery | Read partial JSON output |
| Default timeout | Configured by orchestrator (recommended: 15-20min) |

The skill does NOT manage timeouts. It writes JSON incrementally so the orchestrator can recover partial state.

## Dependency Skip Logic

When a component fails, dependent components are automatically skipped.

```
IF component A is FAILED:
  FOR each component B that depends on A:
    Mark B as SKIPPED
    Log: "Skipped {B}: depends on failed {A}"
    Add warning to JSON output
```

### Determining Dependencies

Dependencies come from the plan's task ordering:
- Explicit `depends_on` in plan
- File-level: if B imports from file created by A
- Test-level: if B's tests use fixtures from A

## Status Decision Table

| Scenario | Status | exit_reason |
|----------|--------|-------------|
| All components SUCCESS | SUCCESS | null |
| Some FAILED, some SUCCESS | PARTIAL | "partial_implementation" |
| 3 consecutive failures | FAILED | "circuit_breaker_consecutive" |
| > 50% failure rate | FAILED | "circuit_breaker_rate" |
| All components FAILED | FAILED | "all_components_failed" |
| Spec invalid | FAILED | "invalid_spec" |
| Explore empty | FAILED | "explore_empty_results" |
| Explore hallucination > 30% | FAILED | "explore_sanity_check_failed" |
