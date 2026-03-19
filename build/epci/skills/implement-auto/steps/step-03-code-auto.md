---
name: step-03-code-auto
description: TDD implementation with stack skills, circuit breaker, and background reviewer [C]
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
@../references/domain-mapping.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER write implementation before test (TDD RED first)
- NEVER skip circuit breaker checks after each component
- NEVER continue after task-level circuit breaker triggers
- ALWAYS load stack skill before implementing a component (per file extension)
- ALWAYS follow TDD cycle: RED -> GREEN -> REFACTOR
- ALWAYS update JSON output after each component
- ALWAYS check dependencies before starting a component
- ALWAYS follow patterns identified in exploration and stack skills

## EXECUTION PROTOCOLS:

### 1. Initialize Tracking

```
consecutive_failures = 0
total_failed = 0
total_attempted = 0
total_skipped = 0
stack_cache = {}  # Cache loaded stack skills (load once per type)
background_reviewer_task_id = null
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

#### 2b. Load Stack Skill (per file extension)

Before implementing the component, identify the target file extension and load the corresponding stack skill:

```
ext = get_extension(component.file)
stack = extension_to_stack(ext)  # See domain-mapping.md

IF stack AND stack NOT IN stack_cache:
  ## Load stack skill SKILL.md + all references/
  Read(src/skills/stack/{stack}/SKILL.md)
  FOR each ref_file in Glob("src/skills/stack/{stack}/references/*.md"):
    Read(ref_file)
  stack_cache[stack] = true
  LOG: "Loaded stack skill: {stack}"

## Extension to stack mapping:
## *.py           → python-django
## *.php          → php-symfony
## *.java         → java-springboot
## *.tsx,*.jsx,*.ts,*.js → javascript-react
## *.css,*.scss,*.html   → frontend-editor
## Other          → No stack skill (use project CLAUDE.md/rules only)
```

Apply ALL loaded stack patterns for this component: architecture, ORM/data, API, testing conventions.

#### 2c. TDD Cycle

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
  - Apply stack skill testing patterns (e.g., pytest fixtures for Django, @SpringBootTest for Spring)

  Run tests: execute test command for this component
  - Stack-specific commands:
    - python-django: pytest {test_file} -v
    - php-symfony: ./vendor/bin/phpunit --filter {test}
    - java-springboot: ./gradlew test --tests "{TestClass}"
    - javascript-react: npm test -- {file} or npx vitest run {file}
  - Expected: test FAILS (exit code != 0)
  - If test PASSES: implementation already exists, mark SUCCESS, break
  - If syntax error: fix test, do NOT count as attempt

  ## GREEN Phase
  Write minimal implementation at component.file
  - Follow patterns from exploration and stack skill
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
  - Apply identified patterns from stack skill
  - Check against stack anti-patterns
  - Remove duplication
  - Improve naming

  Run tests: verify still passing after refactor
  - If PASS: Mark component SUCCESS, BREAK
  - If FAIL: Revert refactor changes, mark SUCCESS (GREEN was passing)
```

#### 2d. Update Component Status

```
total_attempted += 1

IF component.status == "SUCCESS":
  consecutive_failures = 0
ELIF component.status == "FAILED":
  consecutive_failures += 1
  total_failed += 1
```

#### 2e. Circuit Breaker Check (Level 2 - Task)

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

#### 2f. Launch Background Code Reviewer (once at 50%)

```
IF flag_skip_review == false
   AND background_reviewer_task_id == null
   AND total_attempted >= (plan.total_components / 2):

  ## Get list of files modified so far
  completed_files = [c.file for c in plan.components if c.status == "SUCCESS"]

  LANCE Task({
    subagent_type: "code-reviewer",
    model: "opus",
    run_in_background: true,
    prompt: "
      ## Code Review Request (Background - Partial)
      Feature: {feature_slug}
      Requirements: {spec_requirements}

      ## Files to Review
      {completed_files}

      ## Context
      - Patterns from exploration: {patterns}
      - Stack skills loaded: {stack_cache.keys()}
      - Plan: {plan_summary}

      ## Review Focus
      - Code quality: patterns, naming, error handling
      - Test coverage: verify meaningful tests (target {70% or 80%})
      - Security: OWASP Top 10 awareness
      - Plan alignment: implementation matches plan

      ## Expected Output
      Verdict: APPROVED | CHANGES_REQUIRED | SECURITY_REVIEW_NEEDED
      Findings list with severity (Critical, High, Medium, Low, Info)
    "
  })

  background_reviewer_task_id = {task_id}
  LOG: "Background code reviewer launched at {total_attempted}/{plan.total_components} components"
```

#### 2g. Update JSON Output (Incremental)

After each component, update `.implement-auto-output.json`:
- Update `plan.components[i].status`
- Update `plan.components[i].tests_added`
- Update `plan.components[i].retries`
- Update `plan.components[i].error` if failed
- Update `metrics.files_created` / `metrics.files_modified`
- Update `metrics.tests_added`

#### 2h. Update Feature Document §3 (Incremental)

Use Edit tool to update Implementation section:

For the first component, replace the placeholder:
```
old: "*En attente de la phase Code...*"
new: "| {name} | {file} | {test_count} passing | {stack_skill} | {status} |"
```

For subsequent components, append row after the last component entry in the table.

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

Store `background_reviewer_task_id` in execution context for step-04.

## CONTEXT BOUNDARIES:

- This step expects: Ordered component plan from step-02, exploration patterns, complexity level
- This step produces: Implemented components with stack-specific patterns, test results, background reviewer (if launched), updated JSON and Feature Doc

## NEXT STEP TRIGGER:

On completion (all components processed), proceed to step-04-review-auto.md.
On circuit breaker trigger, jump to step-06-finish-auto.md.
