---
description: >-
    Decompose a complex PRD/CDC into actionable sub-specifications (1-5 days each).
    Generates dependency graph, Gantt planning, backlog table, and prd.json for Ralph execution.
    Use for large projects (>5 days) before running /brief on each sub-spec or /ralph for autonomous execution.
argument-hint: "<file.md> [--output <dir>] [--think <level>] [--min-days <n>] [--max-days <n>] [--granularity <size>]"
allowed-tools: [Read, Write, Bash, Grep, Glob, Task, WebFetch]
---

# EPCI Decompose

## Overview

Automates the decomposition of complex PRD/CDC documents into actionable sub-specifications.
Each sub-spec targets 1-5 days of effort, enabling iterative EPCI execution.

**Generates automatically:**
- Sub-spec files (S01-SNN.md)
- INDEX.md with dependency graph and Gantt planning
- **backlog.md** — Structured backlog table (Architector/Orchestrator style)
- **prd.json** — User stories for Ralph autonomous execution
- **ralph.sh** — Executable loop script
- **PROMPT.md** — Customized prompt for Claude

**Use case:** A 25-day migration project becomes 9 manageable sub-specs that can be
executed via `/brief` (manual) or `/ralph` (autonomous overnight).

## Arguments

| Argument          | Description                                                  | Required | Default              |
| ----------------- | ------------------------------------------------------------ | -------- | -------------------- |
| `<file.md>`       | Source PRD/CDC file to decompose                             | Yes      | —                    |
| `--output <dir>`  | Output directory for generated specs                         | No       | `docs/specs/{slug}/` |
| `--think <level>` | Thinking level: `quick`, `think`, `think-hard`, `ultrathink` | No       | `think`              |
| `--min-days <n>`  | Minimum effort per sub-spec                                  | No       | `1`                  |
| `--max-days <n>`  | Maximum effort per sub-spec                                  | No       | `5`                  |
| `--granularity`   | Story size: `micro` (15-30min), `small` (30-60min), `standard` (1-2h) | No | `small`            |

## Pre-Workflow: Load Project Memory

**Skill**: `project-memory`

Load project context from `.project-memory/` before analysis. The skill handles:

- Reading context, conventions, settings, patterns
- Finding similar past decompositions for reference
- Applying project-specific naming conventions to generated specs

**If `.project-memory/` does not exist:** Continue with defaults.

---

## Process

**IMPORTANT: Follow ALL phases in sequence. Do NOT skip the file generation step.**

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
Document: {filename}
├── Lines: {count}
├── Slug: {extracted_slug}
└── Status: Valid
```

### Phase 2: Structural Analysis (MANDATORY)

**DO NOT SKIP:** Analyze the document structure and detect dependencies.

**Skills loaded:** `architecture-patterns`, `flags-system`

**Structure detection:**

| Signal                          | Usage                            |
| ------------------------------- | -------------------------------- |
| Headers `## Phase X`            | Level 1 decomposition candidates |
| Headers `### Step X.Y`          | Sub-decomposition candidates     |
| Headers `### US[N] —`           | User Story → sub-spec candidate  |
| `**Complexite**: S/M/L`         | Effort estimate (S=1d, M=3d, L=5d) |
| `**Priorite**: Must-have`       | Execution priority (MoSCoW)      |
| Tables with "Effort"            | Reuse existing estimates         |
| "Checklist" sections            | Validation boundaries            |
| "Gate", "Prerequisite" mentions | Explicit dependencies            |

**Dependency extraction:**

| Pattern    | Detection                                    |
| ---------- | -------------------------------------------- |
| Explicit   | "depends on", "requires", "after", "before"  |
| Django FK  | `ForeignKey('app.Model')` → model must exist |
| Imports    | `from X import Y` → Y must exist             |
| References | `see S01`, `cf. Phase 1`                     |

**Granularity rules:**

| Block effort         | Action                    |
| -------------------- | ------------------------- |
| < min-days           | Merge with adjacent block |
| min-days to max-days | Target granularity        |
| > max-days           | Seek sub-decomposition    |

**Input format detection:**

| Format | Detection | Behavior |
|--------|-----------|----------|
| PRD/CDC | `## Phase`, `### Step` headers | Standard decomposition |
| Brainstorm Brief | `### US[N] —` headers | User Story mapping |

**Invoke @decompose-validator:**

- Check dependency consistency
- Detect circular dependencies
- Validate granularity compliance

### Phase 3: Proposal (MANDATORY — WAIT FOR USER)

**MANDATORY:** Display the breakpoint and WAIT for user validation before proceeding.

Present decomposition proposal for user validation:

```
+---------------------------------------------------------------------+
| BREAKPOINT — VALIDATION DECOUPAGE                                    |
+---------------------------------------------------------------------+
|                                                                     |
| ANALYSE DE: {filename}                                              |
| ├── Lignes: {line_count}                                            |
| ├── Effort total detecte: {total_days} jours                        |
| └── Structure: {phases} phases, {steps} etapes                      |
|                                                                     |
| DECOUPAGE PROPOSE: {count} sous-specs                               |
|                                                                     |
| | ID  | Title        | Effort | Priority | Dependencies | Status  | |
| |-----|--------------|--------|----------|--------------|---------|  |
| | S01 | {name_1}     | {d1}j  | -        | -            | Pending | |
| | S02 | {name_2}     | {d2}j  | -        | S01          | Pending | |
| | ... | ...          | ...    | ...      | ...          | ...     | |
|                                                                     |
| PARALLELISATION: {parallel_count} specs parallelisables             |
| DUREE OPTIMISEE: {optimized_days}j (vs {sequential_days}j seq)      |
|                                                                     |
| ALERTES: {alerts_or_none}                                           |
|                                                                     |
| @decompose-validator: {verdict}                                     |
|                                                                     |
| Options:                                                            |
|   * "Valider" -> Generer les fichiers                               |
|   * "Modifier" -> Ajuster le decoupage                              |
|   * "Annuler" -> Abandonner                                         |
+---------------------------------------------------------------------+
```

**Modify option sub-menu:**

```
Que souhaitez-vous modifier ?

[1] Fusionner des specs — Ex: "Fusionner S04 et S05"
[2] Decouper une spec — Ex: "Decouper S07 en 2"
[3] Renommer — Ex: "S03 → Modeles Fondamentaux"
[4] Changer dependances — Ex: "S06 ne depend plus de S03"
[5] Ajuster estimation — Ex: "S08 = 3 jours"

Votre choix (ou texte libre):
```

### Phase 4: Generation (USE WRITE TOOL — MANDATORY)

**MANDATORY:** Use the **Write tool** to create ALL output files.

**Skills loaded:** `ralph-converter` (handles prd.json schema, stack detection, template generation)

#### Step 4.1: Create output directory

```bash
mkdir -p {output_dir}
```

#### Step 4.2: Generate sub-spec files

For each sub-spec identified:
- **S01-{slug}.md** through **SNN-{slug}.md** — Individual sub-specs

#### Step 4.3: Generate INDEX.md

Overview with:
- Summary table (ID, Title, Effort, Priority, Dependencies, Status)
- Mermaid dependency graph
- Mermaid Gantt planning

#### Step 4.4: Generate backlog.md (MANDATORY)

**Always generate** the backlog table with:
- Vue d'ensemble — All stories in one table
- Par Spec — Stories grouped by spec
- Statistiques — Totals, parallelizable count, critical path
- Par Priorite — P1/P2/P3 breakdown
- Legende — Status symbols, complexity, types

**Story attributes inferred:**
- **Type**: Script/Logic/API/UI/Test/Task (from title keywords)
- **Complexite**: S (<45min), M (45-90min), L (>90min)
- **Priorite**: P1 (Must), P2 (Should), P3 (Could)

See `references/decompose-templates.md` for full template.

#### Step 4.5: Generate prd.json v2 (MANDATORY)

Convert specs to Ralph Wiggum format using **schema v2** for granular tracking.

**Schema v2 structure:**

```json
{
  "$schema": "https://epci.dev/schemas/prd-v2.json",
  "version": "2.0",
  "branchName": "feature/{slug}",
  "projectName": "{Project Title}",
  "generatedAt": "{ISO date}",
  "generatedBy": "EPCI /decompose v5.2",
  "config": {
    "max_iterations": 50,
    "test_command": "{detected}",
    "lint_command": "{detected}",
    "granularity": "{granularity}"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "{title}",
      "category": "{inferred: backend|frontend|fullstack|infra|test|docs}",
      "type": "{inferred: Script|Logic|API|UI|Test|Task}",
      "complexity": "{inferred: S|M|L}",
      "priority": 1,
      "status": "pending",
      "passes": false,
      "acceptanceCriteria": [
        {"id": "AC1", "description": "{from spec}", "done": false}
      ],
      "tasks": [
        {"id": "T1", "description": "{from spec}", "done": false}
      ],
      "dependencies": {
        "depends_on": [],
        "blocks": []
      },
      "execution": {
        "attempts": 0,
        "last_error": null,
        "files_modified": [],
        "completed_at": null,
        "iteration": null
      },
      "testing": {
        "test_files": [],
        "requires_e2e": false,
        "coverage_target": null
      },
      "context": {
        "parent_spec": "{SXX-name.md}",
        "parent_brief": "{brief path}",
        "estimated_minutes": 60
      }
    }
  ]
}
```

**Inference rules** (see `ralph-converter` skill for details):

| Field | Inference source |
|-------|------------------|
| `category` | File patterns, title keywords |
| `type` | Title keywords (script/entity/api/component/test) |
| `complexity` | Estimated minutes or AC/task count |
| `acceptanceCriteria[]` | `## Acceptance Criteria` section in spec |
| `tasks[]` | `## Tasks` checklist in spec, or inferred from AC |
| `dependencies` | INDEX.md Dependencies column + "depends on" patterns |

**Granularity effects on story count:**

| Granularity | Story Size | Stories/Day |
|-------------|------------|-------------|
| `micro`     | 15-30 min  | 8-12        |
| `small`     | 30-60 min  | 4-8         |
| `standard`  | 1-2 hours  | 2-4         |

#### Step 4.6: Generate ralph.sh (MANDATORY)

Executable loop script for autonomous execution.

#### Step 4.7: Generate PROMPT.md (MANDATORY)

Customized prompt based on detected stack (Node.js, Python, PHP, etc.).

#### Step 4.8: Create symlinks

```bash
ln -s ../../scripts/lib {output_dir}/lib
```

**Final output structure:**

```
{output_dir}/
├── INDEX.md              # Overview with Mermaid diagrams
├── backlog.md            # Backlog table view
├── prd.json              # Ralph stories format
├── ralph.sh              # Executable loop script
├── PROMPT.md             # System prompt
├── progress.txt          # Empty logging file
├── lib/                  # Symlink to scripts/lib/
├── S01-{name}.md
├── S02-{name}.md
└── SNN-{name}.md
```

## Loaded Skills

| Skill                   | Phase        | Purpose                            |
| ----------------------- | ------------ | ---------------------------------- |
| `project-memory`        | Pre-Workflow | Load context and conventions       |
| `architecture-patterns` | Phase 2      | Identify decomposition patterns    |
| `flags-system`          | All          | Handle --think levels              |
| `ralph-converter`       | Phase 4      | Generate prd.json, ralph.sh, PROMPT.md |
| `mcp`                   | Phase 2      | Context7 for architecture patterns |

## Invoked Subagents

| Subagent               | Condition | Role                               |
| ---------------------- | --------- | ---------------------------------- |
| `@decompose-validator` | Always    | Validate decomposition consistency |

## Output Formats

**Complete templates:** See `references/decompose-templates.md` for:
- INDEX.md — Overview with Mermaid diagrams
- backlog.md — Structured backlog table
- SXX-{name}.md — Sub-spec template

## Edge Cases

**Detailed edge case handling:** See `references/decompose-edge-cases.md`

| Code | Situation | Action |
|------|-----------|--------|
| EC1 | PRD without clear structure | Propose structuring |
| EC2 | PRD too small (<3 days) | Redirect to /brief |
| EC3 | Sub-spec too large | Suggest split |
| EC4 | Circular dependency | Blocking alert |
| EC5 | Missing estimates | Default estimation |
| EC6 | Brainstorm brief format | User Story mapping |

## Examples

**Usage examples:** See `references/decompose-examples.md`

Quick reference:

```bash
# Standard usage — generates all files including backlog.md and prd.json
/decompose migration_architecture_gardel.md

# With custom options
/decompose mon-prd.md --output specs/alpha/ --min-days 2 --max-days 4

# With fine granularity for more stories
/decompose mon-prd.md --granularity micro
```

**Output:**
```
docs/specs/migration-gardel/
├── INDEX.md
├── backlog.md            ← Backlog table
├── prd.json              ← Ralph stories
├── ralph.sh              ← Executable script
├── PROMPT.md             ← System prompt
├── progress.txt
├── S01-settings-splitting.md
├── S02-app-datawarehouse.md
└── ...

→ Next: /ralph docs/specs/migration-gardel/
```

## Error Handling

| Error                 | Cause                                  | Solution                                          |
| --------------------- | -------------------------------------- | ------------------------------------------------- |
| File not found        | Path incorrect or file missing         | Check path, use absolute path                     |
| Not a .md file        | Wrong file type                        | Provide a Markdown file                           |
| Circular dependency   | Document has conflicting prerequisites | Fix source document or ignore one direction       |
| No structure detected | Document lacks headers/organization    | Accept proposed structure or restructure manually |

## See Also

- `/brief` — Entry point for individual sub-specs after decomposition
- `/epci` — Complete workflow for STANDARD/LARGE features
- `/quick` — Fast workflow for TINY/SMALL sub-specs
- `/ralph` — Autonomous overnight execution using generated prd.json
