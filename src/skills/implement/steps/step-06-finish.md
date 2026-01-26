---
name: step-06-finish
description: Finalize implementation and generate summary
prev_step: steps/step-05-document.md
next_step: null
---

# Step 06: Finish

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip final validation
- :white_check_mark: ALWAYS verify all tests still passing
- :white_check_mark: ALWAYS verify all outputs generated
- :white_check_mark: ALWAYS present completion summary
- :white_check_mark: ALWAYS suggest next steps
- :thought_balloon: FOCUS on confirming successful completion

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
- Status: :white_check_mark: COMPLETED
- Complexity: {STANDARD|LARGE}
- Duration: {time}

### Deliverables
:white_check_mark: Implementation code
:white_check_mark: Unit tests ({coverage}%)
:white_check_mark: Integration tests
:white_check_mark: Feature Document
:white_check_mark: Documentation updates

### Files Summary
| Action | Count | Files |
|--------|-------|-------|
| Created | {N} | {list} |
| Modified | {N} | {list} |

### Test Summary
- Total tests: {N}
- All passing: :white_check_mark:
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
│ :white_check_mark: IMPLEMENTATION COMPLETE                                          │
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
│ :white_check_mark: [E] Explore                                                      │
│ :white_check_mark: [P] Plan                                                         │
│ :white_check_mark: [C] Code                                                         │
│ :white_check_mark: [I] Inspect                                                      │
│                                                                     │
│ Ready for commit and review.                                        │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

Workflow complete. No next step.

User may proceed with:
- `git commit` to commit changes
- `/commit` to use commit skill
- Create PR for review
