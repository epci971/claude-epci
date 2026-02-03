---
name: step-03-generate-ralph
description: Generate Ralph execution artifacts using templates
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

## Templates (from task-005)

| Template | Output | Location |
|----------|--------|----------|
| `templates/prd.json.template` | PRD v2 with userStories | `docs/specs/{slug}/{slug}.prd.json` |
| `templates/prompt.md.template` | Execution context | `.ralph/{slug}/PROMPT.md` |
| `templates/memory.md.template` | Progress tracking | `.ralph/{slug}/MEMORY.md` |
| `templates/ralph.sh.template` | Autonomous executor | `.ralph/{slug}/ralph.sh` |

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate Ralph without valid specs
- 🔴 NEVER skip stack detection for PROMPT.md
- 🔴 NEVER overwrite existing MEMORY.md with active context
- ✅ ALWAYS use templates from templates/
- ✅ ALWAYS update .ralph/index.json
- ✅ ALWAYS make ralph.sh executable
- ✅ ALWAYS include circuit breaker in ralph.sh (from template)
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
mkdir -p docs/specs/{feature-slug}/
```

### 3. Generate PRD.json (PRD v2 with userStories)

Use template from `templates/prd.json.template`.

**Output location:** `docs/specs/{slug}/{slug}.prd.json`

**Template variables to fill:**
- `{{TITLE}}`: Feature title
- `{{SLUG}}`: Feature slug (kebab-case)
- `{{DESCRIPTION}}`: Feature description
- `{{COMPLEXITY}}`: TINY | SMALL | STANDARD | LARGE
- `{{GENERATED_AT}}`: ISO-8601 timestamp
- `{{SOURCE}}`: Source document (brief, PRD, etc.)
- `{{BRANCH_NAME}}`: Git branch name
- `{{PROJECT_NAME}}`: Project name
- `{{GENERATED_BY}}`: Generator (/spec v1.0)
- `{{MAX_ITERATIONS}}`: Max Ralph iterations (default: 50)
- `{{TEST_COMMAND}}`: Test command from stack detection
- `{{LINT_COMMAND}}`: Lint command (optional)
- `{{GRANULARITY}}`: Task granularity (hour)
- `{{TOTAL_STORIES}}`: Number of userStories

**userStories array structure:**
Each task from step-02 becomes a userStory with:
- `id`: Story ID (US1, US2, etc.)
- `title`: Task title
- `description`: Task description
- `acceptanceCriteria`: Array of ACs from task spec
- `tasks`: Sub-tasks from task spec steps
- `dependencies`: { depends_on: [], blocks: [] }
- `execution`: { attempts: 0, last_error: null, files_modified: [], completed_at: null, iteration: 0 }

**Schema validation:**
PRD must validate against `src/schemas/prd-v2.json`.

### 4. Generate PROMPT.md

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

### 5. Generate MEMORY.md

Use template from `templates/memory.md.template`.

**Template variables to fill:**
- `{{FEATURE_TITLE}}`: Human-readable feature name
- `{{FEATURE_SLUG}}`: URL-friendly identifier
- `{{TASK_COUNT}}`: Number of tasks
- `{{GENERATED_AT}}`: ISO-8601 timestamp
- `{{FIRST_TASK_ID}}`: First task ID (e.g., task-001)
- `{{TASKS}}`: Array for Handlebars loop `{{#each TASKS}}`
- `{{STACK_FRAMEWORK}}`, `{{STACK_LANGUAGE}}`, `{{TEST_COMMAND}}`: From stack detection

**Initialize:**
- All tasks as `pending` in Progress table
- Current Task to first task ID
- Status to `PENDING`
- Started to current ISO-8601 timestamp
- Empty tables for Files/Tests/Issues/Decisions
- Context Notes placeholder

### 6. Generate ralph.sh

Use template from `templates/ralph.sh.template`.

**Template variables to fill:**
- `{{FEATURE_SLUG}}`: Feature identifier (kebab-case)
- `{{PRD_FILE}}`: Path to PRD JSON file (`docs/specs/{slug}/{slug}.prd.json`)
- `{{SPEC_DIR}}`: Spec directory path (`docs/specs/{slug}`)
- `{{RALPH_DIR}}`: Ralph execution directory (`.ralph/{slug}`)

**Features included from template:**
- Inline circuit breaker (detects stuck loops via file/error hash)
- RALPH_STATUS parser (<<<>>> delimiters)
- CLI flags (--quiet, --dry-run, --help)
- Progress display with elapsed time
- Timestamped logging
- MAX_ITERATIONS config (default: 50)
- CB_THRESHOLD config (default: 3)

**Generation:**

```bash
# Read template
TEMPLATE=$(cat templates/ralph.sh.template)

# Replace placeholders
OUTPUT="${TEMPLATE//\{\{FEATURE_SLUG\}\}/$FEATURE_SLUG}"
OUTPUT="${OUTPUT//\{\{PRD_FILE\}\}/$PRD_FILE}"
OUTPUT="${OUTPUT//\{\{SPEC_DIR\}\}/$SPEC_DIR}"
OUTPUT="${OUTPUT//\{\{RALPH_DIR\}\}/$RALPH_DIR}"

# Write output
echo "$OUTPUT" > .ralph/{feature-slug}/ralph.sh
```

Make executable:
```bash
chmod +x .ralph/{feature-slug}/ralph.sh
```

### 7. Update .ralph/index.json

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

### 8. Calculate Routing Recommendation

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

Remplis les variables:
- `{feature-slug}`: Feature slug from state
- `{complexity}`: `TINY`/`SMALL`/`STANDARD`/`LARGE`
- `{slug}`: Same as feature-slug
- `{skill}`: `/quick` or `/implement` based on complexity routing

APPELLE AskUserQuestion({
  questions: [{
    question: "Comment voulez-vous proceder?",
    header: "Next Step",
    multiSelect: false,
    options: [
      { label: "Lancer {skill} (Recommended)", description: "Demarrer workflow implementation" },
      { label: "Run Ralph Batch", description: "Executer ./.ralph/{slug}/ralph.sh" },
      { label: "Review fichiers", description: "Inspecter artifacts generes" },
      { label: "Termine", description: "Fin workflow, implementer plus tard" }
    ]
  }]
})

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
