# Plan de Migration : Intégration Skills SuperPowers dans EPCI

> **Version** : 1.0.0
> **Date** : Janvier 2025
> **Auteur** : Analyse comparative EPCI vs SuperPowers
> **Statut** : En attente d'implémentation

---

## Table des Matières

1. [Contexte et Objectifs](#1-contexte-et-objectifs)
2. [Analyse des Écarts](#2-analyse-des-écarts)
3. [Architecture Cible](#3-architecture-cible)
4. [Plan de Migration par Phases](#4-plan-de-migration-par-phases)
5. [Spécifications Détaillées par Skill](#5-spécifications-détaillées-par-skill)
6. [Impacts sur les Composants Existants](#6-impacts-sur-les-composants-existants)
7. [Tests et Validation](#7-tests-et-validation)
8. [Rollback et Risques](#8-rollback-et-risques)
9. [Checklist de Migration](#9-checklist-de-migration)

---

## 1. Contexte et Objectifs

### 1.1 Contexte

L'analyse comparative entre SuperPowers et EPCI a révélé que :
- **EPCI excelle** en discovery/planning (EMS, personas, frameworks, MCP)
- **SuperPowers excelle** en exécution/qualité (TDD strict, verification, 2-stage review)

### 1.2 Objectifs de la Migration

| Objectif | Métrique | Cible |
|----------|----------|-------|
| Améliorer la discipline d'exécution | Taux de bugs post-implémentation | -50% |
| Renforcer la qualité du code | Score code review | +20% |
| Réduire les faux "terminé" | Claims non vérifiés | 0% |
| Paralléliser les investigations | Temps debugging multi-bugs | -40% |

### 1.3 Périmètre

**IN SCOPE** :
- 6 nouveaux skills à créer
- 1 nouvel agent à créer (@spec-reviewer)
- 3 agents existants à modifier
- 4 commandes à enrichir

**OUT OF SCOPE** :
- Refonte complète du workflow EPCI
- Suppression de skills existants
- Changement de la structure de fichiers

### 1.4 Version Cible

```
EPCI v5.0.0 — "SuperPowers Integration"
```

---

## 2. Analyse des Écarts

### 2.1 Matrice des Écarts

| Capacité | SuperPowers | EPCI Actuel | Écart | Priorité |
|----------|-------------|-------------|-------|----------|
| Vérification avant completion | ✅ Strict | ❌ Absent | CRITIQUE | P0 |
| TDD RED-GREEN-REFACTOR | ✅ Forcé | 🟡 Recommandé | MAJEUR | P0 |
| 2-Stage Review (spec + quality) | ✅ Séparé | 🟡 Combiné | MAJEUR | P0 |
| Parallel agent dispatch | ✅ Structuré | ❌ Absent | MOYEN | P1 |
| Git Worktrees isolation | ✅ Intégré | ❌ Absent | MOYEN | P1 |
| Branch completion workflow | ✅ 4 options | ❌ Absent | MOYEN | P1 |
| Root-cause tracing | ✅ Technique | 🟡 Basique | MINEUR | P2 |
| Defense-in-depth | ✅ 4 couches | ❌ Absent | MINEUR | P2 |
| Testing anti-patterns | ✅ Documenté | ❌ Absent | MINEUR | P2 |

### 2.2 Dépendances entre Skills

```
┌─────────────────────────────────────────────────────────────┐
│                    ORDRE D'IMPLÉMENTATION                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1 (Fondations)                                       │
│  ┌─────────────────────────┐                                │
│  │ verification-before-    │                                │
│  │ completion              │──┐                             │
│  └─────────────────────────┘  │                             │
│                               ▼                             │
│  Phase 2 (TDD)            ┌─────────────────────────┐       │
│  ┌─────────────────────┐  │ @implementer enrichi    │       │
│  │ tdd-strict          │──┤ (dépend de TDD +        │       │
│  │ + anti-patterns     │  │  verification)          │       │
│  └─────────────────────┘  └─────────────────────────┘       │
│                               │                             │
│  Phase 3 (Review)             ▼                             │
│  ┌─────────────────────────┐  ┌─────────────────────┐       │
│  │ @spec-reviewer          │──│ 2-stage review      │       │
│  │ (nouveau)               │  │ workflow            │       │
│  └─────────────────────────┘  └─────────────────────┘       │
│                                                             │
│  Phase 4 (Parallèle - indépendant)                          │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ parallel-           │  │ git-worktrees       │           │
│  │ investigations      │  │                     │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                             │
│  Phase 5 (Finalisation)                                     │
│  ┌─────────────────────────┐                                │
│  │ branch-completion       │                                │
│  │ (dépend de worktrees)   │                                │
│  └─────────────────────────┘                                │
│                                                             │
│  Phase 6 (Enrichissements)                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ root-cause-tracing  │  │ defense-in-depth    │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Architecture Cible

### 3.1 Nouveaux Composants

```
src/
├── skills/
│   └── core/
│       ├── verification-before-completion/    # NOUVEAU
│       │   └── SKILL.md
│       ├── tdd-strict/                        # NOUVEAU
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── anti-patterns.md
│       ├── parallel-investigations/           # NOUVEAU
│       │   └── SKILL.md
│       ├── git-worktrees/                     # NOUVEAU
│       │   └── SKILL.md
│       ├── branch-completion/                 # NOUVEAU
│       │   └── SKILL.md
│       └── debugging-strategy/                # ENRICHI
│           ├── SKILL.md
│           └── references/
│               ├── root-cause-tracing.md      # NOUVEAU
│               └── defense-in-depth.md        # NOUVEAU
│
├── agents/
│   ├── spec-reviewer.md                       # NOUVEAU
│   ├── implementer.md                         # MODIFIÉ
│   ├── code-reviewer.md                       # MODIFIÉ
│   └── templates/                             # NOUVEAU
│       ├── implementer-prompt.md
│       ├── spec-reviewer-prompt.md
│       └── code-quality-reviewer-prompt.md
│
└── commands/
    ├── epci.md                                # MODIFIÉ
    ├── quick.md                               # MODIFIÉ
    ├── debug.md                               # MODIFIÉ
    └── brainstorm.md                          # MODIFIÉ
```

### 3.2 Nouveaux Workflows

#### Workflow 2-Stage Review

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ @implementer │────▶│ @spec-reviewer   │────▶│ @code-reviewer  │
│ (implement + │     │ (spec compliance)│     │ (code quality)  │
│  self-review)│     └────────┬─────────┘     └────────┬────────┘
└─────────────┘              │                         │
       ▲                     │ Issues?                 │ Issues?
       │                     ▼                         ▼
       │              ┌──────────────┐          ┌──────────────┐
       └──────────────│ Fix spec gaps│          │ Fix quality  │
                      └──────────────┘          └──────────────┘
```

#### Workflow Branch Completion

```
Tests Pass? ──▶ Present 4 Options:
                │
                ├─▶ 1. Merge locally ──▶ Cleanup worktree
                │
                ├─▶ 2. Push + PR ──▶ Keep worktree
                │
                ├─▶ 3. Keep as-is ──▶ Keep worktree
                │
                └─▶ 4. Discard ──▶ Confirm ──▶ Cleanup all
```

---

## 4. Plan de Migration par Phases

### Phase 1 : Fondations (Priorité P0)

**Durée estimée** : 1-2 jours
**Dépendances** : Aucune

#### 1.1 Créer `verification-before-completion`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/verification-before-completion/SKILL.md` |
| **Source** | `docs/librairies/superpowers-main/skills/verification-before-completion/SKILL.md` |
| **Adaptations** | Intégrer terminologie EPCI (phases, checkpoints) |
| **Tokens** | < 2000 |

**Contenu clé à inclure** :
- Iron Law : "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- Gate Function (5 étapes)
- Common Failures table
- Red Flags list
- Rationalization Prevention table

**Intégrations** :
- Hook `post-phase-2` : Vérifier tests avant Phase 3
- Hook `post-phase-3` : Vérifier avant /commit
- Checkpoint [T] dans /quick

---

### Phase 2 : TDD Strict (Priorité P0)

**Durée estimée** : 2-3 jours
**Dépendances** : Phase 1

#### 2.1 Créer `tdd-strict`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/tdd-strict/SKILL.md` |
| **Source** | `docs/librairies/superpowers-main/skills/test-driven-development/SKILL.md` |
| **Adaptations** | Intégrer avec testing-strategy existant, références EPCI |
| **Tokens** | < 4000 |

**Contenu clé** :
- Iron Law : "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- Cycle RED → Verify RED → GREEN → Verify GREEN → REFACTOR
- Flowchart du cycle
- Rationalization table (15+ excuses)
- Red Flags list
- Verification Checklist

#### 2.2 Créer `references/anti-patterns.md`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/tdd-strict/references/anti-patterns.md` |
| **Source** | `docs/librairies/superpowers-main/skills/test-driven-development/testing-anti-patterns.md` |
| **Tokens** | < 2000 |

**5 Anti-patterns** :
1. Testing Mock Behavior
2. Test-Only Methods in Production
3. Mocking Without Understanding
4. Incomplete Mocks
5. Integration Tests as Afterthought

#### 2.3 Modifier `@implementer`

| Élément | Modification |
|---------|--------------|
| **Fichier** | `src/agents/implementer.md` |
| **Ajouts** | Self-review section, TDD checkpoints, "Watch it fail" step |

**Template enrichi** :
```markdown
## Before You Begin
[Questions section - existant]

## Your Job (TDD Enforced)
1. Write failing test
2. **VERIFY RED** - Run test, confirm failure message
3. Write minimal code
4. **VERIFY GREEN** - Run test, confirm pass
5. Commit
6. Self-review (see below)

## Self-Review Checklist
- [ ] Did I watch each test fail before implementing?
- [ ] Did I write minimal code only?
- [ ] Did I avoid YAGNI violations?
```

---

### Phase 3 : 2-Stage Review (Priorité P0)

**Durée estimée** : 2-3 jours
**Dépendances** : Phase 2

#### 3.1 Créer `@spec-reviewer`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/agents/spec-reviewer.md` |
| **Model** | sonnet |
| **Rôle** | Vérifie conformité aux specs uniquement |

**Frontmatter** :
```yaml
---
name: spec-reviewer
description: >-
  Validates implementation matches specifications exactly.
  Checks for missing requirements and extra features (YAGNI).
  Use after @implementer, before @code-reviewer.
model: sonnet
allowed-tools: [Read, Grep, Glob]
---
```

**Checklist Spec Reviewer** :
- [ ] Toutes les requirements implémentées ?
- [ ] Rien de plus que demandé (YAGNI) ?
- [ ] Edge cases couverts selon specs ?
- [ ] Tests correspondent aux acceptance criteria ?

**Output format** :
```markdown
## Spec Compliance Review

### Status: ✅ COMPLIANT | ❌ ISSUES FOUND

### Requirements Check
| Requirement | Status | Notes |
|-------------|--------|-------|
| REQ-1       | ✅     |       |
| REQ-2       | ❌     | Missing X |

### YAGNI Check
- [ ] No extra features added
- [ ] No over-engineering

### Issues to Fix
1. [Issue 1 - blocking]
2. [Issue 2 - blocking]

### Verdict
[ ] Ready for code quality review
[ ] Needs fixes (list above)
```

#### 3.2 Modifier `@code-reviewer`

| Élément | Modification |
|---------|--------------|
| **Fichier** | `src/agents/code-reviewer.md` |
| **Focus** | Qualité code uniquement (plus de spec check) |

**Clarifier le scope** :
```markdown
## Scope (Code Quality ONLY)

This review assumes spec compliance is already verified by @spec-reviewer.

Focus on:
- Code quality and maintainability
- Patterns and conventions
- Performance considerations
- Security (if not @security-auditor scope)
- Test quality (not coverage - that's specs)

DO NOT check:
- Spec compliance (done by @spec-reviewer)
- Feature completeness (done by @spec-reviewer)
```

#### 3.3 Créer templates prompts

| Fichier | Contenu |
|---------|---------|
| `src/agents/templates/implementer-prompt.md` | Template dispatch @implementer |
| `src/agents/templates/spec-reviewer-prompt.md` | Template dispatch @spec-reviewer |
| `src/agents/templates/code-quality-reviewer-prompt.md` | Template dispatch @code-reviewer |

---

### Phase 4 : Parallélisation et Isolation (Priorité P1)

**Durée estimée** : 2-3 jours
**Dépendances** : Aucune (parallélisable avec Phase 2-3)

#### 4.1 Créer `parallel-investigations`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/parallel-investigations/SKILL.md` |
| **Source** | `docs/librairies/superpowers-main/skills/dispatching-parallel-agents/SKILL.md` |
| **Tokens** | < 2000 |

**Contenu clé** :
- When to Use flowchart
- Pattern : 1 agent per independent problem domain
- Agent Prompt Structure template
- Common Mistakes
- Integration with /debug

**Intégration /debug** :
```markdown
## Auto-Detection Parallel

Si /debug détecte :
- 3+ test files failing
- Failures dans subsystèmes différents
- Pas de dépendance évidente

Alors proposer :
"Multiple independent failures detected. Dispatch parallel agents? [y/n]"
```

#### 4.2 Créer `git-worktrees`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/git-worktrees/SKILL.md` |
| **Source** | `docs/librairies/superpowers-main/skills/using-git-worktrees/SKILL.md` |
| **Tokens** | < 2500 |

**Contenu clé** :
- Directory Selection Process (priority order)
- Safety Verification (.gitignore check)
- Creation Steps (5 steps)
- Auto-setup per stack (npm/pip/cargo/go)
- Baseline test verification

**Intégration workflow** :
- Proposer en fin de /brainstorm (après EMS >= 70)
- Obligatoire pour /epci --large
- Optionnel pour /epci standard

---

### Phase 5 : Finalisation (Priorité P1)

**Durée estimée** : 1-2 jours
**Dépendances** : Phase 4 (git-worktrees)

#### 5.1 Créer `branch-completion`

| Élément | Détail |
|---------|--------|
| **Fichier** | `src/skills/core/branch-completion/SKILL.md` |
| **Source** | `docs/librairies/superpowers-main/skills/finishing-a-development-branch/SKILL.md` |
| **Tokens** | < 2000 |

**Process** :
1. Verify Tests Pass
2. Determine Base Branch
3. Present 4 Options
4. Execute Choice
5. Cleanup Worktree (si applicable)

**4 Options** :
| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

**Intégration** :
- Fin de Phase 3 /epci
- Fin de /quick après checkpoint [T]
- Après /commit si worktree actif

---

### Phase 6 : Enrichissements (Priorité P2)

**Durée estimée** : 1-2 jours
**Dépendances** : Aucune

#### 6.1 Enrichir `debugging-strategy`

**Ajouts** :
- `references/root-cause-tracing.md`
- `references/defense-in-depth.md`
- Rule "3+ fixes failed = question architecture"

#### 6.2 `root-cause-tracing.md`

| Source | `docs/librairies/superpowers-main/skills/systematic-debugging/root-cause-tracing.md` |
|--------|---|

**Technique** :
1. Observe Symptom
2. Find Immediate Cause
3. Ask "What Called This?"
4. Keep Tracing Up
5. Find Original Trigger

#### 6.3 `defense-in-depth.md`

| Source | `docs/librairies/superpowers-main/skills/systematic-debugging/defense-in-depth.md` |
|--------|---|

**4 Layers** :
1. Entry Point Validation
2. Business Logic Validation
3. Environment Guards
4. Debug Instrumentation

---

## 5. Spécifications Détaillées par Skill

### 5.1 verification-before-completion

```yaml
# Frontmatter
---
name: verification-before-completion
description: >-
  Use before claiming work complete, fixed, or passing. Requires running
  verification commands and confirming output. Evidence before assertions.
  Invoked by: /epci Phase 2-3, /quick checkpoint [T], /commit.
allowed-tools: [Bash, Read]
---
```

**Iron Law** :
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**Gate Function** :
```
BEFORE claiming any status:
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim
```

**Common Failures Table** :

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run |
| Build succeeds | Build exit 0 | Linter passing |
| Bug fixed | Test symptom passes | Code changed |

**Red Flags** :
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- Trusting agent success reports
- ANY wording implying success without verification

---

### 5.2 tdd-strict

```yaml
---
name: tdd-strict
description: >-
  Use when implementing any feature or bugfix. Enforces RED-GREEN-REFACTOR
  cycle with mandatory verification steps. No production code without
  failing test first.
allowed-tools: [Read, Write, Bash, Grep]
---
```

**Iron Law** :
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Cycle** :
```
RED ──▶ Verify RED ──▶ GREEN ──▶ Verify GREEN ──▶ REFACTOR
 │         │            │           │              │
 │         │            │           │              └─▶ Stay GREEN
 │         │            │           │
 │         │            │           └─▶ Test passes? If no, fix code
 │         │            │
 │         │            └─▶ Write minimal code
 │         │
 │         └─▶ Test fails correctly? If no, fix test
 │
 └─▶ Write ONE failing test
```

**Rationalization Table** (extrait) :

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 sec. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "TDD will slow me down" | TDD faster than debugging. |
| "I already manually tested" | Manual ≠ systematic. No record. |

---

### 5.3 parallel-investigations

```yaml
---
name: parallel-investigations
description: >-
  Use when facing 3+ independent failures in different subsystems.
  Dispatches one agent per problem domain for concurrent investigation.
  Invoked by: /debug when multiple independent failures detected.
allowed-tools: [Task, Read, Grep]
---
```

**When to Use** :
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- No shared state between investigations

**Pattern** :
```
1. Identify Independent Domains
2. Create Focused Agent Tasks (one per domain)
3. Dispatch in Parallel (Task tool multiple calls)
4. Review and Integrate results
```

**Agent Prompt Template** :
```markdown
Fix the failing tests in [FILE]:

1. [Test name 1] - [expected behavior]
2. [Test name 2] - [expected behavior]

Your task:
1. Read test file, understand what each test verifies
2. Identify root cause
3. Fix (prefer real fix over timeout increase)
4. Verify all tests pass

Return: Summary of root cause and changes made.
```

---

### 5.4 git-worktrees

```yaml
---
name: git-worktrees
description: >-
  Use when starting feature work needing isolation. Creates git worktrees
  with auto-setup and baseline verification. Invoked by: /brainstorm
  (post-EMS), /epci --large (mandatory).
allowed-tools: [Bash, Read, Glob]
---
```

**Directory Priority** :
1. Check `.worktrees/` exists → use it
2. Check `worktrees/` exists → use it
3. Check CLAUDE.md preference
4. Ask user

**Safety Check** :
```bash
git check-ignore -q .worktrees 2>/dev/null
# If NOT ignored → add to .gitignore + commit
```

**Creation Steps** :
```bash
# 1. Create worktree
git worktree add .worktrees/$BRANCH -b $BRANCH

# 2. Auto-setup
if [ -f package.json ]; then npm install; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
# etc.

# 3. Baseline verification
npm test / pytest / cargo test
```

---

### 5.5 branch-completion

```yaml
---
name: branch-completion
description: >-
  Use when implementation complete and tests pass. Presents 4 structured
  options for branch handling. Invoked by: /epci Phase 3, /quick [T].
allowed-tools: [Bash, Read]
---
```

**Process** :
```
1. Verify tests pass (BLOCKING)
2. Determine base branch (main/master)
3. Present options:
   "Implementation complete. What would you like to do?
    1. Merge back to [base] locally
    2. Push and create Pull Request
    3. Keep branch as-is
    4. Discard this work"
4. Execute choice
5. Cleanup worktree (Options 1, 4 only)
```

**Option 4 Confirmation** :
```
This will permanently delete:
- Branch [name]
- All commits: [list]
- Worktree at [path]

Type 'discard' to confirm.
```

---

## 6. Impacts sur les Composants Existants

### 6.1 Commandes

| Commande | Modifications |
|----------|---------------|
| `/epci` | Intégrer 2-stage review Phase 2, verification Phase 2-3, branch-completion Phase 3, worktrees --large |
| `/quick` | Intégrer verification checkpoint [T], branch-completion après [T] |
| `/debug` | Intégrer parallel-investigations si multi-failures, root-cause-tracing |
| `/brainstorm` | Proposer git-worktrees après EMS >= 70 |
| `/commit` | Intégrer verification-before-completion |

### 6.2 Agents

| Agent | Modifications |
|-------|---------------|
| `@implementer` | Ajouter TDD checkpoints, self-review section |
| `@code-reviewer` | Restreindre scope à quality only (plus de spec check) |
| `@planner` | Intégrer bite-sized tasks (2-5 min) |

### 6.3 Skills Existants

| Skill | Modifications |
|-------|---------------|
| `testing-strategy` | Référencer tdd-strict, anti-patterns |
| `debugging-strategy` | Ajouter root-cause-tracing, defense-in-depth, rule 3+ fixes |
| `git-workflow` | Référencer git-worktrees, branch-completion |

### 6.4 Hooks

| Hook | Modifications |
|------|---------------|
| `post-phase-2` | Ajouter verification check |
| `post-phase-3` | Ajouter verification check avant memory update |

### 6.5 CLAUDE.md

```markdown
### Nouveautés v5.0 (SuperPowers Integration)

- **verification-before-completion** : Vérification obligatoire avant claims
- **tdd-strict** : TDD RED-GREEN-REFACTOR forcé avec checkpoints
- **2-Stage Review** : @spec-reviewer (conformité) + @code-reviewer (qualité)
- **parallel-investigations** : Dispatch agents parallèles pour multi-bugs
- **git-worktrees** : Isolation workspace avec auto-setup
- **branch-completion** : Workflow 4 options de finalisation

### Subagents (11)

| Subagent | Model | Rôle | Invoqué par |
|----------|-------|------|-------------|
| `@spec-reviewer` | sonnet | Conformité specs | `/epci` Phase 2 (après @implementer) |
[... autres agents ...]
```

---

## 7. Tests et Validation

### 7.1 Tests par Skill

| Skill | Tests |
|-------|-------|
| verification-before-completion | Simuler claim sans evidence → doit bloquer |
| tdd-strict | Simuler code avant test → doit forcer delete |
| @spec-reviewer | Brief avec 5 requirements → doit checker les 5 |
| parallel-investigations | 3 failures différentes → doit proposer parallel |
| git-worktrees | Créer worktree → vérifier .gitignore + baseline |
| branch-completion | Tester les 4 options avec/sans worktree |

### 7.2 Tests d'Intégration

| Scénario | Workflow Complet |
|----------|------------------|
| Feature standard | /brainstorm → /epci avec 2-stage review → verification → branch-completion |
| Feature large | /brainstorm → git-worktree → /epci --large → PR |
| Multi-bug debug | /debug → parallel-investigations → merge fixes |
| Quick fix | /quick avec TDD checkpoints → verification → merge |

### 7.3 Validation Scripts

```bash
# Valider nouveaux skills
python src/scripts/validate_skill.py src/skills/core/verification-before-completion/
python src/scripts/validate_skill.py src/skills/core/tdd-strict/
python src/scripts/validate_skill.py src/skills/core/parallel-investigations/
python src/scripts/validate_skill.py src/skills/core/git-worktrees/
python src/scripts/validate_skill.py src/skills/core/branch-completion/

# Valider nouvel agent
python src/scripts/validate_subagent.py src/agents/spec-reviewer.md

# Valider tout
python src/scripts/validate_all.py
```

---

## 8. Rollback et Risques

### 8.1 Risques Identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| TDD trop strict ralentit | Moyenne | Moyen | Flag --skip-tdd pour urgences |
| 2-stage review trop long | Moyenne | Moyen | Mode --quick skip spec-review |
| Worktrees confusion | Faible | Faible | Documentation claire |
| Parallel agents conflits | Faible | Moyen | Vérifier indépendance avant dispatch |

### 8.2 Plan de Rollback

**Par phase** :
- Phase 1 : Supprimer skill, retirer hooks → 30 min
- Phase 2 : Revert @implementer, supprimer tdd-strict → 1h
- Phase 3 : Supprimer @spec-reviewer, revert @code-reviewer → 1h
- Phase 4-6 : Supprimer skills → 30 min chaque

**Rollback complet** :
```bash
git revert --no-commit HEAD~N  # N = nombre de commits migration
git commit -m "Rollback SuperPowers integration"
```

### 8.3 Feature Flags

| Flag | Effet |
|------|-------|
| `--skip-tdd` | Désactiver TDD strict checkpoints |
| `--skip-spec-review` | Passer directement à @code-reviewer |
| `--no-worktree` | Désactiver proposition worktree |
| `--skip-verification` | Désactiver verification-before-completion |

---

## 9. Checklist de Migration

### Phase 1 : Fondations

- [ ] Créer `src/skills/core/verification-before-completion/SKILL.md`
- [ ] Tester skill verification isolément
- [ ] Intégrer hook post-phase-2
- [ ] Intégrer hook post-phase-3
- [ ] Tester intégration /epci
- [ ] Documenter dans CLAUDE.md

### Phase 2 : TDD Strict

- [ ] Créer `src/skills/core/tdd-strict/SKILL.md`
- [ ] Créer `src/skills/core/tdd-strict/references/anti-patterns.md`
- [ ] Modifier `src/agents/implementer.md`
- [ ] Créer `src/agents/templates/implementer-prompt.md`
- [ ] Tester cycle RED-GREEN-REFACTOR
- [ ] Tester anti-patterns detection
- [ ] Mettre à jour testing-strategy avec référence

### Phase 3 : 2-Stage Review

- [ ] Créer `src/agents/spec-reviewer.md`
- [ ] Créer `src/agents/templates/spec-reviewer-prompt.md`
- [ ] Créer `src/agents/templates/code-quality-reviewer-prompt.md`
- [ ] Modifier `src/agents/code-reviewer.md` (scope quality only)
- [ ] Modifier `src/commands/epci.md` (intégrer 2-stage)
- [ ] Tester workflow complet 2-stage
- [ ] Documenter dans CLAUDE.md

### Phase 4 : Parallélisation et Isolation

- [ ] Créer `src/skills/core/parallel-investigations/SKILL.md`
- [ ] Créer `src/skills/core/git-worktrees/SKILL.md`
- [ ] Modifier `src/commands/debug.md` (parallel detection)
- [ ] Modifier `src/commands/brainstorm.md` (worktree proposal)
- [ ] Modifier `src/commands/epci.md` (--large worktree)
- [ ] Tester parallel dispatch
- [ ] Tester worktree création + cleanup

### Phase 5 : Finalisation

- [ ] Créer `src/skills/core/branch-completion/SKILL.md`
- [ ] Intégrer dans /epci Phase 3
- [ ] Intégrer dans /quick
- [ ] Tester les 4 options
- [ ] Tester cleanup worktree

### Phase 6 : Enrichissements

- [ ] Créer `src/skills/core/debugging-strategy/references/root-cause-tracing.md`
- [ ] Créer `src/skills/core/debugging-strategy/references/defense-in-depth.md`
- [ ] Modifier `src/skills/core/debugging-strategy/SKILL.md`
- [ ] Ajouter rule "3+ fixes = question architecture"

### Finalisation

- [ ] Mettre à jour CLAUDE.md version 5.0.0
- [ ] Mettre à jour .claude/CLAUDE.md
- [ ] Exécuter `python src/scripts/validate_all.py`
- [ ] Créer tag git v5.0.0
- [ ] Documenter dans RELEASE-NOTES.md

---

## Annexes

### A. Sources SuperPowers

| Fichier Source | Usage |
|----------------|-------|
| `skills/verification-before-completion/SKILL.md` | Base pour verification |
| `skills/test-driven-development/SKILL.md` | Base pour tdd-strict |
| `skills/test-driven-development/testing-anti-patterns.md` | Référence anti-patterns |
| `skills/dispatching-parallel-agents/SKILL.md` | Base pour parallel-investigations |
| `skills/using-git-worktrees/SKILL.md` | Base pour git-worktrees |
| `skills/finishing-a-development-branch/SKILL.md` | Base pour branch-completion |
| `skills/systematic-debugging/root-cause-tracing.md` | Enrichissement debugging |
| `skills/systematic-debugging/defense-in-depth.md` | Enrichissement debugging |
| `skills/subagent-driven-development/SKILL.md` | Pattern 2-stage review |
| `skills/subagent-driven-development/implementer-prompt.md` | Template |
| `skills/subagent-driven-development/spec-reviewer-prompt.md` | Template |
| `skills/subagent-driven-development/code-quality-reviewer-prompt.md` | Template |

### B. Estimation Effort Total

| Phase | Effort | Cumul |
|-------|--------|-------|
| Phase 1 | 1-2 jours | 1-2 jours |
| Phase 2 | 2-3 jours | 3-5 jours |
| Phase 3 | 2-3 jours | 5-8 jours |
| Phase 4 | 2-3 jours | 7-11 jours |
| Phase 5 | 1-2 jours | 8-13 jours |
| Phase 6 | 1-2 jours | 9-15 jours |
| **Total** | **9-15 jours** | |

### C. Métriques de Succès

| Métrique | Avant | Cible | Mesure |
|----------|-------|-------|--------|
| Claims non vérifiés | ~20% | 0% | Audit logs |
| Tests écrits après code | ~40% | < 5% | Git history |
| Bugs post-implémentation | Baseline | -50% | Issue tracker |
| Temps debug multi-bugs | Baseline | -40% | Session logs |
| Satisfaction review | Baseline | +20% | Feedback |

---

**Document maintenu par** : Équipe EPCI
**Dernière mise à jour** : Janvier 2025
**Prochaine révision** : Après Phase 3
