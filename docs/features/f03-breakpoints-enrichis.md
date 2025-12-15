# Feature Document — F03: Breakpoints Enrichis

> **Feature ID**: F03
> **Version cible**: EPCI v3.1
> **Priorité**: P2
> **Catégorie**: STANDARD

---

## §1 — Brief Fonctionnel

### Contexte

Les breakpoints actuels du workflow `/epci` sont minimalistes : simple message texte demandant confirmation avant de continuer. L'utilisateur valide "à l'aveugle" sans métriques ni aperçu de ce qui va suivre.

### Objectif

Transformer le breakpoint d'un simple "Continuer ?" en un **tableau de bord décisionnel** permettant à l'utilisateur de faire un choix éclairé avec :
- Métriques de complexité et risque
- Verdicts des agents de validation
- Preview de la phase suivante
- Options interactives

### Stack Détectée

| Composant | Technologie |
|-----------|-------------|
| Plugin | Claude Code Plugin v3.0 (Markdown + YAML frontmatter) |
| Commands | Fichiers MD dans `src/commands/` |
| Agents | Subagents custom dans `src/agents/` |
| Skills | Skills auto-loaded dans `src/skills/` |
| Output | Markdown avec émojis/symboles |

### Critères d'Acceptation

- [ ] **AC1**: Les métriques (complexité, fichiers, temps estimé, risque) s'affichent au breakpoint
- [ ] **AC2**: Les verdicts des agents invoqués sont visibles avec status clair
- [ ] **AC3**: Un preview des 3-5 premières tâches de la phase suivante est affiché
- [ ] **AC4**: Les options interactives sont fonctionnelles via instructions textuelles
- [ ] **AC5**: Le format est lisible en terminal (ASCII art + émojis)
- [ ] **AC6**: Score de complexité calculé via algorithme pondéré
- [ ] **AC7**: Estimation temps via heuristique par catégorie

### Contraintes

| Contrainte | Description |
|------------|-------------|
| Autonomie | F04/F06 non disponibles → métriques autonomes |
| Compatibilité | Non-breaking avec workflow `/epci` existant |
| Format | Markdown uniquement (pas d'ANSI colors) |
| Interaction | Instructions textuelles (pas d'API interactive) |
| Tokens | Breakpoint enrichi < 500 tokens |

### Hors Périmètre

- Breakpoints dans outils externes (IDE, CI/CD)
- Notifications push
- Mode batch sans breakpoints
- Historique des décisions aux breakpoints
- Intégration F04/F06/F08

---

## §2 — Plan d'Implémentation

### Fichiers Impactés

| Fichier | Action | Risque | Justification |
|---------|--------|--------|---------------|
| `src/commands/epci.md` | Modify | Moyen | Intégration breakpoints enrichis BP1 & BP2 |
| `src/skills/core/epci-core/SKILL.md` | Modify | Faible | Ajout section format breakpoint |
| `src/skills/core/breakpoint-metrics/SKILL.md` | Create | Faible | Nouveau skill calcul métriques |
| `src/skills/core/breakpoint-metrics/templates/` | Create | Faible | Templates BP1 et BP2 |

### Architecture Solution

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Breakpoint Enrichi Architecture                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  breakpoint-metrics (SKILL)                                         │
│  ├── Scoring Algorithm                                              │
│  │   └── complexity = files×0.3 + LOC×0.3 + deps×0.2 + risk×0.2    │
│  ├── Time Estimation                                                │
│  │   └── TINY=15min, SMALL=1h, STANDARD=3h, LARGE=8h+              │
│  └── Templates                                                      │
│      ├── bp1-template.md (Post-Phase 1)                            │
│      └── bp2-template.md (Post-Phase 2)                            │
│                                                                      │
│  epci.md (COMMAND)                                                  │
│  ├── Phase 1 → Invoke breakpoint-metrics → Display BP1             │
│  └── Phase 2 → Invoke breakpoint-metrics → Display BP2             │
│                                                                      │
│  epci-core (SKILL)                                                  │
│  └── Section "Breakpoint Format" (reference documentation)         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Tâches

#### Phase A: Skill breakpoint-metrics (Foundation)

1. [ ] **Créer structure skill breakpoint-metrics** (5 min)
   - Fichier: `src/skills/core/breakpoint-metrics/SKILL.md`
   - Test: Validation YAML frontmatter
   - Dépendances: Aucune

2. [ ] **Implémenter algorithme de scoring** (10 min)
   - Fichier: `src/skills/core/breakpoint-metrics/SKILL.md` (section Scoring)
   - Test: Exemples de calcul documentés
   - Dépendances: Tâche 1

3. [ ] **Implémenter estimation temps** (5 min)
   - Fichier: `src/skills/core/breakpoint-metrics/SKILL.md` (section Time)
   - Test: Table heuristique complète
   - Dépendances: Tâche 1

4. [ ] **Créer template BP1 (Post-Phase 1)** (10 min)
   - Fichier: `src/skills/core/breakpoint-metrics/templates/bp1-template.md`
   - Test: Validation format ASCII art
   - Dépendances: Tâches 2, 3

5. [ ] **Créer template BP2 (Post-Phase 2)** (10 min)
   - Fichier: `src/skills/core/breakpoint-metrics/templates/bp2-template.md`
   - Test: Validation format ASCII art
   - Dépendances: Tâches 2, 3

#### Phase B: Intégration epci.md

6. [ ] **Modifier BP1 dans epci.md** (15 min)
   - Fichier: `src/commands/epci.md` (section Phase 1 BREAKPOINT)
   - Test: Format enrichi visible
   - Dépendances: Tâche 4

7. [ ] **Modifier BP2 dans epci.md** (15 min)
   - Fichier: `src/commands/epci.md` (section Phase 2 BREAKPOINT)
   - Test: Format enrichi visible
   - Dépendances: Tâche 5

#### Phase C: Documentation epci-core

8. [ ] **Ajouter section Breakpoint Format dans epci-core** (10 min)
   - Fichier: `src/skills/core/epci-core/SKILL.md`
   - Test: Documentation cohérente avec templates
   - Dépendances: Tâches 4, 5

### Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Format ASCII mal rendu | Faible | Moyen | Tester sur plusieurs largeurs terminal |
| Breakpoint trop verbeux (>500 tokens) | Moyen | Faible | Optimiser template, version compacte |
| Confusion utilisateur | Faible | Faible | Options claires et documentées |

### Validation

- **@plan-validator**: ✅ APPROVED
  - Completeness: OK
  - Consistency: OK
  - Feasibility: OK
  - Quality: OK
- **Recommandations**:
  - Tester ASCII art rendering tôt
  - Documenter exemples input/output scoring
  - Prévoir fallback largeur terminal

---

## §3 — Implémentation

### Progress

- [x] **Tâche 1**: Créer structure skill breakpoint-metrics (5 min)
- [x] **Tâche 2**: Implémenter algorithme de scoring (10 min)
- [x] **Tâche 3**: Implémenter estimation temps (5 min)
- [x] **Tâche 4**: Créer template BP1 (10 min)
- [x] **Tâche 5**: Créer template BP2 (10 min)
- [x] **Tâche 6**: Modifier BP1 dans epci.md (15 min)
- [x] **Tâche 7**: Modifier BP2 dans epci.md (15 min)
- [x] **Tâche 8**: Ajouter section Breakpoint Format dans epci-core (10 min)

### Fichiers Créés/Modifiés

| Fichier | Action | Status |
|---------|--------|--------|
| `src/skills/core/breakpoint-metrics/SKILL.md` | Created | ✅ |
| `src/skills/core/breakpoint-metrics/templates/bp1-template.md` | Created | ✅ |
| `src/skills/core/breakpoint-metrics/templates/bp2-template.md` | Created | ✅ |
| `src/commands/epci.md` | Modified | ✅ |
| `src/skills/core/epci-core/SKILL.md` | Modified | ✅ |

### Tests

Validation manuelle des formats:
- ✅ ASCII art rendering correct
- ✅ Variables placeholder identifiées
- ✅ Options interactives documentées
- ✅ Scoring algorithm avec exemples

### Reviews

- **@code-reviewer**: ✅ APPROVED_WITH_FIXES (0 Critical, 0 Important, 2 Minor)
  - Minor 1: Variable format standardisé `{VAR}` → Corrigé ✅
  - Minor 2: Auto-trigger documentation clarifiée → Corrigé ✅
- **@security-auditor**: N/A (pas de fichiers sensibles)
- **@qa-reviewer**: N/A (pas de tests complexes)

### Déviations

| Tâche | Déviation | Justification |
|-------|-----------|---------------|
| - | Aucune | Implémentation conforme au plan |

---

## §4 — Finalisation

### Commit

```
feat(breakpoints): add enriched breakpoint displays for EPCI workflow

- Add breakpoint-metrics skill with complexity scoring algorithm
- Create BP1 and BP2 templates with ASCII-art formatting
- Integrate enriched breakpoints into /epci command (Phase 1 & 2)
- Update epci-core skill with Breakpoint Format documentation
- Add time estimation heuristics and risk assessment display

Implements F03: Breakpoints Enrichis for EPCI v3.1

Refs: docs/features/f03-breakpoints-enrichis.md
```

### Documentation

- **@doc-generator**: 1 fichier vérifié
  - CHANGELOG.md (section [Unreleased] mise à jour)

### Fichiers Finaux

| Fichier | Action | Status |
|---------|--------|--------|
| `src/skills/core/breakpoint-metrics/SKILL.md` | Created | ✅ |
| `src/skills/core/breakpoint-metrics/templates/bp1-template.md` | Created | ✅ |
| `src/skills/core/breakpoint-metrics/templates/bp2-template.md` | Created | ✅ |
| `src/commands/epci.md` | Modified | ✅ |
| `src/skills/core/epci-core/SKILL.md` | Modified | ✅ |
| `docs/features/f03-breakpoints-enrichis.md` | Created | ✅ |
| `CHANGELOG.md` | Modified | ✅ |

### Validation Finale

- ✅ Toutes les tâches complétées (8/8)
- ✅ @plan-validator: APPROVED
- ✅ @code-reviewer: APPROVED_WITH_FIXES (issues corrigées)
- ✅ @doc-generator: Documentation générée
- ✅ Feature Document complet
