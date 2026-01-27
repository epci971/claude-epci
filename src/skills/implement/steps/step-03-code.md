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

## DYNAMIC STACK LOADING (Per-File):

Before implementing each component, load the **complete stack skill** based on file type.

### File Type → Stack Skill Mapping

| File Type | Load Stack Skill | Action |
|-----------|------------------|--------|
| `*.py` | python-django | `Read("src/skills/stack/python-django/SKILL.md")` + tous les fichiers dans `references/` |
| `*.php` | php-symfony | `Read("src/skills/stack/php-symfony/SKILL.md")` + tous les fichiers dans `references/` |
| `*.java` | java-springboot | `Read("src/skills/stack/java-springboot/SKILL.md")` + tous les fichiers dans `references/` |
| `*.tsx`, `*.jsx`, `*.ts`, `*.js` | javascript-react | `Read("src/skills/stack/javascript-react/SKILL.md")` + tous les fichiers dans `references/` |
| `*.css`, `*.scss`, `*.html` | frontend-editor | `Read("src/skills/stack/frontend-editor/SKILL.md")` + tous les fichiers dans `references/` |

### Loading Protocol

For each component in the implementation plan:
1. **Identify** the target file(s) and their extensions
2. **Load** le stack skill complet via Read tool:
   - Lire `SKILL.md` du stack correspondant
   - Lire TOUS les fichiers dans `references/` (architecture, testing, security, etc.)
3. **Apply** ALL stack patterns: architecture, ORM/data, API, testing
4. **Use** stack-specific test commands

### Multi-File Components

If a component spans multiple file types (e.g., API endpoint + React component):
- Load ALL relevant stack skills
- Apply backend patterns for backend files
- Apply frontend patterns for frontend files
- Each file follows its stack's full conventions

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

### Before Each Component

1. Identify target file type(s) from implementation plan
2. Load complete stack skill via Read tool:
   - `Read("src/skills/stack/{stack-name}/SKILL.md")`
   - `Read("src/skills/stack/{stack-name}/references/architecture.md")`
   - `Read("src/skills/stack/{stack-name}/references/testing.md")`
   - etc.
3. All patterns available: architecture, ORM, API, testing, etc.

### Component: {name} [{file-type} → {stack}]

**Stack loaded:** `{stack-name}` via Read ✓

#### RED: Write failing test
- Follow {stack} testing patterns (from SKILL.md + references/testing.md)
- Use {stack} test framework conventions
- Apply {stack} assertion style

```{language}
// {stack-specific test path}
// Example: tests/test_{component}.py (Django)
// Example: __tests__/{component}.test.tsx (React)
{test code following stack patterns}
```

#### Run test: FAIL 🔴
```bash
# Use stack-specific command
{stack test command} → Expected failure
```

#### GREEN: Implement
- Follow {stack} architecture patterns (from SKILL.md + references/architecture.md)
- Apply {stack} ORM/data patterns if applicable
- Respect {stack} anti-patterns list

```{language}
// {stack-specific source path}
{minimal implementation following stack conventions}
```

#### Run test: PASS ✅
```bash
{stack test command} → Pass
```

#### REFACTOR: Improve
- Apply {stack} code conventions
- Check against {stack} anti-patterns
- Run full test suite to verify no regressions

#### Run test: PASS ✅
```bash
{stack test command} → Still passing
```

### Unmapped File Types

For extensions not in the mapping table:
- Use generic TDD cycle without stack-specific patterns
- Follow project conventions from CLAUDE.md
- Apply standard Arrange/Act/Assert structure

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
