---
paths: []
---

# Domain Glossary

> Termes metier specifiques au projet.

## 🟡 CONVENTIONS

Ce glossaire definit les termes metier utilises dans le code et la documentation.
Utiliser ces termes de maniere coherente pour faciliter la comprehension.

## Business Terms

| Terme | Definition | Contexte |
|-------|------------|----------|
| {{term_1}} | {{definition_1}} | {{context_1}} |
| {{term_2}} | {{definition_2}} | {{context_2}} |
| {{term_3}} | {{definition_3}} | {{context_3}} |

## Technical Terms

| Terme | Definition | Usage |
|-------|------------|-------|
| Entity | Objet metier avec identite | Models, Domain |
| DTO | Data Transfer Object | API, Services |
| Repository | Abstraction acces donnees | Data layer |
| Service | Logique metier | Business layer |
| Handler | Traitement d'une action | CQRS, Events |

## Abbreviations

| Abbreviation | Signification |
|--------------|---------------|
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| DTO | Data Transfer Object |
| ORM | Object-Relational Mapping |
| SRP | Single Responsibility Principle |

## Naming Conventions

| Concept | Convention | Exemple |
|---------|------------|---------|
| Entity | Singular, PascalCase | `User`, `Order` |
| Table | Plural, snake_case | `users`, `orders` |
| Service | Descriptive + Service | `UserService`, `OrderHandler` |
| Repository | Entity + Repository | `UserRepository` |
| DTO | Action + Entity + Dto | `CreateUserDto` |

## Quick Reference

Quand vous rencontrez un terme metier dans le code:

1. Verifiez sa definition dans ce glossaire
2. Utilisez le terme exact (pas de synonymes)
3. Si nouveau terme, ajoutez-le ici avec l'equipe
