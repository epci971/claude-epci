# Feature Document — S02 Brainstorm Techniques Library

> **Created**: 2026-01-06
> **Source**: `docs/briefs/brainstorm-v4/specs/S02-techniques.md`
> **Complexity**: STANDARD
> **Estimated effort**: 3 jours

---

## §1 — Functional Brief

### Context

Le brainstormer EPCI v4.1 dispose de 5 frameworks d'analyse (MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem). L'analyse comparative avec BMAD v6 (62 techniques) montre un écart significatif.

Cette spec implémente l'extension de la bibliothèque à 20 techniques réparties en 4 catégories, tout en conservant la compatibilité avec le système existant.

### Objective

Étendre la bibliothèque de techniques de brainstorming de 5 à 20 techniques, organisées par catégorie avec format structuré et intégration dans le workflow via la commande `technique [x]`.

### Scope

**Included:**
- Création de 4 fichiers techniques (analysis, ideation, perspective, breakthrough)
- Documentation de 20 techniques au format structuré
- Commande `technique [x]` pour appliquer une technique
- Mapping techniques → phases (Divergent/Convergent)
- Mise à jour SKILL.md pour référencer les techniques

**Excluded:**
- Session continuation (→ S01)
- Modes --random et --progressive (→ S03)
- Sélection automatique de techniques (→ S03)

### Techniques to Implement

| Catégorie | Techniques | Count |
|-----------|------------|-------|
| **Analysis** | MoSCoW*, 5 Whys*, SWOT*, Scoring*, Pre-mortem*, Constraint Mapping, Assumption Reversal, Question Storming | 8 |
| **Ideation** | SCAMPER, Six Thinking Hats, Mind Mapping, What If Scenarios, Analogical Thinking, First Principles | 6 |
| **Perspective** | Role Playing, Time Travel, Reversal Inversion | 3 |
| **Breakthrough** | Inner Child Conference, Chaos Engineering, Nature's Solutions | 3 |

*\* = existants dans frameworks.md, à migrer avec enrichissement*

### Format per Technique

```markdown
### [Nom Technique]

**Description:** [2-3 lignes explicatives]

**Quand utiliser:**
- [Situation 1]
- [Situation 2]

**Phase recommandée:** [Divergent | Convergent | Les deux]

**Questions types:**
1. [Question guidée 1]
2. [Question guidée 2]
3. [Question guidée 3]

**Exemple:**
> [Exemple concret d'application dans un contexte dev]
```

### Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S02-AC1 | 4 fichiers techniques créés | Vérifier existence dans references/techniques/ |
| S02-AC2 | 20 techniques documentées | Chaque technique suit le format structuré |
| S02-AC3 | Commande technique fonctionne | `technique scamper` affiche les questions SCAMPER |
| S02-AC4 | Mapping phases documenté | SKILL.md contient le mapping techniques → phases |
| S02-AC5 | Techniques existantes enrichies | MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem au nouveau format |
| S02-AC6 | Exemples concrets | Chaque technique a un exemple contexte dev |

### Files Identified

**Créations:**
- `src/skills/core/brainstormer/references/techniques/analysis.md`
- `src/skills/core/brainstormer/references/techniques/ideation.md`
- `src/skills/core/brainstormer/references/techniques/perspective.md`
- `src/skills/core/brainstormer/references/techniques/breakthrough.md`

**Modifications:**
- `src/skills/core/brainstormer/SKILL.md` (références + mapping phases)
- `src/commands/brainstorm.md` (commande `technique [x]`)

### Memory Summary

- **Stack**: Plugin Claude Code (Markdown content)
- **Patterns**: Skill-based architecture, references/ for detailed content
- **Conventions**: Format structuré pour techniques avec exemples dev

---

## §2 — Implementation Plan

### Strategy Clarifications

1. **Terminology**: `techniques/` is NEW directory, complements `frameworks.md`
   - `frameworks.md` remains as quick reference (5 existing)
   - `techniques/*.md` contains detailed documentation (20 total)
   - `technique [x]` command is NEW, `framework [x]` stays unchanged

2. **`technique [x]` command specification**:
   - Purpose: Display full technique documentation
   - Input: technique name (e.g., `technique scamper`)
   - Output: Full technique content (description, when to use, questions, example)

3. **Phase Mapping**:
   - Divergent: SCAMPER, Six Hats, Mind Mapping, What If, Analogical, Time Travel, Inner Child, Chaos, Nature
   - Convergent: MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem, Constraint, First Principles, Role Playing
   - Deblocage: Reversal, Assumption Reversal, Question Storming

### Impacted Files

| File | Action | Risk |
|------|--------|------|
| `src/skills/core/brainstormer/references/techniques/analysis.md` | Create | Medium |
| `src/skills/core/brainstormer/references/techniques/ideation.md` | Create | Low |
| `src/skills/core/brainstormer/references/techniques/perspective.md` | Create | Low |
| `src/skills/core/brainstormer/references/techniques/breakthrough.md` | Create | Low |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Low |
| `src/commands/brainstorm.md` | Modify | Low |

### Tasks

1. [x] **Create techniques/ directory** (2 min)
   - `mkdir -p src/skills/core/brainstormer/references/techniques/`

2. [ ] **Create analysis.md** (45 min)
   - 8 techniques: MoSCoW, 5 Whys, SWOT, Scoring, Pre-mortem (enriched from frameworks.md) + Constraint Mapping, Assumption Reversal, Question Storming (new)

3. [ ] **Create ideation.md** (30 min)
   - 6 techniques: SCAMPER, Six Thinking Hats, Mind Mapping, What If Scenarios, Analogical Thinking, First Principles

4. [ ] **Create perspective.md** (15 min)
   - 3 techniques: Role Playing, Time Travel, Reversal Inversion

5. [ ] **Create breakthrough.md** (15 min)
   - 3 techniques: Inner Child Conference, Chaos Engineering, Nature's Solutions

6. [ ] **Update SKILL.md** (15 min)
   - Add references section to techniques/
   - Add phase mapping table

7. [ ] **Update brainstorm.md** (15 min)
   - Add `technique [x]` command documentation
   - Add lookup logic

8. [ ] **Run validation** (5 min)
   - `python src/scripts/validate_skill.py src/skills/core/brainstormer/`

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Migration loses format | Medium | Compare enriched techniques against frameworks.md originals |
| Inconsistent technique format | Low | Use template for all 20 techniques |
| Lookup logic incomplete | Low | Test with edge cases |

### Validation

- **@plan-validator**: APPROVED

---

## §3 — Implementation & Finalization

### Progress
- [x] Task 1 — Create techniques/ directory
- [x] Task 2 — Create analysis.md (8 techniques)
- [x] Task 3 — Create ideation.md (6 techniques)
- [x] Task 4 — Create perspective.md (3 techniques)
- [x] Task 5 — Create breakthrough.md (3 techniques)
- [x] Task 6 — Update SKILL.md (references + mapping)
- [x] Task 7 — Update brainstorm.md (technique command)
- [x] Task 8 — Run validation

### Tests
```bash
$ python3 src/scripts/validate_skill.py src/skills/core/brainstormer/
RESULT: PASSED (6/6 checks)
```

### Reviews
- **@code-reviewer**: APPROVED_WITH_FIXES (0 Critical after fixes, 1 Minor)
  - Fixed: First Principles phase mapping (Divergent)
  - Fixed: Assumption Reversal moved to Convergent

### Deviations
| Task | Deviation | Justification |
|------|-----------|---------------|
| — | None | Implementation matches spec |

### Documentation
- **Feature Document**: Updated with §2 and §3
- **SKILL.md**: References to techniques/ added
- **brainstorm.md**: `technique [x]` command documented

### PR Ready
- Branch: `master` (direct)
- Tests: validate_skill.py PASSED
- Lint: N/A (Markdown)
- Docs: Up to date
