# Guide de Génération de Rules Claude Code

## Vue d'ensemble

Ce guide permet à Claude Code d'analyser un projet et de générer automatiquement une structure `.claude/rules/` optimisée. Il peut être utilisé comme prompt direct ou intégré dans une commande EPCI.

---

## Phase 1 : Analyse du projet

### 1.1 Détection automatique de la stack

Analyser les fichiers de configuration pour identifier :

| Fichier | Détecte |
|---------|---------|
| `composer.json` | Symfony, Laravel, PHP version, packages |
| `package.json` | React, Vue, TypeScript, Node version |
| `requirements.txt` / `pyproject.toml` | Django, FastAPI, Python version |
| `Gemfile` | Rails, Ruby version |
| `go.mod` | Go version, modules |
| `Cargo.toml` | Rust, crates |
| `docker-compose.yml` | Services (DB, Redis, RabbitMQ...) |
| `.env.example` | Variables d'environnement attendues |

### 1.2 Analyse de la structure

```
Détecter :
├── Architecture (MVC, Hexagonal, DDD, Clean Architecture)
├── Organisation des dossiers (src/, app/, lib/, tests/)
├── Patterns de nommage (fichiers, classes, fonctions)
├── Séparation frontend/backend (monorepo, séparé)
└── Configuration existante (ESLint, PHPStan, Prettier...)
```

### 1.3 Extraction des conventions existantes

Analyser le code existant pour détecter :

- **Naming conventions** : camelCase, snake_case, PascalCase selon contexte
- **Patterns récurrents** : injection de dépendances, repositories, DTOs
- **Style de tests** : unitaires, intégration, e2e, mocking strategy
- **Gestion d'erreurs** : exceptions custom, error handling patterns
- **Documentation** : docblocks, comments, README structure

---

## Phase 2 : Structure de rules recommandée

### 2.1 Arborescence type

```
.claude/
├── CLAUDE.md                      # Essentiels uniquement (< 50 lignes)
└── rules/
    ├── _global/                   # Sans paths = toujours actif
    │   ├── quality.md             # Standards qualité transversaux
    │   ├── git-workflow.md        # Conventions git/commits
    │   └── commands.md            # Commandes fréquentes
    │
    ├── backend/                   # Rules backend conditionnelles
    │   ├── {framework}.md         # Ex: symfony.md, django.md
    │   ├── database.md            # ORM, migrations, queries
    │   ├── api.md                 # REST/GraphQL conventions
    │   └── security.md            # Auth, validation, CORS
    │
    ├── frontend/                  # Rules frontend conditionnelles
    │   ├── {framework}.md         # Ex: react.md, vue.md
    │   ├── components.md          # Architecture composants
    │   ├── state.md               # State management
    │   └── styling.md             # CSS/Tailwind conventions
    │
    ├── testing/                   # Rules de tests conditionnelles
    │   ├── unit.md                # Tests unitaires
    │   ├── integration.md         # Tests d'intégration
    │   └── e2e.md                 # Tests end-to-end
    │
    └── domain/                    # Rules métier spécifiques
        └── {domain}.md            # Glossaire et règles métier
```

### 2.2 Template de fichier rule

```markdown
---
paths:
  - pattern/vers/fichiers/**/*
  - autre/pattern/**/*.ext
---

# {Nom de la Rule}

> Description courte du scope de cette rule

## 🔴 CRITICAL (Ne jamais violer)

1. **Règle absolue** : Explication
2. **Autre règle critique** : Explication

## 🟡 CONVENTIONS (Standard du projet)

- Convention 1 : détail
- Convention 2 : détail

## 🟢 PRÉFÉRENCES (Quand applicable)

- Préférence 1
- Préférence 2

## Patterns

| Besoin | Solution |
|--------|----------|
| Cas d'usage 1 | Pattern à utiliser |
| Cas d'usage 2 | Pattern à utiliser |

## Anti-patterns ❌

- Ne pas faire X parce que Y
- Éviter Z dans ce contexte

## Exemples

### ✅ Correct

```{lang}
// Code exemple correct
```

### ❌ Incorrect

```{lang}
// Code exemple à éviter
```
```

---

## Phase 3 : Génération des rules

### 3.1 CLAUDE.md principal (lean)

```markdown
# {Nom du Projet}

## Quick Start

- `{cmd_install}` — Installation
- `{cmd_dev}` — Serveur de dev
- `{cmd_test}` — Lancer les tests
- `{cmd_lint}` — Linting/formatting

## Stack

- **Backend** : {framework} {version}
- **Frontend** : {framework} {version}
- **Database** : {db} {version}
- **Infra** : {docker/k8s/...}

## Architecture

{description courte de l'architecture}

→ Voir `.claude/rules/` pour les conventions détaillées

## Contacts

- Tech Lead : {nom}
- Repo : {url}
```

### 3.2 Rules par framework

#### Symfony

```markdown
---
paths:
  - src/**/*.php
  - config/**/*.yaml
---

# Symfony Rules

## 🔴 CRITICAL

1. **Controllers thin** : Max 20 lignes par action, déléguer aux services
2. **Injection constructeur** : Jamais `$container->get()`, toujours autowiring
3. **Pas d'entités dans les réponses API** : Utiliser des DTOs

## 🟡 CONVENTIONS

- Naming controllers : `{Resource}{Action}Controller`
- Services : suffixe `Service`, `Handler`, `Provider` selon le rôle
- Repositories : un par entité, méthodes custom nommées `findBy{Criteria}`
- Events : suffixe `Event`, listeners suffixe `Listener`

## Patterns

| Besoin | Solution |
|--------|----------|
| Validation | Symfony Constraints (annotations/attributes) |
| Transformation | AutoMapper ou Serializer avec groups |
| Auth | LexikJWTBundle ou Symfony Security |
| Queue | Messenger avec transports async |
| Cache | Symfony Cache avec tags |

## Commandes utiles

- `bin/console debug:router` — Liste des routes
- `bin/console make:entity` — Créer entité
- `bin/console doctrine:migrations:diff` — Générer migration
```

#### React/TypeScript

```markdown
---
paths:
  - src/**/*.tsx
  - src/**/*.ts
  - "!src/**/*.test.ts"
---

# React/TypeScript Rules

## 🔴 CRITICAL

1. **Jamais `any`** : Typer explicitement, utiliser `unknown` si nécessaire
2. **Composants fonctionnels** : Pas de classes
3. **Keys uniques** : Jamais d'index comme key dans les listes dynamiques

## 🟡 CONVENTIONS

- Naming : PascalCase pour composants, camelCase pour hooks/utils
- Un composant = un fichier
- Props typées avec `interface {Component}Props`
- Hooks custom préfixés `use`

## Patterns

| Besoin | Solution |
|--------|----------|
| State local | useState, useReducer |
| State global | Zustand / Redux Toolkit |
| Data fetching | TanStack Query |
| Forms | React Hook Form + Zod |
| Styling | Tailwind CSS |

## Structure composant

```tsx
interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  // hooks en premier
  const [state, setState] = useState(false);
  
  // handlers
  const handleClick = useCallback(() => {
    onAction?.();
  }, [onAction]);
  
  // render
  return <div onClick={handleClick}>{title}</div>;
}
```
```

#### Django

```markdown
---
paths:
  - "**/*.py"
  - "!**/migrations/**"
---

# Django Rules

## 🔴 CRITICAL

1. **Migrations versionnées** : Jamais de `--fake`, toujours commiter les migrations
2. **Pas de logique dans les views** : Déléguer aux services/managers
3. **QuerySets lazy** : Attention aux N+1, utiliser `select_related`/`prefetch_related`

## 🟡 CONVENTIONS

- Models : singulier, PascalCase
- Apps : pluriel, snake_case
- Services dans `services.py` ou dossier `services/`
- Serializers miroir des models

## Patterns

| Besoin | Solution |
|--------|----------|
| Validation | Serializers DRF + validators |
| Auth | DRF TokenAuth ou SimpleJWT |
| Tasks async | Celery |
| Cache | Django cache framework + Redis |
| Admin | ModelAdmin customisé |
```

### 3.3 Rules transversales

#### Git Workflow

```markdown
# Git Workflow

## Branches

- `main` : Production, protégée
- `develop` : Intégration (si gitflow)
- `feature/{ticket}-{description}` : Nouvelles fonctionnalités
- `fix/{ticket}-{description}` : Corrections
- `refactor/{description}` : Refactoring sans changement fonctionnel

## Commits conventionnels

Format : `{type}({scope}): {description}`

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `refactor` | Refactoring |
| `docs` | Documentation |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dépendances |

## Règles

- Commits atomiques : une modification logique = un commit
- Messages en anglais (ou français si équipe FR)
- Jamais de `--force` sur les branches partagées
- Rebase interactif avant PR pour nettoyer l'historique
```

#### Quality Standards

```markdown
# Quality Standards

## 🔴 CRITICAL

1. **Tests obligatoires** : Toute nouvelle feature doit avoir des tests
2. **Pas de code commenté** : Supprimer, pas commenter
3. **Pas de secrets hardcodés** : Utiliser les variables d'environnement

## Code Review Checklist

- [ ] Tests passent
- [ ] Pas de régression de couverture
- [ ] Naming clair et cohérent
- [ ] Pas de duplication évitable
- [ ] Documentation mise à jour si API publique
- [ ] Pas de TODO sans ticket associé

## Métriques cibles

| Métrique | Cible |
|----------|-------|
| Couverture tests | > 80% sur les services |
| Complexité cyclomatique | < 10 par méthode |
| Lignes par fichier | < 300 |
| Lignes par méthode | < 30 |
```

---

## Phase 4 : Intégration EPCI

### 4.1 Concept de commande `/epci:rules`

```
Commande : /epci:rules [action] [options]

Actions :
  init      Analyse le projet et génère la structure initiale
  update    Met à jour les rules depuis les patterns EPCI enregistrés
  sync      Synchronise avec les conventions détectées dans le code
  validate  Vérifie la cohérence des rules existantes

Options :
  --stack {symfony|react|django|...}  Force la détection de stack
  --scope {backend|frontend|full}     Limite le scope de génération
  --dry-run                           Affiche sans créer les fichiers
  --force                             Écrase les rules existantes
```

### 4.2 Workflow d'intégration

```
┌─────────────────────────────────────────────────────────────┐
│                    /epci:rules init                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  1. ANALYSE                                                  │
│  ├── Détection stack (composer.json, package.json...)       │
│  ├── Scan structure projet                                   │
│  ├── Extraction conventions existantes                       │
│  └── Lecture patterns EPCI enregistrés                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. GÉNÉRATION                                               │
│  ├── Création .claude/CLAUDE.md (lean)                       │
│  ├── Création .claude/rules/ structure                       │
│  ├── Génération rules par domaine                            │
│  └── Ajout au .gitignore si CLAUDE.local.md                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. VALIDATION                                               │
│  ├── Vérification syntaxe YAML frontmatter                   │
│  ├── Test des patterns de paths                              │
│  └── Rapport de génération                                   │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Exploitation des patterns EPCI

L'idée clé : EPCI trace les décisions prises pendant le développement. Ces traces peuvent alimenter les rules :

```yaml
# Exemple de pattern EPCI enregistré
pattern:
  type: "architecture_decision"
  context: "API endpoint creation"
  decision: "Use DTO for all API responses"
  rationale: "Decouple domain from presentation"
  date: "2025-01-02"
  
# Transformation en rule
rule_generated:
  file: ".claude/rules/backend/api.md"
  section: "🔴 CRITICAL"
  content: "All API responses must use DTOs, never expose entities directly"
```

### 4.4 Fichier de configuration EPCI

```yaml
# .claude/epci-rules.config.yaml

version: "1.0"

# Mapping stack → templates de rules
stack_templates:
  symfony:
    - templates/symfony.md
    - templates/doctrine.md
    - templates/api-platform.md
  react:
    - templates/react.md
    - templates/typescript.md
  django:
    - templates/django.md
    - templates/drf.md

# Patterns à tracker pour génération automatique
track_patterns:
  - type: "naming_convention"
    detect_from: ["class_names", "function_names", "file_names"]
  - type: "architecture_pattern"
    detect_from: ["folder_structure", "import_paths"]
  - type: "error_handling"
    detect_from: ["try_catch_blocks", "custom_exceptions"]

# Exclusions
ignore:
  - "**/vendor/**"
  - "**/node_modules/**"
  - "**/*.min.js"

# Règles custom à toujours inclure
custom_rules:
  - path: "rules/domain/metier.md"
    description: "Règles métier spécifiques"
```

---

## Phase 5 : Maintenance des rules

### 5.1 Commande de mise à jour

```bash
# Après une session de dev, synchroniser les nouvelles conventions détectées
/epci:rules update

# Output attendu :
# ✓ Détecté : nouveau pattern de validation dans UserController
# ✓ Détecté : convention de nommage pour les events
# 
# Propositions de mise à jour :
# 1. [backend/symfony.md] Ajouter : "Events must end with 'Event' suffix"
# 2. [backend/api.md] Ajouter : "Use Assert\Valid for nested validation"
#
# Appliquer ces mises à jour ? (y/n/select)
```

### 5.2 Détection de drift

```bash
# Vérifier si le code actuel respecte les rules
/epci:rules validate

# Output attendu :
# ⚠️  Drift détecté :
# - rules/backend/symfony.md ligne 12 : "Controllers max 20 lignes"
#   → UserController.php:45 a 47 lignes
# - rules/frontend/react.md ligne 8 : "Jamais any"
#   → utils/helpers.ts:12 utilise 'any'
#
# 3 violations trouvées. Corriger ou mettre à jour les rules ?
```

---

## Annexe : Checklist de génération

### Avant de générer

- [ ] Projet initialisé (git, package manager)
- [ ] Au moins quelques fichiers de code existants
- [ ] Fichiers de config présents (composer.json, package.json...)

### Après génération

- [ ] Vérifier le CLAUDE.md principal (< 50 lignes)
- [ ] Tester les paths des rules conditionnelles
- [ ] Valider avec l'équipe avant commit
- [ ] Ajouter `.claude/` au repository (sauf .local.md)

### Maintenance régulière

- [ ] Review mensuelle des rules
- [ ] Mise à jour après changements d'architecture
- [ ] Synchronisation avec les linters/formatters existants
