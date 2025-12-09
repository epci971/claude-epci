# epci-3-finalize — Inspect & Document (Full EPCI Workflow) (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> `epci-3-finalize` is the **final step** of the full EPCI workflow for **STANDARD** and **LARGE** changes.
>
> This command **inspects the implementation**, **prepares documentation**, and **finalizes the feature**.
> It does **NOT** implement new features or perform refactors.

---

## Critical Rules

- ⚠️ Prerequisites: `epci-1-analyse` and `epci-2-code` MUST be completed first
- ⚠️ `epci-3-finalize` does NOT implement new features or refactor
- ⚠️ ONLY update `## 3. Final Report` in the Feature Document
- ⚠️ NEVER modify `## 1. Functional Brief` or `## 2. Technical Plan`
- ⚠️ NEVER commit unrelated files — compare with plan + implementation notes
- ⚠️ Phase A (INTERACTIVE) = NO file writes, wait for validation
- ⚠️ `--validate` runs final quality checks before commit preparation
- ⚠️ No section before `## 1.` and no section after `## 8.`

---

## 1. Purpose & Responsibilities

`epci-3-finalize` is responsible for:

1. **Inspecting the implementation** produced by `epci-2-code`:
   - Verify that the plan was followed,
   - Audit changes vs plan + implementation notes,
   - Review the code changes,
   - Check test results.

2. **Preparing documentation**:
   - README updates,
   - Changelog entries,
   - API documentation,
   - ADRs if needed.

3. **Generating a PR-ready report**:
   - Scope & Goal,
   - Changes summary,
   - Testing summary,
   - Impacts & Risks.

4. **Preparing commit and git commands**:
   - Conventional commit message(s),
   - Git commands to stage, commit, and push.

5. **Updating the Feature Document** (`docs/features/<feature-slug>.md`):
   - Populate the `## 3. Final Report — EPCI-3` section with the final report.

**Prerequisites:**
> `epci-1-analyse` and `epci-2-code` MUST be completed successfully before running `epci-3-finalize`.

**Critical constraints:**

- `epci-3-finalize` **MUST NOT implement new features**.
- `epci-3-finalize` **MUST NOT perform refactors**.
- `epci-3-finalize` **MAY apply minimal fixes** (typos, doc adjustments) if clearly justified.
- `epci-3-finalize` **MUST NOT modify `## 1. Functional Brief` or `## 2. Technical Plan`** sections under any circumstances.
- `epci-3-finalize` **MUST NOT ignore manually created files** (docs, configs, assets).
- `epci-3-finalize` **MUST NOT commit unrelated files**.

---

## 2. Inputs, Modes & Flags

### 2.1 `$ARGUMENTS`

`epci-3-finalize` expects the following inputs:

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

From these inputs, `epci-3-finalize` will:

1. Locate the Feature Document at `docs/features/<feature-slug>.md`.
2. Read all sections:
   - `## 1. Functional Brief — EPCI-0`
   - `## 2. Technical Plan — EPCI-1` (including Implementation Notes if present)
3. Inspect the current working tree / diff.

**If the Feature Document is missing:**
- **STOP** and ask the user to run the previous EPCI steps first.

**If the plan section is empty:**
- **STOP** and ask the user to run `epci-1-analyse` and `epci-2-code` first.

### 2.2 Universal Flags

`epci-3-finalize` supports the following **universal flags**:

#### Safety & Quality Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--preview` | Show what would be done without executing | Shows audit, PR description, commit — no writes |
| `--validate` | Run final validation checks | Lint, type-check, security scan, coverage report |
| `--dry-run` | Simulate finalization | Full output but no actual file writes |

#### Output Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--uc` | Ultra-compressed output | Condensed audit + commit commands only |
| `--verbose` | Detailed output | Full diffs, complete audit trail |

#### Debug & Audit Flags

| Flag | Description | Behaviour |
|------|-------------|-----------|
| `--introspect` | Show reasoning process | Displays decision logic for audit findings |
| `--audit-deep` | Extended audit with sub-agent | Independent sub-agent reviews implementation |

**Examples:**

```bash
# Preview finalization without writing
epci-3-finalize FEATURE_SLUG=user-auth --preview

# Full validation before commit
epci-3-finalize FEATURE_SLUG=payment-flow --validate

# Deep audit with sub-agent verification
epci-3-finalize FEATURE_SLUG=security-feature --audit-deep

# Compressed output for CI/CD
epci-3-finalize FEATURE_SLUG=small-fix --uc
```

### 2.3 Persona Flags

Activate specialized expertise during finalization:

| Flag | Persona | Specialization | Use Case |
|------|---------|----------------|----------|
| `--persona-qa` | Quality Engineer | Testing, validation | Audit test coverage |
| `--persona-security` | Security Engineer | Vulnerabilities, auth | Security-focused review |
| `--persona-architect` | System Architect | Design review | Architecture compliance |
| `--persona-devops` | DevOps Engineer | CI/CD, deployment | Deployment readiness |

**Auto-activation rules:**

- Features touching `src/Security/`, auth → `--persona-security`
- Features with > 10 files → `--persona-architect`
- Features with deployment configs → `--persona-devops`
- All features → `--persona-qa` (always active for finalization)

**Manual override:**

```bash
# Security-focused final review
epci-3-finalize FEATURE_SLUG=auth-refactor --persona-security

# Architecture compliance check
epci-3-finalize FEATURE_SLUG=api-redesign --persona-architect --audit-deep
```

### 2.4 Execution Modes & Phases

`epci-3-finalize` supports `EXECUTION_MODE`:

- `"INTERACTIVE"` (default):
  - **Phase A — Inspection (read-only, NO file writes)**:
    - Read the Feature Document (plan + implementation notes).
    - Inspect the working tree / git diff.
    - Audit changes vs plan.
    - Identify all changed files.
    - Prepare the PR description and commit message.
    - Present for user review.
    - **⚠️ STOP HERE. Do NOT write files. Wait for user validation.**
  
  - **Phase B — Finalization (after explicit user validation)**:
    - User confirms the report is correct.
    - Update Feature Document with final report.
    - Apply minimal doc fixes if needed.
    - Provide git commands.

- `"AUTO"`:
  - Single-pass workflow.
  - Inspect → Document → Finalize in one go.
  - Use AUTO only when the implementation is straightforward.

> **No new code guarantee:**  
> In both modes, `epci-3-finalize` never implements new features or refactors.
> Only minimal fixes (typos, doc adjustments) are allowed.

### 2.5 Flag Combinations

| Combination | Use Case |
|-------------|----------|
| `--validate --audit-deep` | Maximum quality assurance |
| `--preview --verbose` | Detailed preview of all finalization steps |
| `--persona-security --validate` | Security-focused final check |
| `--uc --validate` | CI/CD pipeline with validation |
| `--introspect --audit-deep` | Understand audit reasoning |

---

## 3. Output Layout (assistant message)

For IDE / terminal readability, `epci-3-finalize` MUST follow this **fixed layout**.

### 3.1 Standard Output

````markdown
## 1. Inspection Summary

- Feature: `<feature-slug>`
- Feature Document: `docs/features/<feature-slug>.md`
- Prerequisites: epci-1-analyse ✅ | epci-2-code ✅
- Plan status: ✅ Followed / ⚠️ Deviations documented
- Implementation Notes: Present / Not present
- Active personas: <persona-qa>, <persona-security> (if any)
- Flags: <--validate>, <--audit-deep> (if any)

### Files Changed

| File | Status | Description |
|------|--------|-------------|
| `src/...` | modified | ... |
| `tests/...` | new | ... |
| `docs/...` | new | ... |
| ... | ... | ... |

### Manually Created Files (to include in commit)

- `path/to/manual/file` — ...
- *(If none: "No manually created files detected.")*

### Audit vs Plan

| Planned (from §2 Technical Plan) | Actual | Match |
|---------------------------------|--------|-------|
| `src/Domain/...` — new | Created ✅ | ✅ |
| `src/Application/...` — modify | Modified ✅ | ✅ |
| ... | ... | ... |

> All changes MUST correspond to "Proposed Changes" or "Implementation Notes".
> Any unplanned change MUST be flagged.

### Validation Results (if --validate flag)

| Check | Tool | Result | Details |
|-------|------|--------|---------|
| Lint | PHPStan / ESLint | ✅ Pass / ❌ Fail | 0 errors |
| Type-check | Psalm / TypeScript | ✅ Pass / ❌ Fail | — |
| Security | Snyk / OWASP | ✅ Pass / ⚠️ Warnings | — |
| Coverage | PHPUnit | 94% | Above threshold |

### Sub-agent Audit (if --audit-deep flag)

> 🔍 **Independent Review Results:**
> 
> - Requirements coverage: ✅ All FR/AC addressed
> - Security review: ✅ No issues found
> - Performance review: ⚠️ Consider caching for hot path
> - Code quality: ✅ Follows project conventions

---

## 2. PR Description

```markdown
## Scope & Goal

<1-2 paragraphs describing what this feature does>

## Approach

<Brief description of the technical approach>

## Changes

- <change 1>
- <change 2>
- ...

## Testing

- **Automated:**
  - Unit tests: X tests, all passing
  - Integration tests: Y tests, all passing
- **Manual:**
  - <scenario 1>: ✅ verified
  - <scenario 2>: ✅ verified

## Validation (if --validate)

- Lint: ✅ Pass
- Types: ✅ Pass  
- Security: ✅ Pass
- Coverage: 94%

## Impacts & Risks

- <impact/risk 1>
- <impact/risk 2>

## Follow-ups

- <follow-up 1> (out of scope)
- <follow-up 2> (out of scope)
```

---

## 3. Documentation Updates

### 3.1 README

*(If update needed, provide the exact text to add/modify.)*
*(If no update needed: "No README update required.")*

### 3.2 Changelog (mandatory)

```markdown
## [Unreleased]

### Added
- <feature description> (#<issue-number>)
```

### 3.3 API Documentation

*(If applicable, describe what needs to be updated.)*

### 3.4 ADRs

*(If applicable, describe any architecture decision to document.)*

---

## 4. Commit Preparation

> **NEVER commit unrelated files.** Compare with plan + implementation notes + manual files.

### 4.1 Files to Stage

```bash
git add src/Domain/Booking/StayTaxCalculator.php
git add src/Application/Booking/BookingService.php
git add tests/Unit/Domain/Booking/StayTaxCalculatorTest.php
git add docs/features/<feature-slug>.md
# ... (list all files)
```

### 4.2 Files to Exclude (if any)

*(List files that should NOT be committed, with reason.)*
*(If none: "No files to exclude.")*

> Verify that NO unrelated files are staged. Use `git status` to confirm.

### 4.3 Commit Message (conventional commits)

```text
<type>(<scope>): <short summary>

<body - what was done and why>

- <bullet 1>
- <bullet 2>

Refs: #<issue-number>
```

### 4.4 Git Commands

```bash
# Check current status — verify no unrelated files
git status

# Stage all feature files (and ONLY feature files)
git add <list of files>

# Commit with conventional message
git commit -m "<type>(<scope>): <short summary>"

# Push to remote
git push origin <branch-name>

# Create PR (if using GitHub CLI)
gh pr create --title "<type>(<scope>): <short summary>" --body-file docs/features/<feature-slug>.md
```

---

## 5. Feature Document Update

> **NEVER modify `## 1. Functional Brief` or `## 2. Technical Plan` under any circumstances.**

### 5.1 Section to Update

- Section: `## 3. Final Report — EPCI-3`
- Action: **Overwrite with exactly this structure**

### 5.2 Content Written

```markdown
## 3. Final Report — EPCI-3

*(This section is managed by `epci-3-finalize`. Do not modify manually.)*

### Completion Status

- **Date:** <YYYY-MM-DD>
- **Status:** ✅ Complete / ⚠️ Partial (reason)
- **Confidence:** X%
- **PR:** #<number>
- **Commit:** <hash>
- **Personas used:** <persona-qa>, <persona-security>
- **Flags:** <--validate>, <--audit-deep>

### Summary of Changes

- <change 1>
- <change 2>
- ...

### Testing Summary

- Unit tests: X tests, all passing
- Integration tests: Y tests, all passing
- Edge cases: <coverage status>
- Manual verification: ✅ Complete / ⏸️ Pending

### Validation Summary (if --validate)

- Lint: ✅ Pass
- Type-check: ✅ Pass
- Security: ✅ Pass
- Coverage: X%

### Documentation Updates

- README: ✅ Updated / ⏭️ Not needed
- Changelog: ✅ Updated
- API docs: ✅ Updated / ⏭️ Not needed

### Audit vs Plan

- Planned changes: X files
- Actual changes: Y files
- Deviations: <summary>

### Sub-agent Audit (if --audit-deep)

- Requirements: ✅ All covered
- Security: ✅ Reviewed
- Performance: ⚠️ Recommendations noted
- Quality: ✅ Approved

### Impacts & Risks

- <impact 1>
- <risk 1>

### Technical Debt / Residue

- <if any, otherwise "No technical debt introduced.">

### Follow-ups (out of scope)

- [ ] <follow-up 1>
- [ ] <follow-up 2>
```

---

## 6. Final Notes

### Remaining Risks

- <risk 1>
- <risk 2>

### Pre-merge Checklist

- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No console.log / debug statements left
- [ ] No unrelated files in commit
- [ ] Validation passed (if --validate)
- [ ] Sub-agent audit approved (if --audit-deep)

### Post-deployment Checklist

- [ ] Verify feature in staging
- [ ] Monitor logs for errors
- [ ] Verify user-facing behaviour

---

## 7. Next Steps for User

After `epci-3-finalize`, the user should:

1. **Review** the PR description and commit message
2. **Merge** into target branch (after code review)
3. **Deploy** to staging environment
4. **Verify** the feature works as expected
5. **Monitor** logs for any errors
6. **Update** environment-specific documentation if needed
7. **Close** the related ticket/issue

---

## 8. Workflow Complete

```text
✅ EPCI workflow complete for feature: <feature-slug>

Feature Document: docs/features/<feature-slug>.md

All sections populated:
- ## 1. Functional Brief — EPCI-0 ✅
- ## 2. Technical Plan — EPCI-1 ✅
- ## 3. Final Report — EPCI-3 ✅

Prerequisites verified:
- epci-1-analyse ✅
- epci-2-code ✅
- epci-3-finalize ✅

Validation: ✅ Passed (if --validate)
Sub-agent audit: ✅ Approved (if --audit-deep)

Ready for commit, PR, and merge.
```
````

### 3.2 Ultra-Compressed Output (--uc flag)

When `--uc` flag is active, output is condensed:

````markdown
## EPCI-3: <feature-slug>

**Status:** ✅ Complete | **Confidence:** 90%
**Personas:** qa, security | **Flags:** --validate

### Audit
Plan: 5 files | Actual: 6 files (+1 deviation documented)
Validation: Lint ✅ | Types ✅ | Security ✅ | Coverage: 94%

### Commit
```bash
git add src/Domain/... src/Application/... tests/... docs/features/<slug>.md
git commit -m "feat(booking): add stay tax calculation"
git push origin feature/<slug>
```

### PR
**Title:** feat(booking): add stay tax calculation
**Changes:** 6 files, +350 LOC, 18 tests
**Refs:** #123
````

### 3.3 Preview Output (--preview flag)

When `--preview` flag is active:

````markdown
## EPCI-3 Preview: <feature-slug>

**⚠️ PREVIEW MODE — No files will be modified**

### Would Audit

| Planned | Actual | Match |
|---------|--------|-------|
| `StayTaxCalculator.php` — new | ✅ Created | ✅ |
| `BookingService.php` — modify | ✅ Modified | ✅ |
| ... | ... | ... |

**Deviations:** 1 (exception class added, documented)

### Would Write

- Feature Document: `## 3. Final Report` section
- Changelog: Add entry under `[Unreleased]`

### Would Commit

Files: 7 | Message: `feat(booking): add stay tax calculation`

---

**To execute, run without --preview flag.**
````

### 3.4 Introspect Output (--introspect flag)

When `--introspect` flag is active, add reasoning blocks:

````markdown
## 1. Inspection Summary

> 🎯 **Audit Logic:**
> - Comparing Implementation Notes from epci-2-code with actual git diff
> - Detected 1 deviation: `TaxConfigurationException.php` added
> - Deviation justified: documented in Implementation Notes as needed for edge case
> - Verdict: ✅ Acceptable — all deviations are documented

### Audit vs Plan

| Planned | Actual | Match |
|---------|--------|-------|
| 5 files | 6 files | ⚠️ +1 |

> 🔍 **Deviation Analysis:**
> - Extra file: `TaxConfigurationException.php`
> - Reason in Implementation Notes: "Needed for edge case 'rate not configured'"
> - Assessment: Legitimate addition, follows project exception patterns
> - Action: Include in commit, document in Final Report
````

---

## 4. Behaviour Step-by-step

### 4.1 Step 1 — Read Feature Document & Verify Prerequisites

1. **Locate the Feature Document:**
   - Path: `docs/features/<feature-slug>.md`
   - **If not found → STOP** and ask the user to run previous EPCI steps.

2. **Read all sections:**
   - `## 1. Functional Brief — EPCI-0`
   - `## 2. Technical Plan — EPCI-1`
   - Including any `### Implementation Notes` from `epci-2-code`.

3. **Verify prerequisites:**
   - Plan section is populated (EPCI-1 completed).
   - Implementation Notes present if deviations occurred (EPCI-2 completed).
   - **If prerequisites not met → STOP** and ask the user to complete previous steps.

4. **Detect personas** (if not manually specified):
   - Always activate `--persona-qa` for finalization
   - Auto-activate based on feature scope

5. **Apply flags** (if specified):
   - `--preview`: Skip to preview output
   - `--validate`: Run validation checks
   - `--audit-deep`: Prepare sub-agent audit

### 4.2 Step 2 — Inspect Working Tree

1. **Get current diff:**
   - Use `git status` and `git diff` to see all changes.
   
2. **Identify all changed files:**
   - Modified files,
   - New files,
   - Deleted files.

3. **Include manually created files:**
   - Configuration files,
   - Documentation,
   - Assets,
   - Anything not auto-generated.

### 4.3 Step 3 — Audit Changes vs Plan

**Create an Audit Table** comparing:

- Planned changes (from `## 2. Technical Plan`)
- Implementation Notes (if any)
- Actual changes (from git diff)

**For each planned change:**
- Mark as ✅ if implemented as planned.
- Mark as ⚠️ if deviated (should be in Implementation Notes).
- Mark as ❌ if missing.

**For each actual change:**
- Verify it was planned OR documented in Implementation Notes.
- Flag any unplanned changes.

### 4.3.1 Using Sub-agents for Independent Audit (--audit-deep)

When `--audit-deep` flag is active, use **sub-agents** for independent quality verification:

> 💡 **Independent audit pattern:** Sub-agents can provide unbiased review by examining the implementation without the context of prior decisions.

**Sub-agent audit prompts:**

```
"Use an independent sub-agent to audit the implementation against 
the original requirements and verify nothing was missed."

"Use a sub-agent to review the code changes for security issues, 
performance concerns, and adherence to project conventions."

"Use a sub-agent to verify that all acceptance criteria from the 
Functional Brief are properly addressed by the implementation."
```

**Audit dimensions:**

| Dimension | Sub-agent Focus |
|-----------|-----------------|
| **Requirements** | All FR/AC from Brief addressed? |
| **Security** | Vulnerabilities, auth issues, data exposure? |
| **Performance** | Hot paths, N+1 queries, caching opportunities? |
| **Quality** | Conventions, patterns, code style? |
| **Tests** | Coverage adequate, edge cases tested? |

**Benefits of sub-agent audit:**

- Fresh perspective without planning context bias
- More thorough security and performance review
- Independent verification of requirement coverage

### 4.4 Step 4 — Run Validation (if --validate)

When `--validate` flag is active:

1. **Lint check:**
   - PHPStan, ESLint, or project linter
   - Document results

2. **Type check:**
   - Psalm, TypeScript, or project type checker
   - Document results

3. **Security scan:**
   - Snyk, OWASP dependency check
   - Document any findings

4. **Coverage report:**
   - Extract coverage percentage
   - Compare with project threshold

5. **Documentation:**
   - Include all results in output
   - Flag any failures

### 4.5 Step 5 — Prepare PR Description

Generate a **PR-ready description** with:

1. **Scope & Goal**: What the feature does.
2. **Approach**: Technical approach taken.
3. **Changes**: List of changes made.
4. **Testing**: Automated and manual tests.
5. **Validation**: Results if `--validate` used.
6. **Impacts & Risks**: What could be affected.
7. **Follow-ups**: Out-of-scope items for future PRs.

### 4.6 Step 6 — Prepare Documentation Updates

Check what documentation needs updating:

1. **README**: If the feature adds user-facing functionality.
2. **Changelog**: **Always required** — add entry under `[Unreleased]`.
3. **API Documentation**: If endpoints changed.
4. **ADRs**: If significant architecture decisions were made.

### 4.7 Step 7 — Prepare Commit

**Generate commit message** following conventional commits:

```text
<type>(<scope>): <short summary>

<body - what was done and why>

- <bullet 1>
- <bullet 2>

Refs: #<issue-number>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `docs`: Documentation only changes
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

**Generate git commands:**
- `git add` for all feature files
- `git commit` with the message
- `git push` to remote
- `gh pr create` if using GitHub CLI

### 4.8 Step 8 — Update Feature Document

Update `## 3. Final Report — EPCI-3` with:

1. **Completion Status**: Date, status, confidence, PR, commit, personas, flags.
2. **Summary of Changes**: What was implemented.
3. **Testing Summary**: Test coverage and results.
4. **Validation Summary**: If `--validate` used.
5. **Documentation Updates**: What was updated.
6. **Audit vs Plan**: How closely the plan was followed.
7. **Sub-agent Audit**: If `--audit-deep` used.
8. **Impacts & Risks**: What to watch for.
9. **Technical Debt**: Any shortcuts taken.
10. **Follow-ups**: Items for future work.

**Critical rule:**

> **NEVER modify `## 1. Functional Brief` or `## 2. Technical Plan`.**

### 4.9 Step 9 — Final Output

Present:

1. **Final Notes**: Remaining risks, checklists.
2. **Next Steps**: What the user should do.
3. **Workflow Complete**: Confirmation that EPCI is done.

---

## 5. Example — Complete EPCI-3 Session

Below is a **complete example** of an `epci-3-finalize` session with flags and personas.

````markdown
## 1. Inspection Summary

- Feature: `stay-tax-calculation`
- Feature Document: `docs/features/stay-tax-calculation.md`
- Prerequisites: epci-1-analyse ✅ | epci-2-code ✅
- Plan status: ⚠️ Deviations documented
- Implementation Notes: Present
- Active personas: `--persona-qa` (auto), `--persona-security` (manual)
- Flags: `--validate`, `--audit-deep`

### Files Changed

| File | Status | Description |
|------|--------|-------------|
| `src/Domain/Booking/StayTaxCalculator.php` | new | Tax calculation service |
| `src/Domain/Booking/Exception/TaxConfigurationException.php` | new | Exception class |
| `src/Application/Booking/BookingService.php` | modified | Integration |
| `config/packages/tax_rates.yaml` | new | Tax rates config |
| `templates/booking/summary.html.twig` | modified | Display tax |
| `tests/Unit/Domain/Booking/StayTaxCalculatorTest.php` | new | Unit tests |
| `docs/features/stay-tax-calculation.md` | modified | Feature doc |

### Manually Created Files (to include in commit)

- No manually created files detected.

### Audit vs Plan

| Planned (from §2 Technical Plan) | Actual | Match |
|---------------------------------|--------|-------|
| `src/Domain/Booking/StayTaxCalculator.php` — new | Created ✅ | ✅ |
| `src/Application/Booking/BookingService.php` — modify | Modified ✅ | ✅ |
| `src/Infrastructure/Invoice/InvoiceGenerator.php` — modify | **Deferred** ⚠️ | ⚠️ (documented) |
| `templates/booking/summary.html.twig` — modify | Modified ✅ | ✅ |
| — | `TaxConfigurationException.php` — new | ⚠️ (documented) |

> All changes correspond to "Proposed Changes" or "Implementation Notes". ✅

### Validation Results (--validate flag)

| Check | Tool | Result | Details |
|-------|------|--------|---------|
| Lint | PHPStan level 8 | ✅ Pass | 0 errors |
| Type-check | Psalm | ✅ Pass | — |
| Security | Snyk | ✅ Pass | No vulnerabilities |
| Coverage | PHPUnit | 94% | Above 80% threshold |

### Sub-agent Audit (--audit-deep flag)

> 🔍 **Independent Review Results:**
> 
> - **Requirements coverage:** ✅ All FR/AC addressed
>   - FR1 (Calculate tax): ✅ StayTaxCalculator.calculate()
>   - FR2 (Display on summary): ✅ summary.html.twig updated
>   - AC1-AC3: ✅ All tested
> - **Security review:** ✅ No issues found
>   - No user input directly used in calculations
>   - Configuration properly validated
> - **Performance review:** ✅ Good
>   - Tax calculation is O(1)
>   - No DB queries in hot path
> - **Code quality:** ✅ Follows project conventions
>   - Domain service pattern used correctly
>   - Exception handling consistent with project

---

## 2. PR Description

```markdown
## Scope & Goal

Implement stay tax calculation for seasonal rentals. The tax is calculated based on the number of nights and the property category, displayed on the booking summary, and will be included in invoices (follow-up).

## Approach

Created a dedicated `StayTaxCalculator` service in the Domain layer that reads tax rates from configuration. Integrated into `BookingService` to calculate tax during booking creation.

## Changes

- Added `StayTaxCalculator` service for tax calculation
- Added `TaxConfigurationException` for missing rate configuration
- Added tax rates configuration (`tax_rates.yaml`)
- Updated `BookingService` to integrate tax calculation
- Updated booking summary template to display tax breakdown
- Added comprehensive unit tests

## Testing

- **Automated:**
  - Unit tests: 15 tests, all passing
  - Integration tests: 3 tests, all passing
- **Manual:**
  - Create booking with 3-night stay: ✅ verified
  - Verify tax on summary page: ✅ verified

## Validation

- Lint (PHPStan): ✅ Pass
- Types (Psalm): ✅ Pass
- Security (Snyk): ✅ Pass
- Coverage: 94%

## Impacts & Risks

- Invoice template not updated (deferred to next PR)
- Tax rates hardcoded in config (consider admin UI in future)

## Follow-ups

- Add invoice template integration
- Add admin UI for tax rate configuration
- Support historical tax rates
```

---

## 3. Documentation Updates

### 3.1 README

No README update required.

### 3.2 Changelog (mandatory)

```markdown
## [Unreleased]

### Added
- Stay tax calculation for seasonal rentals (#123)
```

### 3.3 API Documentation

No API documentation update required (no new endpoints).

### 3.4 ADRs

No ADR required.

---

## 4. Commit Preparation

> **NEVER commit unrelated files.** Compare with plan + implementation notes + manual files.

### 4.1 Files to Stage

```bash
git add src/Domain/Booking/StayTaxCalculator.php
git add src/Domain/Booking/Exception/TaxConfigurationException.php
git add src/Application/Booking/BookingService.php
git add config/packages/tax_rates.yaml
git add templates/booking/summary.html.twig
git add tests/Unit/Domain/Booking/StayTaxCalculatorTest.php
git add docs/features/stay-tax-calculation.md
```

### 4.2 Files to Exclude

No files to exclude.

> ✅ Verified: no unrelated files staged.

### 4.3 Commit Message (conventional commits)

```text
feat(booking): add stay tax calculation for seasonal rentals

Implement tax calculation based on nights and property category.
Tax is displayed on booking summary page.

- Add StayTaxCalculator service
- Add tax rates configuration
- Integrate into BookingService
- Add unit and integration tests

Refs: #123
```

### 4.4 Git Commands

```bash
# Check current status — verify no unrelated files
git status

# Stage all feature files (and ONLY feature files)
git add src/Domain/Booking/StayTaxCalculator.php \
        src/Domain/Booking/Exception/TaxConfigurationException.php \
        src/Application/Booking/BookingService.php \
        config/packages/tax_rates.yaml \
        templates/booking/summary.html.twig \
        tests/Unit/Domain/Booking/StayTaxCalculatorTest.php \
        docs/features/stay-tax-calculation.md

# Commit with conventional message
git commit -m "feat(booking): add stay tax calculation for seasonal rentals"

# Push
git push origin feature/stay-tax-calculation

# Create PR
gh pr create --title "feat(booking): add stay tax calculation" --body-file docs/features/stay-tax-calculation.md
```

---

## 5. Feature Document Update

> **NEVER modify `## 1. Functional Brief` or `## 2. Technical Plan` under any circumstances.**

### 5.1 Section to Update

- Section: `## 3. Final Report — EPCI-3`
- Action: **Overwrite with exactly this structure**

### 5.2 Content Written

```markdown
## 3. Final Report — EPCI-3

*(This section is managed by `epci-3-finalize`. Do not modify manually.)*

### Completion Status

- **Date:** 2025-01-15
- **Status:** ✅ Complete (invoice template deferred)
- **Confidence:** 90% (plan followed, 1 deferral documented)
- **PR:** #124
- **Commit:** abc1234
- **Personas used:** --persona-qa, --persona-security
- **Flags:** --validate, --audit-deep

### Summary of Changes

- Added `StayTaxCalculator` service for tax calculation
- Added `TaxConfigurationException` for edge case handling
- Added tax rates configuration
- Updated `BookingService` to integrate tax calculation
- Updated booking summary template
- Added 15 unit tests + 3 integration tests

### Testing Summary

- Unit tests: 15 tests, all passing
- Integration tests: 3 tests, all passing
- Edge cases: all covered (zero nights, missing category, unconfigured rate)
- Manual verification: ✅ Complete

### Validation Summary

- Lint (PHPStan): ✅ Pass
- Type-check (Psalm): ✅ Pass
- Security (Snyk): ✅ Pass
- Coverage: 94%

### Documentation Updates

- README: ⏭️ Not needed
- Changelog: ✅ Updated
- API docs: ⏭️ Not needed

### Audit vs Plan

- Planned changes: 5 files
- Actual changes: 6 files (+1 exception class)
- Deviations: invoice template deferred
- Unplanned additions: `TaxConfigurationException.php` (justified)

### Sub-agent Audit

- Requirements: ✅ All FR/AC covered
- Security: ✅ No issues
- Performance: ✅ O(1) calculation
- Quality: ✅ Follows conventions

### Impacts & Risks

- Invoice template not updated (deferred)
- Tax rates in config only (no admin UI)

### Technical Debt / Residue

- No technical debt introduced.

### Follow-ups (out of scope)

- [ ] Add invoice template integration
- [ ] Add admin UI for tax rate configuration
- [ ] Support historical tax rates
```

---

## 6. Final Notes

### Remaining Risks

- Invoice template must be updated in follow-up PR
- Tax rates are hardcoded — consider admin UI for flexibility

### Pre-merge Checklist

- [x] All tests passing
- [ ] Code review completed
- [x] Documentation updated
- [x] Changelog updated
- [x] No console.log / debug statements left
- [x] No unrelated files in commit
- [x] Validation passed (--validate) ✅
- [x] Sub-agent audit approved (--audit-deep) ✅

### Post-deployment Checklist

- [ ] Verify tax calculation in staging
- [ ] Monitor logs for TaxConfigurationException
- [ ] Verify tax display on booking summary

---

## 7. Next Steps for User

After `epci-3-finalize`, the user should:

1. **Review** the PR description and commit message
2. **Merge** into target branch (after code review)
3. **Deploy** to staging environment
4. **Verify** the feature works as expected
5. **Monitor** logs for any errors
6. **Update** environment-specific documentation if needed
7. **Close** the related ticket/issue (#123)

---

## 8. Workflow Complete

```text
✅ EPCI workflow complete for feature: stay-tax-calculation

Feature Document: docs/features/stay-tax-calculation.md

All sections populated:
- ## 1. Functional Brief — EPCI-0 ✅
- ## 2. Technical Plan — EPCI-1 ✅
- ## 3. Final Report — EPCI-3 ✅

Prerequisites verified:
- epci-1-analyse ✅
- epci-2-code ✅
- epci-3-finalize ✅

Validation: ✅ Passed (--validate)
Sub-agent audit: ✅ Approved (--audit-deep)

Ready for commit, PR, and merge.
```
````

---

## 6. Summary

`epci-3-finalize` is the **finalization phase** of the full EPCI workflow:

- It keeps the EPCI philosophy (**Explore → Plan → Code → Inspect**),
- It **verifies prerequisites** (epci-1 and epci-2 completed),
- It **inspects the implementation** against the plan,
- It **audits changes vs plan** (mandatory Audit vs Plan table),
- It **runs validation checks** with `--validate` flag,
- It **performs independent sub-agent audit** with `--audit-deep` flag,
- It **prepares documentation** updates (Changelog mandatory),
- It **generates PR description and commit message** (conventional commits),
- It **updates only `## 3. Final Report`** in the Feature Document,
- It **never modifies** `## 1. Functional Brief` or `## 2. Technical Plan`,
- It **never implements new features** or refactors,
- It **never ignores manually created files**,
- It **never commits unrelated files**,
- It **provides next steps** for the user.

In **INTERACTIVE mode**, the workflow has two phases:
- **Phase A** — Inspect, audit, prepare (read-only, NO file writes, wait for validation),
- **Phase B** — Write final report to Feature Document (after user confirms).

In **AUTO mode**, all steps are executed in a single pass.

This command **completes the EPCI workflow**. After running `epci-3-finalize`, the feature is ready for commit, PR, and merge.

**v2.7 improvements:**

- **Universal flags:** `--preview`, `--validate`, `--dry-run`, `--uc`, `--verbose`, `--introspect`, `--audit-deep`
- **Persona system:** Auto-activation of `--persona-qa`, contextual security/architect personas
- **Validation integration:** Lint, type-check, security scan, coverage with `--validate` flag
- **Deep audit:** Independent sub-agent review with `--audit-deep` flag
- **Enhanced output formats:** Standard, ultra-compressed (--uc), preview (--preview), introspect (--introspect)
- **Audit dimensions:** Requirements, security, performance, quality coverage in sub-agent audit
- **Extended Final Report:** Includes personas, flags, validation summary, sub-agent audit results
