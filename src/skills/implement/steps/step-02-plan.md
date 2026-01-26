---
name: step-02-plan
description: Create implementation plan phase [P]
prev_step: steps/step-01-explore.md
next_step: steps/step-03-code.md
---

# Step 02: Plan [P]

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER start coding before plan approval
- :red_circle: NEVER create plan without exploration data
- :red_circle: NEVER skip test strategy definition
- :white_check_mark: ALWAYS define implementation order
- :white_check_mark: ALWAYS specify test approach for each component
- :white_check_mark: ALWAYS get user approval via breakpoint
- :large_blue_circle: YOU ARE AN ARCHITECT designing the build sequence
- :thought_balloon: FOCUS on testability and incremental progress

## EXECUTION PROTOCOLS:

1. **Synthesize** exploration findings
   - Review identified patterns
   - Review dependencies
   - Review files to modify/create

2. **Define** implementation order
   - Start with foundation components
   - Build dependent components in order
   - End with integration points

3. **Specify** test strategy
   - Unit tests for each component
   - Integration tests for interactions
   - Coverage targets (min 70%)

4. **Create** implementation plan
   - Numbered steps with clear scope
   - TDD approach for each step
   - Expected outputs per step

5. **Update** Feature Document
   - Add implementation plan section
   - Add test strategy section
   - Add acceptance criteria mapping

## CONTEXT BOUNDARIES:

- This step expects: Exploration findings, dependency map
- This step produces: Implementation plan, test strategy, updated Feature Document

## OUTPUT FORMAT:

```
## Implementation Plan

### Phase 1: Foundation
1. {Component} — {description}
   - Test: {test approach}
   - Files: {files to modify/create}

### Phase 2: Core Logic
2. {Component} — {description}
   - Test: {test approach}
   - Files: {files}

### Phase 3: Integration
3. {Component} — {description}
   - Test: {test approach}
   - Files: {files}

### Test Strategy
- Unit tests: {approach}
- Integration tests: {approach}
- Coverage target: {%}

### Acceptance Criteria Mapping
| Criteria | Component | Test |
|----------|-----------|------|
| {AC1} | {component} | {test} |
```

## BREAKPOINT:

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — Plan Validation                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Implementation Plan:                                                │
│ • {N} phases, {N} components                                        │
│ • Estimated: ~{loc} LOC                                             │
│ • Test coverage target: {%}                                         │
│                                                                     │
│ ┌─ Plan Summary ─────────────────────────────────────────────────┐ │
│ │ 1. {Phase 1 summary}                                           │ │
│ │ 2. {Phase 2 summary}                                           │ │
│ │ 3. {Phase 3 summary}                                           │ │
│ └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Approve and proceed to coding (Recommended)                │ │
│ │  2. Modify plan (specify changes)                              │ │
│ │  3. Request more detail on specific phase                      │ │
│ │  4. Abort and revise requirements                              │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When plan is approved by user, proceed to `step-03-code.md`.
