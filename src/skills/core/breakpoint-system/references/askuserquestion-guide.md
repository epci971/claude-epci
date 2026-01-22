# AskUserQuestion Integration Guide

How to properly use AskUserQuestion for interactive breakpoints.

## Overview

AskUserQuestion provides native Claude Code UI for user choices instead of text parsing.

## API Structure

```typescript
AskUserQuestion({
  questions: [{
    question: string,      // The question to display
    header: string,        // Short header (MAX 12 CHARS)
    multiSelect: boolean,  // Allow multiple selections
    options: Array<{
      label: string,       // Option text
      description: string  // Additional context
    }>
  }]
})
```

## Constraints

| Constraint | Value | Handling |
|------------|-------|----------|
| Header max length | 12 characters | Truncate with warning |
| Max options | 4 | Error if exceeded |
| Min options | 1 | At least free response |

## Header Examples

Good headers (within 12 chars):

```typescript
"Validation"    // 10 chars
"Phase 2"       // 7 chars  
"Decoupage"     // 9 chars
"Solution"      // 8 chars
"Action"        // 6 chars
```

## Building Options Array

Always add free response as last option:

```typescript
function buildOptions(customOptions: Option[]): Option[] {
  if (customOptions.length > 3) {
    throw new Error("Maximum 3 custom options allowed");
  }
  
  return [
    ...customOptions,
    { 
      label: "Autre reponse...", 
      description: "Saisir une reponse libre" 
    }
  ];
}
```

## Recommended Marker

First option gets `(Recommended)` suffix if it's the default path:

```typescript
options: [
  { label: "Valider (Recommended)", description: "Continuer" },
  { label: "Modifier", description: "Ajuster" },
  { label: "Annuler", description: "Arreter" }
]
```

## Invocation Example

```typescript
AskUserQuestion({
  questions: [{
    question: "Le brief vous convient-il ?",
    header: "Validation",
    multiSelect: false,
    options: [
      { label: "Valider (Recommended)", description: "Continuer vers exploration" },
      { label: "Modifier", description: "Je reformule moi-meme" },
      { label: "Annuler", description: "Arreter workflow" },
      { label: "Autre reponse...", description: "Saisir une reponse libre" }
    ]
  }]
})
```

## Response Handling

AskUserQuestion returns the selected option label.

```typescript
// Map response to action
const response = await AskUserQuestion(...);

switch (response) {
  case "Valider (Recommended)":
    return { selected: "A", selectedLabel: "Valider" };
  case "Modifier":
    return { selected: "B", selectedLabel: "Modifier" };
  case "Annuler":
    return { selected: "C", selectedLabel: "Annuler" };
  case "Autre reponse...":
    // Prompt for free text
    return { selected: "free", freeText: await getFreeText() };
}
```

## Fallback Mode

If AskUserQuestion is unavailable or fails:

```
AskUserQuestion indisponible. Veuillez repondre par:
- A pour "Valider"
- B pour "Modifier"  
- C pour "Annuler"
- Ou tapez votre reponse libre

Votre choix: _
```

Parse text input and map to selection:

```typescript
function parseFallbackResponse(input: string): Response {
  const normalized = input.trim().toUpperCase();
  
  if (normalized === "A") return { selected: "A", selectedLabel: options[0].label };
  if (normalized === "B") return { selected: "B", selectedLabel: options[1].label };
  if (normalized === "C") return { selected: "C", selectedLabel: options[2].label };
  
  // Treat as free response
  return { selected: "free", freeText: input };
}
```

## MultiSelect Mode

For decomposition modifications or multiple choices:

```typescript
AskUserQuestion({
  questions: [{
    question: "Que souhaitez-vous modifier ?",
    header: "Modifier",
    multiSelect: true,  // Enable multi-select
    options: [
      { label: "Fusionner specs", description: "Combiner specifications" },
      { label: "Decouper spec", description: "Diviser en parties" },
      { label: "Renommer", description: "Changer les noms" }
    ]
  }]
})
```

Response is array of selected labels.

## Error Handling

```typescript
try {
  const response = await AskUserQuestion(config);
  return processResponse(response);
} catch (error) {
  console.warn("AskUserQuestion failed, using fallback");
  return fallbackTextInput(config.options);
}
```

## Best Practices

1. **Keep headers short**: 12 chars max, use abbreviations if needed
2. **3 options max**: Plus free response = 4 total
3. **Clear descriptions**: Help user understand each option
4. **Recommended first**: Default path should be option A
5. **Always free response**: Users may have unexpected needs
6. **Handle failures**: Always have fallback ready
