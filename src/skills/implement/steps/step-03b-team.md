---
name: step-03b-team
description: Conditional agent team orchestration for multi-domain features
prev_step: steps/step-02-plan.md
next_step: steps/step-03-code.md
conditional_next:
  - condition: "team_mode == false"
    step: steps/step-03-code.md
---

# Step 03b: Agent Team Orchestration

## Reference Files

@../references/domain-mapping.md

| Reference | Purpose |
|-----------|---------|
| domain-mapping.md | File extension to domain mapping and threshold logic |

*(Breakpoint templates are inline in this file)*

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER activate team mode for TINY/SMALL features (unless --team flag)
- 🔴 NEVER skip domain detection when this step is reached
- 🔴 NEVER launch background agents without file partitioning
- ✅ ALWAYS check --team/--no-team flags first (override auto-detect)
- ✅ ALWAYS detect domains from the approved plan
- ✅ ALWAYS present breakpoint before activating team mode
- ✅ ALWAYS fallback to classic mode on any team setup failure
- 🔵 YOU ARE AN ORCHESTRATOR coordinating specialized agents
- 💭 FOCUS on parallelism where it adds value, not complexity

## EXECUTION PROTOCOLS:

### 1. Check Override Flags

Read flags from execution context (parsed by step-00-init):

```
IF flag_no_team == true:
  LOG "Team mode disabled by --no-team flag"
  SKIP to step-03-code.md (classic mode)

IF flag_team == true:
  LOG "Team mode forced by --team flag"
  SKIP domain detection, proceed to Section 3 (Team Activation)
  IF complexity < STANDARD:
    WARN "Team mode on {complexity} feature may be overkill"
```

### 2. Detect Domains from Plan

Analyze the approved plan (from step-02) to identify technology domains.

**Protocol:**

1. EXTRACT the list of files to create/modify from the approved plan
2. MAP each file extension to its domain using @domain-mapping.md (see reference for full table)
3. MERGE styling domain into frontend (per domain-mapping.md grouping rules)
4. EXCLUDE non-distinct domains: docs, config, infra
5. COUNT remaining distinct domains
4. BUILD files-per-domain mapping for partitioning

**Detection Output:**
```
Domains detected: {domain_list}
Distinct count: {count}
Files per domain:
  - backend: {files}
  - frontend: {files}
```

### 3. Evaluate Threshold

```
team_mode_active = (
  (complexity >= STANDARD AND distinct_domains >= 2)
  OR flag_team == true
) AND flag_no_team != true
```

**If threshold NOT met:**
```
LOG "Team mode threshold not met ({distinct_domains} domain(s), need >= 2)"
SKIP to step-03-code.md (classic mode)
```

**If threshold met:** proceed to breakpoint.

### 4. BREAKPOINT: Team Mode Activation (OBLIGATOIRE si threshold atteint)

AFFICHE cette boite:

┌─────────────────────────────────────────────────────────────────────┐
│ TEAM MODE ACTIVATION                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Feature: {feature-slug}                                             │
│ Complexity: {complexity}                                            │
│ Domains detected: {domain_list}                                     │
│ Distinct domains: {distinct_count}                                  │
│                                                                     │
│ Files per domain:                                                   │
│   {domain_1}: {file_count_1} files                                  │
│   {domain_2}: {file_count_2} files                                  │
│                                                                     │
│ Orchestration mode: {mode}                                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ PARALLEL AGENTS                                                     │
│ - Code Reviewer (background) — runs during coding                   │
│ - Security Auditor (background) — if auth patterns detected         │
│ - QA Reviewer (background) — if complex tests detected              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Activate team mode (Recommended) - Parallel agents        │ │
│ │  [B] Classic mode - Sequential execution                       │ │
│ │  [?] Autre reponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

Remplis les variables:
- `{feature-slug}`: Feature identifier
- `{complexity}`: STANDARD or LARGE
- `{domain_list}`: Comma-separated domains (e.g., "backend, frontend")
- `{distinct_count}`: Number of distinct domains
- `{domain_1}`, `{domain_2}`: Domain names
- `{file_count_1}`, `{file_count_2}`: File counts per domain
- `{mode}`: "Subagents" or "Agent Teams" (see Section 7)

APPELLE AskUserQuestion({
  questions: [{
    question: "Activer le mode equipe avec agents paralleles?",
    header: "Team Mode",
    multiSelect: false,
    options: [
      { label: "Activate team mode (Recommended)", description: "Code Reviewer en parallele + reviews conditionnelles" },
      { label: "Classic mode", description: "Execution sequentielle standard (step-03 puis step-04)" }
    ]
  }]
})

⏸️ ATTENDS la reponse utilisateur avant de continuer.

**If user selects "Classic mode":** SKIP to step-03-code.md.

### 5. Launch Parallel Code Reviewer

When team mode is confirmed, prepare background Code Reviewer that will run during step-03 coding.

**Protocol:**

Store the team configuration in execution context for step-03-code to consume:

```
team_config = {
  mode: "active",
  domains: {detected_domains},
  files_per_domain: {mapping},
  parallel_agents: {
    code_reviewer: {
      enabled: true,
      trigger: "after_each_component",
      model: "opus"
    }
  }
}
```

**The actual Code Reviewer background launch is in step-03-code.md Section 4 — do NOT launch here.**
Step-03b only prepares the configuration. Step-03-code executes the `LANCE Task` with `run_in_background: true` after the first completed component.

### 6. Launch Conditional Parallel Reviews

In addition to the Code Reviewer, conditionally launch specialized reviewers in background.

#### 6a. Security Auditor (Conditional)

Detect auth/security patterns in the planned files:

```
security_patterns = ["**/auth/**", "**/security/**", "**/password/**",
                     "**/token/**", "**/api/**"]
security_keywords = ["password", "secret", "jwt", "oauth", "encrypt",
                     "authenticate", "authorization"]

IF any planned file matches security_patterns OR contains security_keywords:
  security_review_parallel = true
```

**If security_review_parallel:**

```
LANCE Task({
  subagent_type: "security-auditor",
  model: "opus",
  run_in_background: true,
  prompt: `
## Files to Audit
{auth_security_files}

## Audit Scope
- Authentication/Authorization code
- Data validation and sanitization
- Secret handling and storage
- API security and input handling

## OWASP Top 10 Checklist
Verify against all categories

## Expected Output
Security audit report with:
- Vulnerability count by severity
- OWASP category for each finding
- Remediation recommendations
- Verdict: PASS / FAIL_CRITICAL / FAIL_HIGH
  `
})
```

Store background task ID for step-04b aggregation.

#### 6b. QA Reviewer (Conditional)

Detect complex testing needs:

```
IF test_file_count > 5
   OR plan contains integration/e2e tests
   OR plan mentions complex mocking:
  qa_review_parallel = true
```

**If qa_review_parallel:**

```
LANCE Task({
  subagent_type: "qa-reviewer",
  model: "sonnet",
  run_in_background: true,
  prompt: `
## Test Files
{test_files}

## Test Strategy
{test_strategy_from_plan}

## Acceptance Criteria
{acceptance_criteria}

## QA Focus
- Test strategy: pyramid ratio, isolation
- Coverage: nominal, edge, error cases
- Assertion quality: meaningful, explicit
- Anti-patterns: mock testing, fragile tests

## Expected Output
QA validation report with:
- Test strategy assessment
- Coverage gaps identified
- Anti-patterns detected
- Verdict: PASS / NEEDS_IMPROVEMENT / FAIL
  `
})
```

Store background task ID for step-04c aggregation.

### 7. Select Orchestration Mode (Auto-detect)

Choose between Subagents and Agent Teams based on environment and complexity.

**Decision Logic:**

```
IF env CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS == "1"
   AND complexity == LARGE
   AND distinct_domains >= 2:
  orchestration_mode = "agent_teams"
ELSE:
  orchestration_mode = "subagents"
```

#### 7a. Subagents Mode (Default)

Standard Task tool with `run_in_background`. This is the stable, production-ready approach.

- Code Reviewer runs in background during coding
- Security/QA reviewers run in background if triggered
- Results aggregated by main session in step-04
- No inter-agent communication (each agent reports to parent)

#### 7b. Agent Teams Mode (Experimental — LARGE features only)

Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable.

**Teammate Spawning:**

For each distinct domain, spawn a specialized implementer teammate:

```
FOR EACH domain IN detected_domains:
  SPAWN teammate({
    name: "{domain}-implementer",
    role: "Implement {domain} components following TDD",
    tools: [Read, Write, Edit, Glob, Grep, Bash],
    context: `
## Your Domain: {domain}
## Files Assigned: {files_for_domain}
## Stack Skill: {stack_skill_for_domain}
## TDD Rules: RED → GREEN → REFACTOR
## Constraints:
- Only modify files in your assigned list
- Follow stack patterns from {stack_skill}
- Write tests before implementation
- Report completion via task list
    `
  })
```

**File Partitioning** (conflict avoidance):
- Each teammate gets exclusive write access to their domain files
- Shared files (e.g., config, types) assigned to one teammate only
- Test files follow their implementation files

**Plan Approval Workflow:**
- Team Lead (main session) presents partitioned plan to teammates
- Each teammate confirms understanding of their assigned tasks
- Coding starts only after all teammates acknowledge

**Shared Task List:**
Each task includes:
```
{
  task_id: "T{n}",
  domain: "{domain}",
  description: "{task_description}",
  files: ["{file1}", "{file2}"],
  status: "pending" | "in_progress" | "done",
  assigned_to: "{domain}-implementer"
}
```

**Limitations:**
- No nested teams (teammates cannot spawn teams)
- Token cost linear with teammate count
- Experimental API may change

### 8. Update Feature Document §3 (Team Section)

After team mode activation, add team tracking to the Feature Document.

EXECUTE Edit({
  file_path: "{feature_doc_path}",
  old_string: "## §3 — Implementation",
  new_string: "## §3 — Implementation\n\n### Team Mode\n| Aspect | Value |\n|--------|-------|\n| Mode | {orchestration_mode} |\n| Domains | {domain_list} |\n| Parallel agents | Code Reviewer{+Security}{+QA} |\n| Background tasks | {task_ids} |"
})

## CONTEXT BOUNDARIES:

- This step expects: Approved plan with file list, complexity level, team flags
- This step produces: Team configuration, background agent IDs, domain mapping
- This step passes to step-03: team_config with parallel agent IDs

## OUTPUT FORMAT:

### If team mode activated:
```
## Team Mode Activated

Orchestration: {subagents|agent_teams}
Domains: {domain_list} ({count} distinct)
Parallel agents:
  - Code Reviewer: background (will run during coding)
  - Security Auditor: {enabled|disabled} (auth patterns: {detected})
  - QA Reviewer: {enabled|disabled} (complex tests: {detected})

Proceeding to Code phase with team orchestration...
```

### If team mode skipped:
```
## Team Mode Skipped

Reason: {threshold not met | --no-team flag | user declined}
Proceeding to Code phase (classic mode)...
```

## NEXT STEP TRIGGER:

After team configuration (activated or skipped), proceed to `step-03-code.md`.

Step-03-code.md will:
- Check for team_config in execution context
- If team mode active: launch background Code Reviewer after each component
- If team mode active + agent_teams: coordinate with teammates
- If classic mode: execute standard TDD cycle
