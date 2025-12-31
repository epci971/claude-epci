---
description: >-
  Autonomous EPCT workflow for TINY and SMALL features. Four phases:
  Explore, Plan, Code, Test with adaptive model switching (Haiku/Sonnet).
  TINY mode: <50 LOC, 1 file. SMALL mode: <200 LOC, 2-3 files.
argument-hint: "[--autonomous] [--quick-turbo] [--uc] [--turbo] [--no-hooks]"
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---

# EPCI Quick — EPCT Workflow

## Overview

Autonomous workflow following EPCT logic (Explore, Plan, Code, Test) for TINY and SMALL features.
Optimized for speed with adaptive model switching and minimal breakpoints.

**Key Features:**
- 4-phase EPCT structure
- Adaptive model switching (Haiku for speed, Sonnet for quality)
- Lightweight breakpoint with 3s auto-continue
- Session persistence for resume/tracking

## Modes

### TINY Mode

| Criteria | Value |
|----------|-------|
| Files | 1 only |
| LOC | < 50 |
| Tests | Not required |
| Duration | < 30 seconds target |
| Examples | Typo, config, small fix |

### SMALL Mode

| Criteria | Value |
|----------|-------|
| Files | 2-3 |
| LOC | < 200 |
| Tests | Optional |
| Duration | < 90 seconds target |
| Examples | Small feature, local refactor |

---

## Supported Flags

### Quick-Specific Flags (F13)

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--autonomous` | Skip plan breakpoint, continuous execution | TINY detected |
| `--quick-turbo` | Force Haiku model everywhere (TINY only) | Never (explicit) |
| `--no-bp` | Alias for `--autonomous` | - (alias) |

### Inherited Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--uc` | Compressed output | context > 75% |
| `--turbo` | Use existing turbo mode (@implementer, auto-commit) | Never |
| `--no-hooks` | Disable all hook execution | Never |
| `--safe` | Force breakpoints even with `--autonomous` | Sensitive files |

**Note:** Thinking flags (`--think-hard`, `--ultrathink`) trigger escalation to `/epci`.

### Flag Interactions

| Combination | Behavior |
|-------------|----------|
| `--autonomous` alone | Skip BP plan, continuous execution |
| `--quick-turbo` alone | Haiku everywhere (TINY only, error if SMALL) |
| `--autonomous --quick-turbo` | Skip BP + Haiku everywhere |
| `--turbo --autonomous` | `--turbo` takes precedence (existing turbo workflow) |
| `--safe --autonomous` | `--safe` wins, breakpoints maintained |

---

## Model Matrix (Adaptive Switching)

| Phase | TINY | SMALL | On Error/Retry |
|-------|------|-------|----------------|
| **[E] Explore** | Haiku | Haiku | - |
| **[P] Plan** | Haiku | Sonnet + `think` | `think hard` |
| **[C] Code** | Haiku | Sonnet | Sonnet + `think` |
| **[T] Test** | Haiku | Haiku | Sonnet + `think hard` |

**Model Selection Rules:**
- TINY: Always use Haiku for maximum speed
- SMALL: Use Sonnet for Plan/Code phases (quality matters)
- Error/Retry: Escalate thinking mode for problem resolution
- `--quick-turbo`: Force Haiku everywhere (TINY only)

**Escalation Thresholds (Haiku → Sonnet):**
| Criteria | Threshold |
|----------|-----------|
| LOC estimated | > 30 |
| Files | > 1 |
| New imports/deps | > 3 |
| Complex patterns | async, state, API detected |

---

## Subagent Matrix (By Complexity)

| Phase | TINY | SMALL | SMALL+ (near limit) |
|-------|------|-------|---------------------|
| **[E] Explore** | - | @Explore (Haiku) | @Explore + @clarifier |
| **[P] Plan** | - | - | @planner (Sonnet) |
| **[C] Code** | - | @implementer | @implementer |
| **[T] Test** | - | - | - |

**Subagent Invocation:**
```
Invoke via Task tool with model: {specified_model}
Examples:
- Task tool with subagent_type="Explore", model="haiku"
- Task tool with subagent_type="epci:planner", model="sonnet"
- Task tool with subagent_type="epci:implementer", model="sonnet"
```

---

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | Adaptive per phase (see Model Matrix) |
| **Skills** | project-memory, epci-core, code-conventions, flags-system, [stack] |
| **Subagents** | @Explore, @clarifier, @planner, @implementer (conditional) |

---

## EPCT Workflow

**⚠️ IMPORTANT: Follow ALL phases in sequence.**

```
/quick "description" [--autonomous] [--quick-turbo]
    │
    ▼
[E] EXPLORE ──────────────────────────────────────────────────────────
    │
    ▼
[P] PLAN ─────────────────────────────────────────────────────────────
    │                         ⏸️ Lightweight BP (3s auto-continue)
    ▼                         [skip if --autonomous]
[C] CODE ─────────────────────────────────────────────────────────────
    │
    ▼
[T] TEST ─────────────────────────────────────────────────────────────
    │
    ▼
[RESUME FINAL] ───────────────────────────────────────────────────────
```

---

### [E] EXPLORE Phase (5-10s)

**Model:** Haiku (both TINY and SMALL)

**Purpose:** Quick context gathering and complexity verification.

#### Process

1. **Receive Brief** from `/brief`
   - Extract: target files, detected stack, mode, acceptance criteria
   - If brief absent → Suggest `/brief` first

2. **Quick Scan** (SMALL only)
   - Invoke @Explore (Haiku) via Task tool:
     ```
     Task tool with subagent_type="Explore", model="haiku"
     Focus: File identification, pattern detection
     Skip: Deep analysis (defer to implementation)
     ```

3. **Ambiguity Check** (SMALL+ only)
   - If ambiguity detected → Invoke @clarifier (Haiku)
   - Maximum 1-2 clarification questions

4. **Complexity Guard**
   - If complexity > SMALL detected → Escalate to `/epci`
   ```
   ⚠️ **ESCALATION REQUIRED**
   
   Complexity exceeds SMALL threshold:
   - [Reason: e.g., >3 files, integration tests needed]
   
   → Switching to `/epci` for structured workflow.
   ```

#### Output (Internal)
- Confirmed mode (TINY/SMALL)
- Target files list
- Stack/patterns detected
- Ready for Plan phase

---

### [P] PLAN Phase (10-15s)

**Model:** Haiku (TINY) | Sonnet + `think` (SMALL)

**Purpose:** Generate atomic task breakdown.

#### Process

1. **Task Generation**
   - TINY: 1-2 tasks maximum
   - SMALL: 3-5 atomic tasks (2-10 min each)

2. **Complex Planning** (SMALL+ only)
   - If near SMALL limit → Invoke @planner (Sonnet):
     ```
     Task tool with subagent_type="epci:planner", model="sonnet"
     Input: Brief + identified files
     Output: Ordered task list with dependencies
     ```

3. **Session Initialization**
   - Create session file: `.project-memory/sessions/quick-{timestamp}.json`
   - Record: timestamp, description, complexity, plan tasks

#### ⏸️ Lightweight Breakpoint (unless --autonomous)

**⚠️ Display this breakpoint and auto-continue after 3 seconds.**

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 PLAN: {N} tâches | ~{LOC} LOC | {FILE_COUNT} fichier(s)         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [1] {Task 1 description}                                           │
│ [2] {Task 2 description}                                           │
│ [3] {Task 3 description}                                           │
│                                                                     │
│ Auto-continue dans 3s... (Entrée=modifier, Échap=annuler)          │
└─────────────────────────────────────────────────────────────────────┘
```

**Behavior:**
- **Default (3s timeout):** Auto-continue to Code phase
- **Enter pressed:** User wants to modify plan → prompt for changes
- **Escape pressed:** Cancel workflow
- **`--autonomous` flag:** Skip breakpoint entirely

---

### [C] CODE Phase (variable)

**Model:** Haiku (TINY) | Sonnet (SMALL)

**Purpose:** Execute implementation tasks.

#### Process

1. **Task Execution**
   - TINY: Direct implementation (no subagent)
   - SMALL: Invoke @implementer (Sonnet):
     ```
     Task tool with subagent_type="epci:implementer", model="sonnet"
     Input: Single task from plan
     Output: Implemented code
     ```

2. **For Each Task:**
   ```
   a. Read target file
   b. Apply change (Edit tool)
   c. Micro-validate (syntax check)
   d. Mark task complete in session
   ```

3. **Auto-Fix**
   - Run lint/format on changed files
   - Apply automatic fixes

4. **Error Handling**
   - On error: Activate `think` mode
   - Retry with same model (max 1x)
   - If still failing: Escalate model (Haiku→Sonnet, Sonnet→Opus)
   - After 2 retries: Stop and request intervention

   ```
   ⚠️ **IMPLEMENTATION BLOCKED**
   
   Error persists after 2 retries:
   - [Error description]
   
   Please review and provide guidance.
   ```

#### Output (Internal)
- Files modified list
- LOC changes (+/-)
- Errors encountered (if any)

---

### [T] TEST Phase (5-10s)

**Model:** Haiku (validation) | Sonnet + `think hard` (if fix needed)

**Purpose:** Verify implementation correctness.

#### Process

1. **Run Existing Tests**
   ```bash
   # Detect test runner and execute
   npm test / pytest / php bin/phpunit / etc.
   ```

2. **Lint/Format Check**
   ```bash
   # Run project linter
   eslint / flake8 / phpcs / etc.
   ```

3. **Coherence Verification**
   - Check imports are valid
   - Verify no syntax errors
   - Confirm changes match acceptance criteria

4. **On Test Failure:**
   - Activate `think hard` mode
   - Attempt auto-fix (Sonnet model)
   - If fix fails → Report and stop

#### Output (Internal)
- Test results (pass/fail count)
- Lint status (clean/issues)
- Ready for final resume

---

### Session Persistence

**Location:** `.project-memory/sessions/quick-{timestamp}.json`

**Schema:**
```json
{
  "timestamp": "2025-12-31T14:30:22Z",
  "description": "fix typo in README",
  "complexity": "TINY",
  "plan": [
    {"task": "Fix typo line 42", "status": "completed"}
  ],
  "files_modified": ["README.md"],
  "duration_seconds": 45,
  "models_used": {
    "explore": "haiku",
    "plan": "haiku",
    "code": "haiku",
    "test": "haiku"
  },
  "retries": 0,
  "flags": ["--autonomous"]
}
```

**Session Management:**
- Created at Plan phase start
- Updated after each phase completion
- Enables resume if workflow interrupted
- Used for metrics calibration

---

## Resume Final (MANDATORY)

**⚠️ MANDATORY:** Always display the completion message.

### TINY Mode Output

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ QUICK COMPLETE — TINY                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Fichier modifié: `{path/to/file.ext}`                              │
│ Changement: {description}                                          │
│ Lignes: +{X} / -{Y}                                                │
│                                                                     │
│ Temps total: {N}s                                                  │
│ Session: .project-memory/sessions/quick-{timestamp}.json           │
│                                                                     │
│ Pour commiter: /commit                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### SMALL Mode Output

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│ ✅ QUICK COMPLETE — SMALL                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Fichiers modifiés:                                                 │
│ ├── `{path/to/file1.ext}` (+{X} / -{Y})                           │
│ ├── `{path/to/file2.ext}` (+{Z} / -{W})                           │
│ └── `{path/to/file3.ext}` (+{A} / -{B})                           │
│                                                                     │
│ Tests: {N} passing                                                 │
│ Temps total: {N}s                                                  │
│ Session: .project-memory/sessions/quick-{timestamp}.json           │
│                                                                     │
│ Pour commiter: /commit                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 🪝 Memory Update (MANDATORY)

**⚠️ CRITICAL: Always execute this hook after displaying completion message.**

After every successful `/quick` completion, you MUST execute the `post-phase-3` hook to save feature history:

```bash
python3 src/hooks/runner.py post-phase-3 --context '{
  "phase": "quick-complete",
  "feature_slug": "<brief-slug>",
  "complexity": "<TINY|SMALL>",
  "files_modified": ["<list of modified files>"],
  "loc_added": <number>,
  "loc_removed": <number>,
  "estimated_time": null,
  "actual_time": "<duration in seconds>s",
  "commit_hash": null,
  "commit_status": "pending",
  "test_results": {"status": "<passed|skipped>", "count": <n>}
}'
```

**Why this is mandatory:**
- Updates `.project-memory/history/features/` with feature record
- Enables velocity tracking and calibration
- Maintains feature history for `/memory` command
- Required for accurate project metrics

**Note:** If `--no-hooks` flag is active, skip this step.

---

## Error Handling

### Retry Strategy

| Situation | Action |
|-----------|--------|
| Error detected | Activate `think` mode |
| 1st retry fails | Escalate model (Haiku→Sonnet) |
| 2nd retry fails | Stop, request intervention |
| Tests fail | Activate `think hard`, attempt auto-fix |
| Tests still fail | Report failure, stop |

### Escalation to /epci

Escalate if during implementation you discover:
- More than 3 impacted files
- Regression risk identified
- Underestimated complexity
- Integration tests needed
- Security-sensitive changes

```
⚠️ **ESCALATION RECOMMENDED**

The modification is more complex than anticipated:
- [Reason 1]
- [Reason 2]

Recommendation: Switch to `/epci` for structured workflow.
```

---

## --turbo Mode (Legacy)

**⚠️ MANDATORY: When `--turbo` flag is active, use existing turbo workflow:**

1. **Use @implementer agent** (Sonnet model) for SMALL features
2. **Skip optional review** — No @code-reviewer
3. **Auto-commit** — Skip pre-commit breakpoint
4. **Compact output** — Summary only

**Note:** `--turbo` and `--autonomous` are different:
- `--turbo`: Uses existing turbo infrastructure, auto-commit
- `--autonomous`: Uses new EPCT workflow, skips plan BP only

---

## MCP Flags (F12 — Lightweight)

For SMALL features only:

| Flag | Effect | Note |
|------|--------|------|
| `--c7` | Context7 for quick doc lookup | Recommended for SMALL |
| `--no-mcp` | Disable all MCP servers | Default for TINY |

**Note:** Sequential, Magic, and Playwright are not recommended for TINY/SMALL.

---

## Comparison with /epci

| Aspect | /quick | /epci |
|--------|--------|-------|
| Workflow | EPCT (4 phases) | 3 phases |
| Feature Document | No | Yes |
| Breakpoints | 1 lightweight (3s) | 3 full |
| Model switching | Adaptive Haiku/Sonnet | Flag-based |
| @plan-validator | No | Yes |
| @code-reviewer | No | Full |
| @security-auditor | No | Conditional |
| Session persistence | Yes (.project-memory/sessions/) | Via hooks |
| Target duration | <30s TINY, <90s SMALL | Variable |

---

## Examples

### TINY Example

**Brief:** "Fix typo 'recieve' to 'receive' in UserService"

```
[E] Explore: UserService.php identified, TINY confirmed
[P] Plan: 1 task — Replace typo line 42
    (--autonomous: BP skipped)
[C] Code: Edit applied, syntax OK
[T] Test: Existing tests pass

✅ QUICK COMPLETE — TINY
Fichier: src/Service/UserService.php
Temps: 12s
```

### SMALL Example

**Brief:** "Add isActive() method to User entity"

```
[E] Explore: 2 files identified, SMALL confirmed
    @Explore (Haiku): patterns detected
[P] Plan: 3 tasks generated
    ┌─────────────────────────────────────────┐
    │ [1] Write test for isActive()           │
    │ [2] Implement isActive() method         │
    │ [3] Verify tests pass                   │
    │ Auto-continue dans 3s...                │
    └─────────────────────────────────────────┘
[C] Code: @implementer (Sonnet) executed
[T] Test: 3/3 tests passing

✅ QUICK COMPLETE — SMALL
Fichiers: User.php (+15/-0), UserTest.php (+22/-0)
Temps: 67s
```
