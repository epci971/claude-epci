# Cahier des Charges — Brainstormer pour EPCI

> **Version**: 1.0
> **Date**: 2025-01-XX
> **Statut**: Prêt pour implémentation
> **Cible**: Plugin EPCI v3.0+

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture](#2-architecture)
3. [Commande /brainstorm](#3-commande-brainstorm)
4. [Skill brainstormer](#4-skill-brainstormer)
5. [Références du skill](#5-références-du-skill)
6. [Intégration EPCI](#6-intégration-epci)
7. [Validation et tests](#7-validation-et-tests)

---

## 1. Vue d'ensemble

### 1.1 Objectif

Brainstormer est un outil de **découverte de feature** qui transforme une idée vague en un **brief fonctionnel complet**, prêt à être consommé par le workflow EPCI.

### 1.2 Position dans le workflow

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Idée       │         │ /brainstorm  │         │    Brief     │
│   vague      │ ──────▶ │  (explore,   │ ──────▶ │  Fonctionnel │
│   "Je veux..." │        │   itère)     │         │   Complet    │
└──────────────┘         └──────────────┘         └──────┬───────┘
                                                         │
                                                         ▼
                                                 ┌──────────────┐
                                                 │ /epci-brief  │
                                                 │  ou /epci    │
                                                 └──────────────┘
```

### 1.3 Caractéristiques clés

| Aspect | Décision |
|--------|----------|
| **Scope** | Spécialisé dev/features (pas généraliste) |
| **Contexte** | Analyse codebase automatique via @Explore |
| **Recherche web** | Claude natif (pas besoin de subagent) |
| **Itérations** | 3-5 questions par itération, texte libre ou numéroté |
| **Output** | Brief fonctionnel + Journal d'exploration |
| **Emplacement output** | `./docs/briefs/` |
| **EMS** | Barre compacte en CLI, détail sur demande (`status`) |

### 1.4 Composants à créer

| Type | Nom | Emplacement |
|------|-----|-------------|
| Command | `brainstorm` | `commands/brainstorm.md` |
| Skill | `brainstormer` | `skills/core/brainstormer/SKILL.md` |
| Reference | `ems-system` | `skills/core/brainstormer/references/ems-system.md` |
| Reference | `frameworks` | `skills/core/brainstormer/references/frameworks.md` |
| Reference | `brief-format` | `skills/core/brainstormer/references/brief-format.md` |

**Note**: Pas de subagent custom nécessaire. On utilise :
- `@Explore` (natif) pour l'analyse codebase
- Claude natif pour la recherche web si besoin

---

## 2. Architecture

### 2.1 Structure des fichiers à créer

```
epci/
├── commands/
│   └── brainstorm.md                    # 🆕 Point d'entrée
│
└── skills/
    └── core/
        └── brainstormer/                # 🆕 Skill complet
            ├── SKILL.md                 # Instructions principales
            └── references/
                ├── ems-system.md        # Système EMS (5 axes, scoring)
                ├── frameworks.md        # MoSCoW, 5 Whys, SWOT, Scoring
                └── brief-format.md      # Template du brief EPCI
```

### 2.2 Dépendances (skills existants à réutiliser)

| Composant | Usage |
|-----------|-------|
| `@Explore` (natif) | Analyse codebase initiale |
| `project-memory-loader` | Charger contexte projet |
| `architecture-patterns` | Suggestions architecture |
| `clarification-intelligente` | Système de questions intelligentes |

### 2.3 Flux de données

```
User: /brainstorm "système de notifications temps réel"
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1 — INITIALISATION                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. Charger project-memory (si disponible)                   │
│ 2. Invoquer @Explore (analyse codebase complète)            │
│ 3. Reformuler le besoin                                     │
│ 4. Poser questions de cadrage (3-5)                         │
│ 5. Afficher breakpoint compact                              │
└─────────────────────────────────────────────────────────────┘
         │
         ▼ (user répond)
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2 — ITÉRATIONS (répéter jusqu'à finish)               │
├─────────────────────────────────────────────────────────────┤
│ 1. Intégrer réponses                                        │
│ 2. Mettre à jour EMS                                        │
│ 3. Appliquer frameworks si pertinent                        │
│ 4. Générer nouvelles questions ou suggestions               │
│ 5. Afficher breakpoint compact                              │
│                                                              │
│ Commandes disponibles:                                       │
│ - continue → Itération suivante                             │
│ - dive [topic] → Approfondir un point                       │
│ - pivot → Réorienter l'exploration                          │
│ - status → Afficher EMS détaillé                            │
│ - finish → Générer les livrables                            │
└─────────────────────────────────────────────────────────────┘
         │
         ▼ (user: finish)
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3 — GÉNÉRATION                                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Générer brief fonctionnel complet                        │
│ 2. Générer journal d'exploration                            │
│ 3. Sauvegarder dans ./docs/briefs/                          │
│ 4. Afficher résumé et liens                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Commande /brainstorm

### 3.1 Spécifications

| Élément | Valeur |
|---------|--------|
| **Nom** | `brainstorm` |
| **Description** | Brainstorming guidé pour découvrir et spécifier une feature |
| **Argument** | `[sujet de la feature]` |
| **Tools** | `Read, Write, Bash, Glob, Grep, Task` |

### 3.2 Contenu COMPLET du fichier `commands/brainstorm.md`

```markdown
---
description: >-
  Brainstorming guidé pour découvrir et spécifier une feature.
  Explore le codebase, pose des questions itératives, génère un brief EPCI-ready.
  Use when: idée vague à transformer en specs, besoin de clarifier une feature.
argument-hint: [description de la feature souhaitée]
allowed-tools: [Read, Write, Bash, Glob, Grep, Task]
---

# /brainstorm — Feature Discovery

## Overview

Transforme une idée vague en brief fonctionnel complet, prêt pour EPCI.
Utilise l'analyse du codebase et des questions itératives pour construire
des spécifications exhaustives.

## Usage

```
/brainstorm [description de la feature souhaitée]
```

## Exemples

```
/brainstorm système de notifications en temps réel
/brainstorm refonte du module d'authentification
/brainstorm dashboard analytics pour les admins
```

## Configuration

| Élément | Valeur |
|---------|--------|
| **Thinking** | `think hard` (adaptatif selon complexité) |
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
   - Stocker les résultats pour le questionnement

3. **Reformuler le besoin**
   - Paraphraser la demande utilisateur
   - Identifier les ambiguïtés initiales

4. **Questions de cadrage** (3-5 max)
   - Basées sur l'analyse codebase
   - Suggestions incluses quand pertinent

5. **Afficher breakpoint compact**

### Phase 2 — Itérations

Boucle jusqu'à `finish` :

1. **Intégrer les réponses** utilisateur
2. **Mettre à jour EMS** (score sur 100)
3. **Appliquer frameworks** si pertinent (MoSCoW, 5 Whys, etc.)
4. **Générer questions/suggestions** suivantes
5. **Afficher breakpoint compact**

**Commandes disponibles :**

| Commande | Action |
|----------|--------|
| `continue` | Itération suivante avec nouvelles questions |
| `dive [topic]` | Approfondir un aspect spécifique |
| `pivot` | Réorienter si le vrai besoin émerge |
| `status` | Afficher EMS détaillé (5 axes) |
| `finish` | Générer brief + journal |

### Phase 3 — Génération

1. **Générer le brief fonctionnel**
   - Format: voir `references/brief-format.md`
   - Fichier: `./docs/briefs/brief-[slug]-[date].md`

2. **Générer le journal d'exploration**
   - Historique des itérations
   - Décisions prises
   - Questions résolues
   - Fichier: `./docs/briefs/journal-[slug]-[date].md`

3. **Afficher résumé**
   - EMS final
   - Liens vers les fichiers
   - Suggestion de commande EPCI suivante

## Format Breakpoint (compact pour CLI)

```
───────────────────────────────────────────────────────
📍 Iteration X | EMS: XX/100 (+Y) ████████░░░░ 🌿
───────────────────────────────────────────────────────
✓ Décidé: [éléments validés]
○ Ouvert: [éléments à clarifier]

❓ Questions:
1. [Question 1] → Suggestion: [si applicable]
2. [Question 2]
3. [Question 3]

→ continue | dive [topic] | pivot | status | finish
───────────────────────────────────────────────────────
```

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/journal-[slug]-[date].md` | Journal d'exploration |

## Integration EPCI

Le brief généré peut être utilisé :
- Directement avec `/epci-brief` (copier le contenu)
- Comme référence pour `/epci` ou `/epci-quick`
- Comme documentation de la phase de découverte

## Skills Chargés

- `brainstormer` — Logique métier principale
- `project-memory-loader` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Système de questions
```

---

## 4. Skill brainstormer

### 4.1 Spécifications

| Élément | Valeur |
|---------|--------|
| **Nom** | `brainstormer` |
| **Catégorie** | `core` |
| **Tokens estimés** | ~3500 (SKILL.md) + références |
| **Tools** | `Read, Write, Glob, Grep` |

### 4.2 Contenu COMPLET du fichier `skills/core/brainstormer/SKILL.md`

```markdown
---
name: brainstormer
description: >-
  Feature discovery et brainstorming guidé pour EPCI. Workflow 3 phases
  (Init, Iterate, Finish) avec scoring EMS et frameworks d'analyse.
  Use when: /brainstorm invoked, feature discovery needed.
  Not for: implementation tasks, code generation, simple questions.
allowed-tools: [Read, Write, Glob, Grep]
---

# Brainstormer

## Overview

Skill de brainstorming spécialisé pour la découverte de features.
Transforme des idées vagues en briefs fonctionnels complets via
un processus itératif guidé.

**Reference Documents:**
- [EMS System](references/ems-system.md) — Scoring et progression
- [Frameworks](references/frameworks.md) — Outils d'analyse
- [Brief Format](references/brief-format.md) — Template de sortie

## Workflow 3 Phases

### Phase 1 — Initialisation

**Objectif**: Établir le contexte et commencer l'exploration.

**Actions:**
1. Charger le contexte projet via `project-memory-loader`
2. Invoquer `@Explore` pour analyser le codebase :
   - Structure du projet
   - Stack technique (détection automatique)
   - Patterns architecturaux
   - Fichiers potentiellement impactés
3. Reformuler le besoin utilisateur
4. Identifier les premières ambiguïtés
5. Générer 3-5 questions de cadrage
6. Initialiser EMS à ~20-25/100

**Output**: Premier breakpoint avec questions de cadrage.

### Phase 2 — Itérations

**Objectif**: Approfondir et affiner jusqu'à maturité.

**Boucle:**
1. Intégrer les réponses utilisateur
2. Mettre à jour les 5 axes EMS
3. Détecter si un framework est applicable
4. Générer questions suivantes (3-5 max)
5. Afficher breakpoint compact

**Commandes:**

| Commande | Comportement |
|----------|--------------|
| `continue` | Intégrer réponses, nouvelles questions |
| `dive [topic]` | Focus profond sur un aspect, questions ciblées |
| `pivot` | Réorienter l'exploration, reset partiel EMS |
| `status` | Afficher EMS détaillé (5 axes avec radar) |
| `finish` | Passer en Phase 3 |

**Critères de suggestion `finish`:**
- EMS ≥ 70/100
- Axe Clarté ≥ 80/100
- Axe Actionnabilité ≥ 60/100

### Phase 3 — Génération

**Objectif**: Produire les livrables finaux.

**Actions:**
1. Compiler toutes les décisions en brief structuré
2. Générer le journal d'exploration
3. Créer le dossier `./docs/briefs/` si inexistant
4. Écrire les fichiers
5. Afficher résumé avec liens

## Format Breakpoint Compact

Optimisé pour CLI (évite le scroll) :

```
───────────────────────────────────────────────────────
📍 Iteration X | EMS: XX/100 (+Y) ████████░░░░ [emoji]
───────────────────────────────────────────────────────
✓ Décidé: [liste courte des éléments validés]
○ Ouvert: [liste courte des points à clarifier]

❓ Questions:
1. [Question concise]
2. [Question concise]
3. [Question concise]

→ continue | dive [topic] | pivot | status | finish
───────────────────────────────────────────────────────
```

**Emojis EMS:**
| Score | Emoji | Label |
|-------|-------|-------|
| 0-30 | 🌱 | Germination |
| 31-50 | 🌿 | Développement |
| 51-70 | 🌳 | Mature |
| 71-85 | 🎯 | Très Complète |
| 86-100 | 🏆 | Exceptionnelle |

## Détection de Frameworks

Appliquer automatiquement selon le contexte :

| Signal | Framework | Usage |
|--------|-----------|-------|
| Priorisation demandée | MoSCoW | Catégoriser Must/Should/Could/Won't |
| "Pourquoi" répété | 5 Whys | Creuser la cause racine |
| Plusieurs options | SWOT | Analyser forces/faiblesses |
| Critères multiples | Scoring | Matrice de décision |

## Gestion du Contexte Codebase

L'analyse `@Explore` initiale fournit :

| Élément | Utilisation |
|---------|-------------|
| Stack détecté | Adapter les suggestions techniques |
| Patterns existants | Proposer la cohérence architecturale |
| Fichiers impactés | Estimer la complexité |
| Conventions | Respecter le style du projet |

**Intégrer ces éléments dans les questions et suggestions.**

## Détection de Biais

Surveiller et alerter si détecté :

| Biais | Signal | Action |
|-------|--------|--------|
| Confirmation | Ignore les alternatives | Proposer des contre-exemples |
| Ancrage | Fixé sur première idée | Suggérer un pivot |
| Scope Creep | Expansion continue | Rappeler le focus initial |
| Complexité | Sur-ingénierie | Suggérer MVP |

## Réponses Utilisateur

Accepter les deux formats :

**Texte libre (prioritaire):**
```
Redis pour le cache, on garde l'approche centralisée pour les erreurs,
et oui on peut passer aux endpoints.
```

**Par numéro:**
```
1: Redis, 2: centralisée, 3: oui
```

## Anti-patterns

❌ **Ne pas faire:**
- Poser plus de 5 questions par itération
- Générer un breakpoint de plus de 15 lignes
- Ignorer le contexte codebase dans les suggestions
- Forcer un framework non pertinent
- Suggérer `finish` avant EMS 60/100

✅ **Toujours faire:**
- Baser les questions sur l'analyse codebase
- Proposer des suggestions avec les questions
- Mettre à jour EMS à chaque itération
- Respecter le format compact CLI
- Inclure les éléments décidés/ouverts
```

---

## 5. Références du skill

### 5.1 Contenu COMPLET de `references/ems-system.md`

```markdown
# EMS — Exploration Maturity Score

## Overview

Score composite sur 100 mesurant la maturité de l'exploration.
Calculé sur 5 axes pondérés.

## Les 5 Axes

| Axe | Poids | Description | Indicateurs |
|-----|-------|-------------|-------------|
| **Clarté** | 25% | Précision du besoin | Ambiguïtés résolues, reformulation validée |
| **Profondeur** | 20% | Niveau de détail | Specs détaillées, edge cases identifiés |
| **Couverture** | 20% | Exhaustivité | Tous aspects couverts, rien oublié |
| **Décisions** | 20% | Choix actés | Décisions prises vs en suspens |
| **Actionnabilité** | 15% | Prêt pour action | Assez de détails pour implémenter |

## Calcul

```
EMS = (Clarté × 0.25) + (Profondeur × 0.20) + (Couverture × 0.20) 
    + (Décisions × 0.20) + (Actionnabilité × 0.15)
```

Chaque axe est noté de 0 à 100.

## Échelle de Maturité

| Score | Niveau | Emoji | Signification |
|-------|--------|-------|---------------|
| 0-30 | Germination | 🌱 | Exploration initiale, beaucoup d'inconnues |
| 31-50 | Développement | 🌿 | Contours se précisent, questions clés identifiées |
| 51-70 | Mature | 🌳 | Vision claire, détails à affiner |
| 71-85 | Très Complète | 🎯 | Prêt pour implémentation, finish recommandé |
| 86-100 | Exceptionnelle | 🏆 | Exhaustif, documentation de référence |

## Affichage Compact (CLI)

```
📍 Iteration 3 | EMS: 58/100 (+12) ██████████░░░░░░░░░░ 🌿
```

- 20 caractères pour la barre
- Delta depuis dernière itération
- Emoji de niveau

## Affichage Détaillé (sur `status`)

```
📊 EMS : 58/100 ██████████░░░░░░░░░░ 🌿

   Clarté       █████████████████░░░ 85/100
   Profondeur   ██████████░░░░░░░░░░ 52/100
   Couverture   ██████████░░░░░░░░░░ 55/100
   Décisions    ███████████░░░░░░░░░ 58/100
   Actionnab.   ██████░░░░░░░░░░░░░░ 32/100

💡 Recommandation: Actionnabilité faible, détailler les specs techniques
```

## Évolution Typique

| Phase | EMS attendu | Actions |
|-------|-------------|---------|
| Init | 20-25 | Contexte établi, premières questions |
| Itération 1 | 35-45 | Cadrage initial fait |
| Itération 2 | 50-60 | Approfondissement |
| Itération 3 | 65-75 | Maturité atteinte |
| Finish | 70+ | Brief générable |

## Critères par Axe

### Clarté (25%)
- [ ] Besoin reformulé et validé
- [ ] Objectif principal clair
- [ ] Périmètre défini
- [ ] Utilisateurs cibles identifiés

### Profondeur (20%)
- [ ] Specs fonctionnelles détaillées
- [ ] Edge cases identifiés
- [ ] Contraintes techniques listées
- [ ] Dépendances mappées

### Couverture (20%)
- [ ] Tous les aspects fonctionnels couverts
- [ ] Impacts techniques identifiés
- [ ] Hors scope explicite
- [ ] Questions de sécurité/perf adressées

### Décisions (20%)
- [ ] Choix technologiques actés
- [ ] Approche architecturale décidée
- [ ] Priorités établies
- [ ] Compromis documentés

### Actionnabilité (15%)
- [ ] Assez de détails pour estimer
- [ ] Critères d'acceptation définis
- [ ] Première étape claire
- [ ] Risques identifiés
```

### 5.2 Contenu COMPLET de `references/frameworks.md`

```markdown
# Frameworks d'Analyse

## Overview

Outils méthodologiques à appliquer selon le contexte de l'exploration.
Détection automatique basée sur les signaux de la conversation.

## MoSCoW — Priorisation

### Déclencheur
- "Quelles priorités ?"
- "Qu'est-ce qui est essentiel ?"
- Multiple features à trier

### Application

| Catégorie | Définition | Critère |
|-----------|------------|---------|
| **Must** | Indispensable | Bloquant si absent |
| **Should** | Important | Forte valeur ajoutée |
| **Could** | Souhaitable | Nice to have |
| **Won't** | Exclu (v1) | Hors scope explicite |

### Format Output

```
📊 Priorisation MoSCoW

Must (non négociable):
- [Feature 1]
- [Feature 2]

Should (important):
- [Feature 3]

Could (si temps):
- [Feature 4]

Won't (v1):
- [Feature 5]
```

---

## 5 Whys — Analyse Causale

### Déclencheur
- Besoin flou ou symptôme plutôt que cause
- "Pourquoi" demandé plusieurs fois
- Problème récurrent

### Application

Creuser itérativement :
1. Pourquoi [problème initial] ?
2. Pourquoi [réponse 1] ?
3. Pourquoi [réponse 2] ?
4. Pourquoi [réponse 3] ?
5. Pourquoi [réponse 4] ? → Cause racine

### Format Output

```
🔍 Analyse 5 Whys

Problème: [énoncé initial]

1. Pourquoi ? → [réponse]
2. Pourquoi ? → [réponse]
3. Pourquoi ? → [réponse]
4. Pourquoi ? → [réponse]
5. Pourquoi ? → [cause racine]

✅ Cause racine identifiée: [conclusion]
```

---

## SWOT — Analyse Stratégique

### Déclencheur
- Comparaison d'approches
- Évaluation d'une option technique
- Décision architecture

### Application

| Dimension | Question |
|-----------|----------|
| **Strengths** | Quels avantages de cette approche ? |
| **Weaknesses** | Quelles limites ou risques ? |
| **Opportunities** | Quels bénéfices futurs ? |
| **Threats** | Quels dangers ou obstacles ? |

### Format Output

```
📋 Analyse SWOT — [Option]

┌─────────────────┬─────────────────┐
│ ✅ FORCES       │ ⚠️ FAIBLESSES   │
├─────────────────┼─────────────────┤
│ - [force 1]     │ - [faiblesse 1] │
│ - [force 2]     │ - [faiblesse 2] │
├─────────────────┼─────────────────┤
│ 🚀 OPPORTUNITÉS │ 🔴 MENACES      │
├─────────────────┼─────────────────┤
│ - [opport. 1]   │ - [menace 1]    │
│ - [opport. 2]   │ - [menace 2]    │
└─────────────────┴─────────────────┘
```

---

## Scoring — Matrice de Décision

### Déclencheur
- Plusieurs options à comparer
- Critères multiples
- Besoin de justifier un choix

### Application

1. Lister les options
2. Définir les critères (3-5 max)
3. Pondérer les critères
4. Noter chaque option (1-5)
5. Calculer les scores

### Format Output

```
📊 Matrice de Décision

Critères: Complexité (30%), Performance (25%), 
          Maintenabilité (25%), Coût (20%)

| Option    | Compl. | Perf. | Maint. | Coût | TOTAL |
|-----------|--------|-------|--------|------|-------|
| Option A  | 4      | 5     | 3      | 4    | 4.05  |
| Option B  | 3      | 4     | 5      | 3    | 3.80  |
| Option C  | 5      | 3     | 4      | 5    | 4.20  |

✅ Recommandation: Option C (score 4.20)
```

---

## Quand Appliquer

| Situation | Framework |
|-----------|-----------|
| Trop de features, besoin de trier | MoSCoW |
| Problème flou, symptôme vs cause | 5 Whys |
| Évaluer une approche technique | SWOT |
| Comparer plusieurs solutions | Scoring |
| Aucun signal clair | Continuer questions |

## Anti-patterns

❌ **Ne pas forcer** un framework si non pertinent
❌ **Ne pas combiner** plusieurs frameworks en une itération
❌ **Ne pas bloquer** l'exploration pour appliquer un framework
```

### 5.3 Contenu COMPLET de `references/brief-format.md`

```markdown
# Format du Brief Fonctionnel

## Overview

Template de sortie pour le brief généré par Brainstormer.
Compatible avec le workflow EPCI.

## Template Brief

```markdown
# Brief Fonctionnel — [Titre de la Feature]

> **Généré par**: Brainstormer
> **EMS Final**: XX/100
> **Date**: YYYY-MM-DD
> **Slug**: [feature-slug]

---

## Contexte

[Pourquoi cette feature ? Quel problème résout-elle ?
2-3 paragraphes maximum expliquant le besoin métier.]

## Objectif

[Description claire et concise de ce qu'on veut accomplir.
Une phrase principale, éventuellement 2-3 points de précision.]

## Stack Détecté

- **Framework**: [Symfony 7.x / React 18 / ...]
- **Language**: [PHP 8.3 / TypeScript / ...]
- **Patterns**: [Repository, Service, Controller, ...]
- **Outils**: [Doctrine, API Platform, Mercure, ...]

## Spécifications Fonctionnelles

### SF1 — [Nom du bloc fonctionnel]

[Description du bloc]

- [Spec détaillée 1]
- [Spec détaillée 2]
- [Spec détaillée 3]

**Contraintes**: [Si applicable]

### SF2 — [Nom du bloc fonctionnel]

[Description du bloc]

- [Spec détaillée]
- [Spec détaillée]

### SF3 — [Nom du bloc fonctionnel]

...

## Règles Métier

- **RM1**: [Règle métier 1]
- **RM2**: [Règle métier 2]
- **RM3**: [Règle métier 3]

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

## Contraintes Techniques Identifiées

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| [Contrainte 1] | [Impact] | [Solution] |
| [Contrainte 2] | [Impact] | [Solution] |

## Dépendances

- **Internes**: [Modules/services du projet impactés]
- **Externes**: [Libs, APIs, services tiers]

## Critères d'Acceptation

- [ ] [Critère mesurable 1]
- [ ] [Critère mesurable 2]
- [ ] [Critère mesurable 3]
- [ ] [Critère mesurable 4]

## Questions Ouvertes

> Ces points n'ont pas été résolus pendant l'exploration
> et devront être adressés pendant la phase Plan.

- [ ] [Question non résolue 1]
- [ ] [Question non résolue 2]

## Estimation Préliminaire

| Métrique | Valeur |
|----------|--------|
| Complexité estimée | [SMALL / STANDARD / LARGE] |
| Fichiers impactés | ~X |
| Risque | [Low / Medium / High] |

---

## Métadonnées Brainstormer

| Métrique | Valeur |
|----------|--------|
| Itérations | X |
| EMS Final | XX/100 |
| Frameworks utilisés | [MoSCoW, ...] |
| Durée exploration | ~Xmin |

---

*Brief prêt pour EPCI — Commande suggérée: `/epci-brief` ou `/epci`*
```

## Template Journal d'Exploration

```markdown
# Journal d'Exploration — [Titre]

> **Feature**: [Titre]
> **Date**: YYYY-MM-DD
> **Itérations**: X

---

## Résumé

[2-3 phrases résumant l'exploration]

## Progression EMS

| Itération | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 22 | - | Cadrage initial |
| 1 | 38 | +16 | [Focus] |
| 2 | 55 | +17 | [Focus] |
| 3 | 72 | +17 | [Focus] |
| Final | 78 | +6 | Finalisation |

## Décisions Clés

### Décision 1 — [Sujet]
- **Contexte**: [Pourquoi cette décision]
- **Options considérées**: [A, B, C]
- **Choix**: [Option retenue]
- **Justification**: [Raison]

### Décision 2 — [Sujet]
...

## Pivots

[Si des pivots ont eu lieu]

### Pivot 1 — Itération X
- **Avant**: [Direction initiale]
- **Après**: [Nouvelle direction]
- **Raison**: [Pourquoi le changement]

## Deep Dives

[Si des deep dives ont été faits]

### Deep Dive — [Topic]
- **Itération**: X
- **Résumé**: [Ce qui a été exploré]
- **Conclusion**: [Ce qui en ressort]

## Frameworks Appliqués

### [Framework] — Itération X
[Résultat de l'application du framework]

## Questions Résolues

| Question | Réponse | Itération |
|----------|---------|-----------|
| [Q1] | [R1] | X |
| [Q2] | [R2] | X |

## Biais Détectés

[Si des biais ont été détectés et corrigés]

- **[Biais]**: [Comment il s'est manifesté] → [Comment corrigé]

---

*Journal généré automatiquement par Brainstormer*
```

## Règles de Génération

1. **Slug**: kebab-case, dérivé du titre (ex: `systeme-notifications-temps-reel`)
2. **Date**: Format ISO (YYYY-MM-DD)
3. **Sections vides**: Omettre si rien à mettre (pas de "N/A")
4. **Longueur**: Brief = 1-3 pages, Journal = selon itérations
5. **Emplacement**: `./docs/briefs/`
```

---

## 6. Intégration EPCI

### 6.1 Modifications au README.md du plugin

Ajouter dans la section "Commandes" du tableau :

```markdown
| `/brainstorm` | Feature discovery | Idée vague → Brief complet |
```

Ajouter une nouvelle section après "Quick Start" :

```markdown
### Pré-EPCI : Feature Discovery

Pour les features qui partent d'une idée vague :

```bash
/brainstorm "description de l'idée"
```

Génère un brief fonctionnel complet dans `./docs/briefs/`,
prêt à être consommé par `/epci-brief` ou `/epci`.
```

### 6.2 Arborescence finale attendue

```
epci/
├── commands/
│   ├── brainstorm.md          # 🆕
│   ├── create.md
│   ├── epci-brief.md
│   ├── epci-decompose.md
│   ├── epci-learn.md
│   ├── epci-memory.md
│   ├── epci-quick.md
│   ├── epci-spike.md
│   └── epci.md
│
├── agents/
│   └── (inchangé)
│
└── skills/
    ├── core/
    │   ├── brainstormer/       # 🆕
    │   │   ├── SKILL.md
    │   │   └── references/
    │   │       ├── ems-system.md
    │   │       ├── frameworks.md
    │   │       └── brief-format.md
    │   ├── architecture-patterns/
    │   ├── clarification-intelligente/
    │   └── ...
    │
    ├── stack/
    └── factory/
```

---

## 7. Validation et Tests

### 7.1 Commandes de validation

Après création des fichiers, exécuter :

```bash
# Valider la commande
python scripts/validate_command.py commands/brainstorm.md

# Valider le skill
python scripts/validate_skill.py skills/core/brainstormer/

# Tester le triggering
python scripts/test_triggering.py skills/core/brainstormer/
```

### 7.2 Critères de validation

**Commande brainstorm.md:**
- [ ] YAML frontmatter valide
- [ ] Description présente avec "Use when:"
- [ ] allowed-tools valides : `[Read, Write, Bash, Glob, Grep, Task]`
- [ ] argument-hint présent

**Skill brainstormer/SKILL.md:**
- [ ] YAML frontmatter valide
- [ ] Nom kebab-case ≤ 64 chars : `brainstormer`
- [ ] Description avec "Use when:" et "Not for:"
- [ ] Description ≤ 1024 chars
- [ ] Contenu < 5000 tokens
- [ ] References existent si mentionnées

**References:**
- [ ] `ems-system.md` existe et est valide
- [ ] `frameworks.md` existe et est valide
- [ ] `brief-format.md` existe et est valide

### 7.3 Tests fonctionnels à effectuer

| Test | Commande | Résultat attendu |
|------|----------|------------------|
| Happy path | `/brainstorm "notifications"` | Breakpoint affiché |
| Sans project-memory | `/brainstorm "feature"` | Fonctionne avec @Explore seul |
| Commande continue | `continue` après questions | Nouvelle itération |
| Commande dive | `dive architecture` | Questions ciblées |
| Commande status | `status` | EMS détaillé 5 axes |
| Commande finish | `finish` | Brief + Journal générés |
| Vérif output | `ls ./docs/briefs/` | Fichiers présents |

---

## Annexe A — Checklist d'implémentation pour Claude Code

```
[ ] 1. Créer le dossier skills/core/brainstormer/
[ ] 2. Créer le dossier skills/core/brainstormer/references/
[ ] 3. Créer commands/brainstorm.md (contenu section 3.2)
[ ] 4. Créer skills/core/brainstormer/SKILL.md (contenu section 4.2)
[ ] 5. Créer skills/core/brainstormer/references/ems-system.md (contenu section 5.1)
[ ] 6. Créer skills/core/brainstormer/references/frameworks.md (contenu section 5.2)
[ ] 7. Créer skills/core/brainstormer/references/brief-format.md (contenu section 5.3)
[ ] 8. Valider avec python scripts/validate_command.py commands/brainstorm.md
[ ] 9. Valider avec python scripts/validate_skill.py skills/core/brainstormer/
[ ] 10. Tester le triggering
[ ] 11. Test fonctionnel complet
[ ] 12. Mettre à jour README.md (section 6.1)
```

---

## Annexe B — Exemples d'utilisation

### Exemple 1 : Lancement

```
> /brainstorm système de notifications en temps réel

📍 Brainstormer initialisé | EMS: 22/100 ████░░░░░░░░░░░░░░░░ 🌱

Contexte projet détecté:
- Stack: Symfony 6.4 + React 18
- Patterns: Repository, Service, API Platform
- Mercure déjà présent

Reformulation:
"Implémenter un système de notifications temps réel pour 
informer les utilisateurs des événements de l'application."

❓ Questions:
1. Quels événements doivent déclencher des notifications ?
2. Notifications in-app seulement ou aussi push/email ?
3. Les utilisateurs peuvent-ils configurer leurs préférences ?

→ continue | dive [topic] | status | finish
```

### Exemple 2 : Réponse et itération

```
> 1: Commandes, changements de statut. 2: In-app + email. 3: Oui

───────────────────────────────────────────────────────
📍 Iteration 1 | EMS: 41/100 (+19) ████████░░░░░░░░░░░░ 🌿
───────────────────────────────────────────────────────
✓ Décidé: Événements (commandes, statuts), Canaux (in-app, email), Préférences user
○ Ouvert: Format des notifications, Fréquence, Architecture technique

❓ Questions:
1. Format des notifications : titre + message + action ? Autres champs ?
2. Batching des emails (digest) ou envoi immédiat ?
3. Prêt à utiliser Mercure existant ou autre solution ?

→ continue | dive [topic] | pivot | status | finish
```

### Exemple 3 : Commande status

```
> status

📊 EMS : 41/100 ████████░░░░░░░░░░░░ 🌿

   Clarté       ██████████████░░░░░░ 65/100
   Profondeur   ██████░░░░░░░░░░░░░░ 32/100
   Couverture   ████████░░░░░░░░░░░░ 40/100
   Décisions    ██████████░░░░░░░░░░ 48/100
   Actionnab.   ████░░░░░░░░░░░░░░░░ 22/100

💡 Recommandation: Profondeur et Actionnabilité faibles
   → Détailler les specs techniques et les critères d'acceptation
```

### Exemple 4 : Finish

```
> finish

📍 Génération des livrables | EMS Final: 78/100 🎯

✅ Brief créé: ./docs/briefs/brief-notifications-temps-reel-2025-01-15.md
✅ Journal créé: ./docs/briefs/journal-notifications-temps-reel-2025-01-15.md

Résumé:
- 4 itérations
- 12 décisions prises
- 2 questions ouvertes (à traiter en Plan)

→ Prochaine étape suggérée: /epci-brief ou /epci
```

---

*Fin du cahier des charges — Document prêt pour Claude Code*
