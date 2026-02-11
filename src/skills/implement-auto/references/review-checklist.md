# Self-Review Checklist

> Automated quality checks for implement-auto self-review phase.
> Replaces interactive @code-reviewer for headless execution.

## Checklist Categories

### 1. Tests Quality

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| T1 | All tests pass | critical | Run test suite, exit code 0 |
| T2 | Tests exist for each component | error | Count test files vs components |
| T3 | Tests cover happy path | warning | Grep for assertion patterns |
| T4 | Tests cover error cases | warning | Grep for error/exception tests |
| T5 | No skipped/disabled tests | warning | Grep for skip/xit/xdescribe |

### 2. Code Quality

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| C1 | No debug prints/console.log | error | Grep for print/console.log |
| C2 | No hardcoded secrets | critical | Grep for password/secret/api_key patterns |
| C3 | No commented-out code blocks | warning | Grep for large comment blocks |
| C4 | No TODO/FIXME/HACK markers | warning | Grep for TODO/FIXME/HACK |
| C5 | Files follow project naming conventions | warning | Check against CLAUDE.md patterns |

### 3. Architecture

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| A1 | Follows existing patterns from explore | warning | Compare with identified patterns |
| A2 | No circular dependencies introduced | error | Check import graph |
| A3 | No duplicate functionality | warning | Grep for similar function signatures |

### 4. Security Basics

| # | Check | Severity | How to Verify |
|---|-------|----------|---------------|
| S1 | No SQL injection patterns | critical | Grep for string concatenation in queries |
| S2 | No command injection patterns | critical | Grep for os.system/exec/eval |
| S3 | Input validation present | warning | Check public API entry points |
| S4 | No sensitive data in logs | error | Grep for logging of credentials/tokens |

## Execution Protocol

```
FOR each check in checklist:
  result = execute_verification(check)
  IF result.passed:
    items_passed += 1
  ELSE:
    items_warned += 1
    findings.append({
      check_id: check.id,
      severity: check.severity,
      message: result.message,
      file: result.file,
      line: result.line
    })

self_review = {
  status: items_warned == 0 ? "pass" : (has_critical ? "fail" : "warn"),
  items_checked: total_checks,
  items_passed: items_passed,
  items_warned: items_warned,
  findings: findings
}
```

## Severity Impact on Status

| Severity | Impact on Task Status |
|----------|----------------------|
| critical | Logged but does NOT block (headless mode) |
| error | Logged as warning |
| warning | Informational only |

In headless mode, self-review findings are recorded but never block execution.
The orchestrator/reviewer decides action based on the JSON output.

## Optional: Deep Review (--with-review)

When `--with-review` flag is active:

```
LANCE Task({
  subagent_type: "code-reviewer",
  model: "opus",
  prompt: "Review all modified files for quality, architecture, and test coverage"
})
```

Results are merged into `checks.deep_review` in the JSON output.
If the subagent times out, fall back to self-review only with a warning.
