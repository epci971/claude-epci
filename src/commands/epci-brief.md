---
description: >-
  EPCI entry point. Analyzes raw brief, clarifies ambiguities through
  iterative questions, evaluates complexity and routes to appropriate
  workflow (/epci-quick, /epci, /epci-spike).
allowed-tools: [Read, Glob, Grep, Bash, Task]
---

# EPCI Brief — Entry Point

## Overview

This command is the single entry point for the EPCI workflow.
It transforms a raw brief into a structured brief and routes to the appropriate workflow.

## Process

### Step 1: Initial Analysis

**Invoke @Explore** (medium level) to:
- Scan project structure
- Identify technologies used
- Estimate architectural complexity

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

### Step 5: Routing

| Category | Command | Justification |
|----------|---------|---------------|
| TINY | `/epci-quick` | Immediate execution, no formal plan |
| SMALL | `/epci-quick` | Lightweight integrated plan |
| STANDARD | `/epci` | Complete 3-phase workflow |
| LARGE | `/epci --large` | Enhanced thinking, all subagents |
| SPIKE | `/epci-spike` | Time-boxed exploration |

## Output

Generate the structured brief:

```markdown
# Functional Brief — [Title]

## Context
[Summary of the need in 2-3 sentences]

## Detected Stack
[Stack identified by @Explore: framework, language, versions]

## Acceptance Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)
- [ ] Criterion 3 (measurable)

## Constraints
- [Identified technical constraint]
- [Time/budget constraint if applicable]

## Out of Scope
- [Explicit exclusion 1]
- [Explicit exclusion 2]

## Evaluation
- **Category**: [TINY|SMALL|STANDARD|LARGE|SPIKE]
- **Estimated files**: X
- **Estimated LOC**: ~Y
- **Risk**: [None|Low|Medium|High|Unknown]
- **Justification**: [Reason for categorization]

## Recommendation
→ Use `/epci-quick` | `/epci` | `/epci --large` | `/epci-spike`
```

## Skills Loaded

- `epci-core` (EPCI concepts)
- `architecture-patterns` (complexity evaluation)
- `[stack-skill]` (auto-detected based on project)

## Transition

After brief generation:
1. Present structured brief to user
2. Wait for confirmation before routing
3. Propose launching the recommended command

```
---
📋 **BRIEF COMPLETE**

Functional brief generated and validated.
Category: [CATEGORY]
Recommended workflow: [COMMAND]

**Next step:** Launch `[COMMAND]`?
---
```
