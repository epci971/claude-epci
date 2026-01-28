---
name: step-06-verify
description: Run full test suite, collect metrics AFTER, calculate delta
prev_step: steps/step-05-review.md
next_step: steps/step-07-report.md
---

# Step 06: Verify

> Run full test suite, collect metrics AFTER, calculate delta.

## Trigger

- Previous step: `step-05-review.md` completed (or skipped)

## Inputs

| Input | Source |
|-------|--------|
| Metrics before | From step-01 |
| Modified files | From step-04 |
| Stack context | From step-00 |

## Protocol

### 1. Run Full Test Suite

Execute comprehensive test run (not just target tests):

```bash
# Full test suite by stack
IF python-django:
  pytest --tb=short
ELSE IF javascript-react:
  npm test -- --coverage
ELSE IF java-springboot:
  mvn test
ELSE IF php-symfony:
  php bin/phpunit
```

**CRITICAL**: If any tests fail, investigate:

```
IF tests fail:
  1. Identify failing tests
  2. Check if failures are:
     a) Related to refactored code → Behavior changed (problem)
     b) Unrelated (pre-existing failure) → Continue with warning
  3. If behavior changed:
     → Offer rollback or fix options
```

### 2. Collect Metrics AFTER

Use same tools as step-01 for consistency:

```bash
# Same command as before
radon cc <target> -a -s  # or equivalent
```

Store metrics:

```json
{
  "metrics_after": {
    "files": [
      {
        "path": "src/services/auth.py",
        "loc": 280,
        "cyclomatic_complexity": 12,
        "maintainability_index": 68,
        "methods_count": 8,
        "avg_method_length": 15
      },
      {
        "path": "src/validators/token_validator.py",
        "loc": 85,
        "cyclomatic_complexity": 5,
        "maintainability_index": 75,
        "methods_count": 4,
        "avg_method_length": 12
      }
    ],
    "totals": {
      "loc": 365,
      "avg_cc": 8.5,
      "avg_mi": 71.5
    },
    "tool_used": "radon"
  }
}
```

### 3. Calculate Delta

```python
def calculate_delta(before, after):
    return {
        "loc": {
            "before": before.loc,
            "after": after.loc,
            "delta": after.loc - before.loc,
            "percent": ((after.loc - before.loc) / before.loc) * 100
        },
        "cyclomatic_complexity": {
            "before": before.cc,
            "after": after.cc,
            "delta": after.cc - before.cc,
            "percent": ((after.cc - before.cc) / before.cc) * 100
        },
        "maintainability_index": {
            "before": before.mi,
            "after": after.mi,
            "delta": after.mi - before.mi,
            "percent": ((after.mi - before.mi) / before.mi) * 100
        }
    }
```

### 4. Per-File Delta

Generate detailed breakdown:

```
## Metrics Delta by File

| File | Metric | Before | After | Delta | Change |
|------|--------|--------|-------|-------|--------|
| auth.py | LOC | 450 | 280 | -170 | -37.8% |
| auth.py | CC | 25 | 12 | -13 | -52.0% |
| auth.py | MI | 45 | 68 | +23 | +51.1% |
| token_validator.py | LOC | 0 | 85 | +85 | (new) |
| token_validator.py | CC | 0 | 5 | +5 | (new) |
| token_validator.py | MI | 0 | 75 | +75 | (new) |

### Aggregated Delta

| Metric | Before | After | Delta | Trend |
|--------|--------|-------|-------|-------|
| Total LOC | 450 | 365 | -85 | IMPROVED |
| Avg CC | 25 | 8.5 | -16.5 | IMPROVED |
| Avg MI | 45 | 71.5 | +26.5 | IMPROVED |
```

### 5. Evaluate Improvement

```python
def evaluate_improvement(delta):
    score = 0

    # LOC reduction is good (but not required)
    if delta.loc.delta <= 0:
        score += 1

    # CC reduction is important
    if delta.cc.delta < 0:
        score += 2

    # MI increase is important
    if delta.mi.delta > 0:
        score += 2

    if score >= 4:
        return "SIGNIFICANT_IMPROVEMENT"
    elif score >= 2:
        return "MODERATE_IMPROVEMENT"
    elif score >= 0:
        return "MINOR_IMPROVEMENT"
    else:
        return "NO_IMPROVEMENT"  # Rare for intentional refactoring
```

### 6. Display Verification Summary

```
## Verification Results

### Test Suite
- **Status**: PASSED
- **Tests Run**: 124
- **Coverage**: 85% (was 84%)

### Metrics Improvement

| Metric | Before | After | Delta | Assessment |
|--------|--------|-------|-------|------------|
| LOC | 450 | 365 | -85 (-19%) | IMPROVED |
| CC | 25 | 8.5 | -16.5 (-66%) | IMPROVED |
| MI | 45 | 71.5 | +26.5 (+59%) | IMPROVED |

### Overall Assessment
**SIGNIFICANT_IMPROVEMENT** - Refactoring achieved meaningful code quality gains.

### Code Smells Status
| Smell | Before | After |
|-------|--------|-------|
| Long Method | 2 | 0 |
| Feature Envy | 1 | 0 |
| Deep Nesting | 1 | 0 |
```

## Outputs

| Output | Destination |
|--------|-------------|
| `metrics_after` | State |
| `delta` | State |
| Test results | State |
| Verification summary | User display |

## Next Step

→ `step-07-report.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Tests fail | Investigate, offer rollback |
| Metrics worse | Warn user, but not necessarily a failure |
| Tool unavailable | Use Claude estimation |
| Coverage dropped | Flag as warning |
