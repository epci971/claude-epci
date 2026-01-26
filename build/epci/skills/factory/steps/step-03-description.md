# Step 03: Description Engineering

> Craft optimized description using formula for maximum trigger accuracy.

## Trigger

- Completion of step-02-architecture.md

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From step-02 | Yes |
| Purpose | From step-01 | Yes |
| Triggers | From step-01 | Yes |
| Scope | From step-01 | Yes |

## Protocol

### 1. Apply Description Formula

```
DESCRIPTION = [CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

**Components:**

| Component | Purpose | Example |
|-----------|---------|---------|
| CAPABILITIES | What it does (action verb) | "Generates API documentation" |
| USE CASES | When to use | "Use when documenting endpoints" |
| TRIGGERS | Natural phrases | "Triggers: API docs, document API" |
| BOUNDARIES | What it doesn't do | "Not for: internal docs" |

### 2. Generate Draft Description

Based on collected data:

```python
def generate_description(purpose, triggers, scope):
    # Capability: Start with action verb
    capability = extract_action_verb(purpose) + " " + extract_object(purpose)

    # Use cases: From scope.in
    use_cases = "Use when: " + ", ".join(scope["in"][:3])

    # Triggers: Natural phrases
    trigger_phrases = "Triggers: " + ", ".join(triggers[:5])

    # Boundaries: From scope.out
    boundaries = "Not for: " + ", ".join(scope["out"][:2])

    return f"{capability}. {use_cases}. {trigger_phrases}. {boundaries}."
```

### 3. Validate Description

**Rules:**
- Length: 50-150 words (< 1024 characters)
- Trigger words: Include 3-5 natural phrases
- Specificity: Avoid generic terms ("helper", "utility", "tool")
- Action verbs: Start with what it does

**Validation Checks:**

| Check | Pass | Fail |
|-------|------|------|
| Length < 1024 chars | Continue | Shorten |
| Has 3+ triggers | Continue | Add triggers |
| No generic terms | Continue | Replace terms |
| Starts with action verb | Continue | Rewrite opening |

### 4. Present Draft for Review

```
┌─────────────────────────────────────────────────────────────────┐
│ [DESCRIPTION] Draft for Review                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ description: >-                                                 │
│   {generated description}                                       │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│ Length: {N} chars / 1024 max                                    │
│ Triggers: {count} identified                                    │
│ Validation: {PASS|WARN: issues}                                 │
│                                                                  │
│ [Accept] [Edit] [Regenerate]                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Handle User Edits

If user selects [Edit]:
- Show current description in editable format
- Accept modifications
- Re-validate after changes

### 6. Store Final Description

```json
{
  "collected": {
    "description": "<final validated description>",
    "description_length": N,
    "description_triggers": ["<extracted triggers>"]
  }
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| Validated description | Session state |
| Description metrics | Session state |

## Next Step

→ `step-04-workflow.md`

## Reference Files

- [references/description-formulas.md](../references/description-formulas.md) — Description patterns and examples

## Examples

**Good Description:**
```yaml
description: >-
  Generates comprehensive API documentation from code.
  Extracts endpoints, parameters, responses, and examples.
  Use when: documenting REST APIs, creating OpenAPI specs,
  updating endpoint docs. Triggers: API docs, document API,
  endpoint documentation. Not for: internal code docs.
```

**Bad Description:**
```yaml
description: "Documentation helper"  # Too vague, won't trigger
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Description too long | Auto-shorten, prioritize triggers |
| No clear triggers | Extract from purpose, ask user |
| Generic terms detected | Suggest specific alternatives |
