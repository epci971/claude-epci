# Gold Standard Examples — Annotated Commands

> 3 exemplary EPCI commands with rule compliance annotations

---

## Overview

These commands demonstrate best practices for EPCI command structure.
Each example is annotated to highlight compliance with specific rules.

**Selection Criteria**:
- High audit score (>90/100)
- Clear structure and organization
- Proper integration patterns
- Real production usage

---

## Example 1: `/commit` — Modal Command Pattern

**File**: `src/commands/commit.md`
**Score**: 95/100
**Pattern**: Dual-mode (context-rich / degraded)

### Annotated Frontmatter

```yaml
---
description: >-                                           # ✅ FM-001: Present
  Unified Git commit command for EPCI workflows.          # ✅ FM-004: Starts with noun (ok for tooling)
  Centralizes commit logic for /epci, /quick, and /debug. # ✅ FM-003: ~180 chars
  Supports context-rich mode (via JSON) and standalone
  mode (degraded). Follows Conventional Commits format.
argument-hint: "[--auto-commit] [--amend] [--no-hooks] [--dry-run]"  # ✅ FM-006, FM-007: Format correct
allowed-tools: [Read, Write, Bash, Glob]                  # ✅ FM-009: All valid tools
---                                                       # ✅ FM-001: Closed
```

**Rule Compliance**:
| Rule | Status | Note |
|------|--------|------|
| FM-001 | ✅ | Frontmatter present and closed |
| FM-002 | ✅ | Description present |
| FM-003 | ✅ | ~180 chars (under 500) |
| FM-006 | ✅ | argument-hint matches usage |
| FM-007 | ✅ | `[optional]` and `--flag` format |
| FM-009 | ✅ | All tools in VALID_TOOLS |
| FM-010 | ⚠️ | Bash not pattern-restricted |

### Annotated Structure

```markdown
# EPCI Commit — Unified Git Commit                        # ✅ Title with context

## Overview                                               # ✅ ST-001: Present

Centralized commit command that:                          # ✅ ST-002: 4 bullets, concise
- Handles commits for `/epci`, `/quick`, and `/debug`
- Works standalone for manual commits
- Follows Conventional Commits format
- Integrates with EPCI hooks system

## Modes                                                  # ✅ Clear mode documentation

| Mode | Condition | Behavior |                           # ✅ RD-004: Table format
|------|-----------|----------|
| **Context-rich** | `.epci-commit-context.json` | Uses context |
| **Degraded** | No context file | Asks for input |

## Arguments                                              # ✅ ST-006: Present (matches hint)

| Flag | Effect | Default |                              # ✅ ST-007: Table format
|------|--------|---------|
| `--auto-commit` | Skip breakpoint | Off |
| `--amend` | Amend last commit | Off |

## Configuration                                          # ✅ ST-008: Skills documented

| Element | Value |
|---------|-------|
| **Thinking** | `think` (default) |
| **Skills** | git-workflow |                             # ✅ IN-001: Documented
| **Subagents** | None |                                  # ✅ IN-002: Explicitly none

## Context File Schema                                    # ✅ IN-012: Schema documented

```json
{
  "source": "epci|quick|debug",
  "type": "feat|fix|refactor|...",
  ...
}
```

## Process                                                # ✅ ST-003: Present

### Step 1: Detect Mode                                   # ✅ ST-004: Numbered steps

Check for context file:
```bash                                                   # ✅ RD-003: Language specified
if [ -f ".epci-commit-context.json" ]; then
  # Context-rich mode
fi
```

### Step 2a: Context-Rich Mode                            # ✅ WF-005: Both branches
### Step 2b: Degraded Mode                                #    documented (2a/2b)
...
```

**Why It's Excellent**:
1. **Clear dual-mode pattern** — Documents both paths explicitly
2. **Schema documentation** — Context file format fully specified
3. **Flag documentation** — Each flag has table entry with default
4. **Conditional logic** — Uses `IF` and explicit conditions

---

## Example 2: `/rules` — Multi-Action Command Pattern

**File**: `src/commands/rules.md`
**Score**: 92/100
**Pattern**: Multiple actions (init, add, validate)

### Annotated Frontmatter

```yaml
---
description: >-
  Generate .claude/rules/ structure for a project.        # ✅ FM-004: Imperative verb
  Performs 3-level detection (stack, architecture,
  conventions), generates CLAUDE.md and contextual
  rules, then validates via @rules-validator.
  Also supports incremental rule addition via
  auto-detection or --add flag.
argument-hint: "[--force] [--validate-only] [--dry-run] [--stack <name>] [--add] [\"rule text\"]"
allowed-tools: [Read, Write, Glob, Grep, Bash, Task]     # ✅ FM-009: Valid tools
---
```

**Rule Compliance**:
| Rule | Status | Note |
|------|--------|------|
| FM-001 | ✅ | Present and valid |
| FM-002 | ✅ | Description present |
| FM-003 | ⚠️ | ~350 chars (acceptable) |
| FM-007 | ✅ | Mix of `[opt]`, `<req>`, `--flag` |
| FM-009 | ✅ | All valid including Task |

### Key Structural Patterns

```markdown
## Configuration

| Element       | Value                                     |
| ------------- | ----------------------------------------- |
| **Thinking**  | `think` / `think hard` (complex monorepo) | # ✅ IN-006: Thinking documented
| **Skills**    | rules-generator, project-memory, [stack]  | # ✅ IN-001: Skills listed
| **Subagents** | @Explore, @rules-validator, @rule-clarifier | # ✅ IN-002: Subagents with names

## Arguments                                              # ✅ ST-006: Matches hint

| Argument          | Description                         |
| ----------------- | ----------------------------------- |
| `--force`         | Overwrite existing .claude/         |
| `--validate-only` | Only validate, no generation        |
| `--dry-run`       | Preview without writing             |
| `--stack <name>`  | Force stack detection               | # ✅ FM-007: <required> format
| `--add`           | Force incremental mode              |

## Process

### Step 0: Input Classification & Routing                # ✅ WF-007: Decision point

1. **Parse input and flags**
   - If `--add` flag → **Mode ADD**                       # ✅ RD-009: Explicit IF
   - If explicit flags → **Mode GENERATE**
   - Else → Classify input text

2. **Auto-detect rule input**

   | Indicator | Score |                                   # ✅ RD-004: Table for scoring
   |-----------|-------|
   | "always", "never" | +0.2 each |
   | Structure [context] + [action] | +0.2 |

   **Routing**:                                           # ✅ IN-007: Routing documented
   - Score >= 0.7 → **Mode ADD**
   - Score 0.4-0.7 → Ask confirmation
   - Score < 0.4 → **Mode GENERATE**
```

**Why It's Excellent**:
1. **Multi-mode routing** — Step 0 explicitly routes to different paths
2. **Scoring algorithm** — Quantitative decision making
3. **Reference delegation** — Complex details in `references/`
4. **Subagent integration** — Clear `@agent` documentation

---

## Example 3: `/brief` — Entry Point Command Pattern

**File**: `src/commands/brief.md`
**Score**: 90/100
**Pattern**: Complex multi-step with breakpoints

### Key Excellence Indicators

```markdown
## Configuration                                          # ✅ Comprehensive config

| Element       | Value                                   |
| ------------- | --------------------------------------- |
| **Thinking**  | `think hard` (default) / `ultrathink`   | # ✅ IN-006
| **Skills**    | project-memory, epci-core, architecture | # ✅ IN-001
| **Subagents** | @Explore (thorough), @clarifier (turbo) | # ✅ IN-002

### --turbo Mode (MANDATORY Instructions)                 # ✅ Conditional mode docs

**When `--turbo` flag is active, you MUST:**              # ✅ RD-008: Imperative
1. **Use @clarifier (Haiku)** for fast clarification
2. **Use @Explore with Haiku model** for faster analysis
3. **Maximum 2 clarification questions**
4. **Auto-accept suggestions** if confidence > 0.7
```

### Breakpoint Excellence

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│ 📝 VALIDATION DU BRIEF                                              │  # ✅ ST-018: ASCII box
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📄 BRIEF ORIGINAL                                                   │
│ "{raw_brief}"                                                       │
│                                                                     │
│ [If reformulated:]                                                  │  # ✅ Conditional content
│ 📊 DÉTECTION                                                        │
│ ├── Artefacts vocaux: {COUNT} trouvés                              │
│ ├── Type détecté: {FEATURE|PROBLEM|DECISION}                       │
│ └── Reformulation: OUI                                             │
│                                                                     │
│ ✨ BRIEF REFORMULÉ                                                  │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ **Objectif**: {goal}                                            │ │  # ✅ RD-013: {placeholders}
│ │ **Contexte**: {context}                                         │ │
│ │ **Contraintes**: {constraints}                                  │ │
│ │ **Critères de succès**: {success_criteria}                      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ OPTIONS:                                                            │
│   [1] Valider → Continuer vers l'exploration                       │  # ✅ WF-007: Decision point
│   [2] Modifier → Je reformule moi-même                             │
│   [3] Annuler → Arrêter le workflow                                │
└─────────────────────────────────────────────────────────────────────┘
```

**Breakpoint Analysis**:
| Rule | Status | Note |
|------|--------|------|
| ST-018 | ✅ | Perfect ASCII box format |
| WF-006 | ✅ | Marked as MANDATORY |
| WF-007 | ✅ | User decision point |
| RD-013 | ✅ | `{placeholders}` used |
| RD-017 | ✅ | Emojis only in headers |

### Step Documentation Excellence

```markdown
### Step 1: Reformulation + Validation (MANDATORY BREAKPOINT)  # ✅ WF-006

#### Pre-step: Input Clarification (Conditional)          # ✅ Conditional step

**Skill**: `input-clarifier`                              # ✅ IN-001: Skill reference

```
IF --no-clarify flag:                                     # ✅ RD-009: Explicit IF
   → Skip clarification, proceed to reformulation

ELSE:
   → Calculate clarity score
   → IF score < 0.6: Show reformulation prompt
   → Use cleaned input for subsequent reformulation
```

#### SKIP CONDITIONS (rares)                              # ✅ WF-005: All cases

| Condition | How to detect | Action |                   # ✅ RD-004: Table format
|-----------|---------------|--------|
| Flag `--no-rephrase` | User explicit | SKIP |
| Already structured | Headers present | SKIP |

#### TRIGGER CONDITIONS                                   # ✅ Complete decision tree
```

**Why It's Excellent**:
1. **Comprehensive breakpoints** — ASCII box with all elements
2. **Conditional steps** — Clear pre-step and skip conditions
3. **Complete decision trees** — All paths documented
4. **MANDATORY markers** — Critical steps clearly marked

---

## Anti-Pattern Examples

### Bad Example 1: Missing Frontmatter

```markdown
# My Command                                              # ❌ FM-001: No frontmatter

This command does stuff.

## How to Use

Just run it and it works.
```

**Issues**:
- FM-001: No frontmatter
- FM-002: No description
- ST-001: Missing Overview
- ST-003: Missing Process
- RD-022: Vague purpose

---

### Bad Example 2: Poor Structure

```yaml
---
description: A helper command
---
```

```markdown
# Helper                                                  # ❌ Vague title

It helps with things. You can use it when you need
help with various tasks. It's really useful.             # ❌ ST-002: Too vague

The command works by doing stuff and then more stuff
happens and eventually you get results. Sometimes        # ❌ No numbered steps
it might fail but that's okay.                           # ❌ WF-008: No error handling
```

**Issues**:
- FM-003: Description too short/vague
- FM-004: No action verb
- ST-002: Overview > 4 sentences, vague
- ST-003: No Process section
- ST-004: No numbered steps
- WF-004: No explicit exit points

---

### Bad Example 3: Integration Failures

```yaml
---
description: Process files using the analyzer
allowed-tools: Read, Grep
---
```

```markdown
## Process

Use the analyzer skill to process files.                 # ❌ IN-001: Skill not documented
Delegate to @file-processor for heavy lifting.           # ❌ IN-002: Subagent not documented

After processing:
- Save results to /home/user/output/                     # ❌ RD-012: Hardcoded path
- Run the hook                                           # ❌ IN-003: Hook not documented

Output goes somewhere.                                   # ❌ IN-009: Output not documented
```

**Issues**:
- IN-001: Skills used but not documented
- IN-002: Subagent referenced but not documented
- IN-003: Hook mentioned but not specified
- IN-009: Output path vague
- RD-012: Absolute path hardcoded

---

## Compliance Checklist

Use this checklist when creating new commands:

### Frontmatter
- [ ] `---` delimiters present (FM-001)
- [ ] `description` field with action verb (FM-002, FM-004)
- [ ] `argument-hint` if args used (FM-006, FM-007)
- [ ] `allowed-tools` with valid tools (FM-009)
- [ ] Bash patterns restricted (FM-010)

### Structure
- [ ] `## Overview` with 2-4 sentences (ST-001, ST-002)
- [ ] `## Process` with numbered steps (ST-003, ST-004)
- [ ] `## Arguments` if argument-hint present (ST-006)
- [ ] Breakpoints in ASCII box format (ST-018)
- [ ] Total < 500 lines (ST-012)

### Content
- [ ] No hardcoded paths (RD-012)
- [ ] `@file` syntax for references (RD-005)
- [ ] `@agent` format for subagents (RD-007)
- [ ] No TODO/FIXME markers (RD-015)
- [ ] < 5000 tokens total (RD-001)

### Workflow
- [ ] All paths lead to exit (WF-004)
- [ ] IF/ELSE branches complete (WF-005)
- [ ] MANDATORY markers on critical steps (WF-006)
- [ ] No infinite loops (WF-003)

### Integration
- [ ] Skills documented in Configuration (IN-001)
- [ ] Subagents documented with conditions (IN-002)
- [ ] Output paths explicit (IN-009)
- [ ] Error handling documented (IN-010)

---

*Gold Standard Examples v1.0.0 — Command Auditor*
