# Auto-Retry Strategy

## Overview

When a spec fails validation (tests, lint, or review), the orchestrator
automatically retries with context about the failure.

## Retry Flow

```
Spec execution
     │
     ▼
 Validation ────────── PASS ────────► Commit & Continue
     │
   FAIL
     │
     ▼
 Retry 1 ────────────── PASS ────────► Commit & Continue
     │
   FAIL
     │
     ▼
 Retry 2 ────────────── PASS ────────► Commit & Continue
     │
   FAIL
     │
     ▼
 Retry 3 ────────────── PASS ────────► Commit & Continue
     │
   FAIL
     │
     ▼
 Mark FAILED ─────────► Skip dependents ─────► Continue
```

## Retry Strategies

### Retry 1: Error Context

Pass the error message to Claude for targeted fix:

```
Previous attempt failed with:
{error_message}

Please analyze the error and fix the issue.
```

### Retry 2: Alternative Approach

If Retry 1 fails, suggest trying a different approach:

```
Two attempts have failed:
1. {error_1}
2. {error_2}

Consider an alternative implementation approach.
```

### Retry 3: Minimal Fix

Last attempt focuses on minimal changes:

```
Final attempt. Focus on the smallest possible fix.
Do not refactor or add features.
Only address the specific failure:
{error_3}
```

## Configuration

```bash
# Default: 3 retries
/orchestrate ./specs/

# Custom retry count
/orchestrate ./specs/ --max-retries 5

# No retries (fail fast)
/orchestrate ./specs/ --max-retries 0
```

## Logging

Each retry is logged in the journal:

```markdown
## S03-integration
- Started: 22:40:00
- Phase 1: OK 2min
- Phase 2: FAILED - Test assertion error
- Retry 1/3: FAILED - Same error
- Retry 2/3: SUCCESS - Fixed assertion
- Phase 3: OK 3min
- Commit: abc1234
- Duration: 15min
- Status: SUCCESS (2 retries)
```

## DAG-Aware Skip

When all retries fail:

1. **Mark spec FAILED**
2. **Find dependents** using DAG
3. **Skip all dependents** with reason
4. **Continue** with independent specs

```python
def handle_spec_failure(spec_id, dag):
    specs[spec_id].status = 'FAILED'

    # Find all specs that depend on this one
    dependents = dag.get_all_dependents(spec_id)

    for dep_id in dependents:
        specs[dep_id].status = 'SKIPPED'
        specs[dep_id].skip_reason = f"Depends on failed {spec_id}"
        log(f"Skipping {dep_id}: depends on failed {spec_id}")
```

## Error Categories

| Category | Action |
|----------|--------|
| Test failure | Retry with error context |
| Lint error | Auto-fix if possible, retry |
| Type error | Retry with error context |
| Git conflict | Abort (no retry) |
| Timeout | Skip (no retry) |
| Network error | Retry immediately |
