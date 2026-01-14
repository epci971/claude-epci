---
description: >-
  Execute a single story from prd.json using EPCT workflow inline.
  No routing to /brief or /epci. Fresh context per story.
  Used by ralph.sh for overnight autonomous execution.
argument-hint: "--prd <prd.json> [--story US-XXX] [--max-attempts N]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Ralph-Exec — Single Story Executor

## Overview

Execute ONE user story from prd.json autonomously using EPCT workflow (Explore, Plan, Code-Test, Commit).

**Key Design Principles:**
- **No routing** to /brief or /epci — workflow is inline
- **Context isolation** — Each invocation is independent
- **Single story** — Execute exactly one story per call
- **Promise tag** — Output `<promise>STORY_DONE</promise>` on success

## Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `--prd <file>` | Yes | Path to prd.json | - |
| `--story <id>` | No | Force specific story ID | Auto-select |
| `--max-attempts` | No | Max Code-Test loop attempts | 5 |

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (default) / `think hard` (on retry) |
| **Skills** | project-memory, testing-strategy, git-workflow, code-conventions |
| **Subagents** | @planner (M/L), @implementer (M/L), @Explore (quick), @plan-validator (L/XL), @code-reviewer (L/XL), @qa-reviewer (L/XL, conditional) |

---

## EPCT Workflow

```
/ralph-exec --prd prd.json
    │
    ▼
[STEP 0] LOAD & SELECT ────────────────────────────────────────────────
    │ Parse prd.json
    │ Find story: min(priority) + status=pending + passes=false
    │ Check dependencies
    ▼
[E] EXPLORE ───────────────────────────────────────────────────────────
    │ Read parent_spec, parent_brief
    │ Quick context scan
    ▼
[P] PLAN ──────────────────────────────────────────────────────────────
    │ Generate task list (inline or @planner for M/L)
    │ @plan-validator validates plan (L/XL only)
    ▼
[C] CODE-TEST LOOP ────────────────────────────────────────────────────
    │ FOR attempt = 1 to max_attempts:
    │   Implement → Test → Fix if needed
    │   IF tests pass: BREAK
    ▼
[R] REVIEW (L/XL only) ────────────────────────────────────────────────
    │ @code-reviewer checks quality
    │ @qa-reviewer if >5 test files
    │ IF NEEDS_REVISION → retry [C] (max 2 cycles)
    ▼
[T] COMMIT & UPDATE ───────────────────────────────────────────────────
    │ Git commit
    │ Update prd.json
    │ Append progress.txt
    ▼
OUTPUT ────────────────────────────────────────────────────────────────
    <promise>STORY_DONE</promise> or FAILED
```

---

## Step 0: Load & Select Story

### Step 0.1: Parse prd.json

Read and validate prd.json structure:

```json
{
  "schemaVersion": "2.0",
  "branchName": "feature/xxx",
  "context": {
    "parent_spec": "S01-xxx.md",
    "parent_brief": "brief-xxx.md"
  },
  "userStories": [...]
}
```

**Validation checks:**
- File exists and is valid JSON
- `userStories` array is present and non-empty
- Required fields: id, title, priority, status, passes

### Step 0.2: Select Next Story

**Selection algorithm:**
```
CANDIDATES = stories WHERE (passes == false AND status != "blocked")
SORTED = CANDIDATES ORDER BY priority ASC
SELECTED = SORTED[0]

IF SELECTED is null:
   → All stories complete
   → Output: <promise>ALL_DONE</promise>
   → EXIT
```

**If `--story` flag provided:**
```
SELECTED = stories WHERE id == --story
IF SELECTED.passes == true:
   → Story already complete, skip
```

### Step 0.3: Check Dependencies

```
IF story.dependencies.depends_on is not empty:
   FOR EACH dep_id IN depends_on:
      dep_story = stories WHERE id == dep_id
      IF dep_story.passes != true:
         → Mark story as blocked
         → story.status = "blocked"
         → story.execution.last_error = "Blocked by {dep_id}"
         → Continue to next candidate story
```

### Step 0.4: Update Status

```
story.status = "in_progress"
story.execution.attempts += 1
SAVE prd.json
```

---

## [E] Explore Phase (1-2 min)

### Step E.1: Load Context Files

Read context from prd.json:

```
parent_spec = context.parent_spec
parent_brief = context.parent_brief
progress_txt = ./progress.txt (if exists)
```

**Files to read:**
1. **Parent spec** (S0X.md) — Technical details, architecture
2. **Parent brief** — Original feature description
3. **progress.txt** — Previous iterations, learnings, errors

### Step E.2: Quick Codebase Scan

**For TINY/SMALL stories (complexity S/M):**
- Scan target files mentioned in story.tasks
- Check file existence and basic structure

**For STANDARD/LARGE stories (complexity L/XL):**
- Invoke @Explore (Haiku) via Task tool:
  ```
  Task tool with subagent_type="Explore", model="haiku"
  Focus: File identification, pattern detection
  Scope: Limited to story context
  ```

### Step E.3: Determine Complexity

| Complexity | Criteria | Subagents Used |
|------------|----------|----------------|
| S (TINY) | 1 file, <50 LOC | None |
| M (SMALL) | 2-3 files, <200 LOC | @implementer |
| L (STANDARD) | 4-10 files, <1000 LOC | @planner, @plan-validator, @implementer, @code-reviewer, @qa-reviewer* |
| XL (LARGE) | 10+ files | @planner, @plan-validator, @implementer, @code-reviewer, @qa-reviewer* |

*@qa-reviewer is invoked only if >5 test files are created/modified.

---

## [P] Plan Phase (1-2 min)

### Step P.1: Generate Task List

**For S/M complexity (inline planning):**
```
Extract tasks from story.tasks array
IF story.tasks is empty:
   Generate 2-5 atomic tasks from acceptanceCriteria
```

**For L/XL complexity (use @planner):**
```
Task tool with subagent_type="epci:planner", model="sonnet"
Input: Story brief + context files
Output: Ordered task list with time estimates
```

### Step P.2: Task Structure

Each task should be:
- Atomic (2-10 minutes)
- Testable
- Independent when possible

```json
{
  "tasks": [
    {"id": "T1", "description": "Write tests for new method", "done": false},
    {"id": "T2", "description": "Implement method logic", "done": false},
    {"id": "T3", "description": "Add integration", "done": false}
  ]
}
```

### Step P.3: Plan Validation (L/XL only)

**For L/XL complexity, validate the plan with @plan-validator:**

```
Task tool with subagent_type="epci:plan-validator", model="opus"
Input: Generated task list + story context
Output: APPROVED or NEEDS_REVISION with CQNT alerts
```

**On NEEDS_REVISION:**
- If 🛑 Critical alert: Mark story as blocked, exit
- If ⚠️ Important alerts: Regenerate plan with fixes
- Max 2 plan revision cycles

**CQNT Alerts checked:**
- Backlog < 3 tasks
- Circular dependencies
- Task without target file
- Estimation > 30min per task
- No test planned

---

## [C] Code-Test Loop (Variable)

### Loop Structure

```
FOR attempt = 1 to max_attempts (default 5):

    [IMPLEMENT]
    Execute each task in order
    Apply TDD: Test first when applicable

    [TEST]
    Run project tests (detect command)
    Run linter if configured

    IF tests PASS:
        story.execution.code_test_attempts = attempt
        BREAK LOOP → Go to Commit phase

    ELIF attempt < max_attempts:
        [FIX]
        Analyze error
        Activate "think hard" mode
        Apply fix
        CONTINUE LOOP

    ELSE:
        story.status = "failed"
        story.execution.last_error = error_message
        SAVE prd.json
        OUTPUT: FAILED
        EXIT
```

### Step C.1: Implementation

**For S/M complexity (direct implementation):**
- Use Edit tool directly for changes
- Follow code conventions from .project-memory/

**For L/XL complexity (use @implementer):**
```
Task tool with subagent_type="epci:implementer", model="sonnet"
Input: Single task from plan
Output: Implemented code
```

### Step C.2: Testing

**Detect and run test command:**
```bash
# Auto-detect test runner
IF package.json exists AND scripts.test:
   npm test
ELIF pytest.ini OR conftest.py:
   pytest
ELIF composer.json AND scripts.test:
   composer test
ELIF pom.xml:
   mvn test
ELSE:
   # No tests configured, mark as PASS
```

**On test failure:**
- Parse error output
- Identify failing test/assertion
- Activate `think hard` mode for fix attempt

### Step C.3: Fix Attempt (if needed)

```
IF test_error:
   Analyze error message
   Identify root cause
   Apply targeted fix
   Re-run tests
```

**Fix strategy:**
1. Parse test error output
2. Identify exact failure point
3. Check for common issues (imports, types, logic)
4. Apply minimal fix
5. Re-run tests

---

## [R] Review Phase (L/XL only)

**This phase is ONLY executed for L/XL complexity stories.**

### Step R.1: Code Review

**Invoke @code-reviewer for quality validation:**

```
Task tool with subagent_type="epci:code-reviewer", model="opus"
Input: Modified files list + story context
Output: APPROVED | APPROVED_WITH_FIXES | NEEDS_REVISION
```

**Review checks:**
- Code quality (SRP, error handling, type safety)
- Architecture (project patterns, coupling)
- Tests (coverage, assertions, no anti-patterns)
- Plan alignment (all tasks implemented, no scope creep)

### Step R.2: QA Review (Conditional)

**Invoke @qa-reviewer if >5 test files created/modified:**

```
Task tool with subagent_type="epci:qa-reviewer", model="sonnet"
Input: Test files list + coverage info
Output: APPROVED | NEEDS_IMPROVEMENT
```

**QA checks:**
- Test pyramid balance
- Coverage gaps (edge cases, error cases)
- Anti-patterns (mock testing, coupled tests)

### Step R.3: Handle Review Results

```
IF code_review == APPROVED:
   → Continue to [T] Commit

ELIF code_review == APPROVED_WITH_FIXES:
   → Log fixes needed but non-blocking
   → Continue to [T] Commit

ELIF code_review == NEEDS_REVISION:
   IF review_cycles < 2:
      review_cycles += 1
      → Apply fixes based on review feedback
      → Return to [C] Code-Test Loop
   ELSE:
      → Mark story as "review_failed"
      → Log review issues
      → Continue to [T] Commit with warning
```

**Max 2 review cycles to prevent infinite loops.**

---

## [T] Commit & Update Phase

### Step T.1: Git Commit

**Create atomic commit for the story:**

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat({story.category}): {story.title}

Story: {story.id}
Acceptance Criteria: {count} passed
EOF
)"
```

**Record commit hash:**
```
story.execution.commit_hash = $(git rev-parse HEAD)
```

### Step T.2: Update prd.json

**On SUCCESS, update all v2 fields:**

```json
{
  "id": "{story.id}",
  "status": "completed",
  "passes": true,

  "acceptanceCriteria": [
    {"id": "AC1", "description": "...", "done": true},
    {"id": "AC2", "description": "...", "done": true}
  ],

  "tasks": [
    {"id": "T1", "description": "...", "done": true},
    {"id": "T2", "description": "...", "done": true}
  ],

  "execution": {
    "attempts": {N},
    "code_test_attempts": {N},
    "last_error": null,
    "files_modified": ["file1.ext", "file2.ext"],
    "completed_at": "{ISO_TIMESTAMP}",
    "commit_hash": "{HASH}"
  },

  "testing": {
    "test_files": ["test_file.ext"],
    "requires_e2e": false
  }
}
```

**On FAILURE:**
```json
{
  "status": "failed",
  "passes": false,
  "execution": {
    "attempts": {N},
    "last_error": "{error_message}",
    "files_modified": []
  }
}
```

### Step T.3: Update progress.txt

**Append iteration log:**

```markdown
=== Iteration {N} === [{TIMESTAMP}]
Story: {story.id} — {story.title}
Status: {COMPLETED|FAILED|BLOCKED}
Duration: {X}m {Y}s
Files: {file1}, {file2}, ...
Tests: {PASS|FAIL} ({count} tests)
Commit: {hash}
{Error: {message} if any}

Learnings:
- {Pattern or insight discovered}

---
```

---

## Output

### On Success

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ STORY COMPLETE — {story.id}                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Title: {story.title}                                                │
│ Files: {file_count} modified                                        │
│ Tests: {test_count} passing                                         │
│ Commit: {commit_hash}                                               │
│ Duration: {duration}                                                │
│                                                                     │
│ Attempts: {code_test_attempts}/{max_attempts}                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

<promise>STORY_DONE</promise>
```

### On Failure

```
┌─────────────────────────────────────────────────────────────────────┐
│ ❌ STORY FAILED — {story.id}                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Title: {story.title}                                                │
│ Attempts: {max_attempts}/{max_attempts}                             │
│                                                                     │
│ Error:                                                              │
│ {last_error}                                                        │
│                                                                     │
│ Recommendation: Review manually or split story                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

FAILED
```

### On All Complete

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🎉 ALL STORIES COMPLETE                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Total stories: {total}                                              │
│ Completed: {completed}                                              │
│ Failed: {failed}                                                    │
│                                                                     │
│ Next: Create PR or continue with dependent specs                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

<promise>ALL_DONE</promise>
```

### On Blocked

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️ STORY BLOCKED — {story.id}                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Blocked by: {dependency_ids}                                        │
│ Reason: Dependencies not yet completed                             │
│                                                                     │
│ Trying next available story...                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

BLOCKED
```

---

## Error Handling

| Error | Action |
|-------|--------|
| prd.json not found | Exit with error message |
| Invalid JSON | Exit with parse error |
| Story not found (--story) | Exit with error |
| All stories blocked | Exit with BLOCKED status |
| Test failure after max attempts | Mark FAILED, continue available |
| Git conflict | Mark BLOCKED, require manual resolution |
| Context exceeded | Log warning, attempt completion |

---

## Constraints

- Execute **ONE** story only per invocation
- Do not modify other stories in prd.json
- Always return a result (never hang)
- Max execution time: 30 minutes
- Always output promise tag at end

---

## Examples

### Example 1: Simple Story

```bash
claude --dangerously-skip-permissions "/ralph-exec --prd ./prd.json"

# Output:
[LOAD] Found 5 stories, 3 pending
[SELECT] US-003 — Add validation to email field (priority: 1)
[E] Reading parent_spec S01-core.md...
[P] 2 tasks generated (complexity: S)
[C] Implementing task 1/2...
[C] Implementing task 2/2...
[T] Running tests... PASS (12 tests)
[T] Committing: feat(validation): Add email validation

✅ STORY COMPLETE — US-003
<promise>STORY_DONE</promise>
```

### Example 2: Story with Retries

```bash
claude --dangerously-skip-permissions "/ralph-exec --prd ./prd.json --max-attempts 3"

# Output:
[LOAD] Found 5 stories, 2 pending
[SELECT] US-004 — Add date formatting utility
[E] Reading context...
[P] 3 tasks generated (complexity: M)
[C] Implementing...
[T] Running tests... FAIL (assertion error)
[C] Attempt 2/3: Fixing assertion...
[T] Running tests... PASS (15 tests)
[T] Committing...

✅ STORY COMPLETE — US-004
Attempts: 2/3
<promise>STORY_DONE</promise>
```

### Example 3: All Stories Done

```bash
claude --dangerously-skip-permissions "/ralph-exec --prd ./prd.json"

# Output:
[LOAD] Found 5 stories, 0 pending
All stories already complete!

🎉 ALL STORIES COMPLETE
<promise>ALL_DONE</promise>
```

---

## Integration with ralph.sh

This command is designed to be called by `ralph.sh` in a loop:

```bash
#!/bin/bash
# ralph.sh — generated by /decompose

MAX_ITERATIONS=${MAX_ITERATIONS:-50}
PRD_FILE="./prd.json"

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    echo "=== Iteration $i ==="

    # Check if any stories remain
    PENDING=$(jq '[.userStories[] | select(.passes==false and .status!="blocked")] | length' "$PRD_FILE")
    if [ "$PENDING" -eq 0 ]; then
        echo "All stories complete!"
        exit 0
    fi

    # Execute next story (fresh context each time)
    OUTPUT=$(claude --dangerously-skip-permissions "/ralph-exec --prd $PRD_FILE" 2>&1) || true
    echo "$OUTPUT"

    # Check completion
    if echo "$OUTPUT" | grep -q '<promise>STORY_DONE</promise>'; then
        echo "Story completed successfully"
    elif echo "$OUTPUT" | grep -q '<promise>ALL_DONE</promise>'; then
        echo "All stories complete!"
        exit 0
    fi
done

echo "Max iterations reached"
exit 1
```

---

## See Also

- `/decompose` — Generates prd.json and ralph.sh
- `ralph-analyzer` skill — RALPH_STATUS parsing
- `ralph-converter` skill — Story conversion

---

*Ralph Wiggum Simplification v2 — 2025-01-14*
