---
description: >-
  Brainstorming guide v4 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  Inclut exploration technique (spike) pour valider la faisabilite.
  Use when: idee vague a transformer en specs, incertitude technique a valider.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--no-hmw] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v4.0

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

**Nouveau v4:** Integre l'exploration technique (spike) pour valider
la faisabilite avant de finaliser les specs.

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

**MANDATORY at EACH iteration:**

1. **Integrer les reponses** utilisateur
2. **Recalculer EMS** en utilisant la formule 5 axes de `references/ems-system.md`
   - Evaluer chaque axe (Clarte, Profondeur, Couverture, Decisions, Actionnabilite)
   - Calculer le score composite
   - Determiner le delta depuis la derniere iteration
3. **Appliquer frameworks** si pertinent (MoSCoW, 5 Whys, etc.)
4. **Generer questions/suggestions** suivantes (basees sur les axes faibles)
5. **Afficher breakpoint compact avec EMS visible**

**NEVER skip EMS calculation or display — it's the core metric of brainstorming progress.**

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
| `spike [duration] [question]` | Lancer exploration technique time-boxed |
| `finish` | Generer brief + journal |

---

## Spike — Exploration Technique Integree

### Quand utiliser `spike`

Pendant le brainstorm, si une **incertitude technique** emerge :
- "Est-ce que l'API X peut gerer nos volumes ?"
- "GraphQL est-il adapte a notre cas ?"
- "Comment integrer Redis avec notre stack ?"

### Commande

```
spike [duration] [question technique]
```

**Exemples :**
```
spike 30min Est-ce que Stripe supporte les webhooks async ?
spike 1h GraphQL vs REST pour notre API mobile
spike 2h Integration Redis avec notre stack Django
```

### Process Spike

#### 1. Framing (5 min)

Afficher le setup avant exploration :

```markdown
-------------------------------------------------------
🔬 SPIKE MODE | [duration]
-------------------------------------------------------
**Question:** [Question technique precise]

**Criteres de succes:**
- [ ] Critere 1 (mesurable)
- [ ] Critere 2 (mesurable)

**Scope:**
- Inclus: [Ce qu'on explore]
- Exclus: [Ce qu'on n'explore pas]
-------------------------------------------------------
```

#### 2. Exploration

- Invoquer `@Explore` (thorough level)
- Lire documentation, tester hypotheses
- Creer prototypes **jetables** (pas de code production)
- Respecter strictement le time-box

**Regles :**
- Le code produit est jetable
- Documenter les decouvertes au fur et a mesure
- Rester focus sur la question initiale

#### 3. Verdict

A la fin du time-box, determiner :

| Verdict | Signification | Action |
|---------|---------------|--------|
| **GO** | Faisable, approche identifiee | Continuer brainstorm avec cette info |
| **NO-GO** | Non faisable ou trop couteux | Pivoter vers alternative |
| **MORE_RESEARCH** | Besoin d'un autre spike | Planifier spike supplementaire |

#### 4. Retour au Brainstorm

Afficher resume et reprendre :

```markdown
-------------------------------------------------------
🔬 SPIKE COMPLETE | [duration]
-------------------------------------------------------
Verdict: [GO | NO-GO | MORE_RESEARCH]

Decouvertes cles:
1. [Decouverte 1]
2. [Decouverte 2]

Impact sur le brief:
- [Ajustement 1]
- [Ajustement 2]

-> Retour au brainstorm (EMS recalcule)
-------------------------------------------------------
```

Le verdict et les decouvertes sont integres :
- Dans le **brief final** (section "Technical Validation")
- Dans le **journal** (historique du spike)

---

### Phase 3 — Generation (USE WRITE TOOL)

**MANDATORY: You MUST use the Write tool to create BOTH files. Do NOT just display the content.**

#### Step 3.1: Create Brief File

**USE WRITE TOOL** to create `./docs/briefs/[slug]/brief-[slug]-[date].md`:
- Format: voir `references/brief-format.md`
- **Inclure la section "Exploration Summary"** avec stack, patterns, fichiers candidats
- **Si spike effectue:** Inclure section "Technical Validation" avec verdict et decouvertes
- Create `./docs/briefs/[slug]` directory first if it doesn't exist (use Bash: `mkdir -p ./docs/briefs/[slug]`)

#### Step 3.2: Create Journal File

**USE WRITE TOOL** to create `./docs/briefs/[slug]/journal-[slug]-[date].md`:
- Historique des iterations
- Decisions prises
- Questions resolues
- **Si spike effectue:** Section dedicee avec details de l'exploration

#### Step 3.3: Display Confirmation

**After BOTH files are written**, display resume final (MANDATORY format):

```
-------------------------------------------------------
BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100 [emoji]
Spikes: [X spike(s) effectue(s) | Aucun]

Fichiers generes:
   - Brief: ./docs/briefs/brief-[slug]-[date].md
   - Journal: ./docs/briefs/journal-[slug]-[date].md

Prochaine etape:
   Lancer /brief avec le contenu du brief ci-dessus.
   L'exploration ciblee affinera les fichiers impactes.
-------------------------------------------------------
```

## Format Breakpoint (compact pour CLI)

```
-------------------------------------------------------
[phase] | [persona] | Iter X | EMS: XX/100 (+Y) [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [elements a clarifier]

Questions:
1. [Question] -> Suggestion: [si applicable]
2. [Question]
3. [Question]

-> continue | dive [topic] | spike [duration] [q] | finish
-------------------------------------------------------
```

## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver generation des questions HMW |
| `--quick` | Mode rapide (3 iter max, EMS simplifie) |
| `--turbo` | Mode turbo: @clarifier (Haiku), max 3 iter, auto-accept si EMS > 60 |

### --turbo Mode (MANDATORY Instructions)

**When `--turbo` flag is active, you MUST follow these rules:**

1. **Use @clarifier agent** (Haiku model) for generating clarification questions:
   ```
   Invoke @clarifier via Task tool with model: haiku
   Input: Current brief + codebase context
   Output: 2-3 targeted questions with suggestions
   ```

2. **Maximum 3 iterations** — Auto-finish after iteration 3

3. **Auto-accept suggestions** if EMS > 60:
   - If EMS reaches 60+, suggest `finish` proactively
   - If user provides quick confirmation ("ok", "oui", "c"), auto-accept all suggestions

4. **Reduced breakpoint** — Compact format only, skip detailed explanations

5. **Skip HMW questions** — Equivalent to `--no-hmw`

**Turbo Process:**
```
Init -> @clarifier (Haiku) -> Iter 1 -> Iter 2 -> Iter 3 (max) -> finish
                              |
                        EMS > 60? -> Auto-suggest finish
```

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/[slug]/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/[slug]/journal-[slug]-[date].md` | Journal d'exploration (incluant spikes) |

## Integration EPCI

Le brief genere s'integre dans le workflow EPCI:

1. **Lancer `/brief`** avec le contenu du brief comme description
2. L'exploration ciblee (avec un brief precis) identifie les fichiers exacts
3. Le brief et le journal servent de **documentation** de la phase de decouverte

## Skills Charges

- `brainstormer` — Logique metier principale
- `project-memory` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
