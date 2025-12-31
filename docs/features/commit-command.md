# Feature Document — Commande `/commit` unifiée

> **Slug**: `commit-command`
> **Category**: STANDARD
> **Date**: 2025-01-01

---

## §1 — Functional Brief

### Context

Actuellement, la logique de commit est **dupliquée** entre `/epci` (Phase 3, lignes 630-695) et partiellement absente ailleurs. `/quick` référence déjà `/commit` (ligne 392) mais la commande n'existe pas. `/debug` n'a aucune intégration commit.

Cette fragmentation pose des problèmes de maintenance et d'incohérence. L'objectif est de créer une commande `/commit` unifiée qui centralise toute la logique Git commit.

### Detected Stack

- **Framework**: Claude Code Plugin v4.4.0
- **Language**: Markdown commands, Python hooks
- **Patterns**: command-pattern, hooks-system, conventional-commits, breakpoints

### Acceptance Criteria

- [ ] `/commit` fonctionne en standalone (mode dégradé sans contexte JSON)
- [ ] `/commit` fonctionne avec contexte `.epci-commit-context.json`
- [ ] `/epci` délègue le commit à `/commit` via génération du contexte JSON
- [ ] `/quick` fonctionne avec `/commit` (référence existante ligne 392)
- [ ] `/debug --commit` génère contexte JSON et propose `/commit`
- [ ] Hooks pre-commit/post-commit déclenchés via runner.py
- [ ] Cleanup automatique du fichier JSON après commit réussi
- [ ] Format Conventional Commits respecté

### Constraints

- Réutiliser le hooks system existant (`src/hooks/runner.py`)
- Suivre le pattern des commandes existantes (front-matter, Overview, Process, Output)
- Format Conventional Commits depuis `git-workflow` skill
- Breakpoint PRE-COMMIT obligatoire sauf avec `--turbo` ou `--auto-commit`

### Out of Scope

- Modification du skill `git-workflow` (optionnel, non requis)
- Intégration avec GitHub/GitLab API (PR creation)
- Support multi-commit (batch commits)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 4
  - Créer: `src/commands/commit.md` (~300 LOC)
  - Modifier: `src/commands/epci.md` (~50 LOC)
  - Modifier: `src/commands/quick.md` (~20 LOC)
  - Modifier: `src/commands/debug.md` (~30 LOC)
- **Estimated LOC**: ~400
- **Risk**: Medium (modification de workflows existants)
- **Justification**: 4 fichiers impactés, intégration avec hooks system existant, modification de commandes critiques

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 4 fichiers impactés |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin v4.4.0
- **Conventions**: kebab-case commands, SKILL.md format
- **Velocity**: 9 features completed

### Decisions from Brief Analysis

| Question | Decision |
|----------|----------|
| Emplacement fichier contexte JSON | Racine projet (`.epci-commit-context.json`) — plus visible, cleanup automatique |
| Comportement --amend | Modification complète du message permise (type/scope/description) |
| Timing cleanup JSON | Immédiat après commit réussi (évite commits avec vieux contexte) |

### Architecture Decisions

1. **Fichier pont** `.epci-commit-context.json` à la racine projet
2. **Réutilisation** du hooks system existant (pre-commit, post-commit)
3. **Pattern command** identique aux autres commandes EPCI
4. **Backward compatibility** : epci.md garde un fallback si /commit indisponible

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | LOC |
|------|--------|------|-----|
| `src/commands/commit.md` | Create | Low | ~300 |
| `src/commands/epci.md` | Modify | Medium | ~50 |
| `src/commands/quick.md` | Modify | Low | ~20 |
| `src/commands/debug.md` | Modify | Low | ~30 |

### Tasks

1. [x] **Create `src/commands/commit.md`** (15 min)
   - Front-matter: description, argument-hint, allowed-tools
   - Overview: Centralized commit logic, two modes (context-rich, degraded)
   - Arguments: `--auto-commit`, `--amend`, `--no-hooks`, `--dry-run`
   - Process: Context detection → Message generation → Breakpoint → Execution → Cleanup
   - Test: Command follows EPCI command pattern

2. [ ] **Modify `src/commands/epci.md`** (10 min)
   - Lines 620-700: Replace inline commit with delegation
   - Generate `.epci-commit-context.json` with feature context
   - Replace inline breakpoint with: "→ Lancez `/commit` pour finaliser"
   - Keep post-phase-3 hooks execution
   - Test: epci.md functions end-to-end

3. [ ] **Modify `src/commands/quick.md`** (5 min)
   - Lines 385-420: Add context JSON generation before completion
   - Update output: "Contexte commit préparé → /commit"
   - Test: quick.md completion shows /commit reference

4. [ ] **Modify `src/commands/debug.md`** (5 min)
   - Add `--commit` flag to Arguments table
   - Add section after fix verification for commit context generation
   - Test: debug.md works with and without --commit flag

### JSON Schema (`.epci-commit-context.json`)

```json
{
  "source": "epci|quick|debug",
  "type": "feat|fix|refactor|docs|style|test|chore|perf|ci",
  "scope": "module-name",
  "description": "what was done",
  "files": ["file1.ts", "file2.ts"],
  "featureDoc": "path/to/feature-doc.md",
  "breaking": false,
  "ticket": "JIRA-123"
}
```

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking existing epci workflow | Medium | Keep inline fallback if /commit unavailable |
| JSON schema incompatibility | Low | Consistent schema across all sources |
| Hook integration issues | Low | Reuse existing hook system (runner.py) |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: 7/7 acceptance criteria covered
  - Consistency: Dependencies properly ordered (Task 1 first)
  - Feasibility: ~35 min total (realistic for STANDARD)
  - Quality: Follows EPCI patterns

---

## §3 — Implementation & Finalization

### Progress

- [x] Task 1 — Create `src/commands/commit.md` (~300 LOC)
- [x] Task 2 — Modify `src/commands/epci.md` (delegation to /commit)
- [x] Task 3 — Modify `src/commands/quick.md` (context JSON generation)
- [x] Task 4 — Modify `src/commands/debug.md` (--commit flag)

### Files Modified

| File | Action | Lines Changed |
|------|--------|---------------|
| `src/commands/commit.md` | Created | +295 |
| `src/commands/epci.md` | Modified | -47, +25 |
| `src/commands/quick.md` | Modified | +19 |
| `src/commands/debug.md` | Modified | +23 |

### Reviews

- **@code-reviewer**: APPROVED_WITH_FIXES
  - 0 Critical issues
  - 1 Important issue (fixed: removed inline commit message from epci.md §3 output)
  - 3 Minor suggestions (documentation consistency)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| None | - | Implementation followed plan exactly |

### Documentation

- **Feature Document**: Updated with §2 (Plan) and §3 (Implementation)
- **Commands**: All 4 commands properly documented with front-matter

### PR Ready

- Branch: `master`
- Tests: N/A (Markdown commands)
- Lint: N/A
- Docs: ✅ Up to date
