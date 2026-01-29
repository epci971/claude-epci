---
name: step-07-complex
description: Route C - Full investigation for complex bugs
prev_step: steps/step-04-routing.md
next_step: steps/step-08-post.md
---

# Step 07: Complex Route

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip solution scoring
- 🔴 NEVER skip diagnostic breakpoint (unless --turbo)
- 🔴 NEVER skip code review (@code-reviewer)
- ✅ ALWAYS generate solution scoring matrix
- ✅ ALWAYS present breakpoint for user choice
- ✅ ALWAYS invoke relevant reviewers
- ✅ ALWAYS generate Debug Report (unless --no-report)
- 💭 FOCUS on systematic investigation, user validation

## EXECUTION PROTOCOLS:

### 1. Generate Solution Scoring Matrix

For each top hypothesis, generate solution options:

```
SOLUTION SCORING:

Scoring Criteria (25% each):
- Simplicity: How simple is the fix?
- Risk: What's the risk of regression?
- Time: Estimated implementation time?
- Maintainability: Long-term code quality impact?

Scoring Scale: 1-5 (5 = best)
```

@../references/solution-scoring.md
@../references/debug-report-template.md

See solution-scoring.md (imported above) for formula.

**Example Matrix:**

| Solution | Simplicity | Risk | Time | Maintain | Total |
|----------|------------|------|------|----------|-------|
| S1: Patch cache TTL | 4 | 5 | 5 | 3 | 4.25 |
| S2: Refactor cache layer | 2 | 3 | 2 | 5 | 3.00 |
| S3: Add invalidation hook | 3 | 4 | 3 | 4 | 3.50 |

### 2. BREAKPOINT: Diagnostic (OBLIGATOIRE sauf --turbo)

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 ROOT CAUSE ANALYSIS COMPLETE                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Root Cause: {top hypothesis}                                        │
│ Confidence: {confidence}%                                           │
│                                                                     │
│ Decision Tree: H1 > H2 > H3                                         │
│                                                                     │
│ SOLUTIONS (Ranked):                                                 │
│ ┌──────┬────────────────────────┬────────┬────────┬───────┐        │
│ │ ID   │ Solution               │ Effort │ Risk   │ Score │        │
│ ├──────┼────────────────────────┼────────┼────────┼───────┤        │
│ │ S1   │ {solution 1}           │ Low    │ Low    │ 4.25  │        │
│ │ S2   │ {solution 2}           │ Medium │ Medium │ 3.50  │        │
│ │ S3   │ {solution 3}           │ High   │ Low    │ 3.00  │        │
│ └──────┴────────────────────────┴────────┴────────┴───────┘        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] S1: {title} (Recommended) — Simple, low risk              │ │
│ │  [B] S2: {title} — Plus de travail, meilleur long-terme        │ │
│ │  [C] Détails — Afficher analyse complète                       │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

APPELLE AskUserQuestion({
  questions: [{
    question: "Quelle solution implémenter?",
    header: "Solution",
    multiSelect: false,
    options: [
      { label: "S1: {title} (Recommended)", description: "Simple, low risk" },
      { label: "S2: {title}", description: "Plus de travail, meilleur long-terme" },
      { label: "Détails", description: "Afficher analyse complète" }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 3. --turbo Mode: Skip Breakpoint

In turbo mode, auto-select best solution:

```
if --turbo AND solutions[0].confidence >= 70%:
  selected_solution = solutions[0]
  skip breakpoint
  proceed to implementation
```

### 4. Implement Selected Solution

TDD cycle via @implementer:

```
Task(
  subagent_type: "implementer",
  prompt: """
    Implement bug fix:

    ## Root Cause
    {hypothesis}

    ## Selected Solution
    {solution details}

    ## Files
    {files_to_investigate}

    ## TDD Mode
    Red-Green-Refactor-Verify (full cycle)

    ## Constraints
    - Add regression test
    - Follow existing patterns
    - Minimal scope creep
  """
)
```

### 5. Invoke Reviewers (Parallel)

After implementation, invoke reviewers:

```
REVIEWERS:

@code-reviewer (always):
- Check code quality
- Verify plan alignment
- Architecture review

@security-auditor (conditional):
- Triggered if files match: **/auth/**, **/security/**, **/password/**
- Or keywords: password, token, jwt, oauth, encrypt

@qa-reviewer (conditional):
- Triggered if >= 3 tests added
- Check test quality and coverage
```

**Parallel Invocation:**
```
Task(subagent_type: "code-reviewer", ...)
Task(subagent_type: "security-auditor", ...)  // if triggered
Task(subagent_type: "qa-reviewer", ...)       // if triggered
```

### 6. Generate Debug Report (unless --no-report)

Create report at `docs/debug/{slug}-{date}.md`:

See debug-report-template.md (imported above) for template.

```markdown
# Debug Report: {slug}

**Date**: {ISO-8601}
**Duration**: {minutes}
**Route**: COMPLEX

## Summary
{1-2 paragraph summary}

## Root Cause Analysis
### Hypotheses Investigated
{hypothesis tree}

### Root Cause
{final determination}

## Solution
{implementation details}

## Files Modified
{list with LOC changes}

## Tests Added
{test details}

## Lessons Learned
{what to remember}
```

### 7. Fallback Loop

If solution fails:

```
FALLBACK PROTOCOL:

if implementation fails:
  mark current solution as "failed"
  return to breakpoint with remaining solutions

if all solutions exhausted:
  generate new hypotheses based on findings
  OR escalate with specific questions
  OR suggest targeted Perplexity research
```

## CONTEXT BOUNDARIES:

- This step expects: COMPLEX routing or --full flag, ranked hypotheses
- This step produces: Validated fix with reviews and Debug Report

## OUTPUT FORMAT:

```
## Bug Fixed (Complex)

### Root Cause Analysis
- **Hypotheses Investigated**: {N}
- **Root Cause**: {final hypothesis}
- **Confidence**: {N}%

### Solution Implemented
- **Selected**: S1 - {title}
- **Score**: {N}/5.0

### TDD Cycle
- **RED**: Regression test written ✅
- **GREEN**: Fix implemented ✅
- **REFACTOR**: Code cleaned up ✅
- **VERIFY**: All tests pass ✅

### Files Modified
| File | Changes | LOC |
|------|---------|-----|
| `{path1}` | {description} | +{N} |
| `{path2}` | {description} | +{N} |

### Reviews
- **@code-reviewer**: {verdict}
- **@security-auditor**: {verdict | N/A}
- **@qa-reviewer**: {verdict | N/A}

### Debug Report
Generated: `docs/debug/{slug}-{date}.md`

Proceeding to post-debug phase.
```

## --no-report OUTPUT:

```
### Debug Report
Skipped (--no-report flag)
```

## NEXT STEP TRIGGER:

Proceed to step-08-post.md when:
- Solution implemented
- TDD cycle complete
- All reviews passed (or issues addressed)
- Debug Report generated (unless --no-report)
