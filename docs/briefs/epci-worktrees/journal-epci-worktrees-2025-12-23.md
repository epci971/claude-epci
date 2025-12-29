# Journal d'Exploration — EPCI Worktrees Integration

> **Feature**: EPCI Worktrees Integration
> **Date**: 2025-12-23
> **Iterations**: 6

---

## Resume

Exploration complete pour integrer git worktrees dans le workflow EPCI. La solution permet d'isoler chaque workflow STANDARD/LARGE dans un espace de travail dedie, avec creation automatique, setup de l'environnement, et cleanup assiste. Architecture validee via pre-mortem avec 3 mitigations critiques identifiees.

## Progression EMS

| Iteration | Score | Delta | Phase | Focus |
|-----------|-------|-------|-------|-------|
| Init | 25 | - | 🔀 Divergent | Cadrage initial, HMW |
| 1 | 25 | +0 | 🔀 Divergent | Questions fondamentales (scope, trigger, naming) |
| 2 | 42 | +17 | 🔀 Divergent | Architecture (Feature Doc, branch, hooks) |
| 3 | 58 | +16 | 🔀 Divergent | Specifications (config schema, detection, UX) |
| 4 | 72 | +14 | 🎯 Convergent | Edge cases, scope fichiers |
| 5 | 78 | +6 | 🎯 Convergent | Pre-mortem (3 risques majeurs) |
| 6 | 85 | +7 | 🎯 Convergent | Consolidation finale |

## Decisions Cles

### Decision 1 — Scope d'isolation
- **Contexte**: A quel niveau creer le worktree?
- **Options considerees**: Par workflow complet, par phase, a la demande
- **Choix**: Workflow complet (/epci-brief → Phase 3)
- **Justification**: Isolation maximale, coherence du contexte

### Decision 2 — Trigger
- **Contexte**: Automatique ou explicite?
- **Options considerees**: Auto pour tout, flag --worktree, configurable
- **Choix**: Configurable dans settings.json, defaut OFF
- **Justification**: Opt-in pour eviter surprises, flexibilite par projet

### Decision 3 — Naming convention
- **Contexte**: Comment nommer les repertoires worktree?
- **Options considerees**: epci-<slug>, <project>-<branch>, .worktrees/<slug>
- **Choix**: `../<project>-<branch>` (pattern officiel Claude Code)
- **Justification**: Compatibilite avec documentation officielle

### Decision 4 — Feature Document location
- **Contexte**: Ou stocker le Feature Document?
- **Options considerees**: Worktree, repo principal, les deux
- **Choix**: Repo principal uniquement
- **Justification**: Tracabilite immediate, pas de merge complexe

### Decision 5 — Cleanup lifecycle
- **Contexte**: Quand supprimer le worktree?
- **Options considerees**: Auto apres commit, manuel, semi-auto
- **Choix**: Semi-auto avec proposition au breakpoint final
- **Justification**: Choix eclaire de l'utilisateur, pas de suppression forcee

### Decision 6 — Error handling
- **Contexte**: Si creation worktree echoue?
- **Options considerees**: Abort, fallback, confirmation
- **Choix**: Fallback gracieux sur repo principal
- **Justification**: Worktree = amelioration optionnelle, pas bloquant

### Decision 7 — Edge case branche existe
- **Contexte**: Que faire si la branche existe deja?
- **Options considerees**: Suffixer, demander, abort
- **Choix**: Demander confirmation pour reutilisation
- **Justification**: L'utilisateur sait peut-etre pourquoi elle existe

### Decision 8 — Scope implementation
- **Contexte**: Quels fichiers creer/modifier?
- **Options considerees**: Skill seul, skill + commands, complet
- **Choix**: Complet (skill + commands + settings + cleanup command)
- **Justification**: Integration coherente dans tout le workflow

## Pre-mortem

### Exercice — Iteration 5

**Projection**: Mars 2026, l'integration worktrees a echoue.

**Causes identifiees (Score >= 6)**:

| Cause | Proba | Impact | Score | Mitigation |
|-------|-------|--------|-------|------------|
| Worktrees orphelins | 🔴 3 | 🟡 2 | 6 | /epci:cleanup + reminder 7j |
| Setup echoue silencieusement | 🟡 2 | 🔴 3 | 6 | Timeout + logs + fallback |
| Confusion chemins | 🟡 2 | 🔴 3 | 6 | Contexte dans breakpoints |

**Signaux d'alerte definis**:
- Plus de 3 worktrees actifs → notification
- Desync JSON/git → auto-reconciliation
- Setup > 60s → proposer skip
- Meme slug 2x/24h → confirmation

## Frameworks Appliques

### Pre-mortem — Iteration 5
- **Declencheur**: Commande utilisateur `premortem`
- **Persona active**: 🥊 Sparring
- **Resultat**: 7 causes identifiees, 3 mitigations critiques, 4 signaux d'alerte
- **Impact**: +6 points EMS (72→78), mitigations integrees au brief

## Questions Resolues

| Question | Reponse | Iteration |
|----------|---------|-----------|
| Scope d'isolation? | Workflow complet | 1 |
| Trigger auto ou explicite? | Configurable (defaut OFF) | 1 |
| Naming convention? | ../<project>-<branch> | 1 |
| Cleanup lifecycle? | Semi-auto en Phase 3 | 1 |
| Setup automatique? | Auto-detection package manager | 1 |
| Feature Doc location? | Repo principal | 2 |
| Branch naming? | feature/<slug> | 2 |
| Hook integration? | Dans epci-brief (pas hook) | 2 |
| Error handling? | Fallback gracieux | 2 |
| Tracking? | JSON + git worktree list | 2 |
| Config schema? | { enabled, autoSetup, cleanupPrompt } | 3 |
| Package detection? | Conventions override, sinon auto | 3 |
| Cleanup UX? | Resume + 3 options | 3 |
| --continue handling? | Auto-detect transparent | 3 |
| Tests au setup? | Optionnel (defaut OFF) | 3 |
| Branche existe? | Demander confirmation | 4 |
| Worktree dir existe? | Reutiliser si meme branche | 4 |
| Scope fichiers? | Complet (6 fichiers) | 4 |
| Cleanup dans hook? | Non, dans /epci Phase 3 | 4 |

## Personas Utilises

| Persona | Iterations | Usage |
|---------|------------|-------|
| 📐 Architecte | 1, 2, 3, 4, 6 | Structure, decisions, consolidation |
| 🥊 Sparring | 5 | Pre-mortem, stress-test |

## Biais Detectes

Aucun biais majeur detecte durant l'exploration.

---

*Journal genere automatiquement par Brainstormer v3.0*
