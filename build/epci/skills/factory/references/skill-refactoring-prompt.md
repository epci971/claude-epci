# Skill Refactoring Prompt

> Master prompt for applying the steps→references pattern to existing EPCI skills.

## Overview

This prompt guides the refactoring of existing skills to follow EPCI v6 best practices:
- Steps as orchestrators (< 200 lines)
- References for domain knowledge (formats, rules, schemas)
- Centralized breakpoints via `breakpoint-formats.md`
- Cross-linking with "Reference Files Used" tables

## Target

```
Skill: {SKILL_NAME}
Path: src/skills/{SKILL_NAME}/
```

---

## Phase 1: Analysis (READ-ONLY)

### 1.1 Inventory Current Structure

**Actions:**
1. LIST all files in `steps/`, `references/`, `templates/`
2. COUNT lines for each file
3. FLAG steps > 200 lines as violations

**Output format:**
```
| File | Lines | Status |
|------|-------|--------|
| steps/step-01-xxx.md | 145 | OK |
| steps/step-07-complex.md | 277 | VIOLATION |
```

### 1.2 Detect Duplications

SCAN each step for extractable content:

| Pattern | Threshold | Action |
|---------|-----------|--------|
| ASCII breakpoints | > 10 lines | Extract to `references/breakpoint-formats.md` |
| JSON schemas | > 5 fields | Extract to `references/{domain}-schema.md` |
| Lookup tables | > 10 rows | Extract to `references/{domain}-tables.md` |
| Business rules | > 3 rules | Extract to `references/{domain}-rules.md` |
| Output templates | > 20 lines | Extract to `references/{domain}-templates.md` |

### 1.3 Map Extractions

For each duplication, document:
```
Source: {file}:{start_line}-{end_line}
Type: breakpoint | schema | rules | template | table
Content: {brief description}
Destination: references/{name}.md#{section}
```

### 1.4 Phase 1 Output

Generate analysis table:
```
+----------------------------------------------------------------------+
| PHASE 1: ANALYSIS COMPLETE                                           |
+----------------------------------------------------------------------+
| Steps analyzed: {N}                                                  |
| Violations (>200 lines): {X}                                         |
| Extractions identified: {Y}                                          |
+----------------------------------------------------------------------+

| Step | Lines | Violations | Proposed Extractions |
|------|-------|------------|---------------------|
| step-01-xxx | 145 | 0 | None |
| step-07-complex | 277 | 1 | 3 (breakpoints, schema, rules) |
```

---

## Phase 2: Extraction Plan

### 2.1 New References to Create

| File | Content Type | Sources | Est. Lines |
|------|--------------|---------|------------|
| `references/breakpoint-formats.md` | ASCII templates | step-02, step-05 | ~80 |
| `references/scoring-rules.md` | Business rules | step-03, step-04 | ~50 |

### 2.2 Existing References to Enrich

| File | Additions | Sources |
|------|-----------|---------|
| `references/output-formats.md` | +3 templates | step-06, step-07 |

### 2.3 Steps to Refactor

| Step | Before | After | Sections to Extract |
|------|--------|-------|---------------------|
| step-07-complex | 277 | ~140 | breakpoints (50), schema (40), rules (47) |

### 2.4 Validation Gate

Before proceeding, verify:
- [ ] All resulting steps will be < 200 lines
- [ ] All duplications are addressed
- [ ] Cross-references are consistent
- [ ] No orphan content

---

## Phase 3: Execution

### 3.1 Create New References

For each new reference file:

1. **Create header:**
```markdown
# {Title}

> {One-line description}

## Reference Files Used

N/A (this is a source reference)
```

2. **Extract content** from identified sources
3. **Add anchors** for cross-linking: `## Section Name {#anchor}`
4. **Validate** content completeness

### 3.2 Update Steps

For each step requiring changes:

1. **Add "Reference Files Used" section** at top:
```markdown
## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [breakpoint-formats.md](../references/breakpoint-formats.md) | ASCII templates for phase outputs |
| [scoring-rules.md](../references/scoring-rules.md) | EMS calculation rules |
```

2. **Replace inline content** with links:
```markdown
# Before (inline)
```
+----------------------------------+
| BREAKPOINT: Analysis Complete    |
+----------------------------------+
```

# After (linked)
AFFICHE le breakpoint depuis [breakpoint-formats.md#analysis-complete](../references/breakpoint-formats.md#analysis-complete)
```

3. **Verify line count** < 200

### 3.3 Consolidate Duplications

If same content exists in multiple references:
1. Identify canonical source
2. Update all references to point to single source
3. Remove duplicated content

---

## Phase 4: Validation

### 4.1 Automated Checks

```bash
# Count lines in all steps
wc -l src/skills/{SKILL}/steps/*.md

# Validate skill structure
python3 src/scripts/validate_skill.py src/skills/{SKILL}/

# Run factory audit (if available)
/factory {SKILL} --audit
```

### 4.2 Manual Checklist

- [ ] All steps < 200 lines
- [ ] "Reference Files Used" table in each step
- [ ] Breakpoints via references (not inline ASCII > 10 lines)
- [ ] No duplication across files
- [ ] SKILL.md updated with new references in "Reference Files" section
- [ ] All cross-links resolve correctly

### 4.3 Metrics Report

Generate final metrics:
```
+----------------------------------------------------------------------+
| REFACTORING COMPLETE: {SKILL_NAME}                                   |
+----------------------------------------------------------------------+
| Metric              | Before    | After     | Change                |
|---------------------|-----------|-----------|----------------------|
| Avg lines/step      | {X}       | {Y}       | -{Z}%                |
| Max lines/step      | {A}       | {B}       | -{C}%                |
| Duplications        | {D}       | 0         | -100%                |
| Reference files     | {E}       | {F}       | +{G}                 |
+----------------------------------------------------------------------+
```

---

## Extraction Thresholds Reference

Quick reference for when to extract:

| Content Type | Threshold | Target |
|--------------|-----------|--------|
| ASCII box | > 10 lines | `breakpoint-formats.md` |
| JSON schema | > 5 fields | `{domain}-schema.md` |
| Lookup table | > 10 rows | `{domain}-tables.md` |
| Business rules | > 3 rules | `{domain}-rules.md` |
| Output template | > 20 lines | `{domain}-templates.md` |
| Step file | > 200 lines | Must refactor |

---

## Usage

### Via Factory
```
/factory {skill-name} --refactor
```

### Manual Execution
1. Copy this prompt
2. Replace `{SKILL_NAME}` with target skill
3. Execute phases 1-4 sequentially
4. Validate with checklist

---

## Skills Priority Queue

| Skill | Priority | Critical Step | Estimated Reduction |
|-------|----------|---------------|---------------------|
| debug | P1 | step-07-complex.md (277 lines) | -50% |
| refactor | P1 | step-07-report.md (229 lines) | -40% |
| implement | P2 | step-04-review.md (201 lines) | -25% |
| quick | P3 | step-03-code.md (238 lines) | -15% |
