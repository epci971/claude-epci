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

**⚠️ IMPORTANT: Follow ALL steps in sequence. Do NOT skip any step marked MANDATORY.**

### Step 0: Load Project Memory

**Skill**: `project-memory-loader`

Load project context from `.project-memory/` directory. The skill handles:
- Reading context, conventions, settings, patterns
- Loading velocity metrics and feature history
- Applying defaults and displaying memory status

**If `.project-memory/` does not exist:** Continue without context. Suggest `/epci-memory init` at workflow end.

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

### Step 2: Clarification Loop (MANDATORY)

**⚠️ DO NOT SKIP THIS STEP** — Always ask clarification questions before proceeding.

**Action:** Analyze the brief and identify gaps, ambiguities, or missing information.

**Output format — Present to user:**

```
📋 CLARIFICATION

Based on my analysis, I have the following questions:

1. [Question about scope/boundaries]
   → Suggestion: [Your recommendation based on context]

2. [Question about technical choice]
   → Suggestion: [Your recommendation]

3. [Question about priority/constraints]
   → Suggestion: [Your recommendation]

Please answer these questions to proceed.
```

**Question categories to consider:**

| Category | Example Questions |
|----------|-------------------|
| **Scope** | What's included/excluded? What are the boundaries? |
| **Technical** | Which approach: A or B? Which library/pattern? |
| **Constraints** | Performance requirements? Security concerns? |
| **Integration** | How does this interact with existing components? |

**Rules:**
- Ask 2-3 focused questions maximum
- Provide suggestions based on exploration results
- Wait for user response before proceeding to Step 3
- If brief is very clear, ask at least 1 confirmation question

### Step 3: AI Suggestions (MANDATORY)

**⚠️ DO NOT SKIP THIS STEP** — After receiving clarification answers, provide suggestions.

**Action:** Based on exploration and user answers, propose improvements and recommendations.

**Output format — Present to user:**

```
💡 AI SUGGESTIONS

Based on my analysis and your answers, here are my recommendations:

**Architecture:**
- [Suggestion about patterns/structure]

**Implementation:**
- [Suggestion about approach/methodology]

**Risks to consider:**
- [Identified risk and mitigation]

**Best practices for {detected_stack}:**
- [Stack-specific recommendation]
```

**Categories to cover:**
- Design patterns appropriate for the task
- Best practices for the detected stack
- Potential risks and how to mitigate them
- Attention points specific to this project

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
