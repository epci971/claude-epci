---
name: step-00-clarify
description: Input clarification for ambiguous bug reports
prev_step: null
next_step: steps/step-01-evidence.md
conditional_next:
  - condition: "clarity_score >= 0.6 OR --no-clarify"
    step: steps/step-01-evidence.md
    action: "skip clarification"
---

# Step 00: Clarify

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip if clarity_score < 0.6 (unless --no-clarify)
- ✅ ALWAYS calculate clarity score first
- ✅ ALWAYS use clarification-engine for questions
- ✅ ALWAYS clean voice input artifacts
- 💭 FOCUS on gathering just enough info to proceed

## EXECUTION PROTOCOLS:

### 1. Calculate Clarity Score

Evaluate input on 5 criteria (0-1 each):

| Criterion | Weight | High Score (1.0) | Low Score (0.0) |
|-----------|--------|------------------|-----------------|
| Error specificity | 0.25 | Exact error message | "it's broken" |
| Reproduction | 0.25 | Clear steps | "sometimes happens" |
| Context | 0.20 | When/where/who | No context |
| Expected behavior | 0.15 | Clear expectation | Unclear |
| Stack trace | 0.15 | Full trace | None |

```
clarity_score = sum(criterion * weight)

Example:
- Error: "TypeError: Cannot read property 'id'" → 0.9
- Reproduction: "after clicking submit" → 0.7
- Context: "on checkout page for logged users" → 0.8
- Expected: "should complete order" → 0.6
- Stack trace: "at CheckoutService.js:45" → 0.9

clarity_score = 0.9*0.25 + 0.7*0.25 + 0.8*0.20 + 0.6*0.15 + 0.9*0.15
             = 0.225 + 0.175 + 0.16 + 0.09 + 0.135
             = 0.785 → SKIP CLARIFICATION
```

### 2. Skip Conditions

Skip to step-01-evidence.md if ANY:
- `--no-clarify` flag provided
- `clarity_score >= 0.6`
- Input is pure stack trace
- Input is error code (e.g., "HTTP 500", "SQLSTATE[23000]")

### 3. Clean Voice Input (if needed)

Use `clarification-engine.clean_voice_input()` for dictation artifacts:

| Pattern | Cleaned |
|---------|---------|
| "uh", "um", "like" | removed |
| "period", "new line" | `.`, `\n` |
| "quote X quote" | `"X"` |
| repeated words | deduplicated |

### 4. Generate Clarification Questions

If `clarity_score < 0.6`, invoke `clarification-engine`:

```
clarification.generate_questions({
  input: user_input,
  missing: identify_gaps(criteria_scores),
  max_questions: 3,
  prioritize_by: "blocking_impact"
})
```

### 5. Present Questions via AskUserQuestion

Format questions for user interaction:

```typescript
AskUserQuestion({
  questions: [{
    question: "Can you provide the exact error message?",
    header: "Error",
    multiSelect: false,
    options: [
      { label: "I'll paste it now", description: "Paste error in follow-up" },
      { label: "No error message", description: "Silent failure" },
      { label: "I don't have access", description: "Can't reproduce currently" }
    ]
  }]
})
```

### 6. --turbo Mode

In turbo mode, use `@clarifier` agent (Haiku):

```
Task(
  subagent_type: "clarifier",
  prompt: "Analyze this bug report and generate 2-3 clarification questions: {input}"
)
```

## CONTEXT BOUNDARIES:

- This step expects: Raw user input (text or voice)
- This step produces: Clarified bug description with sufficient detail

## OUTPUT FORMAT:

```
## Clarification Assessment

Clarity Score: {0.XX}

| Criterion | Score | Notes |
|-----------|-------|-------|
| Error specificity | X.X | {note} |
| Reproduction | X.X | {note} |
| Context | X.X | {note} |
| Expected behavior | X.X | {note} |
| Stack trace | X.X | {note} |

Decision: {SKIP | CLARIFY}

[If CLARIFY: questions presented via AskUserQuestion]
```

## SKIP FORMAT:

```
## Clarification Skipped

Reason: {clarity >= 0.6 | --no-clarify flag | pure stack trace}
Clarity Score: {X.XX}

Proceeding to evidence gathering...
```

## NEXT STEP TRIGGER:

- If clarity >= 0.6 OR --no-clarify → step-01-evidence.md
- If clarity < 0.6 → wait for user response, then step-01-evidence.md
