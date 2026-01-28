---
name: step-06-finish
description: Finalize implementation and generate summary
prev_step: steps/step-05-document.md
next_step: steps/step-07-memory.md
---

# Step 06: Finish

## Reference Files

@../references/breakpoint-formats.md
@../references/output-templates.md

| Reference | Purpose |
|-----------|---------|
| output-templates.md | Completion output format (section #finish-output) |
| breakpoint-formats.md | Completion summary box (section #finish) |

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
   - Feature Document complete
   - Related docs updated

3. **Update** state-manager
   - Mark feature as COMPLETED
   - Record completion time
   - Record final metrics

4. **Generate** completion summary
   - Files created/modified
   - Test coverage
   - Key decisions made
   - Any known limitations

5. **Suggest** next steps
   - Commit preparation
   - PR creation
   - Deployment considerations

## CONTEXT BOUNDARIES:

- This step expects: All previous steps completed, documentation done
- This step produces: Final summary, completion confirmation

## OUTPUT FORMAT:

APPLY template from output-templates.md (section #finish-output importé ci-dessus).

## COMPLETION SUMMARY:

AFFICHE la boîte Finish (section #finish du fichier breakpoint-formats.md importé ci-dessus).

**Note:** Info-only display, no user interaction required.

## NEXT STEP TRIGGER:

Proceed to **step-07-memory** to update index.json with feature summary.
