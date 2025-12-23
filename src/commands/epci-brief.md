---
description: >-
  EPCI entry point. Performs thorough exploration, clarifies ambiguities,
  evaluates complexity, generates output (inline brief or Feature Document),
  and routes to appropriate workflow (/epci-quick, /epci, /epci-spike).
allowed-tools: [Read, Write, Glob, Grep, Bash, Task]
---

# EPCI Brief — Entry Point

## Overview

This command is the single entry point for the EPCI workflow.
It transforms a raw brief into a structured brief and routes to the appropriate workflow.

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think hard` (default) / `ultrathink` (LARGE or high uncertainty) |
| **Skills** | project-memory, epci-core, architecture-patterns, flags-system, [stack-skill auto-detected] |
| **Subagents** | @Explore (thorough) |

**Thinking mode selection:**
- `think hard`: Default for most briefs
- `ultrathink`: When complexity appears LARGE or technical uncertainty is high

## Process

**⚠️ IMPORTANT: Follow ALL steps in sequence. The BREAKPOINT in Step 3 is MANDATORY.**

### Step 0: Load Project Memory

**Skill**: `project-memory`

Load project context from `.project-memory/` directory. The skill handles:
- Reading context, conventions, settings, patterns
- Loading velocity metrics and feature history
- Applying defaults and displaying memory status

**If `.project-memory/` does not exist:** Continue without context. Suggest `/epci-memory init` at workflow end.

---

**🪝 Execute `pre-brief` hooks** (if configured in `hooks/active/`)

---

### Step 1: Exploration (MANDATORY)

**⚠️ DO NOT SKIP THIS STEP** — Use Task tool with @Explore subagent.

**Action:** Invoke @Explore (thorough level) using the Task tool to:
- Scan complete project structure
- Identify all technologies, frameworks, versions
- Map architectural patterns (Repository, Service, Controller, etc.)
- Identify files potentially impacted by the brief
- Estimate dependencies and coupling
- Detect existing test patterns

**Internal outputs** (store for Step 2):
- List of candidate files with probable action (Create/Modify/Delete)
- Detailed technical stack
- Detected architectural patterns
- Identified risks

---

### Step 2: Analysis (Internal — No Output Yet)

**⚠️ DO NOT OUTPUT ANYTHING IN THIS STEP** — Prepare data for the breakpoint.

Analyze the brief and exploration results to prepare:

1. **Clarification Questions** (2-3 max):
   - Identify gaps, ambiguities, missing information
   - Prepare suggestions for each question

2. **AI Suggestions** (3-5 max):
   - Architecture recommendations
   - Implementation approach
   - Risks and mitigations
   - Stack-specific best practices

3. **Complexity Evaluation**:
   - Count impacted files
   - Estimate LOC
   - Assess risk level
   - Determine category (TINY/SMALL/STANDARD/LARGE/SPIKE)

4. **Flag Detection**:
   - Auto-detect flags based on thresholds

---

### Step 3: BREAKPOINT — Analysis Review (MANDATORY)

**⚠️ MANDATORY:** Display this breakpoint and WAIT for user choice before proceeding.

Present ALL analysis results in a consolidated breakpoint:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — ANALYSE DU BRIEF                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 EXPLORATION                                                      │
│ ├── Stack détecté: {STACK}                                         │
│ ├── Fichiers impactés: {FILE_COUNT}                                │
│ ├── Patterns identifiés: {PATTERNS}                                │
│ └── Risques détectés: {RISK_COUNT}                                 │
│                                                                     │
│ 📋 QUESTIONS DE CLARIFICATION                                       │
│                                                                     │
│ Q1: {question_1}                                                    │
│     → Suggestion: {suggestion_1}                                    │
│                                                                     │
│ Q2: {question_2}                                                    │
│     → Suggestion: {suggestion_2}                                    │
│                                                                     │
│ Q3: {question_3}                                                    │
│     → Suggestion: {suggestion_3}                                    │
│                                                                     │
│ 💡 SUGGESTIONS IA                                                   │
│                                                                     │
│ Architecture:                                                       │
│   • {architecture_suggestion}                                       │
│                                                                     │
│ Implémentation:                                                     │
│   • {implementation_suggestion}                                     │
│                                                                     │
│ Risques à considérer:                                               │
│   • {risk_suggestion}                                               │
│                                                                     │
│ Best practices {stack}:                                             │
│   • {stack_suggestion}                                              │
│                                                                     │
│ 📈 ÉVALUATION                                                       │
│ ├── Catégorie: {CATEGORY}                                          │
│ ├── Fichiers: {FILE_COUNT}                                         │
│ ├── LOC estimé: ~{LOC}                                             │
│ ├── Risque: {RISK_LEVEL}                                           │
│ └── Flags: {FLAGS}                                                 │
│                                                                     │
│ 🚀 COMMANDE RECOMMANDÉE: {COMMAND} {FLAGS}                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│                                                                     │
│   [1] Répondre aux questions                                        │
│       → Je fournis mes réponses aux questions de clarification     │
│                                                                     │
│   [2] Valider les suggestions                                       │
│       → J'accepte les suggestions IA telles quelles                │
│                                                                     │
│   [3] Modifier les suggestions                                      │
│       → Je veux changer certaines suggestions                      │
│                                                                     │
│   [4] Lancer {COMMAND} {FLAGS}                                      │
│       → Tout est OK, on passe à l'implémentation                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Wait for user response.** Process based on choice:

| Choice | Action |
|--------|--------|
| **[1] Répondre** | Wait for user answers, incorporate into brief, show breakpoint again |
| **[2] Valider** | Use suggestions as-is, generate output (Step 5), show breakpoint again with updated eval |
| **[3] Modifier** | Wait for modifications, update suggestions, show breakpoint again |
| **[4] Lancer** | Generate output (Step 5) then execute the recommended command |

**After [1], [2], or [3]:** Update analysis and show breakpoint again until user chooses [4].
**After [4]:** Proceed to Step 5 (generate output) then Step 6 (execute command).

---

### Step 4: Complexity Finalization

Finalize complexity evaluation based on user answers:

| Criteria | TINY | SMALL | STANDARD | LARGE | SPIKE |
|----------|------|-------|----------|-------|-------|
| Files | 1 | 2-3 | 4-10 | 10+ | ? |
| Estimated LOC | <50 | <200 | <1000 | 1000+ | ? |
| Risk | None | Low | Medium | High | Unknown |
| Tests required | No | Optional | Yes | Yes+ | N/A |
| Arch impacted | No | No | Possible | Yes | ? |

**Flag Auto-Activation:**

| Condition | Threshold | Flag |
|-----------|-----------|------|
| Files impacted | 3-10 | `--think` |
| Files impacted | >10 | `--think-hard` |
| Refactoring/migration detected | true | `--think-hard` |
| Sensitive file patterns | any match | `--safe` |
| Complexity score | >0.7 | `--wave` |

**Sensitive file patterns:**
```
**/auth/**  **/security/**  **/payment/**
**/password/**  **/api/v*/admin/**
```

---

### Step 5: Generate Output (MANDATORY)

**⚠️ DO NOT SKIP THIS STEP** — You MUST generate the appropriate output based on complexity.

Based on complexity evaluation, generate the appropriate output:

#### If TINY or SMALL → Inline Brief

Generate a structured brief directly in your response (no file created):

```markdown
# Functional Brief — [Title]

## Context
[Summary of the need in 2-3 sentences]

## Detected Stack
[Stack identified by @Explore]

## Target Files
- `path/to/file.ext` (action: Create/Modify)

## Acceptance Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

## Memory Summary
[If .project-memory/ exists, include key context:]
- **Project**: [project name from context.json]
- **Conventions**: [key conventions from conventions.json]
- **Patterns**: [relevant patterns if any]

## Category: [TINY|SMALL]

## Suggested Flags
- [flag] (auto/recommended) — if any detected

→ Launch `/epci-quick`
```

#### If STANDARD or LARGE → Feature Document (USE WRITE TOOL)

**⚠️ MANDATORY:** Use the **Write tool** to create the file `docs/features/<slug>.md`

Create the directory if needed, then write the Feature Document:

```markdown
# Feature Document — [Title]

> **Slug**: `<slug>`
> **Category**: [STANDARD|LARGE]
> **Date**: [YYYY-MM-DD]

---

## §1 — Functional Brief

### Context
[Summary of the need]

### Detected Stack
- **Framework**: [detected]
- **Language**: [detected]
- **Patterns**: [detected patterns]

### Acceptance Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

### Constraints
- [Technical constraint]
- [Other constraint if applicable]

### Out of Scope
- [Explicit exclusion 1]
- [Explicit exclusion 2]

### Evaluation
- **Category**: [STANDARD|LARGE]
- **Estimated files**: X
- **Estimated LOC**: ~Y
- **Risk**: [Low|Medium|High]
- **Justification**: [Reason for categorization]

### Suggested Flags
| Flag | Source | Reason |
|------|--------|--------|
| `--think-hard` | auto | >10 files impacted |
| `--safe` | auto | auth files detected |
| `--wave` | auto | complexity > 0.7 |

### Memory Summary
[If .project-memory/ exists, include context loaded in Step 0:]
- **Project**: [project name]
- **Stack**: [detected stack from context.json]
- **Conventions**: [key conventions]
- **Velocity**: [features_completed count, if available]

---

## §2 — Implementation Plan
[To be completed by /epci Phase 1]

---

## §3 — Implementation & Finalization
[To be completed by /epci Phases 2-3]
```

#### If SPIKE → Inline Brief for Exploration

Generate inline brief with exploration focus (no Feature Document).

---

**🪝 Execute `post-brief` hooks** (if configured in `hooks/active/`)

---

### Step 6: Execute Recommended Command

**⚠️ MANDATORY:** After generating output, execute the recommended command.

**Routing table:**

| Category | Command | Output | Typical Flags |
|----------|---------|--------|---------------|
| TINY | `/epci:epci-quick` | Inline brief | (none) |
| SMALL | `/epci:epci-quick` | Inline brief | `--think` if 3+ files |
| STANDARD | `/epci:epci` | Feature Document | `--think` or `--think-hard` |
| LARGE | `/epci:epci --large` | Feature Document | `--think-hard --wave` |
| SPIKE | `/epci:epci-spike` | Inline brief | `--think-hard` if complex |

**Note:** `--large` is an alias for `--think-hard --wave`. Both forms are accepted.

**Action:** Use the SlashCommand tool to execute the recommended command with flags.
