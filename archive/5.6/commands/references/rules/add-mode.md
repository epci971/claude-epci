# Rules Add Mode

> Reference file for `/rules` command incremental rule addition (Mode ADD).

---

## Step A1: Clarity Assessment

**Reference**: `rules-generator/references/rule-classifier.md`

Calculate clarity score:

| Element | Score |
|---------|-------|
| Explicit scope ("Python files", "in backend/") | +0.4 |
| Deducible scope from context | +0.2 |
| Detectable severity (keywords) | +0.3 |
| Actionable content (action verb) | +0.2 |
| Length > 5 words | +0.1 |

**Routing**:
- Clarity >= 0.8 → Step A3 (Direct reformulation)
- Clarity < 0.8 → Step A2 (Clarification)

---

## Step A2: Clarification

**Subagent**: `@rule-clarifier` (Haiku)

Invoke @rule-clarifier for fast clarification:

```
Task: Clarify the following rule
Input: "[user input]"
Context: Project structure, existing .claude/rules/ files
```

**Possible questions** (max 3, one-at-a-time):

1. **Scope** (if not detected):
   ```
   What scope for this rule?
     A) All Python files (**/*.py)
     B) Backend only (backend/**/*.py)
     C) Frontend (frontend/**/*.tsx)
     D) Other (specify)

   Suggestion: [B] based on project structure
   ```

2. **Severity** (if not detected):
   ```
   What severity?
     A) CRITICAL — Never violate
     B) CONVENTIONS — Project standard
     C) PREFERENCES — Recommended but flexible

   Suggestion: [B] based on "should"
   ```

3. **Wording** (if too vague):
   ```
   Can you clarify the rule?
   Current: "Be careful with injections"
   Suggestion: "Always use parameterized queries to prevent SQL injections"
   ```

---

## Step A3: Reformulation & Validation

Display reformulated rule:

```
+---------------------------------------------------------------------+
| RULE DETECTED                                                        |
+---------------------------------------------------------------------+
|                                                                     |
| Content  : "Always use type hints for public functions"             |
| Severity : CONVENTIONS                                              |
| Scope    : backend/**/*.py                                          |
| Placement: .claude/rules/python-conventions.md (existing)           |
|                                                                     |
| [1] Validate and add                                                |
| [2] Modify                                                          |
| [3] Cancel                                                          |
|                                                                     |
+---------------------------------------------------------------------+
```

**If [2] Modify** → Back to Step A2 with modified input
**If [3] Cancel** → End
**If [1] Validate** → Step A4

---

## Step A4: Placement Decision

**Placement logic** (automatic):

```
IF scope is global (empty or **/*):
   → CLAUDE.md
ELSE:
   → Search for .claude/rules/*.md file with similar paths

   IF overlap >= 70%:
      → Append to existing file
   ELSE:
      → Create new rules/*.md file
```

**New file naming**:

| Scope | Filename |
|-------|----------|
| `**/*.py` | `python-conventions.md` |
| `backend/**/*.py` | `backend-python.md` |
| `frontend/**/*.tsx` | `frontend-react.md` |
| `**/test_*.py` | `testing-python.md` |
| Other | `rules-custom.md` |

---

## Step A5: Integration

1. **If CLAUDE.md**:
   - Read existing file
   - Identify appropriate section (create if necessary)
   - Add rule in bullet point format

2. **If existing rules/*.md**:
   - Read file
   - Identify severity section (CRITICAL/CONVENTIONS/PREFERENCES)
   - Append at end of section
   - Check token limit (< 2000)

3. **If new rules/*.md**:
   ```markdown
   ---
   paths:
     - [extracted_scope]
   ---

   # [Category] Conventions

   > Rules for [scope description]

   ## CRITICAL

   ## CONVENTIONS

   - [new_rule]

   ## PREFERENCES
   ```

---

## Step A6: Validation & Completion

**Subagent**: `@rules-validator`

Validate modified/created file.

**If failure**:
```
Validation failed: [error]
Suggestion: [fix]

Do you want to fix? [Y/n]
```

**If success**:
```
+---------------------------------------------------------------------+
| RULE ADDED                                                          |
+---------------------------------------------------------------------+
|                                                                     |
| File    : .claude/rules/python-conventions.md                       |
| Section : CONVENTIONS                                               |
| Tokens  : 1450/2000                                                 |
|                                                                     |
| Rule will be active for: backend/**/*.py                            |
|                                                                     |
+---------------------------------------------------------------------+
```

**Warning if near limit**:
```
File at 90% of limit (1800/2000 tokens)
Consider creating a new file for future rules
```

---

## Mode ADD Flow Example

```
User: /epci:rules "avoid any in TypeScript"

Step 0: Auto-detection
├── Score: 0.7 (avoid = rule indicator)
└── → Mode ADD

Step A1: Clarity
├── Scope: not explicit (→ deducible: **/*.ts)
├── Severity: CONVENTIONS (avoid)
└── Clarity: 0.7 → Quick clarification

Step A2: @rule-clarifier
└── Q1: What scope?
    A) All TS files (**/*.ts, **/*.tsx)
    B) Frontend only
    → User: A

Step A3: Reformulation
+------------------------------------------+
| Content  : "Avoid using any"             |
| Severity : CONVENTIONS                   |
| Scope    : **/*.ts, **/*.tsx             |
| Placement: .claude/rules/typescript.md   |
+------------------------------------------+
→ User: [1] Validate

Step A4-A6: Integration + Validation
→ Rule added to typescript.md
```
