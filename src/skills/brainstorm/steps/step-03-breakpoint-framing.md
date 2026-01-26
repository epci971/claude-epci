# Step 03: Breakpoint Framing

> Validate framing before entering iteration loop.

## Trigger

- Previous step: `step-02-framing.md` completed
- Template, HMW, and EMS baseline established

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | From step-01 | Yes |
| `template` | From step-02 | Yes |
| `hmw_questions` | From step-02 | No |
| `ems` | From step-02 | Yes |
| `codebase_analysis` | From step-02 | No |
| `--quick` flag | From step-00 | No |

## Protocol

### 1. Prepare Framing Summary

Compile all framing information:

```markdown
## Session Framing

**Topic**: {idea_refined}
**Template**: {template}
**Initial EMS**: {ems.global}/100

### Brief Summary
{brief_v0 condensed}

### Codebase Context
- Stack: {detected stack}
- Related modules: {list}
- Patterns found: {list}

### HMW Questions
1. {hmw_1}
2. {hmw_2}
3. {hmw_3}
```

### 2. Generate Framing Questions (3 max)

Target critical missing information:

| Category | Question Type |
|----------|---------------|
| **Target** | "Who exactly will use this?" |
| **Constraints** | "Any technical limits we should know?" |
| **Timeline** | "Is there a deadline or milestone?" |
| **Dependencies** | "Does this depend on other work?" |
| **Priority** | "What's the most critical aspect?" |

```
IF --quick mode:
  → Limit to 2 questions
  → Focus on Target and Priority only
```

### 3. BREAKPOINT: Framing Validation

```typescript
@skill:breakpoint-system
  type: plan-review
  title: "Framing Validation"
  data: {
    metrics: {
      template: "{template}",
      ems_initial: {ems.global},
      hmw_count: {hmw_questions.length},
      codebase_context: "{available|partial|none}"
    },
    brief_summary: "{brief_v0 condensed}",
    framing_questions: [
      {category: "Target", question: "...", suggestion: "..."},
      {category: "Constraints", question: "...", suggestion: "..."},
      {category: "Timeline", question: "...", suggestion: "..."}
    ]
  }
  ask: {
    question: "Ready to start exploration iterations?",
    header: "Framing",
    options: [
      {label: "Start iterations (Recommended)", description: "Begin structured exploration"},
      {label: "Adjust framing", description: "Modify template or brief"},
      {label: "Add context", description: "Provide more background first"}
    ]
  }
  suggestions: [
    {pattern: "template", text: "Template '{template}' selected - seems appropriate for your topic", priority: "P1"},
    {pattern: "ems", text: "Starting EMS: {ems.global} - typical for validated brief", priority: "P2"},
    {pattern: "hmw", text: "Review HMW questions - they guide exploration", priority: "P3"}
  ]
```

### 4. Integrate Responses

```
IF framing questions answered:
  → Update brief with new information
  → Recalculate EMS clarity axis
  → Store decisions made

IF "Adjust framing" selected:
  → Allow template change
  → Allow brief modification
  → Return to this breakpoint

IF "Add context" selected:
  → Open-ended input
  → Process and integrate
  → Return to this breakpoint
```

### 5. Finalize Iteration Setup

```json
{
  "iteration": 1,
  "phase": "DIVERGENT",
  "persona": "architecte",
  "exploration_ready": true,
  "framing_complete": true
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `framing_complete` | Session state |
| `exploration_ready` | Session state |
| Updated `brief_v0` | Session state |
| Updated `ems` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Framing validated | → `step-04-iteration.md` |
| Adjust framing | → `step-03-breakpoint-framing.md` (loop) |
| Cancel session | → Exit with summary |

## Error Handling

| Error | Resolution |
|-------|------------|
| User wants to restart | → `step-01-clarify.md` |
| Template mismatch | Allow template change |
| Missing critical info | Generate additional questions |
