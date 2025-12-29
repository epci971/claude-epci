# Format du Brief Fonctionnel

## Overview

Template de sortie pour le brief genere par Brainstormer.
Compatible avec le workflow EPCI.

## Template Brief

```markdown
# Brief Fonctionnel — [Titre de la Feature]

> **Genere par**: Brainstormer v3.0
> **Template**: [feature/problem/decision]
> **EMS Final**: XX/100
> **Date**: YYYY-MM-DD
> **Slug**: [feature-slug]

---

## Contexte

[Pourquoi cette feature ? Quel probleme resout-elle ?
2-3 paragraphes maximum expliquant le besoin metier.]

## Objectif

[Description claire et concise de ce qu'on veut accomplir.
Une phrase principale, eventuellement 2-3 points de precision.]

## Stack Detecte

- **Framework**: [Symfony 7.x / React 18 / ...]
- **Language**: [PHP 8.3 / TypeScript / ...]
- **Patterns**: [Repository, Service, Controller, ...]
- **Outils**: [Doctrine, API Platform, Mercure, ...]

## Specifications Fonctionnelles

### SF1 — [Nom du bloc fonctionnel]

[Description du bloc]

- [Spec detaillee 1]
- [Spec detaillee 2]
- [Spec detaillee 3]

**Contraintes**: [Si applicable]

### SF2 — [Nom du bloc fonctionnel]

[Description du bloc]

- [Spec detaillee]
- [Spec detaillee]

### SF3 — [Nom du bloc fonctionnel]

...

## Regles Metier

- **RM1**: [Regle metier 1]
- **RM2**: [Regle metier 2]
- **RM3**: [Regle metier 3]

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| [Cas limite 1] | [Comportement] |
| [Cas limite 2] | [Comportement] |
| [Cas limite 3] | [Comportement] |

## Hors Scope (v1)

- [Exclusion explicite 1]
- [Exclusion explicite 2]
- [Exclusion explicite 3]

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| [Contrainte 1] | [Impact] | [Solution] |
| [Contrainte 2] | [Impact] | [Solution] |

## Dependances

- **Internes**: [Modules/services du projet impactes]
- **Externes**: [Libs, APIs, services tiers]

## Criteres d'Acceptation

- [ ] [Critere mesurable 1]
- [ ] [Critere mesurable 2]
- [ ] [Critere mesurable 3]
- [ ] [Critere mesurable 4]

## Questions Ouvertes

> Ces points n'ont pas ete resolus pendant l'exploration
> et devront etre adresses pendant la phase Plan.

- [ ] [Question non resolue 1]
- [ ] [Question non resolue 2]

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | [SMALL / STANDARD / LARGE] |
| Fichiers impactes | ~X |
| Risque | [Low / Medium / High] |

---

## Risques (Pre-mortem)

[Section optionnelle — si pre-mortem effectue]

| Risque | Score | Mitigation |
|--------|-------|------------|
| [Risque 1] | 9 | [Action preventive] |
| [Risque 2] | 6 | [Action preventive] |

---

## EMS Final

Score: XX/100 [emoji]

| Axe | Score |
|-----|-------|
| Clarte | XX/100 |
| Profondeur | XX/100 |
| Couverture | XX/100 |
| Decisions | XX/100 |
| Actionnabilite | XX/100 |

---

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Iterations | X |
| EMS Final | XX/100 |
| Template | [feature/problem/decision] |
| Frameworks utilises | [MoSCoW, Pre-mortem, ...] |
| Duree exploration | ~Xmin |

---

*Brief pret pour EPCI — Commande suggeree: `/epci-brief` ou `/epci`*
```

## Template Journal d'Exploration

```markdown
# Journal d'Exploration — [Titre]

> **Feature**: [Titre]
> **Date**: YYYY-MM-DD
> **Iterations**: X

---

## Resume

[2-3 phrases resumant l'exploration]

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 22 | - | Cadrage initial |
| 1 | 38 | +16 | [Focus] |
| 2 | 55 | +17 | [Focus] |
| 3 | 72 | +17 | [Focus] |
| Final | 78 | +6 | Finalisation |

## Decisions Cles

### Decision 1 — [Sujet]
- **Contexte**: [Pourquoi cette decision]
- **Options considerees**: [A, B, C]
- **Choix**: [Option retenue]
- **Justification**: [Raison]

### Decision 2 — [Sujet]
...

## Pivots

[Si des pivots ont eu lieu]

### Pivot 1 — Iteration X
- **Avant**: [Direction initiale]
- **Apres**: [Nouvelle direction]
- **Raison**: [Pourquoi le changement]

## Deep Dives

[Si des deep dives ont ete faits]

### Deep Dive — [Topic]
- **Iteration**: X
- **Resume**: [Ce qui a ete explore]
- **Conclusion**: [Ce qui en ressort]

## Frameworks Appliques

### [Framework] — Iteration X
[Resultat de l'application du framework]

## Questions Resolues

| Question | Reponse | Iteration |
|----------|---------|-----------|
| [Q1] | [R1] | X |
| [Q2] | [R2] | X |

## Biais Detectes

[Si des biais ont ete detectes et corriges]

- **[Biais]**: [Comment il s'est manifeste] -> [Comment corrige]

---

*Journal genere automatiquement par Brainstormer*
```

## Regles de Generation

1. **Slug**: kebab-case, derive du titre (ex: `systeme-notifications-temps-reel`)
2. **Date**: Format ISO (YYYY-MM-DD)
3. **Sections vides**: Omettre si rien a mettre (pas de "N/A")
4. **Longueur**: Brief = 1-3 pages, Journal = selon iterations
5. **Emplacement**: `./docs/briefs/`
