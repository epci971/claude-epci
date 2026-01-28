---
name: step-03-code
description: TDD implementation phase [C]
prev_step: steps/step-02-plan.md
next_step: steps/step-04-review.md
---

# Step 03: Code [C]

## Reference Files

@../references/tdd-rules.md

| Reference | Purpose |
|-----------|---------|
| tdd-rules.md | TDD cycle and coverage rules |

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

## DYNAMIC STACK LOADING (Per-File):

Before implementing each component, load the **complete stack skill** based on file type.

### File Type → Stack Skill Mapping

| File Type | Load Stack Skill | Action |
|-----------|------------------|--------|
| `*.py` | python-django | Read SKILL.md + all `references/` files |
| `*.php` | php-symfony | Read SKILL.md + all `references/` files |
| `*.java` | java-springboot | Read SKILL.md + all `references/` files |
| `*.tsx`, `*.jsx`, `*.ts`, `*.js` | javascript-react | Read SKILL.md + all `references/` files |
| `*.css`, `*.scss`, `*.html` | frontend-editor | Read SKILL.md + all `references/` files |

### Loading Protocol

For each component in the implementation plan:
1. **Identify** the target file(s) and their extensions
2. **Load** the complete stack skill via Read tool
3. **Apply** ALL stack patterns: architecture, ORM/data, API, testing
4. **Use** stack-specific test commands

### Stack-Specific Test Commands

| Stack | Test Command | Coverage |
|-------|--------------|----------|
| `python-django` | `pytest {test_file} -v` | `pytest --cov={module}` |
| `php-symfony` | `./vendor/bin/phpunit --filter {test}` | `phpunit --coverage-text` |
| `java-springboot` | `./gradlew test --tests "{TestClass}"` | `./gradlew jacocoTestReport` |
| `javascript-react` | `npm test -- {file}` | `npm test -- --coverage` |
| `frontend-editor` | `npm test -- {file}` | N/A (a11y checks) |

## EXECUTION PROTOCOLS:

1. **Follow** implementation plan order
   - Start with Phase 1 components
   - Complete each component before moving to next

2. **For each component**, execute TDD cycle (see tdd-rules.md importé ci-dessus):
   - **RED Phase**: Write failing test, verify it fails for the right reason
   - **GREEN Phase**: Write minimal implementation to pass
   - **REFACTOR Phase**: Improve code quality, run tests to confirm

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

### Before Each Component

1. Identify target file type(s) from implementation plan
2. Load complete stack skill via Read tool
3. All patterns available: architecture, ORM, API, testing, etc.

### Component Implementation

**Stack loaded:** `{stack-name}` via Read

1. **RED**: Write failing test following stack testing patterns
2. **Run test**: Expected failure
3. **GREEN**: Implement minimal code following stack conventions
4. **Run test**: Pass
5. **REFACTOR**: Improve code quality, check against stack anti-patterns
6. **Run test**: Still passing

### Unmapped File Types

For extensions not in the mapping table:
- Use generic TDD cycle without stack-specific patterns
- Follow project conventions from CLAUDE.md
- Apply standard Arrange/Act/Assert structure

## OUTPUT FORMAT:

```
## Coding Progress

### Completed Components
- {Component 1} - {N} tests passing
- {Component 2} - {N} tests passing

### In Progress
- {Component 3} - RED phase

### Test Coverage
- Current: {%}
- Target: {%}
```

## NEXT STEP TRIGGER:

When all planned components are implemented with passing tests,
proceed to `step-04-review.md`.
