# YAML Frontmatter Rules

Complete reference for skill frontmatter syntax.

## Structure

```yaml
---
name: skill-name
description: >-
  Multi-line description
  that continues here.
field: value
---

# Markdown content starts here
```

## Required Syntax

### Delimiters

- Must start with `---` on first line
- Must end frontmatter with `---`
- No content before first `---`

```yaml
# ✅ CORRECT
---
name: my-skill
---

# ❌ INCORRECT (missing delimiter)
name: my-skill
---

# ❌ INCORRECT (wrong delimiter)
~~~
name: my-skill
~~~
```

### Field Format

```yaml
field: value
field-name: value     # hyphens OK
field_name: value     # underscores OK (but prefer hyphens)
```

## Multi-line Strings

### Folded Style (>-)

Newlines become spaces, trailing newline stripped:

```yaml
description: >-
  This is a long description
  that spans multiple lines
  but renders as one paragraph.
```

**Renders as**: `This is a long description that spans multiple lines but renders as one paragraph.`

### Literal Style (|)

Preserves newlines:

```yaml
description: |
  Line one.
  Line two.
  Line three.
```

**Renders as**:
```
Line one.
Line two.
Line three.
```

### When to Use

| Style | Use Case |
|-------|----------|
| `>-` | Descriptions (recommended) |
| `|` | Code blocks, formatted text |
| `""` | Short, single-line values |

---

## Field Reference

### name

```yaml
name: my-skill-name
```

**Rules**:
- Lowercase only
- Hyphens allowed
- Max 64 characters
- No spaces or special characters
- Must be unique across project

**Examples**:
- ✅ `code-review`
- ✅ `api-generator`
- ❌ `Code Review` (spaces, caps)
- ❌ `code_review` (underscore - works but not recommended)

### description

```yaml
description: >-
  What this skill does. When to use it.
  Trigger words: keyword1, keyword2.
```

**Rules**:
- Max 1024 characters
- Use `>-` for multi-line
- Include trigger words
- Be specific, not vague

### user-invocable

```yaml
user-invocable: true   # Shows in / menu (default)
user-invocable: false  # Hidden, only Claude can invoke
```

### disable-model-invocation

```yaml
disable-model-invocation: false  # Claude can auto-invoke (default)
disable-model-invocation: true   # Only user can invoke
```

### argument-hint

```yaml
argument-hint: "[filename]"           # Single arg
argument-hint: "[source] [target]"    # Multiple args
argument-hint: "[pr-number]"          # Descriptive
```

### allowed-tools

```yaml
# List format
allowed-tools: Read, Write, Edit, Glob, Grep

# Restricted Bash
allowed-tools: Read, Bash(git:*)

# Full list
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
```

**Available tools**:
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Bash` - Execute commands
- `Bash(pattern:*)` - Restricted commands
- `AskUserQuestion` - User interaction

### model

```yaml
model: sonnet    # Default, balanced
model: haiku     # Fast, simple tasks
model: opus      # Complex reasoning
```

### context

```yaml
context: fork    # Run in isolated subagent
```

### agent

```yaml
agent: Explore        # Read-only exploration
agent: Plan           # Planning tasks
agent: general-purpose  # Full capabilities (default)
```

---

## Common Patterns

### User Skill (Standard)

```yaml
---
name: my-skill
description: >-
  What it does. Use when: scenario.
  Triggers: keyword1, keyword2.
user-invocable: true
disable-model-invocation: false
argument-hint: "[arg]"
allowed-tools: Read, Write, Edit
---
```

### Core Skill (Internal)

```yaml
---
name: my-component
description: >-
  Internal component description.
  Use when: condition. Not for: direct use.
user-invocable: false
disable-model-invocation: false
allowed-tools: Read, Glob
---
```

### Exploration Skill

```yaml
---
name: deep-research
description: >-
  Deep codebase exploration.
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep
---
```

### Interactive Skill

```yaml
---
name: guided-setup
description: >-
  Interactive setup wizard.
allowed-tools: Read, Write, AskUserQuestion
---
```

---

## Validation

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Parse error | Missing `---` | Add delimiters |
| Unknown field | Typo in field name | Check spelling |
| Invalid value | Wrong type | Check expected type |
| Description too long | Over 1024 chars | Shorten description |

### Validation Commands

```bash
# Check YAML syntax
head -20 SKILL.md | grep -A20 "^---" | head -n -1

# Check description length
grep -A10 "description:" SKILL.md | head -10 | wc -c

# Verify required fields
grep -E "^(name|description):" SKILL.md
```

---

## Examples

### Minimal Valid

```yaml
---
name: simple-skill
description: Does one thing well.
---
```

### Full Featured

```yaml
---
name: comprehensive-skill
description: >-
  Comprehensive skill with all features.
  Handles multiple scenarios with smart defaults.
  Use when: complex task, multi-step process.
  Triggers: comprehensive, full, complete.
  Not for: simple one-off tasks.
user-invocable: true
disable-model-invocation: false
argument-hint: "[target] [--flag]"
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
model: sonnet
---
```
