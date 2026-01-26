---
name: quick
description: >
  Fast implementation for TINY and SMALL tasks. Single-phase execution
  with optional TDD. Ideal for bug fixes, small features, and quick changes.
  Supports plan-first workflow via @plan-path to skip E-P phases.
  Trigger words: quick fix, small change, tiny feature, fast implementation.
user-invocable: true
argument-hint: "<task> | @<plan-path>"
---

# Quick

Fast implementation for TINY and SMALL tasks.

## Usage

```
/epci:quick "fix the login button alignment"
/epci:quick "add validation to email field"
/epci:quick @.claude/plans/fix-auth.md
```

## Input Detection

```
INPUT
├── @plan-path provided → PLAN-FIRST workflow (skip E-P)
│   └─ Load plan, extract objectives, files, criteria
└── Text description → FULL workflow (E-P-C-T-M)
    └─ Mini-Explore + Mini-Plan first
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DETECT INPUT                                             │
│    ├─ @path → Load plan, parse objectives/files/criteria    │
│    └─ text → Mini-Explore + Mini-Plan                       │
├─────────────────────────────────────────────────────────────┤
│ 2. VALIDATE COMPLEXITY                                      │
│    └─ Via complexity-calculator                             │
│    └─ If STANDARD/LARGE → Suggest /implement                │
├─────────────────────────────────────────────────────────────┤
│ 3. PHASE [C+T]: CODE + TDD                                  │
│    ┌──────────────────────────────────────────────────────┐ │
│    │ RED    → Write failing test                          │ │
│    │ GREEN  → Minimal code to pass                        │ │
│    │ REFACTOR → Clean up (tests green)                    │ │
│    │ VERIFY → Run full test suite                         │ │
│    └──────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 4. PHASE [M]: MEMORY                                        │
│    └─ Generate summary (1-2 sentences)                      │
│    └─ Collect modified_files list                           │
│    └─ Count tests added                                     │
│    └─ Append to .claude/state/features/index.json           │
└─────────────────────────────────────────────────────────────┘
```

## Phases

| Phase | Name | Description | Skippable |
|-------|------|-------------|-----------|
| E | Explore | Quick codebase scan | Yes (if @plan) |
| P | Plan | Minimal planning | Yes (if @plan) |
| C+T | Code+Test | TDD implementation | No |
| M | Memory | Update index.json | No |

## Complexity Limits

| Category | Files | LOC | Action |
|----------|-------|-----|--------|
| TINY | 1 | < 50 | Execute |
| SMALL | 2-3 | < 200 | Execute |
| STANDARD | 4+ | 200+ | → Suggest /implement |
| LARGE | 5+ | 500+ | → Suggest /implement |

## MEMORY Phase Details

At completion, update `.claude/state/features/index.json`:

```json
{
  "id": "{feature-slug}",
  "status": "completed",
  "current_phase": "inspect",
  "complexity": "SMALL",
  "summary": "Fixed login button alignment using flexbox",
  "modified_files": ["src/components/LoginButton.tsx"],
  "test_count": 2,
  "created_at": "...",
  "last_update": "..."
}
```

## Shared Components Used

- `state-manager` - Track progress, update index.json
- `complexity-calculator` - Validate scope, routing
- `tdd-enforcer` - TDD cycle enforcement
- `project-memory` - Context persistence

## References

See [references/](references/) for additional documentation.
