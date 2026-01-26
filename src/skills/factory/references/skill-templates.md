# Skill Templates

Ready-to-use templates for creating user, core, and workflow skills in APEX style.

---

## APEX Style Templates

### Template: Simple User Skill (APEX)

For single-purpose skills under 200 lines.

```yaml
---
name: {skill-name}
description: >-
  {ACTION VERB}s {OBJECT} for {PURPOSE}.
  {ADDITIONAL CAPABILITY}.
  Use when: {SCENARIO 1}, {SCENARIO 2}.
  Triggers: {KEYWORD 1}, {KEYWORD 2}, {KEYWORD 3}.
  Not for: {EXCLUSION}.
user-invocable: true
disable-model-invocation: false
argument-hint: "[{param}]"
allowed-tools: {TOOLS}
---

# {Skill Name}

{One-line description of what this skill does.}

## Quick Start

```
/{skill-name} {example-arg}
```

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER {critical prohibition 1}
- :red_circle: NEVER {critical prohibition 2}
- :white_check_mark: ALWAYS {critical requirement 1}
- :white_check_mark: ALWAYS {critical requirement 2}
- :large_blue_circle: {posture directive}
- :thought_balloon: {focus directive}

## EXECUTION PROTOCOLS:

1. **{Verb 1}** {description}
2. **{Verb 2}** {description}
3. **{Verb 3}** {description}
4. **{Verb 4}** {description}

## CONTEXT BOUNDARIES:

- IN scope: {what's included}
- OUT scope: {what's excluded}

## OUTPUT FORMAT:

{Expected output specification}

## BREAKPOINT (if user decision needed):

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — {Title}                                             │
├─────────────────────────────────────────────────────────────────────┤
│ {Context summary}                                                   │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. {Option 1} (Recommended)                                   │ │
│ │  2. {Option 2}                                                 │ │
│ │  3. {Option 3}                                                 │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## Limitations

This skill does NOT:
- {Limitation 1}
- {Limitation 2}
```

---

### Template: Standard User Skill (APEX)

For multi-step skills with references and phases.

```yaml
---
name: {skill-name}
description: >-
  {ACTION VERB}s {OBJECT} for {PURPOSE}.
  {ADDITIONAL CAPABILITY}.
  Use when: {SCENARIO 1}, {SCENARIO 2}.
  Triggers: {KEYWORD 1}, {KEYWORD 2}, {KEYWORD 3}.
  Not for: {EXCLUSION}.
user-invocable: true
disable-model-invocation: false
argument-hint: "[{param}]"
allowed-tools: {TOOLS}
---

# {Skill Name}

{One-line description.}

## Quick Start

```
/{skill-name} {example}
```

## Modes

| Mode | Description | Flag |
|------|-------------|------|
| Default | {default behavior} | - |
| {Mode 2} | {description} | `--{flag}` |

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER {critical prohibition 1}
- :red_circle: NEVER {critical prohibition 2}
- :white_check_mark: ALWAYS {critical requirement 1}
- :white_check_mark: ALWAYS {critical requirement 2}
- :no_entry: FORBIDDEN {hard block}
- :large_blue_circle: {posture directive}
- :thought_balloon: {focus directive}

## EXECUTION PROTOCOLS:

### Phase 1: {Phase Name}

1. **{Verb}** {description}
2. **{Verb}** {description}

### Phase 2: {Phase Name}

1. **{Verb}** {description}
2. **{Verb}** {description}

## CONTEXT BOUNDARIES:

- IN scope: {what's included}
- OUT scope: {what's excluded}

## Decision Tree

```
IF {condition}:
  → {action 1}
ELSE IF {condition}:
  → {action 2}
ELSE:
  → {default action}
```

## OUTPUT FORMAT:

{Expected output specification}

## Reference Files

- [detailed-guide.md](references/detailed-guide.md) — Full documentation
- [examples.md](references/examples.md) — More examples

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| {Error 1} | {cause} | {fix} |
| {Error 2} | {cause} | {fix} |

## Limitations

This skill does NOT:
- {Limitation 1}
- {Limitation 2}
- {Limitation 3}
```

---

## Workflow Templates (--workflow)

### Template: Workflow SKILL.md (Router)

Entry point for workflow skills that routes to steps.

```yaml
---
name: {skill-name}
description: >-
  {ACTION VERB}s {OBJECT} through multi-phase workflow.
  {ADDITIONAL CAPABILITY}.
  Use when: {SCENARIO 1}, {SCENARIO 2}.
  Triggers: {KEYWORD 1}, {KEYWORD 2}, {KEYWORD 3}.
  Not for: {EXCLUSION}.
user-invocable: true
disable-model-invocation: false
argument-hint: "[{param}]"
allowed-tools: {TOOLS}
---

# {Skill Name}

{One-line description.}

## Quick Start

```
/{skill-name} {example}
```

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER execute steps out of order
- :red_circle: NEVER skip breakpoints
- :white_check_mark: ALWAYS start with step-00-init.md
- :white_check_mark: ALWAYS follow next_step from each step
- :white_check_mark: ALWAYS complete current step before proceeding

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoint if specified in step
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: {what's included}
- OUT scope: {what's excluded}

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    {SKILL NAME} WORKFLOW                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Step 00: INIT                                                    │
│  └─ {init description}                                            │
│     └─ Conditional: {condition} → step-00b                        │
│                                                                   │
│  Step 01: {PHASE 1}                                               │
│  └─ {phase 1 description}                                         │
│                                                                   │
│  Step 02: {PHASE 2}                                               │
│  └─ {phase 2 description}                                         │
│                                                                   │
│  Step 99: FINISH                                                  │
│  └─ {finalization}                                                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Steps

| Step | Name | Description |
|------|------|-------------|
| 00 | init | {description} |
| 00b | {variant} | {conditional description} |
| 01 | {phase1} | {description} |
| 02 | {phase2} | {description} |
| 99 | finish | {description} |

## Reference Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-{phase1}.md](steps/step-01-{phase1}.md) — Phase 1
- [steps/step-02-{phase2}.md](steps/step-02-{phase2}.md) — Phase 2
- [steps/step-99-finish.md](steps/step-99-finish.md) — Finalization

## Limitations

This skill does NOT:
- {Limitation 1}
- {Limitation 2}
```

---

### Template: Step File

Individual step file for workflow skills.

```yaml
---
name: step-XX-{name}
description: {short description}
prev_step: steps/step-XX-{prev}.md
next_step: steps/step-XX-{next}.md
conditional_next:
  - condition: "{expression}"
    step: steps/step-XXb-{variant}.md
---

# Step XX: {Name}

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER {critical prohibition for this step}
- :white_check_mark: ALWAYS {critical requirement for this step}
- :large_blue_circle: {posture for this step}
- :thought_balloon: {focus for this step}

## EXECUTION PROTOCOLS:

1. **{Verb}** {action description}
2. **{Verb}** {action description}
3. **{Verb}** {action description}

## CONTEXT BOUNDARIES:

- This step expects: {input requirements}
- This step produces: {output}

## OUTPUT FORMAT:

{Expected output from this step}

## BREAKPOINT (if applicable):

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: BREAKPOINT — {Title}                                             │
├─────────────────────────────────────────────────────────────────────┤
│ {Context summary from this step}                                    │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. {Option 1} (Recommended)                                   │ │
│ │  2. {Option 2}                                                 │ │
│ │  3. {Option 3}                                                 │ │
│ │  4. [Free response]                                            │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## NEXT STEP TRIGGER:

When {condition is met}, proceed to `next_step`.

If {alternative condition}, proceed to `conditional_next[0].step`.
```

---

### Template: Init Step (step-00-init.md)

```yaml
---
name: step-00-init
description: Initialize workflow and detect context
prev_step: null
next_step: steps/step-01-{phase1}.md
conditional_next:
  - condition: "complexity == TINY or complexity == SMALL"
    step: steps/step-00b-{quick-path}.md
---

# Step 00: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip context detection
- :red_circle: NEVER proceed without valid input
- :white_check_mark: ALWAYS validate input parameters
- :white_check_mark: ALWAYS detect complexity level

## EXECUTION PROTOCOLS:

1. **Parse** input arguments
2. **Validate** required parameters present
3. **Detect** complexity/context
4. **Route** to appropriate next step

## CONTEXT BOUNDARIES:

- This step expects: User input, arguments
- This step produces: Validated context, complexity level

## OUTPUT FORMAT:

```
Context:
- Input: {parsed input}
- Complexity: {TINY|SMALL|STANDARD|LARGE}
- Route: {next step path}
```

## NEXT STEP TRIGGER:

When context is validated, proceed to `next_step`.

If complexity is TINY or SMALL, proceed to quick path.
```

---

### Template: Finish Step (step-99-finish.md)

```yaml
---
name: step-99-finish
description: Finalize workflow and generate summary
prev_step: steps/step-XX-{last-phase}.md
next_step: null
---

# Step 99: Finish

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER skip final validation
- :white_check_mark: ALWAYS verify all outputs generated
- :white_check_mark: ALWAYS present completion summary

## EXECUTION PROTOCOLS:

1. **Verify** all expected outputs exist
2. **Validate** output quality/completeness
3. **Generate** completion summary
4. **Present** next steps (if any)

## CONTEXT BOUNDARIES:

- This step expects: All previous step outputs
- This step produces: Final summary, completion status

## OUTPUT FORMAT:

```
## Workflow Complete

:white_check_mark: {Output 1 description}
:white_check_mark: {Output 2 description}
:white_check_mark: {Output 3 description}

### Summary
- {Key result 1}
- {Key result 2}

### Next Steps
1. {Recommended action}
2. {Optional action}
```

## NEXT STEP TRIGGER:

Workflow complete. No next step.
```

---

## Core Skill Templates

### Template: Core Component (APEX)

For internal skills (user-invocable: false).

```yaml
---
name: {component-name}
description: >-
  {CAPABILITY DESCRIPTION}. Internal component for EPCI v6.0.
  Use when: {internal trigger conditions}.
  Not for: direct user invocation.
user-invocable: false
disable-model-invocation: false
allowed-tools: {TOOLS}
---

# {Component Name}

Internal component for {purpose}.

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER expose internal state to user
- :white_check_mark: ALWAYS validate inputs
- :white_check_mark: ALWAYS return structured output

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `{function1}()` | {description} | {input} | {output} |
| `{function2}()` | {description} | {input} | {output} |

## EXECUTION PROTOCOLS:

1. **Receive** input from calling skill
2. **Validate** input structure
3. **Process** according to function
4. **Return** structured output

## CONTEXT BOUNDARIES:

- IN scope: {component responsibilities}
- OUT scope: {what it doesn't handle}

## Data Schema

```json
{
  "field1": "type",
  "field2": "type"
}
```

## Limitations

This component does NOT:
- {Limitation 1}
- {Limitation 2}
```

---

## File Structure Examples

### Simple Structure
```
skills/{name}/
└── SKILL.md
```

### Standard Structure
```
skills/{name}/
├── SKILL.md
└── references/
    ├── guide.md
    └── examples.md
```

### Workflow Structure
```
skills/{name}/
├── SKILL.md                    # Router
├── steps/
│   ├── step-00-init.md
│   ├── step-00b-quick.md       # Optional conditional
│   ├── step-01-{phase1}.md
│   ├── step-02-{phase2}.md
│   └── step-99-finish.md
└── references/
    └── {domain}.md
```

### Core Structure
```
skills/core/{name}/
└── SKILL.md
```

---

## TDD Integration Template

For implementation skills (implement, quick), include this TDD integration section.

### When to Include TDD

| Skill Type | TDD Required | Notes |
|------------|--------------|-------|
| `/implement` | Yes | Full RED-GREEN-REFACTOR cycle |
| `/quick` | Optional | For STANDARD+ complexity only |
| `/debug` | Optional | When adding regression tests |
| `/improve`, `/refactor` | No | Behavior preservation, existing tests |

### TDD Section Template

Add this section to implementation skills:

```markdown
## TDD Integration

This skill follows the TDD workflow via `@skill:tdd-enforcer`.

### TDD Phases

| Phase | Action | Validation |
|-------|--------|------------|
| RED | Write failing test first | Test must fail with expected error |
| GREEN | Implement minimal code | Test passes, nothing more |
| REFACTOR | Clean up code | All tests still pass |

### TDD Rules

- :red_circle: NEVER write implementation before test
- :red_circle: NEVER skip the RED phase
- :white_check_mark: ALWAYS run test after each phase
- :white_check_mark: ALWAYS commit after GREEN and REFACTOR

### TDD Breakpoint

After each phase, verify:

┌─────────────────────────────────────────────────────────────────────┐
│ :pause_button: TDD CHECKPOINT — {Phase} Complete                                   │
├─────────────────────────────────────────────────────────────────────┤
│ Phase: {RED|GREEN|REFACTOR}                                         │
│ Test status: {FAIL (expected) | PASS}                               │
│ Next: {Proceed to next phase | Repeat current phase}                │
│                                                                     │
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  1. Proceed to {next phase}                                    │ │
│ │  2. Review current implementation                              │ │
│ │  3. Adjust test/code                                           │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Skill Reference

```markdown
## Core Skills Integration

| Core Skill | Purpose |
|------------|---------|
| `@skill:tdd-enforcer` | Enforce RED-GREEN-REFACTOR cycle |
| `@skill:state-manager` | Track TDD phase progress |
| `@skill:breakpoint-system` | Phase transition checkpoints |
```

---

## Checklist Before Using Template

- [ ] Choose appropriate template for skill type
- [ ] Replace all `{placeholders}`
- [ ] Verify MANDATORY EXECUTION RULES section present
- [ ] Verify EXECUTION PROTOCOLS are numbered
- [ ] Verify CONTEXT BOUNDARIES defined
- [ ] Max 5 :red_circle: NEVER rules
- [ ] Max 5 :white_check_mark: ALWAYS rules
- [ ] Description follows formula (< 1024 chars)
- [ ] Add specific examples
- [ ] Define clear limitations
- [ ] Remove unused sections
- [ ] Include TDD section if implementation skill
