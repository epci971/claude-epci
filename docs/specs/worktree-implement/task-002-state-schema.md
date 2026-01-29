---
id: task-002
title: Extend state.json schema
slug: state-schema
feature: worktree-implement
complexity: S
estimated_minutes: 60
dependencies: []
files_affected:
  - path: src/schemas/feature-state-v1.json
    action: modify
  - path: src/skills/core/state-manager/references/examples.md
    action: modify
test_approach: Unit
---

## Objective

Extend the feature state schema to include worktree metadata, enabling session persistence and `--continue` support for worktree-enabled implementations.

## Context

The state-manager persists feature state in `.epci/features/{slug}/state.json`. To support worktrees, we need a new `worktree` field that tracks:
- Whether worktree is enabled for this feature
- Path to the worktree directory
- Associated branch name
- Current status (active, merged, abandoned)

This enables `--continue` to automatically change to the correct worktree directory.

## Acceptance Criteria

### AC1: Schema Extension
- **Given**: The existing feature-state-v1.json schema
- **When**: The schema is updated
- **Then**:
  - New optional `worktree` object field is added
  - Field contains: `enabled`, `path`, `branch`, `status`, `created_at`
  - Schema validates correctly (jsonschema validation passes)

### AC2: State Manager Support
- **Given**: A state.json with worktree field
- **When**: State manager loads the state
- **Then**:
  - Worktree metadata is accessible
  - Missing worktree field defaults to `{"enabled": false}`
  - Backward compatible with existing state files

### AC3: Example Documentation
- **Given**: The state-manager examples
- **When**: Examples are updated
- **Then**:
  - New example shows worktree-enabled state
  - Example shows all worktree field options

## Steps

### Step 1: Update feature-state-v1.json schema (20 min)

**Input**: Current schema structure, worktree requirements

**Actions**:
1. Read current `src/schemas/feature-state-v1.json`
2. Add `worktree` property to schema:
```json
"worktree": {
  "type": "object",
  "properties": {
    "enabled": { "type": "boolean" },
    "path": { "type": "string" },
    "branch": { "type": "string" },
    "status": { "enum": ["active", "merged", "abandoned"] },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "required": ["enabled"],
  "additionalProperties": false
}
```
3. Mark `worktree` as optional (not in required array)
4. Validate schema is valid JSON Schema

**Output**: Updated schema file

**Validation**:
- JSON parses correctly
- Schema self-validates

### Step 2: Update state-manager examples (20 min)

**Input**: Updated schema, example format

**Actions**:
1. Read `src/skills/core/state-manager/references/examples.md`
2. Add new example section "State with Worktree":
```json
{
  "feature_slug": "auth-oauth",
  "complexity": "STANDARD",
  "current_phase": "code",
  "worktree": {
    "enabled": true,
    "path": "../worktrees/auth-oauth",
    "branch": "feature/auth-oauth",
    "status": "active",
    "created_at": "2026-01-29T10:00:00Z"
  }
}
```
3. Add example "State without Worktree (default)":
```json
{
  "feature_slug": "quick-fix",
  "complexity": "SMALL",
  "worktree": {
    "enabled": false
  }
}
```
4. Document status transitions: active → merged | abandoned

**Output**: Updated examples documentation

**Validation**:
- Examples match schema
- All status values documented

### Step 3: Verify backward compatibility (20 min)

**Input**: Existing state files, updated schema

**Actions**:
1. Find existing state.json files in `.epci/features/`
2. Validate each against updated schema (should pass - worktree optional)
3. Test loading state without worktree field
4. Verify default behavior: `worktree?.enabled ?? false`
5. Document migration notes if needed (none expected)

**Output**: Verification report

**Validation**:
- All existing states validate
- No breaking changes

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/schemas/feature-state-v1.json` | modify | Add worktree field to schema |
| `src/skills/core/state-manager/references/examples.md` | modify | Add worktree examples |

## Test Approach

- **Type**: Unit
- **Framework**: JSON Schema validation
- **Location**: Manual validation / script
- **Coverage Target**: All new fields validated

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | Schema validates with worktree | Unit | High |
| 2 | Schema validates without worktree | Unit | High |
| 3 | Invalid worktree.status rejected | Unit | Medium |
| 4 | Existing states remain valid | Unit | High |

## Dependencies

### Requires (blockedBy)
- None (foundation task)

### Blocks (blocks)
- **task-003**: step-00c-worktree needs state persistence
