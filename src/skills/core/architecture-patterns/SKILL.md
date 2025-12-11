---
name: architecture-patterns
description: >-
  Patterns d'architecture logicielle courants. Inclut DDD, Clean Architecture,
  CQRS, Event Sourcing, Microservices patterns. Use when: évaluer complexité,
  choisir une architecture, refactoring structurel. Not for: conventions de code
  (→ code-conventions), patterns spécifiques stack (→ skills stack).
---

# Architecture Patterns

## Overview

Catalogue de patterns d'architecture pour guider les décisions de design.

## SOLID Principles

| Principe | Description | Violation typique |
|----------|-------------|-------------------|
| **S**ingle Responsibility | Une classe = une raison de changer | God class |
| **O**pen/Closed | Ouvert à l'extension, fermé à la modification | Switch sur types |
| **L**iskov Substitution | Sous-types substituables | Héritage cassant le contrat |
| **I**nterface Segregation | Interfaces spécifiques > interfaces générales | Interface fourre-tout |
| **D**ependency Inversion | Dépendre d'abstractions | Couplage fort aux implémentations |

## Patterns par niveau

### Application Level

| Pattern | Quand utiliser | Complexité |
|---------|----------------|------------|
| MVC | Apps web classiques | Faible |
| Clean Architecture | Logique métier complexe | Moyenne |
| Hexagonal | Ports & Adapters | Moyenne |
| CQRS | Read/Write séparés | Élevée |

### Domain Level (DDD)

| Pattern | Quand utiliser |
|---------|----------------|
| Entity | Objet avec identité propre |
| Value Object | Objet immuable sans identité |
| Aggregate | Groupe cohérent d'entités |
| Repository | Abstraction de persistance |
| Domain Service | Logique métier sans état |
| Domain Event | Notification de changement métier |

### Integration Level

| Pattern | Quand utiliser |
|---------|----------------|
| API Gateway | Point d'entrée unique |
| Event-Driven | Découplage asynchrone |
| Saga | Transactions distribuées |
| Circuit Breaker | Résilience aux pannes |

## Clean Architecture

```
┌─────────────────────────────────────────┐
│           Frameworks & Drivers          │  ← Web, DB, UI
├─────────────────────────────────────────┤
│         Interface Adapters              │  ← Controllers, Gateways
├─────────────────────────────────────────┤
│         Application Business Rules      │  ← Use Cases
├─────────────────────────────────────────┤
│         Enterprise Business Rules       │  ← Entities
└─────────────────────────────────────────┘
```

**Règle de dépendance** : Les dépendances pointent vers l'intérieur.

## Hexagonal Architecture

```
           ┌─────────────┐
    HTTP ──┤             ├── Database
           │   Domain    │
    CLI  ──┤             ├── External API
           └─────────────┘
        Ports             Adapters
        (in)              (out)
```

## Quick Reference

| Besoin | Pattern recommandé |
|--------|-------------------|
| Séparation UI/Métier | Clean Architecture |
| Testabilité maximale | Hexagonal (Ports & Adapters) |
| Scalabilité lecture | CQRS |
| Découplage services | Event-Driven |
| Transactions multi-services | Saga |
| Logique métier complexe | DDD |

## Anti-patterns à éviter

| Anti-pattern | Symptôme | Solution |
|--------------|----------|----------|
| Big Ball of Mud | Pas de structure visible | Refactor progressif vers Clean Arch |
| God Class | Classe > 500 lignes | Single Responsibility |
| Anemic Domain | Entités sans logique | Domain-Driven Design |
| Distributed Monolith | Micro mais couplé | Event-Driven ou monolithe |
| Leaky Abstraction | Détails qui fuient | Meilleure encapsulation |

## Décision de complexité

```
Complexité = f(domaine, intégrations, scalabilité, équipe)

Score 1-3 → MVC simple
Score 4-6 → Clean/Hexagonal
Score 7-9 → CQRS/Event-Driven
Score 10+ → Microservices
```
