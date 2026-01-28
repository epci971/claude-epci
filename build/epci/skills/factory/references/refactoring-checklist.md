# Refactoring Checklist

> Post-refactoring validation checklist for EPCI skills.

## Pre-Refactoring Gate

Before starting refactoring:

- [ ] Skill exists and is functional
- [ ] Identified at least one step > 200 lines OR duplication issue
- [ ] Analysis phase (Phase 1) completed with extraction map

---

## Structure Validation

### Step Files

| Check | Requirement | Command |
|-------|-------------|---------|
| Line count | All steps < 200 lines | `wc -l steps/*.md` |
| Numbering | Sequential (00, 01, 02...) | `ls steps/` |
| Headers | Consistent format | Manual review |
| Next step | Each step has `→ next_step` | `grep -l "Next Step" steps/*.md` |

### Reference Files

| Check | Requirement |
|-------|-------------|
| Existence | All linked references exist |
| Anchors | Cross-links resolve correctly |
| No orphans | All references are linked from at least one step |
| No duplication | Content exists in single canonical location |

---

## Content Validation

### Steps Must Have

- [ ] "Reference Files Used" table (if using references)
- [ ] Clear protocol/procedure (WHAT to do)
- [ ] Imperative language (AFFICHE, APPELLE, ATTENDS)
- [ ] Output format or link to reference

### Steps Must NOT Have

- [ ] Inline ASCII boxes > 10 lines
- [ ] Inline JSON schemas > 5 fields
- [ ] Inline lookup tables > 10 rows
- [ ] Duplicated content from other steps
- [ ] Business rules > 3 items (extract to references)

### References Must Have

- [ ] Header with description
- [ ] Anchors for sections (`{#anchor}`)
- [ ] Self-contained content (no procedural logic)

### References Must NOT Have

- [ ] Orchestration logic (IF/FOR/Task)
- [ ] Step-specific procedures
- [ ] Duplicated content from other references

---

## Cross-Linking Validation

### Link Format
```markdown
# Correct
See [breakpoint-formats.md#section](../references/breakpoint-formats.md#section)

# Incorrect
See breakpoint-formats.md
```

### Bidirectional Check

For each reference:
1. Find all steps that link to it
2. Verify reference acknowledges usage context (optional but recommended)

---

## Metrics Validation

### Mandatory Thresholds

| Metric | Threshold | Status |
|--------|-----------|--------|
| Max step lines | < 200 | Required |
| SKILL.md lines | < 500 | Required |
| Duplications | 0 | Required |

### Recommended Targets

| Metric | Target |
|--------|--------|
| Avg step lines | < 150 |
| Reference coverage | 100% (all refs linked) |
| "Reference Files Used" tables | In all steps using refs |

---

## Final Validation Commands

```bash
# 1. Line count check
echo "=== Step Line Counts ===" && wc -l src/skills/{SKILL}/steps/*.md

# 2. Validate skill structure
python3 src/scripts/validate_skill.py src/skills/{SKILL}/

# 3. Check for broken links (grep for .md references)
grep -r "](../" src/skills/{SKILL}/steps/ | grep -v "^Binary"

# 4. Run factory audit
/factory {SKILL} --audit
```

---

## Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Broken link | 404 on reference | Update path or create missing file |
| Orphan reference | Reference not linked | Add link from relevant step OR delete if unused |
| Still > 200 lines | Step too long | Extract more content OR split step |
| Duplicate content | Same text in 2+ files | Consolidate to single source |
| Missing anchor | Link with `#section` fails | Add `{#section}` to reference heading |

---

## Sign-Off Template

After completing refactoring, document:

```markdown
## Refactoring Sign-Off: {SKILL_NAME}

**Date**: {DATE}
**Refactored by**: Claude

### Metrics
| Metric | Before | After |
|--------|--------|-------|
| Max step lines | {X} | {Y} |
| Avg step lines | {A} | {B} |
| Reference files | {C} | {D} |
| Duplications | {E} | 0 |

### Changes Made
- Created: {list new reference files}
- Modified: {list modified steps}
- Extracted: {summary of extractions}

### Validation
- [ ] All automated checks pass
- [ ] Manual checklist complete
- [ ] Factory audit: PASS
```
