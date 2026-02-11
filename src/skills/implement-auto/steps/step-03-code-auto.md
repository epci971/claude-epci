---
name: step-03-code-auto
description: TDD implementation with 3-level circuit breaker [C]
prev_step: steps/step-02-plan-auto.md
next_step: steps/step-04-review-auto.md
conditional_next:
  - condition: "circuit_breaker_task_triggered"
    step: steps/step-06-finish-auto.md
---

# Step 03: Code (Auto) [C]

## Reference Files

@../references/tdd-rules.md
@../references/circuit-breaker-rules.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER write implementation before test (TDD RED first)
- NEVER skip circuit breaker checks after each component
- NEVER continue after task-level circuit breaker triggers
- ALWAYS follow TDD cycle: RED -> GREEN -> REFACTOR
- ALWAYS update JSON output after each component
- ALWAYS check dependencies before starting a component
- ALWAYS follow patterns identified in exploration

## EXECUTION PROTOCOLS:

### 1. Initialize Tracking

```
consecutive_failures = 0
total_failed = 0
total_attempted = 0
total_skipped = 0
```

### 2. For Each Component (in plan order)

```
FOR each component in plan.components:
```

#### 2a. Check Dependencies

```
FOR each dep in component.depends_on:
  dep_status = get_component_status(dep)
  IF dep_status == "FAILED" or dep_status == "SKIPPED":
    Mark component as SKIPPED
    total_skipped += 1
    Log warning: "Skipped {component.name}: depends on failed {dep}"
    Update JSON output
    CONTINUE to next component
```

#### 2b. TDD Cycle

Execute for this component (max 2 attempts per circuit-breaker-rules.md):

```
attempts = 0
MAX_ATTEMPTS = 2

WHILE attempts < MAX_ATTEMPTS:
  attempts += 1

  ## RED Phase
  Write test file at component.test_file
  - Define expected behavior based on spec requirements
  - Use project test framework (detected in explore)
  - Follow project conventions from CLAUDE.md/rules/

  Run tests: execute test command for this component
  - Expected: test FAILS (exit code != 0)
  - If test PASSES: implementation already exists, mark SUCCESS, break
  - If syntax error: fix test, do NOT count as attempt

  ## GREEN Phase
  Write minimal implementation at component.file
  - Follow patterns from exploration
  - Use project conventions from CLAUDE.md/rules/
  - Write only enough code to make the test pass

  Run tests: execute test command for this component
  - If PASS: proceed to REFACTOR
  - If FAIL:
    IF attempts < MAX_ATTEMPTS:
      Analyze failure, adjust implementation
      CONTINUE (retry)
    ELSE:
      Mark component FAILED
      BREAK

  ## REFACTOR Phase
  Review implementation for quality:
  - Apply identified patterns
  - Remove duplication
  - Improve naming

  Run tests: verify still passing after refactor
  - If PASS: Mark component SUCCESS, BREAK
  - If FAIL: Revert refactor changes, mark SUCCESS (GREEN was passing)
```

#### 2c. Update Component Status

```
total_attempted += 1

IF component.status == "SUCCESS":
  consecutive_failures = 0
ELIF component.status == "FAILED":
  consecutive_failures += 1
  total_failed += 1
```

#### 2d. Circuit Breaker Check (Level 2 - Task)

```
## Check consecutive failures
IF consecutive_failures >= 3:
  ABORT task
  status = "FAILED"
  exit_reason = "circuit_breaker_consecutive"
  GOTO step-06-finish-auto

## Check failure rate (after at least 4 attempts)
IF total_attempted >= 4 AND (total_failed / total_attempted) > 0.5:
  ABORT task
  status = "FAILED"
  exit_reason = "circuit_breaker_rate"
  GOTO step-06-finish-auto
```

#### 2e. Update JSON Output (Incremental)

After each component, update `.implement-auto-output.json`:
- Update `plan.components[i].status`
- Update `plan.components[i].tests_added`
- Update `plan.components[i].retries`
- Update `plan.components[i].error` if failed
- Update `metrics.files_created` / `metrics.files_modified`
- Update `metrics.tests_added`

#### 2f. Update Feature Document §3 (Incremental)

Use Edit tool to update Implementation Log section:

For the first component, replace the placeholder:
```
old: "*En attente de la phase Code...*"
new: "### Component: {name}\n- Status: {status}\n- Tests: {count}\n- File: {file}"
```

For subsequent components, append after the last component entry.

### 3. Run Full Test Suite

After all components are processed:

```bash
{test_command_full_suite}
```

Record results:
- `metrics.tests_passing` = count of passing tests
- `metrics.tests_failing` = count of failing tests

### 4. Determine Intermediate Status

```
IF total_failed == 0 AND total_skipped == 0:
  intermediate_status = "SUCCESS"
ELIF total_failed == total_attempted:
  intermediate_status = "FAILED"
  exit_reason = "all_components_failed"
ELSE:
  intermediate_status = "PARTIAL"
  exit_reason = "partial_implementation"
```

### 5. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "code"
- `phases.current` = "review"
- Update all metrics

## CONTEXT BOUNDARIES:

- This step expects: Ordered component plan from step-02, exploration patterns
- This step produces: Implemented components, test results, updated JSON and Feature Doc

## NEXT STEP TRIGGER:

On completion (all components processed), proceed to step-04-review-auto.md.
On circuit breaker trigger, jump to step-06-finish-auto.md.
