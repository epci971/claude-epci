---
paths: []
---

# Quality Standards

> Standards qualite transversaux pour le plugin EPCI.

## 🔴 CRITICAL

1. **Tests obligatoires**: Toute modification Python doit avoir des tests
2. **Pas de code commente**: Supprimer, pas commenter
3. **Pas de secrets hardcodes**: Utiliser les variables d'environnement
4. **Validation avant commit**: Executer `validate_all.py`

## 🟡 CONVENTIONS

- Coverage minimum: 70% sur le code Python
- Un commit = une modification logique
- Messages de commit en anglais (conventional commits)
- Limites tokens: commands < 5000, skills < 5000, agents < 2000

## 🟢 PREFERENCES

- Privilegier la lisibilite a la concision
- Documenter le "pourquoi", pas le "quoi"
- Preferer les petites fonctions aux grandes

## Quick Reference

| Metrique | Cible |
|----------|-------|
| Coverage tests | > 70% Python |
| Tokens commande | < 5000 |
| Tokens skill | < 5000 |
| Tokens agent | < 2000 |
| Description | <= 1024 chars |

## Code Review Checklist

- [ ] Tests passent (`python src/scripts/validate_all.py`)
- [ ] Naming coherent avec conventions EPCI
- [ ] Pas de duplication evitable
- [ ] Documentation mise a jour si nouvelle commande/skill
- [ ] Pas de print/console.log de debug

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Code mort | Confusion, maintenance | Supprimer |
| Skills trop longs | Depasse tokens | Split en references/ |
| God skill | SRP viole | Decomposer |
| Deep nesting | Lisibilite | Early return |
