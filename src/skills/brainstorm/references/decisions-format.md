# Decisions Format - Incremental Decisions Log

> Template for incremental decisions tracking during brainstorm sessions.

## Overview

The decisions file captures all decisions made during a brainstorm session as they happen. Unlike the journal (generated at end), this file is updated incrementally after each iteration where decisions are made.

**Filename**: `decisions-{slug}.md`
**Location**: `docs/briefs/{slug}/`
**Audience**: Session participant for tracking progress and resumption context.
**Principle**: Real-time capture - decisions recorded as they happen.

## Template

```markdown
# Decisions - {Topic}

> Incremental decisions log - Session `{session_id}`
> Started: {created_at}

---

## Summary

| Metric | Value |
|--------|-------|
| **Total decisions** | {count} |
| **Current EMS** | {ems_global}/100 |
| **Current iteration** | {iteration} |
| **Last updated** | {last_update} |

---

## Decisions Log

### D001: {decision_title}

| Attribute | Value |
|-----------|-------|
| **Iteration** | {iteration} |
| **EMS at time** | {ems_at_time}/100 |
| **Confidence** | {confidence} |
| **Timestamp** | {timestamp} |

**Decision**: {decision_text}

**Rationale**: {rationale}

**Impact**: {impact_description}

---

### D002: {decision_title}

| Attribute | Value |
|-----------|-------|
| **Iteration** | {iteration} |
| **EMS at time** | {ems_at_time}/100 |
| **Confidence** | {confidence} |
| **Timestamp** | {timestamp} |

**Decision**: {decision_text}

**Rationale**: {rationale}

**Impact**: {impact_description}

---

## Open Threads

| ID | Thread | Opened | Priority | Status | Notes |
|----|--------|--------|----------|--------|-------|
| T001 | {thread_text} | Iteration {N} | {priority} | {status} | {notes} |
| T002 | {thread_text} | Iteration {N} | {priority} | {status} | {notes} |

---

## Session Info

| Attribute | Value |
|-----------|-------|
| **Session ID** | {session_id} |
| **Topic** | {idea_raw} |
| **Template** | {template} |
| **Phase** | {phase} |
| **Persona** | {persona} |

---

*Last updated: {timestamp}*
*Resume with: `/brainstorm --continue {slug}-{timestamp}`*
```

## Field Definitions

### Decision Fields

| Field | Description | Source |
|-------|-------------|--------|
| `decision_title` | Short title (max 50 chars) | Extracted from decision text |
| `iteration` | Iteration number when decision was made | Session state |
| `ems_at_time` | EMS global score at decision time | EMS state |
| `confidence` | User's confidence level | Assessed from language ("definitely"=high, "probably"=medium, "maybe"=low) |
| `decision_text` | Full decision statement | User response |
| `rationale` | Why this decision was made | Extracted from context |
| `impact_description` | Expected impact on project | Inferred from decision |

### Thread Fields

| Field | Description | Values |
|-------|-------------|--------|
| `thread_text` | Description of open topic | Free text |
| `opened` | When thread was opened | Iteration number |
| `priority` | Importance level | high / medium / low |
| `status` | Current state | open / closed |
| `notes` | Additional context | Free text |

### Confidence Assessment

| Confidence | Trigger Words |
|------------|---------------|
| **High** | "definitely", "absolutely", "we must", "decided", "going with" |
| **Medium** | "probably", "likely", "should", "let's try" |
| **Low** | "maybe", "perhaps", "could", "might consider" |

## Decision Extraction Rules

### Markers for Decision Detection

Claude should look for these patterns in user responses:

```
Explicit decisions:
- "I've decided to..."
- "Let's go with..."
- "We'll use..."
- "The approach will be..."
- "I'm choosing..."

Implicit decisions:
- Direct answers to binary questions
- Selection from presented options
- Rejection of alternatives ("not X, but Y")
- Confirmation of suggestions ("yes, that works")
```

### Non-Decisions (Do NOT Extract)

```
- Questions ("Should we...?")
- Hypotheticals ("If we were to...")
- Deferred items ("We'll decide later")
- Exploration ("Let's consider...")
```

## File Operations

### Initial Creation

When first decision is made in a session:

```
1. Check if docs/briefs/{slug}/ directory exists
   - If not, create it
2. Create decisions-{slug}.md with header template
3. Add first decision entry
4. Add empty Open Threads section
```

### Incremental Update

For subsequent decisions:

```
1. Read current decisions-{slug}.md
2. Update Summary section (count, EMS, iteration, timestamp)
3. Insert new decision entry before "## Open Threads" section
4. Update Open Threads if any closed
5. Write updated file
```

### Thread Management

```
Opening a thread:
- Add row to Open Threads table
- Set status = "open"

Closing a thread:
- Update status = "closed"
- Add closing iteration to notes
```

## Integration Points

### With Session JSON

The decisions array in session JSON mirrors this file:

```json
{
  "decisions": [
    {
      "id": "D001",
      "text": "Use OAuth2 for authentication",
      "iteration": 2,
      "ems_at_time": 45,
      "rationale": "Industry standard, good library support",
      "confidence": "high",
      "timestamp": "2026-02-03T10:30:00Z"
    }
  ]
}
```

### With Journal

At session end, journal includes:
- Summary of all decisions (from this file)
- Full decision history (copied from session JSON)
- Thread resolution status

### With Brief

Brief section 6 (Key Decisions) pulls from:
- Decisions marked as high confidence
- Decisions with significant impact
- Final state of each decision area

---

## Example

```markdown
# Decisions - OAuth Authentication

> Incremental decisions log - Session `brainstorm-oauth-auth-20260203-103000`
> Started: 2026-02-03T10:30:00Z

---

## Summary

| Metric | Value |
|--------|-------|
| **Total decisions** | 3 |
| **Current EMS** | 67/100 |
| **Current iteration** | 4 |
| **Last updated** | 2026-02-03T11:15:00Z |

---

## Decisions Log

### D001: Use OAuth2 over custom auth

| Attribute | Value |
|-----------|-------|
| **Iteration** | 2 |
| **EMS at time** | 42/100 |
| **Confidence** | high |
| **Timestamp** | 2026-02-03T10:45:00Z |

**Decision**: Use OAuth2 protocol instead of building custom authentication.

**Rationale**: Industry standard, better security, existing library support (passport.js).

**Impact**: Reduces implementation time, improves security posture.

---

### D002: Support Google and GitHub providers

| Attribute | Value |
|-----------|-------|
| **Iteration** | 3 |
| **EMS at time** | 55/100 |
| **Confidence** | medium |
| **Timestamp** | 2026-02-03T10:58:00Z |

**Decision**: Start with Google and GitHub as OAuth providers, add more later.

**Rationale**: Covers 80% of target users, simplifies initial implementation.

**Impact**: Scopes MVP, leaves room for expansion.

---

### D003: Store tokens in httpOnly cookies

| Attribute | Value |
|-----------|-------|
| **Iteration** | 4 |
| **EMS at time** | 67/100 |
| **Confidence** | high |
| **Timestamp** | 2026-02-03T11:12:00Z |

**Decision**: Use httpOnly cookies for token storage instead of localStorage.

**Rationale**: Better XSS protection, automatic inclusion in requests.

**Impact**: Requires CORS configuration, improves security.

---

## Open Threads

| ID | Thread | Opened | Priority | Status | Notes |
|----|--------|--------|----------|--------|-------|
| T001 | Token refresh strategy | Iteration 3 | high | open | Need to decide on refresh window |
| T002 | Rate limiting approach | Iteration 4 | medium | open | Consider Redis vs in-memory |

---

## Session Info

| Attribute | Value |
|-----------|-------|
| **Session ID** | brainstorm-oauth-auth-20260203-103000 |
| **Topic** | Add OAuth authentication to the app |
| **Template** | feature |
| **Phase** | CONVERGENT |
| **Persona** | architecte |

---

*Last updated: 2026-02-03T11:15:00Z*
*Resume with: `/brainstorm --continue oauth-auth-20260203-103000`*
```

---

*Decisions Format v1.0 - EPCI Brainstorm v6.0*
