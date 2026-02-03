---
name: step-00-init
description: Parse arguments, load context, detect continuation, launch exploration
prev_step: null
next_step: steps/step-01-clarify.md
conditional_next:
  - condition: "--party flag"
    step: null
    action: party-orchestrator
  - condition: "--panel flag"
    step: null
    action: expert-panel
  - condition: "--continue <id> provided"
    step: steps/step-04-iteration.md
---

# Step 00: Init

> Parse arguments, load context, launch codebase exploration.

## Trigger

- Skill invocation: `/brainstorm "<idea>" [--flags]`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `idea` | User argument (quoted string) | Yes |
| `--template` | User flag | No (auto-detect) |
| `--quick` | User flag | No |
| `--turbo` | User flag | No |
| `--party` | User flag | No |
| `--panel` | User flag | No |
| `--continue <id>` | User flag | No |
| `--no-hmw` | User flag | No |
| `--no-security` | User flag | No |
| `--no-clarify` | User flag | No |

## Protocol

### 1. Parse Arguments

```
Extract from user input:
  - idea: The quoted string (main topic)
  - flags: All --flag arguments
```

### 1.5 Handle --continue Flag (Session Resume)

```
IF --continue <id> provided:
  session_path = ".claude/state/sessions/brainstorm-{id}.json"

  IF file exists at session_path:
    session = Read(session_path)
    session = JSON.parse(session)

    # Validate session integrity
    IF session.version != "1.0":
      WARN: "Session version mismatch, may have compatibility issues"

    IF session.status == "completed":
      DISPLAY: "Session already completed. Start a new brainstorm."
      → Exit

    # Update session status for resumption
    session.status = "active"
    session.timestamps.last_update = NOW()
    Write(session_path, JSON.stringify(session, indent=2))

    # Display resumption summary
    DISPLAY:
    ┌─────────────────────────────────────────────────────┐
    │  🔄 RESUMING BRAINSTORM SESSION                     │
    ├─────────────────────────────────────────────────────┤
    │  Session: {session.session_id}                      │
    │  Phase: {session.phase}                             │
    │  Iteration: {session.iteration}                     │
    │  EMS: {session.ems.global}/100                      │
    │  Decisions made: {len(session.decisions)}           │
    │  Open threads: {len(session.open_threads)}          │
    └─────────────────────────────────────────────────────┘

    # Restore state variables
    store("session_id", session.session_id)
    store("session_path", session_path)
    store("slug", session.slug)
    store("ems", session.ems)
    store("phase", session.phase)
    store("persona", session.persona)
    store("iteration", session.iteration)
    store("decisions", session.decisions)
    store("open_threads", session.open_threads)
    store("context", session.context)

    → Skip to step-04-iteration.md at iteration N+1

  ELSE:
    # List available sessions
    available = Glob(".claude/state/sessions/brainstorm-*.json")

    IF available is empty:
      DISPLAY: "No saved brainstorm sessions found."
      → Ask user to start a new brainstorm
    ELSE:
      DISPLAY: "Session '{id}' not found. Available sessions:"
      FOR each file in available:
        session = JSON.parse(Read(file))
        DISPLAY: "  - {session.slug} (EMS: {session.ems.global}, iteration {session.iteration})"
      → Ask user to select or provide correct ID
```

### 2. Load Project Context (SI DISPONIBLE)

Charger le contexte projet depuis les fichiers d'état:

```
SI le fichier `.claude/state/features/index.json` existe:
  Read(".claude/state/features/index.json")
  → Extraire les features récentes liées au sujet
  → Stocker patterns et préférences

SI le fichier `.claude/state/project-patterns.json` existe:
  Read(".claude/state/project-patterns.json")
  → Extraire conventions de code
  → Extraire préférences utilisateur

SINON:
  → Continuer sans historique projet
  → Log: "project-memory unavailable, continuing without history context"
```

Store for later steps:
- Code conventions
- User preferences (verbose, quick mode default, etc.)
- Related past features for context

### 3. Generate Session ID and Initial State

```
# Generate identifiers
timestamp = NOW().format("YYYYMMDD-HHmmss")
slug = slugify(idea)  # lowercase, hyphenated, max 30 chars
session_id = "brainstorm-{slug}-{timestamp}"
session_path = ".claude/state/sessions/{session_id}.json"
```

### 3.5 Create and Persist Initial Session File

🔴 **OBLIGATOIRE**: Créer le fichier session AVANT de continuer.

```json
{
  "session_id": "brainstorm-{slug}-{timestamp}",
  "version": "1.0",
  "slug": "{slug}",
  "status": "initialized",
  "template": null,
  "flags": {
    "quick": false,
    "turbo": false,
    "party": false,
    "panel": false,
    "no_hmw": false,
    "no_security": false,
    "no_clarify": false
  },
  "timestamps": {
    "created_at": "{ISO8601}",
    "last_update": "{ISO8601}",
    "ended_at": null
  },
  "phase": "INIT",
  "persona": "architecte",
  "iteration": 0,
  "ems": {
    "global": 20,
    "axes": { "clarity": 20, "depth": 20, "coverage": 20, "decisions": 20, "actionability": 20 },
    "history": []
  },
  "context": {
    "idea_raw": "<user input>",
    "idea_refined": null,
    "brief_v0": null,
    "codebase_analysis": null,
    "hmw_questions": [],
    "perplexity_prompts": [],
    "perplexity_results": []
  },
  "decisions": [],
  "open_threads": [],
  "techniques_applied": [],
  "persona_history": [
    { "persona": "architecte", "iteration": 0, "trigger": "default" }
  ]
}
```

```
# Persist initial session
Write(session_path, JSON.stringify(initial_session, indent=2))

# Store references for subsequent steps
store("session_id", session_id)
store("session_path", session_path)
store("slug", slug)

DISPLAY: "Session created: {session_id}"
```

### 4. Launch @Explore (Background)

LANCE Task({
  subagent_type: "Explore",
  model: "haiku",
  run_in_background: true,
  prompt: `
## Exploration Objective
Explore codebase for brainstorm context

## Search Focus
- Project stack and architecture
- Related existing features
- Code patterns and conventions
- Test coverage areas
- Security patterns (auth, permissions)

## Thoroughness Level
medium
  `
})

### 5. Check Special Modes

| Mode | Action |
|------|--------|
| `--party` | Load @party-orchestrator, skip to party mode |
| `--panel` | Load @expert-panel, skip to panel mode |
| `--turbo` | Enable @clarifier usage |

## Outputs

| Output | Destination |
|--------|-------------|
| Session JSON | `.claude/state/sessions/{session_id}.json` |
| `session_id` | Stored for subsequent steps |
| `session_path` | Stored for subsequent steps |
| `slug` | Stored for subsequent steps |
| Project context | Loaded for subsequent steps |
| @Explore task | Running in background |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| `--party` flag | → Special mode (party-orchestrator) |
| `--panel` flag | → Special mode (expert-panel) |
| `--continue` flag | → `step-04-iteration.md` |
| Default | → `step-01-clarify.md` |

## Error Handling

| Error | Resolution |
|-------|------------|
| Empty idea | Ask user to provide topic |
| Invalid session ID | List available sessions, ask to select |
| project-memory unavailable | Continue without history context |
