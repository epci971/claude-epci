# RALPH_STATUS Block Format

Complete specification for the RALPH_STATUS block emitted by `/ralph-exec`.

## Purpose

The RALPH_STATUS block provides structured output that the `ralph.sh` shell script can parse to determine:
1. Whether to continue the loop
2. What story to execute next
3. Whether to trigger circuit breaker

## Format Specification

### Delimiters

```
<<<RALPH_STATUS>>>
{content}
<<<END_RALPH_STATUS>>>
```

- Opening delimiter: `<<<RALPH_STATUS>>>`
- Closing delimiter: `<<<END_RALPH_STATUS>>>`
- Content: 7 required fields, one per line

### Required Fields (7)

| Field | Type | Description |
|-------|------|-------------|
| `story_id` | string\|null | Story ID that was executed (e.g., "US1") |
| `status` | enum | Execution result code |
| `passes` | boolean | Whether story tests pass |
| `error` | string\|null | Error message if failed |
| `files_modified` | array | List of modified file paths |
| `next_story` | string\|null | Next eligible story ID |
| `timestamp` | string | ISO-8601 timestamp |

### Status Codes

| Code | Meaning | Shell Action |
|------|---------|--------------|
| `SUCCESS` | Story completed, tests pass | Continue to next story |
| `FAILURE` | Story failed, tests fail | Increment failure counter, maybe retry |
| `BLOCKED` | No story can proceed | Wait or abort |
| `ALL_DONE` | All stories completed | Exit loop successfully |

### Field Formats

**story_id:**
- String: `"US1"`, `"US2"`, etc.
- null: When no story was executed (ALL_DONE, BLOCKED)

**status:**
- One of: `SUCCESS`, `FAILURE`, `BLOCKED`, `ALL_DONE`
- Case-sensitive

**passes:**
- `true` or `false`
- Lowercase boolean

**error:**
- null: No error
- String: Error message in quotes

**files_modified:**
- Array syntax: `[file1, file2, file3]`
- Empty: `[]`
- No quotes around file names

**next_story:**
- String: Next story ID
- null: No next story available

**timestamp:**
- ISO-8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- UTC timezone (Z suffix)

## Examples

### Successful Story Execution

```
<<<RALPH_STATUS>>>
story_id: US1
status: SUCCESS
passes: true
error: null
files_modified: [tests/test_auth.py, src/auth/login.py, src/auth/session.py]
next_story: US2
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

### Failed Story Execution

```
<<<RALPH_STATUS>>>
story_id: US2
status: FAILURE
passes: false
error: "AC3 not satisfied: test_token_refresh failed after 2 attempts"
files_modified: [tests/test_token.py]
next_story: null
timestamp: 2026-02-02T21:15:00Z
<<<END_RALPH_STATUS>>>
```

### All Stories Complete

```
<<<RALPH_STATUS>>>
story_id: null
status: ALL_DONE
passes: true
error: null
files_modified: []
next_story: null
timestamp: 2026-02-02T22:00:00Z
<<<END_RALPH_STATUS>>>
```

### Blocked (Dependencies)

```
<<<RALPH_STATUS>>>
story_id: null
status: BLOCKED
passes: false
error: "Stories US3, US4 blocked by failed dependency US2"
files_modified: []
next_story: null
timestamp: 2026-02-02T21:20:00Z
<<<END_RALPH_STATUS>>>
```

### PRD Not Found

```
<<<RALPH_STATUS>>>
story_id: null
status: FAILURE
passes: false
error: "PRD file not found: .ralph/missing/prd.json"
files_modified: []
next_story: null
timestamp: 2026-02-02T20:00:00Z
<<<END_RALPH_STATUS>>>
```

## Shell Parsing

The `ralph.sh` script parses this block using:

```bash
# Extract status block from Claude output
extract_ralph_status() {
    local output="$1"

    # Extract content between delimiters
    echo "$output" | sed -n '/<<<RALPH_STATUS>>>/,/<<<END_RALPH_STATUS>>>/p' | \
        grep -v '<<<'
}

# Parse individual field
get_field() {
    local content="$1"
    local field="$2"

    echo "$content" | grep "^${field}:" | cut -d':' -f2- | xargs
}

# Usage
status_block=$(extract_ralph_status "$claude_output")
status=$(get_field "$status_block" "status")
next_story=$(get_field "$status_block" "next_story")

case "$status" in
    SUCCESS)
        if [ "$next_story" != "null" ]; then
            # Continue loop with next story
            continue_loop=true
        fi
        ;;
    FAILURE)
        ((failure_count++))
        if [ $failure_count -ge $MAX_FAILURES ]; then
            # Circuit breaker triggered
            exit 1
        fi
        ;;
    ALL_DONE)
        echo "All stories completed successfully"
        exit 0
        ;;
    BLOCKED)
        echo "Execution blocked"
        exit 2
        ;;
esac
```

## Validation Rules

1. **Delimiters MUST be exact** — No extra whitespace
2. **All 7 fields MUST be present** — Order matters
3. **Field names are case-sensitive** — `story_id` not `Story_ID`
4. **Status MUST be uppercase** — `SUCCESS` not `success`
5. **Boolean MUST be lowercase** — `true` not `True`
6. **Block MUST be at END of output** — For reliable parsing

## Anti-Patterns

**Wrong delimiter:**
```
# BAD
[[RALPH_STATUS]]
---RALPH_STATUS---

# GOOD
<<<RALPH_STATUS>>>
```

**Missing field:**
```
# BAD (missing next_story)
<<<RALPH_STATUS>>>
story_id: US1
status: SUCCESS
passes: true
error: null
files_modified: []
timestamp: 2026-02-02T20:30:00Z
<<<END_RALPH_STATUS>>>
```

**Wrong case:**
```
# BAD
status: success
passes: True

# GOOD
status: SUCCESS
passes: true
```
