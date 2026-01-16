---
description: >-
  Execute autonomous EPCT workflow for TINY and SMALL features. Four phases:
  Explore, Plan, Code, Test with adaptive model switching (Haiku/Sonnet).
  TINY mode: <50 LOC, 1 file. SMALL mode: <200 LOC, 2-3 files.
argument-hint: "[--confirm] [--quick-turbo] [--uc] [--turbo] [--no-hooks]"
allowed-tools: [Read, Write, Edit, Bash(npm:*), Bash(pytest:*), Bash(php:*), Bash(eslint:*), Bash(flake8:*), Bash(git:*), Grep, Glob, Task]
---

# EPCI Quick — EPCT Workflow

## Overview

Workflow autonome suivant la logique EPCT (Explore, Plan, Code, Test) pour features TINY et SMALL.
Optimise pour la vitesse avec switching de modele adaptatif et breakpoints minimaux.

**Caracteristiques cles:**
- Structure 4 phases EPCT
- Switching de modele adaptatif (Haiku pour vitesse, Sonnet pour qualite)
- Breakpoint leger avec auto-continue 3s
- Persistence de session pour reprise/suivi

---

## Modes

### Mode TINY

| Critere | Valeur |
|---------|--------|
| Fichiers | 1 seul |
| LOC | < 50 |
| Tests | Non requis |
| Duree | < 30 secondes cible |
| Exemples | Typo, config, petite correction |

### Mode SMALL

| Critere | Valeur |
|---------|--------|
| Fichiers | 2-3 |
| LOC | < 200 |
| Tests | Optionnels |
| Duree | < 90 secondes cible |
| Exemples | Petite feature, refactor local |

---

## Flags Supportes

### Flags Specifiques Quick (F13)

| Flag | Effet | Auto-Declenchement |
|------|-------|-------------------|
| `--confirm` | Activer breakpoint plan avec attente utilisateur | Jamais (explicite) |
| `--quick-turbo` | Forcer modele Haiku partout (TINY uniquement) | Jamais (explicite) |
| `--bp` | Alias pour `--confirm` | - (alias) |

### Flags Herites

| Flag | Effet | Auto-Declenchement |
|------|-------|-------------------|
| `--uc` | Sortie compressee | contexte > 75% |
| `--turbo` | Mode turbo existant (@implementer, auto-commit) | Jamais |
| `--no-hooks` | Desactiver execution de tous les hooks | Jamais |
| `--safe` | Forcer breakpoints meme avec `--autonomous` | Fichiers sensibles |

**Note:** Les flags thinking (`--think-hard`, `--ultrathink`) declenchent une escalade vers `/epci`.

> Voir @references/quick/flags-matrix.md pour les interactions de flags et matrices completes.

---

## Configuration

| Element | Valeur |
|---------|--------|
| **Thinking** | Adaptatif par phase (voir matrice modeles) |
| **Skills** | project-memory, epci-core, code-conventions, flags-system, breakpoint-display, [stack] |
| **Subagents** | @Explore, @clarifier, @planner, @implementer (conditionnel) |

> Voir @references/quick/flags-matrix.md pour les matrices modeles et subagents.

---

## EPCT Workflow

**⚠️ IMPORTANT: Suivre TOUTES les phases en sequence.**

```
/quick "description" [--autonomous] [--quick-turbo]
    │
    ▼
[E] EXPLORE ──────────────────────────────────────────────────────────
    │
    ▼
[P] PLAN ─────────────────────────────────────────────────────────────
    │                         ⏸️ BP leger (SI --confirm)
    ▼
[C] CODE ─────────────────────────────────────────────────────────────
    │
    ▼
[T] TEST ─────────────────────────────────────────────────────────────
    │
    ▼
[RESUME FINAL] ───────────────────────────────────────────────────────
```

### [E] EXPLORE Phase (5-10s)

**Modele:** Haiku (TINY et SMALL)

Collecte rapide du contexte et verification de la complexite.

- SI brief absent → Suggerer `/brief` d'abord
- SI complexite > SMALL → Escalader vers `/epci`

### [P] PLAN Phase (10-15s)

**Modele:** Haiku (TINY) | Sonnet + `think` (SMALL)

Generation du decoupage atomique des taches.

- TINY: 1-2 taches maximum (inline, sans subagent)
- SMALL: 3-5 taches atomiques
- SMALL+ (proche limite): Invoquer @planner (Sonnet) via Task tool

**⏸️ Breakpoint leger** (SI `--confirm`): via `@skill:breakpoint-display type:lightweight`

```yaml
@skill:breakpoint-display
  type: lightweight
  title: "QUICK PLAN"
  data:
    mode: "{TINY|SMALL}"
    tasks:
      - {id: 1, description: "{task 1}"}
      - {id: 2, description: "{task 2}"}
      - {id: 3, description: "{task 3}"}
    auto_continue: 3  # seconds
  ask:  # Only if --confirm flag
    question: "Plan OK ?"
    header: "⏸️ Plan"
    options:
      - {label: "Continuer (Recommended)", description: "Auto-continue dans 3s..."}
      - {label: "Modifier", description: "Ajuster le plan"}
      - {label: "Annuler", description: "Abandonner"}
```

### [C] CODE Phase (variable)

**Modele:** Haiku (TINY) | Sonnet (SMALL)

Execution des taches d'implementation.

- TINY: Implementation directe
- SMALL: Invoquer @implementer (Sonnet)
- SI erreur: Reessayer (max 2x), PUIS escalader modele

### [T] TEST Phase (5-10s)

**Modele:** Haiku (validation) | Sonnet + `think hard` (SI correction necessaire)

Verification de la correction de l'implementation.

- Executer tests existants
- Verification lint/format
- SI echec tests: Tenter auto-correction

> Voir @references/quick/epct-workflow.md pour le detail complet de chaque phase.

---

## Resume Final (MANDATORY)

**⚠️ OBLIGATOIRE:** Toujours afficher le message de completion et executer le hook memoire.

> Voir @references/quick/resume-completion.md pour les formats de sortie et hooks.

---

## Gestion des Erreurs

### Strategie de Reessai

| Situation | Action |
|-----------|--------|
| Erreur detectee | Activer mode `think` |
| 1er reessai echoue | Escalader modele (Haiku→Sonnet) |
| 2eme reessai echoue | Arreter, demander intervention |
| Tests echouent | Activer `think hard`, tenter auto-correction |
| Tests echouent encore | Rapporter echec, arreter |

### Escalade vers /epci

Escalader SI pendant l'implementation vous decouvrez:
- Plus de 3 fichiers impactes
- Risque de regression identifie
- Complexite sous-estimee
- Tests d'integration necessaires
- Changements sensibles securite

```
⚠️ **ESCALADE RECOMMANDEE**

La modification est plus complexe qu'anticipee:
- [Raison 1]
- [Raison 2]

Recommandation: Basculer vers `/epci` pour workflow structure.
```

---

## Comparaison avec /epci

| Aspect | /quick | /epci |
|--------|--------|-------|
| Workflow | EPCT (4 phases) | 3 phases |
| Feature Document | Non | Oui |
| Breakpoints | 1 leger (3s) | 3 complets |
| Switching modele | Adaptatif Haiku/Sonnet | Base sur flags |
| @plan-validator | Non | Oui |
| @code-reviewer | Non | Complet |
| @security-auditor | Non | Conditionnel |
| Persistence session | Oui (.project-memory/sessions/) | Via hooks |
| Duree cible | <30s TINY, <90s SMALL | Variable |

---

## Exemples

### Exemple TINY

**Brief:** "Corriger typo 'recieve' vers 'receive' dans UserService"

```
[E] Explore: UserService.php identifie, TINY confirme
[P] Plan: 1 tache — Remplacer typo ligne 42
    (--autonomous: BP ignore)
[C] Code: Edit applique, syntaxe OK
[T] Test: Tests existants passent

✅ QUICK COMPLETE — TINY
Fichier: src/Service/UserService.php
Temps: 12s
```

### Exemple SMALL

**Brief:** "Ajouter methode isActive() a l'entite User"

```
[E] Explore: 2 fichiers identifies, SMALL confirme
    @Explore (Haiku): patterns detectes
[P] Plan: 3 taches generees
    @skill:breakpoint-display type:lightweight
    Tasks: [1] Ecrire test, [2] Implementer, [3] Verifier
    (Auto-continue dans 3s si --confirm)
[C] Code: @implementer (Sonnet) execute
[T] Test: 3/3 tests reussis

✅ QUICK COMPLETE — SMALL
Fichiers: User.php (+15/-0), UserTest.php (+22/-0)
Temps: 67s
```

---

## References

| Materiel | Emplacement |
|----------|-------------|
| Workflow EPCT detaille | @references/quick/epct-workflow.md |
| Resume et completion | @references/quick/resume-completion.md |
| Flags et matrices | @references/quick/flags-matrix.md |
