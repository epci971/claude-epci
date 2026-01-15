---
description: >-
  Diagnose and fix bugs using structured workflow with adaptive routing.
  Uses thought tree analysis, solution scoring, and automatic research (web + MCP).
  Routes to Trivial/Quick/Complet mode based on complexity.
argument-hint: "[error message | stack trace] [--full] [--turbo] [--no-report] [--c7] [--seq] [--no-clarify]"
allowed-tools: [Read, Glob, Grep, Bash, Task, WebFetch, WebSearch, Write, Edit]
---

# EPCI Debug — Structured Bug Resolution

## Overview

Diagnose and fix bugs systematically with:
- Root cause analysis (thought tree)
- Automatic research (Context7 MCP + web search)
- Solution scoring for complex bugs
- Adaptive routing (Trivial → Quick → Complet)

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `error` | Error message, stack trace, or bug description | Required |

## Flags

| Flag | Effect |
|------|--------|
| `--full` | Force Complet mode (skip routing) |
| `--turbo` | Speed mode: Haiku diagnostic, auto-apply best solution, skip breakpoint |
| `--no-report` | Complet mode without Debug Report file |
| `--context <path>` | Link to existing Feature Document |
| `--commit` | Generate commit context after fix, suggest /commit |
| `--no-clarify` | Skip input clarification (even if input is confusing) |
| `--force-clarify` | Force input clarification (even if input is clear) |

### --turbo Mode

**Comparison: Standard vs Turbo**

| Aspect | Standard | Turbo |
|--------|----------|-------|
| Diagnostic model | Sonnet | **@clarifier (Haiku)** |
| Thought tree | Full | Simplified/Skip |
| Solution selection | Multiple + scoring | Best only (auto-apply) |
| Breakpoint | Required (Complet) | Skipped |
| Confidence threshold | N/A | 70% (fallback if lower) |
| Report | Full Debug Report | Summary only |

**Turbo Agent Invocation:**

```
Task: Launch @clarifier agent for Phase 1 diagnostic
subagent_type: epci:clarifier
model: haiku
prompt: "Analyze this error and identify the most likely root cause with confidence %: [error]"
```

**Turbo Process:** `Error → @clarifier → Best Solution → Auto-Apply → Verify → Done`

**Fallback:** If @clarifier confidence < 70%, switch to standard mode automatically.

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (Quick), `think hard` (Complet) |
| **Skills** | project-memory, debugging-strategy, mcp, [stack-skill] |
| **Subagents** | @code-reviewer (Complet mode), @security-auditor (if security bug) |
| **MCP** | Context7 (error docs), Sequential (multi-step reasoning) |

> **Note**: Bash non restreint car /debug nécessite l'exécution de commandes variées (tests, git, build tools) pour le diagnostic.

## Pre-Workflow: Load Context

**Skill**: `project-memory`

Load project context from `.project-memory/` if exists.
Load `debugging-strategy` skill for methodology.

**🪝 Execute `pre-debug` hooks** (if configured)

---

## Process

**⚠️ IMPORTANT: Follow ALL steps. Routing happens automatically after Phase 1.**

### Step 0: Input Clarification (Conditional)

**Skill**: `input-clarifier`

Clarify error description if confusing (dictated input with hesitations, fillers, etc.).

**Note**: Stack traces and technical error messages are excluded from scoring — only the descriptive part is evaluated.

```
IF --no-clarify flag:
   → Skip to Phase 1

IF input contains only technical content (stack trace, error code):
   → Skip to Phase 1 (score = 1.0)

ELSE:
   → Calculate clarity score
   → IF score < 0.6: Show reformulation prompt
   → IF score >= 0.6: Continue to Phase 1
```

**Example trigger:**
```
Input: "euh le truc là il marche plus, enfin le bouton quoi"
Score: 0.35 → Clarification triggered

⚠️ Input confus détecté

Original: "euh le truc là il marche plus, enfin le bouton quoi"
Reformulation: "Le bouton ne fonctionne plus"

[1] ✅ Utiliser   [2] ✏️ Modifier   [3] ➡️ Garder
```

---

### Phase 1: Diagnostic (MANDATORY)

**⚠️ DO NOT SKIP:** Complete diagnosis before any fix attempt.

#### Step 1.1: Gather Evidence

Collect available information:

```markdown
## Evidence Gathered

**Error**: [Error message or description]

**Stack Trace** (if available):
```
[stack trace]
```

**Reproduction**:
- Steps: [How to reproduce]
- Frequency: [Always / Sometimes / Rare]

**Recent Changes**:
- [Relevant commits or changes]
```

#### Step 1.2: Research

**Context7 MCP** (if available):
- Query library documentation for error patterns
- Check known issues for detected versions

**Fallback**: If Context7 unavailable, display warning and continue:
```
⚠️ Context7 MCP not configured. Using web search only.
```

**Web Search**:
- Search: `[error message] [framework] site:stackoverflow.com`
- Search: `[error message] [framework] site:github.com/issues`
- Filter: Results < 2 years, prioritize official docs

#### Step 1.3: Build Thought Tree

**⚠️ MANDATORY:** Generate root cause analysis.

```
🔍 ROOT CAUSE ANALYSIS
├── 🎯 Primary (XX%): [Most likely cause]
│   └── Evidence: [Supporting observations]
├── 🔸 Secondary (XX%): [Second possibility]
│   └── Evidence: [Supporting observations]
└── 🔹 Tertiary (XX%): [Third possibility]
    └── Evidence: [Supporting observations]
```

**Exception**: Skip thought tree for trivial bugs (typo, missing import).

#### Step 1.4: Evaluate Routing

Apply thresholds:

| Criterion | Trivial | Quick | Complet |
|-----------|---------|-------|---------|
| Causes | 1 (obvious) | 1 | 2+ |
| Est. LOC | < 10 | < 50 | >= 50 |
| Files | 1 | 1-2 | 3+ |
| Risk | None | Low | Medium+ |
| Uncertainty | < 5% | < 20% | >= 20% |

**Rule**: >= 2 Complet criteria → Complet mode

**Routing Decision**: Evaluate against thresholds above

**🪝 Execute `post-diagnostic` hooks** (if configured)

---

### Route A: Trivial Mode

**Trigger**: Obvious cause (typo, missing import, syntax error)

**Process**:
1. Apply fix directly
2. Output inline summary

**Output**:
```
✅ BUG FIXED (Trivial)

Cause: [What was wrong]
Fix: [What was changed]
File: [path/to/file.ext:line]

No further action needed.
```

**End workflow.**

---

### Route B: Quick Mode

**Trigger**: Single cause, < 50 LOC, low risk, < 20% uncertainty

**Process**:
1. Display thought tree (simplified)
2. Propose solution
3. **Write test(s) for the fix** (TDD approach)
4. Implement fix
5. Run verification (tests must pass)

**Output**:
```
✅ BUG FIXED (Quick)

🔍 Root Cause
[Primary cause with evidence]

💡 Solution Applied
[Description of fix]

📁 Files Modified
- path/to/file.ext (lines X-Y)

✓ Verification
[Test result or manual verification]
```

**End workflow.**

---

### Route C: Complet Mode

**Trigger**: ≥ 2 Complet criteria OR `--full` flag

#### Step C.1: Solution Scoring

Generate multiple solutions with scores:

```
💡 SOLUTIONS PROPOSÉES
┌─────────────────────────────────────────────────────────────────┐
│ #1 [Solution A] — Score: XX/100                                 │
├─────────────────────────────────────────────────────────────────┤
│ Simplicity: XX | Risk: XX | Time: XX | Maintainability: XX      │
│ Justification: [Key factors]                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ #2 [Solution B] — Score: XX/100                                 │
├─────────────────────────────────────────────────────────────────┤
│ Simplicity: XX | Risk: XX | Time: XX | Maintainability: XX      │
│ Justification: [Key factors]                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Step C.2: BREAKPOINT (MANDATORY)

**⚠️ MANDATORY:** Wait for user confirmation.

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — Diagnostic Complete                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 🔍 ROOT CAUSE ANALYSIS                                              │
│ ├── 🎯 Primary (XX%): [Cause]                                      │
│ ├── 🔸 Secondary (XX%): [Cause]                                    │
│ └── 🔹 Tertiary (XX%): [Cause]                                     │
│                                                                     │
│ 💡 RECOMMENDED SOLUTION                                             │
│ ├── [Solution #1] — Score: XX/100                                  │
│ ├── Est. LOC: XX                                                   │
│ ├── Files: X                                                       │
│ └── Risk: [Level]                                                  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Continuer" → Implémenter solution #1                    │
│   • Tapez "Solution 2" → Choisir solution alternative              │
│   • Tapez "Détails" → Voir analyse complète                        │
│   • Tapez "Annuler" → Abandonner                                   │
└─────────────────────────────────────────────────────────────────────┘
```

#### Step C.3: Implement Fix

1. Apply chosen solution
2. Run tests
3. Invoke @code-reviewer

**Conditional agents**:

- **@security-auditor** if:
  - Files match: `**/auth/**`, `**/security/**`, `**/api/**`
  - Keywords: `password`, `secret`, `jwt`, `oauth`

- **@qa-reviewer** if:
  - Test files created or modified
  - >= 3 test cases added

#### Step C.4: Generate Debug Report (USE WRITE TOOL)

**⚠️ MANDATORY** (unless `--no-report`): Create `docs/debug/<slug>-<date>.md`

```markdown
# Debug Report — [Title]

> **Date**: [YYYY-MM-DD]
> **Mode**: Complet
> **Duration**: [Time spent]

## Problem

[Description of the bug, how it manifested]

## Evidence

- **Error**: [Error message]
- **Stack trace**: [If applicable]
- **Reproduction**: [Steps]

## Root Cause Analysis

[Thought tree]

## Solutions Evaluated

| Solution | Score | Chosen |
|----------|-------|--------|
| [Solution A] | XX/100 | ✓ |
| [Solution B] | XX/100 | |

## Implementation

### Files Modified
| File | Action | Lines |
|------|--------|-------|
| [path] | Modify | X-Y |

### Changes
```diff
[Key changes]
```

## Verification

- **Tests**: [Pass/Fail]
- **@code-reviewer**: [Verdict]
- **@security-auditor**: [Verdict if applicable]

## Lessons Learned

[What to watch for in future]
```

**🪝 Execute `post-debug` hooks** (if configured)

---

## Output

### If --commit flag active

**Generate commit context before displaying completion:**

```json
{
  "source": "debug",
  "type": "fix",
  "scope": "<detected module from bug location>",
  "description": "<bug fix description>",
  "files": ["<list of modified files>"],
  "featureDoc": null,
  "breaking": false,
  "ticket": null
}
```

**Write to `.epci-commit-context.json`** at project root.

### Trivial/Quick
```
✅ **DEBUG COMPLETE**

Mode: [Trivial | Quick]
Cause: [Root cause]
Fix: [Summary]
{If --commit: 📝 Contexte commit préparé → /commit}
```

### Complet
```
✅ **DEBUG COMPLETE**

Mode: Complet
Debug Report: docs/debug/<slug>-<date>.md

Reviews:
- @code-reviewer: [Verdict]
- @security-auditor: [Verdict or N/A]

{If --commit: 📝 Contexte commit préparé → /commit}
Next: Verify fix in production environment
```

---

## Memory Integration

**Execute `post-debug-complete` hooks** for history tracking:

```bash
python3 src/hooks/runner.py post-debug --context '{
  "mode": "<Trivial|Quick|Complet>",
  "bug_slug": "<slug>",
  "root_cause": "<primary cause>",
  "files_modified": ["<files>"],
  "resolution_time": "<duration>"
}'
```

**Effects**:
- Saves debug session to `.project-memory/history/debug/`
- Updates bug resolution metrics
- Enables pattern detection for recurring issues

---

## Examples

### Example 1: Trivial Bug

```
Input: "TypeError: Cannot read property 'name' of undefined"

→ Trivial Mode (obvious null reference)

✅ BUG FIXED (Trivial)
Cause: Missing null check before accessing user.name
Fix: Added optional chaining: user?.name
File: src/components/Profile.tsx:42
```

### Example 2: Quick Bug

```
Input: "API returns 500 on user registration"

→ Quick Mode (single cause, low complexity)

🔍 Root Cause
Primary (85%): Email validation regex rejects valid emails with + character
Evidence: Stack trace shows ValidationError at line 78

💡 Solution Applied
Updated regex to RFC 5322 compliant pattern

📁 Files Modified
- src/validators/email.ts (lines 78-79)
```

### Example 3: Complet Bug

```
Input: "Intermittent authentication failures in production"

→ Complet Mode (multiple causes, high risk)

[Full thought tree, solution scoring, breakpoint, Debug Report]
```

---

## Skills Loaded

- `project-memory` (context)
- `debugging-strategy` (methodology)
- `mcp` (Context7 for error docs, Sequential for reasoning)
- `[stack-skill]` (auto-detected: php-symfony, javascript-react, python-django, java-springboot)

## Differences with Other Workflows

| Aspect | /debug | /epci | /brainstorm |
|--------|-------------|-------|-------------|
| Trigger | Bug/error | Feature | Uncertainty/Discovery |
| Output | Fix + Report | Feature Doc | Brief/Spike Report |
| Thought tree | Yes | No | No |
| Scoring | Complet only | No | No |
| Routing | Adaptive | Fixed | Fixed |
