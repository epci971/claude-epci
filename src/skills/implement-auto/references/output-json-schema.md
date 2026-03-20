# Output JSON Schema (v1)

> Contract between implement-auto and the pipeline orchestrator.

## File Location

```
{working_directory}/.implement-auto-output.json
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
    "spec_source": "string",
    "complexity": "STANDARD | LARGE",
    "worktree_enabled": "boolean"
  },
  "phases": {
    "completed": ["init", "explore", "plan", "code", "review", "document", "finish"],
    "failed": [],
    "current": "string | null",
    "skipped": []
  },
  "plan": {
    "total_components": 0,
    "planner_used": true,
    "validator_verdict": "APPROVED | NEEDS_REVISION | null",
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
    },
    "deep_review": {
      "status": "pass | warn | fail | skip",
      "verdict": "APPROVED | CHANGES_REQUIRED | SECURITY_REVIEW_NEEDED | null",
      "findings_count": 0,
      "critical_count": 0,
      "skipped_reason": "string | null"
    },
    "security_review": {
      "status": "pass | warn | fail | skip",
      "verdict": "PASS | FAIL_CRITICAL | FAIL_HIGH | null",
      "vulnerabilities": 0,
      "owasp_categories": [],
      "skipped_reason": "string | null"
    },
    "qa_review": {
      "status": "pass | warn | fail | skip",
      "verdict": "PASS | FAIL | null",
      "ac_passed": 0,
      "ac_total": 0,
      "defects_found": 0,
      "skipped_reason": "string | null"
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
  ],
  "publish": {
    "pushed": "boolean",
    "push_error": "string | null",
    "pr_url": "string | null",
    "pr_draft": "boolean",
    "pr_error": "string | null",
    "auto_merge_enabled": "boolean",
    "merged": "boolean",
    "merge_error": "string | null",
    "worktree_cleaned": "boolean | null",
    "skipped": "boolean"
  }
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

### feature.complexity

| Value | Coverage Targets | Security Review |
|-------|-----------------|-----------------|
| `STANDARD` | 70% line / 60% branch | Conditional (auth patterns) |

### feature.worktree_enabled

| Value | Meaning |
|-------|---------|
| `true` | Worktree isolation active (--worktree flag used) |
| `false` | In-place execution (default) |
| `LARGE` | 80% line / 70% branch | Mandatory |

### plan Fields

| Field | Type | Description |
|-------|------|-------------|
| `planner_used` | boolean | Whether @planner agent was invoked |
| `validator_verdict` | string? | `APPROVED`, `NEEDS_REVISION`, or null if skipped |

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

### checks.deep_review Object

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `pass`, `warn`, `fail`, or `skip` |
| `verdict` | string? | `APPROVED`, `CHANGES_REQUIRED`, `SECURITY_REVIEW_NEEDED`, or null |
| `findings_count` | number | Total findings from @code-reviewer |
| `critical_count` | number | Critical/blocking findings |
| `skipped_reason` | string? | Reason if skipped (e.g., `"--skip-review flag"`, `"timeout"`) |

### checks.security_review Object

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `pass`, `warn`, `fail`, or `skip` |
| `verdict` | string? | `PASS`, `FAIL_CRITICAL`, `FAIL_HIGH`, or null |
| `vulnerabilities` | number | Total vulnerabilities found |
| `owasp_categories` | string[] | OWASP categories with findings (e.g., `["A01", "A03"]`) |
| `skipped_reason` | string? | Reason if skipped (e.g., `"no_security_patterns"`, `"--skip-security flag"`) |

### checks.qa_review Object

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `pass`, `warn`, `fail`, or `skip` |
| `verdict` | string? | `PASS` or `FAIL` |
| `ac_passed` | number | Acceptance criteria verified |
| `ac_total` | number | Total acceptance criteria |
| `defects_found` | number | Defects found |
| `skipped_reason` | string? | Reason if skipped (e.g., `"below_threshold"`, `"--skip-qa flag"`) |

### publish Object

| Field | Type | Description |
|-------|------|-------------|
| `pushed` | boolean | Whether branch was pushed to origin |
| `push_error` | string? | Error message if push failed |
| `pr_url` | string? | GitHub PR URL (null if skipped or failed) |
| `pr_draft` | boolean | Whether PR was created as draft (PARTIAL status) |
| `pr_error` | string? | Error message if PR creation failed |
| `auto_merge_enabled` | boolean | Whether auto-merge was activated on the PR |
| `merged` | boolean | Whether PR was immediately squash-merged (SUCCESS only) |
| `merge_error` | string? | Error message if merge failed, or `"skipped_partial_status"` for PARTIAL |
| `worktree_cleaned` | boolean? | Whether worktree was successfully removed. Null if --worktree not used |
| `skipped` | boolean | True if --skip-publish flag was used |

## Incremental Write Protocol

The JSON file is written (overwritten) at each step transition:

```
step-00-init-auto    -> Write initial JSON (status: null, current: "init")
step-01-explore-auto -> Update phases.completed += "explore"
step-02-plan-auto    -> Update phases.completed += "plan", add plan.components
step-03-code-auto    -> Update per-component (most frequent updates)
step-04-review-auto  -> Update checks.self_review, checks.deep_review, checks.security_review, checks.qa_review
step-05-document-auto -> Update feature_doc path
step-06-finish-auto  -> Update final status, metrics
step-07-output-auto  -> Final write with complete data
step-08-publish-auto -> Update publish section (incl. merge status), phases.completed += "publish"
```

## File Persistence

After step-08, the JSON output is copied to a persistent location:

```
.implement-auto-results/{feature-slug}.json
```

If `--worktree` was used, the worktree is removed and the JSON is copied to the main repo.
If working in-place (default), the JSON is copied to `.implement-auto-results/` in the current directory.

The orchestrator should read from this location after execution completes.

## Parsing Notes (for Orchestrator)

- File is always valid JSON (atomic write)
- If `status` is null, skill is still running
- If `phases.current` is set, that step is in progress
- `errors[]` accumulates — check length for failure count
- `metrics` may be incomplete during execution
- After completion, read from `.implement-auto-results/` (worktree is removed if --worktree was used)
