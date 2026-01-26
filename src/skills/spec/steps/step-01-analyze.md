---
name: step-01-analyze
description: Analyze source and decompose into tasks
prev_step: steps/step-00-init.md
next_step: steps/step-02-generate-specs.md
---

# Step 01: Analysis & Decomposition

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER create circular dependencies
- :red_circle: NEVER skip @decompose-validator validation
- :red_circle: NEVER exceed granularity limits (tasks 1-2h, steps 15-30min)
- :white_check_mark: ALWAYS build dependency DAG
- :white_check_mark: ALWAYS calculate complexity first
- :white_check_mark: ALWAYS extract acceptance criteria from source
- :large_blue_circle: YOU ARE A SYSTEMS ANALYST decomposing work
- :thought_balloon: FOCUS on logical task boundaries and dependencies

## EXECUTION PROTOCOLS:

### 1. Parse Source Structure

**For Brief (PRD v3.0):**
```
Extract:
├── Section 1: Context → Background, constraints
├── Section 2: Executive Summary → Key requirements
├── Section 3: Analysis → Technical findings
├── Section 4: Decisions → Architectural choices
├── Section 5: Action Plan → High-level tasks
├── Section 6: Risks → Mitigations to include
└── Section 10: EMS → Confidence level
```

**For Text Description:**
```
Parse:
├── Main objective
├── Key features (bullet points)
├── Constraints mentioned
└── Implicit requirements
```

### 2. Calculate Complexity

Invoke `complexity-calculator`:

```
complexity-calculator.calculate({
  source: "{parsed_content}",
  context: "{project_context}"
})

Returns:
├── complexity: TINY|SMALL|STANDARD|LARGE
├── estimated_loc: number
├── estimated_files: number
├── estimated_hours: number
└── routing: "/quick" | "/implement"
```

Store for later routing recommendation.

### 3. Identify Task Boundaries

Apply decomposition patterns:

| Pattern | When to Apply | Result |
|---------|---------------|--------|
| **Vertical Slice** | UI + API + DB for same feature | Task per slice |
| **Horizontal Layer** | Clear layer separation | Task per layer |
| **Atomic User Story** | Independent user-facing units | Task per story |
| **Technical Debt** | Refactoring needed first | Prep task + main |

**Goldilocks Zone Rules:**
- Task too small (< 30 min): Merge with related
- Task too large (> 3h): Split by subtask

### 4. Define Tasks (1-2h each)

For each identified task:

```yaml
id: "task-{NNN}"
title: "{Action verb} {Component}"
slug: "{action-component}"
objective: "{What this task delivers}"
complexity: "S|M|L"
estimated_minutes: {60-120}
dependencies: ["task-XXX", ...]
acceptance_criteria:
  - "Given X, when Y, then Z"
  - "..."
files_affected:
  - path: "src/..."
    action: "create|modify"
test_approach: "{Unit|Integration|E2E}"
```

### 5. Define Steps (15-30min each)

For each task, decompose into steps:

```yaml
steps:
  - id: "step-1"
    title: "{Action verb} {specific action}"
    duration_minutes: 15
    input: "{What's needed to start}"
    output: "{What's produced}"
    validation: "{How to verify completion}"
  - id: "step-2"
    ...
```

**Step Guidelines:**
- Action verb start: "Create", "Implement", "Configure", "Test"
- Single responsibility
- Clear input/output contract
- Verifiable completion

### 6. Build Dependency DAG

Construct directed acyclic graph:

```
Tasks:
├── task-001: Setup foundation (no deps)
├── task-002: Implement models (deps: task-001)
├── task-003: Implement services (deps: task-002)
├── task-004: Implement API (deps: task-003)
├── task-005: Implement UI (deps: task-004)
└── task-006: Integration tests (deps: task-004, task-005)

Graph:
task-001 ─► task-002 ─► task-003 ─► task-004 ─┬─► task-006
                                               │
                                   task-005 ───┘
```

### 7. Calculate Execution Order

Perform topological sort:

```
Execution Order:
1. task-001 (no deps, critical path start)
2. task-002 (depends on 1)
3. task-003 (depends on 2)
4. task-004 (depends on 3)
5. task-005 (can parallel with 4 if no dep)
6. task-006 (depends on 4, 5)

Parallel Opportunities:
- task-004 and task-005 can run in parallel
- Optimized duration: X hours (vs Y hours sequential)
```

### 8. Validate with @decompose-validator

Invoke agent:

```
@decompose-validator {
  tasks: [...],
  dag: {...},
  source_sections: [...],
  granularity: { min_task_minutes: 60, max_task_minutes: 120 }
}

Expected: APPROVED | NEEDS_REVISION
```

**If NEEDS_REVISION:**
- Display issues from validator
- Apply fixes
- Re-validate until APPROVED

## CONTEXT BOUNDARIES:

- This step expects: Validated source, project context
- This step produces: Task list, DAG, execution order, validation report

## OUTPUT FORMAT:

```
## Decomposition Complete

### Complexity
Level: {TINY|SMALL|STANDARD|LARGE}
Estimated: ~{loc} LOC across {files} files (~{hours}h)

### Tasks ({count})

| # | Task | Deps | Effort | Steps |
|---|------|------|--------|-------|
| 001 | {title} | - | {min} min | {count} |
| 002 | {title} | 001 | {min} min | {count} |
| ... | ... | ... | ... | ... |

### DAG

```mermaid
graph LR
    T001[task-001] --> T002[task-002]
    T002 --> T003[task-003]
    ...
```

### Execution Summary
- Total effort: {hours}h
- Critical path: {path}
- Parallel opportunities: {count}
- Optimized duration: {hours}h

### Validation: {APPROVED}
```

## BREAKPOINT:

```
┌─────────────────────────────────────────────────────────────────────┐
│ [DECOMPOSITION] Task Breakdown Review                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Feature: {feature-slug}                                              │
│ Complexity: {level}                                                  │
│ Tasks: {count} | Steps: {total_steps}                                │
│ Estimated: ~{hours}h ({optimized}h optimized)                        │
│                                                                      │
│ ┌─ Tasks ───────────────────────────────────────────────────────┐   │
│ │ 001. {title} ({min} min, {steps} steps)                       │   │
│ │ 002. {title} ({min} min, {steps} steps) ← 001                 │   │
│ │ 003. {title} ({min} min, {steps} steps) ← 002                 │   │
│ │ ...                                                            │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ ┌─ DAG ─────────────────────────────────────────────────────────┐   │
│ │ T001 ──► T002 ──► T003 ──┬──► T005                            │   │
│ │                          └──► T004 ──► T006                   │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ Validation: @decompose-validator → {APPROVED}                        │
│                                                                      │
│ :bulb: P1: Consider splitting task-003 if scope grows                       │
│ :bulb: P2: task-004 and task-005 can parallelize                            │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ [A] Approve and generate specs (Recommended)                         │
│ [B] Modify task breakdown                                            │
│ [C] View task details                                                │
│ [D] Re-decompose with different strategy                             │
│ [E] Cancel                                                           │
└─────────────────────────────────────────────────────────────────────┘
```

## NEXT STEP TRIGGER:

When decomposition is APPROVED and user confirms, proceed to `step-02-generate-specs.md`.
