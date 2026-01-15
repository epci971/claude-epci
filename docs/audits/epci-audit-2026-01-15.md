# Audit Report — epci.md

> **Date**: 2026-01-15 15:30
> **Auditor**: command-auditor v1.0.0
> **Mode**: STRICT

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Score | **55/100** |
| Rules Checked | 95 |
| Blocking Errors | 2 |
| Errors | 5 |
| Warnings | 10 |
| Suggestions | 3 |
| **Verdict** | **BLOCKED** |

---

## Detected Workflow

```mermaid
flowchart TD
    A[Start] --> B{--from-native-plan?}
    B -->|Yes| C[Step 0.5: Import Native Plan]
    B -->|No| D[Prerequisite Check]
    C --> D
    D -->|§1 Missing| E[❌ ABORT]
    D -->|§1 OK| F[Phase 1: Planning]
    F --> G[@plan-validator]
    G -->|NEEDS_REVISION| F
    G -->|APPROVED| H[⏸️ BP1]
    H -->|Continue| I[Phase 2: TDD]
    I --> J[@code-reviewer]
    J --> K{Security files?}
    K -->|Yes| L[@security-auditor]
    K -->|No| M{5+ test files?}
    L --> M
    M -->|Yes| N[@qa-reviewer]
    M -->|No| O[⏸️ BP2]
    N --> O
    O -->|Continue| P[Phase 3: Finalization]
    P --> Q[@doc-generator]
    Q --> R[Generate Commit Context]
    R --> S[Memory Update Hook]
    S --> T[✅ COMPLETE]
```

---

## Results by Category

### CAT-FM: Frontmatter (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | FM-001 | Frontmatter present | OK — lines 1-8 |
| ✅ | FM-002 | Description required | OK |
| ✅ | FM-003 | Description ≤ 500 chars | OK — ~280 chars |
| ✅ | FM-004 | Verb start | OK — "Complete..." |
| ✅ | FM-005 | < 15 lines | OK — 8 lines |
| ✅ | FM-006 | argument-hint present | OK |
| ✅ | FM-007 | argument-hint format | OK — uses `[--flag]` correctly |
| ✅ | FM-008 | allowed-tools | OK — declared |
| ✅ | FM-009 | Valid tools | OK — Read, Write, Edit, Bash, Grep, Glob, Task |
| ❌ | **FM-010** | **Bash restricted** | **BLOQUANT — `Bash` without pattern restriction** |
| ✅ | FM-011 | No tabs | OK |
| ✅ | FM-012 | Special chars | OK |
| ✅ | FM-013 | Known fields | OK |
| ✅ | FM-014 | `!` requires Bash | N/A — no `!` execution |
| ✅ | FM-015 | Budget < 15K chars | OK |

### CAT-ST: Structure (20 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | ST-001 | Overview present | OK — line 12 |
| ✅ | ST-002 | Overview 2-4 sentences | OK — 2 sentences |
| ⚠️ | ST-003 | Process/Workflow section | **ERREUR — No explicit `## Process`; uses Phase structure** |
| ✅ | ST-004 | Numbered steps | OK — Phase 1/2/3 structure |
| ❌ | ST-005 | Output section | **ERREUR — No explicit `## Output`** |
| ✅ | ST-006 | Arguments section | OK — line 38 |
| ✅ | ST-007 | Arguments table format | OK |
| ✅ | ST-008 | Skills documented | OK — in Configuration tables |
| ✅ | ST-009 | Subagents documented | OK — in Configuration tables |
| ✅ | ST-010 | Examples present | OK — multiple code blocks |
| ⚠️ | ST-011 | 50-200 lines ideal | **WARNING — 727 lines** |
| ❌ | ST-012 | < 500 lines max | **ERREUR — 727 lines** |
| ✅ | ST-013 | Headers correct | OK |
| ✅ | ST-014 | No empty sections | OK |
| ✅ | ST-015 | Logical order | OK |
| ✅ | ST-016 | Error Handling | OK — implicit in phases |
| ⚠️ | ST-017 | Constraints section | WARNING — absent |
| ✅ | ST-018 | Breakpoints ASCII box | OK |
| ⚠️ | ST-019 | See Also section | WARNING — absent |
| ✅ | ST-020 | Flags section | OK — documented |

### CAT-RD: Rédaction (25 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ❌ | **RD-001** | **< 5000 tokens** | **BLOQUANT — ~7250 tokens estimated** |
| ⚠️ | RD-002 | No duplicates | WARNING — repeated MANDATORY blocks |
| ✅ | RD-003 | Code language specified | OK |
| ✅ | RD-004 | Tables for structure | OK |
| ✅ | RD-005 | `@` syntax for refs | OK |
| ✅ | RD-006 | No markdown links | OK |
| ✅ | RD-007 | `@subagent` format | OK |
| ✅ | RD-008 | Imperative verbs | OK |
| ✅ | RD-009 | Explicit conditions | OK — IF/WHEN used |
| ✅ | RD-010 | No double negation | OK |
| ✅ | RD-011 | `--flag` format | OK |
| ✅ | RD-012 | No hardcoded paths | OK — uses `{slug}` placeholders |
| ✅ | RD-013 | Variable placeholders | OK |
| ⚠️ | RD-014 | Terminology consistency | WARNING — French/English mix |
| ✅ | RD-015 | No TODO/FIXME | OK |
| ✅ | RD-016 | No personal comments | OK |
| ⚠️ | RD-017 | Emojis limited | WARNING — ⚠️, ✅, 🪝, 💡 throughout content |
| ✅ | RD-018 | `@` refs valid | OK — all verified to exist |
| ✅ | RD-019 | `!` context < 30 lines | OK |
| ⚠️ | RD-020 | Instructions < 100 lines | WARNING — some sections exceed |
| ✅ | RD-021 | Frontmatter < 15 lines | OK |
| ✅ | RD-022 | Specificity | OK — single purpose |
| ✅ | RD-023 | Determinism | OK |
| ✅ | RD-024 | Testability | OK |
| ✅ | RD-025 | Maintainability | OK |

### CAT-WF: Workflow (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | WF-001 | Coherent workflow | OK — phases connected |
| ✅ | WF-002 | Logical sequence | OK — P1 → P2 → P3 |
| ✅ | WF-003 | No infinite loops | OK |
| ✅ | WF-004 | Explicit exit points | OK — COMPLETION section |
| ✅ | WF-005 | Complete IF/ELSE | OK |
| ✅ | WF-006 | MANDATORY marked | OK |
| ✅ | WF-007 | Breakpoints at decisions | OK — BP1, BP2 |
| ✅ | WF-008 | Fallbacks documented | OK |
| ✅ | WF-009 | DAG representable | OK |
| ⚠️ | WF-010 | Routing documented | WARNING — no explicit routing table |

### CAT-IN: Integration (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | IN-001 | Skills documented | OK |
| ✅ | IN-002 | Subagents documented | OK |
| ✅ | IN-003 | Hooks documented | OK |
| ⚠️ | IN-004 | MCP documented | WARNING — not in Configuration |
| ⚠️ | IN-005 | Personas documented | WARNING — absent |
| ✅ | IN-006 | Thinking level | OK |
| ❌ | IN-007 | Routing table | **ERREUR — no explicit routing to `/brief`, `/quick`** |
| ✅ | IN-008 | MANDATORY breakpoints | OK |
| ✅ | IN-009 | Output paths | OK |
| ⚠️ | IN-010 | Error handling | WARNING — could be more explicit |
| ⚠️ | IN-011 | Fallbacks | WARNING — not comprehensive |
| ✅ | IN-012 | Context schema | OK |
| ⚠️ | IN-013 | Session persistence | WARNING — not explicit |
| ✅ | IN-014 | Memory hooks | OK — `post-phase-3` documented |
| ℹ️ | IN-015 | validate_command.py | INFO |

### CAT-DG: Detection (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | DG-001 | Skill candidate | OK — uses references |
| ✅ | DG-002 | Subagent candidate | OK — properly delegated |
| 💡 | DG-003 | Reference candidate | SUGGESTION — Phase 2/3 > 100 lines |
| 💡 | DG-004 | Pattern repetition | SUGGESTION — MANDATORY blocks |
| ✅ | DG-005 | Template candidate | OK |
| ✅ | DG-006 | Hook candidate | OK |
| ✅ | DG-007 | Script candidate | OK |
| 💡 | DG-008 | Decomposition | SUGGESTION — 727 lines, consider split |
| ✅ | DG-009 | References dir | OK — uses `references/` |
| ✅ | DG-010 | No overlap | OK |

---

## Blocking Errors (MUST FIX)

### 1. FM-010: Bash without pattern restriction

**Severity**: BLOQUANT (-10 points)
**Location**: Frontmatter line 7

```yaml
# Current (INCORRECT)
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]

# Required (CORRECT)
allowed-tools: [Read, Write, Edit, Bash(git:*), Bash(python3:*), Grep, Glob, Task]
```

**Fix**: Restrict Bash to specific command patterns used in the command:
- `Bash(git:*)` — for git operations
- `Bash(python3:*)` — for hook execution

---

### 2. RD-001: Token count exceeds 5000

**Severity**: BLOQUANT (-10 points)
**Current**: ~7250 tokens (727 lines, ~29KB)
**Maximum**: 5000 tokens

**Fix Options**:

1. **Extract Phase details to references** (Recommended)
   ```
   references/epci/
   ├── phase-1-planning.md       # ~150 lines
   ├── phase-2-implementation.md # ~200 lines
   ├── phase-3-finalization.md   # ~150 lines
   └── turbo-mode.md             # Already exists
   ```

2. **Remove redundant MANDATORY blocks**
   - Consolidate repeated `⚠️ MANDATORY` instructions
   - Reference a single "Mandatory Actions" section

3. **Simplify Output templates**
   - Move detailed templates to `references/epci/templates/`
   - Keep inline just the essential format

---

## Errors (SHOULD FIX)

### 1. ST-003: No explicit Process/Workflow section

**Severity**: ERREUR (-3 points)

The command uses Phase structure (Phase 1, 2, 3) instead of a single `## Process` section. While semantically valid, it doesn't match the expected structure.

**Fix**: Add an explicit overview section:
```markdown
## Workflow Overview

```mermaid
[existing diagram]
```

Phases:
1. **Phase 1**: Planning — @plan-validator
2. **Phase 2**: TDD Implementation — @code-reviewer, @security-auditor*, @qa-reviewer*
3. **Phase 3**: Finalization — @doc-generator, commit
```

---

### 2. ST-005: No Output section

**Severity**: ERREUR (-3 points)

**Fix**: Add explicit Output section:
```markdown
## Output

| Phase | Output |
|-------|--------|
| Phase 1 | §2 added to Feature Document |
| Phase 2 | §3 Part 1 (Implementation) |
| Phase 3 | §3 Part 2 (Finalization), `.epci-commit-context.json` |
```

---

### 3. ST-012: File exceeds 500 lines

**Severity**: ERREUR (-3 points)
**Current**: 727 lines

Linked to RD-001 — fixing token count will address this.

---

### 4. IN-007: Routing not explicitly documented

**Severity**: ERREUR (-3 points)

**Fix**: Add routing table in See Also or dedicated section:
```markdown
## Related Commands

| Command | Relationship |
|---------|--------------|
| `/brief` | Creates §1 — prerequisite for `/epci` |
| `/quick` | Alternative for TINY/SMALL features |
| `/commit` | Called after Phase 3 for git commit |
```

---

## Generation Suggestions

| Type | Reason | Suggested Action |
|------|--------|------------------|
| Reference | Phase 2 > 150 lines | Extract to `references/epci/phase-2-implementation.md` |
| Reference | Phase 3 > 120 lines | Extract to `references/epci/phase-3-finalization.md` |
| Consolidation | 6× "MANDATORY" blocks | Create single instruction reference |

---

## Action Items

- [ ] **[BLOCKING]** Fix FM-010: Add Bash pattern restrictions
- [ ] **[BLOCKING]** Fix RD-001: Reduce to < 5000 tokens via extraction
- [ ] Fix ST-003: Add explicit Workflow Overview section
- [ ] Fix ST-005: Add Output section
- [ ] Fix ST-012: Reduce to < 500 lines (follows from RD-001)
- [ ] Fix IN-007: Add Related Commands section
- [ ] Consider: Consolidate MANDATORY instruction blocks
- [ ] Consider: Add Constraints section
- [ ] Consider: Add See Also section

---

## Score Calculation

| Severity | Count | Impact |
|----------|-------|--------|
| BLOQUANT | 2 | -20 |
| ERREUR | 5 | -15 |
| WARNING | 10 | -10 |
| SUGGESTION | 3 | 0 |

**Score**: 100 - 20 - 15 - 10 = **55/100**

**Verdict**: **BLOCKED** — Must fix 2 blocking errors before merge

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ❌ | Error (blocking or not) |
| ⚠️ | Warning |
| 💡 | Suggestion |
| ✅ | Compliant |
| ℹ️ | Info |

---

*Command Auditor v1.0.0 — Audit completed*
