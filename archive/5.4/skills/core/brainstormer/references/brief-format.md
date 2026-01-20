# Format du Brief Fonctionnel

## Overview

Template de sortie pour le brief genere par Brainstormer.
Compatible avec le workflow EPCI. Format hybride PRD-FRD optimise pour le handoff developpeur.

**Version**: 3.0 (Janvier 2026) — PRD Industry Standards Compliant

## Template Brief

```markdown
# PRD — [Titre de la Feature]

| Metadata | Value |
|----------|-------|
| **Document ID** | PRD-[YYYY]-[XXX] |
| **Version** | 1.0 |
| **Status** | Draft |
| **Owner** | TBD |
| **Created** | [YYYY-MM-DD] |
| **Last Updated** | [YYYY-MM-DD] |
| **Slug** | [feature-slug] |
| **EMS Score** | [XX/100] |
| **Template** | [feature/problem/decision] |

### Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | EPCI Brainstormer | Initial generation from /brainstorm |

---

## Executive Summary

**TL;DR** : [1 phrase resumant la feature]

| Aspect | Description |
|--------|-------------|
| **Problem** | [1 phrase decrivant le probleme] |
| **Solution** | [1 phrase decrivant la solution] |
| **Impact** | [Metrique cle attendue] |
| **Target Launch** | [TBD] |

---

## Background & Strategic Fit

### Why Now?
[Contexte business : opportunite marche, pression concurrentielle, demande utilisateur]

### Strategic Alignment
Cette feature s'aligne avec :
- [ ] **OKR** : [Objectif specifique si connu, sinon TBD]
- [ ] **Vision Produit** : [Comment ca s'integre]
- [ ] **Position Marche** : [Avantage concurrentiel]

---

## Competitive Analysis (Optional)

> Section generee si flag `--competitive` ou si pertinent pour le contexte.

| Feature | Nous (Actuel) | Concurrent A | Concurrent B | Leader Marche |
|---------|---------------|--------------|--------------|---------------|
| [Feature 1] | ❌ Non | ✅ Oui | ✅ Oui | ✅ Oui |
| [Feature 2] | ⚠️ Partiel | ✅ Oui | ❌ Non | ✅ Oui |
| [Feature 3] | ✅ Oui | ✅ Oui | ✅ Oui | ✅ Oui |

### Key Insights
- **Gap** : [Ce qui nous manque par rapport aux concurrents]
- **Opportunite** : [Ce qu'on peut faire mieux]
- **Differentiation** : [Notre avantage unique]

---

## Problem Statement

### Current Situation
[Description de la situation actuelle — comment les choses fonctionnent aujourd'hui]

### Problem Definition
[Probleme specifique et mesurable que cette feature resout]

### Evidence & Data
- **Quantitative** : [Metriques existantes, sinon "A collecter"]
- **Qualitative** : [Feedback utilisateur, support tickets, interviews]

### Impact of Not Solving
- **Business** : [Impact revenue/churn/acquisition]
- **User** : [Impact satisfaction/productivite]
- **Technical** : [Impact dette technique/maintenance]

---

## Goals

### Business Goals
- [ ] [Goal avec metrique — ex: Increase retention by 15%]

### User Goals
- [ ] [Enable users to... — ex: Complete task in <2 clicks]

### Technical Goals
- [ ] [Performance/scalability — ex: Page load <2s, 99.9% uptime]

---

## Non-Goals (Out of Scope v1)

**Explicitement NON inclus dans cette version** :

| Exclusion | Raison | Future Version |
|-----------|--------|----------------|
| [Feature X] | Complexite technique | v2 |
| [Feature Y] | Hors perimetre metier | Non prevu |
| [Feature Z] | Dependance externe | v2 si API disponible |

> Ces elements pourront etre consideres dans les iterations futures.

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

## Success Metrics

| Metrique | Baseline | Cible | Methode de mesure |
|----------|----------|-------|-------------------|
| [KPI 1 - ex: Temps de completion] | [valeur actuelle ou N/A] | [objectif] | [Analytics / Logs / User testing] |
| [KPI 2 - ex: Taux d'erreur] | [valeur actuelle] | [objectif] | [Monitoring] |
| [KPI 3 - ex: Satisfaction] | [valeur actuelle] | [objectif] | [Survey / NPS] |

> Note: Metriques a definir avec Product Owner. Si inconnues, marquer "TBD".

## User Flow

### Current Experience (As-Is)

```
[Point d'entree actuel]
       |
       v
  [Etape 1 - Pain point] --> [Friction?]
                                  |
                         [Oui]---+---[Non]
                           |           |
                           v           v
                      [Abandon]   [Completion lente]
```

> Pain points identifies : [lister les frustrations actuelles]

### Proposed Experience (To-Be)

```
[Point d'entree optimise]
       |
       v
  [Etape 1 simplifie] --> [Decision?]
                               |
                      [Oui]---+---[Non]
                        |           |
                        v           v
                   [Etape 2]   [Alternative]
                        |           |
                        v           v
                   [Succes]    [Erreur/Retry]
```

### Key Improvements

| Pain Point Actuel | Solution Proposee | Impact |
|-------------------|-------------------|--------|
| [Pain point 1] | [Amelioration 1] | [Metrique] |
| [Pain point 2] | [Amelioration 2] | [Metrique] |

> Ou lien vers: Figma / Miro / Excalidraw

## Contraintes Techniques Identifiees

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| [Contrainte 1] | [Impact] | [Solution proposee] |
| [Contrainte 2] | [Impact] | [Solution proposee] |

## Dependances

- **Internes**: [Modules/services du projet impactes]
- **Externes**: [Libs, APIs, services tiers]

## Assumptions

Hypotheses considerees vraies pour le succes de cette feature :

- [ ] **Technical** : [Ex: API latency < 200ms, service X disponible]
- [ ] **Business** : [Ex: Budget approuve, stakeholder buy-in]
- [ ] **User** : [Ex: Utilisateurs tech-savvy, mobile-first]
- [ ] **Resources** : [Ex: Equipe design disponible Q1, dev senior alloue]

> **Plan de validation** : [Comment valider les assumptions critiques avant/pendant dev]

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

## FAQ

### Internal FAQ (Equipe)

**Q: Pourquoi ne pas utiliser [Alternative X] ?**
A: [Raisonnement technique ou business]

**Q: Et si [Edge Case Y] se produit ?**
A: [Gestion prevue ou comportement attendu]

**Q: Quel est l'impact sur [Systeme existant] ?**
A: [Evaluation d'impact et strategie de migration]

### External FAQ (Utilisateurs)

**Q: Comment cela affecte les utilisateurs existants ?**
A: [Explication d'impact et communication prevue]

**Q: Quand cette feature sera-t-elle disponible ?**
A: [Timeline ou "TBD - voir section Timeline"]

## Estimation Preliminaire

| Metrique | Valeur |
|----------|--------|
| Complexite estimee | [TINY / SMALL / STANDARD / LARGE] |
| Fichiers impactes | ~X |
| Risque global | [Low / Medium / High] |

---

## Timeline & Milestones

### Target Launch
**Objectif** : [TBD — A definir avec PM/PO]

### Key Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| PRD Review Complete | TBD | PM | ⚪ Not Started |
| Technical Spec Complete | TBD | Tech Lead | ⚪ Not Started |
| Development Start | TBD | Dev Team | ⚪ Not Started |
| Alpha Release (Internal) | TBD | Dev Team | ⚪ Not Started |
| Beta Release (Select Users) | TBD | PM + Dev | ⚪ Not Started |
| General Availability | TBD | All | ⚪ Not Started |

### Phasing Strategy (si applicable)

**Phase 1 (MVP)** : [Core features — Must-have User Stories]
**Phase 2** : [Should-have features]
**Phase 3** : [Could-have features]

> Note: Dates a definir avec Product Owner. Compatible avec planning sprint.

---

## Risques (Pre-mortem)

[Section optionnelle — si pre-mortem effectue]

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | [H/M/L] | [H/M/L] | [Action preventive] |
| [Risque 2] | [H/M/L] | [H/M/L] | [Action preventive] |

---

## Appendix (Optional)

### Research Findings

> Resultats d'interviews utilisateurs, surveys, analytics si disponibles

- [Finding 1 — Source]
- [Finding 2 — Source]

### Technical Deep Dives

> Liens vers analyses techniques detaillees si necessaire

- [Deep Dive 1 — Link/Reference]
- [Deep Dive 2 — Link/Reference]

### Glossary

| Terme | Definition |
|-------|------------|
| [Terme metier 1] | [Explication] |
| [Acronyme 1] | [Signification complete] |
| [Concept technique] | [Definition accessible] |

---

*PRD pret pour EPCI — Lancer `/brief` avec ce contenu.*
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

**⚠️ OBLIGATOIRE** : Cette section doit TOUJOURS être présente dans le journal.
Tracker l'évolution EMS à chaque itération.

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 22 | - | Cadrage initial |
| 1 | 38 | +16 | [Axe amélioré] |
| 2 | 55 | +17 | [Axe amélioré] |
| 3 | 72 | +17 | [Axe amélioré] |
| Final | 78 | +6 | Finalisation |

## EMS Final Détaillé

**⚠️ OBLIGATOIRE** : Utiliser EXACTEMENT ces 5 axes standards (pas d'invention).

| Axe | Score | Poids |
|-----|-------|-------|
| Clarté | XX/100 | 25% |
| Profondeur | XX/100 | 20% |
| Couverture | XX/100 | 20% |
| Décisions | XX/100 | 20% |
| Actionnabilité | XX/100 | 15% |

**❌ NE PAS** utiliser d'autres noms d'axes comme :
- "Faisabilité technique" → utiliser "Actionnabilité"
- "Solution proposée" → utiliser "Décisions"
- "Documentation" → utiliser "Clarté"

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

1. **Document ID**: Format PRD-[YYYY]-[XXX] auto-genere
2. **Slug**: kebab-case, derive du titre (ex: `systeme-notifications-temps-reel`)
3. **Date**: Format ISO (YYYY-MM-DD)
4. **Sections vides**: Omettre si rien a mettre (pas de "N/A")
5. **Sections optionnelles**: Competitive Analysis, Appendix — omettre si non pertinent
6. **Longueur**: Brief = 3-5 pages, Journal = selon iterations
7. **Emplacement**: `./docs/briefs/`
8. **Personas**: Minimum 1 persona primaire obligatoire
9. **User Stories**: Minimum 1 Must-have US obligatoire
10. **Priorite MoSCoW**: Must-have > Should-have > Could-have > Won't-have
11. **Acceptance Criteria**: Format Given/When/Then obligatoire
12. **Success Metrics**: Au moins 1 KPI si connu, sinon "TBD"
13. **Timeline**: Dates TBD par defaut — a definir par PM/PO
14. **FAQ**: Generer au moins 2 questions internal + 1 external

## Changements v3.0 (PRD Industry Standards)

| Section | Changement | Raison |
|---------|------------|--------|
| Document Header | ENRICHI | Document ID, Version, Status, Change History (traçabilite) |
| Executive Summary | AJOUT | Vue d'ensemble rapide pour stakeholders (TL;DR) |
| Background & Strategic Fit | AJOUT | Alignement strategique et "Why Now?" |
| Competitive Analysis | AJOUT (opt) | Analyse concurrentielle (flag --competitive) |
| Contexte | RENOMME | Problem Statement data-driven avec Evidence |
| Objectif | SPLIT | Goals (Business/User/Tech) + Non-Goals |
| Hors Scope | FUSIONNE | Absorbe dans Non-Goals avec tableau |
| User Flow | ENRICHI | As-Is vs To-Be avec Key Improvements |
| Assumptions | AJOUT | Hypotheses explicites avec plan de validation |
| FAQ | AJOUT | Internal + External (Amazon-style) |
| Timeline & Milestones | AJOUT | Planification avec Phasing Strategy |
| Appendix | AJOUT (opt) | Research, Deep Dives, Glossary |

## Changements v2.0

| Section | Changement | Raison |
|---------|------------|--------|
| Personas | AJOUT | Ancrer les decisions dans l'utilisateur |
| User Stories | REMPLACE SF | Format standard industrie |
| Success Metrics | AJOUT | Metriques business mesurables |
| User Flow | AJOUT (opt) | Visualisation parcours |
| Metadonnees | SIMPLIFIE | Deplace vers Journal |
| EMS detaille | DEPLACE | Vers Journal |
