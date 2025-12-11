---
description: >-
  Workflow EPCI complet en 3 phases pour features STANDARD et LARGE.
  Phase 1: Analyse et planification. Phase 2: Implémentation TDD.
  Phase 3: Finalisation et documentation. Inclut breakpoints entre phases.
argument-hint: "[--large] [--continue]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI — Workflow Complet

## Overview

Workflow structuré en 3 phases avec validation à chaque étape.
Génère un Feature Document comme fil rouge de traçabilité.

## Arguments

| Argument | Description |
|----------|-------------|
| `--large` | Active le mode LARGE (thinking renforcé, tous subagents obligatoires) |
| `--continue` | Continue depuis la dernière phase (reprise après interruption) |

## Feature Document

Créer/mettre à jour le fichier : `docs/features/<feature-slug>.md`

```markdown
# Feature Document — [Titre]

## §1 — Brief Fonctionnel
[Copié depuis /epci-brief ou généré ici]

## §2 — Plan d'Implémentation
[Généré en Phase 1]

## §3 — Implémentation
[Mis à jour en Phase 2]

## §4 — Finalisation
[Complété en Phase 3]
```

---

## Phase 1 : Analyse et Planification

### Configuration

| Élément | Valeur |
|---------|--------|
| **Thinking** | `think hard` |
| **Skills** | epci-core, architecture-patterns, [stack] |
| **Subagents** | @Plan (natif), @plan-validator |

### Process

1. **Réception du brief**
   - Vérifier que le brief est complet (vient de `/epci-brief`)
   - Si incomplet → suggérer `/epci-brief` d'abord

2. **Analyse technique** (via @Plan)
   - Identifier les fichiers impactés
   - Analyser les dépendances
   - Évaluer les risques techniques

3. **Génération du plan**
   - Découper en tâches atomiques (2-15 min chacune)
   - Ordonner par dépendances
   - Prévoir un test pour chaque tâche

4. **Validation** (via @plan-validator)
   - Soumettre le plan au validateur
   - Si NEEDS_REVISION → corriger et re-soumettre
   - Si APPROVED → passer au breakpoint

### Output §2

```markdown
## §2 — Plan d'implémentation

### Fichiers impactés
| Fichier | Action | Risque |
|---------|--------|--------|
| src/Service/X.php | Modifier | Moyen |
| src/Entity/Y.php | Créer | Faible |
| tests/Unit/XTest.php | Créer | Faible |

### Tâches
1. [ ] **Créer l'entité Y** (5 min)
   - Fichier : `src/Entity/Y.php`
   - Test : `tests/Unit/Entity/YTest.php`

2. [ ] **Modifier le service X** (10 min)
   - Fichier : `src/Service/X.php`
   - Test : `tests/Unit/Service/XTest.php`

### Risques
| Risque | Probabilité | Mitigation |
|--------|-------------|------------|
| Breaking change | Moyenne | Tests de régression |

### Validation
- **@plan-validator** : APPROVED
```

### ⏸️ BREAKPOINT

```
---
⏸️ **BREAKPOINT PHASE 1**

Plan complet et validé.
- @plan-validator : APPROVED
- Tâches : X tâches identifiées
- Fichiers : Y fichiers impactés

Feature Document §2 mis à jour.

**Attendre confirmation :** "Continue" ou "Plan validé"
---
```

---

## Phase 2 : Implémentation

### Configuration

| Élément | Valeur |
|---------|--------|
| **Thinking** | `think` |
| **Skills** | testing-strategy, code-conventions, [stack] |
| **Subagents** | @code-reviewer (obligatoire), @security-auditor*, @qa-reviewer* |

### Subagents conditionnels

**@security-auditor** si détection de :
- Fichiers : `**/auth/**`, `**/security/**`, `**/api/**`, `**/password/**`
- Mots-clés : `password`, `secret`, `api_key`, `jwt`, `oauth`

**@qa-reviewer** si :
- Plus de 5 fichiers de test créés/modifiés
- Tests d'intégration ou E2E impliqués
- Mocking complexe détecté

### Process

Pour chaque tâche du plan :

```
1. RED — Écrire le test qui échoue
2. Exécuter → confirmer l'échec
3. GREEN — Implémenter le code minimal
4. Exécuter → confirmer le passage
5. REFACTOR — Améliorer si nécessaire
6. Cocher la tâche ✓
```

Après toutes les tâches :
1. Exécuter la suite de tests complète
2. Invoquer @code-reviewer
3. Invoquer @security-auditor (si applicable)
4. Invoquer @qa-reviewer (si applicable)
5. Corriger les issues Critical/Important

### Output §3

```markdown
## §3 — Implémentation

### Progression
- [x] Tâche 1 — Créer l'entité Y
- [x] Tâche 2 — Modifier le service X
- [x] Tâche 3 — Ajouter la validation

### Tests
```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews
- **@code-reviewer** : APPROVED (0 Critical, 2 Minor)
- **@security-auditor** : APPROVED
- **@qa-reviewer** : N/A

### Déviations
| Tâche | Déviation | Justification |
|-------|-----------|---------------|
| #3 | +1 fichier | Extraction de helper |
```

### ⏸️ BREAKPOINT

```
---
⏸️ **BREAKPOINT PHASE 2**

Code implémenté et validé.
- Tests : X/X passing
- @code-reviewer : APPROVED

Feature Document §3 mis à jour.

**Attendre confirmation :** "Continue" ou "Code validé"
---
```

---

## Phase 3 : Finalisation

### Configuration

| Élément | Valeur |
|---------|--------|
| **Thinking** | `think` |
| **Skills** | git-workflow |
| **Subagents** | @doc-generator |

### Process

1. **Commit structuré**
   ```
   feat(scope): description courte

   - Détail 1
   - Détail 2

   Refs: docs/features/<slug>.md
   ```

2. **Documentation** (via @doc-generator)
   - Générer/mettre à jour README si nouveau composant
   - Documenter changements d'API si applicable
   - Mettre à jour CHANGELOG

3. **Préparation PR**
   - Créer la branche si pas fait
   - Préparer le template PR
   - Lister les reviewers

### Output §4

```markdown
## §4 — Finalisation

### Commit
```
feat(user): add email validation

- Create EmailValidator service
- Add validation to User entity
- Update registration controller

Refs: docs/features/user-email-validation.md
```

### Documentation
- **@doc-generator** : 2 fichiers mis à jour
  - README.md (section Configuration)
  - CHANGELOG.md (v1.2.0)

### PR Ready
- Branche : `feature/user-email-validation`
- Tests : ✅ Tous passent
- Lint : ✅ Clean
- Docs : ✅ À jour
```

### ✅ COMPLETION

```
---
✅ **FEATURE COMPLETE**

Feature Document finalisé : docs/features/<slug>.md
- Phase 1 : Plan validé
- Phase 2 : Code implémenté et reviewé
- Phase 3 : Commit et documentation

**Prochaine étape :** Créer la PR ou merger
---
```

---

## Mode --large

En mode `--large`, les différences sont :

| Aspect | Standard | Large |
|--------|----------|-------|
| Thinking P1 | `think hard` | `ultrathink` |
| @security-auditor | Conditionnel | Obligatoire |
| @qa-reviewer | Conditionnel | Obligatoire |
| Breakpoints | Confirmation simple | Validation explicite |
| Feature Document | Standard | Étendu avec sections risques |
