---
id: task-001
title: Create Notion API client with query and update operations
slug: notion-api-client
feature: notion-runner
complexity: M
estimated_minutes: 120
dependencies: []
files_affected:
  - path: src/openclaw/__init__.py
    action: create
  - path: src/openclaw/config.py
    action: create
  - path: src/openclaw/notion_client.py
    action: create
  - path: src/openclaw/tests/__init__.py
    action: create
  - path: src/openclaw/tests/test_notion_client.py
    action: create
test_approach: Unit
---

# Task 001: Create Notion API client with query and update operations

## Objective

Implement the foundation of the OpenClaw project: the Python package structure, configuration module, and Notion API client with query and update capabilities. This provides the data layer that all other modules depend on, using only Python stdlib (urllib, json).

---

## Context

The OpenClaw runner needs to communicate with Notion's REST API to fetch tasks and update their status. Decision D1 mandates Python stdlib only (no requests, no pip dependencies). Decision D2 specifies urllib + NOTION_API_KEY environment variable for standalone operation without MCP.

The OpenClawTasks Notion database schema is defined in `src/schemas/notion-bdd-openClawTasks.json` with 24 properties including status mappings, priority levels, and bidirectional dependency relations.

Key constraints:
- Notion API version: 2022-06-28
- Rate limit: 3 requests/second (sleep 0.35s between batch calls)
- Pagination: max 100 results per query, use has_more/start_cursor

---

## Acceptance Criteria

### AC1: Query database with filtering

- **Given**: A valid NOTION_API_KEY and database ID
- **When**: `query_database` is called with a status filter "A faire"
- **Then**: Returns a list of task dicts with all Notion properties parsed

### AC2: Update page properties

- **Given**: A valid page ID and a properties dict (e.g., `{"Statut": "En cours"}`)
- **When**: `update_page` is called
- **Then**: The Notion page properties are updated via PATCH API call

### AC3: Pagination handling

- **Given**: A database query returns more than 100 results
- **When**: `query_database` is called
- **Then**: Pagination is handled automatically via has_more/start_cursor, returning all results

### AC4: Missing API key error

- **Given**: NOTION_API_KEY environment variable is not set
- **When**: Any API call is made
- **Then**: A clear ConfigError is raised with message "NOTION_API_KEY not set"

### AC5: Config loading with validation

- **Given**: A config.json with database_id and optional settings
- **When**: `load_config` is called
- **Then**: Returns config dict with defaults applied for optional fields (rate_limit_sleep=0.35, log_level="INFO")

---

## Steps

### Step 1: Create project structure and config module (20 min)

**Input**: Brief section 5 (module architecture), decision D5

**Actions**:
1. Create `src/openclaw/__init__.py` with module docstring
2. Create `src/openclaw/config.py` with:
   - `load_config(path)` — Read JSON config file, apply defaults
   - `get_notion_key()` — Read NOTION_API_KEY from env, raise ConfigError if missing
   - `ConfigError` exception class
3. Create `src/openclaw/tests/__init__.py`

**Output**: Package structure with config module

**Validation**: `from openclaw.config import load_config, get_notion_key` imports without error

### Step 2: Implement HTTP request helper with urllib (25 min)

**Input**: Notion API documentation, decision D1 (stdlib only)

**Actions**:
1. In `notion_client.py`, implement `_notion_request(method, endpoint, data=None)`
2. Build URL from `https://api.notion.com/v1/` + endpoint
3. Set headers: Authorization, Notion-Version (2022-06-28), Content-Type
4. Handle HTTP errors (non-2xx) with NotionAPIError exception
5. Parse JSON response with `json.loads`
6. Add rate limiting sleep (configurable, default 0.35s)

**Output**: HTTP helper function in notion_client.py

**Validation**: Function can be called with mock urllib (tested in step 5)

### Step 3: Implement query_database with pagination and filtering (25 min)

**Input**: Notion API POST /v1/databases/{id}/query documentation

**Actions**:
1. Implement `query_database(database_id, filter_obj=None, sorts=None)`
2. Build filter payload for Notion API format
3. Handle pagination loop: while `has_more`, add `start_cursor` to next request
4. Collect all results across pages
5. Return list of raw Notion page objects

**Output**: `query_database` function with full pagination

**Validation**: Returns correct results with mock multi-page responses

### Step 4: Implement update_page with property type mapping (25 min)

**Input**: Notion API PATCH /v1/pages/{id}, OpenClawTasks schema

**Actions**:
1. Implement `update_page(page_id, properties)`
2. Map high-level property dict to Notion API format:
   - `select` type: `{"Statut": {"select": {"name": "En cours"}}}`
   - `number` type: `{"Attempts": {"number": 3}}`
   - `text` type: `{"Erreurs": {"rich_text": [{"text": {"content": "..."}}]}}`
   - `checkbox` type: `{"Passes": {"checkbox": true}}`
   - `url` type: `{"PR URL": {"url": "https://..."}}`
   - `date` type: `{"Demarre le": {"date": {"start": "2026-02-13T..."}}}`
3. Reference `src/schemas/notion-bdd-openClawTasks.json` for property types

**Output**: `update_page` function with property type mapping

**Validation**: Correctly formats all property types for Notion API

### Step 5: Write unit tests with mock urllib (25 min)

**Input**: Functions from steps 1-4

**Actions**:
1. Create `test_notion_client.py`
2. Mock `urllib.request.urlopen` to return controlled responses
3. Test `query_database` with single-page and multi-page responses
4. Test `update_page` with various property types
5. Test error handling (HTTP errors, missing API key)
6. Test config loading with valid and invalid inputs

**Output**: Complete unit test file

**Validation**: All tests pass with `python -m pytest src/openclaw/tests/test_notion_client.py`

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/openclaw/__init__.py` | create | Package init with docstring |
| `src/openclaw/config.py` | create | Config loading and env var management |
| `src/openclaw/notion_client.py` | create | Notion API client (query, update, HTTP helper) |
| `src/openclaw/tests/__init__.py` | create | Test package init |
| `src/openclaw/tests/test_notion_client.py` | create | Unit tests for Notion client |

---

## Test Approach

- **Type**: Unit
- **Framework**: pytest (unittest.mock for urllib mocking)
- **Location**: src/openclaw/tests/test_notion_client.py
- **Coverage Target**: 90%

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Query database with status filter | Unit | High |
| 2 | Query with pagination (multi-page) | Unit | High |
| 3 | Update page with select property | Unit | High |
| 4 | Update page with all property types | Unit | Medium |
| 5 | HTTP error handling (4xx, 5xx) | Unit | High |
| 6 | Missing NOTION_API_KEY raises ConfigError | Unit | High |
| 7 | Config loading with defaults | Unit | Medium |
| 8 | Rate limiting sleep applied | Unit | Low |

---

## Dependencies

### Requires (blockedBy)

*No dependencies — this task can start immediately*

### Blocks

- **task-002**: Needs HTTP helper and query functions for page blocks reading
- **task-003**: Needs query_database for fetching eligible tasks
- **task-005**: Needs update_page for status transitions in main loop

---

## Notes

- Property type mapping should reference `src/schemas/notion-bdd-openClawTasks.json` to ensure correct format for each field
- Rate limiting is conservative (0.35s) to stay under Notion's 3 req/s limit
- The `_notion_request` helper should be reusable by task-002 (read_page_blocks, create_page)

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
