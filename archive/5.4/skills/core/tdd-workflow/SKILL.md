---
name: tdd-workflow
description: >-
  Standardized TDD (Test-Driven Development) workflow for EPCI implementations.
  Manages the RED-GREEN-REFACTOR-VERIFY cycle with state tracking and error recovery.
  Use when: /epci Phase 2, /quick [C], @implementer, /ralph-exec need TDD guidance.
  Not for: Exploratory testing, manual QA processes, non-code tasks.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# TDD Workflow

## Overview

Skill standardisé pour le cycle TDD (Test-Driven Development) dans les workflows EPCI.
Gère la machine d'états RED → GREEN → REFACTOR → VERIFY avec suivi et récupération d'erreurs.

**Utilisé par:** `/epci` Phase 2, `/quick` [C], `@implementer`, `/ralph-exec`

## Configuration

| Element | Value |
|---------|-------|
| **Default test framework** | Auto-detect from stack |
| **Max retry per phase** | 2 |
| **Lint on refactor** | True |
| **Coverage threshold** | 70% (configurable) |

## TDD State Machine

```
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌─────────┐    ┌─────────┐    ┌───────────┐    ┌────────┐│
│   RED   │───▶│  GREEN  │───▶│ REFACTOR  │───▶│ VERIFY ││
└─────────┘    └─────────┘    └───────────┘    └────────┘│
     │              │               │               │     │
     │              │               │               │     │
     ▼              ▼               ▼               ▼     │
  [test           [impl          [improve        [suite   │
   fails]          passes]        code]           OK] ────┘
                                                    │
                                                    ▼
                                              [next task]
                                                  or
                                                [DONE]
```

## Phases

### Phase 1: RED (Write Failing Test)

**Goal:** Write a test that fails for the right reason.

**Actions:**
1. Create/identify test file following project conventions
2. Write test for expected behavior
3. Run test → MUST fail
4. Verify failure is for expected reason (not syntax error)

**Exit criteria:**
- Test exists and is syntactically valid
- Test runs and fails with expected assertion
- Failure message indicates missing functionality

**Output:**
```yaml
red_result:
  test_file: "tests/UserServiceTest.php"
  test_method: "test_user_can_be_activated"
  status: "FAILED"
  expected_failure: true
  failure_reason: "Method activate() does not exist"
```

### Phase 2: GREEN (Make Test Pass)

**Goal:** Write minimal code to make the test pass.

**Actions:**
1. Implement minimal solution
2. Run single test → MUST pass
3. No refactoring yet

**Rules:**
- ONLY write enough code to pass the test
- Ignore code quality for now
- No premature abstraction

**Exit criteria:**
- Test passes
- No syntax errors
- No new test failures introduced

**Output:**
```yaml
green_result:
  implementation_file: "src/Service/UserService.php"
  methods_added: ["activate"]
  lines_added: 8
  test_status: "PASSED"
```

### Phase 3: REFACTOR (Improve Code)

**Goal:** Improve code quality without changing behavior.

**Actions:**
1. Identify improvement opportunities
2. Apply refactoring (extract, rename, simplify)
3. Run lint/format
4. Run test → MUST still pass

**Common refactors:**
- Extract method/class
- Rename for clarity
- Remove duplication
- Simplify conditionals

**Exit criteria:**
- All tests still pass
- Lint passes
- No new warnings introduced

**Output:**
```yaml
refactor_result:
  changes: ["Extracted validation to separate method"]
  lint_status: "PASSED"
  test_status: "PASSED"
```

### Phase 4: VERIFY (Full Suite)

**Goal:** Ensure no regressions in full test suite.

**Actions:**
1. Run complete test suite
2. Check coverage
3. Report results

**Exit criteria:**
- All tests pass
- Coverage >= threshold (or acknowledged decrease)
- No new warnings

**Output:**
```yaml
verify_result:
  total_tests: 142
  passed: 142
  failed: 0
  coverage: 78.5
  duration: "12.3s"
  status: "PASSED"
```

## Invocation

### Input Format

```yaml
tdd_request:
  task: "Add activate method to UserService"
  test_hints:
    - "User should be activatable"
    - "Activation should update status field"
  target_file: "src/Service/UserService.php"
  test_file: "tests/UserServiceTest.php"
  stack: "php-symfony"
```

### Output Format

```yaml
tdd_result:
  status: "COMPLETED"
  phases:
    red: { status: "PASSED", iterations: 1 }
    green: { status: "PASSED", iterations: 1 }
    refactor: { status: "PASSED", iterations: 1 }
    verify: { status: "PASSED", iterations: 1 }
  files_modified: ["src/Service/UserService.php", "tests/UserServiceTest.php"]
  coverage_delta: "+2.3%"
  total_time: "45s"
```

## Stack-Specific Commands

| Stack | Test Command | Lint Command | Coverage |
|-------|--------------|--------------|----------|
| **php-symfony** | `php bin/phpunit` | `php-cs-fixer fix --dry-run` | `--coverage-text` |
| **javascript-react** | `npm test` | `npm run lint` | `--coverage` |
| **python-django** | `pytest` | `flake8` | `--cov` |
| **java-springboot** | `mvn test` | `mvn checkstyle:check` | `jacoco:report` |

## Error Recovery

### Test Failure in GREEN

```
IF test fails in GREEN phase:
  1. Analyze error message
  2. Attempt fix (max 2 retries)
  3. IF still fails:
     - Log detailed error
     - Suggest manual intervention
     - Return to RED phase
```

### Lint Failure in REFACTOR

```
IF lint fails in REFACTOR phase:
  1. Auto-fix if possible (--fix flag)
  2. IF cannot auto-fix:
     - List violations
     - Skip non-critical
     - Warn on critical
```

### Suite Failure in VERIFY

```
IF other tests fail in VERIFY phase:
  1. Identify failing tests
  2. Check if related to current changes
  3. IF regression caused:
     - Return to GREEN phase
     - Adjust implementation
  4. IF pre-existing failure:
     - Log warning
     - Continue if not critical
```

## Integration with @implementer

```markdown
### @implementer TDD Integration

For each atomic task:
1. Load tdd-workflow skill
2. Execute RED phase
3. Execute GREEN phase
4. Execute REFACTOR phase
5. Execute VERIFY phase
6. Report results
7. Move to next task or DONE
```

## Integration with /quick

```markdown
### /quick [C] Phase TDD

Mode TINY:
- Skip formal RED (test optional)
- GREEN: Direct implementation
- REFACTOR: Lint only
- VERIFY: Run existing tests

Mode SMALL:
- Full TDD cycle
- 2 retry max per phase
- Escalate if verify fails
```

## Configuration

Via `.project-memory/settings.yaml`:

```yaml
tdd:
  coverage_threshold: 70
  max_retries_per_phase: 2
  lint_on_refactor: true
  auto_fix_lint: true
  skip_verify_for_tiny: false
  test_timeout: 60  # seconds
```

## State Tracking

Session state stored in `.project-memory/sessions/`:

```yaml
tdd_session:
  task_id: "task-001"
  current_phase: "GREEN"
  phase_history:
    - phase: "RED"
      status: "COMPLETED"
      timestamp: "2025-01-16T10:30:00Z"
  retries_remaining: 2
  files_touched: ["src/Service/UserService.php"]
```

## Quick Reference

### Phase Summary

| Phase | Input | Output | Must Pass |
|-------|-------|--------|-----------|
| RED | Task description | Failing test | Test must FAIL |
| GREEN | Failing test | Minimal impl | Test must PASS |
| REFACTOR | Passing test | Improved code | Test must PASS |
| VERIFY | All changes | Full suite run | Suite must PASS |

### Skip Conditions

| Condition | Skip Phase | Rationale |
|-----------|------------|-----------|
| TINY mode | RED (optional) | Speed optimization |
| No test framework | RED, VERIFY | No infrastructure |
| Hotfix mode | REFACTOR | Critical urgency |
| 0% coverage project | VERIFY coverage | Baseline missing |

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Skip RED | No safety net | Always write test first |
| Big GREEN | Over-engineering | Minimal implementation |
| Skip REFACTOR | Tech debt | Always improve |
| Ignore VERIFY | Regressions | Full suite required |
| Test implementation | Brittle tests | Test behavior |
| Mock everything | False confidence | Prefer integration |

## See Also

| Related | Description |
|---------|-------------|
| `testing-strategy` | Test patterns and coverage |
| `@implementer` | Primary consumer |
| `/epci` Phase 2 | Implementation phase |
| `/quick` [C] | Code phase |
| `code-conventions` | Style enforcement |
