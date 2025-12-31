# Brief Fonctionnel — Quick EPCT Workflow v2.0

> **Date:** 2025-12-31 | **EMS Final:** 82/100 | **Categorie:** STANDARD

---

## 1. Contexte

La commande `/quick` actuelle gere les taches TINY et SMALL avec un workflow simple mais non optimise. L'objectif est de la transformer en workflow autonome ultra-rapide suivant la logique EPCT (Explore, Plan, Code, Test), avec:

- Switch de modeles adaptatif (Haiku/Sonnet) selon la phase et complexite
- Modes de pensee ("think") adaptes par phase
- Autonomie maximale avec breakpoints minimaux
- Alignement avec les best practices Anthropic (subagents, verification continue)

---

## 2. Exploration Summary

| Aspect | Decouverte |
|--------|------------|
| **Stack** | Claude Code Plugin (Python 3), v4.2.0 |
| **Fichiers principaux** | `src/commands/quick.md`, `src/commands/brief.md`, `src/settings/flags.md` |
| **Patterns existants** | Turbo mode dans `/epci`, model switching via agents, @Explore subagent |
| **Dependances** | project-memory, epci-core, code-conventions, flags-system, stack skills |

---

## 3. Objectifs

### 3.1 Objectifs principaux

1. **Workflow EPCT complet** pour `/quick` avec 4 phases distinctes
2. **Switch de modeles adaptatif** : Haiku pour vitesse, Sonnet pour qualite
3. **Autonomie maximale** : 1 seul breakpoint leger (plan), skip avec `--autonomous`
4. **Subagents strategiques** : @Explore, @clarifier, @planner, @implementer selon complexite
5. **Thinking adaptatif** : activation selon phase et detection d'erreurs

### 3.2 Objectifs secondaires

6. **Decouplage commit** : suppression du breakpoint pre-commit, delegation a future `/commit`
7. **Impact `/brief`** : routing optimise avec skip exploration pour TINY
8. **Session persistence** : `.project-memory/sessions/` pour reset/reprise
9. **Metriques calibration** : collecte temps, modeles, retries pour apprentissage

---

## 4. Specifications fonctionnelles

### 4.1 Workflow EPCT

```
/quick "description" [--autonomous] [--quick-turbo]
    |
    v
[E] EXPLORE (Haiku, ~5-10s)
    - @Explore: scan fichiers, stack, patterns
    - @clarifier: si ambiguite detectee (SMALL only)
    - Guard: complexite > SMALL -> escalade /epci
    |
    v
[P] PLAN (Haiku TINY | Sonnet + "think" SMALL, ~10-15s)
    - Generation 3-5 taches atomiques
    - @planner: si SMALL complexe
    - BP leger (3s auto-continue) [sauf --autonomous]
    - Persistence session JSON
    |
    v
[C] CODE (Sonnet, variable)
    - @implementer: execution taches
    - Micro-validation apres chaque tache
    - Auto-fix lint/format
    - Si erreur: "think" + retry (max 2x)
    |
    v
[T] TEST (Haiku validation | Sonnet + "think" si fix, ~5-10s)
    - Run tests existants
    - Lint/format check
    - Coherence finale
    |
    v
[RESUME FINAL]
    - Fichiers modifies, tests, temps
    - Suggestion: /commit
```

### 4.2 Matrice modeles par phase

| Phase | TINY | SMALL | Erreur/Retry |
|-------|------|-------|--------------|
| Explore | Haiku | Haiku | - |
| Plan | Haiku | Sonnet + "think" | "think hard" |
| Code | Haiku | Sonnet | Sonnet + "think" |
| Test | Haiku | Haiku | Sonnet + "think hard" |

### 4.3 Matrice subagents par complexite

| Phase | TINY | SMALL | SMALL+ (proche limite) |
|-------|------|-------|------------------------|
| Explore | - | @Explore (Haiku) | @Explore + @clarifier |
| Plan | - | - | @planner (Sonnet) |
| Code | - | @implementer | @implementer |
| Test | - | - | - |

### 4.4 Nouveaux flags

| Flag | Effet | Auto-trigger |
|------|-------|--------------|
| `--autonomous` | Skip BP plan, execution continue | TINY detecte |
| `--quick-turbo` | Haiku partout (TINY only) | Jamais (explicit) |
| `--no-bp` | Alias de `--autonomous` | - |

### 4.5 Breakpoint leger (Plan)

```
---------------------------------------------
PLAN: 3 taches | ~45 LOC | 2 fichiers

[1] Ajouter fonction validateInput()
[2] Modifier handleSubmit() pour appeler validation
[3] Ajouter tests unitaires

Auto-continue dans 3s... (Enter=modifier, Esc=annuler)
---------------------------------------------
```

### 4.6 Resume final

```
---------------------------------------------
QUICK COMPLETE

Fichiers modifies: 2
Tests: 3/3 passed
Temps total: 45s

Pour commiter: /commit
Session: .project-memory/sessions/quick-20251231-143022.json
---------------------------------------------
```

---

## 5. Impact sur composants existants

### 5.1 `/brief` — Routing optimise

```
/brief "description"
    |
    v
@Explore (Haiku) — 5s scan
    |
    +-- TINY detecte? -> Skip clarif -> /quick --autonomous
    +-- SMALL detecte? -> 1 question max -> /quick  
    +-- STD+ detecte? -> Flow normal -> /epci
```

### 5.2 `flags-system` — Ajouts

Ajouter dans `src/settings/flags.md`:

```markdown
## Quick Workflow Flags (F13)

| Flag | Effet | Auto-trigger |
|------|-------|--------------|
| `--autonomous` | Skip BP plan, execution continue | TINY detecte |
| `--quick-turbo` | Haiku partout (TINY only) | Jamais |
```

### 5.3 Session persistence

Nouveau fichier: `.project-memory/sessions/quick-{timestamp}.json`

```json
{
  "timestamp": "2025-12-31T14:30:22Z",
  "description": "fix typo in README",
  "complexity": "TINY",
  "plan": [
    {"task": "Fix typo line 42", "status": "completed"}
  ],
  "files_modified": ["README.md"],
  "duration_seconds": 45,
  "models_used": {"explore": "haiku", "plan": "haiku", "code": "haiku"},
  "retries": 0
}
```

---

## 6. Regles metier

### 6.1 Seuils escalation Haiku -> Sonnet

| Critere | Seuil |
|---------|-------|
| LOC estime | > 30 |
| Fichiers | > 1 |
| Imports/deps | > 3 nouveaux |
| Pattern complexe | async, state, API detecte |

### 6.2 Gestion erreurs

1. Erreur detectee -> activation "think"
2. Retry avec meme modele (max 1x)
3. Si echec -> escalade modele (Haiku->Sonnet, Sonnet->Opus)
4. Si echec persistant (2 retries) -> arret + demande intervention

### 6.3 Conflits de flags

| Conflit | Resolution |
|---------|------------|
| `--autonomous` + `--safe` | `--safe` gagne |
| `--quick-turbo` + SMALL detecte | Erreur + suggestion /quick normal |
| `--autonomous` + tests fail | Arret + demande intervention |

### 6.4 Hooks

- Mode `--autonomous`: execution silencieuse des hooks
- Erreur hook = arret workflow
- Flag `--no-hooks` disponible pour skip

---

## 7. Skills charges

| Skill | Phase | Justification |
|-------|-------|---------------|
| `project-memory` | Init | Contexte projet |
| `epci-core` | All | Logique workflow |
| `code-conventions` | Plan, Code | Style code |
| `flags-system` | Init | Gestion flags |
| `[stack]` | Code | Patterns stack (auto-detecte) |
| `testing-strategy` | Test | Si tests existants |

---

## 8. Contraintes

- **Performance:** Workflow TINY < 30s, SMALL < 90s
- **Contexte:** Subagents pour preserver contexte principal
- **Compatibilite:** Flags existants (`--turbo`, `--safe`) respectes
- **Retrocompatibilite:** `/quick` sans flags = comportement actuel + optimisations

---

## 9. Hors scope

- Modification de `/epci` (future iteration)
- Implementation de `/commit` (feature separee)
- Wave orchestration (reserve a LARGE)
- MCP integration specifique (herite de flags existants)

---

## 10. Criteres d'acceptation

1. [ ] `/quick` execute workflow EPCT complet
2. [ ] Switch modeles Haiku/Sonnet fonctionne selon seuils
3. [ ] Breakpoint leger avec auto-continue 3s
4. [ ] Flag `--autonomous` skip breakpoint
5. [ ] Flag `--quick-turbo` force Haiku partout
6. [ ] Subagents invoques selon matrice complexite
7. [ ] Thinking adaptatif active sur erreurs
8. [ ] Session JSON persistee dans .project-memory/
9. [ ] `/brief` route TINY directement vers `/quick --autonomous`
10. [ ] Tests passent, lint OK
11. [ ] Documentation flags mise a jour

---

## 11. Fichiers a modifier

| Fichier | Action | Priorite |
|---------|--------|----------|
| `src/commands/quick.md` | Refonte complete workflow EPCT | P0 |
| `src/commands/brief.md` | Ajout routing optimise TINY/SMALL | P0 |
| `src/settings/flags.md` | Ajout F13 Quick Workflow Flags | P0 |
| `src/agents/implementer.md` | Verifier model: sonnet, micro-validation | P1 |
| `src/agents/planner.md` | Verifier integration /quick | P1 |
| `src/skills/core/project-memory/` | Ajout schema session JSON | P2 |

---

## 12. Estimation

| Aspect | Valeur |
|--------|--------|
| Categorie | STANDARD |
| Fichiers | 6 |
| LOC estime | ~400-500 |
| Risque | Moyen (refonte majeure /quick) |
| Flags suggeres | `--think` |

---

## 13. Prochaine etape

```
/brief avec le contenu de ce brief pour exploration ciblee
-> /epci pour implementation complete
```
