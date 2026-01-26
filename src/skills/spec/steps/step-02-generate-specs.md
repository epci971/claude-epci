---
name: step-02-generate-specs
description: Generate specification files
prev_step: steps/step-01-analyze.md
next_step: steps/step-03-generate-ralph.md
---

# Step 02: Generate Specifications

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER generate without APPROVED decomposition
- 🔴 NEVER skip acceptance criteria in task files
- 🔴 NEVER create PRD.json without all required fields
- ✅ ALWAYS use templates from templates/
- ✅ ALWAYS include Mermaid DAG in index.md
- ✅ ALWAYS validate JSON before writing
- 🔵 YOU ARE A TECHNICAL WRITER creating actionable specs
- 💭 FOCUS on clarity and completeness

## EXECUTION PROTOCOLS:

### 1. Create Directory Structure

```bash
mkdir -p docs/specs/{feature-slug}/
```

Verify directory created successfully.

### 2. Generate index.md

Use template from `templates/index.md.template`.

**Content Sections:**

```markdown
# {Feature Title}

> Technical Specification | Generated {date} | {task_count} tasks | {total_hours}h

## Overview

{Brief description from source}

## Scope

**In Scope:**
{bulleted list from source}

**Out of Scope:**
{bulleted list from source}

## Tasks

| # | Task | Description | Effort | Deps |
|---|------|-------------|--------|------|
| 001 | {title} | {description} | {min} min | - |
| 002 | {title} | {description} | {min} min | 001 |
| ... | ... | ... | ... | ... |

## Dependency Graph

```mermaid
graph TD
    subgraph Phase 1: Foundation
        T001[task-001: {title}]
    end
    subgraph Phase 2: Core
        T002[task-002: {title}]
        T003[task-003: {title}]
    end
    subgraph Phase 3: Integration
        T004[task-004: {title}]
    end

    T001 --> T002
    T002 --> T003
    T003 --> T004
```

## Execution Order

1. **task-001** — {title} (no dependencies)
2. **task-002** — {title} (after task-001)
3. ...

## Metrics

- **Total Tasks**: {count}
- **Total Steps**: {step_count}
- **Estimated Effort**: {hours}h
- **Critical Path**: {path}
- **Optimized Duration**: {optimized_hours}h
- **Complexity**: {TINY|SMALL|STANDARD|LARGE}

## Files

- [task-001-{slug}.md](task-001-{slug}.md)
- [task-002-{slug}.md](task-002-{slug}.md)
- ...
- [{feature}.prd.json]({feature}.prd.json)

## Routing

| Complexity | Recommended | Command |
|------------|-------------|---------|
| {level} | {/quick or /implement} | `/{skill} {slug} @docs/specs/{slug}/` |
```

### 3. Generate task-XXX.md Files

For each task, use template from `templates/task.md.template`.

**Content Structure:**

```markdown
---
id: task-{NNN}
title: {Task Title}
slug: {task-slug}
feature: {feature-slug}
complexity: {S|M|L}
estimated_minutes: {60-120}
dependencies: [{list}]
files_affected: [{list}]
test_approach: {Unit|Integration|E2E}
---

# Task {NNN}: {Title}

## Objective

{Clear statement of what this task delivers}

## Context

{Brief background from source relevant to this task}

## Acceptance Criteria

### AC1: {Criterion Title}
- **Given**: {precondition}
- **When**: {action}
- **Then**: {expected result}

### AC2: {Criterion Title}
- **Given**: {precondition}
- **When**: {action}
- **Then**: {expected result}

## Steps

### Step 1: {Action} ({duration} min)

**Input**: {what's needed}

**Actions**:
1. {detailed action 1}
2. {detailed action 2}
3. {detailed action 3}

**Output**: {deliverable}

**Validation**: {how to verify}

### Step 2: {Action} ({duration} min)

...

### Step N: {Action} ({duration} min)

...

## Files

| Path | Action | Description |
|------|--------|-------------|
| `{path}` | create/modify | {description} |
| ... | ... | ... |

## Test Approach

- **Type**: {Unit|Integration|E2E}
- **Framework**: {framework from project context}
- **Coverage Target**: {percentage}

### Test Cases

| # | Description | Type |
|---|-------------|------|
| 1 | {description} | Unit |
| 2 | {description} | Integration |

## Dependencies

- **Requires**: {list of task-XXX this depends on}
- **Blocks**: {list of task-XXX that depend on this}

## Notes

{Any additional context, warnings, or considerations}
```

### 4. Generate PRD.json

Create machine-readable version for Ralph.

**Schema (prd-v2):**

```json
{
  "title": "{Feature Title}",
  "version": "2.0",
  "slug": "{feature-slug}",
  "generated_at": "{ISO-8601}",
  "source": "{brief path or 'text'}",
  "complexity": "{TINY|SMALL|STANDARD|LARGE}",
  "metrics": {
    "total_tasks": {count},
    "total_steps": {count},
    "estimated_hours": {hours},
    "critical_path": ["{task-ids}"],
    "optimized_hours": {hours}
  },
  "tasks": [
    {
      "id": "task-001",
      "title": "{title}",
      "slug": "{slug}",
      "complexity": "S|M|L",
      "estimated_minutes": {60-120},
      "dependencies": [],
      "acceptance_criteria": [
        {
          "id": "AC1",
          "given": "{precondition}",
          "when": "{action}",
          "then": "{result}"
        }
      ],
      "steps": [
        {
          "id": "step-1",
          "title": "{title}",
          "duration_minutes": {15-30},
          "input": "{input}",
          "output": "{output}",
          "validation": "{validation}"
        }
      ],
      "files_affected": [
        {
          "path": "{path}",
          "action": "create|modify"
        }
      ],
      "test_approach": "{Unit|Integration|E2E}"
    }
  ],
  "dependencies_graph": {
    "nodes": ["{task-ids}"],
    "edges": [
      {"from": "task-001", "to": "task-002"}
    ]
  },
  "routing": {
    "recommended_skill": "/quick|/implement",
    "reason": "{rationale}"
  }
}
```

**Validation:**
- All required fields present
- All tasks have >= 2 acceptance criteria
- No circular dependencies in graph
- JSON is valid

### 5. Write Files

Write in order:
1. `index.md`
2. `task-001-{slug}.md`, `task-002-{slug}.md`, ...
3. `{feature}.prd.json`

Verify each file written successfully.

## CONTEXT BOUNDARIES:

- This step expects: Approved decomposition, task list, DAG
- This step produces: index.md, task-XXX.md files, PRD.json

## OUTPUT FORMAT:

```
## Specs Generated

Location: docs/specs/{feature-slug}/

### Files Created
- [x] index.md (orchestrator)
- [x] task-001-{slug}.md
- [x] task-002-{slug}.md
- [x] ...
- [x] {feature}.prd.json

### Summary
- Tasks: {count}
- Total Steps: {step_count}
- Lines: {total_lines}
- JSON valid: Yes
```

## BREAKPOINT:

```typescript
@skill:epci:breakpoint-system
  type: plan-review
  title: "Specifications Generated"
  data: {
    metrics: {
      complexity: "{complexity}",
      complexity_score: {score},
      files_impacted: {task_count},
      time_estimate: "{total_hours}h",
      risk_level: "LOW",
      risk_description: "Spec generation only, no code changes"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "{task_count} tasks with {step_count} steps",
        consistency: "All dependencies mapped in DAG",
        feasibility: "Effort estimates calibrated",
        quality: "Acceptance criteria defined per task"
      }
    },
    skills_loaded: ["project-memory", "decompose-validator"],
    preview_next: {
      tasks: [
        {title: "index.md ({lines} lines)", time: "-"},
        {title: "task-001-{slug}.md", time: "{estimate}"},
        {title: "{feature}.prd.json ({size} KB)", time: "-"}
      ],
      remaining_tasks: {task_count}
    },
    feature_doc_path: "docs/specs/{feature-slug}/"
  }
  ask: {
    question: "Proceed with specifications?",
    header: "Specs Review",
    options: [
      {label: "Continue to Ralph (Recommended)", description: "Generate execution artifacts"},
      {label: "Skip Ralph", description: "Specs only, no execution artifacts"},
      {label: "Edit Tasks", description: "Modify generated task files"},
      {label: "Regenerate", description: "Regenerate with changes"}
    ]
  }
  suggestions: [
    {pattern: "review-ac", text: "Review acceptance criteria for completeness", priority: "P1"},
    {pattern: "edge-cases", text: "Consider adding edge case tests", priority: "P2"}
  ]
```

## NEXT STEP TRIGGER:

When user approves specs, proceed to `step-03-generate-ralph.md`.

If user selects "Skip Ralph", proceed to completion summary.
