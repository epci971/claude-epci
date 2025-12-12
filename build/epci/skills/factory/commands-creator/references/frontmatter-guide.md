# Frontmatter Guide - Command YAML Specification

> Complete reference for command frontmatter configuration

---

## Valid Frontmatter Structure

```yaml
---
description: >-
  Your command description here. Can span multiple lines
  when using the >- notation for readability.
argument-hint: [arg1] [arg2] [--flag]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---
```

---

## Field Specifications

| Field | Required | Constraint | Example |
|-------|----------|------------|---------|
| `description` | Yes | ≤500 chars, clear action | See patterns below |
| `argument-hint` | No | Shows usage pattern | `[target] [--verbose]` |
| `allowed-tools` | No | Comma-separated list | `Read, Write, Bash` |

---

## Description Rules

### Required Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Action** | What the command does | "Analyze code quality" |
| **Context** | When to use it | "for PR reviews" |
| **Result** | Expected outcome | "generates report" |

### Description Formula

```
[ACTION verb infinitive] + [CONTEXT/scope] + [RESULT/output]
```

### Good Examples ✅

```yaml
description: >-
  Analyze project architecture and generate dependency graph.
  Identifies circular dependencies and coupling issues.
  Use for architectural reviews and refactoring planning.
```

```yaml
description: >-
  Run comprehensive test suite with coverage reporting.
  Executes unit, integration, and E2E tests in sequence.
  Generates HTML coverage report in coverage/ directory.
```

### Bad Examples ❌

```yaml
# Too vague
description: Does stuff with code

# Missing context
description: Runs tests

# Too long (>500 chars)
description: >-
  This command does many things including analyzing code,
  running tests, generating reports, checking dependencies,
  validating configurations, and much more...
  [continues for 600+ characters]
```

---

## Argument-Hint Patterns

### Syntax Convention

| Pattern | Meaning | Example |
|---------|---------|---------|
| `[arg]` | Optional positional | `[target]` |
| `<arg>` | Required positional | `<file>` |
| `--flag` | Boolean flag | `--verbose` |
| `--option=value` | Option with value | `--format=json` |

### Common Patterns

```yaml
# Simple command
argument-hint: [target]

# With flags
argument-hint: [target] [--verbose] [--dry-run]

# Multiple arguments
argument-hint: <source> <destination> [--force]

# Complex command
argument-hint: <action> [target] [--format=json|yaml] [--output=path]
```

---

## Allowed-Tools Reference

### Available Tools

| Tool | Capability | Risk Level |
|------|------------|------------|
| `Read` | Read files | Low |
| `Write` | Create/overwrite files | Medium |
| `Edit` | Modify files | Medium |
| `Bash` | Execute shell commands | High |
| `Grep` | Search file contents | Low |
| `Glob` | Find files by pattern | Low |
| `Task` | Invoke subagents | Medium |
| `WebFetch` | HTTP requests | Medium |
| `TodoRead` | Read task list | Low |
| `TodoWrite` | Modify task list | Low |

### Least Privilege Principle

```yaml
# Analysis command (read-only)
allowed-tools: Read, Grep, Glob

# Documentation generator
allowed-tools: Read, Write, Glob

# Full development command
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task

# Testing command
allowed-tools: Read, Bash, Grep, Glob
```

### Tool Combinations by Command Type

| Command Type | Recommended Tools |
|--------------|-------------------|
| Analysis | Read, Grep, Glob |
| Generation | Read, Write, Glob |
| Modification | Read, Edit, Grep, Glob |
| Build/Test | Read, Bash, Grep, Glob |
| Orchestration | Read, Task, Glob |
| Full workflow | All tools |

---

## YAML Syntax Rules

### Multi-line Descriptions

```yaml
# Folded style (recommended)
description: >-
  First line continues here.
  Second line also continues.
  All becomes one paragraph.

# Literal style (preserves newlines)
description: |
  Line 1
  Line 2
  Line 3
```

### Special Characters

| Character | Handling |
|-----------|----------|
| `:` | Wrap value in quotes |
| `"` | Use single quotes or escape |
| `'` | Use double quotes |
| `#` | Wrap in quotes |

### Common Errors

```yaml
# Missing closing delimiter
---
description: Something
# ← missing ---

# Tabs instead of spaces
description:	Something  # ← TAB character

# Unquoted special characters
description: Use for: analysis  # ← colon needs quotes
```

---

## Validation Checklist

- [ ] Frontmatter enclosed by `---` delimiters
- [ ] Description present and clear
- [ ] Description ≤500 characters
- [ ] Action verb in infinitive form
- [ ] Argument-hint matches actual usage
- [ ] Allowed-tools follows least privilege
- [ ] No YAML syntax errors (tabs, special chars)
- [ ] No hardcoded paths or secrets

---

## Quick Reference

```
+-----------------------------------------------------------+
|                    COMMAND FRONTMATTER                     |
+-----------------------------------------------------------+
|  ---                                                       |
|  description: >-                 <- Required, ≤500 chars   |
|    Action verb + context + result                          |
|  argument-hint: [args] [--flags] <- Optional, shows usage  |
|  allowed-tools: Read, Write...   <- Optional, restricts    |
|  ---                                                       |
+-----------------------------------------------------------+
```
