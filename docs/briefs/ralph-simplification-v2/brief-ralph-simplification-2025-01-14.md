# PRD-2025-001 — Ralph Wiggum Simplification v2

> **Version** : 1.0 | **Status** : Draft | **Date** : 2025-01-14

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-14 | Brainstorm Session | Initial PRD |

---

## Executive Summary

### TL;DR

Simplifier radicalement le système Ralph Wiggum en supprimant les commandes `/ralph` et `/cancel-ralph`, et en créant une unique commande `/ralph-exec` qui implémente le workflow EPCT (Explore, Plan, Code, Test) inline, sans routing vers `/brief` ou `/epci`.

### Problem

Le système Ralph actuel est trop complexe :
- Route vers `/brief` → `/quick` ou `/epci` (lourdeur inutile)
- Deux modes (Hook/Script) difficiles à maintenir
- Ne libère pas le contexte entre les itérations
- 45+ user stories pour une intégration qui devrait être simple

### Solution

Architecture ultra-simplifiée :
1. `/decompose` génère tous les fichiers (prd.json, ralph.sh, progress.txt)
2. L'utilisateur lance `./ralph.sh` directement dans le terminal
3. `ralph.sh` appelle `claude "/ralph-exec --prd ./prd.json"` pour chaque story
4. Chaque appel = contexte frais = libération mémoire

### Impact

- **Réduction complexité** : 2 commandes supprimées, 1 agent supprimé
- **Libération contexte** : Contexte frais à chaque story
- **Maintenabilité** : Code plus simple, moins de bugs potentiels

---

## Background & Strategic Fit

### Why Now?

- Le système Ralph actuel (v1) n'a jamais été exécuté avec succès (45 stories pending)
- Claude Code 2.1 apporte des fonctionnalités (hot-reload, skills fusion) qui simplifient l'approche
- Besoin d'un système overnight fonctionnel et robuste

### Strategic Alignment

- **Philosophie EPCI** : Simplicité, modularité, traçabilité
- **Pattern Anthropic** : Workflow "Explore, Plan, Code, Commit" recommandé officiellement
- **Libération contexte** : Essentiel pour les sessions longues (overnight)

---

## Problem Statement

### Current Situation

Le système Ralph actuel (`/ralph` + `@ralph-executor`) :

```
/ralph → @ralph-executor → /brief → /quick ou /epci
```

**Problèmes identifiés** :
1. **Routing lourd** : Passe par 3-4 commandes pour exécuter une story
2. **Pas de libération contexte** : Si lancé via `/ralph`, le contexte parent reste ouvert
3. **Mode Hook complexe** : ralph-stop-hook.sh jamais testé en production
4. **45 user stories** : Trop granulaire, impossible à exécuter

### Evidence & Data

- 0/45 stories complétées dans l'intégration actuelle
- PROMPT.md actuel référence `/quick` et `/epci` (lignes 60-61)
- `@ralph-executor` route explicitement vers `/brief` (ligne 82-103)

### Impact

- Impossibilité d'exécuter des sessions overnight
- Temps de développement perdu sur une architecture trop complexe
- Consommation contexte excessive sans libération

---

## Goals

### Business Goals

| Goal | Metric | Target |
|------|--------|--------|
| Réduire la complexité | Nombre de commandes Ralph | 1 (au lieu de 3) |
| Permettre overnight | Stories exécutées par session | 10+ |

### User Goals

| Goal | Metric | Target |
|------|--------|--------|
| Libérer le contexte | Contexte frais par story | 100% |
| Simplifier l'usage | Commandes à connaître | 2 (`/decompose` + `./ralph.sh`) |

### Technical Goals

| Goal | Metric | Target |
|------|--------|--------|
| Workflow EPCT inline | Pas de routing vers /brief /epci | 0 appels |
| Boucle Code-Test | Max tentatives avant échec | 5 |
| Mise à jour prd.json | Champs modifiés automatiquement | 12 champs |

---

## Non-Goals

| Exclusion | Raison |
|-----------|--------|
| Mode Hook | Trop complexe, supprimé |
| `/ralph` comme commande | Inutile, ralph.sh suffit |
| `/cancel-ralph` | Ctrl+C suffit |
| `@ralph-executor` | Remplacé par `/ralph-exec` |
| Routing vers `/brief` ou `/epci` | C'est le problème à résoudre |
| RALPH_STATUS block complexe | Simplifié en promise tag |

---

## Personas

### Primary Persona

**Développeur EPCI overnight**
- Lance des sessions autonomes pendant la nuit
- Veut retrouver le travail fait au réveil
- A besoin que le contexte soit libéré pour éviter les erreurs mémoire

### Secondary Persona

**Mainteneur EPCI**
- Doit comprendre et maintenir le code
- Préfère une architecture simple avec peu de composants

---

## User Stories

### US1 — Créer la commande /ralph-exec

**En tant que** développeur EPCI overnight,
**Je veux** une commande `/ralph-exec` qui exécute UNE story avec le workflow EPCT inline,
**Afin de** avoir un contexte frais à chaque story sans routing vers /brief ou /epci.

**Complexité** : L (5 jours)
**Priority** : Must-have

**Acceptance Criteria** :

```gherkin
AC1: Given prd.json exists
     When /ralph-exec is called without story-id
     Then it parses prd.json and finds story with min(priority) AND status=pending AND passes=false

AC2: Given a story is identified
     When /ralph-exec executes
     Then it follows EPCT phases: Explore → Plan → Code-Test loop → Commit

AC3: Given Code-Test loop runs
     When tests fail
     Then it retries up to max_attempts (default 5) before marking FAILED

AC4: Given story completes successfully
     When tests pass
     Then it updates prd.json (status, passes, files_modified, etc.) AND outputs <promise>STORY_DONE</promise>

AC5: Given story fails after max_attempts
     When marking as failed
     Then it updates prd.json (status=failed, last_error) AND outputs FAILED

AC6: Given a story has unmet dependencies
     When selecting next story
     Then it skips blocked stories and marks them status=blocked
```

---

### US2 — Modifier /decompose pour générer ralph.sh compatible

**En tant que** développeur EPCI,
**Je veux** que `/decompose` génère un `ralph.sh` qui appelle `/ralph-exec`,
**Afin de** avoir une chaîne cohérente sans intervention manuelle.

**Complexité** : M (3 jours)
**Priority** : Must-have

**Acceptance Criteria** :

```gherkin
AC1: Given /decompose is run
     When ralph.sh is generated
     Then it contains: claude "/ralph-exec --prd ./prd.json"

AC2: Given ralph.sh is generated
     When it runs
     Then it loops until all stories pass=true OR max_iterations reached

AC3: Given /decompose generates specs
     When parent_spec and parent_brief are set in prd.json
     Then they point to valid files that /ralph-exec can read for context
```

---

### US3 — Supprimer les commandes obsolètes

**En tant que** mainteneur EPCI,
**Je veux** supprimer `/ralph`, `/cancel-ralph` et `@ralph-executor`,
**Afin de** réduire la complexité et éviter la confusion.

**Complexité** : S (1 jour)
**Priority** : Must-have

**Acceptance Criteria** :

```gherkin
AC1: Given /ralph command exists
     When cleanup is done
     Then src/commands/ralph.md is deleted

AC2: Given /cancel-ralph command exists
     When cleanup is done
     Then src/commands/cancel-ralph.md is deleted

AC3: Given @ralph-executor agent exists
     When cleanup is done
     Then src/agents/ralph-executor.md is deleted

AC4: Given CLAUDE.md references these commands
     When cleanup is done
     Then CLAUDE.md is updated to reference /ralph-exec only
```

---

### US4 — Définir le format progress.txt comme mémoire persistante

**En tant que** développeur EPCI overnight,
**Je veux** que `progress.txt` serve de mémoire entre les itérations,
**Afin de** que Claude puisse voir l'historique des tentatives et erreurs.

**Complexité** : S (1 jour)
**Priority** : Should-have

**Acceptance Criteria** :

```gherkin
AC1: Given /ralph-exec completes a story
     When it updates progress.txt
     Then it appends: iteration number, story ID, status, duration, files modified, test output, commit hash

AC2: Given /ralph-exec starts
     When it reads progress.txt
     Then it can see previous attempts and errors for context

AC3: Given a story fails
     When logging to progress.txt
     Then it includes the full error message and attempt count
```

---

## User Flow

### As-Is (Current)

```
User → /ralph → @ralph-executor → /brief → /quick ou /epci → Story done
         │                            │
         └── Context stays open ──────┘ (NO liberation)
```

### To-Be (Proposed)

```
User → ./ralph.sh (terminal) → claude "/ralph-exec" → Story done
              │                        │
              └── Context closed ──────┘ (LIBERATION at each call)
```

### Key Improvements

1. **Libération contexte** : Chaque appel `claude "/ralph-exec"` = contexte frais
2. **Pas de routing** : EPCT inline, pas de /brief → /epci
3. **Simplicité** : 1 commande au lieu de 3

---

## Technical Specifications

### /ralph-exec Command Structure

```markdown
---
description: >-
  Execute a single story from prd.json using EPCT workflow inline.
  No routing to /brief or /epci. Fresh context per story.
argument-hint: "[--story US-XXX] --prd <prd.json> [--max-attempts N]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
skills: [testing-strategy, project-memory, git-workflow]
---
```

### EPCT Workflow Phases

| Phase | Duration | Actions |
|-------|----------|---------|
| [E]xplore | 2-3 min | Read parent_spec, parent_brief, related files |
| [P]lan | 1-2 min | Generate task list (inline or @planner for M/L) |
| [C]ode-Test | Variable | Loop: implement → test → fix (max 5x) |
| [T]est & Commit | 1-2 min | Final validation, git commit, update prd.json |

### prd.json Fields Modified by /ralph-exec

| Field | When Modified | New Value |
|-------|---------------|-----------|
| `status` | Start | `"in_progress"` |
| `status` | Success | `"completed"` |
| `status` | Failure | `"failed"` |
| `status` | Dependency not met | `"blocked"` |
| `passes` | Success | `true` |
| `acceptanceCriteria[].done` | Success | `true` for all |
| `tasks[].done` | Success | `true` for all |
| `execution.attempts` | Each invocation | `+1` |
| `execution.code_test_attempts` | Each Code-Test loop | `+1` |
| `execution.last_error` | Failure | Error message |
| `execution.files_modified` | Success | `["file1", "file2"]` |
| `execution.completed_at` | Success | ISO timestamp |
| `testing.test_files` | Success | Test files created |

### ralph.sh Template (generated by /decompose)

```bash
#!/bin/bash
# Ralph loop — generated by /decompose
set -e

# Configuration
MAX_ITERATIONS=${MAX_ITERATIONS:-50}
PRD_FILE="./prd.json"

# Source libraries
source lib/circuit_breaker.sh 2>/dev/null || true

echo "Starting Ralph loop (max $MAX_ITERATIONS iterations)"

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    echo "=== Iteration $i ==="

    # Check circuit breaker (if available)
    if type should_halt_execution &>/dev/null && should_halt_execution; then
        echo "Circuit breaker OPEN - stopping"
        exit 1
    fi

    # Check if any stories remain
    PENDING=$(jq '[.userStories[] | select(.passes==false and .status!="blocked")] | length' "$PRD_FILE")
    if [ "$PENDING" -eq 0 ]; then
        echo "All stories complete!"
        exit 0
    fi

    # Execute next story
    OUTPUT=$(claude "/ralph-exec --prd $PRD_FILE" 2>&1) || true
    echo "$OUTPUT"

    # Check for completion
    if echo "$OUTPUT" | grep -q '<promise>STORY_DONE</promise>'; then
        echo "Story completed successfully"
    else
        echo "Story failed or blocked"
    fi

    # Update circuit breaker (if available)
    if type record_loop_result &>/dev/null; then
        FILES_CHANGED=$(git diff --name-only 2>/dev/null | wc -l || echo "0")
        record_loop_result "$i" "$FILES_CHANGED" "false"
    fi
done

echo "Max iterations reached"
exit 1
```

### Context Strategy

**IMPORTANT** : À chaque itération, `/ralph-exec` doit reconstruire son contexte depuis :

1. **prd.json** — Source de vérité (stories, status, AC)
2. **context.parent_spec** — Fichier S0X.md avec le détail technique
3. **context.parent_brief** — Brief original avec le contexte métier
4. **progress.txt** — Historique des itérations précédentes (erreurs, learnings)

Cela garantit que même sans contexte Claude persistant, l'agent a toutes les informations nécessaires.

---

## Assumptions

### Technical Assumptions

| Assumption | Risk if wrong | Mitigation |
|------------|---------------|------------|
| `claude "/ralph-exec ..."` libère le contexte | High | Tester avec 3+ stories |
| prd.json est lisible par jq dans ralph.sh | Low | Valider format JSON |
| @planner et @implementer fonctionnent depuis /ralph-exec | Medium | Tester invocation subagents |

### Business Assumptions

| Assumption | Risk if wrong | Mitigation |
|------------|---------------|------------|
| Les sessions overnight sont le use case principal | Medium | Supporter aussi runs courts |
| 5 tentatives Code-Test suffisent | Medium | Rendre configurable |

---

## FAQ

### Internal FAQ

**Q: Pourquoi supprimer /ralph au lieu de le simplifier ?**
A: La commande `/ralph` ne libère pas le contexte car elle reste une session Claude ouverte. Seul `ralph.sh` (exécuté directement dans le terminal) permet des appels Claude séparés avec contexte frais.

**Q: Comment annuler une session sans /cancel-ralph ?**
A: Ctrl+C dans le terminal. Les changements déjà commités sont conservés. Pour reprendre, relancer `./ralph.sh` — il reprendra à la prochaine story pending.

**Q: Pourquoi pas de RALPH_STATUS block complexe ?**
A: Simplifié en `<promise>STORY_DONE</promise>`. Le script ralph.sh n'a besoin que de savoir si la story est terminée ou non.

### External FAQ

**Q: Comment savoir où en est l'exécution ?**
A: Consulter `progress.txt` qui log chaque itération, ou regarder `prd.json` qui montre le status de chaque story.

**Q: Que faire si une story échoue ?**
A: Le système passe automatiquement à la suivante (sauf si elle bloque d'autres stories). Les stories en échec sont marquées `status: "failed"` avec l'erreur dans `execution.last_error`.

---

## Success Metrics

| KPI | Current | Target | Measurement |
|-----|---------|--------|-------------|
| Commands Ralph | 3 | 1 | Count in src/commands/ |
| Stories/session overnight | 0 | 10+ | Test run |
| Context liberation | 0% | 100% | Memory monitoring |
| Code-Test loop success rate | N/A | 80% | Log analysis |

---

## Timeline & Milestones

### Phasing Strategy

| Phase | Scope | Deliverables |
|-------|-------|--------------|
| Phase 1 | Core | `/ralph-exec` command |
| Phase 2 | Integration | Modify `/decompose`, generate ralph.sh |
| Phase 3 | Cleanup | Delete `/ralph`, `/cancel-ralph`, `@ralph-executor` |
| Phase 4 | Documentation | Update CLAUDE.md, README |

### Key Milestones

| Milestone | Criteria |
|-----------|----------|
| M1: /ralph-exec functional | Executes 1 story with EPCT inline |
| M2: ralph.sh integration | Loop executes 3+ stories with context liberation |
| M3: Cleanup complete | Old commands deleted, docs updated |
| M4: Overnight test | 10+ stories executed overnight successfully |

---

## Appendix

### A. Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `/ralph-exec` | `src/commands/ralph-exec.md` | New EPCT command |

### B. Files to Modify

| File | Location | Changes |
|------|----------|---------|
| `/decompose` | `src/commands/decompose.md` | Generate ralph.sh with `/ralph-exec` call |
| `CLAUDE.md` | Root | Update command references |
| `ralph.sh` template | `src/templates/ralph/` | Use `/ralph-exec` instead of PROMPT.md |

### C. Files to Delete

| File | Location | Reason |
|------|----------|--------|
| `/ralph` | `src/commands/ralph.md` | Obsolete |
| `/cancel-ralph` | `src/commands/cancel-ralph.md` | Obsolete |
| `@ralph-executor` | `src/agents/ralph-executor.md` | Replaced by /ralph-exec |
| `PROMPT.md` template | `src/templates/ralph/` | Replaced by /ralph-exec |

### D. Glossary

| Term | Definition |
|------|------------|
| **EPCT** | Explore, Plan, Code, Test — workflow simplifié |
| **Context liberation** | Fermeture du contexte Claude entre chaque story |
| **Promise tag** | `<promise>STORY_DONE</promise>` — signal de complétion |
| **Circuit breaker** | Pattern de détection des boucles bloquées |

---

*Generated by /brainstorm — 2025-01-14*
