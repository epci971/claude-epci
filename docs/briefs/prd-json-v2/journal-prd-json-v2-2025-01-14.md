# Journal d'Exploration — prd.json v2

> **Feature**: prd.json v2 : Structure enrichie pour Ralph Wiggum
> **Date**: 2025-01-14
> **Iterations**: 4

---

## Resume

Session de brainstorm pour definir la structure enrichie du fichier prd.json genere par `/decompose`. L'objectif est d'ameliorer le tracking, la validation des criteres d'acceptation et l'execution autonome par Ralph Wiggum. La session a converge vers un schema v2 complet avec acceptanceCriteria[], tasks[], dependencies, execution tracking et testing requirements.

---

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 25 | - | Analyse fichiers existants |
| 1 | 45 | +20 | Structure proposee, questions scope |
| 2 | 65 | +20 | Categories, statuts, dependances |
| 3 | 80 | +15 | Champs finaux, regles d'inference |
| Final | 85 | +5 | Validation schema complet |

---

## EMS Final Detaille

| Axe | Score |
|-----|-------|
| Clarte | 90/100 |
| Profondeur | 85/100 |
| Couverture | 85/100 |
| Decisions | 80/100 |
| Actionnabilite | 85/100 |

---

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Version | v5.0 |
| Template | feature |
| Techniques appliquees | Questions iteratives, schema-first design |
| Duree exploration | ~15min |

---

## Decisions Cles

### Decision 1 — Scope limite a /decompose

- **Contexte**: L'utilisateur voulait potentiellement modifier plusieurs commandes
- **Options considerees**: A) /decompose seul, B) + /brainstorm, C) + Ralph
- **Choix**: A) /decompose seul
- **Justification**: Focus MVP, extension future possible

### Decision 2 — Retrocompatibilite

- **Contexte**: Gestion des anciens prd.json
- **Options considerees**: A) Migration progressive (champs optionnels), B) Breaking change
- **Choix**: A) Migration progressive
- **Justification**: Pas de friction pour utilisateurs existants

### Decision 3 — Source des tasks

- **Contexte**: D'ou viennent les tasks dans chaque US
- **Options considerees**: A) Depuis specs, B) Depuis brainstorm, C) Inference runtime
- **Choix**: A) Depuis specs
- **Justification**: /decompose a acces aux specs, generation automatique

### Decision 4 — Relation status/passes

- **Contexte**: Comment interagissent ces deux champs
- **Options considerees**: A) passes=true → status=completed, B) Independants, C) passes calcule
- **Choix**: A) passes=true → status=completed automatique
- **Justification**: Coherence, pas de desync possible

### Decision 5 — Format IDs

- **Contexte**: IDs des AC et tasks
- **Options considerees**: A) Locaux (AC1, T1), B) Globaux (US-001-AC1), C) Avec spec
- **Choix**: A) Locaux simples
- **Justification**: Simplicite, contexte US suffit

### Decision 6 — Champs obligatoires

- **Contexte**: Quels champs sont requis
- **Options considerees**: A) Core seul, B) Core + AC, C) Tous
- **Choix**: C) Tous les champs obligatoires
- **Justification**: Structure complete, initialisation par defaut

### Decision 7 — Ajout complexity et type

- **Contexte**: Champs additionnels
- **Options considerees**: A) complexity, B) type, C) assignee, D) aucun
- **Choix**: A et B (complexity S/M/L + type Script/Logic/API/UI/Test)
- **Justification**: Deja dans backlog.md, utile pour filtrage

---

## Questions Resolues

| Question | Reponse | Iteration |
|----------|---------|-----------|
| Scope de modification | /decompose uniquement | 1 |
| Retrocompatibilite | Oui, champs additionnels | 1 |
| Source des tasks | Generees depuis specs | 1 |
| Categories supportees | String libre | 2 |
| Statuts US | pending/in_progress/completed/failed/blocked + passes boolean | 2 |
| Structure dependances | Objet imbrique {depends_on, blocks} | 2 |
| Champs obligatoires | Tous | 2 |
| Relation status/passes | passes=true → status=completed | 3 |
| Format IDs | Locaux (AC1, T1) | 3 |
| Champs additionnels | complexity + type | 3 |

---

## Schema Final Valide

```json
{
  "userStories": [{
    "id": "US-001",
    "title": "...",
    "category": "backend",
    "type": "Logic",
    "complexity": "M",
    "priority": 1,
    "status": "pending",
    "passes": false,
    "acceptanceCriteria": [
      {"id": "AC1", "description": "...", "done": false}
    ],
    "tasks": [
      {"id": "T1", "description": "...", "done": false}
    ],
    "dependencies": {
      "depends_on": [],
      "blocks": ["US-002"]
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
      "parent_spec": "S01-core.md",
      "parent_brief": "...",
      "estimated_minutes": 60
    }
  }]
}
```

---

*Journal genere automatiquement par Brainstormer v5.0*
