---
description: >-
  Brainstorming guide v4.8.1 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  Auto-selection techniques basee sur axes faibles, mix de techniques.
  Finalization Checkpoint obligatoire a EMS >= 85 (bloquant).
  Session persistence, energy checkpoints, 3-5 questions avec A/B/C.
  Use when: idee vague a transformer en specs, incertitude technique.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--random] [--progressive] [--no-hmw] [--no-security] [--no-technique] [--no-clarify] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v4.8.1

## Overview

Transforme une idee vague en brief fonctionnel complet, pret pour EPCI.
Utilise l'analyse du codebase, des personas adaptatifs et des questions
iteratives pour construire des specifications exhaustives.

**Nouveautes v4.8.1**:
- **Finalization Checkpoint** obligatoire a EMS >= 85 (bloquant)
- Pas de finalisation automatique — toujours choix explicite

**Nouveautes v4.8**:
- Auto-selection de techniques basee sur axes EMS faibles (< 50)
- Mix de techniques quand 2+ axes faibles
- Transition check explicite Divergent → Convergent
- Preview @planner/@security en phase Convergent
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
7. **Questions de cadrage** — 3-5 max avec suggestions
8. **Afficher breakpoint**

> **Note v4.8**: HMW generes APRES @Explore pour questions contextuelles basees sur le codebase.
> **Note v4.9**: Input clarification en Step 0 ne s'applique qu'a l'input initial, pas aux iterations.

### Phase 2 — Iterations

Boucle jusqu'a `finish`:

1. **Integrer reponses** utilisateur
2. **Recalculer EMS** via `@ems-evaluator`
   - Output: scores, delta, `weak_axes[]` (axes < 50)
3. **Auto-selection technique** (v4.8+):
   - Si `weak_axes` non vide ET technique pas dans les 2 dernieres iterations:
     - Invoquer `@technique-advisor` mode auto-select
     - Proposer: `💡 Technique suggérée: [X] → Appliquer? [Y/n]`
   - Si 2+ axes faibles: proposer mix de techniques
   - Desactiver avec `--no-technique`
4. **Transition check** (si EMS = 50 et Divergent):
   ```
   PHASE TRANSITION | EMS: 50/100
   [1] Continuer Divergent  [2] Passer Convergent  [3] Technique
   ```
5. **Finalization checkpoint** (si EMS >= 85):
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   FINALIZATION CHECKPOINT | EMS: XX/100
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Le brief est suffisamment mature pour être finalisé.

   [1] Continuer (plus d'itérations)
   [2] Preview plan (@planner) sans finaliser
   [3] Finaliser maintenant (finish)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```
   **IMPORTANT**: Ne JAMAIS finaliser automatiquement. Toujours attendre le choix explicite.
6. **Generer 3-5 questions** avec suggestions A/B/C (si choix [1])
7. **Afficher breakpoint compact**
8. **Preview check** (si Convergent et EMS >= 65 et choix [2]):
   - Proposer `@planner preview? [Y/n]`
   - Si patterns auth: `@security-auditor preview? [Y/n]`

**NEVER skip EMS calculation — core metric of progress.**

### Phase 3 — Generation

**MANDATORY: Use Write tool to create BOTH files using official templates.**

**Templates obligatoires** (dans `src/skills/core/brainstormer/references/`):
- `brief-format.md` — Structure Brief v2.0 avec Personas, User Stories, Success Metrics
- Section Journal d'Exploration dans le meme fichier

1. **@planner** (si pas preview fait OU EMS >= 85)
2. **@security-auditor** (si patterns auth ET pas preview)
3. Create directory: `mkdir -p ./docs/briefs/[slug]`
4. **Lire template**: `Read src/skills/core/brainstormer/references/brief-format.md`
5. **Section-by-section validation** (si pas --quick/--turbo)
6. Write `brief-[slug]-[date].md` — **DOIT suivre la structure du template**
7. Write `journal-[slug]-[date].md` — **DOIT suivre le Template Journal d'Exploration**
8. **HOOK: post-brainstorm** — Invocation automatique (voir section Hooks)
9. Display completion summary avec techniques utilisees

**Sections OBLIGATOIRES dans le brief** (v2.0):
- Personas (minimum 1 primaire)
- User Stories format "En tant que... je veux... afin de" avec AC Given/When/Then
- Success Metrics (KPIs ou "TBD")

**Anti-pattern**: Generer un brief sans lire `brief-format.md` d'abord.

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
