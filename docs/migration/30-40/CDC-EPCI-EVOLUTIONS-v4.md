# Cahier des Charges — EPCI Plugin Évolutions v3.x → v4.0

> **Document**: CDC-EPCI-EVOL-001  
> **Version**: 1.0.0  
> **Date**: 2025-12-11  
> **Statut**: Draft pour validation  
> **Auteur**: Claude (Assistant IA)  
> **Commanditaire**: Édouard (Développeur FullStack)

---

## Table des Matières

1. [Introduction](#1-introduction)
2. [Périmètre et Objectifs](#2-périmètre-et-objectifs)
3. [F01 — Java Spring Boot References](#3-f01--java-spring-boot-references)
4. [F02 — Système de Hooks](#4-f02--système-de-hooks)
5. [F03 — Breakpoints Enrichis](#5-f03--breakpoints-enrichis)
6. [F04 — Project Memory](#6-f04--project-memory)
7. [F05 — Clarification Intelligente](#7-f05--clarification-intelligente)
8. [F06 — Suggestions Proactives](#8-f06--suggestions-proactives)
9. [F07 — Orchestration Multi-Agents](#9-f07--orchestration-multi-agents)
10. [F08 — Apprentissage Continu](#10-f08--apprentissage-continu)
11. [Architecture Globale](#11-architecture-globale)
12. [Dépendances Inter-Fonctionnalités](#12-dépendances-inter-fonctionnalités)
13. [Plan de Tests](#13-plan-de-tests)
14. [Planning et Jalons](#14-planning-et-jalons)
15. [Annexes](#15-annexes)

---

## 1. Introduction

### 1.1 Contexte

Le plugin EPCI v3.0.0 est opérationnel avec 23 composants validés. Ce CDC détaille 8 évolutions majeures pour transformer EPCI d'un framework de workflow vers une plateforme de développement assisté intelligente.

### 1.2 Documents de Référence

| Document | Version | Description |
|----------|---------|-------------|
| EPCI Plugin v3.0 | 3.0.0 | Baseline actuelle |
| Audit Report | 2025-12-11 | Analyse conformité |
| Evolution Roadmap | 2025-12-11 | Vision stratégique |

### 1.3 Glossaire

| Terme | Définition |
|-------|------------|
| **Hook** | Script exécuté automatiquement à un point précis du workflow |
| **Project Memory** | Système de persistance du contexte projet inter-sessions |
| **Breakpoint** | Point de pause dans le workflow nécessitant confirmation utilisateur |
| **Orchestrator** | Agent coordinateur d'exécution multi-agents |
| **Learning Loop** | Boucle d'apprentissage continu basée sur le feedback |

### 1.4 Conventions du Document

```
[MUST]    — Exigence obligatoire
[SHOULD]  — Exigence recommandée
[MAY]     — Exigence optionnelle
[REF:XX]  — Référence à une autre section
```

---

## 2. Périmètre et Objectifs

### 2.1 Fonctionnalités Incluses

| ID | Fonctionnalité | Version Cible | Priorité |
|----|----------------|---------------|----------|
| F01 | Java Spring Boot References | v3.1 | P1 |
| F02 | Système de Hooks | v3.1 | P1 |
| F03 | Breakpoints Enrichis | v3.1 | P2 |
| F04 | Project Memory | v3.5 | P1 |
| F05 | Clarification Intelligente | v3.5 | P1 |
| F06 | Suggestions Proactives | v3.5 | P2 |
| F07 | Orchestration Multi-Agents | v4.0 | P1 |
| F08 | Apprentissage Continu | v4.0 | P1 |

### 2.2 Objectifs Mesurables

| Objectif | Métrique | Cible |
|----------|----------|-------|
| Réduire temps onboarding | Temps premier workflow réussi | < 30 min |
| Améliorer pertinence suggestions | Taux acceptation suggestions | > 70% |
| Accélérer cycles développement | Temps moyen feature STANDARD | -25% |
| Réduire erreurs récurrentes | Issues répétées même cause | -50% |
| Améliorer expérience utilisateur | Score satisfaction (1-5) | > 4.2 |

### 2.3 Hors Périmètre

- Intégrations externes (GitHub, Notion, Slack) — CDC séparé
- Marketplace de plugins — CDC séparé
- Mode équipe complet — CDC séparé
- Nouveaux stack skills (Go, .NET, etc.) — CDC séparé


---

## 3. F01 — Java Spring Boot References

### 3.1 Contexte et Justification

#### 3.1.1 Situation Actuelle

Le skill `java-springboot` est le seul stack skill sans dossier `references/`. Cette inconsistance :
- Rompt le pattern Progressive Disclosure appliqué aux autres stacks
- Limite la profondeur d'information disponible
- Crée une expérience utilisateur inégale

#### 3.1.2 Objectif

Aligner `java-springboot` sur les autres stack skills (`php-symfony`, `python-django`, `javascript-react`) en ajoutant des fichiers de référence détaillés.

### 3.2 Spécifications Fonctionnelles

#### 3.2.1 Structure Cible

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

#### 3.2.2 Exigences par Fichier

##### architecture.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Structure projet | Arborescence Maven/Gradle standard | P1 |
| [MUST] Couches architecture | Controller → Service → Repository | P1 |
| [MUST] Clean Architecture | Ports & Adapters avec Spring | P1 |
| [MUST] Hexagonal | Implémentation avec annotations Spring | P1 |
| [SHOULD] CQRS | Command/Query separation avec Spring | P2 |
| [SHOULD] Modular monolith | Multi-module Maven/Gradle | P2 |
| [MAY] DDD tactical | Aggregate, ValueObject, DomainEvent | P3 |

##### jpa-hibernate.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Entity patterns | Annotations JPA, Lombok, equals/hashCode | P1 |
| [MUST] Repository | JpaRepository, custom queries, Specifications | P1 |
| [MUST] Relations | OneToMany, ManyToOne, fetch strategies | P1 |
| [MUST] N+1 prevention | EntityGraph, JOIN FETCH, batch size | P1 |
| [SHOULD] Auditing | @CreatedDate, @LastModifiedDate, Envers | P2 |
| [SHOULD] Migrations | Flyway/Liquibase patterns | P2 |
| [MAY] Multi-tenancy | Discriminator, schema-based | P3 |

##### security.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] SecurityFilterChain | Configuration Spring Security 6 lambda DSL | P1 |
| [MUST] Authentication | JWT, OAuth2, Basic Auth | P1 |
| [MUST] Authorization | @PreAuthorize, Method security | P1 |
| [MUST] CSRF/CORS | Configuration REST API | P1 |
| [SHOULD] Password encoding | BCrypt, Argon2 | P2 |
| [SHOULD] Rate limiting | Bucket4j, Resilience4j | P2 |
| [MAY] Audit logging | Spring Security events | P3 |

##### testing.md

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] JUnit 5 | @Test, @Nested, @ParameterizedTest | P1 |
| [MUST] Mockito | @Mock, @InjectMocks, verify | P1 |
| [MUST] Spring Boot Test | @SpringBootTest, @WebMvcTest, @DataJpaTest | P1 |
| [MUST] MockMvc | API testing patterns | P1 |
| [SHOULD] TestContainers | PostgreSQL, Redis, Kafka | P2 |
| [SHOULD] ArchUnit | Architecture tests | P2 |
| [MAY] Contract testing | Spring Cloud Contract | P3 |

### 3.3 Contraintes Techniques

| Contrainte | Valeur | Justification |
|------------|--------|---------------|
| Taille max par fichier | 400 lignes | Chargement rapide |
| Tokens max par fichier | 3000 tokens | Context window |
| Version Java minimum | Java 17 | LTS actuel |
| Version Spring Boot | 3.2+ | Dernière stable |
| Exemples de code | Complets et exécutables | Copier-coller ready |

### 3.4 Critères d'Acceptation

| ID | Critère | Méthode de Vérification |
|----|---------|-------------------------|
| F01-AC1 | 5 fichiers references créés | `ls skills/stack/java-springboot/references/` |
| F01-AC2 | Chaque fichier < 400 lignes | `wc -l` sur chaque fichier |
| F01-AC3 | SKILL.md met à jour avec liens | Grep `@references/` dans SKILL.md |
| F01-AC4 | Validation script passe | `python scripts/validate_skill.py` |
| F01-AC5 | Exemples de code compilables | Revue manuelle |

### 3.5 Effort Estimé

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

## 4. F02 — Système de Hooks

### 4.1 Contexte et Justification

#### 4.1.1 Situation Actuelle

Le dossier `hooks/` existe mais est vide. Les utilisateurs n'ont aucun moyen d'exécuter des actions automatiques à des points précis du workflow EPCI.

#### 4.1.2 Objectif

Permettre l'exécution de scripts personnalisés à des points clés du workflow pour :
- Exécuter des linters/formatters avant le code
- Notifier des systèmes externes (Slack, email)
- Déclencher des pipelines CI/CD
- Collecter des métriques personnalisées

### 4.2 Types de Hooks

| Hook | Déclencheur | Cas d'usage |
|------|-------------|-------------|
| `pre-phase-1` | Avant Phase 1 (Planning) | Vérifier prérequis, charger contexte |
| `post-phase-1` | Après Phase 1 | Notifier équipe, créer ticket |
| `pre-phase-2` | Avant Phase 2 (Code) | Setup environnement, linters |
| `post-phase-2` | Après Phase 2 | Run tests supplémentaires, coverage |
| `pre-phase-3` | Avant Phase 3 (Finalize) | Vérifier tous tests passent |
| `post-phase-3` | Après Phase 3 (Completion) | Notifier Slack, créer PR, deploy |
| `on-breakpoint` | À chaque breakpoint | Log, métriques |
| `on-error` | En cas d'erreur workflow | Alerting, rollback |

### 4.3 Structure des Hooks

```
hooks/
├── README.md                    # Documentation
├── runner.py                    # Moteur d'exécution
├── pre-phase-1.sh              # Optionnel
├── post-phase-1.sh             # Optionnel
├── pre-phase-2.sh              # Optionnel
├── post-phase-2.sh             # Optionnel
├── pre-phase-3.sh              # Optionnel
├── post-phase-3.sh             # Optionnel
├── on-breakpoint.sh            # Optionnel
├── on-error.sh                 # Optionnel
└── examples/                   # Exemples réutilisables
    ├── slack-notification.sh
    ├── run-linters.sh
    ├── create-github-pr.sh
    └── collect-metrics.sh
```

### 4.4 Variables d'Environnement

Chaque hook reçoit des variables d'environnement contextuelles :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `EPCI_PHASE` | Phase actuelle | `1`, `2`, `3` |
| `EPCI_WORKFLOW` | Type de workflow | `standard`, `large`, `quick` |
| `EPCI_FEATURE_SLUG` | Slug de la feature | `user-email-validation` |
| `EPCI_FEATURE_DOC` | Chemin Feature Document | `docs/features/user-email-validation.md` |
| `EPCI_PROJECT_ROOT` | Racine du projet | `/home/user/myproject` |
| `EPCI_HOOK_TYPE` | Type de hook | `pre-phase-2` |
| `EPCI_TIMESTAMP` | Timestamp ISO | `2025-01-15T14:30:00Z` |
| `EPCI_VALIDATION_STATUS` | Statut dernière validation | `APPROVED`, `NEEDS_REVISION` |
| `EPCI_AGENT_RESULTS` | JSON résultats agents | `{"plan-validator": "APPROVED"}` |

### 4.5 Comportement

- **Exit code 0**: Succès, workflow continue
- **Exit code != 0**: Échec, workflow pause avec message d'erreur
- **Timeout**: 5 minutes par défaut
- **Absence de hook**: Silencieusement ignoré

### 4.6 Exemple: pre-phase-2.sh (Linters)

```bash
#!/bin/bash
# Hook: pre-phase-2.sh
# Purpose: Run linters and formatters before coding phase

set -e
echo "=== EPCI Pre-Phase 2 Hook ==="
echo "Feature: $EPCI_FEATURE_SLUG"

if [ -f "composer.json" ]; then
    echo "PHP project - Running PHP CS Fixer..."
    vendor/bin/php-cs-fixer fix --dry-run --diff || exit 1
fi

if [ -f "package.json" ]; then
    echo "Node.js project - Running ESLint..."
    npm run lint || exit 1
fi

echo "✅ All linters passed"
exit 0
```

### 4.7 Exemple: post-phase-3.sh (Slack Notification)

```bash
#!/bin/bash
# Hook: post-phase-3.sh
# Purpose: Send completion notification to Slack

if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo "SLACK_WEBHOOK_URL not set, skipping"
    exit 0
fi

curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\": \"✅ EPCI Feature Complete: ${EPCI_FEATURE_SLUG}\"}" \
    "$SLACK_WEBHOOK_URL"

echo "✅ Slack notification sent"
```

### 4.8 Critères d'Acceptation

| ID | Critère | Méthode de Vérification |
|----|---------|-------------------------|
| F02-AC1 | 8 types de hooks supportés | Test runner avec tous les types |
| F02-AC2 | Variables d'environnement passées | Script de test affichant les vars |
| F02-AC3 | Timeout après 5 minutes | Test avec `sleep 600` |
| F02-AC4 | Exit code non-0 stoppe workflow | Test avec `exit 1` |
| F02-AC5 | Hook absent = silencieux | Workflow sans hooks fonctionne |
| F02-AC6 | README documenté | Revue manuelle |
| F02-AC7 | 4 exemples fournis | `ls hooks/examples/` |

### 4.9 Effort Estimé: **18h (2.5j)**


---

## 5. F03 — Breakpoints Enrichis

### 5.1 Contexte et Justification

Les breakpoints actuels sont minimalistes. L'objectif est d'enrichir les breakpoints pour fournir :
- Un résumé visuel complet de la phase
- Les métriques clés (temps, estimations, risques)
- L'état de tous les agents (passés et à venir)
- Les actions possibles clairement listées

### 5.2 Format du Breakpoint Enrichi

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️ BREAKPOINT PHASE [N] — [Phase Name]                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─ Summary ───────────────────────────────────────────────────────┐ │
│ │ Tasks planned:     7 tasks                                      │ │
│ │ Files impacted:    4 to create, 2 to modify                     │ │
│ │ Estimated effort:  45 min (±15 min)                             │ │
│ │ Risk level:        Medium (API changes detected)                │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Validations ───────────────────────────────────────────────────┐ │
│ │ ✅ @plan-validator     APPROVED                                 │ │
│ │ ⏳ @code-reviewer       Pending (Phase 2)                       │ │
│ │ ⏳ @security-auditor    Will trigger (API scope detected)       │ │
│ │ ⏳ @qa-reviewer         Will trigger (8 tests planned)          │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Actions ───────────────────────────────────────────────────────┐ │
│ │  "continue"  →  Proceed to Phase [N+1]                          │ │
│ │  "revise"    →  Modify current phase output                     │ │
│ │  "details"   →  Show detailed validation report                 │ │
│ │  "abort"     →  Cancel workflow                                 │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ 📄 Feature Document: docs/features/[slug].md                        │
│ ⏱️  Elapsed: [Xh Xmin] | Estimated remaining: [Xh Xmin]             │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.3 Breakpoint avec NEEDS_REVISION

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️ BREAKPOINT PHASE 2 — Review Issues Detected                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─ Validations ───────────────────────────────────────────────────┐ │
│ │ ❌ @code-reviewer      NEEDS_REVISION                           │ │
│ │    Issues to fix:                                               │ │
│ │    ├─ 🔴 CRITICAL: SQL injection in UserRepository line 45     │ │
│ │    ├─ 🟠 IMPORTANT: Missing null check in UserService line 78  │ │
│ │    └─ 🟡 MINOR: Magic number in validation (line 92)           │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Actions ───────────────────────────────────────────────────────┐ │
│ │  "fix"       →  Apply fixes and re-run validations              │ │
│ │  "details"   →  Show full review reports                        │ │
│ │  "override"  →  Continue anyway (NOT RECOMMENDED)               │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.4 Completion Message

```
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ EPCI WORKFLOW COMPLETE                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Feature:           user-preferences                                 │
│ Total duration:    1h 07min                                         │
│                                                                     │
│ ┌─ Deliverables ──────────────────────────────────────────────────┐ │
│ │ 📄 Feature Document:  docs/features/user-preferences.md         │ │
│ │ 📝 Commit:            feat(user): add preferences management    │ │
│ │ 🌿 Branch:            feature/user-preferences                  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Validation Summary ────────────────────────────────────────────┐ │
│ │ ✅ @plan-validator     ✅ @code-reviewer                        │ │
│ │ ✅ @security-auditor   ✅ @qa-reviewer                          │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Statistics ────────────────────────────────────────────────────┐ │
│ │ Files changed: 6 | Lines: +287/-12 | Coverage: 87%              │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.5 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F03-AC1 | Breakpoint Phase 1 affiche résumé complet |
| F03-AC2 | Breakpoint Phase 2 affiche métriques code |
| F03-AC3 | Tous les agents listés avec statut |
| F03-AC4 | Issues CRITICAL clairement visibles |
| F03-AC5 | Actions listées et fonctionnelles |
| F03-AC6 | Temps écoulé/estimé affichés |
| F03-AC7 | Message completion complet |

### 5.6 Effort Estimé: **14h (2j)**


---

## 6. F04 — Project Memory

### 6.1 Contexte et Justification

Chaque session Claude est indépendante. Le contexte projet est perdu entre les sessions. L'objectif est de créer un système de persistance permettant à EPCI de :
- Retenir le contexte projet entre sessions
- Capitaliser sur l'historique des features
- Apprendre les conventions implicites
- Améliorer les estimations basées sur l'historique

### 6.2 Données Persistées

| Catégorie | Données | Usage |
|-----------|---------|-------|
| **Project Info** | Nom, stack, détection date | Identification projet |
| **Conventions** | Naming, testing, architecture | Application automatique |
| **Team** | Membres, rôles, préférences | Assignation, communication |
| **History** | Features complétées, métriques | Estimation, trends |
| **Patterns** | Code patterns récurrents | Suggestions |
| **Issues** | Problèmes récurrents | Prévention |

### 6.3 Structure des Fichiers

```
.claude/
├── project-memory/
│   ├── context.json           # Contexte projet principal
│   ├── conventions.json       # Conventions détectées/configurées
│   ├── history/               # Historique par feature
│   │   ├── user-auth.json
│   │   ├── payment-api.json
│   │   └── ...
│   ├── patterns/              # Patterns de code détectés
│   │   ├── services.json
│   │   ├── controllers.json
│   │   └── tests.json
│   ├── metrics/               # Métriques agrégées
│   │   └── summary.json
│   └── learning/              # Modèles d'apprentissage
│       ├── estimation.json
│       └── issues.json
```

### 6.4 Schéma context.json

```json
{
  "$schema": "epci-project-context-v1",
  "project": {
    "name": "my-awesome-project",
    "description": "E-commerce platform",
    "repository": "https://github.com/company/my-project",
    "stack": {
      "primary": "php-symfony",
      "secondary": ["javascript-react"],
      "detected_at": "2025-01-10T10:00:00Z"
    },
    "architecture": {
      "type": "hexagonal",
      "layers": ["domain", "application", "infrastructure"]
    }
  },
  "team": {
    "members": [
      {"name": "Alice", "role": "lead", "expertise": ["backend"]},
      {"name": "Bob", "role": "developer", "expertise": ["frontend"]}
    ]
  },
  "preferences": {
    "language": "fr",
    "breakpoint_verbosity": "detailed",
    "auto_commit": false
  }
}
```

### 6.5 Schéma conventions.json

```json
{
  "$schema": "epci-conventions-v1",
  "naming": {
    "classes": {
      "controllers": "{Name}Controller",
      "services": "{Name}Service",
      "repositories": "{Name}Repository"
    },
    "database": {
      "tables": "snake_case_plural",
      "columns": "snake_case"
    }
  },
  "testing": {
    "framework": "phpunit",
    "coverage_target": 80,
    "naming_pattern": "should{Action}When{Condition}"
  },
  "git": {
    "branch_pattern": "{type}/{ticket}-{short-description}",
    "commit_style": "conventional"
  },
  "custom_rules": [
    {
      "id": "no-entity-setters",
      "description": "Entities should not have public setters",
      "auto_detected": true
    }
  ]
}
```

### 6.6 Schéma Feature History

```json
{
  "feature": {
    "slug": "user-auth",
    "title": "User Authentication with OAuth2",
    "complexity": "STANDARD"
  },
  "timeline": {
    "started_at": "2025-01-12T09:00:00Z",
    "completed_at": "2025-01-12T11:45:00Z",
    "total_duration_minutes": 165
  },
  "plan": {
    "tasks_planned": 8,
    "estimated_minutes": 90,
    "actual_minutes": 140,
    "accuracy_percent": 64
  },
  "implementation": {
    "files_created": 6,
    "files_modified": 3,
    "lines_added": 412,
    "tests_added": 12,
    "coverage_after": 82
  },
  "validations": {
    "plan_validator": {"attempts": 1, "final_status": "APPROVED"},
    "code_reviewer": {"attempts": 2, "final_status": "APPROVED"},
    "security_auditor": {"attempts": 1, "final_status": "APPROVED"}
  },
  "learnings": [
    {
      "type": "estimation",
      "observation": "OAuth integration took 50% longer than estimated",
      "recommendation": "Add buffer for third-party integrations"
    }
  ]
}
```

### 6.7 Commande /epci-init

Initialise EPCI pour un nouveau projet :
1. Détection automatique du stack
2. Suggestion de conventions
3. Création de la structure `.claude/project-memory/`
4. Configuration initiale

### 6.8 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F04-AC1 | Structure créée par /epci-init |
| F04-AC2 | Context persisté entre sessions |
| F04-AC3 | History sauvée après feature |
| F04-AC4 | Metrics mis à jour automatiquement |
| F04-AC5 | Conventions appliquées au code |

### 6.9 Effort Estimé: **34h (4.5j)**


---

## 7. F05 — Clarification Intelligente

### 7.1 Contexte et Justification

La clarification actuelle dans `/epci-brief` est générique avec des questions fixes. L'objectif est de créer un système de clarification adaptatif qui :
- Pose des questions pertinentes au contexte projet
- Apprend des features passées pour mieux qualifier
- Réduit le nombre de questions pour les cas simples
- Augmente la précision pour les cas complexes

### 7.2 Types de Questions

| Catégorie | Questions Exemples | Quand Poser |
|-----------|-------------------|-------------|
| **Scope** | "Cette feature modifie-t-elle l'API publique?" | Toujours |
| **Data** | "Y a-t-il des changements de schéma DB?" | Si entité mentionnée |
| **Security** | "Cette feature gère-t-elle des données sensibles?" | Si auth/user/payment |
| **Integration** | "Y a-t-il des dépendances externes à intégrer?" | Si API/service mentionné |
| **UX** | "Y a-t-il des maquettes ou specs UI?" | Si frontend détecté |
| **Performance** | "Y a-t-il des contraintes de performance?" | Si batch/report/export |

### 7.3 Algorithme de Sélection

```
1. ANALYZE brief_text
   - Extract entities, actions, technical markers
   
2. LOAD project_context
   - Get stack, conventions, recent features
   
3. MATCH patterns
   - Check similar features in history
   - Get questions useful for those features
   
4. SELECT questions
   Priority:
   1. High historical value for similar features
   2. Triggered by detected patterns
   3. Triggered by project conventions
   
5. LIMIT questions
   - Confidence > 80%: max 2 questions
   - Confidence 50-80%: max 4 questions
   - Confidence < 50%: max 6 questions
```

### 7.4 Exemples de Clarification Adaptative

#### API Simple (Confidence Haute)

**Brief**: "Ajouter un endpoint GET /users/{id}/preferences"

**Questions** (2 seulement):
```
Projet détecté: Symfony 7 + API Platform

1. Le endpoint doit-il être authentifié? [Oui/Non]
   → Les 3 derniers endpoints user étaient protégés par JWT

2. Format de réponse souhaité? [Standard/Custom]
```

#### Feature Complexe (Confidence Basse)

**Brief**: "Intégrer le paiement Stripe pour les abonnements"

**Questions** (6):
```
Cette feature implique une intégration de paiement - domaine sensible.

1. Stripe est-il déjà configuré? [Oui/Non/Partiel]
2. Quels types d'abonnements? [Mensuel/Annuel/Les deux/Custom]
3. Gestion des webhooks Stripe nécessaire? [Oui/Non]
4. Interface d'administration requise? [Oui/Non]
5. Environnement de test Stripe disponible? [Oui/Non]
6. Utilisez-vous Stripe Elements ou Checkout? [Elements/Checkout/À définir]
```

#### Feature Récurrente (Pattern Connu)

**Brief**: "Ajouter CRUD pour les catégories de produits"

**Questions** (1 seulement):
```
Pattern CRUD détecté - structure similaire à Product, Order, Customer.

1. Particularités par rapport aux CRUDs existants? [Aucune/À préciser]
```

### 7.5 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F05-AC1 | Analyse de brief fonctionnelle |
| F05-AC2 | Questions adaptées au contexte |
| F05-AC3 | Max 2 questions si confidence > 80% |
| F05-AC4 | Max 6 questions si confidence < 50% |
| F05-AC5 | Historique influence les questions |
| F05-AC6 | Skip si user demande |

### 7.6 Effort Estimé: **25h (3j)**


---

## 8. F06 — Suggestions Proactives

### 8.1 Contexte et Justification

EPCI est actuellement réactif : il attend les commandes utilisateur. L'objectif est de permettre à EPCI de suggérer proactivement :
- Des patterns basés sur les conventions projet
- Des améliorations basées sur l'historique d'erreurs
- Des optimisations basées sur les métriques
- Des prochaines étapes logiques

### 8.2 Types de Suggestions

| Type | Déclencheur | Exemple |
|------|-------------|---------|
| **Pattern** | Code similaire existant | "Ce service ressemble à OrderService. Utiliser le même pattern?" |
| **Convention** | Déviation détectée | "Les services utilisent le suffixe 'Handler' plutôt que 'Service'" |
| **Quality** | Issue récurrente | "Les 3 dernières features ont eu des issues de validation null" |
| **Performance** | Pattern lent détecté | "Boucle N+1 potentielle. Utiliser batch fetch?" |
| **Security** | Pattern risqué | "SQL construit par concaténation. Utiliser paramètres?" |
| **Next Step** | Fin de phase | "Phase 1 terminée. Revoir tâches #3 et #5 avec dépendances" |

### 8.3 Moments de Suggestion

| Moment | Suggestions Possibles | Comportement |
|--------|----------------------|--------------|
| Début de session | Rappel feature en cours, métriques | Informatif |
| Pendant /epci-brief | Patterns similaires, conventions | Interactif |
| Pendant Phase 2 | Code patterns, quality checks | Inline dans output |
| À chaque breakpoint | Next steps, optimizations | Section dédiée |
| Après erreur | Correction suggérée | Interactif |

### 8.4 Format des Suggestions

#### Inline (Non-Bloquante)
```
💡 Suggestion: Les services utilisent @required pour l'injection.
   Appliquer ce pattern? [Oui/Non/Ignorer toujours]
```

#### Section Breakpoint
```
┌─ 💡 Suggestions ──────────────────────────────────────────────────┐
│                                                                    │
│ 1. Pattern détecté: Ce repository ressemble à ProductRepository   │
│    → Copier le pattern de pagination? [apply-pattern]             │
│                                                                    │
│ 2. Quality: La validation d'email manque dans UserDTO             │
│    → L'ajouter est recommandé (erreur récurrente) [add-validation]│
│                                                                    │
│ Appliquer toutes: [apply-all] | Ignorer: [skip]                   │
└────────────────────────────────────────────────────────────────────┘
```

#### Début de Session
```
╔════════════════════════════════════════════════════════════════════╗
║ 🌅 Bonjour! Voici le contexte de votre projet:                     ║
╠════════════════════════════════════════════════════════════════════╣
║ Projet: my-awesome-project (php-symfony)                           ║
║ Dernière activité: Hier, 17:45                                     ║
║                                                                    ║
║ 📋 Feature en cours:                                               ║
║    user-preferences (Phase 2 - 60% complété)                       ║
║    → Reprendre? [continue-feature]                                 ║
║                                                                    ║
║ 📊 Métriques (7 jours):                                            ║
║    First-pass rate: 75% (↓ 10% vs semaine précédente)              ║
║    Issue récurrente: Missing null validation (2 occurrences)       ║
║                                                                    ║
║ 💡 Ajouter une règle de validation null systématique?              ║
║    → [add-rule] [remind-later] [ignore]                            ║
╚════════════════════════════════════════════════════════════════════╝
```

### 8.5 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F06-AC1 | Suggestions session start |
| F06-AC2 | Suggestions au breakpoint |
| F06-AC3 | Suggestion pattern détectée |
| F06-AC4 | Suggestion après erreur |
| F06-AC5 | Dismiss fonctionne (cooldown) |
| F06-AC6 | Actions exécutables |

### 8.6 Effort Estimé: **24h (3j)**


---

## 9. F07 — Orchestration Multi-Agents

### 9.1 Contexte et Justification

Les agents sont actuellement invoqués séquentiellement avec une logique câblée. L'objectif est de créer un orchestrateur capable de :
- Gérer un DAG (Directed Acyclic Graph) d'agents
- Exécuter en parallèle quand les dépendances le permettent
- Gérer les erreurs et retries
- Permettre l'ajout dynamique d'agents

### 9.2 Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                                 │
├────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                                   │
│  │   PLANNER   │ → Analyse le contexte, détermine les agents      │
│  └──────┬──────┘                                                   │
│         ▼                                                          │
│  ┌─────────────┐                                                   │
│  │  DAG BUILDER│ → Construit le graphe d'exécution                │
│  └──────┬──────┘                                                   │
│         ▼                                                          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│  │  EXECUTOR   │ ──► │   MONITOR   │ ──► │  REPORTER   │          │
│  └─────────────┘     └─────────────┘     └─────────────┘          │
│         │                                                          │
│         ├──► Agent 1 (parallel) ──┐                               │
│         ├──► Agent 2 (parallel) ──┼──► Merge ──► Agent 4          │
│         └──► Agent 3 (parallel) ──┘                               │
└────────────────────────────────────────────────────────────────────┘
```

### 9.3 Agent Registry

| Agent | Phase | Conditions | Dépendances | Parallélisable |
|-------|-------|------------|-------------|----------------|
| plan-validator | 1 | Toujours | Aucune | Non |
| code-reviewer | 2 | Toujours | Aucune | Oui |
| security-auditor | 2 | Si API/Auth/Data | Aucune | Oui |
| qa-reviewer | 2 | Si Tests | Aucune | Oui |
| performance-auditor | 2 | Si DB/Query/Batch | code-reviewer | Non |
| doc-generator | 3 | Toujours | code-reviewer | Non |

### 9.4 DAG d'Exécution Type (Phase 2)

```
    ┌─────────────────┐
    │   code-reviewer │
    └────────┬────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│security│ │   qa   │ │ perf   │
│auditor │ │reviewer│ │auditor │
└────┬───┘ └────┬───┘ └────┬───┘
     │          │          │
     └──────────┼──────────┘
                │
                ▼
          [MERGE RESULTS]
```

### 9.5 Gestion des Erreurs

| Situation | Comportement | Action |
|-----------|--------------|--------|
| Agent timeout | Retry 2x avec backoff | Automatique |
| Agent failure | Marquer failed, continuer | Voir erreur, décider |
| Dépendance failed | Skip agents dépendants | Fixer puis retry |
| Critical failed | Stop workflow | Review manuel |

### 9.6 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F07-AC1 | DAG construit correctement |
| F07-AC2 | Exécution parallèle fonctionne |
| F07-AC3 | Dépendances respectées |
| F07-AC4 | Skip si dépendance échoue |
| F07-AC5 | Retry avec backoff |
| F07-AC6 | Continue si non-critical fails |

### 9.7 Effort Estimé: **34h (4.5j)**

---

## 10. F08 — Apprentissage Continu

### 10.1 Contexte et Justification

EPCI ne capitalise pas sur l'expérience. L'objectif est de créer un système d'apprentissage continu qui :
- Apprend des succès et échecs passés
- Améliore les estimations de temps
- Détecte et suggère des patterns récurrents
- Adapte le comportement aux préférences utilisateur

### 10.2 Domaines d'Apprentissage

| Domaine | Données Sources | Output |
|---------|----------------|--------|
| **Estimation** | Durée réelle vs estimée | Estimations ajustées |
| **Quality** | Issues par agent, récurrence | Prévention proactive |
| **Patterns** | Code généré, structures | Suggestions de pattern |
| **Preferences** | Choix utilisateur, feedback | Comportement adapté |
| **Conventions** | Code existant, corrections | Auto-application |

### 10.3 Boucle d'Apprentissage

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ COLLECT │ ──► │ ANALYZE │ ──► │  LEARN  │ ──► │  APPLY  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │                                               │
     └───────────────── FEEDBACK ───────────────────┘
```

**COLLECT**: Feature history, user feedback, code patterns, agent results  
**ANALYZE**: Trends, correlations, patterns, clusters  
**LEARN**: Update factors, create rules, extract templates  
**APPLY**: Adjusted estimations, warnings, suggestions

### 10.4 Modèle d'Estimation

```
estimation_factor = base_factor * complexity_multiplier * type_adjustment

Exemple:
  - 10 past "CRUD" features
  - Average actual/estimated ratio: 1.15
  - New CRUD feature estimation: base * 1.15
```

### 10.5 Commande /epci-learn

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🧠 EPCI Learning Status                                             │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Estimation Model ──────────────────────────────────────────────┐ │
│ │ Confidence: 85% (17 samples)                                    │ │
│ │ Base factor: 1.15 (estimations 15% optimistic)                  │ │
│ │                                                                 │ │
│ │ By complexity:                                                  │ │
│ │   TINY:     0.95 (5 samples) - estimates accurate              │ │
│ │   SMALL:    1.08 (6 samples) - slightly optimistic             │ │
│ │   STANDARD: 1.25 (4 samples) - often underestimated            │ │
│ │   LARGE:    1.45 (2 samples) - significantly underestimated    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Issue Patterns ────────────────────────────────────────────────┐ │
│ │ 1. missing_validation (6 occurrences, 70% confidence)          │ │
│ │ 2. n_plus_one (4 occurrences, 55% confidence)                  │ │
│ │ 3. missing_error_handling (3 occurrences, 45% confidence)      │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─ Code Patterns ─────────────────────────────────────────────────┐ │
│ │ • service: 2 patterns (high confidence)                        │ │
│ │ • controller: 2 patterns (high confidence)                     │ │
│ │ • repository: 1 pattern (medium confidence)                    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 10.6 Critères d'Acceptation

| ID | Critère |
|----|---------|
| F08-AC1 | Estimation s'améliore avec données |
| F08-AC2 | Issue patterns détectés |
| F08-AC3 | Warning si issue probable |
| F08-AC4 | Code patterns détectés |
| F08-AC5 | Préférences apprises |
| F08-AC6 | /epci-learn status fonctionne |

### 10.7 Effort Estimé: **35h (4.5j)**


---

## 11. Architecture Globale

### 11.1 Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EPCI v4.0 ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         USER INTERFACE                               │   │
│  │  Commands │ Breakpoints │ Feedback │ Progress │ Suggestions          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      ORCHESTRATION LAYER                             │   │
│  │  Orchestrator │ DAG Builder │ Agent Registry                         │   │
│  │  ┌───────────────────────────────────────────────────────────────┐  │   │
│  │  │ AGENTS: plan-validator │ code-reviewer │ security-auditor │   │  │   │
│  │  │         qa-reviewer │ doc-generator │ performance-auditor     │  │   │
│  │  └───────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    INTELLIGENCE LAYER                                │   │
│  │  Learning Engine │ Suggestions Engine │ Clarification Selector       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     PERSISTENCE LAYER                                │   │
│  │  Project Memory │ Feature History │ Metrics │ Learning Models        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     EXTENSION LAYER                                  │   │
│  │  Hooks │ Skills │ Stack References                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 11.2 Structure des Fichiers

```
.claude/
├── commands/                       # Commandes
│   ├── epci.md
│   ├── epci-brief.md
│   ├── epci-init.md               # NOUVEAU
│   ├── epci-metrics.md
│   ├── epci-memory.md             # NOUVEAU
│   └── epci-learn.md              # NOUVEAU
│
├── agents/                         # Agents
│   ├── plan-validator.md
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── qa-reviewer.md
│   ├── doc-generator.md
│   └── performance-auditor.md     # NOUVEAU
│
├── skills/stack/java-springboot/
│   ├── SKILL.md
│   └── references/                # NOUVEAU
│       ├── architecture.md
│       ├── jpa-hibernate.md
│       ├── security.md
│       ├── testing.md
│       └── reactive.md
│
├── hooks/                          # NOUVEAU
│   ├── README.md
│   ├── runner.py
│   └── examples/
│
├── project-memory/                 # NOUVEAU (données projet)
│   ├── context.json
│   ├── conventions.json
│   ├── history/
│   ├── patterns/
│   ├── metrics/
│   └── learning/
│
└── settings.json
```

---

## 12. Dépendances Inter-Fonctionnalités

### 12.1 Matrice de Dépendances

```
        F01  F02  F03  F04  F05  F06  F07  F08
F01      -    -    -    -    -    -    -    -
F02      -    -    -    -    -    -    ◐    -
F03      -    ◐    -    ●    -    ●    ●    -
F04      -    -    -    -    ●    ●    -    ●
F05      -    -    -    ●    -    -    -    ◐
F06      -    -    -    ●    -    -    -    ●
F07      -    ●    ●    -    -    -    -    -
F08      -    -    -    ●    ◐    ●    -    -

●  Dépendance forte (requise)
◐  Dépendance faible (enrichit)
-  Pas de dépendance
```

### 12.2 Ordre d'Implémentation Recommandé

```
PHASE 1 (v3.1) — Fondations
├── F01: Java Spring Boot References (indépendant)
├── F02: Système de Hooks (indépendant)
└── F03: Breakpoints Enrichis

PHASE 2 (v3.5) — Intelligence
├── F04: Project Memory (fondation)
├── F05: Clarification Intelligente
└── F06: Suggestions Proactives

PHASE 3 (v4.0) — Orchestration & Learning
├── F07: Orchestration Multi-Agents
└── F08: Apprentissage Continu
```

---

## 13. Plan de Tests

### 13.1 Stratégie de Test

| Niveau | Couverture | Outils |
|--------|------------|--------|
| Unitaire | 80% | pytest |
| Intégration | 60% | pytest-integration |
| E2E | Scénarios critiques | Manual + scripts |

### 13.2 Scénario E2E Principal

```gherkin
Feature: Complete EPCI Workflow
  Scenario: Standard feature with all systems active
    Given a project initialized with EPCI
    And project memory contains 5 previous features
    
    When I run "/epci-brief Add user preferences API"
    Then clarification should ask 2-3 context-aware questions
    And estimation should be adjusted based on history
    
    When I complete clarification
    Then @plan-validator should run via orchestrator
    And Breakpoint Phase 1 should show enriched format
    
    When I say "continue"
    Then Phase 2 should execute with parallel agents
    And hooks should run
    And Breakpoint Phase 2 should show results
    
    When I complete Phase 3
    Then learning models should update
    And feature history should be saved
```

### 13.3 Tests de Performance

| Test | Cible |
|------|-------|
| Orchestrator parallel (3 agents) | < 1.2x temps single |
| Memory load (100 features) | < 2s |
| Learning update | < 500ms |
| Suggestion generation | < 1s |

---

## 14. Planning et Jalons

### 14.1 Timeline

```
Janvier (Semaines 3-4)
├── F01: Java Spring Boot References ████████████ (2.5j)
└── F02: Système de Hooks ████████████████ (2.5j)

Février (Semaines 5-6)
├── F03: Breakpoints Enrichis ████████████ (2j)
└── F04: Project Memory █████████████████████████ (4.5j)

Février-Mars (Semaines 7-8)
├── F05: Clarification Intelligente ████████████████ (3j)
└── F06: Suggestions Proactives ████████████████ (3j)

Mars (Semaines 9-11)
├── F07: Orchestration Multi-Agents █████████████████████████ (4.5j)
└── F08: Apprentissage Continu █████████████████████████ (4.5j)

Mars (Semaine 12)
└── Tests E2E & Stabilisation ████████████████████ (5j)

Release v4.0 — Fin Mars 2025
```

### 14.2 Jalons

| Jalon | Date | Livrables |
|-------|------|-----------|
| **v3.1-alpha** | Fin Janvier | F01, F02 |
| **v3.1** | Mi-Février | F01, F02, F03 |
| **v3.5-alpha** | Fin Février | F04 |
| **v3.5** | Mi-Mars | F04, F05, F06 |
| **v4.0-beta** | Fin Mars | F07, F08 |
| **v4.0** | Début Avril | Tous |

### 14.3 Effort Total

| Fonctionnalité | Effort |
|----------------|--------|
| F01: Java Spring Boot | 20h |
| F02: Hooks | 18h |
| F03: Breakpoints | 14h |
| F04: Project Memory | 34h |
| F05: Clarification | 25h |
| F06: Suggestions | 24h |
| F07: Orchestration | 34h |
| F08: Apprentissage | 35h |
| Tests & Intégration | 40h |
| Documentation | 16h |
| **TOTAL** | **260h (≈33 jours ouvrés)** |

---

## 15. Annexes

### 15.1 Glossaire Complet

| Terme | Définition |
|-------|------------|
| Agent | Composant spécialisé effectuant une tâche de validation |
| Breakpoint | Point de pause nécessitant confirmation utilisateur |
| DAG | Directed Acyclic Graph - graphe d'exécution des agents |
| Feature Document | Document structuré décrivant une feature |
| Hook | Script exécuté automatiquement à un point du workflow |
| Learning Loop | Boucle d'apprentissage continu |
| Orchestrator | Composant coordonnant l'exécution des agents |
| Project Memory | Système de persistance du contexte projet |
| Skill | Module de connaissances pour un domaine spécifique |
| Stack | Ensemble technologique (ex: php-symfony) |

### 15.2 Références

| Document | Description |
|----------|-------------|
| EPCI v3.0 Plugin | Baseline actuelle |
| Claude MCP Docs | Documentation officielle Anthropic |
| Conventional Commits | Standard de commits |
| Spring Boot Docs | Documentation Spring |

### 15.3 Changelog du CDC

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0.0 | 2025-12-11 | Version initiale |

---

*Fin du Cahier des Charges*

**Document généré par Claude (Assistant IA)**  
**Pour**: Édouard — Développeur FullStack  
**Projet**: EPCI Plugin Évolutions v3.x → v4.0
