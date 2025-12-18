# Cahier des Charges — F01: Java Spring Boot References

> **Document**: CDC-F01-001
> **Version**: 1.0.0
> **Date**: 2025-12-15
> **Statut**: Validé
> **Feature ID**: F01
> **Version cible**: EPCI v3.1
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

Le plugin EPCI v3.0.0 est opérationnel avec **23 composants validés** :
- 5 commandes
- 5 subagents
- 13 skills (dont 4 stack skills)

### 1.3 Glossaire Pertinent

| Terme | Définition |
|-------|------------|
| **Skill** | Module de connaissances pour un domaine spécifique |
| **Stack Skill** | Skill spécialisé pour une technologie (php-symfony, java-springboot, etc.) |
| **Progressive Disclosure** | Pattern où les références détaillées sont dans un sous-dossier `references/` |

---

## 2. Description de la Feature

### 2.1 Contexte et Justification

Le skill `java-springboot` est **le seul stack skill sans dossier `references/`**. Cette inconsistance rompt le pattern Progressive Disclosure appliqué aux autres stacks.

**Situation actuelle** :
```
skills/stack/java-springboot/
└── SKILL.md                          # Existant mais incomplet
```

**Situation cible** :
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

### 2.2 Objectif

Créer les fichiers de référence Java Spring Boot pour :
1. Aligner avec les autres stack skills (php-symfony, javascript-react, python-django)
2. Fournir des patterns et exemples de code compilables
3. Respecter les contraintes de tokens pour un chargement rapide

---

## 3. Exigences Fonctionnelles

### 3.1 Fichier `architecture.md`

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Structure projet | Arborescence Maven/Gradle standard | P1 |
| [MUST] Couches architecture | Controller → Service → Repository | P1 |
| [MUST] Clean Architecture | Ports & Adapters avec Spring | P1 |
| [MUST] Hexagonal | Implémentation avec annotations Spring | P1 |
| [SHOULD] CQRS | Command/Query separation | P2 |
| [SHOULD] Modular monolith | Multi-module Maven/Gradle | P2 |

### 3.2 Fichier `jpa-hibernate.md`

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] Entity patterns | Annotations JPA, Lombok, equals/hashCode | P1 |
| [MUST] Repository | JpaRepository, custom queries, Specifications | P1 |
| [MUST] Relations | OneToMany, ManyToOne, fetch strategies | P1 |
| [MUST] N+1 prevention | EntityGraph, JOIN FETCH, batch size | P1 |
| [SHOULD] Auditing | @CreatedDate, @LastModifiedDate, Envers | P2 |
| [SHOULD] Migrations | Flyway/Liquibase patterns | P2 |

### 3.3 Fichier `security.md`

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] SecurityFilterChain | Configuration Spring Security 6 lambda DSL | P1 |
| [MUST] Authentication | JWT, OAuth2, Basic Auth | P1 |
| [MUST] Authorization | @PreAuthorize, Method security | P1 |
| [MUST] CSRF/CORS | Configuration REST API | P1 |
| [SHOULD] Password encoding | BCrypt, Argon2 | P2 |
| [SHOULD] Rate limiting | Bucket4j, Resilience4j | P2 |

### 3.4 Fichier `testing.md`

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MUST] JUnit 5 | @Test, @Nested, @ParameterizedTest | P1 |
| [MUST] Mockito | @Mock, @InjectMocks, verify | P1 |
| [MUST] Spring Boot Test | @SpringBootTest, @WebMvcTest, @DataJpaTest | P1 |
| [MUST] MockMvc | API testing patterns | P1 |
| [SHOULD] TestContainers | PostgreSQL, Redis, Kafka | P2 |
| [SHOULD] ArchUnit | Architecture tests | P2 |

### 3.5 Fichier `reactive.md` (Optionnel)

| Exigence | Description | Priorité |
|----------|-------------|----------|
| [MAY] WebFlux | Reactive controllers, RouterFunctions | P3 |
| [MAY] R2DBC | Reactive database access | P3 |
| [MAY] Reactive patterns | Mono, Flux, backpressure | P3 |

---

## 4. Contraintes Techniques

| Contrainte | Valeur | Justification |
|------------|--------|---------------|
| Taille max par fichier | 400 lignes | Chargement rapide |
| Tokens max par fichier | 3000 tokens | Context window |
| Version Java minimum | Java 17 | LTS actuel |
| Version Spring Boot | 3.2+ | Dernière stable |

---

## 5. Critères d'Acceptation

| ID | Critère | Méthode de vérification |
|----|---------|-------------------------|
| F01-AC1 | 5 fichiers references créés | `ls skills/stack/java-springboot/references/` |
| F01-AC2 | Chaque fichier < 400 lignes | `wc -l` sur chaque fichier |
| F01-AC3 | SKILL.md mis à jour avec liens | Grep `@references/` |
| F01-AC4 | Validation script passe | `python scripts/validate_skill.py` |
| F01-AC5 | Exemples de code compilables | Revue manuelle |

---

## 6. Dépendances

### 6.1 Dépendances Entrantes (cette feature dépend de)

| Feature | Type | Description |
|---------|------|-------------|
| Aucune | — | Feature indépendante |

### 6.2 Dépendances Sortantes (dépendent de cette feature)

| Feature | Type | Description |
|---------|------|-------------|
| F09 Personas | Faible | Le persona backend peut utiliser ces références |

---

## 7. Effort Estimé

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

## 8. Livrables

1. `skills/stack/java-springboot/references/architecture.md`
2. `skills/stack/java-springboot/references/jpa-hibernate.md`
3. `skills/stack/java-springboot/references/security.md`
4. `skills/stack/java-springboot/references/testing.md`
5. `skills/stack/java-springboot/references/reactive.md`
6. `skills/stack/java-springboot/SKILL.md` (mis à jour)

---

## 9. Hors Périmètre

- Création de nouveaux stack skills (Go, Rust, .NET)
- Refactoring des autres stack skills existants
- Documentation utilisateur externe

---

*Document généré depuis CDC-EPCI-UNIFIE-v4.md*
