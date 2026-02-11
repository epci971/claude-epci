---
id: task-008
title: Implement spec-to-Notion sync
slug: spec-notion-sync
feature: openclaw
complexity: L
estimated_minutes: 120
dependencies:
  - task-002
files_affected:
  - path: lib/notion-sync.sh
    action: create
  - path: tests/test-notion-sync.sh
    action: create
test_approach: Integration
---

# Task 008: Implement spec-to-Notion sync

## Objective

Implement the automatic sync from /spec output to Notion: after generating spec files (index.md, task-XXX.md, PRD.json), create corresponding pages in the Notion "OpenClawTasks" database with properties mapped from task frontmatter, spec content in the page body, and dependency relations between pages. This eliminates manual backlog population.

---

## Context

Decision D12 establishes that /spec writes directly to Notion after generating local files. The mapping from spec frontmatter to Notion properties is defined in section 4.8. The algorithm: (1) resolve project ID, (2) create all pages collecting page IDs, (3) patch dependency relations with resolved IDs. The Notion API uses curl/jq (D2). Graceful degradation: if Notion is unavailable, log WARNING and continue.

Key decisions from brief:
- D12: /spec sync direct to Notion, zero manual step
- D1r: Content written in page body (not property)
- D9: Dependencies as "Bloque par" relation (resolved after all pages created)
- Section 4.8: Full mapping table and sync algorithm

---

## Acceptance Criteria

### AC1: Pages created with correct properties

- **Given**: A /spec output with 5 task files and a PRD.json
- **When**: `sync_to_notion` is called with the spec directory path
- **Then**: 5 pages are created in the Notion database, each with: Name (title), Complexite (select), Priorite (select), Projet (relation), Statut "A faire", and Flags from brief/config

### AC2: Spec content written in page body

- **Given**: A task file with Objective, Context, Acceptance Criteria, and Steps sections
- **When**: The Notion page is created
- **Then**: The page body contains the full spec content as Notion blocks (headings, paragraphs, lists, code blocks)

### AC3: Dependencies created as relations

- **Given**: task-002 and task-003 depend on task-001
- **When**: All pages are created and dependency patching runs
- **Then**: Pages for task-002 and task-003 have "Bloque par" relation pointing to the page for task-001

### AC4: Graceful degradation

- **Given**: NOTION_API_KEY is not configured or API returns an error
- **When**: `sync_to_notion` is called
- **Then**: A WARNING is logged "Notion sync skipped: {reason}", local spec files are unaffected, and no error blocks the workflow

### AC5: Duplicate detection

- **Given**: A task with the same Name and Projet already exists in Notion
- **When**: `sync_to_notion` tries to create it
- **Then**: The existing page is skipped with WARNING "Task already exists: {name}", no duplicate is created

---

## Steps

### Step 1: Implement property mapping and page creation (30 min)

**Input**: Section 4.8 mapping table, task frontmatter format

**Actions**:
1. Create `lib/notion-sync.sh` sourcing `lib/common.sh`, `lib/config.sh`, `lib/notion.sh`
2. Implement `map_task_to_notion_properties()` accepting a task YAML frontmatter:
   - `title` → Name (title property)
   - `complexity` S/M/L → Complexite: Simple/Moyenne/Complexe
   - Priority from PRD.json → Priorite: P1/P2/P3
   - Project from config → Projet (relation using notion_project_id)
   - Default Statut → "A faire"
   - Flags from brief or config → Flags (multi_select)
3. Implement `create_task_page()` that calls `notion_create_page` with mapped properties
4. Collect returned page IDs for dependency resolution

**Output**: Property mapping and page creation functions

**Validation**: Created page has correct properties in Notion

### Step 2: Implement Markdown to Notion blocks conversion (30 min)

**Input**: Notion blocks API format, task file body content

**Actions**:
1. Implement `markdown_to_notion_blocks()` that converts task body Markdown to Notion block JSON:
   - `# Heading` → heading_1 block
   - `## Heading` → heading_2 block
   - `### Heading` → heading_3 block
   - Plain text → paragraph block
   - `- item` → bulleted_list_item block
   - `1. item` → numbered_list_item block
   - ` ```code``` ` → code block with language
   - `---` → divider block
   - `**bold**` → bold annotation in rich_text
   - `` `code` `` → code annotation in rich_text
2. Handle the 100-block limit per API call: batch into multiple append calls
3. Parse YAML frontmatter (skip it, only convert body content)

**Output**: Markdown to Notion blocks converter

**Validation**: Sample task file body converts to correct Notion block JSON

### Step 3: Implement dependency resolution (30 min)

**Input**: Section 4.8 sync algorithm, D9 (Bloque par relation)

**Actions**:
1. Implement `resolve_dependencies()`:
   - Read PRD.json to get task dependency graph
   - Build map: task-ID → Notion page-ID (from step 1 page creation results)
   - For each task with dependencies: PATCH the "Bloque par" relation property
   - Use `notion_update` to add relation links
2. Implement `check_existing_tasks()`:
   - Query Notion for tasks with matching Name + Projet
   - Return map of existing task names for duplicate detection
3. Handle edge cases:
   - Dependency on a task that failed to create → log WARNING, skip relation
   - Rate limiting during batch creation → sleep 0.35s between creates (Notion 3 req/s)

**Output**: Dependency resolution and duplicate detection

**Validation**: Relations correctly link dependent pages

### Step 4: Implement main sync function and tests (30 min)

**Input**: Full sync algorithm from section 4.8

**Actions**:
1. Implement `sync_to_notion()` main function:
   ```
   0. Check NOTION_API_KEY and NOTION_DB_ID → skip with WARNING if missing
   1. Resolve notion_project_id from projects.json
   2. Check for existing tasks (duplicate detection)
   3. Parse all task-XXX.md files from spec directory
   4. Create pages (collecting page IDs), skipping duplicates
   5. Resolve and patch dependencies
   6. Log "{N} tasks created in Notion for {feature-slug}"
   ```
2. Add `--skip-notion-sync` flag support for manual override
3. Write integration tests with mock Notion API responses
4. Test: successful sync, duplicate detection, missing API key, dependency resolution

**Output**: Complete sync module with tests

**Validation**: Full sync flow works with mock API

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `lib/notion-sync.sh` | create | Spec-to-Notion sync (property mapping, blocks conversion, dependency resolution) |
| `tests/test-notion-sync.sh` | create | Integration tests with mock Notion API |

---

## Test Approach

- **Type**: Integration
- **Framework**: bats or inline test functions
- **Location**: tests/test-notion-sync.sh
- **Coverage Target**: 80%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | map_task_to_notion_properties maps all fields correctly | Unit | High |
| 2 | markdown_to_notion_blocks converts headings | Unit | High |
| 3 | markdown_to_notion_blocks converts lists and code | Unit | High |
| 4 | resolve_dependencies patches correct relations | Integration | High |
| 5 | sync_to_notion skips when NOTION_API_KEY missing | Unit | High |
| 6 | Duplicate task detected and skipped | Integration | Medium |
| 7 | Rate limiting handled during batch creation | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-002**: Needs lib/notion.sh for notion_create_page, notion_update, notion_query

### Blocks

*No other tasks depend on this one*

---

## Notes

- The sync is a "push-only" operation (spec → Notion). Bidirectional sync (Notion → Git) is deferred to V2
- Rate limit: create 1 page every 0.35s = ~170 pages/minute — more than enough for any batch
- The Markdown→Notion blocks conversion doesn't need to be perfect — cover the main block types used in task files
- Consider adding a `--notion-sync-only` flag to re-run sync without regenerating specs

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
