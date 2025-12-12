# epci-soft — Light EPCI workflow for SMALL changes (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> `epci-soft` is the **light workflow** for **SMALL** changes, sitting between `epci-micro` (TINY) and the full EPCI pipeline (`epci-1/2/3`).
> 
> `epci-soft` is a **complete, self-contained workflow**: it explores, plans, implements, and verifies — all in one command.

> 💡 **Recommended:** Activate **extended thinking** (use "think harder") for Phase A (Explore & Plan) to improve analysis quality.
>
> **Thinking mode hierarchy:** think < think hard < think harder < ultrathink
> For complex exploration, consider "think harder" to ensure thorough analysis.

---

## Critical Rules

- ⚠️ SMALL only: 2–3 files, 50–200 LOC, single module, low risk
- ⚠️ Phase A (INTERACTIVE) = NO file writes, wait for validation
- ⚠️ If scope exceeds SMALL → STOP and reroute to full EPCI
- ⚠️ `epci-soft` writes actual code — not just guidance
- ⚠️ `--safe-mode` requires confirmation before each file modification (v2.7)
- ⚠️ No section before `## 1.` and no section after `## 8.`

---

## Supported Flags (v2.7)

`epci-soft` supports **all universal flags** as it is a complete workflow.

### Safety Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--preview` | Show plan and what would be implemented, no file writes | Off |
| `--safe-mode` | Require confirmation before each file modification | Off |
| `--dry-run` | Simulate entire workflow without writing files | Off |
| `--validate` | Run lint, type-check, security scan after implementation | Off |

### Output Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--uc` | Ultra-compressed output (~70% reduction) | Off |
| `--verbose` | Maximum detail in exploration and implementation | Off |

### Debug Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--introspect` | Show decision-making process for plan and implementation | Off |

**Usage examples:**

```bash
# Preview what would be done
epci-soft --preview
FEATURE_SLUG=max-stay-validation

# Safe mode with validation
epci-soft --safe-mode --validate
FEATURE_SLUG=user-profile-update

# Compressed output
epci-soft --uc
FEATURE_SLUG=quick-fix

# Full transparency
epci-soft --introspect --verbose
FEATURE_SLUG=new-filter
```

### Flag Effects by Phase

| Flag | Phase A (Explore & Plan) | Phase B (Code & Inspect) |
|------|--------------------------|--------------------------|
| `--preview` | Shows full exploration/plan | Skips all file writes |
| `--safe-mode` | N/A | Confirms each file modification |
| `--dry-run` | Shows exploration/plan | Simulates implementation |
| `--validate` | N/A | Runs validation checks |
| `--uc` | Compressed exploration | Compressed implementation report |
| `--verbose` | Detailed exploration | Full code diffs shown |
| `--introspect` | Shows plan reasoning | Shows implementation decisions |

### Flag Combinations

| Combination | Use Case |
|-------------|----------|
| `--preview --verbose` | Detailed preview before committing |
| `--safe-mode --validate` | Maximum safety for production code |
| `--uc --validate` | CI/CD pipeline usage |
| `--introspect --verbose` | Learning/debugging the workflow |

> **Note:** For complete flags documentation, see `epci-flags.md`.

---

## Supported Personas (v2.7)

`epci-soft` supports **all 7 personas** for specialized expertise during the workflow.

| Persona | Flag | Specialization | Auto-triggers |
|---------|------|----------------|---------------|
| **Architect** | `--persona-architect` | Design patterns, modularity | N/A (SMALL scope) |
| **Security** | `--persona-security` | Auth, vulnerabilities, data protection | auth/, security/, crypto/ |
| **Performance** | `--persona-performance` | Optimization, caching, queries | "optimize", "slow", "cache" |
| **QA** | `--persona-qa` | Testing, validation, edge cases | tests/, "coverage" |
| **Frontend** | `--persona-frontend` | UI/UX, React, Vue, CSS | .tsx, .jsx, components/ |
| **Backend** | `--persona-backend` | API, database, services | Controller, Service, Repository |
| **DevOps** | `--persona-devops` | CI/CD, deployment, config | Dockerfile, .yml, deploy |

### Persona Behaviour in epci-soft

1. **During Explore (Phase A):**
   - Persona adds domain-specific observations
   - Highlights risks relevant to the persona's expertise
   - Suggests domain-specific edge cases

2. **During Plan (Phase A):**
   - Persona influences plan priorities
   - Adds persona-specific checklist items
   - May recommend additional validation steps

3. **During Code (Phase B):**
   - Persona guides implementation patterns
   - Adds domain-specific code quality checks
   - Highlights potential issues during implementation

4. **During Inspect (Phase B):**
   - Persona-specific test recommendations
   - Domain-focused verification checklist

### Usage Examples

```bash
# Security-focused validation feature
epci-soft --persona-security
FEATURE_SLUG=input-validation

# Performance-focused query optimization
epci-soft --persona-performance --validate
FEATURE_SLUG=search-optimization

# Frontend component update
epci-soft --persona-frontend
FEATURE_SLUG=user-card-component
```

### Auto-activation Rules

| File/Path Pattern | Auto-activated Persona |
|-------------------|------------------------|
| `src/Security/`, `src/Auth/` | `--persona-security` |
| `src/Controller/`, `src/Service/` | `--persona-backend` |
| `assets/`, `templates/`, `*.tsx`, `*.jsx` | `--persona-frontend` |
| `tests/` | `--persona-qa` |
| Files with "cache", "optimize" | `--persona-performance` |

> **Note:** For complete personas documentation, see `epci-personas.md`.

---

## 1. Purpose & Scope

`epci-soft` is designed for **small, well-scoped changes** that:

- are **more substantial** than a micro-fix (TINY), but
- **do not justify** the full weight of `epci-1-analyse` → `epci-2-code` → `epci-3-finalize`.

### 1.1 Typical use cases

- Adding or adjusting a **simple validation rule**.
- Small changes in **one bounded context/module** (1–3 files).
- Minor **UX adjustments** with a bit of logic (e.g. additional field, extra column, new simple filter).
- Light **business tweaks** without DB schema changes and without complex edge-cases.

### 1.2 TINY vs SMALL Clarification

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

Use `epci-soft` when the complexity assessment (from `epci-0-briefing`) is:

- **SMALL**, and
- the task can reasonably be done in **one short cycle** with:
    - a clear light plan,
    - one implementation phase,
    - basic tests and wrap-up.

> **Approximate effort guideline (non-contractual):**  
> A typical SMALL change handled via `epci-soft` corresponds roughly to **30–90 minutes** of focused work for a senior developer (implementation + tests + documentation).

If, during exploration, the change appears to be **STANDARD or LARGE**, `epci-soft` MUST stop and recommend using the **full EPCI workflow** instead.

---

## 2. Inputs & Modes

### 2.1 `$ARGUMENTS`

`epci-soft` is typically called with the `EPCI_READY_BRIEF` produced by `epci-0-briefing`.

```text
$ARGUMENTS=<EPCI_READY_BRIEF>
  FEATURE_TITLE: <human-readable title of the change>
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

If `epci-soft` is called outside of EPCI-0, the brief provided in `$ARGUMENTS` must contain at least the same information to remain self-contained.

### 2.2 Execution modes & phases

`epci-soft` supports `EXECUTION_MODE`:

- `"INTERACTIVE"` (default):
    
    - **Phase A — Explore & Plan (read-only, NO file writes)**:
        - Explore the codebase context.
        - Detect and apply persona if relevant (v2.7).
        - Produce a light technical plan.
        - Show introspection if `--introspect` active (v2.7).
        - Present the plan to the user.
        - **⚠️ Do NOT write any files yet.**
        - Ask the user to validate or adjust the plan before proceeding.
    
    - **Phase B — Code & Inspect (after validation)**:
        - Once the user confirms the plan, **implement the changes** by writing/modifying the actual files.
        - If `--safe-mode`: confirm each file modification (v2.7).
        - Run or describe quick tests.
        - If `--validate`: run validation checks (v2.7).
        - Update the Feature Document.
        - Produce wrap-up (commit message, PR description).

- `"AUTO"`:
    
    - Single-pass, self-validated workflow.
    - Explore → Plan → Code → Inspect in one go.
    - Assumptions MUST be explicitly documented.
    - Use AUTO only when the context is controlled and the task is clearly scoped.

> **Important — `epci-soft` is a complete workflow:**  
> Unlike a "guide-only" assistant, `epci-soft` **actually implements the code**.  
> It writes files, updates the Feature Document, and performs quick verification.  
> The human validates the plan (in INTERACTIVE mode) but does not need to manually apply the code.

### 2.3 Flag Effects on Execution

| Flag | Phase A Effect | Phase B Effect |
|------|----------------|----------------|
| `--preview` | Shows full analysis | Skips all file writes |
| `--safe-mode` | N/A (no writes) | Prompts before each file |
| `--dry-run` | Shows analysis | Simulates all writes |
| `--validate` | N/A | Runs lint/type-check/security |
| `--uc` | Compressed output | Compressed report |
| `--verbose` | Full exploration details | Full code diffs |
| `--introspect` | Shows reasoning | Shows implementation logic |

### 2.4 Recommended prerequisite

> `epci-0-briefing` should be run first to produce the `EPCI_READY_BRIEF`.  
> If `epci-soft` is called directly, ensure all required fields are provided manually.

---

## 3. Responsibilities & Limitations

### 3.1 What `epci-soft` MUST do

`epci-soft` is a **complete implementation workflow** for SMALL changes:

1. **Explore** — Understand the codebase context logically (modules, components, likely files).
2. **Validate FEATURE_SLUG** — Confirm or derive the canonical slug.
3. **Detect persona triggers** — Auto-activate relevant persona if detected (v2.7).
4. **Plan** — Produce a light but structured technical plan (2–6 steps).
5. **Show introspection** — If `--introspect`, explain planning decisions (v2.7).
6. **Code** — **Implement the changes** by writing/modifying actual files in the repository:
    - Apply changes file by file,
    - If `--safe-mode`, confirm each file before writing (v2.7),
    - Follow existing coding style and patterns,
    - Keep changes limited to SMALL scope (1–3 files, limited LOC).
7. **Inspect** — Perform quick verification:
    - Run relevant tests if available,
    - If `--validate`, run lint/type-check/security scan (v2.7),
    - Describe manual checks if needed.
8. **Document** — Update the **Feature Document** (`docs/features/<feature-slug>.md`):
    - Enrich the **Functional Brief** section if needed,
    - Add a **light technical plan** in the **Technical Plan** section,
    - Add a short note in **Final Report** to indicate the task was completed via `epci-soft`.
9. **Wrap-up** — Emit:
    - A short **commit message** (with scope),
    - A short **PR description**,
    - Suggested git commands.

> **`epci-soft` executes the code, it does not just guide.**  
> The implementation is applied directly to the repository.  
> In INTERACTIVE mode, the plan is validated first; in AUTO mode, execution is immediate.

### 3.2 What `epci-soft` MUST NOT do

- MUST NOT perform large refactors.
- MUST NOT modify DB schemas or migrations.
- MUST NOT introduce complex workflows spanning multiple modules.
- MUST NOT manage multi-step data migrations.
- MUST NOT silently treat a **STANDARD** / **LARGE** task as SMALL.
- MUST NOT replace the full EPCI workflow for features that:
    - touch critical business flows,
    - impact security or core data,
    - require significant testing and rollout planning.

> If the scope appears larger than SMALL, `epci-soft` MUST **stop** and recommend using the full EPCI pipeline.

---

## 4. Output Layout (assistant message)

For IDE / terminal readability, `epci-soft` MUST follow this **fixed layout**.

````markdown
## 1. Understanding & Scope

- Feature: `<feature-slug>`
- Objective: ... (1-2 sentences)
- In scope: ...
- Out of scope: ...
- Constraints: ...

### Active Configuration (v2.7)
- Flags: `--safe-mode`, `--validate` (if any)
- Persona: `--persona-backend` (if any, with trigger reason)

---

## 2. Explore — Context & Impact

### 2.1 Modules & components involved
- ...

### 2.2 Existing behaviour (before)
- ...

### 2.3 Target behaviour (after)
- ...

### 2.4 Identified risks / edge cases
- ...

### 2.5 Persona-specific observations (v2.7)
> 🔒 **Security Persona Notes:** (if --persona-security active)
> - Input validation requirements: ...
> - Data protection considerations: ...

---

## 3. Plan — Light Technical Plan (EPCI-Soft)

- [P1] ...
- [P2] ...
- [P3] ...
- (Optional) [P4] ...

### Introspection (if --introspect active)

> 🔍 **Plan Reasoning:**
> - Chose to modify X before Y because: ...
> - Decided against Z approach because: ...
> - Risk mitigation: ...

---

## 4. Implementation — Code Changes

### 4.1 Files modified
- `path/to/file1` — <short description of change>
- `path/to/file2` — <short description of change>

### 4.2 Safe-mode confirmations (if --safe-mode active)

| File | Action | Confirmed |
|------|--------|-----------|
| `src/Service/X.php` | modify | ✅ User confirmed |
| `tests/XTest.php` | new | ✅ User confirmed |

**Code written:** ✅

### 4.3 Deviations from plan (if any)

| Planned | Actual | Reason |
|---------|--------|--------|
| ... | ... | ... |

*(If none: "None. Implementation followed the plan exactly.")*

---

## 5. Inspect — Tests & Verification

### 5.1 Tests executed

- [ ] Test 1: ...
- [ ] Test 2: ...
- (Optional) [ ] Test 3: ...

### 5.2 Test results

- Tests run: `<command or description>`
- Result: ✅ PASS / ❌ FAIL
- Notes: ...

### 5.3 Validation results (if --validate active)

| Check | Tool | Result |
|-------|------|--------|
| Lint | PHPStan | ✅ Pass |
| Type-check | Psalm | ✅ Pass |
| Security | Snyk | ✅ Pass |

---

## 6. Feature Document Update

- Feature slug: `<feature-slug>`
- Feature document: `docs/features/<feature-slug>.md`
- Updates applied:
  - `## 1. Functional Brief — EPCI-0` → (optional) minor clarification
  - `## 2. Technical Plan — EPCI-1` → added "EPCI-Soft plan" subsection
  - `## 3. Final Report — EPCI-3` → added completion note

> Sections enriched, not overwritten.

---

## 7. Wrap-up — Commit & PR

### 7.1 Suggested commit message

```text
<type>(<scope>): <short message>
```

### 7.2 Suggested PR description

```markdown
## Summary
- ...

## Changes
- ...

## Tests
- ...
```

### 7.3 Git commands

```bash
git add <files>
git commit -m "<message>"
git push
```

---

## 8. Workflow Complete (v2.7)

```text
✅ EPCI-Soft workflow complete for feature: <feature-slug>

Configuration:
- Flags: --safe-mode, --validate
- Persona: --persona-backend

Results:
- Files modified: 3
- Tests: ✅ PASS
- Validation: ✅ PASS

Feature Document: docs/features/<feature-slug>.md
```
````

**Strict rule:** No extra sections before `## 1.` or after `## 8.`.

---

## 5. Behaviour Step-by-step

### 5.1 Step 1 — Understanding & Scope

Read `$ARGUMENTS` and restate:

- the feature slug (validate it),
- the objective in 1–2 sentences,
- what's in scope vs out of scope,
- key constraints and assumptions.

**v2.7 additions:**
- List active flags
- Detect and document active persona (auto or explicit)

**Example:**

```markdown
## 1. Understanding & Scope

- Feature: `max-stay-length-validation`
- Objective: Prevent bookings > 30 days for standard rentals
- In scope: Validation logic, error message, unit tests
- Out of scope: Admin override, historical bookings
- Constraints: Must not affect premium rentals

### Active Configuration (v2.7)
- Flags: `--validate`
- Persona: `--persona-backend` (auto-detected: BookingService, BookingValidator)
```

### 5.2 Step 2 — Explore

Identify:

- **Modules & components** involved (file paths, classes, functions),
- **Existing behaviour** (what the system does today),
- **Target behaviour** (what it should do after),
- **Identified risks and edge cases** (things that might break or need attention).

This exploration is **logical**, based on codebase understanding. For more in-depth exploration, use sub-agents:

```
"Use a sub-agent to investigate how booking validation is currently implemented."
```

**v2.7 additions:**
- If a persona is active, add persona-specific observations section
- Show introspection of exploration decisions if `--introspect`

### 5.3 Step 3 — Plan

Produce a **light technical plan** with 2–6 steps:

- `[P1]`, `[P2]`, ... — numbered planning items,
- Each step is actionable and references a specific file or component.

**v2.7 additions:**
- If `--introspect`, add reasoning block explaining plan decisions
- If persona active, plan may include persona-specific checklist items

**Example:**

```markdown
## 3. Plan — Light Technical Plan (EPCI-Soft)

- [P1] Add `MAX_STAY_DAYS = 30` constant in `BookingValidator`
- [P2] Add validation method `validateStayLength(int $days, string $type): bool`
- [P3] Call validation in `BookingService::createBooking()`
- [P4] Add error message in translation files
- [P5] Add unit tests for 29/30/31 days

### Introspection (--introspect)

> 🔍 **Plan Reasoning:**
> - Chose to add constant in Validator (not config) because: simple, single-use value
> - Validation in Service layer because: keeps Validator pure, Service orchestrates
> - Testing boundary conditions because: critical for acceptance criteria
```

> **In INTERACTIVE mode — STOP here in Phase A.**  
> Present the plan for user validation before continuing to Phase B.

### 5.4 Step 4 — Code (Phase B)

**Actually implement** the changes by writing / modifying files.

**v2.7 safe-mode behaviour:**

If `--safe-mode` is active:

```markdown
### File 1/3: src/Domain/Booking/BookingValidator.php

Action: MODIFY
Changes:
```diff
+ public const MAX_STAY_DAYS = 30;
+
+ public function validateStayLength(int $days, string $type): bool
+ {
+     if ($type === 'standard' && $days > self::MAX_STAY_DAYS) {
+         return false;
+     }
+     return true;
+ }
```

Confirm this change? [y/n/skip/abort]: y
✅ File modified.
```

**Standard behaviour (no --safe-mode):**

- Modify files directly
- Report each file modified with short description

**Output:**

```markdown
## 4. Implementation — Code Changes

### 4.1 Files modified
- `src/Domain/Booking/BookingValidator.php` — added constant and validation method
- `src/Application/Booking/BookingService.php` — integrated validation call
- `translations/messages.fr.yaml` — added error message
- `tests/Unit/Domain/Booking/BookingValidatorTest.php` — added 3 test cases

**Code written:** ✅

### 4.3 Deviations from plan

None. Implementation followed the plan exactly.
```

### 5.5 Step 5 — Inspect (Phase B)

Describe how the change is verified:

- **Run tests** (or suggest which tests to run).
- **Manual checks** (or describe them).
- **v2.7:** If `--validate`, run additional validation checks.

**Standard output:**

```markdown
## 5. Inspect — Tests & Verification

### 5.1 Tests executed

- [x] Test 29-day booking → accepted ✅
- [x] Test 30-day booking → accepted ✅
- [x] Test 31-day booking → rejected ✅
- [x] Test premium 45-day booking → accepted ✅

### 5.2 Test results

- Tests run: `php bin/phpunit tests/Unit/Domain/Booking/BookingValidatorTest.php`
- Result: ✅ PASS (4 tests, 4 assertions)
```

**With --validate flag:**

```markdown
### 5.3 Validation results (--validate)

| Check | Tool | Result |
|-------|------|--------|
| Lint | PHPStan level 8 | ✅ Pass (0 errors) |
| Type-check | Psalm | ✅ Pass |
| Security | Snyk | ✅ Pass (no vulnerabilities) |

Overall validation: ✅ PASS
```

### 5.6 Step 6 — Feature Document Update (Phase B)

Update the Feature Document at `docs/features/<feature-slug>.md`.

**Behaviour:**

1. If the file does not exist, create it with the skeleton.
2. If the file exists:
    - Under `## 2. Technical Plan — EPCI-1`, add:
        ```markdown
        ### EPCI-Soft plan — <YYYY-MM-DD>
        
        - [P1] ...
        - [P2] ...
        ```
    - Under `## 3. Final Report — EPCI-3`, add:
        ```markdown
        ### EPCI-Soft completion — <YYYY-MM-DD>
        
        - Task completed via `epci-soft`.
        - Flags used: --validate (v2.7)
        - Persona: --persona-backend (v2.7)
        - Tests: ✅ PASS
        - Validation: ✅ PASS (v2.7)
        - Commit: `<commit message>`
        ```

3. **Use the available file tools to actually write these updates** into the Feature Document.

### 5.7 Step 7 — Wrap-up — Commit & PR

Provide:

- A **short commit message** (50–72 chars recommended, conventional commits with scope).
- A **short PR description** that:
    - recalls the objective,
    - summarises the change,
    - lists the key tests executed.
- **Git helper commands** for the developer to commit and push.

**Commit format for epci-soft (with scope):**

```text
<type>(<scope>): <short message>
```

**Examples:**

- Commit: `feat(booking): add max stay length validation (30 days)`
    
- PR description:
    
    ```markdown
    ## Summary
    - Add max stay length validation on booking form (30 days)
    - Display user-friendly error message on violation
    
    ## Tests
    - Unit tests for boundary conditions (29/30/31 days)
    - Manual verification on staging
    
    ## Validation (v2.7)
    - PHPStan: ✅ Pass
    - Psalm: ✅ Pass
    ```

### 5.8 Step 8 — Workflow Complete (v2.7)

End with a summary block:

```markdown
## 8. Workflow Complete (v2.7)

```text
✅ EPCI-Soft workflow complete for feature: max-stay-length-validation

Configuration:
- Flags: --validate
- Persona: --persona-backend

Results:
- Files modified: 4
- Tests: ✅ PASS (4 tests)
- Validation: ✅ PASS

Feature Document: docs/features/max-stay-length-validation.md
```
```

---

## 6. Guardrails: Detecting Non-SMALL Tasks

At any point (Understanding, Explore, Plan, Implementation), `epci-soft` MUST re-check whether the task is still compatible with the **SMALL** constraints.

### 6.1 Complexity Reference (SMALL thresholds)

| Criterion | SMALL limit | If exceeded → |
|-----------|-------------|---------------|
| Files | 1–3 | → full EPCI |
| LOC | 50–200 | → full EPCI |
| Modules | 1 | → full EPCI |
| Risk | Low | → full EPCI |
| Schema change | None | → full EPCI |
| Security impact | Minimal | → full EPCI |

### 6.2 When to Stop and Reroute

If any of the following holds true:

- More than **3 files** expected to be modified,
- Estimated LOC change > **200** lines,
- Multiple modules / bounded contexts impacted,
- New DB schema or heavy data manipulation required,
- Security-critical flows or core business invariants impacted,
- Complexity of edge cases grows significantly,

Then:

1. **STOP** — Clearly state that the task is no longer SMALL.
    
2. **Reroute** — Suggest switching to the full EPCI pipeline with persona recommendation (v2.7):
    
    ```markdown
    ⚠️ This task is not suitable for `epci-soft` anymore (scope is beyond SMALL).
    
    **Reason:** <explain why>
    
    **Recommendation:** Use the full EPCI workflow:
    - epci-1-analyse [--persona-<x>]
    - epci-2-code [--persona-<x>]
    - epci-3-finalize
    
    **Suggested persona:** --persona-security (detected auth-related changes)
    ```
    
3. **Do NOT continue** with a soft-level plan.

---

## 7. Example — Complete EPCI-Soft Session

Below is a **complete example** of an `epci-soft` session with v2.7 features.

````markdown
## 1. Understanding & Scope

- Feature: `max-stay-length-validation`
- Objective: Prevent bookings longer than 30 days for standard rentals
- In scope: Validation logic, error message, unit tests
- Out of scope: Admin override, historical bookings
- Constraints: Must not affect premium rentals

### Active Configuration (v2.7)
- Flags: `--safe-mode`, `--validate`
- Persona: `--persona-backend` (auto-detected: BookingValidator, BookingService)

---

## 2. Explore — Context & Impact

### 2.1 Modules & components involved
- `src/Domain/Booking/BookingValidator.php`
- `src/Application/Booking/BookingService.php`
- `templates/booking/form.html.twig`

### 2.2 Existing behaviour (before)
- No limit on booking duration
- Any number of days accepted

### 2.3 Target behaviour (after)
- Bookings > 30 days rejected for standard rentals
- Clear error message displayed to user

### 2.4 Identified risks / edge cases
- Edge case: exactly 30 days should be accepted
- Risk: must not affect premium rentals (different validation path)

### 2.5 Persona-specific observations (v2.7)
> 🔧 **Backend Persona Notes:**
> - Validation should be in Domain layer (BookingValidator)
> - Service layer orchestrates, doesn't contain business rules
> - Consider throwing domain exception for invalid bookings

---

## 3. Plan — Light Technical Plan (EPCI-Soft)

- [P1] Add `MAX_STAY_DAYS = 30` constant in `BookingValidator`
- [P2] Add validation method `validateStayLength(int $days, string $type): bool`
- [P3] Call validation in `BookingService::createBooking()`
- [P4] Add error message in translation files
- [P5] Add unit tests for 29/30/31 days

### Introspection (--introspect)

> 🔍 **Plan Reasoning:**
> - Constant in Validator: single source of truth, easy to find
> - Method signature with type parameter: allows different rules per rental type
> - Service integration: keeps validation at orchestration level
> - Test boundary conditions: critical for AC1/AC2/AC3

---

> ⚠️ **Phase A — Plan ready for validation.**
> Please review and confirm to proceed with implementation.

---

## 4. Implementation — Code Changes

### 4.1 Files modified
- `src/Domain/Booking/BookingValidator.php` — added constant and validation method
- `src/Application/Booking/BookingService.php` — integrated validation call
- `translations/messages.fr.yaml` — added error message
- `tests/Unit/Domain/Booking/BookingValidatorTest.php` — added 4 test cases

### 4.2 Safe-mode confirmations (--safe-mode)

| File | Action | Confirmed |
|------|--------|-----------|
| `src/Domain/Booking/BookingValidator.php` | modify | ✅ User confirmed |
| `src/Application/Booking/BookingService.php` | modify | ✅ User confirmed |
| `translations/messages.fr.yaml` | modify | ✅ User confirmed |
| `tests/Unit/Domain/Booking/BookingValidatorTest.php` | modify | ✅ User confirmed |

**Code written:** ✅

### 4.3 Deviations from plan

None. Implementation followed the plan exactly.

---

## 5. Inspect — Tests & Verification

### 5.1 Tests executed

- [x] Test 29-day booking → accepted ✅
- [x] Test 30-day booking → accepted ✅
- [x] Test 31-day booking → rejected with correct message ✅
- [x] Test premium rental 45-day booking → accepted (not affected) ✅

### 5.2 Test results

- Tests run: `php bin/phpunit tests/Unit/Domain/Booking/BookingValidatorTest.php`
- Result: ✅ PASS (4 tests, 4 assertions)
- Notes: All boundary conditions verified

### 5.3 Validation results (--validate)

| Check | Tool | Result |
|-------|------|--------|
| Lint | PHPStan level 8 | ✅ Pass (0 errors) |
| Type-check | Psalm | ✅ Pass |
| Security | Snyk | ✅ Pass (no vulnerabilities) |

Overall validation: ✅ PASS

---

## 6. Feature Document Update

- Feature slug: `max-stay-length-validation`
- Feature document: `docs/features/max-stay-length-validation.md`
- Updates applied:
  - `## 2. Technical Plan — EPCI-1` → added "EPCI-Soft plan — 2025-01-15"
  - `## 3. Final Report — EPCI-3` → added completion note with flags/persona

> Sections enriched, not overwritten.

---

## 7. Wrap-up — Commit & PR

### 7.1 Suggested commit message

```text
feat(booking): add max stay length validation (30 days)
```

### 7.2 Suggested PR description

```markdown
## Summary
- Add max stay length validation on booking form (30 days)
- Display user-friendly error message on violation
- Premium rentals unaffected

## Changes
- Added `MAX_STAY_DAYS` constant and validation method
- Integrated validation in BookingService
- Added French error message

## Tests
- Unit tests for boundary conditions (29/30/31 days)
- Verified premium rentals not affected

## Validation (v2.7)
- PHPStan: ✅ Pass
- Psalm: ✅ Pass
- Snyk: ✅ Pass
```

### 7.3 Git commands

```bash
git status
git diff
# review changes

git add src/Domain/Booking/BookingValidator.php \
        src/Application/Booking/BookingService.php \
        translations/messages.fr.yaml \
        tests/Unit/Domain/Booking/BookingValidatorTest.php \
        docs/features/max-stay-length-validation.md

git commit -m "feat(booking): add max stay length validation (30 days)"
git push
```

---

## 8. Workflow Complete (v2.7)

```text
✅ EPCI-Soft workflow complete for feature: max-stay-length-validation

Configuration:
- Flags: --safe-mode, --validate
- Persona: --persona-backend

Results:
- Files modified: 4
- Tests: ✅ PASS (4 tests, 4 assertions)
- Validation: ✅ PASS

Feature Document: docs/features/max-stay-length-validation.md
```
````

---

## 8. Summary

`epci-soft` is the **middle tier** of the EPCI workflow:

- It keeps the EPCI philosophy (**Explore → Plan → Code → Inspect**),
- Compresses it into a **single, complete command** suitable for SMALL changes,
- **Actually implements the code** (not just guidance),
- Validates **FEATURE_SLUG** consistently,
- Documents **deviations from plan** when they occur,
- Integrates cleanly with the **Feature Document** (`docs/features/<feature-slug>.md`),
- Ensures each SMALL change still has:
    - a clear objective,
    - a light technical plan,
    - actual implementation,
    - minimal tests,
    - and a trace in documentation and version control.

In **INTERACTIVE mode**, the workflow has two phases:

- **Phase A** — Explore & Plan (read-only, NO file writes, wait for validation),
- **Phase B** — Code & Inspect (after user confirms the plan).

In **AUTO mode**, all steps are executed in a single pass.

It must remain **strict** on scope (SMALL only) while giving developers a **productive, low-friction path** for everyday enhancements.

When in doubt about complexity, **reroute to the full EPCI workflow**.

**v2.7 improvements:**

- **Universal flags support:** `--preview`, `--safe-mode`, `--dry-run`, `--validate`, `--uc`, `--verbose`, `--introspect`
- **Persona system:** All 7 personas with auto-activation based on file patterns
- **Safe-mode:** Confirmation prompts before each file modification
- **Validation integration:** Lint, type-check, security scan with `--validate`
- **Introspection:** Plan reasoning visible with `--introspect`
- **Enhanced output:** Active configuration section, validation results, workflow complete summary
- **Reroute with personas:** Suggests relevant personas when escalating to full EPCI

**Previous improvements (preserved):**

- Thinking mode hierarchy documented (think < think hard < think harder < ultrathink)
- Sub-agents pattern for exploration without context pollution
- Effort guideline: ~30-90 minutes for a senior developer

---

## 9. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-flags.md` | Universal flags reference |
| `epci-personas.md` | Expert personas system |
| `epci-workflow-guide.md` | Complete workflow documentation |
| `epci-micro.md` | TINY changes workflow |
| `epci-1-analyse.md` | Full EPCI - Explore & Plan |

---

*This document is part of the EPCI v2.7 workflow system.*
