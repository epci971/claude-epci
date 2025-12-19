---
name: brainstormer
description: >-
  Feature discovery et brainstorming guide pour EPCI. Workflow 3 phases
  (Init, Iterate, Finish) avec scoring EMS et frameworks d'analyse.
  Use when: /brainstorm invoked, feature discovery needed.
  Not for: implementation tasks, code generation, simple questions.
allowed-tools: [Read, Write, Glob, Grep]
---

# Brainstormer

## Overview

Skill de brainstorming specialise pour la decouverte de features.
Transforme des idees vagues en briefs fonctionnels complets via
un processus iteratif guide.

**Reference Documents:**
- [EMS System](references/ems-system.md) — Scoring et progression
- [Frameworks](references/frameworks.md) — Outils d'analyse
- [Brief Format](references/brief-format.md) — Template de sortie

## Workflow 3 Phases

### Phase 1 — Initialisation

**Objectif**: Etablir le contexte et commencer l'exploration.

**Actions:**
1. Charger le contexte projet via `project-memory-loader`
2. Invoquer `@Explore` pour analyser le codebase :
   - Structure du projet
   - Stack technique (detection automatique)
   - Patterns architecturaux
   - Fichiers potentiellement impactes
3. Reformuler le besoin utilisateur
4. Identifier les premieres ambiguites
5. Generer 3-5 questions de cadrage
6. Initialiser EMS a ~20-25/100

**Output**: Premier breakpoint avec questions de cadrage.

### Phase 2 — Iterations

**Objectif**: Approfondir et affiner jusqu'a maturite.

**Boucle:**
1. Integrer les reponses utilisateur
2. Mettre a jour les 5 axes EMS
3. Detecter si un framework est applicable
4. Generer questions suivantes (3-5 max)
5. Afficher breakpoint compact

**Commandes:**

| Commande | Comportement |
|----------|--------------|
| `continue` | Integrer reponses, nouvelles questions |
| `dive [topic]` | Focus profond sur un aspect, questions ciblees |
| `pivot` | Reorienter l'exploration, reset partiel EMS |
| `status` | Afficher EMS detaille (5 axes avec radar) |
| `finish` | Passer en Phase 3 |

**Criteres de suggestion `finish`:**
- EMS >= 70/100
- Axe Clarte >= 80/100
- Axe Actionnabilite >= 60/100

### Phase 3 — Generation

**Objectif**: Produire les livrables finaux.

**Actions:**
1. Compiler toutes les decisions en brief structure
2. Generer le journal d'exploration
3. Creer le dossier `./docs/briefs/` si inexistant
4. Ecrire les fichiers
5. Afficher resume avec liens

## Format Breakpoint Compact

Optimise pour CLI (evite le scroll) :

```
-------------------------------------------------------
Iteration X | EMS: XX/100 (+Y) [progress] [emoji]
-------------------------------------------------------
Done: [liste courte des elements valides]
Open: [liste courte des points a clarifier]

Questions:
1. [Question concise]
2. [Question concise]
3. [Question concise]

-> continue | dive [topic] | pivot | status | finish
-------------------------------------------------------
```

**Emojis EMS:**

| Score | Emoji | Label |
|-------|-------|-------|
| 0-30 | seed | Germination |
| 31-50 | seedling | Developpement |
| 51-70 | tree | Mature |
| 71-85 | target | Tres Complete |
| 86-100 | trophy | Exceptionnelle |

## Detection de Frameworks

Appliquer automatiquement selon le contexte :

| Signal | Framework | Usage |
|--------|-----------|-------|
| Priorisation demandee | MoSCoW | Categoriser Must/Should/Could/Won't |
| "Pourquoi" repete | 5 Whys | Creuser la cause racine |
| Plusieurs options | SWOT | Analyser forces/faiblesses |
| Criteres multiples | Scoring | Matrice de decision |

## Gestion du Contexte Codebase

L'analyse `@Explore` initiale fournit :

| Element | Utilisation |
|---------|-------------|
| Stack detecte | Adapter les suggestions techniques |
| Patterns existants | Proposer la coherence architecturale |
| Fichiers impactes | Estimer la complexite |
| Conventions | Respecter le style du projet |

**Integrer ces elements dans les questions et suggestions.**

## Detection de Biais

Surveiller et alerter si detecte :

| Biais | Signal | Action |
|-------|--------|--------|
| Confirmation | Ignore les alternatives | Proposer des contre-exemples |
| Ancrage | Fixe sur premiere idee | Suggerer un pivot |
| Scope Creep | Expansion continue | Rappeler le focus initial |
| Complexite | Sur-ingenierie | Suggerer MVP |

## Reponses Utilisateur

Accepter les deux formats :

**Texte libre (prioritaire):**
```
Redis pour le cache, on garde l'approche centralisee pour les erreurs,
et oui on peut passer aux endpoints.
```

**Par numero:**
```
1: Redis, 2: centralisee, 3: oui
```

## Anti-patterns

**Ne pas faire:**
- Poser plus de 5 questions par iteration
- Generer un breakpoint de plus de 15 lignes
- Ignorer le contexte codebase dans les suggestions
- Forcer un framework non pertinent
- Suggerer `finish` avant EMS 60/100

**Toujours faire:**
- Baser les questions sur l'analyse codebase
- Proposer des suggestions avec les questions
- Mettre a jour EMS a chaque iteration
- Respecter le format compact CLI
- Inclure les elements decides/ouverts
