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

### 1. Quick Keyword Search

Based on input description, search for relevant files:

```bash
# Example for "fix login button"
grep -r "login" --include="*.{ts,tsx,js,jsx}" src/
grep -r "LoginButton" --include="*.{ts,tsx,js,jsx}" src/
```

**Output:**
- List of potentially relevant files (max 5)
- Note file locations and purposes

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

If exploration reveals more complexity than expected, invoke breakpoint:

```typescript
@skill:breakpoint-system
  type: validation
  title: "Complexity Alert"
  data: {
    context: "Exploration reveals higher complexity than estimated",
    item_to_validate: {
      objectif: "Decide whether to continue with /quick or escalate",
      contexte: "Initial: {TINY|SMALL}, After exploration: Appears {STANDARD}",
      contraintes: "{explanation of why complexity seems higher}",
      success_criteria: "User confirms appropriate workflow"
    }
  }
  ask: {
    question: "How to proceed with higher complexity?",
    header: "Complexity",
    options: [
      {label: "Continue with /quick", description: "Proceed despite higher complexity (may take longer)"},
      {label: "Use /implement (Recommended)", description: "Escalate to full EPCI workflow"},
      {label: "Abort", description: "Cancel and reassess requirements"}
    ]
  }
  suggestions: [
    {pattern: "escalate", text: "STANDARD+ tasks benefit from full EPCI workflow", priority: "P1"}
  ]
```

## NEXT STEP TRIGGER:

Proceed to step-02-mini-plan.md with target files and patterns.
