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
| `name` | ✅ Yes | Kebab-case, ≤64 chars, no spaces | `sql-analytics` |
| `description` | ✅ Yes | ≤1024 chars, explicit triggers | See formulas |
| `allowed-tools` | ❌ No | Comma-separated list | `Read, Grep, Glob` |
| `license` | ❌ No | License information | `MIT` |

---

## Name Rules

### ✅ Valid Names
```yaml
name: sql-analytics
name: pdf-processor
name: code-review-python
name: excel-kpi-analyst
name: my-custom-skill-v2
```

### ❌ Invalid Names
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

### ❌ Common Errors

```yaml
# ❌ TABS instead of spaces
name:	my-skill    # TAB character = parse error

# ❌ Special characters without quotes
description: Use for: analysis, reports    # colon without quotes

# ❌ Unclosed frontmatter
---
name: test
# missing closing ---

# ❌ Wrong indentation
---
  name: my-skill    # unexpected indent

# ❌ Unquoted special chars
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
# ✅ Correct handling of special characters
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
        print("✅ Valid YAML")
        print(f"  name: {data.get('name')}")
        print(f"  description length: {len(data.get('description', ''))}")
    except yaml.YAMLError as e:
        print(f"❌ YAML Error: {e}")
```

### Method 3: Online Validators
- [YAML Lint](https://www.yamllint.com/)
- [YAML Validator](https://yamlvalidator.com/)

---

## Complete Valid Example

```yaml
---
name: sql-analytics
description: >-
  Comprehensive SQL analysis toolkit for ACME's data warehouse. 
  Query revenue metrics, ARR calculations, customer segmentation, 
  and sales pipeline data. Provides table schemas, required filters 
  (exclude test accounts, complete periods only), and metric definitions. 
  Use when analyzing business data, building reports, or querying 
  financial metrics. Not for raw event logs or system monitoring data.
allowed-tools: Read, Grep, Glob
---

# SQL Analytics

## Overview
...
```

---

## Troubleshooting

### "Skill not loading"
1. Check frontmatter is properly closed with `---`
2. Verify no tabs in file
3. Validate YAML syntax
4. Check file encoding (UTF-8)

### "Description truncated"
1. Check length ≤1024 chars
2. Use `>-` for multi-line
3. Remove unnecessary whitespace

### "Parse error at line X"
1. Look for special characters on that line
2. Check indentation
3. Verify quote matching

### "Name invalid"
1. Use only lowercase letters
2. Use hyphens, not underscores or spaces
3. Keep under 64 characters

---

## Quick Reference Card

```
╔═══════════════════════════════════════════════════════════╗
║                    YAML FRONTMATTER                       ║
╠═══════════════════════════════════════════════════════════╣
║  ---                         ← Opening delimiter          ║
║  name: kebab-case-name       ← Required, ≤64 chars        ║
║  description: >-             ← Required, ≤1024 chars      ║
║    Multi-line description    ← 2-space indent             ║
║    continues here.           ← No tabs, ever              ║
║  allowed-tools: Read, Grep   ← Optional, Claude Code only ║
║  ---                         ← Closing delimiter          ║
╚═══════════════════════════════════════════════════════════╝
```
