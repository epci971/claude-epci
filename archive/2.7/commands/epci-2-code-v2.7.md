# epci-2-code — Code & Test (Full EPCI Workflow) (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> `epci-2-code` is the **second step** of the full EPCI workflow for **STANDARD** and **LARGE** changes.
>
> This command **implements the code** and **runs tests** based on the plan produced by `epci-1-analyse`.
> It **writes actual code** to the repository.

---

## Critical Rules

- ⚠️ `epci-2-code` MUST write actual code to the repository
- ⚠️ ONLY modify files listed in the plan's "Proposed Changes"
- ⚠️ Phase A (INTERACTIVE) = NO code writes, wait for validation
- ⚠️ NEVER modify `## 1. Functional Brief` or `## 3. Final Report`
- ⚠️ Document ALL deviations from the plan
- ⚠️ `--safe-mode` requires confirmation before each file modification
- ⚠️ No section before `## 1.` and no section after `## 6.`

---

## 1. Purpose & Responsibilities

`epci-2-code` is responsible for:

1. **Reading the implementation plan** from the Feature Document (`## 2. Technical Plan — EPCI-1`).

2. **Implementing the code** according to the plan:
   - Follow the file-by-file breakdown,
   - Respect existing patterns and conventions,
   - Write actual code to the repository.

3. **Running tests** to verify the implementation:
   - Execute automated tests (unit, integration, e2e),
   - **Test all edge cases defined in the plan** (section 3.5),
   - Document test results,
   - Fix issues if tests fail.

4. **Updating the Feature Document** if deviations from the plan occur:
   - Document what changed vs the original plan,
   - Add `### Implementation Notes` subsection in `## 2. Technical Plan`.

5. **Suggesting the next command** (`epci-3-finalize`) with explicit parameters.

**Critical constraints:**

- `epci-2-code` **MUST write actual code** to the repository.
- `epci-2-code` **MUST run tests** (or document how to run them).
- `epci-2-code` **MUST follow the plan** as closely as possible.
- `epci-2-code` **MUST NOT modify `## 1. Functional Brief` or `## 3. Final Report`** sections.
- `epci-2-code` **MUST NOT modify unrelated files** (only files listed in the plan).
- `epci-2-code` **MUST NOT create commits or PRs** (that's `epci-3-finalize`'s job).

---

## 2. Inputs, Modes & Flags

### 2.1 `$ARGUMENTS`

`epci-2-code` expects the following inputs:

```text
$ARGUMENTS=<EPCI_READY_BRIEF>
  FEATURE_TITLE: <human-readable title>
  FEATURE_SLUG: <kebab-case-slug>
  OBJECTIVE: <concise goal>
  CONTEXT: <ticket refs, modules, URLs>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ...
  CONSTRAINTS: <technical or business constraints>
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS: <if any>
```

Required fields:
- `FEATURE_SLUG` (string, required) — canonical slug for the feature (kebab-case).
- `PLAN_PATH` (string, optional) — path to the Feature Document. Defaults to `docs/features/<feature-slug>.md`.

From these inputs, `epci-2-code` will:

1. Locate the Feature Document at `docs/features/<feature-slug>.md`.
2. Read the plan from `## 2. Technical Plan — EPCI-1`.
3. Extract the implementation checklist and file-by-file breakdown.

**If the Feature Document is missing:**
- **STOP** and ask the user to run `epci-0-briefing` and `epci-1-analyse` first.
- Do NOT create the Feature Document (that's `epci-0`'s job).
- Do NOT proceed without a validated plan.

**If the plan section (`## 2. Technical Plan`) is empty or missing:**
- **STOP** and ask the user to run `epci-1-analyse` first.
- Do NOT proceed without a validated plan.

### 2.2 Universal Flags

`epci-2-code` supports the following **universal flags**:

#### Safety Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--preview` | Show what would be done without executing | Lists all files that would be modified, estimated LOC, tests to run |
| `--safe-mode` | Require confirmation before each file modification | Prompts "Modify `src/User.php`? [y/n]" before each write |
| `--dry-run` | Simulate the entire implementation | Full output but no actual file writes |
| `--validate` | Run extra validation checks | Lint, type-check, security scan before commit |

#### Output Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--uc` | Ultra-compressed output | Reduces verbosity by ~70%, key info only |
| `--verbose` | Detailed output | Shows all code diffs, full test output |

#### Debug Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--introspect` | Show reasoning process | Displays decision logic for implementation choices |

**Examples:**

```bash
# Preview what would be implemented
epci-2-code FEATURE_SLUG=user-auth --preview

# Safe mode with confirmations
epci-2-code FEATURE_SLUG=payment-flow --safe-mode

# Dry run with validation
epci-2-code FEATURE_SLUG=api-refactor --dry-run --validate

# Compressed output for CI/CD
epci-2-code FEATURE_SLUG=small-fix --uc
```

### 2.3 Persona Flags

Activate specialized expertise during implementation:

| Flag | Persona | Specialization | Auto-activation |
|------|---------|----------------|-----------------|
| `--persona-backend` | Backend Architect | API, DB, business logic | PHP, Python, Node.js files |
| `--persona-frontend` | Frontend Architect | UI/UX, React, Vue | JSX, TSX, CSS files |
| `--persona-security` | Security Engineer | Vulnerabilities, auth | Auth, crypto, data handling |
| `--persona-performance` | Performance Engineer | Optimization, profiling | Hot paths, DB queries |
| `--persona-qa` | Quality Engineer | Testing, validation | Test files |

**Auto-activation rules:**

- Files in `src/Security/`, `src/Auth/` → `--persona-security`
- Files in `src/Controller/`, `src/Api/` → `--persona-backend`
- Files in `assets/`, `templates/`, `*.tsx` → `--persona-frontend`
- Hot paths, caching, queries → `--persona-performance`
- Test files → `--persona-qa`

**Manual override:**

```bash
# Force security focus on all files
epci-2-code FEATURE_SLUG=user-profile --persona-security

# Combine personas for full-stack
epci-2-code FEATURE_SLUG=checkout --persona-backend --persona-frontend
```

### 2.4 Execution Modes & Phases

`epci-2-code` supports `EXECUTION_MODE`:

- `"INTERACTIVE"` (default):
  - **Phase A — Plan Review (read-only, NO code writes)**:
    - Read and summarize the plan from the Feature Document.
    - Present the implementation strategy.
    - Confirm understanding with the user.
    - **⚠️ STOP HERE. Do NOT write any code. Wait for user validation.**
  
  - **Phase B — Implementation (after explicit user validation)**:
    - User confirms to proceed.
    - Validate FEATURE_SLUG.
    - Implement the code file by file.
    - Run tests (including all edge cases from plan).
    - Document results.
    - Update Feature Document if deviations.
    - Suggest next command.

- `"AUTO"`:
  - Single-pass workflow.
  - Read plan → Implement → Test → Document in one go.
  - Use AUTO only when the plan is clear and the context is controlled.
  - **All deviations MUST be explicitly documented in Implementation Notes.**

> **Code execution guarantee:**  
> In both modes, `epci-2-code` **writes actual code** to the repository in Phase B (or directly in AUTO mode).
> Exception: `--preview` and `--dry-run` flags prevent actual writes.

### 2.5 Flag Combinations

| Combination | Use Case |
|-------------|----------|
| `--preview --verbose` | Detailed preview of all changes |
| `--safe-mode --validate` | Maximum safety for critical code |
| `--dry-run --introspect` | Understand implementation reasoning without executing |
| `--uc --validate` | CI/CD pipeline with validation |
| `--persona-security --validate` | Security-focused implementation with checks |

---

## 3. Output Layout (assistant message)

For IDE / terminal readability, `epci-2-code` MUST follow this **fixed layout**.

### 3.1 Standard Output

````markdown
## 1. Plan Summary

- Feature: `<feature-slug>`
- Feature Document: `docs/features/<feature-slug>.md`
- Scope: ... (1-2 sentences)
- Files to modify: X files
- Estimated complexity: STANDARD / LARGE
- Active personas: <persona-backend>, <persona-security> (if any)
- Flags: <--safe-mode>, <--validate> (if any)

### Implementation Checklist (from plan)

- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...
- ...

### Edge Cases to Test (from plan section 3.5)

- Edge case 1: ... → expected behaviour: ...
- Edge case 2: ... → expected behaviour: ...
- ...

---

## 2. Implementation

> Only files listed in the plan are modified. No unrelated changes.

### 2.1 File: `path/to/file1`

**Change type:** new / modify / delete
**Persona:** <persona-backend> (if applicable)

**Changes made:**
- ...

**Code written:** ✅

### 2.2 File: `path/to/file2`

**Change type:** new / modify / delete
**Persona:** <persona-frontend> (if applicable)

**Changes made:**
- ...

**Code written:** ✅

... (repeat for each file)

### 2.X Deviations from Plan

| Planned | Actual | Reason |
|---------|--------|--------|
| ... | ... | ... |

*(If no deviations: "None. Implementation followed the plan exactly.")*

> All deviations listed here MUST also be documented in Implementation Notes (section 5).

---

## 3. Testing

### 3.1 Automated Tests

| Test | Command | Result |
|------|---------|--------|
| Unit tests | `php bin/phpunit tests/Unit/...` | ✅ Pass / ❌ Fail |
| Integration tests | `php bin/phpunit tests/Integration/...` | ✅ Pass / ❌ Fail |
| ... | ... | ... |

### 3.2 Edge Cases Coverage (from plan section 3.5)

| Edge Case | Test | Result |
|-----------|------|--------|
| Zero nights | `StayTaxCalculatorTest::testZeroNights` | ✅ Pass |
| Missing category | `StayTaxCalculatorTest::testMissingCategory` | ✅ Pass |
| ... | ... | ... |

### 3.3 Manual Verification (if applicable)

- [ ] Scenario 1: ...
- [ ] Scenario 2: ...

### 3.4 Test Failures & Fixes

*(If tests failed, document the issue and the fix applied.)*
*(If fix required deviation from plan, add to section 2.X and Implementation Notes.)*

### 3.5 Validation Results (if --validate flag)

| Check | Tool | Result |
|-------|------|--------|
| Lint | PHPStan / ESLint | ✅ Pass / ❌ Fail |
| Type-check | TypeScript / Psalm | ✅ Pass / ❌ Fail |
| Security | Snyk / OWASP | ✅ Pass / ⚠️ Warnings |

---

## 4. Updated Checklist

- [x] Step 1: ... ✅
- [x] Step 2: ... ✅
- [x] Step 3: ... ✅
- [ ] Step 4: ... (if not completed, explain why)
- ...

---

## 5. Feature Document Update

### 5.1 Sections Modified

- Section updated: `## 2. Technical Plan — EPCI-1` (added Implementation Notes)

> **Sections `## 1. Functional Brief` and `## 3. Final Report` are NOT modified.**

### 5.2 Implementation Notes Added

*(Only if deviations occurred. Otherwise: "No deviations. Implementation Notes not needed.")*

```markdown
### Implementation Notes — <YYYY-MM-DD>

**Author:** epci-2-code
**Personas used:** <persona-backend>, <persona-security>
**Flags:** <--safe-mode>, <--validate>

**Deviations from original plan:**
- Deviation 1: <planned> → <actual> — Reason: ...
- Deviation 2: <planned> → <actual> — Reason: ...

**Files added (not in original plan):**
- `path/to/new/file.php` — Reason: ...

**Files removed (not in original plan):**
- None

**Additional edge cases discovered:**
- Edge case X: ... → handled by: ...

**Test coverage:**
- Unit: X%
- Integration: Y%

**Validation results:**
- Lint: ✅ Pass
- Security: ✅ Pass
```

---

## 6. Next Command

```text
To finalize documentation and prepare the commit, run:

epci-3-finalize
FEATURE_SLUG=<feature-slug>
PLAN_PATH=docs/features/<feature-slug>.md
$ARGUMENTS=<EPCI_READY_BRIEF or brief summary>
```

Implementation complete. Ready for finalization.
````

### 3.2 Ultra-Compressed Output (--uc flag)

When `--uc` flag is active, output is condensed:

````markdown
## EPCI-2: <feature-slug>

**Plan:** docs/features/<feature-slug>.md | **Files:** 5 | **Complexity:** STANDARD
**Personas:** backend, security | **Flags:** --safe-mode, --validate

### Implementation
| File | Type | Status |
|------|------|--------|
| `src/Domain/Calculator.php` | new | ✅ |
| `src/Service/BookingService.php` | modify | ✅ |
| `tests/CalculatorTest.php` | new | ✅ |

**Deviations:** 1 (exception class added)

### Tests
Unit: 15/15 ✅ | Integration: 3/3 ✅ | Edge cases: 3/3 ✅
Validation: Lint ✅ | Types ✅ | Security ✅

### Next
`epci-3-finalize FEATURE_SLUG=<feature-slug>`
````

### 3.3 Preview Output (--preview flag)

When `--preview` flag is active:

````markdown
## EPCI-2 Preview: <feature-slug>

**⚠️ PREVIEW MODE — No files will be modified**

### Would Modify

| File | Action | Est. LOC | Persona |
|------|--------|----------|---------|
| `src/Domain/Calculator.php` | create | ~80 | backend |
| `src/Service/BookingService.php` | modify | ~20 | backend |
| `config/tax_rates.yaml` | create | ~15 | — |
| `tests/CalculatorTest.php` | create | ~120 | qa |

**Total:** 4 files, ~235 LOC

### Would Test

- Unit tests: `tests/Unit/Domain/` (est. 12 tests)
- Integration tests: `tests/Integration/Booking/` (est. 3 tests)
- Edge cases: 3 scenarios

### Validation Would Run

- PHPStan level 8
- Psalm strict mode
- Security audit (Snyk)

---

**To execute, run without --preview flag.**
````

### 3.4 Introspect Output (--introspect flag)

When `--introspect` flag is active, add reasoning blocks:

````markdown
## 2. Implementation

### 2.1 File: `src/Domain/Booking/StayTaxCalculator.php`

> 🎯 **Decision Logic:**
> - Detected: Tax calculation = financial logic → **--persona-backend** activated
> - Pattern match: Project uses Money pattern (found in `src/Domain/Money.php`)
> - Convention: Domain services are stateless, injected via DI
> - Risk assessment: Low (isolated domain logic, no side effects)

**Change type:** new
**Persona:** <persona-backend>

**Changes made:**
- Created `StayTaxCalculator` service following existing Money pattern
- Used constructor injection for `TaxRateRepository`
- Implemented `calculate(int $nights, string $category): Money`

**Code written:** ✅
````

---

## 4. Behaviour Step-by-step

### 4.1 Step 1 — Read & Summarize the Plan

1. **Locate the Feature Document:**
   - Path: `docs/features/<feature-slug>.md`
   - **If not found → STOP** and ask the user to run `epci-0-briefing` first.

2. **Read the plan section:**
   - Section: `## 2. Technical Plan — EPCI-1`
   - **If empty or missing → STOP** and ask the user to run `epci-1-analyse` first.
   - Extract:
     - Scope & Goal,
     - Proposed Changes (file by file),
     - Control & Data Flow,
     - Edge Cases & Error Handling (section 3.5),
     - Testing Strategy,
     - Implementation Checklist.

3. **Detect personas** (if not manually specified):
   - Analyze file types and paths
   - Auto-activate relevant personas
   - Display in output header

4. **Apply flags** (if specified):
   - `--preview`: Skip to preview output
   - `--dry-run`: Mark all outputs as simulated
   - `--uc`: Use compressed output format

5. **Summarize for user confirmation** (in INTERACTIVE mode):
   - List files to be modified.
   - List edge cases to test.
   - Present the implementation checklist.
   - Show active personas and flags.
   - **STOP** and wait for user validation.

### 4.2 Step 2 — Validate FEATURE_SLUG

Before implementing, validate the `FEATURE_SLUG`:

1. Confirm it is in **kebab-case** (lowercase, hyphens only).
2. Confirm the Feature Document exists at `docs/features/<feature-slug>.md`.
3. Confirm the plan section is populated.

If invalid, stop and ask for clarification.

### 4.3 Step 3 — Implement the Code

**Actually implement the changes** by writing/modifying files in the repository.

**For each file in the plan:**

1. **Identify the change type**: new / modify / delete.
2. **Activate relevant persona** for the file type.
3. **If `--safe-mode`**: Prompt for confirmation before writing.
4. **Apply the changes** following:
   - The plan's description,
   - Existing patterns and conventions,
   - The project's coding standards,
   - Persona-specific best practices.
5. **Document what was done** in section 2.X of the output.
6. **Confirm code was written** with "Code written: ✅".

**Rules:**

- ONLY modify files listed in the plan.
- If a new file is needed that was NOT in the plan, document it as a deviation.
- If a planned file change is not needed, document it as a deviation.
- Follow existing patterns exactly.
- If `--dry-run`, show what would be written but don't write.

### 4.4 Step 4 — Run Tests

**Execute tests** to verify the implementation:

1. **Automated tests:**
   - Run unit tests for new/modified code.
   - Run integration tests if applicable.
   - Document commands and results.

2. **Edge cases coverage:**
   - Explicitly verify each edge case from plan section 3.5.
   - Map each edge case to a specific test.
   - Document results.

3. **Sub-agent verification (recommended for complex implementations):**
   
   > 💡 **Anti-overfitting check:** Use an independent sub-agent to verify that the implementation isn't overfitting to the tests and handles real-world scenarios properly.
   
   ```
   "Use an independent sub-agent to review the implementation and verify:
   - The code handles edge cases not covered by tests
   - The implementation follows project conventions
   - No obvious security or performance issues
   - The solution is general, not overfitted to test cases"
   ```

4. **Validation checks** (if `--validate` flag):
   - Run linter (PHPStan, ESLint, etc.)
   - Run type checker (Psalm, TypeScript, etc.)
   - Run security scanner (Snyk, OWASP, etc.)
   - Document all results.

5. **Manual verification:**
   - If automated tests are not sufficient, list manual scenarios to verify.
   - Mark as completed or pending.

6. **Handle failures:**
   - If tests fail, fix the issue.
   - Document the fix.
   - If the fix required deviating from the plan, document the deviation.

### 4.5 Step 5 — Document Deviations

If ANY deviation from the plan occurred:

1. **List deviations** in section 2.X of the output.
2. **Add Implementation Notes** to the Feature Document.

**Deviation examples:**

- File added that was not in the plan.
- File removed that was planned.
- Different implementation approach than planned.
- Additional edge case discovered.
- Test strategy changed.

**Implementation Notes format:**

```markdown
### Implementation Notes — <YYYY-MM-DD>

**Author:** epci-2-code
**Personas used:** <persona-backend>, <persona-security>
**Flags:** <--safe-mode>, <--validate>

**Deviations from original plan:**
- Deviation 1: <planned> → <actual> — Reason: ...

**Files added (not in original plan):**
- `path/to/file` — Reason: ...

**Files removed (not in original plan):**
- None

**Additional edge cases discovered:**
- Edge case X: ... → handled by: ...

**Test coverage:**
- Unit: X%
- Integration: Y%

**Validation results:**
- Lint: ✅ Pass
- Security: ✅ Pass
```

### 4.6 Step 6 — Feature Document Update

Update the Feature Document at `docs/features/<feature-slug>.md`:

**Critical rule:**

> **NEVER modify `## 1. Functional Brief` or `## 3. Final Report`.**  
> Only add to `## 2. Technical Plan` if needed (Implementation Notes).

**Behaviour:**

1. **If deviations occurred:**
   - Add `### Implementation Notes` subsection to `## 2. Technical Plan`.

2. **If no deviations:**
   - No changes needed to the Feature Document.
   - State: "No deviations. Implementation Notes not needed."

3. **Use the available file tools** to write updates.

### 4.7 Step 7 — Next Command Suggestion

At the end of the command, **explicitly suggest the next command**:

````markdown
## 6. Next Command

```text
To finalize documentation and prepare the commit, run:

epci-3-finalize
FEATURE_SLUG=<feature-slug>
PLAN_PATH=docs/features/<feature-slug>.md
$ARGUMENTS=<EPCI_READY_BRIEF or brief summary>
```

Implementation complete. Ready for finalization.
````

**Then STOP.**

- Do NOT create commits or PRs.
- Do NOT write final documentation (that's `epci-3-finalize`'s job).

---

## 5. Guardrails: Scope Validation

During implementation, `epci-2-code` MUST validate that the task matches the expected complexity.

### 5.1 If scope is SMALLER than expected

If during implementation you realize the task is actually **TINY** or **SMALL**:

- Fewer files than expected,
- Less code than expected,
- No edge cases,

Then:
- Complete the implementation anyway (you've already started).
- Note in section 5 that the full EPCI workflow may have been overkill.
- Suggest using `epci-micro` or `epci-soft` for similar tasks in the future.

### 5.2 If scope is LARGER than expected

If during implementation the task reveals:

- More files to modify than planned,
- More complex logic than anticipated,
- Missing requirements or edge cases,
- Schema changes not in the plan,

Then:

1. **STOP implementation** on the unexpected parts.
2. Document the scope creep in section 2.X (Deviations).
3. Flag the risks in section 5.
4. Recommend updating the plan before continuing.
5. Ask the user how to proceed.

**Do NOT proceed with unplanned changes without user confirmation.**

### 5.3 Complexity reference grid

| Level | Files | LOC | Risk | Modules | Workflow |
|-------|-------|-----|------|---------|----------|
| **TINY** | 1 (max 2) | < 50 | Very low | 1 | `epci-micro` |
| **SMALL** | 2–3 | 50–200 | Low | 1 | `epci-soft` |
| **STANDARD** | 3–10 | 200–1000 | Medium | 1–3 | `epci-1` → `epci-2` → `epci-3` |
| **LARGE** | > 10 | > 1000 | High | > 3 | `epci-1` → `epci-2` → `epci-3` |

---

## 6. Example — Implementation Session

Below is a **concrete example** of an `epci-2-code` session with flags and personas.

````markdown
## 1. Plan Summary

- Feature: `stay-tax-calculation`
- Feature Document: `docs/features/stay-tax-calculation.md`
- Scope: Implement stay tax calculation for seasonal rentals
- Files to modify: 5 files
- Estimated complexity: STANDARD
- Active personas: `--persona-backend` (auto), `--persona-qa` (auto)
- Flags: `--safe-mode`, `--validate`

### Implementation Checklist (from plan)

- [ ] Create `StayTaxCalculator` with `calculate(int $nights, string $category): Money`
- [ ] Add tax rates configuration
- [ ] Integrate into `BookingService`
- [ ] Update `Booking` entity to store tax amount
- [ ] Modify invoice template
- [ ] Modify booking summary template
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update API documentation

### Edge Cases to Test (from plan section 3.5)

- Zero nights → tax = 0
- Property without category → use default rate
- Tax rate not configured → throw `TaxConfigurationException`

---

## 2. Implementation

> Only files listed in the plan are modified. No unrelated changes.
> **--safe-mode active:** Each file modification confirmed.

### 2.1 File: `src/Domain/Booking/StayTaxCalculator.php`

**Change type:** new
**Persona:** `--persona-backend`
**Confirmation:** ✅ User confirmed

**Changes made:**
- Created `StayTaxCalculator` service
- Implemented `calculate(int $nights, string $category): Money` method
- Added tax rate lookup from configuration

**Code written:** ✅

### 2.2 File: `config/packages/tax_rates.yaml`

**Change type:** new
**Confirmation:** ✅ User confirmed

**Changes made:**
- Created tax rates configuration file
- Defined rates for categories: standard, luxury, budget

**Code written:** ✅

### 2.3 File: `src/Application/Booking/BookingService.php`

**Change type:** modify
**Persona:** `--persona-backend`
**Confirmation:** ✅ User confirmed

**Changes made:**
- Injected `StayTaxCalculator` dependency
- Added tax calculation call in `createBooking()` method
- Stored tax amount in `Booking` entity

**Code written:** ✅

### 2.4 File: `templates/booking/summary.html.twig`

**Change type:** modify
**Persona:** `--persona-frontend`
**Confirmation:** ✅ User confirmed

**Changes made:**
- Added tax breakdown display
- Updated total calculation to include tax

**Code written:** ✅

### 2.5 File: `tests/Unit/Domain/Booking/StayTaxCalculatorTest.php`

**Change type:** new
**Persona:** `--persona-qa`
**Confirmation:** ✅ User confirmed

**Changes made:**
- Created unit test class
- Added tests for: 1-night stay, 7-night stay, 30-night stay
- Added tests for each property category
- Added edge case tests: zero nights, missing category, unconfigured rate

**Code written:** ✅

### 2.X Deviations from Plan

| Planned | Actual | Reason |
|---------|--------|--------|
| Modify invoice template | Deferred to next PR | Invoice template requires design review first |
| — | Added `TaxConfigurationException.php` | Needed for edge case "rate not configured" |

> These deviations are documented in Implementation Notes (section 5.2).

---

## 3. Testing

### 3.1 Automated Tests

| Test | Command | Result |
|------|---------|--------|
| Unit tests | `php bin/phpunit tests/Unit/Domain/Booking/` | ✅ Pass (15 tests) |
| Integration tests | `php bin/phpunit tests/Integration/Booking/` | ✅ Pass (3 tests) |

### 3.2 Edge Cases Coverage (from plan section 3.5)

| Edge Case | Test | Result |
|-----------|------|--------|
| Zero nights | `StayTaxCalculatorTest::testZeroNights` | ✅ Pass |
| Property without category | `StayTaxCalculatorTest::testMissingCategory` | ✅ Pass |
| Tax rate not configured | `StayTaxCalculatorTest::testUnconfiguredRate` | ✅ Pass |

### 3.3 Manual Verification

- [x] Create booking with 3-night stay → tax correctly calculated
- [x] Verify tax appears on booking summary page
- [ ] Invoice template (deferred)

### 3.4 Test Failures & Fixes

None. All tests passed on first run.

### 3.5 Validation Results (--validate flag)

| Check | Tool | Result |
|-------|------|--------|
| Lint | PHPStan level 8 | ✅ Pass (0 errors) |
| Type-check | Psalm | ✅ Pass |
| Security | Snyk | ✅ Pass (no vulnerabilities) |

---

## 4. Updated Checklist

- [x] Create `StayTaxCalculator` ✅
- [x] Add tax rates configuration ✅
- [x] Integrate into `BookingService` ✅
- [x] Update `Booking` entity ✅
- [ ] Modify invoice template ⏸️ (deferred — needs design review)
- [x] Modify booking summary template ✅
- [x] Write unit tests ✅
- [x] Write integration tests ✅
- [ ] Update API documentation (will be done in epci-3-finalize)

---

## 5. Feature Document Update

### 5.1 Sections Modified

- Section updated: `## 2. Technical Plan — EPCI-1` (added Implementation Notes)

> **Sections `## 1. Functional Brief` and `## 3. Final Report` are NOT modified.**

### 5.2 Implementation Notes Added

```markdown
### Implementation Notes — 2025-01-15

**Author:** epci-2-code
**Personas used:** --persona-backend, --persona-frontend, --persona-qa
**Flags:** --safe-mode, --validate

**Deviations from original plan:**
- Invoice template modification deferred to next PR — Reason: requires design review
- Added exception class not in original plan — Reason: needed for edge case handling

**Files added (not in original plan):**
- `src/Domain/Booking/Exception/TaxConfigurationException.php` — Reason: edge case "rate not configured"

**Files removed (not in original plan):**
- None

**Additional edge cases discovered:**
- None (all edge cases were in the plan)

**Test coverage:**
- Unit: 94%
- Integration: 87%

**Validation results:**
- PHPStan: ✅ Pass (level 8)
- Psalm: ✅ Pass
- Snyk: ✅ Pass (no vulnerabilities)
```

---

## 6. Next Command

```text
To finalize documentation and prepare the commit, run:

epci-3-finalize
FEATURE_SLUG=stay-tax-calculation
PLAN_PATH=docs/features/stay-tax-calculation.md
$ARGUMENTS=Stay tax calculation for seasonal rentals
```

Implementation complete. Ready for finalization.
````

---

## 7. Summary

`epci-2-code` is the **implementation phase** of the full EPCI workflow:

- It keeps the EPCI philosophy (**Explore → Plan → Code → Inspect**),
- It **reads the plan** from the Feature Document,
- It **writes actual code** to the repository,
- It **only modifies files listed in the plan** (no unrelated changes),
- It **runs tests** including all edge cases from the plan,
- It **updates the Feature Document** with Implementation Notes if deviations occur,
- It **never modifies** `## 1. Functional Brief` or `## 3. Final Report`,
- It suggests the **next command** with complete parameters.

In **INTERACTIVE mode**, the workflow has two phases:
- **Phase A** — Read & summarize plan (read-only, NO code writes, wait for validation),
- **Phase B** — Validate FEATURE_SLUG, implement code, run tests (after user confirms).

In **AUTO mode**, all steps are executed in a single pass.

The implementation must **follow the plan** as closely as possible. Any deviation must be documented in both the output (section 2.X) and the Feature Document (Implementation Notes).

**v2.7 improvements:**

- **Universal flags:** `--preview`, `--safe-mode`, `--dry-run`, `--validate`, `--uc`, `--verbose`, `--introspect`
- **Persona system:** Auto-activation based on file types, manual override with `--persona-*` flags
- **Enhanced output formats:** Standard, ultra-compressed (--uc), preview (--preview), introspect (--introspect)
- **Validation integration:** Lint, type-check, security scan with `--validate` flag
- **Sub-agent verification:** Anti-overfitting pattern for complex implementations
- **Safe mode:** Confirmation prompts before each file modification
