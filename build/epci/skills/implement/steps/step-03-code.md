---
name: step-03-code
description: TDD implementation phase [C]
prev_step: steps/step-03b-team.md
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

### 0. Initialize Circuit Breaker Tracking

Track component failures to detect cascading problems early:

```
consecutive_failures = 0
total_failed = 0
total_attempted = 0
total_skipped = 0
```

1. **Follow** implementation plan order
   - Start with Phase 1 components
   - Complete each component before moving to next
   - **Check dependencies**: Before each component, verify its depends_on components are SUCCESS
     - If any dependency is FAILED or SKIPPED: mark component as SKIPPED, total_skipped += 1, warn user

2. **For each component**, execute TDD cycle (see tdd-rules.md importé ci-dessus):
   - **RED Phase**: Write failing test, verify it fails for the right reason
   - **GREEN Phase**: Write minimal implementation to pass
   - **REFACTOR Phase**: Improve code quality, run tests to confirm

3. **Update** Feature Document §3 (after EACH completed component)

   Path: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md` (from `artifacts.feature_doc`)

   **First component** — Replace the placeholder:

   EXECUTE Edit({
     file_path: "{feature_doc_path}",
     old_string: "## §3 — Implementation\n> Section remplie progressivement par step-03-code [C]\n\n*En attente de la phase Code...*",
     new_string: "## §3 — Implementation\n> Rempli progressivement par step-03-code [C]\n\n### Composants implementes\n| Composant | Fichier | Tests | Status |\n|-----------|---------|-------|--------|\n| {component_name} | {file_path} | {test_count} passing | DONE |\n\n### Deviations du plan\nAucune\n\n### Coverage\n- Actuelle: {current_coverage}%\n- Cible: {target_coverage}%"
   })

   **Subsequent components** — Append row to table:

   EXECUTE Edit({
     file_path: "{feature_doc_path}",
     old_string: "| {previous_component} | {prev_path} | {prev_tests} passing | DONE |",
     new_string: "| {previous_component} | {prev_path} | {prev_tests} passing | DONE |\n| {new_component} | {new_path} | {new_tests} passing | DONE |"
   })

   Also update Coverage section and Deviations if any occurred.

4. **Launch background Code Reviewer** (Team Mode only)

   IF team_config.mode == "active" AND team_config.parallel_agents.code_reviewer.enabled:

   After the first complete component (or at 50% plan completion), launch the Code Reviewer in background:

   ```
   LANCE Task({
     subagent_type: "code-reviewer",
     model: "opus",
     run_in_background: true,
     prompt: `
   ## Files to Review
   {files_completed_so_far}

   ## Original Requirements
   {feature_requirements}

   ## Implementation Plan Summary
   {plan_summary}

   ## Review Focus
   - Code quality: patterns, naming, error handling
   - Test coverage: target {coverage_target}% minimum
   - Security: OWASP Top 10 awareness
   - Plan alignment: implementation matches plan

   ## Expected Output
   Review report with:
   - Files reviewed count
   - Issues found (Critical/Important/Minor)
   - Test coverage assessment
   - Verdict: APPROVED / CHANGES_REQUIRED / SECURITY_REVIEW_NEEDED
     `
   })
   ```

   Store the background task ID for step-04-review aggregation.
   LOG "Code Reviewer launched in background (team mode)"

   Continue implementing remaining components while reviewer runs.

5. **Update Circuit Breaker** after each component

   ```
   total_attempted += 1

   IF component.status == "SUCCESS":
     consecutive_failures = 0
   ELIF component.status == "FAILED":
     consecutive_failures += 1
     total_failed += 1
   ```

   **Circuit Breaker Alert** (breakpoint `diagnostic`):

   IF consecutive_failures >= 3 OR (total_attempted >= 4 AND total_failed / total_attempted > 0.5):

   Present a diagnostic breakpoint via AskUserQuestion:

   ```
   "3 consecutive component failures detected" OR ">50% failure rate ({total_failed}/{total_attempted})"

   Options:
   [A] Continuer malgre les echecs — Keep implementing remaining components
   [B] Investiguer — Switch to /debug for root cause analysis
   [C] Abandonner — Stop implementation, proceed to review with partial results
   ```

   - If user chooses Continue: reset consecutive_failures, continue
   - If user chooses Investigate: invoke /debug skill, then resume
   - If user chooses Abandon: skip remaining components, proceed to step-04-review

6. **Invoke** tdd-enforcer periodically
   - Verify TDD compliance
   - Check coverage targets

## CONTEXT BOUNDARIES:

- This step expects: Approved implementation plan, test strategy, feature_doc_path (from step-00)
- This step produces: Working code, passing tests, Feature Document §3 filled incrementally

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
