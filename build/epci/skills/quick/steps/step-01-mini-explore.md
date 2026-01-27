---
name: step-01-mini-explore
description: Quick codebase scan to identify target files and patterns
prev_step: steps/step-00-detect.md
next_step: steps/step-02-mini-plan.md
---

# Step 01: Mini-Explore [E]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER modify any files during exploration
- 🔴 NEVER spend more than 10 seconds on exploration
- ✅ ALWAYS identify target files for modification
- ✅ ALWAYS note existing patterns to follow
- 💭 FOCUS on speed - this is a quick scan, not deep analysis

## EXECUTION PROTOCOLS:

### 1. Invoke Native Explore Agent (Quick Mode)

Delegate fast codebase scan to Claude Code's native Explore agent:

```typescript
Task({
  subagent_type: "Explore",
  prompt: `
## Quick Exploration
Feature/Fix: {feature_or_fix_description}

## Find
- Target files for modification (max 3)
- Relevant patterns to follow
- Test file location

## Thoroughness Level
quick

## Output Format
- Primary file: {path} — {purpose}
- Test file: {path} — {exists|create}
- Pattern: {key pattern to follow}
  `
})
```

**Why Native Explore (Quick):**
- Haiku model = fastest response
- Read-only guaranteed (safe exploration)
- Context isolation (efficient memory)
- `quick` thoroughness matches /quick workflow speed

### 2. Identify Target Files

Determine which files need modification:

```
TARGET FILES:
├── Primary: {file that needs main change}
├── Test: {corresponding test file}
└── Related: {any supporting files, max 1-2}
```

**Rules:**
- Max 3 files for SMALL, 1-2 for TINY
- If more files needed → complexity may be underestimated

### 3. Note Existing Patterns

Quick scan of target file(s):

- Import style (relative vs absolute)
- Naming conventions (camelCase, kebab-case)
- Test framework and patterns
- Component/function structure

```
PATTERNS OBSERVED:
- Imports: {style}
- Naming: {convention}
- Tests: {framework} with {pattern}
- Structure: {component type / function style}
```

### 4. Check for Test File

Verify test file exists or note where to create:

```
TEST FILE:
├── Exists: {path/to/file.test.ts}
│   └─ Add tests to existing file
└── Create: {path/to/new.test.ts}
    └─ Follow project test conventions
```

## CONTEXT BOUNDARIES:

- This step expects: Validated input from step-00-detect
- This step produces: Target files, patterns, test file location
- Time budget: < 10 seconds

## OUTPUT FORMAT:

```
## Mini-Exploration Complete

Target Files:
1. {path/to/primary.ts} — {purpose}
2. {path/to/test.ts} — {test file}

Patterns:
- {pattern 1}
- {pattern 2}

Stack Context: {stack skill loaded, if any}
```

## COMPLEXITY RE-EVALUATION:

If exploration reveals more complexity than expected, AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️ ALERTE COMPLEXITÉ                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ L'exploration révèle une complexité plus élevée qu'estimée          │
│                                                                     │
│ Initial: {TINY|SMALL}                                               │
│ Après exploration: Semble {STANDARD}                                │
│                                                                     │
│ Raison: {explanation of why complexity seems higher}                │
│                                                                     │
│ Critère de succès: Utilisateur confirme le workflow approprié       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Les tâches STANDARD+ bénéficient du workflow EPCI complet      │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer avec /quick — Malgré complexité plus élevée     │ │
│ │  [B] Utiliser /implement (Recommended) — Workflow EPCI complet │ │
│ │  [C] Abandonner — Réévaluer les requirements                   │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Comment procéder avec la complexité plus élevée?",
    header: "Complexity",
    multiSelect: false,
    options: [
      { label: "Continuer avec /quick", description: "Procéder malgré complexité (peut prendre plus de temps)" },
      { label: "Utiliser /implement (Recommended)", description: "Escalader vers workflow EPCI complet" },
      { label: "Abandonner", description: "Annuler et réévaluer requirements" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

Proceed to step-02-mini-plan.md with target files and patterns.
