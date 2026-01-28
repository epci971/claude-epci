# Step 07: Refactor

> Apply steps→references pattern to existing skills.

## Trigger

- Mode: `--refactor` detected in step-00-init
- Skill path resolved and exists

## Reference Files

@../references/skill-refactoring-prompt.md
@../references/refactoring-checklist.md
@../references/refactoring-formats.md
@../references/best-practices-synthesis.md

| Reference | Purpose |
|-----------|---------|
| skill-refactoring-prompt.md | Master workflow and thresholds |
| refactoring-checklist.md | Post-refactoring validation |
| refactoring-formats.md | ASCII display templates |
| best-practices-synthesis.md | Content location rules |

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `skill_name` | From step-00 | Yes |
| `skill_path` | Resolved path | Yes |

---

## Phase 1: Analysis

### 1.1 Inventory Structure

EXECUTE:
1. LIST files in `{skill_path}/steps/` and `{skill_path}/references/`
2. COUNT lines for each file
3. FLAG files > 200 lines (steps) or > 300 lines (references)

AFFICHE le format depuis refactoring-formats.md (section #structure-inventory importé ci-dessus)

### 1.2 Detect Extractions

SCAN each step using thresholds from best-practices-synthesis.md (section #7.2 importé ci-dessus):

| Pattern | Threshold | Marker |
|---------|-----------|--------|
| ASCII boxes | > 10 lines | `[EXTRACT:breakpoint]` |
| JSON schemas | > 5 fields | `[EXTRACT:schema]` |
| Lookup tables | > 10 rows | `[EXTRACT:table]` |
| Business rules | > 3 rules | `[EXTRACT:rules]` |
| Output templates | > 20 lines | `[EXTRACT:template]` |

### 1.3 Map Extractions

FOR each extraction found, document:
- Source: `{file}:{start_line}-{end_line}`
- Type: `{breakpoint|schema|table|rules|template}`
- Lines: `{count}`
- Destination: `references/{proposed_name}.md#{section}`

### 1.4 Phase 1 Output

AFFICHE le format depuis refactoring-formats.md (section #analysis-complete importé ci-dessus)

ATTENDS confirmation avant Phase 2.

---

## Phase 2: Extraction Plan

### 2.1 Plan New References

FOR each unique destination, list: New Reference, Content Types, Source Files, Est. Lines

### 2.2 Plan Reference Enrichments

IF extraction targets existing reference, list: Reference, Additions, Source Files

### 2.3 Plan Step Modifications

FOR each step with extractions, list: Step, Current lines, Target (< 200), Extraction count

### 2.4 Validation Gate

VERIFY before execution:
- [ ] All target steps will be < 200 lines
- [ ] No circular dependencies
- [ ] All destinations are valid

AFFICHE le format depuis refactoring-formats.md (section #extraction-plan importé ci-dessus)

ATTENDS approval avant Phase 3.

---

## Phase 3: Execution

### 3.1 Create New References

FOR each new reference:
1. CREATE file using template from refactoring-formats.md (section #reference-template importé ci-dessus)
2. ADD anchors for cross-linking: `## Section {#anchor}`

### 3.2 Update Steps

FOR each step with extractions:
1. ADD "Reference Files" section (see refactoring-formats.md section #step-update-pattern importé ci-dessus)
2. REPLACE inline content with links
3. VERIFY line count < 200

### 3.3 Consolidate Duplications

IF same content exists in multiple locations:
1. IDENTIFY canonical source
2. UPDATE all references to point to single source
3. DELETE duplicated content

---

## Phase 4: Validation

### 4.1 Automated Checks

EXECUTE:
```bash
wc -l {skill_path}/steps/*.md
python3 src/scripts/validate_skill.py {skill_path}/
```

### 4.2 Manual Checklist

VERIFY using refactoring-checklist.md (importé ci-dessus):
- [ ] All steps < 200 lines
- [ ] "Reference Files Used" in steps using references
- [ ] No inline ASCII > 10 lines
- [ ] No duplications across files
- [ ] All cross-links resolve
- [ ] SKILL.md references section updated

### 4.3 Final Report

AFFICHE le format depuis refactoring-formats.md (section #final-report importé ci-dessus)

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Skill not found | Verify skill name and path |
| No extractions found | Skill already optimized, exit |
| Circular dependency | Reorganize extraction plan |
| Line count still > 200 | Additional extraction needed |
| Broken cross-link | Fix path or create missing anchor |

---

## Next Step

EXIT workflow after Phase 4 completion.

Optional: Run `/factory {skill_name} --audit` to verify final state.
