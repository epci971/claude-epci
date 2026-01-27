---
name: step-06-quick
description: Route B - TDD cycle for single-cause bugs
prev_step: steps/step-04-routing.md
next_step: steps/step-08-post.md
---

# Step 06: Quick Route

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip regression test
- 🔴 NEVER skip VERIFY phase
- ✅ ALWAYS follow TDD Red-Green-Verify cycle
- ✅ ALWAYS invoke @implementer for fix
- ✅ ALWAYS use tdd-enforcer
- 💭 FOCUS on proving hypothesis via failing test

## EXECUTION PROTOCOLS:

### 1. Display Simplified Thought Tree

Show top 2 hypotheses:

```
## Investigation Plan

### H1: {title} [Confidence: XX%] ⬅️ Starting here
- Quick Check: {action}
- Files: {list}

### H2: {title} [Confidence: XX%] (Fallback)
- Quick Check: {action}

Proceeding with TDD cycle for H1.
```

### 2. Execute Quick Check

Verify hypothesis prediction:

```
QUICK CHECK: {action from hypothesis}

Result: {CONFIRMED | REJECTED}

if CONFIRMED:
  proceed to TDD cycle
if REJECTED:
  mark H1 as "infirmed"
  proceed to H2
```

### 3. TDD Cycle via tdd-enforcer

#### RED Phase

Write failing test that reproduces the bug:

```
tdd.start_cycle({ mode: "debug", hypothesis: "H1" })
tdd.check_phase("RED")

Write test:
- Test name: test_{bug_description}
- Reproduce: {steps from evidence}
- Assert: {expected behavior}
- Run: MUST FAIL (reproduces bug)
```

**Test Example:**
```python
def test_user_cannot_login_after_password_reset():
    user = UserFactory.create()
    user.reset_password("newpassword123")

    # This should work but currently fails
    result = user.login("newpassword123")

    assert result.success is True  # FAILS - reproduces bug
```

#### GREEN Phase

Write minimal fix to pass test:

```
tdd.advance_phase()  # Move to GREEN

Invoke @implementer:
- Task: Fix {bug description}
- Hypothesis: {H1 details}
- Test to pass: {test name}
- Constraint: Minimal changes only
```

```
Task(
  subagent_type: "implementer",
  prompt: """
    Fix the following bug:

    ## Bug
    {bug description}

    ## Hypothesis
    {hypothesis details}

    ## Files
    {files_to_investigate}

    ## Failing Test
    {test code}

    ## Constraint
    Minimal fix only. Make test pass with smallest change.
  """
)
```

#### VERIFY Phase

Run full test suite:

```
tdd.advance_phase()  # Move to VERIFY

Commands (by stack):
- npm test / pytest / phpunit / gradlew test

VERIFY CHECKLIST:
[ ] New test passes
[ ] All existing tests pass
[ ] No regressions introduced
[ ] Linter passes
```

### 4. Fallback Loop

If hypothesis rejected or fix fails:

```
FALLBACK PROTOCOL:

if quick_check REJECTED:
  H1.status = "infirmed"
  confidence_boost(H2, H3)  # Adjust remaining
  proceed with H2

if TDD fails after 2 attempts:
  escalate to COMPLEX route (step-07)
```

### 5. Skip REFACTOR

For /debug Quick route, skip refactoring:

```
REFACTOR: SKIPPED

Rationale: Focus is bug fix, not code improvement.
If refactoring needed, suggest /refactor after fix.
```

## CONTEXT BOUNDARIES:

- This step expects: QUICK routing, ranked hypotheses
- This step produces: Bug fix with regression test

## OUTPUT FORMAT:

```
## Bug Fixed (Quick)

### Investigation
- **Hypothesis Tested**: H1 - {title}
- **Quick Check**: {action}
- **Result**: CONFIRMED

### TDD Cycle
- **RED**: Test written, failing ✅
- **GREEN**: Fix implemented, passing ✅
- **VERIFY**: All tests pass ✅

### Root Cause
{detailed explanation of actual root cause}

### Solution Applied
**Files Modified**:
- `{path1}` (+{N} LOC)
- `{path2}` (+{N} LOC)

**Changes**:
{description of fix}

### Regression Test
**File**: `{test_path}`
**Test**: `{test_name}`
```python
{test code}
```

### Verification
```
Tests: {N} passed, 0 failed
Time: {X}s
```

Proceeding to post-debug phase.
```

## FALLBACK OUTPUT:

```
## Hypothesis Rejected

### H1: {title}
- **Quick Check**: {action}
- **Result**: REJECTED
- **Reason**: {why prediction failed}

### Adjusting Hypotheses
- H1: infirmed
- H2: confidence boosted to {N}%
- H3: confidence boosted to {N}%

Proceeding with H2...
```

## ESCALATION OUTPUT:

```
+---------------------------------------------------------------------+
| [ESCALATION] Quick Fix Failed                                        |
+---------------------------------------------------------------------+
| Attempts: 2/2                                                        |
| Last Error: {error}                                                  |
|                                                                      |
| Root cause appears more complex than initially assessed.             |
| Escalating to COMPLEX route for full investigation.                  |
+---------------------------------------------------------------------+
```

Proceed to step-07-complex.md.

## NEXT STEP TRIGGER:

Proceed to step-08-post.md when:
- TDD cycle complete (Red-Green-Verify)
- All tests passing
- Fix verified
