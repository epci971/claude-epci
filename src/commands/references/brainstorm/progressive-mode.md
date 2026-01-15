# Brainstorm Progressive Mode Reference

> Reference pour le flag `--progressive` de la commande `/brainstorm`.
> Mode 3 phases structurees: Divergent -> Transition -> Convergent.

---

## Rules

**When `--progressive` flag is active, you MUST follow these rules:**

1. **Three structured phases:**

   | Phase | EMS Range | Focus | Techniques |
   |-------|-----------|-------|------------|
   | DIVERGENT | 0-49 | Exploration, generation | Ideation, Perspective, Breakthrough |
   | TRANSITION | ~50 | Energy check + summary | Forced pause |
   | CONVERGENT | 50-100 | Decisions, prioritization | Analysis |

2. **Forced transition at EMS 50:**
   - When EMS reaches 50, MUST trigger energy check
   - Display mid-session summary
   - Auto-switch to Convergent phase after validation

3. **Phase-specific technique auto-selection:**
   - Divergent: Prioritize creative techniques (SCAMPER, Six Hats, What-If)
   - Convergent: Prioritize analytical techniques (MoSCoW, Scoring, Pre-mortem)

4. **Transition checkpoint format:**
   ```
   -------------------------------------------------------
   TRANSITION | EMS: 50/100 | Phase: Divergent -> Convergent
   -------------------------------------------------------
   Mi-parcours atteint! Resume des idees explorees:

   Valide:
   - [Idea 1]
   - [Idea 2]

   A approfondir:
   - [Idea 3]

   [1] Continuer vers Convergent
   [2] Pause — Sauvegarder
   [3] Revenir en Divergent (annuler transition)
   -------------------------------------------------------
   ```

5. **@planner availability** — Auto-available at EMS 70+ in Convergent phase

## Process

```
DIVERGENT (EMS 0-49)
       |
       v (EMS reaches 50)
   TRANSITION
   |-- Energy check
   |-- Summary display
   +-- Direction validation
       |
       v
CONVERGENT (EMS 50-100)
       |
       v (EMS reaches 70)
   @planner available
```

## Usage

```
/brainstorm --progressive "nouveau module de paiement"
```
