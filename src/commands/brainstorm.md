---
description: >-
  Brainstorming guide pour decouvrir et specifier une feature.
  Explore le codebase, pose des questions iteratives, genere un brief EPCI-ready.
  Use when: idee vague a transformer en specs, besoin de clarifier une feature.
argument-hint: [description de la feature souhaitee]
allowed-tools: [Read, Write, Bash, Glob, Grep, Task]
---

# /brainstorm — Feature Discovery

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase et des questions iteratives pour construire
des specifications exhaustives.

## Usage

```
/brainstorm [description de la feature souhaitee]
```

## Exemples

```
/brainstorm systeme de notifications en temps reel
/brainstorm refonte du module d'authentification
/brainstorm dashboard analytics pour les admins
```

## Configuration

| Element | Valeur |
|---------|--------|
| **Thinking** | `think hard` (adaptatif selon complexite) |
| **Skills** | `brainstormer`, `project-memory-loader`, `architecture-patterns` |
| **Subagents** | `@Explore` (analyse codebase) |

## Process

### Phase 1 — Initialisation

1. **Charger le contexte projet**
   - Skill: `project-memory-loader`
   - Si `.project-memory/` existe → charger
   - Sinon → continuer sans contexte

2. **Analyser le codebase**
   - Invoquer `@Explore` avec Task tool
   - Scan complet : structure, stack, patterns, fichiers pertinents
   - Stocker les resultats pour le questionnement

3. **Reformuler le besoin**
   - Paraphraser la demande utilisateur
   - Identifier les ambiguites initiales

4. **Questions de cadrage** (3-5 max)
   - Basees sur l'analyse codebase
   - Suggestions incluses quand pertinent

5. **Afficher breakpoint compact**

### Phase 2 — Iterations

Boucle jusqu'a `finish` :

1. **Integrer les reponses** utilisateur
2. **Mettre a jour EMS** (score sur 100)
3. **Appliquer frameworks** si pertinent (MoSCoW, 5 Whys, etc.)
4. **Generer questions/suggestions** suivantes
5. **Afficher breakpoint compact**

**Commandes disponibles :**

| Commande | Action |
|----------|--------|
| `continue` | Iteration suivante avec nouvelles questions |
| `dive [topic]` | Approfondir un aspect specifique |
| `pivot` | Reorienter si le vrai besoin emerge |
| `status` | Afficher EMS detaille (5 axes) |
| `finish` | Generer brief + journal |

### Phase 3 — Generation

1. **Generer le brief fonctionnel**
   - Format: voir `references/brief-format.md`
   - Fichier: `./docs/briefs/brief-[slug]-[date].md`

2. **Generer le journal d'exploration**
   - Historique des iterations
   - Decisions prises
   - Questions resolues
   - Fichier: `./docs/briefs/journal-[slug]-[date].md`

3. **Afficher resume**
   - EMS final
   - Liens vers les fichiers
   - Suggestion de commande EPCI suivante

## Format Breakpoint (compact pour CLI)

```
-------------------------------------------------------
Iteration X | EMS: XX/100 (+Y) [progress bar] [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

Questions:
1. [Question 1] -> Suggestion: [si applicable]
2. [Question 2]
3. [Question 3]

-> continue | dive [topic] | pivot | status | finish
-------------------------------------------------------
```

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/journal-[slug]-[date].md` | Journal d'exploration |

## Integration EPCI

Le brief genere peut etre utilise :
- Directement avec `/epci-brief` (copier le contenu)
- Comme reference pour `/epci` ou `/epci-quick`
- Comme documentation de la phase de decouverte

## Skills Charges

- `brainstormer` — Logique metier principale
- `project-memory-loader` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
