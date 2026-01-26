---
name: implement
description: >-
  Full implementation workflow for STANDARD and LARGE features through multi-phase
  EPCI execution. Routes through Explore, Plan, Code, Inspect phases with TDD enforcement.
  Supports plan-first workflow via @plan-path to skip E-P phases (uses Claude Code native plan).
  Use when: building features, implementing specs, developing from PRD.
  Triggers: implement feature, build, develop, create feature.
  Not for: quick fixes (use /quick), debugging (use /debug), refactoring (use /refactor).
user-invocable: true
argument-hint: "<feature-slug> [@spec-path | @plan-path]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Task
---

# Implement

Full implementation workflow for STANDARD and LARGE features using EPCI phases.

## Quick Start

```
/epci:implement feature-slug
/epci:implement feature-slug @docs/specs/feature.md
/epci:implement feature-slug @.claude/plans/feature-plan.md
```

## Input Detection

```
INPUT
├── @.claude/plans/*.md → PLAN-FIRST workflow (skip E-P)
│   └─ Native Claude Code plan already done, go directly to CODE
├── @docs/specs/*.md → SPEC-FIRST workflow (skip E)
│   └─ Spec exists, do minimal planning then CODE
└── feature-slug only → FULL workflow (E-P-C-I-M)
    └─ Full Explore + Plan phases first
```

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER execute steps out of order
- :red_circle: NEVER skip the planning phase
- :red_circle: NEVER modify files during exploration (Step 01)
- :red_circle: NEVER skip TDD for STANDARD+ complexity
- :white_check_mark: ALWAYS start with step-00-init.md
- :white_check_mark: ALWAYS follow next_step from each step
- :white_check_mark: ALWAYS present breakpoints at phase transitions
- :white_check_mark: ALWAYS complete code review before documentation
- :no_entry: FORBIDDEN skipping tests for STANDARD or LARGE features
- :large_blue_circle: YOU ARE A METHODICAL IMPLEMENTER following EPCI discipline
- :thought_balloon: FOCUS on one phase at a time, complete before proceeding

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoint if specified in step
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: Feature implementation following EPCI phases, TDD workflow, code review
- OUT scope: Quick fixes (use /quick), debugging (use /debug), pure refactoring (use /refactor)

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    IMPLEMENT WORKFLOW (EPCI)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Step 00: INIT                                                       │
│  └─ Detect complexity, validate input                                │
│     └─ If TINY/SMALL → step-00b-turbo (redirect to /quick)           │
│                                                                      │
│  Step 01: EXPLORE [E]                                                │
│  └─ Read-only codebase analysis                                      │
│  └─ Identify patterns, dependencies                                  │
│     └─ BREAKPOINT: Exploration findings                              │
│                                                                      │
│  Step 02: PLAN [P]                                                   │
│  └─ Create implementation plan                                       │
│  └─ Define test strategy                                             │
│     └─ BREAKPOINT: Plan validation                                   │
│                                                                      │
│  Step 03: CODE [C]                                                   │
│  └─ TDD cycle: RED → GREEN → REFACTOR                                │
│  └─ Implement feature incrementally                                  │
│                                                                      │
│  Step 04: REVIEW [I]                                                 │
│  └─ Code review with @code-reviewer                                  │
│     └─ If security concerns → step-04b-security                      │
│     └─ If QA needed → step-04c-qa                                    │
│     └─ BREAKPOINT: Review approval                                   │
│                                                                      │
│  Step 05: DOCUMENT                                                   │
│  └─ Update Feature Document                                          │
│  └─ Update relevant docs                                             │
│                                                                      │
│  Step 06: FINISH                                                     │
│  └─ Final validation                                                 │
│  └─ Completion summary                                               │
│                                                                      │
│  Step 07: MEMORY [M]                                                 │
│  └─ Generate summary (1-2 sentences)                                 │
│  └─ Collect modified_files list                                      │
│  └─ Count tests added                                                │
│  └─ Append/update index.json                                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Steps

| Step | Name | Phase | Description |
|------|------|-------|-------------|
| 00 | init | - | Detect complexity, validate input |
| 00b | turbo | - | Redirect TINY/SMALL to /quick |
| 01 | explore | [E] | Read-only codebase analysis |
| 02 | plan | [P] | Implementation planning |
| 03 | code | [C] | TDD implementation |
| 04 | review | [I] | Code review |
| 04b | security | [I] | Security-focused review |
| 04c | qa | [I] | QA validation |
| 05 | document | - | Documentation updates |
| 06 | finish | - | Finalization |
| 07 | memory | [M] | Update index.json with summary |

## Decision Tree

```
IF complexity == TINY or SMALL:
  → Redirect to /quick (step-00b-turbo)
ELSE IF complexity == STANDARD:
  → Full EPCI workflow (step-01 → step-06)
ELSE IF complexity == LARGE:
  → Full EPCI workflow with enhanced reviews
  → Always include step-04b-security
```

## Complexity Routing

| Complexity | LOC | Files | Workflow |
|------------|-----|-------|----------|
| TINY | < 50 | 1-2 | → /quick |
| SMALL | 50-200 | 1-3 | → /quick |
| STANDARD | 200-500 | 2-5 | → Full EPCI |
| LARGE | 500+ | 5+ | → Full EPCI + security |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-00b-turbo.md](steps/step-00b-turbo.md) — Turbo redirect
- [steps/step-01-explore.md](steps/step-01-explore.md) — Exploration [E]
- [steps/step-02-plan.md](steps/step-02-plan.md) — Planning [P]
- [steps/step-03-code.md](steps/step-03-code.md) — Coding [C]
- [steps/step-04-review.md](steps/step-04-review.md) — Review [I]
- [steps/step-04b-security.md](steps/step-04b-security.md) — Security review
- [steps/step-04c-qa.md](steps/step-04c-qa.md) — QA review
- [steps/step-05-document.md](steps/step-05-document.md) — Documentation
- [steps/step-06-finish.md](steps/step-06-finish.md) — Finalization
- [steps/step-07-memory.md](steps/step-07-memory.md) — Memory update

## Reference Files

- [references/tdd-rules.md](references/tdd-rules.md) — TDD workflow rules
- [references/review-checklists.md](references/review-checklists.md) — Code review checklists

## Shared Components Used

- `state-manager` — Track progress across sessions
- `complexity-calculator` — Scope validation and routing
- `tdd-enforcer` — Ensure TDD compliance
- `breakpoint-system` — Phase checkpoints
- `project-memory` — Context persistence

## Limitations

This skill does NOT:
- Handle quick fixes (use /quick)
- Debug existing bugs (use /debug)
- Pure refactoring without feature change (use /refactor)
- Generate specifications (use /spec)
