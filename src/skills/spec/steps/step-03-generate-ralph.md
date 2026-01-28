---
name: step-03-generate-ralph
description: Generate Ralph execution artifacts
prev_step: steps/step-02-generate-specs.md
next_step: null
---

# Step 03: Generate Ralph Artifacts

## Reference Files

@../references/stack-guidelines.md
@../references/memory-template.md
@../references/execution-workflow.md

| Reference | Purpose |
|-----------|---------|
| stack-guidelines.md | Stack detection and conventions |
| memory-template.md | MEMORY.md structure |
| execution-workflow.md | TDD and completion rules |

*(Breakpoint templates are inline in this file)*

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

Use detection matrix from stack-guidelines.md (section #stack-detection-matrix importé ci-dessus).

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
- Stack guidelines: inject content from stack-guidelines.md (importé ci-dessus)

Load appropriate stack section based on detection:
- Django → stack-guidelines.md section #django-guidelines
- React → stack-guidelines.md section #react-guidelines
- Spring → stack-guidelines.md section #spring-boot-guidelines
- Symfony → stack-guidelines.md section #symfony-guidelines
- Generic → stack-guidelines.md section #generic-guidelines

### 4. Generate MEMORY.md

Use template structure from memory-template.md (section #complete-template importé ci-dessus).

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

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ SPECIFICATION COMPLETE                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Tous les artifacts de spec et Ralph generes                         │
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexite: {complexity}                                            │
│ Specs: docs/specs/{slug}/                                           │
│ Ralph: .ralph/{slug}/                                               │
│                                                                     │
│ Critere de succes: Utilisateur selectionne chemin implementation    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Reviser PROMPT.md pour ajustements stack-specific              │
│ [P2] Considerer execution parallele des taches pour optimisation    │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Lancer {skill} (Recommended)                              │ │
│ │  [B] Run Ralph Batch — Executer ralph.sh                       │ │
│ │  [C] Review fichiers — Inspecter artifacts generes             │ │
│ │  [D] Termine — Fin workflow, implementer plus tard             │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

Remplis les variables:
- `{feature-slug}`: Feature slug from state
- `{complexity}`: `TINY`/`SMALL`/`STANDARD`/`LARGE`
- `{slug}`: Same as feature-slug
- `{skill}`: `/quick` or `/implement` based on complexity routing

APPELLE AskUserQuestion:
```json
{
  "question": "Comment voulez-vous proceder?",
  "header": "Next Step",
  "multiSelect": false,
  "options": [
    { "label": "Lancer {skill} (Recommended)", "description": "Demarrer workflow implementation" },
    { "label": "Run Ralph Batch", "description": "Executer ./.ralph/{slug}/ralph.sh" },
    { "label": "Review fichiers", "description": "Inspecter artifacts generes" },
    { "label": "Termine", "description": "Fin workflow, implementer plus tard" }
  ]
}
```

**Note**: Replace `{skill}` with `/quick` or `/implement` based on complexity routing.

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
