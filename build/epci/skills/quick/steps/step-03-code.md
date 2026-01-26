---
name: step-03-code
description: TDD implementation via @implementer with Red-Green-Verify cycle
prev_step: steps/step-02-mini-plan.md
next_step: steps/step-04-document.md
---

# Step 03: Code [C]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip TDD cycle (Red-Green-Verify required)
- 🔴 NEVER write implementation before test
- 🔴 NEVER skip VERIFY phase
- ✅ ALWAYS invoke @implementer (Sonnet model)
- ✅ ALWAYS follow Red-Green cycle (skip Refactor for speed)
- 💭 FOCUS on minimal code that passes tests

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

If still failing after 2 retries, invoke diagnostic breakpoint:

```typescript
@skill:epci:breakpoint-system
  type: diagnostic
  title: "TDD Failure"
  data: {
    root_cause: "{identified cause or 'Unknown - needs investigation'}",
    confidence: 0.5,
    decision_tree: "RED failed → GREEN attempt 1 failed → GREEN attempt 2 failed",
    solutions: [
      {id: "S1", title: "Continue Investigation", effort: "5-10 min", risk: "Medium"},
      {id: "S2", title: "Use /debug Workflow", effort: "15-30 min", risk: "Low"},
      {id: "S3", title: "Abort and Fix Manually", effort: "Variable", risk: "Low"}
    ]
  }
  ask: {
    question: "Tests failing after 2 attempts. How to proceed?",
    header: "TDD Failure",
    options: [
      {label: "Continue Investigation", description: "May take longer but stays in /quick"},
      {label: "Use /debug (Recommended)", description: "Structured debugging workflow"},
      {label: "Abort", description: "Fix manually outside workflow"}
    ]
  }
  suggestions: [
    {pattern: "error", text: "Last error: {error message}", priority: "P1"},
    {pattern: "debug", text: "/debug provides hypothesis-driven investigation", priority: "P2"}
  ]
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
