---
name: brainstormer
description: >-
  Feature discovery et brainstorming guide pour EPCI v4.7. Workflow avec
  personas adaptatifs (Architecte, Sparring, Pragmatique), phases Divergent/
  Convergent, scoring EMS v2 via @ems-evaluator, auto-techniques via @technique-advisor.
  Use when: /brainstorm invoked, feature discovery needed.
  Not for: implementation tasks, code generation, simple questions.
allowed-tools: [Read, Write, Glob, Grep, Task]
---

# Brainstormer v4.7

## Overview

Skill de brainstorming specialise pour la decouverte de features.
Transforme des idees vagues en briefs fonctionnels complets via
un processus iteratif guide avec personas adaptatifs.

**Reference Documents:**
- [Personas](references/personas.md) — 3 modes de facilitation
- [EMS System](references/ems-system.md) — Scoring v2 avec 5 axes
- [Frameworks](references/frameworks.md) — 5 frameworks d'analyse
- [Techniques](references/techniques/) — 20 techniques (4 categories)
- [Brief Format](references/brief-format.md) — Template de sortie
- [Session Format](references/session-format.md) — Format YAML persistence

**Session Storage:** `.project-memory/brainstorm-sessions/[slug].yaml`

## Personas

| Persona | Role |
|---------|------|
| **Architecte** | Structure, frameworks, synthese (DEFAUT) |
| **Sparring** | Challenge, stress-test |
| **Pragmatique** | Action, deblocage |

> Voir [personas.md](references/personas.md) pour regles de bascule

## Phases

| Phase | Focus |
|-------|-------|
| **Divergent** | Generer, explorer, quantite |
| **Convergent** | Evaluer, decider, qualite |

**Transition auto**: Couverture >= 60% ET iter >= 3

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `@Explore` | - | Analyse codebase initiale |
| `@clarifier` | haiku | Questions turbo mode |
| `@planner` | sonnet | Plan en phase Convergent |
| `@security-auditor` | opus | Audit securite conditionnel |
| `@ems-evaluator` | haiku | Calcul EMS 5 axes (v4.3) |
| `@technique-advisor` | haiku | Selection techniques (v4.3) |

## EMS Calculation (via @ems-evaluator)

**MANDATORY: Invoke @ems-evaluator at each iteration.**

Axes (weights):
- Clarte (25%) — Precision du besoin
- Profondeur (20%) — Niveau de detail
- Couverture (20%) — Exhaustivite
- Decisions (20%) — Choix actes
- Actionnabilite (15%) — Pret pour action

**Invocation:**
```
Task tool -> @ems-evaluator (haiku)
Input: current brief state, previous EMS, open questions
Output: 5-axis scores, composite, delta, weak_axes, recommendations
```

**Output includes (v4.7+):**
- `weak_axes[]` — Liste des axes avec score < 50
- Trigger auto-technique si `weak_axes` non vide

**Thresholds:**

| EMS Range | Recommendation | Technique Trigger |
|-----------|----------------|-------------------|
| 0-49 | CONTINUE | Si axe < 50 → SUGGEST_TECHNIQUE |
| 50-69 | SUGGEST_CONVERGE | Si axe < 50 → SUGGEST_TECHNIQUE |
| 70-84 | SUGGEST_FINISH | Non (proche finish) |
| 85-100 | FINISH | Non |

## Technique Selection (via @technique-advisor)

### Auto-Invocation (v4.7+)

**Declenchement automatique** a chaque iteration si:
1. Au moins un axe EMS < 50 (retourne par `@ems-evaluator` dans `weak_axes`)
2. Technique correspondante pas utilisee dans les 2 dernieres iterations
3. Pas en mode `--no-technique`

**Invocation manuelle:**
- `technique [name]` — Applique technique specifique
- `--random` flag — Selection aleatoire

### Mapping EMS → Technique

| Axe Faible | Technique Primaire | Techniques Secondaires |
|------------|-------------------|------------------------|
| Clarte < 50 | question-storming | 5whys, first-principles |
| Profondeur < 50 | first-principles | 5whys, dive |
| Couverture < 50 | six-hats | scamper, what-if |
| Decisions < 50 | moscow | scoring, swot |
| Actionnabilite < 50 | premortem | constraint-mapping |

### Mix de Techniques

Quand 2+ axes sont faibles:
- Combiner 1 technique par axe faible (max 2)
- Privilegier techniques complementaires (Divergent + Convergent)
- Eviter 2 techniques de meme categorie
- Ordre: Divergent d'abord, puis Convergent

### Format Proposition

**Technique unique:**
```
💡 Technique suggérée: [NOM] ([CATEGORIE])
   Raison: Axe [X] à [Y]% — [effet attendu]

→ Appliquer? [Y/n/autre]
```

**Mix (2+ axes faibles):**
```
💡 TECHNIQUES SUGGÉRÉES | Iteration [N]

Axes faibles: [Axis1] ([X]%), [Axis2] ([Y]%)

[1] [Technique1] → [Axis1]
[2] [Technique2] → [Axis2]

→ [1] / [2] / [b]oth / [n]one
```

### Session Tracking

Ajouter dans session YAML (`techniques_history`):
```yaml
techniques_history:
  - iteration: 3
    suggested: ["six-hats", "moscow"]
    applied: ["six-hats"]
    reason: "Couverture 35%, Decisions 42%"
```

### Invocation Agent

```
Task tool -> @technique-advisor (haiku)
Input: phase, weak_axes, techniques_used
Output: selected technique(s), adapted questions
```

## Question Format

3-5 questions par iteration avec choix A/B/C:

```
1. [Question 1]
   A) Option A  B) Option B  C) Option C
   -> Suggestion: B

2. [Question 2]
   A) Option A  B) Option B  C) Option C
```

## Breakpoint Format

```
-------------------------------------------------------
[PHASE] | [PERSONA] | Iter X | EMS: XX/100 (+Y)
-------------------------------------------------------
Done: [elements valides]
Open: [points a clarifier]

Questions:
1. [Question] -> Suggestion: [si applicable]
2. [Question]
3. [Question]

-> continue | dive [topic] | back | save | energy | finish
-------------------------------------------------------
```

## @planner Integration

**Auto-invocation:** Phase Convergent OU EMS >= 70

**Confirmation:** `Lancer @planner? [Y/n]`

Invoke via Task tool (model: sonnet).
Output integre dans brief section "Preliminary Plan".

## @security-auditor Integration

**Auto-detection:** Patterns auth/security/payment/api

**Confirmation:** `Lancer @security-auditor? [Y/n]`

Invoke via Task tool (model: opus).
Output integre dans brief section "Security Considerations".

## Phase 3 — Generation

**MANDATORY: Use Write tool for BOTH files.**

1. Create directory: `mkdir -p ./docs/briefs/[slug]`
2. Section-by-section validation (si pas --quick/--turbo)
3. Write `brief-[slug]-[date].md`
4. Write `journal-[slug]-[date].md`
5. Display completion summary

**Completion format:**
```
-------------------------------------------------------
BRAINSTORM COMPLETE
-------------------------------------------------------
EMS Final: XX/100
Agents: [@planner | @security-auditor | Aucun]

Fichiers generes:
   - Brief: ./docs/briefs/[slug]/brief-[slug]-[date].md
   - Journal: ./docs/briefs/[slug]/journal-[slug]-[date].md

Prochaine etape: Lancer /brief avec le contenu du brief.
-------------------------------------------------------
```

## Framework Detection

| Signal | Framework |
|--------|-----------|
| Priorisation | MoSCoW |
| "Pourquoi" repete | 5 Whys |
| Plusieurs options | SWOT |
| Criteres multiples | Scoring |
| Risques | Pre-mortem |

## Anti-patterns

**Ne pas faire:**
- Plus de 5 questions par iteration
- Breakpoint > 15 lignes
- Ignorer contexte codebase
- `finish` avant EMS 60

**Toujours faire:**
- Invoquer @ems-evaluator a chaque iteration
- Proposer suggestions avec questions
- Respecter format compact CLI
