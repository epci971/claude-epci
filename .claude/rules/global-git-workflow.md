---
paths: []
---

# Git Workflow

> Conventions Git pour le plugin EPCI.

## 🔴 CRITICAL

1. **Jamais de force push sur master**: Proteger la branche principale
2. **Jamais de secrets dans l'historique**: Utiliser .env
3. **Validation avant commit**: `python src/scripts/validate_all.py`

## 🟡 CONVENTIONS

### Branches

| Type | Format | Exemple |
|------|--------|---------|
| Feature | `feature/{description}` | `feature/add-rules-command` |
| Fix | `fix/{description}` | `fix/validation-error` |
| Refactor | `refactor/{description}` | `refactor/skill-structure` |

### Commits Conventionnels

Format: `{type}({scope}): {description}`

| Type | Usage |
|------|-------|
| `feat` | Nouveau skill, agent |
| `fix` | Correction de bug |
| `refactor` | Refactoring sans changement fonctionnel |
| `docs` | Documentation |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dependances |

### Scopes EPCI

| Scope | Usage | Fichiers concernés |
|-------|-------|-------------------|
| `(skills)` | Modification de skills | `src/skills/**` |
| `(agents)` | Modification de subagents | `src/agents/**` |
| `(infra)` | Scripts, worktree, CI | `src/scripts/**`, `.github/**` |
| `(ralph)` | Système Ralph Wiggum | `ralph.sh`, `/ralph-exec` |
| `(decompose)` | Décomposition PRD | `/decompose`, `prd.json` |
| `(hooks)` | Système hooks | `src/hooks/**` |
| `(mcp)` | Intégration MCP | `src/mcp/**` |
| `(validation)` | Scripts validation | `validate_*.py` |
| `(memory)` | Project memory | `src/project-memory/**` |

### Exemples

```bash
# Correct
feat(skills): add rules-generator skill for project conventions
fix(validation): handle missing frontmatter in skills
refactor(orchestration): extract wave planner logic
docs(readme): update installation instructions

# Incorrect
fixed stuff
WIP
update
```

## 🟢 PREFERENCES

- Commits atomiques: une modification logique = un commit
- Squash des commits WIP avant merge

## Quick Reference

| Action | Commande |
|--------|----------|
| Nouvelle feature | `git checkout -b feature/desc` |
| Commit | `git commit -m "type(scope): description"` |
| Sync avec master | `git fetch origin && git rebase origin/master` |
| Push | `git push -u origin HEAD` |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| `git add .` aveugle | Commits non atomiques | `git add -p` |
| Messages vagues | Historique inutile | Commits conventionnels |
| Branches longues | Conflits, drift | PRs frequentes |
