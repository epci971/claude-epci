# Invocation Guide - When and How to Use Subagents

> Patterns for invoking native and custom subagents effectively

---

## Subagent Types

### Native Claude Code Subagents

Built-in agents provided by Claude Code with predefined capabilities.

| Agent | Model | Tools | Best For |
|-------|-------|-------|----------|
| `@Explore` | Haiku | Read-only | Quick codebase exploration |
| `@Plan` | Sonnet | Read-only | Research and planning |
| `general-purpose` | Sonnet | All | Complex implementation |

### Custom EPCI Subagents

Specialized agents created for EPCI workflows.

| Agent | Focus | Output |
|-------|-------|--------|
| `@plan-validator` | Plan quality | APPROVED/NEEDS_REVISION |
| `@code-reviewer` | Code quality | Review report |
| `@security-auditor` | Security | Vulnerability report |
| `@qa-reviewer` | Test quality | QA report |
| `@doc-generator` | Documentation | Generated docs |

---

## When to Use Subagents

### Use Subagents When

| Scenario | Recommended Agent |
|----------|-------------------|
| Need quick codebase scan | `@Explore` |
| Research before planning | `@Plan` |
| Validate implementation plan | `@plan-validator` |
| Review code quality | `@code-reviewer` |
| Audit security | `@security-auditor` |
| Review test quality | `@qa-reviewer` |
| Generate documentation | `@doc-generator` |
| Complex multi-step task | `general-purpose` |

### Don't Use Subagents When

| Scenario | Alternative |
|----------|-------------|
| Simple file read | Use `Read` directly |
| Basic grep/search | Use `Grep` directly |
| Single file modification | Use `Edit` directly |
| Linear straightforward task | Handle directly |

---

## Invocation Patterns

### Native Agent Invocation

```markdown
# In command or skill content:

**Explore codebase:**
Use @Explore with thoroughness "medium" to analyze the authentication module.

**Research phase:**
Use @Plan to research existing patterns for caching implementation.

**Complex implementation:**
Delegate to general-purpose agent to implement the feature.
```

### Custom Agent Invocation

```markdown
# Conditional invocation in workflow:

**After Phase 1 (Plan):**
Invoke @plan-validator with the implementation plan for validation.

**After Phase 2 (Code):**
Invoke @code-reviewer with the implemented code.
If security-sensitive files changed, also invoke @security-auditor.
If test files were created, invoke @qa-reviewer.

**Phase 3 (Finalize):**
Invoke @doc-generator to create documentation.
```

---

## Invocation Syntax

### Task Tool Invocation

```yaml
Task:
  subagent_type: "Explore"
  prompt: "Find all authentication patterns in this codebase"

Task:
  subagent_type: "general-purpose"
  prompt: "Implement the UserService class following the existing patterns"
```

### Reference Syntax in Commands

```markdown
## Process

### Step 1: Exploration
Use @Explore (quick) to identify relevant files.

### Step 2: Analysis
Use @Plan to research implementation approaches.

### Step 3: Validation
Invoke @plan-validator with the generated plan.
Wait for verdict before proceeding.

**BREAKPOINT**: If verdict is NEEDS_REVISION, revise and re-validate.
```

---

## Thoroughness Levels

### @Explore Levels

| Level | Scope | Use When |
|-------|-------|----------|
| `quick` | Surface scan | Know what you're looking for |
| `medium` | Moderate exploration | General understanding |
| `very thorough` | Deep analysis | Complex codebase, unknown structure |

### Choosing Thoroughness

```
Known file/function?
├── Yes → quick
└── No → Familiar with codebase?
         ├── Yes → medium
         └── No → very thorough
```

---

## Conditional Invocation

### Based on File Changes

```markdown
## Invoked Subagents

| Subagent | Condition |
|----------|-----------|
| `@code-reviewer` | Always |
| `@security-auditor` | If auth/*, api/*, or input handling changed |
| `@qa-reviewer` | If test complexity > threshold |
```

### Based on Complexity

```markdown
**Complexity-based invocation:**
- TINY: No subagent review
- SMALL: @code-reviewer only
- STANDARD: @code-reviewer + conditional @security-auditor
- LARGE: All reviewers
```

### Based on Verdict

```markdown
**Verdict-based flow:**

1. Invoke @plan-validator
2. If APPROVED → proceed to Phase 2
3. If NEEDS_REVISION → revise plan, re-invoke @plan-validator
4. Max 3 iterations, then escalate to user
```

---

## Parallel vs Sequential

### Sequential Invocation

Use when agents depend on each other's output:

```markdown
1. @plan-validator → Wait for verdict
2. If APPROVED → @code-reviewer
3. If code changes → @security-auditor
```

### Parallel Invocation

Use when agents are independent:

```markdown
After implementation, invoke in parallel:
- @code-reviewer
- @security-auditor
- @qa-reviewer

Aggregate verdicts: All must be APPROVED or APPROVED_WITH_NOTES.
```

---

## Error Handling

### Timeout Handling

```markdown
If subagent times out:
1. Retry once with simplified prompt
2. If still fails, log and continue with warning
3. Mark in report: "⚠️ [Agent] review skipped due to timeout"
```

### Rejection Handling

```markdown
If @plan-validator returns NEEDS_REVISION:
1. Extract issues from report
2. Attempt automatic fix for each issue
3. Re-invoke @plan-validator
4. After 3 attempts: escalate to user with accumulated issues
```

---

## EPCI Workflow Integration

### Phase 1: Analysis

```markdown
1. @Explore (medium) → Understand codebase
2. @Plan → Research approach
3. Generate implementation plan
4. @plan-validator → Validate plan

**Gate:** APPROVED to proceed
```

### Phase 2: Implementation

```markdown
1. Implement code following plan
2. @code-reviewer → Quality review
3. Conditional: @security-auditor → Security check
4. Conditional: @qa-reviewer → Test review

**Gate:** All APPROVED or APPROVED_WITH_NOTES
```

### Phase 3: Finalization

```markdown
1. @doc-generator → Generate documentation
2. Update Feature Document with all reports
3. Prepare commit with changelog
```

---

## Best Practices

### Do

| Practice | Benefit |
|----------|---------|
| Specify clear prompts | Better agent focus |
| Include context/scope | Relevant results |
| Handle verdicts programmatically | Automated flow |
| Log agent invocations | Traceability |

### Don't

| Anti-Pattern | Problem |
|--------------|---------|
| Invoke for trivial tasks | Overhead, latency |
| Ignore agent verdicts | Bypasses quality gate |
| Chain too many agents | Complexity, slow |
| Use wrong thoroughness | Incomplete or slow |

---

## Quick Reference

```
+------------------------------------------+
|         SUBAGENT INVOCATION               |
+------------------------------------------+
| NATIVE:                                   |
|   @Explore (quick|medium|very thorough)  |
|   @Plan (research)                        |
|   general-purpose (implement)             |
+------------------------------------------+
| CUSTOM:                                   |
|   @plan-validator  → Plan quality         |
|   @code-reviewer   → Code quality         |
|   @security-auditor → Security            |
|   @qa-reviewer     → Test quality         |
|   @doc-generator   → Documentation        |
+------------------------------------------+
| PATTERN: Invoke → Wait → Check verdict   |
| FLOW: APPROVED → continue | REJECTED → fix|
+------------------------------------------+
```
