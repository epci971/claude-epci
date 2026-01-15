# Brainstorm Turbo Mode Reference

> Reference pour le flag `--turbo` de la commande `/brainstorm`.
> Utilise `@clarifier` (Haiku) pour des iterations rapides.

---

## Rules

**When `--turbo` flag is active, you MUST follow these rules:**

1. **Use @clarifier agent** (Haiku model) for generating clarification questions:
   ```
   Invoke @clarifier via Task tool with model: haiku
   Input: Current brief + codebase context
   Output: 2-3 targeted questions with suggestions
   ```

2. **Maximum 3 iterations** — Auto-finish after iteration 3

3. **Auto-accept suggestions** if EMS > 60:
   - If EMS reaches 60+, suggest `finish` proactively
   - If user provides quick confirmation ("ok", "oui", "c"), auto-accept all suggestions

4. **Reduced breakpoint** — Compact format only, skip detailed explanations

5. **Skip HMW questions** — Equivalent to `--no-hmw`

## Process

```
Init -> @clarifier (Haiku) -> Iter 1 -> Iter 2 -> Iter 3 (max) -> finish
                              |
                        EMS > 60? -> Auto-suggest finish
```

## Usage

```
/brainstorm --turbo "description de la feature"
```
