---
name: epci:implement-auto
description: >-
  Standalone headless EPCI workflow for autonomous feature implementation via claude -p.
  Executes Explore-Plan-Code-Inspect without interaction. Produces incremental JSON output.
  3-level circuit breaker protects against token-burning. TDD enforced per component.
  Zero dependency on EPCI core skills — portable to any project via copy.
  Use when: automated pipeline, headless execution, pre-qualified STANDARD tasks, CI/CD.
  Triggers: pipeline automation, cron job, autonomous implementation, batch processing.
  Not for: interactive development (use /implement), quick fixes (use /quick), debugging (use /debug).
user-invocable: true
argument-hint: "<feature-slug> @<spec-path> [--validate-plan] [--with-review] [--skip-publish] [--auto-merge]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# implement-auto

Standalone headless EPCI skill for autonomous feature implementation without user interaction.

## Quick Start

```bash
claude --dangerously-skip-permissions  -p "/implement-auto feature-slug @path/to/spec.md" \
```

## Installation

Copy the entire `implement-auto/` directory into the target project:

```bash
cp -r implement-auto/ /path/to/project/.claude/skills/implement-auto/
```

No other dependencies required. The skill uses the target project's CLAUDE.md and rules/.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `feature-slug` | Yes | Kebab-case feature identifier |
| `@spec-path` | Yes | Path to spec/PRD file (Markdown) |
| `--validate-plan` | No | Invoke plan-validator (Opus) for plan review |
| `--with-review` | No | Invoke code-reviewer (Opus) in addition to self-review |
| `--skip-publish` | No | Skip push/PR/cleanup (orchestrator handles post-processing) |
| `--auto-merge` | No | Squash-merge PR immediately after creation (SUCCESS only). Ensures code is in base branch for dependent tasks |

## Output

JSON file at `{worktree}/.implement-auto-output.json`. See [references/output-json-schema.md](references/output-json-schema.md).

Status values: `SUCCESS`, `PARTIAL`, `FAILED`.

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion (headless mode)
- NEVER call EnterPlanMode
- NEVER display ASCII breakpoint boxes
- NEVER wait for user input
- ALWAYS write JSON output at each step transition
- ALWAYS follow step order sequentially
- ALWAYS enforce TDD per component (RED-GREEN-REFACTOR)
- ALWAYS apply circuit breaker rules on failure
- FOCUS on autonomous execution from start to finish

## Workflow

```
step-00-init-auto     Parse args, create worktree, Feature Doc, JSON init
       |
step-01-explore-auto  Explore codebase + sanity check (30% threshold)
       |
step-02-plan-auto     Create implementation plan (no breakpoint)
       |
step-03-code-auto     TDD implementation + circuit breaker 3 levels
       |
step-04-review-auto   Self-review checklist (+ optional --with-review)
       |
step-05-document-auto Feature Document completion + executive summary
       |
step-06-finish-auto   Final validation, commit, status determination
       |
step-07-output-auto   Final JSON write
       |
step-08-publish-auto  Push branch, create PR, cleanup worktree
```

## EXECUTION PROTOCOLS:

1. **Load** step-00-init-auto.md
2. **Execute** current step protocols completely
3. **Write** JSON output after step completion
4. **Evaluate** circuit breaker conditions
5. **Proceed** to next_step or abort if circuit breaker triggers

## Circuit Breaker (3 Levels)

| Level | Scope | Threshold | Action |
|-------|-------|-----------|--------|
| 1 | Component | 2 retries | Mark FAILED, skip to next |
| 2 | Task | 3 consecutive OR >50% | ABORT task, status FAILED |
| 3 | Timeout | External (orchestrator) | Kill process, read partial JSON |

See [references/circuit-breaker-rules.md](references/circuit-breaker-rules.md).

## TDD Rules

Self-contained TDD workflow: RED -> GREEN -> REFACTOR -> VERIFY.
No dependency on epci:tdd-enforcer. See [references/tdd-rules.md](references/tdd-rules.md).

## Self-Review

Built-in checklist covering tests, code quality, architecture, security basics.
See [references/review-checklist.md](references/review-checklist.md).

## Steps

| Step | Name | Phase | Description |
|------|------|-------|-------------|
| 00 | init-auto | - | Parse args, worktree, Feature Doc, JSON |
| 01 | explore-auto | [E] | Explore + sanity check |
| 02 | plan-auto | [P] | Implementation plan |
| 03 | code-auto | [C] | TDD + circuit breaker |
| 04 | review-auto | [I] | Self-review checklist |
| 05 | document-auto | - | Feature Document + summary |
| 06 | finish-auto | - | Finalization + commit |
| 07 | output-auto | - | Final JSON output |
| 08 | publish-auto | - | Push, PR, worktree cleanup |

## Step Files

- [steps/step-00-init-auto.md](steps/step-00-init-auto.md)
- [steps/step-01-explore-auto.md](steps/step-01-explore-auto.md)
- [steps/step-02-plan-auto.md](steps/step-02-plan-auto.md)
- [steps/step-03-code-auto.md](steps/step-03-code-auto.md)
- [steps/step-04-review-auto.md](steps/step-04-review-auto.md)
- [steps/step-05-document-auto.md](steps/step-05-document-auto.md)
- [steps/step-06-finish-auto.md](steps/step-06-finish-auto.md)
- [steps/step-07-output-auto.md](steps/step-07-output-auto.md)
- [steps/step-08-publish-auto.md](steps/step-08-publish-auto.md)

## Reference Files

- [references/tdd-rules.md](references/tdd-rules.md) — TDD workflow (self-contained)
- [references/circuit-breaker-rules.md](references/circuit-breaker-rules.md) — Circuit breaker logic
- [references/output-json-schema.md](references/output-json-schema.md) — JSON output contract
- [references/review-checklist.md](references/review-checklist.md) — Self-review items
- [references/feature-document-template.md](references/feature-document-template.md) — Feature Document

## Flags

| Flag | Effect |
|------|--------|
| `--validate-plan` | Invoke plan-validator (Opus) to review the plan before coding |
| `--with-review` | Invoke code-reviewer (Opus) after self-review for deep analysis |
| `--skip-publish` | Skip push, PR creation, and worktree cleanup (orchestrator handles) |
| `--auto-merge` | Immediately squash-merge PR (`gh pr merge --squash --delete-branch`) after creation. SUCCESS only — PARTIAL keeps draft PR, FAILED skips |

## Conventions

The skill relies on the target project's CLAUDE.md and .claude/rules/ for:
- Architecture patterns
- Naming conventions
- Test commands
- Code style

No stack skills are embedded. This makes the skill portable across any stack.

## Limitations

- No interactive breakpoints (by design)
- No team mode / multi-agent orchestration
- No complexity routing (always STANDARD)
- Timeout managed externally by orchestrator
- Self-review is lighter than full code-reviewer
- Auto-merge requires gh CLI installed + merge permissions on the repository. Merges immediately on SUCCESS only; PARTIAL status keeps the PR as draft
