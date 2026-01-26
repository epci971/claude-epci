---
name: step-03-generate-ralph
description: Generate Ralph execution artifacts
prev_step: steps/step-02-generate-specs.md
next_step: null
---

# Step 03: Generate Ralph Artifacts

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER generate Ralph without valid specs
- :red_circle: NEVER skip stack detection for PROMPT.md
- :red_circle: NEVER overwrite existing MEMORY.md with active context
- :white_check_mark: ALWAYS use templates from templates/
- :white_check_mark: ALWAYS update .ralph/index.json
- :white_check_mark: ALWAYS make ralph.sh executable
- :large_blue_circle: YOU ARE A DEVOPS ENGINEER preparing execution
- :thought_balloon: FOCUS on stack-awareness and automation

## EXECUTION PROTOCOLS:

### 1. Detect Project Stack

Use @Explore or existing project context:

```
Stack Detection:
├── Python/Django → manage.py, requirements.txt with django
├── JavaScript/React → package.json with react
├── Java/Spring → pom.xml or build.gradle with spring-boot
├── PHP/Symfony → composer.json with symfony
└── Generic → No specific markers
```

Store stack info for PROMPT.md generation.

### 2. Create Directory Structure

```bash
mkdir -p .ralph/{feature-slug}/
```

### 3. Generate PROMPT.md

Use template from `templates/prompt.md.template`.

**Stack-Aware Content:**

```markdown
# Ralph Execution Context — {Feature Title}

## Feature

- **Slug**: {feature-slug}
- **Complexity**: {level}
- **Tasks**: {count}
- **Estimated**: {hours}h

## Stack

- **Framework**: {Django|React|Spring|Symfony|Generic}
- **Language**: {Python|TypeScript|Java|PHP}
- **Test Framework**: {pytest|vitest|junit|phpunit}

## Execution Rules

### MANDATORY:
- :red_circle: Follow TDD cycle: RED → GREEN → REFACTOR
- :red_circle: Complete each task before moving to next
- :red_circle: Run tests after each step
- :red_circle: Update MEMORY.md after each task completion

### WORKFLOW:
1. Read current task from specs/task-XXX.md
2. Execute steps sequentially
3. Write tests before implementation (TDD)
4. Validate acceptance criteria
5. Mark task complete in MEMORY.md
6. Proceed to next task by dependency order

## Specifications

Location: `docs/specs/{feature-slug}/`

Files:
- `index.md` — Overview and DAG
- `task-001-{slug}.md` — First task
- `task-002-{slug}.md` — Second task
- ...
- `{feature}.prd.json` — Machine-readable

## Execution Order

{Topological order from DAG}

1. task-001: {title}
2. task-002: {title}
3. ...

## Stack-Specific Guidelines

{Content varies by stack}

### For Django:
- Use service layer pattern
- pytest for testing
- Factory Boy for fixtures
- Type hints required

### For React:
- Functional components with hooks
- Vitest + React Testing Library
- Zustand for state if needed
- TypeScript strict mode

### For Spring:
- Service layer pattern
- JUnit 5 + Mockito
- Lombok for boilerplate
- Constructor injection

### For Symfony:
- Service layer pattern
- PHPUnit + Prophecy
- Doctrine for persistence
- Voters for authorization

### For Generic:
- Follow existing project conventions
- Write tests for all code
- Document decisions

## Context Persistence

After each task completion:
1. Update MEMORY.md with:
   - Task ID completed
   - Files modified
   - Tests added
   - Issues encountered

2. Commit changes:
   ```bash
   git add .
   git commit -m "feat({feature}): complete task-XXX - {title}"
   ```

## Resumption

To resume after interruption:
1. Read MEMORY.md for last state
2. Check git log for completed work
3. Continue from next uncompleted task
```

### 4. Generate MEMORY.md

**Template Structure:**

```markdown
# Ralph Memory — {Feature Title}

## Current State

- **Feature**: {feature-slug}
- **Started**: {timestamp}
- **Current Task**: task-001
- **Status**: IN_PROGRESS

## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | pending | - | - |
| task-002 | pending | - | - |
| ... | ... | ... | ... |

## Files Modified

{Updated during execution}

| File | Action | Task |
|------|--------|------|
| - | - | - |

## Tests Added

{Updated during execution}

| Test | Coverage | Task |
|------|----------|------|
| - | - | - |

## Issues Encountered

{Updated during execution}

| Issue | Resolution | Task |
|-------|------------|------|
| - | - | - |

## Decisions Made

{Updated during execution}

| Decision | Rationale | Task |
|----------|-----------|------|
| - | - | - |

## Context Notes

{Free-form notes for context preservation}

---

*Last updated: {timestamp}*
```

### 5. Generate ralph.sh

**Runner Script:**

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

# Start Claude Code with context
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

**Registry Structure:**

```json
{
  "version": "1.0",
  "features": [
    {
      "slug": "{feature-slug}",
      "title": "{Feature Title}",
      "created_at": "{timestamp}",
      "status": "ready",
      "complexity": "{level}",
      "tasks": {count},
      "spec_path": "docs/specs/{feature-slug}/",
      "ralph_path": ".ralph/{feature-slug}/",
      "prd_path": "docs/specs/{feature-slug}/{feature}.prd.json"
    }
  ]
}
```

**Update Logic:**
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

## BREAKPOINT:

```typescript
@skill:breakpoint-system
  type: validation
  title: "Specification Complete"
  data: {
    context: "All specification and Ralph artifacts generated",
    item_to_validate: {
      objectif: "Choose next action for feature implementation",
      contexte: "Feature: {feature-slug}, Complexity: {TINY|SMALL|STANDARD|LARGE}",
      contraintes: "Specs: docs/specs/{slug}/, Ralph: .ralph/{slug}/",
      success_criteria: "User selects implementation path"
    }
  }
  ask: {
    question: "How would you like to proceed?",
    header: "Next Step",
    options: [
      {label: "Launch {/quick or /implement} (Recommended)", description: "Start implementation workflow"},
      {label: "Run Ralph Batch", description: "Execute ./.ralph/{slug}/ralph.sh"},
      {label: "Review Files", description: "Inspect generated artifacts"},
      {label: "Done", description: "End workflow, implement later"}
    ]
  }
  suggestions: [
    {pattern: "stack", text: "Review PROMPT.md for stack-specific adjustments", priority: "P1"},
    {pattern: "parallel", text: "Consider parallel task execution for optimization", priority: "P2"}
  ]
```

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
