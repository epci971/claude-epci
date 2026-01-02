---
# Global rule: empty paths means "apply to all files"
# This rule is always active regardless of file context
paths: []
---

# Git Workflow

> Conventions Git pour le projet.

## 🔴 CRITICAL

1. **Jamais de force push sur main/master**: Proteger les branches principales
2. **Jamais de secrets dans l'historique**: Utiliser git-secrets ou pre-commit
3. **Jamais de merge sans review**: Au moins 1 approbation requise

## 🟡 CONVENTIONS

### Branches

| Type | Format | Exemple |
|------|--------|---------|
| Feature | `feature/{ticket}-{description}` | `feature/PROJ-123-user-auth` |
| Fix | `fix/{ticket}-{description}` | `fix/PROJ-456-login-error` |
| Refactor | `refactor/{description}` | `refactor/extract-auth-service` |
| Hotfix | `hotfix/{ticket}-{description}` | `hotfix/PROJ-789-security-patch` |

### Commits Conventionnels

Format: `{type}({scope}): {description}`

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalite |
| `fix` | Correction de bug |
| `refactor` | Refactoring sans changement fonctionnel |
| `docs` | Documentation |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dependances |
| `perf` | Amelioration performance |
| `style` | Formatting, pas de changement de code |

### Exemples

```bash
# Correct
feat(auth): add JWT token refresh endpoint
fix(api): handle null response in user service
refactor(orders): extract payment validation logic
docs(readme): update installation instructions

# Incorrect
fixed stuff
WIP
update
```

## 🟢 PREFERENCES

- Commits atomiques: une modification logique = un commit
- Rebase interactif avant PR pour nettoyer l'historique
- Squash des commits WIP avant merge

## Quick Reference

| Action | Commande |
|--------|----------|
| Nouvelle feature | `git checkout -b feature/TICKET-desc` |
| Commit | `git commit -m "type(scope): description"` |
| Sync avec main | `git fetch origin && git rebase origin/main` |
| Push | `git push -u origin HEAD` |
| PR | `gh pr create --fill` |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| `git add .` aveugle | Commits non atomiques | `git add -p` |
| Messages vagues | Historique inutile | Commits conventionnels |
| Branches longues | Conflits, drift | PRs frequentes |
| Force push partage | Perte de travail | Communication equipe |
