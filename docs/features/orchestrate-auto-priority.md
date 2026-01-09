# Feature Document — Orchestrateur Automatique EPCI

> **Slug**: `orchestrate-auto-priority`
> **Category**: LARGE
> **Date**: 2026-01-09

---

## S1 — Functional Brief

### Context

Le workflow EPCI actuel traite les features une par une avec intervention humaine. Pour les projets avec de nombreuses specs indépendantes (issues de `/decompose`), ce mode manuel devient un goulot d'étranglement.

L'objectif est de lancer une orchestration automatique avant la nuit et revenir le matin avec toutes les features implémentées, testées et committées.

### Detected Stack

- **Framework**: Plugin EPCI pour Claude Code
- **Language**: Python 3 (orchestration), Markdown (specs, commandes)
- **Patterns**: DAGBuilder, WaveContext, HookRunner, ProjectMemory
- **Outils**: asyncio, project-memory, hook system

### Acceptance Criteria

- [ ] Parse INDEX.md avec dépendances → DAG construit correctement
- [ ] Exécute specs dans l'ordre DAG + priorité (effort croissant)
- [ ] Skip specs si dépendance échoue (DAG-aware)
- [ ] Auto-correction jusqu'à 3 retries par spec
- [ ] Commit automatique si validation réussie
- [ ] Journal MD lisible avec format documenté
- [ ] Journal JSON parsable avec structure validée
- [ ] INDEX.md mis à jour en temps réel
- [ ] Rapport final avec métriques complètes
- [ ] `--dry-run` affiche plan sans exécuter
- [ ] `--continue` reprend après interruption
- [ ] Libération contexte entre chaque spec
- [ ] Plan interactif avec actions Y/n/edit/reorder/skip
- [ ] Priority format: entier 1-99 (1 = plus haute)
- [ ] Timeout proportionnel: TINY:15m, SMALL:30m, STD:1h, LARGE:2h

### Constraints

- Mode séquentiel uniquement (évite conflits git)
- Maximum 3 retries par spec (configurable)
- Un commit = une spec validée
- Clear contexte entre chaque spec

### Out of Scope

- Parallélisme inter-features
- Orchestration cross-repos
- Notifications externes (Slack/email/webhook)
- Rollback automatique

### Evaluation

- **Category**: LARGE
- **Estimated files**: 8-10
- **Estimated LOC**: ~2000-2500
- **Risk**: LOW (infrastructure mature, pas de conflits)
- **Justification**: Nouvelle commande majeure avec skill complet et 6 références

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think-hard` | auto | LARGE complexity |
| `--wave` | auto | complexity > 0.7 |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin (Python 3 + Markdown)
- **Features completed**: 15
- **Velocity**: stable
- **Conventions**: kebab-case files, SKILL.md pattern

### Files to Create

| File | Action | Description |
|------|--------|-------------|
| `src/commands/orchestrate.md` | CREATE | Définition commande |
| `src/skills/core/orchestrator-batch/SKILL.md` | CREATE | Logique orchestration |
| `src/skills/core/orchestrator-batch/references/dag-building.md` | CREATE | DAG construction |
| `src/skills/core/orchestrator-batch/references/priority-sorting.md` | CREATE | Algorithme tri |
| `src/skills/core/orchestrator-batch/references/auto-retry-strategy.md` | CREATE | Stratégie retry |
| `src/skills/core/orchestrator-batch/references/dual-journaling.md` | CREATE | Formats journal |
| `src/skills/core/orchestrator-batch/references/project-memory-integration.md` | CREATE | Intégration mémoire |
| `src/skills/core/orchestrator-batch/references/hooks-integration.md` | CREATE | Points hooks |

### Reusable Infrastructure

| Module | API | Usage |
|--------|-----|-------|
| `dag_builder.py` | `DAGBuilder`, `DAG.topological_sort()` | Construction DAG, détection cycles |
| `wave_context.py` | `WaveContext`, `Wave` | Accumulation état |
| `hooks/runner.py` | `run_hooks()` | Lifecycle events |
| `project-memory/manager.py` | `save_feature_history()` | Persistence résultats |

### Decisions

| # | Decision | Justification |
|---|----------|---------------|
| D1 | Full auto sans breakpoints | Use case overnight |
| D2 | Retry-then-skip (max 3) | Robustesse sans blocage |
| D3 | Séquentiel strict | Évite conflits git |
| D4 | Journal dual (MD + JSON) | Lisibilité + tooling |
| D5 | DAG-aware skip | Intelligence sur dépendances |
| D6 | Update INDEX.md temps réel | Visibilité progression |
| D7 | Full loop validation | Tests + lint + review |
| D8 | Tri par effort croissant | Quick wins d'abord |
| D9 | Override via priority | Flexibilité sans refonte DAG |
| D10 | Plan interactif | Validation avant exécution |
| D11 | Propagation priorité | Gestion cas complexes DAG |
| D12 | Format tableau | Affichage clair du plan |
| D13 | Actions Y/n/edit/reorder/skip | Contrôle complet utilisateur |
| D14 | Priority = entier 1-99 | Tri fin, 1 = plus haute |
| D15 | Timeout proportionnel | TINY:15m, SMALL:30m, STD:1h, LARGE:2h |

---

## S2 — Implementation Plan

### Impacted Files

| File | Action | Risk | Est. |
|------|--------|------|------|
| `src/commands/orchestrate.md` | CREATE | Low | 15min |
| `src/skills/core/orchestrator-batch/SKILL.md` | CREATE | Medium | 20min |
| `src/skills/core/orchestrator-batch/references/dag-building.md` | CREATE | Low | 10min |
| `src/skills/core/orchestrator-batch/references/priority-sorting.md` | CREATE | Low | 10min |
| `src/skills/core/orchestrator-batch/references/auto-retry-strategy.md` | CREATE | Low | 10min |
| `src/skills/core/orchestrator-batch/references/dual-journaling.md` | CREATE | Low | 10min |
| `src/skills/core/orchestrator-batch/references/project-memory-integration.md` | CREATE | Low | 5min |
| `src/skills/core/orchestrator-batch/references/hooks-integration.md` | CREATE | Low | 5min |

**Total estimé**: ~90 min (LARGE) — 10 tasks atomiques (2-15 min chacune)

### Tasks

#### T1 — Créer la commande orchestrate.md (15 min)
- **File**: `src/commands/orchestrate.md`
- **Content**:
  - Frontmatter YAML (description, argument-hint, allowed-tools)
  - 6 phases: Load Memory, Parse INDEX.md, Build Plan, Execute Loop, Journal, Report
  - Plan interactif avec prompt Y/n/edit/reorder/skip
  - Flags: `--dry-run`, `--continue`, `--max-retries`, `--skip`, `--only`, `--no-commit`, `--verbose`
- **Pattern**: Suivre structure de `decompose.md`
- **Test**: Validation via `validate_command.py`

#### T2a — Créer le skill SKILL.md structure (10 min)
- **File**: `src/skills/core/orchestrator-batch/SKILL.md`
- **Content**: Frontmatter, Overview, Configuration table, Process overview
- **Pattern**: Suivre structure de `epci-core/SKILL.md`
- **Dependencies**: T1

#### T2b — Créer le skill SKILL.md intégration (10 min)
- **File**: `src/skills/core/orchestrator-batch/SKILL.md` (append)
- **Content**: Agents section, Hooks section, References links, Examples
- **Dependencies**: T2a

#### T3 — Créer reference dag-building.md (10 min)
- **File**: `src/skills/core/orchestrator-batch/references/dag-building.md`
- **Content**: Utilisation DAGBuilder API, cycle detection, topological sort
- **Dependencies**: T2b

#### T4 — Créer reference priority-sorting.md (10 min)
- **File**: `src/skills/core/orchestrator-batch/references/priority-sorting.md`
- **Content**: Algorithme tri (effort croissant + priority override + propagation)
- **Dependencies**: T3 (builds on DAG concepts)

#### T5 — Créer reference auto-retry-strategy.md (10 min)
- **File**: `src/skills/core/orchestrator-batch/references/auto-retry-strategy.md`
- **Content**: Stratégie retry (3 tentatives, skip, DAG-aware)
- **Dependencies**: T2b

#### T6 — Créer reference dual-journaling.md (10 min)
- **File**: `src/skills/core/orchestrator-batch/references/dual-journaling.md`
- **Content**: Format journal MD + JSON, templates
- **Dependencies**: T2b

#### T7 — Créer reference project-memory-integration.md (5 min)
- **File**: `src/skills/core/orchestrator-batch/references/project-memory-integration.md`
- **Content**: Sauvegarde résultats, métriques vélocité
- **Dependencies**: T2b

#### T8 — Créer reference hooks-integration.md (5 min)
- **File**: `src/skills/core/orchestrator-batch/references/hooks-integration.md`
- **Content**: Hook points (pre-orchestrate, post-spec, post-orchestrate)
- **Dependencies**: T2b

#### T9 — Valider tous les fichiers (5 min)
- **Action**: Exécuter `python src/scripts/validate_all.py`
- **Verify**: Token limits (command < 5000, skill < 5000, refs < 2000 each)
- **Dependencies**: T1-T8
- **Success**: Aucune erreur de validation

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Tokens skill > 5000 | Medium | Validation fail | Split en références |
| Incohérence avec patterns existants | Low | Maintenance | Suivre templates exacts |
| Oubli d'un flag | Low | Fonctionnalité incomplète | Checklist flags |

### Validation

- **@plan-validator**: APPROVED (2026-01-09)
  - All 10 tasks atomic (2-15 min)
  - Dependencies verified
  - Infrastructure confirmed

---

## S3 — Implementation & Finalization

### Progress

- [x] T1 — Créer orchestrate.md (15 min)
- [x] T2a — Créer SKILL.md structure (10 min)
- [x] T2b — Créer SKILL.md intégration (10 min)
- [x] T3 — Créer dag-building.md (10 min)
- [x] T4 — Créer priority-sorting.md (10 min)
- [x] T5 — Créer auto-retry-strategy.md (10 min)
- [x] T6 — Créer dual-journaling.md (10 min)
- [x] T7 — Créer project-memory-integration.md (5 min)
- [x] T8 — Créer hooks-integration.md (5 min)
- [x] T9 — Validation (5 min)

### Files Created

| File | Tokens | Status |
|------|--------|--------|
| `src/commands/orchestrate.md` | ~1652 | PASSED |
| `src/skills/core/orchestrator-batch/SKILL.md` | ~1380 | PASSED |
| `src/skills/core/orchestrator-batch/references/dag-building.md` | ~650 | OK |
| `src/skills/core/orchestrator-batch/references/priority-sorting.md` | ~700 | OK |
| `src/skills/core/orchestrator-batch/references/auto-retry-strategy.md` | ~600 | OK |
| `src/skills/core/orchestrator-batch/references/dual-journaling.md` | ~900 | OK |
| `src/skills/core/orchestrator-batch/references/project-memory-integration.md` | ~450 | OK |
| `src/skills/core/orchestrator-batch/references/hooks-integration.md` | ~500 | OK |

### Validation

```
Skills:      28 passed (including orchestrator-batch)
Commands:    12 passed (including orchestrate)
```

### Reviews

- **@code-reviewer**: APPROVED (2 minor fixes applied)
  - Fixed: DAG API reference (DAGBuilder → DAG)
  - Fixed: Added --no-hooks flag to arguments
- **@security-auditor**: N/A (no auth/security files)
- **@qa-reviewer**: N/A (no test files)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| - | None | Implementation matches plan |

### Documentation

- **CLAUDE.md**: Ready for update (add /orchestrate to commands table)
- **README**: N/A (internal plugin component)
- **CHANGELOG**: Pending commit

### PR Ready

- Branch: `master` (direct commit, internal plugin)
- Tests: N/A (Markdown documentation only)
- Lint: PASSED (validate_all.py)
- Docs: Feature Document complete
