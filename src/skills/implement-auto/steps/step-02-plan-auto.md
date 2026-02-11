---
name: step-02-plan-auto
description: Create implementation plan without breakpoint [P]
prev_step: steps/step-01-explore-auto.md
next_step: steps/step-03-code-auto.md
conditional_next:
  - condition: "plan_validation_failed and flag_validate_plan"
    step: steps/step-07-output-auto.md
---

# Step 02: Plan (Auto) [P]

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER skip test strategy definition
- ALWAYS define implementation order with dependencies
- ALWAYS specify TDD approach per component
- ALWAYS update Feature Document section 2

## EXECUTION PROTOCOLS:

### 1. Synthesize Exploration Findings

Review from step-01:
- Verified relevant files and their purposes
- Identified architecture patterns
- Test framework and conventions
- Files to modify and create

### 2. Create Implementation Plan

Decompose the feature into atomic components ordered by dependency:

For each component, define:

| Field | Description |
|-------|-------------|
| `name` | Component name (kebab-case) |
| `file` | Primary file path to create/modify |
| `type` | `create` or `modify` |
| `depends_on` | List of component names this depends on |
| `test_file` | Path to test file |
| `test_approach` | TDD strategy (unit, integration) |
| `description` | What this component does |

### Ordering Rules

1. Foundation components first (models, types, interfaces)
2. Core logic second (services, business rules)
3. Integration third (controllers, API, views)
4. Configuration last (settings, env)

### 3. Invoke Plan-Validator Agent (--validate-plan)

IF `flag_validate_plan` is true:

```
LANCE Task({
  subagent_type: "plan-validator",
  model: "opus",
  prompt: "
    ## Plan to Validate
    {plan_components}

    ## Feature Requirements
    {spec_requirements}

    ## Validation Checklist
    - Completeness: All requirements covered
    - Consistency: No circular dependencies
    - Feasibility: Files and patterns exist
    - Quality: TDD strategy per component

    ## Expected Output
    APPROVED or NEEDS_REVISION with feedback
  "
})
```

If NEEDS_REVISION: apply feedback, regenerate plan (max 1 retry).
If still NEEDS_REVISION after retry: add warning, continue anyway.

### 4. Update Feature Document §2

Use Edit tool to replace the plan section placeholder in the Feature Document:

```
## Plan d'implementation

| # | Composant | Fichier | Dependances | Status |
|---|-----------|---------|-------------|--------|
{generated plan table}

### Strategie de test
- Framework: {detected_framework}
- Commande: {test_command}
- Approche: TDD RED-GREEN-REFACTOR par composant
```

### 5. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "plan"
- `phases.current` = "code"
- `plan.total_components` = count
- `plan.components` = [{name, file, status: "pending", ...}]

## CONTEXT BOUNDARIES:

- This step expects: Verified exploration data from step-01
- This step produces: Ordered component plan, updated Feature Doc §2, updated JSON

## NEXT STEP TRIGGER:

On success, proceed to step-03-code-auto.md.
If plan validation fails with --validate-plan and no recovery: jump to step-07-output-auto.md.
