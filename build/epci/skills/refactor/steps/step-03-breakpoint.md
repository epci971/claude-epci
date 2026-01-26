# Step 03: Breakpoint

> User validates the refactoring plan before execution.

## Trigger

- Previous step: `step-02-planning.md` completed

## Inputs

| Input | Source |
|-------|--------|
| Transformation plan | From step-02 |
| Impact estimate | From step-02 |
| Mikado graph (optional) | From step-02 |

## Protocol

### 1. Display Plan Summary and Request Approval

Present the complete plan using breakpoint-system:

```typescript
@skill:epci:breakpoint-system
  type: plan-review
  title: "Refactoring Plan Validation"
  data: {
    metrics: {
      complexity: "{scope}",
      complexity_score: {transformations_count},
      files_impacted: {files_count},
      time_estimate: "{estimate}",
      risk_level: "{LOW|MEDIUM|HIGH}",
      risk_description: "{highest risk transformation}"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "{transformations_count} transformations defined",
        consistency: "Dependency order validated",
        feasibility: "All transformations atomic",
        quality: "TDD strategy per transformation"
      }
    },
    skills_loaded: ["tdd-enforcer"],
    preview_next: {
      tasks: [
        {title: "T1: {transformation_1_title}", time: "{estimate}"},
        {title: "T2: {transformation_2_title}", time: "{estimate}"},
        {title: "T3: {transformation_3_title}", time: "{estimate}"}
      ],
      remaining_tasks: {transformations_count}
    },
    feature_doc_path: "{target_file}"
  }
  ask: {
    question: "Proceed with refactoring plan?",
    header: "Plan Review",
    options: [
      {label: "Execute (Recommended)", description: "Proceed with TDD-enforced transformations"},
      {label: "Modify Plan", description: "Adjust transformations or order"},
      {label: "Cancel", description: "Abort refactoring"}
    ]
  }
  suggestions: [
    {pattern: "baseline", text: "Run tests first to ensure baseline is green", priority: "P1"},
    {pattern: "risk", text: "{highest_risk_transformation} could be split into smaller steps", priority: "P2"},
    {pattern: "atomic", text: "Use --atomic flag for easier rollback", priority: "P3"}
  ]
```

### 2. Expected Metrics Delta (displayed in breakpoint)

Include in the plan-review data:
- LOC: {before} → {after} ({delta}%)
- CC (Cyclomatic Complexity): {before} → {after} ({delta}%)
- MI (Maintainability Index): {before} → {after} ({delta}%)

### 3. Handle Response

| Response | Action |
|----------|--------|
| Execute | → `step-04-execute.md` |
| Modify Plan | → Allow user to adjust, return to step-02 |
| Cancel | → Abort with summary of analysis done |

### 4. If --dry-run Flag

Skip execution, generate report:

```
## Dry Run Complete

Plan generated but not executed (--dry-run flag).

### To execute this plan:
/refactor src/services/auth.py --scope module

### Plan exported to:
.claude/refactor-plans/auth-refactor-{timestamp}.md
```

## Outputs

| Output | Destination |
|--------|-------------|
| User decision | Workflow routing |
| Plan export (dry-run) | File system |

## Next Step

| Decision | Next Step |
|----------|-----------|
| Execute | → `step-04-execute.md` |
| Modify | → `step-02-planning.md` (revise) |
| Cancel | → Exit with analysis summary |
| --dry-run | → Exit with plan export |

## Error Handling

| Error | Resolution |
|-------|------------|
| User timeout | Remind and wait |
| Ambiguous response | Clarify options |
