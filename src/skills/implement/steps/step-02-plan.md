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

```typescript
@skill:breakpoint-system
  type: plan-review
  title: "Plan Validation"
  data: {
    metrics: {
      complexity: "{complexity}",
      complexity_score: {score},
      files_impacted: {N},
      time_estimate: "{hours}h",
      risk_level: "{LOW|MEDIUM|HIGH}",
      risk_description: "{risk notes}"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "{phases} phases defined",
        consistency: "Dependencies mapped",
        feasibility: "Within scope",
        quality: "TDD strategy defined"
      }
    },
    skills_loaded: ["tdd-enforcer", "state-manager"],
    preview_next: {
      tasks: [
        {title: "{Phase 1 summary}", time: "{estimate}"},
        {title: "{Phase 2 summary}", time: "{estimate}"},
        {title: "{Phase 3 summary}", time: "{estimate}"}
      ],
      remaining_tasks: {N}
    },
    feature_doc_path: ".epci/features/{feature-slug}/FEATURE.md"
  }
  ask: {
    question: "Approve implementation plan?",
    header: "Plan Review",
    options: [
      {label: "Approve and Code (Recommended)", description: "Proceed to TDD implementation"},
      {label: "Modify Plan", description: "Adjust phases or approach"},
      {label: "Abort", description: "Revise requirements first"}
    ]
  }
  suggestions: [
    {pattern: "tdd", text: "TDD cycle enforced: RED → GREEN → REFACTOR", priority: "P1"},
    {pattern: "coverage", text: "Coverage target: {%}%", priority: "P2"}
  ]
```

## NEXT STEP TRIGGER:

When plan is approved by user, proceed to `step-03-code.md`.
