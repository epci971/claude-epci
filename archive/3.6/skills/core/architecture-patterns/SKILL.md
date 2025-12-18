---
name: architecture-patterns
description: >-
  Common software architecture patterns. Includes DDD, Clean Architecture,
  CQRS, Event Sourcing, Microservices patterns. Use when: evaluating complexity,
  choosing an architecture, structural refactoring. Not for: code conventions
  (→ code-conventions), stack-specific patterns (→ stack skills).
---

# Architecture Patterns

## Overview

Catalog of architecture patterns to guide design decisions.

## SOLID Principles

| Principle | Description | Typical Violation |
|-----------|-------------|-------------------|
| **S**ingle Responsibility | One class = one reason to change | God class |
| **O**pen/Closed | Open for extension, closed for modification | Type switch |
| **L**iskov Substitution | Subtypes must be substitutable | Inheritance breaking contract |
| **I**nterface Segregation | Specific interfaces > general interfaces | Catch-all interface |
| **D**ependency Inversion | Depend on abstractions | Tight coupling to implementations |

## Patterns by Level

### Application Level

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| MVC | Classic web apps | Low |
| Clean Architecture | Complex business logic | Medium |
| Hexagonal | Ports & Adapters | Medium |
| CQRS | Separate Read/Write | High |

### Domain Level (DDD)

| Pattern | When to Use |
|---------|-------------|
| Entity | Object with own identity |
| Value Object | Immutable object without identity |
| Aggregate | Coherent group of entities |
| Repository | Persistence abstraction |
| Domain Service | Stateless business logic |
| Domain Event | Business change notification |

### Integration Level

| Pattern | When to Use |
|---------|-------------|
| API Gateway | Single entry point |
| Event-Driven | Asynchronous decoupling |
| Saga | Distributed transactions |
| Circuit Breaker | Fault resilience |

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

**Dependency Rule**: Dependencies point inward.

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

| Need | Recommended Pattern |
|------|---------------------|
| UI/Business separation | Clean Architecture |
| Maximum testability | Hexagonal (Ports & Adapters) |
| Read scalability | CQRS |
| Service decoupling | Event-Driven |
| Multi-service transactions | Saga |
| Complex business logic | DDD |

## Anti-patterns to Avoid

| Anti-pattern | Symptom | Solution |
|--------------|---------|----------|
| Big Ball of Mud | No visible structure | Progressive refactor to Clean Arch |
| God Class | Class > 500 lines | Single Responsibility |
| Anemic Domain | Entities without logic | Domain-Driven Design |
| Distributed Monolith | Micro but coupled | Event-Driven or monolith |
| Leaky Abstraction | Details leaking out | Better encapsulation |

## Complexity Decision

```
Complexity = f(domain, integrations, scalability, team)

Score 1-3 → Simple MVC
Score 4-6 → Clean/Hexagonal
Score 7-9 → CQRS/Event-Driven
Score 10+ → Microservices
```
