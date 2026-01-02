# EPCI Rules Generator Command

> Commande : `/project:epci-rules` ou `/epci:rules`
> Arguments : `$ARGUMENTS` (init|update|validate|sync)

## Mission

Tu es un expert en configuration Claude Code. Ta mission est d'analyser ce projet et de générer une structure `.claude/rules/` optimisée selon les meilleures pratiques.

## Étape 1 : Détection de la stack

Analyse ces fichiers pour identifier la stack :

```
composer.json → Symfony, Laravel, PHP
package.json → React, Vue, Node, TypeScript
requirements.txt / pyproject.toml → Django, FastAPI, Python
docker-compose.yml → Services infrastructure
.env.example → Variables d'environnement
```

**Action** : Liste la stack détectée avec les versions.

## Étape 2 : Analyse de l'architecture

Examine la structure du projet :

1. **Organisation des dossiers** : src/, app/, lib/, tests/, assets/
2. **Patterns de nommage** : fichiers, classes, fonctions
3. **Architecture** : MVC, Hexagonal, DDD, Clean Architecture
4. **Séparation concerns** : monorepo, backend/frontend séparés

**Action** : Décris l'architecture détectée.

## Étape 3 : Extraction des conventions existantes

Analyse le code pour détecter :

- Conventions de nommage utilisées
- Patterns récurrents (DI, repositories, DTOs...)
- Style de tests
- Gestion d'erreurs
- Documentation (docblocks, comments)

**Action** : Liste les conventions détectées.

## Étape 4 : Génération des rules

### Structure à créer

```
.claude/
├── CLAUDE.md                    # < 50 lignes, essentiels uniquement
└── rules/
    ├── _global/
    │   ├── quality.md           # Standards qualité
    │   ├── git-workflow.md      # Conventions git
    │   └── commands.md          # Commandes fréquentes
    ├── backend/
    │   └── {framework}.md       # Rules backend avec paths
    ├── frontend/
    │   └── {framework}.md       # Rules frontend avec paths
    ├── testing/
    │   └── {framework}.md       # Rules tests avec paths
    └── domain/
        └── glossary.md          # Termes métier
```

### Format des fichiers rules

```markdown
---
paths:
  - pattern/matching/**/*.ext
---

# {Nom Rule}

## 🔴 CRITICAL
1. Règle absolue

## 🟡 CONVENTIONS
- Convention standard

## 🟢 PRÉFÉRENCES
- Préférence optionnelle

## Patterns
| Besoin | Solution |
|--------|----------|
| Cas | Pattern |
```

## Étape 5 : Création des fichiers

**Action** : Crée les fichiers suivants :

1. `.claude/CLAUDE.md` — Version lean avec :
   - Nom du projet
   - Commandes essentielles (dev, test, lint)
   - Stack résumée
   - Pointeur vers rules/

2. `.claude/rules/_global/quality.md` — Standards qualité

3. `.claude/rules/_global/git-workflow.md` — Conventions git

4. `.claude/rules/backend/{framework}.md` — Rules backend avec paths appropriés

5. `.claude/rules/frontend/{framework}.md` — Rules frontend (si applicable)

6. `.claude/rules/testing/{test-framework}.md` — Rules tests

## Règles de génération

### CLAUDE.md principal

- Maximum 50 lignes
- Uniquement les commandes les plus utilisées
- Pas de détails, juste des pointeurs vers rules/

### Fichiers rules

- Toujours un frontmatter `paths:` sauf pour _global/
- Utiliser la graduation 🔴/🟡/🟢
- Inclure des exemples de code quand pertinent
- Maximum 100 lignes par fichier rule

### Paths patterns

```yaml
# Backend PHP/Symfony
paths:
  - src/**/*.php
  - config/**/*.yaml

# Frontend React/TS
paths:
  - src/**/*.tsx
  - src/**/*.ts
  - "!src/**/*.test.ts"

# Tests
paths:
  - tests/**/*.php
  - "**/*.test.ts"
```

## Actions selon $ARGUMENTS

### `init` (défaut)
- Analyse complète du projet
- Génère toute la structure
- Affiche un rapport de ce qui a été créé

### `update`
- Analyse les nouveaux patterns dans le code
- Propose des ajouts aux rules existantes
- Demande confirmation avant modification

### `validate`
- Compare le code aux rules existantes
- Liste les violations (drift)
- Propose des corrections

### `sync`
- Synchronise les rules avec les linters existants
- Importe les règles de .eslintrc, phpstan.neon, etc.

## Output attendu

```
📁 Structure générée :

.claude/
├── CLAUDE.md (42 lignes)
└── rules/
    ├── _global/
    │   ├── quality.md ✓
    │   └── git-workflow.md ✓
    ├── backend/
    │   └── symfony.md ✓ (paths: src/**/*.php)
    ├── frontend/
    │   └── react.md ✓ (paths: assets/**/*.tsx)
    └── testing/
        └── phpunit.md ✓ (paths: tests/**/*.php)

✅ 6 fichiers créés
📊 Stack détectée : Symfony 7.2 + React 19 + PostgreSQL 16
🎯 Prochaine étape : Revue des rules générées avec l'équipe
```

## Notes

- Ne pas écraser les rules existantes sans confirmation
- Toujours proposer avant de modifier
- Garder les rules concises et actionnables
- Privilégier les exemples de code aux longues explications
