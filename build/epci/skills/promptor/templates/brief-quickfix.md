# Brief Template — Quick Fix

> Template for simple corrections (1h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | < 50 words |
| Verb type | Corrective (fixer, corriger, réparer) |
| Scope | Very limited |

---

## Template

```markdown
# {Action Verb} {Object Description}

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: {HIGH|MEDIUM|LOW}

## Objectif

{2-3 sentences describing what needs to be fixed and why}

## Contexte

{Brief context: where, when, impact}

## Correction attendue

- {Action 1: Identify/locate}
- {Action 2: Apply fix}
- {Action 3: Verify}

## Notes

- {Notes or "Aucune note complémentaire."}
```

---

## Title Guidelines

**Good**:
- "Corriger l'affichage des dates format FR"
- "Fixer le bug de validation email"
- "Réparer le bouton de soumission"

**Bad**:
- "Bug à corriger" (too vague)
- "Fix" (incomplete)

---

## Example

```markdown
# Corriger l'affichage des dates format FR dans le module laboratoire

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH

## Objectif

Corriger l'affichage incorrect des dates dans le module laboratoire. 
Les dates apparaissent en format US (MM/DD/YYYY) au lieu du format FR (DD/MM/YYYY).

## Contexte

Le problème apparaît sur la page de résultats d'analyses. 
Toutes les dates de prélèvement s'affichent mal.

## Correction attendue

- Identifier le composant DateDisplay utilisé
- Modifier le formateur pour utiliser le pattern `d/m/Y`
- Vérifier la cohérence sur toutes les vues du module

## Notes

- Aucune note complémentaire.
```

---

## Characteristics

- No implementation plan
- ~100-150 words total
- Simple bullet list (no checkboxes)
