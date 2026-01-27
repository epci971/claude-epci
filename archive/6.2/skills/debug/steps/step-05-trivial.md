---
name: step-05-trivial
description: Route A - Direct fix for trivial bugs
prev_step: steps/step-04-routing.md
next_step: steps/step-08-post.md
---

# Step 05: Trivial Route

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER use this route if uncertainty > 5%
- 🔴 NEVER modify more than 1 file
- 🔴 NEVER write more than 10 LOC
- ✅ ALWAYS verify fix compiles/parses
- ✅ ALWAYS provide inline summary
- 💭 FOCUS on minimal, precise fix

## EXECUTION PROTOCOLS:

### 1. Verify Trivial Criteria

Re-confirm before applying:

```
TRIVIAL CHECKLIST:
[ ] Single, obvious cause
[ ] Fix is < 10 LOC
[ ] Single file
[ ] No complex dependencies
[ ] No test required (self-evident fix)
```

If any criterion fails, escalate to QUICK route.

### 2. Apply Direct Fix

Apply fix directly without TDD cycle:

```
FIX ACTIONS:
1. Read target file
2. Identify exact location (line from stack trace)
3. Apply minimal fix
4. Verify syntax (no parse errors)
```

**Common Trivial Fixes:**

| Bug Type | Fix Pattern |
|----------|-------------|
| Typo | Correct spelling |
| Missing import | Add import statement |
| Wrong literal | Replace string/number |
| Off-by-one | Adjust operator (<= vs <) |
| Null check | Add `if (x != null)` |
| Wrong variable | Replace with correct one |

### 3. Syntax Verification

Verify fix doesn't break parsing:

```bash
# JavaScript/TypeScript
npx tsc --noEmit {file}

# Python
python -m py_compile {file}

# PHP
php -l {file}

# Java (compilation check)
./gradlew compileJava
```

### 4. No Breakpoint

TRIVIAL route skips breakpoints for speed.

User is not asked for confirmation - fix is applied directly.

### 5. Generate Inline Summary

Output concise fix summary:

```
+-- BUG FIXED (Trivial) -------------------------+
| Cause: {cause description}                      |
| Fix: {what was changed}                         |
| File: {path}:{line}                             |
+-------------------------------------------------+
```

## CONTEXT BOUNDARIES:

- This step expects: TRIVIAL routing from step-04, single hypothesis
- This step produces: Applied fix with inline summary

## OUTPUT FORMAT:

```
## Bug Fixed (Trivial)

### Root Cause
{1-2 sentence description}

### Fix Applied
**File**: `{path}:{line}`

**Before**:
```{lang}
{old code}
```

**After**:
```{lang}
{new code}
```

### Verification
- Syntax check: ✅ Passed

### Summary
+-- BUG FIXED (Trivial) -------------------------+
| Cause: {cause}                                  |
| Fix: {description}                              |
| File: {path}:{line}                             |
+-------------------------------------------------+

Proceeding to post-debug phase.
```

## ESCALATION TRIGGER:

If fix is more complex than expected:

```
+---------------------------------------------------------------------+
| [ESCALATION] Fix More Complex Than Expected                          |
+---------------------------------------------------------------------+
| Expected: < 10 LOC, 1 file                                           |
| Actual: {N} LOC, {N} files                                           |
|                                                                      |
| Escalating to QUICK route for proper TDD cycle.                      |
+---------------------------------------------------------------------+
```

Proceed to step-06-quick.md instead.

## NEXT STEP TRIGGER:

Proceed to step-08-post.md when:
- Fix applied successfully
- Syntax verification passed
- Single file modified
- < 10 LOC changed
