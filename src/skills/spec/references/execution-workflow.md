# Execution Workflow

> TDD rules, task completion protocol, and error handling for Ralph execution.

## Overview

This reference defines the mandatory execution rules that Claude Code must follow when executing Ralph tasks. These rules ensure consistent, high-quality implementation.

---

## TDD Cycle Rules (MANDATORY)

### The RED-GREEN-REFACTOR Cycle

```
┌─────────────────────────────────────────────┐
│           TDD Cycle (Per Step)              │
├─────────────────────────────────────────────┤
│  1. RED    → Write failing test first       │
│  2. GREEN  → Write minimal code to pass     │
│  3. REFACTOR → Clean up without breaking    │
│  4. VERIFY → Confirm all tests still pass   │
└─────────────────────────────────────────────┘
```

### Rules

| Rule | Description |
|------|-------------|
| 🔴 Tests first | ALWAYS write tests before implementation |
| 🔴 One step at a time | Complete each step fully before next |
| 🔴 Run tests after each change | Never assume tests pass |
| 🔴 Never skip failing tests | Fix or mark as TODO with reason |
| 🔴 Refactor only when green | Never refactor with failing tests |

### Per-Step Workflow

1. **Read step requirements** from task spec
2. **Write test(s)** for expected behavior
3. **Run tests** → should fail (RED)
4. **Implement** minimal code to pass
5. **Run tests** → should pass (GREEN)
6. **Refactor** if needed (clean up)
7. **Run tests** → confirm still green
8. **Commit** step changes

---

## Task Completion Checklist

Before marking a task as `completed`:

### Code Quality
- [ ] All step outputs delivered
- [ ] Code follows project conventions
- [ ] No debug code or console.log
- [ ] Type hints / types where applicable

### Testing
- [ ] All acceptance criteria have tests
- [ ] All tests passing
- [ ] Coverage meets target (70%+ default)
- [ ] Edge cases considered

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic has comments
- [ ] API changes documented

### MEMORY.md
- [ ] Task status updated to `completed`
- [ ] Files Modified table updated
- [ ] Tests Added table updated
- [ ] Decisions recorded if any
- [ ] Timestamp updated

### Git
- [ ] Changes committed
- [ ] Commit message follows format
- [ ] No untracked files left behind

---

## Commit Protocol

### Per-Task Commit

After completing a task:

```bash
git add .
git commit -m "feat({feature}): complete {task-id} - {title}"
```

### Commit Message Format

```
{type}({scope}): {description}

Types:
- feat: New feature/functionality
- fix: Bug fix
- test: Adding tests
- refactor: Code restructuring
- docs: Documentation only

Scope: feature-slug or component name
Description: What was done (imperative mood)
```

### Examples

```bash
# Feature task
git commit -m "feat(auth-oauth): complete task-001 - setup database models"

# Bug fix during task
git commit -m "fix(auth-oauth): resolve foreign key constraint in user model"

# Test additions
git commit -m "test(auth-oauth): add integration tests for oauth flow"
```

---

## Resumption Protocol

### After Interruption

1. **Read MEMORY.md** for current state
   ```bash
   cat .ralph/{feature-slug}/MEMORY.md
   ```

2. **Check git log** for committed work
   ```bash
   git log --oneline --grep="{feature-slug}" -5
   ```

3. **Identify last completed task** from Progress table

4. **Find next pending task** by execution order

5. **Check for in_progress task**
   - If found, check which step was last
   - Continue from that step

6. **Resume execution** from correct point

### Never Repeat Completed Work

- Skip tasks marked `completed`
- Trust MEMORY.md as source of truth
- If uncertain, check git history

---

## Error Handling

### If a Step Fails

```
┌─────────────────────────────────────────────┐
│           Step Failure Protocol             │
├─────────────────────────────────────────────┤
│  1. Document error in MEMORY.md Issues      │
│  2. Analyze error message                   │
│  3. Attempt fix (max 3 attempts)            │
│  4. If stuck > 15 min → pause + request help│
│  5. Never skip — all steps must pass        │
└─────────────────────────────────────────────┘
```

### If Tests Fail

| Scenario | Action |
|----------|--------|
| Test bug | Fix the test |
| Implementation bug | Fix the implementation |
| Flaky test | Investigate root cause |
| Environment issue | Document and retry |

**Never**:
- Disable or skip tests
- Comment out failing tests
- Reduce coverage requirements

### If Acceptance Criteria Not Met

1. Review implementation against AC
2. Identify missing functionality
3. Implement missing parts
4. Add tests for AC validation
5. Verify AC passes
6. Then mark task complete

---

## Status Check Commands

### Memory State

```bash
# Full memory
cat .ralph/{feature-slug}/MEMORY.md

# Current task only
grep "Current Task" .ralph/{feature-slug}/MEMORY.md
```

### Git Status

```bash
# Feature commits
git log --oneline --grep="{feature-slug}"

# Uncommitted changes
git status

# Diff from last commit
git diff
```

### Test Status

| Stack | Command |
|-------|---------|
| Django | `pytest -v` |
| React | `npm test` or `pnpm test` |
| Spring | `./mvnw test` or `./gradlew test` |
| Symfony | `./vendor/bin/phpunit` |
| Generic | Check project's test script |

---

## Completion Checklist (Final)

Before marking feature as complete:

- [ ] All tasks marked `completed` in MEMORY.md
- [ ] All acceptance criteria validated
- [ ] All tests passing
- [ ] All changes committed
- [ ] No pending TODOs in code
- [ ] MEMORY.md fully updated
- [ ] Final summary displayed

---

## Quick Reference

| Phase | Action | Verify |
|-------|--------|--------|
| Start Step | Write test | Test fails |
| Implement | Write code | Test passes |
| Refactor | Clean up | Test still passes |
| Complete Step | Update docs | All green |
| Complete Task | Commit | MEMORY.md updated |
| Complete Feature | Final check | All complete |
