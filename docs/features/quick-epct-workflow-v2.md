# Feature Document — Quick EPCT Workflow v2.0

> **Slug**: `quick-epct-workflow-v2`
> **Category**: STANDARD
> **Date**: 2025-12-31

---

## §1 — Functional Brief

### Context

La commande `/quick` actuelle gère les tâches TINY et SMALL avec un workflow simple mais non optimisé. L'objectif est de la transformer en workflow autonome ultra-rapide suivant la logique EPCT (Explore, Plan, Code, Test), avec switch de modèles adaptatif (Haiku/Sonnet), modes de pensée adaptés par phase, et autonomie maximale avec breakpoints minimaux.

### Detected Stack

- **Framework**: Claude Code Plugin v4.4.0
- **Language**: Python 3 / Markdown
- **Patterns**: Turbo mode, Model switching, Subagents (@Explore, @planner, @implementer, @clarifier)

### Acceptance Criteria

- [ ] `/quick` exécute workflow EPCT complet (4 phases)
- [ ] Switch modèles Haiku/Sonnet fonctionne selon seuils
- [ ] Breakpoint léger avec auto-continue 3s
- [ ] Flag `--autonomous` skip breakpoint
- [ ] Flag `--quick-turbo` force Haiku partout
- [ ] Subagents invoqués selon matrice complexité
- [ ] Thinking adaptatif activé sur erreurs
- [ ] Session JSON persistée dans .project-memory/sessions/
- [ ] `/brief` route TINY directement vers `/quick --autonomous`
- [ ] Tests passent, lint OK
- [ ] Documentation flags mise à jour (F13)

### Constraints

- Performance: Workflow TINY < 30s, SMALL < 90s
- Contexte: Subagents pour préserver contexte principal
- Compatibilité: Flags existants (`--turbo`, `--safe`) respectés
- Rétrocompatibilité: `/quick` sans flags = comportement actuel + optimisations

### Out of Scope

- Modification de `/epci` (future itération)
- Implémentation de `/commit` (feature séparée)
- Wave orchestration (réservé à LARGE)
- MCP integration spécifique (hérite de flags existants)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 6
- **Estimated LOC**: ~400-500
- **Risk**: Medium (refonte majeure /quick)
- **Justification**: 6 fichiers, workflow structuré, subagents existants réutilisés

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 6 fichiers impactés (range 3-10) |

### Memory Summary

- **Project**: tools-claude-code-epci (claude-code-plugin)
- **Stack**: Claude Code Plugin v4.4.0
- **Conventions**: kebab-case files, kebab-case.md commands
- **Velocity**: 9 features completed

---

## §2 — Implementation Plan

### Phase 1: Planning

#### 2.1 Fichiers à modifier

| Fichier | Action | Priorité | LOC estimé |
|---------|--------|----------|------------|
| `src/commands/quick.md` | Refonte complète workflow EPCT | P0 | ~200 |
| `src/commands/brief.md` | Ajout routing optimisé TINY/SMALL | P0 | ~30 |
| `src/settings/flags.md` | Ajout section F13 Quick Workflow Flags | P0 | ~50 |
| `src/agents/implementer.md` | Vérifier model: sonnet, micro-validation | P1 | ~20 |
| `src/agents/planner.md` | Vérifier intégration /quick | P1 | ~20 |
| `src/skills/core/project-memory/SKILL.md` | Ajout schema session JSON | P2 | ~40 |

#### 2.2 Architecture EPCT pour /quick

```
/quick "description" [--autonomous] [--quick-turbo]
    │
    ▼
[E] EXPLORE (Haiku, ~5-10s)
    - @Explore: scan fichiers, stack, patterns
    - @clarifier: si ambiguïté détectée (SMALL only)
    - Guard: complexité > SMALL → escalade /epci
    │
    ▼
[P] PLAN (Haiku TINY | Sonnet + "think" SMALL, ~10-15s)
    - Génération 3-5 tâches atomiques
    - @planner: si SMALL complexe
    - BP léger (3s auto-continue) [sauf --autonomous]
    - Persistence session JSON
    │
    ▼
[C] CODE (Sonnet, variable)
    - @implementer: exécution tâches
    - Micro-validation après chaque tâche
    - Auto-fix lint/format
    - Si erreur: "think" + retry (max 2x)
    │
    ▼
[T] TEST (Haiku validation | Sonnet + "think" si fix, ~5-10s)
    - Run tests existants
    - Lint/format check
    - Cohérence finale
    │
    ▼
[RESUME FINAL]
    - Fichiers modifiés, tests, temps
    - Suggestion: /commit
```

#### 2.3 Matrice modèles par phase

| Phase | TINY | SMALL | Erreur/Retry |
|-------|------|-------|--------------|
| Explore | Haiku | Haiku | - |
| Plan | Haiku | Sonnet + "think" | "think hard" |
| Code | Haiku | Sonnet | Sonnet + "think" |
| Test | Haiku | Haiku | Sonnet + "think hard" |

#### 2.4 Matrice subagents par complexité

| Phase | TINY | SMALL | SMALL+ (proche limite) |
|-------|------|-------|------------------------|
| Explore | - | @Explore (Haiku) | @Explore + @clarifier |
| Plan | - | - | @planner (Sonnet) |
| Code | - | @implementer | @implementer |
| Test | - | - | - |

#### 2.5 Nouveaux flags (F13)

| Flag | Effet | Auto-trigger |
|------|-------|--------------|
| `--autonomous` | Skip BP plan, exécution continue | TINY détecté |
| `--quick-turbo` | Haiku partout (TINY only) | Jamais (explicit) |
| `--no-bp` | Alias de `--autonomous` | - |

#### 2.6 Session persistence schema

```json
{
  "timestamp": "2025-12-31T14:30:22Z",
  "description": "fix typo in README",
  "complexity": "TINY",
  "plan": [
    {"task": "Fix typo line 42", "status": "completed"}
  ],
  "files_modified": ["README.md"],
  "duration_seconds": 45,
  "models_used": {"explore": "haiku", "plan": "haiku", "code": "haiku"},
  "retries": 0
}
```

#### 2.7 Tâches d'implémentation (révisées)

**T1: Refonte `src/commands/quick.md`** (atomisé en 6 sous-tâches)

1. [ ] **T1a**: Add EPCT phase structure (E-P-C-T sections) (~40 LOC, 10 min)
   - File: `src/commands/quick.md`
   - Acceptance: 4 phases clairement définies avec sections markdown

2. [ ] **T1b**: Add model matrix table (Haiku/Sonnet per phase) (~30 LOC, 5 min)
   - File: `src/commands/quick.md`
   - Acceptance: Matrice visible, règles claires TINY vs SMALL

3. [ ] **T1c**: Add subagent matrix per complexity (~30 LOC, 5 min)
   - File: `src/commands/quick.md`
   - Acceptance: Matrice TINY/SMALL/SMALL+ avec subagents associés

4. [ ] **T1d**: Implement lightweight breakpoint with 3s auto-continue (~50 LOC, 10 min)
   - File: `src/commands/quick.md`
   - Acceptance: Format BP léger documenté, comportement timeout décrit

5. [ ] **T1e**: Add session persistence logic (write to sessions/) (~30 LOC, 10 min)
   - File: `src/commands/quick.md`
   - Acceptance: Instructions de persistence session JSON

6. [ ] **T1f**: Update output/resume format (~20 LOC, 5 min)
   - File: `src/commands/quick.md`
   - Acceptance: Format QUICK COMPLETE documenté

**Autres tâches:**

7. [ ] **T2**: Ajout section F13 dans `src/settings/flags.md` (~50 LOC, 10 min)
   - Document `--autonomous`, `--quick-turbo`, `--no-bp`
   - Acceptance: Section F13 visible, flags documentés avec auto-trigger

8. [ ] **T3**: Modifier `src/commands/brief.md` — routing optimisé (~30 LOC, 10 min)
   - Add TINY → `/quick --autonomous` direct route
   - Acceptance: Routing table mise à jour

9. [ ] **T4**: Vérifier/ajuster `src/agents/implementer.md` (~20 LOC, 5 min)
   - Add note: "Used by /quick for SMALL features"
   - Acceptance: Note ajoutée dans When to Use

10. [ ] **T5**: Vérifier/ajuster `src/agents/planner.md` (~20 LOC, 5 min)
    - Add note: "Used by /quick for SMALL+ complexity"
    - Acceptance: Note ajoutée dans When to Use

11. [ ] **T6**: Ajout schema session dans `src/skills/core/project-memory/SKILL.md` (~40 LOC, 10 min)
    - Document `.project-memory/sessions/` directory
    - Add session JSON schema with write instructions
    - Acceptance: Section sessions/ visible avec schema complet

12. [ ] **T7**: Validation finale (~5 min)
    - Run `python src/scripts/validate_command.py src/commands/quick.md`
    - Verify cross-references between files
    - Acceptance: Validation pass, no errors

#### 2.8 Dépendances

```
T1a → T1b → T1c → T1d → T1e → T1f
                              ↓
T2 ────────────────────────→ T7
T3 ────────────────────────→ T7
T4 ────────────────────────→ T7
T5 ────────────────────────→ T7
T6 ────────────────────────→ T7
```

Note: T2-T6 peuvent être exécutées en parallèle après T1f.

#### 2.9 Stratégie de validation

| Critère d'acceptation | Validation |
|----------------------|------------|
| `/quick` exécute workflow EPCT | Vérifier 4 sections E-P-C-T dans quick.md |
| Switch modèles fonctionne | Vérifier matrice modèles dans quick.md |
| BP léger 3s auto-continue | Vérifier format BP et instructions timeout |
| `--autonomous` skip BP | Vérifier documentation flag dans flags.md |
| `--quick-turbo` force Haiku | Vérifier documentation flag dans flags.md |
| Session JSON persistée | Vérifier schema dans project-memory SKILL |
| `/brief` route TINY | Vérifier routing table dans brief.md |

#### 2.10 Interactions flags

| Combinaison | Comportement |
|-------------|-------------|
| `--autonomous` seul | Skip BP plan, exécution continue |
| `--quick-turbo` seul | Haiku partout (TINY only, erreur si SMALL) |
| `--autonomous --quick-turbo` | Skip BP + Haiku partout |
| `--turbo --autonomous` | `--turbo` prend précédence (workflow turbo existant) |
| `--safe --autonomous` | `--safe` gagne, breakpoints maintenus |

---

## §3 — Implementation & Finalization

### Progress
- [x] T1a — Add EPCT phase structure
- [x] T1b — Add model matrix table
- [x] T1c — Add subagent matrix per complexity
- [x] T1d — Implement lightweight breakpoint with 3s auto-continue
- [x] T1e — Add session persistence logic
- [x] T1f — Update output/resume format
- [x] T2 — Add F13 section in flags.md
- [x] T3 — Modify brief.md routing
- [x] T4 — Verify/adjust implementer.md
- [x] T5 — Verify/adjust planner.md
- [x] T6 — Add session schema in project-memory SKILL.md
- [x] T7 — Final validation (PASSED 5/5 checks)

### Files Modified
| File | LOC Added | LOC Removed |
|------|-----------|-------------|
| `src/commands/quick.md` | ~320 | ~180 |
| `src/settings/flags.md` | ~75 | 0 |
| `src/commands/brief.md` | ~12 | ~2 |
| `src/agents/implementer.md` | ~5 | ~2 |
| `src/agents/planner.md` | ~5 | ~2 |
| `src/skills/core/project-memory/SKILL.md` | ~65 | 0 |

### Reviews
- **@code-reviewer**: APPROVED_WITH_FIXES (0 Critical, 0 Important, 5 Minor)
  - Minor fixes applied: subagent invocation syntax, flag alias clarification, filename format

### Deviations
| Task | Deviation | Justification |
|------|-----------|---------------|
| T1 | +140 LOC vs estimate | More comprehensive documentation for clarity |

### Commit Message (Prepared)
```
feat(quick): implement EPCT workflow with adaptive model switching

- Add 4-phase EPCT structure (Explore, Plan, Code, Test)
- Add model matrix (Haiku/Sonnet) per phase and complexity
- Add subagent matrix per complexity (TINY/SMALL/SMALL+)
- Add lightweight breakpoint with 3s auto-continue
- Add session persistence in .project-memory/sessions/
- Add --autonomous and --quick-turbo flags (F13)
- Update /brief routing for TINY → /quick --autonomous
- Update @implementer and @planner with /quick notes
- Add sessions/ schema to project-memory skill

Refs: docs/features/quick-epct-workflow-v2.md
```

### Documentation
- Feature Document: Complete (§1, §2, §3)
- Flags: F13 section added to flags.md
- Agents: Integration notes added

### Validation
- validate_command.py: PASSED (5/5 checks)
- @code-reviewer: APPROVED_WITH_FIXES
- @plan-validator: APPROVED
