# Format du Brief Fonctionnel

## Overview

Template de sortie pour le brief genere par Brainstormer.
Compatible avec le workflow EPCI. Format hybride PRD-FRD optimise pour le handoff developpeur.

**Version**: 2.0 (Janvier 2025)

## Template Brief

```markdown
# Brief Fonctionnel — [Titre de la Feature]

> **Brainstormer**: v4.8 | **EMS**: XX/100 | **Template**: [feature/problem/decision]
> **Date**: YYYY-MM-DD | **Slug**: [feature-slug]

---

## Contexte

[Pourquoi cette feature ? Quel probleme resout-elle ?
2-3 paragraphes maximum expliquant le besoin metier.]

## Objectif

[Description claire et concise de ce qu'on veut accomplir.
Une phrase principale, eventuellement 2-3 points de precision.]

## Personas

### Persona Primaire — [Nom/Role]

- **Role**: [ex: Developpeur frontend, PM startup, Admin systeme]
- **Contexte**: [environnement de travail, outils utilises, frequence d'utilisation]
- **Pain points**: [frustrations actuelles, problemes rencontres]
- **Objectifs**: [ce qu'il cherche a accomplir avec cette feature]
- **Quote**: "[Citation representative du besoin]"

### Persona Secondaire — [Nom/Role] (si applicable)

- **Role**: [role secondaire impacte]
- **Contexte**: [son environnement]
- **Pain points**: [ses frustrations]
- **Objectifs**: [ses objectifs]

> Note: Personas issus de l'exploration Brainstormer ou a valider avec stakeholders.

## Stack Detecte

- **Framework**: [Symfony 7.x / React 18 / ...]
- **Language**: [PHP 8.3 / TypeScript / ...]
- **Patterns**: [Repository, Service, Controller, ...]
- **Outils**: [Doctrine, API Platform, Mercure, ...]

## Exploration Summary

> Cette section documente l'analyse initiale du codebase effectuee pendant le brainstorm.
> Elle sert de reference pour `/brief` qui effectuera une exploration ciblee.

### Codebase Analysis

- **Structure**: [monorepo / multi-module / single-app]
- **Architecture**: [MVC / Hexagonal / Clean / etc.]
- **Test patterns**: [PHPUnit / Jest / Pytest / etc.]

### Fichiers Potentiels

| Fichier | Action probable | Notes |
|---------|-----------------|-------|
| `path/to/file1.ext` | Create | [Description] |
| `path/to/file2.ext` | Modify | [Description] |

> Note: Liste indicative. L'exploration de `/brief` affinera ces fichiers.

### Risques Identifies

- [Risque 1 avec niveau: Low/Medium/High]
- [Risque 2 avec niveau]

## User Stories

### US1 — [Titre action]

**En tant que** [persona primaire],
**Je veux** [action/fonctionnalite],
**Afin de** [benefice/valeur].

**Acceptance Criteria:**
- [ ] Given [contexte initial], When [action utilisateur], Then [resultat attendu]
- [ ] Given [autre contexte], When [action], Then [resultat]
- [ ] Given [cas erreur], When [action invalide], Then [message erreur]

**Priorite**: Must-have
**Complexite**: [S | M | L]

### US2 — [Titre action]

**En tant que** [persona],
**Je veux** [action],
**Afin de** [benefice].

**Acceptance Criteria:**
- [ ] Given [contexte], When [action], Then [resultat]

**Priorite**: Should-have
**Complexite**: [S | M | L]

### US3 — [Titre action]

**En tant que** [persona],
**Je veux** [action],
**Afin de** [benefice].

**Acceptance Criteria:**
- [ ] Given [contexte], When [action], Then [resultat]

**Priorite**: Could-have
**Complexite**: [S | M | L]

> Note: Priorite MoSCoW. Must-have = MVP obligatoire. Could-have = nice-to-have v2+.

## Regles Metier

- **RM1**: [Regle metier 1 — condition et consequence]
- **RM2**: [Regle metier 2]
- **RM3**: [Regle metier 3]

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| [Cas limite 1] | [Comportement] |
| [Cas limite 2] | [Comportement] |
| [Cas limite 3] | [Comportement] |

## Hors Scope (v1)

- [Exclusion explicite 1 — raison]
- [Exclusion explicite 2 — raison]
- [Exclusion explicite 3 — raison]

## Success Metrics

| Metrique | Baseline | Cible | Methode de mesure |
|----------|----------|-------|-------------------|
| [KPI 1 - ex: Temps de completion] | [valeur actuelle ou N/A] | [objectif] | [Analytics / Logs / User testing] |
| [KPI 2 - ex: Taux d'erreur] | [valeur actuelle] | [objectif] | [Monitoring] |
| [KPI 3 - ex: Satisfaction] | [valeur actuelle] | [objectif] | [Survey / NPS] |

> Note: Metriques a definir avec Product Owner. Si inconnues, marquer "TBD".

## User Flow (optionnel)

```
[Point d'entree]
       |
       v
  [Etape 1] --> [Decision?]
                    |
           [Oui]---+---[Non]
             |           |
             v           v
        [Etape 2]   [Alternative]
             |           |
             v           v
        [Succes]    [Erreur/Retry]
```

> Ou lien vers: Figma / Miro / Excalidraw

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| [Contrainte 1] | [Impact] | [Solution proposee] |
| [Contrainte 2] | [Impact] | [Solution proposee] |

## Dependances

- **Internes**: [Modules/services du projet impactes]
- **Externes**: [Libs, APIs, services tiers]

## Criteres d'Acceptation Globaux

> Criteres techniques de validation (au-dela des AC par User Story)

- [ ] [Critere performance - ex: Page load < 2s]
- [ ] [Critere securite - ex: Inputs sanitizes]
- [ ] [Critere accessibilite - ex: WCAG 2.1 AA]
- [ ] [Critere tests - ex: Coverage > 80%]

## Questions Ouvertes

> Ces points n'ont pas ete resolus pendant l'exploration
> et devront etre adresses pendant la phase Plan.

- [ ] [Question non resolue 1]
- [ ] [Question non resolue 2]

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | [TINY / SMALL / STANDARD / LARGE] |
| Fichiers impactes | ~X |
| Risque global | [Low / Medium / High] |

---

## Risques (Pre-mortem)

[Section optionnelle — si pre-mortem effectue]

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | [H/M/L] | [H/M/L] | [Action preventive] |
| [Risque 2] | [H/M/L] | [H/M/L] | [Action preventive] |

---

*Brief pret pour EPCI — Lancer `/brief` avec ce contenu.*
*Details du processus de brainstorming dans le Journal d'Exploration.*
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

## EMS Final Detaille

| Axe | Score |
|-----|-------|
| Clarte | XX/100 |
| Profondeur | XX/100 |
| Couverture | XX/100 |
| Decisions | XX/100 |
| Actionnabilite | XX/100 |

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Version | v4.8 |
| Template | [feature/problem/decision] |
| Techniques appliquees | [MoSCoW, Pre-mortem, SCAMPER, ...] |
| Duree exploration | ~Xmin |

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
4. **Longueur**: Brief = 2-4 pages, Journal = selon iterations
5. **Emplacement**: `./docs/briefs/`
6. **Personas**: Minimum 1 persona primaire obligatoire
7. **User Stories**: Minimum 1 Must-have US obligatoire
8. **Priorite MoSCoW**: Must-have > Should-have > Could-have > Won't-have
9. **Acceptance Criteria**: Format Given/When/Then obligatoire
10. **Success Metrics**: Au moins 1 KPI si connu, sinon "TBD"

## Changements v2.0

| Section | Changement | Raison |
|---------|------------|--------|
| Personas | AJOUT | Ancrer les decisions dans l'utilisateur |
| User Stories | REMPLACE SF | Format standard industrie |
| Success Metrics | AJOUT | Metriques business mesurables |
| User Flow | AJOUT (opt) | Visualisation parcours |
| Metadonnees | SIMPLIFIE | Deplace vers Journal |
| EMS detaille | DEPLACE | Vers Journal |
