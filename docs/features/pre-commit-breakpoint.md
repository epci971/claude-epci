# Feature Document — Pre-Commit Breakpoint & Hooks Reorganization

> **Slug**: `pre-commit-breakpoint`
> **Category**: STANDARD
> **Date**: 2025-12-23

---

## §1 — Functional Brief

### Context

Dans le workflow EPCI actuel, la Phase 3 (Finalisation) s'exécute automatiquement après le breakpoint de Phase 2 sans offrir de point d'arrêt avant le commit. Cela pose plusieurs problèmes :

- Pas de possibilité de validation manuelle avant commit
- Pas de support pour des comités de validation
- Le commit est implicitement obligatoire
- Les hooks `post-phase-3` attendent un `commit_hash` qui peut ne pas exister

### Objectives

1. **Ajouter un breakpoint pre-commit** dans `/epci` et `/epci-quick` permettant :
   - Validation manuelle avant commit
   - Option de finaliser sans commit
   - Modification du message de commit
   - Annulation du workflow

2. **Réorganiser le système de hooks Phase 3** :
   - Nouveau hook `pre-commit` : Documentation, mémoire projet, métriques (exécuté même sans commit)
   - Nouveau hook `post-commit` : Notifications, CI trigger (exécuté seulement si commit)
   - Hook `post-phase-3` allégé : Fin de workflow uniquement

### Detected Stack

- **Framework**: Claude Code Plugin (EPCI v3.x)
- **Language**: Markdown (commands), Python (hooks)
- **Patterns**: EPCI workflow, breakpoint pattern, hook system

### Identified Files

| File | Action | Risk | Description |
|------|--------|------|-------------|
| `src/commands/epci.md` | Modify | Medium | Ajouter breakpoint Phase 3, réorg hooks |
| `src/commands/epci-quick.md` | Modify | Low | Ajouter breakpoint pre-commit |
| `src/hooks/README.md` | Modify | Low | Documenter nouveaux hooks |
| `src/hooks/runner.py` | Modify | Medium | Ajouter types pre-commit, post-commit |
| `src/hooks/examples/pre-commit-memory.py` | Create | Low | Migrer logique mémoire depuis post-phase-3 |
| `src/hooks/examples/post-commit-notify.py` | Create | Low | Nouveau hook notifications post-commit |

### Acceptance Criteria

- [ ] Breakpoint affiché avant commit dans `/epci` Phase 3
- [ ] Breakpoint affiché avant commit dans `/epci-quick`
- [ ] 4 options disponibles : Commiter, Finaliser sans commit, Modifier message, Annuler
- [ ] Hook `pre-commit` exécuté avant le breakpoint
- [ ] Hook `post-commit` exécuté seulement si commit effectué
- [ ] Hook `post-phase-3` reste fonctionnel (fin de workflow)
- [ ] Documentation hooks mise à jour
- [ ] Exemple `pre-commit-memory.py` fonctionnel
- [ ] Rétrocompatibilité avec hooks existants

### Constraints

- Rétrocompatibilité avec les hooks `post-phase-3` existants
- Le breakpoint doit suivre le format visuel des autres breakpoints EPCI
- Les options du breakpoint doivent être en français (cohérence avec les autres)

### Out of Scope

- Migration automatique des hooks utilisateurs existants
- Modification des breakpoints Phase 1 et Phase 2
- Ajout de nouvelles options au-delà des 4 prévues

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 6
- **Estimated LOC**: ~250
- **Risk**: Medium (réorganisation hooks existants)
- **Justification**: Modification de plusieurs fichiers avec logique de hooks

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 4-6 files impacted |

---

## §2 — Implementation Plan

### Restructured Phase 3 Workflow

**BEFORE (current):**
```
Phase 3:
├── pre-phase-3 hooks
├── 1. Structured commit (message generation)
├── 2. Documentation (@doc-generator)
├── 3. PR preparation
├── 4. Learning update
├── Output §4 to Feature Document
└── post-phase-3 hooks
```

**AFTER (proposed):**
```
Phase 3:
├── pre-phase-3 hooks (unchanged)
├── 1. Generate commit message (prepare, don't execute)
├── 2. Documentation (@doc-generator)
├── 3. PR preparation
├── 4. Learning update (mémoire, métriques)
├── Output §4 to Feature Document
├── pre-commit hooks (NEW)
├── ⏸️ BREAKPOINT PRE-COMMIT (NEW)
│   ├── [1] "Commiter" → git commit → post-commit hooks
│   ├── [2] "Finaliser" → Skip commit, continue
│   ├── [3] "Modifier" → Edit message, return to breakpoint
│   └── [4] "Annuler" → Return to Phase 2
├── post-commit hooks (NEW - only if commit)
└── post-phase-3 hooks (unchanged - always at end)
```

### Hook Execution Order

| Hook | When | Always runs? |
|------|------|--------------|
| `pre-phase-3` | Before Phase 3 starts | Yes |
| `pre-commit` | After all prep, before user decision | Yes |
| `post-commit` | After git commit executed | Only if user commits |
| `post-phase-3` | End of Phase 3 | Yes |

### Impacted Files

| File | Action | Risk |
|------|--------|------|
| `src/hooks/runner.py` | Modify | Low |
| `src/commands/epci.md` | Modify | Medium |
| `src/commands/epci-quick.md` | Modify | Low |
| `src/hooks/README.md` | Modify | Low |
| `src/hooks/examples/pre-commit-memory.py` | Create | Low |
| `src/hooks/examples/post-commit-notify.py` | Create | Low |

### Tasks

1. [ ] **Update runner.py hook types** (5 min)
   - Add 'pre-commit' and 'post-commit' to VALID_HOOK_TYPES
   - File: `src/hooks/runner.py`
   - Test: `python runner.py --list`

2. [ ] **Modify epci.md Phase 3 structure** (20 min)
   - Add pre-commit hook invocation
   - Add BREAKPOINT with 4 options
   - Add conditional post-commit hook
   - File: `src/commands/epci.md`

3. [ ] **Modify epci-quick.md** (10 min)
   - Add breakpoint before "Ready to commit"
   - Same 4 options as epci.md
   - File: `src/commands/epci-quick.md`

4. [ ] **Update hooks README.md** (10 min)
   - Add pre-commit and post-commit to table
   - Document context fields
   - File: `src/hooks/README.md`

5. [ ] **Create pre-commit-memory.py** (15 min)
   - Based on post-phase-3-memory-update.py
   - Works without commit_hash
   - File: `src/hooks/examples/pre-commit-memory.py`

6. [ ] **Create post-commit-notify.py** (5 min)
   - Simple notification example
   - File: `src/hooks/examples/post-commit-notify.py`

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Existing post-phase-3 hooks break | Very Low | Hook kept unchanged |
| User confusion on options | Low | Clear French labels |
| Git commit fails | Medium | Catch error, allow retry |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: ✓
  - Consistency: ✓
  - Feasibility: ✓
  - Quality: ✓

---

## §3 — Implementation
[To be completed by /epci Phase 2]

---

## §4 — Finalization
[To be completed by /epci Phase 3]
