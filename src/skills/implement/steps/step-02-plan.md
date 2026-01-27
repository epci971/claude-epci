---
name: step-02-plan
description: Create implementation plan phase [P]
prev_step: steps/step-01-explore.md
next_step: steps/step-03-code.md
---

# Step 02: Plan [P]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER start coding before plan approval
- 🔴 NEVER create plan without exploration data
- 🔴 NEVER skip test strategy definition
- ✅ ALWAYS define implementation order
- ✅ ALWAYS specify test approach for each component
- ✅ ALWAYS get user approval via breakpoint
- 🔵 YOU ARE AN ARCHITECT designing the build sequence
- 💭 FOCUS on testability and incremental progress

## EXECUTION PROTOCOLS:

### 1. Synthesize Exploration Findings

- Review identified patterns
- Review dependencies
- Review files to modify/create

### 2. Invoke @planner (Sonnet)

Delegate task decomposition to the planner agent:

```typescript
Task({
  subagent_type: "planner",
  prompt: `
## Feature
{feature_name}

## Requirements
{requirements_from_exploration}

## Identified Files
{files_to_modify_create}

## Constraints
{identified_constraints}

## Output Format
Atomic tasks (2-15 min each) with dependencies, ordered by implementation sequence.
Include test strategy for each task.
  `
})
```

### 3. Validate Plan with @plan-validator (Opus)

```typescript
Task({
  subagent_type: "plan-validator",
  prompt: `
## Plan to Validate
{plan_from_planner}

## Feature Requirements
{original_requirements}

## Validation Checklist
- Completeness: All requirements covered
- Consistency: No circular dependencies
- Feasibility: Resources available
- Quality: Tasks atomic and testable (TDD strategy defined)

## Expected Output
APPROVED or NEEDS_REVISION with specific feedback
  `
})
```

**Handle Result:**
- If APPROVED: continue to breakpoint
- If NEEDS_REVISION: apply feedback and re-invoke @planner

### 4. Update Feature Document

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
@skill:epci:breakpoint-system
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
