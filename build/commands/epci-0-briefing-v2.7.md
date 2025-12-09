# epci-0-briefing — EPCI Entry Point: Briefing, Complexity & Routing (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> `epci-0-briefing` is the **entry point** of the EPCI workflow.  
> It clarifies the request, builds a functional brief, evaluates complexity, and routes to the right workflow (Micro / Soft / Full).

> 💡 **Recommended:** Activate **extended thinking** (use "think harder") for this step to improve analysis quality.
>
> **Thinking mode hierarchy:** think < think hard < think harder < ultrathink
> Each level allocates progressively more thinking budget. For EPCI-0 briefing, "think harder" is recommended.

---

## Critical Rules

- ⚠️ `epci-0-briefing` does NOT explore the codebase — that's for downstream commands
- ⚠️ Phase A (INTERACTIVE) = NO file writes
- ⚠️ Phase B = Write ONLY after human validation
- ⚠️ Always validate FEATURE_SLUG before proceeding
- ⚠️ Always end with QUESTIONS & SUGGESTIONS block
- ⚠️ If request is unclear/vague, recommend `epci-discover` first (v2.7)

---

## Supported Flags (v2.7)

| Flag | Effect | Default |
|------|--------|---------|
| `--preview` | Show what would be done without writing Feature Document | Off |
| `--uc` | Ultra-compressed output (~70% reduction) | Off |
| `--verbose` | Maximum detail in analysis and questions | Off |
| `--introspect` | Show decision-making process for complexity/routing | Off |

**Usage examples:**

```bash
epci-0-briefing --introspect
epci-0-briefing --uc --preview
epci-0-briefing --verbose
```

**Flag effects by phase:**

| Flag | Phase A Effect | Phase B Effect |
|------|----------------|----------------|
| `--preview` | Shows analysis | Skips Feature Document write |
| `--uc` | Compressed output | Compressed brief |
| `--verbose` | Detailed analysis, more questions | Full brief details |
| `--introspect` | Shows complexity reasoning | Shows routing logic |

> **Note:** For complete flags documentation, see `epci-flags.md`.

---

## Supported Personas (v2.7)

Personas can be **suggested** during EPCI-0 based on keyword detection. The actual persona activation happens in downstream commands (EPCI-1, EPCI-2, EPCI-3).

| Persona | Flag | Auto-suggestion Triggers |
|---------|------|--------------------------|
| **Architect** | `--persona-architect` | LARGE complexity, "architecture", "refactor", "modular" |
| **Security** | `--persona-security` | "auth", "login", "password", "token", "permission", "encrypt" |
| **Performance** | `--persona-performance` | "slow", "optimize", "performance", "cache", "latency" |
| **QA** | `--persona-qa` | "test", "coverage", "quality", "validation" |
| **Frontend** | `--persona-frontend` | "component", "UI", "React", "Vue", "CSS", "form" |
| **Backend** | `--persona-backend` | "API", "endpoint", "database", "service", "repository" |
| **DevOps** | `--persona-devops` | "deploy", "CI", "pipeline", "Docker", "infrastructure" |

**Behaviour:**

1. EPCI-0 **detects keywords** in the raw brief
2. EPCI-0 **suggests** relevant personas in the routing recommendation
3. User can **accept or override** the suggestion
4. Actual activation happens in downstream commands with `--persona-*` flag

**Example output:**

```markdown
## 4. Complexity & Workflow Recommendation

- Estimated complexity: **STANDARD**
- Recommended workflow: **epci-1-analyse → epci-2-code → epci-3-finalize**
- **Suggested personas:** `--persona-security` (detected: "authentication", "JWT", "password")

### Next command

epci-1-analyse --persona-security
FEATURE_SLUG=user-authentication
...
```

> **Note:** For complete personas documentation, see `epci-personas.md`.

---

## Pre-routing: When to Use epci-discover (v2.7)

Before proceeding with `epci-0-briefing`, assess if the request is clear enough.

### Decision Rule

```
Is the request clear enough to write acceptance criteria?
├── YES → Proceed with epci-0-briefing
└── NO  ↓

Does the user know WHAT they want (just not HOW)?
├── YES → Proceed with epci-0-briefing
└── NO  ↓

Is this vague, unclear, or exploratory?
├── YES → Recommend epci-discover first
└── NO  → Proceed with epci-0-briefing
```

### Vague Request Indicators

| Indicator | Example | Action |
|-----------|---------|--------|
| No clear objective | "Make it better" | → `epci-discover` |
| Missing acceptance criteria | "Improve search" | → `epci-discover` |
| Exploratory language | "What if we..." | → `epci-discover` |
| Multiple interpretations | "Users are unhappy" | → `epci-discover` |
| References competitor without specifics | "Like Airbnb does" | → `epci-discover` |

### How to Redirect to Discover

If the request is too vague, output:

```markdown
## Pre-routing Assessment

This request appears to need clarification before proceeding to EPCI workflow.

**Indicators detected:**
- [x] No clear acceptance criteria
- [x] Multiple possible interpretations
- [ ] Exploratory language

**Recommendation:** Use `epci-discover` to clarify requirements first.

### Suggested Command

```text
epci-discover
$ARGUMENTS=<DISCOVERY_REQUEST>
  IDEA: <original vague request>
  CONTEXT: <any context available>
```

After discovery, the generated `EPCI_READY_BRIEF` can be passed to `epci-0-briefing` or routed directly.
```

---

## 1. Purpose & Responsibilities

`epci-0-briefing` is responsible for:

1. **Assessing request clarity** — redirect to `epci-discover` if too vague (v2.7).
2. **Clarifying the incoming request** (ticket, idea, Promptor brief, voice transcript, etc.).
3. **Identifying gaps, ambiguities, risks** and constraints.
4. **Proposing AI-powered improvements** to strengthen the feature (AI suggestions).
5. **Asking targeted clarification questions** to the human.
6. **Validating FEATURE_SLUG** (derive if not provided).
7. **Detecting persona triggers** and suggesting relevant personas (v2.7).
8. **Producing a structured functional brief**, called `EPCI_READY_BRIEF`, which can be passed as `$ARGUMENTS` to:
    - `epci-micro` (TINY),
    - `epci-soft` (SMALL),
    - `epci-1-analyse` (STANDARD / LARGE).
9. **Evaluating the complexity** (TINY / SMALL / STANDARD / LARGE) using a clear reference grid.
10. **Routing explicitly** to **EPCI-Micro**, **EPCI-Soft** or the full EPCI workflow.
11. **Persisting the brief** into a **single Feature Document** in Markdown:
    - `docs/features/<feature-slug>.md`
    - with 3 sections: Functional Brief (EPCI-0), Technical Plan (EPCI-1), Final Report (EPCI-3).

**Important:**

- `epci-0-briefing` **does not explore the codebase** and **does not design the technical implementation** in detail. Those responsibilities belong to `epci-micro`, `epci-soft` or `epci-1-analyse` and the rest of the EPCI workflow.
- `epci-0-briefing` is mainly a **functional scoping + routing + persistence** command.

---

## 2. Inputs & Execution Modes

### 2.1 `$ARGUMENTS` structure

`epci-0-briefing` expects a payload with:

```text
$ARGUMENTS=<RAW_REQUEST>
  TASK: <ticket ID or short label>
  RAW_BRIEF: <raw description of the feature/bug/change>
  FEATURE_TITLE: <human-readable title> (optional, derived if absent)
  FEATURE_SLUG: <kebab-case-slug> (optional, derived if absent)
  EXECUTION_MODE: "INTERACTIVE" | "AUTO" (default: INTERACTIVE)
  FROM_PROMPTOR: true | false (optional)
```

**Field descriptions:**

| Field | Required | Description |
|-------|----------|-------------|
| `TASK` | Yes | Short identifier: ticket ID, short label |
| `RAW_BRIEF` | Yes | Raw description of the feature / bug / change request |
| `FEATURE_TITLE` | Optional | Human-readable title. If absent, derive from `RAW_BRIEF` |
| `FEATURE_SLUG` | Optional | Canonical slug (kebab-case). If absent, derive from title |
| `EXECUTION_MODE` | Optional | `"INTERACTIVE"` (default) or `"AUTO"` |
| `FROM_PROMPTOR` | Optional | `true` if brief comes from Promptor-like pipeline |

### 2.2 Execution modes & phases

`epci-0-briefing` supports **two execution modes** and, for INTERACTIVE, **two phases**.

#### INTERACTIVE mode (default)

- **Phase A — Draft & Questions (NO file writes)**
    
    - Assess request clarity (redirect to `epci-discover` if needed).
    - Clarify and understand the request.
    - Validate FEATURE_SLUG.
    - Detect persona triggers (v2.7).
    - Propose AI suggestions.
    - Ask clarification questions.
    - Build an **initial** `EPCI_READY_BRIEF` (with explicit assumptions).
    - Estimate complexity & propose routing with persona suggestions.
    - **⚠️ Do NOT write or update any file** in Phase A.

- **Phase B — Validation & Persistence**
    
    - Triggered **after**:
        - the human has answered the clarification questions,
        - AI suggestions have been accepted/rejected/amended,
        - the brief is considered "ready".
    - Update the functional brief and regenerate the **final** `EPCI_READY_BRIEF`.
    - Re-assess complexity & routing if needed.
    - **Write or update** the Feature Document in `docs/features/<feature-slug>.md`.

> In INTERACTIVE mode:
> 
> - **Phase A** = analysis + questions, no side effects on the repo.
> - **Phase B** = explicit persistence, only after human validation.

#### AUTO mode

- **Single-pass**: behaves as if Phase A + Phase B were merged.
- Suitable for advanced workflows or scripted usage.
- Behaviour:
    - Assess request clarity first.
    - Ask questions **only if absolutely necessary**.
    - Make **reasonable assumptions**, clearly documented in the brief.
    - Produce final `EPCI_READY_BRIEF`.
    - Decide routing (Micro / Soft / Full) with persona suggestions.
    - **Write or update** the Feature Document in one go.
- AUTO should be used **only** when the environment and calling context are controlled.

### 2.3 Flag Effects on Execution

| Flag | Phase A Effect | Phase B Effect |
|------|----------------|----------------|
| `--preview` | Shows full analysis | Skips Feature Document write |
| `--uc` | Compressed understanding/brief | Compressed final output |
| `--verbose` | Detailed analysis, 10+ questions | Full brief with all details |
| `--introspect` | Shows complexity scoring logic | Shows routing decision process |

---

## 3. Output Layout (assistant message)

For IDE / terminal readability, **both Phase A and Phase B (and AUTO)** MUST follow this **fixed layout**.

**Strict rules:**

- No section before `## 1.` and no section after `QUESTIONS & SUGGESTIONS`

````markdown
## 1. Understanding

### 1.1 Objective
- ...

### 1.2 Feature identification
- Feature title: ...
- Feature slug: `<feature-slug>`

### 1.3 In scope
- ...

### 1.4 Out of scope
- ...

### 1.5 Context & constraints
- ...

### 1.6 Open points / unknowns
- ...

### 1.7 Active Flags & Persona Detection (v2.7)
- Flags: `--introspect`, `--verbose` (if any)
- Persona triggers detected: "authentication", "JWT" → suggests `--persona-security`

---

## 2. Draft — Functional Brief (EPCI-0)

### 2.1 Feature Title
...

### 2.2 Objective
...

### 2.3 Functional Requirements
- [FR1] ...
- [FR2] ...

### 2.4 Non-functional Requirements
- [NFR1] ...
- [NFR2] ...

### 2.5 Constraints & Dependencies
- ...

### 2.6 Acceptance Criteria
- [AC1] ...
- [AC2] ...

### 2.7 Links & References
- Ticket: ...
- Specs: ...

---

## 3. EPCI_READY_BRIEF

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: <title>
  FEATURE_SLUG: <slug>
  OBJECTIVE: <1-3 sentences>
  CONTEXT: <ticket refs, modules, URLs>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ...
  CONSTRAINTS: <technical or business>
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS: <if any, clearly marked>
````

---

## 4. Complexity & Workflow Recommendation

- Estimated complexity: **TINY / SMALL / STANDARD / LARGE**
    
- Rationale:
    
    - ...
    - ...

- Recommended workflow:
    
    - If TINY → **epci-micro**
    - If SMALL → **epci-soft**
    - If STANDARD/LARGE → **epci-1-analyse → epci-2-code → epci-3-finalize**

- **Suggested personas (v2.7):** `--persona-<x>` (based on detected triggers)

### Introspection (if --introspect active)

> 🔍 **Complexity Scoring:**
> - Files estimate: X (SMALL range)
> - LOC estimate: Y (SMALL range)  
> - Risk factors: Z
> - Final score: SMALL (confidence: 85%)
>
> 🎯 **Routing Decision:**
> - Considered: epci-micro (rejected: > 2 files)
> - Selected: epci-soft
>
> 💡 **Persona Suggestion:**
> - Detected keywords: "auth", "login"
> - Suggested: `--persona-security`

### Next command

```text
<command> [--persona-<x>]
FEATURE_SLUG=<feature-slug>
PLAN_PATH=docs/features/<feature-slug>.md
$ARGUMENTS=<EPCI_READY_BRIEF>
```

---

## 5. Feature Document Update (Phase B only)

- Feature slug: `<feature-slug>`
- Feature document: `docs/features/<feature-slug>.md`
- Status: **CREATED** / **UPDATED**

---

## QUESTIONS & SUGGESTIONS

### AI Suggestions (to validate)

1. [AI-suggestion] ...
2. [AI-suggestion] ...
3. ...

### Clarification Questions (to answer)

1. ...
2. ...
3. ...
4. ...
5. ...

````

**Strict rule:** No extra sections before `## 1.` or after `QUESTIONS & SUGGESTIONS`.

---

## 4. Step 1 — Understanding

Section: `## 1. Understanding`

### 4.1 Behaviour

Read `$ARGUMENTS` and restate:

- **Objective** of the feature / bugfix.
- **Scope**: what is explicitly in scope and what is clearly out of scope.
- **Context**: module, domain, ticket, environment.
- **Constraints**: technical, business, UX, performance, regulatory, etc.
- **Open points**: unknowns, contradictions, missing information.
- **Persona triggers** (v2.7): keywords that suggest specific personas.

If `FROM_PROMPTOR = true`:

- Assume the brief has already been structured.
- Focus on detecting gaps and edge cases.
- Fewer questions may be needed.

### 4.2 FEATURE_SLUG Validation

Before proceeding, validate the `FEATURE_SLUG`:

1. Confirm it is in **kebab-case** (lowercase, hyphens only).
2. If not provided, derive from `FEATURE_TITLE`:
    - "Stay Tax Calculation" → `stay-tax-calculation`
3. If `FEATURE_TITLE` is also missing, derive from `RAW_BRIEF` or `TASK`.
4. Confirm the path `docs/features/<feature-slug>.md` is valid.

If invalid, fix it before continuing.

### 4.3 Persona Detection (v2.7)

Scan the `RAW_BRIEF` for keywords that suggest personas:

| Keywords Detected | Suggested Persona |
|-------------------|-------------------|
| auth, login, password, token, permission | `--persona-security` |
| API, endpoint, database, service | `--persona-backend` |
| component, UI, React, Vue, CSS | `--persona-frontend` |
| slow, optimize, cache, performance | `--persona-performance` |
| test, coverage, quality | `--persona-qa` |
| deploy, CI, pipeline, Docker | `--persona-devops` |
| architecture, refactor, modular + LARGE | `--persona-architect` |

Document detected triggers in section `1.7 Active Flags & Persona Detection`.

---

## 5. Step 2 — Draft the Functional Brief

Section: `## 2. Draft — Functional Brief (EPCI-0)`

Build a **draft functional brief** with:

| Subsection | Content |
|------------|---------|
| 2.1 Feature Title | Human-readable title |
| 2.2 Objective | 1–3 sentences: goal + expected outcome |
| 2.3 Functional Requirements | [FR1], [FR2], ... — what the system must do |
| 2.4 Non-functional Requirements | [NFR1], [NFR2], ... — performance, security, etc. |
| 2.5 Constraints & Dependencies | Technical, business, regulatory constraints |
| 2.6 Acceptance Criteria | [AC1], [AC2], ... — testable conditions |
| 2.7 Links & References | Ticket, specs, external docs |

This section is **preliminary** in Phase A. It may be updated after user answers questions.

---

## 6. Step 3 — Produce the EPCI_READY_BRIEF

Section: `## 3. EPCI_READY_BRIEF`

Generate a **structured text block** that downstream commands (`epci-micro`, `epci-soft`, `epci-1-analyse`) can consume as `$ARGUMENTS`.

**Format:**

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: <title>
  FEATURE_SLUG: <slug>
  OBJECTIVE: <1-3 sentences>
  CONTEXT: <ticket refs, modules, URLs>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ...
  CONSTRAINTS: <technical or business>
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS: <if any>
```

In **Phase A** (INTERACTIVE), mark any assumptions clearly:
- `[ASSUMPTION]` prefix for items that need validation.

In **Phase B** (or AUTO), assumptions should be resolved or documented as "accepted".

---

## 7. Step 4 — Complexity & Routing

Section: `## 4. Complexity & Workflow Recommendation`

### 7.1 Complexity Reference Grid

| Level | Files | LOC | Risk | Modules | Workflow |
|-------|-------|-----|------|---------|----------|
| **TINY** | 1 (max 2) | < 50 | Very low | 1 | `epci-micro` |
| **SMALL** | 2–3 | 50–200 | Low | 1 | `epci-soft` |
| **STANDARD** | 3–10 | 200–1000 | Medium | 1–3 | Full EPCI |
| **LARGE** | > 10 | > 1000 | High | > 3 | Full EPCI |

### 7.2 TINY vs SMALL Clarification

**TINY** (epci-micro) applies when ALL of these are true:
- 1 file modified (2 maximum if strictly in same module)
- Total LOC < 50
- No new business logic introduced
- No schema changes
- Very low risk

**SMALL** (epci-soft) applies when ANY of these is true:
- 2–3 files modified
- OR 1 file but 50–200 LOC
- OR new business logic (even simple)
- Low risk, single module

**Ambiguous case (2 files, < 50 LOC):**
- If no new logic → TINY (use `epci-micro`)
- If new logic introduced → SMALL (use `epci-soft`)

### 7.3 Routing with Persona Suggestions (v2.7)

The routing recommendation should include:

1. **Complexity level** (TINY / SMALL / STANDARD / LARGE)
2. **Recommended workflow** (epci-micro / epci-soft / full EPCI)
3. **Suggested personas** based on detected triggers
4. **Complete next command** with optional persona flag

**Example:**

```markdown
- Estimated complexity: **STANDARD**
- Recommended workflow: **epci-1-analyse → epci-2-code → epci-3-finalize**
- **Suggested personas:** `--persona-security` (detected: "authentication", "JWT")

### Next command

```text
epci-1-analyse --persona-security
FEATURE_SLUG=user-authentication
PLAN_PATH=docs/features/user-authentication.md
$ARGUMENTS=<EPCI_READY_BRIEF>
```
```

### 7.4 Introspection Output (v2.7)

If `--introspect` flag is active, add an introspection block showing the reasoning:

```markdown
### Introspection (--introspect)

> 🔍 **Complexity Scoring:**
> - Files estimate: 5-8 files (STANDARD range)
> - LOC estimate: 300-500 (STANDARD range)
> - Risk factors: authentication = high sensitivity
> - Modules: 2 (Auth, User)
> - Final: STANDARD (confidence: 82%)
>
> 🎯 **Routing Decision:**
> - Considered: epci-soft (rejected: > 3 files, new business logic)
> - Considered: epci-micro (rejected: multiple modules)
> - Selected: Full EPCI (epci-1-analyse)
>
> 💡 **Persona Detection:**
> - Keywords found: "JWT", "authentication", "login", "password"
> - Security score: 0.85
> - Suggested: `--persona-security`
```

---

## 8. Step 5 — Feature Document Persistence

Section: `## 5. Feature Document Update`

### 8.1 When to Write

| Mode | Phase | Write Feature Document? |
|------|-------|------------------------|
| INTERACTIVE | Phase A | ❌ NO |
| INTERACTIVE | Phase B | ✅ YES |
| AUTO | — | ✅ YES |
| Any + `--preview` | — | ❌ NO (preview only) |

### 8.2 Feature Document Structure

Create or update the file at `docs/features/<feature-slug>.md` with:

```markdown
# <Feature Title>

## 1. Functional Brief — EPCI-0

*(This section is managed by `epci-0-briefing`. Do not modify manually.)*

### Objective
...

### Functional Requirements
- [FR1] ...
- [FR2] ...

### Non-functional Requirements
- [NFR1] ...

### Constraints & Dependencies
...

### Acceptance Criteria
- [AC1] ...
- [AC2] ...

### Links & References
- Ticket: ...
- Specs: ...

---

## 2. Technical Plan — EPCI-1

*(This section is managed by `epci-1-analyse`. Do not modify manually.)*

*(To be filled during EPCI-1.)*

---

## 3. Final Report — EPCI-3

*(This section is managed by `epci-3-finalize`. Do not modify manually.)*

*(To be filled during EPCI-3.)*
```

### 8.3 Rules

- Only modify `## 1. Functional Brief — EPCI-0`.
- Never touch `## 2. Technical Plan` or `## 3. Final Report`.
- If the file exists, only update section 1.
- If the file doesn't exist, create it with the full skeleton.

---

## 9. Questions & Suggestions Guidelines

Section: `## QUESTIONS & SUGGESTIONS`

### 9.1 AI Suggestions Guidelines

Provide **2–5 AI suggestions** that could strengthen the feature:

| Category | Examples |
|----------|----------|
| **Functionality** | "Add audit logging for compliance" |
| **UX** | "Show warning before destructive action" |
| **Performance** | "Cache results to reduce DB load" |
| **Security** | "Add rate limiting to prevent abuse" |
| **Maintainability** | "Extract into reusable service" |

**Suggestion quality guidelines:**

- Be **concrete** and **actionable** — not vague.
- Explain **why** it would help (briefly).
- Mark as `[AI-suggestion]` prefix.
- Order by impact (most impactful first).

### 9.2 Clarification Questions Guidelines

Ask **5–10 clarification questions**, grouped by theme where relevant:

| Theme | Example Questions |
|-------|-------------------|
| **Business / Functional** | What happens if X? Should Y be allowed? |
| **Data / API contracts** | What format for the response? Which fields are required? |
| **UX / UI / Edge cases** | What message on error? What if the list is empty? |
| **Security / Performance** | Who can access this? Any rate limits? |
| **Dependencies / Rollout** | Any migration needed? Feature flag required? |

**Question quality guidelines:**

- Be **specific** and **concrete** — avoid vague questions.
- Avoid yes/no questions unless they unlock a major decision.
- Prioritise questions that **change the implementation or risk profile**.
- Group related questions together for easier answering.
- Order from most critical to least critical.

Example prompt to the user (in narrative text, before the final block):

> Please answer the clarification questions below and confirm AI suggestions.
> Once validated, I will proceed to Phase B (persistence) or you can run the next EPCI command with the EPCI_READY_BRIEF.

---

## 10. Example — EPCI-0 Session (Phase A)

Below is a **complete example** of an `epci-0-briefing` Phase A session.

````markdown
## 1. Understanding

### 1.1 Objective
- Add validation to prevent bookings longer than 30 days for standard rentals

### 1.2 Feature identification
- Feature title: Max stay length validation
- Feature slug: `max-stay-length-validation`

### 1.3 In scope
- Validation logic in booking service
- User-facing error message
- Unit tests

### 1.4 Out of scope
- Admin override functionality
- Historical bookings
- Premium rentals (different rules)

### 1.5 Context & constraints
- Module: Booking
- Ticket: BOOK-1234
- Constraint: Must not affect premium rentals

### 1.6 Open points / unknowns
- Should the limit be configurable?
- What exact error message wording?

### 1.7 Active Flags & Persona Detection (v2.7)
- Flags: None active
- Persona triggers detected: "validation", "booking" → suggests `--persona-backend`

---

## 2. Draft — Functional Brief (EPCI-0)

### 2.1 Feature Title
Max stay length validation

### 2.2 Objective
Prevent standard rental bookings longer than 30 consecutive days to comply with local regulations.

### 2.3 Functional Requirements
- [FR1] Reject bookings > 30 days for standard rentals
- [FR2] Display clear error message to user
- [FR3] Allow bookings of exactly 30 days

### 2.4 Non-functional Requirements
- [NFR1] Validation must complete in < 50ms
- [NFR2] Error message must be translatable

### 2.5 Constraints & Dependencies
- Must not affect premium rentals
- Must not affect admin booking creation

### 2.6 Acceptance Criteria
- [AC1] 31-day booking rejected with correct message
- [AC2] 30-day booking accepted
- [AC3] Premium 45-day booking accepted

### 2.7 Links & References
- Ticket: BOOK-1234
- Regulation: Local housing law §12.3

---

## 3. EPCI_READY_BRIEF (initial draft)

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: Max stay length validation
  FEATURE_SLUG: max-stay-length-validation
  OBJECTIVE: Prevent standard rental bookings > 30 days to comply with local regulations
  CONTEXT: Ticket BOOK-1234, Booking module
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] Reject bookings > 30 days for standard rentals
    - [FR2] Display clear error message
    - [FR3] Allow exactly 30 days
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] Validation < 50ms
  CONSTRAINTS: Must not affect premium rentals or admin bookings
  ACCEPTANCE_CRITERIA:
    - [AC1] 31-day booking rejected
    - [AC2] 30-day booking accepted
    - [AC3] Premium 45-day accepted
  ASSUMPTIONS:
    - [ASSUMPTION] Limit is hardcoded (not configurable) — to confirm
````

---

## 4. Complexity & Workflow Recommendation

- Estimated complexity: **SMALL**
- Rationale:
  - Files: ~3 (service, controller, tests)
  - LOC: ~100
  - Risk: Low (isolated validation)
  - Modules: 1 (Booking)

- Recommended workflow: **epci-soft**
- **Suggested personas:** `--persona-backend` (detected: "booking", "validation")

### Next command

```text
epci-soft --persona-backend
FEATURE_SLUG=max-stay-length-validation
PLAN_PATH=docs/features/max-stay-length-validation.md
$ARGUMENTS=<EPCI_READY_BRIEF above>
```

---

## QUESTIONS & SUGGESTIONS

### AI Suggestions (to validate)

1. [AI-suggestion] Add a configuration parameter for the 30-day limit to allow easy adjustment without code changes.
2. [AI-suggestion] Log validation failures for monitoring and analytics.
3. [AI-suggestion] Consider adding a warning at 25+ days instead of only blocking at 31+.

### Clarification Questions (to answer)

1. Should the 30-day limit be configurable via admin panel or environment variable?
2. What exact error message should be displayed? (Please provide French and English versions)
3. Should we log failed validation attempts for analytics?
4. Are there any other rental types besides "standard" and "premium" that need different limits?
5. Should the validation apply to booking modifications as well as new bookings?

> ⚠️ **Phase A — No files written yet.**
> Please answer the clarification questions and confirm AI suggestions.
> Once validated, I will proceed to Phase B to persist the Feature Document.
````

---

## 11. Example — EPCI-0 Session (Phase B)

After the user answers questions and validates:

````markdown
## 1. Understanding

*(Same as Phase A, with open points resolved)*

### 1.6 Open points / unknowns
- ✅ Limit will be hardcoded (confirmed)
- ✅ Error message: "Maximum stay length is 30 days"

### 1.7 Active Flags & Persona Detection (v2.7)
- Flags: None active
- Persona triggers: "booking", "validation" → `--persona-backend` confirmed

---

## 2. Draft — Functional Brief (EPCI-0)

*(Updated with user answers)*

### 2.3 Functional Requirements
- [FR1] Reject bookings > 30 days for standard rentals
- [FR2] Display error: "Maximum stay length is 30 days"
- [FR3] Allow bookings of exactly 30 days
- [FR4] Log validation failures *(accepted AI suggestion)*

---

## 3. EPCI_READY_BRIEF (final, validated)

```text
EPCI_READY_BRIEF:
  FEATURE_TITLE: Max stay length validation
  FEATURE_SLUG: max-stay-length-validation
  OBJECTIVE: Prevent standard rental bookings > 30 days
  CONTEXT: Ticket BOOK-1234, Booking module
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] Reject bookings > 30 days for standard rentals
    - [FR2] Display translated error message
    - [FR3] Allow exactly 30 days
    - [FR4] Log validation failures
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] Validation < 50ms
  CONSTRAINTS: Must not affect premium rentals or admin bookings
  ACCEPTANCE_CRITERIA:
    - [AC1] 31-day booking rejected with correct message
    - [AC2] 30-day booking accepted
    - [AC3] Premium 45-day accepted
    - [AC4] Failed validations logged
  ASSUMPTIONS: None
````

---

## 4. Complexity & Workflow Recommendation

- Estimated complexity: **SMALL**
- Recommended workflow: **epci-soft**
- **Suggested personas:** `--persona-backend`

### Next command

```text
epci-soft --persona-backend
FEATURE_SLUG=max-stay-length-validation
PLAN_PATH=docs/features/max-stay-length-validation.md
$ARGUMENTS=<EPCI_READY_BRIEF above>
```

---

## 5. Feature Document Update

- Feature slug: `max-stay-length-validation`
- Feature document: `docs/features/max-stay-length-validation.md`
- Status: **CREATED** ✅

> ⚠️ **Phase B — Feature Document written.**
> You can now run the suggested next command.
````

---

## 12. Summary

This `epci-0-briefing` specification (v2.7):

- Keeps the original strengths:
    
    - INTERACTIVE vs AUTO modes,
    - Phase A (no write) / Phase B (write) safety,
    - clear QUESTIONS & SUGGESTIONS block,
    - strong functional scoping and AI assistance.

- Aligns with the **EPCI v2.7 goals**:
    
    - Single Feature Document per feature (English sections),
    - Explicit routing to **Micro / Soft / Full**,
    - Numeric complexity thresholds with TINY/SMALL clarification,
    - Explicit "Next command" suggestion with complete parameters,
    - Clear separation of responsibilities between EPCI-0 and downstream commands,
    - Unified `EPCI_READY_BRIEF` format across all commands.

- Adds **v2.7 improvements**:
    
    - **Pre-routing to epci-discover** for vague/unclear requests,
    - **Universal flags support** (`--preview`, `--uc`, `--verbose`, `--introspect`),
    - **Persona detection and suggestion** based on keyword triggers,
    - **Introspection output** showing complexity/routing reasoning,
    - Enhanced output layout with flags and persona sections,
    - Links to new reference documentation (epci-flags.md, epci-personas.md, epci-discover.md).

- Preserves **previous improvements**:
    
    - Thinking mode hierarchy documented (think < think hard < think harder < ultrathink),
    - Enhanced AI Suggestions guidelines (2-5 concrete, actionable),
    - Enhanced Clarification Questions guidelines (5-10, grouped by theme),
    - All sections in English (Functional Brief, Technical Plan, Final Report),
    - Consolidated critical rules at top.

It is **self-contained**, ready to be used as the reference for the EPCI-0 command in your workflow.

---

## 13. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-discover.md` | Pre-briefing discovery for vague requests |
| `epci-flags.md` | Universal flags reference |
| `epci-personas.md` | Expert personas system |
| `epci-workflow-guide.md` | Complete workflow documentation |

---

*This document is part of the EPCI v2.7 workflow system.*
