---
name: step-01-explore
description: Read-only codebase exploration phase [E]
prev_step: steps/step-00-init.md
next_step: steps/step-02-plan.md
---

# Step 01: Explore [E]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER modify any files during exploration
- 🔴 NEVER write code during exploration
- 🔴 NEVER skip pattern identification
- ✅ ALWAYS use read-only tools (Read, Glob, Grep)
- ✅ ALWAYS identify existing patterns before planning
- ✅ ALWAYS document dependencies found
- ✅ ALWAYS use @Explore agent for comprehensive search
- 🔵 YOU ARE AN INVESTIGATOR, not an implementer yet
- 💭 FOCUS on understanding before acting

## EXECUTION PROTOCOLS:

1. **Analyze** requirements
   - Parse spec/requirements into discrete components
   - Identify functional requirements
   - Identify non-functional requirements (performance, security)

2. **Invoke Native Explore Agent**

Delegate comprehensive codebase exploration to Claude Code's native Explore agent:

```typescript
Task({
  subagent_type: "Explore",
  model: "haiku",
  prompt: `
## Exploration Objective
Analyze codebase for feature: {feature_name}

## Search Focus
1. Files matching patterns/keywords: {patterns_keywords}
2. Existing patterns for: {functionality_type}
3. Dependencies in modules: {target_modules}

## Thoroughness Level
very thorough

## Required Output
- Relevant files with purpose annotations
- Architecture patterns identified
- Internal/external dependencies mapped
- Files to modify/create list
  `
})
```

**Why Native Explore:**
- Read-only guaranteed (no accidental modifications)
- Haiku model = fast and cost-effective
- Context isolation (doesn't pollute main thread)
- Supports thoroughness levels: quick, medium, very thorough

3. **Identify** existing patterns
   - Architecture patterns in use
   - Coding conventions
   - Testing patterns
   - Error handling patterns

4. **Map** dependencies
   - Internal dependencies (other modules)
   - External dependencies (libraries, APIs)
   - Data flow dependencies

5. **Document** findings
   - Update Feature Document with exploration results
   - List files that will need modification
   - Note patterns to follow

## CONTEXT BOUNDARIES:

- This step expects: Validated STANDARD+ complexity, feature requirements
- This step produces: Exploration findings, pattern documentation, dependency map

## OUTPUT FORMAT:

```
## Exploration Findings

### Relevant Files
- `path/to/file1.ts` — {purpose}
- `path/to/file2.ts` — {purpose}

### Existing Patterns
- Pattern 1: {description}
- Pattern 2: {description}

### Dependencies
- Internal: {list}
- External: {list}

### Files to Modify
- `path/to/modify1.ts` — {change type}
- `path/to/modify2.ts` — {change type}

### Files to Create
- `path/to/new1.ts` — {purpose}
```

## BREAKPOINT: Exploration Complete (OBLIGATOIRE)

AFFICHE cette boîte:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 EXPLORATION TERMINÉE [E→P]                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ RÉSUMÉ DE PHASE                                                     │
│ • Phase terminée: explore                                           │
│ • Phase suivante: plan                                              │
│ • Durée: {duration}                                                 │
│ • Fichiers modifiés: aucun (read-only)                              │
│ • Tests: N/A                                                        │
│                                                                     │
│ CHECKPOINT                                                          │
│ • ID: {feature_id}-checkpoint-explore                               │
│ • Reprise possible: oui                                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Réviser {N} fichiers à modifier avant planning                 │
│ [P2] Suivre les patterns identifiés: {patterns}                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Continuer vers Plan (Recommended) — Planifier implémentation│
│ │  [B] Étendre exploration — Explorer plus de fichiers           │ │
│ │  [C] Abandonner — Scope trop large                             │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

APPELLE:
```
AskUserQuestion({
  questions: [{
    question: "Passer à la phase Planning?",
    header: "Phase E→P",
    multiSelect: false,
    options: [
      { label: "Continuer vers Plan (Recommended)", description: "Procéder à la planification" },
      { label: "Étendre exploration", description: "Explorer plus de fichiers avant de planifier" },
      { label: "Abandonner", description: "Scope trop large, annuler implémentation" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

## NEXT STEP TRIGGER:

When exploration is complete and user approves findings, proceed to `step-02-plan.md`.
