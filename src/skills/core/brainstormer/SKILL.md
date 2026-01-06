---
name: brainstormer
description: >-
  Feature discovery et brainstorming guide pour EPCI v4.2. Workflow avec
  personas adaptatifs (Architecte, Sparring, Pragmatique), phases Divergent/
  Convergent, scoring EMS v2 et frameworks d'analyse incluant pre-mortem.
  v4.2: Session persistence, back command, energy checkpoints, 3-5 questions,
  agent confirmation [Y/n], @planner/@security integration.
  Use when: /brainstorm invoked, feature discovery needed.
  Not for: implementation tasks, code generation, simple questions.
allowed-tools: [Read, Write, Glob, Grep, Task]
---

# Brainstormer v4.2

## Overview

Skill de brainstorming specialise pour la decouverte de features.
Transforme des idees vagues en briefs fonctionnels complets via
un processus iteratif guide avec personas adaptatifs.

**Nouveautes v4.2:**
- **Session Persistence** — Sauvegarder et reprendre les sessions (`save`, `back`)
- **Energy Checkpoints** — Points de controle pour gerer la fatigue cognitive
- **3-5 Questions** — Plusieurs questions par iteration avec suggestions A/B/C
- **Agent Confirmation** — Prompt [Y/n] avant @planner/@security-auditor
- **@planner Integration** — Plan preliminaire en phase Convergent
- **@security-auditor Integration** — Analyse securite conditionnelle

**Reference Documents:**
- [Personas](references/personas.md) — 3 modes de facilitation
- [EMS System](references/ems-system.md) — Scoring v2 avec ancres objectives
- [Frameworks](references/frameworks.md) — Outils d'analyse rapide (5 frameworks)
- **[Techniques](references/techniques/)** — Bibliotheque etendue (20 techniques v4.2)
  - [Analysis](references/techniques/analysis.md) — 8 techniques (priorisation, causalite, decision)
  - [Ideation](references/techniques/ideation.md) — 6 techniques (generation d'idees)
  - [Perspective](references/techniques/perspective.md) — 3 techniques (changement de point de vue)
  - [Breakthrough](references/techniques/breakthrough.md) — 3 techniques (deblocage creatif)
- [Brief Format](references/brief-format.md) — Template de sortie
- [Session Format](references/session-format.md) — Format YAML pour persistence (v4.2)

**Session Storage:** `.project-memory/brainstorm-sessions/[slug].yaml`

## Personas

3 modes de facilitation avec bascule automatique.

| Persona | Icone | Role |
|---------|-------|------|
| **Architecte** | 📐 | Structure, frameworks, synthese (DEFAUT) |
| **Sparring** | 🥊 | Challenge, stress-test |
| **Pragmatique** | 🛠️ | Action, deblocage |

**Signalement** : En debut de message quand le mode change.
```
📐 [Structure] Organisons ce qu'on a explore...
🥊 [Challenge] Attends — qu'est-ce qui te fait dire ca ?
🛠️ [Action] Assez analyse. Quelle est la decision ?
```

→ Voir [personas.md](references/personas.md) pour les regles de bascule

## Phases

| Phase | Icone | Focus |
|-------|-------|-------|
| **Divergent** | 🔀 | Generer, explorer, quantite |
| **Convergent** | 🎯 | Evaluer, decider, qualite |

**Transition auto** : Couverture >= 60% ET iter >= 3 → suggerer Convergent

## Workflow 3 Phases

### Phase 1 — Initialisation

**Objectif**: Etablir le contexte, definir la phase et le persona.

**Actions:**
1. Charger le contexte projet via `project-memory`
2. Invoquer `@Explore` pour analyser le codebase
3. Reformuler le besoin utilisateur
4. Detecter template (feature/problem/decision)
5. Generer 3-5 questions de cadrage
6. Initialiser EMS a ~20-25/100
7. Definir phase → 🔀 Divergent
8. Definir persona → 📐 Architecte
9. Generer HMW (si pas --no-hmw)

**HMW (How Might We)** — Apres validation brief :
```
💡 Questions "How Might We"

1. HMW [simplifier] [processus] sans [compromis] ?
2. HMW garantir [qualite] meme si [contrainte] ?
3. HMW permettre [fonctionnalite] dans [contexte difficile] ?

→ Laquelle on explore en premier ?
```

**Output**: Premier breakpoint avec phase, persona et questions.

### Phase 2 — Iterations

**Objectif**: Approfondir et affiner jusqu'a maturite.

**⚠️ MANDATORY — EMS CALCULATION AT EACH ITERATION:**

The EMS (Exploration Maturity Score) is the core metric of brainstorming progress.
It MUST be calculated and displayed at every iteration.

**Boucle:**
1. Integrer les reponses utilisateur
2. **Recalculer les 5 axes EMS** (voir `references/ems-system.md`):
   - Clarte (25%) — Precision du besoin
   - Profondeur (20%) — Niveau de detail
   - Couverture (20%) — Exhaustivite
   - Decisions (20%) — Choix actes
   - Actionnabilite (15%) — Pret pour action
3. **Calculer le delta** depuis la derniere iteration
4. Detecter si un framework est applicable (basé sur les axes faibles)
5. **Generer 3-5 questions** avec choix multiples A/B/C (voir Question Format v4.2)
6. **Afficher breakpoint compact AVEC EMS visible**

### Question Format (v4.2)

**3-5 questions par iteration avec choix multiples A/B/C.**

**Regles:**
- 3-5 questions par iteration (defaut v4.2)
- Choix multiples A/B/C par question
- Suggestions incluses quand pertinent
- Focus sur les blocages uniquement

**Format:**
```
1. [Question 1]
   A) Option A  B) Option B  C) Option C
   → Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
   → Suggestion: A

3. [Question 3]
   A) Option A  B) Option B  C) Option C
```

**Une seule question**: Pour decisions complexes ou `dive` command.

**⚠️ NEVER skip EMS display in breakpoint header:**
```
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y) [emoji]
```

**Commandes (v4.2):**

| Commande | Comportement |
|----------|--------------|
| `continue` | Iteration suivante (3-5 questions) |
| `dive [topic]` | Focus profond sur un aspect |
| `pivot` | Reorienter l'exploration |
| `status` | Afficher EMS detaille (5 axes) |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer un persona |
| `premortem` | Lancer exercice pre-mortem |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent + invoquer @planner |
| `scoring` | Evaluer les idees |
| `framework [x]` | Appliquer un framework |
| `plan-preview` | Invoquer @planner manuellement |
| `security-check` | Invoquer @security-auditor manuellement |
| `save` | Sauvegarder session (v4.2) |
| `back` | Revenir a l'iteration precedente (v4.2) |
| `energy` | Forcer energy check (v4.2) |
| `finish` | Passer en Phase 3 |

**Criteres de suggestion `finish`:**
- EMS >= 70/100
- Axe Clarte >= 80/100
- Axe Actionnabilite >= 60/100

### @planner Integration (v4.2)

**Auto-invocation:** En phase Convergent OU quand EMS >= 70

**Confirmation [Y/n] (v4.2):** Demander confirmation avant invocation auto.
```
🎯 EMS atteint 72 — Pret pour un plan preliminaire?
   Lancer @planner? [Y/n]
```

Invoquer via Task tool (model: sonnet) pour generer un plan preliminaire.
Integre dans brief final section "Preliminary Plan".

### @security-auditor Integration (v4.2)

**Auto-detection:** Si brief contient patterns auth/security/payment/api

**Confirmation [Y/n] (v4.2):** Demander confirmation avant invocation auto.
```
🔒 Patterns securite detectes: [auth, payment]
   Lancer @security-auditor? [Y/n]
```

Invoquer via Task tool (model: opus) pour analyse securite.
Integre dans brief final section "Security Considerations".

### Phase 3 — Generation (USE WRITE TOOL)

**Objectif**: Produire les livrables finaux avec validation incrementale.

**⚠️ MANDATORY: You MUST use the Write tool to create BOTH files. Do NOT just display content.**

### Section-by-Section Validation

**Avant d'ecrire le brief, valider chaque section avec l'utilisateur:**

```
1. Afficher section Contexte (200-300 mots)
   -> "Does this look right? [y/edit/skip]"

2. Continuer pour chaque section majeure:
   - Contexte -> Objectif -> Specifications -> Regles Metier
   - Contraintes Techniques -> Criteres d'Acceptation

3. Une fois validees -> Ecrire le fichier complet
```

**Format validation section:**
```
-------------------------------------------------------
📝 BRIEF SECTION: [Nom] (X/6)
-------------------------------------------------------

[Contenu 200-300 mots]

-> y (valider) | edit (modifier) | skip
-------------------------------------------------------
```

**Quand skipper:** `--quick`, `--turbo`, ou EMS >= 85

**Actions:**
1. Create directory: `mkdir -p ./docs/briefs/[slug]` (use Bash tool)
2. **Validation section par section** (si pas --quick/--turbo)
3. **USE WRITE TOOL** to create `./docs/briefs/[slug]/brief-[slug]-[date].md`:
   - Compiler toutes les decisions en brief structure
   - **Inclure "Exploration Summary"** (stack, patterns, fichiers)
   - **Si @planner:** Inclure "Preliminary Plan"
   - **Si @security-auditor:** Inclure "Security Considerations"
4. **USE WRITE TOOL** to create `./docs/briefs/[slug]/journal-[slug]-[date].md`:
   - Historique des iterations, decisions prises, questions resolues
   - Section agents invoques si applicable
5. **After BOTH files written**, afficher resume final (MANDATORY):

```
-------------------------------------------------------
✅ BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100 [emoji]
Agents: [@planner | @security-auditor | Aucun]

📄 Fichiers generes:
   • Brief: ./docs/briefs/[slug]/brief-[slug]-[date].md
   • Journal: ./docs/briefs/[slug]/journal-[slug]-[date].md

🚀 Prochaine etape:
   Lancer /brief avec le contenu du brief.
-------------------------------------------------------
```

## Format Breakpoint Compact

Optimise pour CLI (evite le scroll) :

```
-------------------------------------------------------
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y) [emoji]
-------------------------------------------------------
Done: [elements valides]
Open: [points a clarifier]

Questions:
1. [Question] → Suggestion: [si applicable]
2. [Question]
3. [Question]

-> continue | dive [topic] | back | save | energy | finish
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
| Risques, projet important | Pre-mortem | Anticiper les echecs |

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

Surveiller et alerter si detecte (max 1 alerte par type par session) :

| Biais | Signal | Action |
|-------|--------|--------|
| Over-engineering | "Ajoutons X au cas ou" | Suggerer MVP |
| Scope creep | Expansion continue | Rappeler le focus initial |
| Sunk cost | "On a deja fait X" | Challenger l'attachment |
| Bikeshedding | Focus sur details triviaux | Recentrer sur le critique |

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

## Mapping Techniques → Phases (v4.2)

Guide de selection des techniques selon la phase du brainstorm.

| Phase | Techniques Recommandees |
|-------|------------------------|
| 🔀 **Divergent** | SCAMPER, Six Thinking Hats, Mind Mapping, What If Scenarios, Analogical Thinking, First Principles, Time Travel, Inner Child Conference, Chaos Engineering, Nature's Solutions |
| 🎯 **Convergent** | MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem, Constraint Mapping, Assumption Reversal, Role Playing |
| ⚡ **Deblocage** | Reversal Inversion, Question Storming |

**Usage:** Commande `technique [nom]` pour afficher la documentation complete d'une technique.

**Auto-suggestion:** Selon les axes EMS faibles:
- Clarte faible → Question Storming, 5 Whys
- Profondeur faible → First Principles, Dive
- Couverture faible → SCAMPER, Six Thinking Hats
- Decisions faible → MoSCoW, Scoring
- Actionnabilite faible → Pre-mortem, Constraint Mapping
