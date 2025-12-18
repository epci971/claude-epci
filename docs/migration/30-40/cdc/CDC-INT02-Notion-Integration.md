# Cahier des Charges — INT-02: Notion Integration

> **Document**: CDC-INT02-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: INT-02
> **Version cible**: EPCI v4.1
> **Priorité**: P1

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

### 1.2 État Actuel (Baseline v3.0.0)

Les Feature Documents EPCI restent **dans le projet**. Pas de synchronisation avec des outils de gestion comme Notion.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Notion** | Outil de productivité avec bases de données et pages |
| **Database** | Base de données Notion (table de features, métriques) |
| **Page** | Page Notion liée à une feature |
| **Sync** | Synchronisation bidirectionnelle Feature Doc ↔ Notion |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Problème** : Les Feature Documents restent isolés dans le projet :
- Pas de vue centralisée des features
- Pas de reporting/dashboard
- Difficile de partager l'avancement
- Métriques dispersées

**Solution** : Intégration Notion pour :
- Centraliser les features dans une database
- Dashboard de métriques automatique
- Synchronisation bidirectionnelle
- Partage facilité avec l'équipe

### 2.2 Objectif

Fournir une **vue centralisée** de toutes les features EPCI avec métriques et reporting, accessible à toute l'équipe.

---

## 3. Fonctionnalités

### 3.1 Feature Database

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Create page** | Fin `/epci-brief` | Crée page Feature dans database |
| **Update status** | Changement phase | Met à jour propriété Status |
| **Sync content** | Fin workflow | Copie Feature Doc dans page |

### 3.2 Propriétés de la Database

| Propriété | Type | Valeurs |
|-----------|------|---------|
| **Name** | Title | Titre de la feature |
| **Status** | Select | 📝 Planning, 🔄 In Progress, ✅ Complete, ❌ Cancelled |
| **Complexity** | Select | TINY, SMALL, STANDARD, LARGE |
| **Estimated Time** | Text | Format "XhYm" |
| **Actual Time** | Text | Format "XhYm" |
| **Tests** | Number | Nombre de tests |
| **Coverage** | Number | % coverage |
| **Created** | Date | Date création |
| **Completed** | Date | Date completion |
| **PR Link** | URL | Lien vers PR GitHub |
| **Feature Doc** | URL | Lien vers fichier local |

### 3.3 Metrics Dashboard

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Push metrics** | Fin workflow | Envoie métriques |
| **Velocity chart** | Hebdo | Met à jour graphique |
| **Quality metrics** | Fin workflow | Coverage, issues |

### 3.4 Structure Notion

```
📁 EPCI Workspace
├── 📊 Features Database
│   ├── [Page] User Preferences
│   │   ├── Status: ✅ Complete
│   │   ├── Complexity: STANDARD
│   │   ├── Time: 2h30 (estimated: 2h)
│   │   ├── Tests: 12 ✅
│   │   └── [Content] Feature Document
│   └── [Page] Notification System
│       └── Status: 🔄 In Progress
│
├── 📈 Metrics Dashboard
│   ├── Velocity Chart
│   ├── Quality Metrics
│   └── Agent Performance
│
└── 📋 Backlog (optional sync)
```

---

## 4. Configuration

### 4.1 Configuration Projet

```json
// project-memory/context.json
{
  "integrations": {
    "notion": {
      "enabled": true,
      "workspace_id": "xxx",
      "features_database_id": "yyy",
      "metrics_database_id": "zzz",
      "auto_sync": true,
      "sync_content": true,
      "sync_on_phase_change": true
    }
  }
}
```

### 4.2 Commande `/epci-notion`

```yaml
---
description: Manage Notion integration
argument-hint: "[status|sync|push|link]"
---

# Usage

/epci-notion status    # Show sync status
/epci-notion sync      # Sync current feature
/epci-notion push      # Push metrics
/epci-notion link      # Get Notion page URL
```

---

## 5. Workflow Intégré

```
/epci-brief "Add user preferences"
         │
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Brief Complete  │ ──► │ 📄 Create Notion page       │
└────────┬────────┘     │    Status: 📝 Planning      │
         │              └─────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Phase 1: Plan   │ ──► │ 📄 Update Notion            │
└────────┬────────┘     │    Status: 🔄 In Progress   │
         │              └─────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Phase 2: Code   │ ──► │ 📄 Update Notion            │
└────────┬────────┘     │    + Tests count, coverage  │
         │              └─────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Phase 3: Final  │ ──► │ 📄 Update Notion            │
└────────┬────────┘     │    Status: ✅ Complete      │
         │              │    + Final metrics          │
         │              │    + Feature Doc content    │
         │              └─────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│   Completion    │ ──► │ 📊 Push to Metrics Dashboard│
└─────────────────┘     └─────────────────────────────┘
```

---

## 6. Exigences Techniques

### 6.1 Notion API

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Création page | POST /pages | P1 |
| [MUST] Update propriétés | PATCH /pages/{id} | P1 |
| [MUST] Append content | PATCH /blocks/{id}/children | P1 |
| [SHOULD] Query database | POST /databases/{id}/query | P2 |

### 6.2 Synchronisation

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Sync propriétés | Status, temps, métriques | P1 |
| [MUST] Sync content | Feature Doc → Notion blocks | P1 |
| [SHOULD] Bidirectionnel | Notion → Feature Doc | P2 |
| [SHOULD] Conflict resolution | Last-write-wins | P2 |

### 6.3 Mode Dégradé

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Sans Notion | Workflow fonctionne sans intégration | P1 |
| [MUST] API indisponible | Retry puis skip avec warning | P1 |
| [MUST] Token invalide | Message explicatif | P1 |

---

## 7. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| INT02-AC1 | Page créée automatiquement | Vérifier Notion |
| INT02-AC2 | Status synchronisé | Changement phase |
| INT02-AC3 | Métriques poussées | Dashboard Notion |
| INT02-AC4 | Contenu synchronisé | Feature Doc dans page |
| INT02-AC5 | Mode dégradé | Test sans Notion config |

---

## 8. Dépendances

### 8.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F04 Project Memory | **Forte** | Configuration Notion stockée |

### 8.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature terminale |

### 8.3 Dépendances Externes

| Dépendance | Type | Description |
|------------|------|-------------|
| Notion API | Optionnelle | Pour synchronisation |
| Notion Token | Optionnelle | Authentification |

---

## 9. Effort Estimé

| Tâche | Effort |
|-------|--------|
| Features database sync | 8h |
| Status sync | 4h |
| Content sync | 6h |
| Metrics dashboard | 6h |
| Commande /epci-notion | 4h |
| Tests | 2h |
| **Total** | **30h (4j)** |

---

## 10. Livrables

1. Module de synchronisation Features Database
2. Module de synchronisation Status
3. Module de synchronisation Content
4. Module Metrics Dashboard
5. Commande `/epci-notion`
6. Template Notion (exportable)
7. Documentation utilisateur
8. Tests unitaires et d'intégration

---

## 11. Sécurité

| Préoccupation | Mesure |
|---------------|--------|
| **Token Notion** | Jamais stocké en clair, variable d'environnement |
| **Données sensibles** | Ne pas sync code source, seulement métriques |
| **Permissions** | Vérifier accès workspace avant sync |
| **Rate limiting** | Respecter limites API Notion |

---

## 12. Template Notion

### 12.1 Database Features (à créer)

```
Name          | Status      | Complexity | Est. Time | Actual | Tests | Coverage
--------------|-------------|------------|-----------|--------|-------|----------
User Prefs    | ✅ Complete | STANDARD   | 2h        | 2h30   | 12    | 87%
Notifications | 🔄 Progress | LARGE      | 4h        | -      | 5     | 45%
Auth Refactor | 📝 Planning | STANDARD   | 3h        | -      | -     | -
```

### 12.2 Dashboard Metrics

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPCI METRICS DASHBOARD                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📊 Velocity (Last 30 days)                                        │
│  ────────────────────────────────────────────────                  │
│  Features completed: 8                                              │
│  Avg time/feature: 2h15                                            │
│  Estimation accuracy: 87%                                           │
│                                                                     │
│  🧪 Quality                                                         │
│  ────────────────────────────────────────────────                  │
│  Avg test count: 10.5                                              │
│  Avg coverage: 82%                                                  │
│  Security issues: 0                                                 │
│                                                                     │
│  📈 Trend                                                           │
│  [Graphique vélocité sur 4 semaines]                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 13. Exemples d'Usage

### 13.1 Sync Automatique

```bash
# Configuration activée, sync automatique
/epci-brief "Add notifications"
# → Page Notion créée automatiquement

/epci  # Workflow complet
# → Status mis à jour à chaque phase
# → Métriques poussées à la fin
```

### 13.2 Commandes Manuelles

```bash
# Vérifier status sync
/epci-notion status
# → Feature: user-preferences
# → Notion Page: https://notion.so/xxx
# → Last Sync: 2025-01-18 14:30
# → Status: ✅ Synced

# Forcer synchronisation
/epci-notion sync

# Obtenir lien Notion
/epci-notion link
# → https://notion.so/workspace/user-preferences-xxx

# Pousser métriques manuellement
/epci-notion push
```

---

## 14. Hors Périmètre

- Intégration autres outils (Linear, Jira, Trello)
- Sync bidirectionnel complet (Notion → Code)
- Notifications Notion
- Commentaires et collaboration temps réel
- Génération de rapports PDF depuis Notion

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
