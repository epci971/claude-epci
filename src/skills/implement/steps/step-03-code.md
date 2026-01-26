---
name: step-03-code
description: TDD implementation phase [C]
prev_step: steps/step-02-plan.md
next_step: steps/step-04-review.md
---

# Step 03: Code [C]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER write implementation before test
- 🔴 NEVER skip the RED phase (failing test first)
- 🔴 NEVER commit code with failing tests
- 🔴 NEVER over-engineer beyond requirements
- ✅ ALWAYS follow TDD cycle: RED → GREEN → REFACTOR
- ✅ ALWAYS write minimal code to pass test
- ✅ ALWAYS run tests after each change
- ✅ ALWAYS follow identified patterns from exploration
- ⛔ FORBIDDEN skipping tests for any component
- 🔵 YOU ARE A DISCIPLINED TDD PRACTITIONER
- 💭 FOCUS on one test at a time, complete cycle before next

## EXECUTION PROTOCOLS:

1. **Follow** implementation plan order
   - Start with Phase 1 components
   - Complete each component before moving to next

2. **For each component**, execute TDD cycle:

   ### RED Phase
   a. Write failing test that defines expected behavior
   b. Run test to confirm it fails
   c. Verify test fails for the right reason

   ### GREEN Phase
   a. Write minimal implementation to pass test
   b. Run test to confirm it passes
   c. Verify no other tests broken

   ### REFACTOR Phase
   a. Improve code quality without changing behavior
   b. Run tests to confirm all still pass
   c. Apply identified patterns from exploration

3. **Update** progress in Feature Document
   - Mark components as completed
   - Record test coverage
   - Note any deviations from plan

4. **Invoke** tdd-enforcer periodically
   - Verify TDD compliance
   - Check coverage targets

## CONTEXT BOUNDARIES:

- This step expects: Approved implementation plan, test strategy
- This step produces: Working code, passing tests, updated Feature Document

## TDD CYCLE TEMPLATE:

```
## Component: {name}

### RED: Write failing test
```{language}
// test/{component}.test.ts
describe('{component}', () => {
  it('should {expected behavior}', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

### Run test: FAIL 🔴
{test output showing failure}

### GREEN: Implement
```{language}
// src/{component}.ts
{minimal implementation}
```

### Run test: PASS ✅
{test output showing pass}

### REFACTOR: Improve
{refactoring notes if any}

### Run test: PASS ✅
{confirm tests still pass}
```

## OUTPUT FORMAT:

```
## Coding Progress

### Completed Components
- ✅ {Component 1} — {N} tests passing
- ✅ {Component 2} — {N} tests passing

### In Progress
- ⏳ {Component 3} — RED phase

### Test Coverage
- Current: {%}
- Target: {%}
```

## NEXT STEP TRIGGER:

When all planned components are implemented with passing tests,
proceed to `step-04-review.md`.
