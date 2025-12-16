# Skill Compliance Report — Propositor

**Skill**: propositor  
**Version**: 1.0.0  
**Date**: 2025-12-15  
**Reviewer**: Claude (via skill-factory)  

---

## Results Summary

| Category | Score | Status |
|----------|-------|--------|
| Structure & Files | 4/4 | ✅ |
| YAML Frontmatter | 4/4 | ✅ |
| Description (Triggering) | 5/5 | ✅ |
| Instructions & Workflow | 4/4 | ✅ |
| Context Window | 3/3 | ✅ |
| Scripts & Dependencies | 3/4 | ✅ |
| Security | 4/4 | ✅ |
| Tests | 5/6 | ✅ |
| Documentation | 3/3 | ✅ |
| Sharing Ready | 2/3 | ⚠️ |
| **TOTAL** | **37/40** | ✅ **APPROVED** |

---

## Detailed Validation

### 1. Structure & Files ✅ 4/4

- [x] Folder `propositor/` with `SKILL.md` at root
- [x] Name in kebab-case, no spaces or capitals
- [x] Clear tree structure (max 2 levels)
- [x] All referenced files exist

```
propositor/
├── SKILL.md
├── references/
│   ├── output-format.md
│   ├── templates.md
│   ├── tone-adaptation.md
│   └── workflow-details.md
└── scripts/
    └── test_triggering.py
```

### 2. YAML Frontmatter ✅ 4/4

- [x] `name`: 10 chars ≤64 ✓
- [x] `description`: 605 chars ≤1024 ✓
- [x] Valid YAML syntax (no tabs, proper quotes)
- [x] Frontmatter closed with `---`

### 3. Description Quality ✅ 5/5

| Element | Present | Score |
|---------|---------|-------|
| Action verbs | ✅ "Creates", "Adapts", "Generates", "validates" | +2 |
| File/data types | ✅ "proposals", "templates", "Gantt charts" | +2 |
| "Use when..." | ✅ Present with 4 contexts | +3 |
| "Not for..." | ✅ Present with 3 exclusions | +2 |
| No overlap | ✅ Clear distinction from estimator | +1 |
| **Total** | | **10/10** |

### 4. Instructions & Workflow ✅ 4/4

- [x] Workflow in numbered steps (4 phases)
- [x] Decision tree for templates
- [x] Concrete examples in references
- [x] Explicit limitations section
- [x] **Critical dependency documented** (Estimator required)

### 5. Context Window ✅ 3/3

- [x] SKILL.md: ~2,129 tokens (<5000) ✓
- [x] Details in `references/` with explicit links
- [x] No duplication between SKILL.md and references

**Token breakdown**:
| File | Est. Tokens |
|------|-------------|
| SKILL.md | ~2,129 |
| workflow-details.md | ~2,800 |
| templates.md | ~4,200 |
| tone-adaptation.md | ~2,600 |
| output-format.md | ~3,500 |

### 6. Scripts & Dependencies ⚠️ 3/4

- [x] Script with shebang (`#!/usr/bin/env python3`)
- [x] Paths in Unix format
- [ ] Dependencies documented (none required)
- [x] No hardcoded paths

**Note**: Script is standalone Python, no external dependencies.

### 7. Security ✅ 4/4

- [x] No hardcoded credentials
- [x] `allowed-tools` not specified (not restrictive)
- [x] Scripts audited (no malicious code)
- [x] Trusted source (internal development)

### 8. Tests ⚠️ 5/6

- [x] Explicit triggering test cases defined (27 queries)
- [x] Implicit triggering test cases defined
- [x] Out-of-scope test cases defined (18 queries)
- [ ] Actual testing not performed (requires deployment)
- [x] Dependency tests defined (3 scenarios)
- [x] Coherence validation tests documented

**Test coverage**: 
- 27 SHOULD_TRIGGER queries
- 18 SHOULD_NOT_TRIGGER queries
- 3 DEPENDENCY_TESTS
- 5 COHERENCE_TESTS

### 9. Documentation ✅ 3/3

- [x] Version documented in SKILL.md
- [x] Version History section present
- [x] Owner/contact identified

### 10. Sharing Ready ⚠️ 2/3

- [ ] Tested by another team member (pending)
- [x] Ready for Git commit
- [x] Self-contained with all references

---

## Package Contents

| File | Purpose | Size |
|------|---------|------|
| `SKILL.md` | Main entry point | ~8.5 KB |
| `references/workflow-details.md` | Phase details, checkpoints | ~11 KB |
| `references/templates.md` | 5 template structures | ~17 KB |
| `references/tone-adaptation.md` | Client tone guidelines | ~10 KB |
| `references/output-format.md` | Output template | ~14 KB |
| `scripts/test_triggering.py` | Test suite | ~6 KB |
| **Total** | | **~66.5 KB** |

---

## Dependency Chain

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEPENDENCY VALIDATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  estimator ────────────► PROPOSITOR                             │
│  (REQUIRED)                   │                                  │
│                               ▼                                  │
│                          critiquor (suggested)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Propositor will NOT proceed without valid Estimator input.**

---

## Coherence Validation Features

| Check | Type | Behavior |
|-------|------|----------|
| Amount mismatch | 🔴 Blocking | Halt and alert |
| Planning unrealistic | 🟡 Warning | Alert, allow continue |
| Missing FCT refs | 🟡 Warning | Alert, allow continue |
| Placeholder remaining | 🔴 Blocking | Halt and alert |
| All coherent | ✅ OK | Proceed normally |

---

## Deployment Instructions

### For Claude.ai

1. Go to **Settings** → **Skills**
2. Create new skill
3. Copy content of `SKILL.md` to the skill editor
4. Upload reference files as attachments OR inline critical content

### For Claude Code

1. Copy folder to `~/.claude/skills/propositor/`
2. Restart Claude Code
3. Test with: "use propositor" (after running estimator)

### For Project Sharing

```bash
# Add to project
cp -r propositor/ .claude/skills/

# Commit
git add .claude/skills/propositor/
git commit -m "feat(skills): add propositor skill v1.0.0

- Commercial proposal generator from estimator output
- 5 templates (dev, refonte, TMA, audit, ao-public)
- 6 client type tone adaptations
- Automatic Gantt generation
- Coherence validation"

# Push
git push
```

---

## Suggested Test Queries

### Quick Validation (5 queries)

1. `"use propositor"` → Should trigger (needs estimator first)
2. `"rédige une proposition commerciale"` → Should trigger
3. `"prépare une propale pour ce projet"` → Should trigger
4. `"estime ce projet"` → Should NOT trigger (estimator domain)
5. `"génère une facture"` → Should NOT trigger

### Integration Test Flow

```
1. Run estimator: "estime ce projet web"
   → Complete estimation workflow
   
2. Run propositor: "génère la proposition commerciale"
   → Should detect estimator output
   → Proceed with proposal generation
```

### Full Test

Run: `python scripts/test_triggering.py`

---

## Status

✅ **APPROVED** (37/40)

The skill meets all critical requirements and is ready for deployment. Minor items pending:
- Actual triggering tests after deployment
- Team review for collaborative projects

---

## Integration with Estimator

### Workflow Sequence

```
User Brief
    │
    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  ESTIMATOR  │ ──► │ PROPOSITOR  │ ──► │  CRITIQUOR  │
│  (required) │     │  (this)     │     │  (suggested)│
└─────────────┘     └─────────────┘     └─────────────┘
    │                     │
    ▼                     ▼
  EST-YYYY-NNN         PROP-YYYY-NNN
  (Estimation)         (Proposal)
```

### Data Exchange

Propositor parses Estimator output via:
- `<!-- ESTIMATOR_DATA_START/END -->` tags
- `<!-- ESTIMATOR_BUDGET_START/END -->` tags
- Feature table (FCT-xxx references)
- Stack choices (for solution section)

---

## Next Steps

1. **Deploy Estimator first** (if not already done)
2. **Deploy Propositor** to Claude.ai or Claude Code
3. **Test integration** with real project
4. **Iterate** based on feedback
5. **Consider critiquor** integration for quality review

---

*Report generated by skill-factory v1.0.0*
