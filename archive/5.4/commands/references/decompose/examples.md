# Decompose Examples

> Reference file for `/decompose` command usage examples.

---

## Example 1: Standard Usage

```
> /decompose migration_architecture_gardel.md

📄 Document: migration_architecture_gardel.md
├── Lines: 1738
├── Slug: migration-gardel
└── Status: Valid

[Analysis in progress...]

⏸️  BREAKPOINT — VALIDATION DÉCOUPAGE

📋 DÉCOUPAGE PROPOSÉ: 9 sous-specs (1-5 jours chacune)

| ID  | Nom                    | Effort | Dépendances |
|-----|------------------------|--------|-------------|
| S01 | Settings Splitting     | 1j     | —           |
| S02 | App Datawarehouse      | 1j     | S01         |
| S03 | Modèles Base           | 2j     | S02         |
| S04 | Modèles Analyses       | 2j     | S03         |
| S05 | Modèles Sources        | 2j     | S03         |
| S06 | Modèles Users          | 2j     | S03         |
| S07 | Admin + Services       | 3j     | S04,S05,S06 |
| S08 | Migration ETL          | 2j     | S07         |
| S09 | Tests + Docs           | 2j     | S08         |

Duration: 17 days (parallel) vs 25 days (sequential)

> Valider

docs/specs/migration-gardel/
├── INDEX.md
├── backlog.md            ← 50 stories (1-2h each)
├── prd.json              ← Ralph format
├── ralph.sh              ← Executable script
├── PROMPT.md             ← System prompt
├── progress.txt          ← Empty logging file
├── S01-settings-splitting.md
├── S02-app-datawarehouse.md
├── S03-modeles-base.md
├── S04-modeles-analyses.md
├── S05-modeles-sources.md
├── S06-modeles-users.md
├── S07-admin-services.md
├── S08-migration-etl.md
└── S09-tests-documentation.md

→ Next: /ralph docs/specs/migration-gardel/
```

---

## Granularity Explanation

The decompose command works at **two levels**:

### Level 1: Sub-Specs (1-5 days each)
Files like `S01-settings-splitting.md` represent **multi-day work packages**.
These are suitable for `/brief` → `/epci` manual execution.

### Level 2: Stories in backlog.md/prd.json (1-2 hours each)
The backlog table breaks down sub-specs into **granular tasks** for Ralph:

| Spec | Effort | Stories Generated |
|------|--------|-------------------|
| S01 (1j) | 8h | 4-8 stories (standard) |
| S03 (2j) | 16h | 8-16 stories (standard) |
| S07 (3j) | 24h | 12-24 stories (standard) |

**Granularity options:**
- `--granularity standard` (default): 1-2h per story
- `--granularity small`: 30-60min per story
- `--granularity micro`: 15-30min per story

---

## Example 2: With Custom Options

```
> /decompose mon-prd.md --output specs/alpha/ --min-days 2 --max-days 4 --think think-hard

[Deep analysis with think-hard...]
[Granularity adjusted to 2-4 days per spec...]

specs/alpha/
├── INDEX.md
├── backlog.md            ← Stories at standard granularity
├── prd.json
├── ralph.sh
├── PROMPT.md
├── progress.txt
└── S01-S05.md files
```

---

## Example 3: With Fine Granularity

```
> /decompose mon-prd.md --granularity micro

[Same sub-specs generated...]
[But backlog.md contains MORE stories, each 15-30 minutes]

backlog.md summary:
- Total stories: 120 (vs 50 with standard)
- Average duration: 20 min per story
- Better for overnight Ralph execution with many small commits
```

---

## Example 4: Small Document (Auto-Redirect)

```
> /decompose simple-feature.md

This document seems simple enough for a single EPCI session.

Estimated effort: 2 days
Recommendation: Use /brief directly

/brief @simple-feature.md
```

---

## backlog.md Sample Output

```markdown
# Backlog — Migration Gardel

> **Généré**: 2025-01-13
> **Source PRD**: migration_architecture_gardel.md
> **Stories totales**: 50
> **Durée estimée**: 100h (17j)
> **Granularité**: standard (1-2h)

## Vue d'ensemble

| # | ID | Tâche | Spec | Type | Cmplx | Prio | Dépendances | Estim. | Status |
|---|-----|-------|------|------|-------|------|-------------|--------|--------|
| 1 | US-001 | Create settings module structure | S01 | Script | M | P1 | - | 1.5h | ⏳ |
| 2 | US-002 | Split database config | S01 | Logic | S | P1 | US-001 | 1h | ⏳ |
| 3 | US-003 | Add environment detection | S01 | Logic | S | P1 | US-001 | 1h | ⏳ |
| 4 | US-004 | Create base settings tests | S01 | Test | M | P1 | US-003 | 1.5h | ⏳ |
| 5 | US-005 | Initialize datawarehouse app | S02 | Script | M | P1 | US-004 | 1.5h | ⏳ |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Par Spec

### S01 — Settings Splitting (4 stories, 5h)

| # | ID | Tâche | Estim. | Dépendances | Status |
|---|-----|-------|--------|-------------|--------|
| 1 | US-001 | Create settings module structure | 1.5h | - | ⏳ |
| 2 | US-002 | Split database config | 1h | US-001 | ⏳ |
| 3 | US-003 | Add environment detection | 1h | US-001 | ⏳ |
| 4 | US-004 | Create base settings tests | 1.5h | US-003 | ⏳ |

### S02 — App Datawarehouse (6 stories, 8h)

...

## Statistiques

| Métrique | Valeur |
|----------|--------|
| Stories totales | 50 |
| Complétées | 0 |
| En cours | 0 |
| Restantes | 50 |
| Parallélisables | 12 |
| Chemin critique | 38 stories |
```
