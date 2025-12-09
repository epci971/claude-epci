# epci-1-analyse — Explore & Plan (Full EPCI Workflow) (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> `epci-1-analyse` is the **first step** of the full EPCI workflow for **STANDARD** and **LARGE** changes.
> 
> This command is **read-only**: it explores the codebase and produces a detailed implementation plan.  
> It does **NOT** write any implementation code.

> 💡 **Recommended:** Activate **think hard** mode for this step to improve technical analysis quality.
>
> **Thinking mode hierarchy:** think < think hard < think harder < ultrathink
> For complex architecture decisions, consider "think harder" or "ultrathink".

---

## Critical Rules

- ⚠️ `epci-1-analyse` is strictly READ-ONLY — no implementation code
- ⚠️ Phase A (INTERACTIVE) = NO file writes, wait for validation
- ⚠️ ONLY update `## 2. Technical Plan` in the Feature Document
- ⚠️ NEVER modify `## 1. Functional Brief` or `## 3. Final Report`
- ⚠️ No section before `## 1.` and no section after `## 6.`

---

## Supported Flags (v2.7)

| Flag | Effect | Default |
|------|--------|---------|
| `--preview` | Show what would be planned without writing | Off |
| `--dry-run` | Simulate the entire workflow | Off |
| `--uc` | Ultra-compressed output (~70% reduction) | Off |
| `--verbose` | Maximum detail in exploration | Off |
| `--introspect` | Show decision-making process | Off |

**Usage example:**
```bash
epci-1-analyse --persona-architect --introspect
epci-1-analyse --uc --preview
```

---

## Supported Personas (v2.7)

| Persona | Flag | Best For | Auto-triggers |
|---------|------|----------|---------------|
| **Architect** | `--persona-architect` | System design, patterns | LARGE complexity |
| **Security** | `--persona-security` | Auth, vulnerabilities | auth/, security/, crypto/ |
| **Performance** | `--persona-performance` | Optimization, profiling | "optimize", "slow", "cache" |
| **QA** | `--persona-qa` | Testing strategy | tests/, "coverage" |
| **Frontend** | `--persona-frontend` | UI/UX, components | .tsx, .jsx, components/ |
| **Backend** | `--persona-backend` | API, databases | Controller, Service, Repository |
| **DevOps** | `--persona-devops` | CI/CD, deployment | Dockerfile, .yml, deploy |

**Auto-activation:** Personas are automatically suggested based on detected patterns. You can override with explicit flags.

---

## 1. Purpose & Responsibilities

`epci-1-analyse` is responsible for:

1. **Exploring the codebase** (read-only) to understand:
    
    - the current architecture and patterns,
    - the files that will be impacted,
    - the constraints and invariants to respect.

2. **Producing a detailed implementation plan** that will guide `epci-2-code`:
    
    - scope & goal,
    - file-by-file changes,
    - control & data flow,
    - edge cases & error handling,
    - testing strategy,
    - implementation checklist.

3. **Updating the Feature Document** (`docs/features/<feature-slug>.md`):
    
    - populate **only** the `## 2. Technical Plan — EPCI-1` section with the full plan.

4. **Suggesting the next command** (`epci-2-code`) with explicit parameters.

**Critical constraints:**

- `epci-1-analyse` **MUST NOT write any implementation code**.
- `epci-1-analyse` **MUST NOT modify any source files** (only the Feature Document).
- `epci-1-analyse` **MUST NOT run tests** (that's `epci-2-code`'s job).
- `epci-1-analyse` **MUST NOT modify `## 1. Functional Brief` or `## 3. Final Report`** sections of the Feature Document.

---

## 2. Inputs & Modes

### 2.1 `$ARGUMENTS`

`epci-1-analyse` is typically called with the `EPCI_READY_BRIEF` produced by `epci-0-briefing`.

```text
$ARGUMENTS=<EPCI_READY_BRIEF>
  FEATURE_TITLE: <human-readable title of the feature>
  FEATURE_SLUG: <kebab-case-slug>
  OBJECTIVE: <concise description of the goal>
  CONTEXT: <ticket refs, modules, URLs>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ... (optional)
  CONSTRAINTS: <technical or business constraints> (optional)
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS: <if any>
```

If `FEATURE_SLUG` is not provided, derive it from `FEATURE_TITLE`:

- lowercase,
- kebab-case (e.g. "Stay tax calculation" → `stay-tax-calculation`).

### 2.2 Execution modes & phases

`epci-1-analyse` supports `EXECUTION_MODE`:

- `"INTERACTIVE"` (default):
    
    - **Phase A — Explore & Draft (read-only, NO file writes)**:
        - Explore the codebase using repo tools.
        - Produce an exploration summary.
        - Draft the detailed plan.
        - Present everything for user review.
        - **⚠️ STOP HERE. Do NOT write any files. Wait for user validation.**
    
    - **Phase B — Persist (after explicit user validation)**:
        - User confirms the plan is correct.
        - **Only then**, write the plan to the Feature Document.
        - Suggest the next command.

- `"AUTO"`:
    
    - Single-pass, self-validated workflow.
    - Explore → Plan → Write Feature Document in one go.
    - **All assumptions MUST be explicitly documented** in the output.
    - Use AUTO only when the context is controlled and the task is clearly scoped.

> **Read-only guarantee:**  
> In both modes, `epci-1-analyse` never writes implementation code.  
> It only updates the Feature Document with the plan (in Phase B for INTERACTIVE).

### 2.3 Flag Effects

| Flag | Phase A Effect | Phase B Effect |
|------|----------------|----------------|
| `--preview` | Shows planned changes | Skips file writes |
| `--dry-run` | Full simulation | No actual changes |
| `--uc` | Compressed exploration output | Compressed plan |
| `--verbose` | Detailed file analysis | Full plan details |
| `--introspect` | Shows reasoning for file selection | Shows planning logic |

---

## 3. Output Layout (assistant message)

For IDE / terminal readability, `epci-1-analyse` MUST follow this **fixed layout**.

````markdown
## 1. Understanding & Scope

... short restatement of the brief and constraints ...

### Active Persona (v2.7)
- Persona: <name> (if activated)
- Reason: <why this persona was selected/auto-activated>

### Active Flags (v2.7)
- Flags: <list of active flags>

---

## 2. Explore — Codebase Analysis

### 2.1 Key files & directories
- `path/to/file1` — <role, why it matters>
- `path/to/file2` — <role, why it matters>
- ...

### 2.2 Existing patterns to respect
- Architecture: ...
- Naming conventions: ...
- Error handling: ...
- Logging: ...
- Testing: ...

### 2.3 Constraints & invariants
- ...

### 2.4 Obvious risks / couplings
- ...

### 2.5 Introspection (if --introspect)
> 🔍 **Decision Logic:**
> - Selected files because: ...
> - Identified patterns by: ...
> - Risk assessment based on: ...

---

## 3. Plan — Detailed Implementation Plan (EPCI-1)

### 3.1 Scope & Goal
... (1–2 paragraphs) ...

### 3.2 Context & Key Files
... (recap from Explore) ...

### 3.3 Proposed Changes (file by file)

| File | Change type | Description |
|------|-------------|-------------|
| `src/...` | modify | ... |
| `src/...` | new | ... |
| `tests/...` | new | ... |

### 3.4 Control & Data Flow
... (entry points, data movement, error propagation) ...

### 3.5 Edge Cases & Error Handling
- Edge case 1: ... → behaviour: ...
- Edge case 2: ... → behaviour: ...
- ...

### 3.6 Testing Strategy
- Unit tests: ...
- Integration tests: ...
- E2E tests (if applicable): ...

### 3.7 Documentation & ADRs
- README: ...
- Changelog: ...
- API docs: ...
- ADRs: ...

### 3.8 Assumptions & Open Questions
- Assumption 1: ...
- Assumption 2: ...
- Open question 1: ...

### 3.9 Implementation Checklist

- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...
- [ ] Step 4: ...
- ...

### 3.10 Confidence & Risks
- Confidence: X%
- Top risks:
  1. ...
  2. ...
  3. ...

### 3.11 Persona Recommendations (v2.7)
> 💡 **For epci-2-code, consider:**
> - `--persona-<x>` because: ...
> - `--validate` because: ...

---

## 4. Assumptions (AUTO mode only)

> This section is **mandatory in AUTO mode** and optional in INTERACTIVE mode.

- Assumption A: ...
- Assumption B: ...
- Assumption C: ...

If any assumption is incorrect, the plan may need revision.

---

## 5. Feature Document Update

- Feature slug: `<feature-slug>`
- Feature document: `docs/features/<feature-slug>.md`
- Section updated: `## 2. Technical Plan — EPCI-1`

> ⚠️ **Sections `## 1. Functional Brief` and `## 3. Final Report` are NOT modified.**

---

## 6. Next Command

```text
To continue with implementation and tests, run:

epci-2-code
FEATURE_SLUG=<feature-slug>
PLAN_PATH=docs/features/<feature-slug>.md
$ARGUMENTS=<EPCI_READY_BRIEF or brief summary>

Recommended flags: --validate
Recommended persona: --persona-<x> (based on analysis)
````

The plan is available in: `docs/features/<feature-slug>.md` (section "2. Technical Plan — EPCI-1").

````

**Strict rule:** No extra sections before `## 1.` or after `## 6.`.

---

## 4. Behaviour Step-by-step

### 4.1 Step 1 — Understanding & Scope

- Read `$ARGUMENTS` carefully.
- Restate the objective, scope, and constraints.
- Identify what is in scope vs out of scope.
- Flag any obvious ambiguities or missing information.
- **Detect applicable personas** based on content (v2.7).
- **Apply active flags** to modify behavior (v2.7).

If the scope is **unclear** or appears **smaller than STANDARD** (should be Micro or Soft):

1. Explicitly state that the task might not need the full EPCI workflow.
2. Recommend using `epci-micro` or `epci-soft` instead.
3. Stop and ask the user to confirm.

### 4.2 Step 2 — Explore — Codebase Analysis

**This step is strictly read-only. No file writes allowed.**

Use repo tools (`read_file`, `tree`, `grep`, `find`, etc.) to:

1. **Locate relevant files**:
   - Source files that will be modified,
   - Configuration files,
   - Test files,
   - Related helpers or utilities.

2. **Understand the current architecture**:
   - Folder structure and layering,
   - Naming conventions,
   - Error handling patterns,
   - Logging patterns,
   - Dependency injection patterns,
   - Test layout and conventions.

3. **Identify constraints and invariants**:
   - Contracts that must not be broken,
   - Performance constraints,
   - Security requirements,
   - Data integrity rules.

4. **Spot risks and couplings**:
   - Files that depend on others,
   - Shared utilities,
   - External services,
   - Potential side effects.

### 4.2.1 Using Sub-agents for Deep Exploration

For complex codebases, consider using **sub-agents** to investigate specific questions without polluting your main context:

> 💡 **Sub-agent pattern:** "Use a sub-agent to investigate how [specific aspect] is handled in this codebase, then report back your findings."

**When to use sub-agents:**

- Investigating authentication, authorization, or security patterns
- Understanding complex data flows across multiple files
- Exploring test patterns and conventions
- Analyzing error handling strategies

**Benefits:**

- Preserves main context window for planning and decision-making
- Allows parallel investigation of multiple areas
- More thorough exploration without context pollution
- Each sub-agent can focus on a specific question

**Example prompts for sub-agents:**

```
"Use a sub-agent to find all places where user permissions are checked 
and summarize the patterns used."

"Use a sub-agent to investigate how the caching layer works 
and report back the key classes and methods."

"Use a sub-agent to analyze the test structure and conventions 
used in this project."
```

### 4.2.2 Persona-Enhanced Exploration (v2.7)

When a persona is active, the exploration is enhanced:

| Persona | Enhanced Exploration Focus |
|---------|---------------------------|
| **Architect** | System boundaries, dependencies, scalability patterns |
| **Security** | Auth flows, data exposure, input validation |
| **Performance** | Hot paths, N+1 queries, caching opportunities |
| **QA** | Test coverage, edge cases, error scenarios |
| **Frontend** | Component structure, state management, accessibility |
| **Backend** | API contracts, database queries, service boundaries |
| **DevOps** | Configuration, deployment, monitoring hooks |

### 4.3 Step 3 — Plan — Detailed Implementation Plan

Produce a **detailed, actionable plan** with the following subsections:

1. **Scope & Goal**: 1–2 paragraphs summarizing what will be done.
2. **Context & Key Files**: recap from exploration.
3. **Proposed Changes**: file-by-file breakdown with change type (new/modify/delete).
4. **Control & Data Flow**: how data moves through the system.
5. **Edge Cases & Error Handling**: explicit list of edge cases and how they are handled.
6. **Testing Strategy**: what tests will be written.
7. **Documentation & ADRs**: what docs need updating.
8. **Assumptions & Open Questions**: anything not yet confirmed.
9. **Implementation Checklist**: numbered steps for `epci-2-code` to follow.
10. **Confidence & Risks**: confidence percentage and top risks.
11. **Persona Recommendations** (v2.7): suggest personas and flags for next steps.

**In INTERACTIVE mode:**

- Present the complete plan.
- **STOP** and wait for user validation.
- Do NOT write to the Feature Document yet.

**In AUTO mode:**

- Self-validate and proceed directly to writing.
- **Document all assumptions explicitly** in section 4 of the output.

### 4.4 Step 4 — Validate FEATURE_SLUG

Before writing to the Feature Document, validate the `FEATURE_SLUG`:

1. Confirm it is in **kebab-case** (lowercase, hyphens only).
2. Confirm it matches the feature title or was explicitly provided.
3. Confirm the path `docs/features/<feature-slug>.md` is valid.

If invalid, fix it or ask the user to confirm.

### 4.5 Step 5 — Feature Document Update

`epci-1-analyse` works with the **single Feature Document** created by `epci-0-briefing`:

- Path: `docs/features/<feature-slug>.md`

**Critical rule:**

> **NEVER modify `## 1. Functional Brief — EPCI-0` or `## 3. Final Report — EPCI-3`.**  
> Only update `## 2. Technical Plan — EPCI-1`.

**Behaviour:**

1. **If the Feature Document does not exist** (edge case — `epci-0` was skipped):
    
    - **Create it** using the standard skeleton:
    
    ```markdown
    # <Feature Title>
    
    ## 1. Functional Brief — EPCI-0
    
    *(Brief not available — `epci-1-analyse` called directly.)*
    
    *(Do not modify this section.)*
    
    ## 2. Technical Plan — EPCI-1
    
    <full plan content here>
    
    ## 3. Final Report — EPCI-3
    
    *(To be filled by `epci-3-finalize`.)*
    
    *(Do not modify this section.)*
    ```

2. **If the Feature Document exists**:
    
    - **Read** the existing content.
    - **Preserve** `## 1. Functional Brief — EPCI-0` exactly as-is.
    - **Replace or update** `## 2. Technical Plan — EPCI-1` with the full plan.
    - **Preserve** `## 3. Final Report — EPCI-3` exactly as-is.

3. **Use the available file tools** to actually write these updates.

**In INTERACTIVE mode:**

- Only write after explicit user validation (Phase B).
- Phase A = strictly read-only, no file writes.

**Flag effects on writing:**

| Flag | Effect on Feature Document |
|------|---------------------------|
| `--preview` | Shows what would be written, doesn't write |
| `--dry-run` | Full simulation, no actual writes |
| Normal | Writes to Feature Document |

### 4.6 Step 6 — Next Command Suggestion

At the end of the command, **explicitly suggest the next command** with a complete, copy-pastable block:

````markdown
## 6. Next Command

```text
To continue with implementation and tests, run:

epci-2-code
FEATURE_SLUG=<feature-slug>
PLAN_PATH=docs/features/<feature-slug>.md
$ARGUMENTS=<EPCI_READY_BRIEF or brief summary>

Recommended flags: --validate
Recommended persona: --persona-<x> (based on analysis)
````

The plan is available in: `docs/features/<feature-slug>.md` (section "2. Technical Plan — EPCI-1").

````

**Then STOP.**

- Do NOT write any implementation code.
- Do NOT run tests.
- Do NOT modify source files.

---

## 5. Guardrails: Scope Validation

At any point (Understanding, Explore, Plan), `epci-1-analyse` MUST validate that the task matches the expected complexity.

### 5.1 If scope is SMALLER than expected

If the task appears to be **TINY** or **SMALL**:

- Estimated files: 1–3
- Estimated LOC: < 200
- Single module, low risk

Then:

1. Clearly state that the full EPCI workflow may be overkill.
2. Suggest using `epci-micro` (TINY) or `epci-soft` (SMALL) instead.
3. Ask the user to confirm before continuing.

### 5.2 If scope is LARGER than expected

If during exploration the task reveals:

- More than **10 files** to modify,
- Estimated LOC > **1000**,
- More than **3 modules** impacted,
- **Schema changes** or **migrations** required,
- **Security-critical** changes,
- **Many unknowns** or ambiguities,

Then:

1. Clearly flag that this is a **LARGE** task.
2. Recommend extra caution and possibly breaking down into smaller sub-tasks.
3. Document the risks explicitly in section 3.10.
4. **Suggest `--persona-architect`** for complex multi-module tasks (v2.7).

### 5.3 Complexity reference grid

| Level | Files | LOC | Risk | Modules | Workflow |
|-------|-------|-----|------|---------|----------|
| **TINY** | 1 (max 2) | < 50 | Very low | 1 | `epci-micro` |
| **SMALL** | 2–3 | 50–200 | Low | 1 | `epci-soft` |
| **STANDARD** | 3–10 | 200–1000 | Medium | 1–3 | `epci-1` → `epci-2` → `epci-3` |
| **LARGE** | > 10 | > 1000 | High | > 3 | `epci-1` → `epci-2` → `epci-3` |

---

## 6. Example — Feature Document after EPCI-1

Below is a **concrete example** of how the Feature Document might look after running `epci-0-briefing` and `epci-1-analyse`.

```markdown
# Stay tax calculation for seasonal rentals

## 1. Functional Brief — EPCI-0

*(This section is managed by `epci-0-briefing`. Do not modify.)*

- Objective: Calculate and display stay tax for seasonal rentals.
- Functional requirements:
  - [FR1] Calculate tax based on rental duration and property type.
  - [FR2] Display tax breakdown on booking summary.
  - [FR3] Include tax in invoice generation.
- Acceptance criteria:
  - [AC1] Tax is correctly calculated for 1-day, 7-day, 30-day stays.
  - [AC2] Tax breakdown is visible on booking confirmation page.

## 2. Technical Plan — EPCI-1

*(This section is managed by `epci-1-analyse`.)*

### Scope & Goal

Implement stay tax calculation for seasonal rentals. The tax is based on the number of nights and the property category. It must be displayed on the booking summary and included in invoices.

In scope:
- Tax calculation logic
- Booking summary display
- Invoice integration

Out of scope:
- Admin configuration UI for tax rates
- Historical tax rate changes

### Context & Key Files

| File | Role |
|------|------|
| `src/Domain/Booking/StayTaxCalculator.php` | New — core tax calculation |
| `src/Application/Booking/BookingService.php` | Modify — integrate tax |
| `src/Infrastructure/Invoice/InvoiceGenerator.php` | Modify — add tax line |
| `templates/booking/summary.html.twig` | Modify — display tax |

### Proposed Changes (file by file)

| File | Change type | Description |
|------|-------------|-------------|
| `src/Domain/Booking/StayTaxCalculator.php` | new | Create tax calculation service |
| `src/Application/Booking/BookingService.php` | modify | Call StayTaxCalculator, add tax to booking |
| `src/Infrastructure/Invoice/InvoiceGenerator.php` | modify | Add tax line item to invoice |
| `templates/booking/summary.html.twig` | modify | Display tax breakdown |
| `tests/Unit/Domain/Booking/StayTaxCalculatorTest.php` | new | Unit tests for tax calculation |

### Control & Data Flow

1. User creates a booking → `BookingController`
2. `BookingService` calculates total → calls `StayTaxCalculator`
3. Tax amount stored in `Booking` entity
4. On confirmation page, `summary.html.twig` displays tax
5. On invoice generation, `InvoiceGenerator` adds tax line

### Edge Cases & Error Handling

- Zero nights: tax = 0
- Property without category: use default rate
- Tax rate not configured: throw `TaxConfigurationException`

### Testing Strategy

- Unit: `StayTaxCalculatorTest` — test calculation for various durations/categories
- Integration: `BookingServiceTest` — verify tax is correctly added to booking
- E2E: Manual — create booking, verify tax on summary and invoice

### Assumptions & Open Questions

- Assumption: Tax rates are stored in configuration, not database.
- Assumption: All properties have a category assigned.
- Open question: Should we support historical tax rates?

### Implementation Checklist

- [ ] Create `StayTaxCalculator` with `calculate(int $nights, string $category): Money`
- [ ] Add tax rates configuration
- [ ] Integrate into `BookingService`
- [ ] Update `Booking` entity to store tax amount
- [ ] Modify invoice template
- [ ] Modify booking summary template
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update API documentation

### Confidence & Risks

- Confidence: 85%
- Risks:
  1. Tax rate configuration format not yet defined
  2. Invoice template might need design review
  3. Edge case for exempt properties not fully specified

### Persona Recommendations (v2.7)

> 💡 **For epci-2-code, consider:**
> - `--persona-backend` for service implementation
> - `--validate` for tax calculation accuracy

## 3. Final Report — EPCI-3

*(This section is managed by `epci-3-finalize`. Do not modify.)*

*(To be filled after implementation.)*
```

---

## 7. Summary

`epci-1-analyse` is the **planning phase** of the full EPCI workflow:

- It keeps the EPCI philosophy (**Explore → Plan → Code → Inspect**),
- It is **strictly read-only** (no implementation code),
- It produces a **detailed, actionable plan** for `epci-2-code`,
- It updates **only** `## 2. Technical Plan` in the Feature Document,
- It **never modifies** `## 1. Functional Brief` or `## 3. Final Report`,
- It suggests the **next command** with complete parameters.

In **INTERACTIVE mode**, the workflow has two phases:

- **Phase A** — Explore & draft plan (strictly read-only, NO file writes, wait for validation),
- **Phase B** — Write plan to Feature Document (only after explicit user confirmation).

In **AUTO mode**, all steps are executed in a single pass, with all assumptions documented.

The plan must be **dense and specific** — detailed enough that `epci-2-code` can implement without guessing.

**v2.7 improvements:**

- **Flags support**: `--preview`, `--dry-run`, `--uc`, `--verbose`, `--introspect`
- **Personas support**: All 7 personas with auto-activation
- **Persona-enhanced exploration**: Deeper analysis based on active persona
- **Persona recommendations**: Suggests optimal personas for next steps
- **Introspection output**: Shows reasoning when `--introspect` is active
- Thinking mode hierarchy documented (think < think hard < think harder < ultrathink)
- Sub-agents pattern for deep codebase exploration
- Preserves context by delegating investigation to sub-agents

---

## 8. Related Documentation

- **Flags Reference**: See `epci-flags.md` for complete flags documentation
- **Personas Reference**: See `epci-personas.md` for persona details
- **Workflow Guide**: See `epci-workflow-guide.md` for overall workflow

---

*This document is part of the EPCI v2.7 workflow system.*
