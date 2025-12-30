# Journal d'Exploration — Optimisation Workflow EPCI (Turbo Mode)

> **Feature**: Optimisation Workflow EPCI
> **Date**: 2025-12-30
> **Iterations**: 3
> **EMS Final**: 82/100

---

## Resume

Exploration pour réduire le temps du workflow EPCI de ~30 min à ~15-18 min.
Solution retenue : modèles adaptatifs (Haiku/Sonnet/Opus) + nouveaux agents + parallélisation + flag --turbo.

---

## Progression EMS

| Iteration | Score | Delta | Focus |
|-----------|-------|-------|-------|
| Init | 25 | - | Problème identifié |
| 1 | 25 | +0 | Questions HMW, analyse temps |
| 2 | 58 | +33 | Décisions architecture, solutions proposées |
| 3 | 78 | +20 | Validation stratégie modèles + agents |
| Final | 82 | +4 | Recherche technique, finalisation specs |

---

## Decisions Cles

### Decision 1 — Garder les 3 commandes existantes

- **Contexte**: Option de fusionner brainstorm + brief en /epci-start
- **Options considerees**:
  - A) Fusionner en /epci-start
  - B) Garder séparés avec optimisations
- **Choix**: Option B
- **Justification**: Flexibilité préservée, l'utilisateur ne passe pas toujours par brainstorm

### Decision 2 — Modèles par phase

- **Contexte**: Quel modèle pour quelle tâche ?
- **Options considerees**:
  - A) Tout Opus (actuel)
  - B) Tout Sonnet
  - C) Adaptatif (Haiku/Sonnet/Opus selon tâche)
- **Choix**: Option C
- **Justification**: Optimise temps sans sacrifier qualité sur les validations critiques

### Decision 3 — Flag --turbo suggéré automatiquement

- **Contexte**: Comment activer les optimisations ?
- **Options considerees**:
  - A) --turbo explicite uniquement
  - B) --turbo par défaut
  - C) --turbo suggéré si project-memory existe
- **Choix**: Option C
- **Justification**: Guide l'utilisateur sans forcer, permet opt-out facile

### Decision 4 — 3 nouveaux agents

- **Contexte**: Quels agents créer ?
- **Options considerees**:
  - A) Aucun nouveau (modifier existants)
  - B) @clarifier seulement
  - C) @clarifier + @planner + @implementer
- **Choix**: Option C
- **Justification**: Séparation claire des responsabilités, modèles optimisés par rôle

### Decision 5 — Reviews en parallèle

- **Contexte**: Comment accélérer Phase 2 ?
- **Options considerees**:
  - A) Séquentiel (actuel)
  - B) Parallèle total
  - C) Parallèle conditionnel (--turbo only)
- **Choix**: Option C
- **Justification**: Préserve comportement standard, optimise en mode turbo

---

## Recherche technique

### Verification: Modèles dans agents Claude Code

**Question**: Les Task tools peuvent-ils utiliser différents modèles ?

**Résultat**: OUI, confirmé via documentation officielle.

**Syntaxe**:
```yaml
---
name: agent-name
model: haiku  # ou sonnet, opus, inherit
---
```

**Options disponibles**:
- `haiku` : Claude Haiku 4.5 (rapide, léger)
- `sonnet` : Claude Sonnet 4.5 (équilibré)
- `opus` : Claude Opus 4.5 (puissant)
- `inherit` : Même modèle que conversation principale

**Source**: Claude Code Subagents Documentation

---

## Questions Resolues

| Question | Reponse | Iteration |
|----------|---------|-----------|
| Peut-on utiliser Haiku pour agents ? | Oui, paramètre `model: haiku` | 3 |
| Combien de temps gaspillé ? | ~13 min sur 30 (43%) | 1 |
| Quelles reviews paralléliser ? | @code-reviewer + @qa-reviewer + @security-auditor | 2 |
| Auto-accept comment ? | EMS > 60 ou confiance > 0.7 | 2 |
| Garder qualité validations ? | Opus obligatoire pour @plan-validator, @code-reviewer | 2 |

---

## Architecture retenue

### Mapping Modèle × Agent

```
HAIKU (rapide, exploration)
├── @Explore (natif)
└── @clarifier (nouveau)

SONNET (équilibré, implémentation)
├── @planner (nouveau)
├── @implementer (nouveau)
├── @qa-reviewer (modifié)
└── @doc-generator (modifié)

OPUS (puissant, validation critique)
├── @plan-validator (modifié)
├── @code-reviewer (modifié)
├── @security-auditor (modifié)
└── @decompose-validator (modifié)
```

### Flow optimisé (/epci --turbo)

```
Phase 1 (Plan)
├── @Explore (Haiku) → Analyse rapide
├── @planner (Sonnet) → Génère plan
└── @plan-validator (Opus) → Valide plan
    │
    ▼ BREAKPOINT (unique)
    │
Phase 2 (Code)
├── @implementer (Sonnet) → Implémente
└── Reviews PARALLÈLES:
    ├── @code-reviewer (Opus)
    ├── @qa-reviewer (Sonnet)
    └── @security-auditor (Opus, si fichiers sensibles)
    │
Phase 3 (Finalize)
└── @doc-generator (Sonnet) → Documentation
```

---

## Estimations de gain

| Optimisation | Gain estimé |
|--------------|-------------|
| Haiku pour exploration | -3 min |
| Haiku pour clarifications | -2 min |
| Sonnet pour plan (vs Opus) | -2 min |
| Reviews parallèles | -3-4 min |
| Auto-accept suggestions | -2 min |
| **Total** | **~12-14 min** |

**Temps final estimé**: ~15-18 min (vs 30 min actuel)

---

## Risques identifies

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Haiku manque des fichiers | Moyenne | Moyen | Fallback Opus si incomplet |
| Coût API plus élevé (parallèle) | Haute | Faible | Acceptable pour gain temps |
| Breakpoint unique insuffisant | Faible | Moyen | Option --safe pour 2 breakpoints |

---

## Prochaines etapes

1. Lancer `/epci-brief` avec le brief généré
2. Créer les 3 nouveaux agents
3. Modifier les 6 agents existants
4. Modifier les 5 commandes
5. Tester workflow complet avec --turbo
6. Mesurer temps réel et ajuster si nécessaire

---

*Journal genere par Brainstormer v3.0*
