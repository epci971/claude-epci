---
name: subagents-creator
description: >-
  Guided creation of new Claude Code subagents. Workflow with templates,
  validation and least privilege principle. Use when: /epci:create agent
  invoked. Not for: skills or commands, native Claude Code subagents.
---

# Subagents Creator

## Overview

Guides new subagent creation with automatic validation.
Focus on least privilege principle and single mission.

## Key Concepts

### What is a subagent?

A subagent is a specialized agent with:
- **Single mission** — One well-defined objective
- **Restricted tools** — Minimum necessary
- **Adapted model** — Haiku (fast) or Sonnet (complex)
- **Output format** — Structured and predictable

### Native vs Custom Subagents

| Type | Examples | Usage |
|------|----------|-------|
| **Native** | @Explore, @Plan | Provided by Claude Code |
| **Custom** | @code-reviewer, @security-auditor | Created by EPCI |

## Workflow

### Phase 1: Qualification

Questions to define the subagent:

1. **Mission**: What is the single task?
2. **Invocation**: When is it called?
3. **Input**: What does it receive?
4. **Output**: What does it produce?
5. **Tools**: What tools does it need?

### Phase 2: Frontmatter Definition

```yaml
---
name: [kebab-case]
description: >-
  [Mission in 1-2 sentences]. [When it's invoked].
  [What it produces as output].
model: claude-sonnet-4-20250514  # or haiku for simple tasks
allowed-tools: [Read, Grep]  # MINIMUM NECESSARY
---
```

### Phase 3: Content Structure

```markdown
# [Name] Agent

## Mission
[Clear description of single mission]

## Invocation Conditions
[When this subagent is called]

## Checklist
### [Category 1]
- [ ] Criterion 1
- [ ] Criterion 2

### [Category 2]
- [ ] Criterion 3

## Severity Levels
| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | ... | Must fix |
| 🟠 Important | ... | Should fix |
| 🟡 Minor | ... | Nice to have |

## Output Format
```markdown
## [Output Report Title]

### Summary
[...]

### Findings
[...]

### Verdict
**[APPROVED | NEEDS_FIXES | ...]**
```
```

### Phase 4: Validation

```bash
python src/scripts/validate_subagent.py src/agents/[name].md
```

**Criteria:**
- [ ] .md file exists
- [ ] Valid YAML frontmatter
- [ ] Kebab-case name ≤ 64 chars
- [ ] Clear description
- [ ] Restrictive tools (least privilege principle)
- [ ] Focused content (< 2000 tokens)

## Least Privilege Principle

### Tools by Mission Type

| Mission | Recommended Tools |
|---------|-------------------|
| Reading/Analysis | `Read`, `Grep`, `Glob` |
| Validation | `Read`, `Grep` |
| Generation | `Read`, `Write` |
| Execution | `Read`, `Bash` |

### ⚠️ Tools to Avoid Unless Necessary

- `Write` — Avoid if subagent doesn't need to create files
- `Edit` — Avoid if subagent doesn't modify files
- `Bash` — Avoid if no command execution needed

## Template

```markdown
---
name: [name]
description: >-
  [Clear single mission]. [Invocation context].
  [Output produced].
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep]
---

# [Name] Agent

## Mission

[Single mission description in 2-3 sentences.
What the subagent does and why.]

## Invocation Conditions

Automatically invoked if:
- [Condition 1]
- [Condition 2]

OR manually invoked by:
- [Command/context]

## Expected Input

- [Input 1] — [Description]
- [Input 2] — [Description]

## Checklist

### [Category 1]
- [ ] Verifiable criterion 1
- [ ] Verifiable criterion 2
- [ ] Verifiable criterion 3

### [Category 2]
- [ ] Verifiable criterion 4
- [ ] Verifiable criterion 5

## Severity Levels

| Level | Criteria | Required Action |
|-------|----------|-----------------|
| 🔴 Critical | [Definition] | Must fix |
| 🟠 Important | [Definition] | Should fix |
| 🟡 Minor | [Definition] | Nice to have |

## Output Format

```markdown
## [Report Title]

### Summary
[1-2 sentences summarizing result]

### [Main Section]
[Structured details]

### Issues (if applicable)

#### 🔴 Critical
1. **[Title]**
   - **Location**: [file:line]
   - **Issue**: [Description]
   - **Fix**: [Suggested solution]

### Verdict
**[APPROVED | NEEDS_FIXES | REJECTED]**

**Reasoning:** [Technical justification]
```

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

## Best Practices

### Mission

| Do | Avoid |
|----|-------|
| Single mission | Multi-task |
| Action verb | Vague description |
| Limited scope | "Check everything" |

### Tools

| Do | Avoid |
|----|-------|
| Minimum necessary | All tools |
| Read-only if possible | Write without reason |
| Justify each tool | Copy from other agents |

### Output

| Do | Avoid |
|----|-------|
| Structured format | Free text |
| Clear verdicts | Ambiguity |
| Evidence/locations | Claims without proof |

## Output

```markdown
✅ **SUBAGENT CREATED**

Agent: [name]
File: src/agents/[name].md

Validation: ✅ PASSED (5/5 checks)
- Mission: Single and clear
- Tools: Restrictive (X tools)
- Content: < 2000 tokens

Next steps:
1. Customize the checklist
2. Define severity levels
3. Test with real cases
```
