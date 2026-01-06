# Session Format — Brainstorm Persistence

## Overview

Format YAML pour la persistence des sessions de brainstorming.
Permet de sauvegarder et reprendre une session interrompue.

**Storage**: `.project-memory/brainstorm-sessions/[slug].yaml`

## Schema

```yaml
format_version: "1.0"

session:
  id: string           # Unique identifier: "{slug}-{date}"
  slug: string         # Feature slug (kebab-case)
  status: enum         # in_progress | completed | abandoned
  phase: enum          # divergent | transition | convergent
  ems: integer         # Current EMS score (0-100)
  persona: string      # Current persona: architecte | sparring | pragmatique
  iteration: integer   # Current iteration number
  techniques_used: []  # List of technique slugs used

  ideas:               # Collected ideas with scores
    - id: integer
      content: string
      score: integer   # 0-10

  history:             # Iteration history for back command
    - iteration: integer
      phase: string
      ems: integer
      ems_delta: integer
      questions: []
      responses: []
      timestamp: string

  last_question: string  # Last question asked (for context)
  created: datetime      # ISO 8601 format
  updated: datetime      # ISO 8601 format
```

## Field Descriptions

### Session Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format_version` | string | Yes | Schema version for migrations ("1.0") |
| `session.id` | string | Yes | Unique ID: `{slug}-{YYYY-MM-DD}` |
| `session.slug` | string | Yes | Feature name in kebab-case |
| `session.status` | enum | Yes | `in_progress`, `completed`, `abandoned` |
| `session.phase` | enum | Yes | `divergent`, `transition`, `convergent` |
| `session.ems` | integer | Yes | Current EMS score (0-100) |
| `session.persona` | string | Yes | Active persona |
| `session.iteration` | integer | Yes | Current iteration number |
| `session.mode` | string | No | Mode flag: `random`, `progressive`, or null (v4.2) |

### Mode-Specific State (v4.2)

| Field | Type | When | Description |
|-------|------|------|-------------|
| `session.random_state` | object | `--random` | Tracks random selection state |
| `session.random_state.last_category` | string | | Last selected category |
| `session.random_state.category_counts` | object | | Count per category |
| `session.progressive_state` | object | `--progressive` | Tracks phase progression state |
| `session.progressive_state.divergent_completed` | bool | | Divergent phase done |
| `session.progressive_state.transition_completed` | bool | | Transition done |
| `session.progressive_state.transition_summary` | object | | Summary at EMS 50 |

### Ideas

| Field | Type | Description |
|-------|------|-------------|
| `ideas[].id` | integer | Sequential ID |
| `ideas[].content` | string | Idea description |
| `ideas[].score` | integer | Priority score (0-10) |

### History

| Field | Type | Description |
|-------|------|-------------|
| `history[].iteration` | integer | Iteration number |
| `history[].phase` | string | Phase at that iteration |
| `history[].ems` | integer | EMS at that iteration |
| `history[].ems_delta` | integer | EMS change from previous |
| `history[].questions` | array | Questions asked |
| `history[].responses` | array | User responses |
| `history[].timestamp` | string | ISO 8601 timestamp |

## Example

```yaml
format_version: "1.0"

session:
  id: "feature-auth-2026-01-06"
  slug: "feature-auth"
  status: "in_progress"
  phase: "divergent"
  ems: 52
  persona: "architecte"
  iteration: 3
  techniques_used: ["moscow", "5whys"]

  ideas:
    - id: 1
      content: "OAuth2 avec refresh tokens"
      score: 8
    - id: 2
      content: "Session JWT stateless"
      score: 7
    - id: 3
      content: "Magic links pour login"
      score: 5

  history:
    - iteration: 1
      phase: "divergent"
      ems: 25
      ems_delta: 0
      questions:
        - "Quel type d'authentification privilegier?"
        - "Quels sont les utilisateurs cibles?"
      responses:
        - "OAuth2 pour les integrations tierces"
        - "Developpeurs et admins internes"
      timestamp: "2026-01-06T10:30:00Z"

    - iteration: 2
      phase: "divergent"
      ems: 38
      ems_delta: 13
      questions:
        - "Comment gerer les sessions longues?"
        - "Quelle strategie de refresh token?"
      responses:
        - "Sliding window avec timeout configurable"
        - "Rotation a chaque refresh"
      timestamp: "2026-01-06T10:45:00Z"

    - iteration: 3
      phase: "divergent"
      ems: 52
      ems_delta: 14
      questions:
        - "Quel mecanisme de revocation?"
        - "Comment gerer le multi-device?"
        - "Faut-il un rate limiting?"
      responses: []  # Awaiting response
      timestamp: "2026-01-06T11:00:00Z"

  last_question: "Quel mecanisme de revocation privilegier?"
  created: "2026-01-06T10:30:00Z"
  updated: "2026-01-06T11:00:00Z"
```

## Operations

### Save Session

Triggered by:
- `save` command (explicit)
- `finish` command (auto-save before generating brief)
- Phase change (auto-save checkpoint)

```
Session saved: .project-memory/brainstorm-sessions/feature-auth.yaml
```

### Load Session (Auto-detect)

At `/brainstorm` launch, check for existing sessions:

```
-------------------------------------------------------
Session existante detectee: "feature-auth" (EMS: 52)
   Derniere activite: il y a 2 heures
   Phase: Divergent | Iteration: 3

[1] Reprendre cette session
[2] Nouvelle session
-------------------------------------------------------
```

### Back Command

Uses `history` array to restore previous state:
1. Pop last entry from `history`
2. Restore `ems`, `phase`, `iteration` from previous entry
3. Display restored questions

**Limitation**: 1 step back only (simple rollback)

## Storage Rules

1. **One file per session**: `{slug}.yaml`
2. **Auto-cleanup**: Sessions older than 30 days with status `completed` or `abandoned`
3. **Directory creation**: Create `.project-memory/brainstorm-sessions/` if not exists
4. **Validation**: YAML must be valid, required fields must be present

## Migration

When `format_version` changes:
1. Check version on load
2. Apply migrations sequentially
3. Update `format_version` field
4. Save migrated session
