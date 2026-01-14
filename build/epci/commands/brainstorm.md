---
description: >-
  Brainstorming guide v5.2 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  Brief output conforme PRD Industry Standards v3.0.
  Breakpoints style /brief (boite ASCII + EMS 5 axes visuels).
  Questions via AskUserQuestion natif (3 max, headers priorite, suggestions).
  Finalization Checkpoint obligatoire a EMS >= 70 (bloquant).
  Session persistence, energy checkpoints.
  Use when: idee vague a transformer en specs, incertitude technique.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--random] [--progressive] [--no-hmw] [--no-security] [--no-technique] [--no-clarify] [--competitive] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch, AskUserQuestion]
---

# /brainstorm — Feature Discovery v5.2

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

**Nouveautes v5.2**:
- **Breakpoints style /brief** — Boîtes ASCII (`┌─ │ ├─ └─`) au lieu de tirets simples
- **EMS 5 axes visuels** — Barres de progression (`████████░░`) à chaque itération
- **Axes faibles marqués** — `[WEAK]` sur les axes < 50
- **Progression EMS** — Historique visible au checkpoint (Init→Iter1→Iter2→Final)
- **Tracking obligatoire** — `ems_history` stocké dans session_state
- **Journal corrigé** — Axes standards obligatoires (pas d'invention)

**Nouveautes v5.1**:
- **AskUserQuestion natif** — Questions via outil Claude Code (UI QCM interactive)
- **3 questions max** par iteration (au lieu de 5)
- **Headers priorité** — `🛑 Critical`, `⚠️ Important`, `ℹ️ Info` (max 12 chars)
- **Suggestions visuelles** — `(Recommended)` dans le label de l'option suggérée
- **Breakpoint séparé** — Status en texte, questions via AskUserQuestion
- **Technique-advisor adapté** — Retourne JSON, main thread pose la question

**Nouveautes v5.0**:
- **Brief PRD Industry Standards v3.0** — Executive Summary, Problem Statement, Goals/Non-Goals, Timeline & Milestones, FAQ, Assumptions, Appendix
- **Flag `--competitive`** — Active la section Competitive Analysis
- **Finalization Checkpoint** abaisse a EMS >= 70 (bloquant)
- Pas de finalisation automatique — toujours choix explicite

**Nouveautes v4.9**:
- **Finalization Checkpoint** obligatoire a EMS >= 85 (bloquant)
- Pas de finalisation automatique — toujours choix explicite

**Nouveautes v4.8**:
- Auto-selection de techniques basee sur axes EMS faibles (< 50)
- Mix de techniques quand 2+ axes faibles
- Transition check explicite Divergent → Convergent
- Preview @planner/@security en phase
- Hook post-brainstorm documente

## Usage

```
/brainstorm [description de la feature souhaitee]
```

## Configuration

| Element | Valeur |
|---------|--------|
| **Thinking** | `think hard` (adaptatif) |
| **Skills** | `brainstormer`, `project-memory`, `architecture-patterns`, `mcp` |
| **Subagents** | `@Explore`, `@clarifier`, `@planner`, `@security-auditor`, `@ems-evaluator`, `@technique-advisor` |
| **Personas** | Architecte (defaut), Sparring, Pragmatique |
| **Phases** | Divergent -> Convergent |
| **Storage** | `.project-memory/brainstorm-sessions/[slug].yaml` |

## Process

### Phase 0 — Session Detection

**MANDATORY: Check for existing session before starting.**

1. Look in `.project-memory/brainstorm-sessions/` for matching slug
2. If found: Prompt resume or new session
3. If new: Archive existing, start fresh

### Step 0 — Input Clarification (Conditional)

**Skill**: `input-clarifier`

Clarify initial description if confusing (dictated input with hesitations, fillers, etc.).

**Important**: Only applies to **initial input**, NOT to iteration responses during Phase 2.

```
IF --no-clarify flag:
   → Skip to Phase 1

ELSE:
   → Calculate clarity score on initial description
   → IF score < 0.6: Show reformulation prompt
   → IF score >= 0.6: Continue to Phase 1
```

**Example trigger:**
```
Input: "euh une feature de notifications, genre tu vois pour les users"
Score: 0.4 → Clarification triggered

⚠️ Input confus détecté

Original: "euh une feature de notifications, genre tu vois pour les users"
Reformulation: "Une feature de notifications pour les utilisateurs"

[1] ✅ Utiliser   [2] ✏️ Modifier   [3] ➡️ Garder
```

---

### Phase 1 — Initialisation

1. **Charger contexte** — Skill: `project-memory`
2. **Reformuler besoin** — Detecter template (feature/problem/decision)
3. **Analyser codebase** — `@Explore` avec `run_in_background: true`
4. **Initialiser session** — Phase: Divergent, Persona: Architecte, EMS: ~25
5. **SYNC @Explore** — Attendre completion si non termine
6. **Generer HMW** (si pas `--no-hmw`) — 3 questions "How Might We" **avec contexte codebase**
7. **Afficher status breakpoint** (texte markdown):
   ```
   -------------------------------------------------------
   PHASE 1 — INITIALISATION COMPLÈTE
   -------------------------------------------------------
   ✅ Contexte chargé | ✅ @Explore terminé | ✅ HMW générées
   Prochaine étape: Questions de cadrage (3 max)
   -------------------------------------------------------
   ```
8. **Questions de cadrage** — Utiliser AskUserQuestion (3 max):
   - Header pour priorité: `🛑 Critical`, `⚠️ Important`, `ℹ️ Info` (max 12 chars)
   - `(Recommended)` sur l'option suggérée basée sur patterns codebase
   - Ordre: 🛑 d'abord, puis ⚠️, puis ℹ️
   - Option "Other..." automatiquement disponible
   ```typescript
   AskUserQuestion({
     questions: [
       {
         question: "Quelle est la cible principale de cette feature ?",
         header: "🛑 Critical",
         multiSelect: false,
         options: [
           { label: "Utilisateurs finaux", description: "Focus UX et facilité d'usage" },
           { label: "Développeurs (Recommended)", description: "Focus API et intégration" },
           { label: "Admins", description: "Focus gestion et monitoring" }
         ]
       },
       // ... 2 autres questions max
     ]
   })
   ```

> **Note v4.8**: HMW generes APRES @Explore pour questions contextuelles basees sur le codebase.
> **Note v4.9**: Input clarification en Step 0 ne s'applique qu'a l'input initial, pas aux iterations.

### Phase 2 — Iterations

Boucle jusqu'a `finish`:

1. **Integrer reponses** utilisateur
2. **Recalculer EMS** via `@ems-evaluator`
   - Output: scores, delta, `weak_axes[]` (axes < 50)
   - **Tracking obligatoire (v5.2)**: Stocker dans `session_state.ems_history`:
     ```yaml
     ems_history:
       - iter: 0
         ems: 22
         delta: null
         focus: "Cadrage initial"
       - iter: 1
         ems: 38
         delta: "+16"
         focus: "Clarté"
     ```
3. **Afficher breakpoint** (v5.2 — boîte ASCII avec EMS détaillé):
   - Voir format détaillé dans `src/skills/core/brainstormer/SKILL.md` section "Breakpoint Format"
   - Utiliser output compact JSON de `@ems-evaluator` pour les barres de progression
4. **Auto-selection technique** (v4.8+ — AskUserQuestion):
   - Si `weak_axes` non vide ET technique pas dans les 2 dernieres iterations:
     - Invoquer `@technique-advisor` (subagent) → retourne JSON structuré
     - **Main thread** pose la question via AskUserQuestion:
     ```typescript
     // Technique unique (1 axe faible)
     AskUserQuestion({
       questions: [{
         question: "Technique suggérée: [NOM] pour améliorer [AXE] (XX%). Appliquer ?",
         header: "💡 Technique",
         multiSelect: false,
         options: [
           { label: "Appliquer (Recommended)", description: "[description technique]" },
           { label: "Autre technique", description: "Choisir parmi alternatives" },
           { label: "Ignorer", description: "Continuer sans technique" }
         ]
       }]
     })

     // Mix (2+ axes faibles)
     AskUserQuestion({
       questions: [{
         question: "2 axes faibles détectés. Quelle(s) technique(s) appliquer ?",
         header: "💡 Mix",
         multiSelect: true,
         options: [
           { label: "[Technique1]", description: "Pour [Axe1] (XX%)" },
           { label: "[Technique2]", description: "Pour [Axe2] (YY%)" },
           { label: "Les deux (Recommended)", description: "Application séquentielle" }
         ]
       }]
     })
     ```
   - Desactiver avec `--no-technique`
5. **Transition check** (si EMS = 50 et Divergent):
   - **Étape A — Status (texte)**:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔄 PHASE TRANSITION | EMS: 50/100
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Mi-parcours atteint. Choix de direction requis.
   ```
   - **Étape B — Question (AskUserQuestion)**:
   ```typescript
   AskUserQuestion({
     questions: [{
       question: "Mi-parcours EMS 50. Quelle direction prendre ?",
       header: "🔄 Transition",
       multiSelect: false,
       options: [
         { label: "Continuer Divergent", description: "Explorer plus d'options" },
         { label: "Passer Convergent (Recommended)", description: "Commencer à converger" },
         { label: "Appliquer technique", description: "Utiliser technique pour débloquer" }
       ]
     }]
   })
   ```
6. **Finalization checkpoint** (si EMS >= 70):
   - **Utiliser format boîte ASCII v5.2** (voir SKILL.md section "Finalization Checkpoint")
   - Inclut: EMS final avec 5 axes visuels + ligne de progression
   - **Étape B — Question (AskUserQuestion)**:
   ```typescript
   AskUserQuestion({
     questions: [{
       question: "Brief EMS XX/100 prêt. Quelle action ?",
       header: "🎯 Checkpoint",
       multiSelect: false,
       options: [
         { label: "Continuer", description: "Plus d'itérations pour affiner" },
         { label: "Preview (Recommended)", description: "@planner sans finaliser" },
         { label: "Finaliser", description: "Générer brief + journal maintenant" }
       ]
     }]
   })
   ```
   - **Comportement**: Continuer → questions, Preview → @planner puis redemande, Finaliser → Phase 3
   - **CRITICAL**: Checkpoint BLOQUANT. Attendre réponse explicite.
7. **Générer questions** — AskUserQuestion (3 max, si choix Continuer):
   ```typescript
   AskUserQuestion({
     questions: [
       { question: "...", header: "🛑 Critical", multiSelect: false, options: [...] },
       { question: "...", header: "⚠️ Important", multiSelect: false, options: [...] },
       { question: "...", header: "ℹ️ Info", multiSelect: false, options: [...] }
     ]
   })
   ```
   - Ordre: 🛑 d'abord, puis ⚠️, puis ℹ️
   - `(Recommended)` sur option suggérée
8. **Preview check** (si Convergent et EMS >= 65 et choix [2]):
   - Proposer `@planner preview? [Y/n]`
   - Si patterns auth: `@security-auditor preview? [Y/n]`

**NEVER skip EMS calculation — core metric of progress.**

### Phase 3 — Generation

**MANDATORY: Use Write tool to create BOTH files using official templates.**

**Templates obligatoires** (dans `src/skills/core/brainstormer/references/`):
- `brief-format.md` — Structure PRD v3.0 (Industry Standards Compliant)
- Section Journal d'Exploration dans le meme fichier

1. **@planner** (si pas preview fait OU EMS >= 70)
2. **@security-auditor** (si patterns auth ET pas preview)
3. Create directory: `mkdir -p ./docs/briefs/[slug]`
4. **Lire template**: `Read src/skills/core/brainstormer/references/brief-format.md`
5. **Section-by-section validation** (si pas --quick/--turbo)
6. Write `brief-[slug]-[date].md` — **DOIT suivre la structure PRD v3.0**
7. Write `journal-[slug]-[date].md` — **DOIT suivre le Template Journal d'Exploration**
8. **Calculate project estimation** — Sum story complexity to determine category
9. **HOOK: post-brainstorm** — Invocation automatique (voir section Hooks)
10. **Display completion summary** — With next steps recommendation (see format below)

**Sections OBLIGATOIRES dans le brief** (PRD v3.0):
- **Document Header** — PRD-YYYY-XXX, Version, Status, Change History
- **Executive Summary** — TL;DR, Problem, Solution, Impact
- **Background & Strategic Fit** — Why Now?, Strategic Alignment
- **Problem Statement** — Current Situation, Evidence & Data, Impact
- **Goals** — Business/User/Technical goals avec metriques
- **Non-Goals** — Exclusions explicites (remplace Hors Scope)
- **Personas** (minimum 1 primaire)
- **User Stories** format "En tant que... je veux... afin de" avec AC Given/When/Then
- **User Flow** — As-Is vs To-Be avec Key Improvements
- **Assumptions** — Hypotheses Technical/Business/User/Resources
- **FAQ** — Internal + External (Amazon-style)
- **Success Metrics** (KPIs ou "TBD")
- **Timeline & Milestones** — Key milestones avec Phasing Strategy

**Sections OPTIONNELLES**:
- **Competitive Analysis** — Avec flag `--competitive`
- **Appendix** — Research Findings, Technical Deep Dives, Glossary

**Anti-pattern**: Generer un brief sans lire `brief-format.md` d'abord.

---

### Project Estimation & Next Steps Logic

**Step 8: Calculate Project Estimation**

Calculate total estimated effort from User Stories to determine project category:

```python
# Sum complexity from Must-have stories
total_effort = sum(
    1 if story.complexite == "S" else
    3 if story.complexite == "M" else
    5 for story in must_have_stories
)

# Determine category
if total_effort <= 2:
    category = "TINY"
elif total_effort <= 5:
    category = "SMALL/STANDARD"
else:
    category = "LARGE"
```

**Step 10: Completion Summary Format**

Display structured summary with next steps recommendation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BRAINSTORM COMPLETED | EMS: {score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files Generated:
├── Brief: ./docs/briefs/{slug}/brief-{slug}-{date}.md
└── Journal: ./docs/briefs/{slug}/journal-{slug}-{date}.md

📊 Project Estimation:
├── User Stories: {total_count} ({must_count} Must-have, {should_count} Should-have, {could_count} Could-have)
├── Estimated Effort: {total_effort} days ({must_effort}j Must-have + {should_effort}j Should-have)
└── Complexity Category: {TINY|SMALL|STANDARD|LARGE}

🎯 RECOMMENDED NEXT STEPS:

{if category == "TINY"}
  TINY project detected (≤2 days)

  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md
    Claude will route automatically to /quick --autonomous

{else if category == "SMALL/STANDARD" and total_effort <= 5}
  SMALL/STANDARD project ({total_effort} days)

  Option 1 (Recommended): Direct EPCI workflow
  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md

  Option 2: Decompose first (if you want granular tracking)
  → /decompose ./docs/briefs/{slug}/brief-{slug}-{date}.md

{else if category == "LARGE"}
  ⚠️  LARGE project detected ({total_effort} days)

  Recommended: Decompose into manageable sub-specs
  → /decompose ./docs/briefs/{slug}/brief-{slug}-{date}.md
     Breaks down into sub-specs of 1-5 days each
     Generates INDEX.md with dependency graph

  Then, choose execution strategy:

  Option A: Batch execution (recommended for 5+ sub-specs)
  → /orchestrate ./docs/specs/{slug}/
     Automatic DAG-based execution with priority handling

  Option B: Manual execution (for sequential control)
  → /brief @./docs/specs/{slug}/S01-{name}.md
     Execute each sub-spec individually as needed

  Alternative: Direct workflow (not recommended for >10 days)
  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md --large
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Session Metrics:
├── Techniques applied: {techniques_list}
├── Duration: ~{duration} min
├── Iterations: {count}
└── Phase transitions: {phase_transitions}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Effort Calculation Examples:**

| User Stories | Complexity | Calculated Effort | Category | Recommended Command |
|--------------|------------|-------------------|----------|---------------------|
| US1, US2 | S, S | 1 + 1 = 2j | TINY | `/brief` → `/quick --autonomous` |
| US1, US2, US3 | S, M, M | 1 + 3 + 3 = 7j | LARGE | `/decompose` |
| US1, US2 | M, M | 3 + 3 = 6j | LARGE | `/decompose` |
| US1, US2, US3 | S, S, M | 1 + 1 + 3 = 5j | STANDARD | `/brief` (or `/decompose` for tracking) |

**Important Notes:**

- Only Must-have stories count toward MVP effort
- Should-have and Could-have are mentioned but don't trigger LARGE category
- If total effort > 5 days from Must-have alone → Always recommend `/decompose`
- If 3-5 days → Present both options, let user decide
- If ≤2 days → Direct to `/brief` (will auto-route to `/quick`)

---

## Commands

### Standard Commands

| Commande | Action |
|----------|--------|
| `continue` | Iteration suivante (3-5 questions) |
| `dive [topic]` | Approfondir un aspect |
| `pivot` | Reorienter si vrai besoin emerge |
| `status` | Afficher EMS detaille (5 axes) |
| `modes` | Afficher/changer persona |
| `mode [nom]` | Forcer persona (architecte/sparring/pragmatique) |
| `premortem` | Exercice anticipation risques |
| `diverge` | Forcer phase Divergent |
| `converge` | Forcer phase Convergent + @planner |
| `scoring` | Evaluer et prioriser idees |
| `framework [x]` | Appliquer framework (moscow/5whys/swot) |
| `technique [x]` | Afficher technique complete via @technique-advisor |
| `spike [duration] [q]` | Exploration technique (voir reference) |
| `security-check` | Invoquer @security-auditor |
| `plan-preview` | Invoquer @planner |
| `save` | Sauvegarder session |
| `back` | Iteration precedente |
| `energy` | Forcer energy check |
| `finish` | Generer brief + journal |

### Party Mode Commands (v5.0)

| Commande | Action |
|----------|--------|
| `party` | Demarrer discussion multi-persona |
| `party add [persona]` | Ajouter persona au round actuel |
| `party focus [persona]` | Deep dive d'un persona specifique |
| `party exit` | Quitter party mode, retour standard |

**Personas disponibles**: Architect, Security, Frontend, Backend, QA

### Expert Panel Commands (v5.0)

| Commande | Action |
|----------|--------|
| `panel` | Demarrer panel d'experts (phase discussion) |
| `panel debate` | Passer en phase debate (stress-test) |
| `panel socratic` | Passer en phase socratic (questions) |
| `panel exit` | Quitter panel mode, retour standard |

**Experts disponibles**: Martin, Fowler, Newman, Gamma, Beck

## Flags

### Core Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver HMW |
| `--quick` | 3 iter max, skip validation |
| `--turbo` | Mode turbo (voir reference) |
| `--no-security` | Desactiver @security-auditor auto |
| `--no-plan` | Desactiver @planner auto |
| `--no-technique` | Desactiver auto-suggestion techniques |
| `--no-clarify` | Desactiver clarification input initial |
| `--force-clarify` | Forcer clarification meme si input clair |
| `--competitive` | Activer section Competitive Analysis dans le brief (PRD v3.0) |

### Technique Mode Flags (v5.0)

| Flag | Effet |
|------|-------|
| `--random` | Selection aleatoire techniques avec equilibrage categories |
| `--progressive` | Mode 4 phases progressives (Expansion → Exploration → Convergence → Action) |

### Collaboration Mode Flags (v5.0)

| Flag | Effet |
|------|-------|
| `--party` | Demarrer en party mode (multi-persona) |
| `--panel` | Demarrer en expert panel mode |

**Note**: `--party` et `--panel` sont mutuellement exclusifs. Un seul mode actif a la fois.

## References

| Topic | Reference |
|-------|-----------|
| Turbo mode | [brainstorm-turbo-mode.md](references/brainstorm-turbo-mode.md) |
| Random mode | [brainstorm-random-mode.md](references/brainstorm-random-mode.md) |
| Progressive mode | [brainstorm-progressive-mode.md](references/brainstorm-progressive-mode.md) |
| Spike process | [brainstorm-spike-process.md](references/brainstorm-spike-process.md) |
| Session commands | [brainstorm-session-commands.md](references/brainstorm-session-commands.md) |
| Energy checkpoints | [brainstorm-energy-checkpoints.md](references/brainstorm-energy-checkpoints.md) |

## Agents

### Core Agents

| Agent | Model | Role |
|-------|-------|------|
| `@Explore` | - | Analyse codebase |
| `@clarifier` | haiku | Questions turbo mode |
| `@planner` | sonnet | Plan convergent |
| `@security-auditor` | opus | Audit securite |
| `@ems-evaluator` | haiku | Calcul EMS 5 axes |
| `@technique-advisor` | haiku | Selection techniques (63 en CSV) |

### v5.0 Agents

| Agent | Model | Role |
|-------|-------|------|
| `@party-orchestrator` | sonnet | Orchestration multi-persona (5 personas) |
| `@expert-panel` | sonnet | Panel 5 experts dev (3 phases) |

**@planner auto-invocation**: En phase Convergent OU quand EMS >= 85

**@security-auditor auto-detection**: Si patterns auth/security/payment/api detectes

**@party-orchestrator**: Invoque via commande `party` ou flag `--party`

**@expert-panel**: Invoque via commande `panel` ou flag `--panel`

## Hooks

| Hook | Quand | Donnees |
|------|-------|---------|
| `post-brainstorm` | Apres `finish` (Phase 3) | feature_slug, ems_score, techniques_applied, personas_used, iterations, duration_minutes |

**Invocation automatique** a la fin de Phase 3 via hook runner.

**Effets**:
- Sauvegarde metriques dans `.project-memory/brainstorm-sessions/`
- Tracking des techniques utilisees pour analyse
- Mise a jour compteur sessions

## Energy Checkpoints

Points de controle automatiques pour gerer la fatigue cognitive.

**Triggers automatiques**:
- EMS atteint 50 (mi-parcours)
- EMS atteint 75 (pres de la fin)
- Iteration >= 7 sans commande (session longue)
- Phase change (Divergent -> Convergent)
- EMS stagne (delta < 3 sur 2 iterations)

**Actions proposees**: continuer, pause (save), accelerer (converge), pivoter.

Forcer manuellement: commande `energy`

## Skill Reference

Pour les details complets (EMS system, personas, techniques, formats):
- Skill: `brainstormer` (`src/skills/core/brainstormer/SKILL.md`)

## Output

| Fichier | Description |
|---------|-------------|
| `./docs/briefs/[slug]/brief-[slug]-[date].md` | Brief fonctionnel EPCI-ready |
| `./docs/briefs/[slug]/journal-[slug]-[date].md` | Journal d'exploration |

## Integration EPCI

1. Lancer `/brief` avec le contenu du brief
2. L'exploration ciblee identifie les fichiers exacts
3. Le brief et journal servent de documentation

## Skills Charges

- `brainstormer` — Logique metier principale
- `project-memory` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
