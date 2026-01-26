# PRD Schema Reference

> Machine-readable specification format for Ralph execution.

## Overview

The PRD.json file is a JSON representation of the specification, designed for:
- Ralph batch execution
- Automated tooling
- Progress tracking
- Dependency analysis

**Key Principle:** PRD.json is generated from Markdown sources. Never edit PRD.json directly — modify task-XXX.md files and regenerate.

## Schema Version

Current: `2.0`

Location: `src/schemas/prd-v2.json`

## Root Structure

```json
{
  "title": "Feature Title",
  "version": "2.0",
  "slug": "feature-slug",
  "generated_at": "2026-01-26T10:30:00Z",
  "source": "docs/briefs/feature/brief.md",
  "complexity": "STANDARD",
  "metrics": { ... },
  "tasks": [ ... ],
  "dependencies_graph": { ... },
  "routing": { ... }
}
```

## Field Definitions

### Root Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Human-readable feature title |
| `version` | string | Yes | Schema version (always "2.0") |
| `slug` | string | Yes | Kebab-case identifier |
| `generated_at` | string | Yes | ISO-8601 timestamp |
| `source` | string | Yes | Path to source brief or "text" |
| `complexity` | enum | Yes | TINY, SMALL, STANDARD, LARGE |
| `metrics` | object | Yes | Aggregate metrics |
| `tasks` | array | Yes | Task definitions |
| `dependencies_graph` | object | Yes | DAG representation |
| `routing` | object | Yes | Execution recommendation |

### Metrics Object

```json
{
  "metrics": {
    "total_tasks": 5,
    "total_steps": 18,
    "estimated_hours": 8.5,
    "critical_path": ["task-001", "task-002", "task-004"],
    "optimized_hours": 6.0
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total_tasks` | integer | Number of tasks |
| `total_steps` | integer | Sum of all steps |
| `estimated_hours` | number | Sequential execution time |
| `critical_path` | array | Task IDs on longest path |
| `optimized_hours` | number | Parallel execution time |

### Task Object

```json
{
  "id": "task-001",
  "title": "Setup Database Models",
  "slug": "setup-models",
  "complexity": "M",
  "estimated_minutes": 90,
  "dependencies": [],
  "acceptance_criteria": [ ... ],
  "steps": [ ... ],
  "files_affected": [ ... ],
  "test_approach": "Unit"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (task-NNN) |
| `title` | string | Human-readable title |
| `slug` | string | URL-friendly identifier |
| `complexity` | enum | S, M, L |
| `estimated_minutes` | integer | 60-120 range |
| `dependencies` | array | Task IDs this depends on |
| `acceptance_criteria` | array | AC objects |
| `steps` | array | Step objects |
| `files_affected` | array | File objects |
| `test_approach` | enum | Unit, Integration, E2E |

### Acceptance Criteria Object

```json
{
  "id": "AC1",
  "title": "User Model Fields",
  "given": "A new User instance",
  "when": "All required fields are provided",
  "then": "The user is saved with correct field values"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique within task (AC1, AC2, ...) |
| `title` | string | Short description |
| `given` | string | Precondition |
| `when` | string | Action |
| `then` | string | Expected result |

### Step Object

```json
{
  "id": "step-1",
  "title": "Create User Model",
  "duration_minutes": 20,
  "input": "Model specifications from brief",
  "output": "User model file created",
  "validation": "Model can be instantiated"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique within task |
| `title` | string | Action-oriented title |
| `duration_minutes` | integer | 15-30 range |
| `input` | string | What's needed to start |
| `output` | string | Deliverable produced |
| `validation` | string | How to verify completion |

### Files Affected Object

```json
{
  "path": "src/models/user.py",
  "action": "create",
  "description": "User model class"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Relative file path |
| `action` | enum | create, modify, delete |
| `description` | string | What's done to file |

### Dependencies Graph Object

```json
{
  "dependencies_graph": {
    "nodes": ["task-001", "task-002", "task-003", "task-004"],
    "edges": [
      {"from": "task-001", "to": "task-002"},
      {"from": "task-002", "to": "task-003"},
      {"from": "task-002", "to": "task-004"}
    ]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `nodes` | array | All task IDs |
| `edges` | array | Dependency relationships |
| `edges[].from` | string | Source task ID |
| `edges[].to` | string | Target task ID (depends on from) |

### Routing Object

```json
{
  "routing": {
    "recommended_skill": "/implement",
    "reason": "STANDARD complexity with 5 interdependent tasks"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `recommended_skill` | string | /quick or /implement |
| `reason` | string | Rationale for recommendation |

## Complete Example

```json
{
  "title": "OAuth Authentication",
  "version": "2.0",
  "slug": "auth-oauth",
  "generated_at": "2026-01-26T10:30:00Z",
  "source": "docs/briefs/auth/brief-auth-oauth-20260126.md",
  "complexity": "STANDARD",
  "metrics": {
    "total_tasks": 5,
    "total_steps": 18,
    "estimated_hours": 8.5,
    "critical_path": ["task-001", "task-002", "task-004", "task-005"],
    "optimized_hours": 6.0
  },
  "tasks": [
    {
      "id": "task-001",
      "title": "Setup Database Models",
      "slug": "setup-models",
      "complexity": "M",
      "estimated_minutes": 90,
      "dependencies": [],
      "acceptance_criteria": [
        {
          "id": "AC1",
          "title": "User Model Fields",
          "given": "A new User instance",
          "when": "All required fields are provided",
          "then": "The user is saved with email, password_hash, created_at"
        },
        {
          "id": "AC2",
          "title": "OAuth Provider Model",
          "given": "An OAuth authentication",
          "when": "User authenticates via Google",
          "then": "Provider record links user to Google ID"
        }
      ],
      "steps": [
        {
          "id": "step-1",
          "title": "Create User Model",
          "duration_minutes": 20,
          "input": "Model specifications",
          "output": "User model file",
          "validation": "Model instantiates correctly"
        },
        {
          "id": "step-2",
          "title": "Create OAuthProvider Model",
          "duration_minutes": 20,
          "input": "OAuth requirements",
          "output": "OAuthProvider model file",
          "validation": "FK relationship works"
        },
        {
          "id": "step-3",
          "title": "Write Unit Tests",
          "duration_minutes": 25,
          "input": "Models created",
          "output": "Test file with coverage",
          "validation": "All tests pass"
        },
        {
          "id": "step-4",
          "title": "Create Migration",
          "duration_minutes": 15,
          "input": "Models complete",
          "output": "Migration file",
          "validation": "Migration applies successfully"
        }
      ],
      "files_affected": [
        {"path": "src/models/user.py", "action": "create"},
        {"path": "src/models/oauth_provider.py", "action": "create"},
        {"path": "tests/models/test_user.py", "action": "create"},
        {"path": "migrations/001_auth_models.py", "action": "create"}
      ],
      "test_approach": "Unit"
    }
  ],
  "dependencies_graph": {
    "nodes": ["task-001", "task-002", "task-003", "task-004", "task-005"],
    "edges": [
      {"from": "task-001", "to": "task-002"},
      {"from": "task-002", "to": "task-003"},
      {"from": "task-002", "to": "task-004"},
      {"from": "task-003", "to": "task-005"},
      {"from": "task-004", "to": "task-005"}
    ]
  },
  "routing": {
    "recommended_skill": "/implement",
    "reason": "STANDARD complexity with 5 interdependent tasks requiring full EPCI workflow"
  }
}
```

## Validation Rules

1. **Schema Compliance**: Must match prd-v2.json schema
2. **ID Uniqueness**: All task IDs unique within feature
3. **Dependency Validity**: All dependencies reference existing tasks
4. **No Cycles**: Dependencies form valid DAG
5. **AC Minimum**: Each task has >= 2 acceptance criteria
6. **Duration Bounds**: Tasks 60-120 min, steps 15-30 min
7. **Critical Path**: Must include at least one task

## Usage

### Reading in Code

```python
import json

with open("docs/specs/auth-oauth/auth-oauth.prd.json") as f:
    prd = json.load(f)

# Access metrics
print(f"Tasks: {prd['metrics']['total_tasks']}")
print(f"Hours: {prd['metrics']['estimated_hours']}")

# Iterate tasks
for task in prd['tasks']:
    print(f"{task['id']}: {task['title']}")
```

### Ralph Integration

Ralph uses PRD.json to:
1. Determine execution order (topological sort)
2. Track progress (update MEMORY.md)
3. Validate completion (check acceptance criteria)
4. Report metrics (steps completed, time elapsed)

## Regeneration

To regenerate PRD.json after editing task files:

```bash
# Not implemented yet - manual regeneration
/spec {slug} --regenerate-json
```

Or manually re-run `/spec` with the same source.
