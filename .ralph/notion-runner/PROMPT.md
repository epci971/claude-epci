# Ralph Execution Context — OpenClaw Notion Task Runner

## Feature

| Property | Value |
|----------|-------|
| **Slug** | notion-runner |
| **Complexity** | STANDARD |
| **Tasks** | 7 |
| **Estimated** | 11.25h |

---

## Stack

| Property | Value |
|----------|-------|
| **Framework** | Generic (Python stdlib only) |
| **Language** | Python |
| **Test Framework** | pytest |

---

## Execution Rules

### MANDATORY

- Follow TDD cycle: RED -> GREEN -> REFACTOR
- Complete each task fully before moving to next
- Run tests after each step completion
- Update MEMORY.md after each task completion
- Commit changes with conventional commit format
- Never skip acceptance criteria validation

### WORKFLOW

1. Read current task from `docs/specs/notion-runner/task-XXX.md`
2. Execute steps sequentially (15-30 min each)
3. Write tests BEFORE implementation (TDD)
4. Validate ALL acceptance criteria
5. Mark task complete in MEMORY.md
6. Commit: `feat(openclaw): complete task-XXX - {title}`
7. Proceed to next task by dependency order

---

## Specifications

### Location

```
docs/specs/notion-runner/
```

### Files

| File | Description |
|------|-------------|
| `index.md` | Overview, DAG, metrics |
| `task-001-notion-api-client.md` | Create Notion API client: query + update |
| `task-002-notion-blocks.md` | Implement Notion blocks + page creation |
| `task-003-task-selector.md` | Implement task selector |
| `task-004-execution-runner.md` | Implement execution runner |
| `task-005-main-loop.md` | Implement main orchestration loop |
| `task-006-prd-injector.md` | Implement PRD-to-Notion injector |
| `task-007-integration-tests.md` | Integration tests and validation |
| `notion-runner.prd.json` | Machine-readable PRD |

---

## Execution Order

Execute tasks in this order (respects dependencies):

1. **task-001**: Create Notion API client with query and update operations
2. **task-004**: Implement execution runner (implement-auto subprocess wrapper)
3. **task-002**: Implement Notion page blocks reading and page creation
   -> After: task-001
4. **task-003**: Implement task selector with priority and dependency resolution
   -> After: task-001
5. **task-005**: Implement main orchestration loop
   -> After: task-001, task-003, task-004
6. **task-006**: Implement PRD-to-Notion injector
   -> After: task-002
7. **task-007**: Integration tests and validation
   -> After: task-005, task-006

### Parallel Opportunities

**Group 1**: task-001 and task-004 can run in parallel (Wave 1)
**Group 2**: task-002 and task-003 can run in parallel (Wave 2)
**Group 3**: task-005 and task-006 can run in parallel (Wave 3)

---

## Stack-Specific Guidelines

### Python Conventions

- Python 3 stdlib only — NO pip dependencies (urllib, json, subprocess, os, pathlib, logging, argparse)
- 4-space indentation
- Double quotes for strings
- Type hints where helpful (stdlib `typing` module)
- Docstrings for public functions
- Use `unittest.mock` for test mocking (stdlib)

### Key Design Decisions

- **D1**: Python stdlib only (urllib, json, subprocess) — zero external dependencies
- **D2**: Notion API via urllib with `NOTION_API_KEY` environment variable
- **D3**: implement-auto as execution engine via subprocess
- **D5**: All code in `src/openclaw/` package
- **D6**: Spec Path (Git file) prioritized over Notion page body
- **D7**: Circuit breaker — 3 consecutive failures = stop
- **D11**: Worktrees delegated to implement-auto, Python does orphan cleanup only

### Important References

- `src/schemas/notion-bdd-openClawTasks.json` — Notion database schema (24 properties)
- `src/skills/implement-auto/SKILL.md` — Execution engine documentation
- Notion API version: `2022-06-28`
- Rate limit: 3 req/s (sleep 0.35s between batch calls)

### Commit Format

```
feat(openclaw): {description}
fix(openclaw): {description}
test(openclaw): {description}
```

---

## Context Persistence

After completing EACH TASK (not step):

### 1. Update MEMORY.md

```markdown
## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | completed | {ISO-8601} | {brief note} |
| task-002 | in_progress | - | Starting step 1 |
```

### 2. Record Files Modified

```markdown
## Files Modified

| File | Action | Task |
|------|--------|------|
| src/openclaw/notion_client.py | created | task-001 |
| src/openclaw/tests/test_notion_client.py | created | task-001 |
```

### 3. Record Tests Added

```markdown
## Tests Added

| Test | Coverage | Task |
|------|----------|------|
| test_query_database | 90% | task-001 |
```

### 4. Record Decisions (if any)

```markdown
## Decisions Made

| Decision | Rationale | Task |
|----------|-----------|------|
| Used dataclass for config | Cleaner than dict, stdlib | task-001 |
```

---

## Resumption Protocol

If execution is interrupted:

1. **Read MEMORY.md** for current state
2. **Check git log** for committed work
3. **Identify last completed task** from Progress table
4. **Find next pending task** by dependency order
5. **Continue from there** (don't repeat completed work)

### Status Check Commands

```bash
# View current memory state
cat .ralph/notion-runner/MEMORY.md

# Check git commits for this feature
git log --oneline --grep="openclaw"

# Verify test status
python -m pytest src/openclaw/tests/
```

---

## Error Handling

### If a Step Fails

1. Document error in MEMORY.md Issues section
2. Attempt fix based on error message
3. If stuck > 15 min, pause and request help
4. Never skip — all steps must pass

### If Tests Fail

1. Fix failing tests before proceeding
2. Never disable or skip tests
3. Document any test adjustments

### If Acceptance Criteria Not Met

1. Review implementation against AC
2. Identify missing functionality
3. Implement until AC passes
4. Add tests for AC validation

---

## Completion Checklist

Before marking feature complete:

- [ ] All tasks marked `completed` in MEMORY.md
- [ ] All acceptance criteria validated
- [ ] All tests passing (`python -m pytest src/openclaw/tests/`)
- [ ] All changes committed
- [ ] No pending TODOs in code
- [ ] MEMORY.md fully updated

---

*Ralph Execution Context generated by /spec v1.0 — EPCI v6.3.0*
*Feature: notion-runner | 2026-02-13*
