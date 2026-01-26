---
name: step-00-init
description: Initialize implement workflow and detect complexity
prev_step: null
next_step: steps/step-01-explore.md
conditional_next:
  - condition: "complexity == TINY or complexity == SMALL"
    step: steps/step-00b-turbo.md
---

# Step 00: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip complexity detection
- :red_circle: NEVER proceed without valid feature-slug
- :white_check_mark: ALWAYS parse input arguments first
- :white_check_mark: ALWAYS invoke complexity-calculator
- :white_check_mark: ALWAYS create Feature Document skeleton if STANDARD+
- :thought_balloon: FOCUS on correct routing based on complexity

## EXECUTION PROTOCOLS:

1. **Parse** input arguments
   - Extract feature-slug (required)
   - Extract spec-path (optional, prefixed with @)

2. **Validate** input
   - feature-slug must be kebab-case
   - If spec-path provided, verify file exists

3. **Load** spec if provided
   - Read spec file content
   - Extract requirements, acceptance criteria

4. **Detect** complexity using complexity-calculator
   - Analyze scope from spec or description
   - Estimate LOC and file count
   - Determine complexity level: TINY, SMALL, STANDARD, LARGE

5. **Route** based on complexity
   - TINY/SMALL → step-00b-turbo (redirect to /quick)
   - STANDARD/LARGE → step-01-explore

6. **Initialize** Feature Document (STANDARD+ only)
   - Create `.epci/features/{feature-slug}/FEATURE.md` skeleton
   - Record complexity, start time, initial scope

## CONTEXT BOUNDARIES:

- This step expects: User input (feature-slug, optional @spec-path)
- This step produces: Validated context, complexity level, routing decision

## OUTPUT FORMAT:

```
## Initialization Complete

Feature: {feature-slug}
Spec: {spec-path or "none provided"}
Complexity: {TINY|SMALL|STANDARD|LARGE}

Routing: {next step path}
```

## BREAKPOINT (for STANDARD+ only):

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — Complexity Assessment                               │
├─────────────────────────────────────────────────────────────────────┤
│ Feature: {feature-slug}                                             │
│ Detected Complexity: {complexity}                                   │
│ Estimated: ~{loc} LOC across {files} files                          │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Proceed with full EPCI workflow (Recommended)              │ │
│ │  2. Downgrade to /quick (simpler than estimated)               │ │
│ │  3. Upgrade complexity (more complex than estimated)           │ │
│ │  4. Abort and refine requirements                              │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When complexity is STANDARD or LARGE and user confirms, proceed to `step-01-explore.md`.

If complexity is TINY or SMALL, proceed to `step-00b-turbo.md`.
