# PRD — prd.json v2 : Structure enrichie pour Ralph Wiggum

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-2025-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Owner** | EPCI Team |
| **Created** | 2025-01-14 |
| **Last Updated** | 2025-01-14 |
| **Slug** | prd-json-v2 |
| **EMS Score** | 85/100 |
| **Template** | feature |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-14 | EPCI Brainstormer | Initial generation from /brainstorm |

---

## Executive Summary

**TL;DR** : Enrichir la structure du fichier `prd.json` generee par `/decompose` pour ameliorer le tracking, la validation et l'execution autonome par Ralph Wiggum.

| Aspect | Description |
|--------|-------------|
| **Problem** | Le prd.json actuel manque de granularite (pas d'AC structures, pas de tasks, pas de dependances inter-US) |
| **Solution** | Schema prd.json v2 avec acceptanceCriteria[], tasks[], dependencies, execution tracking, testing requirements |
| **Impact** | Ralph peut valider AC par AC, retry intelligent, tracking granulaire |
| **Target Launch** | v5.2.0 |

---

## Background & Strategic Fit

### Why Now?

Le systeme Ralph Wiggum est operationnel mais son efficacite est limitee par le manque de structure dans prd.json :
- Impossible de valider les criteres d'acceptation individuellement
- Pas de breakdown en sous-taches pour le tracking
- Dependances entre User Stories implicites seulement
- Retry aveugle sans historique d'erreurs

### Strategic Alignment

Cette feature s'aligne avec :
- [x] **Vision Produit** : Autonomie complete de Ralph pour execution overnight
- [x] **Position Marche** : Structure proche des standards industrie (Jira, Linear, etc.)

---

## Problem Statement

### Current Situation

Le fichier `prd.json` genere par `/decompose` a une structure minimale :

```json
{
  "id": "US-001",
  "title": "Story title",
  "priority": 1,
  "acceptanceCriteria": "AC in markdown (texte libre)",
  "passes": false
}
```

### Problem Definition

1. **Criteres d'acceptation** : Texte libre, impossible a valider individuellement
2. **Tasks** : Absentes, pas de granularite pour le tracking
3. **Categories/Types** : Absents, pas de filtrage possible
4. **Dependances** : Absentes, ordre d'execution implicite
5. **Tracking** : Minimal (`passes` boolean), pas de retry intelligent
6. **Tests** : Pas de reference aux fichiers de test attendus

### Evidence & Data

- **Quantitative** : Ralph execute ~50 iterations en mode overnight, sans savoir quels AC sont valides
- **Qualitative** : Impossible de reprendre une execution bloquee avec contexte

### Impact of Not Solving

- **Business** : Temps perdu en executions Ralph inefficaces
- **User** : Frustration lors de debug post-execution
- **Technical** : Dette technique dans le workflow EPCI

---

## Goals

### Business Goals

- [ ] Reduire le temps de debug post-Ralph de 50%
- [ ] Permettre le retry intelligent (reprendre au bon endroit)

### User Goals

- [ ] Voir la progression par AC/task dans le prd.json
- [ ] Filtrer les stories par categorie/type

### Technical Goals

- [ ] Schema JSON valide et documente
- [ ] Retrocompatibilite avec prd.json v1

---

## Non-Goals (Out of Scope v1)

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| Modification de `/brainstorm` | Focus sur `/decompose` uniquement | v2 si necessaire |
| Modification de Ralph | Integration dans un second temps | v5.3 |
| UI de visualisation | Hors perimetre CLI | Non prevu |

---

## Personas

### Persona Primaire — Developpeur EPCI

- **Role**: Developpeur utilisant le workflow EPCI pour des features complexes
- **Contexte**: Execute `/decompose` puis `/ralph` pour implementation overnight
- **Pain points**: Pas de visibilite sur la progression, retry aveugle, debug difficile
- **Objectifs**: Avoir un tracking granulaire, reprendre au bon endroit apres echec
- **Quote**: "Je veux savoir exactement quel AC a echoue, pas juste que la story a fail"

---

## Stack Detecte

- **Framework**: Plugin EPCI pour Claude Code
- **Language**: Markdown (commandes), Python (scripts), JSON (schemas)
- **Patterns**: Skill-based architecture, subagent delegation
- **Outils**: `/decompose`, `/ralph`, `ralph-converter` skill

## Exploration Summary

### Codebase Analysis

- **Structure**: Monorepo `src/` avec commands/, skills/, agents/
- **Architecture**: Plugin modulaire avec skills et subagents
- **Test patterns**: Python pytest pour scripts

### Fichiers Potentiels

| Fichier | Action probable | Notes |
|---------|-----------------|-------|
| `src/commands/decompose.md` | Modify | Ajouter schema v2 dans Phase 4 |
| `src/skills/core/ralph-converter/SKILL.md` | Modify | Nouveau schema prd.json |
| `src/commands/references/decompose-templates.md` | Modify | Template prd.json v2 |

### Risques Identifies

- Retrocompatibilite avec anciens prd.json : Low (champs additionnels optionnels)
- Complexite de generation des tasks : Medium (inference depuis specs)

---

## User Stories

### US1 — Generer prd.json avec schema v2

**En tant que** developpeur EPCI,
**Je veux** que `/decompose` genere un prd.json avec le schema v2,
**Afin de** avoir une structure enrichie pour le tracking.

**Acceptance Criteria:**
- [ ] Given une spec decomposee, When `/decompose` s'execute, Then prd.json contient `version: "2.0"`
- [ ] Given une User Story, When generee, Then elle contient `acceptanceCriteria[]` (array structure)
- [ ] Given une User Story, When generee, Then elle contient `tasks[]` (array structure)
- [ ] Given une User Story, When generee, Then elle contient `category`, `type`, `complexity`
- [ ] Given une User Story, When generee, Then elle contient `dependencies.depends_on[]` et `dependencies.blocks[]`
- [ ] Given une User Story, When generee, Then elle contient `execution` (attempts, last_error, files_modified)
- [ ] Given une User Story, When generee, Then elle contient `testing` (test_files, requires_e2e)

**Priorite**: Must-have
**Complexite**: M

---

### US2 — Inferer les tasks depuis les specs

**En tant que** developpeur EPCI,
**Je veux** que les tasks soient generees automatiquement depuis les specs,
**Afin de** ne pas avoir a les ecrire manuellement.

**Acceptance Criteria:**
- [ ] Given une spec avec `## Tasks` ou checklist `- [ ]`, When parsee, Then tasks[] est peuplee
- [ ] Given une spec sans tasks explicites, When parsee, Then tasks[] est inferee depuis les AC
- [ ] Given une task, When generee, Then elle a format `{id: "T1", description: "...", done: false}`

**Priorite**: Must-have
**Complexite**: M

---

### US3 — Inferer category et type

**En tant que** developpeur EPCI,
**Je veux** que category et type soient inferes automatiquement,
**Afin de** pouvoir filtrer les stories.

**Acceptance Criteria:**
- [ ] Given un titre avec "Entity/Model/Service", When analyse, Then category = "backend"
- [ ] Given un titre avec "Component/View/CSS", When analyse, Then category = "frontend"
- [ ] Given un titre avec "endpoint/route/API", When analyse, Then type = "API"
- [ ] Given un titre avec "test/spec", When analyse, Then type = "Test"
- [ ] Given un titre sans keyword reconnu, When analyse, Then type = "Task" (defaut)

**Priorite**: Must-have
**Complexite**: S

---

### US4 — Calculer les dependances inter-US

**En tant que** developpeur EPCI,
**Je veux** que les dependances soient calculees automatiquement,
**Afin de** connaitre l'ordre d'execution optimal.

**Acceptance Criteria:**
- [ ] Given une spec avec "depends on S01", When parsee, Then depends_on inclut les US de S01
- [ ] Given US-002 qui depend de US-001, When calculee, Then US-001.blocks inclut "US-002"
- [ ] Given des US sans dependances explicites, When generees, Then depends_on = []

**Priorite**: Must-have
**Complexite**: M

---

### US5 — Initialiser les champs execution et testing

**En tant que** developpeur EPCI,
**Je veux** que les champs de tracking soient initialises correctement,
**Afin de** pouvoir tracker l'execution.

**Acceptance Criteria:**
- [ ] Given une nouvelle US, When generee, Then `execution.attempts = 0`
- [ ] Given une nouvelle US, When generee, Then `execution.last_error = null`
- [ ] Given une nouvelle US, When generee, Then `execution.files_modified = []`
- [ ] Given une US avec titre mentionnant un fichier, When analysee, Then `testing.test_files` est infere
- [ ] Given une US UI, When analysee, Then `testing.requires_e2e = true` est suggere

**Priorite**: Must-have
**Complexite**: S

---

### US6 — Documenter le schema JSON v2

**En tant que** developpeur EPCI,
**Je veux** un schema JSON documente,
**Afin de** valider les fichiers prd.json.

**Acceptance Criteria:**
- [ ] Given le schema v2, When documente, Then il existe dans `src/schemas/prd-v2.schema.json`
- [ ] Given le schema, When lu, Then toutes les proprietes sont documentees
- [ ] Given un prd.json, When valide contre le schema, Then les erreurs sont claires

**Priorite**: Should-have
**Complexite**: S

---

## Regles Metier

- **RM1**: `passes = true` implique automatiquement `status = "completed"`
- **RM2**: `complexity` est infere : < 45min = S, 45-90min = M, > 90min = L
- **RM3**: `estimated_minutes` est calcule depuis complexity : S=30, M=60, L=120
- **RM4**: IDs sont locaux par US : AC1, AC2, T1, T2 (pas globaux)
- **RM5**: `blocks[]` est l'inverse calcule de `depends_on[]`

---

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| Spec sans tasks explicites | Inferer depuis AC ou titre |
| Spec sans AC | Generer AC generique "Story implementee et testee" |
| Dependance circulaire | Erreur bloquante avec message |
| Category non reconnue | Utiliser string fourni tel quel |
| Type non reconnu | Defaut "Task" |

---

## Success Metrics

| Metrique | Baseline | Cible | Methode de mesure |
|----------|----------|-------|-------------------|
| Champs par US | 8 | 20+ | Comptage schema |
| Tracking granulaire | Non | Oui | AC/tasks individuels |
| Retrocompat | N/A | 100% | Tests anciens prd.json |

---

## User Flow

### Current Experience (As-Is)

```
/decompose PRD.md
       |
       v
  prd.json minimal
       |
       v
  /ralph execute
       |
       v
  Story fail → Pas de detail
       |
       v
  Debug manuel penible
```

### Proposed Experience (To-Be)

```
/decompose PRD.md
       |
       v
  prd.json v2 enrichi
       |
       v
  /ralph execute
       |
       v
  Story fail → AC2 fail, T3 incomplete
       |
       v
  Retry cible + Historique erreur
```

### Key Improvements

| Pain Point Actuel | Solution Proposee | Impact |
|-------------------|-------------------|--------|
| AC en texte libre | AC[] structure | Validation individuelle |
| Pas de tasks | tasks[] | Tracking granulaire |
| Pas de dependances | dependencies{} | Ordre optimal |
| Pas d'historique | execution{} | Retry intelligent |

---

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Retrocompat prd.json v1 | Doit continuer a fonctionner | Champs additionnels, pas de breaking change |
| Inference tasks | Peut etre imprecise | Fallback vers AC si pas de tasks |

---

## Dependances

- **Internes**: `ralph-converter` skill, `decompose-templates.md`
- **Externes**: Aucune

---

## Assumptions

- [x] **Technical** : Les specs ont une structure parsable (## Tasks, ## AC)
- [x] **Business** : Le format enrichi ne complique pas l'usage
- [x] **User** : Les developpeurs veulent plus de granularite

---

## Criteres d'Acceptation Globaux

- [ ] prd.json v2 genere correctement par `/decompose`
- [ ] Anciens prd.json v1 toujours lisibles par Ralph
- [ ] Schema JSON documente
- [ ] Tests de non-regression

---

## Questions Ouvertes

- [ ] Faut-il un outil de migration v1 → v2 ?

---

## FAQ

### Internal FAQ (Equipe)

**Q: Pourquoi pas modifier aussi `/brainstorm` ?**
A: Focus sur `/decompose` d'abord. Si le schema v2 fonctionne bien, on pourra l'etendre a `/brainstorm` dans une version ulterieure.

**Q: Comment gerer les anciens prd.json ?**
A: Retrocompatibilite : les champs additionnels sont ignores par Ralph actuel. Migration progressive.

**Q: Les tasks doivent-elles etre ordonnees ?**
A: Non, l'ordre dans l'array n'implique pas de sequence. Les dependances sont explicites.

### External FAQ (Utilisateurs)

**Q: Mon ancien prd.json va-t-il continuer a fonctionner ?**
A: Oui, retrocompatibilite totale. Les nouveaux champs sont additionnels.

**Q: Dois-je regenerer mes prd.json existants ?**
A: Non obligatoire, mais recommande pour beneficier du tracking enrichi.

---

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | SMALL |
| Fichiers impactes | ~4 |
| Risque global | Low |

---

## Timeline & Milestones

### Target Launch

**Objectif** : v5.2.0

### Key Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| PRD Review Complete | 2025-01-14 | EPCI | In Progress |
| Implementation | TBD | Dev | Not Started |
| Tests | TBD | Dev | Not Started |
| Release v5.2.0 | TBD | EPCI | Not Started |

### Phasing Strategy

**Phase 1 (MVP)** : US1-US5 (generation prd.json v2)
**Phase 2** : US6 (schema JSON formel)

---

## Appendix

### Schema prd.json v2 complet

```json
{
  "$schema": "https://epci.dev/schemas/prd-v2.json",
  "version": "2.0",
  "branchName": "feature/my-feature",
  "projectName": "My Project",
  "generatedAt": "2025-01-14T10:00:00Z",
  "generatedBy": "EPCI /decompose v5.2",

  "config": {
    "max_iterations": 50,
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "granularity": "small"
  },

  "userStories": [
    {
      "id": "US-001",
      "title": "Creer l'entite Priority",
      "category": "backend",
      "type": "Logic",
      "complexity": "M",
      "priority": 1,
      "status": "pending",
      "passes": false,

      "acceptanceCriteria": [
        {"id": "AC1", "description": "L'entite existe avec champs id, name, level", "done": false},
        {"id": "AC2", "description": "Les validations sont en place", "done": false},
        {"id": "AC3", "description": "Les tests unitaires passent", "done": false}
      ],

      "tasks": [
        {"id": "T1", "description": "Creer src/Entity/Priority.php", "done": false},
        {"id": "T2", "description": "Ajouter annotations ORM", "done": false},
        {"id": "T3", "description": "Creer tests/Unit/PriorityTest.php", "done": false}
      ],

      "dependencies": {
        "depends_on": [],
        "blocks": ["US-002", "US-003"]
      },

      "execution": {
        "attempts": 0,
        "last_error": null,
        "files_modified": [],
        "completed_at": null,
        "iteration": null
      },

      "testing": {
        "test_files": [],
        "requires_e2e": false,
        "coverage_target": null
      },

      "context": {
        "parent_spec": "S01-core-models.md",
        "parent_brief": "docs/briefs/my-feature/brief-2025-01-14.md",
        "estimated_minutes": 60
      }
    }
  ]
}
```

### Tables d'inference

**Types (depuis keywords titre):**

| Type | Keywords |
|------|----------|
| Script | script, hook, bash, shell, automation |
| Logic | entity, model, service, function, business |
| API | endpoint, route, controller, REST, GraphQL |
| UI | component, form, view, page, modal |
| Test | test, spec, coverage, e2e |
| Task | (defaut) |

**Categories (depuis contexte):**

| Categorie | Patterns |
|-----------|----------|
| backend | Entity, Repository, Service, Controller |
| frontend | Component, View, CSS, React, Vue |
| fullstack | Mixte backend + frontend |
| infra | Docker, CI, deploy, config |
| test | Tests uniquement |
| docs | Documentation, README |

**Complexity:**

| Complexity | Minutes | Critere |
|------------|---------|---------|
| S | 30 | < 45 min |
| M | 60 | 45-90 min |
| L | 120 | > 90 min |

---

*PRD pret pour EPCI — Lancer `/brief` avec ce contenu.*
