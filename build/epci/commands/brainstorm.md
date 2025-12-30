---
description: >-
  Brainstorming guide v3 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  Use when: idee vague a transformer en specs, besoin de clarifier une feature.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--no-hmw] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v3.0

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

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
| **Skills** | `brainstormer`, `project-memory`, `architecture-patterns`, `mcp` |
| **Subagents** | `@Explore` (analyse codebase) |
| **Personas** | 📐 Architecte (defaut), 🥊 Sparring, 🛠️ Pragmatique |
| **Phases** | 🔀 Divergent → 🎯 Convergent |
| **MCP** | Context7 (patterns architecture), Sequential (raisonnement complexe) |

## Process

### Phase 1 — Initialisation

1. **Charger le contexte projet**
   - Skill: `project-memory`
   - Si `.project-memory/` existe → charger
   - Sinon → continuer sans contexte

2. **Analyser le codebase**
   - Invoquer `@Explore` avec Task tool
   - Scan complet : structure, stack, patterns, fichiers pertinents

3. **Reformuler le besoin**
   - Paraphraser la demande utilisateur
   - Detecter template (feature/problem/decision)

4. **Initialiser session**
   - Phase → 🔀 Divergent
   - Persona → 📐 Architecte
   - EMS → ~25/100

5. **Generer HMW** (si pas `--no-hmw`)
   - 3 questions "How Might We" orientees dev
   - Permettent de cadrer l'exploration

6. **Questions de cadrage** (3-5 max)
   - Basees sur l'analyse codebase
   - Suggestions incluses quand pertinent

7. **Afficher breakpoint compact**

### Phase 2 — Iterations

Boucle jusqu'a `finish` :

**⚠️ MANDATORY at EACH iteration:**

1. **Integrer les reponses** utilisateur
2. **Recalculer EMS** en utilisant la formule 5 axes de `references/ems-system.md`
   - Evaluer chaque axe (Clarte, Profondeur, Couverture, Decisions, Actionnabilite)
   - Calculer le score composite
   - Determiner le delta depuis la derniere iteration
3. **Appliquer frameworks** si pertinent (MoSCoW, 5 Whys, etc.)
4. **Generer questions/suggestions** suivantes (basees sur les axes faibles)
5. **Afficher breakpoint compact avec EMS visible**

**⚠️ NEVER skip EMS calculation or display — it's the core metric of brainstorming progress.**

**Commandes disponibles :**

| Commande | Action |
|----------|--------|
| `continue` | Iteration suivante avec nouvelles questions |
| `dive [topic]` | Approfondir un aspect specifique |
| `pivot` | Reorienter si le vrai besoin emerge |
| `status` | Afficher EMS detaille (5 axes) |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer un persona (architecte/sparring/pragmatique) |
| `premortem` | Lancer exercice d'anticipation des risques |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent |
| `scoring` | Evaluer et prioriser les idees |
| `framework [x]` | Appliquer un framework (moscow/5whys/swot) |
| `finish` | Generer brief + journal |

### Phase 3 — Generation (USE WRITE TOOL)

**⚠️ MANDATORY: You MUST use the Write tool to create BOTH files. Do NOT just display the content.**

#### Step 3.1: Create Brief File

**⚠️ USE WRITE TOOL** to create `./docs/briefs/brief-[slug]-[date].md`:
- Format: voir `references/brief-format.md`
- **Inclure la section "Exploration Summary"** avec stack, patterns, fichiers candidats
- Create `./docs/briefs/` directory first if it doesn't exist (use Bash: `mkdir -p ./docs/briefs`)

#### Step 3.2: Create Journal File

**⚠️ USE WRITE TOOL** to create `./docs/briefs/journal-[slug]-[date].md`:
- Historique des iterations
- Decisions prises
- Questions resolues

#### Step 3.3: Display Confirmation

**After BOTH files are written**, display resume final (MANDATORY format):

```
-------------------------------------------------------
✅ BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100 [emoji]

📄 Fichiers generes:
   • Brief: ./docs/briefs/brief-[slug]-[date].md
   • Journal: ./docs/briefs/journal-[slug]-[date].md

🚀 Prochaine etape:
   Lancer /epci-brief avec le contenu du brief ci-dessus.
   L'exploration ciblee affinera les fichiers impactes.
-------------------------------------------------------
```

## Format Breakpoint (compact pour CLI)

```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y) [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

Questions:
1. [Question] → Suggestion: [si applicable]
2. [Question]
3. [Question]

-> continue | dive [topic] | premortem | modes | finish
-------------------------------------------------------
```

## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver generation des questions HMW |
| `--quick` | Mode rapide (3 iter max, EMS simplifie) |

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/journal-[slug]-[date].md` | Journal d'exploration |

## Integration EPCI

Le brief genere s'integre dans le workflow EPCI:

1. **Lancer `/epci-brief`** avec le contenu du brief comme description
2. L'exploration ciblee (avec un brief precis) identifie les fichiers exacts
3. Le brief et le journal servent de **documentation** de la phase de decouverte

## Skills Charges

- `brainstormer` — Logique metier principale
- `project-memory` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
