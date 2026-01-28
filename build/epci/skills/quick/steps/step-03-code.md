---
name: step-03-code
description: TDD implementation via @implementer with Red-Green-Verify cycle
prev_step: steps/step-02-mini-plan.md
next_step: steps/step-04-document.md
---

# Step 03: Code [C]

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [tdd-rules.md](../references/tdd-rules.md) | TDD cycle rules and examples |
| [breakpoint-formats.md](../references/breakpoint-formats.md#tdd-failure) | TDD failure breakpoint |

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

```typescript
Task({
  subagent_type: "implementer",
  model: "sonnet",
  prompt: `
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
  `
})
```

### 3. Execute TDD Cycle

Follow the TDD cycle as defined in [tdd-rules.md](../references/tdd-rules.md):

1. **RED Phase**: Write failing test, run to confirm failure
2. **GREEN Phase**: Write minimal code to pass, run to confirm pass
3. **VERIFY Phase**: Run ALL tests + lint, confirm no regressions
4. **REFACTOR Phase**: SKIP for /quick (speed priority)

See [tdd-rules.md](../references/tdd-rules.md) for detailed rules, examples, and stack-specific commands.

### 4. Stack-Specific Commands

| Stack | Test Command | Lint Command |
|-------|--------------|--------------|
| JavaScript | `npm test` | `npm run lint` |
| Python | `pytest` | `ruff check` |
| PHP | `./vendor/bin/phpunit` | `./vendor/bin/php-cs-fixer check` |
| Java | `./gradlew test` | `./gradlew checkstyle` |

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

AFFICHE le format depuis [breakpoint-formats.md#tdd-failure](../references/breakpoint-formats.md#tdd-failure)

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Tests en echec apres 2 tentatives. Comment proceder?",
    header: "TDD Failure",
    multiSelect: false,
    options: [
      { label: "Continuer investigation", description: "Peut prendre plus de temps mais reste dans /quick" },
      { label: "Utiliser /debug (Recommended)", description: "Workflow debugging structure" },
      { label: "Abandonner", description: "Corriger manuellement en dehors du workflow" }
    ]
  }]
})
```

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## OUTPUT FORMAT:

```
## Code Phase Complete

TDD Cycle:
- RED: Test written, failing
- GREEN: Implementation passing
- VERIFY: All tests pass

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
