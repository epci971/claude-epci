# Ralph Wiggum Integration — Backlog

> **Generated**: 2025-01-13
> **Source**: PRD-ralph-wiggum-integration-2025-01-13.md
> **Total Stories**: 32
> **Estimated Duration**: ~48h (12 jours parallélisés)

---

## Sub-Specifications Summary

| Spec | Title | Effort | Stories | Dependencies |
|------|-------|--------|---------|--------------|
| S01 | Mode Hook Anthropic | 2j | 5 | — |
| S02 | Circuit Breaker | 2j | 4 | — |
| S03 | Response Analyzer + RALPH_STATUS | 2j | 5 | S02 |
| S04 | Mode Script Externe | 2j | 5 | S02, S03 |
| S05 | Génération prd.json et templates | 3j | 5 | S03 |
| S06 | Subagent @ralph-executor | 3j | 4 | S01, S04 |
| S07 | Commande /ralph unifiée | 2j | 2 | S06 |
| S08 | Polish & Migration | 2j | 2 | S07 |

---

## Stories Backlog

### S01 — Mode Hook Anthropic (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-001 | Create ralph-stop-hook.sh with hook registration | 90min | 1 | ⏳ |
| US-002 | Implement YAML frontmatter parsing in stop hook | 60min | 1 | ⏳ |
| US-003 | Implement completion detection (`<promise>COMPLETE</promise>`) | 60min | 1 | ⏳ |
| US-004 | Create ralph-loop.local.md template | 45min | 1 | ⏳ |
| US-005 | Create /cancel-ralph command | 60min | 1 | ⏳ |

### S02 — Circuit Breaker (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-006 | Create circuit_breaker.sh with cb_init and cb_get_state | 90min | 1 | ⏳ |
| US-007 | Implement cb_record_success and cb_record_failure | 60min | 1 | ⏳ |
| US-008 | Implement state transitions (CLOSED/HALF_OPEN/OPEN) | 90min | 1 | ⏳ |
| US-009 | Implement same error detection and cb_reset | 60min | 1 | ⏳ |

### S03 — Response Analyzer + RALPH_STATUS (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-010 | Create response_analyzer.sh with ra_init and ra_detect_format | 90min | 1 | ⏳ |
| US-011 | Implement ra_parse_json and ra_parse_text | 90min | 1 | ⏳ |
| US-012 | Implement RALPH_STATUS block parsing | 60min | 1 | ⏳ |
| US-013 | Implement dual-condition exit logic (ra_should_exit) | 90min | 1 | ⏳ |
| US-014 | Create PROMPT.md template with RALPH_STATUS section | 60min | 1 | ⏳ |

### S04 — Mode Script Externe (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-015 | Create date_utils.sh with cross-platform functions | 60min | 1 | ⏳ |
| US-016 | Create ralph_loop.sh main structure and argument parsing | 90min | 1 | ⏳ |
| US-017 | Implement main loop with story execution | 120min | 1 | ⏳ |
| US-018 | Implement session management and --continue flag | 90min | 1 | ⏳ |
| US-019 | Implement Ctrl+C handling and checkpoint saving | 60min | 1 | ⏳ |

### S05 — Génération prd.json et templates (3j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-020 | Create ralph-converter skill structure | 90min | 1 | ⏳ |
| US-021 | Implement spec parsing and granularity-based splitting | 120min | 1 | ⏳ |
| US-022 | Implement prd.json generation with parent_spec mapping | 90min | 1 | ⏳ |
| US-023 | Implement ralph.sh launcher script generation | 60min | 1 | ⏳ |
| US-024 | Implement PROMPT.md stack detection and generation | 90min | 1 | ⏳ |

### S06 — Subagent @ralph-executor (3j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-025 | Create @ralph-executor agent definition | 90min | 1 | ⏳ |
| US-026 | Implement /brief integration and routing logic | 120min | 1 | ⏳ |
| US-027 | Create ralph-analyzer skill for result analysis | 90min | 1 | ⏳ |
| US-028 | Implement minimal Feature Document generation | 60min | 1 | ⏳ |

### S07 — Commande /ralph unifiée (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-029 | Create /ralph command with argument parsing | 90min | 1 | ⏳ |
| US-030 | Implement hybrid mode and progress display | 90min | 1 | ⏳ |

### S08 — Polish & Migration (2j)

| ID | Story | Est. | Priority | Status |
|----|-------|------|----------|--------|
| US-031 | Implement security levels and rate limiting | 90min | 2 | ⏳ |
| US-032 | Implement /orchestrate deprecation and documentation updates | 90min | 2 | ⏳ |

---

## Execution Order (DAG)

```
Parallel Start:
├── S01 (Mode Hook) ─────────────────────────────────┐
└── S02 (Circuit Breaker) ──┐                        │
                            ↓                        │
                    S03 (Response Analyzer) ──┐      │
                            │                 │      │
                            ↓                 ↓      │
                    S04 (Mode Script)    S05 (Gen)   │
                            │                 │      │
                            └────────┬────────┘      │
                                     ↓               │
                            S06 (@ralph-executor) ←──┘
                                     ↓
                            S07 (/ralph command)
                                     ↓
                            S08 (Polish & Migration)
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⏳ | Pending |
| 🔄 | In Progress |
| ✅ | Completed |
| ❌ | Failed |
| ⏸️ | Blocked |

---

*Generated by /decompose — Project: ralph-wiggum-integration*
