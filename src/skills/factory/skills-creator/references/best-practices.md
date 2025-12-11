# Best Practices Guide - Complete Reference

> Comprehensive methodology for creating production-ready Claude skills

---

## 1. Skill Conception Principles

### Definition
A Skill is a **modular expertise package** that Claude loads dynamically via **semantic matching** between user request and skill description. Unlike slash commands, Skills are invoked **autonomously** by Claude.

### When to Create a Skill

| Criterion | Key Question |
|-----------|--------------|
| **Recurrence** | Task performed >=5 times? Will be repeated >=10 times? |
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

| Anti-pattern | Better approach |
|--------------|-----------------|
| `document-helper` (PDF + summaries + contracts) | `pdf-structured-review` + `contract-redlining` |
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

- **Minimal but complete SKILL.md** - details go in `references/`
- **Explicit links** to annexed files (Claude only finds what's linked)
- **Flat structure** - maximum 2 levels deep
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

- **SKILL.md**: <5000 tokens (~2-4 pages)
- **Reference files**: No strict limit (loaded on demand)
- **Total Skill**: Keep lean

### "Menu" Pattern for Multi-Process Skills

```markdown
## Available Workflows

| Workflow | Use When | Reference |
|----------|----------|-----------|
| Text Extraction | Reading PDF content | [extraction.md](references/extraction.md) |
| Form Filling | Completing interactive forms | [forms.md](references/forms.md) |
| Merge/Split | Combining multiple documents | [merge.md](references/merge.md) |

## Quick Decision
- Just reading? -> Text Extraction
- Interactive form? -> Form Filling
- Multiple PDFs? -> Merge/Split
```

### Information Hierarchy

```
1. Overview (2-3 sentences)
   |
2. Quick Start / Decision Tree
   |
3. Main workflow (numbered steps)
   |
4. Critical rules (filters, validations)
   |
5. Links to detailed references
   |
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
description: Read-only code analysis. Use when reviewing code without modifications.
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

---

## 6. Maintenance and Versioning

### Versioning in SKILL.md

```markdown
## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-12-01 | Added customer_lifetime_value table |
| 2.0.0 | 2025-11-15 | **BREAKING**: New ARR calculation method |
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

- The `name` once the Skill is deployed
- Main triggers without documentation update
