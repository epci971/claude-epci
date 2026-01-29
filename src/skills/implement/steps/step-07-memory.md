---
name: step-07-memory
description: Update index.json with feature summary, modified files, and test count
prev_step: steps/step-06-finish.md
next_step: null
---

# Step 07: Memory

## Reference Files

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip index.json update
- 🔴 NEVER skip worktree finalization if enabled
- ✅ ALWAYS generate a concise summary (1-2 sentences)
- ✅ ALWAYS collect all modified files
- ✅ ALWAYS count tests added
- ✅ ALWAYS check worktree status before completion
- 💭 FOCUS on persistence and cleanup for future sessions

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

5. **Check** worktree status

IF state.worktree?.enabled == true:
  → Proceed to Worktree Finalization Breakpoint (section below)
ELSE:
  → Proceed to Completion Summary (normal flow)

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

AFFICHE cette boîte (info-only, pas d'interaction):


+------------------------------------------------------------------+
| [M] MEMORY PHASE COMPLETE                                        |
+------------------------------------------------------------------+
| Feature: {feature-slug}                                          |
|                                                                  |
| Summary: {summary}                                               |
|                                                                  |
| Modified Files: {files_count}                                    |
| Tests Added: {tests_count}                                       |
|                                                                  |
| index.json updated at:                                           |
| .claude/state/features/index.json                                |
+------------------------------------------------------------------+


Remplis les variables:
- `{feature-slug}`: Feature identifier
- `{summary}`: 1-2 sentence implementation summary
- `{files_count}`: Files modified count
- `{tests_count}`: Tests added count

**Note:** Info-only display, no AskUserQuestion needed.

## WORKTREE FINALIZATION BREAKPOINT (if worktree enabled):

IF state.worktree?.enabled == true AND state.worktree.status == "active":

First, check worktree status:

EXECUTE Bash({
  command: "./scripts/worktree-status.sh {feature-slug}",
  description: "Check worktree status for finalization"
})

AFFICHE cette boite:


┌─────────────────────────────────────────────────────────────────────┐
│ WORKTREE FINALIZATION                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Worktree: {worktree.path}                                           │
│ Branch: {worktree.branch}                                           │
│ Status: {clean/uncommitted changes}                                 │
│                                                                     │
│ Feature implementation is complete. Choose how to handle worktree:  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Finalize (Recommended) - Cleanup worktree, keep branch    │ │
│ │  [B] Keep worktree - Continue working in worktree              │ │
│ │  [C] Abandon - Cleanup worktree, delete branch                 │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘


APPELLE AskUserQuestion({
  questions: [{
    question: "Comment finaliser le worktree?",
    header: "Worktree",
    multiSelect: false,
    options: [
      { label: "Finalize (Recommended)", description: "Remove worktree, keep branch for PR" },
      { label: "Keep worktree", description: "Keep working in worktree" },
      { label: "Abandon", description: "Remove worktree and delete branch" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

### Handle Finalization Choice

**IF "Finalize" selected:**
1. Check for uncommitted changes (warn if present)
2. Execute: `./scripts/worktree-finalize.sh {feature-slug}`
3. Update state.worktree.status = "merged"
4. Change directory back to main repo
5. Log: "Worktree finalized. Branch {branch} ready for PR."

**IF "Keep worktree" selected:**
1. Keep state.worktree.status = "active"
2. Log: "Worktree kept at {path}. Remember to finalize later."

**IF "Abandon" selected:**
1. Execute: `./scripts/worktree-finalize.sh {feature-slug} --force --delete-branch`
2. Update state.worktree.status = "abandoned"
3. Log: "Worktree abandoned and cleaned up."

## NEXT STEP TRIGGER:

Workflow complete. No next step.

User may proceed with:
- `git commit` to commit changes
- `/commit` to use commit skill
- Create PR for review
