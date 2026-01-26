# Debug Examples

## Overview

Three complete examples demonstrating each debug route.

---

## Example 1: TRIVIAL Route

### Input

```
/debug "TypeError: Cannot read property 'length' of undefined in ProductList.tsx"
```

### Step 00: Clarify

```
Clarity Score: 0.85

| Criterion | Score |
|-----------|-------|
| Error specificity | 1.0 |
| Reproduction | 0.6 |
| Context | 0.8 |
| Expected behavior | 0.7 |
| Stack trace | 1.0 |

Decision: SKIP (clarity >= 0.6)
```

### Step 01: Evidence

```
Stack Trace:
  TypeError: Cannot read property 'length' of undefined
    at ProductList (ProductList.tsx:23)
    at renderWithHooks (react-dom.development.js:14985)

Similar Bugs: None found
Recent Changes: No changes to ProductList.tsx in last week
Stack Detected: javascript-react
```

### Step 03: Thought Tree

```
H1: Missing null check on products array [Confidence: 95%]
- Evidence: Line 23 likely accesses products.length without check
- Quick Check: Read line 23

H2: Products not initialized in state [Confidence: 40%]
- Evidence: Possible useState initial value issue
```

### Step 04: Routing

```
| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 1 obvious | 0 |
| LOC | 1 | 0 |
| Files | 1 | 0 |
| Uncertainty | 5% | 0 |

Route: TRIVIAL
```

### Step 05: Trivial Fix

```
File: src/components/ProductList.tsx:23

Before:
const count = products.length;

After:
const count = products?.length ?? 0;

Verification: Syntax check passed
```

### Output

```
+-- BUG FIXED (Trivial) -------------------------+
| Cause: Missing null check on products array     |
| Fix: Added optional chaining and nullish        |
|      coalescing operator                        |
| File: src/components/ProductList.tsx:23         |
+-------------------------------------------------+
```

---

## Example 2: QUICK Route

### Input

```
/debug "Users can't login after password reset"
```

### Step 00: Clarify

```
Clarity Score: 0.55

Questions:
Q1: What error do users see?
→ User: "Invalid credentials" message

Q2: Does this affect all users or specific ones?
→ User: All users who reset password

Clarity Score (after): 0.75
```

### Step 01: Evidence

```
Error: "Invalid credentials" on login attempt
Reproduction: 100% reproducible for users who reset password
Similar Bugs: Bug #42 - "Session not cleared after password change" (6 months ago)
Recent Changes: commit abc123 - "Refactored auth service" (3 days ago)
Stack: python-django
```

### Step 02: Research

```
Context7 Query: "Django password reset login fails"
Results: 3 relevant docs about session handling after password change

Key Finding: Django requires session flush after password change
Source: Django security docs
```

### Step 03: Thought Tree

```
H1: Session not invalidated after password reset [Confidence: 82%]
- Evidence: Similar bug #42, Django docs mention this
- Prediction: Old session token still valid, but password hash changed
- Quick Check: Add logging to check session state

H2: Password hash not saved correctly [Confidence: 35%]
- Evidence: Possible but no direct evidence
```

### Step 04: Routing

```
| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 1 | 1 |
| LOC | ~15 | 1 |
| Files | 2 | 1 |
| Uncertainty | 18% | 1 |

Route: QUICK
```

### Step 06: Quick Fix

#### Quick Check Result
```
Added logging: session.auth_hash != user.get_session_auth_hash()
Result: CONFIRMED - session hash mismatch
```

#### TDD Cycle

**RED:**
```python
def test_user_can_login_after_password_reset():
    user = UserFactory.create(password="oldpass")
    user.set_password("newpass")
    user.save()

    # Login should work with new password
    client = Client()
    response = client.post('/login/', {
        'username': user.username,
        'password': 'newpass'
    })

    assert response.status_code == 302  # FAILS
```

**GREEN:**
```python
# auth/services/password.py
def reset_password(user, new_password):
    user.set_password(new_password)
    user.save()
    # Fix: Invalidate all sessions
    update_session_auth_hash(request, user)
```

**VERIFY:**
```
Tests: 45 passed, 0 failed
Time: 2.3s
```

### Output

```
+---------------------------------------------------------------------+
| :white_check_mark: DEBUG COMPLETE (Quick)                                              |
+---------------------------------------------------------------------+
| Bug: Users can't login after password reset                          |
| Root Cause: Session auth hash not updated after password change      |
| Files Modified: 2                                                    |
| Tests Added: 1                                                       |
| Duration: 8m                                                         |
|                                                                      |
| Pattern stored in project-memory for future reference.               |
+---------------------------------------------------------------------+
```

---

## Example 3: COMPLEX Route

### Input

```
/debug --full "Intermittent 500 errors on /api/orders endpoint under load"
```

### Step 01: Evidence

```
Error: HTTP 500 Internal Server Error
Frequency: ~5% of requests under load
Environment: Production only
Stack Trace: Varies - sometimes ORM, sometimes cache
Recent Changes: Multiple commits to orders module
Stack: python-django
```

### Step 02: Research

```
Context7: Django race conditions, connection pooling
WebSearch: "Django intermittent 500 load" - multiple causes found
Perplexity: Suggested for deep analysis
```

### Step 03: Thought Tree

```
H1: Database connection pool exhaustion [Confidence: 65%]
- Evidence: Error more frequent under load
- Prediction: Connection count will hit limit during spike

H2: Race condition in order status update [Confidence: 58%]
- Evidence: Two threads might update same order
- Prediction: Database constraint violation in logs

H3: Cache stampede on order lookup [Confidence: 45%]
- Evidence: Cache TTL might cause simultaneous refreshes
- Prediction: Spike in DB queries when cache expires

H4: Memory pressure causing OOM [Confidence: 30%]
- Evidence: Possible but no direct indication
```

### Step 04: Routing

```
| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 3+ | 2 |
| LOC | Unknown | 2 |
| Files | 4+ | 2 |
| Uncertainty | 35% | 2 |

Route: COMPLEX (--full flag also set)
```

### Step 07: Complex Investigation

#### Solution Scoring

| Solution | Simplicity | Risk | Time | Maintain | Total |
|----------|------------|------|------|----------|-------|
| S1: Increase pool size | 4 | 5 | 5 | 2 | 4.00 |
| S2: Add select_for_update | 3 | 3 | 3 | 4 | 3.25 |
| S3: Implement cache locking | 2 | 4 | 2 | 4 | 3.00 |

#### Breakpoint

```
+---------------------------------------------------------------------+
| [DIAGNOSTIC] Root Cause Analysis Complete                            |
+---------------------------------------------------------------------+
| Root Cause: Database connection pool exhaustion under load           |
| Confidence: 65%                                                      |
|                                                                      |
| Solutions (Ranked):                                                  |
| S1: Increase connection pool size (4.00) - Quick fix                 |
| S2: Add select_for_update locking (3.25) - Prevents races            |
| S3: Implement cache locking (3.00) - Prevents stampede               |
+---------------------------------------------------------------------+
| [A] S1 (Recommended)  [B] S2  [C] Both S1+S2  [?] Details            |
+---------------------------------------------------------------------+

User selected: [C] Both S1+S2
```

#### Implementation

Files modified:
- `config/settings/prod.py` - Increased CONN_MAX_AGE and pool size
- `apps/orders/services/order_service.py` - Added select_for_update
- `apps/orders/tests/test_concurrency.py` - Added load test

#### Reviews

```
@code-reviewer: APPROVED
- Clean implementation
- Tests cover concurrent scenarios

@security-auditor: N/A (not auth-related)

@qa-reviewer: APPROVED
- Good test coverage for race conditions
```

### Debug Report Generated

```
Location: docs/debug/orders-500-load-2026-01-26.md
```

### Output

```
+---------------------------------------------------------------------+
| :white_check_mark: DEBUG COMPLETE (Complex)                                            |
+---------------------------------------------------------------------+
| Bug: Intermittent 500 errors on /api/orders under load               |
| Root Cause: DB connection exhaustion + race condition                |
| Solution: Increased pool + added locking                             |
| Files Modified: 3                                                    |
| Tests Added: 4                                                       |
| Duration: 35m                                                        |
|                                                                      |
| Reviews:                                                             |
| - Code Review: APPROVED                                              |
| - QA Review: APPROVED                                                |
|                                                                      |
| Debug Report: docs/debug/orders-500-load-2026-01-26.md               |
| Pattern stored in project-memory for future reference.               |
+---------------------------------------------------------------------+
```

---

## Summary

| Example | Route | Duration | Key Technique |
|---------|-------|----------|---------------|
| Missing null check | TRIVIAL | ~1 min | Direct fix |
| Password reset session | QUICK | ~8 min | TDD cycle, project-memory |
| Load-related 500s | COMPLEX | ~35 min | Multi-hypothesis, solution scoring |
