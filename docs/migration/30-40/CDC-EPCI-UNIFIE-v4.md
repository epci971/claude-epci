# Cahier des Charges Unifié — EPCI Plugin v4.0

> **Document**: CDC-EPCI-UNIFIE-001  
> **Version**: 1.0.0  
> **Date**: 2025-12-15  
> **Statut**: Validé  
> **Auteur**: Claude (Assistant IA)  
> **Commanditaire**: Édouard (Développeur FullStack)

---

## Table des Matières

1. [Introduction](#1-introduction)
2. [Périmètre et Objectifs](#2-périmètre-et-objectifs)
3. [Vue d'Ensemble des Fonctionnalités](#3-vue-densemble-des-fonctionnalités)
4. [F01 — Java Spring Boot References](#4-f01--java-spring-boot-references)
5. [F02 — Système de Hooks](#5-f02--système-de-hooks)
6. [F03 — Breakpoints Enrichis](#6-f03--breakpoints-enrichis)
7. [F04 — Project Memory](#7-f04--project-memory)
8. [F05 — Clarification Intelligente](#8-f05--clarification-intelligente)
9. [F06 — Suggestions Proactives](#9-f06--suggestions-proactives)
10. [F07 — Orchestration Multi-Agents](#10-f07--orchestration-multi-agents)
11. [F08 — Apprentissage Continu](#11-f08--apprentissage-continu)
12. [F09 — Système de Personas](#12-f09--système-de-personas)
13. [F10 — Flags Universels](#13-f10--flags-universels)
14. [F11 — Wave Orchestration](#14-f11--wave-orchestration)
15. [F12 — MCP Integration](#15-f12--mcp-integration)
16. [INT-01 — GitHub Integration](#16-int-01--github-integration)
17. [INT-02 — Notion Integration](#17-int-02--notion-integration)
18. [Architecture Globale](#18-architecture-globale)
19. [Dépendances Inter-Fonctionnalités](#19-dépendances-inter-fonctionnalités)
20. [Plan de Tests](#20-plan-de-tests)
21. [Planning et Jalons](#21-planning-et-jalons)
22. [Annexes](#22-annexes)

---

## 1. Introduction

### 1.1 Contexte

Le plugin EPCI v3.0.0 est opérationnel avec 23 composants validés (5 commandes, 5 subagents, 13 skills). Ce CDC unifié détaille **14 évolutions majeures** pour transformer EPCI d'un framework de workflow vers une plateforme de développement assisté intelligente.

Ce document consolide :
- Le CDC original EPCI Évolutions (F01-F08)
- Le CDC Intégrations GitHub & Notion (INT-01, INT-02)
- Les enrichissements issus de l'analyse WD Framework (F09-F12)

### 1.2 Philosophie EPCI

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
│  Ces principes sont PRÉSERVÉS dans toutes les évolutions.          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 Documents de Référence

| Document | Version | Description |
|----------|---------|-------------|
| EPCI Plugin v3.0 | 3.0.0 | Baseline actuelle |
| WD Framework v2.0 | 2.1.1 | Source d'inspiration (analyse comparative) |
| Brainstorm Report | 2025-12-15 | Session d'analyse EPCI × WD |

### 1.4 Glossaire

| Terme | Définition |
|-------|------------|
| **Agent/Subagent** | Composant spécialisé effectuant une tâche de validation |
| **Breakpoint** | Point de pause nécessitant confirmation utilisateur |
| **Feature Document** | Document structuré décrivant une feature (§1-§4) |
| **Flag** | Option modifiant le comportement d'une commande |
| **Hook** | Script exécuté automatiquement à un point du workflow |
| **MCP** | Model Context Protocol — serveurs enrichissant le contexte |
| **Orchestrator** | Composant coordonnant l'exécution multi-agents |
| **Persona** | Mode de pensée influençant tout le comportement Claude |
| **Project Memory** | Système de persistance du contexte projet |
| **Skill** | Module de connaissances pour un domaine spécifique |
| **Wave** | Vague d'exécution dans une orchestration multi-étapes |

### 1.5 Conventions du Document

```
[MUST]    — Exigence obligatoire
[SHOULD]  — Exigence recommandée
[MAY]     — Exigence optionnelle
[REF:XX]  — Référence à une autre section
[NEW]     — Nouveauté issue de l'analyse WD Framework
```

---

## 2. Périmètre et Objectifs

### 2.1 Fonctionnalités Incluses

| ID | Fonctionnalité | Version | Priorité | Source |
|----|----------------|---------|----------|--------|
| F01 | Java Spring Boot References | v3.1 | P1 | CDC Original |
| F02 | Système de Hooks | v3.1 | P1 | CDC Original |
| F03 | Breakpoints Enrichis | v3.1 | P2 | CDC Original |
| F04 | Project Memory | v3.5 | P1 | CDC Original |
| F05 | Clarification Intelligente | v3.5 | P1 | CDC Original |
| F06 | Suggestions Proactives | v3.5 | P2 | CDC Original |
| F07 | Orchestration Multi-Agents | v4.0 | P1 | CDC Original |
| F08 | Apprentissage Continu | v4.0 | P1 | CDC Original |
| F09 | Système de Personas | v3.5 | P1 | **[NEW]** WD Analysis |
| F10 | Flags Universels | v3.1 | P1 | **[NEW]** WD Analysis |
| F11 | Wave Orchestration | v4.0 | P2 | **[NEW]** WD Analysis |
| F12 | MCP Integration | v4.0 | P2 | **[NEW]** WD Analysis |
| INT-01 | GitHub Integration | v4.1 | P1 | CDC Intégrations |
| INT-02 | Notion Integration | v4.1 | P1 | CDC Intégrations |

### 2.2 Objectifs Mesurables

| Objectif | Métrique | Cible |
|----------|----------|-------|
| Réduire temps onboarding | Temps premier workflow réussi | < 30 min |
| Améliorer pertinence suggestions | Taux acceptation suggestions | > 70% |
| Accélérer cycles développement | Temps moyen feature STANDARD | -25% |
| Réduire erreurs récurrentes | Issues répétées même cause | -50% |
| Améliorer expérience utilisateur | Score satisfaction (1-5) | > 4.2 |
| Réduire actions manuelles | Clics/feature (avec intégrations) | -70% |
| Améliorer traçabilité | Lien Feature ↔ PR | 100% |

### 2.3 Hors Périmètre

- Marketplace de plugins
- Mode équipe complet (multi-utilisateurs)
- Nouveaux stack skills (Go, Rust, .NET)
- Intégrations Slack, Linear, Jira (CDC futur)

---

## 3. Vue d'Ensemble des Fonctionnalités

### 3.1 Matrice par Phase

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ROADMAP EPCI v3.1 → v4.1                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  v3.1 (Janvier-Février)                                            │
│  ├── F01: Java Spring Boot References                              │
│  ├── F02: Système de Hooks                                         │
│  ├── F03: Breakpoints Enrichis                                     │
│  └── F10: Flags Universels [NEW]                                   │
│                                                                     │
│  v3.5 (Février-Mars)                                               │
│  ├── F04: Project Memory                                           │
│  ├── F05: Clarification Intelligente                               │
│  ├── F06: Suggestions Proactives                                   │
│  └── F09: Système de Personas [NEW]                                │
│                                                                     │
│  v4.0 (Mars-Avril)                                                 │
│  ├── F07: Orchestration Multi-Agents                               │
│  ├── F08: Apprentissage Continu                                    │
│  ├── F11: Wave Orchestration [NEW]                                 │
│  └── F12: MCP Integration [NEW]                                    │
│                                                                     │
│  v4.1 (Avril-Mai)                                                  │
│  ├── INT-01: GitHub Integration                                    │
│  └── INT-02: Notion Integration                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Architecture Cible

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EPCI v4.0 ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     INTERACTION LAYER                        │   │
│  │  Commands │ Flags │ Personas │ Breakpoints                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     INTELLIGENCE LAYER                       │   │
│  │  Clarification │ Suggestions │ Learning │ Scoring            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     ORCHESTRATION LAYER                      │   │
│  │  Wave System │ Multi-Agent │ DAG Execution │ MCP Routing     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     VALIDATION LAYER                         │   │
│  │  @plan-validator │ @code-reviewer │ @security-auditor │ etc. │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     PERSISTENCE LAYER                        │   │
│  │  Project Memory │ Feature History │ Metrics │ Learning       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     INTEGRATION LAYER                        │   │
│  │  GitHub │ Notion │ MCP Servers │ Hooks                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. F01 — Java Spring Boot References

### 4.1 Contexte et Justification

Le skill `java-springboot` est le seul stack skill sans dossier `references/`. Cette inconsistance rompt le pattern Progressive Disclosure appliqué aux autres stacks.

### 4.2 Structure Cible

```
skills/stack/java-springboot/
├── SKILL.md                          # Existant (à enrichir)
└── references/                       # À CRÉER
    ├── architecture.md               # Architecture hexagonale, Clean
    ├── jpa-hibernate.md              # Entity, Repository, Specifications
    ├── security.md                   # Spring Security 6
    ├── testing.md                    # JUnit 5, Mockito, TestContainers
    └── reactive.md                   # WebFlux, R2DBC (optionnel)
```

### 4.3 Exigences par Fichier

#### architecture.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Structure projet | Arborescence Maven/Gradle standard | P1 |
| [MUST] Couches architecture | Controller → Service → Repository | P1 |
| [MUST] Clean Architecture | Ports & Adapters avec Spring | P1 |
| [MUST] Hexagonal | Implémentation avec annotations Spring | P1 |
| [SHOULD] CQRS | Command/Query separation | P2 |
| [SHOULD] Modular monolith | Multi-module Maven/Gradle | P2 |

#### jpa-hibernate.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Entity patterns | Annotations JPA, Lombok, equals/hashCode | P1 |
| [MUST] Repository | JpaRepository, custom queries, Specifications | P1 |
| [MUST] Relations | OneToMany, ManyToOne, fetch strategies | P1 |
| [MUST] N+1 prevention | EntityGraph, JOIN FETCH, batch size | P1 |
| [SHOULD] Auditing | @CreatedDate, @LastModifiedDate, Envers | P2 |
| [SHOULD] Migrations | Flyway/Liquibase patterns | P2 |

#### security.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] SecurityFilterChain | Configuration Spring Security 6 lambda DSL | P1 |
| [MUST] Authentication | JWT, OAuth2, Basic Auth | P1 |
| [MUST] Authorization | @PreAuthorize, Method security | P1 |
| [MUST] CSRF/CORS | Configuration REST API | P1 |
| [SHOULD] Password encoding | BCrypt, Argon2 | P2 |
| [SHOULD] Rate limiting | Bucket4j, Resilience4j | P2 |

#### testing.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] JUnit 5 | @Test, @Nested, @ParameterizedTest | P1 |
| [MUST] Mockito | @Mock, @InjectMocks, verify | P1 |
| [MUST] Spring Boot Test | @SpringBootTest, @WebMvcTest, @DataJpaTest | P1 |
| [MUST] MockMvc | API testing patterns | P1 |
| [SHOULD] TestContainers | PostgreSQL, Redis, Kafka | P2 |
| [SHOULD] ArchUnit | Architecture tests | P2 |

### 4.4 Contraintes Techniques

| Contrainte | Valeur | Justification |
|------------|--------|---------------|
| Taille max par fichier | 400 lignes | Chargement rapide |
| Tokens max par fichier | 3000 tokens | Context window |
| Version Java minimum | Java 17 | LTS actuel |
| Version Spring Boot | 3.2+ | Dernière stable |

### 4.5 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F01-AC1 | 5 fichiers references créés | `ls skills/stack/java-springboot/references/` |
| F01-AC2 | Chaque fichier < 400 lignes | `wc -l` sur chaque fichier |
| F01-AC3 | SKILL.md mis à jour avec liens | Grep `@references/` |
| F01-AC4 | Validation script passe | `python scripts/validate_skill.py` |
| F01-AC5 | Exemples de code compilables | Revue manuelle |

### 4.6 Effort Estimé

| Tâche | Effort |
|-------|--------|
| architecture.md | 4h |
| jpa-hibernate.md | 4h |
| security.md | 4h |
| testing.md | 4h |
| reactive.md | 2h |
| Mise à jour SKILL.md | 1h |
| Tests et validation | 1h |
| **Total** | **20h (2.5j)** |

---

## 5. F02 — Système de Hooks

### 5.1 Contexte et Justification

Le dossier `hooks/` existe mais est vide. Les utilisateurs n'ont aucun moyen d'exécuter des actions automatiques à des points précis du workflow.

### 5.2 Types de Hooks

| Hook | Déclencheur | Cas d'usage |
|------|-------------|-------------|
| `pre-phase-1` | Avant Phase 1 (Planning) | Vérifier prérequis, charger contexte |
| `post-phase-1` | Après Phase 1 | Notifier équipe, créer ticket |
| `pre-phase-2` | Avant Phase 2 (Code) | Setup environnement, linters |
| `post-phase-2` | Après Phase 2 | Run tests supplémentaires, coverage |
| `pre-phase-3` | Avant Phase 3 (Finalize) | Vérifier tests passent |
| `post-phase-3` | Après Phase 3 | Déployer, notifier |
| `on-breakpoint` | À chaque breakpoint | Logging, métriques |

### 5.3 Structure

```
hooks/
├── README.md                    # Documentation
├── runner.py                    # Exécuteur de hooks
├── examples/
│   ├── pre-phase-2-lint.sh     # Exemple linter
│   ├── post-phase-3-notify.py  # Exemple notification
│   └── on-breakpoint-log.sh    # Exemple logging
└── active/                      # Hooks actifs (symlinks)
```

### 5.4 Format d'un Hook

```python
#!/usr/bin/env python3
"""
Hook: post-phase-2
Description: Run additional quality checks after implementation
"""

import sys
import json

def main(context: dict) -> dict:
    """
    Args:
        context: {
            "phase": "phase-2",
            "feature_slug": "user-preferences",
            "files_modified": [...],
            "test_results": {...}
        }
    
    Returns:
        {"status": "success|warning|error", "message": "..."}
    """
    # Hook logic here
    return {"status": "success", "message": "Quality checks passed"}

if __name__ == "__main__":
    context = json.loads(sys.stdin.read())
    result = main(context)
    print(json.dumps(result))
```

### 5.5 Configuration

```json
// project-memory/settings.json
{
  "hooks": {
    "enabled": true,
    "timeout_seconds": 30,
    "fail_on_error": false,
    "active": [
      "pre-phase-2-lint",
      "post-phase-3-notify"
    ]
  }
}
```

### 5.6 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F02-AC1 | runner.py exécute hooks | Test manuel |
| F02-AC2 | 7 points de hook disponibles | Documentation |
| F02-AC3 | Timeout respecté | Test avec hook lent |
| F02-AC4 | Contexte passé correctement | Test avec hook de debug |
| F02-AC5 | Mode dégradé si hook échoue | Test avec hook en erreur |

### 5.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| runner.py | 6h |
| Documentation | 2h |
| 3 exemples hooks | 3h |
| Intégration workflow | 4h |
| Tests | 3h |
| **Total** | **18h (2.5j)** |

---

## 6. F03 — Breakpoints Enrichis

### 6.1 Contexte et Justification

Les breakpoints actuels sont minimalistes. Les enrichir permettrait de donner plus de contexte à l'utilisateur avant qu'il valide.

### 6.2 Format Enrichi

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

### 6.3 Données Affichées

| Section | Contenu | Source |
|---------|---------|--------|
| Métriques | Complexité, fichiers, temps, risque | Scoring F06 |
| Validations | Verdicts agents, persona active | Subagents, F09 |
| Preview | Prochaines tâches | Plan Phase 1 |
| Liens | Feature Document | Chemin fichier |

### 6.4 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F03-AC1 | Métriques affichées | Test visuel |
| F03-AC2 | Verdicts agents visibles | Test avec agents |
| F03-AC3 | Preview phase suivante | Test workflow complet |
| F03-AC4 | Options interactives | Test UX |

### 6.5 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Format enrichi | 4h |
| Collecte métriques | 4h |
| Intégration agents | 3h |
| Tests | 3h |
| **Total** | **14h (2j)** |

---

## 7. F04 — Project Memory

### 7.1 Contexte et Justification

EPCI n'a pas de mémoire entre sessions. Chaque nouvelle session repart de zéro sans contexte projet.

### 7.2 Structure

```
project-memory/
├── context.json              # Contexte projet global
├── conventions.json          # Conventions détectées/définies
├── history/
│   ├── features/             # Historique features
│   │   ├── user-auth.json
│   │   └── user-preferences.json
│   └── decisions/            # Décisions architecturales
├── patterns/
│   ├── detected.json         # Patterns auto-détectés
│   └── custom.json           # Patterns définis par user
├── metrics/
│   ├── velocity.json         # Métriques de vélocité
│   └── quality.json          # Métriques qualité
└── learning/
    ├── corrections.json      # Corrections appliquées
    └── preferences.json      # Préférences utilisateur
```

### 7.3 context.json

```json
{
  "project": {
    "name": "my-symfony-app",
    "stack": "php-symfony",
    "detected_at": "2025-01-15T10:00:00Z"
  },
  "team": {
    "primary_developer": "Édouard",
    "code_style": "PSR-12"
  },
  "integrations": {
    "github": {
      "enabled": true,
      "repository": "owner/repo",
      "branch_pattern": "feature/{slug}"
    },
    "notion": {
      "enabled": true,
      "workspace_id": "xxx",
      "features_database": "yyy"
    }
  },
  "epci": {
    "version": "4.0.0",
    "features_completed": 15,
    "last_session": "2025-01-20T14:30:00Z"
  }
}
```

### 7.4 Commande /epci-memory

```yaml
---
description: Manage project memory
argument-hint: "[status|init|reset|export]"
---

# Usage

/epci-memory status      # Affiche état mémoire
/epci-memory init        # Initialise mémoire projet
/epci-memory reset       # Réinitialise (avec confirmation)
/epci-memory export      # Exporte en JSON
```

### 7.5 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F04-AC1 | Structure créée à l'init | `ls project-memory/` |
| F04-AC2 | Context chargé au démarrage | Logs |
| F04-AC3 | Historique features sauvé | Après workflow complet |
| F04-AC4 | Export fonctionnel | `/epci-memory export` |

### 7.6 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Structure données | 6h |
| Commande /epci-memory | 4h |
| Chargement auto | 6h |
| Sauvegarde features | 6h |
| Détection patterns | 8h |
| Tests | 4h |
| **Total** | **34h (4.5j)** |

---

## 8. F05 — Clarification Intelligente

### 8.1 Contexte et Justification

La phase de clarification dans `/epci-brief` pose des questions génériques. Avec Project Memory, on peut poser des questions contextuelles.

### 8.2 Fonctionnement

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLARIFICATION INTELLIGENTE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Brief: "Ajouter un système de notifications"                       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 ANALYSE CONTEXTUELLE                         │   │
│  │                                                               │   │
│  │  Project Memory dit:                                          │   │
│  │  ├── Stack: Symfony + Messenger                              │   │
│  │  ├── Pattern: Event-driven déjà en place                     │   │
│  │  └── Feature similaire: user-alerts (il y a 2 mois)          │   │
│  │                                                               │   │
│  │  Questions générées:                                          │   │
│  │  ├── "Voulez-vous réutiliser le pattern Event de user-alerts?"│   │
│  │  ├── "Quels canaux: email, push, in-app?"                    │   │
│  │  └── "Intégration avec Messenger existant?"                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 8.3 Sources de Contexte

| Source | Données | Usage |
|--------|---------|-------|
| Project Memory | Features passées | Suggestions réutilisation |
| Stack Skill | Patterns framework | Questions techniques |
| Persona Active | Priorités | Orientation questions |
| MCP Context7 | Docs externes | Best practices |

### 8.4 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F05-AC1 | Questions contextuelles | Test avec historique |
| F05-AC2 | Max 3 questions | Comptage |
| F05-AC3 | Références features passées | Présence dans questions |
| F05-AC4 | Adaptation à la persona | Test avec différentes personas |

### 8.5 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Analyse contextuelle | 8h |
| Génération questions | 6h |
| Intégration Memory | 4h |
| Intégration Personas | 4h |
| Tests | 3h |
| **Total** | **25h (3j)** |

---

## 9. F06 — Suggestions Proactives

### 9.1 Contexte et Justification

EPCI est réactif. Avec l'historique et les patterns, il peut devenir proactif et suggérer des améliorations.

### 9.2 Types de Suggestions

| Type | Déclencheur | Exemple |
|------|-------------|---------|
| **Pattern réutilisable** | Code similaire détecté | "Ce service ressemble à UserService, extraire un trait?" |
| **Test manquant** | Coverage < seuil | "Aucun test pour la méthode X" |
| **Refactoring** | Dette technique | "Cette classe dépasse 500 lignes" |
| **Sécurité** | Pattern risqué | "Input non validé détecté" |
| **Performance** | Anti-pattern | "N+1 query potentiel" |

### 9.3 Affichage

```
┌─────────────────────────────────────────────────────────────────────┐
│ 💡 SUGGESTIONS PROACTIVES                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [P1] 🔒 Sécurité                                                  │
│  └── Le paramètre 'email' n'est pas validé dans register()         │
│      Suggestion: Ajouter Assert\Email                               │
│      [Appliquer] [Ignorer] [Ne plus suggérer]                      │
│                                                                     │
│  [P2] ♻️ Refactoring                                                │
│  └── Pattern Repository similaire à ProductRepository              │
│      Suggestion: Extraire AbstractCrudRepository                   │
│      [Voir détails] [Ignorer]                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.4 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F06-AC1 | Suggestions pertinentes | Taux acceptation > 70% |
| F06-AC2 | Prioritisation | P1 avant P2 |
| F06-AC3 | Action "Ignorer" fonctionne | Ne revient pas |
| F06-AC4 | Apprentissage préférences | Suggestions adaptées |

### 9.5 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Détection patterns | 8h |
| Génération suggestions | 6h |
| UI suggestions | 4h |
| Apprentissage | 4h |
| Tests | 2h |
| **Total** | **24h (3j)** |

---

## 10. F07 — Orchestration Multi-Agents

### 10.1 Contexte et Justification

Les subagents s'exécutent séquentiellement. Pour les features LARGE, une orchestration parallèle/DAG serait plus efficace.

### 10.2 Modes d'Orchestration

| Mode | Description | Quand |
|------|-------------|-------|
| **Séquentiel** | Un agent après l'autre | Dépendances fortes |
| **Parallèle** | Agents indépendants simultanés | Validations indépendantes |
| **DAG** | Graphe de dépendances | Features complexes |

### 10.3 DAG Exemple

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DAG ORCHESTRATION                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ┌──────────────────┐                            │
│                    │ @plan-validator  │                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│              ┌──────────────┼──────────────┐                       │
│              ▼              ▼              ▼                       │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│    │@code-review │ │@security   │ │@qa-reviewer │                │
│    └──────┬──────┘ └──────┬─────┘ └──────┬──────┘                │
│           │               │              │                         │
│           └───────────────┼──────────────┘                         │
│                           ▼                                         │
│                  ┌─────────────────┐                               │
│                  │ @doc-generator  │                               │
│                  └─────────────────┘                               │
│                                                                     │
│  Parallèle: code-review, security, qa (pas de dépendance)         │
│  Séquentiel: plan-validator → ... → doc-generator                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 10.4 Composant Orchestrator

```python
# agents/orchestrator.py

class Orchestrator:
    def __init__(self, dag: Dict[str, List[str]]):
        self.dag = dag
        self.results = {}
    
    def execute(self) -> Dict[str, AgentResult]:
        """
        Exécute les agents selon le DAG.
        Parallélise quand possible.
        """
        # Topological sort + parallel execution
        pass
```

### 10.5 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F07-AC1 | Exécution parallèle | Temps < séquentiel |
| F07-AC2 | Respect dépendances | Ordre correct |
| F07-AC3 | Gestion erreurs | Un agent échoue → suite gérée |
| F07-AC4 | Timeout global | Configurable |

### 10.6 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Orchestrator core | 12h |
| DAG builder | 6h |
| Exécution parallèle | 8h |
| Gestion erreurs | 4h |
| Tests | 4h |
| **Total** | **34h (4.5j)** |

---

## 11. F08 — Apprentissage Continu

### 11.1 Contexte et Justification

EPCI ne s'améliore pas avec l'usage. Un système de feedback et apprentissage permettrait d'améliorer les suggestions et estimations.

### 11.2 Boucle d'Apprentissage

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LEARNING LOOP                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌───────────┐     ┌───────────┐     ┌───────────┐              │
│    │  MESURE   │ ──► │  ANALYSE  │ ──► │  ADAPTE   │              │
│    └───────────┘     └───────────┘     └───────────┘              │
│         │                                     │                     │
│         │                                     │                     │
│         └─────────────────────────────────────┘                    │
│                         │                                           │
│                         ▼                                           │
│                  ┌─────────────┐                                   │
│                  │   AMÉLIORE  │                                   │
│                  └─────────────┘                                   │
│                                                                     │
│  MESURE: Temps réel, estimé, déviations, erreurs                   │
│  ANALYSE: Patterns, corrélations, causes                           │
│  ADAPTE: Ajuste modèles, seuils, suggestions                       │
│  AMÉLIORE: Prochaine estimation plus précise                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 11.3 Métriques Collectées

| Métrique | Usage |
|----------|-------|
| Temps estimé vs réel | Calibrer estimations |
| Suggestions acceptées/rejetées | Améliorer pertinence |
| Erreurs récurrentes | Prévenir proactivement |
| Patterns de correction | Suggérer automatiquement |
| Vélocité par type | Affiner scoring complexité |

### 11.4 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F08-AC1 | Métriques collectées | Fichiers learning/ |
| F08-AC2 | Estimations améliorées | Variance diminue |
| F08-AC3 | Suggestions pertinentes | Taux acceptation augmente |
| F08-AC4 | Feedback intégré | Commande /epci-learn |

### 11.5 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Collecte métriques | 8h |
| Analyse patterns | 10h |
| Modèle apprentissage | 10h |
| Commande /epci-learn | 4h |
| Tests | 3h |
| **Total** | **35h (4.5j)** |

---

## 12. F09 — Système de Personas [NEW]

### 12.1 Contexte et Justification

**Source**: Analyse WD Framework v2.0

Les subagents EPCI sont des validateurs ponctuels. Les Personas sont des **modes de pensée** qui influencent TOUT le comportement de Claude pendant une session.

### 12.2 Les 6 Personas EPCI

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

### 12.3 Structure Fichiers

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

### 12.4 Format d'une Persona

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

### 12.5 Auto-activation

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
│  EXEMPLE                                                            │
│  Brief: "Ajouter un endpoint API pour les préférences utilisateur" │
│  ├── Keywords: "endpoint", "API" → backend (0.8)                   │
│  ├── Fichiers: Controller, Service → backend (0.9)                 │
│  └── Score final: 0.82 → --persona-backend activée                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 12.6 Différence Persona vs Subagent

| Aspect | Persona | Subagent |
|--------|---------|----------|
| **Portée** | Tout le workflow | Point de validation |
| **Moment** | Pendant génération | Après génération |
| **Rôle** | Mode de pensée | Vérification |
| **Output** | Influence le code | Verdict (APPROVED/REJECTED) |
| **Activation** | Auto ou `--persona-X` | Toujours aux checkpoints |

**Coexistence** : Persona active + Subagents qui valident = complémentaire.

### 12.7 Matrice Persona × MCP

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | ● | ● | ○ | ○ |
| frontend | ● | ○ | ● | ● |
| backend | ● | ● | ○ | ○ |
| security | ○ | ● | ○ | ○ |
| qa | ○ | ○ | ○ | ● |
| doc | ● | ○ | ○ | ○ |

`●` Auto-activé | `○` Sur demande

### 12.8 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F09-AC1 | 6 personas définies | Fichiers présents |
| F09-AC2 | Auto-activation fonctionne | Test avec brief varié |
| F09-AC3 | Comportement différencié | Output selon persona |
| F09-AC4 | Override manuel | `--persona-X` respecté |
| F09-AC5 | Intégration MCP | MCP activé selon persona |

### 12.9 Effort Estimé

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

## 13. F10 — Flags Universels [NEW]

### 13.1 Contexte et Justification

**Source**: Analyse WD Framework v2.0

Le flag `--large` actuel est binaire. Un système de flags granulaires permet un contrôle fin de la profondeur d'analyse et du comportement.

### 13.2 Catégories de Flags

```yaml
# settings/flags.md

## THINKING FLAGS — Profondeur d'analyse

--think              # Standard (~4K tokens)
                     # Analyse multi-fichiers, dépendances directes
                     # Auto: 3-10 fichiers impactés

--think-hard         # Approfondi (~10K tokens)
                     # Analyse système entier, impacts indirects
                     # Auto: >10 fichiers OU refactoring OU migration

--ultrathink         # Critique (~32K tokens)
                     # Refonte majeure, décisions irréversibles
                     # JAMAIS auto (explicite uniquement)


## COMPRESSION FLAGS — Gestion tokens

--uc                 # Ultra-compressed output (30-50% tokens)
                     # Symboles: ✓/✗/⚠️, abréviations
                     # Auto: context > 75% utilisé

--verbose            # Output détaillé, explications complètes
                     # Opposé de --uc


## WORKFLOW FLAGS — Contrôle exécution

--safe               # Mode conservateur
                     # Toutes validations, confirmations supplémentaires
                     # Auto: production, données sensibles

--fast               # Skip validations optionnelles
                     # Pour itérations rapides en dev
                     # Incompatible avec --safe

--dry-run            # Simulation sans modifications
                     # Affiche ce qui serait fait


## WAVE FLAGS — Orchestration multi-vagues

--wave               # Active le découpage en vagues
                     # Pour features LARGE uniquement

--wave-strategy      # Stratégie de découpage
    progressive      # Itératif, validation entre vagues
    systematic       # Méthodique, analyse complète puis exécution
```

### 13.3 Règles de Précédence

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLAG PRECEDENCE RULES                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Flags explicites > Auto-activation                             │
│  2. --safe > --fast (safety first)                                 │
│  3. Thinking: --ultrathink > --think-hard > --think                │
│  4. --uc auto-active si context > 75%                              │
│  5. --wave implicite si --think-hard + LARGE                       │
│                                                                     │
│  CONFLITS                                                          │
│  ├── --safe + --fast → Erreur, incompatible                        │
│  ├── --uc + --verbose → --verbose gagne (explicite)                │
│  └── --think + --think-hard → --think-hard gagne                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 13.4 Auto-activation

| Flag | Condition | Seuil |
|------|-----------|-------|
| `--think` | Fichiers impactés | 3-10 fichiers |
| `--think-hard` | Fichiers OU refactoring | >10 fichiers OU migration |
| `--uc` | Context window usage | > 75% |
| `--safe` | Fichiers sensibles | **/auth/**, **/payment/** |
| `--wave` | Complexité LARGE | score > 0.7 |

### 13.5 Intégration Commandes

```bash
# Exemples d'usage

# Équivalent ancien --large
/epci --think-hard --wave

# Feature sécurité avec toutes validations
/epci --persona-security --think-hard --safe

# Quick fix sans overhead
/epci-quick --fast

# Refonte majeure
/epci --ultrathink --wave-strategy systematic

# Debug avec analyse approfondie
/epci-spike 1h --think-hard "Pourquoi les perfs sont dégradées?"
```

### 13.6 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F10-AC1 | Tous flags documentés | settings/flags.md |
| F10-AC2 | Auto-activation fonctionne | Tests automatisés |
| F10-AC3 | Précédence respectée | Tests conflits |
| F10-AC4 | Intégration toutes commandes | Test chaque commande |
| F10-AC5 | --uc réduit tokens | Mesure avant/après |

### 13.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Documentation flags | 4h |
| Parsing flags | 4h |
| Auto-activation | 6h |
| Intégration commandes | 6h |
| Tests | 4h |
| **Total** | **24h (3j)** |

---

## 14. F11 — Wave Orchestration [NEW]

### 14.1 Contexte et Justification

**Source**: Analyse WD Framework v2.0

Pour les features LARGE, une exécution monolithique perd le fil. Le découpage en "vagues" avec accumulation de contexte améliore les résultats de 30-50%.

### 14.2 Concept

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WAVE ORCHESTRATION                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SANS WAVE (actuel --large)                                        │
│  ════════════════════════════════════════════════════════►         │
│  Exécution monolithique, risque de perdre le fil                   │
│                                                                     │
│  AVEC WAVE (--wave)                                                │
│                                                                     │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│  │ Vague 1 │ ──► │ Vague 2 │ ──► │ Vague 3 │ ──► │ Vague 4 │      │
│  │ Analyse │     │  Core   │     │ Périph. │     │  Tests  │      │
│  │ + Fonda.│     │         │     │         │     │ + Docs  │      │
│  └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘      │
│       │               │               │               │            │
│       ▼               ▼               ▼               ▼            │
│   Contexte        Contexte        Contexte        Contexte         │
│   initial         enrichi         complet          final           │
│                                                                     │
│  Breakpoint optionnel entre chaque vague (si --safe)               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 14.3 Stratégies

| Stratégie | Description | Cas d'usage |
|-----------|-------------|-------------|
| **progressive** | Vague par vague avec validation | Incertitude, besoin feedback fréquent |
| **systematic** | Analyse complète d'abord, puis exécution groupée | Feature bien définie, confiance élevée |

### 14.4 Découpage Automatique

```
Feature: "Système de notifications multi-canal"
Complexité: LARGE (score: 0.82)
Stratégie: progressive

┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 1 — Fondations                                               │
├─────────────────────────────────────────────────────────────────────┤
│ ├── Entité Notification                                            │
│ ├── NotificationRepository                                         │
│ ├── NotificationService (base)                                     │
│ └── Tests unitaires fondations                                     │
│                                                                     │
│ Contexte acquis: Structure données, interfaces de base             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 2 — Canaux                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ ├── NotificationChannelInterface                                   │
│ ├── EmailNotificationChannel                                       │
│ ├── PushNotificationChannel                                        │
│ ├── InAppNotificationChannel                                       │
│ └── Tests unitaires canaux                                         │
│                                                                     │
│ Contexte enrichi: Patterns canal, templates                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 3 — Orchestration                                            │
├─────────────────────────────────────────────────────────────────────┤
│ ├── NotificationDispatcher                                         │
│ ├── Integration Symfony Messenger                                  │
│ ├── Retry logic + Dead letter                                      │
│ └── Tests intégration                                              │
│                                                                     │
│ Contexte complet: Flow complet, edge cases                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VAGUE 4 — Finalisation                                             │
├─────────────────────────────────────────────────────────────────────┤
│ ├── Tests E2E                                                      │
│ ├── Documentation API                                              │
│ ├── Migration script                                               │
│ └── Feature Document §3-§4                                         │
│                                                                     │
│ Contexte final: Prêt pour review                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### 14.5 Intégration avec Flags

```bash
# Activation explicite
/epci --wave --wave-strategy progressive

# Activation implicite (LARGE + think-hard)
/epci --think-hard   # Si LARGE détecté → --wave auto

# Forcer sans wave même si LARGE
/epci --think-hard --no-wave
```

### 14.6 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F11-AC1 | Découpage automatique | Test feature LARGE |
| F11-AC2 | 2 stratégies fonctionnelles | Test progressive et systematic |
| F11-AC3 | Contexte accumulé | Vague N voit résultats N-1 |
| F11-AC4 | Breakpoints entre vagues (si --safe) | Test mode safe |
| F11-AC5 | Intégration F07 Orchestration | Agents par vague |

### 14.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Wave planner | 8h |
| Stratégie progressive | 4h |
| Stratégie systematic | 4h |
| Accumulation contexte | 6h |
| Intégration orchestrator | 6h |
| Tests | 4h |
| **Total** | **32h (4j)** |

---

## 15. F12 — MCP Integration [NEW]

### 15.1 Contexte et Justification

**Source**: Analyse WD Framework v2.0

Les MCP (Model Context Protocol) servers enrichissent le contexte de Claude avec des données externes. 4 MCPs sont pertinents pour EPCI.

### 15.2 Les 4 MCPs

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP SERVERS EPCI                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📚 CONTEXT7 — Documentation librairies                            │
│  ├── Fonction: Recherche docs librairies/frameworks externes       │
│  ├── URL: https://context7.dev                                     │
│  ├── Déclencheurs:                                                 │
│  │   ├── Imports externes détectés                                 │
│  │   ├── Questions sur un framework                                │
│  │   └── --persona-frontend ou --persona-backend                   │
│  └── Exemple: "Doctrine pagination" → KnpPaginator, Pagerfanta     │
│                                                                     │
│  🔗 SEQUENTIAL — Analyse multi-étapes                               │
│  ├── Fonction: Raisonnement structuré pour problèmes complexes     │
│  ├── Déclencheurs:                                                 │
│  │   ├── --think-hard ou --ultrathink                              │
│  │   ├── Debugging complexe                                        │
│  │   └── --persona-architect ou --persona-security                 │
│  └── Exemple: "Perf dégradée" → Analyse systématique 5 étapes      │
│                                                                     │
│  ✨ MAGIC — Génération UI                                           │
│  ├── Fonction: Génération composants UI modernes (21st.dev)        │
│  ├── Déclencheurs:                                                 │
│  │   ├── --persona-frontend                                        │
│  │   ├── Fichiers *.jsx, *.tsx, *.vue                              │
│  │   └── Keywords: component, button, form, modal                  │
│  └── Exemple: "DataTable" → Composant accessible + variants        │
│                                                                     │
│  🎭 PLAYWRIGHT — Tests E2E & Browser                                │
│  ├── Fonction: Automatisation browser, tests E2E, a11y             │
│  ├── Déclencheurs:                                                 │
│  │   ├── --persona-qa                                              │
│  │   ├── Fichiers *.spec.ts, *.e2e.ts                              │
│  │   └── Keywords: e2e, browser, accessibility                     │
│  └── Exemple: "Test inscription" → Parcours complet + a11y         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 15.3 Structure

```
skills/
└── mcp/                               # NOUVEAU dossier
    ├── MCP.md                         # Index et configuration
    ├── context7.md                    # Documentation Context7
    ├── sequential.md                  # Documentation Sequential
    ├── magic.md                       # Documentation Magic
    └── playwright.md                  # Documentation Playwright
```

### 15.4 Configuration

```json
// project-memory/settings.json
{
  "mcp": {
    "enabled": true,
    "servers": {
      "context7": {
        "enabled": true,
        "auto_activate": true
      },
      "sequential": {
        "enabled": true,
        "auto_activate": true
      },
      "magic": {
        "enabled": true,
        "auto_activate": true
      },
      "playwright": {
        "enabled": true,
        "auto_activate": true
      }
    }
  }
}
```

### 15.5 Matrice Persona × MCP

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | ● | ● | ○ | ○ |
| frontend | ● | ○ | ● | ● |
| backend | ● | ● | ○ | ○ |
| security | ○ | ● | ○ | ○ |
| qa | ○ | ○ | ○ | ● |
| doc | ● | ○ | ○ | ○ |

`●` Auto-activé avec persona | `○` Disponible sur demande

### 15.6 Mode Dégradé

Si un MCP est indisponible :

| Situation | Comportement | Message |
|-----------|--------------|---------|
| MCP timeout | Retry 2x, puis skip | "⚠️ Context7 unreachable, continuing without" |
| MCP non configuré | Skip silencieux | — |
| MCP erreur | Log, continue | "⚠️ Sequential error, fallback to standard" |

### 15.7 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| F12-AC1 | 4 MCPs documentés | Fichiers présents |
| F12-AC2 | Auto-activation persona | Test avec personas |
| F12-AC3 | Configuration projet | settings.json |
| F12-AC4 | Mode dégradé | Test avec MCP down |
| F12-AC5 | Flags manuels | --c7, --seq, --magic, --play |

### 15.8 Effort Estimé

| Tâche | Effort |
|-------|--------|
| 4 fichiers documentation | 8h |
| MCP.md index | 2h |
| Auto-activation | 6h |
| Intégration personas | 4h |
| Mode dégradé | 4h |
| Tests | 4h |
| **Total** | **28h (3.5j)** |

---

## 16. INT-01 — GitHub Integration

### 16.1 Contexte et Justification

EPCI fonctionne en isolation. Les développeurs doivent manuellement créer branches, commits et PRs.

### 16.2 Fonctionnalités

#### Branch Management

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| Auto-create branch | Début Phase 2 | Crée `feature/{slug}` depuis base |
| Branch naming | Convention projet | Applique pattern configuré |
| Switch branch | Création | Checkout automatique |

#### Commit Automation

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| Commit message | Fin Phase 2 | Génère message conventionnel |
| Staged files | Code généré | Liste fichiers à commiter |
| Auto-commit | Option user | Commit avec message généré |

**Format commit** :
```
feat(user): add preferences management endpoint

- Add UserPreferencesController with CRUD operations
- Add UserPreferences entity with validation
- Add unit and integration tests (12 tests)

Refs: #123
EPCI: user-preferences
```

#### Pull Request

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| Create PR | Fin Phase 3 | Ouvre PR vers base branch |
| PR template | Config projet | Utilise template EPCI |
| Auto-fill | Feature Doc | Remplit description |
| Labels | Complexité | size/S, type/feature |
| Reviewers | Config équipe | Assigne reviewers |

### 16.3 Configuration

```json
// project-memory/context.json
{
  "integrations": {
    "github": {
      "enabled": true,
      "repository": "owner/repo-name",
      "branch_pattern": "{type}/{ticket}-{slug}",
      "base_branch": "develop",
      "auto_create_branch": true,
      "auto_commit": true,
      "auto_pr": true,
      "reviewers": ["reviewer1", "reviewer2"]
    }
  }
}
```

### 16.4 Commande /epci-github

```yaml
---
description: Manage GitHub integration for current feature
argument-hint: "[status|branch|commit|pr|sync]"
---

/epci-github status    # Show integration status
/epci-github branch    # Create feature branch
/epci-github commit    # Stage and commit changes
/epci-github pr        # Create pull request
/epci-github sync      # Sync all (branch + commit + pr)
```

### 16.5 Workflow Intégré

```
/epci-brief "Add user preferences #123"
         │
         ▼
┌─────────────────┐
│ Phase 1: Plan   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Phase 2: Code   │ ──► │ 🔀 git checkout -b feature/ │
└────────┬────────┘     │    user-preferences         │
         │              └─────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│ Phase 3: Final  │ ──► │ 📝 git commit -m "feat:..." │
└────────┬────────┘     └─────────────────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│   Completion    │ ──► │ 🔃 Create PR + Link #123    │
└─────────────────┘     └─────────────────────────────┘
```

### 16.6 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| INT01-AC1 | Branche créée automatiquement | Vérifier sur GitHub |
| INT01-AC2 | Commit message conventionnel | Regex validation |
| INT01-AC3 | PR créée avec template | Vérifier sur GitHub |
| INT01-AC4 | Issue liée | Refs dans PR |
| INT01-AC5 | Mode dégradé | Test sans GitHub |

### 16.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Branch management | 6h |
| Commit automation | 4h |
| PR creation | 6h |
| Issue linking | 2h |
| Commande /epci-github | 4h |
| Tests | 2h |
| **Total** | **24h (3j)** |

---

## 17. INT-02 — Notion Integration

### 17.1 Contexte et Justification

Les Feature Documents restent dans le projet. Une synchronisation Notion permettrait un suivi centralisé et du reporting.

### 17.2 Fonctionnalités

#### Feature Database

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| Create page | Fin /epci-brief | Crée page Feature |
| Update status | Changement phase | Met à jour propriété |
| Sync content | Fin workflow | Copie Feature Doc |

#### Metrics Dashboard

| Fonction | Déclencheur | Action |
|----------|-------------|--------|
| Push metrics | Fin workflow | Envoie métriques |
| Velocity chart | Hebdo | Met à jour graphique |
| Quality metrics | Fin workflow | Coverage, issues |

### 17.3 Structure Notion

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

### 17.4 Configuration

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
      "sync_content": true
    }
  }
}
```

### 17.5 Commande /epci-notion

```yaml
---
description: Manage Notion integration
argument-hint: "[status|sync|push|link]"
---

/epci-notion status    # Show sync status
/epci-notion sync      # Sync current feature
/epci-notion push      # Push metrics
/epci-notion link      # Get Notion page URL
```

### 17.6 Critères d'Acceptation

| ID | Critère | Vérification |
|----|---------|--------------|
| INT02-AC1 | Page créée automatiquement | Vérifier Notion |
| INT02-AC2 | Status synchronisé | Changement phase |
| INT02-AC3 | Métriques poussées | Dashboard Notion |
| INT02-AC4 | Contenu synchronisé | Feature Doc dans page |
| INT02-AC5 | Mode dégradé | Test sans Notion |

### 17.7 Effort Estimé

| Tâche | Effort |
|-------|--------|
| Features database | 8h |
| Status sync | 4h |
| Content sync | 6h |
| Metrics dashboard | 6h |
| Commande /epci-notion | 4h |
| Tests | 2h |
| **Total** | **30h (4j)** |

---

## 18. Architecture Globale

### 18.1 Structure des Fichiers v4.0

```
.claude/
├── commands/                       # 8 commandes (+3)
│   ├── epci.md
│   ├── epci-brief.md
│   ├── epci-quick.md
│   ├── epci-spike.md
│   ├── create.md
│   ├── epci-memory.md             # NOUVEAU (F04)
│   ├── epci-github.md             # NOUVEAU (INT-01)
│   └── epci-notion.md             # NOUVEAU (INT-02)
│
├── agents/                         # 6 subagents (+1)
│   ├── plan-validator.md
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   ├── doc-generator.md
│   └── performance-auditor.md     # NOUVEAU
│
├── skills/
│   ├── core/                      # 5 skills existants
│   ├── stack/
│   │   └── java-springboot/
│   │       └── references/        # NOUVEAU (F01)
│   ├── factory/                   # 4 skills existants
│   ├── personas/                  # NOUVEAU (F09)
│   │   ├── PERSONAS.md
│   │   ├── architect.md
│   │   ├── frontend.md
│   │   ├── backend.md
│   │   ├── security.md
│   │   ├── qa.md
│   │   └── doc.md
│   └── mcp/                       # NOUVEAU (F12)
│       ├── MCP.md
│       ├── context7.md
│       ├── sequential.md
│       ├── magic.md
│       └── playwright.md
│
├── settings/                       # NOUVEAU
│   └── flags.md                   # (F10)
│
├── hooks/                          # ENRICHI (F02)
│   ├── README.md
│   ├── runner.py
│   ├── examples/
│   └── active/
│
├── project-memory/                 # NOUVEAU (F04)
│   ├── context.json
│   ├── conventions.json
│   ├── settings.json
│   ├── history/
│   ├── patterns/
│   ├── metrics/
│   └── learning/
│
└── scripts/                        # Existant
    ├── validate_skill.py
    ├── validate_command.py
    ├── validate_subagent.py
    └── validate_all.py
```

### 18.2 Diagramme Composants

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EPCI v4.0                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  COMMANDS (8)           AGENTS (6)            SKILLS               │
│  ├── epci               ├── plan-validator    ├── core/ (5)        │
│  ├── epci-brief         ├── code-reviewer     ├── stack/ (4)       │
│  ├── epci-quick         ├── security-auditor  ├── factory/ (4)     │
│  ├── epci-spike         ├── qa-reviewer       ├── personas/ (6)    │
│  ├── create             ├── doc-generator     └── mcp/ (4)         │
│  ├── epci-memory        └── perf-auditor                           │
│  ├── epci-github                                                    │
│  └── epci-notion        FLAGS         HOOKS        MCP             │
│                         ├── --think*   ├── pre-*    ├── context7   │
│                         ├── --uc       ├── post-*   ├── sequential │
│                         ├── --wave*    └── on-*     ├── magic      │
│                         └── --safe                  └── playwright │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PROJECT MEMORY                            │   │
│  │  context │ history │ patterns │ metrics │ learning           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    INTEGRATIONS                              │   │
│  │  GitHub (branch, commit, PR) │ Notion (features, metrics)    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 19. Dépendances Inter-Fonctionnalités

### 19.1 Matrice de Dépendances

```
        F01 F02 F03 F04 F05 F06 F07 F08 F09 F10 F11 F12 I01 I02
F01      -   -   -   -   -   -   -   -   -   -   -   -   -   -
F02      -   -   -   -   -   -   ◐   -   -   -   -   -   -   -
F03      -   ◐   -   ●   -   ●   ●   -   ◐   ◐   -   -   -   -
F04      -   -   -   -   ●   ●   -   ●   -   -   -   -   ◐   ●
F05      -   -   -   ●   -   -   -   ◐   ●   -   -   ◐   -   -
F06      -   -   -   ●   -   -   -   ●   -   -   -   -   -   -
F07      -   ●   ●   -   -   -   -   -   ◐   ●   ●   ◐   -   -
F08      -   -   -   ●   ◐   ●   -   -   ●   -   -   -   -   -
F09      -   -   -   -   -   -   -   -   -   ◐   -   ●   -   -
F10      -   -   -   -   -   -   -   -   -   -   ●   -   -   -
F11      -   -   -   -   -   -   ●   -   -   ●   -   -   -   -
F12      -   -   -   -   -   -   -   -   ●   -   -   -   -   -
I01      -   -   -   ●   -   -   -   -   -   -   -   -   -   -
I02      -   -   -   ●   -   -   -   -   -   -   -   -   -   -

●  Dépendance forte (requise)
◐  Dépendance faible (enrichit)
-  Pas de dépendance
```

### 19.2 Ordre d'Implémentation

```
PHASE 1 (v3.1) — Fondations
├── F01: Java Spring Boot References (indépendant)
├── F02: Système de Hooks (indépendant)
├── F03: Breakpoints Enrichis (dépend F04 pour métriques)
└── F10: Flags Universels (fondation pour F11) ★ NEW

PHASE 2 (v3.5) — Intelligence
├── F04: Project Memory (fondation critique)
├── F05: Clarification Intelligente (dépend F04)
├── F06: Suggestions Proactives (dépend F04)
└── F09: Système de Personas (dépend F12 pour MCP) ★ NEW

PHASE 3 (v4.0) — Orchestration & Learning
├── F07: Orchestration Multi-Agents (dépend F02, F10)
├── F08: Apprentissage Continu (dépend F04, F09)
├── F11: Wave Orchestration (dépend F07, F10) ★ NEW
└── F12: MCP Integration (dépend F09) ★ NEW

PHASE 4 (v4.1) — Intégrations
├── INT-01: GitHub Integration (dépend F04)
└── INT-02: Notion Integration (dépend F04)
```

---

## 20. Plan de Tests

### 20.1 Stratégie de Test

| Niveau | Couverture | Outils |
|--------|------------|--------|
| Unitaire | 80% | pytest |
| Intégration | 60% | pytest-integration |
| E2E | Scénarios critiques | Manual + scripts |

### 20.2 Scénario E2E Principal

```gherkin
Feature: Complete EPCI Workflow v4.0

  Scenario: Standard feature with all systems active
    Given a project initialized with EPCI v4.0
    And project memory contains 5 previous features
    And GitHub and Notion integrations are configured
    
    When I run "/epci-brief Add user preferences API"
    Then persona --persona-backend should auto-activate
    And clarification should ask context-aware questions
    And scoring should calculate complexity 0.58 (STANDARD)
    
    When I complete clarification
    Then @plan-validator should run via orchestrator
    And breakpoint Phase 1 should show enriched format
    And GitHub branch should be created
    
    When I say "continue"
    Then Phase 2 should execute with --think flag
    And hooks pre-phase-2 should run
    And @code-reviewer should validate
    And breakpoint Phase 2 should show results
    
    When I say "continue"  
    Then Phase 3 should finalize
    And GitHub commit should be created
    And GitHub PR should be opened
    And Notion page should be updated
    And Feature Document should be complete
    
    Then learning models should update
    And feature history should be saved
    And metrics should be pushed to Notion
```

### 20.3 Tests Spécifiques Nouvelles Fonctionnalités

| Fonctionnalité | Test | Critère |
|----------------|------|---------|
| F09 Personas | Auto-activation | Score > 0.6 → activation |
| F10 Flags | Précédence | --safe > --fast |
| F11 Wave | Découpage | 4 vagues pour LARGE |
| F12 MCP | Mode dégradé | Continue si MCP down |

### 20.4 Tests de Performance

| Test | Cible |
|------|-------|
| Orchestrator parallel (3 agents) | < 1.2x temps single |
| Memory load (100 features) | < 2s |
| Learning update | < 500ms |
| Suggestion generation | < 1s |
| Persona scoring | < 100ms |
| Flag parsing | < 50ms |

---

## 21. Planning et Jalons

### 21.1 Timeline

```
Janvier (Semaines 3-4)
├── F01: Java Spring Boot References ████████████ (2.5j)
├── F02: Système de Hooks ████████████████ (2.5j)
└── F10: Flags Universels ████████████ (3j) ★ NEW

Février (Semaines 5-6)
├── F03: Breakpoints Enrichis ████████████ (2j)
└── F04: Project Memory █████████████████████████ (4.5j)

Février-Mars (Semaines 7-8)
├── F05: Clarification Intelligente ████████████████ (3j)
├── F06: Suggestions Proactives ████████████████ (3j)
└── F09: Système de Personas ████████████████████ (4j) ★ NEW

Mars (Semaines 9-11)
├── F07: Orchestration Multi-Agents █████████████████████████ (4.5j)
├── F08: Apprentissage Continu █████████████████████████ (4.5j)
├── F11: Wave Orchestration ████████████████████ (4j) ★ NEW
└── F12: MCP Integration ██████████████████ (3.5j) ★ NEW

Mars (Semaine 12)
└── Tests E2E & Stabilisation v4.0 ████████████████████ (5j)

Avril-Mai (Semaines 15-19)
├── INT-01: GitHub Integration ████████████████████████ (3j)
├── INT-02: Notion Integration ██████████████████████████████ (4j)
└── Tests & Stabilisation v4.1 ████████████████ (2j)

Release v4.0 — Fin Mars 2025
Release v4.1 — Mi-Mai 2025
```

### 21.2 Jalons

| Jalon | Date | Livrables |
|-------|------|-----------|
| **v3.1-alpha** | Fin Janvier | F01, F02, F10 |
| **v3.1** | Mi-Février | F01, F02, F03, F10 |
| **v3.5-alpha** | Fin Février | F04 |
| **v3.5** | Mi-Mars | F04, F05, F06, F09 |
| **v4.0-beta** | Fin Mars | F07, F08, F11, F12 |
| **v4.0** | Début Avril | Toutes fonctionnalités core |
| **v4.1-beta** | Fin Avril | INT-01, INT-02 |
| **v4.1** | Mi-Mai | Intégrations complètes |

### 21.3 Effort Total

| Fonctionnalité | Effort | Source |
|----------------|--------|--------|
| F01: Java Spring Boot | 20h | CDC Original |
| F02: Hooks | 18h | CDC Original |
| F03: Breakpoints | 14h | CDC Original |
| F04: Project Memory | 34h | CDC Original |
| F05: Clarification | 25h | CDC Original |
| F06: Suggestions | 24h | CDC Original |
| F07: Orchestration | 34h | CDC Original |
| F08: Apprentissage | 35h | CDC Original |
| F09: Personas | 32h | **NEW** |
| F10: Flags | 24h | **NEW** |
| F11: Wave | 32h | **NEW** |
| F12: MCP | 28h | **NEW** |
| INT-01: GitHub | 24h | CDC Intégrations |
| INT-02: Notion | 30h | CDC Intégrations |
| Tests & Intégration | 50h | — |
| Documentation | 20h | — |
| **TOTAL** | **444h (≈56 jours ouvrés)** | — |

### 21.4 Répartition par Source

| Source | Fonctionnalités | Effort |
|--------|-----------------|--------|
| CDC Original | F01-F08 | 204h |
| CDC Intégrations | INT-01, INT-02 | 54h |
| Analyse WD (NEW) | F09-F12 | 116h |
| Transverse | Tests, docs | 70h |
| **Total** | 14 fonctionnalités | **444h** |

---

## 22. Annexes

### 22.1 Glossaire Complet

| Terme | Définition |
|-------|------------|
| Agent/Subagent | Composant spécialisé effectuant validation/génération |
| Breakpoint | Point de pause nécessitant confirmation utilisateur |
| Context7 | MCP server pour documentation librairies externes |
| DAG | Directed Acyclic Graph — graphe d'exécution agents |
| Feature Document | Document structuré §1-§4 décrivant une feature |
| Flag | Option modifiant le comportement (--think, --wave) |
| Hook | Script exécuté automatiquement à un point workflow |
| Learning Loop | Boucle d'apprentissage continu |
| Magic | MCP server pour génération UI moderne |
| MCP | Model Context Protocol — enrichissement contextuel |
| Orchestrator | Composant coordonnant exécution multi-agents |
| Persona | Mode de pensée influençant tout le comportement |
| Playwright | MCP server pour tests E2E et browser |
| Project Memory | Système persistance contexte projet |
| Sequential | MCP server pour analyse multi-étapes |
| Skill | Module de connaissances domaine spécifique |
| Stack | Ensemble technologique (php-symfony, etc.) |
| Wave | Vague d'exécution dans orchestration multi-étapes |

### 22.2 Références

| Document | Description |
|----------|-------------|
| EPCI v3.0 Plugin | Baseline actuelle |
| WD Framework v2.0 | Source d'inspiration analyse |
| Brainstorm Report | Session EPCI × WD |
| Claude MCP Docs | Documentation Anthropic |
| Conventional Commits | Standard de commits |
| GitHub REST API | docs.github.com/rest |
| Notion API | developers.notion.com |
| MCP Specification | modelcontextprotocol.io |

### 22.3 Changelog du CDC

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0.0 | 2025-12-15 | Version unifiée initiale |
| — | — | Fusion CDC Original + Intégrations + WD Analysis |
| — | — | Ajout F09 Personas, F10 Flags, F11 Wave, F12 MCP |

---

*Fin du Cahier des Charges Unifié*

**Document généré par**: Claude (Assistant IA)  
**Pour**: Édouard — Développeur FullStack  
**Projet**: EPCI Plugin v4.0 → v4.1  
**Méthode**: Brainstormer Skill v1.1
