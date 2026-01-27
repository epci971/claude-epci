# Step 01: Clarify

> Clarify user input, reformulate, and validate brief.

## Trigger

- Previous step: `step-00-init.md` completed (default flow)
- `--no-clarify` flag: Skip to step-02

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `idea_raw` | From step-00 state | Yes |
| `project_context` | From step-00 | No |
| `--turbo` flag | From step-00 | No |

## Protocol

### 1. Assess Input Clarity

Calculate clarity score (0.0 - 1.0):

| Factor | Weight | Indicators |
|--------|--------|------------|
| Specificity | 0.3 | Named entities, concrete nouns |
| Completeness | 0.3 | Who, what, why present |
| Actionability | 0.2 | Verbs, outcomes mentioned |
| Context | 0.2 | Domain references, constraints |

```
IF clarity_score >= 0.8:
  → Skip clarification, proceed to reformulation
ELSE IF clarity_score >= 0.6:
  → Light clarification (1-2 questions)
ELSE:
  → Full clarification (2-3 questions)
```

### 2. Generate Clarification Questions

```python
IF --turbo flag:
  @agent:clarifier (Haiku)
    input: idea_raw, project_context
    output: questions[], suggestions[]
ELSE:
  @skill:epci:clarification-engine
    input: idea_raw, project_context
    mode: brainstorm
    max_questions: 3
```

Question categories:
- **Scope**: "What's the boundary of this feature?"
- **Users**: "Who is the primary user?"
- **Constraints**: "Any technical or business constraints?"
- **Success**: "How will you know it's successful?"

### 3. BREAKPOINT: Clarification

```typescript
@skill:epci:breakpoint-system
  type: validation
  title: "Clarification"
  data: {
    original_input: "{idea_raw}",
    clarity_score: {score},
    questions: [
      {category: "Scope", question: "...", suggestion: "..."},
      {category: "Users", question: "...", suggestion: "..."}
    ]
  }
  ask: {
    question: "Please answer these questions to clarify your idea:",
    header: "Clarify",
    options: [
      {label: "Answer questions", description: "Provide answers inline"},
      {label: "Skip clarification", description: "Proceed with current understanding"},
      {label: "Rephrase idea", description: "Start over with clearer description"}
    ]
  }
```

### 4. Integrate Responses

```
FOR each answer:
  - Extract key information
  - Update context with new details
  - Recalculate clarity_score
```

### 5. Generate Reformulation

Synthesize into structured brief:

```markdown
## Brief (v0)

**Subject**: {one-line summary}

**Context**: {why this matters, what problem it solves}

**Scope**: {what's included and excluded}

**Users**: {primary and secondary users}

**Constraints**: {technical, business, timeline}

**Success Criteria**: {how to measure success}
```

### 6. BREAKPOINT: Brief Validation

```typescript
@skill:epci:breakpoint-system
  type: validation
  title: "Brief Validation"
  data: {
    brief: "{reformulated brief}",
    changes_from_original: ["{diff1}", "{diff2}"]
  }
  ask: {
    question: "Is this reformulation accurate?",
    header: "Validate",
    options: [
      {label: "Validate (Recommended)", description: "Proceed with this brief"},
      {label: "Adjust", description: "Make corrections"},
      {label: "Reject", description: "Start over"}
    ]
  }
```

### 7. Handle Rejection Loop

```
IF rejected:
  rejection_count++
  IF rejection_count >= 3:
    BREAKPOINT: "Multiple rejections - let's reformulate the topic entirely"
    → Return to step-01 with fresh input
  ELSE:
    → Iterate on reformulation
```

## Outputs

| Output | Destination |
|--------|-------------|
| `idea_refined` | Session state |
| `clarity_score` | Session state |
| `brief_v0` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Brief validated | → `step-02-framing.md` |
| Rejection loop (3x) | → `step-01-clarify.md` (restart) |
| `--no-clarify` flag | → `step-02-framing.md` |

## Error Handling

| Error | Resolution |
|-------|------------|
| @clarifier unavailable | Use built-in question generation |
| User timeout | Remind and wait |
| All questions skipped | Proceed with low confidence flag |
