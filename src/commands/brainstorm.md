---
description: >-
  Transformer une idee vague en brief fonctionnel via brainstorming structure.
  Phases Divergent/Convergent, scoring EMS v2, personas adaptatifs.
  Breakpoints style /brief, questions via AskUserQuestion (3 max).
  Use when: incertitude technique, idee a clarifier.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--random] [--progressive] [--no-hmw] [--no-security] [--no-technique] [--no-clarify] [--competitive] [--c7] [--seq]"
allowed-tools: [Read, Write, Glob, Grep, Task, WebFetch, WebSearch, AskUserQuestion]
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

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `description` | String | Oui | Description de la feature a explorer |
| `--template` | Enum | Non | Template: `feature`, `problem`, `decision` |
| `--quick` | Flag | Non | Mode rapide (moins d'iterations) |
| `--turbo` | Flag | Non | Mode turbo via @clarifier (Haiku) |
| `--random` | Flag | Non | Technique aleatoire |
| `--progressive` | Flag | Non | Mode progressif |
| `--no-hmw` | Flag | Non | Desactive les questions HMW |
| `--no-security` | Flag | Non | Desactive @security-auditor |
| `--no-technique` | Flag | Non | Desactive auto-suggestion techniques |
| `--no-clarify` | Flag | Non | Desactive clarification initiale |
| `--competitive` | Flag | Non | Active analyse concurrentielle |
| `--c7` | Flag | Non | Active Context7 MCP |
| `--seq` | Flag | Non | Active Sequential MCP |

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

**Skill**: `input-clarifier`, `breakpoint-display`

Clarify initial description if confusing (dictated input with hesitations, fillers, etc.).

**Important**: Only applies to **initial input**, NOT to iteration responses during Phase 2.

```
IF --no-clarify flag:
   → Skip to Phase 1

ELSE:
   → Calculate clarity score on initial description
   → IF score < 0.6: Show reformulation breakpoint
   → IF score >= 0.6: Continue to Phase 1
```

**Breakpoint (si clarification requise):**
```yaml
@skill:breakpoint-display
  type: validation
  title: "CLARIFICATION INPUT"
  data:
    original: "{input_brut}"
    modified: true
    detection_info:
      clarity_score: {score}
      artefacts: ["euh", "genre", "tu vois"]
    modified_content:
      reformulated: "{input_clarifie}"
  ask:
    question: "La reformulation vous convient-elle ?"
    header: "⚠️ Clarify"
    options:
      - {label: "✅ Utiliser (Recommended)", description: "Version clarifiée"}
      - {label: "✏️ Modifier", description: "Éditer la reformulation"}
      - {label: "➡️ Garder original", description: "Utiliser tel quel"}
```

---

### Phase 1 — Initialisation

1. **Charger contexte** — Skill: `project-memory`
2. **Reformuler besoin** — Detecter template (feature/problem/decision)
3. **Analyser codebase** — `@Explore` avec `run_in_background: true`
4. **Initialiser session** — Phase: Divergent, Persona: Architecte, EMS: ~25
5. **SYNC @Explore** — Attendre completion si non termine
6. **Generer HMW** (si pas `--no-hmw`) — 3 questions "How Might We" **avec contexte codebase**
7. **Afficher status breakpoint:**
   ```yaml
   @skill:breakpoint-display
     type: ems-status
     title: "PHASE 1 — INITIALISATION"
     data:
       phase: "DIVERGENT"
       persona: "Architecte"
       iteration: 0
       ems:
         score: 25
         delta: null
         axes: {clarity: 30, depth: 20, coverage: 20, decisions: 25, actionability: 30}
         weak_axes: ["depth", "coverage", "decisions"]
         progression: ["Init(25)"]
       done: ["Contexte chargé", "@Explore terminé", "HMW générées"]
       open: ["Questions de cadrage"]
       commands: ["continue"]
   ```
8. **Questions de cadrage** (breakpoint AskUserQuestion):
   ```yaml
   @skill:breakpoint-display
     type: analysis
     title: "QUESTIONS CADRAGE"
     data:
       context:
         phase: "DIVERGENT"
         iteration: 0
         ems: 25
       questions:
         - {tag: "🛑", text: "Quelle cible principale ?", suggestion: "{basé sur @Explore}"}
         - {tag: "⚠️", text: "Contraintes techniques ?", suggestion: "{basé sur stack}"}
         - {tag: "ℹ️", text: "Délai souhaité ?", suggestion: "Non spécifié"}
     ask:
       question: "Répondez aux questions de cadrage"
       header: "📋 Cadrage"
       options:
         - {label: "Répondre (Recommended)", description: "Répondre une par une"}
         - {label: "Valider suggestions", description: "Accepter suggestions IA"}
         - {label: "Skip", description: "Passer directement aux itérations"}
   ```

> **Note v4.8**: HMW generes APRES @Explore pour questions contextuelles basees sur le codebase.
> **Note v4.9**: Input clarification en Step 0 ne s'applique qu'a l'input initial, pas aux iterations.
> **Note v5.3**: Breakpoints via @skill:breakpoint-display pour cohérence et économie tokens.

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
      a) Invoquer @technique-advisor (haiku)
      b) Afficher breakpoint suggestion
   ```

   **Breakpoint technique unique:**
   ```yaml
   @skill:breakpoint-display
     type: validation
     title: "TECHNIQUE SUGGÉRÉE"
     data:
       original: null
       modified: false
       detection_info:
         weak_axes: ["Couverture"]
         technique: "Six Hats"
         category: "creative"
         reason: "Axe Couverture à 35% — exploration angles multiples"
     ask:
       question: "Appliquer cette technique ?"
       header: "💡 Technique"
       options:
         - {label: "Appliquer (Recommended)", description: "Utiliser Six Hats"}
         - {label: "Autre technique", description: "Choisir une autre"}
         - {label: "Ignorer", description: "Continuer sans technique"}
   ```

   **Breakpoint technique mix (2+ axes faibles):**
   ```yaml
   @skill:breakpoint-display
     type: validation
     title: "TECHNIQUES SUGGÉRÉES"
     data:
       original: null
       modified: false
       detection_info:
         weak_axes: ["Couverture", "Actionnabilité"]
         techniques: ["Six Hats", "Pre-mortem"]
         reason: "2 axes faibles nécessitent techniques complémentaires"
     ask:
       question: "Quelles techniques appliquer ?"
       header: "💡 Mix"
       options:
         - {label: "Six Hats (Recommended)", description: "→ Couverture (35%)"}
         - {label: "Pre-mortem", description: "→ Actionnabilité (42%)"}
         - {label: "Les deux", description: "Appliquer en séquence"}
         - {label: "Ignorer", description: "Continuer sans technique"}
   ```

   **SKIP uniquement si:**
   - `--no-technique` flag actif
   - Technique appliquée dans les 2 dernières iterations
   - EMS >= 70 (proche finish)

4. **Afficher breakpoint status** (via skill):
   ```yaml
   @skill:breakpoint-display
     type: ems-status
     title: "BRAINSTORM STATUS"
     data:
       phase: "{DIVERGENT|CONVERGENT}"
       persona: "{Architecte|Sparring|Pragmatique}"
       iteration: {N}
       ems:
         score: {EMS}
         delta: "{+N}"
         axes: {clarity: X, depth: X, coverage: X, decisions: X, actionability: X}
         weak_axes: ["{axes < 50}"]
         progression: ["Init(22)", "Iter1(38)", ..., "Current({EMS})"]
       done: ["{éléments validés}"]
       open: ["{points restants}"]
       commands: ["continue", "dive", "back", "save", "energy", "finish"]
   ```
5. **Transition check** (si EMS = 50 et Divergent):
   ```yaml
   @skill:breakpoint-display
     type: plan-review
     title: "PHASE TRANSITION"
     data:
       metrics:
         ems_score: 50
         ems_delta: "{delta}"
         milestone: "Mi-parcours atteint"
       preview_next_phase:
         phase_name: "CONVERGENT"
         description: "Passage de l'exploration à la convergence"
     ask:
       question: "Mi-parcours EMS 50. Quelle direction prendre ?"
       header: "🔄 Transition"
       options:
         - {label: "Continuer Divergent", description: "Explorer plus d'options"}
         - {label: "Passer Convergent (Recommended)", description: "Commencer à converger"}
         - {label: "Appliquer technique", description: "Utiliser technique pour débloquer"}
   ```
6. **Finalization checkpoint** (si EMS >= 70):
   ```yaml
   @skill:breakpoint-display
     type: plan-review
     title: "FINALIZATION CHECKPOINT"
     data:
       metrics:
         ems_score: {EMS}
         ems_delta: "{delta}"
         axes: {clarity: X, depth: X, coverage: X, decisions: X, actionability: X}
         weak_axes: []
       progression: "Init(22) → Iter1(38) → ... → Final({EMS})"
       preview_next_phase:
         phase_name: "Phase 3: Generation"
         tasks:
           - {title: "Générer brief PRD v3.0", time: "auto"}
           - {title: "Créer journal exploration", time: "auto"}
         message: "Le brief est suffisamment mature pour être finalisé."
     ask:
       question: "Brief EMS {EMS}/100 prêt. Quelle action ?"
       header: "🎯 Checkpoint"
       options:
         - {label: "Continuer", description: "Plus d'itérations pour affiner"}
         - {label: "Preview (Recommended)", description: "@planner sans finaliser"}
         - {label: "Finaliser", description: "Générer brief + journal maintenant"}
   ```
   - **Comportement**: Continuer → questions, Preview → @planner puis redemande, Finaliser → Phase 3
   - **CRITICAL**: Checkpoint BLOQUANT. Attendre réponse explicite.
7. **Générer questions** (si choix Continuer):
   ```yaml
   @skill:breakpoint-display
     type: analysis
     title: "QUESTIONS ITÉRATION"
     data:
       context:
         phase: "{PHASE}"
         iteration: {N}
         ems: {EMS}
       questions:
         - {tag: "🛑", text: "{question critique}", suggestion: "{suggestion}"}
         - {tag: "⚠️", text: "{question importante}", suggestion: "{suggestion}"}
         - {tag: "ℹ️", text: "{question info}", suggestion: "{suggestion}"}
     ask:
       question: "Répondez aux questions pour affiner le brief"
       header: "📋 Questions"
       options:
         - {label: "Répondre (Recommended)", description: "Répondre une par une"}
         - {label: "Valider suggestions", description: "Accepter suggestions IA"}
         - {label: "Finish", description: "Finaliser maintenant"}
   ```
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

See @references/brainstorm/completion-summary.md for full format.

**Quick reference:**
- TINY (≤2j) → `/brief` → `/quick --autonomous`
- SMALL/STANDARD (3-5j) → `/brief` or `/decompose`
- LARGE (>5j) → `/decompose` → `/orchestrate`

---

## Commands

See @references/brainstorm/commands.md for full reference.

**Quick reference:** `continue`, `dive`, `pivot`, `status`, `finish`, `party`, `panel`

## Flags

See @references/brainstorm/flags.md for full reference.

**Quick reference:** `--quick`, `--turbo`, `--no-hmw`, `--competitive`, `--party`, `--panel`

## References

| Topic | Reference |
|-------|-----------|
| Commands | @references/brainstorm/commands.md |
| Flags | @references/brainstorm/flags.md |
| Completion summary | @references/brainstorm/completion-summary.md |
| Turbo mode | @references/brainstorm/turbo-mode.md |
| Random mode | @references/brainstorm/random-mode.md |
| Progressive mode | @references/brainstorm/progressive-mode.md |
| Spike process | @references/brainstorm/spike-process.md |
| Session commands | @references/brainstorm/session-commands.md |
| Energy checkpoints | @references/brainstorm/energy-checkpoints.md |

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

## Error Handling

| Error | Recovery |
|-------|----------|
| @Explore timeout | Continue avec contexte partiel, marquer exploration incomplete |
| @ems-evaluator echec | Utiliser estimation manuelle, continuer iterations |
| @technique-advisor indisponible | Proposer technique par defaut (Six Hats) |
| Session file corrupted | Archiver et demarrer nouvelle session |
| EMS stagnation (delta < 3 sur 3 iterations) | Proposer pivot ou changement technique |

## Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max iterations | 10 | Eviter sessions trop longues |
| EMS minimum pour finaliser | 70 | Garantir qualite brief |
| Questions par iteration | 3 max | Eviter surcharge cognitive |
| Techniques par session | 5 max | Focus sur convergence |
| Session timeout | 2h | Preservation contexte |

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

## See Also

| Command | Relation |
|---------|----------|
| `/brief` | Utilise le brief genere par /brainstorm |
| `/epci` | Workflow complet apres brief valide |
| `/quick` | Workflow rapide pour TINY/SMALL |
| `/decompose` | Pour projets LARGE (>5 jours) |
| `/debug` | Si besoin diagnostic technique |

## Skills Charges

- `brainstormer` — Logique metier principale
- `breakpoint-display` — Affichage breakpoints interactifs (v5.3)
- `project-memory` — Contexte projet
- `architecture-patterns` — Suggestions architecture
- `clarification-intelligente` — Systeme de questions
