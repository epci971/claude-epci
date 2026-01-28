---
name: step-05-memory
description: Update index.json with feature summary, modified files, and test count
prev_step: steps/step-04-document.md
next_step: null
---

# Step 05: Memory [M]

## Reference Files

@../references/breakpoint-formats.md

| Reference | Purpose |
|-----------|---------|
| breakpoint-formats.md | Completion summary display (section #complete) |

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip index.json update
- ✅ ALWAYS generate a concise summary (1-2 sentences)
- ✅ ALWAYS collect all modified files
- ✅ ALWAYS count tests added
- ✅ ALWAYS present completion breakpoint
- 💭 FOCUS on persistence for future sessions

## EXECUTION PROTOCOLS:

### 1. Generate Summary

Write 1-2 sentences describing what was done:

```
SUMMARY RULES:
├── Max 200 characters
├── Focus on "what" and "why"
├── Use action verbs (Fixed, Added, Updated)
└── Be specific, not generic
```

**Good examples:**
- "Fixed login button alignment using flexbox centering"
- "Added email validation with regex pattern for standard format"
- "Updated user avatar component to support lazy loading"

**Bad examples:**
- "Made some changes" (too vague)
- "Fixed the thing" (not specific)
- "Implemented feature as requested" (no information)

### 2. Collect Modified Files

List all files created or modified during implementation:

```python
modified_files = [
    "src/components/LoginButton.tsx",
    "src/components/LoginButton.test.tsx"
]
```

**Include:**
- Source files modified
- Test files created/modified
- Config files if changed

**Exclude:**
- Lock files (package-lock.json, etc.)
- Build artifacts

### 3. Count Tests Added

Count new test cases/functions:

```python
def count_new_tests(test_files: list) -> int:
    """Count new test cases added."""
    count = 0
    for file in test_files:
        # Count it() or test() calls added
        # Count def test_* functions added
        count += count_test_functions(file)
    return count
```

### 4. Update index.json

Path: `.claude/state/features/index.json`

Use `state-manager` to update:

```json
{
  "id": "{feature-slug}",
  "status": "completed",
  "current_phase": "memory",
  "complexity": "{TINY|SMALL}",
  "branch": "{current-branch}",
  "created_at": "{start-time}",
  "last_update": "{now}",
  "created_by": "/quick",
  "summary": "{1-2 sentence summary}",
  "modified_files": ["{path1}", "{path2}"],
  "test_count": {N}
}
```

### 5. Present Completion Summary

AFFICHE la boîte Complete (section #complete du fichier breakpoint-formats.md importé ci-dessus).

**Note:** Info-only display, no user interaction required.

## CONTEXT BOUNDARIES:

- This step expects: Implementation complete, all files finalized
- This step produces: Updated index.json, completion summary
- This is the final step

## INDEX.JSON EXAMPLE:

```json
{
  "version": "1.0",
  "last_update": "2026-01-26T15:30:00Z",
  "features": [
    {
      "id": "fix-login-button",
      "status": "completed",
      "current_phase": "memory",
      "complexity": "TINY",
      "branch": "main",
      "created_at": "2026-01-26T15:28:00Z",
      "last_update": "2026-01-26T15:30:00Z",
      "created_by": "/quick",
      "summary": "Fixed login button alignment using flexbox centering",
      "modified_files": [
        "src/components/LoginButton.tsx",
        "src/components/LoginButton.test.tsx"
      ],
      "test_count": 2
    }
  ]
}
```

## NEXT STEP TRIGGER:

Workflow complete. No next step.

User may proceed with:
- `git commit` to commit changes
- `/commit` to use commit skill
- Create PR for review
