# Phase 3: Finalization — Detailed Process

> Reference for `/epci` Phase 3 detailed workflow

---

## Process Steps

### Step 1: Structured Commit Preparation

```
feat(scope): short description

- Detail 1
- Detail 2

Refs: docs/features/<slug>.md
```

### Step 2: Documentation (via @doc-generator)

- Generate/update README if new component
- Document API changes if applicable
- Update CHANGELOG

### Step 3: PR Preparation

- Create branch if not done
- Prepare PR template
- List reviewers

### Step 4: Learning Update (F08 - automatic)

- Save feature history to `.project-memory/history/features/{slug}.json`
- Trigger calibration with estimated vs actual times
- Update velocity metrics
- Record any corrections for pattern detection

---

## Output §3 Part 2 Format

**Use Edit tool** to **append** finalization content to §3.

**Path:** `docs/features/<slug>.md`

```markdown
### Documentation
- **@doc-generator**: 2 files updated
  - README.md (Configuration section)
  - CHANGELOG.md (v1.2.0)

### PR Ready
- Branch: `feature/user-email-validation`
- Tests: All passing
- Lint: Clean
- Docs: Up to date
```

---

## Generate Commit Context (MANDATORY)

Write `.epci-commit-context.json` to project root:

```json
{
  "source": "epci",
  "type": "<type from commit message>",
  "scope": "<scope from feature>",
  "description": "<description from plan>",
  "files": ["<list of modified files>"],
  "featureDoc": "docs/features/<slug>.md",
  "breaking": false,
  "ticket": null
}
```

**Display commit suggestion:**

```
+---------------------------------------------------------------------+
| CONTEXTE COMMIT PREPARE                                             |
+---------------------------------------------------------------------+
|                                                                     |
| Message propose:                                                    |
| {TYPE}({SCOPE}): {DESCRIPTION}                                      |
|                                                                     |
| Fichiers: {FILE_COUNT}                                              |
| Feature Document: docs/features/{slug}.md                           |
|                                                                     |
| -> Lancez /commit pour finaliser                                    |
| -> Ou /commit --auto-commit pour commit direct                      |
+---------------------------------------------------------------------+
```

**Note:** The `/commit` command handles:
- Pre-commit breakpoint with user confirmation
- Git commit execution
- Pre/post-commit hooks
- Context file cleanup after success

---

## Memory Update (MANDATORY)

**CRITICAL: Execute this hook before displaying completion message.**

```bash
python3 hooks/runner.py post-phase-3 --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<complexity>",
  "files_modified": ["<list of files>"],
  "estimated_time": "<estimated>",
  "actual_time": "<actual>",
  "commit_hash": "<hash or null>",
  "commit_status": "<committed|pending|cancelled>",
  "test_results": {"status": "passed", "count": <n>}
}'
```

**Why mandatory:**
- Saves feature to `.project-memory/history/features/`
- Updates velocity metrics for calibration
- Increments `features_completed` counter
- Required for `/memory` command accuracy

**Note:** Skip only if `--no-hooks` flag is active.

---

## Worktree Finalization (CONDITIONAL)

**Condition:** Execute only if current directory is a worktree.

**Detection:**
```bash
git rev-parse --git-dir 2>/dev/null | grep -q "worktrees"
```

**IF in worktree:**

```
+---------------------------------------------------------------------+
| WORKTREE DETECTED                                                   |
+---------------------------------------------------------------------+
|                                                                     |
| Feature complete dans worktree: {slug}                              |
|                                                                     |
| Pour merger dans develop et nettoyer:                               |
|   ./src/scripts/worktree-finalize.sh                                |
|                                                                     |
| Pour abandonner le worktree:                                        |
|   ./src/scripts/worktree-abort.sh                                   |
|                                                                     |
| Pour garder le worktree ouvert:                                     |
|   (aucune action requise)                                           |
|                                                                     |
+---------------------------------------------------------------------+
```

**IF NOT in worktree:** Skip silently.

---

## Completion Message

```
---
FEATURE COMPLETE

Feature Document finalized: docs/features/<slug>.md
- Phase 1: Plan validated
- Phase 2: Code implemented and reviewed
- Phase 3: Documentation and commit validation

Commit status: {COMMITTED | PENDING}
Next step: {Create PR | Manual commit then PR}

Tip: If .claude/ doesn't exist, run /rules to generate conventions
---
```

**Rules Suggestion:** If `.claude/` directory doesn't exist, suggest `/rules` command.

---

*Reference for epci.md Phase 3*
