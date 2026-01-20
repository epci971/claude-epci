# AskUserQuestion Integration Guide

## Overview

Guide complet pour utiliser `AskUserQuestion` avec le skill `breakpoint-display`.

**Référence:** Implementation en production dans `/brainstorm`

## Basic Usage

```typescript
AskUserQuestion({
  questions: [{
    question: "{QUESTION}",
    header: "{HEADER}",  // Max 12 chars
    multiSelect: {true|false},
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }]
})
```

## Headers Constraints

**CRITICAL:** Headers must be ≤ 12 characters (including emojis).

### Valid Headers (from /brainstorm)

```typescript
"📝 Validation"  // 12 chars ✅
"🚀 Action"      // 8 chars ✅
"🚀 Phase 2"     // 10 chars ✅
"📋 Découpage"   // 12 chars ✅
"🔧 Modifier"    // 10 chars ✅
"🔄 Transition"  // 12 chars ✅
"💡 Solution"    // 11 chars ✅
```

### Invalid Headers

```typescript
"💡 Diagnostic"  // 13 chars ❌ → Use "💡 Solution"
"🚀 Next Phase"  // 13 chars ❌ → Use "🚀 Phase X"
```

**Tip:** Count emojis as 2 characters when calculating length.

## Options Format

### Simple Options

```typescript
options: [
  {
    label: "Valider",
    description: "Continuer vers exploration"
  },
  {
    label: "Modifier",
    description: "Je reformule moi-même"
  },
  {
    label: "Annuler",
    description: "Arrêter workflow"
  }
]
```

### Recommended Option

First option should be marked `(Recommended)` if it's the default choice:

```typescript
options: [
  {
    label: "Valider (Recommended)",
    description: "Continuer vers exploration"
  },
  {
    label: "Modifier",
    description: "Je reformule moi-même"
  }
]
```

### MultiSelect Mode

For selecting multiple options simultaneously:

```typescript
multiSelect: true,
options: [
  {
    label: "5 Whys",
    description: "Creuser causes profondes"
  },
  {
    label: "Pre-mortem",
    description: "Anticiper échecs"
  },
  {
    label: "SWOT",
    description: "Analyser forces/faiblesses"
  }
]
```

**Note:** Users can select 0, 1, or multiple options in multiSelect mode.

## Response Handling

### Single Select

```typescript
// User selected one option
const response = await AskUserQuestion({...});
const selected = response.answers["header"];

if (selected === "Valider (Recommended)") {
  // Continue workflow
} else if (selected === "Modifier") {
  // Wait for modifications
} else if (selected === "Annuler") {
  // Stop workflow
}
```

### Multi Select

```typescript
// User selected multiple options
const response = await AskUserQuestion({...});
const selected = response.answers["header"];

// selected is a comma-separated string: "5 Whys, Pre-mortem"
const techniques = selected.split(", ");

techniques.forEach(technique => {
  // Apply each technique
});
```

### "Other" Option

Users can always select "Other" and provide free text input. Handle this case:

```typescript
const selected = response.answers["header"];

if (selected.startsWith("Other:")) {
  const customInput = selected.replace("Other: ", "");
  // Handle custom input
}
```

## Two-Level Questions

For complex workflows with sub-menus (e.g., `/decompose` modify options):

### Level 1: Main Choice

```typescript
AskUserQuestion({
  questions: [{
    question: "Le découpage vous convient-il ?",
    header: "📋 Découpage",
    options: [
      {label: "Valider (Recommended)", description: "Générer fichiers"},
      {label: "Modifier", description: "Ajuster découpage"},
      {label: "Annuler", description: "Abandonner"}
    ]
  }]
})
```

### Level 2: Sub-Menu (if "Modifier" selected)

```typescript
if (level1_response === "Modifier") {
  AskUserQuestion({
    questions: [{
      question: "Que souhaitez-vous modifier ?",
      header: "🔧 Modifier",
      multiSelect: true,
      options: [
        {label: "Fusionner specs", description: "Ex: Fusionner S04 et S05"},
        {label: "Découper spec", description: "Ex: Découper S07 en 2"},
        {label: "Renommer", description: "Ex: S03 → Modèles"},
        {label: "Changer dépendances", description: "Ex: S06 ne dépend plus de S03"},
        {label: "Ajuster estimation", description: "Ex: S08 = 3j au lieu de 5j"}
      ]
    }]
  })
}
```

Then wait for free text describing the modifications.

## Error Handling

### Fallback to Textual Input

If `AskUserQuestion` fails (e.g., not available in environment), fallback to legacy textual choices:

```typescript
try {
  const response = await AskUserQuestion({...});
  // Handle response
} catch (error) {
  console.log("OPTIONS:");
  console.log("  [1] Valider → Continuer");
  console.log("  [2] Modifier → Réviser");
  console.log("  [3] Annuler → Arrêter");

  // Wait for textual input "1", "2", or "3"
}
```

## Best Practices

### DO

✅ Use clear, concise labels (1-4 words)
✅ Provide helpful descriptions (5-10 words)
✅ Mark default choice as `(Recommended)`
✅ Use multiSelect for non-exclusive choices
✅ Keep headers ≤ 12 characters
✅ Use emojis for visual clarity

### DON'T

❌ Don't use long labels (> 5 words)
❌ Don't duplicate info in label and description
❌ Don't use multiSelect for exclusive choices
❌ Don't exceed 12-char header limit
❌ Don't forget to handle "Other" case

## Examples from Production

### /brainstorm Technique Selection

```typescript
AskUserQuestion({
  questions: [{
    question: "Quelles techniques appliquer ?",
    header: "💡 Technique",
    multiSelect: true,
    options: [
      {label: "5 Whys", description: "Creuser causes profondes"},
      {label: "Pre-mortem (Recommended)", description: "Anticiper échecs possibles"},
      {label: "SWOT", description: "Forces/faiblesses/opportunités/menaces"}
    ]
  }]
})
```

### /brainstorm Transition Check

```typescript
AskUserQuestion({
  questions: [{
    question: "Passer en mode Convergent ?",
    header: "🔄 Transition",
    options: [
      {label: "Continuer Divergent", description: "Explorer davantage d'options"},
      {label: "Passer Convergent (Recommended)", description: "Commencer à converger vers solution"}
    ]
  }]
})
```

## Integration with breakpoint-display

When using `breakpoint-display`, the skill handles AskUserQuestion invocation:

```typescript
// In a command (e.g., /brief)
@skill:breakpoint-display
  type: validation
  title: "VALIDATION DU BRIEF"
  data: {...}
  ask: {
    question: "Le brief vous convient-il ?",
    header: "📝 Validation",
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-même"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
```

The skill will:
1. Display the data section (brief, metrics, etc.)
2. Invoke AskUserQuestion with the provided options
3. Return the response to the calling workflow

## References

- Brainstorm Implementation: voir `/brainstorm`
- Breakpoint Display Skill: voir skill `breakpoint-display`
- Template Examples: @templates/
