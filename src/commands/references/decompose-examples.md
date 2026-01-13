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

📋 DÉCOUPAGE PROPOSÉ: 9 sous-specs

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
├── S01-settings-splitting.md
├── S02-app-datawarehouse.md
├── S03-modeles-base.md
├── S04-modeles-analyses.md
├── S05-modeles-sources.md
├── S06-modeles-users.md
├── S07-admin-services.md
├── S08-migration-etl.md
├── S09-tests-documentation.md
├── prd.json              ← Stories (if Ralph mode)
├── backlog.md            ← Backlog table view
├── ralph.sh              ← Executable loop script
├── PROMPT.md             ← System prompt
└── progress.txt          ← Empty logging file

→ Next: /ralph docs/specs/migration-gardel/
```

---

## Example 2: With Custom Options

```
> /decompose mon-prd.md --output specs/alpha/ --min-days 2 --max-days 4 --think think-hard

[Deep analysis with think-hard...]
[Granularity adjusted to 2-4 days per spec...]
```

---

## Example 3: Small Document (Auto-Redirect)

```
> /decompose simple-feature.md

This document seems simple enough for a single EPCI session.

Estimated effort: 2 days
Recommendation: Use /brief directly

/brief @simple-feature.md
```
