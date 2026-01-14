---
description: >-
    Decompose a complex PRD/CDC into actionable sub-specifications (1-5 days each).
    Generates dependency graph, Gantt planning, backlog table, and prd.json for Ralph execution.
    Use for large projects (>5 days) before running /brief on each sub-spec or ./ralph.sh for autonomous execution.
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
- **ralph.sh** — Executable loop script calling `/epci:ralph-exec`
- **progress.txt** — Empty file for iteration logging

**Use case:** A 25-day migration project becomes 9 manageable sub-specs that can be
executed via `/brief` (manual) or `./ralph.sh` (autonomous overnight).

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

Executable loop script calling `/epci:ralph-exec` for each story.

**Template:**

```bash
#!/bin/bash
# Ralph loop — generated by /decompose
# Run this script directly in terminal for context liberation between stories
#
# Usage:
#   ./ralph.sh              # Verbose output (default)
#   ./ralph.sh --quiet      # Minimal output
#   ./ralph.sh --dry-run    # Show stories without executing
#   ./ralph.sh --help       # Show help
#
# To stop: Ctrl+C
set -e

# Configuration
MAX_ITERATIONS=${MAX_ITERATIONS:-50}
PRD_FILE="./prd.json"
PROGRESS_FILE="./progress.txt"

# Verbose mode is ON by default
VERBOSE=${VERBOSE:-true}
DRY_RUN=false

# Lib directory (for response_analyzer, etc.)
LIB_DIR="/home/epci/apps/claude-epci/src/scripts/lib"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Help function
show_help() {
    cat << EOF
Ralph Wiggum — Autonomous Executor
Usage: ./ralph.sh [OPTIONS]
Options:
    -q, --quiet      Disable verbose output
    --dry-run        Show pending stories without executing
    -h, --help       Show this help
EOF
}

# Argument parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet) VERBOSE=false; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Source libs if available
[[ -f "$LIB_DIR/date_utils.sh" ]] && source "$LIB_DIR/date_utils.sh"
[[ -f "$LIB_DIR/response_analyzer.sh" ]] && source "$LIB_DIR/response_analyzer.sh" && HAS_ANALYZER=true || HAS_ANALYZER=false

# Progress bar
show_progress_bar() {
    local c=$1 t=$2 w=40
    [[ $t -eq 0 ]] && return
    local p=$((c * 100 / t)) f=$((c * w / t))
    printf "[%-${w}s] %d%% (%d/%d)\n" "$(printf '#%.0s' $(seq 1 $f))" "$p" "$c" "$t"
}

# Time tracking
START_TIME=$(date +%s)
get_elapsed() { local e=$(($(date +%s) - START_TIME)); printf "%02d:%02d:%02d" $((e/3600)) $((e%3600/60)) $((e%60)); }
STORY_START=0
start_story_timer() { STORY_START=$(date +%s); }
get_story_time() { local e=$(($(date +%s) - STORY_START)); printf "%02d:%02d" $((e/60)) $((e%60)); }

echo "========================================"
echo "  Ralph Wiggum — Autonomous Executor"
[[ "$VERBOSE" == "true" ]] && echo -e "         ${CYAN}[VERBOSE MODE]${NC}"
echo "========================================"
echo "PRD: $PRD_FILE"
echo "Max iterations: $MAX_ITERATIONS"
echo ""

# Validation
[[ ! -f "$PRD_FILE" ]] && echo -e "${RED}Error: PRD not found${NC}" && exit 1

# Dry run
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${CYAN}=== DRY RUN ===${NC}"
    jq -r '.userStories[] | select(.passes==false) | "  - \(.id) — \(.title)"' "$PRD_FILE"
    exit 0
fi

echo "[$(date -Iseconds)] Ralph started" >> "$PROGRESS_FILE"

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    PENDING=$(jq '[.userStories[] | select(.passes==false and .status!="blocked")] | length' "$PRD_FILE")
    COMPLETED=$(jq '[.userStories[] | select(.passes==true)] | length' "$PRD_FILE")
    TOTAL=$(jq '.userStories | length' "$PRD_FILE")

    [[ "$PENDING" -eq 0 ]] && echo -e "${GREEN}All stories complete!${NC}" && exit 0

    NEXT_STORY=$(jq -r '[.userStories[] | select(.passes==false and .status!="blocked")][0].id' "$PRD_FILE")
    NEXT_TITLE=$(jq -r '[.userStories[] | select(.passes==false and .status!="blocked")][0].title' "$PRD_FILE")

    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "\n${BLUE}+--------------------------------------------------------------------+${NC}"
        echo -e "${BLUE}|        Story Execution — Iteration $i                              |${NC}"
        echo -e "${BLUE}+--------------------------------------------------------------------+${NC}"
        echo -e "${YELLOW}Story:${NC}   $NEXT_STORY"
        echo -e "${YELLOW}Title:${NC}   $NEXT_TITLE"
        echo -e "${YELLOW}Elapsed:${NC} $(get_elapsed)"
        show_progress_bar "$COMPLETED" "$TOTAL"
    else
        echo -e "\n${YELLOW}=== Iteration $i ===${NC}"
        echo "Progress: $COMPLETED/$TOTAL, Next: $NEXT_STORY"
    fi

    start_story_timer
    # Use tee to show output in real-time AND capture for analysis
    OUTPUT_FILE=$(mktemp)
    claude --dangerously-skip-permissions --verbose "/epci:ralph-exec --prd $PRD_FILE" 2>&1 | tee "$OUTPUT_FILE" || true
    OUTPUT=$(cat "$OUTPUT_FILE")

    # Verbose: analyze response
    if [[ "$VERBOSE" == "true" && "$HAS_ANALYZER" == "true" ]]; then
        analyze_response "$OUTPUT_FILE" "$i" ".analysis_$i" 2>/dev/null && log_analysis_summary ".analysis_$i" 2>/dev/null
        rm -f ".analysis_$i"
        echo -e "${YELLOW}Duration:${NC} $(get_story_time)"
    fi
    rm -f "$OUTPUT_FILE"

    # Check signals
    if echo "$OUTPUT" | grep -q '<promise>STORY_DONE</promise>'; then
        echo -e "${GREEN}Story $NEXT_STORY completed${NC}"
    elif echo "$OUTPUT" | grep -q '<promise>ALL_DONE</promise>'; then
        echo -e "${GREEN}All complete!${NC}"; exit 0
    else
        echo -e "${RED}Story $NEXT_STORY failed${NC}"
    fi

    sleep 2
done

echo -e "${RED}Max iterations reached${NC}"
exit 1
```

**Key design:**
- Each `claude "/epci:ralph-exec"` call = fresh context (memory liberation)
- No PROMPT.md needed — workflow is inline in /epci:ralph-exec
- Simple promise tag detection for completion
- **Autonomous mode**: `--dangerously-skip-permissions` enables overnight execution

**Security considerations:**
- The script uses `--dangerously-skip-permissions` for autonomous execution
- **Recommended safeguards:**
  - Run in Docker container without network access
  - Use Git worktree to isolate changes
  - Review changes before merging to main branch
  - Never run on production branches directly

#### Step 4.7: Create progress.txt (MANDATORY)

Create empty progress.txt file for iteration logging:

```bash
touch {output_dir}/progress.txt
```

The `/epci:ralph-exec` command will append iteration logs to this file.

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
├── ralph.sh              # Executable loop script (calls /epci:ralph-exec)
├── progress.txt          # Empty logging file
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
- `/epci:ralph-exec` — Single story executor (called by ralph.sh)

## Autonomous Execution

After decomposition, run overnight execution directly from terminal:

```bash
cd {output_dir}
./ralph.sh
```

**Key benefit:** Each `claude "/epci:ralph-exec"` call creates fresh context, enabling
long-running sessions without memory issues.
