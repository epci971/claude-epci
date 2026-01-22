# Plan d'Implémentation — EPCI v6

> **Date**: 2026-01-22
> **Objectif**: Implémenter le plugin EPCI v6 complet
> **Scope**: Phases 1-4 = 30 features
> **Sources**: v6-brainstorm-report.md + v5-brainstorm-report.md

---

## Vue d'Ensemble

### État Actuel

```
src/skills/core/
├── state-manager/       [SKILL.md: 86L] [refs: 1 fichier créé]
├── breakpoint-system/   [SKILL.md: 107L] [refs: vide]
├── complexity-calculator/ [SKILL.md: 107L] [refs: vide]
├── clarification-engine/  [SKILL.md: 120L] [refs: vide]
├── tdd-enforcer/        [SKILL.md: 138L] [refs: vide]
└── project-memory/      [SKILL.md: 137L] [refs: vide]
```

**Git status**: 4 skills non trackés (state-manager, breakpoint-system, clarification-engine, tdd-enforcer)

### Stratégie

1. **Compléter** les SKILL.md existants avec références utiles
2. **Valider** après chaque phase avec `validate_all.py`
3. **Commiter** à la fin de chaque phase

---

## Phase 1 — Core Skills (F01-F06)

> **Priorité**: CRITIQUE — Fondations pour tous les autres composants
> **Parallélisable**: Oui (pas de dépendances inter-skills)

### F01: state-manager => OK

**État**: SKILL.md complet (86L), 1 reference créé

**Tâches restantes**:
- [ ] Valider que `examples.md` est suffisant
- [ ] Ajouter `state-schema.md` si nécessaire (schéma JSON détaillé)

**Fichiers à créer/modifier**:
```
src/skills/core/state-manager/
├── SKILL.md              [existant, OK]
└── references/
    ├── examples.md       [créé]
    └── state-schema.md   [optionnel]
```

---

### F02: breakpoint-system

**État**: SKILL.md complet (107L), references/ vide

**Tâches**:
- [ ] Créer `references/ascii-templates.md` — Templates ASCII pour chaque type de breakpoint
- [ ] Créer `references/integration-guide.md` — Comment intégrer avec AskUserQuestion

**Fichiers à créer**:
```
src/skills/core/breakpoint-system/
├── SKILL.md                    [existant, OK]
└── references/
    ├── ascii-templates.md      [à créer]
    └── integration-guide.md    [à créer]
```

**Contenu ascii-templates.md**:
```markdown
# Templates ASCII par Type

## Type: analysis
┌─────────────────────────────────────────────┐
│ 🔍 ANALYSE — {title}                        │
├─────────────────────────────────────────────┤
│ {findings}                                  │
├─────────────────────────────────────────────┤
│ [1] Continuer  [2] Modifier  [3] Annuler    │
└─────────────────────────────────────────────┘

## Type: validation
┌─────────────────────────────────────────────┐
│ ✓ VALIDATION — {title}                      │
├─────────────────────────────────────────────┤
│ ✓ Check 1                                   │
│ ✓ Check 2                                   │
│ ✗ Check 3 (failed)                          │
├─────────────────────────────────────────────┤
│ [1] Approuver  [2] Corriger  [3] Rejeter    │
└─────────────────────────────────────────────┘

## Type: decision
┌─────────────────────────────────────────────┐
│ ⚡ DÉCISION REQUISE — {title}               │
├─────────────────────────────────────────────┤
│ {context}                                   │
├─────────────────────────────────────────────┤
│ [1] Option A  [2] Option B  [3] Autre       │
└─────────────────────────────────────────────┘
```

---

### F03: complexity-calculator

**État**: SKILL.md complet (107L), references/ vide

**Tâches**:
- [ ] Créer `references/scoring-details.md` — Formule complète avec exemples
- [ ] Créer `references/routing-table.md` — Table de décision workflow

**Fichiers à créer**:
```
src/skills/core/complexity-calculator/
├── SKILL.md                  [existant, OK]
└── references/
    ├── scoring-details.md    [à créer]
    └── routing-table.md      [à créer]
```

**Contenu scoring-details.md** (extrait):
```markdown
# Formule de Scoring Détaillée

## Conversion des facteurs en scores (0-100)

### Files Score
| Files | Score |
|-------|-------|
| 1     | 10    |
| 2-3   | 30    |
| 4-6   | 50    |
| 7-10  | 70    |
| 10+   | 100   |

## Exemples de calcul
...
```

---

### F04: clarification-engine

**État**: SKILL.md complet (120L), references/ vide

**Tâches**:
- [ ] Créer `references/ambiguity-patterns.md` — Patterns de détection d'ambiguïté
- [ ] Créer `references/question-templates.md` — Templates de questions par contexte

**Fichiers à créer**:
```
src/skills/core/clarification-engine/
├── SKILL.md                    [existant, OK]
└── references/
    ├── ambiguity-patterns.md   [à créer]
    └── question-templates.md   [à créer]
```

---

### F05: tdd-enforcer

**État**: SKILL.md complet (138L), references/ vide

**Tâches**:
- [ ] Créer `references/workflow-red-green-refactor.md` — Cycle TDD détaillé
- [ ] Créer `references/coverage-rules.md` — Règles de couverture par complexité

**Fichiers à créer**:
```
src/skills/core/tdd-enforcer/
├── SKILL.md                          [existant, OK]
└── references/
    ├── workflow-red-green-refactor.md [à créer]
    └── coverage-rules.md              [à créer]
```

---

### F06: project-memory

**État**: SKILL.md complet (137L), references/ vide

**Tâches**:
- [ ] Créer `references/storage-format.md` — Format des fichiers JSON
- [ ] Créer `references/migration-guide.md` — Migration depuis v5 (.project-memory/)

**Fichiers à créer**:
```
src/skills/core/project-memory/
├── SKILL.md                  [existant, OK]
└── references/
    ├── storage-format.md     [à créer]
    └── migration-guide.md    [à créer]
```

---

### Validation Phase 1

```bash
# Après création de tous les fichiers
python src/scripts/validate_all.py

# Commit
git add src/skills/core/
git commit -m "feat(skills): complete Phase 1 core skills references"
```

---

## Phase 2 — User Skills (F07-F14)

> **Priorité**: HAUTE — Interface utilisateur
> **Dépendances**: Phase 1 (core skills)
> **Ordre recommandé**: factory → brainstorm → spec → implement → quick → debug → improve → refactor

### F07: brainstorm

**État**: SKILL.md minimal (41L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec workflow complet
- [ ] Créer `references/ems-scoring.md` — Système EMS 5 axes
- [ ] Créer `references/hmw-questions.md` — Templates "How Might We"
- [ ] Créer `references/techniques-library.md` — Bibliothèque de techniques

**Output**: CDC.md

---

### F08: spec

**État**: SKILL.md minimal (52L), references/ + templates/ vides

**Tâches**:
- [ ] Enrichir SKILL.md avec workflow décomposition
- [ ] Créer `templates/prd-template.md` — Template PRD
- [ ] Créer `templates/cdc-template.md` — Template CDC
- [ ] Créer `references/ralph-generation.md` — Génération .ralph/

**Output**: PRD.md + PRD.json + .ralph/

---

### F09: implement

**État**: SKILL.md minimal (54L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec phases EPCI détaillées
- [ ] Créer `references/phase-workflow.md` — Détail de chaque phase
- [ ] Créer `templates/feature-doc.md` — Template Feature Document

**Output**: Code + Tests + Feature Doc

---

### F10: quick

**État**: SKILL.md minimal (51L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec workflow TINY vs SMALL
- [ ] Créer `references/tiny-workflow.md` — Workflow < 50 LOC
- [ ] Créer `references/small-workflow.md` — Workflow < 200 LOC

**Output**: Code + Tests

---

### F11: debug

**État**: SKILL.md minimal (52L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec Tree of Thought
- [ ] Créer `references/hypothesis-workflow.md` — Méthodologie diagnostic
- [ ] Créer `references/tree-of-thought.md` — Exploration structurée

**Output**: Fix + Test régression

---

### F12: improve

**État**: SKILL.md minimal (53L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec impact analysis
- [ ] Créer `references/impact-analysis.md` — Analyse d'impact
- [ ] Créer `references/minimal-plan.md` — Planification minimale

**Output**: Updated code + Updated Feature Doc

---

### F13: refactor

**État**: SKILL.md minimal (54L), references/ vide

**Tâches**:
- [ ] Enrichir SKILL.md avec métriques
- [ ] Créer `references/code-smells.md` — Catalogue de code smells
- [ ] Créer `references/metrics-report.md` — Format rapport métriques

**Output**: Cleaner code + Metrics report

---

### F14: factory

**État**: SKILL.md complet (369L), 5 références existantes

**Tâches**:
- [ ] Vérifier que les 5 références sont à jour
- [ ] Ajouter support `--agent` pour Phase 3

**Fichiers existants**:
```
src/skills/factory/references/
├── best-practices-synthesis.md  [existant]
├── checklist-validation.md      [existant]
├── description-formulas.md      [existant]
├── yaml-rules.md                [existant]
└── skill-templates.md           [existant]
```

---

### Validation Phase 2

```bash
python src/scripts/validate_all.py
git add src/skills/
git commit -m "feat(skills): complete Phase 2 user skills"
```

---

## Phase 3 — Subagents (F15-F28)

> **Priorité**: MOYENNE — Délégation de tâches spécialisées
> **Prérequis**: F14 (factory avec --agent)

### F15: Étendre factory avec --agent

**Tâches**:
- [ ] Modifier `factory/SKILL.md` pour supporter `--agent`
- [ ] Créer `references/agent-template.md` — Template pour agents
- [ ] Documenter différences skill vs agent

**Différences agent vs skill**:
| Aspect | Skill | Agent |
|--------|-------|-------|
| Emplacement | `skills/` | `agents/` |
| Frontmatter | name, description | + model, + skills |
| Invocation | Direct | Délégation |
| Contexte | Partagé | Isolé |

---

### Agents Brainstorm (F16-F19)

| ID | Agent | Model | Fichier |
|----|-------|-------|---------|
| F16 | @ems-evaluator | Haiku | `agents/ems-evaluator.md` |
| F17 | @technique-advisor | Haiku | `agents/technique-advisor.md` |
| F18 | @expert-panel | Sonnet | `agents/expert-panel.md` |
| F19 | @party-orchestrator | Sonnet | `agents/party-orchestrator.md` |

---

### Agents Shared (F20-F21)

| ID | Agent | Model | Fichier |
|----|-------|-------|---------|
| F20 | @clarifier | Haiku | `agents/clarifier.md` |
| F21 | @planner | Sonnet | `agents/planner.md` |

---

### Agents Implement (F22-F28)

| ID | Agent | Model | Fichier |
|----|-------|-------|---------|
| F22 | @plan-validator | Opus | `agents/plan-validator.md` |
| F23 | @decompose-validator | Opus | `agents/decompose-validator.md` |
| F24 | @implementer | Sonnet | `agents/implementer.md` |
| F25 | @code-reviewer | Opus | `agents/code-reviewer.md` |
| F26 | @security-auditor | Opus | `agents/security-auditor.md` |
| F27 | @qa-reviewer | Sonnet | `agents/qa-reviewer.md` |
| F28 | @doc-generator | Sonnet | `agents/doc-generator.md` |

---

### Validation Phase 3

```bash
python src/scripts/validate_all.py
git add src/agents/ src/skills/factory/
git commit -m "feat(agents): complete Phase 3 subagents"
```

---

## Phase 4 — Ralph System (F29-F30)

> **Priorité**: MOYENNE — Exécution batch overnight

### F29: Templates .ralph/

**Tâches**:
- [ ] Créer template `PROMPT.md` — Instructions Claude Code
- [ ] Créer template `MEMORY.md` — Contexte persistant
- [ ] Créer template `ralph.sh` — Script runner
- [ ] Intégrer génération dans `/spec`

**Structure générée par /spec**:
```
.ralph/
├── PROMPT.md     # Instructions pour Claude Code
├── MEMORY.md     # Contexte persistant entre sessions
├── ralph.sh      # Script exécution batch
└── stories/      # Stories atomiques
    ├── 001-*.md
    └── ...
```

---

### F30: Validation Schemas

**État**: 2 schemas existent dans `src/schemas/`

**Tâches**:
- [ ] Vérifier `ralph-index-v1.json` conformité v6
- [ ] Vérifier `feature-state-v1.json` conformité v6
- [ ] Mettre à jour si nécessaire

---

### Validation Phase 4

```bash
python src/scripts/validate_all.py
git add src/schemas/ src/skills/spec/
git commit -m "feat(ralph): complete Phase 4 Ralph system"
```

---

## Résumé des Livrables

### Par Phase

| Phase | Features | Fichiers créés | Fichiers modifiés |
|-------|----------|----------------|-------------------|
| 1 | F01-F06 | ~12 références | 0 |
| 2 | F07-F14 | ~16 références + templates | 8 SKILL.md enrichis |
| 3 | F15-F28 | 13 agents + 1 référence | factory/SKILL.md |
| 4 | F29-F30 | 3 templates | 2 schemas (si nécessaire) |

### Commits

```
feat(skills): complete Phase 1 core skills references
feat(skills): complete Phase 2 user skills
feat(agents): complete Phase 3 subagents
feat(ralph): complete Phase 4 Ralph system
```

---

## Notes

1. **Validation continue**: Exécuter `validate_all.py` après chaque sous-phase
2. **Git tracking**: Commiter les 4 skills non trackés en Phase 1
3. **Tests manuels**: Tester chaque skill après complétion
4. **Documentation**: Mettre à jour CLAUDE.md si API change
