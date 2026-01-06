# Feature Document — Brainstorm v4.2 S03: Modes & Finish

## §1 — Brief Fonctionnel

### Context

Cette spec finalise le brainstormer v4.2 avec les modes avancés (`--random`, `--progressive`), la parallélisation @Explore et les tests de validation.

**Prérequis validés:**
- S01 Core ✅ : Session save/restore, energy checkpoints, format 3-5 questions
- S02 Techniques ✅ : 20 techniques documentées, commande `technique [x]`, mapping phases

**Source:** `docs/briefs/brainstorm-v4/specs/S03-modes-finish.md`

### Objective

Implémenter les deux derniers flags avancés du brainstormer v4.2:
1. `--random` : Sélection aléatoire pondérée de techniques
2. `--progressive` : 3 phases structurées (Divergent → Transition → Convergent)

Plus la parallélisation, les tests unitaires et les exemples de sessions.

### Functional Specifications

#### Flag --random

**Comportement:**
- Sélection aléatoire de techniques parmi celles disponibles
- Pondération par phase:
  - Divergent → favorise Ideation (0.4), Perspective (0.3), Breakthrough (0.2), Analysis (0.1)
  - Convergent → favorise Analysis (0.5), Ideation (0.2), Perspective (0.2), Breakthrough (0.1)
- Exclut les techniques déjà utilisées dans la session

**Usage:**
```
/brainstorm --random "améliorer le système de cache"
```

**Affichage:**
```
-------------------------------------------------------
🎲 RANDOM MODE | Technique: SCAMPER (Ideation)
-------------------------------------------------------
[Questions SCAMPER appliquées au contexte]
```

#### Flag --progressive

**Comportement:**
- 3 phases structurées avec transition automatique:
  1. **Divergent** (EMS 0-50): Focus exploration, techniques Ideation
  2. **Transition** (EMS ~50): Energy check obligatoire + résumé
  3. **Convergent** (EMS 50-100): Focus décisions, techniques Analysis

**Flow:**
```
Phase 1: DIVERGENT (EMS 0-50)
├── Techniques: Ideation, Perspective, Breakthrough
├── Questions ouvertes
└── À EMS 50 → TRANSITION

Phase 2: TRANSITION
├── Energy check obligatoire
├── Résumé mi-parcours
├── Validation direction
└── → CONVERGENT

Phase 3: CONVERGENT (EMS 50-100)
├── Techniques: Analysis
├── Questions décisionnelles
└── À EMS 70+ → @planner disponible
```

**Usage:**
```
/brainstorm --progressive "nouveau module de paiement"
```

#### Parallélisation @Explore

**Comportement:**
- Lancer @Explore en background au démarrage
- Continuer avec questions pendant que @Explore analyse
- Intégrer résultats @Explore quand disponibles
- Pré-calculer suggestions techniques en parallèle

**Implémentation:**
```markdown
1. En parallèle:
   - Task A: Lancer @Explore (Task tool, background)
   - Task B: Afficher premières questions de cadrage

2. Quand @Explore termine:
   - Intégrer fichiers pertinents dans le contexte
   - Enrichir suggestions avec patterns détectés
```

### Business Rules

1. `--random` et `--progressive` sont mutuellement exclusifs
2. `--random` respecte la phase actuelle pour la pondération
3. `--progressive` force la transition à EMS 50 (pas d'override possible)
4. La parallélisation @Explore ne change pas le comportement visible (best-effort)

### Technical Constraints

- Stack: Plugin Claude Code (Markdown + Python)
- Les flags doivent être ajoutés dans le frontmatter de `brainstorm.md`
- Tests avec pytest, structure conforme à `src/scripts/test_*.py`
- Exemples en YAML, format conforme à `references/session-format.md`

### Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S03-AC1 | --random fonctionne | Flag sélectionne technique aléatoire pondérée |
| S03-AC2 | --random exclut utilisées | Techniques déjà utilisées ne sont pas re-sélectionnées |
| S03-AC3 | --progressive 3 phases | Transition automatique à EMS 50 |
| S03-AC4 | @Explore parallélisé | Questions affichées pendant que @Explore tourne |
| S03-AC5 | Tests passent | 100% tests session + techniques + modes |
| S03-AC6 | Exemples valides | 3 fichiers exemples YAML valides |
| S03-AC7 | Pas de régression | Toutes features v4.1 fonctionnent encore |

### Files Impacted

**Modifications:**
| Fichier | Changements |
|---------|-------------|
| `src/commands/brainstorm.md` | Flags --random, --progressive, parallélisation |

**Créations:**
| Fichier | Description |
|---------|-------------|
| `src/scripts/test_brainstorm_session.py` | Tests unitaires |
| `docs/briefs/brainstorm-v4/examples/session-example-standard.yaml` | Exemple session standard |
| `docs/briefs/brainstorm-v4/examples/session-example-random.yaml` | Exemple session random |
| `docs/briefs/brainstorm-v4/examples/session-example-progressive.yaml` | Exemple session progressive |

### Exploration Summary

**Stack:** Plugin Claude Code (Markdown + Python)
**Patterns:** Skill-based architecture, project-memory, subagents
**Complexity:** STANDARD (4-10 fichiers, tests requis)
**Estimated time:** 2-3h

### Memory Summary

- Convention commits: conventional commits avec Co-Author EPCI
- Tests: pytest avec fixtures dans conftest.py
- Validation: `python src/scripts/validate_all.py`

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk |
|------|--------|------|
| `src/commands/brainstorm.md` | Modify | Low |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Low |
| `src/scripts/test_brainstorm_session.py` | Create | Low |
| `docs/briefs/brainstorm-v4/examples/session-example-standard.yaml` | Create | Low |
| `docs/briefs/brainstorm-v4/examples/session-example-random.yaml` | Create | Low |
| `docs/briefs/brainstorm-v4/examples/session-example-progressive.yaml` | Create | Low |

### Tasks

1. [ ] **Add flags to frontmatter** (5 min)
   - File: `src/commands/brainstorm.md:8`
   - Action: Add `--random` and `--progressive` to argument-hint
   - Test: Visual verification

2. [ ] **Add flags to Flags table** (5 min)
   - File: `src/commands/brainstorm.md:788-795`
   - Action: Add 2 rows for `--random` and `--progressive`
   - Test: Visual verification

3. [ ] **Add --random Mode section** (10 min)
   - File: `src/commands/brainstorm.md` (insert after line 823, before line 825 Output section)
   - Action: Add detailed documentation:
     - Weighted selection logic by phase (Divergent: Ideation 0.4, Perspective 0.3, Breakthrough 0.2, Analysis 0.1; Convergent inverse)
     - Exclude techniques from session.techniques_used
     - Display format with 🎲 RANDOM MODE header
     - Document how techniques_used is updated when technique is selected
   - Test: Documentation completeness

4. [ ] **Add --progressive Mode section** (10 min)
   - File: `src/commands/brainstorm.md` (insert after --random Mode section)
   - Action: Add detailed documentation:
     - 3-phase structure (Divergent EMS 0-50 → Transition → Convergent EMS 50-100)
     - Forced energy check + transition at EMS 50
     - Phase-specific technique auto-selection
   - Test: Documentation completeness

5. [ ] **Add @Explore parallelization to Phase 1** (10 min)
   - File: `src/commands/brainstorm.md:96-98`
   - Action: Modify step 2 "Analyser le codebase" to:
     - Launch @Explore with Task tool using `run_in_background: true`
     - Continue with steps 3-6 while @Explore runs
     - Integrate @Explore results when available (before step 7)
   - Test: Documentation clarity

6. [ ] **Create unit tests** (30 min)
   - File: `src/scripts/test_brainstorm_session.py` (CREATE)
   - Action: Create pytest file following project conventions:
     - `TestSessionFormat`: YAML schema validation with tmp_path fixtures
     - `TestTechniques`: Validate 4 technique files in `references/techniques/*.md`
     - `TestModes`: --random weighted selection, --progressive phase transitions
   - Test: `pytest src/scripts/test_brainstorm_session.py -v`

7. [ ] **Create session examples** (15 min)
   - Files: `docs/briefs/brainstorm-v4/examples/` (CREATE directory + 3 files)
     - `session-example-standard.yaml`: Standard session divergent→convergent
     - `session-example-random.yaml`: Session with random technique selection
     - `session-example-progressive.yaml`: Session with 3-phase progression
   - Action: Follow `references/session-format.md` schema, add mode-specific fields
   - Test: YAML validation

8. [ ] **Update SKILL.md frontmatter** (5 min)
   - File: `src/skills/core/brainstormer/SKILL.md`
   - Action: Update description to mention --random and --progressive flags (CLI flags, not interactive commands)
   - Test: Documentation consistency

### Dependencies

```
Task 1 ──┬──→ Task 3 ──→ Task 4 ──→ Task 8
Task 2 ──┘                │
                          └──→ Task 5

Task 6 (independent, can run in parallel)
Task 7 (independent, can run in parallel)
```

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking existing functionality | Low | Documentation-only changes to flows |
| Invalid YAML examples | Low | Validate against session-format.md schema |
| Test failures | Medium | Run pytest after creating test file |

### Validation

- **@plan-validator**: APPROVED (after revision)

---

## §3 — Implementation & Finalization

### Progress

- [x] Task 1 — Add flags to frontmatter
- [x] Task 2 — Add flags to Flags table
- [x] Task 3 — Add --random Mode section
- [x] Task 4 — Add --progressive Mode section
- [x] Task 5 — Add @Explore parallelization
- [x] Task 6 — Create unit tests (24 tests)
- [x] Task 7 — Create session examples (3 YAML files)
- [x] Task 8 — Update SKILL.md frontmatter

### Tests

```
Python syntax validation: OK
Test count: 24 tests
- TestSessionFormat: 11 tests
- TestTechniques: 5 tests
- TestModes: 8 tests
```

### Reviews

- **@code-reviewer**: APPROVED_WITH_FIXES (0 Critical, 4 Important fixed, 5 Minor)
- **@security-auditor**: N/A (no auth/security patterns detected)
- **@qa-reviewer**: N/A (< 5 test files)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| Schema | +1 file modified | Added mode-specific fields to session-format.md |
| Tests | +2 tests added | Added invalid session test and mode field test |

### Documentation

- **brainstorm.md**: Updated with --random and --progressive mode sections
- **SKILL.md**: Updated description with new flags
- **session-format.md**: Added mode-specific state fields

### PR Ready

- Branch: `master` (current)
- Tests: ✅ Syntax validated
- Lint: ✅ Clean
- Docs: ✅ Up to date
