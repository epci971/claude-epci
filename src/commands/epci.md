---
description: >-
  Complete EPCI workflow in 3 phases for STANDARD and LARGE features.
  Phase 1: Analysis and planning. Phase 2: TDD implementation.
  Phase 3: Finalization and documentation. Includes breakpoints between phases.
argument-hint: "[--large] [--think|--think-hard|--ultrathink] [--safe] [--wave] [--sequential] [--parallel] [--uc] [--dry-run] [--continue]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI — Complete Workflow

## Overview

Structured workflow in 3 phases with validation at each step.
Generates a Feature Document as traceability thread.

## Arguments

### Workflow Control

| Argument | Description |
|----------|-------------|
| `--large` | Alias for `--think-hard --wave` (backward compatible) |
| `--continue` | Continue from last phase (resume after interruption) |
| `--dry-run` | Simulate workflow without making changes |

### Thinking Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--think` | Standard analysis (~4K tokens) | 3-10 files |
| `--think-hard` | Deep analysis (~10K tokens) | >10 files, refactoring |
| `--ultrathink` | Critical analysis (~32K tokens) | Never (explicit only) |

### Safety Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--safe` | Maximum validations, extra confirmations | Sensitive files |
| `--fast` | Skip optional validations | Never |

### Output Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--uc` | Ultra-compressed output (30-50% reduction) | context > 75% |
| `--verbose` | Full detailed output | Never |

### Orchestration Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--wave` | Enable multi-wave DAG orchestration | complexity > 0.7 |
| `--wave-strategy` | `progressive` (default) or `systematic` | With --wave |
| `--sequential` | Force sequential agent execution | Never |
| `--parallel` | Force all agents in parallel (ignores DAG) | Never |

**Flag Reference:** See `src/settings/flags.md` for complete documentation.

## Feature Document

The Feature Document is created by `/epci-brief` at: `docs/features/<feature-slug>.md`

```markdown
# Feature Document — [Title]

## §1 — Functional Brief
[Created by /epci-brief with thorough exploration]

## §2 — Implementation Plan
[Generated in Phase 1]

## §3 — Implementation
[Updated in Phase 2]

## §4 — Finalization
[Completed in Phase 3]
```

**Prerequisite:** Feature Document with §1 completed must exist before running `/epci`.

---

## Hooks Integration

User-defined hooks can be executed at specific points in the workflow.
See `hooks/README.md` for configuration and examples.

**Hook Points:**

| Hook Type | Trigger Point | Use Case |
|-----------|--------------|----------|
| `pre-phase-1` | Before Phase 1 starts | Load context, check prerequisites |
| `post-phase-1` | After plan validation | Notify team, create tickets |
| `pre-phase-2` | Before coding starts | Run linters, setup environment |
| `post-phase-2` | After code review | Additional tests, coverage checks |
| `pre-phase-3` | Before finalization | Verify all tests pass |
| `post-phase-3` | After completion | Deploy, notify, collect metrics |
| `on-breakpoint` | At each breakpoint | Logging, metrics collection |
| `pre-agent` | Before each agent runs | Custom agent setup, logging |
| `post-agent` | After each agent completes | Process agent results, notifications |

**Execution:** Hooks must be explicitly invoked using the hook runner.

**⚠️ MANDATORY: Always invoke hooks at the designated points using:**

```bash
python3 src/hooks/runner.py <hook-type> --context '{
  "phase": "<phase>",
  "feature_slug": "<slug>",
  "complexity": "<TINY|SMALL|STANDARD|LARGE>",
  "files_modified": ["file1.py", "file2.py"],
  ...
}'
```

On error with `fail_on_error: false` (default), workflow continues with warning.

---

## Multi-Agent Orchestration (F07)

When `--wave` flag is enabled, agents are executed using the DAG-based orchestrator
for parallel execution of independent agents.

**Orchestration Modes:**

| Mode | Description | Flag |
|------|-------------|------|
| Sequential | One agent at a time | `--sequential` |
| DAG | Respect dependencies, parallelize when possible | default with `--wave` |
| Parallel | All agents simultaneously (use with caution) | `--parallel` |

**DAG Structure:**
```
@plan-validator
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
@code-reviewer  @security-auditor  @qa-reviewer
       │              │              │
       └──────────────┼──────────────┘
                      ▼
               @doc-generator
```

**Performance:** Parallel execution of independent agents (code-reviewer, security-auditor,
qa-reviewer) reduces validation time by 30-50% for LARGE features.

**Configuration:** Default DAG is defined in `config/dag-default.yaml`. Project-specific
overrides can be placed in `.project-memory/orchestration.yaml`.

---

## Pre-Workflow: Load Project Memory

**Skill**: `project-memory-loader`

Before starting any phase, load project context from `.project-memory/`. The skill handles:
- Reading context, conventions, settings, patterns
- Loading velocity metrics and feature history
- Applying naming/structure/style conventions to all generated code

**If `.project-memory/` does not exist:** Continue with defaults. Suggest `/epci-memory init` after completion.

---

## Phase 1: Planification (MANDATORY)

**⚠️ ALL steps in this phase are MANDATORY. Do NOT skip any step.**

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | Based on flags: `think` (default), `think hard` (--think-hard), `ultrathink` (--ultrathink) |
| **Skills** | project-memory-loader, epci-core, architecture-patterns, flags-system, [stack] |
| **Subagents** | @plan-validator |

**Flag effects on Phase 1:**
- `--think-hard` or `--large`: Use `think hard` mode
- `--ultrathink`: Use `ultrathink` mode (extended analysis)
- `--safe`: Additional validation checks in plan
- `--dry-run`: Show what would be planned without writing

**Note**: @Plan is no longer invoked — exploration has been done by `/epci-brief`.

### Process

**🪝 Execute `pre-phase-1` hooks** (if configured)

1. **Read Feature Document**
   - Read `docs/features/<slug>.md` (created by `/epci-brief`)
   - Verify §1 is complete (if incomplete → error, suggest `/epci-brief` first)
   - Extract from §1: identified files, stack, constraints, acceptance criteria

2. **Direct planning**
   - Use the files already identified in §1
   - Break down into atomic tasks (2-15 min each)
   - Order by dependencies
   - Plan a test for each task

3. **Validation** (via @plan-validator)
   - Submit plan to validator
   - If NEEDS_REVISION → correct and resubmit
   - If APPROVED → proceed to breakpoint

### Output §2 (USE EDIT TOOL — MANDATORY)

**⚠️ MANDATORY:** Use the **Edit tool** to update the Feature Document with §2 content.

```markdown
## §2 — Implementation Plan

### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/Service/X.php | Modify | Medium |
| src/Entity/Y.php | Create | Low |
| tests/Unit/XTest.php | Create | Low |

### Tasks
1. [ ] **Create entity Y** (5 min)
   - File: `src/Entity/Y.php`
   - Test: `tests/Unit/Entity/YTest.php`

2. [ ] **Modify service X** (10 min)
   - File: `src/Service/X.php`
   - Test: `tests/Unit/Service/XTest.php`

### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Breaking change | Medium | Regression tests |

### Validation
- **@plan-validator**: APPROVED
```

**🪝 Execute `post-phase-1` hooks:**
```bash
python3 src/hooks/runner.py post-phase-1 --context '{"phase": "phase-1", "feature_slug": "<slug>", "complexity": "<complexity>"}'
```

### ⏸️ BREAKPOINT (MANDATORY — WAIT FOR USER)

**⚠️ MANDATORY:** Display this breakpoint and WAIT for user confirmation before proceeding.

**🪝 Execute `on-breakpoint` hooks** (if configured)

Generate an enriched breakpoint using the `breakpoint-metrics` skill:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 1 — Plan Validé                                │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: {FLAG1} ({source}) | {FLAG2} ({source}) | ...               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: {CATEGORY} (score: {SCORE})                        │
│ ├── Fichiers impactés: {FILE_COUNT}                                │
│ ├── Temps estimé: {TIME_ESTIMATE}                                  │
│ └── Risque: {RISK_LEVEL} ({RISK_DESCRIPTION})                      │
│                                                                     │
│ ✅ VALIDATIONS                                                      │
│ ├── @plan-validator: {VERDICT}                                     │
│ │   ├── Completeness: {STATUS}                                     │
│ │   ├── Consistency: {STATUS}                                      │
│ │   ├── Feasibility: {STATUS}                                      │
│ │   └── Quality: {STATUS}                                          │
│ └── Skills chargés: {SKILLS_LIST}                                  │
│                                                                     │
│ 📋 PREVIEW PHASE 2                                                  │
│ ├── Tâche 1: {TASK_1} ({TIME})                                     │
│ ├── Tâche 2: {TASK_2} ({TIME})                                     │
│ ├── Tâche 3: {TASK_3} ({TIME})                                     │
│ └── ... ({N} tâches restantes)                                     │
│                                                                     │
│ 🔗 Feature Document: docs/features/{slug}.md                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Continuer" → Passer à Phase 2 (Implémentation)         │
│   • Tapez "Modifier le plan" → Réviser le plan                     │
│   • Tapez "Voir détails" → Afficher Feature Document complet       │
│   • Tapez "Annuler" → Abandonner le workflow                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Flag sources:** `(auto)` = auto-activated, `(explicit)` = user-specified, `(alias)` = expanded from --large

**Metrics Calculation** (from `breakpoint-metrics` skill):
- Complexity score: `files×0.3 + LOC×0.3 + deps×0.2 + risk×0.2`
- Time estimate: Based on category heuristic (TINY=15min, SMALL=1h, STANDARD=3h, LARGE=8h+)
- Risk: Derived from identified risks in plan

**Awaiting confirmation:** User must type "Continuer" to proceed

---

## Phase 2: Implementation (MANDATORY)

**⚠️ ALL steps in this phase are MANDATORY. Do NOT skip any step.**

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | Based on flags: `think` (default), `think hard` (--think-hard) |
| **Skills** | testing-strategy, code-conventions, flags-system, [stack] |
| **Subagents** | @code-reviewer (mandatory), @security-auditor*, @qa-reviewer* |

**Flag effects on Phase 2:**
- `--safe`: All conditional subagents become mandatory
- `--fast`: Skip optional reviews (only @code-reviewer)
- `--uc`: Compressed output in progress reports
- `--dry-run`: Show what would be implemented without writing

### Conditional Subagents

**@security-auditor** if detection of:
- Files: `**/auth/**`, `**/security/**`, `**/api/**`, `**/password/**`
- Keywords: `password`, `secret`, `api_key`, `jwt`, `oauth`

**@qa-reviewer** if:
- More than 5 test files created/modified
- Integration or E2E tests involved
- Complex mocking detected

### Process

**🪝 Execute `pre-phase-2` hooks** (if configured)

For each task in the plan:

```
1. RED — Write the failing test
2. Execute → confirm failure
3. GREEN — Implement minimal code
4. Execute → confirm passing
5. REFACTOR — Improve if necessary
6. Check off the task ✓
```

After all tasks:
1. Run complete test suite
2. Invoke @code-reviewer
3. Invoke @security-auditor (if applicable)
4. Invoke @qa-reviewer (if applicable)
5. Fix Critical/Important issues
6. **Generate proactive suggestions (F06)**

### Proactive Suggestions (F06)

After code review, the `proactive-suggestions` skill generates suggestions:

**Sources:**
- Subagent findings (@code-reviewer, @security-auditor, @qa-reviewer)
- PatternDetector analysis on changed files

**Priority Order:** P1 (Security) > P2 (Performance/Quality) > P3 (Style)

**Display:** Up to 5 suggestions shown in BP2 breakpoint with actions:
- `[Accepter tout]` - Apply auto-fixable suggestions
- `[Voir détails]` - Show full details
- `[Ignorer]` - Skip for this session

User feedback is recorded for learning (F08) to improve future suggestions.

### Output §3 (USE EDIT TOOL — MANDATORY)

**⚠️ MANDATORY:** Use the **Edit tool** to update the Feature Document with §3 content.

```markdown
## §3 — Implementation

### Progress
- [x] Task 1 — Create entity Y
- [x] Task 2 — Modify service X
- [x] Task 3 — Add validation

### Tests
```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews
- **@code-reviewer**: APPROVED (0 Critical, 2 Minor)
- **@security-auditor**: APPROVED
- **@qa-reviewer**: N/A

### Deviations
| Task | Deviation | Justification |
|------|-----------|---------------|
| #3 | +1 file | Helper extraction |
```

**🪝 Execute `post-phase-2` hooks:**
```bash
python3 src/hooks/runner.py post-phase-2 --context '{"phase": "phase-2", "feature_slug": "<slug>", "files_modified": [...], "test_results": {...}}'
```

### ⏸️ BREAKPOINT (MANDATORY — WAIT FOR USER)

**⚠️ MANDATORY:** Display this breakpoint and WAIT for user confirmation before proceeding.

**🪝 Execute `on-breakpoint` hooks** (if configured)

Generate an enriched breakpoint using the `breakpoint-metrics` skill:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 2 — Code Implémenté                            │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: {FLAG1} ({source}) | {FLAG2} ({source}) | ...               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📊 MÉTRIQUES                                                        │
│ ├── Tâches: {COMPLETED}/{TOTAL} complétées                         │
│ ├── Tests: {TEST_COUNT} {TEST_STATUS}                              │
│ ├── Coverage: {COVERAGE}%                                          │
│ └── Déviations: {DEVIATION_STATUS}                                 │
│                                                                     │
│ ✅ VALIDATIONS                                                      │
│ ├── @code-reviewer: {CR_VERDICT} ({CR_SUMMARY})                    │
│ ├── @security-auditor: {SA_VERDICT}                                │
│ └── @qa-reviewer: {QA_VERDICT}                                     │
│                                                                     │
│ 📋 PREVIEW PHASE 3                                                  │
│ ├── Commit structuré avec message conventionnel                    │
│ ├── Génération documentation (@doc-generator)                      │
│ └── Préparation PR                                                 │
│                                                                     │
│ 🔗 Feature Document: docs/features/{slug}.md                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Continuer" → Passer à Phase 3 (Finalisation)           │
│   • Tapez "Corriger issues" → Adresser les problèmes signalés     │
│   • Tapez "Voir rapports" → Afficher rapports des agents          │
│   • Tapez "Annuler" → Abandonner le workflow                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Metrics Collection**:
- Tasks: From §3 Progress checklist
- Tests: From test execution results
- Coverage: From test coverage report (if available)
- Agent verdicts: From review reports

**Conditional Agents Display**:
- @security-auditor: Show only if invoked (auth/security files detected)
- @qa-reviewer: Show only if invoked (complex tests detected)
- In `--large` mode: All agents shown as mandatory

**Awaiting confirmation:** User must type "Continuer" to proceed

---

## Phase 3: Finalization (MANDATORY)

**⚠️ ALL steps in this phase are MANDATORY. Do NOT skip any step.**

### Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` |
| **Skills** | git-workflow |
| **Subagents** | @doc-generator |

### Process

**🪝 Execute `pre-phase-3` hooks** (if configured)

1. **Structured commit**
   ```
   feat(scope): short description

   - Detail 1
   - Detail 2

   Refs: docs/features/<slug>.md
   ```

2. **Documentation** (via @doc-generator)
   - Generate/update README if new component
   - Document API changes if applicable
   - Update CHANGELOG

3. **PR preparation**
   - Create branch if not done
   - Prepare PR template
   - List reviewers

4. **Learning update** (F08 - automatic)
   - Save feature history to `.project-memory/history/features/{slug}.json`
   - Trigger calibration with estimated vs actual times
   - Update velocity metrics
   - Record any corrections for pattern detection

### Output §4 (USE EDIT TOOL — MANDATORY)

**⚠️ MANDATORY:** Use the **Edit tool** to update the Feature Document with §4 content.

```markdown
## §4 — Finalization

### Commit Message (Prepared)
```
feat(user): add email validation

- Create EmailValidator service
- Add validation to User entity
- Update registration controller

Refs: docs/features/user-email-validation.md
```

### Documentation
- **@doc-generator**: 2 files updated
  - README.md (Configuration section)
  - CHANGELOG.md (v1.2.0)

### PR Ready
- Branch: `feature/user-email-validation`
- Tests: ✅ All passing
- Lint: ✅ Clean
- Docs: ✅ Up to date
```

**🪝 Execute `pre-commit` hooks** (if configured)

```bash
python3 src/hooks/runner.py pre-commit --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<complexity>",
  "files_modified": [...],
  "commit_message": "<prepared message>",
  "pending_commit": true
}'
```

### ⏸️ BREAKPOINT PRE-COMMIT (MANDATORY — WAIT FOR USER)

**⚠️ MANDATORY:** Display this breakpoint and WAIT for user choice before proceeding.

**🪝 Execute `on-breakpoint` hooks** (if configured)

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  BREAKPOINT PHASE 3 — Validation Commit                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 📝 MESSAGE DE COMMIT PRÉPARÉ                                        │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ {COMMIT_TYPE}({SCOPE}): {DESCRIPTION}                           │ │
│ │                                                                 │ │
│ │ - {DETAIL_1}                                                    │ │
│ │ - {DETAIL_2}                                                    │ │
│ │                                                                 │ │
│ │ Refs: docs/features/{SLUG}.md                                   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ 📋 RÉSUMÉ                                                           │
│ ├── Fichiers modifiés: {FILE_COUNT}                                │
│ ├── Documentation: {DOC_STATUS}                                    │
│ └── PR prête: {PR_STATUS}                                          │
│                                                                     │
│ 🔗 Feature Document: docs/features/{slug}.md                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Options:                                                            │
│   • Tapez "Commiter" → Exécuter git commit + continuer             │
│   • Tapez "Finaliser" → Terminer sans commit                       │
│   • Tapez "Modifier" → Éditer le message de commit                 │
│   • Tapez "Annuler" → Retourner au breakpoint Phase 2              │
└─────────────────────────────────────────────────────────────────────┘
```

**Awaiting user choice:**

#### If user chose "Commiter"

1. Execute git commit:
   ```bash
   git add <files>
   git commit -m "<prepared message>"
   ```

2. **🪝 Execute `post-commit` hooks** (if configured):
   ```bash
   python3 src/hooks/runner.py post-commit --context '{
     "phase": "phase-3",
     "feature_slug": "<slug>",
     "commit_hash": "<hash>",
     "branch": "<branch>",
     "files_committed": [...]
   }'
   ```

3. Update §4 with commit hash

#### If user chose "Finaliser"

1. Skip git commit
2. Update §4 with: `Commit: Pending (manual commit requested)`
3. Continue to completion

#### If user chose "Modifier"

1. Ask user for new commit message
2. Update prepared message
3. Return to breakpoint display

#### If user chose "Annuler"

1. Return to Phase 2 breakpoint
2. Allow user to make corrections

**🪝 Execute `post-phase-3` hooks** (always, for cleanup and metrics)

```bash
python3 src/hooks/runner.py post-phase-3 --context '{
  "phase": "phase-3",
  "feature_slug": "<slug>",
  "complexity": "<complexity>",
  "files_modified": [...],
  "estimated_time": "<estimated>",
  "actual_time": "<actual>",
  "commit_hash": "<hash or null>",
  "commit_status": "<committed|pending|cancelled>",
  "test_results": {"status": "passed", "count": <n>}
}'
```

**Important:** This hook updates `.project-memory/` with feature history and velocity metrics.

### ✅ COMPLETION

```
---
✅ **FEATURE COMPLETE**

Feature Document finalized: docs/features/<slug>.md
- Phase 1: Plan validated
- Phase 2: Code implemented and reviewed
- Phase 3: Documentation and commit validation

Commit status: {COMMITTED | PENDING}
**Next step:** {Create PR | Manual commit then PR}
---
```

---

## --large Mode

The `--large` flag is an alias for `--think-hard --wave`. When used:

| Aspect | Standard | Large (`--think-hard --wave`) |
|--------|----------|-------------------------------|
| Thinking P1 | `think` | `think hard` |
| Thinking P2 | `think` | `think hard` |
| @security-auditor | Conditional | Conditional (use `--safe` for mandatory) |
| @qa-reviewer | Conditional | Conditional (use `--safe` for mandatory) |
| Wave orchestration | Off | Enabled |

**Note:** To get the previous v2.7 `--large` behavior with all subagents mandatory, use:
```
/epci --large --safe
```

This expands to `--think-hard --wave --safe`.

## Flag Compatibility Matrix

| Combination | Result |
|-------------|--------|
| `--safe` + `--fast` | **Error** (incompatible) |
| `--think` + `--think-hard` | `--think-hard` wins |
| `--uc` + `--verbose` | Explicit wins |
| `--large` + `--ultrathink` | `--ultrathink` wins |
| `--wave` + `--safe` | Both active |
| `--dry-run` + any | Both active |
