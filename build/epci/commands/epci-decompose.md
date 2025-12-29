---
description: >-
  Decompose a complex PRD/CDC into actionable sub-specifications (1-5 days each).
  Generates dependency graph and Gantt planning with parallelization.
  Use for large projects (>5 days) before running /epci-brief on each sub-spec.
argument-hint: "<file.md> [--output <dir>] [--think <level>] [--min-days <n>] [--max-days <n>] [--c7]"
allowed-tools: [Read, Write, Bash, Grep, Glob, Task, WebFetch]
---

# EPCI Decompose

## Overview

Automates the decomposition of complex PRD/CDC documents into actionable sub-specifications.
Each sub-spec targets 1-5 days of effort, enabling iterative EPCI execution.
Generates a dependency graph (Mermaid flowchart) and optimized Gantt planning.

**Use case:** A 25-day migration project becomes 9 manageable sub-specs that can be
executed sequentially or in parallel where dependencies allow.

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `<file.md>` | Source PRD/CDC file to decompose | Yes | — |
| `--output <dir>` | Output directory for generated specs | No | `docs/specs/{slug}/` |
| `--think <level>` | Thinking level: `quick`, `think`, `think-hard`, `ultrathink` | No | `think` |
| `--min-days <n>` | Minimum effort per sub-spec | No | `1` |
| `--max-days <n>` | Maximum effort per sub-spec | No | `5` |

## Pre-Workflow: Load Project Memory

**Skill**: `project-memory`

Load project context from `.project-memory/` before analysis. The skill handles:
- Reading context, conventions, settings, patterns
- Finding similar past decompositions for reference
- Applying project-specific naming conventions to generated specs

**If `.project-memory/` does not exist:** Continue with defaults.

---

## Process

**⚠️ IMPORTANT: Follow ALL phases in sequence. Do NOT skip the file generation step.**

### Phase 1: Validation (MANDATORY)

**Checks:**
1. File exists and is readable
2. File extension is `.md`
3. Extract title/slug from document
4. Count lines (complexity indicator)

**Exit conditions:**
- File not found → Error with suggestion
- Not a `.md` file → Error with suggestion

**Output:**
```
📄 Document: {filename}
├── Lines: {count}
├── Slug: {extracted_slug}
└── Status: Valid
```

### Phase 2: Structural Analysis (MANDATORY)

**⚠️ DO NOT SKIP:** Analyze the document structure and detect dependencies.

**Skills loaded:** `architecture-patterns`, `flags-system`

**Structure detection:**

| Signal | Usage |
|--------|-------|
| Headers `## Phase X` | Level 1 decomposition candidates |
| Headers `### Step X.Y` | Sub-decomposition candidates |
| Tables with "Effort" | Reuse existing estimates |
| "Checklist" sections | Validation boundaries |
| "Gate", "Prerequisite" mentions | Explicit dependencies |

**Dependency extraction:**

| Pattern | Detection |
|---------|-----------|
| Explicit | "depends on", "requires", "after", "before" |
| Django FK | `ForeignKey('app.Model')` → model must exist |
| Imports | `from X import Y` → Y must exist |
| References | `see S01`, `cf. Phase 1` |

**Granularity rules:**

| Block effort | Action |
|--------------|--------|
| < min-days | Merge with adjacent block |
| min-days to max-days | Target granularity |
| > max-days | Seek sub-decomposition |

**Invoke @decompose-validator:**
- Check dependency consistency
- Detect circular dependencies
- Validate granularity compliance

### Phase 3: Proposal (MANDATORY — WAIT FOR USER)

**⚠️ MANDATORY:** Display the breakpoint and WAIT for user validation before proceeding.

Present decomposition proposal for user validation:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT — VALIDATION DÉCOUPAGE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 ANALYSE DE: {filename}                                          │
│ ├── Lignes: {line_count}                                           │
│ ├── Effort total détecté: {total_days} jours                       │
│ └── Structure: {phases} phases, {steps} étapes                     │
│                                                                     │
│ 📋 DÉCOUPAGE PROPOSÉ: {count} sous-specs                           │
│                                                                     │
│ | ID  | Nom                    | Effort | Dépendances |            │
│ |-----|------------------------|--------|-------------|            │
│ | S01 | {name_1}               | {d1}j  | —           |            │
│ | S02 | {name_2}               | {d2}j  | S01         |            │
│ | ... | ...                    | ...    | ...         |            │
│                                                                     │
│ 🔀 PARALLÉLISATION: {parallel_count} specs parallélisables         │
│ ⏱️  DURÉE OPTIMISÉE: {optimized_days}j (vs {sequential_days}j seq) │
│                                                                     │
│ ⚠️  ALERTES: {alerts_or_none}                                       │
│                                                                     │
│ ✅ @decompose-validator: {verdict}                                  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • "Valider" → Générer les fichiers                               │
│   • "Modifier" → Ajuster le découpage                              │
│   • "Annuler" → Abandonner                                         │
└─────────────────────────────────────────────────────────────────────┘
```

**Modify option sub-menu:**

```
Que souhaitez-vous modifier ?

[1] Fusionner des specs — Ex: "Fusionner S04 et S05"
[2] Découper une spec — Ex: "Découper S07 en 2"
[3] Renommer — Ex: "S03 → Modèles Fondamentaux"
[4] Changer dépendances — Ex: "S06 ne dépend plus de S03"
[5] Ajuster estimation — Ex: "S08 = 3 jours"

Votre choix (ou texte libre):
```

### Phase 4: Generation (USE WRITE TOOL — MANDATORY)

**⚠️ MANDATORY:** Use the **Write tool** to create all output files.

**Create output directory:**
```bash
mkdir -p {output_dir}
```

**Generate files:**

1. **INDEX.md** — Overview with Mermaid diagrams
2. **S01-{slug}.md** through **SNN-{slug}.md** — Individual sub-specs

**Output structure:**
```
{output_dir}/
├── INDEX.md
├── S01-{name}.md
├── S02-{name}.md
├── ...
└── SNN-{name}.md
```

## Loaded Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `project-memory` | Pre-Workflow | Load context and conventions |
| `architecture-patterns` | Phase 2 | Identify decomposition patterns |
| `flags-system` | All | Handle --think levels |
| `mcp` | Phase 2 | Context7 for architecture patterns |

## Invoked Subagents

| Subagent | Condition | Role |
|----------|-----------|------|
| `@decompose-validator` | Always | Validate decomposition consistency |

## Output Formats

### INDEX.md

```markdown
# {Project Title} — Index

> **Generated**: {date}
> **Source**: {source_file}
> **Sub-specs**: {count}
> **Total effort**: {total_days} days

---

## Overview

| ID | Sub-Spec | Effort | Dependencies | Parallelizable |
|----|----------|--------|--------------|----------------|
| S01 | {name} | {d}j | — | No |
| S02 | {name} | {d}j | S01 | No |
| ... | ... | ... | ... | ... |

---

## Dependency Graph

```mermaid
flowchart TD
    S01[S01: {name}] --> S02[S02: {name}]
    S02 --> S03[S03: {name}]
    S03 --> S04[S04: {name}]
    S03 --> S05[S05: {name}]
    ...
```

---

## Gantt Planning

```mermaid
gantt
    title {Project Title}
    dateFormat  YYYY-MM-DD

    section Foundations
    S01 {name}    :s01, {start_date}, {d1}d
    S02 {name}    :s02, after s01, {d2}d

    section Core
    S03 {name}    :s03, after s02, {d3}d
    ...
```

---

## Progress

| Spec | Status | Comment |
|------|--------|---------|
| S01 | To do | |
| S02 | To do | |
| ... | ... | |

---

## Usage

Launch a sub-spec:
```bash
/epci-brief @{output_dir}/S01-{name}.md
```

---

*Generated by epci-decompose*
```

### SXX-{name}.md (Sub-Spec Template)

```markdown
# Specification — {ID}: {Title}

> **Parent project**: {slug}
> **Spec ID**: {ID}
> **Estimated effort**: {effort} day(s)
> **Dependencies**: {deps_list}
> **Blocks**: {blocking_list}

---

## 1. Context

This sub-spec is part of the **{project_title}** project.

**Source**: `{source_file}` — {section_reference}

---

## 2. Scope

### Included

{included_list}

### Excluded

{excluded_list}

---

## 3. Tasks

{task_checklist}

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| {ID}-AC1 | {criterion_1} | {verification_1} |
| {ID}-AC2 | {criterion_2} | {verification_2} |
| ... | ... | ... |

---

## 5. Source Reference

> Extract from `{source_file}`

{condensed_relevant_content}

---

*Generated by epci-decompose — Project: {slug}*
```

## Edge Cases

### EC1: PRD Without Clear Structure

**Detection:** Less than 3 `##` headers or no "Phase/Step" patterns.

**Behavior:**
```
Document structure insufficient.

Proposed structuring:

## Proposed Structure

1. Phase Preparation (estimated: Xd)
   - ...

2. Phase Implementation (estimated: Xd)
   - ...

3. Phase Validation (estimated: Xd)
   - ...

Options: [Validate structure] [Modify] [Cancel]
```

### EC2: PRD Too Small

**Detection:** Total estimated effort < 3 days.

**Behavior:**
```
This document seems simple enough for a single EPCI session.

Estimated effort: {X} days
Recommendation: Use /epci-brief directly

/epci-brief @{file}
```

**No decomposition** — command ends.

### EC3: Sub-Spec Too Large

**Detection:** A sub-spec exceeds `--max-days`.

**Behavior:**
```
ALERT: Sub-spec {ID} too large ({X} days estimated)

Suggestion: Split {ID} into sub-parts:
  {ID}a: {title_a} ({Xa}d)
  {ID}b: {title_b} ({Xb}d)

Options:
[1] Apply sub-decomposition
[2] Keep {ID} as is
[3] Define manually
```

### EC4: Circular Dependency

**Detection:** Cycle in dependency graph.

**Behavior:**
```
ERROR: Circular dependency detected

{SA} {SB} {SA}

This indicates an error in the source document.

Document references:
  Line {X}: "{quote_1}"
  Line {Y}: "{quote_2}"

Options:
[1] Ignore {SA}{SB}
[2] Ignore {SB}{SA}
[3] Cancel — Fix source document
```

### EC5: Missing Estimates

**Detection:** No estimation patterns found.

**Behavior:**
```
No estimates found in document

Using default estimates based on:
  Lines per section
  Detected complexity (models, services, tests)

Estimates are indicative. Adjust if needed.
```

## Examples

### Example 1: Standard Usage

```
> /epci-decompose migration_architecture_gardel.md

📄 Document: migration_architecture_gardel.md
├── Lines: 1738
├── Slug: migration-gardel
└── Status: Valid

[Analysis in progress...]

⏸️  BREAKPOINT — VALIDATION DÉCOUPAGE

📋 DÉCOUPAGE PROPOSÉ: 9 sous-specs

| ID  | Nom                    | Effort | Dépendances |
|-----|------------------------|--------|-------------|
| S01 | Settings Splitting     | 1j     | —           |
| S02 | App Datawarehouse      | 1j     | S01         |
| S03 | Modèles Base           | 2j     | S02         |
| S04 | Modèles Analyses       | 2j     | S03         |
| S05 | Modèles Sources        | 2j     | S03         |
| S06 | Modèles Users          | 2j     | S03         |
| S07 | Admin + Services       | 3j     | S04,S05,S06 |
| S08 | Migration ETL          | 2j     | S07         |
| S09 | Tests + Docs           | 2j     | S08         |

Duration: 17 days (parallel) vs 25 days (sequential)

> Valider

docs/specs/migration-gardel/
├── INDEX.md
├── S01-settings-splitting.md
├── S02-app-datawarehouse.md
├── S03-modeles-base.md
├── S04-modeles-analyses.md
├── S05-modeles-sources.md
├── S06-modeles-users.md
├── S07-admin-services.md
├── S08-migration-etl.md
└── S09-tests-documentation.md
```

### Example 2: With Custom Options

```
> /epci-decompose mon-prd.md --output specs/alpha/ --min-days 2 --max-days 4 --think think-hard

[Deep analysis with think-hard...]
[Granularity adjusted to 2-4 days per spec...]
```

### Example 3: Small Document (Auto-Redirect)

```
> /epci-decompose simple-feature.md

This document seems simple enough for a single EPCI session.

Estimated effort: 2 days
Recommendation: Use /epci-brief directly

/epci-brief @simple-feature.md
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Path incorrect or file missing | Check path, use absolute path |
| Not a .md file | Wrong file type | Provide a Markdown file |
| Circular dependency | Document has conflicting prerequisites | Fix source document or ignore one direction |
| No structure detected | Document lacks headers/organization | Accept proposed structure or restructure manually |

## See Also

- `/epci-brief` — Entry point for individual sub-specs after decomposition
- `/epci` — Complete workflow for STANDARD/LARGE features
- `/epci-quick` — Fast workflow for TINY/SMALL sub-specs
