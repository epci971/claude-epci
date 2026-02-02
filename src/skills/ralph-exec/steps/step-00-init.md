---
name: step-00-init
description: Parse PRD argument, validate PRD.json, select next story
prev_step: null
next_step: steps/step-01-execute.md
conditional_next:
  - condition: "no story available (all done or blocked)"
    step: steps/step-02-report.md
    note: "Skip to report with ALL_DONE or BLOCKED status"
---

# Step 00: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER proceed without valid --prd argument
- 🔴 NEVER select story with unsatisfied dependencies
- 🔴 NEVER select story with passes == true
- ✅ ALWAYS validate PRD against prd-v2 schema
- ✅ ALWAYS respect dependency order
- ✅ ALWAYS store selected story in session context
- 💭 FOCUS on finding the next eligible story efficiently

## EXECUTION PROTOCOLS:

### 1. Parse Arguments

Extract `--prd <path>` from user input:

```
INPUT FORMAT:
/ralph-exec --prd <path-to-prd.json>

Examples:
  /ralph-exec --prd .ralph/auth-feature/prd.json
  /ralph-exec --prd docs/specs/my-feature/prd.json
```

**Validation:**
- `--prd` argument is required
- Path must be absolute or relative to project root
- File must exist

**If missing or invalid:**

```
EMIT RALPH_STATUS:
  story_id: null
  status: FAILURE
  passes: false
  error: "PRD file not found: {path}"
  files_modified: []
  next_story: null
  timestamp: {ISO-8601}

→ ABORT workflow
```

### 2. Load PRD.json

Read and parse the PRD file:

```python
prd = read_json(prd_path)

# Validate structure
required_fields = ["title", "version", "userStories", "meta", "config", "metrics"]
for field in required_fields:
    assert field in prd, f"Missing required field: {field}"

# Validate version
assert prd["version"] == "2.0", "PRD must be v2.0 format"
```

**If validation fails:**

```
EMIT RALPH_STATUS:
  story_id: null
  status: FAILURE
  passes: false
  error: "PRD validation failed: {details}"
  files_modified: []
  next_story: null
  timestamp: {ISO-8601}

→ ABORT workflow
```

### 3. Select Next Story

Apply selection algorithm:

```python
def select_next_story(prd):
    """
    Select first eligible story:
    - status == "pending"
    - passes == false
    - All depends_on stories have passes == true
    """
    stories_by_id = {s["id"]: s for s in prd["userStories"]}

    for story in prd["userStories"]:
        # Skip if not pending or already passes
        if story["status"] != "pending" or story["passes"]:
            continue

        # Check dependencies
        deps_satisfied = True
        for dep_id in story["dependencies"]["depends_on"]:
            dep_story = stories_by_id.get(dep_id)
            if not dep_story or not dep_story["passes"]:
                deps_satisfied = False
                break

        if deps_satisfied:
            return story

    return None  # No eligible story
```

### 4. Handle No Story Available

**Case A: All stories completed**

```python
all_done = all(s["passes"] for s in prd["userStories"])
if all_done:
    # Jump to step-02-report with ALL_DONE status
    session.status = "ALL_DONE"
    → GOTO step-02-report.md
```

**Case B: Stories blocked**

```python
if not all_done and selected_story is None:
    # Some stories pending but blocked by dependencies
    session.status = "BLOCKED"
    session.blocked_stories = [s["id"] for s in prd["userStories"]
                               if s["status"] == "pending" and not s["passes"]]
    → GOTO step-02-report.md
```

### 5. Initialize Session Context

Store context for subsequent steps:

```json
{
  "prd_path": "{path}",
  "selected_story": {
    "id": "{US1}",
    "title": "{story title}",
    "acceptanceCriteria": [...],
    "tasks": [...]
  },
  "execution": {
    "start_time": "{ISO-8601}",
    "files_modified": [],
    "test_results": []
  }
}
```

## CONTEXT BOUNDARIES:

- This step expects: `--prd <path>` argument
- This step produces: Validated PRD, selected story, session context

## OUTPUT FORMAT:

```
## Initialization Complete

PRD: {prd.title}
Story Selected: {story.id} - {story.title}
Complexity: {story.complexity}
Acceptance Criteria: {count}
Tasks: {count}

Dependencies: {satisfied/blocked}

→ Proceeding to execution...
```

## NEXT STEP TRIGGER:

When story is selected successfully, proceed to `step-01-execute.md`.

If no story available (ALL_DONE or BLOCKED), proceed to `step-02-report.md`.
