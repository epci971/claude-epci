---
name: step-01-preanalysis
description: Ask discovery questions to understand skill need, then apply decision gate
prev_step: steps/step-00-init.md
next_step: steps/step-02-architecture.md
conditional_next:
  - condition: "STOP (no override)"
    step: null
---

# Step 01: Pre-Analysis

> Ask discovery questions to understand skill need, then apply decision gate.

## Trigger

- Completion of step-00-init.md

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From step-00 | Yes |
| Mode | From step-00 | Yes |

## Protocol

### 1. Ask Discovery Questions

Present questions via AskUserQuestion (one at a time or batched):

**Question 1: Purpose**
```
What problem does this skill solve?
(Describe the main functionality in 1-2 sentences)
```

**Question 2: Frequency**
```
How often will this skill be used?
Options:
  - Daily (high frequency, core workflow)
  - Weekly (regular but not constant)
  - Occasional (specific situations)
  - Rare (edge cases, special scenarios)
```

**Question 3: Triggers**
```
What phrases would naturally invoke this skill?
(List 3-5 natural language triggers, e.g., "create API docs", "document endpoints")
```

**Question 4: Scope**
```
What's in scope and out of scope?
  - IN: {what this skill handles}
  - OUT: {what this skill does NOT handle}
```

**Question 5: Persona**
```
Who uses this skill?
Options:
  - All users (general purpose)
  - Developers only
  - Specific role (specify)
```

### 2. Store Responses

```json
{
  "collected": {
    "purpose": "<user response>",
    "frequency": "<daily|weekly|occasional|rare>",
    "triggers": ["<trigger1>", "<trigger2>", ...],
    "scope": {
      "in": ["<included1>", ...],
      "out": ["<excluded1>", ...]
    },
    "persona": "<all|developers|specific>"
  }
}
```

### 3. Apply Decision Gate

**PROCEED if:**
- Purpose is clear and specific
- Frequency >= occasional
- Has 3+ distinct triggers
- Solves a repeatable problem

**STOP if:**
- One-time task → Suggest using conversation directly
- Volatile procedure → Suggest documenting elsewhere
- Runtime config → Suggest using settings/env
- Vague purpose → Ask for clarification

### 4. Decision Gate Output

```
IF PROCEED:
  Display:
  ┌─────────────────────────────────────────────────────────────────┐
  │ [DECISION GATE] Skill Creation Approved                         │
  ├─────────────────────────────────────────────────────────────────┤
  │ Purpose: {purpose summary}                                      │
  │ Frequency: {frequency}                                          │
  │ Triggers: {trigger count} identified                            │
  │                                                                  │
  │ Proceeding to architecture design...                            │
  └─────────────────────────────────────────────────────────────────┘

IF STOP:
  Display:
  ┌─────────────────────────────────────────────────────────────────┐
  │ [DECISION GATE] Skill Creation Not Recommended                  │
  ├─────────────────────────────────────────────────────────────────┤
  │ Reason: {specific reason}                                       │
  │                                                                  │
  │ Alternatives:                                                   │
  │ • {alternative 1}                                               │
  │ • {alternative 2}                                               │
  │                                                                  │
  │ Override? [Yes, proceed anyway] [No, cancel]                    │
  └─────────────────────────────────────────────────────────────────┘
```

## Outputs

| Output | Destination |
|--------|-------------|
| Discovery responses | Session state |
| Decision gate result | For routing |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| PROCEED or Override | → `step-02-architecture.md` |
| STOP (no override) | → End workflow |

## Error Handling

| Error | Resolution |
|-------|------------|
| Incomplete responses | Re-ask specific question |
| Conflicting scope | Ask for clarification |
| Too many triggers | Suggest grouping or splitting skill |
