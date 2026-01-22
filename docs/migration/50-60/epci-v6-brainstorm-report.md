# 📋 Rapport de Brainstorming — Architecture EPCI v6.0

**Date** : 22 janvier 2026  
**Auteur** : Édouard + Claude  
**Session** : Brainstorming Architectural  
**Durée** : ~40 minutes  
**EMS Final** : 89/100 🌳

---

## 1. Résumé Exécutif

### Contexte

Le plugin EPCI v5 avait divergé entre la vision (7 skills, ~3000 LOC) et la réalité (23 skills, architecture fragmentée). La v6 reprend les fondamentaux avec une approche "un rôle, un workflow = un skill" et intègre les best practices multi-agents 2026.

### Principe de Design

> **"Un rôle, un workflow = un skill"**
> 
> Pas de flags multiples qui changent le comportement. Chaque skill a une responsabilité claire et un workflow dédié.

### Décisions Clés

| Décision | Choix retenu | Justification |
|----------|--------------|---------------|
| Nombre de skills | **8 skills** | Consolidation vs 23 en v5 |
| State management | **JSON file-based** | Pas de dépendance externe (Redis/DB) |
| Ralph | **Système auto-généré** | `/spec` produit automatiquement les artifacts |
| Feature Tracking | **`/implement` crée, `/improve` MAJ** | Responsabilité claire |
| `/quick` vs `/implement` | **Skills séparés** | UX différente, pas de flag |
| `/refactor` | **Skill dédié** | Cross-module, métriques complètes |
| Audit | **Hook CI, pas skill** | Pas d'usage interactif |
| Brainstorm EPCI | **Gardé** | Accès codebase via Explore, plugin partagé |

### Livrables Attendus

1. **8 user skills** : `/brainstorm`, `/spec`, `/implement`, `/quick`, `/debug`, `/improve`, `/refactor`, `/factory`
2. **6 core skills (internal)** : state-manager, breakpoint-system, complexity-calculator, clarification-engine, tdd-enforcer, project-memory
3. **Système Ralph** : Artifacts auto-générés (PROMPT.md, MEMORY.md, ralph.sh)
4. **Schemas JSON** : feature-state, prd-v2, ralph-index, ralph-iterations

---

## 2. Architecture Cible

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PLUGIN EPCI v6.0                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    STATE LAYER                                  ││
│  │  .claude/state/                                                 ││
│  │  ├── config.json              # Config globale                  ││
│  │  ├── features/                                                  ││
│  │  │   ├── index.json           # Liste features + statuts        ││
│  │  │   └── {slug}/                                                ││
│  │  │       ├── state.json       # État machine feature            ││
│  │  │       ├── history.json     # Historique actions              ││
│  │  │       └── checkpoints/     # Points de reprise               ││
│  │  └── sessions/                # Sessions brainstorm/debug       ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │  DISCOVERY  │  │   PLANNING  │  │  EXECUTION  │  │  EVOLUTION  ││
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤│
│  │             │  │             │  │             │  │             ││
│  │ /brainstorm │  │ /spec       │  │ /implement  │  │ /debug      ││
│  │ (EMS+HMW)   │  │ (PRD+Ralph) │  │ (STANDARD+) │  │             ││
│  │             │  │             │  │             │  │ /improve    ││
│  │             │  │             │  │ /quick      │  │             ││
│  │             │  │             │  │ (TINY/SMALL)│  │ /refactor   ││
│  │             │  │             │  │             │  │             ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    CORE SKILLS LAYER (internal)                 ││
│  │  • state-manager          — Persistence, checkpoints, resume    ││
│  │  • breakpoint-system      — Affichage + interaction uniformisée ││
│  │  • complexity-calculator  — Routing TINY→LARGE                  ││
│  │  • clarification-engine   — Nettoyage input vocal               ││
│  │  • tdd-enforcer           — Red-Green-Refactor                  ││
│  │  • project-memory         — Contexte projet, conventions        ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    META LAYER                                   ││
│  │  • /factory               — Création skills/agents              ││
│  │  • audit (CI hook)        — Validation conformité               ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    RALPH SYSTEM (externe)                       ││
│  │  .ralph/                                                        ││
│  │  ├── index.json           # Registre features Ralph-ready       ││
│  │  └── {feature}/                                                 ││
│  │      ├── PROMPT.md        # Instructions Claude Code            ││
│  │      ├── MEMORY.md        # Contexte persistant                 ││
│  │      ├── ralph.sh         # Script runner                       ││
│  │      └── logs/            # Execution logs                      ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Spécifications des Skills

### 3.1 `/brainstorm`

**Rôle** : Idéation + exploration codebase → CDC fonctionnel

**Workflow** :
1. Auto-exploration codebase via @Explore (stack, patterns, conventions)
2. Reformulation + validation brief
3. Génération HMW questions
4. Itérations avec EMS tracking
5. **Breakpoint à chaque itération**
6. Output: CDC.md

**Input** : Idée brute + accès codebase
**Output** : CDC.md + score EMS
**State** : Session temporaire (`.claude/state/sessions/`)

**Différence vs brainstormer Claude.ai** :
- Accès codebase via @Explore
- Plugin partagé (équipe sans accès web)
- Intégration state layer pour persistence

---

### 3.2 `/spec`

**Rôle** : Décomposition CDC → PRD technique + tâches granulaires

**Workflow** :
1. Parse CDC.md
2. Complexity calculation
3. Task decomposition (15-30 min par tâche)
4. Success criteria + test_type mapping
5. **BREAKPOINT** : PRD Review
6. Generate outputs

**Input** : CDC.md
**Output** :
- `docs/specs/{feature}.md` — Version humaine
- `docs/specs/{feature}.prd.json` — Version machine (schéma PRD v2)
- `.ralph/{feature}/` — Artifacts auto-générés
  - `PROMPT.md`
  - `MEMORY.md`
  - `ralph.sh`

**Granularité tâches (Goldilocks Zone)** :

| Complexité | Durée estimée | Nb tâches | Routing |
|------------|---------------|-----------|---------|
| TINY | <15 min | 1 | `/quick` |
| SMALL | 15-45 min | 1-2 | `/quick` |
| STANDARD | 1-4h | 3-8 | `/implement` |
| LARGE | 4h+ | 8+ | `/implement` (stages) |

---

### 3.3 `/implement`

**Rôle** : Exécution features STANDARD/LARGE avec workflow EPCI complet

**Workflow (phases EPCI)** :

| Phase | Icône | Actions | Breakpoint |
|-------|-------|---------|------------|
| **E**xplore | 🔍 | Analyse codebase, patterns, risques | ✅ Fin phase |
| **P**lan | 📋 | Séquençage tâches, dépendances | ✅ Fin phase |
| **C**ode | ⚡ | TDD: Red→Green→Refactor par tâche | |
| **I**nspect | 🔎 | Review, tests, documentation | ✅ Si révision |

**Input** : PRD.json
**Output** : Code + Tests + Feature Doc
**State** : **Crée** feature state (`state-manager.createFeature()`)

**Responsabilités état** :
- Crée `features/{slug}/state.json`
- Crée `docs/features/{slug}.md` (Feature Doc)
- Checkpoint après phases E et P
- Update state à chaque tâche complétée

---

### 3.4 `/quick`

**Rôle** : Exécution rapide TINY/SMALL sans overhead

**Workflow simplifié** :
1. Analyse rapide
2. Code + Tests
3. Done

**Différences vs `/implement`** :
- Pas de Feature Doc
- Pas de state persisté
- Pas de breakpoints (sauf SMALL avant code)
- Pas de rapport final

**Input** : Description simple ou PRD.json léger
**Output** : Code + Tests
**State** : Non

---

### 3.5 `/debug`

**Rôle** : Fix bugs avec analyse root cause

**Workflow** :
1. Analyse stack trace / reproduction
2. Isolation du problème
3. Fix avec test de non-régression
4. Verify fix ne casse rien
5. Document root cause

**Input** : Issue/Error description
**Output** : Fix + Tests + Root cause analysis
**State** : Session temporaire

---

### 3.6 `/improve`

**Rôle** : Amélioration feature existante avec contexte

**Workflow** :
1. Load Feature State existant
2. Load Feature Doc (contexte complet)
3. Analyse demande amélioration
4. Mini-spec (delta, pas full PRD)
5. Implement improvement
6. Update Feature State + Doc

**Input** : Feature ID + demande d'amélioration
**Output** : Updated code + Updated Feature Doc
**State** : **MAJ** feature state (ajoute à `improvements[]`)

---

### 3.7 `/refactor`

**Rôle** : Optimisation / simplification code sans changer le comportement

**Scope supportés** :
- Single file
- Module entier
- Cross-module (extraction services)
- Architecture (patterns globaux)

**Workflow** :
1. Analyse statique (métriques avant)
2. Dependency graph
3. Code smells detection
4. **BREAKPOINT** : Proposition plan
5. Exécution step-by-step (tests verts obligatoires)
6. Rapport métriques delta

**Input** : Path(s) fichier/module/pattern
**Output** : Cleaner code + Metrics report
**State** : Non

**Métriques trackées** :
- Cyclomatic complexity
- LOC
- Dependencies count
- Code smells fixed

---

### 3.8 `/factory`

**Rôle** : Création skills et agents conformes aux standards

**Workflow** :
1. Questions sur le besoin
2. Architecture (structure fichiers)
3. Description crafting (pour triggering)
4. Workflow design
5. **BREAKPOINT** : Validation
6. Génération fichiers

**Input** : Description du skill/agent souhaité
**Output** : Fichiers skill/agent complets
**State** : Non

---

## 4. State-Manager — Spécification Complète

### 4.1 Structure Fichiers

```
.claude/state/
├── config.json
├── features/
│   ├── index.json
│   └── {feature-slug}/
│       ├── state.json
│       ├── history.json
│       └── checkpoints/
│           └── {phase}-{timestamp}.json
└── sessions/
    └── {session-id}.json
```

### 4.2 Schema `index.json`

```json
{
  "$schema": "https://epci.dev/schemas/feature-index-v1.json",
  "version": 1,
  "last_update": "2026-01-22T15:00:00Z",
  "features": [
    {
      "id": "auth-oauth-google",
      "status": "in_progress",
      "current_phase": "code",
      "complexity": "STANDARD",
      "branch": "feature/auth-oauth-google",
      "created_at": "2026-01-20T10:00:00Z"
    }
  ]
}
```

### 4.3 Schema `state.json`

```json
{
  "$schema": "https://epci.dev/schemas/feature-state-v1.json",
  "feature_id": "auth-oauth-google",
  "version": 1,
  
  "lifecycle": {
    "status": "in_progress",
    "current_phase": "code",
    "completed_phases": ["explore", "plan"],
    "created_at": "2026-01-22T10:00:00Z",
    "last_update": "2026-01-22T14:30:00Z",
    "created_by": "/implement",
    "last_updated_by": "/implement"
  },
  
  "spec": {
    "prd_json": "docs/specs/auth-oauth-google.prd.json",
    "prd_md": "docs/specs/auth-oauth-google.md",
    "complexity": "STANDARD",
    "total_tasks": 6,
    "estimated_minutes": 180
  },
  
  "execution": {
    "tasks": {
      "completed": ["US-001", "US-002"],
      "current": "US-003",
      "pending": ["US-004", "US-005", "US-006"],
      "failed": []
    },
    "iterations": 12,
    "last_error": null
  },
  
  "artifacts": {
    "feature_doc": "docs/features/auth-oauth-google.md",
    "test_files": ["tests/integration/oauth.test.ts"],
    "modified_files": ["src/auth/oauth.ts", "src/auth/types.ts"]
  },
  
  "checkpoints": [
    {
      "id": "ckpt-001",
      "phase": "plan",
      "timestamp": "2026-01-22T11:00:00Z",
      "git_ref": "abc123",
      "resumable": true
    }
  ],
  
  "improvements": []
}
```

### 4.4 API State-Manager

```typescript
interface StateManager {
  // Features
  createFeature(featureId: string, spec: SpecOutput): FeatureState;
  loadFeature(featureId: string): FeatureState | null;
  updateFeature(featureId: string, updates: Partial<FeatureState>): void;
  listFeatures(filter?: { status?: Status }): FeatureSummary[];
  
  // Checkpoints
  createCheckpoint(featureId: string, phase: Phase): Checkpoint;
  listCheckpoints(featureId: string): Checkpoint[];
  restoreCheckpoint(checkpointId: string): FeatureState;
  
  // History
  appendHistory(featureId: string, entry: HistoryEntry): void;
  getHistory(featureId: string): HistoryEntry[];
  
  // Sessions (brainstorm, debug)
  saveSession(sessionId: string, data: SessionData): void;
  loadSession(sessionId: string): SessionData | null;
}
```

---

## 5. Système Ralph — Spécification Complète

### 5.1 Vue d'Ensemble

Ralph est un système d'exécution batch autonome. Les artifacts sont **auto-générés par `/spec`**.

```
.ralph/
├── index.json
└── {feature-slug}/
    ├── PROMPT.md        # Instructions Claude Code
    ├── MEMORY.md        # Contexte persistant
    ├── ralph.sh         # Script runner
    └── logs/
        ├── execution.log
        └── iterations.json
```

### 5.2 `PROMPT.md` — Template

```markdown
# Ralph Execution Prompt — {feature_name}

## Context

You are executing feature **{feature_id}** in autonomous batch mode.
Branch: `{branch_name}`
Complexity: {complexity}
Total tasks: {total_tasks}

## Source Documents

- PRD (human readable): `{prd_md_path}`
- PRD (machine readable): `{prd_json_path}`
- Memory file: `.ralph/{feature_slug}/MEMORY.md`

## Project Stack

{stack_detection_output}

## Conventions

{project_conventions}

## Execution Rules

### Task Processing

For each task in PRD.json `userStories[]`:
1. Read the task and its `acceptanceCriteria`
2. Read `success_criteria` with associated `test_type`
3. Implement using TDD:
   - **RED**: Write failing test based on success_criteria
   - **GREEN**: Implement minimal code to pass
   - **REFACTOR**: Clean up while keeping tests green
4. Mark task as done in MEMORY.md
5. Commit: `feat({feature_id}): {task_title} [US-{id}]`

### Stop Conditions

- All tasks done ✓
- Max iterations reached ({max_iterations})
- 3 consecutive blocked tasks
- Critical error
```

### 5.3 `MEMORY.md` — Template

```markdown
# Ralph Memory — {feature_name}

> Auto-generated by `/spec` — Updated by Ralph during execution

## Feature Info

| Key | Value |
|-----|-------|
| Feature ID | {feature_id} |
| Branch | {branch_name} |
| Complexity | {complexity} |
| Total Tasks | {total_tasks} |

## Progress

| Task ID | Title | Status | Iteration | Files Modified |
|---------|-------|--------|-----------|----------------|
| US-001 | {title} | ⏳ pending | - | - |

**Legend**: ✅ done | ⏳ pending | 🚫 blocked | ⏭️ skipped

## Statistics

Total iterations: 0
Tasks completed: 0/{total_tasks}

## Errors

_No errors recorded_

## Final Status

_Execution not complete_
```

### 5.4 `ralph.sh` — Script

```bash
#!/bin/bash
# Ralph Runner — EPCI v6.0

FEATURE_ID="{feature_slug}"
PRD_JSON="{prd_json_path}"
BRANCH="{branch_name}"
MAX_ITERATIONS={max_iterations}

# Pre-flight checks
# ...

# Launch Claude Code
claude --print \
    --prompt-file ".ralph/${FEATURE_ID}/PROMPT.md" \
    --context-file ".ralph/${FEATURE_ID}/MEMORY.md" \
    --context-file "$PRD_JSON" \
    --max-turns "$MAX_ITERATIONS"

# Post-execution
# ...
```

### 5.5 Boucle d'Exécution

```
ralph.sh (launcher)
    │
    ▼
Pre-flight (branch, PRD, memory)
    │
    ▼
┌─────────────────────────────────┐
│         CLAUDE CODE             │
│                                 │
│  Load PROMPT.md + MEMORY.md     │
│           │                     │
│           ▼                     │
│  Parse PRD.json                 │
│  Select next eligible task      │
│           │                     │
│           ▼                     │
│  TDD Cycle (RED→GREEN→REFACTOR) │
│           │                     │
│           ▼                     │
│  Update MEMORY.md               │
│           │                     │
│           ▼                     │
│  Check Stop Conditions          │
│           │                     │
│     Continue / Stop             │
└─────────────────────────────────┘
    │
    ▼
Post-exec (tests, lint, report)
```

---

## 6. PRD JSON v2 — Schema avec Success Criteria

```json
{
  "$schema": "https://epci.dev/schemas/prd-v2.json",
  "version": "2.0",
  "branchName": "feature/my-feature",
  "projectName": "My Project",
  "generatedAt": "2026-01-22T10:00:00Z",
  "generatedBy": "EPCI /spec v6.0",
  
  "config": {
    "max_iterations": 50,
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "granularity": "standard"
  },
  
  "userStories": [
    {
      "id": "US-001",
      "title": "Validate OAuth token",
      "category": "backend",
      "type": "Logic",
      "complexity": "M",
      "priority": 1,
      "status": "pending",
      
      "acceptanceCriteria": [
        {"id": "AC1", "description": "Token validated against Google", "done": false}
      ],
      
      "success_criteria": [
        {
          "id": "SC1",
          "description": "Returns 200 on valid token",
          "test_type": "integration",
          "test_file": "tests/integration/oauth.test.ts"
        },
        {
          "id": "SC2",
          "description": "Returns 401 on expired token",
          "test_type": "unit",
          "test_file": "tests/unit/token-validator.test.ts"
        }
      ],
      
      "tasks": [
        {"id": "T1", "description": "Create token validator service", "done": false}
      ],
      
      "dependencies": {
        "depends_on": [],
        "blocks": ["US-002"]
      },
      
      "execution": {
        "attempts": 0,
        "last_error": null,
        "files_modified": [],
        "completed_at": null
      },
      
      "context": {
        "parent_spec": "docs/specs/auth-oauth.md",
        "estimated_minutes": 30
      }
    }
  ]
}
```

---

## 7. Flux Global EPCI v6.0

```
┌──────────────┐
│    Idée      │
│    brute     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌───────────────────────────────────────────┐
│ /brainstorm  │     │ • Auto-explore codebase                   │
│              │────▶│ • EMS itératif + breakpoints              │
│              │     │ • Output: CDC.md                          │
└──────┬───────┘     └───────────────────────────────────────────┘
       │ CDC.md
       ▼
┌──────────────┐     ┌───────────────────────────────────────────┐
│    /spec     │     │ • Complexity calculation                  │
│              │────▶│ • Task decomposition (15-30 min)          │
│              │     │ • Output: PRD.md + PRD.json + Ralph       │
└──────┬───────┘     └───────────────────────────────────────────┘
       │ PRD.json
       ├────────────────────────────┐
       │                            │
       ▼                            ▼
┌──────────────┐              ┌──────────────┐
│ /implement   │              │   /quick     │
│ (STANDARD+)  │              │ (TINY/SMALL) │
└──────┬───────┘              └──────┬───────┘
       │                             │
       │ Feature Doc + State         │ Code + Tests
       ▼                             │
┌──────────────┐                     │
│  /improve    │◄────────────────────┘
│  /refactor   │
│  /debug      │
└──────────────┘
```

---

## 8. Récapitulatif Composants

### Skills (8)

| Skill | Rôle | State |
|-------|------|-------|
| `/brainstorm` | Idéation + exploration | Session temp |
| `/spec` | CDC → PRD + Ralph | Non |
| `/implement` | Exécution STANDARD/LARGE | **Crée** |
| `/quick` | Exécution TINY/SMALL | Non |
| `/debug` | Fix bugs | Session temp |
| `/improve` | Amélioration feature | **MAJ** |
| `/refactor` | Optimisation code | Non |
| `/factory` | Création skills/agents | Non |

### Core Skills (6) — Internal (user-invocable: false)

| Core Skill | Responsabilité | Location |
|------------|----------------|----------|
| `state-manager` | Persistence, checkpoints, resume | `skills/core/state-manager/` |
| `breakpoint-system` | Affichage + interaction | `skills/core/breakpoint-system/` |
| `complexity-calculator` | Routing TINY→LARGE | `skills/core/complexity-calculator/` |
| `clarification-engine` | Nettoyage input vocal | `skills/core/clarification-engine/` |
| `tdd-enforcer` | Red-Green-Refactor | `skills/core/tdd-enforcer/` |
| `project-memory` | Contexte projet | `skills/core/project-memory/` |

### External

| Element | Type |
|---------|------|
| Ralph system | Fichiers générés |
| Audit | Hook CI |

---

## 9. Plan de Développement Suggéré

| Phase | Contenu | Effort estimé |
|-------|---------|---------------|
| 1 | Shared Components (state-manager, breakpoint-system) | 8h |
| 2 | `/factory` (pour générer les autres skills) | 4h |
| 3 | `/spec` + système Ralph | 10h |
| 4 | `/implement` + `/quick` | 12h |
| 5 | `/brainstorm` (adaptation EPCI) | 6h |
| 6 | `/debug` + `/improve` + `/refactor` | 10h |
| 7 | Intégration + Tests | 8h |

**Total estimé** : ~58 heures

---

## 10. Critères de Succès

| Critère | Cible | Mesure |
|---------|-------|--------|
| Nombre skills | ≤10 | 8 ✓ |
| State layer | Fonctionnel | Checkpoint/resume testable |
| Ralph auto-généré | `/spec` produit tout | Artifacts complets |
| Task granularity | 15-30 min | Moyenne temps exécution |
| Success criteria | Mappé test_type | Couverture tests |
| Feature tracking | Maintenu auto | State.json à jour |

---

## 11. Risques Identifiés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Complexité state-manager | Medium | Commencer simple, itérer |
| Ralph drift avec Claude Code updates | Medium | Versionner PROMPT.md template |
| Overhead `/implement` vs `/quick` | Low | UX tests avec vrais use cases |
| 8 skills encore trop ? | Low | Principe "un rôle = un skill" validé |

---

## 12. Prochaine Étape

**Recommandation** : Développer dans cet ordre :

1. `state-manager` shared component (fondation)
2. `/factory` (pour générer les skills suivants de manière standardisée)
3. `/spec` + système Ralph (cœur du workflow)

Chaînage suggéré : `/spec` sur ce rapport pour générer le PRD technique et les tâches.

---

*Document généré par brainstormer EPCI v6.0*  
*EMS Final: 89/100 🌳 | Itérations: 5 | Durée: ~40 min*
