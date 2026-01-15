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
   - **CRITICAL: Utiliser UNIQUEMENT les 5 axes officiels** :
     - Clarté, Profondeur, Couverture, Décisions, Actionnabilité
     - Ne JAMAIS inventer d'axes (ex: "Risques" n'est PAS un axe)
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
3. **MANDATORY — Auto-technique check** (si pas `--no-technique`):
   ```
   IF weak_axes[] non vide
      AND technique pas appliquée dans les 2 dernières iterations:
   THEN:
      a) Invoquer @technique-advisor (haiku) avec:
         - weak_axes, phase, techniques_used[-2:]
      b) Recevoir JSON: {mode, suggested_technique(s), reason}
      c) Afficher suggestion via AskUserQuestion:
         - Header: "💡 Technique" ou "💡 Mix"
         - Options: Appliquer (Recommended), Autre, Ignorer
   ```

   **Trace attendue:**
   ```
   [EMS: 45] weak_axes: ["Couverture", "Actionnabilité"]
   → @technique-advisor invoqué (mode: mix)
   → Suggestion: "Six Hats" + "Pre-mortem"
   → AskUserQuestion affiché avec options
   ```

   **SKIP uniquement si:**
   - `--no-technique` flag actif
   - Technique appliquée dans les 2 dernières iterations
   - EMS >= 70 (proche finish)

4. **Afficher breakpoint** (v5.2 — boîte ASCII avec EMS détaillé):
   - Voir format détaillé dans `src/skills/core/brainstormer/SKILL.md` section "Breakpoint Format"
   - Utiliser output compact JSON de `@ems-evaluator` pour les barres de progression
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

### Project Estimation & Completion Summary

See [completion-summary.md](references/brainstorm/completion-summary.md) for full format.

**Quick reference:**
- TINY (≤2j) → `/brief` → `/quick --autonomous`
- SMALL/STANDARD (3-5j) → `/brief` or `/decompose`
- LARGE (>5j) → `/decompose` → `/orchestrate`

---

## Commands

See [commands.md](references/brainstorm/commands.md) for full reference.

**Quick reference:** `continue`, `dive`, `pivot`, `status`, `finish`, `party`, `panel`

## Flags

See [flags.md](references/brainstorm/flags.md) for full reference.

**Quick reference:** `--quick`, `--turbo`, `--no-hmw`, `--competitive`, `--party`, `--panel`

## References

| Topic | Reference |
|-------|-----------|
| Commands | [commands.md](references/brainstorm/commands.md) |
| Flags | [flags.md](references/brainstorm/flags.md) |
| Completion summary | [completion-summary.md](references/brainstorm/completion-summary.md) |
| Turbo mode | [turbo-mode.md](references/brainstorm/turbo-mode.md) |
| Random mode | [random-mode.md](references/brainstorm/random-mode.md) |
| Progressive mode | [progressive-mode.md](references/brainstorm/progressive-mode.md) |
| Spike process | [spike-process.md](references/brainstorm/spike-process.md) |
| Session commands | [session-commands.md](references/brainstorm/session-commands.md) |
| Energy checkpoints | [energy-checkpoints.md](references/brainstorm/energy-checkpoints.md) |

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
