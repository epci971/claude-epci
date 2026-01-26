---
name: step-03-code
description: TDD implementation via @implementer with Red-Green-Verify cycle
prev_step: steps/step-02-mini-plan.md
next_step: steps/step-04-document.md
---

# Step 03: Code [C]

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip TDD cycle (Red-Green-Verify required)
- :red_circle: NEVER write implementation before test
- :red_circle: NEVER skip VERIFY phase
- :white_check_mark: ALWAYS invoke @implementer (Sonnet model)
- :white_check_mark: ALWAYS follow Red-Green cycle (skip Refactor for speed)
- :thought_balloon: FOCUS on minimal code that passes tests

## EXECUTION PROTOCOLS:

### 1. Prepare Implementation Context

Gather context for @implementer:

```
IMPLEMENTATION CONTEXT:
├── Plan: {from step-02 or @plan-path}
├── Target Files: {list}
├── Test Strategy: {framework, cases}
├── Stack Patterns: {from detected stack skill}
└── Completion Criteria: {measurable}
```

### 2. Invoke @implementer (Sonnet)

Spawn Task with implementer agent:

```
@implementer

## Task
{objective from plan}

## Files
{target files list}

## Test Strategy
{test cases to write}

## Patterns to Follow
{from stack skill and exploration}

## TDD Mode
Red-Green-Verify (skip Refactor)
```

### 3. TDD Cycle: RED

Write failing test first:

```
┌─────────────────────────────────────────┐
│ RED PHASE                                │
├─────────────────────────────────────────┤
│ 1. Write test that describes behavior   │
│ 2. Run test → MUST FAIL                 │
│ 3. If test passes → test is wrong       │
└─────────────────────────────────────────┘
```

**Verification:**
```bash
# Run test, expect failure
npm test -- --testPathPattern="file.test.ts"
# Expected: FAIL
```

### 4. TDD Cycle: GREEN

Write minimal code to pass:

```
┌─────────────────────────────────────────┐
│ GREEN PHASE                              │
├─────────────────────────────────────────┤
│ 1. Write minimal code to pass test      │
│ 2. No extra features, no optimization   │
│ 3. Run test → MUST PASS                 │
└─────────────────────────────────────────┘
```

**Rules:**
- Minimal changes only
- Follow existing patterns
- No premature optimization
- No extra features

**Verification:**
```bash
# Run test, expect pass
npm test -- --testPathPattern="file.test.ts"
# Expected: PASS
```

### 5. TDD Cycle: VERIFY

Final verification:

```
┌─────────────────────────────────────────┐
│ VERIFY PHASE                             │
├─────────────────────────────────────────┤
│ 1. Run ALL tests (not just new ones)    │
│ 2. Run linter                           │
│ 3. Confirm no regressions               │
└─────────────────────────────────────────┘
```

**Commands (by stack):**

| Stack | Test Command | Lint Command |
|-------|--------------|--------------|
| JavaScript | `npm test` | `npm run lint` |
| Python | `pytest` | `ruff check` |
| PHP | `./vendor/bin/phpunit` | `./vendor/bin/php-cs-fixer check` |
| Java | `./gradlew test` | `./gradlew checkstyle` |

### 6. Skip REFACTOR (Speed Priority)

For /quick, skip refactoring phase:

```
┌─────────────────────────────────────────┐
│ REFACTOR PHASE                           │
├─────────────────────────────────────────┤
│ SKIPPED for /quick                       │
│                                          │
│ Rationale: Speed > perfection            │
│ If refactor needed → use /refactor later │
└─────────────────────────────────────────┘
```

## CONTEXT BOUNDARIES:

- This step expects: Plan (from step-02 or @plan-path)
- This step produces: Working implementation with passing tests
- Agent: @implementer (Sonnet model)

## TDD FAILURE HANDLING:

If tests fail after GREEN:

```
RETRY PROTOCOL:
├── Attempt 1: Fix implementation
│   └─ Re-run tests
├── Attempt 2: Fix implementation differently
│   └─ Re-run tests
└── Attempt 3: ESCALATE
    └─ Suggest /debug or manual investigation
```

**Max retries: 2**

If still failing after 2 retries:

```
┌─────────────────────────────────────────────────────────────────┐
│ [TDD FAILURE] Tests Not Passing                                  │
├─────────────────────────────────────────────────────────────────┤
│ Attempts: 2/2                                                    │
│ Last Error: {error message}                                      │
│                                                                  │
│ Options:                                                         │
│ 1. Continue investigation (may take longer)                      │
│ 2. Use /debug to investigate                                     │
│ 3. Abort and fix manually                                        │
└─────────────────────────────────────────────────────────────────┘
```

## OUTPUT FORMAT:

```
## Code Phase Complete

TDD Cycle:
- RED: Test written, failing ✓
- GREEN: Implementation passing ✓
- VERIFY: All tests pass ✓

Files Modified:
- {path/to/file1.ts} (+{N} LOC)
- {path/to/file2.test.ts} (+{N} LOC)

Tests:
- {test_count} new tests
- All passing

Ready for documentation check.
```

## NEXT STEP TRIGGER:

Proceed to step-04-document.md with implementation complete.
