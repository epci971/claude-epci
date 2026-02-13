---
id: task-002
title: Implement Notion page blocks reading and page creation
slug: notion-blocks
feature: notion-runner
complexity: M
estimated_minutes: 90
dependencies:
  - task-001
files_affected:
  - path: src/openclaw/notion_client.py
    action: modify
  - path: src/openclaw/tests/test_notion_blocks.py
    action: create
test_approach: Unit
---

# Task 002: Implement Notion page blocks reading and page creation

## Objective

Extend the Notion API client with page body reading (blocks-to-Markdown conversion) and page creation capabilities. These functions are required by the PRD injector (task-006) to create task pages in Notion and by the runner to read spec content from Notion page bodies (decision D6: Spec Path > body Notion).

---

## Context

Decision D6 establishes that spec content is sourced from Git files first (Spec Path property), with fallback to Notion page body. The `read_page_body` function converts Notion blocks to Markdown for use as implement-auto spec input.

Decision D10 requires these libs to be reusable by `/spec` for PRD-to-Notion injection. The `create_page` function must support both properties and body content.

Notion blocks API: GET /v1/blocks/{block_id}/children (paginated, max 100 per request). Page creation: POST /v1/pages with parent, properties, and children (body blocks).

---

## Acceptance Criteria

### AC1: Read page body as Markdown

- **Given**: A Notion page with blocks (headings, paragraphs, bulleted lists, to-do items, code blocks)
- **When**: `read_page_body(page_id)` is called
- **Then**: Returns Markdown string with correct formatting:
  - heading_1 → `# Title`
  - heading_2 → `## Title`
  - heading_3 → `### Title`
  - paragraph → plain text with newline
  - bulleted_list_item → `- item`
  - to_do → `- [ ] item` / `- [x] item`
  - code → triple-backtick block with language

### AC2: Create page with properties and body

- **Given**: A database ID, properties dict, and body content as Markdown string
- **When**: `create_page(database_id, properties, body_markdown)` is called
- **Then**: A new page is created with correct properties and body blocks

### AC3: Blocks pagination

- **Given**: A page body with more than 100 blocks
- **When**: `read_page_body` is called
- **Then**: Pagination is handled automatically via has_more/start_cursor

---

## Steps

### Step 1: Implement read_page_blocks with pagination (25 min)

**Input**: Notion blocks API documentation, `_notion_request` from task-001

**Actions**:
1. Implement `read_page_blocks(page_id)` using GET /v1/blocks/{page_id}/children
2. Handle pagination (has_more/start_cursor loop)
3. Return list of raw block objects

**Output**: `read_page_blocks` function in notion_client.py

**Validation**: Returns all blocks from a multi-page mock response

### Step 2: Implement blocks_to_markdown converter (25 min)

**Input**: Notion block types specification

**Actions**:
1. Implement `blocks_to_markdown(blocks)` converter
2. Handle block types:
   - `heading_1`, `heading_2`, `heading_3` → `#`, `##`, `###`
   - `paragraph` → plain text
   - `bulleted_list_item` → `- item`
   - `numbered_list_item` → `1. item`
   - `to_do` → `- [ ] item` / `- [x] item`
   - `code` → triple-backtick block with language
   - `divider` → `---`
3. Handle rich_text formatting (bold, italic, code inline)
4. Combine into `read_page_body(page_id)` convenience function

**Output**: Markdown conversion functions

**Validation**: Known block structures produce expected Markdown output

### Step 3: Implement create_page with properties and body (25 min)

**Input**: Notion POST /v1/pages documentation, OpenClawTasks schema

**Actions**:
1. Implement `markdown_to_blocks(markdown_text)` — basic Markdown to Notion blocks
   - `# Title` → heading_1
   - `## Title` → heading_2
   - `- item` → bulleted_list_item
   - `- [ ] item` → to_do (unchecked)
   - Plain text → paragraph
2. Implement `create_page(database_id, properties, body_markdown=None)`
   - Build payload with parent, properties (reuse mapping from task-001), children (blocks)
   - POST /v1/pages
   - Return created page object with id

**Output**: `create_page` and `markdown_to_blocks` functions

**Validation**: Creates page with correct JSON payload structure

### Step 4: Write unit tests (15 min)

**Input**: Functions from steps 1-3

**Actions**:
1. Test `blocks_to_markdown` with various block types
2. Test `markdown_to_blocks` round-trip
3. Test `create_page` payload construction
4. Test pagination in `read_page_blocks`

**Output**: Complete test file

**Validation**: All tests pass

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/notion_client.py` | modify | Add read_page_blocks, blocks_to_markdown, create_page, markdown_to_blocks |
| `src/openclaw/tests/test_notion_blocks.py` | create | Unit tests for blocks and page creation |

---

## Test Approach

- **Type**: Unit
- **Framework**: pytest (unittest.mock)
- **Location**: src/openclaw/tests/test_notion_blocks.py
- **Coverage Target**: 85%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Convert heading blocks to Markdown | Unit | High |
| 2 | Convert bulleted_list and to_do blocks | Unit | High |
| 3 | Convert code block with language | Unit | Medium |
| 4 | Handle rich_text formatting (bold, italic) | Unit | Medium |
| 5 | Pagination in read_page_blocks | Unit | High |
| 6 | Create page with properties and body | Unit | High |
| 7 | Markdown to blocks conversion | Unit | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-001**: Needs `_notion_request` HTTP helper and property type mapping

### Blocks

- **task-006**: PRD injector needs `create_page` for Notion page creation

---

## Notes

- The Markdown-to-blocks converter doesn't need to handle all Markdown features — just the subset used in EPCI specs (headings, lists, checkboxes, code blocks, paragraphs)
- Rich text formatting in blocks uses an array of text objects with annotations (bold, italic, code, etc.)
- Block children are limited to simple types — no nested blocks for MVP

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
