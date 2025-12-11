---
name: epci-core
description: >-
  Concepts fondamentaux du workflow EPCI. Définit les phases (Explore, Plan,
  Code, Inspect), les catégories de complexité, le Feature Document et les
  breakpoints. Use when: tout workflow EPCI, comprendre la méthodologie.
  Not for: création de composants (utiliser /epci:create).
---

# EPCI Core

## Overview

EPCI (Explore → Plan → Code → Inspect) est une méthodologie de développement
structurée en phases avec validation à chaque étape.

## Les 4 Phases

| Phase | Objectif | Output |
|-------|----------|--------|
| **Explore** | Comprendre le besoin et l'existant | Brief fonctionnel |
| **Plan** | Concevoir la solution | Plan d'implémentation |
| **Code** | Implémenter avec tests | Code + tests |
| **Inspect** | Valider et finaliser | PR prête |

## Catégories de complexité

| Catégorie | Fichiers | LOC | Risque | Workflow |
|-----------|----------|-----|--------|----------|
| TINY | 1 | <50 | Aucun | /epci-quick |
| SMALL | 2-3 | <200 | Faible | /epci-quick |
| STANDARD | 4-10 | <1000 | Moyen | /epci |
| LARGE | 10+ | 1000+ | Élevé | /epci |
| SPIKE | ? | ? | Inconnu | /epci-spike |

## Feature Document

Document central de traçabilité pour chaque feature STANDARD/LARGE.

### Structure

```markdown
# Feature Document — [ID]

## §1 — Brief Fonctionnel
[Contexte, critères d'acceptation, contraintes]

## §2 — Plan d'Implémentation
[Tâches, fichiers, risques]

## §3 — Implémentation
[Progression, tests, reviews]

## §4 — Finalisation
[Commit, documentation, PR]
```

### Emplacement

```
docs/features/<feature-slug>.md
```

## Breakpoints

Points de synchronisation obligatoires :

| Breakpoint | Après | Condition de passage |
|------------|-------|---------------------|
| BP1 | Phase 1 | Plan validé par @plan-validator |
| BP2 | Phase 2 | Code reviewé par @code-reviewer |

## Subagents EPCI

| Subagent | Rôle | Phase |
|----------|------|-------|
| @plan-validator | Valide le plan technique | Phase 1 → BP1 |
| @code-reviewer | Revue qualité code | Phase 2 → BP2 |
| @security-auditor | Audit sécurité OWASP | Phase 2 (conditionnel) |
| @qa-reviewer | Revue tests | Phase 2 (conditionnel) |
| @doc-generator | Génère documentation | Phase 3 |

## Routing

```
Brief utilisateur
      │
      ▼
  /epci-brief (évaluation)
      │
      ├─► TINY/SMALL ──► /epci-quick
      │
      ├─► STANDARD ────► /epci
      │
      ├─► LARGE ───────► /epci --large
      │
      └─► Incertain ───► /epci-spike
```

## Principes EPCI

1. **Traçabilité** — Tout est documenté dans le Feature Document
2. **Validation** — Chaque phase a une gate de sortie
3. **Itération** — Les phases peuvent être revisitées si nécessaire
4. **Adaptation** — Le workflow s'adapte à la complexité
5. **Automatisation** — Les subagents automatisent les reviews
