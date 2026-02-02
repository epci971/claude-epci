---
name: step-01-execute
description: TDD Red-Green implementation of selected story
prev_step: steps/step-00-init.md
next_step: steps/step-02-report.md
---

# Step 01: Execute

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER write implementation before test (TDD)
- 🔴 NEVER skip the RED phase
- 🔴 NEVER proceed with failing tests
- 🔴 NEVER over-engineer beyond story requirements
- ✅ ALWAYS follow TDD cycle: RED → GREEN
- ✅ ALWAYS track files_modified
- ✅ ALWAYS run tests after each change
- ✅ ALWAYS implement minimal code to pass
- ⛔ FORBIDDEN skipping tests for any AC
- 🔵 YOU ARE A FAST TDD EXECUTOR (skip REFACTOR for speed)
- 💭 FOCUS on one AC at a time, complete before next

## EXECUTION PROTOCOLS:

### 1. Load Story Context

From session context, extract:

```python
story = session.selected_story
acs = story["acceptanceCriteria"]
tasks = story["tasks"]

# Log story summary
print(f"Executing: {story['id']} - {story['title']}")
print(f"ACs to satisfy: {len(acs)}")
print(f"Tasks to complete: {len(tasks)}")
```

### 2. Detect Stack (Optional)

Check project for stack signatures:

```python
STACK_DETECTION = {
    "python-django": ["manage.py", "django" in requirements],
    "javascript-react": ["react" in package.json, "*.tsx"],
    "java-springboot": ["spring-boot" in pom.xml or build.gradle],
    "php-symfony": ["symfony" in composer.json]
}
```

If stack detected, load stack skill for patterns:
- `Read("src/skills/stack/{stack}/SKILL.md")`

### 3. TDD Red-Green Cycle (Per AC)

For each acceptance criterion:

#### 3.1 RED Phase: Write Failing Test

```
LANCE Task({
  subagent_type: "implementer",
  model: "sonnet",
  prompt: `
## Objective
Write a FAILING test for this acceptance criterion.

## Story Context
ID: ${story.id}
Title: ${story.title}

## Acceptance Criterion
${ac.id}: ${ac.description}

## Requirements
1. Write test that verifies the AC
2. Use project's test framework
3. Test MUST fail initially (no implementation yet)
4. Follow existing test patterns in codebase

## Output
- Test file path
- Test function name
- Expected failure reason
  `
})
```

**Verify RED:**

```bash
# Run test - MUST fail
{test_command} {test_file}

# Expected: Test fails with assertion error
```

If test passes (false positive):
- Fix test to properly verify AC
- Re-run until properly failing

#### 3.2 GREEN Phase: Implement to Pass

```
LANCE Task({
  subagent_type: "implementer",
  model: "sonnet",
  prompt: `
## Objective
Write MINIMAL implementation to make the test pass.

## Story Context
ID: ${story.id}
AC: ${ac.id}

## Test to Pass
File: ${test_file}
Failure: ${failure_reason}

## Requirements
1. Write minimal code to pass the test
2. Do NOT over-engineer
3. Follow existing code patterns
4. Keep changes focused on this AC only

## Output
- Implementation file path
- Changes made
- Any new dependencies
  `
})
```

**Verify GREEN:**

```bash
# Run test - MUST pass
{test_command} {test_file}

# Expected: Test passes
```

If test still fails after 2 attempts:
- Mark AC as failed
- Record error in session
- Continue to next AC (best effort)

#### 3.3 Track Files Modified

After each AC:

```python
session.execution.files_modified.extend([
    test_file_path,
    implementation_file_path
])

# Deduplicate
session.execution.files_modified = list(set(
    session.execution.files_modified
))
```

### 4. Update AC Status

After successful implementation:

```python
ac["done"] = True
```

After failure:

```python
ac["done"] = False
session.execution.last_error = error_message
```

### 5. Complete Tasks

For each task in story:

```python
for task in story["tasks"]:
    if task_completed_by_ac_implementation(task):
        task["done"] = True
```

### 6. Determine Story Outcome

```python
all_acs_done = all(ac["done"] for ac in story["acceptanceCriteria"])

if all_acs_done:
    session.story_passes = True
    session.story_status = "completed"
else:
    session.story_passes = False
    session.story_status = "failed"
    session.story_error = "Not all ACs satisfied"
```

## CONTEXT BOUNDARIES:

- This step expects: Selected story from step-00, session context
- This step produces: Implemented code, test results, files_modified list

## TDD CYCLE SUMMARY:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TDD RED-GREEN (Per AC)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AC: {ac.description}                                           │
│                                                                  │
│  [RED]   Write failing test                                     │
│     ↓    Verify: Test FAILS                                     │
│  [GREEN] Write minimal implementation                           │
│     ↓    Verify: Test PASSES                                    │
│  [DONE]  Mark AC as done, track files                           │
│                                                                  │
│  (REFACTOR skipped for Ralph speed)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## OUTPUT FORMAT:

```
## Execution Progress

### Story: {story.id}

#### ACs Completed
- [x] AC1: {description} - PASS
- [x] AC2: {description} - PASS
- [ ] AC3: {description} - FAIL (reason)

#### Files Modified
- tests/test_feature.py
- src/feature.py

#### Test Results
- Passed: {n}
- Failed: {n}

→ Proceeding to report...
```

## ERROR HANDLING:

| Error | Cause | Action |
|-------|-------|--------|
| Test won't fail (RED) | Test incorrectly written | Fix test, retry |
| Test won't pass (GREEN) | Implementation issue | Retry 2x, then mark FAIL |
| Syntax error | Code issue | Fix and retry |
| Dependency missing | Missing import | Add dependency |

## NEXT STEP TRIGGER:

When all ACs have been attempted (pass or fail), proceed to `step-02-report.md`.
