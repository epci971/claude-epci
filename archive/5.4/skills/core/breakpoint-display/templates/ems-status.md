# Template: EMS-Status Breakpoint

## Overview

Affichage du status de session brainstorm avec score EMS et 5 axes de progression.
Display-only avec commandes suggérées (pas de AskUserQuestion).

**Usage:** `/brainstorm` iteration status display

## Data Structure

```typescript
{
  type: "ems-status",
  title: "{TITLE}",
  data: {
    phase: "DIVERGENT" | "CONVERGENT",
    persona: "Architecte" | "Sparring" | "Pragmatique",
    iteration: {number},
    ems: {
      score: {number},       // 0-100
      delta: "{string}",     // "+12" or null
      axes: {
        clarity: {number},       // 0-100
        depth: {number},
        coverage: {number},
        decisions: {number},
        actionability: {number}
      },
      weak_axes: ["{string}"],   // Axes < 50
      progression: ["{string}"]  // History: ["Init(22)", "Iter1(38)", ...]
    },
    done: ["{string}"],      // Completed items this iteration
    open: ["{string}"],      // Remaining open items
    commands: ["{string}"]   // Available commands
  }
  // No 'ask' field - display only with command hints
}
```

## Display Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 BRAINSTORM | {PHASE} {PERSONA} | Iter {N}                        │
├─────────────────────────────────────────────────────────────────────┤
│ 🎯 EMS: {SCORE}/100 ({DELTA})                                       │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Clarté      {BAR} {VAL}  │ Profondeur   {BAR} {VAL}            │ │
│ │ Couverture  {BAR} {VAL}  │ Décisions    {BAR} {VAL}            │ │
│ │ Action      {BAR} {VAL}  │              [WEAK: {AXES}]         │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ✅ Done: {done items}                                               │
│ 📋 Open: {open items}                                               │
├─────────────────────────────────────────────────────────────────────┤
│ → {commands}                                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Progress Bar Generation

Generate 10-character progress bars:
- Score / 10 rounded = number of `█` (filled)
- Remaining = `░` (empty)
- Mark axes < 50 as `[WEAK]`

```typescript
function generateBar(score: number): string {
  const filled = Math.round(score / 10);
  return '█'.repeat(filled) + '░'.repeat(10 - filled);
}

// Examples:
// 80 → "████████░░"
// 45 → "████░░░░░░"
// 100 → "██████████"
```

## Example: Brainstorm Iteration

```typescript
{
  type: "ems-status",
  title: "BRAINSTORM STATUS",
  data: {
    phase: "DIVERGENT",
    persona: "Architecte",
    iteration: 3,
    ems: {
      score: 65,
      delta: "+12",
      axes: {
        clarity: 80,
        depth: 60,
        coverage: 45,
        decisions: 75,
        actionability: 70
      },
      weak_axes: ["coverage"],
      progression: ["Init(22)", "Iter1(38)", "Iter2(53)", "Current(65)"]
    },
    done: ["Cible identifiée", "Contraintes listées", "Persona défini"],
    open: ["Délais à préciser", "Intégrations externes", "Risques à évaluer"],
    commands: ["continue", "dive", "back", "save", "energy", "finish"]
  }
}
```

**Rendered:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 BRAINSTORM | DIVERGENT Architecte | Iter 3                       │
├─────────────────────────────────────────────────────────────────────┤
│ 🎯 EMS: 65/100 (+12)                                                │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Clarté      ████████░░ 80  │ Profondeur   ██████░░░░ 60        │ │
│ │ Couverture  ████░░░░░░ 45  │ Décisions    ████████░░ 75        │ │
│ │ Action      ███████░░░ 70  │              [WEAK: Couverture]   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ✅ Done: Cible identifiée, Contraintes listées, Persona défini      │
│ 📋 Open: Délais à préciser, Intégrations externes                   │
├─────────────────────────────────────────────────────────────────────┤
│ → continue | dive | back | save | energy | finish                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Variant: Finalization Checkpoint

When EMS >= 70, use `type: plan-review` instead for the checkpoint, but `ems-status`
can still be used for the status display portion before the AskUserQuestion.

## Token Savings

**Before:** ~150 tokens (manual ASCII box)
**After:** ~65 tokens (skill reference)
**Gain:** 57%

## Notes

- NO AskUserQuestion - this is purely informational display
- Commands are displayed as hints, user types them directly
- Always show weak_axes if any axis < 50
- Progression line shows EMS history for context
- Used after each iteration in brainstorm Phase 2
