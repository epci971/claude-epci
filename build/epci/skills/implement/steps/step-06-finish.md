---
name: step-06-finish
description: Finalize implementation and generate summary
prev_step: steps/step-05-document.md
next_step: steps/step-07-memory.md
---

# Step 06: Finish

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

```
## Implementation Complete

### Feature: {feature-slug}
- Status: ✅ COMPLETED
- Complexity: {STANDARD|LARGE}
- Duration: {time}

### Deliverables
✅ Implementation code
✅ Unit tests ({coverage}%)
✅ Integration tests
✅ Feature Document
✅ Documentation updates

### Files Summary
| Action | Count | Files |
|--------|-------|-------|
| Created | {N} | {list} |
| Modified | {N} | {list} |

### Test Summary
- Total tests: {N}
- All passing: ✅
- Coverage: {%}

### Key Decisions
- {decision 1}
- {decision 2}

### Known Limitations
- {limitation 1 if any}

### Next Steps
1. Review changes: `git diff`
2. Stage files: `git add {files}`
3. Commit: `git commit -m "feat({scope}): {description}"`
4. Create PR (if applicable)
```

## COMPLETION SUMMARY:

┌─────────────────────────────────────────────────────────────────────┐
│ ✅ IMPLEMENTATION COMPLETE                                          │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│                                                                     │
│ Summary:                                                            │
│ • {N} files created                                                 │
│ • {N} files modified                                                │
│ • {N} tests added ({coverage}% coverage)                            │
│ • Documentation complete                                            │
│                                                                     │
│ EPCI Phases Completed:                                              │
│ ✅ [E] Explore                                                      │
│ ✅ [P] Plan                                                         │
│ ✅ [C] Code                                                         │
│ ✅ [I] Inspect                                                      │
│                                                                     │
│ Ready for commit and review.                                        │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

Proceed to **step-07-memory** to update index.json with feature summary.
