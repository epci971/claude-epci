# Ralph Generation Guide

> Reference for generating Ralph execution artifacts.

## Cross-References

| Topic | Reference File |
|-------|---------------|
| Stack detection & guidelines | [stack-guidelines.md](stack-guidelines.md) |
| MEMORY.md structure | [memory-template.md](memory-template.md) |
| TDD & execution rules | [execution-workflow.md](execution-workflow.md) |
| Breakpoint formats | [breakpoint-formats.md](breakpoint-formats.md) |

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

---

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
{MANDATORY rules — see execution-workflow.md}

## Specifications
{Location and files list}

## Execution Order
{Topological order from DAG}

## Stack-Specific Guidelines
{Conventions for detected stack — see stack-guidelines.md}

## Context Persistence
{Instructions for updating MEMORY.md}

## Resumption
{How to continue after interruption}
```

### Generation

1. Detect stack using [stack-guidelines.md#stack-detection-matrix](stack-guidelines.md#stack-detection-matrix)
2. Load appropriate guidelines from stack-guidelines.md
3. Fill template from `templates/prompt.md.template`
4. Inject execution rules from [execution-workflow.md](execution-workflow.md)

---

## MEMORY.md

### Purpose

Tracks execution state for:
- Progress monitoring
- Resumption after interruption
- History and decisions

### Template

See [memory-template.md](memory-template.md) for complete template structure.

### Generation

1. Initialize all tasks as `pending` in Progress table
2. Set Current Task to first task ID
3. Set Status to `PENDING`
4. Set Started to current ISO-8601 timestamp
5. Leave modification tables empty
6. Add Context Notes placeholder

---

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
claude --resume-with-context "${RALPH_DIR}/PROMPT.md" \
       --memory "${RALPH_DIR}/MEMORY.md"

echo ""
echo "=== Ralph Execution Complete ==="
```

### Making Executable

```bash
chmod +x .ralph/{feature-slug}/ralph.sh
```

---

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

---

## Execution

### Starting

```bash
cd /path/to/project
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

See [execution-workflow.md](execution-workflow.md) for detailed rules.

### Resumption

If interrupted:
1. Run ralph.sh again
2. Claude Code reads MEMORY.md
3. Continues from last in_progress task
4. Skips completed tasks

See [execution-workflow.md#resumption-protocol](execution-workflow.md#resumption-protocol).

---

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

---

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
