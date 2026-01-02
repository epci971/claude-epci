# YAML Rules - Frontmatter Syntax Validation

> Avoid common YAML errors that break skill loading

---

## Valid Frontmatter Structure

```yaml
---
name: skill-name-here
description: >-
  Your description here. Can span multiple lines
  when using the >- notation.
allowed-tools: Read, Grep, Glob
---
```

---

## Field Specifications

| Field | Required | Constraint | Example |
|-------|----------|------------|---------|
| `name` | Yes | Kebab-case, ≤64 chars, no spaces | `sql-analytics` |
| `description` | Yes | ≤1024 chars, explicit triggers | See formulas |
| `allowed-tools` | No | Comma-separated list | `Read, Grep, Glob` |

---

## Name Rules

### Valid Names
```yaml
name: sql-analytics
name: pdf-processor
name: code-review-python
name: excel-kpi-analyst
name: my-custom-skill-v2
```

### Invalid Names
```yaml
name: SQL Analytics      # spaces not allowed
name: pdf_processor      # underscores, prefer hyphens
name: CodeReviewPython   # no camelCase
name: this-is-a-very-long-skill-name-that-exceeds-the-sixty-four-character-limit  # too long
name: skill.name         # no dots
```

---

## Description Syntax

### Multi-line with `>-` (Recommended)
```yaml
description: >-
  This is a multi-line description that will be folded
  into a single line. Line breaks become spaces.
  Use this for long descriptions.
```

### Single line with quotes
```yaml
description: "Short description with special chars: colons, quotes"
```

### Common Errors

```yaml
# TABS instead of spaces
name:	my-skill    # TAB character = parse error

# Special characters without quotes
description: Use for: analysis, reports    # colon without quotes

# Unclosed frontmatter
---
name: test
# missing closing ---

# Wrong indentation
---
  name: my-skill    # unexpected indent

# Unquoted special chars
description: "Use for" analysis    # mismatched quotes
```

---

## Special Characters Handling

### Characters Requiring Quotes

| Character | Example | Solution |
|-----------|---------|----------|
| `:` | `Use for: analysis` | Wrap in quotes |
| `"` | `the "best" tool` | Use single quotes or escape |
| `'` | `user's files` | Use double quotes |
| `#` | `C# code` | Wrap in quotes |
| `@` | `@mentions` | Wrap in quotes |
| `&` | `R&D` | Wrap in quotes |
| `*` | `*.pdf files` | Wrap in quotes |
| `!` | `Important!` | Wrap in quotes |

### Safe Examples

```yaml
# Correct handling of special characters
description: "Use for: analysis, reports, and data extraction"
description: "Process user's files and generate reports"
description: "Review C# and Python code for issues"
description: "Handle R&D documentation and reports"
```

---

## Whitespace Rules

### Indentation
- Always use **2 spaces** for indentation
- **Never use tabs**
- Consistent indentation throughout

### Line Endings
- Use Unix line endings (`\n`)
- Avoid Windows line endings (`\r\n`)

### Trailing Spaces
- Remove trailing spaces
- Some parsers are sensitive to trailing whitespace

---

## Validation Methods

### Method 1: Quick Visual Check
```bash
# View first 10 lines
cat SKILL.md | head -n 10
```

### Method 2: Python Validation
```python
import yaml

with open('SKILL.md', 'r') as f:
    content = f.read()

# Extract frontmatter (between --- markers)
parts = content.split('---')
if len(parts) >= 3:
    frontmatter = parts[1]
    try:
        data = yaml.safe_load(frontmatter)
        print("Valid YAML")
        print(f"  name: {data.get('name')}")
        print(f"  description length: {len(data.get('description', ''))}")
    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
```

---

## Quick Reference Card

```
+-----------------------------------------------------------+
|                    YAML FRONTMATTER                       |
+-----------------------------------------------------------+
|  ---                         <- Opening delimiter         |
|  name: kebab-case-name       <- Required, <=64 chars      |
|  description: >-             <- Required, <=1024 chars    |
|    Multi-line description    <- 2-space indent            |
|    continues here.           <- No tabs, ever             |
|  allowed-tools: Read, Grep   <- Optional, Claude Code     |
|  ---                         <- Closing delimiter         |
+-----------------------------------------------------------+
```

---

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Skill not loading | Frontmatter not closed | Add `---` after frontmatter |
| Description truncated | >1024 chars | Use `>-` and condense |
| Parse error at line X | Special characters | Wrap in quotes |
| Name invalid | Spaces or uppercase | Use lowercase with hyphens |
