---
name: step-04-review
description: Code review phase [I]
prev_step: steps/step-03-code.md
next_step: steps/step-05-document.md
conditional_next:
  - condition: "security_concerns == true"
    step: steps/step-04b-security.md
  - condition: "qa_needed == true"
    step: steps/step-04c-qa.md
---

# Step 04: Review [I]

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER auto-approve without thorough analysis
- 🔴 NEVER skip security consideration
- 🔴 NEVER ignore edge cases
- ✅ ALWAYS invoke @code-reviewer agent
- ✅ ALWAYS check for OWASP top 10 vulnerabilities
- ✅ ALWAYS verify test coverage meets target
- ✅ ALWAYS verify code follows identified patterns
- 🔵 YOU ARE A SKEPTICAL REVIEWER, not a defender
- 💭 FOCUS on what could go wrong, not what went right

## EXECUTION PROTOCOLS:

### 1. Invoke @code-reviewer (Opus)

Delegate code review to the code-reviewer agent:

```typescript
Task({
  subagent_type: "code-reviewer",
  prompt: `
## Files to Review
{modified_files_list}

## Original Requirements
{feature_requirements}

## Implementation Plan Summary
{plan_summary}

## Review Focus
- Code quality: patterns, naming, error handling
- Test coverage: target 70% minimum
- Security: OWASP Top 10 awareness
- Plan alignment: implementation matches plan

## Expected Output
Review report with:
- Files reviewed count
- Issues found (Critical/Important/Minor)
- Test coverage assessment
- Verdict: APPROVED / CHANGES_REQUIRED / SECURITY_REVIEW_NEEDED
  `
})
```

### 2. Process Review Results

Based on @code-reviewer verdict:
- If APPROVED: continue to breakpoint
- If CHANGES_REQUIRED: address findings before proceeding
- If SECURITY_REVIEW_NEEDED: proceed to step-04b-security

### 3. Verify Test Coverage

- Confirm coverage target met (min 70%)
- Identify any untested paths flagged by reviewer
- Check edge case coverage

### 4. Determine Additional Reviews

Based on review findings:
- Security review required? → step-04b-security
- QA validation required? → step-04c-qa
- Performance concerns? → note for documentation

## CONTEXT BOUNDARIES:

- This step expects: Implemented code, passing tests
- This step produces: Review findings, approval or revision requests

## REVIEW CHECKLIST:

```
### Code Quality
- [ ] Follows existing patterns
- [ ] Proper error handling
- [ ] No code duplication
- [ ] Clear naming
- [ ] No dead code

### Tests
- [ ] Coverage target met
- [ ] Edge cases covered
- [ ] Failure modes tested
- [ ] Integration tested

### Security
- [ ] No injection vulnerabilities
- [ ] Auth/authz correct
- [ ] No sensitive data exposure
- [ ] Input validation present

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No blocking operations in hot paths
```

## OUTPUT FORMAT:

```
## Code Review Results

### Summary
- Files reviewed: {N}
- Issues found: {N}
- Severity: {HIGH|MEDIUM|LOW|NONE}

### Findings
| # | Severity | File | Issue | Recommendation |
|---|----------|------|-------|----------------|
| 1 | {severity} | {file} | {issue} | {fix} |

### Test Coverage
- Achieved: {%}
- Target: {%}
- Status: {PASS|FAIL}

### Verdict
{APPROVED | CHANGES_REQUIRED | SECURITY_REVIEW_NEEDED | QA_NEEDED}
```

## BREAKPOINT:

```typescript
@skill:epci:breakpoint-system
  type: phase-transition
  title: "Code Review Complete [C→I]"
  data: {
    phase_completed: "code",
    phase_next: "inspect",
    summary: {
      duration: "{duration}",
      tasks_completed: {N},
      files_modified: ["{files}"],
      tests_status: "{passing}/{total} passing"
    },
    checkpoint_created: {
      id: "{feature_id}-checkpoint-code",
      resumable: true
    }
  }
  ask: {
    question: "Proceed with review outcome?",
    header: "Phase C→I",
    options: [
      {label: "Accept and Document (Recommended)", description: "Proceed to documentation phase"},
      {label: "Request Security Review", description: "Deep security audit needed"},
      {label: "Request QA Validation", description: "Additional QA testing needed"},
      {label: "Address Findings", description: "Fix issues before proceeding"}
    ]
  }
  suggestions: [
    {pattern: "coverage", text: "Coverage: {%}% achieved", priority: "P1"},
    {pattern: "issues", text: "{N} issues found ({severity})", priority: "P2"}
  ]
```

## NEXT STEP TRIGGER:

When review is approved and no additional reviews needed, proceed to `step-05-document.md`.

If security concerns identified, proceed to `step-04b-security.md`.

If QA validation needed, proceed to `step-04c-qa.md`.
