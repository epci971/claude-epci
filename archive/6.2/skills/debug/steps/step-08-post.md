---
name: step-08-post
description: Post-debug memory storage and hooks
prev_step: null
next_step: null
---

# Step 08: Post-Debug

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip project-memory storage
- ✅ ALWAYS store bug pattern for future reference
- ✅ ALWAYS execute post-debug hook if configured
- ✅ ALWAYS suggest /commit if --commit flag
- 💭 FOCUS on capitalizing learnings for future debugging

## EXECUTION PROTOCOLS:

### 1. Store Bug Pattern (project-memory)

Store bug resolution for future reference:

```
project_memory.store_bug({
  id: "{generated-id}",
  description: "{bug description}",
  error_pattern: "{error message pattern}",
  root_cause: "{identified cause}",
  fix_summary: "{what was done}",
  keywords: ["{kw1}", "{kw2}", "{kw3}"],
  category: "{category}",
  files_affected: ["{path1}", "{path2}"],
  route: "{TRIVIAL | QUICK | COMPLEX}",
  duration_minutes: {N},
  timestamp: "{ISO-8601}"
})
```

**Bug Categories:**

| Category | Examples |
|----------|----------|
| `logic` | Wrong condition, incorrect calculation |
| `data` | Null handling, type mismatch |
| `config` | Environment, settings |
| `integration` | API, external service |
| `concurrency` | Race condition, deadlock |
| `security` | Auth, validation |
| `performance` | Memory leak, slow query |

### 2. Extract Keywords

Generate searchable keywords:

```
KEYWORD EXTRACTION:

From error:
- Error type: "TypeError", "NullPointerException"
- Error code: "SQLSTATE[23000]", "HTTP 500"
- Module: "CacheService", "AuthController"

From root cause:
- Concept: "race condition", "null reference"
- Component: "cache", "session", "auth"

From files:
- Domain: "user", "order", "payment"
- Layer: "service", "controller", "repository"
```

### 3. Execute Post-Debug Hook

If hook configured in `.epci/hooks/`:

```python
# hooks/post-debug.py
def on_post_debug(context):
    """
    context = {
      "mode": "TRIVIAL | QUICK | COMPLEX",
      "slug": "bug-id",
      "root_cause": "description",
      "files_modified": ["path1", "path2"],
      "duration_minutes": N,
      "tests_added": N
    }
    """
    # Custom actions: notify, log, track
```

### 4. --commit Flag Handling

If `--commit` flag provided:

```
COMMIT CONTEXT:

Write .epci-commit-context.json:
{
  "type": "fix",
  "scope": "{affected-module}",
  "description": "{bug fix description}",
  "files": ["{path1}", "{path2}"],
  "tests": ["{test_path}"],
  "breaking": false,
  "debug_report": "{report_path | null}"
}

Suggest: "Run /commit to commit this fix"
```

### 5. Generate Completion Summary

Final summary based on route:

#### TRIVIAL Summary
```
+---------------------------------------------------------------------+
| ✅ DEBUG COMPLETE (Trivial)                                            |
+---------------------------------------------------------------------+
| Bug: {short description}                                             |
| Cause: {root cause}                                                  |
| Fix: {file}:{line}                                                   |
| Duration: {N}s                                                       |
+---------------------------------------------------------------------+
```

#### QUICK Summary
```
+---------------------------------------------------------------------+
| ✅ DEBUG COMPLETE (Quick)                                              |
+---------------------------------------------------------------------+
| Bug: {short description}                                             |
| Root Cause: {cause}                                                  |
| Files Modified: {N}                                                  |
| Tests Added: {N}                                                     |
| Duration: {N}m                                                       |
|                                                                      |
| Pattern stored in project-memory for future reference.               |
+---------------------------------------------------------------------+
```

#### COMPLEX Summary
```
+---------------------------------------------------------------------+
| ✅ DEBUG COMPLETE (Complex)                                            |
+---------------------------------------------------------------------+
| Bug: {short description}                                             |
| Root Cause: {cause}                                                  |
| Solution: {selected solution}                                        |
| Files Modified: {N}                                                  |
| Tests Added: {N}                                                     |
| Duration: {N}m                                                       |
|                                                                      |
| Reviews:                                                             |
| - Code Review: {verdict}                                             |
| - Security Audit: {verdict | N/A}                                    |
| - QA Review: {verdict | N/A}                                         |
|                                                                      |
| Debug Report: docs/debug/{slug}-{date}.md                            |
| Pattern stored in project-memory for future reference.               |
+---------------------------------------------------------------------+
```

### 6. Suggest Next Actions

Based on outcome:

```
NEXT ACTIONS:

if --commit:
  "Run /commit to commit this fix"

if COMPLEX and not --no-report:
  "Debug report available: docs/debug/{slug}.md"

if related_improvement_found:
  "Consider /improve for {suggestion}"

if refactoring_recommended:
  "Consider /refactor for {area}"
```

## CONTEXT BOUNDARIES:

- This step expects: Completed fix from any route
- This step produces: Stored pattern, hook execution, completion summary

## OUTPUT FORMAT:

```
## Post-Debug Complete

### Memory Storage
- **Pattern stored**: Yes
- **Keywords**: {kw1}, {kw2}, {kw3}
- **Category**: {category}

### Hook Execution
- **post-debug hook**: {Executed | Not configured}

{if --commit}
### Commit Context
- **File created**: `.epci-commit-context.json`
- **Suggested**: Run `/commit` to commit this fix
{/if}

### Summary
{Route-specific summary box}

### Suggested Next Actions
{context-aware suggestions}
```

## COMPLETION:

Debug workflow complete. No further steps.
