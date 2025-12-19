# Feature Document — Brainstormer Feature Discovery

> **Slug**: `brainstormer-feature-discovery`
> **Category**: STANDARD
> **Date**: 2025-12-19

---

## §1 — Functional Brief

### Context

Brainstormer est un outil de **découverte de feature** qui transforme une idée vague en un **brief fonctionnel complet**, prêt à être consommé par le workflow EPCI. Il se positionne en amont du workflow EPCI standard, permettant aux utilisateurs de clarifier et structurer leurs besoins avant de passer à l'implémentation.

Le CDC complet est disponible dans `docs/migration/30-40/brainstormer-cdc.md`.

### Detected Stack

- **Framework**: Claude Code Plugin v3.8.3
- **Language**: Python3 (scripts), Markdown (components)
- **Patterns**: SKILL.md + references/, commands/*.md, YAML frontmatter
- **Tools**: Validation scripts (validate_skill.py, validate_command.py)

### Identified Files

| File | Action | Risk |
|------|--------|------|
| `src/commands/brainstorm.md` | Create | Low |
| `src/skills/core/brainstormer/SKILL.md` | Create | Low |
| `src/skills/core/brainstormer/references/ems-system.md` | Create | Low |
| `src/skills/core/brainstormer/references/frameworks.md` | Create | Low |
| `src/skills/core/brainstormer/references/brief-format.md` | Create | Low |

### Dependencies (Verified)

| Skill | Status | Usage |
|-------|--------|-------|
| `project-memory-loader` | ✓ Exists | Charger contexte projet |
| `architecture-patterns` | ✓ Exists | Suggestions architecture |
| `clarification-intelligente` | ✓ Exists | Système de questions intelligentes |

### Acceptance Criteria

- [ ] Command `/brainstorm` créée et valide (validate_command.py pass)
- [ ] Skill `brainstormer` créé et valide (validate_skill.py pass)
- [ ] 3 références créées (ems-system.md, frameworks.md, brief-format.md)
- [ ] Tous les fichiers suivent les patterns existants du projet
- [ ] validate_all.py passe sans erreur

### Constraints

- Token limit: < 5000 tokens par fichier
- Description formula: "Use when:" + "Not for:" obligatoires
- Nom kebab-case ≤ 64 caractères
- YAML frontmatter valide

### Out of Scope

- Mise à jour du README.md du plugin (section 6.1 du CDC)
- Tests fonctionnels interactifs (section 7.3 du CDC)
- Intégration avec système de personas (futur F09)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 5
- **Estimated LOC**: ~1000
- **Risk**: Low
- **Justification**: Contenu pré-spécifié dans CDC, patterns existants à suivre, dépendances vérifiées

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 5 fichiers (range 4-10) |

### Source Document

Le contenu exact à utiliser provient du CDC:
- Section 3.2: `commands/brainstorm.md`
- Section 4.2: `skills/core/brainstormer/SKILL.md`
- Section 5.1: `references/ems-system.md`
- Section 5.2: `references/frameworks.md`
- Section 5.3: `references/brief-format.md`

---

## §2 — Implementation Plan

### Impacted Files

| # | File | Action | Risk | Source |
|---|------|--------|------|--------|
| 1 | `src/skills/core/brainstormer/` | Create dir | None | - |
| 2 | `src/skills/core/brainstormer/references/` | Create dir | None | - |
| 3 | `src/commands/brainstorm.md` | Create | Low | CDC §3.2 |
| 4 | `src/skills/core/brainstormer/SKILL.md` | Create | Low | CDC §4.2 |
| 5 | `src/skills/core/brainstormer/references/ems-system.md` | Create | Low | CDC §5.1 |
| 6 | `src/skills/core/brainstormer/references/frameworks.md` | Create | Low | CDC §5.2 |
| 7 | `src/skills/core/brainstormer/references/brief-format.md` | Create | Low | CDC §5.3 |

### Tasks

1. [ ] **T1: Create directory structure** (2 min)
   - Create `src/skills/core/brainstormer/`
   - Create `src/skills/core/brainstormer/references/`
   - Test: directories exist

2. [ ] **T2: Create command brainstorm.md** (5 min)
   - File: `src/commands/brainstorm.md`
   - Content: CDC Section 3.2
   - Test: `python src/scripts/validate_command.py src/commands/brainstorm.md`

3. [ ] **T3: Create SKILL.md** (5 min)
   - File: `src/skills/core/brainstormer/SKILL.md`
   - Content: CDC Section 4.2
   - Test: `python src/scripts/validate_skill.py src/skills/core/brainstormer/`

4. [ ] **T4: Create ems-system.md reference** (5 min)
   - File: `src/skills/core/brainstormer/references/ems-system.md`
   - Content: CDC Section 5.1
   - Test: file exists, valid markdown

5. [ ] **T5: Create frameworks.md reference** (5 min)
   - File: `src/skills/core/brainstormer/references/frameworks.md`
   - Content: CDC Section 5.2
   - Test: file exists, valid markdown

6. [ ] **T6: Create brief-format.md reference** (5 min)
   - File: `src/skills/core/brainstormer/references/brief-format.md`
   - Content: CDC Section 5.3
   - Test: file exists, valid markdown

7. [ ] **T7: Run full validation** (3 min)
   - Run: `python src/scripts/validate_all.py`
   - Expected: All checks pass

### Dependencies

```
T1 → T2, T3, T4, T5, T6 (directories needed first)
T2, T3, T4, T5, T6 → T7 (all files needed for validation)
```

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Token limit exceeded | Low | Content pre-measured in CDC |
| YAML syntax error | Low | Copy exact content from CDC |
| Validation script fail | Low | Fix based on error message |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: ✅ All 5 files covered
  - Consistency: ✅ Dependencies ordered correctly
  - Feasibility: ✅ ~30 min total, realistic
  - Quality: ✅ Tests defined for each task

---

## §3 — Implementation

### Progress

- [x] T1 — Create directory structure
- [x] T2 — Create command brainstorm.md
- [x] T3 — Create SKILL.md
- [x] T4 — Create ems-system.md reference
- [x] T5 — Create frameworks.md reference
- [x] T6 — Create brief-format.md reference
- [x] T7 — Run validation

### Validation Results

```
brainstorm.md: PASSED (5/5 checks, ~967 tokens)
brainstormer skill: PASSED (6/6 checks, ~1154 tokens)
```

### Reviews

- **@code-reviewer**: APPROVED (0 Critical, 0 Important, 3 Minor)
  - Minor: Emoji handling uses text names instead of actual emojis
  - Minor: Token efficiency could be improved
  - Minor: French language may limit international adoption
- **@security-auditor**: N/A (no sensitive files)
- **@qa-reviewer**: N/A (no complex tests)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| - | None | Implementation matches plan exactly |

---

## §4 — Finalization

### Commit

```
feat(brainstormer): add feature discovery skill and command

- Add /brainstorm command for guided feature discovery
- Create brainstormer skill with 3-phase workflow (Init, Iterate, Finish)
- Add EMS (Exploration Maturity Score) system with 5 weighted axes
- Add analysis frameworks reference (MoSCoW, 5 Whys, SWOT, Scoring)
- Add brief format template for EPCI-ready output
- Include Feature Document for traceability

Refs: docs/features/brainstormer-feature-discovery.md
```

### Files Committed

| File | Lines |
|------|-------|
| `src/commands/brainstorm.md` | +124 |
| `src/skills/core/brainstormer/SKILL.md` | +178 |
| `src/skills/core/brainstormer/references/ems-system.md` | +103 |
| `src/skills/core/brainstormer/references/frameworks.md` | +130 |
| `src/skills/core/brainstormer/references/brief-format.md` | +194 |
| `docs/features/brainstormer-feature-discovery.md` | +200 |
| **Total** | **+992** |

### Documentation

- **@doc-generator**: N/A (self-documenting markdown components)
- **Feature Document**: Complete (§1-§4)

### Status

- Branch: `master`
- Commit: `0550e65`
- Tests: ✅ All validations passed
- Ready for: Use immediately with `/brainstorm`
