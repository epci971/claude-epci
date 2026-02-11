---
name: step-07-output-auto
description: Final JSON output write and stdout summary
prev_step: steps/step-06-finish-auto.md
next_step: steps/step-08-publish-auto.md
---

# Step 07: Output (Auto)

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- ALWAYS write final JSON output
- ALWAYS print stdout summary for pipeline logging
- ALWAYS ensure JSON is valid and parseable

## EXECUTION PROTOCOLS:

### 1. Finalize JSON Output

Write the complete final JSON to `.implement-auto-output.json`:

- `phases.current` = null (execution complete)
- `phases.completed` includes all completed phases
- `timestamp` = current ISO-8601
- All metrics finalized
- All errors and warnings collected

Ensure the write is atomic (write complete content, not incremental).

### 2. Print Stdout Summary

Output a concise summary for pipeline logging:

```
[implement-auto] Execution complete
  Status: {status}
  Feature: {feature-slug}
  Branch: feature/{feature-slug}
  Components: {success}/{total} ({skipped} skipped, {failed} failed)
  Tests: {tests_passing} passing, {tests_failing} failing
  Files: {files_created} created, {files_modified} modified
  Feature Doc: {feature_doc_path}
  JSON Output: {json_output_path}
  Exit Reason: {exit_reason or "none"}
```

### 3. Early Termination Output

If this step is reached via early termination (circuit breaker, validation failure):

Ensure JSON reflects the failure state:
- `status` = "FAILED"
- `exit_reason` = specific reason
- `phases.failed` includes the failed phase
- `phases.current` = null
- `errors[]` contains details of the failure

### 4. Handoff to Publish

The worktree, branch, and JSON output are preserved for step-08-publish-auto.
Step-08 handles: push to origin, PR creation, optional auto-merge, and worktree cleanup.

## CONTEXT BOUNDARIES:

- This step expects: Final status, all metrics, all errors/warnings
- This step produces: Final JSON file, stdout summary

## NEXT STEP TRIGGER:

Proceed to step-08-publish-auto.md for branch push, PR creation, and worktree cleanup.
If --skip-publish flag is set, step-08 will skip all post-processing.
