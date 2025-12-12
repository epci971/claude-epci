# Validation Checklist - 40-Point Verification

> Complete verification before deploying a skill

---

## Quick Summary

| Category | Points |
|----------|--------|
| Structure & Files | 4 |
| YAML Frontmatter | 4 |
| Description (Triggering) | 5 |
| Instructions & Workflow | 5 |
| Context Window | 3 |
| Scripts & Dependencies | 4 |
| Security | 4 |
| Tests | 6 |
| Documentation | 3 |
| Sharing Ready | 2 |
| **Total** | **40 checkpoints** |

**Minimum required**: >=36/40 for APPROVED status

---

## 1. Structure & Files

- [ ] Folder `skill-name/` with `SKILL.md` at root
- [ ] Name in kebab-case, no spaces or capitals
- [ ] Clear tree structure (max 2 levels)
- [ ] All referenced files exist

### Verification Command
```bash
# Check structure
find skill-name/ -type f | head -20

# Verify SKILL.md exists
test -f skill-name/SKILL.md && echo "SKILL.md exists"
```

---

## 2. YAML Frontmatter

- [ ] `name`: <=64 chars, kebab-case
- [ ] `description`: <=1024 chars, explicit triggers
- [ ] Valid YAML syntax (no tabs, proper quotes)
- [ ] Frontmatter closed with `---`

### Verification Script
```python
import yaml
content = open('SKILL.md').read()
frontmatter = content.split('---')[1]
data = yaml.safe_load(frontmatter)

assert len(data['name']) <= 64, "Name too long"
assert '-' in data['name'] or data['name'].islower(), "Must be kebab-case"
assert len(data['description']) <= 1024, "Description too long"
print("Frontmatter valid")
```

---

## 3. Optimized Description

- [ ] Includes action verbs (extract, analyze, create...)
- [ ] Includes file types / data types concerned
- [ ] Includes "Use when..." with usage contexts
- [ ] Includes "Not for..." with exclusions
- [ ] No overlap with existing skills

### Description Quality Score

| Element | Present? | Score |
|---------|----------|-------|
| Action verbs | [ ] | +2 |
| File/data types | [ ] | +2 |
| "Use when..." | [ ] | +3 |
| "Not for..." | [ ] | +2 |
| No overlap | [ ] | +1 |
| **Total** | | /10 |

**Minimum required**: 7/10

---

## 4. Instructions & Workflow

- [ ] Overview present (2-3 sentences)
- [ ] Workflow in numbered steps
- [ ] Decision tree if multiple workflows
- [ ] Concrete examples (at least 1)
- [ ] Explicit limitations documented

### Required Sections Checklist

```markdown
[ ] Overview (2-3 sentences)
[ ] Quick Start / Decision Tree
[ ] Numbered workflow steps (1, 2, 3...)
[ ] Critical rules / validations
[ ] Examples with input -> output
[ ] Links to references
[ ] Limitations section
```

---

## 5. Context Window Optimization

- [ ] SKILL.md < 5000 tokens (~2-4 pages)
- [ ] Details in `references/` with explicit links
- [ ] No duplication between SKILL.md and references

### Token Estimation
```python
# Quick token estimate (rough: 1 token ~ 4 chars)
content = open('SKILL.md').read()
estimated_tokens = len(content) / 4
print(f"Estimated: {estimated_tokens:.0f} tokens")
print("OK" if estimated_tokens < 5000 else "Consider splitting")
```

---

## 6. Scripts & Dependencies

- [ ] Scripts with execution permissions or called via interpreter
- [ ] Paths in Unix format (`/`)
- [ ] Dependencies documented
- [ ] No hardcoded paths to local system

### Verification Commands
```bash
# Check script permissions
ls -la scripts/

# Verify shebang or interpreter call documented
head -1 scripts/*.py

# Search for hardcoded paths
grep -r "/home/" scripts/ || echo "No hardcoded home paths"
grep -r "C:\\" scripts/ || echo "No Windows paths"
```

---

## 7. Security

- [ ] No hardcoded credentials
- [ ] `allowed-tools` configured if restriction needed
- [ ] Scripts audited (no malicious code)
- [ ] Trusted source

### Security Scan
```bash
# Search for potential secrets
grep -rE "(password|secret|api.?key|token)\s*=" . || echo "No obvious secrets"

# Check allowed-tools is restrictive
grep "allowed-tools" SKILL.md
```

---

## 8. Tests Passed

- [ ] Explicit triggering works
- [ ] Implicit triggering works
- [ ] No false positives (out-of-scope)
- [ ] Main workflow works
- [ ] Edge cases handled
- [ ] Tested with >=3 different formulations

### Test Matrix Template

| Test Type | Query | Expected | Result |
|-----------|-------|----------|--------|
| Explicit | "Use [skill] to [action]" | Triggers | [ ] |
| Implicit | "[natural request]" | Triggers | [ ] |
| Out-of-scope | "[related but excluded]" | No trigger | [ ] |
| Edge case | "[unusual input]" | Graceful | [ ] |
| Workflow | "[full process]" | Completes | [ ] |

---

## 9. Documentation

- [ ] Version documented in SKILL.md
- [ ] Version History section present
- [ ] Owner/contact identified

### Version History Template
```markdown
## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |

## Current: v1.0.0

## Owner
- Name: [Owner Name]
- Contact: [email/slack]
```

---

## 10. Ready for Sharing

- [ ] Tested by at least one other team member
- [ ] Committed to Git with descriptive message

### Git Commit Template
```bash
git add .claude/skills/my-skill/
git commit -m "feat(my-skill): add [capability] skill v1.0.0

- [Main feature 1]
- [Main feature 2]
- Tested with [test scenarios]"
```

---

## Compliance Report Template

```markdown
# Skill Compliance Report

**Skill**: [name]
**Version**: [version]
**Date**: [date]
**Reviewer**: [name]

## Results

| Category | Score | Status |
|----------|-------|--------|
| Structure | /4 | [ ] |
| YAML | /4 | [ ] |
| Description | /5 | [ ] |
| Instructions | /5 | [ ] |
| Context Window | /3 | [ ] |
| Scripts | /4 | [ ] |
| Security | /4 | [ ] |
| Tests | /6 | [ ] |
| Documentation | /3 | [ ] |
| Sharing | /2 | [ ] |
| **TOTAL** | /40 | |

## Status
- [ ] APPROVED (>=36/40)
- [ ] NEEDS WORK (28-35/40)
- [ ] REJECTED (<28/40)

## Issues Found
1. [Issue description]
2. [Issue description]

## Recommendations
1. [Recommendation]
2. [Recommendation]
```
