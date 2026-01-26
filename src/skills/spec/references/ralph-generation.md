# Ralph Generation Guide

> Reference for generating Ralph execution artifacts.

## Overview

Ralph is the batch execution system for EPCI. It uses Claude Code with persistent context to execute tasks autonomously. The `/spec` skill generates three artifacts:

1. **PROMPT.md** — Instructions for Claude Code
2. **MEMORY.md** — Persistent execution state
3. **ralph.sh** — Runner script

## Directory Structure

```
.ralph/{feature-slug}/
├── PROMPT.md      # Claude Code instructions
├── MEMORY.md      # Execution state (updates during run)
└── ralph.sh       # Executable runner script
```

## PROMPT.md

### Purpose

Provides Claude Code with:
- Feature context and scope
- Execution rules and workflow
- Stack-specific guidelines
- Context persistence instructions

### Template Structure

```markdown
# Ralph Execution Context — {Feature Title}

## Feature
{Basic metadata: slug, complexity, tasks, estimated hours}

## Stack
{Detected stack info: framework, language, test framework}

## Execution Rules
{MANDATORY rules for execution}

## Specifications
{Location and files list}

## Execution Order
{Topological order from DAG}

## Stack-Specific Guidelines
{Conventions for detected stack}

## Context Persistence
{Instructions for updating MEMORY.md}

## Resumption
{How to continue after interruption}
```

### Stack Detection

Detect from project files:

| Stack | Detection Files | Result |
|-------|-----------------|--------|
| Django | `manage.py` + `requirements.txt` with django | Python/Django |
| React | `package.json` with react | JavaScript/React |
| Spring | `pom.xml` or `build.gradle` with spring-boot | Java/Spring |
| Symfony | `composer.json` with symfony | PHP/Symfony |
| Generic | No specific markers | Generic |

### Stack-Specific Content

**Django:**
```markdown
### For Django:
- Use service layer pattern (avoid fat models/views)
- pytest for testing with Factory Boy fixtures
- Type hints required (mypy compatible)
- Django REST Framework for APIs
- Celery for async tasks
```

**React:**
```markdown
### For React:
- Functional components with hooks (no classes)
- Vitest + React Testing Library
- Zustand for state management (if needed)
- TypeScript in strict mode
- Tailwind CSS for styling
```

**Spring:**
```markdown
### For Spring:
- Service layer pattern with interfaces
- JUnit 5 + Mockito for testing
- Lombok to reduce boilerplate
- Constructor injection (not field)
- Spring Security for auth
```

**Symfony:**
```markdown
### For Symfony:
- Service layer pattern
- PHPUnit + Prophecy for testing
- Doctrine ORM for persistence
- Voters for authorization
- Messenger for async processing
```

## MEMORY.md

### Purpose

Tracks execution state for:
- Progress monitoring
- Resumption after interruption
- History and decisions

### Template Structure

```markdown
# Ralph Memory — {Feature Title}

## Current State
{Feature slug, start time, current task, status}

## Progress
{Table of tasks with status}

## Files Modified
{Updated during execution}

## Tests Added
{Updated during execution}

## Issues Encountered
{Updated during execution}

## Decisions Made
{Updated during execution}

## Context Notes
{Free-form notes}

---
*Last updated: {timestamp}*
```

### Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Not yet started |
| `in_progress` | Currently executing |
| `completed` | Successfully finished |
| `blocked` | Waiting on external factor |
| `failed` | Encountered error |

### Update Protocol

After each task completion:

1. Update task status to `completed`
2. Add files modified to table
3. Add tests created to table
4. Record any decisions made
5. Update timestamp

Example update:

```markdown
## Progress

| Task | Status | Completed At | Notes |
|------|--------|--------------|-------|
| task-001 | completed | 2026-01-26T11:00:00Z | - |
| task-002 | in_progress | - | Working on step 2 |
| task-003 | pending | - | - |

## Files Modified

| File | Action | Task |
|------|--------|------|
| src/models/user.py | created | task-001 |
| tests/test_user.py | created | task-001 |
```

## ralph.sh

### Purpose

Executable script that:
- Validates prerequisites
- Launches Claude Code with context
- Passes PROMPT.md and MEMORY.md

### Template

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
# Note: Actual invocation depends on Claude Code CLI version
claude --resume-with-context "${RALPH_DIR}/PROMPT.md" \
       --memory "${RALPH_DIR}/MEMORY.md"

echo ""
echo "=== Ralph Execution Complete ==="
```

### Making Executable

```bash
chmod +x .ralph/{feature-slug}/ralph.sh
```

## index.json Registry

### Purpose

Central registry of all Ralph-enabled features.

### Location

`.ralph/index.json`

### Schema

```json
{
  "version": "1.0",
  "features": [
    {
      "slug": "auth-oauth",
      "title": "OAuth Authentication",
      "created_at": "2026-01-26T10:30:00Z",
      "status": "ready",
      "complexity": "STANDARD",
      "tasks": 5,
      "spec_path": "docs/specs/auth-oauth/",
      "ralph_path": ".ralph/auth-oauth/",
      "prd_path": "docs/specs/auth-oauth/auth-oauth.prd.json"
    }
  ]
}
```

### Status Values

| Status | Meaning |
|--------|---------|
| `ready` | Can be executed |
| `running` | Currently executing |
| `completed` | All tasks done |
| `paused` | Execution paused |

### Update Protocol

When generating new feature:
1. Read existing index.json (or create if missing)
2. Check for duplicate slug
3. Append new feature entry
4. Write updated index.json

## Execution Workflow

### Starting Execution

```bash
# Navigate to project root
cd /path/to/project

# Run Ralph for feature
./.ralph/auth-oauth/ralph.sh
```

### During Execution

Claude Code will:
1. Read PROMPT.md for context
2. Check MEMORY.md for current state
3. Execute next pending task
4. Follow steps sequentially
5. Update MEMORY.md after each task
6. Commit changes with conventional commits

### Resumption

If interrupted:
1. Run ralph.sh again
2. Claude Code reads MEMORY.md
3. Continues from last in_progress task
4. Skips completed tasks

### Completion

When all tasks completed:
1. MEMORY.md shows all tasks as `completed`
2. Final summary displayed
3. Consider running `/implement` review phase

## Best Practices

### PROMPT.md

- Keep stack guidelines focused
- Include commit message format
- Reference spec file locations explicitly
- Add project-specific conventions

### MEMORY.md

- Initialize with all tasks in `pending`
- Update after each task, not each step
- Keep context notes brief but useful
- Include error details if failed

### ralph.sh

- Always check prerequisites
- Display clear progress messages
- Handle missing files gracefully
- Support dry-run mode (future)

## Troubleshooting

### Ralph Won't Start

1. Check `.ralph/{slug}/` directory exists
2. Verify `ralph.sh` is executable
3. Confirm `PROMPT.md` and `MEMORY.md` exist
4. Check spec directory exists

### Task Stuck

1. Check MEMORY.md for current state
2. Look at Issues Encountered section
3. Manually update status if needed
4. Restart Ralph

### Wrong Stack Detected

1. Edit PROMPT.md manually
2. Adjust stack-specific guidelines
3. Regenerate if needed

## Integration

### With /implement

After Ralph completes:
```bash
/implement {slug} @docs/specs/{slug}/
```

This triggers code review phase.

### With /quick

For simpler features:
```bash
/quick {slug} @docs/specs/{slug}/
```

Faster execution without full review.

### Manual Execution

If Ralph not available, follow specs manually:
1. Read `docs/specs/{slug}/index.md`
2. Execute tasks in order
3. Follow acceptance criteria
4. Run tests after each task
