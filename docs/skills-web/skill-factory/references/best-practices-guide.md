# Best Practices Guide - Complete Reference

> Comprehensive methodology for creating production-ready Claude skills

---

## 1. Skill Conception Principles

### Definition
A Skill is a **modular expertise package** that Claude loads dynamically via **semantic matching** between user request and skill description. Unlike slash commands, Skills are invoked **autonomously** by Claude.

### When to Create a Skill

| Criterion | Key Question |
|-----------|--------------|
| **Recurrence** | Task performed ≥5 times? Will be repeated ≥10 times? |
| **Complexity** | Requires non-trivial business rules? |
| **Standardization** | Multiple people need consistent approach? |
| **Stability** | Procedures stable (not changing every sprint)? |

**Ideal candidates**: Data warehouse SQL, internal documentation, code standards, recurring analysis workflows, business templates.

### When NOT to Create a Skill

- One-time or unique task
- Simple prompt in project suffices
- Procedures that change frequently
- Duplicates native Claude capability

### Principle: One Skill = One Focused Capability

| ❌ Anti-pattern | ✅ Better approach |
|-----------------|-------------------|
| `document-helper` (PDF + summaries + contracts + spelling) | `pdf-structured-review` + `contract-redlining` |
| `data-tools` (SQL + Excel + reporting) | `sql-analytics` + `excel-kpi-analyst` |
| `dev-helper` (debug + review + refactor) | `python-security-audit` + `react-refactor` |

---

## 2. Structure and Architecture

### Standard Hierarchy

```
my-skill/
├── SKILL.md                    # REQUIRED - Entry point (<5000 tokens)
├── references/                 # Detailed documentation (loaded on demand)
│   ├── schemas.md
│   ├── api-reference.md
│   └── edge-cases.md
├── scripts/                    # Executable scripts
│   ├── validator.py
│   └── helper.sh
└── templates/                  # Output templates (optional)
    └── output-template.json
```

### Storage Locations

| Type | Path | Scope | Sharing |
|------|------|-------|---------|
| **Personal** | `~/.claude/skills/skill-name/` | All your projects | No |
| **Project** | `.claude/skills/skill-name/` | Current project | Via Git |
| **Plugin** | `skills/skill-name/` (in plugin) | Packaged distribution | Via marketplace |

### Best Practices

- **Minimal but complete SKILL.md** — details go in `references/`
- **Explicit links** to annexed files (Claude only finds what's linked)
- **Flat structure** — maximum 2 levels deep
- **Clear naming**: `references/excel-kpis.md`, not `references/doc1.md`
- **Unix paths**: always `/`, even on Windows

### Pitfalls to Avoid

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Everything in SKILL.md | Context window saturated | Split into references |
| Files without link from SKILL.md | Never loaded | Explicit links `[file.md](path)` |
| Deep hierarchy (>2 levels) | Complex navigation | Flatten structure |
| Filenames with spaces | Parsing errors | Use hyphens or underscores |

---

## 3. Progressive Disclosure (Context Window)

### Loading Levels

| Level | Content | Tokens | Loading |
|-------|---------|--------|---------|
| **Level 1** | Frontmatter (name, description) | ~100 | Always |
| **Level 2** | SKILL.md body (workflow, rules) | <5000 | On triggering |
| **Level 3** | References (`references/*.md`) | Variable | On demand |

### Recommended Limits

- **SKILL.md**: <5000 tokens (~2-4 pages, ~1-2 KB)
- **Reference files**: No strict limit (loaded on demand)
- **Total Skill**: Depends on context window, keep lean

### "Menu" Pattern for Multi-Process Skills

```markdown
## Available Workflows

| Workflow | Use When | Reference |
|----------|----------|-----------|
| Text Extraction | Reading PDF content | [extraction.md](references/extraction.md) |
| Form Filling | Completing interactive forms | [forms.md](references/forms.md) |
| Merge/Split | Combining multiple documents | [merge.md](references/merge.md) |

## Quick Decision
- Just reading? → Text Extraction
- Interactive form? → Form Filling  
- Multiple PDFs? → Merge/Split
```

### Information Hierarchy

```
1. Overview (2-3 sentences)
   ↓
2. Quick Start / Decision Tree
   ↓
3. Main workflow (numbered steps)
   ↓
4. Critical rules (filters, validations)
   ↓
5. Links to detailed references
   ↓
6. Explicit limitations
```

---

## 4. External Files and Scripts

### Supported File Types

| Type | Extension | Usage |
|------|-----------|-------|
| Documentation | `.md` | Schemas, API reference, guides |
| Scripts | `.py`, `.sh`, `.js` | Executable utilities |
| Templates | `.json`, `.xml`, `.txt` | Output structures |
| Data | `.csv`, `.json` | Static reference data |

### Golden Rule: Determinism vs Reasoning

| Need | Solution | Example |
|------|----------|---------|
| Calculations, strict formatting, validation | **External script** | JSON validation, SQL lint |
| Semantic analysis, synthesis, creativity | **LLM instructions** | Summary, recommendations |

### Utility Script Pattern

```python
# scripts/validate_query.py
"""
Validates SQL queries against data warehouse rules.
Usage: python validate_query.py "SELECT * FROM revenue"
"""

import sys
import re

REQUIRED_FILTERS = [
    r"WHERE.*account\s*!=\s*'Test'",
    r"WHERE.*month\s*<=\s*DATE_TRUNC"
]

def validate(query: str) -> tuple[bool, list[str]]:
    errors = []
    for pattern in REQUIRED_FILTERS:
        if not re.search(pattern, query, re.IGNORECASE):
            errors.append(f"Missing required filter: {pattern}")
    return len(errors) == 0, errors

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    valid, errors = validate(query)
    print("✅ Valid" if valid else f"❌ Invalid: {errors}")
```

### Dependencies Section

```markdown
## Dependencies

Required packages (install if not available):

```bash
# Python
pip install pandas sqlalchemy

# System
sudo apt-get install jq
```

Note: Claude will ask for permission before installing packages.
```

---

## 5. Security and Confidentiality

### Fundamental Principles

| Principle | Application |
|-----------|-------------|
| **Trusted sources only** | Internal skills or validated repos |
| **Review before installation** | Read SKILL.md and scripts before activating |
| **Least privilege** | `allowed-tools` restricted to minimum |
| **No hardcoded secrets** | Environment variables for credentials |
| **Script audit** | Verify code before execution |

### Tool Restriction with `allowed-tools`

```yaml
---
name: safe-code-reviewer
description: Read-only code analysis for security audit. Use when reviewing code without modifications.
allowed-tools: Read, Grep, Glob
---
```

**Available tools**: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `LS`

For read-only Skill, **do not** authorize: `Write`, `Edit`, `Bash`

### Dangerous Practices

| Practice | Risk | Alternative |
|----------|------|-------------|
| Hardcoded credentials | Secret exposure | Environment variables |
| Scripts downloaded from URLs | Malicious code | Locally versioned scripts |
| `allowed-tools` too permissive | Undesired actions | Restrict to minimum |
| Skills from unknown sources | Malicious execution | Audit before use |

### Secure Credentials Pattern

```markdown
## Configuration

This skill requires database credentials. Set environment variables:

```bash
export ACME_DB_HOST="your-host"
export ACME_DB_USER="your-user"
export ACME_DB_PASSWORD="your-password"  # Never commit this!
```

The skill reads credentials from environment, never from files.
```

---

## 6. Technical Constraints

### Documented Limits

| Constraint | Value | Impact |
|------------|-------|--------|
| `name` size | Max 64 characters | Short, descriptive names |
| `description` size | Max 1024 characters | Mandatory conciseness |
| Metadata tokens | ~100 tokens | Always loaded |
| Instruction tokens | <5000 recommended | Performance |
| `allowed-tools` | Claude Code only | Not supported on API/claude.ai |

### Platform Differences

| Feature | Claude.ai | Claude Code | API |
|---------|-----------|-------------|-----|
| Custom Skills | ✅ (Settings) | ✅ (files) | ✅ (endpoint) |
| `allowed-tools` | ❌ | ✅ | ❌ |
| Code Execution | ✅ (beta) | ✅ | ✅ (beta) |
| Organization sharing | ❌ | ✅ (Git) | ✅ (API) |

### Limitations to Anticipate

| Limitation | Workaround |
|------------|------------|
| No memory between sessions | State in files or external DB |
| No arbitrary network access | MCP for external integrations |
| Limited context window | Progressive disclosure, references |
| No native GUI | Artifacts for visualization |

---

## 7. Maintenance and Versioning

### Versioning in SKILL.md

```markdown
## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-12-01 | Added customer_lifetime_value table |
| 2.0.0 | 2025-11-15 | **BREAKING**: New ARR calculation method |
| 1.2.0 | 2025-10-20 | Added sales pipeline schemas |
| 1.0.0 | 2025-09-01 | Initial release |

## Current: v2.1.0
```

### Update Workflow

```bash
# 1. Edit the Skill
code .claude/skills/my-skill/SKILL.md

# 2. Test locally (restart Claude Code)
claude  # Changes are loaded

# 3. Commit with descriptive message
git add .claude/skills/my-skill/
git commit -m "feat(my-skill): add new validation rules v1.2.0"

# 4. Push for team sharing
git push
```

### Best Practices

| Practice | Benefit |
|----------|---------|
| Changelog in SKILL.md | Evolution traceability |
| Semantic versioning | Clear breaking change communication |
| Non-regression tests | Triggering stability |
| Team review | Quality and relevance |
| Quarterly audit | Remove obsolete Skills |

### Never Change

- The `name` once the Skill is deployed (Claude associates this name with a task)
- Main triggers without documentation update

---

## 8. Migration: Prompts → Skills

### 5-Step Workflow

| Step | Action | Deliverable |
|------|--------|-------------|
| **1. Identify** | What does the prompt actually do? | Input/output list |
| **2. Extract** | What are the invariants? | Sections, style, constraints |
| **3. Simplify** | Reduce verbosity, keep operational | Condensed instructions |
| **4. Encapsulate** | YAML frontmatter + structured body | Initial `SKILL.md` |
| **5. Externalize** | Examples, business docs → `references/` | Final structure |

### Transformation Questions

1. **Is this behavior stable?** If yes → Skill. If no → remains prompt.
2. **Will others use it?** If yes → shared Skill.
3. **Is the prompt too tied to a single project?** If yes → abstract before converting.

---

## Resources

### Official Documentation
- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)

### Examples and Templates
- [GitHub anthropics/skills](https://github.com/anthropics/skills)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
