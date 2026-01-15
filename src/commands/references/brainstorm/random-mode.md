# Brainstorm Random Mode Reference

> Reference pour le flag `--random` de la commande `/brainstorm`.
> Selection aleatoire ponderee de techniques par phase.

---

## Rules

**When `--random` flag is active, you MUST follow these rules:**

1. **Weighted technique selection** based on current phase:

   | Phase | Ideation | Perspective | Breakthrough | Analysis |
   |-------|----------|-------------|--------------|----------|
   | Divergent | 0.4 | 0.3 | 0.2 | 0.1 |
   | Convergent | 0.1 | 0.2 | 0.2 | 0.5 |

2. **Exclude used techniques** — Check `session.techniques_used` array and exclude from selection pool

3. **Update techniques_used** — After selecting a technique, add it to `session.techniques_used`

4. **Display format** at each iteration:
   ```
   -------------------------------------------------------
   RANDOM MODE | Technique: [NAME] ([CATEGORY])
   -------------------------------------------------------
   [Apply selected technique's questions to current context]
   ```

5. **Fallback behavior** — If all techniques in a category are used, expand to other categories

## Process

```
Check phase -> Calculate weights -> Filter used techniques -> Weighted random select -> Apply technique -> Update techniques_used
```

## Usage

```
/brainstorm --random "ameliorer le systeme de cache"
```
