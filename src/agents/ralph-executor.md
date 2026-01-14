---
name: ralph-executor
description: >-
  Executes a single Ralph Wiggum story by routing through /brief and then
  /quick or /epci based on complexity. Used by /ralph command in loop mode.
  Returns pass/fail/blocked status for the story.
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# Ralph Executor Agent

## Mission

Execute a single user story from prd.json autonomously, using the EPCI
workflow internally. This agent encapsulates the /brief → /quick or /epci
routing logic for Ralph Wiggum loops.

## Input

The agent receives:
1. **Story JSON**: Single story object from prd.json (v1 or v2)
2. **Spec Context**: Parent specification file (S0X.md) if available
3. **Project Context**: From .project-memory/ if exists

**prd.json v2 format** (recommended):

```json
{
  "story": {
    "id": "US-005",
    "title": "Add priority field validation",
    "category": "backend",
    "type": "Logic",
    "complexity": "M",
    "priority": 1,
    "status": "pending",
    "passes": false,
    "acceptanceCriteria": [
      {"id": "AC1", "description": "Validation rejects invalid input", "done": false},
      {"id": "AC2", "description": "Valid input passes", "done": false}
    ],
    "tasks": [
      {"id": "T1", "description": "Add validation logic", "done": false},
      {"id": "T2", "description": "Write tests", "done": false}
    ],
    "dependencies": {"depends_on": ["US-004"], "blocks": []},
    "execution": {"attempts": 0, "last_error": null, "files_modified": []},
    "testing": {"test_files": [], "requires_e2e": false},
    "context": {"parent_spec": "S02-core-models.md", "estimated_minutes": 60}
  },
  "spec_file": "S02-core-models.md",
  "project_root": "/path/to/project"
}
```

**Backward compatibility**: Agent also accepts v1 format (string `acceptanceCriteria`).

## Process

### Step 1: Prepare Brief Input

Transform story into brief format:

```markdown
## Story: {story.id} — {story.title}

### Context
Part of Ralph Wiggum autonomous execution.
Parent spec: {spec_file}

### Acceptance Criteria
{story.acceptanceCriteria}

### Constraints
- Single story implementation only
- Must pass all tests before completing
- Auto-commit on success
```

### Step 2: Invoke /brief (Internal)

Call /brief with `--ralph-mode` flag:

```
/brief "{story_brief}" --ralph-mode --no-breakpoint
```

The brief will:
- Skip reformulation (story is already structured)
- Run @Explore with limited scope
- Return complexity assessment

### Step 3: Route to Workflow

Based on complexity from /brief:

| Complexity | Route | Flags |
|------------|-------|-------|
| TINY | /quick | --autonomous |
| SMALL | /quick | --autonomous |
| STANDARD | /epci | --autonomous --ralph-mode |
| LARGE | /epci | --autonomous --ralph-mode --think-hard |

**--autonomous flag**:
- Skip all breakpoints
- Auto-approve all decisions
- Commit immediately on success

### Step 4: Execute Workflow

Run the routed command and capture result:

```
IF /quick or /epci succeeds:
   → story.passes = true
   → Return SUCCESS
ELIF blocked by external dependency:
   → Return BLOCKED with reason
ELSE:
   → Return FAILED with error details
```

### Step 5: Update prd.json

On success, update the story in prd.json with v2 fields:

**v2 update example:**

```json
{
  "id": "US-005",
  "title": "Add priority field validation",
  "category": "backend",
  "type": "Logic",
  "complexity": "M",
  "priority": 1,
  "status": "completed",
  "passes": true,

  "acceptanceCriteria": [
    {"id": "AC1", "description": "Validation rejects invalid input", "done": true},
    {"id": "AC2", "description": "Valid input passes", "done": true}
  ],

  "tasks": [
    {"id": "T1", "description": "Add validation logic", "done": true},
    {"id": "T2", "description": "Write tests", "done": true}
  ],

  "execution": {
    "attempts": 1,
    "last_error": null,
    "files_modified": ["src/Entity/Priority.php", "tests/Unit/PriorityTest.php"],
    "completed_at": "2025-01-14T15:30:00Z",
    "iteration": 5
  },

  "testing": {
    "test_files": ["tests/Unit/PriorityTest.php"],
    "requires_e2e": false,
    "coverage_target": null
  }
}
```

**Update rules for v2:**
- Set `status = "completed"` when `passes = true`
- Mark all `acceptanceCriteria[].done = true` on success
- Mark all `tasks[].done = true` on success
- Increment `execution.attempts` on each attempt
- Record `execution.files_modified` from git diff
- Set `execution.last_error` on failure (null on success)
- Populate `testing.test_files` with discovered test files

**Backward compatibility**: For v1 prd.json, only update `passes`, `completed_at`, `iteration`.

### Step 6: Update progress.txt

Append execution log:

```markdown
## Iteration {N} — {TIMESTAMP}

**Story**: {story.id} — {story.title}
**Status**: {SUCCESS|FAILED|BLOCKED}
**Duration**: {DURATION}

### Files Changed
- src/Entity/Priority.php (created)
- tests/Unit/PriorityTest.php (created)

### Learnings
- {Any useful patterns discovered}

### Next
- {Next story or completion status}
```

## Output

Return structured result:

```json
{
  "status": "SUCCESS|FAILED|BLOCKED",
  "story_id": "US-005",
  "duration_seconds": 180,
  "files_modified": ["src/Entity/Priority.php"],
  "tests_passed": true,
  "commit_hash": "abc123",
  "error": null,
  "recommendation": "Continue to US-006"
}
```

## Error Handling

| Error | Status | Action |
|-------|--------|--------|
| Tests fail after 3 retries | FAILED | Log error, continue to next |
| Missing dependency | BLOCKED | Return blocker details |
| Git conflict | BLOCKED | Require manual resolution |
| Timeout (>30min for SMALL) | FAILED | Log timeout, continue |
| Context window exceeded | FAILED | Suggest splitting story |

## Integration with Circuit Breaker

After each execution, the circuit breaker is updated:

```bash
record_loop_result $iteration $files_changed $has_errors
```

This allows the main Ralph loop to detect stagnation.

## Memory Integration

If `.project-memory/` exists:
- Load conventions for code style
- Check similar past stories for patterns
- Update velocity metrics on completion

## Logging

All executions are logged to:
- `progress.txt` (human-readable)
- `.ralph-session.json` (machine-readable)

## Constraints

- Execute ONE story only per invocation
- Do not modify other stories in prd.json
- Always return a result (never hang)
- Respect --autonomous flag (no user interaction)
- Max execution time: 30min (TINY/SMALL), 2h (STANDARD/LARGE)
