---
name: step-06-finish
description: Finalize implementation and generate summary
prev_step: steps/step-05-document.md
next_step: steps/step-07-memory.md
---

# Step 06: Finish

## Reference Files

@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| output-templates.md | Completion output format (section #finish-output) |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip final validation
- ✅ ALWAYS verify all tests still passing
- ✅ ALWAYS verify all outputs generated
- ✅ ALWAYS present completion summary
- ✅ ALWAYS suggest next steps
- 💭 FOCUS on confirming successful completion

## EXECUTION PROTOCOLS:

1. **Verify** all tests passing
   - Run full test suite
   - Confirm coverage target met
   - No regressions

2. **Verify** all outputs exist
   - Implementation code complete
   - Tests in place
   - Feature Document complete (docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md)
   - Related docs updated

3. **Verify** Feature Document completeness

Path: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md` (from `artifacts.feature_doc`)

Check that the Feature Document contains all sections:
- §0 Metadata: slug, complexity, date filled
- §1 Contexte: objective and criteria present
- §2 Plan: tasks table filled (not placeholder)
- §3 Implementation: components table filled
- §4 Revue: review verdicts present
- §5 Finalisation: summary and files list present

IF any section still contains placeholder text ("*En attente de..."):
  WARN: "Feature Document incomplete - section {X} not filled"
  Attempt to fill from available data

Update §0 Status from IN_PROGRESS to COMPLETED:

EXECUTE Edit({
  file_path: "{feature_doc_path}",
  old_string: "| Status | IN_PROGRESS |",
  new_string: "| Status | COMPLETED |"
})

4. **Update** state-manager
   - Mark feature as COMPLETED
   - Record completion time
   - Record final metrics

5. **Generate** completion summary
   - Files created/modified
   - Test coverage
   - Key decisions made
   - Any known limitations

6. **Suggest** next steps
   - Commit preparation
   - PR creation
   - Deployment considerations

## CONTEXT BOUNDARIES:

- This step expects: All previous steps completed, documentation done
- This step produces: Final summary, completion confirmation

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #finish-output importé ci-dessus).

## COMPLETION SUMMARY:

AFFICHE cette boîte (info-only, pas d'interaction):

```
┌─────────────────────────────────────────────────────────────────────┐
│ IMPLEMENTATION COMPLETE                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Summary:                                                            │
│ - {files_created} files created                                     │
│ - {files_modified} files modified                                   │
│ - {tests_added} tests added ({coverage}% coverage)                  │
│ - Documentation complete                                            │
│                                                                     │
│ EPCI Phases Completed:                                              │
│ [E] Explore                                                         │
│ [P] Plan                                                            │
│ [C] Code                                                            │
│ [I] Inspect                                                         │
│                                                                     │
│ Ready for commit and review.                                        │
└─────────────────────────────────────────────────────────────────────┘
```

Remplis les variables:
- `{feature-slug}`: Feature identifier
- `{files_created}`: New files count
- `{files_modified}`: Modified files count
- `{tests_added}`: New tests count
- `{coverage}`: Final coverage percentage

**Note:** Info-only display, no AskUserQuestion needed.

## NEXT STEP TRIGGER:

Proceed to **step-07-memory** to update index.json with feature summary.
