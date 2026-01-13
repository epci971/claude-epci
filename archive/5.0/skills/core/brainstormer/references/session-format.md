# Session Format — Brainstorm Persistence v1.2

## Overview

Format YAML pour la persistence des sessions de brainstorming.
Permet de sauvegarder et reprendre une session interrompue.
Supporte les modes Standard, Party et Panel (v5.0).

**Storage**: `.project-memory/brainstorm-sessions/[slug].yaml`

## Schema v1.2

```yaml
format_version: "1.2"

session:
  id: string           # Unique identifier: "{slug}-{date}"
  slug: string         # Feature slug (kebab-case)
  status: enum         # in_progress | completed | abandoned
  phase: enum          # divergent | transition | convergent
  mode: enum           # standard | party | panel (v5.0)
  ems: integer         # Current EMS score (0-100)
  persona: string      # Current persona: architecte | sparring | pragmatique
  iteration: integer   # Current iteration number
  techniques_used: []  # List of technique slugs used (legacy, kept for compat)
  started_at: datetime # Session start timestamp (ISO 8601)
  duration_minutes: integer  # Total session duration in minutes

  # v5.0: Enhanced technique tracking
  techniques_history:
    - iteration: integer
      technique_slug: string
      category: string
      suggested_reason: string
      applied: boolean
      source: enum       # auto | manual | random | progressive
      weak_axes: []      # Axes that triggered suggestion

  # v5.0: Party mode tracking
  party_active: boolean
  party_history:
    - round: integer
      topic: string
      personas_selected: []
      contributions:
        - persona: string
          key_points: []
          references: []   # Other personas referenced
      synthesis: string
      user_question: string

  # v5.0: Expert panel tracking
  panel_active: boolean
  panel_history:
    - round: integer
      topic: string
      phase: enum        # discussion | debate | socratic
      experts_selected: []
      contributions:
        - expert: string
          framework: string
          position: string
          references: []
      synthesis:
        convergent: []
        tensions: []

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
      duration: integer  # Duration of this iteration in minutes

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
| `session.started_at` | datetime | Yes | Session start timestamp (ISO 8601) |
| `session.duration_minutes` | integer | Yes | Total session duration in minutes |
| `session.mode` | enum | Yes | Active mode: `standard`, `party`, `panel` (v5.0) |

### v5.0: Enhanced Technique Tracking

| Field | Type | Description |
|-------|------|-------------|
| `techniques_history[].iteration` | integer | Iteration when technique was suggested |
| `techniques_history[].technique_slug` | string | Technique slug from CSV |
| `techniques_history[].category` | string | Category (creative, structured, etc.) |
| `techniques_history[].suggested_reason` | string | Why suggested (e.g., "Couverture 35%") |
| `techniques_history[].applied` | boolean | Whether user applied it |
| `techniques_history[].source` | enum | `auto`, `manual`, `random`, `progressive` |
| `techniques_history[].weak_axes` | array | EMS axes that triggered suggestion |

### v5.0: Party Mode State

| Field | Type | Description |
|-------|------|-------------|
| `party_active` | boolean | Whether party mode is currently active |
| `party_history[].round` | integer | Discussion round number |
| `party_history[].topic` | string | Topic discussed this round |
| `party_history[].personas_selected` | array | Personas participating |
| `party_history[].contributions[].persona` | string | Persona name |
| `party_history[].contributions[].key_points` | array | Main points made |
| `party_history[].contributions[].references` | array | Other personas referenced |
| `party_history[].synthesis` | string | Round synthesis |
| `party_history[].user_question` | string | Question posed to user |

### v5.0: Expert Panel State

| Field | Type | Description |
|-------|------|-------------|
| `panel_active` | boolean | Whether panel mode is currently active |
| `panel_history[].round` | integer | Panel round number |
| `panel_history[].topic` | string | Topic analyzed |
| `panel_history[].phase` | enum | `discussion`, `debate`, `socratic` |
| `panel_history[].experts_selected` | array | Experts participating |
| `panel_history[].contributions[].expert` | string | Expert name |
| `panel_history[].contributions[].framework` | string | Framework used (SOLID, etc.) |
| `panel_history[].contributions[].position` | string | Expert's position |
| `panel_history[].synthesis.convergent` | array | Points of agreement |
| `panel_history[].synthesis.tensions` | array | Productive tensions |

### Mode-Specific State (v4.2 - Legacy)

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
| `history[].duration` | integer | Duration of iteration in minutes |

## Example (v1.2)

```yaml
format_version: "1.2"

session:
  id: "feature-auth-2026-01-09"
  slug: "feature-auth"
  status: "in_progress"
  phase: "divergent"
  mode: "standard"      # standard | party | panel
  ems: 52
  persona: "architecte"
  iteration: 3
  techniques_used: ["moscow", "5whys"]  # Legacy, kept for compat
  started_at: "2026-01-09T10:30:00Z"
  duration_minutes: 30

  # v5.0: Enhanced technique tracking
  techniques_history:
    - iteration: 2
      technique_slug: "5whys"
      category: "deep"
      suggested_reason: "Clarte 42%"
      applied: true
      source: "auto"
      weak_axes: ["Clarte"]
    - iteration: 3
      technique_slug: "six-hats"
      category: "structured"
      suggested_reason: "Couverture 38%"
      applied: false
      source: "auto"
      weak_axes: ["Couverture"]

  # v5.0: Party mode (inactive in this example)
  party_active: false
  party_history: []

  # v5.0: Panel mode (inactive in this example)
  panel_active: false
  panel_history: []

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
      timestamp: "2026-01-09T10:30:00Z"

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
      timestamp: "2026-01-09T10:45:00Z"

    - iteration: 3
      phase: "divergent"
      ems: 52
      ems_delta: 14
      questions:
        - "Quel mecanisme de revocation?"
        - "Comment gerer le multi-device?"
        - "Faut-il un rate limiting?"
      responses: []  # Awaiting response
      timestamp: "2026-01-09T11:00:00Z"

  last_question: "Quel mecanisme de revocation privilegier?"
  created: "2026-01-09T10:30:00Z"
  updated: "2026-01-09T11:00:00Z"
```

## Example with Party Mode Active

```yaml
format_version: "1.2"

session:
  id: "feature-checkout-2026-01-09"
  slug: "feature-checkout"
  status: "in_progress"
  phase: "divergent"
  mode: "party"
  ems: 45
  persona: "architecte"
  iteration: 2

  party_active: true
  party_history:
    - round: 1
      topic: "Payment gateway integration approach"
      personas_selected: ["Architect", "Security", "Backend"]
      contributions:
        - persona: "Architect"
          key_points:
            - "Recommend facade pattern for gateway abstraction"
            - "Consider async processing for reliability"
          references: []
        - persona: "Security"
          key_points:
            - "PCI-DSS compliance mandatory"
            - "Token-based approach preferred"
          references: ["Architect"]
        - persona: "Backend"
          key_points:
            - "Idempotency keys essential"
            - "Webhook handling needs careful design"
          references: ["Architect", "Security"]
      synthesis: "Consensus on facade + async, debate on token storage strategy"
      user_question: "Preferred token storage: DB or Redis?"
```

## Example with Expert Panel Active

```yaml
format_version: "1.2"

session:
  id: "refactor-api-2026-01-09"
  slug: "refactor-api"
  status: "in_progress"
  phase: "convergent"
  mode: "panel"
  ems: 68
  iteration: 4

  panel_active: true
  panel_history:
    - round: 1
      topic: "Repository pattern vs Active Record for data access"
      phase: "discussion"
      experts_selected: ["Martin", "Fowler", "Beck"]
      contributions:
        - expert: "Martin"
          framework: "SOLID"
          position: "Repository pattern for testability and SRP"
          references: []
        - expert: "Fowler"
          framework: "Enterprise Patterns"
          position: "Context-dependent - Active Record for simple CRUD, Repository for complex domain"
          references: ["Martin"]
        - expert: "Beck"
          framework: "TDD"
          position: "Repository enables test doubles, critical for fast tests"
          references: ["Martin"]
      synthesis:
        convergent:
          - "Testability is primary concern"
          - "Abstraction needed for complex domain logic"
        tensions:
          - "Simplicity vs flexibility trade-off"
          - "Initial velocity vs long-term maintainability"
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

**Syntax**: `back [n]` where n = 1-5 (default: 1)

Uses `history` array to restore previous state:
1. Validate that `iteration >= n` (can't go back more than available)
2. Calculate `target_iteration = current_iteration - n`
3. Restore state from `history[target_iteration - 1]`
4. Restore `ems`, `phase`, `iteration` from target entry
5. Display restored questions with jump summary

**Examples**:
- `back` → Go back 1 iteration
- `back 2` → Go back 2 iterations
- `back 5` → Go back 5 iterations (max allowed)

**Jump Summary Display**:
```
-------------------------------------------------------
Retour de 2 iterations
   Iteration: 5 → 3
   EMS: 68/100 → 52/100 (-16)
   Phase: transition → divergent

   Questions restaurees (iteration 3):
   - Quel mecanisme de revocation?
   - Comment gerer le multi-device?
-------------------------------------------------------
```

**Limits**:
- Maximum 5 steps back per command
- Cannot go below iteration 1
- History is preserved (can `continue` forward after back)

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

### Migration v1.0 → v1.2

```python
def migrate_v1_to_v12(session):
    """Migrate session from v1.0 to v1.2"""

    # Add mode field (default: standard)
    session['mode'] = 'standard'

    # Convert techniques_used to techniques_history
    techniques_history = []
    for i, slug in enumerate(session.get('techniques_used', [])):
        techniques_history.append({
            'iteration': i + 1,
            'technique_slug': slug,
            'category': 'unknown',  # Cannot infer from v1.0
            'suggested_reason': 'migrated from v1.0',
            'applied': True,
            'source': 'manual',
            'weak_axes': []
        })
    session['techniques_history'] = techniques_history

    # Initialize party and panel as inactive
    session['party_active'] = False
    session['party_history'] = []
    session['panel_active'] = False
    session['panel_history'] = []

    # Update version
    session['format_version'] = '1.2'

    return session
```

### Backward Compatibility

- v1.0 sessions are auto-migrated on load
- `techniques_used[]` kept for backward compat (updated in parallel with `techniques_history`)
- Missing fields default to empty/false
