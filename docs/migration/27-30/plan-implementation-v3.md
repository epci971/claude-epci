# Plan d'Implémentation EPCI v3.0

> **Document** : Plan de migration détaillé v2.7 → v3.0
> **Date** : Décembre 2024
> **Statut** : En cours d'implémentation

---

## Table des matières

1. [Résumé exécutif](#1-résumé-exécutif)
2. [Architecture cible](#2-architecture-cible)
3. [Mapping v2.7 → v3.0](#3-mapping-v27--v30)
4. [Phases d'implémentation](#4-phases-dimplémentation)
5. [Détail fichier par fichier](#5-détail-fichier-par-fichier)
6. [Dépendances et ordre](#6-dépendances-et-ordre)
7. [Critères de validation](#7-critères-de-validation)
8. [Risques et mitigations](#8-risques-et-mitigations)

---

## 1. Résumé exécutif

### Objectif

Migrer le plugin EPCI de la version 2.7 (12 commandes monolithiques, ~350KB) vers la version 3.0 (architecture modulaire avec 5 commandes + 5 subagents + 13 skills).

### Gains attendus

| Métrique | v2.7 | v3.0 | Évolution |
|----------|------|------|-----------|
| Commandes | 12 | 5 | -58% |
| Subagents custom | 0 | 5 | +5 |
| Skills | 0 | 13 | +13 |
| Points d'entrée utilisateur | 5 | 1 | -80% |
| Lignes de code | ~10,775 | ~8,500 | -21% |
| Modularité | Faible | Haute | ++ |
| Auto-extension | Non | Oui | ++ |

### Livrables

1. ✅ `CLAUDE.md` — Documentation architecturale développeur
2. ✅ `docs/plan-implementation-v3.md` — Ce document
3. ⏳ `src/` — Implémentation complète v3.0

---

## 2. Architecture cible

### Structure des fichiers

```
src/
├── .claude-plugin/
│   └── plugin.json                    # Manifeste plugin
│
├── agents/                            # 5 subagents custom
│   ├── code-reviewer.md              # Revue qualité code
│   ├── doc-generator.md              # Génération documentation
│   ├── plan-validator.md             # Validation plans
│   ├── qa-reviewer.md                # Revue QA/tests
│   └── security-auditor.md           # Audit sécurité
│
├── commands/                          # 5 commandes
│   ├── create.md                     # /epci:create - Factory
│   ├── epci-brief.md                 # Point d'entrée + routing
│   ├── epci-quick.md                 # Workflow TINY/SMALL
│   ├── epci-spike.md                 # Exploration
│   └── epci.md                       # Workflow complet 3 phases
│
├── scripts/                           # Validation
│   ├── validate_all.py               # Orchestrateur
│   ├── validate_command.py           # Validation commandes
│   ├── validate_skill.py             # Validation skills
│   ├── validate_subagent.py          # Validation subagents
│   └── test_triggering.py            # Tests déclenchement skills
│
└── skills/                            # 13 skills
    ├── core/                          # 5 skills fondamentaux
    │   ├── architecture-patterns/
    │   │   └── SKILL.md
    │   ├── code-conventions/
    │   │   └── SKILL.md
    │   ├── epci-core/
    │   │   └── SKILL.md
    │   ├── git-workflow/
    │   │   └── SKILL.md
    │   └── testing-strategy/
    │       └── SKILL.md
    │
    ├── stack/                         # 4 skills par technologie
    │   ├── java-springboot/
    │   │   └── SKILL.md
    │   ├── javascript-react/
    │   │   └── SKILL.md
    │   ├── php-symfony/
    │   │   └── SKILL.md
    │   └── python-django/
    │       └── SKILL.md
    │
    └── factory/                       # 4 skills Component Factory
        ├── commands-creator/
        │   ├── SKILL.md
        │   ├── references/
        │   │   ├── best-practices.md
        │   │   ├── frontmatter-guide.md
        │   │   ├── argument-patterns.md
        │   │   └── checklist.md
        │   ├── templates/
        │   │   ├── command-simple.md
        │   │   └── command-advanced.md
        │   └── scripts/
        │       └── validate_command.py
        │
        ├── component-advisor/
        │   └── SKILL.md
        │
        ├── skills-creator/
        │   ├── SKILL.md
        │   ├── references/
        │   │   ├── best-practices.md
        │   │   ├── description-formulas.md
        │   │   ├── yaml-rules.md
        │   │   └── checklist.md
        │   ├── templates/
        │   │   ├── skill-simple.md
        │   │   └── skill-advanced.md
        │   └── scripts/
        │       ├── validate_skill.py
        │       └── test_triggering.py
        │
        └── subagents-creator/
            ├── SKILL.md
            ├── references/
            │   ├── best-practices.md
            │   ├── delegation-patterns.md
            │   ├── tools-restriction.md
            │   └── checklist.md
            ├── templates/
            │   └── subagent-template.md
            └── scripts/
                └── validate_subagent.py
```

### Conventions

| Élément | Convention | Exemple |
|---------|------------|---------|
| Commandes | kebab-case, `.md` | `epci-brief.md` |
| Subagents | kebab-case, `.md` | `code-reviewer.md` |
| Skills | kebab-case (dossier) | `php-symfony/SKILL.md` |
| Scripts | snake_case, `.py` | `validate_skill.py` |

---

## 3. Mapping v2.7 → v3.0

### Transformation des commandes

| Fichier v2.7 | Lignes | Destination v3.0 | Action |
|--------------|--------|------------------|--------|
| `epci-workflow-guide-v2.7.md` | 1213 | `docs/migration/v2.7-reference.md` | Archive comme référence |
| `epci-discover-v2.7.md` | 719 | → `epci-brief.md` | Intégrer la boucle de clarification |
| `epci-0-briefing-v2.7.md` | 1019 | → `epci-brief.md` | Point d'entrée + routing |
| `epci-micro-v2.7.md` | 729 | → `epci-quick.md` | Mode TINY |
| `epci-soft-v2.7.md` | 1086 | → `epci-quick.md` | Mode SMALL |
| `epci-1-analyse-v2.7.md` | 744 | → `epci.md` Phase 1 | + @Plan + @plan-validator |
| `epci-2-code-v2.7.md` | 982 | → `epci.md` Phase 2 | + @code-reviewer + conditionnels |
| `epci-3-finalize-v2_7.md` | 1241 | → `epci.md` Phase 3 | + @doc-generator |
| `epci-spike-v2.7.md` | 1161 | → `epci-spike.md` | Simplifier, @Explore very thorough |
| `epci-hotfix-v2.7.md` | 684 | (déprécié) | → `epci-quick` avec urgence |
| `epci-flags-v2.7.md` | 602 | (déprécié) | Utiliser flags natifs Claude |
| `epci-personas-v2.7.md` | 595 | (déprécié) | Utiliser personas natifs Claude |

### Extraction vers Skills

| Source v2.7 | Skill v3.0 | Contenu extrait |
|-------------|------------|-----------------|
| `epci-workflow-guide` | `epci-core` | Workflow EPCI, Feature Document |
| `epci-1-analyse` | `architecture-patterns` | Design patterns, SOLID |
| `epci-2-code` | `code-conventions` | Naming, formatting |
| `epci-2-code` | `testing-strategy` | TDD, coverage |
| `epci-3-finalize` | `git-workflow` | Conventional Commits |

### Extraction vers Subagents

| Source v2.7 | Subagent v3.0 | Rôle extrait |
|-------------|---------------|--------------|
| `epci-1-analyse` | `plan-validator` | Validation du plan |
| `epci-2-code` | `code-reviewer` | Revue code |
| `epci-2-code` | `security-auditor` | Audit sécurité |
| `epci-2-code` | `qa-reviewer` | Revue tests |
| `epci-3-finalize` | `doc-generator` | Génération docs |

---

## 4. Phases d'implémentation

### Vue d'ensemble

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5 ──► Phase 6 ──► Phase 7 ──► Phase 8
Fondations   Core       Subagents   Commands    Stack       Factory     Migration   Tests
             Skills                              Skills      Skills      Docs
```

### Phase 1 : Fondations (Priorité Critique)

**Objectif** : Infrastructure de base pour validation et développement

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 1.1 | `CLAUDE.md` | Doc architecturale | Aucune | ✅ Fait |
| 1.2 | `docs/plan-implementation-v3.md` | Ce document | Aucune | ✅ Fait |
| 1.3 | `src/.claude-plugin/plugin.json` | Manifeste plugin | Aucune | 1h |
| 1.4 | `src/scripts/validate_skill.py` | Validation skills | Aucune | 4h |
| 1.5 | `src/scripts/validate_command.py` | Validation commandes | Aucune | 3h |
| 1.6 | `src/scripts/validate_subagent.py` | Validation subagents | Aucune | 3h |
| 1.7 | `src/scripts/test_triggering.py` | Tests déclenchement | Aucune | 4h |
| 1.8 | `src/scripts/validate_all.py` | Orchestrateur | 1.4-1.7 | 2h |

**Critère de succès** : `python validate_all.py` exécutable sans erreur

---

### Phase 2 : Skills Core (Fondamentaux)

**Objectif** : Skills chargés par toutes les commandes

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 2.1 | `src/skills/core/epci-core/SKILL.md` | Workflow, Feature Doc | 1.4 | 6h |
| 2.2 | `src/skills/core/code-conventions/SKILL.md` | Naming, formatting | 1.4 | 4h |
| 2.3 | `src/skills/core/testing-strategy/SKILL.md` | TDD, coverage | 1.4 | 4h |
| 2.4 | `src/skills/core/architecture-patterns/SKILL.md` | SOLID, DDD | 1.4 | 5h |
| 2.5 | `src/skills/core/git-workflow/SKILL.md` | Commits, branching | 1.4 | 4h |

**Critère de succès** : Tous skills passent `validate_skill.py`

---

### Phase 3 : Subagents Custom

**Objectif** : Quality gates automatisés

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 3.1 | `src/agents/code-reviewer.md` | Revue qualité code | 1.6 | 5h |
| 3.2 | `src/agents/plan-validator.md` | Validation plans | 1.6 | 4h |
| 3.3 | `src/agents/doc-generator.md` | Génération docs | 1.6 | 3h |
| 3.4 | `src/agents/security-auditor.md` | Audit sécurité | 1.6 | 6h |
| 3.5 | `src/agents/qa-reviewer.md` | Revue QA | 1.6 | 5h |

**Critère de succès** : Tous subagents passent `validate_subagent.py`

---

### Phase 4 : Commandes Principales

**Objectif** : Workflows utilisateur

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 4.1 | `src/commands/epci-quick.md` | Workflow TINY/SMALL | 2.1, 2.2, 3.1 | 6h |
| 4.2 | `src/commands/epci-brief.md` | Point d'entrée + routing | 2.1, 2.4 | 8h |
| 4.3 | `src/commands/epci-spike.md` | Exploration time-boxed | 2.1 | 5h |
| 4.4 | `src/commands/epci.md` | Workflow complet 3 phases | 2.*, 3.* | 12h |

**Critère de succès** : Tous commandes passent `validate_command.py`

---

### Phase 5 : Skills Stack

**Objectif** : Support des technologies courantes

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 5.1 | `src/skills/stack/javascript-react/SKILL.md` | React/JS patterns | 1.4 | 5h |
| 5.2 | `src/skills/stack/php-symfony/SKILL.md` | Symfony patterns | 1.4 | 5h |
| 5.3 | `src/skills/stack/python-django/SKILL.md` | Django patterns | 1.4 | 5h |
| 5.4 | `src/skills/stack/java-springboot/SKILL.md` | Spring Boot patterns | 1.4 | 5h |

**Critère de succès** : Auto-détection fonctionnelle

---

### Phase 6 : Component Factory

**Objectif** : Auto-extension du plugin

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 6.1 | `src/skills/factory/skills-creator/` | Création skills | 1.4, 1.7 | 10h |
| 6.2 | `src/skills/factory/commands-creator/` | Création commandes | 1.5 | 8h |
| 6.3 | `src/skills/factory/subagents-creator/` | Création subagents | 1.6 | 8h |
| 6.4 | `src/skills/factory/component-advisor/SKILL.md` | Conseiller | 1.4 | 4h |
| 6.5 | `src/commands/create.md` | Dispatcher Factory | 6.1-6.4 | 4h |

**Critère de succès** : `/epci:create skill test` fonctionne end-to-end

---

### Phase 7 : Documentation Migration

**Objectif** : Guides pour utilisateurs v2.7

| # | Fichier | Description | Dépendances | Effort |
|---|---------|-------------|-------------|--------|
| 7.1 | `docs/migration/v2.7-reference.md` | Archive concepts v2.7 | Aucune | 3h |
| 7.2 | `docs/migration/breaking-changes.md` | Changements cassants | Aucune | 2h |
| 7.3 | `docs/migration/upgrade-guide.md` | Guide migration | 7.1, 7.2 | 4h |

**Critère de succès** : Documentation complète et cohérente

---

### Phase 8 : Tests & Validation

**Objectif** : Validation end-to-end

| # | Test | Scénario | Workflow |
|---|------|----------|----------|
| 8.1 | TINY | Validation 30 chars username | `/epci-brief` → `/epci-quick` |
| 8.2 | SMALL | Email confirmation inscription | `/epci-brief` → `/epci-quick` |
| 8.3 | STANDARD | Reset password avec tokens | `/epci-brief` → `/epci` (3 phases) |
| 8.4 | LARGE | Support multi-tenancy | `/epci-brief` → `/epci --large` |
| 8.5 | SPIKE | GraphQL vs REST | `/epci-brief` → `/epci-spike` |
| 8.6 | Factory | Création skill docker-analyzer | `/epci:create skill` |

**Critère de succès** : Tous scénarios passent sans intervention manuelle

---

## 5. Détail fichier par fichier

### 5.1 plugin.json

**Chemin** : `src/.claude-plugin/plugin.json`

```json
{
  "name": "epci",
  "version": "3.0.0",
  "description": "EPCI - Explore Plan Code Inspect workflow for structured development",
  "author": {
    "name": "EPCI Team"
  },
  "commands": [
    "./commands/epci-brief.md",
    "./commands/epci.md",
    "./commands/epci-quick.md",
    "./commands/epci-spike.md",
    "./commands/create.md"
  ],
  "agents": [
    "./agents/plan-validator.md",
    "./agents/code-reviewer.md",
    "./agents/security-auditor.md",
    "./agents/qa-reviewer.md",
    "./agents/doc-generator.md"
  ]
}
```

---

### 5.2 validate_skill.py

**Chemin** : `src/scripts/validate_skill.py`

**Fonctionnalités** :
- Vérifier existence `SKILL.md`
- Parser YAML frontmatter
- Valider nom (kebab-case, ≤64 chars)
- Valider description (présente, ≤1024 chars, formule correcte)
- Compter tokens (< 5000)
- Vérifier structure références/templates si présents

**Usage** :
```bash
python validate_skill.py <path-to-skill-folder>
python validate_skill.py src/skills/core/epci-core/
```

---

### 5.3 epci-core/SKILL.md

**Chemin** : `src/skills/core/epci-core/SKILL.md`

**Contenu clé** :
- Définition workflow EPCI (4 phases)
- Structure Feature Document
- Catégories de complexité
- Règles de routing
- BREAKPOINTS entre phases

**Chargé par** : Toutes les commandes EPCI

---

### 5.4 epci-brief.md

**Chemin** : `src/commands/epci-brief.md`

**Sources v2.7** :
- `epci-discover-v2.7.md` (boucle clarification)
- `epci-0-briefing-v2.7.md` (évaluation + routing)

**Workflow** :
1. Réception brief brut
2. `@Explore` (medium) — analyse codebase
3. Boucle clarification (max 3 itérations)
4. Évaluation complexité
5. Génération brief structuré
6. Recommandation routing

**Output** : Brief fonctionnel + recommandation (`/epci-quick`, `/epci`, `/epci-spike`)

---

### 5.5 epci.md

**Chemin** : `src/commands/epci.md`

**Sources v2.7** :
- `epci-1-analyse-v2.7.md` → Phase 1
- `epci-2-code-v2.7.md` → Phase 2
- `epci-3-finalize-v2_7.md` → Phase 3

**Structure** :

```markdown
## Phase 1 — Analyse et Planification
- Skills: epci-core, architecture-patterns, [stack]
- Subagents: @Plan (natif), @plan-validator
- Thinking: think hard
- Output: Feature Document §2
- ⏸️ BREAKPOINT

## Phase 2 — Implémentation
- Skills: testing-strategy, code-conventions, [stack]
- Subagents: @code-reviewer, @security-auditor*, @qa-reviewer*
- Thinking: think
- Output: Feature Document §3
- ⏸️ BREAKPOINT

## Phase 3 — Finalisation
- Skills: git-workflow
- Subagents: @doc-generator
- Thinking: think
- Output: Feature Document §4, commits, docs
```

---

### 5.6 code-reviewer.md

**Chemin** : `src/agents/code-reviewer.md`

**Mission** : Revue qualité et maintenabilité du code

**Checklist** :
- SOLID principles
- DRY, KISS, YAGNI
- Naming conventions
- Error handling
- Test coverage
- Performance considerations

**Tools** : `[Read, Grep, Glob]` (read-only)

**Output** : Rapport avec `APPROVED` | `NEEDS_CHANGES` + liste détaillée

---

### 5.7 skills-creator/

**Chemin** : `src/skills/factory/skills-creator/`

**Structure** :
```
skills-creator/
├── SKILL.md                    # Workflow 6 phases
├── references/
│   ├── best-practices.md       # Règles d'or
│   ├── description-formulas.md # Formules triggering
│   ├── yaml-rules.md           # Règles frontmatter
│   └── checklist.md            # Checklist finale
├── templates/
│   ├── skill-simple.md         # Template basique
│   └── skill-advanced.md       # Template avec références
└── scripts/
    ├── validate_skill.py       # Copie pour validation
    └── test_triggering.py      # Tests sémantiques
```

**Workflow 6 phases** :
1. **Analyse** : Problème, scope, persona
2. **Architecture** : Simple/standard/avancé
3. **Description Engineering** : Mots-clés triggering
4. **Workflow Design** : Instructions, exemples
5. **Validation** : Dry-run, checklist
6. **Génération** : Fichiers + scripts + tests

---

## 6. Dépendances et ordre

### Graphe de dépendances

```
                    ┌─────────────────┐
                    │   CLAUDE.md     │
                    │  plan-impl.md   │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   plugin.json   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│validate_skill │   │validate_cmd   │   │validate_agent │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │           ┌───────┴───────┐           │
        │           │ test_trigger  │           │
        │           └───────┬───────┘           │
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴───────┐
                    │ validate_all  │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Core Skills  │   │Stack Skills   │   │Factory Skills │
│   (2.1-2.5)   │   │  (5.1-5.4)    │   │  (6.1-6.4)    │
└───────┬───────┘   └───────────────┘   └───────┬───────┘
        │                                       │
        │           ┌───────────────┐           │
        └──────────►│   Subagents   │◄──────────┘
                    │   (3.1-3.5)   │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │   Commands    │
                    │   (4.1-4.5)   │
                    └───────────────┘
```

### Ordre d'exécution recommandé

1. ✅ `CLAUDE.md`
2. ✅ `docs/plan-implementation-v3.md`
3. `src/.claude-plugin/plugin.json`
4. `src/scripts/validate_skill.py`
5. `src/scripts/validate_command.py`
6. `src/scripts/validate_subagent.py`
7. `src/scripts/test_triggering.py`
8. `src/scripts/validate_all.py`
9. `src/skills/core/epci-core/SKILL.md`
10. `src/skills/core/code-conventions/SKILL.md`
11. `src/skills/core/testing-strategy/SKILL.md`
12. `src/skills/core/architecture-patterns/SKILL.md`
13. `src/skills/core/git-workflow/SKILL.md`
14. `src/agents/code-reviewer.md`
15. `src/agents/plan-validator.md`
16. `src/agents/doc-generator.md`
17. `src/agents/security-auditor.md`
18. `src/agents/qa-reviewer.md`
19. `src/commands/epci-quick.md`
20. `src/commands/epci-brief.md`
21. `src/commands/epci-spike.md`
22. `src/commands/epci.md`
23. `src/skills/stack/javascript-react/SKILL.md`
24. `src/skills/stack/php-symfony/SKILL.md`
25. `src/skills/stack/python-django/SKILL.md`
26. `src/skills/stack/java-springboot/SKILL.md`
27. `src/skills/factory/skills-creator/`
28. `src/skills/factory/commands-creator/`
29. `src/skills/factory/subagents-creator/`
30. `src/skills/factory/component-advisor/SKILL.md`
31. `src/commands/create.md`
32. Tests end-to-end

---

## 7. Critères de validation

### 7.1 Validation automatique

| Script | Cible | Critères |
|--------|-------|----------|
| `validate_skill.py` | Skills | YAML valide, nom kebab-case ≤64 chars, description ≤1024 chars, tokens < 5000 |
| `validate_command.py` | Commands | YAML valide, frontmatter complet, structure correcte |
| `validate_subagent.py` | Subagents | YAML valide, mission focus, tools restrictifs |
| `test_triggering.py` | Skills | Tests matching sémantique positifs et négatifs |
| `validate_all.py` | Tout | Orchestration de tous les validateurs |

### 7.2 Tests fonctionnels

| Scénario | Commandes | Résultat attendu |
|----------|-----------|------------------|
| TINY | `/epci-brief` → `/epci-quick` | 1 fichier modifié, pas de Feature Document |
| SMALL | `/epci-brief` → `/epci-quick` | 2-3 fichiers, tests optionnels |
| STANDARD | `/epci-brief` → `/epci` | Feature Document complet, 3 phases |
| LARGE | `/epci-brief` → `/epci --large` | Tous subagents invoqués |
| SPIKE | `/epci-brief` → `/epci-spike` | Spike Report avec verdict |
| Factory | `/epci:create skill test` | Skill créé et validé |

### 7.3 Quality gates

- [ ] Tous scripts validation passent (exit code 0)
- [ ] Feature Documents bien formés
- [ ] Subagents invoqués appropriément
- [ ] Skills auto-loaded correctement
- [ ] BREAKPOINTS respectés
- [ ] Pas de régression v2.7

---

## 8. Risques et mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Skills ne se déclenchent pas | Moyenne | Haut | Tests triggering exhaustifs |
| Subagents trop verbeux | Moyenne | Moyen | Instructions concises, tools limités |
| Routing incorrect | Faible | Haut | Tests end-to-end par catégorie |
| Performance dégradée | Faible | Moyen | Monitoring tokens, limites strictes |
| Feature Documents incohérents | Moyenne | Moyen | Template strict, validation |
| Factory génère du code invalide | Moyenne | Haut | Validation automatique post-génération |

---

## Changelog

| Date | Version | Changement |
|------|---------|------------|
| 2024-12 | 1.0 | Création initiale |
