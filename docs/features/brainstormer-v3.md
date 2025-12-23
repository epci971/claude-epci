# Feature Document — Brainstormer v3 Claude Code

> **Slug**: `brainstormer-v3`
> **Category**: STANDARD
> **Date**: 2025-12-23

---

## §1 — Functional Brief

### Context

Mise à niveau du skill Brainstormer pour Claude Code vers la version 3.0. Le skill actuel (~5K tokens actifs) manque de personnalité, de structure de processus créatif, et de frameworks d'analyse avancés. Cette refonte intègre les fonctionnalités à haute valeur de la version Web v3.0 adaptées au contexte développement logiciel et CLI.

**Source**: Cahier des charges `docs/briefs/brainstormer-v3/brief-brainstormer-v3-claude-code-2025-12-23.md`

### Detected Stack

- **Framework**: claude-code-plugin v3.5.0
- **Language**: Markdown (skills/commands) + Python (scripts)
- **Patterns**: skill-pattern, command-pattern, subagent-pattern

### Identified Files

| File | Action | Risk | Est. Lines |
|------|--------|------|------------|
| `src/skills/core/brainstormer/references/personas.md` | Create | Low | ~150 |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Medium | +25 |
| `src/skills/core/brainstormer/references/ems-system.md` | Modify | Low | +50 |
| `src/skills/core/brainstormer/references/frameworks.md` | Modify | Medium | +60 |
| `src/skills/core/brainstormer/references/brief-format.md` | Modify | Low | +20 |
| `src/commands/brainstorm.md` | Modify | Medium | +50 |

### Acceptance Criteria

- [ ] SKILL.md < 5000 tokens
- [ ] 3 personas (Architecte, Sparring, Pragmatique) avec bascule auto
- [ ] Phases Divergent/Convergent affichées dans breakpoints
- [ ] Pre-mortem comme framework avec output structuré
- [ ] EMS v2 avec ancres objectives (20/40/60/80/100)
- [ ] 5 frameworks documentés (5 Whys, MoSCoW, SWOT, Pre-mortem, Scoring)
- [ ] 4 biais dev (Over-engineering, Scope creep, Sunk cost, Bikeshedding)
- [ ] Commandes: modes, mode [x], premortem, diverge, converge, scoring
- [ ] Flags: --template, --no-hmw, --quick
- [ ] Brief généré compatible avec /epci-brief
- [ ] Journal d'exploration créé

### Constraints

- Budget tokens: SKILL.md < 5K, références en lazy-load
- Rétrocompatibilité: commandes existantes (continue, finish, dive, pivot, status) préservées
- Format breakpoint: compact pour CLI (< 20 lignes)

### Out of Scope

- Templates audit/project/research/strategy (garder uniquement feature/problem/decision)
- Frameworks Six Hats, Starbursting, Reverse, Weighted Criteria
- Persona Maïeuticien (trop "soft" pour contexte dev)
- Checkpoint JSON (fichiers .md suffisent)
- Web search proactif (non pertinent CLI)
- Notion export (non pertinent CLI)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 6
- **Estimated LOC**: ~400
- **Risk**: MEDIUM
- **Justification**: Refonte significative d'un skill core avec nouvelle architecture (personas, phases), mais spécifications claires et patterns existants réutilisables.

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 6 fichiers impactés |

### Implementation Sequence (Recommended)

1. `personas.md` (Create) — Foundation, no dependencies
2. `ems-system.md` (Modify) — Add anchor table
3. `frameworks.md` (Modify) — Add pre-mortem
4. `SKILL.md` (Modify) — Core refactor with refs to new files
5. `brainstorm.md` (Modify) — Update command with new features
6. `brief-format.md` (Modify) — Final template updates

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | Est. Time |
|------|--------|------|-----------|
| `src/skills/core/brainstormer/references/personas.md` | Create | Low | 15 min |
| `src/skills/core/brainstormer/references/ems-system.md` | Modify | Low | 10 min |
| `src/skills/core/brainstormer/references/frameworks.md` | Modify | Medium | 15 min |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Medium | 20 min |
| `src/commands/brainstorm.md` | Modify | Medium | 15 min |
| `src/skills/core/brainstormer/references/brief-format.md` | Modify | Low | 10 min |

### Tasks

#### Task 1: Create personas.md (15 min)

**File**: `src/skills/core/brainstormer/references/personas.md`

**Content specification**:
```
# 3 Personas

| Persona | Icon | Philosophy | Default |
|---------|------|------------|---------|
| Architecte | 📐 | Structurant, frameworks, synthèse | YES |
| Sparring | 🥊 | Challenger, stress-test | No |
| Pragmatique | 🛠️ | Action, débloquer | No |

# Auto-Switch Rules

| Context | Persona |
|---------|---------|
| Session start, complex topic | 📐 Architecte |
| Words "évidemment", "forcément" | 🥊 Sparring |
| Pre-mortem triggered | 🥊 Sparring |
| EMS stagnation (<5 pts / 2 iter) | 🛠️ Pragmatique |
| Iteration ≥ 5 without decision | 🛠️ Pragmatique |
| Convergent phase | 📐 + 🛠️ |

# Commands

| Command | Action |
|---------|--------|
| modes | Display 3 personas + current state |
| mode [name] | Force persona |
| mode auto | Return to auto-switch |

# Signaling (message prefix)

📐 [Structure] ...
🥊 [Challenge] ...
🛠️ [Action] ...
```

**Test**: File exists, YAML valid, ~150 lines

---

#### Task 2: Update ems-system.md (10 min)

**File**: `src/skills/core/brainstormer/references/ems-system.md`

**Add section**: Objective Anchors (after "Les 5 Axes")

```markdown
## Ancres Objectives

| Score | Clarté | Profondeur | Décisions |
|-------|--------|------------|-----------|
| 20 | Sujet énoncé | Questions surface | Tout ouvert |
| 40 | Brief validé + scope | 1 "pourquoi" creusé | 1-2 orientations |
| 60 | + Contraintes (≥2) | Framework appliqué | Choix clés verrouillés |
| 80 | + Critères acceptation | Insights non-évidents | Priorisation faite |
| 100 | Zéro ambiguïté | Cause racine identifiée | Tous threads fermés |
```

**Add section**: Phase-Aware Recommendations

```markdown
## Recommandations Phase-Aware

| Phase | Focus |
|-------|-------|
| 🔀 Divergent | Couverture, Profondeur |
| 🎯 Convergent | Décisions, Actionnabilité |
```

**Test**: Token count check, sections present

---

#### Task 3: Update frameworks.md (15 min)

**File**: `src/skills/core/brainstormer/references/frameworks.md`

**Add section**: Pre-mortem Framework (after Scoring)

```markdown
## Pre-mortem — Anticipation des Risques

### Declencheur
- Commande `premortem`
- Projet à risque identifié
- Avant décision finale

### Persona
Active automatiquement 🥊 Sparring

### Application
1. Projection: "Nous sommes dans 3 mois. L'implémentation a échoué."
2. Identification: Lister toutes les causes possibles
3. Scoring: Probabilité × Impact (1-3 chaque, max 9)
4. Mitigation: Action préventive pour causes majeures
5. Signaux: Alertes à surveiller

### Format Output

⚰️ Pre-mortem : [Feature]

Projection: 3 mois, échec.

| # | Cause | Proba | Impact | Score |
|---|-------|-------|--------|-------|
| 1 | [Cause] | 🔴 Haute | 🔴 Critique | 9 |

Mitigations:
| Cause | Action | Qui | Quand |

Signaux d'alerte:
- 🚨 [Signal] → [Action]
```

**Update**: "Quand Appliquer" table to add Pre-mortem row

**Test**: Pre-mortem section exists, format valid

---

#### Task 4: Refactor SKILL.md (20 min)

**File**: `src/skills/core/brainstormer/SKILL.md`

**Changes**:

1. **Add Personas section** (after Overview):
```markdown
## Personas

3 modes de facilitation avec bascule automatique.

| Persona | Icône | Rôle |
|---------|-------|------|
| Architecte | 📐 | Structure, frameworks (DÉFAUT) |
| Sparring | 🥊 | Challenge, stress-test |
| Pragmatique | 🛠️ | Action, déblocage |

→ Voir [personas.md](references/personas.md)
```

2. **Add Phases section** (after Personas):
```markdown
## Phases

| Phase | Icône | Focus |
|-------|-------|-------|
| Divergent | 🔀 | Générer, explorer, quantité |
| Convergent | 🎯 | Évaluer, décider, qualité |

Transition auto: Couverture ≥ 60% ET iter ≥ 3 → suggérer Convergent
```

3. **Update Breakpoint format**:
```
🔀 DIVERGENT | 📐 Architecte | Iter X | EMS: XX/100 (+Y) 🌿
```

4. **Add HMW section** (in Phase 1):
```markdown
### HMW (How Might We)

Après validation brief, générer 3 questions:
1. HMW [simplifier] [processus] sans [compromis] ?
2. HMW garantir [qualité] même si [contrainte] ?
3. HMW permettre [fonctionnalité] dans [contexte difficile] ?

Flag: `--no-hmw` pour désactiver
```

5. **Update Commands** (add):
- `modes` — Afficher personas
- `mode [x]` — Forcer persona
- `premortem` — Lancer pre-mortem
- `diverge` — Forcer phase Divergent
- `converge` — Forcer phase Convergent
- `scoring` — Évaluer idées

6. **Update Biais section** (replace with 4 dev-specific):
```markdown
| Biais | Signal | Action |
|-------|--------|--------|
| Over-engineering | "Ajoutons X au cas où" | Suggérer MVP |
| Scope creep | Expansion continue | Rappeler focus |
| Sunk cost | "On a déjà fait X" | Challenger |
| Bikeshedding | Focus détails triviaux | Recentrer |
```

**Test**: Token count < 5000, all sections present

---

#### Task 5: Update brainstorm.md (15 min)

**File**: `src/commands/brainstorm.md`

**Changes**:

1. **Add Personas section** (in Configuration):
```markdown
| **Personas** | Architecte (défaut), Sparring, Pragmatique |
```

2. **Add Phases section** (after Commandes):
```markdown
## Phases

| Phase | Icône | Comportement |
|-------|-------|--------------|
| Divergent | 🔀 | Explorer, générer, pas de jugement |
| Convergent | 🎯 | Évaluer, prioriser, décider |

Commandes: `diverge`, `converge`
```

3. **Update Commandes table** (add):
- `modes` — Afficher/changer persona
- `mode [nom]` — Forcer persona
- `premortem` — Exercice pre-mortem
- `diverge` — Phase Divergent
- `converge` — Phase Convergent
- `scoring` — Évaluer idées
- `framework [name]` — Appliquer framework

4. **Add Flags section**:
```markdown
## Flags

| Flag | Effet |
|------|-------|
| `--template [name]` | Forcer template (feature/problem/decision) |
| `--no-hmw` | Désactiver génération HMW |
| `--quick` | Mode rapide (3 iter max) |
```

5. **Update Breakpoint example**:
```
🔀 DIVERGENT | 📐 Architecte | Iter 3 | EMS: 58/100 (+12) 🌿
```

**Test**: All new commands documented

---

#### Task 6: Update brief-format.md (10 min)

**File**: `src/skills/core/brainstormer/references/brief-format.md`

**Changes**:

1. **Add Template metadata** (in header):
```markdown
> **Template**: [feature/problem/decision]
```

2. **Add EMS Final section** (after Metadonnées):
```markdown
## EMS Final

Score: XX/100 [emoji]

| Axe | Score |
|-----|-------|
| Clarté | XX/100 |
| Profondeur | XX/100 |
| Couverture | XX/100 |
| Décisions | XX/100 |
| Actionnabilité | XX/100 |
```

3. **Add optional Pre-mortem section**:
```markdown
## Risques (Pre-mortem)

[Si pre-mortem effectué]

| Risque | Score | Mitigation |
|--------|-------|------------|
```

**Test**: Template updated, new sections present

---

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| SKILL.md exceeds 5K tokens | Medium | Move details to references, keep core minimal |
| Persona auto-switch confusing | Low | Clear rules in personas.md, manual override |
| Breaking existing commands | Low | All existing commands preserved |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: OK
  - Consistency: OK
  - Feasibility: OK
  - Quality: OK
- **Dependencies**: Tasks ordered correctly (1→2→3→4→5→6)
- **Backward compatibility**: All existing commands preserved

---

## §3 — Implementation

### Progress

- [x] Task 1: Create personas.md (~150 lines)
- [x] Task 2: Update ems-system.md (+50 lines)
- [x] Task 3: Update frameworks.md (+60 lines)
- [x] Task 4: Refactor SKILL.md (+25 lines)
- [x] Task 5: Update brainstorm.md (+50 lines)
- [x] Task 6: Update brief-format.md (+20 lines)

### Tests

- SKILL.md token count: ~1,300 tokens (well under 5K limit)
- All internal links valid
- Markdown formatting clean

### Reviews

- **@code-reviewer**: APPROVED
  - Token budget: OK (~1,300 tokens)
  - Consistency: OK (terminology, icons)
  - References: OK (all links valid)
  - Backwards compatibility: OK
  - Minor: hyphenation inconsistency (premortem vs pre-mortem)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| None | - | All tasks completed as planned |

---

## §4 — Finalization

### Commit

```
feat(brainstormer): upgrade to v3 with personas, phases and pre-mortem

- Add 3 personas (Architecte, Sparring, Pragmatique) with auto-switch
- Add Divergent/Convergent phases with explicit indicators
- Add pre-mortem framework for risk anticipation
- Add EMS v2 with objective anchors (20/40/60/80/100)
- Add HMW (How Might We) question generation
- Add new commands: modes, premortem, diverge, converge, scoring
- Add flags: --template, --no-hmw, --quick
- Update biases to 4 dev-specific ones
- Update breakpoint format with phase/persona header

Refs: docs/features/brainstormer-v3.md
```

### Documentation

- Feature Document: `docs/features/brainstormer-v3.md` (complet)
- Cahier des charges: `docs/briefs/brainstormer-v3/brief-brainstormer-v3-claude-code-2025-12-23.md`

### Validation Finale

- [x] SKILL.md < 5000 tokens (~1,300 tokens)
- [x] 3 personas avec bascule auto
- [x] Phases Divergent/Convergent affichées
- [x] Pre-mortem framework ajouté
- [x] EMS v2 avec ancres objectives
- [x] 5 frameworks documentés
- [x] 4 biais dev-specific
- [x] Nouvelles commandes ajoutées
- [x] Flags documentés
- [x] Rétrocompatibilité maintenue
