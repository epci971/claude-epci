# Output JSON Schema (v1)

> Contract between implement-auto and the pipeline orchestrator.

## File Location

```
{worktree_path}/.implement-auto-output.json
```

Written incrementally at each step completion. Always valid JSON.

## Schema

```json
{
  "$schema": "implement-auto-output-v1",
  "version": 1,
  "timestamp": "ISO-8601",
  "status": "SUCCESS | PARTIAL | FAILED",
  "exit_reason": "string | null",
  "feature": {
    "slug": "string",
    "branch": "string",
    "spec_source": "string"
  },
  "phases": {
    "completed": ["init", "explore", "plan", "code", "review", "document", "finish"],
    "failed": [],
    "current": "string | null",
    "skipped": []
  },
  "plan": {
    "total_components": 0,
    "components": [
      {
        "name": "string",
        "file": "string",
        "status": "SUCCESS | FAILED | SKIPPED",
        "tests_added": 0,
        "retries": 0,
        "error": "string | null"
      }
    ]
  },
  "metrics": {
    "files_created": 0,
    "files_modified": 0,
    "tests_added": 0,
    "tests_passing": 0,
    "tests_failing": 0
  },
  "checks": {
    "tests": { "status": "pass | fail | skip", "count": 0, "failures": 0 },
    "self_review": {
      "status": "pass | warn | fail",
      "items_checked": 0,
      "items_passed": 0,
      "items_warned": 0,
      "findings": []
    }
  },
  "feature_doc": "string (path)",
  "errors": [
    {
      "phase": "string",
      "component": "string | null",
      "message": "string",
      "severity": "critical | error | warning"
    }
  ],
  "warnings": [
    {
      "phase": "string",
      "message": "string"
    }
  ]
}
```

## Field Reference

### Top-Level

| Field | Type | Description |
|-------|------|-------------|
| `$schema` | string | Always `"implement-auto-output-v1"` |
| `version` | number | Always `1` |
| `timestamp` | string | ISO-8601 timestamp of last update |
| `status` | enum | `SUCCESS`, `PARTIAL`, or `FAILED` |
| `exit_reason` | string? | Null on SUCCESS, reason string otherwise |

### status Values

| Value | Meaning |
|-------|---------|
| `SUCCESS` | All components implemented, all tests pass |
| `PARTIAL` | Some components failed but others succeeded |
| `FAILED` | Task aborted (circuit breaker, invalid spec, etc.) |

### exit_reason Values

| Value | Trigger |
|-------|---------|
| `null` | SUCCESS |
| `"invalid_spec"` | Spec file empty or unreadable |
| `"explore_empty_results"` | Explore returned 0 files |
| `"explore_sanity_check_failed"` | > 30% hallucinated files |
| `"circuit_breaker_consecutive"` | 3 consecutive component failures |
| `"circuit_breaker_rate"` | > 50% failure rate |
| `"all_components_failed"` | Every component failed |
| `"partial_implementation"` | Some components failed (PARTIAL) |

### phases Object

| Field | Type | Description |
|-------|------|-------------|
| `completed` | string[] | Steps finished successfully |
| `failed` | string[] | Steps that failed |
| `current` | string? | Step currently executing (null when done) |
| `skipped` | string[] | Steps skipped |

### plan.components Array

Each component from the implementation plan:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Component name from plan |
| `file` | string | Primary file path |
| `status` | enum | `SUCCESS`, `FAILED`, `SKIPPED` |
| `tests_added` | number | Number of tests written |
| `retries` | number | Number of retry attempts (0-2) |
| `error` | string? | Error message if FAILED |

## Incremental Write Protocol

The JSON file is written (overwritten) at each step transition:

```
step-00-init-auto    -> Write initial JSON (status: null, current: "init")
step-01-explore-auto -> Update phases.completed += "explore"
step-02-plan-auto    -> Update phases.completed += "plan", add plan.components
step-03-code-auto    -> Update per-component (most frequent updates)
step-04-review-auto  -> Update checks.self_review
step-05-document-auto -> Update feature_doc path
step-06-finish-auto  -> Update final status, metrics
step-07-output-auto  -> Final write with complete data
```

## Parsing Notes (for Orchestrator)

- File is always valid JSON (atomic write)
- If `status` is null, skill is still running
- If `phases.current` is set, that step is in progress
- `errors[]` accumulates — check length for failure count
- `metrics` may be incomplete during execution
