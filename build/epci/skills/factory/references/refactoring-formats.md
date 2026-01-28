# Refactoring Display Formats

> ASCII box templates for refactoring workflow outputs.

## Phase 1: Structure Inventory {#structure-inventory}

```
+----------------------------------------------------------------------+
| PHASE 1: STRUCTURE INVENTORY                                         |
+----------------------------------------------------------------------+
| Skill: {skill_name}                                                  |
| Path: {skill_path}                                                   |
+----------------------------------------------------------------------+

Steps ({count}):
| File | Lines | Status |
|------|-------|--------|
{foreach step: | {name} | {lines} | {OK|VIOLATION} |}

References ({count}):
| File | Lines |
|------|-------|
{foreach ref: | {name} | {lines} |}
```

## Phase 1: Analysis Complete {#analysis-complete}

```
+----------------------------------------------------------------------+
| ANALYSIS COMPLETE                                                    |
+----------------------------------------------------------------------+
| Steps analyzed: {N}                                                  |
| Steps with violations: {X}                                           |
| Extractions identified: {Y}                                          |
+----------------------------------------------------------------------+

Extraction Map:
| # | Source | Type | Lines | Destination |
|---|--------|------|-------|-------------|
{foreach extraction}
```

## Phase 2: Extraction Plan {#extraction-plan}

```
+----------------------------------------------------------------------+
| EXTRACTION PLAN                                                      |
+----------------------------------------------------------------------+
| New references to create: {N}                                        |
| Existing references to enrich: {M}                                   |
| Steps to modify: {X}                                                 |
| Total extractions: {Y}                                               |
+----------------------------------------------------------------------+
```

## Phase 4: Final Report {#final-report}

```
+----------------------------------------------------------------------+
| REFACTORING COMPLETE: {skill_name}                                   |
+----------------------------------------------------------------------+
| Metric              | Before    | After     | Change                |
|---------------------|-----------|-----------|----------------------|
| Max step lines      | {X}       | {Y}       | -{Z}%                |
| Avg step lines      | {A}       | {B}       | -{C}%                |
| Duplications        | {D}       | 0         | -100%                |
| Reference files     | {E}       | {F}       | +{G}                 |
+----------------------------------------------------------------------+

Files Created:
{list new files}

Files Modified:
{list modified files}

+----------------------------------------------------------------------+
| STATUS: {PASS|FAIL}                                                  |
+----------------------------------------------------------------------+
```

## Reference File Template {#reference-template}

```markdown
# {Title}

> {Description based on content type}

## Contents

{Extracted content with anchors}
```

## Step Update Pattern {#step-update-pattern}

Add "Reference Files Used" table:
```markdown
## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [{ref}](../references/{ref}) | {purpose} |
```

Replace inline content:
```markdown
# Before
{inline content > threshold}

# After
AFFICHE le contenu depuis [{ref}#{section}](../references/{ref}#{section})
```
