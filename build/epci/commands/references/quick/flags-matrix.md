# Flags et Matrices — Detail

> Reference pour `/quick` — Flags, modeles, subagents

---

## Interactions de Flags

| Combinaison | Comportement |
|-------------|--------------|
| `--autonomous` seul | Ignorer BP plan, execution continue |
| `--quick-turbo` seul | Haiku partout (TINY uniquement, erreur si SMALL) |
| `--autonomous --quick-turbo` | Ignorer BP + Haiku partout |
| `--turbo --autonomous` | `--turbo` a la priorite (workflow turbo existant) |
| `--safe --autonomous` | `--safe` gagne, breakpoints maintenus |

---

## Matrice des Modeles (Switching Adaptatif)

| Phase | TINY | SMALL | En Cas d'Erreur/Reessai |
|-------|------|-------|-------------------------|
| **[E] Explore** | Haiku | Haiku | - |
| **[P] Plan** | Haiku | Sonnet + `think` | `think hard` |
| **[C] Code** | Haiku | Sonnet | Sonnet + `think` |
| **[T] Test** | Haiku | Haiku | Sonnet + `think hard` |

### Regles de Selection Modele

- TINY: Toujours utiliser Haiku pour vitesse maximale
- SMALL: Utiliser Sonnet pour phases Plan/Code (qualite importante)
- Erreur/Reessai: Escalader le mode thinking pour resolution de probleme
- `--quick-turbo`: Forcer Haiku partout (TINY uniquement)

### Seuils d'Escalade (Haiku → Sonnet)

| Critere | Seuil |
|---------|-------|
| LOC estime | > 30 |
| Fichiers | > 1 |
| Nouveaux imports/deps | > 3 |
| Patterns complexes | async, state, API detectes |

---

## Matrice des Subagents (Par Complexite)

| Phase | TINY | SMALL | SMALL+ (proche limite) |
|-------|------|-------|------------------------|
| **[E] Explore** | - | @Explore (Haiku) | @Explore + @clarifier |
| **[P] Plan** | - | - | @planner (Sonnet) |
| **[C] Code** | - | @implementer | @implementer |
| **[T] Test** | - | - | - |

### Invocation Subagent

```
Invoquer via Task tool avec model: {modele_specifie}
Exemples:
- Task tool avec subagent_type="Explore", model="haiku"
- Task tool avec subagent_type="epci:planner", model="sonnet"
- Task tool avec subagent_type="epci:implementer", model="sonnet"
```

---

## Flags MCP (F12 — Leger)

Pour features SMALL uniquement:

| Flag | Effet | Note |
|------|-------|------|
| `--c7` | Context7 pour lookup doc rapide | Recommande pour SMALL |
| `--no-mcp` | Desactiver tous les serveurs MCP | Defaut pour TINY |

**Note:** Sequential, Magic et Playwright ne sont pas recommandes pour TINY/SMALL.

---

## Mode --turbo (Legacy)

**⚠️ OBLIGATOIRE: QUAND le flag `--turbo` est actif, utiliser le workflow turbo existant:**

1. **Utiliser l'agent @implementer** (modele Sonnet) pour features SMALL
2. **Ignorer la revue optionnelle** — Pas de @code-reviewer
3. **Auto-commit** — Ignorer le breakpoint pre-commit
4. **Sortie compacte** — Resume uniquement

**Note:** `--turbo` et `--autonomous` sont differents:
- `--turbo`: Utilise l'infrastructure turbo existante, auto-commit
- `--autonomous`: Utilise le nouveau workflow EPCT, ignore BP plan uniquement

---

*Reference Flags Matrix — /quick command*
