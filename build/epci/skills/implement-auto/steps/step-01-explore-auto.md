---
name: step-01-explore-auto
description: Explore codebase with sanity check [E]
prev_step: steps/step-00-init-auto.md
next_step: steps/step-02-plan-auto.md
conditional_next:
  - condition: "explore_empty or sanity_check_failed"
    step: steps/step-07-output-auto.md
---

# Step 01: Explore (Auto) [E]

## MANDATORY EXECUTION RULES:

- NEVER modify any files during exploration
- NEVER call AskUserQuestion
- ALWAYS use read-only tools (Read, Glob, Grep)
- ALWAYS run sanity check on explore results
- ALWAYS abort if hallucination rate > 30%

## EXECUTION PROTOCOLS:

### 1. Analyze Requirements

Parse the spec content (loaded in step-00) into:
- Functional requirements (features to build)
- Files likely to be created or modified
- Keywords and patterns to search for
- Target modules and directories

### 2. Invoke Explore Agent

Delegate codebase exploration to the native Explore agent:

```
LANCE Task({
  subagent_type: "Explore",
  model: "haiku",
  prompt: "
    ## Exploration Objective
    Analyze codebase for feature: {feature_slug}

    ## Requirements Summary
    {requirements_from_spec}

    ## Search Focus
    1. Files matching patterns: {patterns_from_spec}
    2. Existing patterns for: {functionality_type}
    3. Test framework and conventions
    4. Architecture patterns (imports, structure)

    ## Thoroughness Level
    very thorough

    ## Required Output (structured)
    - relevant_files: [{path, purpose}]
    - patterns: [{name, description}]
    - dependencies: {internal: [], external: []}
    - test_framework: {name, config_file, run_command}
    - files_to_modify: [{path, change_type}]
    - files_to_create: [{path, purpose}]
  "
})
```

### 3. Sanity Check

Verify that files reported by the Explore agent actually exist.

```
hallucinated = 0
verified = 0
total = len(relevant_files + files_to_modify)

FOR each file in explore_results:
  exists = Glob(pattern: file.path)
  IF exists:
    verified += 1
  ELSE:
    hallucinated += 1
    Remove from results
    Add warning: "File not found: {file.path}"

hallucination_rate = hallucinated / total
```

**Decision table:**

| Condition | Action |
|-----------|--------|
| total == 0 | ABORT: exit_reason = "explore_empty_results" |
| hallucination_rate > 0.30 | ABORT: exit_reason = "explore_sanity_check_failed" |
| hallucination_rate > 0 and <= 0.30 | WARN: clean results, continue |
| hallucination_rate == 0 | OK: proceed normally |

### 4. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "explore"
- `phases.current` = "plan"
- Add any warnings from sanity check

### 5. Store Exploration Context

Preserve for step-02-plan-auto:
- Verified relevant files with purposes
- Identified patterns
- Test framework details
- Files to modify and create

## CONTEXT BOUNDARIES:

- This step expects: Execution context from step-00, spec content
- This step produces: Verified exploration data, updated JSON

## NEXT STEP TRIGGER:

On success (sanity check passed), proceed to step-02-plan-auto.md.
On failure (empty or >30% hallucinated), jump to step-07-output-auto.md.
