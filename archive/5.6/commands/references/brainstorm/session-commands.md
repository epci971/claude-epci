# Brainstorm Session Commands Reference

> Reference pour les commandes de session dans `/brainstorm`.
> Gestion de la persistence: save, back.

---

## Commande `save`

Sauvegarde explicite de la session en cours.

```
> save

-------------------------------------------------------
Session sauvegardee
   Fichier: .project-memory/brainstorm-sessions/feature-auth.yaml
   EMS: 52/100 | Phase: Divergent | Iteration: 3

   Pour reprendre: /brainstorm feature-auth
-------------------------------------------------------
```

**Auto-save**: La session est aussi sauvegardee automatiquement:
- A chaque changement de phase
- Avant `finish`
- Apres chaque energy check

## Commande `back`

Revient a une iteration precedente (1 a 5 steps).

**Syntaxe**: `back [n]` ou n = 1-5 (defaut: 1)

### Exemples

```
> back

-------------------------------------------------------
Retour de 1 iteration
   Iteration: 3 → 2
   EMS: 52/100 → 38/100 (-14)
   Phase: Divergent

   Questions restaurees:
   - Comment gerer les sessions longues?
   - Quelle strategie de refresh token?
-------------------------------------------------------
```

```
> back 3

-------------------------------------------------------
Retour de 3 iterations
   Iteration: 5 → 2
   EMS: 68/100 → 38/100 (-30)
   Phase: transition → divergent

   Questions restaurees:
   - Comment gerer les sessions longues?
   - Quelle strategie de refresh token?
-------------------------------------------------------
```

### Regles

| Regle | Description |
|-------|-------------|
| Max steps | 5 iterations maximum par commande |
| Min iteration | Impossible d'aller en dessous de iteration 1 |
| Preservation | L'historique est conserve (peut revenir en avant avec `continue`) |
| Validation | Si n > iteration actuelle, erreur affichee |

### Erreur possible

```
> back 10

-------------------------------------------------------
Erreur: Impossible de revenir de 10 iterations
   Iteration actuelle: 5
   Maximum possible: back 4
-------------------------------------------------------
```

## Session Storage

Les sessions sont stockees dans:
```
.project-memory/brainstorm-sessions/[slug].yaml
```

Format defini dans le skill `brainstormer` (references/session-format.md).
