# Brief Fonctionnel — Optimisation Workflow EPCI (Turbo Mode)

> **Genere par**: Brainstormer v3.0
> **Template**: feature
> **EMS Final**: 82/100
> **Date**: 2025-12-30
> **Slug**: workflow-turbo-optimization

---

## Contexte

Le workflow EPCI actuel prend ~30 minutes pour une feature STANDARD (8 fichiers).
L'analyse révèle ~13 minutes de gaspillage (43%) dues à :
- Explorations redondantes (brainstorm + brief)
- Breakpoints de clarification validés automatiquement
- Utilisation d'Opus pour des tâches simples (exploration)
- Reviews séquentielles au lieu de parallèles

L'objectif est de diviser le temps par 2 (~15-18 min) sans perdre en qualité.

## Objectif

Optimiser le workflow EPCI via :
1. **Modèles adaptatifs** : Haiku pour exploration, Sonnet pour implémentation, Opus pour validation critique
2. **Nouveaux agents spécialisés** : @clarifier, @planner, @implementer
3. **Parallélisation** : Reviews en parallèle
4. **Flag --turbo** : Active toutes les optimisations, suggéré automatiquement

---

## Specifications Fonctionnelles

### SF1 — Flag `--turbo` (suggéré automatiquement)

**Description** : Flag global activant toutes les optimisations de performance.

**Comportement** :
- Utilise Haiku pour explorations (@Explore)
- Utilise les nouveaux agents optimisés
- Auto-accept suggestions si EMS > 60 (brainstorm) ou score confiance > 0.7 (brief)
- Lance reviews en parallèle
- Réduit les breakpoints (1 au lieu de 2 pour /epci)

**Auto-suggestion** :
```
Si projet connu (project-memory existe) ET tâche STANDARD/SMALL :
    → Suggérer: "Utiliser --turbo ? (workflow optimisé, ~15 min au lieu de 30)"
```

**Commandes impactées** :
- `/brainstorm --turbo`
- `/epci-brief --turbo`
- `/epci --turbo`
- `/epci-quick --turbo`
- `/epci-debug --turbo`

### SF2 — Nouveaux agents avec modèles optimisés

#### Agent @clarifier (Haiku)

```yaml
---
name: clarifier
description: >-
  Fast clarification agent for generating context-aware questions.
  Use when: need to clarify requirements quickly.
  Do NOT use for: complex architectural decisions.
model: haiku
allowed-tools: [Read, Grep]
---
```

**Rôle** : Génère les questions de clarification avec suggestions
**Invoqué par** : `/brainstorm`, `/epci-brief` (en mode --turbo)
**Gain** : ~2 min (Haiku 3x plus rapide qu'Opus)

#### Agent @planner (Sonnet)

```yaml
---
name: planner
description: >-
  Implementation planning agent. Generates detailed task breakdown,
  file impact analysis, and risk assessment.
  Use when: Phase 1 of /epci or /epci-quick planning.
model: sonnet
allowed-tools: [Read, Grep, Glob]
---
```

**Rôle** : Crée le plan d'implémentation (tâches, fichiers, risques)
**Invoqué par** : `/epci` Phase 1, `/epci-quick`
**Gain** : ~2 min (Sonnet suffisant pour planification)

#### Agent @implementer (Sonnet)

```yaml
---
name: implementer
description: >-
  Code implementation agent. Writes code following established patterns.
  Use when: Phase 2 implementation tasks.
  Focuses on: code generation, test writing, pattern adherence.
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

**Rôle** : Implémente le code selon le plan validé
**Invoqué par** : `/epci` Phase 2, `/epci-quick`, `/epci-debug`
**Gain** : Qualité équivalente, légèrement plus rapide

### SF3 — Modification agents existants

| Agent | Modèle actuel | Nouveau modèle | Justification |
|-------|---------------|----------------|---------------|
| `@plan-validator` | inherit | **opus** | Validation critique, doit être rigoureuse |
| `@code-reviewer` | inherit | **opus** | Qualité code critique |
| `@security-auditor` | inherit | **opus** | Sécurité non négociable |
| `@qa-reviewer` | inherit | **sonnet** | Patterns de tests connus |
| `@doc-generator` | inherit | **sonnet** | Documentation structurée |
| `@decompose-validator` | inherit | **opus** | Validation architecture |

### SF4 — Parallélisation des reviews (Phase 2)

**Comportement actuel** (séquentiel) :
```
@code-reviewer → @security-auditor → @qa-reviewer
Temps: ~6 min (2 min chacun)
```

**Nouveau comportement** (parallèle en mode --turbo) :
```
┌────────────────────────────────────────┐
│ Code terminé                           │
│       │                                │
│  ┌────┴────┬────────────┐              │
│  ▼         ▼            ▼              │
│ @code-reviewer  @qa-reviewer  @security-auditor
│   (Opus)        (Sonnet)      (Opus, conditionnel)
│  └────┬────┴────────────┘              │
│       ▼                                │
│ Consolidation résultats                │
└────────────────────────────────────────┘
Temps: ~2-3 min (parallèle)
```

**Gain** : ~3-4 min

### SF5 — Modifications des commandes

#### /brainstorm

**Ajouts** :
- Flag `--turbo` dans argument-hint
- Step 2 (Exploration) : `model: haiku` pour @Explore
- Phase 2 : Utiliser @clarifier (Haiku) pour questions
- Auto-accept : Si EMS > 60 ET toutes suggestions ont confiance > 0.7 → skip breakpoint clarification
- Suggestion --turbo en début si project-memory existe

**Instructions MANDATORY** :
```markdown
**⚠️ MANDATORY (--turbo mode):**
- Use Task tool with model: haiku for @Explore
- Invoke @clarifier (Haiku) for clarification questions
- If EMS > 60 AND all suggestions confidence > 0.7: auto-accept and continue
```

#### /epci-brief

**Ajouts** :
- Flag `--turbo`
- Step 1 : @Explore avec `model: haiku`
- Step 2 : @clarifier pour questions (si --turbo)
- Auto-accept suggestions si confiance > 0.7
- Suggestion --turbo en début

**Instructions MANDATORY** :
```markdown
**⚠️ MANDATORY (--turbo mode):**
- Step 1: Invoke @Explore with model: haiku (NOT opus)
- Step 2: Use @clarifier for clarification questions
- Auto-accept: If suggestion confidence > 0.7, use as-is without breakpoint
```

#### /epci

**Ajouts** :
- Flag `--turbo`
- Phase 1 : Utiliser @planner (Sonnet) pour génération plan
- Phase 1 : @plan-validator reste Opus
- Phase 2 : @implementer (Sonnet) pour code
- Phase 2 : Reviews en parallèle (@code-reviewer + @qa-reviewer + @security-auditor)
- Réduire à 1 breakpoint (après Phase 1 seulement, pas après Phase 2)

**Instructions MANDATORY** :
```markdown
**⚠️ MANDATORY (--turbo mode):**
- Phase 1: Use @planner (Sonnet) to generate plan, then @plan-validator (Opus) to validate
- Phase 2: Use @implementer (Sonnet) for implementation
- Phase 2 reviews: Launch @code-reviewer, @qa-reviewer, @security-auditor IN PARALLEL using multiple Task tool calls in single message
- Breakpoints: Only 1 breakpoint after Phase 1 (skip breakpoint after Phase 2)
```

#### /epci-quick

**Ajouts** :
- Flag `--turbo`
- Utiliser @planner (Sonnet) pour mini-plan
- Utiliser @implementer (Sonnet) pour code
- @code-reviewer (Opus) pour review

**Instructions MANDATORY** :
```markdown
**⚠️ MANDATORY (--turbo mode):**
- Use @planner (Sonnet) for quick planning
- Use @implementer (Sonnet) for implementation
- Use @code-reviewer (Opus) for quality review
```

#### /epci-debug

**Ajouts** :
- Flag `--turbo`
- Diagnostic : @Explore avec Haiku
- Fix : @implementer (Sonnet)
- Review : @code-reviewer (Opus)

---

## Regles Metier

- **RM1**: Le flag `--turbo` ne compromet JAMAIS la qualité des validations (Opus pour @plan-validator, @code-reviewer, @security-auditor)
- **RM2**: Les reviews Opus restent obligatoires même en mode turbo
- **RM3**: L'auto-accept ne s'applique qu'aux suggestions, jamais aux validations de plan ou code
- **RM4**: Si un agent Haiku/Sonnet échoue ou retourne un résultat insuffisant, fallback vers Opus

---

## Cas Limites & Edge Cases

| Cas | Comportement attendu |
|-----|---------------------|
| Tâche LARGE avec --turbo | Avertir: "Tâche complexe détectée, --turbo peut être sous-optimal" |
| Agent Haiku indisponible | Fallback automatique vers Sonnet |
| Reviews parallèles avec erreur | Attendre toutes les reviews, consolider erreurs |
| EMS = 59 (juste sous seuil) | Pas d'auto-accept, poser les questions |
| Fichiers sécurité + --turbo | @security-auditor reste obligatoire (Opus) |

---

## Hors Scope (v1)

- Modification de /epci-spike (exploration, pas de gain significatif)
- Modification de /epci-decompose (déjà optimisé)
- Nouveau workflow /epci-start (fusion brainstorm+brief) → v2
- Dashboard métriques de temps → v2
- Auto-détection du meilleur mode (ML) → v2

---

## Contraintes Techniques

| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Haiku moins précis | Exploration peut manquer des fichiers | Fallback Opus si résultat incomplet |
| Parallélisation agents | Consommation API plus haute | Acceptable pour le gain de temps |
| Modèle dans frontmatter | Nécessite mise à jour tous les agents | One-time migration |

---

## Dependances

- **Internes**: Tous les agents existants, toutes les commandes
- **Externes**: API Claude (Haiku, Sonnet, Opus disponibles)

---

## Criteres d'Acceptation

- [ ] Flag --turbo disponible sur les 5 commandes (brainstorm, epci-brief, epci, epci-quick, epci-debug)
- [ ] 3 nouveaux agents créés (@clarifier, @planner, @implementer) avec bons modèles
- [ ] 6 agents existants mis à jour avec modèle explicite
- [ ] Instructions MANDATORY ajoutées dans chaque commande pour --turbo
- [ ] Reviews parallèles fonctionnelles en mode --turbo
- [ ] Auto-accept implémenté (EMS > 60 / confiance > 0.7)
- [ ] Suggestion automatique de --turbo si project-memory existe
- [ ] Tests: workflow complet en ~15-18 min (vs 30 min actuel)

---

## Estimation

| Metrique | Valeur |
|----------|--------|
| Complexite | LARGE |
| Fichiers impactes | ~15 (5 commandes + 9 agents + 1 skill flags) |
| Risque | Medium (modification workflow critique) |
| Gain attendu | ~12-15 min par feature |

---

## Fichiers a modifier

### Nouveaux fichiers (3)
- `src/agents/clarifier.md`
- `src/agents/planner.md`
- `src/agents/implementer.md`

### Agents existants (6)
- `src/agents/plan-validator.md` → ajouter `model: opus`
- `src/agents/code-reviewer.md` → ajouter `model: opus`
- `src/agents/security-auditor.md` → ajouter `model: opus`
- `src/agents/qa-reviewer.md` → ajouter `model: sonnet`
- `src/agents/doc-generator.md` → ajouter `model: sonnet`
- `src/agents/decompose-validator.md` → ajouter `model: opus`

### Commandes (5)
- `src/commands/brainstorm.md` → --turbo, @clarifier, auto-accept
- `src/commands/epci-brief.md` → --turbo, Haiku exploration
- `src/commands/epci.md` → --turbo, @planner, @implementer, parallel reviews
- `src/commands/epci-quick.md` → --turbo, agents optimisés
- `src/commands/epci-debug.md` → --turbo, agents optimisés

### Settings (1)
- `src/settings/flags.md` → documenter --turbo

---

## EMS Final

Score: 82/100 🎯

| Axe | Score |
|-----|-------|
| Clarte | 90/100 |
| Profondeur | 85/100 |
| Couverture | 80/100 |
| Decisions | 85/100 |
| Actionnabilite | 70/100 |

---

## Metadonnees Brainstormer

| Metrique | Valeur |
|----------|--------|
| Iterations | 3 |
| EMS Final | 82/100 |
| Template | feature |
| Frameworks utilises | - |
| Duree exploration | ~15min |

---

*Brief pret pour EPCI — Lancer `/epci-brief` avec ce contenu.*
