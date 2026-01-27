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

## BREAKPOINT:

```typescript
@skill:epci:breakpoint-system
  type: phase-transition
  title: "Exploration Complete [E→P]"
  data: {
    phase_completed: "explore",
    phase_next: "plan",
    summary: {
      duration: "{duration}",
      tasks_completed: 1,
      files_modified: [],
      tests_status: "N/A"
    },
    checkpoint_created: {
      id: "{feature_id}-checkpoint-explore",
      resumable: true
    }
  }
  ask: {
    question: "Proceed to Planning phase?",
    header: "Phase E→P",
    options: [
      {label: "Continue to Plan (Recommended)", description: "Proceed with implementation planning"},
      {label: "Extend Exploration", description: "Explore more files before planning"},
      {label: "Abort", description: "Scope too large, cancel implementation"}
    ]
  }
  suggestions: [
    {pattern: "findings", text: "Review {N} files to modify before planning", priority: "P1"},
    {pattern: "patterns", text: "Follow identified patterns: {patterns}", priority: "P2"}
  ]
```

## NEXT STEP TRIGGER:

When exploration is complete and user approves findings, proceed to `step-02-plan.md`.
