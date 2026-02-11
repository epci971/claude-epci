---
id: task-002
title: Implement Notion API client library
slug: notion-api
feature: openclaw
complexity: L
estimated_minutes: 120
dependencies: []
files_affected:
  - path: lib/notion.sh
    action: create
  - path: tests/test-notion.sh
    action: create
test_approach: Unit
---

# Task 002: Implement Notion API client library

## Objective

Implement a pure curl/jq Notion API client library that handles querying tasks, updating properties, reading page body blocks (with Markdown conversion), and creating new pages. This library is the data layer for the entire pipeline, used by both run-task.sh and pipeline-runner.sh.

---

## Context

The pipeline uses Notion as the source of truth (D1r). All Notion interactions use curl/jq (D2, no MCP, no SDK). The database "OpenClawTasks" has 16 properties (section 4.1). The API version is fixed at `2022-06-28`. Rate limit is 3 req/s. Pagination via `next_cursor` for > 100 results.

Key decisions from brief:
- D1r: Specs in Notion body by default, Git optional (if Spec Path set)
- D2: curl/jq pure — no MCP, no Python SDK
- Section 4.1: Full schema with 16 properties
- API version: 2022-06-28

---

## Acceptance Criteria

### AC1: Query tasks with filter and sort

- **Given**: A configured NOTION_API_KEY and NOTION_DB_ID
- **When**: `notion_query` is called with filter `{"property": "Statut", "select": {"equals": "A faire"}}`
- **Then**: Returns JSON array of matching tasks with all properties, sorted by Priorite, handling pagination if > 100 results

### AC2: Update task properties

- **Given**: A valid Notion page ID and properties to update
- **When**: `notion_update "page_id" '{"Statut": {"select": {"name": "En cours"}}}'` is called
- **Then**: The page properties are updated via PATCH and the function returns the updated page JSON

### AC3: Read page body and convert to Markdown

- **Given**: A Notion page with body content (paragraphs, headings, lists, code blocks)
- **When**: `notion_read_body "page_id"` is called
- **Then**: Returns Markdown text converted from Notion blocks (paragraph, heading_1/2/3, bulleted_list_item, numbered_list_item, code, divider), handling pagination via next_cursor

### AC4: Create new page with properties and content

- **Given**: A database ID, page properties, and body content as Markdown
- **When**: `notion_create_page` is called
- **Then**: A new page is created in the database with correct properties and body blocks

---

## Steps

### Step 1: Implement notion_query — Database query with pagination (30 min)

**Input**: Notion API documentation for POST /v1/databases/{id}/query

**Actions**:
1. Implement `notion_query()` accepting database_id, filter JSON, and optional sorts JSON
2. Set headers: `Authorization: Bearer $NOTION_API_KEY`, `Notion-Version: 2022-06-28`, `Content-Type: application/json`
3. Handle pagination: loop while `has_more == true`, accumulate results using `next_cursor`
4. Return merged JSON array of all pages
5. Add rate limit awareness: sleep 0.35s between paginated requests

**Output**: `notion_query` function in lib/notion.sh

**Validation**: Query returns correctly filtered results from test database

### Step 2: Implement notion_update — Property PATCH (30 min)

**Input**: Notion API documentation for PATCH /v1/pages/{id}

**Actions**:
1. Implement `notion_update()` accepting page_id and properties JSON
2. Build PATCH request body with `{"properties": {...}}`
3. Handle HTTP errors (401, 404, 429) with appropriate messages
4. Return updated page JSON on success
5. Add retry logic for 429 (rate limit): wait 1s and retry once

**Output**: `notion_update` function in lib/notion.sh

**Validation**: Successfully updates a test page property

### Step 3: Implement notion_read_body — Block reading with Markdown conversion (30 min)

**Input**: Notion API documentation for GET /v1/blocks/{id}/children

**Actions**:
1. Implement `notion_read_body()` accepting page_id
2. Fetch all child blocks with pagination (next_cursor)
3. Convert blocks to Markdown using jq:
   - `paragraph` → plain text with rich_text extraction
   - `heading_1/2/3` → `#`, `##`, `###`
   - `bulleted_list_item` → `- text`
   - `numbered_list_item` → `1. text`
   - `code` → fenced code block with language
   - `divider` → `---`
   - `to_do` → `- [ ] text` / `- [x] text`
4. Handle nested rich_text (bold, italic, code, links)
5. Return concatenated Markdown string

**Output**: `notion_read_body` function with block-to-Markdown conversion

**Validation**: Known Notion page body converts to expected Markdown output

### Step 4: Implement notion_create_page — Page creation with body (30 min)

**Input**: Notion API documentation for POST /v1/pages

**Actions**:
1. Implement `notion_create_page()` accepting database_id, properties JSON, and optional body Markdown
2. Build request with `{"parent": {"database_id": ...}, "properties": {...}, "children": [...]}`
3. Convert Markdown to Notion blocks (reverse of step 3) for the `children` array
4. Handle property types: title, select, text, url, number, date, checkbox, relation
5. Return created page JSON (including page_id)
6. Write unit tests for all functions with mock curl responses

**Output**: `notion_create_page` function and test file

**Validation**: Creates a test page with correct properties and body content

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `lib/notion.sh` | create | Notion API client (query, update, read_body, create_page) |
| `tests/test-notion.sh` | create | Unit tests with mock curl responses |

---

## Test Approach

- **Type**: Unit
- **Framework**: bats or inline test functions with mock curl
- **Location**: tests/test-notion.sh
- **Coverage Target**: 85%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | notion_query returns filtered results | Unit | High |
| 2 | notion_query handles pagination (2 pages) | Unit | High |
| 3 | notion_update patches property successfully | Unit | High |
| 4 | notion_update handles 404 error | Unit | Medium |
| 5 | notion_read_body converts headings to Markdown | Unit | High |
| 6 | notion_read_body converts lists to Markdown | Unit | High |
| 7 | notion_read_body handles code blocks | Unit | Medium |
| 8 | notion_create_page sends correct payload | Unit | High |
| 9 | notion_create_page handles rate limit (429) | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-005**: Task executor needs notion_query and notion_read_body
- **task-008**: Spec-to-Notion sync needs notion_create_page and notion_update

---

## Notes

- API version `2022-06-28` is pinned — do not upgrade without testing
- Rate limit: 3 requests/second — sleep 0.35s between requests in batch operations
- Rich text extraction from Notion blocks is the most complex part (nested annotations)
- The Markdown→Notion blocks conversion (for create_page) is simpler — only need basic block types

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
