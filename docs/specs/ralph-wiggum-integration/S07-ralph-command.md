# Specification — S07: Commande /ralph unifiée

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S07
> **Estimated effort**: 2 day(s)
> **Dependencies**: S06
> **Blocks**: S08

---

## 1. Context

This sub-spec implements the main `/ralph` command, which unifies both Hook and Script modes under a single interface. It supports mode selection (automatic or explicit), dry-run for planning, and hybrid mode for combining prd.json tracking with spec context.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US5, US6

---

## 2. Scope

### Included

- `/ralph` command definition
- `--mode hook|script` flag
- `--dry-run` flag for planning
- `--max-iterations` mandatory parameter
- `--overnight` flag for script mode suggestion
- Hybrid mode: prd.json + parent spec context
- Progress display and status output

### Excluded

- Stop hook implementation (S01)
- Circuit Breaker (S02)
- Response Analyzer (S03)
- ralph_loop.sh (S04)
- prd.json generation (S05)
- @ralph-executor (S06)
- Rate limiting, sécurité (S08)

---

## 3. Tasks

- [ ] Create `src/commands/ralph.md`
  - [ ] Define command metadata and description
  - [ ] Document all arguments and flags
  - [ ] Implement argument parsing:
    - [ ] `<specs-dir>`: Directory with prd.json
    - [ ] `--mode hook|script`: Execution mode
    - [ ] `--dry-run`: Show plan without execution
    - [ ] `--max-iterations N`: Mandatory iteration limit
    - [ ] `--overnight`: Suggest script mode
    - [ ] `--continue`: Resume interrupted session
    - [ ] `--reset-circuit`: Reset circuit breaker

- [ ] Implement mode selection:
  - [ ] Auto-select based on context:
    - [ ] < 10 stories, < 2h estimated → hook
    - [ ] >= 10 stories, >= 2h estimated → script
    - [ ] --overnight flag → script
  - [ ] Display recommendation with reason
  - [ ] Allow explicit override with --mode

- [ ] Implement dry-run mode:
  - [ ] Load prd.json
  - [ ] Display story list with status
  - [ ] Show estimated duration
  - [ ] Show recommended mode
  - [ ] Exit without execution

- [ ] Implement hybrid mode (US6):
  - [ ] Read story from prd.json
  - [ ] Load parent_spec file for context
  - [ ] Pass both to @ralph-executor
  - [ ] Update prd.json on completion

- [ ] Implement progress display:
  - [ ] Show current story (X/N)
  - [ ] Show elapsed time
  - [ ] Show completed/failed counts
  - [ ] Update progress.txt in real-time

- [ ] Implement validation:
  - [ ] Check prd.json exists
  - [ ] Check specs directory valid
  - [ ] Validate --max-iterations provided
  - [ ] Check dependencies (jq installed)

- [ ] Write tests for /ralph command

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S07-AC1 | Given directory with prd.json, When `/ralph` launched, Then execution starts | Basic execution test |
| S07-AC2 | Given `--dry-run` flag, When /ralph runs, Then plan displayed without execution | Dry-run test |
| S07-AC3 | Given `--max-iterations 20`, When limit reached, Then execution stops cleanly | Iteration limit test |
| S07-AC4 | Given story US-005 in S02, When @ralph-executor runs, Then S02.md loaded as context | Hybrid mode test |
| S07-AC5 | Given context loaded, When /brief analyzes, Then exploration targeted to spec scope | Context targeting test |
| S07-AC6 | Given < 10 stories, When mode not specified, Then hook mode recommended | Auto-selection test |
| S07-AC7 | Given --overnight flag, When mode not specified, Then script mode recommended | Overnight test |

---

## 5. Technical Notes

### Command Arguments

```
/ralph <specs-dir> [options]

Arguments:
  <specs-dir>         Directory containing prd.json

Options:
  --mode <hook|script>  Execution mode (auto-detected if not specified)
  --dry-run             Show plan without execution
  --max-iterations <N>  Maximum iterations (REQUIRED)
  --overnight           Suggest script mode, enable rate limiting
  --continue            Resume interrupted session
  --reset-circuit       Reset circuit breaker to CLOSED
  --calls <N>           Rate limit per hour (default: 100)
  --safety-level <L>    minimal|moderate|strict (default: moderate)
```

### Mode Auto-Selection

```
┌─────────────────────────────────┐
│ Mode Auto-Selection             │
├─────────────────────────────────┤
│ IF stories < 10                 │
│    AND estimated_hours < 2      │
│    THEN recommend: hook         │
│                                 │
│ IF stories >= 10                │
│    OR estimated_hours >= 2      │
│    OR --overnight flag          │
│    THEN recommend: script       │
└─────────────────────────────────┘
```

### Hybrid Mode Flow

```
/ralph docs/specs/project/
    │
    ├── Load prd.json
    │   └── Get story with passes=false
    │
    ├── Load parent_spec
    │   └── Read S02-circuit-breaker.md
    │
    ├── Call @ralph-executor
    │   ├── story: {id, title, ...}
    │   └── context: S02.md content
    │
    ├── Update prd.json
    │   └── Set passes=true if success
    │
    └── Continue to next story
```

### Progress Display

```
┌─────────────────────────────────────────────────┐
│ 🔄 Ralph Wiggum — Iteration 15/50               │
├─────────────────────────────────────────────────┤
│ Current: US-015 — Implement cb_evaluate         │
│ Parent:  S02-circuit-breaker.md                 │
│                                                 │
│ Progress: ████████░░ 8/10 stories               │
│ Status:   ✅ 7 passed | ❌ 1 failed | ⏳ 2 pending│
│ Elapsed:  1h 23m                                │
│ Circuit:  CLOSED                                │
└─────────────────────────────────────────────────┘
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US5 — Commande /ralph**

- Given un dossier avec prd.json, When je lance `/ralph`, Then l'exécution démarre
- Given le flag `--dry-run`, When je lance /ralph, Then le plan est affiché sans exécution
- Given le flag `--max-iterations 20`, When la limite est atteinte, Then l'exécution s'arrête proprement

**US6 — Mode hybride (prd.json + specs contexte)**

- Given une story US-005 appartenant à S02, When @ralph-executor s'exécute, Then S02.md est chargé comme contexte
- Given le contexte chargé, When /brief analyse, Then l'exploration est ciblée sur le périmètre de la spec

---

*Generated by /decompose — Project: ralph-wiggum-integration*
