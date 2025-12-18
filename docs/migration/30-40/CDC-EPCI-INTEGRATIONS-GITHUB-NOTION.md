# Mini-CDC — Intégrations GitHub & Notion pour EPCI

> **Document**: CDC-EPCI-INT-001  
> **Version**: 1.0.0  
> **Date**: 2025-12-11  
> **Statut**: Draft  
> **Dépendance**: EPCI v4.0 (CDC-EPCI-EVOL-001)

---

## 1. Contexte et Objectifs

### 1.1 Problématique

EPCI fonctionne en isolation. Les développeurs doivent manuellement :
- Créer les branches Git et PRs
- Copier les Feature Documents vers leur outil de gestion
- Synchroniser l'avancement entre Claude et leurs outils
- Exporter les métriques pour reporting

### 1.2 Objectifs

| Objectif | Métrique | Cible |
|----------|----------|-------|
| Réduire les actions manuelles | Clics/feature | -70% |
| Améliorer traçabilité | Lien Feature ↔ PR | 100% |
| Centraliser documentation | Docs dans Notion | Auto |
| Faciliter reporting | Métriques accessibles | Dashboard |

### 1.3 Prérequis

- **EPCI v4.0** avec Project Memory (F04) opérationnel
- **MCP Connectors** GitHub et Notion disponibles
- **Authentification OAuth** configurée par l'utilisateur

---

## 2. Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EPCI CORE v4.0                              │
├─────────────────────────────────────────────────────────────────────┤
│                              │                                      │
│                    ┌─────────┴─────────┐                           │
│                    │ Integration Layer │                           │
│                    └─────────┬─────────┘                           │
│                              │                                      │
│              ┌───────────────┼───────────────┐                     │
│              │               │               │                     │
│              ▼               ▼               ▼                     │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│     │   GitHub    │  │   Notion    │  │   Future    │             │
│     │  Connector  │  │  Connector  │  │ (Slack,etc) │             │
│     └──────┬──────┘  └──────┬──────┘  └─────────────┘             │
│            │                │                                      │
└────────────┼────────────────┼──────────────────────────────────────┘
             │                │
             ▼                ▼
      ┌─────────────┐  ┌─────────────┐
      │   GitHub    │  │   Notion    │
      │    API      │  │    API      │
      └─────────────┘  └─────────────┘
```

---

## 3. INT-01 — GitHub Integration

### 3.1 Fonctionnalités

#### 3.1.1 Branch Management

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Auto-create branch** | Début Phase 2 | Crée `feature/{slug}` depuis `main` |
| **Branch naming** | Convention projet | Applique pattern configuré |
| **Switch branch** | Création | Checkout automatique local |

**Configuration** (dans `project-memory/context.json`):
```json
{
  "integrations": {
    "github": {
      "enabled": true,
      "repository": "owner/repo-name",
      "branch_pattern": "{type}/{ticket}-{slug}",
      "base_branch": "develop",
      "auto_create_branch": true
    }
  }
}
```

#### 3.1.2 Commit Automation

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Commit message** | Fin Phase 2 | Génère message conventionnel |
| **Staged files** | Code généré | Liste fichiers à commiter |
| **Auto-commit** | Option user | Commit avec message généré |

**Format commit généré**:
```
feat(user): add preferences management endpoint

- Add UserPreferencesController with CRUD operations
- Add UserPreferences entity with validation
- Add unit and integration tests (12 tests)

Refs: #123
EPCI: user-preferences
```

#### 3.1.3 Pull Request

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Create PR** | Fin Phase 3 | Ouvre PR vers base branch |
| **PR template** | Config projet | Utilise template EPCI |
| **Auto-fill** | Feature Doc | Remplit description depuis FD |
| **Labels** | Complexité | Ajoute labels (size/S, type/feature) |
| **Reviewers** | Config équipe | Assigne reviewers par défaut |

**Template PR généré**:
```markdown
## 📋 Feature: User Preferences Management

### Summary
[Auto-filled from Feature Document Section 1]

### Changes
- [ ] `src/Controller/UserPreferencesController.php` (new)
- [ ] `src/Entity/UserPreferences.php` (new)
- [ ] `tests/...` (new)

### Testing
- Unit tests: 8 ✅
- Integration tests: 4 ✅
- Coverage: 87%

### EPCI Validation
| Agent | Status |
|-------|--------|
| @plan-validator | ✅ APPROVED |
| @code-reviewer | ✅ APPROVED |
| @security-auditor | ✅ APPROVED |

### Documentation
- Feature Document: `docs/features/user-preferences.md`

---
_Generated by EPCI v4.0_
```

#### 3.1.4 Issue Linking

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Link issue** | Brief contient #123 | Référence dans commits/PR |
| **Update issue** | Fin workflow | Commente avancement |
| **Close issue** | PR merged | Auto-close si configuré |

### 3.2 Commandes

#### /epci-github

```yaml
---
description: Manage GitHub integration for current feature
argument-hint: "[status|branch|commit|pr|sync]"
---

# Usage

/epci-github status    # Show integration status
/epci-github branch    # Create feature branch
/epci-github commit    # Stage and commit changes
/epci-github pr        # Create pull request
/epci-github sync      # Sync all (branch + commit + pr)
```

### 3.3 Workflow Intégré

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPCI + GitHub Workflow                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  /epci-brief "Add user preferences #123"                           │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────────┐                                               │
│  │ Phase 1: Plan   │                                               │
│  └────────┬────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐     ┌─────────────────────────────┐          │
│  │ Phase 2: Code   │ ──► │ 🔀 git checkout -b feature/ │          │
│  └────────┬────────┘     │    user-preferences         │          │
│           │              └─────────────────────────────┘          │
│           ▼                                                         │
│  ┌─────────────────┐     ┌─────────────────────────────┐          │
│  │ Phase 3: Final  │ ──► │ 📝 git commit -m "feat:..." │          │
│  └────────┬────────┘     └─────────────────────────────┘          │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐     ┌─────────────────────────────┐          │
│  │   Completion    │ ──► │ 🔃 Create PR + Link #123    │          │
│  └─────────────────┘     └─────────────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.4 Critères d'Acceptation

| ID | Critère | Test |
|----|---------|------|
| INT01-AC1 | Branche créée automatiquement | Vérifier sur GitHub |
| INT01-AC2 | Commit message conventionnel | Regex validation |
| INT01-AC3 | PR créée avec template | Vérifier contenu PR |
| INT01-AC4 | Issue liée dans PR | Vérifier refs |
| INT01-AC5 | Labels appliqués | Vérifier labels |
| INT01-AC6 | Fonctionne sans config | Mode dégradé OK |

### 3.5 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Branch management | 4h |
| Commit automation | 3h |
| PR creation | 6h |
| Issue linking | 3h |
| Command /epci-github | 4h |
| Tests | 4h |
| **Total INT-01** | **24h (3j)** |

---

## 4. INT-02 — Notion Integration

### 4.1 Fonctionnalités

#### 4.1.1 Feature Document Export

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Export to Notion** | Fin Phase 1 ou 3 | Crée page Notion |
| **Update page** | Chaque phase | Met à jour la page |
| **Link in FD** | Export | Ajoute lien Notion dans FD |

**Structure page Notion générée**:
```
📄 [Feature] User Preferences Management
├── 📋 Status: ✅ Completed
├── 📅 Dates: 2025-01-15 → 2025-01-15
├── 👤 Assignee: @edouard
├── 🏷️ Tags: api, user, backend
│
├── 📝 Description
│   └── [Section 1 du Feature Document]
│
├── ✅ Tasks
│   ├── ☑️ Task 1: Create entity
│   ├── ☑️ Task 2: Create controller
│   └── ...
│
├── 📊 Metrics
│   ├── Estimated: 45 min
│   ├── Actual: 52 min
│   └── Accuracy: 87%
│
├── 🔗 Links
│   ├── GitHub PR: #456
│   ├── Feature Doc: docs/features/...
│   └── Related: #123
│
└── 📜 Validation History
    ├── @plan-validator: ✅ APPROVED
    ├── @code-reviewer: ✅ APPROVED (2 attempts)
    └── @security-auditor: ✅ APPROVED
```

#### 4.1.2 Project Board Sync

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Add to board** | Nouvelle feature | Crée carte dans "To Do" |
| **Move card** | Changement phase | Déplace vers colonne appropriée |
| **Update status** | Fin workflow | Marque "Done" |

**Mapping colonnes**:
```
EPCI Phase    →    Notion Column
─────────────────────────────────
Brief créé         To Do
Phase 1 done       In Progress
Phase 2 done       Review
Phase 3 done       Done
Abandoned          Cancelled
```

#### 4.1.3 Backlog Import

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Import brief** | /epci-notion import | Récupère brief depuis Notion |
| **Parse properties** | Import | Extrait priorité, tags, assignee |
| **Start workflow** | Import | Lance /epci-brief avec données |

**Commande**:
```
/epci-notion import [page-url]
```

#### 4.1.4 Metrics Dashboard

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| **Push metrics** | Fin feature | Envoie métriques à DB Notion |
| **Aggregate** | Daily/Weekly | Met à jour dashboard |
| **Trends** | Historique | Calcule tendances |

**Database Notion "EPCI Metrics"**:
```
| Feature | Complexity | Estimated | Actual | Accuracy | First-Pass | Date |
|---------|------------|-----------|--------|----------|------------|------|
| user-preferences | STANDARD | 45min | 52min | 87% | Yes | 2025-01-15 |
| payment-api | LARGE | 180min | 210min | 86% | No | 2025-01-14 |
```

### 4.2 Configuration

```json
{
  "integrations": {
    "notion": {
      "enabled": true,
      "workspace_id": "xxx",
      "databases": {
        "features": "database-id-features",
        "metrics": "database-id-metrics",
        "backlog": "database-id-backlog"
      },
      "auto_export": true,
      "sync_on_phase_change": true,
      "export_format": "detailed"
    }
  }
}
```

### 4.3 Commandes

#### /epci-notion

```yaml
---
description: Manage Notion integration for EPCI
argument-hint: "[status|export|import|sync|dashboard]"
---

# Usage

/epci-notion status              # Show integration status
/epci-notion export              # Export current feature to Notion
/epci-notion import [url]        # Import brief from Notion page
/epci-notion sync                # Sync all features
/epci-notion dashboard           # Update metrics dashboard
```

### 4.4 Templates Notion

EPCI fournit des templates Notion prêts à l'emploi :

| Template | Description | Contenu |
|----------|-------------|---------|
| **EPCI Features Board** | Kanban des features | Colonnes par phase |
| **EPCI Metrics Dashboard** | Dashboard métriques | Graphiques, KPIs |
| **EPCI Feature Page** | Template de page feature | Structure complète |
| **EPCI Backlog** | Database backlog | Properties EPCI-ready |

**Lien d'installation** (à générer) :
```
https://notion.so/templates/epci-workspace
```

### 4.5 Workflow Intégré

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPCI + Notion Workflow                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐                                              │
│  │  Notion Backlog  │ ◄─── PM ajoute feature request               │
│  │  ┌────────────┐  │                                              │
│  │  │ Feature X  │──┼───► /epci-notion import                      │
│  │  └────────────┘  │            │                                 │
│  └──────────────────┘            ▼                                 │
│                          ┌─────────────┐                           │
│                          │ EPCI Brief  │                           │
│                          └──────┬──────┘                           │
│                                 │                                   │
│  ┌──────────────────┐           │                                  │
│  │  Notion Board    │           │                                  │
│  │  ┌────────────┐  │           │                                  │
│  │  │  To Do     │◄─┼───────────┘ (auto-add)                       │
│  │  └────────────┘  │                                              │
│  │  ┌────────────┐  │                                              │
│  │  │In Progress │◄─┼─── Phase 1 complete                          │
│  │  └────────────┘  │                                              │
│  │  ┌────────────┐  │                                              │
│  │  │  Review    │◄─┼─── Phase 2 complete                          │
│  │  └────────────┘  │                                              │
│  │  ┌────────────┐  │                                              │
│  │  │   Done     │◄─┼─── Phase 3 complete                          │
│  │  └────────────┘  │                                              │
│  └──────────────────┘                                              │
│                                 │                                   │
│  ┌──────────────────┐           │                                  │
│  │ Notion Dashboard │◄──────────┘ (metrics push)                   │
│  │  📊 First-pass: 78%                                             │
│  │  📊 Avg time: 1h12                                              │
│  │  📊 Features/week: 4.2                                          │
│  └──────────────────┘                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.6 Critères d'Acceptation

| ID | Critère | Test |
|----|---------|------|
| INT02-AC1 | Page créée dans Notion | Vérifier page existe |
| INT02-AC2 | Contenu FD exporté | Comparer contenu |
| INT02-AC3 | Board mis à jour | Vérifier colonne |
| INT02-AC4 | Import backlog fonctionne | Tester import |
| INT02-AC5 | Métriques poussées | Vérifier DB metrics |
| INT02-AC6 | Templates installables | Tester lien template |

### 4.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Feature Doc export | 6h |
| Board sync | 4h |
| Backlog import | 4h |
| Metrics dashboard | 5h |
| Command /epci-notion | 3h |
| Templates Notion | 4h |
| Tests | 4h |
| **Total INT-02** | **30h (4j)** |

---

## 5. Configuration Unifiée

### 5.1 /epci-integrations

```yaml
---
description: Configure and manage EPCI integrations
argument-hint: "[status|setup|test|disable]"
---

# Usage

/epci-integrations status          # Show all integrations status
/epci-integrations setup github    # Interactive GitHub setup
/epci-integrations setup notion    # Interactive Notion setup
/epci-integrations test github     # Test GitHub connection
/epci-integrations test notion     # Test Notion connection
/epci-integrations disable github  # Disable GitHub integration
```

### 5.2 Setup Interactif

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔧 EPCI Integration Setup — GitHub                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Step 1/4: Repository                                                │
│ Enter your GitHub repository (owner/repo): _                        │
│                                                                     │
│ Step 2/4: Branch Configuration                                      │
│ Base branch for PRs: [develop]                                      │
│ Branch pattern: [feature/{slug}]                                    │
│                                                                     │
│ Step 3/4: Automation                                                │
│ ☑ Auto-create branch on Phase 2                                    │
│ ☑ Auto-commit with conventional message                            │
│ ☑ Auto-create PR on completion                                     │
│ ☐ Auto-assign reviewers                                            │
│                                                                     │
│ Step 4/4: Test Connection                                           │
│ Testing GitHub API... ✅ Connected                                  │
│ Repository found: ✅ owner/repo                                     │
│ Write access: ✅ Confirmed                                          │
│                                                                     │
│ ✅ GitHub integration configured successfully!                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.3 Status Dashboard

```
/epci-integrations status

┌─────────────────────────────────────────────────────────────────────┐
│ 🔌 EPCI Integrations Status                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─ GitHub ────────────────────────────────────────────────────────┐│
│ │ Status: ✅ Connected                                            ││
│ │ Repository: company/my-project                                  ││
│ │ Last sync: 2 hours ago                                          ││
│ │ Features: auto-branch ✓ auto-commit ✓ auto-pr ✓                ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Notion ────────────────────────────────────────────────────────┐│
│ │ Status: ✅ Connected                                            ││
│ │ Workspace: My Workspace                                         ││
│ │ Databases: features ✓ metrics ✓ backlog ✓                      ││
│ │ Last sync: 30 minutes ago                                       ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Slack ─────────────────────────────────────────────────────────┐│
│ │ Status: ⚪ Not configured                                       ││
│ │ → Run /epci-integrations setup slack                            ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Gestion des Erreurs

### 6.1 Mode Dégradé

Si une intégration échoue, EPCI continue en mode dégradé :

| Situation | Comportement | Message User |
|-----------|--------------|--------------|
| GitHub non connecté | Skip actions GitHub | "⚠️ GitHub not configured, skipping branch creation" |
| API timeout | Retry 2x, puis skip | "⚠️ GitHub unreachable, manual action required" |
| Permission denied | Log erreur, continue | "❌ Cannot create PR: permission denied" |
| Notion page exists | Update instead of create | "ℹ️ Page exists, updating..." |

### 6.2 Logs d'Intégration

```
/epci-integrations logs

┌─ Integration Logs (last 24h) ─────────────────────────────────────┐
│                                                                    │
│ [2025-01-15 14:32] GitHub: Branch created feature/user-preferences│
│ [2025-01-15 14:45] GitHub: Commit pushed (3 files)                │
│ [2025-01-15 14:46] GitHub: PR #456 created                        │
│ [2025-01-15 14:46] Notion: Page updated "User Preferences"        │
│ [2025-01-15 14:46] Notion: Metrics pushed to dashboard            │
│ [2025-01-15 10:15] ⚠️ Notion: Rate limit, retry in 60s           │
│ [2025-01-15 10:16] Notion: Retry successful                       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 7. Sécurité et Permissions

### 7.1 Tokens et Credentials

| Intégration | Type Auth | Stockage | Scope Requis |
|-------------|-----------|----------|--------------|
| GitHub | OAuth / PAT | MCP Connector | repo, workflow |
| Notion | OAuth | MCP Connector | read/write pages, databases |

### 7.2 Principes de Sécurité

- **Tokens jamais en clair** dans les fichiers projet
- **MCP Connectors** gèrent l'authentification
- **Permissions minimales** demandées
- **Révocation facile** via `/epci-integrations disable`

---

## 8. Planning et Effort

### 8.1 Dépendances

```
EPCI v4.0 (F04 Project Memory)
         │
         ▼
┌─────────────────────────────────────┐
│     MCP Connectors Disponibles      │
│  (GitHub MCP + Notion MCP stables)  │
└─────────────────────────────────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
    INT-01          INT-02         INT-03
    GitHub          Notion         (Future)
```

### 8.2 Timeline

```
Après EPCI v4.0 (Avril 2025)

Avril (Semaines 15-16)
├── INT-01: GitHub Integration ████████████████████████ (3j)
└── Tests & Documentation ████████ (1j)

Avril-Mai (Semaines 17-18)
├── INT-02: Notion Integration ██████████████████████████████ (4j)
└── Tests & Documentation ████████ (1j)

Mai (Semaine 19)
└── Intégration finale + Templates ████████████████ (2j)

Release EPCI v4.1 — Mi-Mai 2025
```

### 8.3 Effort Total

| Composant | Effort |
|-----------|--------|
| INT-01: GitHub | 24h |
| INT-02: Notion | 30h |
| Commandes unifiées | 4h |
| Templates Notion | 4h |
| Tests E2E | 8h |
| Documentation | 6h |
| **TOTAL** | **76h (≈10 jours)** |

---

## 9. Évolutions Futures

### 9.1 Autres Intégrations Envisagées

| Intégration | Priorité | Description |
|-------------|----------|-------------|
| **Slack** | P2 | Notifications, commandes slash |
| **Linear** | P2 | Alternative à Notion pour issues |
| **Jira** | P3 | Pour contextes enterprise |
| **GitLab** | P3 | Alternative à GitHub |
| **Discord** | P4 | Pour communautés open-source |

### 9.2 Fonctionnalités Avancées

| Feature | Description | Dépendance |
|---------|-------------|------------|
| **Bi-directional sync** | Notion → EPCI updates | INT-02 stable |
| **Webhook listeners** | React to GitHub events | INT-01 stable |
| **Multi-repo support** | Monorepo / multi-project | INT-01 v2 |
| **Custom exporters** | Plugin system pour exports | Architecture v5 |

---

## 10. Annexes

### 10.1 Schéma MCP

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Claude    │────►│  MCP Host   │────►│   GitHub    │
│   (EPCI)    │     │             │     │    API      │
└─────────────┘     │  ┌───────┐  │     └─────────────┘
                    │  │GitHub │  │
                    │  │Connec.│  │     ┌─────────────┐
                    │  └───────┘  │────►│   Notion    │
                    │  ┌───────┐  │     │    API      │
                    │  │Notion │  │     └─────────────┘
                    │  │Connec.│  │
                    │  └───────┘  │
                    └─────────────┘
```

### 10.2 Références

| Document | Description |
|----------|-------------|
| CDC-EPCI-EVOL-001 | CDC principal EPCI v4.0 |
| GitHub REST API | docs.github.com/rest |
| Notion API | developers.notion.com |
| MCP Specification | modelcontextprotocol.io |

---

*Fin du Mini-CDC Intégrations*

**Document généré par Claude (Assistant IA)**  
**Pour**: Édouard — Développeur FullStack  
**Projet**: EPCI Plugin — Intégrations GitHub & Notion
