# Inventaire des Fonctionnalités — Plugin EPCI v3.0+

> **Version**: 1.0
> **Date**: 2025-01-XX
> **Objectif**: Audit d'intégrité et vérification fonctionnelle

---

## Table des matières

1. [Commandes](#1-commandes)
2. [Subagents](#2-subagents)
3. [Skills Core](#3-skills-core)
4. [Skills Stack](#4-skills-stack)
5. [Skills Factory](#5-skills-factory)
6. [Système de Hooks](#6-système-de-hooks)
7. [Project Memory](#7-project-memory)
8. [Système de Flags](#8-système-de-flags)
9. [Scripts de Validation](#9-scripts-de-validation)
10. [Brainstormer (à implémenter)](#10-brainstormer-à-implémenter)

---

## 1. Commandes

### 1.1 `/epci-brief` — Point d'entrée universel

**Fichier**: `commands/epci-brief.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-BRIEF-01 | Chargement Project Memory | Charge le contexte depuis `.project-memory/` | Le skill `project-memory-loader` est invoqué |
| CMD-BRIEF-02 | Exploration @Explore | Analyse codebase via Task tool avec @Explore | Subagent @Explore invoqué, résultats stockés |
| CMD-BRIEF-03 | Détection de stack | Identifie automatiquement le stack technique | Stack détecté et affiché dans le breakpoint |
| CMD-BRIEF-04 | Questions de clarification | Génère 2-3 questions max avec suggestions | Questions affichées avec suggestions IA |
| CMD-BRIEF-05 | Évaluation complexité | Calcule TINY/SMALL/STANDARD/LARGE/SPIKE | Catégorie affichée avec justification |
| CMD-BRIEF-06 | Auto-activation flags | Détecte et active les flags appropriés | Flags affichés avec source (auto/explicit) |
| CMD-BRIEF-07 | Breakpoint analyse | Affiche le breakpoint consolidé | Format conforme avec toutes sections |
| CMD-BRIEF-08 | Options interactives | 4 options : Répondre, Valider, Modifier, Lancer | Options fonctionnelles |
| CMD-BRIEF-09 | Génération inline brief | Brief inline pour TINY/SMALL | Brief structuré dans la réponse |
| CMD-BRIEF-10 | Génération Feature Document | Fichier `docs/features/<slug>.md` pour STANDARD/LARGE | Fichier créé avec §1 complet |
| CMD-BRIEF-11 | Routing workflow | Lance la commande recommandée | Commande appropriée déclenchée |

---

### 1.2 `/epci` — Workflow complet 3 phases

**Fichier**: `commands/epci.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-EPCI-01 | Pré-workflow Memory | Charge Project Memory avant Phase 1 | Contexte chargé et appliqué |
| CMD-EPCI-02 | Support arguments | `--large`, `--think`, `--safe`, `--wave`, etc. | Arguments parsés correctement |
| CMD-EPCI-03 | Alias `--large` | Expansion vers `--think-hard --wave` | Flags expandus et affichés |
| CMD-EPCI-04 | Mode `--continue` | Reprend une phase interrompue | Reprise depuis dernier état |
| CMD-EPCI-05 | Mode `--dry-run` | Simulation sans modifications | Aucun fichier modifié |
| **Phase 1** |
| CMD-EPCI-06 | Lecture Feature Document | Lit §1 du Feature Document | Vérifie que §1 existe |
| CMD-EPCI-07 | Planification directe | Création du plan d'implémentation | Tâches atomiques 2-15 min |
| CMD-EPCI-08 | Validation @plan-validator | Soumet le plan au validateur | Verdict APPROVED ou NEEDS_REVISION |
| CMD-EPCI-09 | Écriture §2 | Met à jour Feature Document avec Edit tool | §2 ajouté au document |
| CMD-EPCI-10 | Hooks pre/post Phase 1 | Exécution des hooks configurés | Hooks exécutés si actifs |
| CMD-EPCI-11 | Breakpoint enrichi BP1 | Affiche métriques, validations, preview | Format conforme avec toutes sections |
| **Phase 2** |
| CMD-EPCI-12 | Implémentation TDD | Red → Green → Refactor | Tests écrits avant code |
| CMD-EPCI-13 | @code-reviewer | Revue qualité obligatoire | Rapport généré avec verdict |
| CMD-EPCI-14 | @security-auditor | Audit OWASP (conditionnel) | Invoqué si fichiers sensibles |
| CMD-EPCI-15 | @qa-reviewer | Revue tests (conditionnel) | Invoqué si tests complexes |
| CMD-EPCI-16 | Suggestions proactives F06 | Génère suggestions après review | Suggestions affichées dans BP2 |
| CMD-EPCI-17 | Écriture §3 | Met à jour Feature Document | §3 ajouté avec progress |
| CMD-EPCI-18 | Hooks pre/post Phase 2 | Exécution des hooks | Hooks exécutés si actifs |
| CMD-EPCI-19 | Breakpoint enrichi BP2 | Métriques, verdicts, preview Phase 3 | Format conforme |
| **Phase 3** |
| CMD-EPCI-20 | Commit structuré | Conventional Commits format | Message conforme |
| CMD-EPCI-21 | @doc-generator | Génère/met à jour documentation | README, CHANGELOG mis à jour |
| CMD-EPCI-22 | Préparation PR | Prépare la Pull Request | Template PR généré |
| CMD-EPCI-23 | Learning update F08 | Sauvegarde dans Project Memory | Feature history mise à jour |
| CMD-EPCI-24 | Écriture §4 | Finalise le Feature Document | §4 complété |
| CMD-EPCI-25 | Hooks pre/post Phase 3 | Exécution des hooks | Hooks exécutés si actifs |
| CMD-EPCI-26 | Message completion | Affiche résumé final | Feature Document finalisé |

---

### 1.3 `/epci-quick` — Workflow condensé

**Fichier**: `commands/epci-quick.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-QUICK-01 | Mode TINY | 1 fichier, <50 LOC, sans tests | Modification appliquée |
| CMD-QUICK-02 | Mode SMALL | 2-3 fichiers, <200 LOC, tests optionnels | Modifications appliquées |
| CMD-QUICK-03 | Réception brief | Utilise le brief de `/epci-brief` | Brief détecté et utilisé |
| CMD-QUICK-04 | Implémentation directe | Sans Feature Document formel | Code modifié directement |
| CMD-QUICK-05 | Review light (SMALL) | @code-reviewer en mode light | Review simplifiée |
| CMD-QUICK-06 | Commit simplifié | Format Conventional Commits court | Commit généré |
| CMD-QUICK-07 | Détection escalade | Signale si complexité sous-estimée | Recommandation `/epci` |
| CMD-QUICK-08 | Flags supportés | `--fast`, `--uc` | Flags appliqués |
| CMD-QUICK-09 | Output formaté | Message TINY/SMALL COMPLETE | Format conforme |

---

### 1.4 `/epci-spike` — Exploration time-boxée

**Fichier**: `commands/epci-spike.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-SPIKE-01 | Arguments duration/question | Parse durée et question | Valeurs extraites |
| CMD-SPIKE-02 | Framing initial | Setup avec question, critères, scope | Spike Setup affiché |
| CMD-SPIKE-03 | Exploration @Explore | Recherche et analyse | Subagent invoqué |
| CMD-SPIKE-04 | Respect time-box | Arrêt à l'expiration | Durée respectée |
| CMD-SPIKE-05 | Synthèse findings | Résumé des découvertes | Synthèse générée |
| CMD-SPIKE-06 | Verdict GO/NO-GO/MORE_RESEARCH | Recommandation claire | Verdict justifié |
| CMD-SPIKE-07 | Génération Spike Report | Fichier `docs/spikes/<slug>.md` | Fichier créé |
| CMD-SPIKE-08 | Flag `--think-hard` | Support du flag | Analyse approfondie |

---

### 1.5 `/epci-decompose` — Décomposition PRD/CDC

**Fichier**: `commands/epci-decompose.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-DECOMP-01 | Validation fichier | Vérifie existence et format | Erreur si invalide |
| CMD-DECOMP-02 | Analyse structurelle | Détecte phases, étapes, dépendances | Structure extraite |
| CMD-DECOMP-03 | Détection dépendances | Explicit, FK, imports, références | Dépendances listées |
| CMD-DECOMP-04 | Granularité 1-5 jours | Respect des seuils min/max | Specs dans la plage |
| CMD-DECOMP-05 | @decompose-validator | Validation cohérence | Verdict généré |
| CMD-DECOMP-06 | Breakpoint proposition | Affiche découpage proposé | Format conforme |
| CMD-DECOMP-07 | Options modification | Fusionner, découper, renommer, etc. | Options fonctionnelles |
| CMD-DECOMP-08 | Génération INDEX.md | Overview avec Mermaid | Fichier créé |
| CMD-DECOMP-09 | Génération SXX-*.md | Sous-specs individuelles | Fichiers créés |
| CMD-DECOMP-10 | Graphe Mermaid | Flowchart dépendances | Diagramme valide |
| CMD-DECOMP-11 | Gantt Mermaid | Planning avec parallélisation | Diagramme valide |
| CMD-DECOMP-12 | EC: PRD trop petit | Redirect vers `/epci-brief` | Suggestion affichée |
| CMD-DECOMP-13 | EC: Dépendance circulaire | Détection et options | Erreur avec solutions |

---

### 1.6 `/epci-memory` — Gestion mémoire projet

**Fichier**: `commands/epci-memory.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-MEM-01 | Subcommand `status` | Affiche état mémoire | Dashboard affiché |
| CMD-MEM-02 | Subcommand `init` | Initialise `.project-memory/` | Structure créée |
| CMD-MEM-03 | Auto-détection stack | Détecte stack, conventions, patterns | Valeurs détectées |
| CMD-MEM-04 | Subcommand `reset` | Supprime avec confirmation | Backup créé, reset effectué |
| CMD-MEM-05 | Subcommand `export` | Export JSON complet | JSON valide généré |
| CMD-MEM-06 | Structure complète | Tous dossiers/fichiers créés | Arborescence conforme |

---

### 1.7 `/epci-learn` — Gestion apprentissage

**Fichier**: `commands/epci-learn.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-LEARN-01 | Subcommand `status` | Affiche état calibration | Dashboard affiché |
| CMD-LEARN-02 | Facteurs par complexité | TINY/SMALL/STANDARD/LARGE | Facteurs avec samples |
| CMD-LEARN-03 | Suggestion learning | Patterns trackés, disabled, preferred | Stats affichées |
| CMD-LEARN-04 | Subcommand `reset` | Reset avec backup | Données réinitialisées |
| CMD-LEARN-05 | Subcommand `export` | Export JSON complet | JSON valide |
| CMD-LEARN-06 | Subcommand `calibrate` | Recalibration forcée | Nouveaux facteurs calculés |

---

### 1.8 `/epci:create` — Factory de composants

**Fichier**: `commands/create.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| CMD-CREATE-01 | Type `skill` | Route vers `skills-creator` | Skill invoqué |
| CMD-CREATE-02 | Type `command` | Route vers `commands-creator` | Skill invoqué |
| CMD-CREATE-03 | Type `agent` | Route vers `subagents-creator` | Skill invoqué |
| CMD-CREATE-04 | Validation nom kebab-case | Vérifie format | Erreur si invalide |
| CMD-CREATE-05 | Détection existant | Vérifie si composant existe | Erreur avec options |
| CMD-CREATE-06 | Validation automatique | Exécute script de validation | Résultat affiché |

---

## 2. Subagents

### 2.1 `@plan-validator`

**Fichier**: `agents/plan-validator.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-PLAN-01 | Check Completeness | Stories, fichiers, tests, dépendances | Checklist complète |
| AGT-PLAN-02 | Check Consistency | Ordre, dépendances, estimates | Pas de cycle détecté |
| AGT-PLAN-03 | Check Feasibility | Risques, resources, tech | Mitigations identifiées |
| AGT-PLAN-04 | Check Quality | Tâches atomiques, claires | Descriptions actionnables |
| AGT-PLAN-05 | Verdict | APPROVED ou NEEDS_REVISION | Verdict justifié |
| AGT-PLAN-06 | Severity levels | Critical/Important/Minor | Issues classées |
| AGT-PLAN-07 | Format rapport | Markdown structuré | Format conforme |

---

### 2.2 `@code-reviewer`

**Fichier**: `agents/code-reviewer.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-CODE-01 | Review Code Quality | SRP, error handling, types, DRY | Checklist vérifiée |
| AGT-CODE-02 | Review Architecture | Patterns, coupling, performance | Issues identifiées |
| AGT-CODE-03 | Review Tests | Existence, logic, coverage | Tests évalués |
| AGT-CODE-04 | Plan Alignment | Tasks implemented, scope creep | Alignement vérifié |
| AGT-CODE-05 | Severity levels | 🔴 Critical / 🟠 Important / 🟡 Minor | Classification correcte |
| AGT-CODE-06 | Verdict | APPROVED / APPROVED_WITH_FIXES / NEEDS_REVISION | Verdict justifié |
| AGT-CODE-07 | Light mode | Review simplifiée pour `/epci-quick` | Mode activable |
| AGT-CODE-08 | Format rapport | Files, strengths, issues, verdict | Format conforme |

---

### 2.3 `@security-auditor`

**Fichier**: `agents/security-auditor.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-SEC-01 | OWASP Top 10 check | Injection, XSS, Auth, etc. | Vulnérabilités détectées |
| AGT-SEC-02 | Invocation conditionnelle | Fichiers auth/security/payment | Activé si patterns match |
| AGT-SEC-03 | Severity classification | Critical/High/Medium/Low | Classification CVSS |
| AGT-SEC-04 | Remediations | Suggestions de correction | Fixes proposés |
| AGT-SEC-05 | Verdict | APPROVED / NEEDS_FIXES | Verdict justifié |

---

### 2.4 `@qa-reviewer`

**Fichier**: `agents/qa-reviewer.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-QA-01 | Test coverage | Unit, integration, E2E | Coverage évaluée |
| AGT-QA-02 | Test quality | Assertions, mocking, edge cases | Qualité analysée |
| AGT-QA-03 | Invocation conditionnelle | >5 fichiers test ou tests complexes | Activé si critères |
| AGT-QA-04 | Recommendations | Amélioration tests | Suggestions fournies |
| AGT-QA-05 | Verdict | APPROVED / NEEDS_IMPROVEMENT | Verdict justifié |

---

### 2.5 `@doc-generator`

**Fichier**: `agents/doc-generator.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-DOC-01 | README update | Mise à jour si nouveau composant | README modifié |
| AGT-DOC-02 | CHANGELOG update | Entrée pour la feature | CHANGELOG modifié |
| AGT-DOC-03 | API documentation | Docblocks, swagger si applicable | Docs générées |
| AGT-DOC-04 | Files list | Liste des fichiers modifiés | Liste fournie |

---

### 2.6 `@decompose-validator`

**Fichier**: `agents/decompose-validator.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| AGT-DEC-01 | Dependency consistency | Pas de cycles, ordre valide | Graphe acyclique |
| AGT-DEC-02 | Granularity compliance | Specs dans plage min-max | Tailles conformes |
| AGT-DEC-03 | Coverage check | Tout le PRD couvert | Rien d'oublié |
| AGT-DEC-04 | Verdict | VALID / NEEDS_ADJUSTMENT | Verdict justifié |

---

## 3. Skills Core

### 3.1 `epci-core`

**Fichier**: `skills/core/epci-core/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-CORE-01 | Définition 4 phases | Explore, Plan, Code, Inspect | Documentation claire |
| SKL-CORE-02 | Catégories complexité | TINY/SMALL/STANDARD/LARGE/SPIKE | Critères définis |
| SKL-CORE-03 | Feature Document structure | §1-§4 sections | Template complet |
| SKL-CORE-04 | Breakpoints definition | BP1 et BP2 | Formats définis |
| SKL-CORE-05 | Routing logic | Brief → workflow approprié | Logique documentée |

---

### 3.2 `architecture-patterns`

**Fichier**: `skills/core/architecture-patterns/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-ARCH-01 | SOLID principles | Définitions et exemples | Documentation complète |
| SKL-ARCH-02 | Design patterns | Repository, Service, etc. | Patterns documentés |
| SKL-ARCH-03 | Clean Architecture | Layers et boundaries | Structure expliquée |
| SKL-ARCH-04 | Anti-patterns | Ce qu'il faut éviter | Liste avec exemples |

---

### 3.3 `breakpoint-metrics`

**Fichier**: `skills/core/breakpoint-metrics/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-BPM-01 | Scoring complexité | Algorithme de calcul | Formule documentée |
| SKL-BPM-02 | Estimation temps | Calibration appliquée | Temps ajustés |
| SKL-BPM-03 | Template BP1 | Format Phase 1 breakpoint | Template conforme |
| SKL-BPM-04 | Template BP2 | Format Phase 2 breakpoint | Template conforme |
| SKL-BPM-05 | Verdicts display | Format agents verdicts | Couleurs et status |

---

### 3.4 `clarification-intelligente`

**Fichier**: `skills/core/clarification-intelligente/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-CLAR-01 | Brief analysis | Extraction keywords, domain, gaps | Analyse générée |
| SKL-CLAR-02 | Similarity matching | Trouve features similaires | Matches trouvés |
| SKL-CLAR-03 | Question types | REUSE, TECHNICAL, SCOPE, INTEGRATION, PRIORITY | Types utilisés |
| SKL-CLAR-04 | Max 3 questions | Limite par itération | Limite respectée |
| SKL-CLAR-05 | Suggestions incluses | Réponses suggérées | Suggestions présentes |
| SKL-CLAR-06 | Graceful degradation | Fonctionne sans Project Memory | Fallback actif |

---

### 3.5 `flags-system`

**Fichier**: `skills/core/flags-system/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-FLAG-01 | Thinking flags | `--think`, `--think-hard`, `--ultrathink` | Comportement correct |
| SKL-FLAG-02 | Compression flags | `--uc`, `--verbose` | Output adapté |
| SKL-FLAG-03 | Workflow flags | `--safe`, `--fast`, `--dry-run` | Comportement correct |
| SKL-FLAG-04 | Wave flags | `--wave`, `--wave-strategy` | Orchestration activée |
| SKL-FLAG-05 | Auto-activation | Thresholds respectés | Flags auto-activés |
| SKL-FLAG-06 | Precedence rules | Résolution conflits | Conflits gérés |
| SKL-FLAG-07 | Display format | `FLAGS: flag (source)` | Format conforme |
| SKL-FLAG-08 | Alias expansion | `--large` → `--think-hard --wave` | Expansion correcte |

---

### 3.6 `proactive-suggestions` (F06)

**Fichier**: `skills/core/proactive-suggestions/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-SUGG-01 | Priority levels | P1 Security, P2 Perf/Quality, P3 Style | Classification correcte |
| SKL-SUGG-02 | Pattern catalog | Security, Performance, Quality patterns | Patterns définis |
| SKL-SUGG-03 | Scoring algorithm | base × impact × preference | Score calculé |
| SKL-SUGG-04 | Threshold filtering | score < 0.3 filtré | Suggestions filtrées |
| SKL-SUGG-05 | User actions | Accepter, Voir détails, Ignorer, Ne plus suggérer | Actions fonctionnelles |
| SKL-SUGG-06 | Learning integration | Feedback enregistré | Préférences mises à jour |
| SKL-SUGG-07 | Breakpoint display | Format full et compact | Affichage correct |

---

### 3.7 `learning-optimizer` (F08)

**Fichier**: `skills/core/learning-optimizer/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-LEARN-01 | Calibration EMA | Formule exponentielle | Calcul correct |
| SKL-LEARN-02 | Factor interpretation | >1.0 = under-estimate, <1.0 = over-estimate | Documentation claire |
| SKL-LEARN-03 | Confidence calculation | Logarithmique avec samples | Confidence correcte |
| SKL-LEARN-04 | Suggestion scoring | acceptance_rate × recency × relevance | Score calculé |
| SKL-LEARN-05 | Pattern detection | Auto-suggest après 3 occurrences | Détection fonctionnelle |

---

### 3.8 `project-memory`

**Fichier**: `skills/core/project-memory/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-PMEM-01 | Structure documentation | Arborescence `.project-memory/` | Structure documentée |
| SKL-PMEM-02 | Context schema | `context.json` format | Schema défini |
| SKL-PMEM-03 | Conventions schema | `conventions.json` format | Schema défini |
| SKL-PMEM-04 | Velocity metrics | `metrics/velocity.json` | Métriques définies |
| SKL-PMEM-05 | Feature history | `history/features/*.json` | Format défini |

---

### 3.9 `project-memory-loader`

**Fichier**: `skills/core/project-memory-loader/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-LOAD-01 | Load context | Charge context.json | Données disponibles |
| SKL-LOAD-02 | Load conventions | Charge conventions.json | Conventions appliquées |
| SKL-LOAD-03 | Load settings | Charge settings.json | Settings actifs |
| SKL-LOAD-04 | Load velocity | Charge velocity.json | Métriques disponibles |
| SKL-LOAD-05 | Graceful fallback | Fonctionne sans mémoire | Defaults appliqués |
| SKL-LOAD-06 | Status display | Affiche état mémoire | Status visible |

---

### 3.10 Autres skills core

| Skill | Fichier | Fonctionnalités principales |
|-------|---------|----------------------------|
| `code-conventions` | `skills/core/code-conventions/SKILL.md` | Naming, structure, DRY/KISS |
| `testing-strategy` | `skills/core/testing-strategy/SKILL.md` | TDD, coverage, mocking |
| `git-workflow` | `skills/core/git-workflow/SKILL.md` | Conventional Commits, branching |

---

## 4. Skills Stack

| Skill | Fichier | Critères d'auto-détection |
|-------|---------|---------------------------|
| `php-symfony` | `skills/stack/php-symfony/SKILL.md` | `composer.json` + symfony |
| `javascript-react` | `skills/stack/javascript-react/SKILL.md` | `package.json` + react |
| `python-django` | `skills/stack/python-django/SKILL.md` | `requirements.txt` + django |
| `java-springboot` | `skills/stack/java-springboot/SKILL.md` | `pom.xml` + spring-boot |

Pour chaque stack skill :

| ID | Fonctionnalité | Critère de vérification |
|----|----------------|-------------------------|
| SKL-STACK-01 | Auto-détection | Skill chargé si pattern détecté |
| SKL-STACK-02 | Architecture patterns | Patterns spécifiques au stack |
| SKL-STACK-03 | Testing patterns | Stratégies de test du stack |
| SKL-STACK-04 | References | Fichiers références disponibles |

---

## 5. Skills Factory

### 5.1 `skills-creator`

**Fichier**: `skills/factory/skills-creator/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-FAC-SK-01 | 6-phase workflow | Qualification → Definition → Content → References → Validation → Triggering | Phases suivies |
| SKL-FAC-SK-02 | Templates | Core skill, Stack skill | Templates disponibles |
| SKL-FAC-SK-03 | Description formula | Use when + Not for | Format respecté |
| SKL-FAC-SK-04 | Validation | Script `validate_skill.py` | Validation exécutée |
| SKL-FAC-SK-05 | Triggering test | Script `test_triggering.py` | Test exécuté |
| SKL-FAC-SK-06 | References | YAML rules, best practices, etc. | Références disponibles |

---

### 5.2 `commands-creator`

**Fichier**: `skills/factory/commands-creator/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-FAC-CMD-01 | Templates | Simple command, Workflow command | Templates disponibles |
| SKL-FAC-CMD-02 | Frontmatter guide | YAML format documentation | Guide disponible |
| SKL-FAC-CMD-03 | Tools reference | Liste des tools valides | Référence disponible |
| SKL-FAC-CMD-04 | Validation | Script `validate_command.py` | Validation exécutée |

---

### 5.3 `subagents-creator`

**Fichier**: `skills/factory/subagents-creator/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-FAC-AGT-01 | Templates | Reviewer, Validator, Generator | Templates disponibles |
| SKL-FAC-AGT-02 | Least privilege guide | Minimal tools | Guide disponible |
| SKL-FAC-AGT-03 | Output patterns | Formats de sortie | Patterns documentés |
| SKL-FAC-AGT-04 | Validation | Script `validate_subagent.py` | Validation exécutée |

---

### 5.4 `component-advisor`

**Fichier**: `skills/factory/component-advisor/SKILL.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| SKL-FAC-ADV-01 | Detection patterns | Quand suggérer un nouveau composant | Patterns définis |
| SKL-FAC-ADV-02 | Suggestion examples | Exemples de suggestions | Exemples disponibles |
| SKL-FAC-ADV-03 | Passive activation | S'active automatiquement | Détection passive |

---

## 6. Système de Hooks

**Fichiers**: `hooks/README.md`, `hooks/runner.py`, `hooks/active/`, `hooks/examples/`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| HOOK-01 | 7 types de hooks | pre/post phase-1/2/3, on-breakpoint | Types documentés |
| HOOK-02 | Découverte automatique | Hooks dans `active/` détectés | Hooks découverts |
| HOOK-03 | Naming convention | `{type}[-name].{ext}` | Convention respectée |
| HOOK-04 | Input JSON context | Contexte passé via stdin | Contexte reçu |
| HOOK-05 | Output JSON | status, message | Format respecté |
| HOOK-06 | Support Bash/Python/Node | 3 langages supportés | Exécution correcte |
| HOOK-07 | Timeout configurable | Default 30s | Timeout respecté |
| HOOK-08 | Error handling | fail_on_error configurable | Comportement correct |
| HOOK-09 | Context fields | phase, feature_slug, flags, etc. | Champs disponibles |
| HOOK-10 | Hooks actifs par défaut | pre-phase-2-lint, post-phase-2-suggestions, post-phase-3-memory-update, on-breakpoint-memory-context | Hooks fonctionnels |

---

## 7. Project Memory

**Fichiers**: `project-memory/*.py`, `project-memory/schemas/`, `project-memory/templates/`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| PMEM-01 | Manager | Gestion centralisée | CRUD fonctionnel |
| PMEM-02 | Detector | Auto-détection stack/conventions | Détection correcte |
| PMEM-03 | Calibration | EMA pour estimations | Calcul correct |
| PMEM-04 | Clarification analyzer | Analyse de brief | Keywords/gaps extraits |
| PMEM-05 | Similarity matcher | Jaccard similarity | Matches trouvés |
| PMEM-06 | Question generator | Génération questions intelligentes | Questions pertinentes |
| PMEM-07 | Suggestion engine | Scoring et filtrage | Suggestions générées |
| PMEM-08 | Learning analyzer | Apprentissage patterns | Patterns détectés |
| PMEM-09 | Pattern catalog | Catalogue de patterns | Patterns disponibles |
| PMEM-10 | Schemas JSON | Validation des fichiers | Schemas valides |
| PMEM-11 | Templates | Fichiers par défaut | Templates disponibles |
| PMEM-12 | Tests unitaires | Couverture des modules | Tests passent |

---

## 8. Système de Flags

**Fichier**: `settings/flags.md`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| FLAG-01 | Documentation complète | Tous flags documentés | Flags listés |
| FLAG-02 | Thresholds définis | Seuils d'auto-activation | Seuils documentés |
| FLAG-03 | Compatibility matrix | Conflits documentés | Matrice disponible |
| FLAG-04 | Source tracking | auto/explicit/alias | Sources trackées |

---

## 9. Scripts de Validation

**Fichiers**: `scripts/*.py`

| Script | Fonctionnalité | Critère de vérification |
|--------|----------------|-------------------------|
| `validate_skill.py` | Valide un skill | Retourne pass/fail avec détails |
| `validate_command.py` | Valide une commande | Retourne pass/fail avec détails |
| `validate_subagent.py` | Valide un subagent | Retourne pass/fail avec détails |
| `validate_all.py` | Valide tous les composants | Rapport global |
| `validate_flags.py` | Valide configuration flags | Configuration valide |
| `validate_memory.py` | Valide Project Memory | Structure valide |
| `test_triggering.py` | Teste auto-activation skills | Tests pass/fail |

---

## 10. Brainstormer (à implémenter)

**Fichiers à créer**: `commands/brainstorm.md`, `skills/core/brainstormer/`

| ID | Fonctionnalité | Description | Critère de vérification |
|----|----------------|-------------|-------------------------|
| BRAIN-01 | Commande `/brainstorm` | Point d'entrée | Commande reconnue |
| BRAIN-02 | Phase Init | Analyse codebase + questions cadrage | @Explore invoqué, questions générées |
| BRAIN-03 | Phase Iterate | Boucle questions/réponses | Itérations fonctionnelles |
| BRAIN-04 | Commande `continue` | Itération suivante | Nouvelles questions |
| BRAIN-05 | Commande `dive [topic]` | Approfondissement | Questions ciblées |
| BRAIN-06 | Commande `pivot` | Réorientation | Reset partiel EMS |
| BRAIN-07 | Commande `status` | EMS détaillé | 5 axes affichés |
| BRAIN-08 | Commande `finish` | Génération livrables | Brief + Journal créés |
| BRAIN-09 | EMS scoring | 5 axes, 0-100 | Score calculé |
| BRAIN-10 | Breakpoint compact | <15 lignes | Format respecté |
| BRAIN-11 | Frameworks | MoSCoW, 5 Whys, SWOT, Scoring | Application automatique |
| BRAIN-12 | Détection biais | Confirmation, Ancrage, Scope Creep | Alertes générées |
| BRAIN-13 | Output brief | `./docs/briefs/brief-*.md` | Fichier créé |
| BRAIN-14 | Output journal | `./docs/briefs/journal-*.md` | Fichier créé |
| BRAIN-15 | Format brief | Compatible EPCI | Structure conforme |

---

## Annexe A — Matrice de couverture

### Commandes

| Commande | Fichier existe | Frontmatter valide | Process documenté | Tests |
|----------|----------------|-------------------|-------------------|-------|
| `/epci-brief` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci-quick` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci-spike` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci-decompose` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci-memory` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci-learn` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/epci:create` | ⬜ | ⬜ | ⬜ | ⬜ |
| `/brainstorm` | ⬜ | ⬜ | ⬜ | ⬜ |

### Subagents

| Agent | Fichier existe | Frontmatter valide | Tools restrictifs | Output documenté |
|-------|----------------|-------------------|-------------------|------------------|
| `@plan-validator` | ⬜ | ⬜ | ⬜ | ⬜ |
| `@code-reviewer` | ⬜ | ⬜ | ⬜ | ⬜ |
| `@security-auditor` | ⬜ | ⬜ | ⬜ | ⬜ |
| `@qa-reviewer` | ⬜ | ⬜ | ⬜ | ⬜ |
| `@doc-generator` | ⬜ | ⬜ | ⬜ | ⬜ |
| `@decompose-validator` | ⬜ | ⬜ | ⬜ | ⬜ |

### Skills

| Catégorie | Nombre | Fichiers existent | YAML valide | < 5000 tokens | Références ok |
|-----------|--------|-------------------|-------------|---------------|---------------|
| Core | 12 | ⬜ | ⬜ | ⬜ | ⬜ |
| Stack | 4 | ⬜ | ⬜ | ⬜ | ⬜ |
| Factory | 4 | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Annexe B — Checklist d'audit

### Audit rapide (10 min)

```
[ ] Tous les fichiers commands/*.md existent
[ ] Tous les fichiers agents/*.md existent
[ ] Tous les dossiers skills/core/* ont SKILL.md
[ ] Scripts de validation exécutables
[ ] hooks/runner.py fonctionne
```

### Audit complet (1h)

```
[ ] Exécuter validate_all.py
[ ] Exécuter test_triggering.py
[ ] Tester /epci-brief avec un brief simple
[ ] Tester /epci-quick en mode TINY
[ ] Tester /epci-memory init
[ ] Tester /epci-learn status
[ ] Vérifier hooks actifs
[ ] Vérifier schemas JSON valides
```

### Audit fonctionnel (2h+)

```
[ ] Workflow complet /epci-brief → /epci (3 phases)
[ ] /epci-decompose sur un PRD réel
[ ] /epci-spike avec time-box
[ ] /epci:create skill + validation
[ ] Vérifier calibration après feature complète
[ ] Vérifier suggestions proactives en BP2
```

---

*Fin de l'inventaire — Document prêt pour audit Claude Code*
