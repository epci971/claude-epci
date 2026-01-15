# Audit Report — debug.md

> **Date**: 2026-01-15
> **Auditor**: command-auditor v1.0.0
> **Mode**: STRICT

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Score | **77**/100 |
| Rules Checked | 95 |
| Blocking Errors | 1 |
| Errors | 3 |
| Warnings | 4 |
| Suggestions | 4 |
| **Verdict** | **BLOCKED** |

---

## Detected Workflow

```mermaid
flowchart TD
    A[Start] --> B[Step 0: Input Clarification]
    B --> C[Phase 1: Diagnostic]
    C --> D{Evaluate Routing}
    D -->|Obvious cause| E[Route A: Trivial]
    D -->|1 cause, <50 LOC| F[Route B: Quick]
    D -->|≥2 Complet criteria| G[Route C: Complet]
    E --> H[Apply fix]
    H --> I[End - Trivial]
    F --> J[Thought tree + TDD]
    J --> K[End - Quick]
    G --> L[Solution Scoring]
    L --> M{BREAKPOINT}
    M -->|Continue| N[Implement Fix]
    M -->|Cancel| O[End - Cancelled]
    N --> P[@code-reviewer]
    P --> Q[Generate Debug Report]
    Q --> R[End - Complet]
```

---

## Results by Category

### CAT-FM: Frontmatter (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | FM-001 | Frontmatter present | OK (délimiteurs `---`) |
| ✅ | FM-002 | Description present | OK |
| ✅ | FM-003 | Description ≤ 500 chars | OK (~220 chars) |
| ❌ | FM-004 | Description starts with verb | "Structured..." → Devrait commencer par "Diagnose..." |
| ✅ | FM-005 | Frontmatter < 15 lines | OK (7 lignes) |
| ✅ | FM-006 | argument-hint present | OK |
| ✅ | FM-007 | argument-hint format | OK (`[optional]`, `--flag`) |
| ✅ | FM-008 | allowed-tools present | OK |
| ✅ | FM-009 | Tools valid | OK |
| ❌ | **FM-010** | **Bash restricted** | **BLOQUANT: `Bash` sans pattern restriction** |
| ✅ | FM-011 | No tabs | OK |
| ✅ | FM-012 | Special chars escaped | OK |
| ✅ | FM-013 | Known fields only | OK |
| ✅ | FM-014 | Bash for `!` | N/A |
| ✅ | FM-015 | Budget description | OK |

### CAT-ST: Structure (20 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | ST-001 | Overview present | OK |
| ✅ | ST-002 | Overview 2-4 sentences | OK (4 bullet points) |
| ✅ | ST-003 | Process present | OK |
| ✅ | ST-004 | Numbered steps | OK (`### Phase X:`, `### Step X:`) |
| ❌ | ST-005 | Output section | **ERREUR: Pas de section `## Output`** (seulement `## Completion`) |
| ✅ | ST-006 | Arguments section | OK |
| ✅ | ST-007 | Arguments table | OK |
| ✅ | ST-008 | Skills documented | OK (`## Skills Loaded`) |
| ✅ | ST-009 | Subagents documented | OK (Configuration table) |
| ✅ | ST-010 | Concrete examples | OK (`## Examples`) |
| ⚠️ | ST-011 | 50-200 lines (ideal) | WARNING: 495 lignes |
| ✅ | ST-012 | < 500 lines | OK (495 < 500) |
| ✅ | ST-013 | Headers correct | OK |
| ✅ | ST-014 | No empty sections | OK |
| ✅ | ST-015 | Logical order | OK |
| ⚠️ | ST-016 | Error Handling section | WARNING: Pas de section dédiée |
| ⚠️ | ST-017 | Constraints section | WARNING: Absent |
| ✅ | ST-018 | Breakpoints ASCII box | OK |
| ⚠️ | ST-019 | See Also section | WARNING: Absent malgré référence à `/commit` |
| ✅ | ST-020 | Flags section | OK |

### CAT-RD: Rédaction (25 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | RD-001 | < 5000 tokens | OK (~4750 tokens) |
| ✅ | RD-002 | No duplicate content | OK |
| ✅ | RD-003 | Code blocks with lang | OK |
| ✅ | RD-004 | Tables for structured data | OK |
| ✅ | RD-005-007 | References format | OK |
| ✅ | RD-008 | Imperative instructions | OK |
| ✅ | RD-009 | Explicit conditions | OK (IF/ELSE/WHEN) |
| ✅ | RD-010-016 | Content quality | OK |
| ✅ | RD-017 | Emojis limited | OK (⏸️, 🔍, 💡, ⚠️) |
| ✅ | RD-018-025 | Content rules | OK |

### CAT-WF: Workflow (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | WF-001 | Coherent workflow | OK |
| ✅ | WF-002 | Logical sequence | OK |
| ✅ | WF-003 | No infinite loops | OK |
| ✅ | WF-004 | Explicit exits | OK ("End workflow") |
| ✅ | WF-005 | Complete IF/ELSE | OK |
| ✅ | WF-006 | MANDATORY marked | OK |
| ✅ | WF-007 | Breakpoints at decisions | OK |
| ✅ | WF-008 | Fallbacks documented | OK (Context7 fallback) |
| ✅ | WF-009 | DAG representable | OK |
| ✅ | WF-010 | Routing documented | OK |

### CAT-IN: Integration (15 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| ✅ | IN-001 | Skills documented | OK |
| ✅ | IN-002 | Subagents documented | OK |
| ✅ | IN-003 | Hooks documented | OK (pre-debug, post-debug) |
| ✅ | IN-004 | MCP documented | OK (Context7, Sequential) |
| ✅ | IN-006 | Thinking level | OK (think, think hard) |
| ✅ | IN-007 | Routing documented | OK |
| ✅ | IN-008 | MANDATORY breakpoints | OK |
| ✅ | IN-009 | Output paths | OK (`docs/debug/<slug>-<date>.md`) |
| ⚠️ | IN-010 | Error handling | Partiel |
| ✅ | IN-011 | Fallbacks | OK |
| ✅ | IN-012 | Context file schema | OK (JSON --commit) |
| ✅ | IN-013 | Session persistence | OK |
| ❌ | IN-014 | Memory hooks | **ERREUR: `post-phase-3` non documenté** |

### CAT-DG: Detection (10 rules)

| Status | ID | Rule | Detail |
|--------|-----|------|--------|
| 💡 | DG-001 | Skill candidate | Section logique > 500 tokens |
| 💡 | DG-003 | Reference candidate | Route C > 100 lignes |
| 💡 | DG-005 | Template candidate | Debug Report template |
| 💡 | DG-008 | Decomposition | 495 lignes, proche seuil |
| ✅ | DG-010 | No overlap | OK |

---

## Blocking Errors (MUST FIX)

### 1. FM-010: Bash sans restriction pattern

**Line**: 7 (frontmatter)
**Current**:
```yaml
allowed-tools: [Read, Glob, Grep, Bash, Task, WebFetch, WebSearch, Write, Edit]
```

**Fix**:
```yaml
allowed-tools: [Read, Glob, Grep, Bash(git:*), Bash(npm:*), Bash(python:*), Task, WebFetch, WebSearch, Write, Edit]
```

Ou si Bash est nécessaire sans restriction, documenter pourquoi avec un commentaire explicatif ou utiliser pattern générique mais justifié.

---

## Errors (SHOULD FIX)

### 1. FM-004: Description ne commence pas par verbe

**Line**: 2
**Current**: `"Structured debugging workflow with adaptive routing..."`
**Fix**: `"Diagnose and fix bugs using structured workflow with adaptive routing..."`

### 2. ST-005: Section Output manquante

**Location**: Structure
**Issue**: La section `## Completion` ne remplace pas `## Output`
**Fix**: Ajouter une section `## Output` ou renommer `## Completion` en `## Output` et déplacer/fusionner le contenu

### 3. IN-014: Memory hooks non documentés

**Location**: Fin du workflow
**Issue**: Pas de documentation `post-phase-3` pour sauvegarder l'historique debug
**Fix**: Ajouter après `## Completion`:
```markdown
**Execute `post-debug-complete` hooks** (if configured)

For history tracking, consider calling memory hook:
```bash
python3 src/hooks/runner.py post-debug --context '{
  "mode": "<Trivial|Quick|Complet>",
  "bug_slug": "<slug>",
  "root_cause": "<cause>",
  "files_modified": ["<files>"]
}'
```
```

---

## Warnings (CONSIDER FIXING)

| ID | Issue | Suggestion |
|----|-------|------------|
| ST-011 | 495 lignes | Extraire content dense vers `references/` |
| ST-016 | Pas de Error Handling | Ajouter section dédiée |
| ST-017 | Pas de Constraints | Ajouter limites/boundaries |
| ST-019 | Pas de See Also | Ajouter références `/commit`, `/epci` |

---

## Generation Suggestions

| Type | Reason | Suggested Action |
|------|--------|------------------|
| Reference | Route C > 100 lignes | Extraire vers `references/complet-mode.md` |
| Template | Debug Report format | Extraire vers `references/debug-report-template.md` |
| Decomposition | 495 lignes dense | Considérer split en références |

---

## Action Items

- [ ] **CRITICAL**: Fix FM-010 — Restrict Bash patterns in allowed-tools
- [ ] Fix FM-004 — Description starts with verb ("Diagnose...")
- [ ] Fix ST-005 — Add or rename `## Output` section
- [ ] Fix IN-014 — Document memory hooks for debug history
- [ ] Consider ST-016 — Add `## Error Handling` section
- [ ] Consider extracting Route C to `references/complet-mode.md`

---

## Score Calculation

```
Score = 100 - (BLOQUANT × 10) - (ERREUR × 3) - (WARNING × 1)
Score = 100 - (1 × 10) - (3 × 3) - (4 × 1)
Score = 100 - 10 - 9 - 4
Score = 77/100

Verdict: BLOCKED (has blocking error)
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ❌ | Error (blocking or not) |
| ⚠️ | Warning |
| 💡 | Suggestion |
| ✅ | Compliant |

---

*Command Auditor v1.0.0 — EPCI Plugin*
