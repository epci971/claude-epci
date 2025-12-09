# epci-hotfix — Emergency Workflow for Critical Fixes (v2.7)

> ⚠️ **EMERGENCY MODE** — Use ONLY for production-critical incidents
> 
> `epci-hotfix` is an **inverted workflow**: Fix first, document after.
> It trades upfront planning for speed, but maintains discipline through strict constraints.

> **Philosophy**: "Stop the bleeding, then do the surgery properly."

---

## Critical Rules

- ⚠️ **P0/P1 incidents ONLY** — Not for "urgent but can wait"
- ⚠️ **Max 1 file modified** (2 absolute max if same module)
- ⚠️ **Max 50 LOC changed** — If more, it's not a hotfix
- ⚠️ **NO refactoring** — Fix only, improvements come later
- ⚠️ **NO new features** — Even if "it's easy while we're here"
- ⚠️ **Rollback plan MANDATORY** — Always have an exit strategy
- ⚠️ **Post-mortem within 24h** — Learn from the incident
- ⚠️ **Minimal flags only** — Speed over features (v2.7)

---

## Supported Flags (v2.7)

`epci-hotfix` supports only **2 flags** — emergency mode prioritizes speed over features.

### Available Flags

| Flag | Effect | Use Case |
|------|--------|----------|
| `--uc` | Ultra-compressed output | Reduce noise during crisis |
| `--validate` | Run syntax check after fix | Verify fix doesn't break build |

### Usage Examples

```bash
# Compressed output during incident
epci-hotfix --uc
$ARGUMENTS=<HOTFIX_BRIEF>

# Validate fix before deploy
epci-hotfix --validate
$ARGUMENTS=<HOTFIX_BRIEF>

# Both
epci-hotfix --uc --validate
$ARGUMENTS=<HOTFIX_BRIEF>
```

### Flag Behaviour

| Flag | Effect in epci-hotfix |
|------|----------------------|
| `--uc` | Removes explanatory text, keeps only critical info (incident, fix, verify) |
| `--validate` | Runs syntax/lint check before deploy step |

---

## Not Available in epci-hotfix (v2.7)

The following features are **intentionally disabled** — emergency mode needs **speed and focus**.

| Feature | Reason |
|---------|--------|
| `--preview` | Emergencies need immediate action, not previews |
| `--safe-mode` | Confirmations slow down incident response |
| `--introspect` | Focus on fix, not explaining reasoning |
| `--verbose` | Brevity is critical during incidents |
| `--dry-run` | No time for simulations in P0/P1 |
| `--persona-*` | Emergencies need focus, not multiple perspectives |
| Phase A/B separation | Single-pass emergency workflow only |

> **If you need these features, you're not in a real emergency** → use `epci-soft` or full EPCI.

---

## 1. When to Use epci-hotfix

### 1.1 Valid Triggers (USE epci-hotfix)

| Situation | Example |
|-----------|---------|
| **Production down** | 500 errors on critical endpoints |
| **Security breach active** | Data exposure, unauthorized access |
| **Data corruption ongoing** | Records being corrupted in real-time |
| **SLA breach imminent** | System will breach SLA in < 1 hour |
| **Business-critical blocker** | Payments failing, orders stuck |

### 1.2 Invalid Triggers (DO NOT USE)

| Situation | Use Instead |
|-----------|-------------|
| "Client is complaining" (no technical impact) | `epci-soft` or `epci-micro` |
| "It's urgent but can wait until tomorrow" | `epci-micro` |
| "I want to go fast" | Standard EPCI |
| "While we're at it, let's also..." | NO — separate ticket |
| Bug in staging/dev environment | Standard EPCI |

### 1.3 Severity Classification

| Severity | Definition | Response Time | Example |
|----------|------------|---------------|---------|
| **P0** | Complete outage, all users affected | Immediate | Site down, API 500s |
| **P1** | Major feature broken, many users affected | < 1 hour | Checkout broken, login failing |
| **P2** | Feature degraded, some users affected | < 4 hours | Slow queries, partial failures |
| **P3** | Minor issue, workaround exists | Next business day | UI glitch, non-critical bug |

> **epci-hotfix** is for **P0 and P1 only**. P2/P3 use standard EPCI.

---

## 2. Inputs

### 2.1 Minimal Input Required

```text
$ARGUMENTS=<HOTFIX_BRIEF>
  INCIDENT: <1-2 sentence description of what's broken>
  SEVERITY: P0 | P1
  SYMPTOMS: <what users/systems are experiencing>
  SUSPECTED_CAUSE: <if known, otherwise "unknown">
  ROLLBACK_PLAN: <how to revert if fix fails>
```

### 2.2 Example Input

```text
$ARGUMENTS=<HOTFIX_BRIEF>
  INCIDENT: Production API returning 500 on /api/bookings endpoint
  SEVERITY: P0
  SYMPTOMS: All booking requests failing, 100% error rate since 14:32 UTC
  SUSPECTED_CAUSE: Null pointer in UserSerializer after deploy at 14:30
  ROLLBACK_PLAN: Revert commit abc123 or disable user avatar feature flag
```

---

## 3. Workflow Steps

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 0        STEP 1        STEP 2        STEP 3        STEP 4 │
│  DECLARE  →   DIAGNOSE  →    FIX     →    DEPLOY   →   DOCUMENT │
│  (30 sec)     (2-5 min)    (5-15 min)    (5 min)      (< 24h)   │
└─────────────────────────────────────────────────────────────────┘
         │                                      │
         └──────────── IMMEDIATE ───────────────┘
                                                        POST-FACTO
```

### 3.2 Step 0 — Declare Emergency (30 seconds)

**Objective**: Confirm this is a real emergency and capture context.

**Actions**:
1. State the incident in 1-2 sentences
2. Confirm severity (P0 or P1)
3. State rollback plan (even if "revert last commit")

**Output**:
```markdown
## HOTFIX INITIATED

- **Incident**: API 500 errors on /api/bookings
- **Severity**: P0
- **Time**: 2025-01-15 14:35 UTC
- **Rollback**: Revert commit abc123
- **Flags**: --validate (v2.7)
```

### 3.3 Step 1 — Diagnose (2-5 minutes)

**Objective**: Identify root cause and target file.

**Actions**:
1. Check error logs, stack traces, monitoring
2. Identify the most likely root cause
3. Identify the ONE file to change (max 2)
4. Verbally confirm the fix approach

**Constraints**:
- Do NOT start coding yet
- If cause unclear after 5 min → escalate or apply broader rollback

**Output**:
```markdown
## DIAGNOSIS

### Root Cause
Null pointer exception in `UserSerializer.php` line 45.
`$user->profile->avatar` accessed without null check when user has no profile.

### Target File
`src/Serializer/UserSerializer.php`

### Fix Approach
Add null-safe operator: `$user->profile?->avatar ?? self::DEFAULT_AVATAR`
```

### 3.4 Step 2 — Fix (5-15 minutes)

**Objective**: Implement minimal fix.

**Actions**:
1. Implement the smallest possible change that fixes the issue
2. Run existing tests (no new tests required at this stage)
3. If `--validate`: run syntax/lint check (v2.7)
4. Manual smoke test if possible

**Constraints**:
- NO refactoring ("while we're here...")
- NO optimization
- NO additional improvements
- If fix exceeds 50 LOC → STOP, this needs standard EPCI

**Output**:
```markdown
## FIX IMPLEMENTED

### Change
```php
// Before (line 45)
$avatar = $user->profile->avatar;

// After
$avatar = $user->profile?->avatar ?? self::DEFAULT_AVATAR;
```

### Tests
- [x] Existing test suite passes (47/47)
- [x] Manual test: API returns 200 with null profile

### Validation (--validate) (v2.7)
- [x] Syntax check: `php -l src/Serializer/UserSerializer.php` → ✅ Pass
- [x] Lint: PHPStan → ✅ Pass (0 errors)
```

### 3.5 Step 3 — Deploy (5 minutes)

**Objective**: Get the fix to production safely.

**Actions**:
1. Commit with `[HOTFIX]` tag
2. Push to production branch (follow your deployment process)
3. Verify fix in production
4. Monitor for 5-10 minutes

**Commit Format**:
```
[HOTFIX] fix: null pointer in UserSerializer when profile missing

Incident: P0 - API 500 on /api/bookings
Root cause: Accessing avatar on null profile object
Fix: Add null-safe operator with default fallback

Refs: incident-2025-01-15-1432
```

**Output**:
```markdown
## DEPLOYED

- **Commit**: def456
- **Deployed at**: 2025-01-15 14:52 UTC
- **Verification**:
  - [x] API returning 200
  - [x] Error rate back to 0%
  - [x] No new errors in logs
```

### 3.6 Step 4 — Document Post-Facto (within 24 hours)

**Objective**: Capture learnings and create follow-up items.

**Actions**:
1. Create minimal Feature Document (or Hotfix Report)
2. Write incident timeline
3. Identify follow-up actions
4. Schedule post-mortem if needed

**This step is NOT optional** — even in emergencies, we learn and improve.

---

## 4. Output Format

### 4.1 Standard Hotfix Report Template

```markdown
# HOTFIX REPORT: <short-description>

## Incident Summary

| Field | Value |
|-------|-------|
| **Incident ID** | hotfix-2025-01-15-api-500 |
| **Severity** | P0 |
| **Reported** | 2025-01-15 14:32 UTC |
| **Resolved** | 2025-01-15 14:52 UTC |
| **Duration** | 20 minutes |
| **Affected Users** | ~500 (all booking attempts) |
| **Flags Used** | --validate (v2.7) |

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:30 | Deploy of commit abc123 |
| 14:32 | First 500 errors reported |
| 14:35 | Incident declared, hotfix initiated |
| 14:40 | Root cause identified |
| 14:48 | Fix implemented and tested |
| 14:52 | Fix deployed to production |
| 14:55 | Verification complete, incident resolved |

## Root Cause

`UserSerializer.php` line 45: accessing `$user->profile->avatar` without 
null check. This code path was introduced in commit abc123 and wasn't 
covered by existing tests.

## Fix Applied

```php
// File: src/Serializer/UserSerializer.php
// Line: 45

// Before
$avatar = $user->profile->avatar;

// After  
$avatar = $user->profile?->avatar ?? self::DEFAULT_AVATAR;
```

## Files Changed

| File | Changes |
|------|---------|
| `src/Serializer/UserSerializer.php` | +1, -1 |

## Rollback Plan Used

N/A — Fix was successful. Prepared rollback was: revert commit abc123.

## Verification

- [x] Existing tests pass (47/47)
- [x] Manual test on staging
- [x] Production API returning 200
- [x] Error rate at 0%
- [x] No new errors in monitoring
- [x] Syntax/lint validation passed (--validate) (v2.7)

## Follow-up Actions

| Action | Owner | Ticket | Priority |
|--------|-------|--------|----------|
| Add unit test for null profile case | @dev | #1234 | High |
| Review other serializers for similar issues | @dev | #1235 | Medium |
| Add null-profile test user to QA dataset | @qa | #1236 | Medium |

## Post-Mortem

**Scheduled**: 2025-01-16 10:00 UTC

**Questions to Address**:
1. Why wasn't this caught in code review?
2. Why wasn't this caught by tests?
3. Should we add static analysis for null-safety?

## Lessons Learned

1. Serializers need defensive null checks
2. Test data should include edge cases (null profile)
3. Consider adding nullable type hints to catch this at compile time
```

### 4.2 Ultra-Compressed Output (--uc)

When `--uc` flag is active, use this minimal format:

```markdown
## HOTFIX: API 500 on /api/bookings

**P0** | 14:35 UTC | Rollback: revert abc123

### Diagnosis
NullPointer in `UserSerializer.php:45` — accessing avatar on null profile

### Fix
```php
$avatar = $user->profile?->avatar ?? self::DEFAULT_AVATAR;
```

### Status
✅ Deployed 14:52 UTC | Tests: 47/47 | Errors: 0%

### Follow-up
- #1234: Add null profile test
```

### 4.3 Minimal Feature Document (Alternative)

If your project requires Feature Documents for all changes:

```markdown
# Hotfix: Null Pointer in User Serializer

## 1. Functional Brief — EPCI-HOTFIX

### Context
Emergency fix for P0 incident — API 500 errors on /api/bookings.

### Objective
Prevent null pointer exception when serializing users without profiles.

### Acceptance Criteria
- [AC1] API returns 200 for users with profiles
- [AC2] API returns 200 for users without profiles (with default avatar)

---

## 2. Technical Plan — EPCI-HOTFIX

### Fix
Add null-safe operator in UserSerializer.php line 45.

### Files Changed
- `src/Serializer/UserSerializer.php`

---

## 3. Final Report — EPCI-HOTFIX

### Status
✅ DEPLOYED — 2025-01-15 14:52 UTC

### Flags Used (v2.7)
- `--validate`: Syntax and lint checks passed

### Verification
All acceptance criteria met. See Hotfix Report for details.

### Follow-up
- #1234: Add unit test
- #1235: Review other serializers
```

---

## 5. Constraints & Boundaries

### 5.1 Hard Limits

| Constraint | Limit | If Exceeded |
|------------|-------|-------------|
| Files modified | 1 (max 2) | → Standard EPCI |
| Lines changed | < 50 LOC | → Standard EPCI |
| Time to fix | < 30 min ideal | → Consider rollback |
| Scope creep | Zero tolerance | → Separate ticket |

### 5.2 What epci-hotfix MUST Do

1. ✅ Declare the emergency explicitly
2. ✅ Diagnose before coding
3. ✅ Implement minimal fix only
4. ✅ If `--validate`: run syntax/lint check (v2.7)
5. ✅ Verify in production
6. ✅ Document within 24 hours
7. ✅ Create follow-up tickets for proper fixes

### 5.3 What epci-hotfix MUST NOT Do

1. ❌ Refactor code "while we're here"
2. ❌ Add new features
3. ❌ Optimize performance
4. ❌ Fix unrelated bugs
5. ❌ Skip documentation
6. ❌ Be used for non-emergencies
7. ❌ Use advanced flags (preview, safe-mode, introspect, personas) (v2.7)

---

## 6. Recovery — When Things Go Wrong

### 6.1 Fix Doesn't Work

```
IF fix doesn't resolve the issue:
  1. Immediately execute rollback plan
  2. Re-assess root cause
  3. Either: try alternative fix OR escalate
  4. Consider: is this bigger than a hotfix?
```

### 6.2 Fix Causes New Issues

```
IF fix introduces new problems:
  1. Rollback immediately
  2. Document what went wrong
  3. This needs standard EPCI — too complex for hotfix
```

### 6.3 Can't Identify Root Cause

```
IF root cause unclear after 5-10 minutes:
  1. Apply broadest safe rollback (last known good state)
  2. Communicate: "service restored via rollback, investigating root cause"
  3. Switch to standard EPCI for proper investigation
```

### 6.4 Validation Fails (--validate) (v2.7)

```
IF --validate reports errors:
  1. Fix syntax/lint errors before deploy
  2. If errors are in unrelated code: investigate
  3. Do NOT deploy with validation failures
  4. Consider: is the fix correct?
```

---

## 7. Integration with EPCI Workflow

### 7.1 Decision Point

```
Is this a P0/P1 production incident?
├── YES → epci-hotfix
└── NO  → epci-0-briefing (standard routing)
```

### 7.2 Transition to Standard EPCI

After a hotfix, you often need follow-up work:

```
epci-hotfix (emergency fix)
       │
       ▼
  Follow-up ticket created
       │
       ▼
  epci-0-briefing (for proper fix/refactor/tests)
       │
       ▼
  Standard EPCI workflow (with full flags/personas available)
```

---

## 8. Example — Complete Hotfix Session

Below is a **complete example** of an `epci-hotfix` session with `--validate` flag.

````markdown
User: We have a P0! API is returning 500 on all booking requests since 
the deploy 10 minutes ago.

---

## HOTFIX INITIATED

- **Incident**: API 500 errors on /api/bookings
- **Severity**: P0
- **Time**: 2025-01-15 14:35 UTC
- **Rollback**: Revert commit abc123
- **Flags**: --validate

---

## DIAGNOSIS

### Root Cause
Null pointer exception in `UserSerializer.php` line 45.
`$user->profile->avatar` accessed without null check when user has no profile.

### Target File
`src/Serializer/UserSerializer.php`

### Fix Approach
Add null-safe operator: `$user->profile?->avatar ?? self::DEFAULT_AVATAR`

---

## FIX IMPLEMENTED

### Change
```php
// Before (line 45)
$avatar = $user->profile->avatar;

// After
$avatar = $user->profile?->avatar ?? self::DEFAULT_AVATAR;
```

### Tests
- [x] Existing test suite passes (47/47)
- [x] Manual test: API returns 200 with null profile

### Validation (--validate)
- [x] Syntax: `php -l UserSerializer.php` → ✅ Pass
- [x] Lint: PHPStan level 8 → ✅ Pass

---

## DEPLOYED

- **Commit**: def456
- **Deployed at**: 2025-01-15 14:52 UTC
- **Verification**:
  - [x] API returning 200
  - [x] Error rate back to 0%
  - [x] No new errors in logs

---

## INCIDENT RESOLVED

```text
✅ HOTFIX COMPLETE

Incident: P0 - API 500 on /api/bookings
Duration: 20 minutes (14:32 → 14:52 UTC)
Fix: Null-safe operator in UserSerializer.php
Validation: ✅ Pass (--validate)

Follow-up tickets created:
- #1234: Add unit test for null profile
- #1235: Review other serializers
```

Post-mortem scheduled: 2025-01-16 10:00 UTC
````

---

## 9. Summary

`epci-hotfix` is the **emergency mode** of the EPCI workflow:

- It **inverts the normal workflow**: Fix first, document after
- It is for **P0/P1 production incidents ONLY**
- It has **strict constraints**: 1-2 files, < 50 LOC, no refactoring
- It requires a **rollback plan** before starting
- It mandates **post-incident documentation** within 24 hours
- It creates **follow-up tickets** for proper fixes via standard EPCI

The philosophy is **"Stop the bleeding, then do the surgery properly."**

When in doubt about whether something is a real emergency, it probably isn't → use standard EPCI.

**v2.7 improvements:**

- **Limited flags support:** `--uc` for compressed output, `--validate` for syntax check
- **Explicit exclusions:** Documents why most flags are NOT available
- **Validation step:** Optional syntax/lint check before deploy
- **Ultra-compressed template:** Minimal output format for `--uc`
- **Recovery for validation failures:** What to do if `--validate` reports errors

**Design principle:**

> Emergency mode needs **speed and focus**. Every feature that doesn't directly help fix the incident is removed. If you need advanced features, you're not in a real emergency.

---

## 10. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-flags.md` | Universal flags reference (shows hotfix limitations) |
| `epci-workflow-guide.md` | Complete workflow documentation |
| `epci-0-briefing.md` | Standard EPCI entry point (for follow-ups) |

---

*This document is part of the EPCI v2.7 workflow system.*
