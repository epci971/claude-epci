# Cahier des Charges — F09: Système de Personas

> **Document**: CDC-F09-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F09
> **Version cible**: EPCI v3.5
> **Priorité**: P1
> **Source**: Analyse WD Framework v2.0 [NEW]

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

EPCI v3.0.0 utilise des **subagents ponctuels** pour validation, mais n'a pas de **mode de pensée global** influençant tout le comportement de Claude.

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Persona** | Mode de pensée global influençant tout le comportement Claude |
| **Subagent** | Composant ponctuel pour validation/génération |
| **MCP** | Model Context Protocol — serveurs enrichissant le contexte |
| **Auto-activation** | Activation automatique basée sur le contexte |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

**Source** : Analyse comparative WD Framework v2.0

**Différence Persona vs Subagent** :

| Aspect | Persona | Subagent |
|--------|---------|----------|
| **Portée** | Tout le workflow | Point de validation |
| **Moment** | Pendant génération | Après génération |
| **Rôle** | Mode de pensée | Vérification |
| **Output** | Influence le code | Verdict (APPROVED/REJECTED) |
| **Activation** | Auto ou `--persona-X` | Toujours aux checkpoints |

**Solution** : Système de 6 personas qui sont des **modes de pensée** influençant la génération de code, les priorités, et les questions posées.

### 2.2 Objectif

Permettre à Claude d'adapter son **comportement global** selon le domaine :
1. **Questions posées** adaptées au domaine
2. **Priorités** selon la hiérarchie de la persona
3. **Code généré** suivant les best practices du domaine
4. **MCP activés** automatiquement selon la persona

---

## 3. Les 6 Personas EPCI

### 3.1 Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPCI PERSONAS (6)                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🏗️  --persona-architect                                           │
│      Pensée système, patterns architecturaux, scalabilité          │
│      Priorités: maintainabilité > scalabilité > performance        │
│                                                                     │
│  🎨  --persona-frontend                                             │
│      UI/UX, accessibilité, Core Web Vitals, design systems         │
│      Priorités: user needs > accessibility > performance           │
│                                                                     │
│  ⚙️  --persona-backend                                              │
│      APIs, data integrity, fiabilité, microservices                │
│      Priorités: reliability > security > performance > features    │
│                                                                     │
│  🔒  --persona-security                                             │
│      Threat modeling, OWASP, audit, compliance                     │
│      Priorités: defense in depth > least privilege > audit         │
│                                                                     │
│  🧪  --persona-qa                                                   │
│      Tests, edge cases, coverage, quality gates                    │
│      Priorités: prevention > detection > correction                │
│                                                                     │
│  📝  --persona-doc                                                  │
│      Documentation, clarté, exemples, API docs                     │
│      Priorités: clarity > completeness > brevity                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Détail de Chaque Persona

#### 🏗️ `--persona-architect`

| Attribut | Valeur |
|----------|--------|
| **Focus** | Pensée système, patterns, scalabilité |
| **Priorités** | Maintainabilité > Scalabilité > Performance |
| **MCP préféré** | Context7 (patterns), Sequential (analyse) |
| **Questions typiques** | "Quel pattern pour découpler X de Y ?" |
| **Trigger keywords** | architecture, design, scalability, pattern, DDD |
| **Trigger files** | `**/Architecture/**`, `**/Domain/**` |

#### 🎨 `--persona-frontend`

| Attribut | Valeur |
|----------|--------|
| **Focus** | UI/UX, accessibilité, Core Web Vitals |
| **Priorités** | User needs > Accessibility > Performance |
| **MCP préféré** | Magic (UI), Playwright (tests), Context7 |
| **Questions typiques** | "Quel composant pour ce use case ?" |
| **Trigger keywords** | component, responsive, accessibility, UI, UX |
| **Trigger files** | `*.jsx`, `*.tsx`, `*.vue`, `*.css` |

#### ⚙️ `--persona-backend`

| Attribut | Valeur |
|----------|--------|
| **Focus** | APIs, data integrity, fiabilité |
| **Priorités** | Reliability > Security > Performance > Features |
| **MCP préféré** | Context7 (patterns), Sequential (debug) |
| **Questions typiques** | "Quelle stratégie de retry ?" |
| **Trigger keywords** | API, database, service, endpoint, repository |
| **Trigger files** | `**/Controller/**`, `**/Service/**`, `**/Repository/**` |

#### 🔒 `--persona-security`

| Attribut | Valeur |
|----------|--------|
| **Focus** | Threat modeling, OWASP, compliance |
| **Priorités** | Defense in depth > Least privilege > Audit |
| **MCP préféré** | Sequential (analyse menaces) |
| **Questions typiques** | "Quelles données sensibles ici ?" |
| **Trigger keywords** | vulnerability, threat, auth, encryption, OWASP |
| **Trigger files** | `**/auth/**`, `**/security/**`, `**/payment/**` |

#### 🧪 `--persona-qa`

| Attribut | Valeur |
|----------|--------|
| **Focus** | Tests, edge cases, coverage |
| **Priorités** | Prevention > Detection > Correction |
| **MCP préféré** | Playwright (E2E), Sequential (stratégie) |
| **Questions typiques** | "Quels edge cases tester ?" |
| **Trigger keywords** | test, coverage, quality, edge case, validation |
| **Trigger files** | `**/tests/**`, `*.spec.*`, `*.test.*` |

#### 📝 `--persona-doc`

| Attribut | Valeur |
|----------|--------|
| **Focus** | Documentation, clarté, exemples |
| **Priorités** | Clarity > Completeness > Brevity |
| **MCP préféré** | Context7 (standards docs) |
| **Questions typiques** | "Quel niveau de détail pour ce public ?" |
| **Trigger keywords** | document, README, wiki, guide, API docs |
| **Trigger files** | `*.md`, `**/docs/**`, `README*` |

---

## 4. Auto-Activation

### 4.1 Algorithme de Scoring

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERSONA AUTO-ACTIVATION                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SCORING MULTI-FACTEURS                                            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Keywords dans le brief     ████████████░░░░░░░░  40%       │   │
│  │  Fichiers impactés          ████████████░░░░░░░░  40%       │   │
│  │  Stack détectée             ████░░░░░░░░░░░░░░░░  20%       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  SEUILS                                                            │
│  ├── Score > 0.6  → Activation automatique                         │
│  ├── Score 0.4-0.6 → Suggestion à l'utilisateur                    │
│  └── Score < 0.4  → Pas d'activation                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Exemple de Scoring

**Brief** : "Ajouter un endpoint API pour les préférences utilisateur"

| Facteur | Persona | Score |
|---------|---------|-------|
| Keywords: "endpoint", "API" | backend | 0.8 |
| Files: Controller, Service | backend | 0.9 |
| Stack: Symfony | backend | 0.7 |
| **Score final** | **backend** | **0.82** |

→ `--persona-backend` activée automatiquement

---

## 5. Structure des Fichiers

```
skills/
└── personas/                          # NOUVEAU dossier
    ├── PERSONAS.md                    # Index et auto-activation
    ├── architect.md                   # 🏗️
    ├── frontend.md                    # 🎨
    ├── backend.md                     # ⚙️
    ├── security.md                    # 🔒
    ├── qa.md                          # 🧪
    └── doc.md                         # 📝
```

### 5.1 Format d'une Persona

```yaml
# skills/personas/backend.md
---
name: backend
description: >-
  Backend specialist. APIs, data integrity, reliability.
  Use when: API, database, service, microservices.
  Not for: UI components, documentation only.
trigger-keywords:
  - api
  - database
  - service
  - endpoint
  - repository
  - migration
trigger-files:
  - "**/Controller/**"
  - "**/Service/**"
  - "**/Repository/**"
  - "**/Entity/**"
priority-hierarchy:
  - reliability
  - security
  - performance
  - features
  - convenience
mcp-preference:
  primary: context7
  secondary: sequential
---

# Persona: Backend ⚙️

## Comportement

Quand cette persona est active, Claude :

1. **Pense fiabilité** — Gestion d'erreurs, retry, fallbacks
2. **Pense sécurité** — Validation inputs, sanitization, auth
3. **Pense performance** — Queries optimisées, caching, indexes
4. **Documente les APIs** — Contracts clairs, versioning

## Principes appliqués

- SOLID systématiquement
- Repository pattern
- Service layer
- DTO pour les APIs
- Validation à chaque couche

## Questions typiques posées

- "Quelle stratégie de retry en cas d'échec ?"
- "Comment gérer la pagination ?"
- "Quel format de réponse API ?"

## Collaboration avec subagents

- Renforce @code-reviewer sur patterns backend
- Active @security-auditor pour endpoints sensibles
```

---

## 6. Matrice Persona × MCP

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | ● | ● | ○ | ○ |
| frontend | ● | ○ | ● | ● |
| backend | ● | ● | ○ | ○ |
| security | ○ | ● | ○ | ○ |
| qa | ○ | ○ | ○ | ● |
| doc | ● | ○ | ○ | ○ |

`●` Auto-activé | `○` Sur demande

---

## 7. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F09-AC1 | 6 personas définies | Fichiers présents dans `skills/personas/` |
| F09-AC2 | Auto-activation fonctionne | Test avec brief varié |
| F09-AC3 | Comportement différencié | Output différent selon persona |
| F09-AC4 | Override manuel respecté | `--persona-X` surcharge auto |
| F09-AC5 | Intégration MCP | MCP activé selon persona |

---

## 8. Dépendances

### 8.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| F10 Flags Universels | Faible | Flags `--persona-X` |
| F12 MCP Integration | Forte | Auto-activation MCP |

### 8.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F05 Clarification | Forte | Questions adaptées à la persona |
| F08 Apprentissage | Forte | Apprentissage par persona |
| F03 Breakpoints | Faible | Affichage persona active |

---

## 9. Effort Estimé

| Tâche | Effort |
|-------|--------|
| 6 fichiers personas | 12h |
| PERSONAS.md index | 2h |
| Scoring auto-activation | 6h |
| Intégration workflow | 4h |
| Intégration MCP | 4h |
| Tests | 4h |
| **Total** | **32h (4j)** |

---

## 10. Livrables

1. `skills/personas/` — Dossier complet avec 6 personas
2. `skills/personas/PERSONAS.md` — Index et documentation
3. Module de scoring auto-activation
4. Intégration avec commandes EPCI
5. Documentation utilisateur
6. Tests unitaires et d'intégration

---

## 11. Coexistence Persona + Subagents

Les personas et subagents sont **complémentaires** :

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERSONA + SUBAGENT                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  --persona-backend active pendant tout le workflow                 │
│       │                                                             │
│       ├── Phase 1: Génère plan orienté API/fiabilité               │
│       │       └── @plan-validator vérifie (ponctuel)               │
│       │                                                             │
│       ├── Phase 2: Code avec patterns backend                      │
│       │       ├── @code-reviewer vérifie (ponctuel)                │
│       │       └── @security-auditor vérifie (ponctuel)             │
│       │                                                             │
│       └── Phase 3: Documentation API                               │
│               └── @doc-generator génère (ponctuel)                 │
│                                                                     │
│  Persona = Influence continue | Subagent = Validation ponctuelle   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 12. Hors Périmètre

- Personas custom par utilisateur (v5+)
- Personas combinées (multi-persona simultanées)
- Marketplace de personas
- Apprentissage de nouvelles personas

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
