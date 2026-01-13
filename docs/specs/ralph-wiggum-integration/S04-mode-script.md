# Specification — S04: Mode Script Externe

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S04
> **Estimated effort**: 2 day(s)
> **Dependencies**: S02, S03
> **Blocks**: S06

---

## 1. Context

This sub-spec implements the **Script mode** for Ralph, using an external bash script that provides fresh context for each iteration. This mode is more robust for overnight sessions (>2h) as it survives Claude crashes and avoids context bloat.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US15

---

## 2. Scope

### Included

- Main loop script (`ralph_loop.sh`)
- Date utilities (`date_utils.sh`) for cross-platform support
- Integration with Circuit Breaker (S02)
- Integration with Response Analyzer (S03)
- prd.json tracking (passes: true/false)
- `--continue` flag for resuming interrupted sessions
- Session state persistence

### Excluded

- prd.json generation from /decompose (S05)
- @ralph-executor subagent (S06)
- /ralph command (S07)
- Rate limiting (S08)

---

## 3. Tasks

- [ ] Create `src/scripts/lib/date_utils.sh`
  - [ ] Implement `du_now()` — Current timestamp (cross-platform)
  - [ ] Implement `du_elapsed()` — Time elapsed since timestamp
  - [ ] Implement `du_format()` — Format duration human-readable
  - [ ] Implement `du_is_expired()` — Check if session expired (24h default)
  - [ ] Handle macOS vs Linux date differences

- [ ] Create `src/scripts/ralph_loop.sh`
  - [ ] Argument parsing (--continue, --max-iterations, --dry-run)
  - [ ] Load dependencies (circuit_breaker.sh, response_analyzer.sh, date_utils.sh)
  - [ ] Validate prd.json exists
  - [ ] Implement main loop:
    - [ ] Get next pending story from prd.json
    - [ ] Check circuit breaker state
    - [ ] Launch Claude with story context (`claude --print`)
    - [ ] Capture output to temp file
    - [ ] Parse response with response_analyzer
    - [ ] Update prd.json (passes: true/false)
    - [ ] Commit changes if story complete
    - [ ] Log to progress.txt
    - [ ] Evaluate exit conditions

- [ ] Implement session management:
  - [ ] Create `.ralph-session.json` with metadata
  - [ ] Track iterations, start_time, last_activity
  - [ ] Auto-reset on: circuit breaker OPEN, Ctrl+C, completion
  - [ ] Restore state with `--continue`
  - [ ] Session expiration after 24h

- [ ] Implement story execution:
  - [ ] Read story from prd.json
  - [ ] Load parent spec context (parent_spec field)
  - [ ] Build Claude prompt with context
  - [ ] Execute `claude --print -p "prompt"`
  - [ ] Handle Claude errors gracefully

- [ ] Implement Ctrl+C handling:
  - [ ] Trap SIGINT/SIGTERM
  - [ ] Save checkpoint to session file
  - [ ] Clean exit with message
  - [ ] Allow resume with --continue

- [ ] Write BATS tests for ralph_loop.sh

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S04-AC1 | Given `/ralph --mode script`, When launched, Then ralph_loop.sh is executed | Execution test |
| S04-AC2 | Given story completed, When script verifies, Then new Claude instance launched (fresh context) | Context isolation test |
| S04-AC3 | Given Claude crash, When detected, Then script survives and can resume with --continue | Crash recovery test |
| S04-AC4 | Given script mode active, When running, Then Circuit Breaker and Response Analyzer are used | Integration test |
| S04-AC5 | Given prd.json with pending stories, When loop runs, Then stories executed in order | Story ordering test |
| S04-AC6 | Given Ctrl+C during execution, When trapped, Then checkpoint saved and clean exit | Signal handling test |
| S04-AC7 | Given session older than 24h, When --continue used, Then new session started | Expiration test |

---

## 5. Technical Notes

### Script Flow

```
ralph_loop.sh
    │
    ├── Load libraries
    │   ├── circuit_breaker.sh
    │   ├── response_analyzer.sh
    │   └── date_utils.sh
    │
    ├── Parse arguments
    │
    ├── Validate prd.json
    │
    ├── Initialize/restore session
    │
    └── Main loop
        ├── Get next story (passes=false)
        ├── Check circuit breaker
        ├── Load parent spec context
        ├── Execute: claude --print -p "$prompt"
        ├── Parse response (response_analyzer)
        ├── Update prd.json
        ├── Commit if success
        ├── Log to progress.txt
        └── Evaluate exit (ra_should_exit)
```

### Session File Format

```json
{
  "session_id": "uuid",
  "start_time": "2025-01-13T22:00:00Z",
  "last_activity": "2025-01-14T03:45:00Z",
  "iterations": 15,
  "stories_completed": 8,
  "stories_failed": 1,
  "circuit_state": "CLOSED",
  "prd_path": "docs/specs/project/prd.json"
}
```

### Claude Execution

```bash
# Build prompt with context
prompt="You are working on: ${story_title}

Context from spec:
$(cat "${parent_spec}")

Task:
${story_description}

[RALPH_STATUS block required at end]"

# Execute with fresh context
output=$(claude --print -p "$prompt" 2>&1)

# Parse response
echo "$output" | ra_parse_text
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US15 — Mode Script Externe (Fresh Context)**

- Given `/ralph --mode script`, When lancé, Then ralph_loop.sh est exécuté en externe
- Given une story complétée, When le script vérifie, Then nouvelle instance Claude est lancée (fresh context)
- Given crash Claude, When détecté, Then le script survit et peut reprendre avec --continue
- Given mode script, When actif, Then Circuit Breaker et Response Analyzer sont utilisés

**Notes techniques:**
- Basé sur la librairie frankbria/ralph-claude-code
- Fresh context évite le bloat sur longues sessions
- Plus robuste pour overnight (survit aux crashs)
- Utilise prd.json pour le tracking des stories

---

*Generated by /decompose — Project: ralph-wiggum-integration*
