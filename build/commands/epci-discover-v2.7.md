# epci-discover — Requirement Discovery Mode (v2.7)

> **PRE-BRIEFING MODE** — Transform vague ideas into structured briefs
>
> `epci-discover` is for **unclear requests**: when the user has an idea but hasn't
> fully defined what they want. It uses Socratic questioning to clarify requirements
> before entering the standard EPCI workflow.
>
> Output: A **validated EPCI_READY_BRIEF**, ready for `epci-0-briefing` or direct routing.

> **Philosophy**: "Ask the right questions before building the wrong thing."

---

## Critical Rules

- ⚠️ `epci-discover` is PRE-workflow — it comes BEFORE `epci-0-briefing`
- ⚠️ NO code exploration, NO technical planning — purely functional discovery
- ⚠️ Output MUST be an `EPCI_READY_BRIEF` or explicit "NOT READY" with reasons
- ⚠️ Maximum 3 rounds of questions before forcing a decision
- ⚠️ Always end with routing recommendation

---

## 1. When to Use epci-discover

### 1.1 Valid Triggers (USE epci-discover)

| Situation | Example |
|-----------|---------|
| **Vague request** | "I want to improve the app" |
| **Missing context** | "Add a feature like competitor X has" |
| **Unclear scope** | "Make the booking process better" |
| **Ambiguous goal** | "Users are complaining about performance" |
| **Exploratory idea** | "What if we added social features?" |
| **Multiple interpretations** | "We need better security" |

### 1.2 Invalid Triggers (DO NOT USE)

| Situation | Use Instead |
|-----------|-------------|
| Clear, detailed brief | `epci-0-briefing` directly |
| Technical uncertainty (not functional) | `epci-spike` |
| Production incident | `epci-hotfix` |
| Small, well-defined fix | `epci-micro` |
| Already has acceptance criteria | `epci-0-briefing` |

### 1.3 Decision Rule

```
Is the request clear enough to write acceptance criteria?
├── YES → Skip discover, go to epci-0-briefing
└── NO  ↓

Does the user know WHAT they want (just not HOW)?
├── YES → Skip discover, go to epci-0-briefing
└── NO  ↓

Is this technical uncertainty (feasibility, approach)?
├── YES → Use epci-spike instead
└── NO  → USE epci-discover ✓
```

---

## 2. Inputs

### 2.1 Minimal Input

`epci-discover` accepts very loose input:

```text
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: <vague description of what user wants>
  CONTEXT: <any context available> (optional)
  CONSTRAINTS: <known constraints> (optional)
```

### 2.2 Example Inputs

**Vague Performance Request:**
```text
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: The app feels slow, users are complaining
  CONTEXT: Booking module, mainly mobile users
  CONSTRAINTS: No budget for infrastructure changes
```

**Unclear Feature Request:**
```text
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: We want something like Airbnb's instant booking
  CONTEXT: Current system requires manual confirmation
```

**Ambiguous Improvement:**
```text
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: Make the admin panel better
```

---

## 3. Workflow Steps

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1        STEP 2        STEP 3        STEP 4               │
│  UNDERSTAND → QUESTION  →   CLARIFY   →   GENERATE             │
│  (parse)     (socratic)    (iterate)     (brief)               │
└─────────────────────────────────────────────────────────────────┘
                    │
                    │ Max 3 rounds
                    │
                    ▼
            ┌───────────────┐
            │ EPCI_READY_   │
            │ BRIEF         │
            └───────────────┘
```

### 3.2 Step 1 — Understand the Raw Request

**Objective**: Parse what little information is available.

**Actions**:
1. Identify the core intent (what problem? what desire?)
2. Note what's explicitly stated vs assumed
3. Identify the biggest gaps in understanding
4. Categorize the request type

**Request Categories**:

| Category | Indicators | Question Focus |
|----------|------------|----------------|
| **Performance** | "slow", "fast", "optimize" | Metrics, targets, scope |
| **New Feature** | "add", "new", "want", "like X" | User value, scope, priority |
| **Bug/Issue** | "broken", "wrong", "doesn't work" | Reproduction, impact, urgency |
| **Improvement** | "better", "improve", "enhance" | Current pain, desired state |
| **Refactoring** | "clean up", "reorganize", "technical debt" | Goals, constraints, risk tolerance |

### 3.3 Step 2 — Socratic Questioning

**Objective**: Ask targeted questions to fill knowledge gaps.

**Question Categories**:

#### Business/Value Questions
- What problem does this solve for users?
- Who are the primary users affected?
- What's the business impact of not doing this?
- How will we measure success?

#### Scope Questions
- What's explicitly IN scope?
- What's explicitly OUT of scope?
- Is this a one-time fix or ongoing capability?
- Are there related features we should consider?

#### Constraint Questions
- What's the timeline expectation?
- Are there budget constraints?
- Technical constraints (legacy systems, integrations)?
- Compliance or regulatory requirements?

#### Priority Questions
- How urgent is this?
- What happens if we delay?
- Are there dependencies blocking other work?
- Is this a must-have or nice-to-have?

### 3.4 Step 3 — Clarify Through Iteration

**Objective**: Refine understanding through dialogue.

**Rules**:
- Maximum **3 rounds** of questions
- Each round: 3-5 questions maximum
- Prioritize questions by impact on scope/approach
- Accept "I don't know" as valid — document as assumption

**Iteration Flow**:

```
Round 1: High-level questions (goal, users, value)
    ↓
Round 2: Scope and constraints (boundaries, limitations)
    ↓
Round 3: Details and edge cases (specific behaviors)
    ↓
STOP: Generate brief with documented assumptions
```

### 3.5 Step 4 — Generate EPCI_READY_BRIEF

**Objective**: Produce a structured brief ready for EPCI workflow.

**Output**: Complete `EPCI_READY_BRIEF` with:
- Clear title and slug
- Well-defined objective
- Functional requirements (even if high-level)
- Acceptance criteria (even if preliminary)
- Documented assumptions (marked clearly)

---

## 4. Question Templates by Category

### 4.1 Performance Discovery

```markdown
## Performance Discovery Questions

### Round 1: Understanding the Problem
1. Which specific part of the app feels slow? (page, action, flow?)
2. How do users describe the slowness? (seconds? timeouts? freezing?)
3. When did this start? (always? after a change? under load?)

### Round 2: Defining Success
4. What response time would be acceptable? (< 1s? < 200ms?)
5. How many users are affected? (all? subset? specific conditions?)
6. Is this impacting business metrics? (conversions? complaints?)

### Round 3: Constraints
7. Can we change the database schema?
8. Is caching an option?
9. What's the timeline for this fix?
```

### 4.2 New Feature Discovery

```markdown
## New Feature Discovery Questions

### Round 1: User Value
1. Who will use this feature? (role, frequency, context)
2. What problem does it solve for them?
3. How do they solve this problem today? (workaround?)

### Round 2: Scope
4. What's the minimum viable version of this feature?
5. What's explicitly NOT part of this feature?
6. Are there similar features elsewhere we should integrate with?

### Round 3: Details
7. What happens in edge cases? (errors, empty states, limits)
8. Are there permission/access requirements?
9. Mobile/desktop specific considerations?
```

### 4.3 Bug/Issue Discovery

```markdown
## Bug Discovery Questions

### Round 1: Reproduction
1. How do you reproduce the issue? (steps)
2. Does it happen every time or intermittently?
3. When did it start? (version, date, event)

### Round 2: Impact
4. How many users are affected?
5. Is there a workaround?
6. What's the business impact? (revenue, reputation)

### Round 3: Context
7. Any recent changes to this area?
8. Any error messages or logs available?
9. Environment specific? (browser, device, region)
```

### 4.4 Improvement Discovery

```markdown
## Improvement Discovery Questions

### Round 1: Current State
1. What specifically is wrong with the current state?
2. Who is most affected by the current limitations?
3. How long has this been a pain point?

### Round 2: Desired State
4. What would "better" look like concretely?
5. How will we know the improvement is successful?
6. Are there examples (competitors, other products) to reference?

### Round 3: Approach
7. Is this a UX improvement, technical improvement, or both?
8. Are there quick wins vs long-term improvements?
9. Any constraints on how we can change things?
```

### 4.5 Refactoring Discovery

```markdown
## Refactoring Discovery Questions

### Round 1: Goals
1. What's the primary goal? (maintainability, performance, testability)
2. What pain is the current code causing?
3. Is this blocking other work?

### Round 2: Scope
4. Which specific modules/files are in scope?
5. Should behavior change or stay exactly the same?
6. What's the test coverage currently?

### Round 3: Risk
7. What's the risk tolerance? (production critical? low traffic?)
8. Can we do this incrementally or all-at-once?
9. Who needs to review/approve changes?
```

---

## 5. Output Format

### 5.1 Discovery Output Template

```markdown
## 1. Request Understanding

### Original Request
> <verbatim quote of the original request>

### Interpreted Intent
<1-2 sentence summary of what user actually wants>

### Category
<Performance | New Feature | Bug | Improvement | Refactoring>

### Knowledge Gaps Identified
- Gap 1: ...
- Gap 2: ...
- Gap 3: ...

---

## 2. Discovery Questions

### Round 1
1. <question>
2. <question>
3. <question>

*(Answers received: ...)*

### Round 2 (if needed)
1. <question>
2. <question>

*(Answers received: ...)*

---

## 3. Findings Summary

### Confirmed Facts
- <fact 1>
- <fact 2>

### Assumptions Made
- [ASSUMPTION] <assumption 1> — to be validated
- [ASSUMPTION] <assumption 2> — to be validated

### Out of Scope (confirmed)
- <item 1>
- <item 2>

---

## 4. Generated EPCI_READY_BRIEF

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: <derived title>
  FEATURE_SLUG: <kebab-case-slug>
  OBJECTIVE: <clear objective>
  CONTEXT: <ticket, module, background>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ...
  CONSTRAINTS: <confirmed constraints>
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS:
    - [ASSUMPTION] ...
```

---

## 5. Routing Recommendation

- Estimated complexity: **TINY / SMALL / STANDARD / LARGE**
- Recommended workflow: **epci-micro / epci-soft / epci-1-analyse**
- Confidence: **High / Medium / Low**
- Reason: <brief explanation>

### Next Command

```text
<recommended command>
FEATURE_SLUG=<slug>
$ARGUMENTS=<EPCI_READY_BRIEF above>
```

---

## 6. Open Questions (if any)

*(Questions that couldn't be answered but don't block progress)*

1. <question>
2. <question>
```

---

## 6. Flags Available

### 6.1 `--quick`

Skip detailed questioning, generate brief with more assumptions.

```bash
epci-discover --quick
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: Make the checkout faster

# Output: Brief with [ASSUMPTION] tags for unknowns
```

### 6.2 `--deep`

Extra thorough discovery, up to 5 rounds of questions.

```bash
epci-discover --deep
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: Redesign the entire booking flow

# Output: Comprehensive brief after detailed exploration
```

### 6.3 `--context <path>`

Load project context to inform questions.

```bash
epci-discover --context src/Booking/
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: Improve the booking confirmation

# Claude reads the Booking module to ask more relevant questions
```

---

## 7. Integration with EPCI Workflow

### 7.1 Position in Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                            │
│                    (vague, unclear, incomplete)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Is it clear?   │
                    └────────┬────────┘
                             │
              NO ────────────┼──────────── YES
               │             │               │
               ▼             │               ▼
      ┌─────────────────┐    │    ┌─────────────────────┐
      │  epci-discover  │    │    │  epci-0-briefing    │
      │                 │    │    │  (standard entry)   │
      │  Clarify →      │    │    └─────────────────────┘
      │  Generate brief │    │
      └────────┬────────┘    │
               │             │
               ▼             │
      ┌─────────────────┐    │
      │ EPCI_READY_BRIEF│────┘
      └────────┬────────┘
               │
               ▼
      ┌─────────────────────┐
      │  epci-0-briefing    │
      │  (or direct route)  │
      └─────────────────────┘
               │
               ▼
          Standard EPCI
```

### 7.2 Direct Routing Option

If discovery produces a very clear brief, it can **skip EPCI-0** and route directly:

```markdown
## Routing Recommendation

Brief is comprehensive and validated.

**Direct routing available:**
- For TINY → `epci-micro`
- For SMALL → `epci-soft`
- For STANDARD/LARGE → `epci-1-analyse`

**Or standard routing:**
- `epci-0-briefing` for additional validation
```

---

## 8. Constraints & Boundaries

### 8.1 What epci-discover MUST Do

1. ✅ Parse and understand the vague request
2. ✅ Ask targeted clarifying questions (max 3 rounds)
3. ✅ Document assumptions explicitly
4. ✅ Generate a structured `EPCI_READY_BRIEF`
5. ✅ Provide routing recommendation
6. ✅ Identify what's still unknown

### 8.2 What epci-discover MUST NOT Do

1. ❌ Explore the codebase
2. ❌ Design technical solutions
3. ❌ Write any code
4. ❌ Make architectural decisions
5. ❌ Exceed 3 rounds of questions (unless `--deep`)
6. ❌ Generate incomplete briefs without assumptions documented

---

## 9. Recovery — When Things Go Wrong

### 9.1 User Can't Answer Questions

```
IF user repeatedly says "I don't know":
  1. Document as [ASSUMPTION] with reasonable default
  2. Mark assumption for validation in EPCI-0
  3. Reduce scope to what IS known
  4. Generate brief with explicit uncertainty markers
```

### 9.2 Scope Keeps Growing

```
IF scope grows with each answer:
  1. Acknowledge the larger vision
  2. Propose phased approach (Phase 1, 2, 3)
  3. Generate brief for Phase 1 only
  4. Document future phases as follow-ups
```

### 9.3 Request is Actually Technical

```
IF discovery reveals technical uncertainty (not functional):
  1. Note this isn't a discover case
  2. Recommend epci-spike instead
  3. Provide spike brief format
```

---

## 10. Example — Complete Discovery Session

```markdown
## User Input

$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: Users are complaining about the search
  CONTEXT: E-commerce site, product search

---

## 1. Request Understanding

### Original Request
> "Users are complaining about the search"

### Interpreted Intent
User wants to improve the product search functionality based on user complaints.

### Category
**Improvement**

### Knowledge Gaps Identified
- What specifically are users complaining about?
- Is this a performance issue, relevance issue, or UX issue?
- How is success measured?

---

## 2. Discovery Questions

### Round 1

1. What are users specifically complaining about? (slow? wrong results? hard to use?)
2. Do you have examples of searches that don't work well?
3. How many users are affected / how often do you hear complaints?

**Answers received:**
1. "Results are irrelevant - they search for 'red shoes' and get accessories"
2. "Yes, 'running shoes' shows hiking boots first"
3. "About 10 complaints per week, and analytics show high exit rate on search results"

### Round 2

1. Are users expecting exact matches or "smart" fuzzy matching?
2. Is the current search using database LIKE or a search engine (Elasticsearch)?
3. What's the acceptable response time for search?

**Answers received:**
1. "They expect relevant results, not exact. Like Amazon."
2. "Basic SQL LIKE query currently"
3. "Under 500ms ideally"

---

## 3. Findings Summary

### Confirmed Facts
- Search relevance is the main issue (not performance)
- Current implementation uses basic SQL LIKE
- ~10 complaints/week, measurable via exit rate
- Users expect "smart" search like major e-commerce sites

### Assumptions Made
- [ASSUMPTION] Elasticsearch or similar is acceptable solution
- [ASSUMPTION] Budget allows for search infrastructure
- [ASSUMPTION] Product data has good categorization

### Out of Scope (confirmed)
- Search UI redesign (separate initiative)
- Autocomplete/suggestions (future phase)

---

## 4. Generated EPCI_READY_BRIEF

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: Improve Product Search Relevance
  FEATURE_SLUG: search-relevance-improvement
  OBJECTIVE: Replace basic SQL search with relevant, smart product search to reduce user complaints and exit rate
  CONTEXT: E-commerce site, ~10 complaints/week, high exit rate on search results
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] Search returns relevant products based on query intent
    - [FR2] "Red shoes" returns red shoes, not red accessories
    - [FR3] Results ranked by relevance, not just alphabetical
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] Search response time < 500ms
    - [NFR2] Support 1000+ concurrent searches
  CONSTRAINTS: No UI changes in this phase
  ACCEPTANCE_CRITERIA:
    - [AC1] "Running shoes" returns running shoes in top 5 results
    - [AC2] Exit rate on search results page decreases by 20%
    - [AC3] User complaints about search drop to < 3/week
  ASSUMPTIONS:
    - [ASSUMPTION] Elasticsearch is acceptable technology choice
    - [ASSUMPTION] Budget allows for search infrastructure
```

---

## 5. Routing Recommendation

- Estimated complexity: **STANDARD**
- Recommended workflow: **epci-1-analyse → epci-2-code → epci-3-finalize**
- Confidence: **High**
- Reason: Multi-file change (search service, indexing, configuration), requires technical exploration

### Next Command

```text
epci-0-briefing
FEATURE_SLUG=search-relevance-improvement
$ARGUMENTS=<EPCI_READY_BRIEF above>
```

---

## 6. Open Questions

1. Which search technology to use? (Elasticsearch, Algolia, Meilisearch) — to decide in EPCI-1
2. Do we need to re-index all products? — to assess in EPCI-1
```

---

## 11. Summary

`epci-discover` provides:

1. **Pre-briefing clarification** — Transforms vague ideas into structured briefs
2. **Socratic questioning** — Targeted questions by category (Performance, Feature, Bug, etc.)
3. **Assumption documentation** — Explicitly marks what's assumed vs confirmed
4. **EPCI_READY_BRIEF generation** — Output ready for standard EPCI workflow
5. **Routing recommendation** — Suggests next command and complexity

Use `epci-discover` when requests are unclear, then flow into the standard EPCI workflow with a solid foundation.

---

*This document is part of the EPCI v2.7 workflow system.*
