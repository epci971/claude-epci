# Backlog — Ralph Wiggum Integration

> **Generated**: 2025-01-14
> **Source PRD**: PRD-ralph-wiggum-integration-2025-01-13.md
> **Stories totales**: 45
> **Duration estimee**: 48h (12j)
> **Granularite**: small

---

## Vue d'ensemble

| # | ID | Tache | Spec | Type | Cmplx | Prio | Dependances | Estim. | Status |
|---|-----|-------|------|------|-------|------|-------------|--------|--------|
| 1 | US-001 | Create ralph-stop-hook.sh script | S01 | Script | M | P1 | - | 1.5h | ⏳ |
| 2 | US-002 | Implement JSONL transcript reading | S01 | Logic | S | P1 | US-001 | 1h | ⏳ |
| 3 | US-003 | Implement completion promise detection | S01 | Logic | S | P1 | US-002 | 1h | ⏳ |
| 4 | US-004 | Implement prompt re-injection | S01 | Logic | M | P1 | US-003 | 1h | ⏳ |
| 5 | US-005 | Create ralph-loop.local.md template | S01 | Task | S | P1 | US-001 | 0.5h | ⏳ |
| 6 | US-006 | Create cancel-ralph command | S01 | Logic | S | P1 | US-005 | 1h | ⏳ |
| 7 | US-007 | Write stop hook tests | S01 | Test | M | P1 | US-004 | 1.5h | ⏳ |
| 8 | US-008 | Create circuit_breaker.sh state machine | S02 | Script | M | P1 | - | 1.5h | ⏳ |
| 9 | US-009 | Implement no-progress tracking | S02 | Logic | S | P1 | US-008 | 1h | ⏳ |
| 10 | US-010 | Implement same-error tracking | S02 | Logic | S | P1 | US-008 | 1h | ⏳ |
| 11 | US-011 | Implement state transitions (CLOSED/HALF_OPEN/OPEN) | S02 | Logic | M | P1 | US-009, US-010 | 1.5h | ⏳ |
| 12 | US-012 | Implement circuit reset function | S02 | Logic | S | P1 | US-011 | 0.5h | ⏳ |
| 13 | US-013 | Create response_analyzer.sh | S02 | Script | M | P1 | - | 1.5h | ⏳ |
| 14 | US-014 | Implement JSON parsing with jq | S02 | Logic | S | P1 | US-013 | 1h | ⏳ |
| 15 | US-015 | Implement RALPH_STATUS extraction | S02 | Logic | M | P1 | US-014 | 1h | ⏳ |
| 16 | US-016 | Implement stuck loop detection | S02 | Logic | M | P1 | US-015 | 1h | ⏳ |
| 17 | US-017 | Implement dual-condition exit evaluation | S02 | Logic | M | P1 | US-016 | 1h | ⏳ |
| 18 | US-018 | Create date_utils.sh | S02 | Script | S | P1 | - | 0.5h | ⏳ |
| 19 | US-019 | Document RALPH_STATUS format | S02 | Task | S | P1 | US-015 | 0.5h | ⏳ |
| 20 | US-020 | Write Circuit Breaker tests | S02 | Test | M | P1 | US-012 | 1.5h | ⏳ |
| 21 | US-021 | Write Response Analyzer tests | S02 | Test | M | P1 | US-017 | 1.5h | ⏳ |
| 22 | US-022 | Create ralph-converter skill structure | S03 | Task | S | P1 | US-017 | 0.5h | ⏳ |
| 23 | US-023 | Implement prd.json v2 generation | S03 | Logic | M | P1 | US-022 | 1.5h | ⏳ |
| 24 | US-024 | Implement story inference rules | S03 | Logic | M | P1 | US-023 | 1h | ⏳ |
| 25 | US-025 | Implement acceptance criteria extraction | S03 | Logic | S | P1 | US-024 | 1h | ⏳ |
| 26 | US-026 | Implement dependency mapping | S03 | Logic | S | P1 | US-025 | 1h | ⏳ |
| 27 | US-027 | Create PROMPT.md template | S03 | Task | M | P1 | US-019 | 1h | ⏳ |
| 28 | US-028 | Implement stack detection | S03 | Logic | S | P1 | US-027 | 1h | ⏳ |
| 29 | US-029 | Create ralph.sh template | S03 | Script | M | P1 | US-008, US-013 | 1.5h | ⏳ |
| 30 | US-030 | Implement session state persistence | S03 | Logic | M | P1 | US-029 | 1h | ⏳ |
| 31 | US-031 | Update decompose command documentation | S03 | Task | S | P1 | US-026 | 0.5h | ⏳ |
| 32 | US-032 | Write ralph-converter tests | S03 | Test | M | P1 | US-026 | 1.5h | ⏳ |
| 33 | US-033 | Create ralph-executor agent structure | S04 | Task | S | P1 | US-030 | 0.5h | ⏳ |
| 34 | US-034 | Implement story context loading | S04 | Logic | M | P1 | US-033 | 1h | ⏳ |
| 35 | US-035 | Implement /brief integration | S04 | Logic | M | P1 | US-034 | 1.5h | ⏳ |
| 36 | US-036 | Implement complexity-based routing | S04 | Logic | M | P1 | US-035 | 1h | ⏳ |
| 37 | US-037 | Implement Feature Document generation | S04 | Logic | M | P1 | US-036 | 1h | ⏳ |
| 38 | US-038 | Create ralph command structure | S04 | Task | S | P1 | US-037 | 0.5h | ⏳ |
| 39 | US-039 | Implement mode selection and flags | S04 | Logic | M | P1 | US-038 | 1.5h | ⏳ |
| 40 | US-040 | Implement dry-run mode | S04 | Logic | S | P1 | US-039 | 1h | ⏳ |
| 41 | US-041 | Write ralph-executor tests | S04 | Test | M | P1 | US-037 | 1.5h | ⏳ |
| 42 | US-042 | Implement --safety-level flag | S05 | Logic | S | P2 | US-039 | 1h | ⏳ |
| 43 | US-043 | Add /orchestrate deprecation warning | S05 | Task | S | P2 | - | 0.5h | ⏳ |
| 44 | US-044 | Implement rate limiting | S05 | Logic | M | P2 | US-029 | 1.5h | ⏳ |
| 45 | US-045 | Implement intelligent mode selection | S05 | Logic | S | P2 | US-039 | 1h | ⏳ |

---

## Par Spec

### S01 — Mode Hook (Anthropic) (7 stories, 8h)

| # | ID | Tache | Estim. | Dependances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-001 | Create ralph-stop-hook.sh script | 1.5h | - | ⏳ |
| 2 | US-002 | Implement JSONL transcript reading | 1h | US-001 | ⏳ |
| 3 | US-003 | Implement completion promise detection | 1h | US-002 | ⏳ |
| 4 | US-004 | Implement prompt re-injection | 1h | US-003 | ⏳ |
| 5 | US-005 | Create ralph-loop.local.md template | 0.5h | US-001 | ⏳ |
| 6 | US-006 | Create cancel-ralph command | 1h | US-005 | ⏳ |
| 7 | US-007 | Write stop hook tests | 1.5h | US-004 | ⏳ |

### S02 — Circuit Breaker & Analyzer (14 stories, 14h)

| # | ID | Tache | Estim. | Dependances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-008 | Create circuit_breaker.sh state machine | 1.5h | - | ⏳ |
| 2 | US-009 | Implement no-progress tracking | 1h | US-008 | ⏳ |
| 3 | US-010 | Implement same-error tracking | 1h | US-008 | ⏳ |
| 4 | US-011 | Implement state transitions | 1.5h | US-009, US-010 | ⏳ |
| 5 | US-012 | Implement circuit reset function | 0.5h | US-011 | ⏳ |
| 6 | US-013 | Create response_analyzer.sh | 1.5h | - | ⏳ |
| 7 | US-014 | Implement JSON parsing with jq | 1h | US-013 | ⏳ |
| 8 | US-015 | Implement RALPH_STATUS extraction | 1h | US-014 | ⏳ |
| 9 | US-016 | Implement stuck loop detection | 1h | US-015 | ⏳ |
| 10 | US-017 | Implement dual-condition exit evaluation | 1h | US-016 | ⏳ |
| 11 | US-018 | Create date_utils.sh | 0.5h | - | ⏳ |
| 12 | US-019 | Document RALPH_STATUS format | 0.5h | US-015 | ⏳ |
| 13 | US-020 | Write Circuit Breaker tests | 1.5h | US-012 | ⏳ |
| 14 | US-021 | Write Response Analyzer tests | 1.5h | US-017 | ⏳ |

### S03 — Generation prd.json & Scripts (11 stories, 11h)

| # | ID | Tache | Estim. | Dependances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-022 | Create ralph-converter skill structure | 0.5h | US-017 | ⏳ |
| 2 | US-023 | Implement prd.json v2 generation | 1.5h | US-022 | ⏳ |
| 3 | US-024 | Implement story inference rules | 1h | US-023 | ⏳ |
| 4 | US-025 | Implement acceptance criteria extraction | 1h | US-024 | ⏳ |
| 5 | US-026 | Implement dependency mapping | 1h | US-025 | ⏳ |
| 6 | US-027 | Create PROMPT.md template | 1h | US-019 | ⏳ |
| 7 | US-028 | Implement stack detection | 1h | US-027 | ⏳ |
| 8 | US-029 | Create ralph.sh template | 1.5h | US-008, US-013 | ⏳ |
| 9 | US-030 | Implement session state persistence | 1h | US-029 | ⏳ |
| 10 | US-031 | Update decompose command documentation | 0.5h | US-026 | ⏳ |
| 11 | US-032 | Write ralph-converter tests | 1.5h | US-026 | ⏳ |

### S04 — Integration Commande Ralph (9 stories, 10h)

| # | ID | Tache | Estim. | Dependances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-033 | Create ralph-executor agent structure | 0.5h | US-030 | ⏳ |
| 2 | US-034 | Implement story context loading | 1h | US-033 | ⏳ |
| 3 | US-035 | Implement /brief integration | 1.5h | US-034 | ⏳ |
| 4 | US-036 | Implement complexity-based routing | 1h | US-035 | ⏳ |
| 5 | US-037 | Implement Feature Document generation | 1h | US-036 | ⏳ |
| 6 | US-038 | Create ralph command structure | 0.5h | US-037 | ⏳ |
| 7 | US-039 | Implement mode selection and flags | 1.5h | US-038 | ⏳ |
| 8 | US-040 | Implement dry-run mode | 1h | US-039 | ⏳ |
| 9 | US-041 | Write ralph-executor tests | 1.5h | US-037 | ⏳ |

### S05 — Security & Polish (4 stories, 4h)

| # | ID | Tache | Estim. | Dependances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-042 | Implement --safety-level flag | 1h | US-039 | ⏳ |
| 2 | US-043 | Add /orchestrate deprecation warning | 0.5h | - | ⏳ |
| 3 | US-044 | Implement rate limiting | 1.5h | US-029 | ⏳ |
| 4 | US-045 | Implement intelligent mode selection | 1h | US-039 | ⏳ |

---

## Statistiques

| Metrique | Valeur |
|----------|--------|
| Stories totales | 45 |
| Completees | 0 |
| En cours | 0 |
| Echouees | 0 |
| Restantes | 45 |
| Parallelisables | 8 (US-001, US-008, US-013, US-018 peuvent demarrer en parallele) |
| Chemin critique | 28 stories |

---

## Par Priorite

| Priorite | Stories | Heures |
|----------|---------|--------|
| P1 (Must) | 41 | 44h |
| P2 (Should) | 4 | 4h |
| P3 (Could) | 0 | 0h |

---

## Legende

| Symbole | Status |
|---------|--------|
| ⏳ | Pending |
| 🔄 | In Progress |
| ✅ | Completed |
| ❌ | Failed |
| 🚫 | Blocked |

| Complexite | Duree |
|------------|-------|
| S (Small) | < 45 min |
| M (Medium) | 45-90 min |
| L (Large) | > 90 min |

| Type | Description |
|------|-------------|
| Script | Shell scripts, hooks, automation |
| Logic | Business logic, functions |
| API | Endpoints, routes, REST |
| UI | Components, forms, views |
| Test | Test files, specs |
| Task | General tasks |

---

_Generated by /decompose — Project: ralph-wiggum-integration_
