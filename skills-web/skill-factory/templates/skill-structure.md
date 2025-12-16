# Skill Structure Template

> Reference for skill folder organization and SKILL.md structure

---

## Folder Structures by Complexity

### Simple Skill (Single Purpose)

```
skill-name/
└── SKILL.md                    # Everything in one file
```

**Use when**: Single workflow, no external references needed, <100 lines

---

### Standard Skill (Most Common)

```
skill-name/
├── SKILL.md                    # Main file (<5000 tokens)
└── references/
    ├── main-reference.md       # Primary documentation
    └── edge-cases.md           # Known quirks and exceptions
```

**Use when**: Single or few workflows, needs reference documentation

---

### Advanced Skill (Full Package)

```
skill-name/
├── SKILL.md                    # Entry point + workflow
├── references/
│   ├── schemas.md              # Data schemas
│   ├── api-reference.md        # API documentation
│   ├── rules.md                # Business rules
│   └── edge-cases.md           # Edge cases
├── scripts/
│   ├── validate.py             # Validation script
│   ├── helper.sh               # Utility script
│   └── test_triggering.py      # Triggering tests
└── templates/
    ├── output-template.json    # Output format
    └── report-template.md      # Report structure
```

**Use when**: Complex workflows, needs scripts, multiple output formats

---

### Multi-Domain Skill (Rare)

```
skill-name/
├── SKILL.md                    # Router + decision tree
├── domains/
│   ├── domain-a/
│   │   ├── workflow.md
│   │   └── references/
│   └── domain-b/
│       ├── workflow.md
│       └── references/
├── shared/
│   ├── common-rules.md
│   └── glossary.md
└── scripts/
    └── test_triggering.py
```

**Use when**: Multiple distinct domains with shared foundation

⚠️ **Consider splitting** into separate skills if domains are truly independent

---

## SKILL.md Structure Template

```yaml
---
name: skill-name
description: >-
  [Primary capability]. [Secondary capabilities].
  Provides [value proposition].
  Use when [context 1], [context 2], or [context 3].
  Not for [exclusion 1] or [exclusion 2].
allowed-tools: Read, Grep, Glob    # Optional, Claude Code only
---

# Skill Title

## Overview

[2-3 sentences describing the skill purpose and main capability.
Focus on what problem it solves and for whom.]

## Quick Start

[For single workflow:]
1. [First step]
2. [Second step]
3. [Third step]

[For multiple workflows - use Decision Tree:]

## Decision Tree

```
┌─────────────────────────────────────────┐
│           What do you need?             │
└─────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Path A  │   │ Path B  │   │ Path C  │
└────┬────┘   └────┬────┘   └────┬────┘
     ↓             ↓             ↓
  [Action]     [Action]      [Action]
```

## Workflows

### Workflow A: [Name]

**When to use**: [Condition]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output**: [Expected output]

### Workflow B: [Name]

[Same structure...]

## Critical Rules

[Mandatory rules that must ALWAYS be followed]

- **Rule 1**: [Description]
- **Rule 2**: [Description]
- **Rule 3**: [Description]

## Examples

### Example 1: [Scenario]

**Input**:
```
[Example input]
```

**Output**:
```
[Example output]
```

### Example 2: [Scenario]

[Same structure...]

## Knowledge Base

For detailed information:
- [Reference Name](references/file.md) - [Brief description]
- [Reference Name](references/file.md) - [Brief description]
- [Reference Name](references/file.md) - [Brief description]

## Validation

[If scripts are available:]

```bash
python scripts/validate.py "[input]"
```

## Limitations

This skill does NOT:
- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

## Dependencies

[If external packages needed:]

```bash
pip install [package1] [package2]
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |

## Current: v1.0.0

## Owner

- **Name**: [Owner name]
- **Contact**: [Email/Slack]
```

---

## File Naming Conventions

### Folders
- Lowercase with hyphens: `my-skill/`, `references/`
- Max 2 levels deep
- Descriptive names

### Files
- Lowercase with hyphens: `api-reference.md`, `edge-cases.md`
- No spaces: ❌ `my file.md` → ✅ `my-file.md`
- Meaningful names: ❌ `doc1.md` → ✅ `finance-schemas.md`

### Extensions
| Type | Extension |
|------|-----------|
| Documentation | `.md` |
| Python scripts | `.py` |
| Shell scripts | `.sh` |
| JSON templates | `.json` |
| YAML configs | `.yaml` or `.yml` |

---

## Token Budget Guidelines

| Component | Target | Max |
|-----------|--------|-----|
| Frontmatter | ~100 tokens | 150 |
| SKILL.md body | ~2000 tokens | 5000 |
| Single reference | ~1000 tokens | 3000 |
| Total active | ~3000 tokens | 8000 |

### Estimation Formula
```
Tokens ≈ Characters / 4
```

### Check Command
```bash
wc -c SKILL.md  # Character count
# Divide by 4 for rough token estimate
```

---

## Progressive Disclosure Pattern

```
Level 1: Always loaded (~100 tokens)
├── name
└── description

Level 2: Loaded on trigger (<5000 tokens)
├── Overview
├── Quick Start
├── Workflows
├── Critical Rules
└── Examples (brief)

Level 3: Loaded on demand (variable)
├── references/schemas.md
├── references/api-reference.md
└── references/edge-cases.md
```

---

## Link Syntax

### Relative Links (Recommended)
```markdown
See [schemas](references/schemas.md) for details.
```

### With Description
```markdown
- [Finance Schemas](references/finance.md) - Revenue and ARR tables
```

### In Tables
```markdown
| Topic | Reference |
|-------|-----------|
| Schemas | [schemas.md](references/schemas.md) |
```

---

## Checklist Before Finalizing Structure

- [ ] SKILL.md at root level
- [ ] All referenced files exist
- [ ] No broken links
- [ ] Max 2 folder levels
- [ ] No spaces in filenames
- [ ] Token budget respected
- [ ] Progressive disclosure applied
- [ ] Critical content in SKILL.md, details in references
