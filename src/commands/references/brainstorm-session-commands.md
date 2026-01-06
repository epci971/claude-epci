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

Revient a l'iteration precedente.

```
> back

-------------------------------------------------------
Retour a l'iteration 2
   EMS: 38/100 (etait 52)
   Phase: Divergent

   Questions restaurees:
   1. [Question de l'iteration 2]
   2. [Question de l'iteration 2]
-------------------------------------------------------
```

**Limitations**:
- 1 step back uniquement (pas de back multiple)
- Impossible si iteration == 1
- L'historique de l'iteration annulee est conserve (peut revenir en avant avec `continue`)

## Session Storage

Les sessions sont stockees dans:
```
.project-memory/brainstorm-sessions/[slug].yaml
```

Format defini dans `src/skills/core/brainstormer/references/session-format.md`.
