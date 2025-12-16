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
| **Skills** | epci-core, architecture-patterns, [stack-skill auto-detected] |
| **Subagents** | @Explore (thorough) |

**Thinking mode selection:**
- `think hard`: Default for most briefs
- `ultrathink`: When complexity appears LARGE or technical uncertainty is high

## Process

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

### Step 2: Clarification Loop

If ambiguities are detected, ask targeted questions (max 3 iterations):

| Category | Example Questions |
|----------|-------------------|
| **Business/Value** | Why? For whom? What business impact? |
| **Scope** | What's included/excluded? What limits? |
| **Constraints** | Technical? Time? Budget? Dependencies? |
| **Priority** | Criticality? Deadline? Blocking what? |

**Rules:**
- Maximum 5 questions per iteration
- Maximum 3 clarification iterations
- Prioritize blocking questions

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
| Arch impacted | No | No | Possible | Yes | ? |

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

| Category | Command | Output |
|----------|---------|--------|
| TINY | `/epci-quick` | Inline brief |
| SMALL | `/epci-quick` | Inline brief |
| STANDARD | `/epci` | Feature Document created |
| LARGE | `/epci --large` | Feature Document created |
| SPIKE | `/epci-spike` | Inline brief |

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
Recommended workflow: [COMMAND]

**Next step:** Launch `[COMMAND]`?
---
```
