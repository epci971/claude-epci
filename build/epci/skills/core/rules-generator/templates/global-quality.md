---
# Global rule: empty paths means "apply to all files"
# This rule is always active regardless of file context
paths: []
---

# Quality Standards

> Standards qualite transversaux pour tout le projet.

## 🔴 CRITICAL

1. **Tests obligatoires**: Toute nouvelle feature doit avoir des tests
2. **Pas de code commente**: Supprimer, pas commenter
3. **Pas de secrets hardcodes**: Utiliser les variables d'environnement
4. **Pas de TODO sans ticket**: Chaque TODO doit referencer un ticket

## 🟡 CONVENTIONS

- Coverage minimum: 70% sur le code metier
- Revue de code obligatoire avant merge
- Un commit = une modification logique
- Messages de commit en anglais (ou francais si equipe FR)

## 🟢 PREFERENCES

- Privilegier la lisibilite a la concision
- Documenter le "pourquoi", pas le "quoi"
- Preferer les petites fonctions aux grandes

## Quick Reference

| Metrique | Cible |
|----------|-------|
| Coverage tests | > 70% services |
| Complexite cyclomatique | < 10 par methode |
| Lignes par fichier | < 300 |
| Lignes par methode | < 30 |

## Code Review Checklist

- [ ] Tests passent
- [ ] Pas de regression de couverture
- [ ] Naming clair et coherent
- [ ] Pas de duplication evitable
- [ ] Documentation mise a jour si API publique
- [ ] Pas de TODO sans ticket associe
- [ ] Pas de console.log/print de debug

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Code mort | Confusion, maintenance | Supprimer |
| Magic numbers | Incomprehensible | Constantes nommees |
| God class | SRP viole | Decomposer |
| Deep nesting | Lisibilite | Early return, extraction |
