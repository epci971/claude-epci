# Brief Template — Quick Fix

> Template for simple corrections (1h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | < 50 words |
| Verb type | Corrective (fixer, corriger, réparer, débugger) |
| Scope | Very limited (single element) |
| Components | 1 |

---

## Template Structure

```markdown
# {Action Verb} {Object Description}

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: {HIGH|MEDIUM|LOW}

## Objectif

{2-3 sentences describing what needs to be fixed and why}

## Contexte

{Brief context: where the issue occurs, when it was noticed, impact}

## Correction attendue

- {Action 1: Identify/locate the issue}
- {Action 2: Apply the fix}
- {Action 3: Verify the fix works}

## Notes

- {Additional notes or "Aucune note complémentaire."}
```

---

## Field Guidelines

### Title

**Format**: `{Verb} {Issue} {Location/Context}`

**Good examples**:
- "Corriger l'affichage des dates format FR"
- "Fixer le bug de validation email"
- "Réparer le bouton de soumission formulaire"
- "Débugger le calcul de TVA"

**Bad examples**:
- "Bug à corriger" (too vague)
- "Le truc qui marche pas" (informal)
- "Fix" (incomplete)

### Objective

2-3 sentences covering:
1. What is broken
2. Expected vs actual behavior
3. (Optional) Impact on users

**Template**:
> Corriger {le problème} qui {description du comportement actuel} au lieu de {comportement attendu}. {Impact si pertinent}.

### Context

Brief context including:
- Where: Page, module, component
- When: Since when, after what change
- Who: Users affected

**Template**:
> Le problème apparaît {où}. {Depuis quand ou déclencheur}. {Qui est impacté}.

### Correction attendue

3-4 bullet points, NOT implementation plan:
1. Identify/locate step
2. Fix action
3. Verification step
4. (Optional) Related check

**Note**: No checkboxes `[ ]` for Quick fix — too simple.

### Notes

Use one of:
- Specific note if relevant context exists
- "Aucune note complémentaire." if nothing to add

---

## Complete Example

```markdown
# Corriger l'affichage des dates format FR dans le module laboratoire

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH

## Objectif

Corriger l'affichage incorrect des dates dans le module laboratoire. Les dates apparaissent actuellement en format américain (MM/DD/YYYY) au lieu du format français attendu (DD/MM/YYYY).

## Contexte

Le problème apparaît sur la page de résultats d'analyses du laboratoire. Il affecte toutes les dates de prélèvement et d'analyse. Les utilisateurs ont signalé des confusions lors de la lecture des rapports.

## Correction attendue

- Identifier le composant DateDisplay utilisé dans les vues laboratoire
- Modifier le formateur de date pour utiliser le pattern `d/m/Y`
- Vérifier que le format est cohérent sur toutes les vues du module
- S'assurer que l'export PDF utilise également le bon format

## Notes

- Aucune note complémentaire.
```

---

## Variation: With Notes

```markdown
# Fixer le bug de validation email sur le formulaire d'inscription

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: MEDIUM

## Objectif

Corriger la validation email qui accepte des adresses invalides. Actuellement, des adresses sans domaine valide (ex: "test@test") passent la validation.

## Contexte

Le bug a été introduit suite à la mise à jour du validateur la semaine dernière. Il concerne uniquement le formulaire d'inscription, les autres formulaires utilisent l'ancien validateur.

## Correction attendue

- Localiser le validateur email dans le composant RegisterForm
- Appliquer une regex plus stricte incluant la validation du domaine
- Tester avec une liste d'emails valides et invalides

## Notes

- Vérifier si le même validateur est utilisé ailleurs avant modification
- Le ticket client #1234 est lié à ce bug
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Include implementation plan | Keep to 3-4 simple actions |
| Use checkboxes `[ ]` | Use simple bullets `-` |
| Write > 150 words | Keep concise |
| Include NFR section | Skip for quick fixes |
| Add time estimates per action | Single 1h estimate only |
