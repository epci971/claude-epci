---
name: step-00-init-auto
description: Parse arguments, detect complexity, create worktree, Feature Document, and initialize JSON output
prev_step: null
next_step: steps/step-01-explore-auto.md
conditional_next:
  - condition: "invalid_spec or spec_not_found"
    step: steps/step-07-output-auto.md
  - condition: "plan_path provided"
    step: steps/step-03-code-auto.md
---

# Step 00: Init (Auto)

## Reference Files

@../references/output-json-schema.md
@../references/feature-document-template.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER display breakpoint boxes
- ALWAYS parse and validate all arguments
- ALWAYS detect complexity via epci:complexity-calculator
- ALWAYS create worktree from origin's default branch (dynamically detected)
- ALWAYS create Feature Document
- ALWAYS initialize JSON output file

## EXECUTION PROTOCOLS:

### 1. Parse Input Arguments

Extract from the invocation prompt:

- `feature-slug` (required) — kebab-case identifier
- `@spec-path` (conditionally required) — path to spec/PRD file
- `@plan-path` (optional) — path to Claude Code plan (.claude/plans/*.md)
- `--skip-plan-validation` (optional) — skip @plan-validator
- `--skip-review` (optional) — skip @code-reviewer (keep self-review)
- `--skip-security` (optional) — skip @security-auditor
- `--skip-qa` (optional) — skip @qa-reviewer
- `--skip-publish` (optional) — skip push/PR/cleanup
- `--auto-merge` (optional) — enable auto-merge after PR creation

Store in execution context:

```
context = {
  feature_slug: string,
  spec_path: string | null,
  plan_path: string | null,
  complexity: "STANDARD" | "LARGE",
  flag_skip_plan_validation: boolean,
  flag_skip_review: boolean,
  flag_skip_security: boolean,
  flag_skip_qa: boolean,
  flag_skip_publish: boolean,
  flag_auto_merge: boolean
}
```

### 2. Validate Input

Perform these checks sequentially:

1. **feature-slug format**: Must be kebab-case (lowercase, hyphens, no spaces)
   - If invalid: Write FAILED JSON with exit_reason "invalid_slug", go to step-07

2. **Input path**: Either @spec-path or @plan-path must be provided
   - If @plan-path provided: Verify file exists and is readable
     - If not found: Write FAILED JSON with exit_reason "plan_not_found", go to step-07
   - If @spec-path provided: Verify file exists and is readable
     - If not found: Write FAILED JSON with exit_reason "spec_not_found", go to step-07
     - If empty: Write FAILED JSON with exit_reason "invalid_spec", go to step-07
   - If neither provided: Write FAILED JSON with exit_reason "no_input_path", go to step-07

3. **Git status**: Verify we're in a git repository
   - If not: Write FAILED JSON with exit_reason "not_git_repo", go to step-07

### 3. Read Input & Detect Complexity

**If @plan-path provided (PLAN-FIRST workflow):**
- Read plan file content
- Extract components, files to modify/create, estimated scope
- Set `workflow_mode = "plan-first"`
- Steps 01 (explore) and 02 (plan) will be SKIPPED

**If @spec-path provided (SPEC-FIRST workflow):**
- Read spec file content. Extract:
  - **Objective**: Main goal of the feature
  - **Acceptance criteria**: Success conditions
  - **Technical context**: Stack, constraints, dependencies
  - **Scope**: What's in/out
- If spec is unstructured, extract what's available
- Set `workflow_mode = "spec-first"`

**Complexity Detection:**
- Invoke `epci:complexity-calculator` with extracted scope information
- Record detected complexity (STANDARD or LARGE)
- This affects:
  - Coverage targets: STANDARD (70%/60%) vs LARGE (80%/70%)
  - Security review: mandatory for LARGE
  - QA review threshold: lower for LARGE
- Store `complexity` in execution context

### 4. Create Git Worktree

Create an isolated worktree for this feature:

```bash
git fetch origin
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || echo "main")
git worktree add ../worktrees/{feature-slug} -b feature/{feature-slug} origin/$DEFAULT_BRANCH
```

If worktree already exists:
- Check if branch exists: `git branch --list feature/{feature-slug}`
- If exists and clean: reuse it
- If exists and dirty: log warning, reuse anyway

Change working context to worktree path.

### 5. Create Feature Document

Generate timestamp: `YYYYMMDD-HHmmss`

Create directory:
```bash
mkdir -p docs/features
```

Write Feature Document at `docs/features/{feature-slug}-{timestamp}.md` using the template from feature-document-template.md reference.

Fill sections:
- §0 Metadata: slug, complexity, date, branch, spec source, status=IN_PROGRESS, source=implement-auto
- §1 Contexte & Objectif: objective, technical context, acceptance criteria (from spec or plan)
- Remaining sections: placeholder text

Store `feature_doc_path` for all subsequent steps.

### 6. Initialize JSON Output

Write initial JSON to `{worktree_path}/.implement-auto-output.json`:

```json
{
  "$schema": "implement-auto-output-v1",
  "version": 1,
  "timestamp": "{ISO-8601}",
  "status": null,
  "exit_reason": null,
  "feature": {
    "slug": "{feature-slug}",
    "branch": "feature/{feature-slug}",
    "spec_source": "{spec-path or plan-path}",
    "complexity": "{STANDARD or LARGE}"
  },
  "phases": {
    "completed": ["init"],
    "failed": [],
    "current": "{explore or code}",
    "skipped": [],
  },
  "plan": {
    "total_components": 0,
    "planner_used": false,
    "validator_verdict": null,
    "components": []
  },
  "metrics": {
    "files_created": 0,
    "files_modified": 0,
    "tests_added": 0,
    "tests_passing": 0,
    "tests_failing": 0
  },
  "checks": {
    "tests": { "status": "pending", "count": 0, "failures": 0 },
    "self_review": {
      "status": "pending",
      "items_checked": 0,
      "items_passed": 0,
      "items_warned": 0,
      "findings": []
    },
    "deep_review": { "status": "skip", "verdict": null, "findings_count": 0, "critical_count": 0, "skipped_reason": "pending" },
    "security_review": { "status": "skip", "verdict": null, "vulnerabilities": 0, "owasp_categories": [], "skipped_reason": "pending" },
    "qa_review": { "status": "skip", "verdict": null, "ac_passed": 0, "ac_total": 0, "defects_found": 0, "skipped_reason": "pending" }
  },
  "feature_doc": "{feature_doc_path}",
  "errors": [],
  "warnings": []
}
```

If `workflow_mode == "plan-first"`:
- Set `phases.skipped = ["explore", "plan"]`
- Set `phases.current = "code"`

### 7. Log Initialization

Output to stdout (for pipeline logging):

```
[implement-auto] Init complete
  Feature: {feature-slug}
  Complexity: {STANDARD|LARGE}
  Input: {spec-path or plan-path}
  Workflow: {spec-first or plan-first}
  Worktree: {worktree_path}
  Branch: feature/{feature-slug}
  Feature Doc: {feature_doc_path}
  Flags: skip-plan-validation={flag}, skip-review={flag}, skip-security={flag}, skip-qa={flag}, skip-publish={flag}, auto-merge={flag}
```

## CONTEXT BOUNDARIES:

- This step expects: User prompt with feature-slug and @spec-path or @plan-path
- This step produces: Worktree, Feature Document, initial JSON, execution context with complexity

## NEXT STEP TRIGGER:

- If `workflow_mode == "plan-first"`: skip to step-03-code-auto.md (mark explore + plan as skipped)
- If `workflow_mode == "spec-first"`: proceed to step-01-explore-auto.md
- On validation failure: jump to step-07-output-auto.md with FAILED status
