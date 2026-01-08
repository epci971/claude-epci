---
description: >-
  Brainstorming guide v4.3 pour decouvrir et specifier une feature.
  Personas adaptatifs, phases Divergent/Convergent, scoring EMS v2.
  Session persistence, energy checkpoints, 3-5 questions avec A/B/C.
  Use when: idee vague a transformer en specs, incertitude technique.
argument-hint: "[description] [--template feature|problem|decision] [--quick] [--turbo] [--random] [--progressive] [--no-hmw] [--no-security] [--c7] [--seq]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch]
---

# /brainstorm — Feature Discovery v4.3

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

### Phase 1 — Initialisation

1. **Charger contexte** — Skill: `project-memory`
2. **Analyser codebase** — `@Explore` avec `run_in_background: true`
3. **Reformuler besoin** — Detecter template (feature/problem/decision)
4. **Initialiser session** — Phase: Divergent, Persona: Architecte, EMS: ~25
5. **Generer HMW** (si pas `--no-hmw`) — 3 questions "How Might We"
6. **Questions de cadrage** — 3-5 max avec suggestions
7. **Afficher breakpoint**

### Phase 2 — Iterations

Boucle jusqu'a `finish`:

1. **Integrer reponses** utilisateur
2. **Recalculer EMS** via `@ems-evaluator` (5 axes, voir skill brainstormer)
3. **Appliquer techniques** si pertinent via `@technique-advisor`
4. **Generer 3-5 questions** avec suggestions A/B/C
5. **Afficher breakpoint compact**

**NEVER skip EMS calculation — core metric of progress.**

### Phase 3 — Generation

**MANDATORY: Use Write tool to create BOTH files.**

1. Create directory: `mkdir -p ./docs/briefs/[slug]`
2. **Section-by-section validation** (si pas --quick/--turbo)
3. Write `brief-[slug]-[date].md`
4. Write `journal-[slug]-[date].md`
5. Display completion summary

## Commands

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

## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Desactiver HMW |
| `--quick` | 3 iter max, skip validation |
| `--turbo` | Mode turbo (voir reference) |
| `--random` | Selection aleatoire techniques (voir reference) |
| `--progressive` | Mode 3 phases (voir reference) |
| `--no-security` | Desactiver @security-auditor auto |
| `--no-plan` | Desactiver @planner auto |

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

| Agent | Model | Role |
|-------|-------|------|
| `@Explore` | - | Analyse codebase |
| `@clarifier` | haiku | Questions turbo mode |
| `@planner` | sonnet | Plan convergent |
| `@security-auditor` | opus | Audit securite |
| `@ems-evaluator` | haiku | Calcul EMS 5 axes |
| `@technique-advisor` | haiku | Selection techniques |

**@planner auto-invocation**: En phase Convergent OU quand EMS >= 70

**@security-auditor auto-detection**: Si patterns auth/security/payment/api detectes

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
