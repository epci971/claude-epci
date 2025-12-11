---
name: git-workflow
description: >-
  Workflow Git et conventions de commit. Branching strategy, Conventional
  Commits, PR workflow. Use when: Phase 3 finalisation, commit, préparation PR.
  Not for: commandes git basiques.
---

# Git Workflow

## Overview

Workflow Git standardisé pour une collaboration efficace.

## Branching Strategy

```
main ─────────────────────────────────────────►
        │                           │
develop ├───────────────────────────┼─────────►
        │           │               │
feature/x ──────────┘               │
                                    │
feature/y ──────────────────────────┘
```

### Types de branches

| Type | Convention | Base | Merge vers |
|------|------------|------|------------|
| main | `main` | - | - |
| develop | `develop` | main | main |
| feature | `feature/nom-court` | develop | develop |
| bugfix | `bugfix/nom-court` | develop | develop |
| hotfix | `hotfix/nom-court` | main | main + develop |
| release | `release/vX.Y.Z` | develop | main + develop |

### Nommage des branches

```
feature/add-user-authentication
bugfix/fix-login-redirect
hotfix/security-patch-xss
release/v2.1.0
```

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[body]

[footer]
```

### Types

| Type | Usage | Exemple |
|------|-------|---------|
| `feat` | Nouvelle fonctionnalité | `feat(auth): add JWT refresh` |
| `fix` | Correction de bug | `fix(api): handle null response` |
| `docs` | Documentation | `docs(readme): add install guide` |
| `style` | Formatage (pas de code) | `style: fix indentation` |
| `refactor` | Refactoring | `refactor(user): extract validator` |
| `test` | Tests | `test(auth): add login tests` |
| `chore` | Maintenance | `chore(deps): update lodash` |
| `perf` | Performance | `perf(query): optimize user fetch` |
| `ci` | CI/CD | `ci: add github actions` |

### Règles

1. **Type obligatoire** — Toujours commencer par le type
2. **Scope optionnel** — Contexte entre parenthèses
3. **Description impérative** — "add" pas "added"
4. **Ligne < 72 chars** — Pour la lisibilité
5. **Body optionnel** — Détails si nécessaire
6. **Footer pour refs** — `Closes #123`, `BREAKING CHANGE:`

### Exemples

```
feat(auth): add JWT token refresh

- Implement token refresh endpoint
- Add refresh token to login response
- Update auth middleware

Closes #123
```

```
fix(api): handle null response from external service

The external API sometimes returns null instead of an empty
array. This caused a TypeError in the mapping function.

Fixes #456
```

```
feat(user)!: change email validation rules

BREAKING CHANGE: Email addresses must now include a TLD.
Previously accepted emails like "user@localhost" are no longer valid.
```

## PR Workflow

### Avant de créer la PR

- [ ] Rebase sur develop récent
- [ ] Tous les tests passent
- [ ] Lint clean (pas d'erreurs)
- [ ] Commits squashés si nécessaire
- [ ] Feature Document à jour (STANDARD/LARGE)

### Template PR

```markdown
## Description
[Résumé des changements en 2-3 phrases]

## Type de changement
- [ ] Bug fix (non-breaking)
- [ ] Nouvelle feature (non-breaking)
- [ ] Breaking change
- [ ] Refactoring (pas de changement fonctionnel)

## Tests
- [ ] Tests unitaires ajoutés/modifiés
- [ ] Tests d'intégration ajoutés/modifiés
- [ ] Tests manuels effectués

## Checklist
- [ ] Code auto-reviewé
- [ ] Documentation mise à jour
- [ ] Pas de console.log/var_dump
- [ ] Feature Document complété (si applicable)

## Screenshots (si UI)
[Avant/Après si applicable]

## Liens
- Feature Document: docs/features/xxx.md
- Issue: #123
```

### Review Workflow

```
1. Créer PR → Draft si WIP
2. Auto-assign reviewers
3. CI/CD checks passent
4. Review par pairs
5. Résoudre commentaires
6. Approval (min 1)
7. Squash & Merge
```

## Commandes utiles

### Workflow quotidien

```bash
# Nouvelle feature
git checkout develop
git pull
git checkout -b feature/ma-feature

# Commit
git add .
git commit -m "feat(scope): description"

# Push et PR
git push -u origin feature/ma-feature
```

### Maintenance

```bash
# Rebase sur develop
git fetch origin
git rebase origin/develop

# Squash commits
git rebase -i HEAD~3

# Amend dernier commit
git commit --amend
```

## Git Hooks recommandés

| Hook | Action |
|------|--------|
| pre-commit | Lint, format |
| commit-msg | Valide Conventional Commit |
| pre-push | Tests unitaires |

## Checklist Phase 3 EPCI

- [ ] Commits suivent Conventional Commits
- [ ] Branche nommée correctement
- [ ] Rebase sur develop récent
- [ ] PR template complété
- [ ] Feature Document finalisé
- [ ] CI/CD passe
