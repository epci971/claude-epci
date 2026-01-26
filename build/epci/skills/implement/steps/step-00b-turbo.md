---
name: step-00b-turbo
description: Redirect TINY/SMALL tasks to /quick skill
prev_step: steps/step-00-init.md
next_step: null
---

# Step 00b: Turbo Redirect

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER force full EPCI for TINY/SMALL tasks
- :white_check_mark: ALWAYS inform user of redirect reason
- :white_check_mark: ALWAYS preserve context for /quick
- :thought_balloon: FOCUS on smooth handoff to /quick

## EXECUTION PROTOCOLS:

1. **Inform** user of complexity assessment
   - Explain why /quick is more appropriate
   - Show detected complexity level

2. **Preserve** context
   - Feature slug
   - Spec path if provided
   - Any parsed requirements

3. **Invoke** /quick skill
   - Pass feature-slug
   - Pass spec reference

## CONTEXT BOUNDARIES:

- This step expects: Validated TINY or SMALL complexity
- This step produces: Handoff to /quick skill

## OUTPUT FORMAT:

```
## Redirecting to /quick

Detected complexity: {TINY|SMALL}
Reason: Task scope is small enough for streamlined workflow

Invoking: /quick {feature-slug} {@spec-path}
```

## NEXT STEP TRIGGER:

This step terminates the /implement workflow.
Control passes to /quick skill.
