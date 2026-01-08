# Brainstorm Energy Checkpoints Reference

> Reference pour les energy checkpoints dans `/brainstorm`.
> Points de controle pour gerer la fatigue cognitive.

---

## Objectif

Points de controle pour gerer la fatigue cognitive et maintenir l'engagement.

## Triggers (5 conditions)

| Trigger | Condition | Raison |
|---------|-----------|--------|
| **EMS 50** | EMS atteint 50 | Mi-parcours, verification du flow |
| **EMS 75** | EMS atteint 75 | Pres de la fin, suggerer finish |
| **Iter 7+** | Iteration >= 7 sans commande | Session longue, risque de fatigue |
| **Phase change** | Divergent -> Convergent | Transition importante |
| **EMS stagnant** | Delta EMS < 3 sur 2 iterations | Exploration peut-etre bloquee |

## Format Energy Check

```
-------------------------------------------------------
ENERGY CHECK | EMS: XX/100 | Phase: [phase]
-------------------------------------------------------
On a bien avance sur l'exploration. Comment tu te sens?

[1] Continuer — Je suis dans le flow
[2] Pause — Sauvegarder et reprendre plus tard
[3] Accelerer — Passons a la convergence
[4] Pivoter — Je veux changer d'angle
-------------------------------------------------------
```

## Actions par choix

| Choix | Action |
|-------|--------|
| **[1] Continuer** | Poursuivre l'iteration normale |
| **[2] Pause** | Executer `save`, afficher instructions pour reprendre |
| **[3] Accelerer** | Executer `converge`, passer en phase Convergent |
| **[4] Pivoter** | Executer `pivot`, reorienter l'exploration |

## Commande `energy`

Force un energy check a tout moment:
```
> energy
```

Utile pour:
- Faire une pause planifiee
- Evaluer son etat avant une decision importante
- Changer de direction explicitement
