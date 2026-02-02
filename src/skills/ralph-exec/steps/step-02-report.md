---
name: step-02-report
description: Update PRD.json and emit RALPH_STATUS block
prev_step: steps/step-01-execute.md
next_step: null
---

# Step 02: Report

## Reference Files

@../references/status-block.md

| Reference | Purpose |
|-----------|---------|
| status-block.md | RALPH_STATUS format specification |

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip PRD update
- 🔴 NEVER skip RALPH_STATUS emission
- 🔴 NEVER emit malformed RALPH_STATUS
- ✅ ALWAYS update PRD.json before emitting status
- ✅ ALWAYS include all 7 required fields in status
- ✅ ALWAYS use exact delimiter format
- ✅ ALWAYS increment attempts counter
- ⛔ FORBIDDEN emitting status without <<<RALPH_STATUS>>> delimiters
- 🔵 YOU ARE A PRECISE STATUS REPORTER

## EXECUTION PROTOCOLS:

### 1. Prepare Story Update

Based on execution results from step-01:

```python
now = datetime.utcnow().isoformat() + "Z"

story_update = {
    "status": session.story_status,  # "completed" or "failed"
    "passes": session.story_passes,  # true or false
    "execution": {
        "attempts": story["execution"]["attempts"] + 1,
        "last_error": session.execution.last_error,  # or null
        "files_modified": session.execution.files_modified,
        "completed_at": now if session.story_passes else None,
        "iteration": story["execution"]["iteration"] + 1
    }
}
```

### 2. Update PRD.json

Apply updates to PRD file:

```python
# Find and update story in PRD
for i, s in enumerate(prd["userStories"]):
    if s["id"] == session.selected_story["id"]:
        # Update story fields
        prd["userStories"][i]["status"] = story_update["status"]
        prd["userStories"][i]["passes"] = story_update["passes"]
        prd["userStories"][i]["execution"] = story_update["execution"]

        # Update AC done flags
        for j, ac in enumerate(session.selected_story["acceptanceCriteria"]):
            prd["userStories"][i]["acceptanceCriteria"][j]["done"] = ac["done"]

        # Update task done flags
        for j, task in enumerate(session.selected_story["tasks"]):
            prd["userStories"][i]["tasks"][j]["done"] = task["done"]

        break

# Update metrics
completed_count = sum(1 for s in prd["userStories"] if s["passes"])
prd["metrics"]["completed"] = completed_count

# Write updated PRD
write_json(session.prd_path, prd)
```

### 3. Determine Next Story

Find what story would be next (for status block):

```python
def find_next_story(prd, current_story_id):
    """Find next eligible story after current one."""
    stories_by_id = {s["id"]: s for s in prd["userStories"]}

    for story in prd["userStories"]:
        if story["id"] == current_story_id:
            continue  # Skip current
        if story["status"] != "pending" or story["passes"]:
            continue

        # Check dependencies
        deps_satisfied = all(
            stories_by_id.get(dep, {}).get("passes", False)
            for dep in story["dependencies"]["depends_on"]
        )

        if deps_satisfied:
            return story["id"]

    return None  # No more stories

next_story_id = find_next_story(prd, session.selected_story["id"])
```

### 4. Determine Status Code

```python
if session.status == "ALL_DONE":
    status_code = "ALL_DONE"
elif session.status == "BLOCKED":
    status_code = "BLOCKED"
elif session.story_passes:
    status_code = "SUCCESS"
else:
    status_code = "FAILURE"
```

### 5. Emit RALPH_STATUS Block

**CRITICAL: Use exact format for shell parsing**

Output the following block (MUST be at END of response):

```
<<<RALPH_STATUS>>>
story_id: {story_id or null}
status: {SUCCESS|FAILURE|BLOCKED|ALL_DONE}
passes: {true|false}
error: {null|"error message"}
files_modified: [{comma-separated list}]
next_story: {next_story_id|null}
timestamp: {ISO-8601}
<<<END_RALPH_STATUS>>>
```

### Status Block Examples

**SUCCESS:**

```
<<<RALPH_STATUS>>>
story_id: US1
status: SUCCESS
passes: true
error: null
files_modified: [tests/test_auth.py, src/auth/login.py]
next_story: US2
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

**FAILURE:**

```
<<<RALPH_STATUS>>>
story_id: US1
status: FAILURE
passes: false
error: "AC2 not satisfied: test_redirect_after_login failed"
files_modified: [tests/test_auth.py]
next_story: null
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

**ALL_DONE:**

```
<<<RALPH_STATUS>>>
story_id: null
status: ALL_DONE
passes: true
error: null
files_modified: []
next_story: null
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

**BLOCKED:**

```
<<<RALPH_STATUS>>>
story_id: null
status: BLOCKED
passes: false
error: "Stories US3, US4 blocked by unfinished dependencies"
files_modified: []
next_story: null
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

## CONTEXT BOUNDARIES:

- This step expects: Execution results from step-01, session context
- This step produces: Updated PRD.json, RALPH_STATUS block

## OUTPUT FORMAT:

```
## Report Complete

### PRD Updated
- Story: {story.id}
- Status: {completed|failed}
- Passes: {true|false}
- Attempts: {n}
- Files Modified: {count}

### Metrics
- Total Stories: {n}
- Completed: {n}
- Remaining: {n}

<<<RALPH_STATUS>>>
story_id: {id}
status: {status}
passes: {passes}
error: {error}
files_modified: [{files}]
next_story: {next}
timestamp: {timestamp}
<<<END_RALPH_STATUS>>>
```

## NEXT STEP TRIGGER:

Workflow complete. No next step.

The shell script (ralph.sh) will parse the RALPH_STATUS block to determine next action.
