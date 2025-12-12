# epci-micro — Ultra-light EPCI workflow for TINY changes (v2.7)

> EPCI workflow: **Explore → Plan → Code → Inspect**  
> This command implements a **single-pass, ultra-light workflow** for **TINY** changes.
> 
> `epci-micro` is the **fast lane** — minimal overhead, maximum focus.

---

## Critical Rules

- ⚠️ TINY only: 1 file (max 2 if same module), < 50 LOC, no new business logic
- ⚠️ If task appears larger than TINY → STOP and reroute to `epci-soft` or full EPCI
- ⚠️ NEVER expand scope beyond the given objective
- ⚠️ `--safe-mode` available but keep confirmations minimal (v2.7)
- ⚠️ No section before `## 1.` and no section after `## 7.`

---

## Supported Flags (v2.7)

`epci-micro` supports a **limited subset** of flags to maintain its ultra-light nature.

### Available Flags

| Flag | Effect | Default |
|------|--------|---------|
| `--preview` | Show what would be changed without writing files | Off |
| `--safe-mode` | Require confirmation before file modification | Off |
| `--uc` | Ultra-compressed output (even more minimal) | Off |
| `--verbose` | Show full diff instead of summary | Off |
| `--validate` | Run basic syntax/lint check after change | Off |

### Usage Examples

```bash
# Preview the change without applying
epci-micro --preview
FEATURE_SLUG=typo-fix

# Safe mode for production files
epci-micro --safe-mode
FEATURE_SLUG=config-update

# Compressed output for CI/CD
epci-micro --uc
FEATURE_SLUG=log-message-fix
```

### Flag Behaviour

| Flag | Effect in epci-micro |
|------|---------------------|
| `--preview` | Shows diff, skips file write, skips commit |
| `--safe-mode` | Single confirmation before the one file change |
| `--uc` | Removes explanatory text, keeps only essential info |
| `--verbose` | Shows complete file diff, not just changed lines |
| `--validate` | Runs syntax check (e.g., `php -l`, `node --check`) |

> **Note:** Flags in `epci-micro` have minimal overhead. Even with flags, the workflow remains single-pass and fast.

---

## Not Available in epci-micro (v2.7)

The following features are **intentionally disabled** to keep `epci-micro` ultra-light:

| Feature | Reason |
|---------|--------|
| `--introspect` | TINY changes don't need reasoning explanation |
| `--persona-*` | Personas add overhead, not needed for trivial fixes |
| `--dry-run` | Use `--preview` instead (simpler) |
| `--audit-deep` | Overkill for 1-file changes |
| Phase A/B separation | Single-pass workflow only |
| Sub-agents | TINY changes don't need context delegation |

If you need these features, your task is probably **not TINY** → use `epci-soft` or full EPCI.

> **Note:** For complete flags documentation, see `epci-flags.md`.

---

## 1. Purpose & Scope

`epci-micro` is designed for **very small, low-risk changes** that still deserve a minimum of:

- clarification of intent,
- explicit impact analysis,
- basic tests,
- and a short written trace.

Use `epci-micro` **only** when ALL the following conditions are met:

- The change is **TINY**:
    - 1 file touched (2 maximum if strictly in same module)
    - < 50 lines of code changed
    - No new business logic introduced
    - No data model change, no schema migration
- The impact on security, data integrity, performance, external APIs is **negligible or null**.
- The change can be explained in **1–2 sentences**.

### 1.1 TINY vs SMALL Clarification

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

### 1.2 Examples of valid `epci-micro` tasks

- Fixing a typo or label in a template or translation file.
- Adjusting a log message, comment or error string.
- Changing a CSS class or a trivial display condition.
- Adding a very small guard condition with obvious behaviour.
- Updating a configuration value.
- Fixing an obvious bug in a single line.

For anything beyond that (new behaviour, non-trivial condition, multiple files, DB impact), use `epci-soft` (SMALL) or the full EPCI workflow (`epci-1/2/3`).

---

## 2. Inputs & Modes

### 2.1 `$ARGUMENTS`

`epci-micro` consumes a **compact brief**. For TINY changes, a simplified format is sufficient:

```text
$ARGUMENTS=<MICRO_BRIEF>
  FEATURE_TITLE: <short human title of the micro-change>
  FEATURE_SLUG: <kebab-case-slug> (optional, derived from title if absent)
  OBJECTIVE: <one sentence: what should be improved/fixed>
  CONTEXT: <ticket ID, URL, module>
  CONSTRAINTS: <if any, e.g. specific browser, language>
```

> **Compatibility note:** If `epci-micro` receives a full `EPCI_READY_BRIEF` from `epci-0-briefing` (with FUNCTIONAL_REQUIREMENTS, ACCEPTANCE_CRITERIA, etc.), it will accept it but focus only on the essential fields above. The full format is not required for TINY changes.

If `epci-micro` is called directly by a human (without EPCI-0), provide at minimum:
- `FEATURE_TITLE` or `FEATURE_SLUG`
- `OBJECTIVE` (one sentence)

### 2.2 Execution modes

`epci-micro` supports the same `EXECUTION_MODE` parameter as other EPCI commands:

- `EXECUTION_MODE = "AUTO"` (recommended):
    
    - Single-pass, no explicit A/B phases.
    - The command performs: Explore → Micro-plan → Code → Tests → Report.
    - Best for controlled, clearly-scoped micro-fixes.

- `EXECUTION_MODE = "INTERACTIVE"`:
    
    - Still **single-pass** logically, but the assistant may:
        - ask **1–3 quick confirmation questions**,
        - explicitly confirm the intent before proposing code.

In both modes, `epci-micro` must remain **short and focused**.

### 2.3 Flag Effects (v2.7)

| Flag | Effect on Workflow |
|------|-------------------|
| `--preview` | Shows plan + diff, writes nothing |
| `--safe-mode` | Asks "Apply this change? [y/n]" once |
| `--uc` | Output reduced to ~50% of standard |
| `--verbose` | Full file diff shown |
| `--validate` | Adds syntax check after code change |

---

## 3. Responsibilities & Limitations

### 3.1 What `epci-micro` MUST do

1. **Restate the objective** in one or two sentences.
2. **Validate FEATURE_SLUG** (derive if not provided).
3. **Identify the target file(s)** and the type of change.
4. Produce a **micro-plan** with 2–5 bullet points maximum.
5. Propose the **minimal code change** necessary.
6. If `--safe-mode`: ask for confirmation before writing (v2.7).
7. Describe **basic tests** to validate the change.
8. If `--validate`: run syntax/lint check (v2.7).
9. Update the **Feature Document** (`docs/features/<feature-slug>.md`) minimally.
10. Emit a **suggested commit message** (simple format: `<type>: <message>`).

### 3.2 What `epci-micro` MUST NOT do

- MUST NOT refactor non-trivial logic.
- MUST NOT introduce new business rules.
- MUST NOT create or modify DB schemas.
- MUST NOT change public API contracts.
- MUST NOT modify more than one module or area.
- MUST NOT trigger complex refactors "because it's cleaner".
- MUST NOT expand scope beyond the given objective.
- MUST NOT silently turn a TINY task into a SMALL/STANDARD one.
- MUST NOT use personas or introspection (not available).

> If during exploration the task appears bigger than expected, `epci-micro` MUST stop and recommend using `epci-soft` or the full EPCI workflow.

---

## 4. Output Layout (assistant message)

For IDE / terminal readability, `epci-micro` MUST follow this **fixed layout**.

### Standard Output

````markdown
## 1. Objective & Scope

... short restatement (1-2 sentences) ...

- Feature slug: `<feature-slug>`
- Target: <file or area>
- Change type: <typo / CSS / log / guard / etc.>
- Flags: `--validate` (if any active) (v2.7)

---

## 2. Micro-plan (auto-validated)

- Step 1: ...
- Step 2: ...
- Step 3: ...

---

## 3. Code Change

```diff
... minimal diff or relevant code snippet ...
````

**Code written:** ✅

---

## 4. Micro-tests

- [ ] Test 1: ...
- [ ] Test 2: ...

### Validation (if --validate active) (v2.7)

- Syntax check: `php -l <file>` → ✅ Pass

---

## 5. Feature Document Update

- Feature slug: `<feature-slug>`
- Feature document: `docs/features/<feature-slug>.md`
- Sections updated:
    - `## 1. Functional Brief` → added micro-entry
    - `## 3. Final Report` → added completion note

---

## 6. Commit

```text
<type>: <short, meaningful commit message>
```

```bash
git add <file(s)>
git commit -m "<type>: <message>"
git push
```

---

## 7. Complete (v2.7)

```text
✅ EPCI-Micro complete: <feature-slug>
   File: <file-path>
   Flags: --validate
   Validation: ✅ Pass
```
````

### Ultra-Compressed Output (--uc)

````markdown
## `<feature-slug>` — <change-type>

**Target:** `<file-path>`
**Change:** <one-line description>

```diff
<minimal diff>
```

✅ Written | ✅ Tested | ✅ Validated

```bash
git add <file> && git commit -m "<type>: <message>" && git push
```
````

**Strict rule:** No extra sections before `## 1.` or after `## 7.` (or after diff block for `--uc`).

---

## 5. Behaviour Step-by-step

### 5.1 Step 1 — Objective & Scope

- Read `$ARGUMENTS`.
- Restate the objective concisely, including:
  - the module or area (if known),
  - the type of change (typo, style, log, small condition).
- Note active flags if any (v2.7).

**Example:**

```markdown
## 1. Objective & Scope

Fix a typo in the French error message displayed on the login page when credentials are invalid.

- Feature slug: `login-typo-fix`
- Target: `translations/messages.fr.yaml`
- Change type: typo fix
- Flags: `--validate`
```

If the change has **any sign** of being larger than TINY, stop and propose to reroute to `epci-soft` or the full EPCI pipeline.

### 5.2 Step 2 — Validate FEATURE_SLUG

Before proceeding, validate the `FEATURE_SLUG`:

1. Confirm it is in **kebab-case** (lowercase, hyphens only).
2. If not provided, derive from `FEATURE_TITLE`:
    - "Fix French login typo" → `fix-french-login-typo`
3. Confirm the path `docs/features/<feature-slug>.md` is valid.

If invalid, fix it before continuing.

### 5.3 Step 3 — Micro-plan (auto-validated)

Produce a **very short plan** (2–5 bullets max):

- Identify target file & location.
- Describe the minimal edit.
- Note any side-effect / check needed.

**Example:**

```markdown
## 2. Micro-plan (auto-validated)

- Locate the login error message in `translations/messages.fr.yaml`.
- Fix the French typo ("connextion" → "connexion").
- Verify the key is not duplicated elsewhere.
```

The plan is **implicitly validated** in `epci-micro`: no separate confirmation round.

> **With `--preview`:** Stop here. Show the plan and proposed diff, but don't write files.

### 5.4 Step 4 — Code Change

Provide either:

- a `diff` style block (preferred), or
- a small code snippet with clear comments.

**With `--safe-mode` (v2.7):**

```markdown
## 3. Code Change

```diff
--- a/translations/messages.fr.yaml
+++ b/translations/messages.fr.yaml
@@ -15,7 +15,7 @@
 security:
   login:
     error:
-      bad_credentials: "Échec de connextion"
+      bad_credentials: "Échec de connexion"
```

**Apply this change?** [y/n]: y
**Code written:** ✅
```

**Standard (no --safe-mode):**

````markdown
## 3. Code Change

```diff
--- a/translations/messages.fr.yaml
+++ b/translations/messages.fr.yaml
@@ -15,7 +15,7 @@
 security:
   login:
     error:
-      bad_credentials: "Échec de connextion"
+      bad_credentials: "Échec de connexion"
````

**Code written:** ✅
````

The diff must remain **minimal**.

### 5.5 Step 5 — Micro-tests

Describe **how to validate the change**, at least:

- 1–2 manual tests, or
- 1 small automated test if relevant.

**With `--validate` (v2.7):**

```markdown
## 4. Micro-tests

- [ ] Try to log in with invalid credentials and verify the French error message shows "connexion" (not "connextion").
- [ ] Verify that English and other languages are unaffected.

### Validation (--validate)

- Syntax check: `php -l translations/messages.fr.yaml` → ✅ Pass (no syntax errors)
```

**Standard (no --validate):**

```markdown
## 4. Micro-tests

- [ ] Try to log in with invalid credentials and verify the French error message shows "connexion" (not "connextion").
- [ ] Verify that English and other languages are unaffected.
```

### 5.6 Step 6 — Feature Document Update

Update the **Feature Document** at `docs/features/<feature-slug>.md`.

> `epci-micro` adds minimal notes to existing sections. It does NOT overwrite content created by other EPCI commands.

**Behaviour:**

1. **If the file does not exist:**
    
    - Create it with the standard skeleton.
    - Fill a small entry under `## 1. Functional Brief` describing the micro-change.
    - Add a completion note under `## 3. Final Report`.

2. **If the file exists:**
    
    - Under `## 1. Functional Brief — EPCI-0`: append a small bullet noting the micro-change.
    - Under `## 3. Final Report — EPCI-3`: add a short note:
        
        ```markdown
        ### EPCI-Micro completion — <YYYY-MM-DD>
        
        - Task completed via `epci-micro`.
        - Flags: --validate (v2.7)
        - Validation: ✅ Pass (v2.7)
        - Commit: `fix: correct French typo in login error`
        ```

**Example output:**

```markdown
## 5. Feature Document Update

- Feature slug: `login-typo-fix`
- Feature document: `docs/features/login-typo-fix.md`
- Sections updated:
  - `## 1. Functional Brief` → added line: "Fix French typo in login error message"
  - `## 3. Final Report` → added EPCI-Micro completion note
```

### 5.7 Step 7 — Commit

Provide:

- A **short, conventional commit message** (50–72 chars).
- **Git commands** for convenience.

**Commit format for epci-micro (simple):**

```text
<type>: <short message>
```

**Examples:**

- `fix: correct French typo in login error message`
- `style: adjust padding on stay tax badge`
- `chore: improve log message for failed CSV import`

````markdown
## 6. Commit

```text
fix: correct French typo in login error message
````

```bash
git add translations/messages.fr.yaml docs/features/login-typo-fix.md
git commit -m "fix: correct French typo in login error message"
git push
```
````

### 5.8 Step 8 — Complete Summary (v2.7)

End with a brief completion block:

```markdown
## 7. Complete (v2.7)

```text
✅ EPCI-Micro complete: login-typo-fix
   File: translations/messages.fr.yaml
   Flags: --validate
   Validation: ✅ Pass
```
```

---

## 6. Guardrails: Detecting Non-TINY Tasks

At the very beginning (Objective & Scope) and while drafting the micro-plan, `epci-micro` MUST evaluate if the task really matches the **TINY** constraints.

### 6.1 Complexity Reference (TINY thresholds)

| Criterion | TINY limit | If exceeded → |
|-----------|------------|---------------|
| Files | 1 (max 2 if same module) | → `epci-soft` |
| LOC | < 50 | → `epci-soft` |
| Modules | 1 | → `epci-soft` or full |
| Risk | Very low | → `epci-soft` or full |
| Schema change | None | → full EPCI |
| New business rule | None | → `epci-soft` or full |

### 6.2 When to Stop and Reroute

If any of the following holds true:

- More than 1–2 files likely impacted,
- Non-trivial condition or new branch in business logic,
- Need for DB schema changes or migrations,
- Multiple modules or layers involved,
- Security or data integrity could be impacted,

Then:

1. **STOP** the micro workflow.
2. Explain **why** the task is not TINY.
3. Recommend a reroute:
   - **SMALL** → use `epci-soft`
   - **STANDARD/LARGE** → use full EPCI (`epci-1` → `epci-2` → `epci-3`)

**Example:**

```markdown
⚠️ This task is not suitable for `epci-micro`.

**Reason:** The change will likely impact 3+ files and introduce new validation logic in the booking flow.

**Recommendation:** Use `epci-soft` for this SMALL-level change, or the full EPCI workflow if complexity increases further.

**Suggested command:**
```text
epci-soft
FEATURE_SLUG=<slug>
$ARGUMENTS=<brief>
```
```

---

## 7. Example — Micro Session

Below is a **complete example** of an `epci-micro` session with v2.7 features.

````markdown
## 1. Objective & Scope

Fix a typo in the French error message displayed on the login page when credentials are invalid.

- Feature slug: `login-typo-fix`
- Target: `translations/messages.fr.yaml`
- Change type: typo fix
- Flags: `--validate`

---

## 2. Micro-plan (auto-validated)

- Locate the login error message key `security.login.error.bad_credentials` in `translations/messages.fr.yaml`.
- Fix the French typo ("connextion" → "connexion").
- Verify no other file uses this incorrect spelling.

---

## 3. Code Change

```diff
--- a/translations/messages.fr.yaml
+++ b/translations/messages.fr.yaml
@@ -15,7 +15,7 @@
 security:
   login:
     error:
-      bad_credentials: "Échec de connextion"
+      bad_credentials: "Échec de connexion"
````

**Code written:** ✅

---

## 4. Micro-tests

- [x] Try to log in with invalid credentials → French error shows "connexion" ✅
- [x] Verify English version unchanged ✅

### Validation (--validate)

- Syntax check: `php -l translations/messages.fr.yaml` → ✅ Pass

---

## 5. Feature Document Update

- Feature slug: `login-typo-fix`
- Feature document: `docs/features/login-typo-fix.md`
- Sections updated:
    - `## 1. Functional Brief` → added: "Fix French typo in login error message"
    - `## 3. Final Report` → added EPCI-Micro completion note (2025-01-15)

---

## 6. Commit

```text
fix: correct French typo in login error message
```

```bash
git add translations/messages.fr.yaml docs/features/login-typo-fix.md
git commit -m "fix: correct French typo in login error message"
git push
```

---

## 7. Complete (v2.7)

```text
✅ EPCI-Micro complete: login-typo-fix
   File: translations/messages.fr.yaml
   Flags: --validate
   Validation: ✅ Pass
```
````

---

## 8. Summary

`epci-micro` provides a **disciplined but ultra-light** way to handle TINY changes by:

- Keeping the **EPCI philosophy** (Explore → Plan → Code → Inspect),
- Compressing everything into a **single, short pass**,
- Validating **FEATURE_SLUG** consistently,
- Updating the **Feature Document** minimally but consistently,
- Enforcing a clear **scope guardrail** with numeric thresholds,
- Providing **complete git commands** for immediate commit.

It is intentionally narrow in scope and MUST remain focused on **small, low-risk, quickly verifiable** updates.

When in doubt about complexity, **reroute to `epci-soft`** or the full EPCI workflow.

**v2.7 improvements:**

- **Limited flags support:** `--preview`, `--safe-mode`, `--uc`, `--verbose`, `--validate`
- **Safe-mode:** Single confirmation before file write
- **Validation:** Optional syntax/lint check with `--validate`
- **Ultra-compressed output:** Even more minimal with `--uc`
- **Completion summary:** Quick status block at end
- **Explicit exclusions:** Documents what's NOT available (personas, introspect)

**Previous improvements (preserved):**

- Simplified $ARGUMENTS format (full EPCI_READY_BRIEF accepted but not required)
- Clarified TINY vs SMALL boundary with decision tree
- Version aligned with other EPCI commands

> **Note:** Sub-agents, personas, and introspection are **not available** in `epci-micro` — TINY changes don't need them. If you need those features, your task is not TINY.

---

## 9. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-flags.md` | Universal flags reference (shows micro compatibility) |
| `epci-soft.md` | SMALL changes workflow (next level up) |
| `epci-workflow-guide.md` | Complete workflow documentation |

---

*This document is part of the EPCI v2.7 workflow system.*
