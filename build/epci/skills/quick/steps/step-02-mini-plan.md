---
name: step-02-mini-plan
description: Generate minimal implementation plan with test strategy
prev_step: steps/step-01-mini-explore.md
next_step: steps/step-03-code.md
---

# Step 02: Mini-Plan [P]

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER create a plan longer than necessary
- :red_circle: NEVER skip test strategy definition
- :white_check_mark: ALWAYS follow plan structure from references
- :white_check_mark: ALWAYS define completion criteria
- :thought_balloon: FOCUS on minimal viable plan - just enough to guide implementation

## EXECUTION PROTOCOLS:

### 1. Generate Minimal Plan

Create a lightweight plan following the structure in [references/plan-structure.md](../references/plan-structure.md):

```markdown
# Plan: {Feature Name}

## Objective
{1-2 sentences describing what to achieve}

## Files
- [ ] {path/to/file1} -- {action: modify}
- [ ] {path/to/file2} -- {action: modify}

## Steps
1. [ ] {Action verb} {target} -- {success criteria}
2. [ ] {Action verb} {target} -- {success criteria}
3. [ ] {Action verb} {target} -- {success criteria}

## Tests
- [ ] Unit: {test description}

## Done When
{Clear completion criteria}
```

### 2. Define Test Strategy

Determine what tests to write:

```
TEST STRATEGY:
├── Type: {unit | integration | both}
├── Framework: {jest | pytest | phpunit | junit}
├── Target: {function/component to test}
└── Cases:
    ├── Happy path: {description}
    └── Edge case: {if applicable}
```

**Rules:**
- At minimum: 1 test for happy path
- TINY: 1 test sufficient
- SMALL: 1-3 tests recommended

### 3. Estimate LOC

Quick estimate of code changes:

| File | Action | Estimated LOC |
|------|--------|---------------|
| {file1} | modify | +{N} |
| {file2} | modify | +{N} |
| {test} | create/modify | +{N} |
| **Total** | | **+{total}** |

**Validation:**
- TINY: max 50 LOC total
- SMALL: max 200 LOC total
- If exceeds → warn but continue (user accepted complexity)

### 4. Define Completion Criteria

Clear, measurable criteria:

```
COMPLETION CRITERIA:
1. [ ] All tests pass
2. [ ] Lint passes
3. [ ] {Specific behavioral criteria}
```

## CONTEXT BOUNDARIES:

- This step expects: Target files and patterns from step-01
- This step produces: Minimal plan with test strategy
- Time budget: < 15 seconds

## OUTPUT FORMAT:

```
## Mini-Plan Ready

Plan Summary:
- Files: {count}
- Steps: {count}
- Tests: {count}
- Est. LOC: {total}

Test Strategy:
- Framework: {name}
- Type: {unit/integration}

Ready to execute with @implementer.
```

## PLAN VALIDATION:

Check plan is viable for /quick:

| Check | Limit | Actual |
|-------|-------|--------|
| Files | ≤ 3 | {count} |
| Steps | ≤ 5 | {count} |
| LOC | ≤ 200 | {estimate} |
| Tests | ≥ 1 | {count} |

## NEXT STEP TRIGGER:

Proceed to step-03-code.md with plan ready for @implementer.
