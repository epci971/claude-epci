---
name: step-03-generate-ralph
description: Generate Ralph execution artifacts
prev_step: steps/step-02-generate-specs.md
next_step: null
---

# Step 03: Generate Ralph Artifacts

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [stack-guidelines.md](../references/stack-guidelines.md) | Stack detection and conventions |
| [memory-template.md](../references/memory-template.md) | MEMORY.md structure |
| [execution-workflow.md](../references/execution-workflow.md) | TDD and completion rules |
| [breakpoint-formats.md#completion-summary-box](../references/breakpoint-formats.md#completion-summary-box) | Final breakpoint |

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate Ralph without valid specs
- 🔴 NEVER skip stack detection for PROMPT.md
- 🔴 NEVER overwrite existing MEMORY.md with active context
- ✅ ALWAYS use templates from templates/
- ✅ ALWAYS update .ralph/index.json
- ✅ ALWAYS make ralph.sh executable
- 🔵 YOU ARE A DEVOPS ENGINEER preparing execution
- 💭 FOCUS on stack-awareness and automation

## EXECUTION PROTOCOLS:

### 1. Detect Project Stack

Use detection matrix from [stack-guidelines.md](../references/stack-guidelines.md#stack-detection-matrix).

Store detected stack for PROMPT.md generation:
- `STACK_FRAMEWORK`: Django | React | Spring | Symfony | Generic
- `STACK_LANGUAGE`: Python | TypeScript | Java | PHP | -
- `TEST_FRAMEWORK`: pytest | vitest | junit | phpunit | project-specific

### 2. Create Directory Structure

```bash
mkdir -p .ralph/{feature-slug}/
```

### 3. Generate PROMPT.md

Use template from `templates/prompt.md.template`.

**Template variables to fill:**
- Feature metadata: slug, complexity, task count, hours
- Stack info: framework, language, test framework
- Execution order: from DAG topological sort
- Stack guidelines: inject content from [stack-guidelines.md](../references/stack-guidelines.md)

Load appropriate stack section based on detection:
- Django → [stack-guidelines.md#django-guidelines](../references/stack-guidelines.md#django-guidelines)
- React → [stack-guidelines.md#react-guidelines](../references/stack-guidelines.md#react-guidelines)
- Spring → [stack-guidelines.md#spring-boot-guidelines](../references/stack-guidelines.md#spring-boot-guidelines)
- Symfony → [stack-guidelines.md#symfony-guidelines](../references/stack-guidelines.md#symfony-guidelines)
- Generic → [stack-guidelines.md#generic-guidelines](../references/stack-guidelines.md#generic-guidelines)

### 4. Generate MEMORY.md

Use template structure from [memory-template.md](../references/memory-template.md#complete-template).

**Initialize:**
- All tasks as `pending` in Progress table
- Current Task to first task ID
- Status to `PENDING`
- Started to current ISO-8601 timestamp
- Empty tables for Files/Tests/Issues/Decisions
- Context Notes placeholder

### 5. Generate ralph.sh

**Runner Script Structure:**

```bash
#!/bin/bash
# Ralph Runner — {Feature Title}
# Generated: {timestamp}

set -e

FEATURE_SLUG="{feature-slug}"
SPEC_DIR="docs/specs/${FEATURE_SLUG}"
RALPH_DIR=".ralph/${FEATURE_SLUG}"

echo "=== Ralph Execution: ${FEATURE_SLUG} ==="
echo "Specs: ${SPEC_DIR}/"
echo "Memory: ${RALPH_DIR}/MEMORY.md"
echo ""

# Check prerequisites
if [[ ! -d "${SPEC_DIR}" ]]; then
    echo "Error: Spec directory not found: ${SPEC_DIR}"
    exit 1
fi

if [[ ! -f "${RALPH_DIR}/PROMPT.md" ]]; then
    echo "Error: PROMPT.md not found"
    exit 1
fi

# Display context
echo "Starting Claude Code with Ralph context..."
echo ""
echo "Context loaded:"
echo "- PROMPT.md: ${RALPH_DIR}/PROMPT.md"
echo "- MEMORY.md: ${RALPH_DIR}/MEMORY.md"
echo "- Specs: ${SPEC_DIR}/"
echo ""

# Launch Claude Code
claude --resume-with-context "${RALPH_DIR}/PROMPT.md" \
       --memory "${RALPH_DIR}/MEMORY.md"

echo ""
echo "=== Ralph Execution Complete ==="
```

Make executable:
```bash
chmod +x .ralph/{feature-slug}/ralph.sh
```

### 6. Update .ralph/index.json

**Registry entry:**

```json
{
  "slug": "{feature-slug}",
  "title": "{Feature Title}",
  "created_at": "{ISO-8601}",
  "status": "ready",
  "complexity": "{level}",
  "tasks": {count},
  "spec_path": "docs/specs/{feature-slug}/",
  "ralph_path": ".ralph/{feature-slug}/",
  "prd_path": "docs/specs/{feature-slug}/{feature}.prd.json"
}
```

**Update logic:**
- If index.json exists: append to features array
- If not: create new with this feature
- Check for duplicates by slug

### 7. Calculate Routing Recommendation

Based on complexity from Step 01:

| Complexity | Recommended | Rationale |
|------------|-------------|-----------|
| TINY | `/quick` | Single task, < 1h |
| SMALL | `/quick` | Few tasks, < 3h |
| STANDARD | `/implement` | Multiple tasks, 3-10h |
| LARGE | `/implement` | Many tasks, > 10h |

## CONTEXT BOUNDARIES:

- This step expects: Generated specs, stack info
- This step produces: PROMPT.md, MEMORY.md, ralph.sh, updated index.json

## OUTPUT FORMAT:

```
## Ralph Artifacts Generated

Location: .ralph/{feature-slug}/

### Files Created
- [x] PROMPT.md (stack-aware instructions)
- [x] MEMORY.md (execution memory template)
- [x] ralph.sh (runner script, executable)

### Registry Updated
- .ralph/index.json → {feature-slug} added

### Execution Command
```bash
./.ralph/{feature-slug}/ralph.sh
```
```

## BREAKPOINT: Specification Complete (OBLIGATOIRE)

AFFICHE le format depuis [references/breakpoint-formats.md#completion-summary-box](../references/breakpoint-formats.md#completion-summary-box).

Remplis les variables:
- `{feature-slug}`: Feature slug from state
- `{complexity}`: TINY/SMALL/STANDARD/LARGE
- `{slug}`: Same as feature-slug
- `{/quick ou /implement}`: Based on routing recommendation

APPELLE AskUserQuestion avec les options depuis la reference.

⏸️ ATTENDS la reponse utilisateur avant de continuer.

## COMPLETION:

When user selects an option:

- **[A] Launch skill**: Execute `/quick` or `/implement` with spec path
- **[B] Run Ralph**: Display command to run ralph.sh
- **[C] Review**: Display file paths for manual review
- **[D] Done**: End workflow with summary

### Final Summary

```
## /spec Complete

Feature: {feature-slug}
Duration: {elapsed}

### Generated
- {task_count} task specifications
- {step_count} execution steps
- 1 PRD.json (machine-readable)
- 3 Ralph artifacts (PROMPT, MEMORY, runner)

### Metrics
- Estimated effort: {hours}h
- Critical path: {tasks on path}
- Optimized duration: {hours}h

### Next Step
{recommended command or action}

---
*Specification generated by /spec v1.0 — EPCI v6.0*
```

## NEXT STEP TRIGGER:

This is the final step. Workflow ends after user action.
