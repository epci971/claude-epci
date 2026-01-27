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

IF --continue <id> provided:
  → Load session from .claude/state/sessions/brainstorm-{id}.json
  → Restore EMS, phase, persona, iteration
  → Skip to step-04-iteration.md at iteration N+1
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

### 3. Generate Session ID

```json
{
  "session_id": "brainstorm-{slug}-{timestamp}",
  "slug": "{slugified-idea}",
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
    "codebase_analysis": null
  }
}
```

### 4. Launch @Explore (Background)

```
Task: Explore codebase for brainstorm context
Focus:
  - Project stack and architecture
  - Related existing features
  - Code patterns and conventions
  - Test coverage areas
  - Security patterns (auth, permissions)

run_in_background: true
```

### 5. Check Special Modes

| Mode | Action |
|------|--------|
| `--party` | Load @party-orchestrator, skip to party mode |
| `--panel` | Load @expert-panel, skip to panel mode |
| `--turbo` | Enable @clarifier usage |

## Outputs

| Output | Destination |
|--------|-------------|
| Session state | `state-manager` |
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
