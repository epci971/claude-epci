---
name: step-04-workflow
description: Design workflow, define steps, create decision trees, determine steps generation
prev_step: steps/step-03-description.md
next_step: steps/step-05-validation.md
---

# Step 04: Workflow Design

> Design workflow, define steps, create decision trees, determine steps generation.

## Trigger

- Completion of step-03-description.md

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From step-03 | Yes |
| Mode | From step-00 | Yes |
| Structure | From step-02 | Yes |
| Purpose | From step-01 | Yes |

## Protocol

### 1. Check Steps Generation Flag

```
IF mode == "core":
  → skip_steps_design = true
  → Proceed with simple workflow section

ELSE IF mode == "simple" (--simple flag):
  → skip_steps_design = true
  → Proceed with simple workflow section

ELSE (default standard mode):
  → skip_steps_design = false
  → Full steps design required
```

### 2. Design Workflow Phases

Ask user to describe workflow phases:

```
What are the main phases of this skill's workflow?
(List 2-6 phases in order, e.g., "1. Analyze input, 2. Process data, 3. Generate output")

Examples:
- Simple (2-3 phases): Analyze → Execute → Report
- Standard (4-5 phases): Init → Analyze → Plan → Execute → Verify
- Complex (5-6 phases): Init → Clarify → Design → Execute → Review → Report
```

### 3. Generate Workflow Diagram

Based on phases:

```
┌─────────────────────────────────────────────────────────────────┐
│                    {SKILL NAME} WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 00: INIT                                                   │
│  └─ Parse input, initialize context                             │
│                                                                  │
│  Step 01: {PHASE 1 NAME}                                        │
│  └─ {phase 1 description}                                       │
│                                                                  │
│  Step 02: {PHASE 2 NAME}                                        │
│  └─ {phase 2 description}                                       │
│     └─ Conditional: {if condition} → step-02b                   │
│                                                                  │
│  ...                                                            │
│                                                                  │
│  Step 99: FINISH                                                │
│  └─ Generate outputs, summary                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Define Decision Trees (if multi-path)

For conditional flows:

```
IF {condition 1}:
  → {action / next step}
ELSE IF {condition 2}:
  → {action / next step}
ELSE:
  → {default action}
```

### 5. Define Input/Output Examples

```markdown
## Examples

### Input
```
/{skill-name} {example-arg}
```

### Output
{expected output format}
```

### 6. Generate Step Content (DECLARATIVE)

**Rule**: If content exceeds 50 words or contains structured data (schemas, templates, tables > 10 rows), move to reference file and link.

❌ **BAD** - Inline schema in step:
```markdown
### Generate Output
Use this schema:
```json
{ "id": "H1", "hypothesis": "...", "confidence": 0.8, ... }
```
```

✅ **GOOD** - Reference to schema:
```markdown
### Generate Output
Apply schema from [references/hypothesis-schema.md](../references/hypothesis-schema.md).
Populate fields with current analysis data.
```

### 7. Determine Steps to Generate

**For standard mode (default):**

```python
steps_to_generate = [
    "step-00-init.md",      # Always: Parse args, context
]

for i, phase in enumerate(phases, 1):
    steps_to_generate.append(f"step-{i:02d}-{phase.slug}.md")

steps_to_generate.append("step-99-finish.md")  # Always: Finalization

# Add conditional steps if multi-path
for condition in conditional_flows:
    step_num = condition.branch_from
    steps_to_generate.append(f"step-{step_num:02d}b-{condition.slug}.md")
```

**Steps generation summary:**

| Step | Template | Content |
|------|----------|---------|
| step-00-init.md | step-init-template.md | Parse, context, routing |
| step-01-{phase1}.md | step-generic-template.md | Phase 1 logic |
| step-02-{phase2}.md | step-generic-template.md | Phase 2 logic |
| step-0Xb-{variant}.md | step-generic-template.md | Conditional branch |
| step-99-finish.md | step-finish-template.md | Finalize, outputs |

### 8. Store Workflow Design

```json
{
  "collected": {
    "workflow": {
      "phases": [
        {"name": "<phase1>", "description": "<desc>"},
        {"name": "<phase2>", "description": "<desc>"}
      ],
      "decision_trees": [...],
      "examples": {
        "input": "<example input>",
        "output": "<example output>"
      }
    },
    "steps_to_generate": [
      "step-00-init.md",
      "step-01-{phase1}.md",
      ...
    ]
  }
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| Workflow design | Session state |
| Steps list | For generation |
| Decision trees | For step conditionals |

## Next Step

→ `step-05-validation.md`

## Reference Files

- [templates/step-init-template.md](../templates/step-init-template.md) — Init step template
- [templates/step-generic-template.md](../templates/step-generic-template.md) — Generic step template
- [templates/step-finish-template.md](../templates/step-finish-template.md) — Finish step template

## Error Handling

| Error | Resolution |
|-------|------------|
| Too few phases (< 2) | Suggest simple mode or add phases |
| Too many phases (> 6) | Suggest splitting into multiple skills |
| Circular dependencies | Highlight and ask to resolve |
