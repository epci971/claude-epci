---
name: step-00-init-auto
description: Parse arguments, create worktree, Feature Document, and initialize JSON output
prev_step: null
next_step: steps/step-01-explore-auto.md
conditional_next:
  - condition: "invalid_spec or spec_not_found"
    step: steps/step-07-output-auto.md
---

# Step 00: Init (Auto)

## Reference Files

@../references/output-json-schema.md
@../references/feature-document-template.md

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- NEVER display breakpoint boxes
- ALWAYS parse and validate all arguments
- ALWAYS create worktree from origin's default branch (dynamically detected)
- ALWAYS create Feature Document
- ALWAYS initialize JSON output file

## EXECUTION PROTOCOLS:

### 1. Parse Input Arguments

Extract from the invocation prompt:

- `feature-slug` (required) — kebab-case identifier
- `@spec-path` (required) — path to spec/PRD file
- `--validate-plan` (optional) — enable plan validation with Opus
- `--with-review` (optional) — enable deep code review with Opus
- `--skip-publish` (optional) — skip push/PR/cleanup (orchestrator handles)
- `--auto-merge` (optional) — enable auto-merge after PR creation

Store in execution context:

```
context = {
  feature_slug: string,
  spec_path: string,
  flag_validate_plan: boolean,
  flag_with_review: boolean,
  flag_skip_publish: boolean,
  flag_auto_merge: boolean
}
```

### 2. Validate Input

Perform these checks sequentially:

1. **feature-slug format**: Must be kebab-case (lowercase, hyphens, no spaces)
   - If invalid: Write FAILED JSON with exit_reason "invalid_slug", go to step-07

2. **spec-path exists**: Read the file at spec_path
   - If not found: Write FAILED JSON with exit_reason "spec_not_found", go to step-07
   - If empty: Write FAILED JSON with exit_reason "invalid_spec", go to step-07

3. **Git status**: Verify we're in a git repository
   - If not: Write FAILED JSON with exit_reason "not_git_repo", go to step-07

### 3. Read Spec

Read the spec file content. Extract:

- **Objective**: Main goal of the feature
- **Acceptance criteria**: Success conditions
- **Technical context**: Stack, constraints, dependencies
- **Scope**: What's in/out

If spec is unstructured, extract what's available and proceed.

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
- Metadata: slug, date, branch, spec source, status=IN_PROGRESS, mode=implement-auto
- Objectif: extracted from spec
- Criteres d'acceptation: extracted from spec as checklist
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
    "spec_source": "{spec-path}"
  },
  "phases": {
    "completed": ["init"],
    "failed": [],
    "current": "explore",
    "skipped": []
  },
  "plan": {
    "total_components": 0,
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
    }
  },
  "feature_doc": "{feature_doc_path}",
  "errors": [],
  "warnings": []
}
```

### 7. Log Initialization

Output to stdout (for pipeline logging):

```
[implement-auto] Init complete
  Feature: {feature-slug}
  Spec: {spec-path}
  Worktree: {worktree_path}
  Branch: feature/{feature-slug}
  Feature Doc: {feature_doc_path}
  Flags: validate-plan={flag}, with-review={flag}, skip-publish={flag}, auto-merge={flag}
```

## CONTEXT BOUNDARIES:

- This step expects: User prompt with feature-slug and @spec-path
- This step produces: Worktree, Feature Document, initial JSON, execution context

## NEXT STEP TRIGGER:

On success, proceed to step-01-explore-auto.md.
On validation failure, jump to step-07-output-auto.md with FAILED status.
