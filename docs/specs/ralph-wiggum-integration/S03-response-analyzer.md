# Specification — S03: Response Analyzer + RALPH_STATUS

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S03
> **Estimated effort**: 2 day(s)
> **Dependencies**: S02
> **Blocks**: S04, S05

---

## 1. Context

This sub-spec implements the **Response Analyzer** and **RALPH_STATUS block** for structured communication between Claude and the Ralph loop script. The dual-condition exit pattern (completion indicators + explicit EXIT_SIGNAL) prevents both premature exits and infinite loops.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US10, US11

---

## 2. Scope

### Included

- Response Analyzer shell library (`response_analyzer.sh`)
- RALPH_STATUS block format specification
- JSON and text output parsing
- Dual-condition exit logic
- Stuck loop detection
- PROMPT.md template with RALPH_STATUS section

### Excluded

- Circuit Breaker (S02 — dependency)
- Full ralph_loop.sh script (S04)
- prd.json generation (S05)

---

## 3. Tasks

- [ ] Create `src/scripts/lib/response_analyzer.sh`
  - [ ] Implement `ra_init()` — Initialize analyzer
  - [ ] Implement `ra_parse_json()` — Parse JSON-formatted output
  - [ ] Implement `ra_parse_text()` — Parse text output with RALPH_STATUS block
  - [ ] Implement `ra_extract_status()` — Extract RALPH_STATUS fields
  - [ ] Implement `ra_detect_format()` — Auto-detect JSON vs text
  - [ ] Implement `ra_should_exit()` — Dual-condition exit evaluation
  - [ ] Implement `ra_detect_stuck_loop()` — Check for repeated errors
  - [ ] Implement `ra_get_work_type()` — Extract work type from output

- [ ] Implement RALPH_STATUS parsing:
  - [ ] STATUS: IN_PROGRESS | COMPLETE | BLOCKED
  - [ ] TASKS_COMPLETED_THIS_LOOP: number
  - [ ] FILES_MODIFIED: number
  - [ ] TESTS_STATUS: PASSING | FAILING | NOT_RUN
  - [ ] WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
  - [ ] EXIT_SIGNAL: false | true
  - [ ] RECOMMENDATION: string

- [ ] Implement dual-condition exit:
  - [ ] Check completion_indicators >= 2
  - [ ] Check EXIT_SIGNAL explicit value
  - [ ] EXIT_SIGNAL=false overrides completion heuristics
  - [ ] Return exit reason (project_complete, max_iterations, blocked, etc.)

- [ ] Create `src/templates/ralph/PROMPT.md`
  - [ ] Project context section
  - [ ] Task instructions section
  - [ ] RALPH_STATUS format specification (mandatory)
  - [ ] Example RALPH_STATUS block
  - [ ] Stack-specific placeholders

- [ ] Implement fallback for missing RALPH_STATUS:
  - [ ] Warning message
  - [ ] Heuristic text analysis
  - [ ] Conservative continue behavior

- [ ] Write BATS tests for response analyzer

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S03-AC1 | Given JSON output, When response_analyzer runs, Then structured fields extracted | JSON parsing test |
| S03-AC2 | Given text output with RALPH_STATUS, When parsed, Then EXIT_SIGNAL extracted | Text parsing test |
| S03-AC3 | Given same error in last 3 outputs, When detect_stuck_loop runs, Then returns true | Stuck detection test |
| S03-AC4 | Given completion_indicators >= 2 AND EXIT_SIGNAL=true, When should_exit evaluated, Then returns "project_complete" | Exit logic test |
| S03-AC5 | Given completion_indicators >= 2 BUT EXIT_SIGNAL=false, When should_exit evaluated, Then continues (explicit signal priority) | Override test |
| S03-AC6 | Given PROMPT.md generated, When created, Then contains RALPH_STATUS section with format | Template test |
| S03-AC7 | Given RALPH_STATUS absent, When analyzed, Then warning logged and fallback used | Fallback test |
| S03-AC8 | Given STATUS=BLOCKED in output, When analyzed, Then circuit breaker notified | Integration test |

---

## 5. Technical Notes

### RALPH_STATUS Block Format

```
---RALPH_STATUS---
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_COMPLETED_THIS_LOOP: <number>
FILES_MODIFIED: <number>
TESTS_STATUS: PASSING | FAILING | NOT_RUN
WORK_TYPE: IMPLEMENTATION | TESTING | DOCUMENTATION | REFACTORING
EXIT_SIGNAL: false | true
RECOMMENDATION: <one line summary>
---END_RALPH_STATUS---
```

### Dual-Condition Exit Logic

```
completion_indicators = count of:
  - All tasks done
  - Tests passing
  - No pending stories
  - STATUS=COMPLETE

if completion_indicators >= 2:
    if EXIT_SIGNAL == true:
        return "project_complete"
    else:
        # Claude explicitly wants to continue
        return "continue"
else:
    return "continue"
```

### API Functions

```bash
# Initialize
ra_init

# Parse Claude output
output=$(cat claude_response.txt)
format=$(ra_detect_format "$output")

if [[ "$format" == "json" ]]; then
    ra_parse_json "$output"
else
    ra_parse_text "$output"
fi

# Check exit condition
exit_reason=$(ra_should_exit)
case "$exit_reason" in
    "project_complete") echo "Done!"; exit 0 ;;
    "blocked") cb_record_failure "blocked" ;;
    "continue") continue_loop ;;
esac
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US10 — Response Analyzer**

- Given sortie Claude en JSON, When response_analyzer s'exécute, Then les champs structurés sont extraits
- Given sortie Claude en texte, When le bloc RALPH_STATUS est présent, Then il est parsé pour extraire exit_signal
- Given même erreur dans les 3 dernières sorties, When detect_stuck_loop s'exécute, Then retourne true
- Given completion_indicators >= 2 ET EXIT_SIGNAL=true, When should_exit est évalué, Then retourne "project_complete"
- Given completion_indicators >= 2 MAIS EXIT_SIGNAL=false, When should_exit est évalué, Then continue

**US11 — RALPH_STATUS Block obligatoire**

- Given template PROMPT.md généré, When il est créé, Then il contient la section RALPH_STATUS avec format obligatoire
- Given une itération Claude terminée, When la sortie est analysée, Then le bloc RALPH_STATUS est présent
- Given bloc RALPH_STATUS avec EXIT_SIGNAL=false, When completion patterns détectés, Then EXIT_SIGNAL a priorité
- Given bloc RALPH_STATUS avec STATUS=BLOCKED, When analysé, Then le circuit breaker est notifié

---

*Generated by /decompose — Project: ralph-wiggum-integration*
