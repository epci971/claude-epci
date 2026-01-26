---
name: step-07-memory
description: Update index.json with feature summary, modified files, and test count
prev_step: steps/step-06-finish.md
next_step: null
---

# Step 07: Memory

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip index.json update
- :white_check_mark: ALWAYS generate a concise summary (1-2 sentences)
- :white_check_mark: ALWAYS collect all modified files
- :white_check_mark: ALWAYS count tests added
- :thought_balloon: FOCUS on persistence for future sessions

## EXECUTION PROTOCOLS:

1. **Generate** summary
   - Write 1-2 sentences describing what was done
   - Max 200 characters
   - Focus on the "what" and "why"
   - Example: "Added OAuth2 Google authentication with refresh token support"

2. **Collect** modified files
   - List all files created or modified
   - Get from artifacts.modified_files in state.json
   - Include source files and test files

3. **Count** tests added
   - Count new test cases/functions
   - Include unit + integration tests

4. **Update** index.json
   - Path: `.claude/state/features/index.json`
   - Add/update feature entry with new fields
   - Use state-manager skill for persistence

## CONTEXT BOUNDARIES:

- This step expects: Implementation complete, all files finalized
- This step produces: Updated index.json with summary, files, test count

## INDEX.JSON UPDATE FORMAT:

```json
{
  "id": "{feature-slug}",
  "status": "completed",
  "current_phase": "inspect",
  "complexity": "{TINY|SMALL|STANDARD|LARGE}",
  "branch": "feature/{feature-slug}",
  "created_at": "{ISO-8601}",
  "last_update": "{ISO-8601}",
  "summary": "{1-2 sentence summary, max 200 chars}",
  "modified_files": ["{path1}", "{path2}"],
  "test_count": {N}
}
```

## EXAMPLE:

For an OAuth feature:

```json
{
  "id": "auth-oauth-google",
  "status": "completed",
  "current_phase": "inspect",
  "complexity": "STANDARD",
  "branch": "feature/auth-oauth-google",
  "created_at": "2026-01-20T10:00:00Z",
  "last_update": "2026-01-22T14:30:00Z",
  "summary": "OAuth2 Google authentication with refresh token and session persistence",
  "modified_files": [
    "src/auth/oauth.ts",
    "src/auth/types.ts",
    "src/auth/session.ts",
    "tests/auth/oauth.test.ts"
  ],
  "test_count": 8
}
```

## COMPLETION SUMMARY:

```
+------------------------------------------------------------------+
| [M] MEMORY PHASE COMPLETE                                        |
+------------------------------------------------------------------+
| Feature: {feature-slug}                                          |
|                                                                  |
| Summary: {1-2 sentence summary}                                  |
|                                                                  |
| Modified Files: {count}                                          |
| Tests Added: {count}                                             |
|                                                                  |
| index.json updated at:                                           |
| .claude/state/features/index.json                                |
+------------------------------------------------------------------+
```

## NEXT STEP TRIGGER:

Workflow complete. No next step.

User may proceed with:
- `git commit` to commit changes
- `/commit` to use commit skill
- Create PR for review
