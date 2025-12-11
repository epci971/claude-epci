---
description: >-
  Complete EPCI workflow in 3 phases for STANDARD and LARGE features.
  Phase 1: Analysis and planning. Phase 2: TDD implementation.
  Phase 3: Finalization and documentation. Includes breakpoints between phases.
argument-hint: "[--large] [--continue]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI — Complete Workflow

## Overview

Structured workflow in 3 phases with validation at each step.
Generates a Feature Document as traceability thread.

## Arguments

| Argument | Description |
|----------|-------------|
| `--large` | Activates LARGE mode (enhanced thinking, all subagents mandatory) |
| `--continue` | Continue from last phase (resume after interruption) |

## Feature Document

Create/update file: `docs/features/<feature-slug>.md`

```markdown
# Feature Document — [Title]

## §1 — Functional Brief
[Copied from /epci-brief or generated here]

## §2 — Implementation Plan
[Generated in Phase 1]

## §3 — Implementation
[Updated in Phase 2]

## §4 — Finalization
[Completed in Phase 3]
```

---

## Phase 1: Analysis and Planning

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` |
| **Skills** | epci-core, architecture-patterns, [stack] |
| **Subagents** | @Plan (native), @plan-validator |

### Process

1. **Brief reception**
   - Verify brief is complete (comes from `/epci-brief`)
   - If incomplete → suggest `/epci-brief` first

2. **Technical analysis** (via @Plan)
   - Identify impacted files
   - Analyze dependencies
   - Evaluate technical risks

3. **Plan generation**
   - Break down into atomic tasks (2-15 min each)
   - Order by dependencies
   - Plan a test for each task

4. **Validation** (via @plan-validator)
   - Submit plan to validator
   - If NEEDS_REVISION → correct and resubmit
   - If APPROVED → proceed to breakpoint

### Output §2

```markdown
## §2 — Implementation Plan

### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/Service/X.php | Modify | Medium |
| src/Entity/Y.php | Create | Low |
| tests/Unit/XTest.php | Create | Low |

### Tasks
1. [ ] **Create entity Y** (5 min)
   - File: `src/Entity/Y.php`
   - Test: `tests/Unit/Entity/YTest.php`

2. [ ] **Modify service X** (10 min)
   - File: `src/Service/X.php`
   - Test: `tests/Unit/Service/XTest.php`

### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking change | Medium | Regression tests |

### Validation
- **@plan-validator**: APPROVED
```

### ⏸️ BREAKPOINT

```
---
⏸️ **BREAKPOINT PHASE 1**

Plan complete and validated.
- @plan-validator: APPROVED
- Tasks: X tasks identified
- Files: Y files impacted

Feature Document §2 updated.

**Awaiting confirmation:** "Continue" or "Plan validated"
---
```

---

## Phase 2: Implementation

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` |
| **Skills** | testing-strategy, code-conventions, [stack] |
| **Subagents** | @code-reviewer (mandatory), @security-auditor*, @qa-reviewer* |

### Conditional Subagents

**@security-auditor** if detection of:
- Files: `**/auth/**`, `**/security/**`, `**/api/**`, `**/password/**`
- Keywords: `password`, `secret`, `api_key`, `jwt`, `oauth`

**@qa-reviewer** if:
- More than 5 test files created/modified
- Integration or E2E tests involved
- Complex mocking detected

### Process

For each task in the plan:

```
1. RED — Write the failing test
2. Execute → confirm failure
3. GREEN — Implement minimal code
4. Execute → confirm passing
5. REFACTOR — Improve if necessary
6. Check off the task ✓
```

After all tasks:
1. Run complete test suite
2. Invoke @code-reviewer
3. Invoke @security-auditor (if applicable)
4. Invoke @qa-reviewer (if applicable)
5. Fix Critical/Important issues

### Output §3

```markdown
## §3 — Implementation

### Progress
- [x] Task 1 — Create entity Y
- [x] Task 2 — Modify service X
- [x] Task 3 — Add validation

### Tests
```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews
- **@code-reviewer**: APPROVED (0 Critical, 2 Minor)
- **@security-auditor**: APPROVED
- **@qa-reviewer**: N/A

### Deviations
| Task | Deviation | Justification |
|------|-----------|---------------|
| #3 | +1 file | Helper extraction |
```

### ⏸️ BREAKPOINT

```
---
⏸️ **BREAKPOINT PHASE 2**

Code implemented and validated.
- Tests: X/X passing
- @code-reviewer: APPROVED

Feature Document §3 updated.

**Awaiting confirmation:** "Continue" or "Code validated"
---
```

---

## Phase 3: Finalization

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` |
| **Skills** | git-workflow |
| **Subagents** | @doc-generator |

### Process

1. **Structured commit**
   ```
   feat(scope): short description

   - Detail 1
   - Detail 2

   Refs: docs/features/<slug>.md
   ```

2. **Documentation** (via @doc-generator)
   - Generate/update README if new component
   - Document API changes if applicable
   - Update CHANGELOG

3. **PR preparation**
   - Create branch if not done
   - Prepare PR template
   - List reviewers

### Output §4

```markdown
## §4 — Finalization

### Commit
```
feat(user): add email validation

- Create EmailValidator service
- Add validation to User entity
- Update registration controller

Refs: docs/features/user-email-validation.md
```

### Documentation
- **@doc-generator**: 2 files updated
  - README.md (Configuration section)
  - CHANGELOG.md (v1.2.0)

### PR Ready
- Branch: `feature/user-email-validation`
- Tests: ✅ All passing
- Lint: ✅ Clean
- Docs: ✅ Up to date
```

### ✅ COMPLETION

```
---
✅ **FEATURE COMPLETE**

Feature Document finalized: docs/features/<slug>.md
- Phase 1: Plan validated
- Phase 2: Code implemented and reviewed
- Phase 3: Commit and documentation

**Next step:** Create PR or merge
---
```

---

## --large Mode

In `--large` mode, the differences are:

| Aspect | Standard | Large |
|--------|----------|-------|
| Thinking P1 | `think hard` | `ultrathink` |
| @security-auditor | Conditional | Mandatory |
| @qa-reviewer | Conditional | Mandatory |
| Breakpoints | Simple confirmation | Explicit validation |
| Feature Document | Standard | Extended with risk sections |
