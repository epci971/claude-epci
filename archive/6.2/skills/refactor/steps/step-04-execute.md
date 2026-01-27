# Step 04: Execute

> Apply transformations with TDD enforcement, revert on failure.

## Trigger

- Previous step: `step-03-breakpoint.md` with "Execute" decision

## Inputs

| Input | Source |
|-------|--------|
| Transformation plan | From step-02 |
| Stack context | From step-00 |
| Test command | Auto-detected or user config |

## Protocol

### 1. Verify Baseline (Tests Green)

```bash
# Detect test command
IF python-django:
  pytest <target_tests>
ELSE IF javascript-react:
  npm test -- --testPathPattern=<target>
ELSE IF java-springboot:
  mvn test -Dtest=<target>
ELSE IF php-symfony:
  php bin/phpunit <target_tests>
ELSE:
  # Generic detection
  npm test OR pytest OR mvn test
```

**CRITICAL**: If baseline tests fail, STOP and notify user:

```
## Baseline Tests Failed

Cannot proceed with refactoring - existing tests are failing.

**Failing tests**:
- test_authenticate_valid_user
- test_token_refresh

**Recommendation**: Fix failing tests first, then restart /refactor
```

### 2. Execute Each Transformation

For each transformation in order:

```
FOR transformation in transformations:

  1. LOG: "Starting {transformation.id}: {transformation.description}"

  2. IF transformation.dependencies not all completed:
       SKIP (will be executed after dependencies)

  3. APPLY transformation:
     - Read source file(s)
     - Apply pattern (extract, move, inline, etc.)
     - Write modified file(s)
     - Create new file(s) if needed

  4. RUN tests:
     - Execute test command
     - Capture output

  5. IF tests PASS:
       MARK transformation as completed
       IF --atomic flag:
         git add <modified files>
         git commit -m "refactor: {transformation.description}"

  6. IF tests FAIL:
       LOG: "Tests failed after {transformation.id}"
       REVERT all changes from this transformation
       ANALYZE failure:
         - Was behavior accidentally changed?
         - Are tests too tightly coupled?
       NOTIFY user with options:
         [A] Skip this transformation, continue
         [B] Retry with modifications
         [C] Abort entire refactoring
```

### 3. TDD Cycle per Transformation

Use `tdd-enforcer` in REFACTOR mode:

```
tdd-enforcer mode: REFACTOR
expectations:
  - Tests must pass BEFORE transformation (baseline)
  - Tests must pass AFTER transformation (preservation)
  - No new tests required (behavior unchanged)

on_failure:
  - Automatic revert
  - Detailed diff of what changed
  - Suggestion for fix
```

### 4. Progress Tracking

```
## Execution Progress

| # | Transformation | Status | Tests |
|---|----------------|--------|-------|
| T1 | Extract validate_credentials() | [DONE] | 12/12 |
| T2 | Extract TokenValidator class | [IN PROGRESS] | ... |
| T3 | Move user lookups | [PENDING] | - |
| T4 | Inline dead refresh code | [PENDING] | - |

Current: T2 - Applying extract-class pattern...
```

### 5. Handle Complex Patterns

#### Extract Method

```python
# Before
def authenticate(self, username, password):
    # 80 lines of mixed logic
    ...

# After
def authenticate(self, username, password):
    if not self._validate_credentials(username, password):
        raise AuthError()
    return self._create_session(username)

def _validate_credentials(self, username, password):
    # Extracted 30 lines
    ...
```

#### Strangler Fig (Architecture)

```
1. Create new implementation alongside old
2. Route small percentage of traffic to new
3. Gradually increase routing
4. Remove old implementation when 100% migrated

Note: Full strangler fig may span multiple sessions
```

### 6. Completion Summary

```
## Execution Complete

**Transformations**: 4/4 completed
**Tests**: 48/48 passing
**Time**: ~3 minutes

### Applied Changes
- T1: Extracted validate_credentials() [OK]
- T2: Created TokenValidator class [OK]
- T3: Moved user lookups to user.py [OK]
- T4: Removed dead code [OK]

### Files Modified
- src/services/auth.py (modified)
- src/services/user.py (modified)
- src/validators/token_validator.py (created)
- tests/test_auth.py (modified)
- tests/validators/test_token_validator.py (created)
```

## Outputs

| Output | Destination |
|--------|-------------|
| Completed transformations | State |
| Modified files list | State |
| Execution log | User display |
| Atomic commits (if flag) | Git |

## Next Step

→ `step-05-review.md` (conditional based on scope)

## Error Handling

| Error | Resolution |
|-------|------------|
| Tests fail after transformation | Revert, offer options |
| File write error | Check permissions, retry |
| Git commit fails | Skip atomic, continue |
| Transformation conflict | Reorder or manual intervention |
