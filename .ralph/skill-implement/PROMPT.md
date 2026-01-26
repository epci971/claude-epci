# Ralph Execution Prompt — Skill /implement v6 Refonte

## Context

You are executing feature **skill-implement** in autonomous batch mode.
Branch: `feature/skill-implement-v6-refonte`
Complexity: STANDARD
Total tasks: 6

## Source Documents

- PRD (human readable): `docs/specs/skill-implement/index.md`
- PRD (machine readable): `docs/specs/skill-implement/skill-implement.prd.json`
- Memory file: `.ralph/skill-implement/MEMORY.md`
- Brief: `docs/briefs/skill-implement/brief-skill-implement-20260126.md`

## Project Stack

This is a **plugin project** for Claude Code:
- Content: Markdown (skills, agents)
- Scripts: Python 3
- Config: JSON/YAML
- No frontend framework
- No database

## Conventions

### File Naming
- SKILL.md for main skill files
- step-XX-name.md for step files
- kebab-case for file names

### Markdown Structure
- YAML frontmatter required
- Sections with ## headers
- Tables for structured data
- Mermaid for diagrams

### Token Limits
- SKILL.md: < 5000 tokens
- Step files: < 300 lines
- Reference files: < 300 lines

## Execution Rules

### Task Processing

For each task in PRD.json `tasks[]`:
1. Read the task and its `acceptance_criteria`
2. Read each `step` within the task
3. Implement using the step instructions:
   - Follow Input → Actions → Output → Validation pattern
   - Update MEMORY.md after each step
4. Mark task as done in MEMORY.md
5. Commit: `feat(skills): {task_title} [task-{id}]`

### Task Order (respect dependencies)

1. **task-001**: Update SKILL.md Structure (no deps)
2. **task-002**: Add Stack & Core Skills Section (after task-001)
3. **task-003**: Update step-00-init.md (after task-001)
4. **task-004**: Update step-03-code.md (after task-001)
5. **task-005**: Update step-04-review.md (after task-001)
6. **task-006**: Create New References (after task-002, 003, 004, 005)

**Note**: Tasks 002-005 can run in parallel after task-001 completes.

### Validation After Each Task

```bash
python src/scripts/validate_all.py
```

If validation fails, fix issues before proceeding.

### Stop Conditions

- All tasks done
- Max iterations reached (50)
- 3 consecutive blocked tasks
- Critical error (validation repeatedly fails)

## Files to Modify/Create

### Modify
- `src/skills/implement/SKILL.md`
- `src/skills/implement/steps/step-00-init.md`
- `src/skills/implement/steps/step-03-code.md`
- `src/skills/implement/steps/step-04-review.md`

### Create
- `src/skills/implement/references/stack-integration.md`
- `src/skills/implement/references/multi-agent-review.md`
- `src/skills/implement/references/turbo-mode.md`

## Quality Gates

- [ ] Token count < 5000 for SKILL.md
- [ ] All sections present and complete
- [ ] Mermaid diagram renders correctly
- [ ] Cross-references are valid
- [ ] Validation script passes

## Commit Convention

```
feat(skills): {task title} [task-{NNN}]

- {change 1}
- {change 2}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```
