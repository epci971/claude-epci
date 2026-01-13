# Specification — S02: Circuit Breaker

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S02
> **Estimated effort**: 2 day(s)
> **Dependencies**: —
> **Blocks**: S03, S04

---

## 1. Context

This sub-spec implements the **Circuit Breaker pattern** for Ralph, preventing infinite loops and token waste when the agent gets stuck. Based on Michael Nygard's "Release It!" pattern and frankbria/ralph-claude-code implementation.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US9

---

## 2. Scope

### Included

- Circuit Breaker shell library (`circuit_breaker.sh`)
- Three states: CLOSED (normal), HALF_OPEN (monitoring), OPEN (stopped)
- Stagnation detection (no file changes)
- Same error detection (repeated failures)
- State persistence in session file
- `--reset-circuit` flag to recover from OPEN state

### Excluded

- Response Analyzer (S03)
- RALPH_STATUS parsing (S03)
- Rate limiting (S08)
- Full ralph_loop.sh script (S04)

---

## 3. Tasks

- [ ] Create `src/scripts/lib/circuit_breaker.sh`
  - [ ] Implement `cb_init()` — Initialize circuit breaker state
  - [ ] Implement `cb_get_state()` — Return current state (CLOSED/HALF_OPEN/OPEN)
  - [ ] Implement `cb_record_success()` — Record successful iteration
  - [ ] Implement `cb_record_failure()` — Record failed iteration
  - [ ] Implement `cb_check_progression()` — Check if files were modified
  - [ ] Implement `cb_evaluate()` — Main evaluation logic
  - [ ] Implement `cb_reset()` — Reset to CLOSED state
  - [ ] Implement `cb_get_stats()` — Return diagnostic info

- [ ] Implement state transitions:
  - [ ] CLOSED → HALF_OPEN: 3 iterations without file changes
  - [ ] HALF_OPEN → OPEN: Still no progression after threshold
  - [ ] HALF_OPEN → CLOSED: Progression detected (files modified)
  - [ ] OPEN → CLOSED: Manual `--reset-circuit` flag

- [ ] Implement same error detection:
  - [ ] Track last N error messages (default 5)
  - [ ] Detect if same error repeated consecutively
  - [ ] Trigger OPEN state after CB_SAME_ERROR_THRESHOLD (default 5)

- [ ] Add configurable thresholds:
  - [ ] `CB_NO_PROGRESS_THRESHOLD` (default 3)
  - [ ] `CB_SAME_ERROR_THRESHOLD` (default 5)
  - [ ] `CB_HALF_OPEN_RETRIES` (default 2)

- [ ] Write BATS tests for circuit breaker

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S02-AC1 | Given 3 loops without file changes, When circuit breaker evaluates, Then state becomes HALF_OPEN | State transition test |
| S02-AC2 | Given HALF_OPEN and still no progression, When threshold reached, Then state becomes OPEN | State transition test |
| S02-AC3 | Given OPEN state, When user runs `--reset-circuit`, Then state becomes CLOSED | Reset test |
| S02-AC4 | Given 5 loops with same error, When circuit breaker evaluates, Then state becomes OPEN | Error detection test |
| S02-AC5 | Given HALF_OPEN and files modified, When circuit breaker evaluates, Then state becomes CLOSED | Recovery test |
| S02-AC6 | Given circuit breaker stats requested, When `cb_get_stats()` called, Then diagnostic info returned | Stats test |

---

## 5. Technical Notes

### State Machine

```
┌─────────┐   3 no progress   ┌───────────┐   threshold   ┌────────┐
│ CLOSED  │ ───────────────→  │ HALF_OPEN │ ───────────→  │  OPEN  │
└─────────┘                   └───────────┘               └────────┘
     ↑                              │                          │
     │      progression detected    │                          │
     └──────────────────────────────┘                          │
     │                                                         │
     │                    --reset-circuit                      │
     └─────────────────────────────────────────────────────────┘
```

### API Functions

```bash
# Initialize
cb_init "/path/to/session.json"

# Check state before iteration
state=$(cb_get_state)
if [[ "$state" == "OPEN" ]]; then
    echo "Circuit breaker OPEN - manual intervention required"
    exit 1
fi

# After iteration
if files_modified; then
    cb_record_success
else
    cb_record_failure "$error_message"
fi

# Evaluate state
cb_evaluate
new_state=$(cb_get_state)
```

### Configuration

```bash
# Environment variables (optional)
export CB_NO_PROGRESS_THRESHOLD=3
export CB_SAME_ERROR_THRESHOLD=5
export CB_HALF_OPEN_RETRIES=2
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US9 — Circuit Breaker Pattern**

- Given 3 boucles consécutives sans changement de fichiers, When le circuit breaker évalue, Then il passe en état HALF_OPEN
- Given état HALF_OPEN et toujours pas de progression, When le seuil est atteint, Then circuit passe en OPEN
- Given état OPEN, When l'utilisateur lance `--reset-circuit`, Then circuit revient en CLOSED
- Given 5 boucles avec la même erreur répétée, When le circuit breaker évalue, Then il passe en OPEN
- Given progression détectée en HALF_OPEN, When des fichiers sont modifiés, Then circuit revient en CLOSED

**Notes techniques:**
- Pattern basé sur Michael Nygard "Release It!"
- États: CLOSED (normal) → HALF_OPEN (monitoring) → OPEN (arrêt)
- Seuils configurables

---

*Generated by /decompose — Project: ralph-wiggum-integration*
