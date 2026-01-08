---
description: >-
    EPCI entry point. Validates and reformulates the brief, performs thorough
    exploration, evaluates complexity, generates output (inline brief or Feature
    Document), and routes to appropriate workflow (/quick, /epci).
argument-hint: "[brief] [--turbo] [--rephrase] [--no-rephrase] [--c7] [--seq] [--magic] [--play]"
allowed-tools: [Read, Write, Glob, Grep, Bash, Task]
---

# EPCI Brief — Entry Point

## Overview

This command is the single entry point for the EPCI workflow.
It transforms a raw brief into a structured brief and routes to the appropriate workflow.

**Key principle**: Validate the need BEFORE exploring the codebase.

## Configuration

| Element       | Value                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| **Thinking**  | `think hard` (default) / `ultrathink` (LARGE or high uncertainty)                                          |
| **Skills**    | project-memory, epci-core, architecture-patterns, flags-system, mcp, personas, [stack-skill auto-detected] |
| **Subagents** | @Explore (thorough), @clarifier (turbo mode)                                                               |

**Thinking mode selection:**

- `think hard`: Default for most briefs
- `ultrathink`: When complexity appears LARGE or technical uncertainty is high

### --turbo Mode (MANDATORY Instructions)

**When `--turbo` flag is active, you MUST follow these rules:**

1. **Use @clarifier (Haiku)** for fast clarification:

    ```
    Invoke @clarifier via Task tool with model: haiku
    Maximum 2 questions, suggestions included
    Skip deep analysis, focus on blocking ambiguities
    ```

2. **Use @Explore with Haiku model** for faster codebase analysis:

    ```
    Invoke @Explore via Task tool with model: haiku
    Focus: Quick scan, file identification only
    Skip: Deep pattern analysis (defer to implementation)
    ```

3. **Maximum 2 clarification questions** — Focus on blocking ambiguities only

4. **Auto-accept suggestions** if confidence > 0.7:
    - If AI suggestions have high confidence, skip question [1] option
    - Present only [2] Validate, [3] Modify, [4] Launch

5. **Suggest --turbo automatically** if:
    - `.project-memory/` exists (experienced project)
    - Coming from `/brainstorm` with EMS > 60
    - Category is STANDARD (not LARGE)

6. **Reduced breakpoints** — Compact format, single confirmation step

**Turbo Suggestion Logic:**

```
IF .project-memory/ exists AND category != LARGE:
   Display: "💡 --turbo recommandé (projet connu)"
   Auto-add --turbo to recommended command
```

## Process

**Follow ALL steps in sequence. Steps 1 and 4 have MANDATORY BREAKPOINTS.**

---

### Step 0: Load Project Memory

**Skill**: `project-memory`

Load project context from `.project-memory/` directory. The skill handles:

- Reading context, conventions, settings, patterns
- Loading velocity metrics and feature history
- Applying defaults and displaying memory status

**If `.project-memory/` does not exist:** Continue without context. Suggest `/memory init` at workflow end.

---

### Step 1: Reformulation + Validation (MANDATORY BREAKPOINT)

**BREAKPOINT OBLIGATOIRE** — Toujours affiche pour valider le besoin AVANT exploration.

#### SKIP CONDITIONS (rares)

| Condition | How to detect | Action |
|-----------|---------------|--------|
| **Flag `--no-rephrase`** | User explicitly skipped | SKIP — go to Step 2 |
| **Brief already structured** | Contains "## Objectif", "## Context", "## Critères" headers | SKIP — already from /brainstorm |

**If ANY skip condition is met:** Display brief as-is with validation breakpoint, then proceed to Step 2.

#### TRIGGER CONDITIONS (if ANY is true → MUST reformulate)

| Condition | How to detect |
|-----------|---------------|
| **Flag `--rephrase`** | User explicitly requested |
| **Voice artifacts detected** | Contains: `euh`, `hum`, `genre`, `tu vois`, `quoi`, `en fait`, `du coup`, `truc`, `machin` |
| **Vague/incomplete brief** | < 30 words AND contains vague terms: `système`, `améliorer`, `ajouter`, `truc`, `chose`, `something` |
| **No clear action verb** | Missing: `implémenter`, `créer`, `ajouter`, `corriger`, `fixer`, `add`, `create`, `fix`, `implement` |
| **Self-corrections detected** | Contains: `non`, `pardon`, `enfin`, `plutôt`, `je veux dire` |

#### ACTION: Reformulation Process

**If triggered, you MUST:**

1. **Clean the brief:**
   - Remove hesitations: `euh`, `hum`, `uh`, `um`, `bah`, `ben`
   - Remove fillers: `tu vois`, `genre`, `quoi`, `en fait`, `du coup`
   - Apply self-corrections: "CSV non pardon JSON" → "JSON"
   - Normalize voice: "je veux" → "Le système doit", "faudrait que" → "doit"

2. **Detect template type:**
   - **FEATURE**: Keywords `ajouter`, `créer`, `implémenter`, `nouveau`, `add`, `create`
   - **PROBLEM**: Keywords `bug`, `erreur`, `fixer`, `corriger`, `cassé`, `fix`, `broken`
   - **DECISION**: Keywords `choisir`, `quelle`, `comment`, `stratégie`, `which`, `how`

3. **Restructure into format:**

```
**Objectif**: [Action verb] + [what] + [purpose]
**Contexte**: [Domain detected] | [Initial understanding]
**Contraintes**: [Extracted from brief OR "À définir"]
**Critères de succès**: [Based on template type]
```

#### BREAKPOINT Format (ALWAYS DISPLAYED)

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📝 VALIDATION DU BRIEF                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📄 BRIEF ORIGINAL                                                   │
│ "{raw_brief}"                                                       │
│                                                                     │
│ [If reformulated:]                                                  │
│ 📊 DÉTECTION                                                        │
│ ├── Artefacts vocaux: {COUNT} trouvés                              │
│ ├── Type détecté: {FEATURE|PROBLEM|DECISION}                       │
│ └── Reformulation: OUI                                             │
│                                                                     │
│ ✨ BRIEF REFORMULÉ                                                  │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ **Objectif**: {goal}                                            │ │
│ │ **Contexte**: {context}                                         │ │
│ │ **Contraintes**: {constraints}                                  │ │
│ │ **Critères de succès**: {success_criteria}                      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ [If NOT reformulated:]                                              │
│ ✅ Brief propre — pas de reformulation nécessaire                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│   [1] Valider → Continuer vers l'exploration                       │
│   [2] Modifier → Je reformule moi-même                             │
│   [3] Annuler → Arrêter le workflow                                │
└─────────────────────────────────────────────────────────────────────┘
```

**Wait for user choice:**

| Choice | Action |
|--------|--------|
| **[1] Valider** | Store validated brief, proceed to Step 2 |
| **[2] Modifier** | Wait for user input, update brief, show breakpoint again |
| **[3] Annuler** | Stop workflow |

#### --turbo mode behavior

- Auto-validate if brief is clean (no artifacts detected)
- Compact format display
- Only show breakpoint if > 3 voice artifacts detected

---

### Step 2: Exploration (MANDATORY)

**🪝 Execute `pre-brief` hooks** (if configured in `hooks/active/`)

**Use the VALIDATED brief from Step 1.**

**Action:** Invoke @Explore (thorough level) using the Task tool to:

- Scan complete project structure
- Identify all technologies, frameworks, versions
- Map architectural patterns (Repository, Service, Controller, etc.)
- Identify files potentially impacted by the brief
- Estimate dependencies and coupling
- Detect existing test patterns

**Internal outputs** (store for Step 3):

- List of candidate files with probable action (Create/Modify/Delete)
- Detailed technical stack
- Detected architectural patterns
- Identified risks

#### Error Handling

If @Explore fails or times out:
1. Log warning: "Exploration incomplete"
2. Continue with partial results if available
3. Mark complexity as UNKNOWN
4. Suggest `--think-hard` for safety
5. Display warning in Step 4 breakpoint

---

### Step 3: Analysis & Complexity Evaluation (Internal)

**DO NOT OUTPUT ANYTHING IN THIS STEP** — Prepare data for the breakpoint.

Analyze the brief and exploration results to prepare:

#### 3.1 Complexity Evaluation

| Criteria       | TINY | SMALL    | STANDARD | LARGE |
| -------------- | ---- | -------- | -------- | ----- |
| Files          | 1    | 2-3      | 4-10     | 10+   |
| Estimated LOC  | <50  | <200     | <1000    | 1000+ |
| Risk           | None | Low      | Medium   | High  |
| Tests required | No   | Optional | Yes      | Yes+  |
| Arch impacted  | No   | No       | Possible | Yes   |

**Flag Auto-Activation:**

| Condition                      | Threshold | Flag           |
| ------------------------------ | --------- | -------------- |
| Files impacted                 | 3-10      | `--think`      |
| Files impacted                 | >10       | `--think-hard` |
| Refactoring/migration detected | true      | `--think-hard` |
| Sensitive file patterns        | any match | `--safe`       |
| Complexity score               | >0.7      | `--wave`       |

**Sensitive file patterns:**

```
**/auth/**  **/security/**  **/payment/**
**/password/**  **/api/v*/admin/**
```

#### 3.2 Clarification Questions (2-3 max)

- Identify gaps, ambiguities, missing information
- Prepare suggestions for each question

#### 3.3 AI Suggestions (3-5 max)

- Architecture recommendations
- Implementation approach
- Risks and mitigations
- Stack-specific best practices

#### 3.4 Persona Detection (F09)

- Score all 6 personas using algorithm from `src/skills/personas/SKILL.md`
- `Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)`
- If score > 0.6: Auto-activate persona
- If score 0.4-0.6: Suggest persona in breakpoint
- Include active/suggested persona in FLAGS line

#### 3.5 MCP Activation (F12)

- Based on activated personas, determine MCP servers to activate
- Check keyword triggers in brief text
- Check file pattern triggers in impacted files
- Check flag triggers (`--c7`, `--seq`, `--magic`, `--play`, `--think-hard`)
- Auto-activate MCPs based on `src/skills/mcp/SKILL.md` matrix
- Include active MCP flags in FLAGS line: `--c7 (auto: architect)`

---

### Step 4: BREAKPOINT — Analysis Review (MANDATORY)

**MANDATORY:** Display this breakpoint and WAIT for user choice before proceeding.

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

| Choice           | Action                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **[1] Répondre** | Wait for user answers, incorporate into brief, show breakpoint again                     |
| **[2] Valider**  | Use suggestions as-is, generate output (Step 5), show breakpoint again with updated eval |
| **[3] Modifier** | Wait for modifications, update suggestions, show breakpoint again                        |
| **[4] Lancer**   | Generate output (Step 5) then execute the recommended command                            |

**After [1], [2], or [3]:** Update analysis and show breakpoint again until user chooses [4].
**After [4]:** Proceed to Step 5 (generate output) then Step 6 (execute command).

---

### Step 5: Generate Output (MANDATORY)

**DO NOT SKIP THIS STEP** — You MUST generate the appropriate output based on complexity.

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

→ Launch `/quick`
```

#### If STANDARD or LARGE → Feature Document (USE WRITE TOOL)

**MANDATORY:** Use the **Write tool** to create the file `docs/features/<slug>.md`

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

| Flag           | Source | Reason              |
| -------------- | ------ | ------------------- |
| `--think-hard` | auto   | >10 files impacted  |
| `--safe`       | auto   | auth files detected |
| `--wave`       | auto   | complexity > 0.7    |

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

---

**🪝 Execute `post-brief` hooks** (if configured in `hooks/active/`)

---

### Step 6: Execute Recommended Command

**MANDATORY:** After generating output, execute the recommended command.

**Routing table:**

| Category | Command              | Output           | Typical Flags               |
| -------- | -------------------- | ---------------- | --------------------------- |
| TINY     | `/epci:quick --autonomous` | Inline brief | `--autonomous` (auto)      |
| SMALL    | `/epci:quick`        | Inline brief     | `--think` if 3+ files       |
| STANDARD | `/epci:epci`         | Feature Document | `--think` or `--think-hard` |
| LARGE    | `/epci:epci --large` | Feature Document | `--think-hard --wave`       |

**TINY Optimized Routing:**
```
IF category == TINY:
   Skip clarification questions (no ambiguity expected)
   Route directly to /quick --autonomous
   Display: "Mode TINY détecté → exécution autonome"
```

**Note:** `--large` is an alias for `--think-hard --wave`. Both forms are accepted.

**Action:** Use the SlashCommand tool to execute the recommended command with flags.

---

### Step 7: Rules Suggestion (Optional)

If `.claude/` directory does not exist in the project:

```
💡 Aucune règle projet détectée (.claude/ absent).
   → Lancez /rules pour générer les conventions projet automatiquement.
```

This suggestion appears at the end of the breakpoint, after the recommended command.
The user can run `/rules` before or after the main workflow.
