# TDD Rules

> Ce contenu est centralisé dans le core skill `tdd-enforcer`.

## Référence

Voir: `src/skills/core/tdd-enforcer/references/`
- `workflow-red-green-refactor.md` — Cycle TDD complet (RED-GREEN-REFACTOR-VERIFY)
- `coverage-rules.md` — Règles de couverture par complexité

## Quick Reference

Le skill `/implement` utilise automatiquement `tdd-enforcer` en mode `guided`.

### Cycle TDD

```
RED → GREEN → REFACTOR → VERIFY
```

### Coverage par Complexité

| Complexité | Line | Branch | Mode |
|------------|------|--------|------|
| TINY | - | - | optional |
| SMALL | 50% | 40% | guided |
| STANDARD | 70% | 60% | guided |
| LARGE | 80% | 70% | strict |
