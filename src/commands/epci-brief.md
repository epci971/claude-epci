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
| **Skills** | project-memory-loader, epci-core, architecture-patterns, flags-system, [stack-skill auto-detected] |
| **Subagents** | @Explore (thorough) |

**Thinking mode selection:**
- `think hard`: Default for most briefs
- `ultrathink`: When complexity appears LARGE or technical uncertainty is high

## Process

### Step 0: Load Project Memory

**Skill**: `project-memory-loader`

Load project context from `.project-memory/` directory. The skill handles:
- Reading context, conventions, settings, patterns
- Loading velocity metrics and feature history
- Applying defaults and displaying memory status

**If `.project-memory/` does not exist:** Continue without context. Suggest `/epci-memory init` at workflow end.

---

### Step 1: Exploration Complète

**Invoke @Explore** (thorough level) to:
- Scan complete project structure
- Identify all technologies, frameworks, versions
- Map architectural patterns (Repository, Service, Controller, etc.)
- Identify files potentially impacted by the brief
- Estimate dependencies and coupling
- Detect existing test patterns

**Internal outputs** (for use in subsequent steps):
- List of candidate files with probable action (Create/Modify/Delete)
- Detailed technical stack
- Detected architectural patterns
- Identified risks

Analyze the brief to identify:
- Clear and actionable elements
- Ambiguities and unclear areas
- Critical missing information
- Potential inconsistencies

### Step 2: Clarification Loop (Intelligent)

**Skill**: `clarification-intelligente`

Use the intelligent clarification system (F05) to generate context-aware questions:

#### If Project Memory Available

1. **Analyze Brief**
   ```python
   from project_memory.clarification_analyzer import analyze_brief
   analysis = analyze_brief(brief)
   # → keywords, domain, gaps
   ```

2. **Find Similar Features**
   ```python
   similar = manager.find_similar_features(analysis.keywords, threshold=0.3)
   # → List of similar past features with scores
   ```

3. **Generate Intelligent Questions**
   ```python
   from project_memory.question_generator import generate_questions
   result = generate_questions(brief, context, similar_features, gaps, persona)
   # → Max 3 targeted questions with suggestions
   ```

4. **Present Questions with Context**
   ```
   📋 CLARIFICATION (basée sur l'historique projet)

   [If similar feature found]
   💡 Feature similaire détectée: `{slug}` (score: {score}%)

   Questions:
   1. {question_1} (Suggestion: {suggestion_1})
   2. {question_2} (Suggestion: {suggestion_2})
   3. {question_3}
   ```

#### If Project Memory Unavailable (Graceful Degradation)

Fall back to generic questions by category:

| Category | Example Questions |
|----------|-------------------|
| **Business/Value** | Why? For whom? What business impact? |
| **Scope** | What's included/excluded? What limits? |
| **Constraints** | Technical? Time? Budget? Dependencies? |
| **Priority** | Criticality? Deadline? Blocking what? |

#### Question Types (F05)

| Type | Trigger | Example |
|------|---------|---------|
| **REUSE** | Similar feature found | "Feature X uses pattern Y. Reuse?" |
| **TECHNICAL** | Domain-specific gap | "Which auth method: OAuth, JWT?" |
| **SCOPE** | Unclear boundaries | "What is included/excluded?" |
| **INTEGRATION** | Existing components | "Integrate with Messenger?" |
| **PRIORITY** | Persona-specific | "What reliability guarantee?" |

**Rules:**
- Maximum 3 questions per iteration
- Maximum 3 clarification iterations
- Prioritize blocking questions
- Include suggestions based on project history
- Adapt to active persona (when F09 available)

### Step 3: AI Suggestions

Propose improvements based on @Explore analysis:
- Design suggestions (based on architecture-patterns)
- Best practices for detected stack
- Context-specific attention points
- Identified potential risks

### Step 4: Complexity Evaluation

| Criteria | TINY | SMALL | STANDARD | LARGE | SPIKE |
|----------|------|-------|----------|-------|-------|
| Files | 1 | 2-3 | 4-10 | 10+ | ? |
| Estimated LOC | <50 | <200 | <1000 | 1000+ | ? |
| Risk | None | Low | Medium | High | Unknown |
| Tests required | No | Optional | Yes | Yes+ | N/A |
| Arch impacted | No | No | Possible | Yes | ?

### Step 4b: Flag Auto-Activation

Based on the exploration and complexity evaluation, detect flags to auto-activate:

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

**Output:** List of suggested flags with source (auto/recommended)

### Step 5: Génération Output

Based on complexity evaluation, generate the appropriate output:

#### If TINY or SMALL → Inline Brief

Generate a structured brief in the response (no file created):

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

## Category: [TINY|SMALL]

## Suggested Flags
- [flag] (auto/recommended) — if any detected

→ Launch `/epci-quick`
```

#### If STANDARD or LARGE → Feature Document

Create file `docs/features/<slug>.md`:

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

### Identified Files
| File | Action | Risk |
|------|--------|------|
| path/to/file | Modify | Medium |
| path/to/other | Create | Low |

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

---

## §2 — Implementation Plan
[To be completed by /epci Phase 1]

---

## §3 — Implementation
[To be completed by /epci Phase 2]

---

## §4 — Finalization
[To be completed by /epci Phase 3]
```

#### If SPIKE → Inline Brief for Exploration

Generate inline brief with exploration focus (no Feature Document).

### Step 6: Routing

| Category | Command | Output | Typical Flags |
|----------|---------|--------|---------------|
| TINY | `/epci-quick` | Inline brief | (none or `--fast`) |
| SMALL | `/epci-quick` | Inline brief | `--think` if 3+ files |
| STANDARD | `/epci` | Feature Document | `--think` or `--think-hard` |
| LARGE | `/epci --large` | Feature Document | `--think-hard --wave` |
| SPIKE | `/epci-spike` | Inline brief | `--think-hard` if complex |

**Note:** `--large` is an alias for `--think-hard --wave`. Both forms are accepted.

## Transition

After output generation:
1. Present brief (inline) or confirm Feature Document creation
2. Wait for user confirmation
3. Propose launching the recommended command

```
---
📋 **BRIEF COMPLETE**

[TINY/SMALL] Inline brief generated.
[STANDARD/LARGE] Feature Document created: docs/features/<slug>.md

Category: [CATEGORY]
Suggested flags: [FLAGS] (source: auto/explicit)
Recommended workflow: [COMMAND] [FLAGS]

**Next step:** Launch `[COMMAND] [FLAGS]`?
---
```
