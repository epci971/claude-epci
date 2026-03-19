---
name: step-02-plan-auto
description: Create implementation plan via @planner + @plan-validator [P]
prev_step: steps/step-01-explore-auto.md
next_step: steps/step-03-code-auto.md
---

# Step 02: Plan (Auto) [P]

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER skip test strategy definition
- ALWAYS invoke @planner (Sonnet) for plan generation
- ALWAYS invoke @plan-validator (Opus) unless --skip-plan-validation
- ALWAYS define implementation order with dependencies
- ALWAYS specify TDD approach per component
- ALWAYS update Feature Document §2

## EXECUTION PROTOCOLS:

### 1. Synthesize Exploration Findings

Review from step-01:
- Verified relevant files and their purposes
- Identified architecture patterns
- Test framework and conventions
- Files to modify and create

### 2. Invoke @planner Agent

Invoke @planner (Sonnet) via Task tool to create the implementation plan:

```
LANCE Task({
  subagent_type: "planner",
  model: "sonnet",
  prompt: "
    ## Feature
    {feature_slug}: {spec_objective}

    ## Requirements
    {spec_requirements_and_acceptance_criteria}

    ## Exploration Findings
    - Relevant files: {verified_files_with_purposes}
    - Patterns: {identified_patterns}
    - Test framework: {test_framework_name}, command: {test_run_command}
    - Files to modify: {files_to_modify}
    - Files to create: {files_to_create}

    ## Constraints
    - Follow existing architecture patterns
    - TDD required: each component needs test_file and test_approach
    - Dependencies must be acyclic

    ## Expected Output
    Ordered list of atomic components with:
    - name (kebab-case)
    - file (primary file path)
    - type (create or modify)
    - depends_on (list of component names)
    - test_file (path to test file)
    - test_approach (unit or integration)
    - description (what this component does)

    Order: foundation first, core logic second, integration third, config last.
  "
})
```

Parse the planner output into the component structure.

### 3. Invoke @plan-validator Agent

IF `flag_skip_plan_validation` is false (default):

```
LANCE Task({
  subagent_type: "plan-validator",
  model: "opus",
  prompt: "
    ## Plan to Validate
    {plan_components_from_planner}

    ## Feature Requirements
    {spec_requirements}

    ## Exploration Context
    - Existing files: {verified_files}
    - Patterns: {identified_patterns}

    ## Validation Checklist
    - Completeness: All requirements and acceptance criteria covered
    - Consistency: No circular dependencies in depends_on
    - Feasibility: Referenced files and patterns exist in codebase
    - Quality: TDD strategy defined per component, tests are meaningful

    ## Expected Output
    APPROVED or NEEDS_REVISION with specific feedback per component
  "
})
```

**Process validation result:**
- If APPROVED: continue to step 4
- If NEEDS_REVISION: apply feedback, re-invoke @planner (max 1 retry)
  - Pass validator feedback as additional constraints to @planner
  - Re-validate with @plan-validator
  - If still NEEDS_REVISION: add warning to JSON, continue anyway
- Record verdict in JSON: `plan.validator_verdict`

IF `flag_skip_plan_validation` is true:
- Set `plan.validator_verdict = null`
- Add warning: "Plan validation skipped (--skip-plan-validation flag)"

### 4. Record Plan Metadata

```
plan.planner_used = true
plan.validator_verdict = "{APPROVED or NEEDS_REVISION or null}"
```

### 5. Update Feature Document §2

Use Edit tool to replace the plan section placeholder in the Feature Document:

```markdown
## §2 — Plan d'implementation

### Composants

| # | Composant | Fichier | Dependencies | Status |
|---|-----------|---------|--------------|--------|
| 1 | {name} | {file} | {depends_on} | PENDING |
{... all components}

### Strategie de tests
- Framework: {detected_framework}
- Commande: {test_command}
- Approche: TDD RED-GREEN-REFACTOR par composant
- Coverage cible: {70% or 80%} line / {60% or 70%} branch

### Validation du plan
| Champ | Valeur |
|-------|--------|
| @planner | Sonnet |
| @plan-validator | {APPROVED / NEEDS_REVISION / skipped} |
```

### 6. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "plan"
- `phases.current` = "code"
- `plan.total_components` = count
- `plan.planner_used` = true
- `plan.validator_verdict` = "{verdict or null}"
- `plan.components` = [{name, file, status: "pending", tests_added: 0, retries: 0, error: null}]

## CONTEXT BOUNDARIES:

- This step expects: Verified exploration data from step-01
- This step produces: Ordered component plan (from @planner), validation verdict (from @plan-validator), updated Feature Doc §2, updated JSON

## NEXT STEP TRIGGER:

On success, proceed to step-03-code-auto.md.
