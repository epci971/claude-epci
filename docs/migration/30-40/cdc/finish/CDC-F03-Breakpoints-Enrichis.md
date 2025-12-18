# Cahier des Charges — F03: Breakpoints Enrichis

> **Document**: CDC-F03-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F03
> **Version cible**: EPCI v3.1
> **Priorité**: P2

---

## 1. Contexte Global EPCI

### 1.1 Philosophie EPCI v4.0

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHILOSOPHIE EPCI                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 SIMPLICITÉ        — 5 commandes ciblées, pas 22                │
│  📋 TRAÇABILITÉ       — Feature Document pour chaque feature        │
│  ⏸️  BREAKPOINTS       — L'humain valide entre les phases           │
│  🔄 TDD               — Red → Green → Refactor systématique         │
│  🧩 MODULARITÉ        — Skills, Agents, Commands séparés            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Les **BREAKPOINTS** sont un pilier fondamental d'EPCI : ils garantissent que l'humain reste dans la boucle de décision.

### 1.2 État Actuel (Baseline v3.0.0)

Les breakpoints actuels sont **minimalistes** : simple message texte demandant confirmation avant de continuer.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Breakpoint** | Point de pause nécessitant confirmation utilisateur |
| **Scoring** | Évaluation numérique de la complexité/risque |
| **Subagent** | Composant spécialisé effectuant une tâche de validation |
| **Persona** | Mode de pensée influençant tout le comportement Claude |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

Les breakpoints actuels sont minimalistes et ne donnent pas assez de contexte à l'utilisateur avant qu'il valide la continuation.

**Problème** : L'utilisateur valide "à l'aveugle" sans métriques ni aperçu.

**Solution** : Enrichir les breakpoints avec :
- Métriques de complexité et risque
- Verdicts des agents de validation
- Preview de la phase suivante
- Options interactives

### 2.2 Objectif

Transformer le breakpoint d'un simple "Continuer ?" en un **tableau de bord décisionnel** permettant à l'utilisateur de faire un choix éclairé.

---

## 3. Spécifications Fonctionnelles

### 3.1 Format Enrichi du Breakpoint

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 1 — Plan Validé                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: STANDARD (score: 0.58)                             │
│ ├── Fichiers impactés: 7                                           │
│ ├── Temps estimé: 2h30                                             │
│ └── Risque: Modéré (breaking change possible)                      │
│                                                                     │
│ ✅ VALIDATIONS                                                      │
│ ├── @plan-validator: APPROVED                                      │
│ └── Persona active: --persona-backend                              │
│                                                                     │
│ 📋 PREVIEW PHASE 2                                                  │
│ ├── Tâche 1: Créer entité UserPreferences (5 min)                  │
│ ├── Tâche 2: Créer repository (5 min)                              │
│ ├── Tâche 3: Créer service (15 min)                                │
│ └── ... (4 tâches restantes)                                       │
│                                                                     │
│ 🔗 Feature Document: docs/features/user-preferences.md             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options: [Continuer] [Modifier le plan] [Annuler]                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Sections du Breakpoint

| Section | Contenu | Source |
|---------|---------|--------|
| **Métriques** | Complexité, fichiers, temps estimé, risque | Scoring interne |
| **Validations** | Verdicts agents, persona active | Subagents, F09 |
| **Preview** | Prochaines tâches (3-5 premières) | Plan Phase 1 |
| **Liens** | Feature Document, fichiers clés | Chemin fichier |
| **Options** | Actions possibles | Interactif |

### 3.3 Métriques Affichées

| Métrique | Calcul | Affichage |
|----------|--------|-----------|
| **Complexité** | Score 0-1 basé sur fichiers, LOC, dépendances | TINY/SMALL/STANDARD/LARGE + score |
| **Fichiers impactés** | Comptage fichiers dans le plan | Nombre entier |
| **Temps estimé** | Basé sur scoring + historique (F08) | Format XhYm |
| **Risque** | Breaking changes, sécurité, données | Faible/Modéré/Élevé |

### 3.4 Verdicts des Agents

| Agent | Verdict possible | Affiché si |
|-------|------------------|------------|
| @plan-validator | APPROVED / NEEDS_REVISION | Toujours |
| @code-reviewer | APPROVED / NEEDS_CHANGES | Post Phase 2 |
| @security-auditor | PASSED / WARNINGS / FAILED | Si fichiers sensibles |
| @qa-reviewer | PASSED / NEEDS_MORE_TESTS | Si tests complexes |

### 3.5 Options Interactives

| Option | Action | Disponibilité |
|--------|--------|---------------|
| **[Continuer]** | Passer à la phase suivante | Toujours |
| **[Modifier le plan]** | Revenir en édition | Phase 1 uniquement |
| **[Voir détails]** | Afficher Feature Document complet | Toujours |
| **[Annuler]** | Abandonner le workflow | Toujours |

---

## 4. Exigences Techniques

### 4.1 Collecte des Métriques

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Score complexité | Calculer score 0-1 normalisé | P1 |
| [MUST] Comptage fichiers | Extraire du plan | P1 |
| [MUST] Estimation temps | Algorithme basé sur complexité | P1 |
| [SHOULD] Évaluation risque | Détecter breaking changes, sécurité | P2 |
| [MAY] Historique | Comparer avec features passées (F08) | P3 |

### 4.2 Intégration Agents

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Récupérer verdicts | Parser output agents | P1 |
| [MUST] Affichage conditionnel | N'afficher que agents invoqués | P1 |
| [SHOULD] Détails on-demand | Clic pour voir rapport complet | P2 |

### 4.3 Affichage

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Format box | Bordures ASCII art lisibles | P1 |
| [MUST] Codes couleur | Vert/Jaune/Rouge selon status | P1 |
| [MUST] Responsive | S'adapter à la largeur terminal | P2 |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F03-AC1 | Métriques affichées au breakpoint | Test visuel |
| F03-AC2 | Verdicts agents visibles | Test avec agents |
| F03-AC3 | Preview phase suivante | Test workflow complet |
| F03-AC4 | Options interactives fonctionnelles | Test UX |
| F03-AC5 | Format lisible en terminal | Test différentes largeurs |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F04 Project Memory | Forte | Source des métriques historiques |
| F06 Suggestions Proactives | Forte | Scoring de complexité |
| F02 Hooks | Faible | Hook `on-breakpoint` |
| F09 Personas | Faible | Affichage persona active |
| F10 Flags | Faible | Affichage flags actifs |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F07 Orchestration Multi-Agents | Forte | Breakpoints dans orchestration DAG |

---

## 7. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Format enrichi (template) | 4h |
| Collecte métriques | 4h |
| Intégration agents | 3h |
| Options interactives | 2h |
| Tests | 3h |
| **Total** | **14h (2j)** |

---

## 8. Livrables

1. Module de génération breakpoint enrichi
2. Collecteur de métriques
3. Intégration avec subagents
4. Documentation format breakpoint
5. Tests unitaires et d'intégration

---

## 9. Exemples de Breakpoints par Phase

### 9.1 Breakpoint Post-Phase 1 (Plan)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 1 — Plan Validé                                │
├─────────────────────────────────────────────────────────────────────┤
│ 📊 Complexité: STANDARD (0.58) | 7 fichiers | ~2h30 | Risque: Moyen│
│ ✅ @plan-validator: APPROVED                                        │
│ 🎭 Persona: --persona-backend                                       │
│ 📋 Preview: 7 tâches planifiées                                     │
├─────────────────────────────────────────────────────────────────────┤
│ [Continuer Phase 2] [Modifier plan] [Voir détails] [Annuler]       │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.2 Breakpoint Post-Phase 2 (Code)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 2 — Code Implémenté                            │
├─────────────────────────────────────────────────────────────────────┤
│ 📊 7/7 tâches complétées | 12 tests ✅ | Coverage: 87%             │
│ ✅ @code-reviewer: APPROVED (3 suggestions mineures)               │
│ ✅ @security-auditor: PASSED                                        │
│ ⚠️ @qa-reviewer: 2 edge cases à vérifier                           │
│ 📋 Preview Phase 3: Commits, docs, changelog                       │
├─────────────────────────────────────────────────────────────────────┤
│ [Continuer Phase 3] [Corriger issues] [Voir rapports] [Annuler]    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 10. Hors Périmètre

- Breakpoints dans des outils externes (IDE, CI/CD)
- Notifications push pour breakpoints
- Mode batch sans breakpoints (déjà géré par flags)
- Historique des décisions aux breakpoints

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
