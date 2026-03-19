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

## Circuit Breaker (Component Failure Protection)

Track component failures during step-03-code to detect cascading problems.

### Tracking

```
consecutive_failures = 0  # Reset on each SUCCESS
total_failed = 0
total_attempted = 0
```

### Thresholds

| Condition | Threshold | Action (interactive) |
|-----------|-----------|---------------------|
| Consecutive failures | >= 3 | Diagnostic breakpoint — user decides: continue, investigate (/debug), or abandon |
| Failure rate | > 50% (after >= 4 attempts) | Diagnostic breakpoint — same options |

### Dependency Skip Logic

When component A fails, all components depending on A are SKIPPED:

```
FOR each component B where A in B.depends_on:
  Mark B as SKIPPED
  Log: "Skipped {B}: depends on failed {A}"
```

### Differences with implement-auto

In interactive mode, the circuit breaker presents a diagnostic breakpoint (not an automatic abort).
In headless mode (implement-auto), the circuit breaker triggers an automatic ABORT.
