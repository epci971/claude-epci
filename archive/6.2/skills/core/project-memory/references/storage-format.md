# Storage Format Reference

Complete JSON schemas for project-memory storage files.

## Storage Location

```
.claude/state/memory/
├── patterns.json
├── preferences.json
├── velocity.json
├── bugs.json
└── features/
    └── {slug}.json
```

---

## 1. patterns.json

Detected code patterns for the project.

### Schema

```json
{
  "version": "1.0",
  "last_scan": "2026-01-22T10:00:00Z",
  "scan_files_count": 156,
  "patterns": {
    "api_style": {
      "type": "REST",
      "confidence": 0.95,
      "examples": ["src/api/users.ts", "src/api/products.ts"]
    },
    "error_handling": {
      "pattern": "try-catch",
      "confidence": 0.88,
      "examples": ["src/services/auth.ts:45"]
    },
    "naming": {
      "files": "kebab-case",
      "functions": "camelCase",
      "classes": "PascalCase",
      "constants": "SCREAMING_SNAKE",
      "confidence": 0.92
    },
    "tests": {
      "framework": "vitest",
      "location": "tests/",
      "pattern": "*.test.ts",
      "confidence": 0.98
    },
    "components": {
      "framework": "react",
      "styling": "tailwind",
      "state": "zustand",
      "confidence": 0.90
    }
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version (always "1.0") |
| `last_scan` | ISO-8601 | When patterns were last detected |
| `scan_files_count` | number | Number of files analyzed |
| `patterns` | object | Detected pattern categories |

### Pattern Categories

| Category | Fields | Possible Values |
|----------|--------|-----------------|
| `api_style` | type, confidence, examples | REST, GraphQL, gRPC, tRPC |
| `error_handling` | pattern, confidence, examples | try-catch, result-type, error-boundary |
| `naming` | files, functions, classes, constants, confidence | kebab-case, camelCase, PascalCase, snake_case |
| `tests` | framework, location, pattern, confidence | vitest, jest, pytest, mocha |
| `components` | framework, styling, state, confidence | react, vue, svelte; tailwind, css-modules |

### Confidence Thresholds

| Confidence | Meaning |
|------------|---------|
| 0.0 - 0.5 | Low confidence, few examples found |
| 0.5 - 0.8 | Medium confidence, some inconsistency |
| 0.8 - 1.0 | High confidence, consistent pattern |

### Staleness Rule

Patterns are considered stale after 7 days. Rescan triggered when:
- `is_pattern_stale()` returns `true`
- Major file changes detected
- User explicitly requests rescan

---

## 2. preferences.json

User workflow and technical preferences.

### Schema

```json
{
  "version": "1.0",
  "last_update": "2026-01-22T14:30:00Z",
  "workflow": {
    "tdd_preference": {
      "value": "guided",
      "confidence": 0.85,
      "observations": 8
    },
    "breakpoint_frequency": {
      "value": "high",
      "confidence": 0.72,
      "observations": 5
    },
    "verbosity": {
      "value": "concise",
      "confidence": 0.90,
      "observations": 12
    },
    "commit_style": {
      "value": "conventional",
      "confidence": 0.95,
      "observations": 20
    }
  },
  "technical": {
    "test_framework": {
      "value": "vitest",
      "confidence": 0.98,
      "observations": 15
    },
    "css_approach": {
      "value": "tailwind",
      "confidence": 0.95,
      "observations": 10
    },
    "state_management": {
      "value": "zustand",
      "confidence": 0.80,
      "observations": 4
    }
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version (always "1.0") |
| `last_update` | ISO-8601 | Last preference update timestamp |
| `workflow` | object | Workflow-related preferences |
| `technical` | object | Technical stack preferences |

### Workflow Preferences

| Key | Possible Values | Description |
|-----|-----------------|-------------|
| `tdd_preference` | guided, always, never | TDD approach preference |
| `breakpoint_frequency` | high, medium, low | How often to ask for confirmation |
| `verbosity` | concise, detailed, minimal | Output verbosity preference |
| `commit_style` | conventional, descriptive, minimal | Commit message style |

### Technical Preferences

| Key | Possible Values | Description |
|-----|-----------------|-------------|
| `test_framework` | vitest, jest, pytest, mocha | Testing framework |
| `css_approach` | tailwind, css-modules, styled, sass | Styling approach |
| `state_management` | zustand, redux, jotai, context | State management library |

### Confidence Calculation

Confidence increases with observations:

```
confidence = min(0.95, 0.5 + (observations * 0.1))
```

| Observations | Confidence |
|--------------|------------|
| 1 | 0.50 |
| 3 | 0.75 |
| 5 | 0.90 |
| 6+ | 0.95 (max) |

---

## 3. velocity.json

Estimation accuracy calibration by complexity level.

### Schema

```json
{
  "version": "1.0",
  "last_update": "2026-01-22T16:00:00Z",
  "total_samples": 24,
  "calibration": {
    "TINY": {
      "estimated_avg": 30,
      "actual_avg": 25,
      "sample_count": 8,
      "accuracy": 0.83,
      "adjustment_factor": 0.83
    },
    "SMALL": {
      "estimated_avg": 120,
      "actual_avg": 135,
      "sample_count": 10,
      "accuracy": 0.89,
      "adjustment_factor": 1.13
    },
    "STANDARD": {
      "estimated_avg": 480,
      "actual_avg": 520,
      "sample_count": 5,
      "accuracy": 0.92,
      "adjustment_factor": 1.08
    },
    "LARGE": {
      "estimated_avg": 1440,
      "actual_avg": 1600,
      "sample_count": 1,
      "accuracy": 0.90,
      "adjustment_factor": 1.11
    }
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version (always "1.0") |
| `last_update` | ISO-8601 | Last velocity update timestamp |
| `total_samples` | number | Total completed tasks tracked |
| `calibration` | object | Per-complexity calibration data |

### Calibration Fields

| Field | Type | Description |
|-------|------|-------------|
| `estimated_avg` | number | Average estimated minutes |
| `actual_avg` | number | Average actual minutes |
| `sample_count` | number | Number of completed tasks |
| `accuracy` | number | Estimation accuracy (0.0-1.0) |
| `adjustment_factor` | number | Multiplier to adjust future estimates |

### Calculation Formulas

```
accuracy = 1 - abs(estimated_avg - actual_avg) / estimated_avg
adjustment_factor = actual_avg / estimated_avg
```

### Usage Example

```
# When estimating a SMALL task:
base_estimate = 120  # minutes
adjustment = velocity.calibration.SMALL.adjustment_factor  # 1.13
adjusted_estimate = base_estimate * adjustment  # 136 minutes
```

---

## 4. bugs.json

Bug fix history for recall and pattern matching.

### Schema

```json
{
  "version": "1.0",
  "last_update": "2026-01-22T11:00:00Z",
  "bugs": [
    {
      "id": "oauth-redirect-fix",
      "created_at": "2026-01-20T14:00:00Z",
      "description": "OAuth callback fails on production due to redirect URI mismatch",
      "root_cause": "OAUTH_REDIRECT_URI not configured in production .env",
      "fix_summary": "Added OAUTH_REDIRECT_URI to production environment and unified config",
      "keywords": ["oauth", "redirect", "callback", "production", "env"],
      "category": "integration",
      "files_modified": [".env.production", "src/auth/oauth.ts"],
      "time_to_fix_minutes": 45
    },
    {
      "id": "null-user-crash",
      "created_at": "2026-01-18T09:00:00Z",
      "description": "App crashes when user object is null on profile page",
      "root_cause": "Missing null check before accessing user.name",
      "fix_summary": "Added optional chaining and fallback for user properties",
      "keywords": ["null", "crash", "user", "profile"],
      "category": "logic",
      "files_modified": ["src/pages/Profile.tsx"],
      "time_to_fix_minutes": 15
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique slug identifier |
| `created_at` | ISO-8601 | Yes | When bug was fixed |
| `description` | string | Yes | Bug description (max 200 chars) |
| `root_cause` | string | Yes | What caused the bug |
| `fix_summary` | string | Yes | How it was fixed |
| `keywords` | string[] | Yes | Search terms for recall |
| `category` | enum | Yes | Bug category |
| `files_modified` | string[] | No | Files changed to fix |
| `time_to_fix_minutes` | number | No | Time spent fixing |

### Bug Categories

| Category | Description |
|----------|-------------|
| `logic` | Logic errors, wrong conditions |
| `ui` | Visual/layout issues |
| `security` | Security vulnerabilities |
| `integration` | API/service integration issues |
| `performance` | Performance problems |
| `data` | Data handling/validation issues |

### Size Limits

| Limit | Value |
|-------|-------|
| Max bugs stored | 100 |
| Description max length | 200 chars |
| Keywords max count | 10 |
| Archive threshold | 6 months |

---

## 5. features/{slug}.json

Completed feature history with decisions and learnings.

### Schema

```json
{
  "version": "1.0",
  "slug": "auth-oauth-google",
  "created_at": "2026-01-20T10:00:00Z",
  "completed_at": "2026-01-22T15:30:00Z",
  "summary": "OAuth2 authentication with Google provider for user login",
  "complexity": "STANDARD",
  "duration_minutes": 195,
  "estimated_minutes": 180,
  "keywords": ["authentication", "oauth", "google", "login", "security"],
  "files_modified": [
    "src/auth/oauth.ts",
    "src/auth/types.ts",
    "src/pages/Login.tsx",
    "src/api/auth.ts"
  ],
  "test_count": 12,
  "test_files": [
    "tests/auth/oauth.test.ts",
    "tests/integration/login.test.ts"
  ],
  "decisions": [
    {
      "question": "Where to store OAuth tokens?",
      "choice": "httpOnly cookies",
      "reasoning": "More secure than localStorage, prevents XSS token theft",
      "alternatives_considered": ["localStorage", "sessionStorage", "memory"]
    },
    {
      "question": "Session duration?",
      "choice": "7 days with refresh",
      "reasoning": "Balance between security and user convenience",
      "alternatives_considered": ["24 hours", "30 days", "no expiry"]
    }
  ],
  "learnings": [
    "Google requires verified redirect URIs before going live",
    "Token refresh should happen before expiry, not after",
    "Use state parameter to prevent CSRF attacks"
  ],
  "spec_reference": "docs/specs/auth-oauth-google.prd.json"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Schema version (always "1.0") |
| `slug` | string | Yes | Feature identifier (kebab-case) |
| `created_at` | ISO-8601 | Yes | When feature started |
| `completed_at` | ISO-8601 | Yes | When feature completed |
| `summary` | string | Yes | Brief description (max 200 chars) |
| `complexity` | enum | Yes | TINY, SMALL, STANDARD, LARGE |
| `duration_minutes` | number | Yes | Actual time spent |
| `estimated_minutes` | number | Yes | Original estimate |
| `keywords` | string[] | Yes | Search terms for recall |
| `files_modified` | string[] | Yes | Files created/modified |
| `test_count` | number | Yes | Number of tests written |
| `test_files` | string[] | No | Test file paths |
| `decisions` | object[] | No | Key decisions made |
| `learnings` | string[] | No | Insights gained |
| `spec_reference` | string | No | Path to PRD/CDC file |

### Decision Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | What decision was needed |
| `choice` | string | Yes | What was chosen |
| `reasoning` | string | Yes | Why this choice |
| `alternatives_considered` | string[] | No | Other options considered |

### Size Limits

| Limit | Value |
|-------|-------|
| Max features stored | 200 |
| Summary max length | 200 chars |
| Keywords max count | 10 |
| Decisions max count | 10 |
| Learnings max count | 10 |
| Archive threshold | 6 months |

---

## Validation Rules

### All Files

1. Must be valid JSON
2. Must have `version` field set to "1.0"
3. Timestamps must be ISO-8601 format
4. Confidence values must be 0.0-1.0

### String Limits

| Field Type | Max Length |
|------------|------------|
| description/summary | 200 chars |
| id/slug | 64 chars |
| keyword | 32 chars |
| file path | 256 chars |

### Array Limits

| Array | Max Items |
|-------|-----------|
| keywords | 10 |
| examples | 5 |
| files_modified | 50 |
| decisions | 10 |
| learnings | 10 |
| bugs | 100 |
| features | 200 |

---

## Initialization

When `init()` is called on a new project:

```
.claude/state/memory/
├── patterns.json      # { "version": "1.0", "patterns": {} }
├── preferences.json   # { "version": "1.0", "workflow": {}, "technical": {} }
├── velocity.json      # { "version": "1.0", "calibration": {} }
├── bugs.json         # { "version": "1.0", "bugs": [] }
└── features/         # Empty directory
```

---

## Archiving

Features and bugs older than 6 months are archived:

```
.claude/state/memory/
├── features/
│   └── {active-features}
└── archive/
    ├── features/
    │   └── {archived-features}
    └── bugs-archive.json
```
