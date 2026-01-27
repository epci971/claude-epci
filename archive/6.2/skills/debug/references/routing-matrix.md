# Routing Matrix

## Overview

Decision matrix for routing bugs to TRIVIAL, QUICK, or COMPLEX investigation paths.

## Routing Criteria

| Criterion | TRIVIAL | QUICK | COMPLEX |
|-----------|---------|-------|---------|
| Causes | 1 obvious | 1 | 2+ |
| LOC to fix | <10 | <50 | >=50 |
| Files affected | 1 | 1-2 | 3+ |
| Uncertainty | <5% | <20% | >=20% |
| Test needed | No | Yes | Yes |
| Review needed | No | No | Yes |

## Scoring System

Each criterion scores 0, 1, or 2:

```
Score 0 = TRIVIAL indicator
Score 1 = QUICK indicator
Score 2 = COMPLEX indicator
```

### Causes Score

| Situation | Score |
|-----------|-------|
| 1 obvious cause, no alternatives | 0 |
| 1 likely cause, low uncertainty | 1 |
| 2+ potential causes | 2 |
| Unknown, need investigation | 2 |

### LOC Score

| Estimated LOC | Score |
|---------------|-------|
| 1-9 | 0 |
| 10-49 | 1 |
| 50+ | 2 |

### Files Score

| Files Affected | Score |
|----------------|-------|
| 1 | 0 |
| 2 | 1 |
| 3+ | 2 |

### Uncertainty Score

| Confidence in Root Cause | Score |
|--------------------------|-------|
| >95% (near certain) | 0 |
| 80-95% (confident) | 1 |
| <80% (uncertain) | 2 |

## Routing Decision

```python
def determine_route(scores):
    complex_count = sum(1 for s in scores if s == 2)

    if complex_count >= 2:
        return "COMPLEX"
    elif max(scores) == 0:
        return "TRIVIAL"
    else:
        return "QUICK"
```

## Decision Examples

### Example 1: TRIVIAL

**Bug**: `TypeError: Cannot read property 'length' of undefined`
**Stack trace**: Points to line 42 in `utils.ts`

| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 1 obvious (missing null check) | 0 |
| LOC | 1 line | 0 |
| Files | 1 | 0 |
| Uncertainty | 99% (stack trace is clear) | 0 |

**Decision**: TRIVIAL (all scores = 0)

### Example 2: QUICK

**Bug**: "Users can't login after password reset"
**Research**: Similar bug found in project-memory

| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 1 likely (session not cleared) | 1 |
| LOC | ~20 lines | 1 |
| Files | 2 (auth service, session manager) | 1 |
| Uncertainty | 85% confidence | 1 |

**Decision**: QUICK (max score = 1, no score = 2)

### Example 3: COMPLEX

**Bug**: "Intermittent 500 errors on /api/orders under load"
**Research**: Multiple potential causes

| Criterion | Value | Score |
|-----------|-------|-------|
| Causes | 3+ (race condition, timeout, memory) | 2 |
| LOC | Unknown, likely 50+ | 2 |
| Files | 4+ (controller, service, queue, cache) | 2 |
| Uncertainty | 60% confidence | 2 |

**Decision**: COMPLEX (4 scores = 2)

## Override Rules

### --full Flag

```
if --full:
  route = COMPLEX
  // Ignore scoring
```

### --turbo Flag

```
if --turbo AND route == COMPLEX AND confidence >= 70%:
  route = QUICK
  // Simplify for speed
```

### Escalation from TRIVIAL

If during TRIVIAL fix:
- Fix requires >10 LOC → Escalate to QUICK
- Fix requires >1 file → Escalate to QUICK
- Fix introduces regression → Escalate to QUICK

### Escalation from QUICK

If during QUICK fix:
- TDD fails 2x → Escalate to COMPLEX
- Root cause different than expected → Escalate to COMPLEX
- Multiple components involved → Escalate to COMPLEX

## Route Characteristics

### TRIVIAL
- No breakpoint (direct fix)
- No test required
- No review required
- Inline summary only
- Duration: < 2 minutes

### QUICK
- No breakpoint
- TDD cycle required (Red-Green-Verify)
- @implementer invoked
- No review required
- Duration: 5-15 minutes

### COMPLEX
- Diagnostic breakpoint required
- TDD cycle required (Red-Green-Refactor-Verify)
- @implementer invoked
- @code-reviewer required
- @security-auditor (if applicable)
- @qa-reviewer (if >= 3 tests)
- Debug Report generated
- Duration: 15-60 minutes

## Visual Decision Tree

```
START
  |
  +-- Causes > 1? ──────────────────┐
  |   YES                           │
  |                                 v
  +-- LOC >= 50? ──────────────────> COMPLEX
  |   YES                           ^
  |                                 │
  +-- Files >= 3? ─────────────────┘
  |   YES
  |
  +-- Uncertainty >= 20%? ─────────┐
      YES                          │
                                   v
                                 COMPLEX
  |
  +-- All criteria = 0? ───────────> TRIVIAL
  |   YES
  |
  +-- Otherwise ───────────────────> QUICK
```
