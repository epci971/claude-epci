---
name: step-04-review-auto
description: Self-review checklist and optional deep review [I]
prev_step: steps/step-03-code-auto.md
next_step: steps/step-05-document-auto.md
---

# Step 04: Review (Auto) [I]

## Reference Files

@../references/review-checklist.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- ALWAYS execute self-review checklist
- ALWAYS record findings in JSON output
- ALWAYS continue even if critical findings (headless mode)

## EXECUTION PROTOCOLS:

### 1. Self-Review Checklist

Execute each check from review-checklist.md on all modified/created files.

#### Tests Quality Checks

| Check | Command |
|-------|---------|
| T1: All tests pass | Run full test suite, verify exit code 0 |
| T2: Tests exist per component | Count test files vs plan components |
| T5: No skipped tests | Grep for skip/xit/xdescribe/pytest.mark.skip |

#### Code Quality Checks

| Check | Command |
|-------|---------|
| C1: No debug prints | Grep for `print(` / `console.log` in created/modified files |
| C2: No hardcoded secrets | Grep for `password\|secret\|api_key\|token` patterns |
| C3: No commented-out code | Grep for large comment blocks (3+ consecutive comment lines) |
| C4: No TODO/FIXME | Grep for `TODO\|FIXME\|HACK\|XXX` in created files |

#### Security Basics Checks

| Check | Command |
|-------|---------|
| S1: No SQL injection | Grep for string concatenation in SQL (f-string + SELECT/INSERT) |
| S2: No command injection | Grep for `os.system\|subprocess.call.*shell=True\|exec(` |

### 2. Record Results

Build self_review object:

```json
{
  "status": "pass | warn | fail",
  "items_checked": 10,
  "items_passed": 8,
  "items_warned": 2,
  "findings": [
    {
      "check_id": "C1",
      "severity": "error",
      "message": "Debug print found",
      "file": "path/to/file.py",
      "line": 42
    }
  ]
}
```

Status determination:
- `pass`: 0 findings
- `warn`: findings exist but none critical
- `fail`: critical findings exist (still continues in headless mode)

### 3. Invoke Code-Reviewer Agent (--with-review)

IF `flag_with_review` is true:

```
LANCE Task({
  subagent_type: "code-reviewer",
  model: "opus",
  prompt: "
    Review these files for quality, architecture, and test coverage:
    {list of modified/created files}

    Context:
    - Feature: {feature_slug}
    - Spec requirements: {spec_summary}
    - Identified patterns: {patterns_from_explore}

    Output format:
    - findings: [{severity, file, line, message, suggestion}]
    - overall_assessment: string
    - recommendation: APPROVE | NEEDS_CHANGES
  "
})
```

If subagent completes: merge results into `checks.deep_review` in JSON.
If subagent times out: add warning "code-reviewer timeout, using self-review only".

### 4. Update Feature Document §4

Use Edit tool to update the Review section:

```
## Review

### Self-Review Results
- Status: {self_review.status}
- Checks: {items_passed}/{items_checked} passed
- Findings: {items_warned} warnings
{list of findings if any}

### Deep Review (optional)
{deep review results if --with-review}
```

### 5. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "review"
- `phases.current` = "document"
- `checks.self_review` = self_review results
- `checks.deep_review` = deep review results (if applicable)

## CONTEXT BOUNDARIES:

- This step expects: Implemented components from step-03, list of modified files
- This step produces: Review findings, updated Feature Doc §4, updated JSON

## NEXT STEP TRIGGER:

Always proceed to step-05-document-auto.md (review never blocks in headless mode).
