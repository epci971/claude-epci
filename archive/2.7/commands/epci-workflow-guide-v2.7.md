# EPCI Workflow Guide (v2.7)

> **EPCI** = **Explore → Plan → Code → Inspect**
>
> A structured, documented pipeline for AI-assisted development with full traceability.

This document explains the complete EPCI workflow, from initial request clarification to final commit preparation. It covers all commands, routing options, special modes, universal flags, and expert personas, providing a repeatable methodology for features, bugs, technical tasks, emergencies, and exploration.

---

## 1. Overview

### 1.1 What is EPCI?

EPCI is a **4-phase development workflow** designed for AI-assisted coding:

| Phase | Name | Description |
|-------|------|-------------|
| **E** | **Explore** | Understand the codebase, identify files, patterns, constraints |
| **P** | **Plan** | Design a detailed implementation strategy |
| **C** | **Code** | Implement the changes, write actual code |
| **I** | **Inspect** | Verify, test, document, and finalize |

### 1.2 Key Principles

1. **Single Feature Document** — One Markdown file per feature (`docs/features/<slug>.md`) with 3 sections:
   - `## 1. Functional Brief — EPCI-0`
   - `## 2. Technical Plan — EPCI-1`
   - `## 3. Final Report — EPCI-3`

2. **3-Tier Routing** — Tasks are classified by complexity and routed to the appropriate workflow:
   - **TINY** → `epci-micro`
   - **SMALL** → `epci-soft`
   - **STANDARD / LARGE** → `epci-1` → `epci-2` → `epci-3`

3. **Phase A/B Safety** — In INTERACTIVE mode:
   - **Phase A** = Read-only analysis, no file writes
   - **Phase B** = Execution, only after human validation

4. **Explicit Routing** — Each command suggests the next command with copy-pastable parameters.

5. **Traceability** — Every change leaves a Markdown trace in the repository.

6. **Universal Flags** — Modifiers that work across commands for safety, output control, and debugging.

7. **Expert Personas** — Specialized expertise activated on demand or automatically.

### 1.3 Thinking Mode Hierarchy

Claude Code supports a hierarchy of thinking modes, each allocating progressively more "thinking budget":

| Level | Trigger Phrase | Thinking Budget | Use Case |
|-------|----------------|-----------------|----------|
| **Basic** | `think` | Low | Simple decisions, quick analysis |
| **Standard** | `think hard` | Medium | Technical analysis, code review |
| **Extended** | `think harder` | High | Complex architecture, deep exploration |
| **Maximum** | `ultrathink` | Maximum | Critical decisions, large refactors |

**EPCI Recommended Settings:**

| Command | Thinking Mode | Rationale |
|---------|---------------|-----------|
| `epci-discover` | **think harder** | Requirement clarification needs deep questioning |
| `epci-0-briefing` | **think harder** | Initial scoping requires deep analysis |
| `epci-1-analyse` | **think hard** | Technical exploration needs thorough reasoning |
| `epci-soft` (Phase A) | **think harder** | Explore & Plan phase benefits from extended analysis |
| `epci-2-code` | None | Executing a validated plan |
| `epci-3-finalize` | None | Inspection and documentation |
| `epci-micro` | None | Trivial changes |

> 💡 **Tip:** For critical features or large refactors, consider using `ultrathink` during EPCI-0 or EPCI-1.

### 1.4 Sub-agents Pattern

For complex codebases, use **sub-agents** to investigate specific questions without polluting your main context:

```
"Use a sub-agent to investigate how [specific aspect] is handled in this codebase, 
then report back your findings."
```

**When to use sub-agents:**

| Phase | Sub-agent Use Case | Benefit |
|-------|-------------------|---------|
| **EPCI-1** (Explore) | Investigate specific modules, patterns, or conventions | Preserves main context for planning |
| **EPCI-Soft** (Phase A) | Parallel exploration of multiple files | Faster, less context pollution |
| **EPCI-2** (after tests) | Verify implementation doesn't "overfit" to tests | Independent quality check |
| **EPCI-3** (Audit) | Cross-check plan vs implementation | Objective verification |

**Example sub-agent prompts:**

- `"Use a sub-agent to find all places where user permissions are checked"`
- `"Use a sub-agent to analyze the test structure and conventions in this project"`
- `"Use a sub-agent to investigate how error handling is done across the codebase"`

### 1.5 Context Management Tips

Long sessions can fill Claude's context with irrelevant content, reducing performance:

| Tip | Command/Action | When to Use |
|-----|----------------|-------------|
| **Clear context** | `/clear` | Between features or after completing a task |
| **Use Feature Document** | Update as you progress | Keep a "living scratchpad" of decisions |
| **Sub-agents for investigation** | See pattern above | Preserve main context for decisions |
| **Multiple Claude instances** | Separate terminals | Parallel work on independent tasks |

> 💡 **Best Practice:** Use `/clear` frequently between tasks to reset the context window and maintain Claude's performance.

### 1.6 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER REQUEST                                   │
│                    (ticket, idea, voice transcript, etc.)                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │   Is request clear?    │
                         └───────────┬────────────┘
                                     │
                      NO ────────────┼──────────── YES
                       │             │              │
                       ▼             │              ▼
              ┌─────────────┐        │    ┌─────────────────────┐
              │ epci-discover│       │    │ epci-0-briefing     │
              │             │        │    │                     │
              │ Clarify &   │        │    │ Functional brief    │
              │ Structure   │────────┘    │ & Routing           │
              └─────────────┘              └──────────┬──────────┘
                                                     │
                    ┌────────────────────────────────┼────────────────────┐
                    │                                │                    │
                    ▼                                ▼                    ▼
              ┌──────────┐                    ┌──────────┐        ┌──────────────┐
              │   TINY   │                    │  SMALL   │        │ STANDARD/    │
              │          │                    │          │        │ LARGE        │
              └────┬─────┘                    └────┬─────┘        └──────┬───────┘
                   │                               │                     │
                   ▼                               ▼                     ▼
           ┌─────────────┐                 ┌─────────────┐       ┌─────────────────┐
           │ epci-micro  │                 │ epci-soft   │       │ epci-1-analyse  │
           │             │                 │             │       │                 │
           │ Single-pass │                 │ Light       │       │ Explore + Plan  │
           │ ultra-light │                 │ complete    │       │ (read-only)     │
           └──────┬──────┘                 └──────┬──────┘       └────────┬────────┘
                  │                               │                       │
                  │                               │                       ▼
                  │                               │              ┌─────────────────┐
                  │                               │              │ epci-2-code     │
                  │                               │              │                 │
                  │                               │              │ Code + Test     │
                  │                               │              └────────┬────────┘
                  │                               │                       │
                  │                               │                       ▼
                  │                               │              ┌─────────────────┐
                  │                               │              │ epci-3-finalize │
                  │                               │              │                 │
                  │                               │              │ Inspect + Docs  │
                  └────────┬─────────────────────┴──────────────┴────────┬────────┘
                           │                                             │
                           ▼                                             ▼
                  ┌─────────────────────────────────────────────────────────────┐
                  │                    Feature Document                         │
                  │               docs/features/<slug>.md                       │
                  │                                                             │
                  │  ## 1. Functional Brief — EPCI-0                      ✅   │
                  │  ## 2. Technical Plan — EPCI-1                        ✅   │
                  │  ## 3. Final Report — EPCI-3                          ✅   │
                  └─────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                           ┌───────────────────┐
                           │  Commit & Merge   │
                           └───────────────────┘
```

---

## 2. Pre-Routing: Special Modes

Before standard EPCI routing, assess if the situation requires a special mode:

### 2.1 Discovery Mode — epci-discover (NEW in v2.7)

**When to use**: Request is vague, unclear, or needs structured clarification.

| Situation | Example | Action |
|-----------|---------|--------|
| **Vague idea** | "Improve performance" | → `epci-discover` |
| **Missing context** | "Add that feature we discussed" | → `epci-discover` |
| **Multiple interpretations** | "Make the form better" | → `epci-discover` |
| **Clear request** | "Add max 30 days validation to bookings" | → `epci-0-briefing` |

**Workflow**: Clarify → Structure → Generate Brief → Route to EPCI-0

**Output**: `EPCI_READY_BRIEF` ready for `epci-0-briefing`

See `epci-discover.md` for full documentation.

### 2.2 Emergency Mode — epci-hotfix

**When to use**: Production is down, security breach active, data corruption ongoing.

| Severity | Definition | Action |
|----------|------------|--------|
| **P0** | Complete outage | Immediate → `epci-hotfix` |
| **P1** | Major feature broken | < 1 hour → `epci-hotfix` |
| **P2** | Degraded service | Standard EPCI |
| **P3** | Minor issue | Standard EPCI |

**Workflow**: Fix → Deploy → Document (inverted)

**Constraints**:
- Max 1 file modified
- Max 50 LOC changed
- Post-mortem within 24h

See `epci-hotfix.md` for full documentation.

### 2.3 Exploration Mode — epci-spike

**When to use**: Technical uncertainty requires exploration before committing.

| Question Type | Example | Time-box |
|---------------|---------|----------|
| **Feasibility** | "Can we do X?" | 30min-1h |
| **Comparison** | "A vs B?" | 1-2h |
| **Estimation** | "How long for X?" | 30min-1h |
| **Architecture** | "Best approach for X?" | 2-4h |

**Workflow**: Frame → Explore → Synthesize → Decide

**Output**: GO / NO-GO / MORE RESEARCH (not code)

See `epci-spike.md` for full documentation.

### 2.4 Pre-Routing Decision Tree

```
                         USER REQUEST
                              │
                              ▼
                 ┌────────────────────────┐
                 │   Is production down   │
                 │   or critically broken?│
                 └───────────┬────────────┘
                             │
              YES ───────────┼─────────── NO
               │             │             │
               ▼             │             ▼
        ┌─────────────┐      │    ┌────────────────────┐
        │ epci-hotfix │      │    │ Is request clear   │
        │             │      │    │ and specific?      │
        └─────────────┘      │    └─────────┬──────────┘
                             │              │
                             │   NO ────────┼──────── YES
                             │    │         │          │
                             │    ▼         │          ▼
                             │ ┌───────────┐│  ┌────────────────────┐
                             │ │epci-      ││  │ Do you know exactly│
                             │ │discover   ││  │ what to build?     │
                             │ └─────┬─────┘│  └─────────┬──────────┘
                             │       │      │            │
                             │       ▼      │   NO ──────┼──────── YES
                             │   epci-0     │    │       │          │
                             │   briefing   │    ▼       │          ▼
                             │              │ ┌─────────┐│  ┌─────────────────┐
                             │              │ │epci-    ││  │ epci-0-briefing │
                             │              │ │spike    ││  │ (standard route)│
                             │              │ └────┬────┘│  └─────────────────┘
                             │              │      │     │
                             │              │      ▼     │
                             │              │  ┌───────┐ │
                             │              │  │  GO?  │ │
                             │              │  └───┬───┘ │
                             │              │      │     │
                             │              │  YES─┼─NO  │
                             │              │   │  │  │  │
                             │              │   ▼  │  ▼  │
                             │              │ epci-0 Archive
                             │              │            │
                             └──────────────┴────────────┘
```

---

## 3. Universal Flags (NEW in v2.7)

Flags are modifiers that work across EPCI commands. They allow you to customize behavior without changing the core workflow.

### 3.1 Flag Categories

| Category | Flags | Purpose |
|----------|-------|---------|
| **Safety** | `--preview`, `--safe-mode`, `--dry-run` | Prevent unintended changes |
| **Output** | `--uc`, `--verbose` | Control output verbosity |
| **Debug** | `--introspect` | Show reasoning process |
| **Quality** | `--validate` | Run validation checks |

### 3.2 Flag Reference

| Flag | Description | Example |
|------|-------------|---------|
| `--preview` | Show what would happen without executing | `epci-2-code --preview` |
| `--safe-mode` | Require confirmation before each file change | `epci-2-code --safe-mode` |
| `--dry-run` | Simulate the entire workflow | `epci-soft --dry-run` |
| `--uc` | Ultra-compressed output (~70% reduction) | `epci-1-analyse --uc` |
| `--verbose` | Maximum detail in output | `epci-0-briefing --verbose` |
| `--introspect` | Show decision-making process | `epci-0-briefing --introspect` |
| `--validate` | Run extra validation checks | `epci-2-code --validate` |

### 3.3 Flag Compatibility Matrix

| Flag | discover | epci-0 | epci-1 | epci-2 | epci-3 | soft | micro | hotfix | spike |
|------|----------|--------|--------|--------|--------|------|-------|--------|-------|
| `--preview` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| `--safe-mode` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `--dry-run` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| `--uc` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--verbose` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--introspect` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| `--validate` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

See `epci-flags.md` for detailed flag documentation.

---

## 4. Expert Personas (NEW in v2.7)

Personas bring specialized expertise to specific phases of the EPCI workflow.

### 4.1 Available Personas

| Persona | Flag | Specialization | Best For |
|---------|------|----------------|----------|
| **Architect** | `--persona-architect` | System design, patterns, scalability | LARGE features, refactors |
| **Security** | `--persona-security` | Vulnerabilities, compliance, auth | Auth, data, API security |
| **Performance** | `--persona-performance` | Optimization, profiling, caching | Hot paths, scaling issues |
| **QA** | `--persona-qa` | Testing, validation, edge cases | Test strategy, coverage |
| **Frontend** | `--persona-frontend` | UI/UX, React, accessibility | Component design, UX |
| **Backend** | `--persona-backend` | API, databases, services | API design, data modeling |
| **DevOps** | `--persona-devops` | CI/CD, deployment, infrastructure | Deployment, monitoring |

### 4.2 Persona Usage

**Manual activation:**
```bash
epci-1-analyse @feature.md --persona-security
epci-2-code --persona-performance
```

**Auto-activation triggers:**

| Trigger | Persona Activated |
|---------|-------------------|
| Files in `security/`, `auth/`, `crypto/` | Security |
| Keywords: "optimize", "slow", "cache" | Performance |
| Files in `tests/`, keywords: "coverage" | QA |
| Files: `.tsx`, `.jsx`, `components/` | Frontend |
| Files: `Controller`, `Service`, `Repository` | Backend |
| Files: `Dockerfile`, `.yml`, `deploy` | DevOps |
| Complexity: LARGE, multi-module | Architect |

### 4.3 Persona Compatibility

| Persona | discover | epci-0 | epci-1 | epci-2 | epci-3 | soft | micro | hotfix | spike |
|---------|----------|--------|--------|--------|--------|------|-------|--------|-------|
| Architect | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Security | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Performance | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| QA | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Frontend | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Backend | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| DevOps | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |

See `epci-personas.md` for detailed persona documentation.

---

## 5. Complexity Assessment & Routing

### 5.1 Complexity Grid

| Level | Files | LOC | Risk | Modules | Examples |
|-------|-------|-----|------|---------|----------|
| **TINY** | 1 (max 2 if same module) | < 50 | Very low | 1 | Typo fix, CSS tweak, log message, trivial guard |
| **SMALL** | 2–3 OR 1 with new logic | 50–200 | Low | 1 | Simple validation, minor UI change, small business tweak |
| **STANDARD** | 3–10 | 200–1000 | Medium | 1–3 | New endpoint, new small feature, moderate refactor |
| **LARGE** | > 10 | > 1000 | High | > 3 | Cross-module feature, major refactor, complex workflow |

### 5.2 TINY vs SMALL Clarification

This is the most common ambiguity. Use this decision tree:

**TINY** (epci-micro) applies when **ALL** of these are true:
- 1 file modified (2 maximum if strictly in same module)
- Total LOC < 50
- No new business logic introduced
- No schema changes
- Very low risk

**SMALL** (epci-soft) applies when **ANY** of these is true:
- 2–3 files modified
- OR 1 file but 50–200 LOC
- OR new business logic (even simple)
- Low risk, single module

**Ambiguous case (2 files, < 50 LOC):**
- If no new logic → **TINY** (use `epci-micro`)
- If new logic introduced → **SMALL** (use `epci-soft`)

### 5.3 Additional Factors

Beyond the numeric thresholds, consider:

- **Data impact**: Migrations, data integrity, backfill → increases complexity
- **Security impact**: Auth, permissions, exposed endpoints → increases complexity
- **Performance**: Hot paths, heavy computations → increases complexity
- **Unknowns**: Ambiguities, missing requirements → increases complexity

### 5.4 Routing Rules

| Complexity | Workflow | Commands |
|------------|----------|----------|
| **TINY** | EPCI-Micro | `epci-micro` |
| **SMALL** | EPCI-Soft | `epci-soft` |
| **STANDARD** | Full EPCI | `epci-1-analyse` → `epci-2-code` → `epci-3-finalize` |
| **LARGE** | Full EPCI | `epci-1-analyse` → `epci-2-code` → `epci-3-finalize` |

---

## 6. Common Conventions

### 6.1 Feature Slug

All EPCI commands share a common **feature identifier**, called `FEATURE_SLUG`.

- **Format**: kebab-case, lowercase
- **Derivation**: From `FEATURE_TITLE` if not provided
- **Example**: "Stay tax calculation" → `stay-tax-calculation`

### 6.2 Feature Document

Single Markdown file per feature:

```
docs/features/<feature-slug>.md
```

**Structure:**

```markdown
# <Feature Title>

## 1. Functional Brief — EPCI-0

*(Managed by epci-0-briefing. Do not modify manually.)*

## 2. Technical Plan — EPCI-1

*(Managed by epci-1-analyse or epci-soft. Do not modify manually.)*

## 3. Final Report — EPCI-3

*(Managed by epci-3-finalize or epci-soft. Do not modify manually.)*
```

### 6.3 `$ARGUMENTS` / `EPCI_READY_BRIEF` Structure

All EPCI commands use a **unified format** for the brief:

```text
$ARGUMENTS=<EPCI_READY_BRIEF>
  FEATURE_TITLE: <human-readable title>
  FEATURE_SLUG: <kebab-case-slug>
  OBJECTIVE: <1-3 sentences describing the goal>
  CONTEXT: <ticket refs, modules, URLs>
  FUNCTIONAL_REQUIREMENTS:
    - [FR1] ...
    - [FR2] ...
  NON_FUNCTIONAL_REQUIREMENTS:
    - [NFR1] ...
  CONSTRAINTS: <technical or business constraints>
  ACCEPTANCE_CRITERIA:
    - [AC1] ...
    - [AC2] ...
  ASSUMPTIONS: <if any, clearly marked>
```

This format is produced by `epci-0-briefing` (or `epci-discover`) and consumed by all downstream commands.

### 6.4 Execution Modes

| Mode | Behaviour |
|------|-----------|
| **INTERACTIVE** (default) | Phase A (read-only) → Human validation → Phase B (execution) |
| **AUTO** | Single-pass, self-validated, assumptions documented |

### 6.5 Commit Message Formats

Different workflows use different levels of commit detail:

| Workflow | Format | Example |
|----------|--------|---------|
| **epci-micro** | Simple | `fix: correct French typo in login error` |
| **epci-soft** | With scope | `feat(booking): add max stay validation` |
| **Full EPCI** | Full with body | See below |

**Full commit format (epci-3-finalize):**

```text
<type>(<scope>): <short summary>

<body - what was done and why>

- <bullet 1>
- <bullet 2>

Refs: #<issue-number>
```

---

## 7. Command Reference

### 7.1 `epci-discover` — Pre-Briefing Discovery (NEW in v2.7)

**Purpose:** Transform vague ideas into structured EPCI briefs through Socratic questioning.

**Thinking mode:** Extended thinking recommended.

**Inputs:**
- Raw, potentially vague request
- Optional: domain hints

**Outputs:**
- Structured `EPCI_READY_BRIEF`
- Routing recommendation

**Phases (INTERACTIVE):**
- **Phase A**: Ask clarifying questions (5-10 questions)
- **Phase B**: Generate structured brief, route to EPCI-0

See `epci-discover.md` for full documentation.

---

### 7.2 `epci-0-briefing` — Entry Point & Routing

**Purpose:** Clarify the request, build functional brief, assess complexity, route to workflow.

**Thinking mode:** Extended thinking recommended.

**Supported flags:** `--preview`, `--uc`, `--verbose`, `--introspect`, `--dry-run`

**Supported personas:** All (with auto-activation)

**Inputs:**
- Raw description of the task/ticket (or `EPCI_READY_BRIEF` from discover)
- Optional: `FEATURE_SLUG`, `EXECUTION_MODE`, `FROM_PROMPTOR`

**Outputs:**
- `EPCI_READY_BRIEF` — Compact brief for downstream commands
- Feature Document created: `docs/features/<slug>.md` (section 1)
- Routing recommendation with next command

**Phases (INTERACTIVE):**
- **Phase A**: Understand, ask questions, propose AI suggestions, draft brief (NO file writes)
- **Phase B**: Finalize brief, write to Feature Document, suggest next command

**Output Layout:**
```markdown
## 1. Understanding
## 2. Draft — Functional Brief (EPCI-0)
## 3. EPCI_READY_BRIEF
## 4. Complexity & Workflow Recommendation
## 5. Feature Document Update (Phase B only)
---
## QUESTIONS & SUGGESTIONS
```

---

### 7.3 `epci-micro` — Ultra-Light Workflow (TINY)

**Purpose:** Fast-lane for very small, low-risk changes.

**Thinking mode:** None needed.

**Supported flags:** `--preview`, `--safe-mode`, `--uc`, `--verbose`, `--validate`, `--dry-run`

**Supported personas:** Frontend, Backend (limited)

**Scope:**
- 1 file (max 2 if same module, no new logic)
- < 50 LOC
- No schema changes, no new business logic
- Examples: typo, CSS, log message, trivial guard

**Inputs:**
- `EPCI_READY_BRIEF` from `epci-0-briefing`

**Behaviour:**
- Single-pass workflow
- Explore → Micro-plan → Code → Tests → Commit
- Updates Feature Document minimally
- Provides simple commit message format

**Output Layout:**
```markdown
## 1. Objective & Scope
## 2. Micro-plan (auto-validated)
## 3. Code Change
## 4. Micro-tests
## 5. Feature Document Update
## 6. Commit
```

**Guardrails:**
- If scope exceeds TINY → STOP and recommend `epci-soft` or full EPCI

---

### 7.4 `epci-soft` — Light Workflow (SMALL)

**Purpose:** Complete workflow for small, well-scoped changes.

**Thinking mode:** Extended thinking recommended for Phase A.

**Supported flags:** `--preview`, `--safe-mode`, `--uc`, `--verbose`, `--introspect`, `--validate`, `--dry-run`

**Supported personas:** All

**Scope:**
- 2–3 files OR 1 file with new logic
- 50–200 LOC
- Single module, low risk
- Examples: simple validation, minor UI change, light business tweak

**Inputs:**
- `EPCI_READY_BRIEF` from `epci-0-briefing`

**Behaviour:**
- **Actually implements code** (not just guidance)
- Phase A: Explore & Plan (read-only)
- Phase B: Code & Inspect (after validation)
- Updates Feature Document with plan and completion note
- Provides commit message with scope

**Output Layout:**
```markdown
## 1. Understanding & Scope
## 2. Explore — Context & Impact
## 3. Plan — Light Technical Plan (EPCI-Soft)
## 4. Implementation — Code Changes
## 5. Inspect — Tests & Verification
## 6. Feature Document Update
## 7. Wrap-up — Commit & PR
```

**Guardrails:**
- If scope exceeds SMALL → STOP and recommend full EPCI

---

### 7.5 `epci-1-analyse` — Explore & Plan (Full EPCI)

**Purpose:** Deep exploration and detailed planning for STANDARD/LARGE changes.

**Thinking mode:** Think hard recommended.

**Supported flags:** `--preview`, `--uc`, `--verbose`, `--introspect`, `--dry-run`

**Supported personas:** All (with auto-activation)

**Scope:**
- STANDARD: 3–10 files, 200–1000 LOC, 1–3 modules
- LARGE: > 10 files, > 1000 LOC, > 3 modules

**Inputs:**
- `EPCI_READY_BRIEF` from `epci-0-briefing`

**Behaviour:**
- **Strictly read-only** — no implementation code
- Explores codebase thoroughly
- Produces detailed implementation plan
- Updates Feature Document section 2 only
- Suggests `epci-2-code` as next command

**Output Layout:**
```markdown
## 1. Understanding & Scope
## 2. Explore — Codebase Analysis
## 3. Plan — Detailed Implementation Plan (EPCI-1)
## 4. Assumptions (AUTO mode only)
## 5. Feature Document Update
## 6. Next Command
```

**Guardrails:**
- If scope is smaller than expected → suggest `epci-micro` or `epci-soft`
- If scope is larger than expected → flag risks, suggest breaking down

---

### 7.6 `epci-2-code` — Code & Test (Full EPCI)

**Purpose:** Implement the plan and run tests.

**Thinking mode:** None needed (plan is already validated).

**Supported flags:** `--preview`, `--safe-mode`, `--uc`, `--verbose`, `--validate`, `--dry-run`

**Supported personas:** All

**Inputs:**
- `FEATURE_SLUG`
- Feature Document with populated `## 2. Technical Plan`

**Behaviour:**
- **Writes actual code** to the repository
- Follows the plan from `epci-1-analyse`
- Runs tests including all edge cases
- Documents deviations in Implementation Notes
- Suggests `epci-3-finalize` as next command

**Output Layout:**
```markdown
## 1. Plan Summary
## 2. Implementation
## 3. Testing
## 4. Updated Checklist
## 5. Feature Document Update
## 6. Next Command
```

**Guardrails:**
- Only modify files listed in the plan
- Document all deviations
- Stop if scope creep detected

---

### 7.7 `epci-3-finalize` — Inspect & Document (Full EPCI)

**Purpose:** Final inspection, documentation, and commit preparation.

**Thinking mode:** None needed.

**Supported flags:** `--uc`, `--verbose`, `--validate`, `--safe-mode`, `--dry-run`

**Supported personas:** All (QA auto-activated)

**Prerequisites:** `epci-1-analyse` and `epci-2-code` completed.

**Inputs:**
- `FEATURE_SLUG`
- Feature Document with sections 1 and 2 populated

**Behaviour:**
- Inspects implementation vs plan
- Prepares PR description and commit message
- Updates documentation (Changelog mandatory)
- Writes `## 3. Final Report` in Feature Document
- Provides complete git commands

**Output Layout:**
```markdown
## 1. Inspection Summary
## 2. PR Description
## 3. Documentation Updates
## 4. Commit Preparation
## 5. Feature Document Update
## 6. Final Notes
## 7. Next Steps for User
## 8. Workflow Complete
```

**Guardrails:**
- Never implement new features or refactor
- Never modify sections 1 or 2
- Never commit unrelated files

---

### 7.8 `epci-hotfix` — Emergency Workflow

**Purpose:** Handle production-critical incidents with inverted workflow.

**Thinking mode:** None (speed is priority).

**Supported flags:** `--uc`, `--verbose`, `--validate`

**Supported personas:** None (emergency mode)

**Constraints:**
- P0/P1 incidents only
- Max 1 file, max 50 LOC
- Post-mortem within 24h

**Workflow:** Declare → Diagnose → Fix → Deploy → Document

See `epci-hotfix.md` for full documentation.

---

### 7.9 `epci-spike` — Exploration Workflow

**Purpose:** Time-boxed technical exploration before committing to a feature.

**Thinking mode:** Think hard recommended.

**Supported flags:** `--preview`, `--uc`, `--verbose`, `--introspect`, `--dry-run`

**Supported personas:** Architect, Security, Performance, Frontend, Backend, DevOps

**Constraints:**
- Time-box: 30min to 4h max
- Output: Decision (GO / NO-GO / MORE RESEARCH)
- Code is throwaway

**Workflow:** Frame → Explore → Synthesize → Decide

See `epci-spike.md` for full documentation.

---

## 8. Typical Workflows

### 8.1 Vague Request (epci-discover → epci-0)

**Scenario:** User says "Make the app faster"

1. Run `epci-discover` with the vague request
2. Answer the 5-10 clarifying questions
3. EPCI-discover generates structured `EPCI_READY_BRIEF`
4. Run `epci-0-briefing` with the generated brief
5. Continue with normal EPCI routing

**Typical duration:** 15–30 minutes (discovery) + standard workflow

### 8.2 TINY Change (epci-micro)

**Scenario:** Fix a typo in a translation file.

1. Run `epci-0-briefing` with the task description
2. EPCI-0 assesses as TINY, routes to `epci-micro`
3. Run `epci-micro` with `FEATURE_SLUG`
4. Review output, run suggested commit

**Typical duration:** 5–15 minutes

### 8.3 SMALL Change (epci-soft)

**Scenario:** Add a simple validation rule to a form.

1. Run `epci-0-briefing` with the task description
2. EPCI-0 assesses as SMALL, routes to `epci-soft`
3. Run `epci-soft` with `FEATURE_SLUG`
4. Review Phase A plan, validate
5. EPCI-Soft executes Phase B, implements code
6. Review output, run suggested commit

**Typical duration:** 30–90 minutes

### 8.4 STANDARD/LARGE Change (Full EPCI)

**Scenario:** Implement stay tax calculation feature.

1. Run `epci-0-briefing` with the task description
2. Answer clarification questions, validate AI suggestions
3. EPCI-0 assesses as STANDARD, routes to `epci-1-analyse`
4. Run `epci-1-analyse` with `FEATURE_SLUG`
5. Review exploration and plan, validate
6. Run `epci-2-code` with `FEATURE_SLUG`
7. Review implementation, verify tests
8. Run `epci-3-finalize` with `FEATURE_SLUG`
9. Review PR description, run suggested commit

**Typical duration:** 2–8 hours (depending on complexity)

---

## 9. Feature Document Lifecycle

### 9.1 Creation (EPCI-0)

```markdown
# Stay tax calculation

## 1. Functional Brief — EPCI-0

*(Managed by epci-0-briefing. Do not modify manually.)*

- Objective: Calculate stay tax for seasonal rentals
- Functional requirements:
  - [FR1] Calculate tax based on nights and category
  - [FR2] Display on booking summary
- Acceptance criteria:
  - [AC1] Tax correctly calculated for various durations

## 2. Technical Plan — EPCI-1

*(Managed by epci-1-analyse or epci-soft. Do not modify manually.)*

*(To be filled by downstream command.)*

## 3. Final Report — EPCI-3

*(Managed by epci-3-finalize or epci-soft. Do not modify manually.)*

*(To be filled after implementation.)*
```

### 9.2 After Planning (EPCI-1 or Soft)

```markdown
## 2. Technical Plan — EPCI-1

*(Managed by epci-1-analyse or epci-soft. Do not modify manually.)*

### Scope & Goal
Implement stay tax calculation...

### Proposed Changes

| File | Change type | Description |
|------|-------------|-------------|
| `src/Domain/StayTaxCalculator.php` | new | Tax calculation service |
| `src/Application/BookingService.php` | modify | Integrate tax |

### Implementation Checklist
- [ ] Create StayTaxCalculator
- [ ] Integrate into BookingService
- [ ] Add unit tests
```

### 9.3 After Completion (EPCI-3 or Soft)

```markdown
## 3. Final Report — EPCI-3

*(Managed by epci-3-finalize or epci-soft. Do not modify manually.)*

### Completion Status
- **Date:** 2025-01-15
- **Status:** ✅ Complete
- **Confidence:** 90%
- **PR:** #124
- **Commit:** abc1234

### Summary of Changes
- Added StayTaxCalculator service
- Integrated into BookingService
- Added 15 unit tests

### Testing Summary
- Unit tests: 15 tests, all passing
- Integration tests: 3 tests, all passing

### Follow-ups (out of scope)
- [ ] Add invoice template integration
- [ ] Add admin UI for tax rates
```

---

## 10. Section Protection Rules

Each EPCI command has specific sections it can modify:

| Command | Section 1 (Functional Brief) | Section 2 (Technical Plan) | Section 3 (Final Report) |
|---------|------------------------------|---------------------------|-------------------------|
| `epci-discover` | ❌ Never | ❌ Never | ❌ Never |
| `epci-0-briefing` | ✅ Create/Update | ❌ Never | ❌ Never |
| `epci-micro` | ➕ Append note | ➕ Append note | ➕ Append completion note |
| `epci-soft` | ➕ Minor enrichment | ✅ Add plan subsection | ✅ Add completion note |
| `epci-1-analyse` | ❌ Never | ✅ Create/Update | ❌ Never |
| `epci-2-code` | ❌ Never | ➕ Add Implementation Notes | ❌ Never |
| `epci-3-finalize` | ❌ Never | ❌ Never | ✅ Create/Update |

**Legend:**
- ✅ = Full control (create or replace)
- ➕ = Append only (add subsection or note)
- ❌ = Never modify

---

## 11. Guardrails & Scope Validation

### 11.1 Scope Creep Detection

Every EPCI command MUST validate that the task matches the expected complexity:

**If scope is SMALLER than expected:**
- Note that a lighter workflow could be used
- Complete the task anyway (already started)
- Suggest lighter workflow for similar future tasks

**If scope is LARGER than expected:**
- STOP immediately
- Document the scope creep
- Recommend appropriate workflow
- Ask user how to proceed

### 11.2 Rerouting Examples

**From epci-micro to epci-soft:**
```markdown
⚠️ This task is not suitable for `epci-micro`.

**Reason:** The change will likely impact 3+ files and introduce new validation logic.

**Recommendation:** Use `epci-soft` for this SMALL-level change.
```

**From epci-soft to full EPCI:**
```markdown
⚠️ This task is not suitable for `epci-soft` anymore (scope is beyond SMALL).

**Reason:**
- 6 files identified (> 3)
- Schema changes required
- Multiple modules impacted

**Recommendation:** Use the full EPCI workflow:
- epci-1-analyse
- epci-2-code
- epci-3-finalize
```

---

## 12. Quick Reference

### 12.1 Command Cheat Sheet

| Command | Purpose | Writes Code? | Thinking Mode | Flags | Next Command |
|---------|---------|--------------|---------------|-------|--------------|
| `epci-discover` | Clarify vague requests | No | think harder | preview, uc, introspect | `epci-0-briefing` |
| `epci-0-briefing` | Clarify & Route | No | think harder | preview, uc, introspect | micro/soft/1 |
| `epci-micro` | TINY changes | Yes | None | preview, safe-mode, validate | (done) |
| `epci-soft` | SMALL changes | Yes | think harder (A) | all | (done) |
| `epci-1-analyse` | Explore & Plan | No | think hard | preview, uc, introspect | `epci-2-code` |
| `epci-2-code` | Implement & Test | Yes | None | preview, safe-mode, validate | `epci-3-finalize` |
| `epci-3-finalize` | Inspect & Commit | No | None | uc, validate | (done) |
| `epci-hotfix` | Emergency fix | Yes | None | uc, validate | (done) |
| `epci-spike` | Technical exploration | No | think hard | preview, uc, introspect | GO → `epci-0` |

### 12.2 Persona Quick Reference

| Persona | Flag | Auto-triggers |
|---------|------|---------------|
| Architect | `--persona-architect` | LARGE complexity, multi-module |
| Security | `--persona-security` | auth/, security/, crypto/ |
| Performance | `--persona-performance` | "optimize", "slow", "cache" |
| QA | `--persona-qa` | tests/, "coverage", EPCI-3 |
| Frontend | `--persona-frontend` | .tsx, .jsx, components/ |
| Backend | `--persona-backend` | Controller, Service, Repository |
| DevOps | `--persona-devops` | Dockerfile, .yml, deploy |

### 12.3 Flag Quick Reference

| Flag | Effect | Best For |
|------|--------|----------|
| `--preview` | Show what would happen | Before executing |
| `--safe-mode` | Confirm each change | Critical code |
| `--uc` | 70% less output | Long outputs |
| `--introspect` | Show reasoning | Debugging decisions |
| `--validate` | Extra checks | Quality assurance |

### 12.4 Thinking Mode Hierarchy

| Level | Trigger | Budget | Use Case |
|-------|---------|--------|----------|
| Basic | "think" | Low | Quick decisions |
| Standard | "think hard" | Medium | EPCI-1, spike |
| Extended | "think harder" | High | EPCI-0, discover, soft |
| Maximum | "ultrathink" | Maximum | Critical architecture |

### 12.5 Minimal Quickstart

**For any task:**

1. If request is vague, start with `epci-discover`:
   ```text
   epci-discover
   $ARGUMENTS = <your vague idea>
   ```

2. Otherwise, start with `epci-0-briefing`:
   ```text
   epci-0-briefing
   $ARGUMENTS = <your task description>
   ```

3. Follow the routing recommendation.

4. Use the `EPCI_READY_BRIEF` provided as `$ARGUMENTS` for the next command.

5. Continue until workflow completion.

### 12.6 File Outputs

| File | Created by | Purpose |
|------|------------|---------|
| `docs/features/<slug>.md` | All commands | Feature Document (single source of truth) |
| `docs/spikes/<slug>.md` | epci-spike | Spike Report |

---

## 13. Best Practices

### 13.1 For Requesters

1. **Provide context** — Ticket numbers, module names, URLs
2. **Be specific** — Clear acceptance criteria
3. **Answer questions** — Clarification questions improve quality
4. **Review AI suggestions** — They often catch edge cases
5. **Use discover for vague ideas** — Don't force unclear requests through EPCI-0

### 13.2 For Developers

1. **Trust the routing** — Let EPCI-0 assess complexity
2. **Validate plans** — Review before Phase B
3. **Check guardrails** — If scope creeps, stop and reroute
4. **Keep the trace** — Feature Document is the source of truth
5. **Use thinking modes** — "think harder" for EPCI-0, "think hard" for EPCI-1
6. **Leverage sub-agents** — Deep exploration without context pollution
7. **Use `/clear` often** — Keep context focused between tasks
8. **Use flags wisely** — `--preview` before critical changes, `--uc` for long outputs
9. **Activate personas** — Use `--persona-security` for auth changes, etc.

### 13.3 For Teams

1. **Consistent slugs** — Use meaningful, stable feature slugs
2. **Review Feature Documents** — They're part of the codebase
3. **Link to tickets** — Reference in EPCI_READY_BRIEF
4. **Archive completed features** — Move to `docs/features/archive/` if needed
5. **Share persona patterns** — Document which personas work best for your stack

---

## 14. Migration from V2.6

If you're migrating from v2.6:

| V2.6 | V2.7 |
|------|------|
| No pre-briefing for vague requests | `epci-discover` for unclear requests |
| No universal flags | 7 flags across all commands |
| Implicit expertise | 7 explicit personas |
| No `--preview` or `--safe-mode` | Safety flags available |
| No compressed output option | `--uc` for 70% reduction |
| No reasoning visibility | `--introspect` shows decisions |

### Key Changes in v2.7:

1. **Discovery Mode** — `epci-discover` for vague requests
2. **Universal Flags** — `--preview`, `--safe-mode`, `--uc`, `--introspect`, `--validate`, `--dry-run`, `--verbose`
3. **Expert Personas** — 7 personas with manual and auto-activation
4. **Enhanced Workflow Diagram** — Includes discover path
5. **Flag Compatibility Matrix** — Clear documentation of what works where
6. **Persona Compatibility Matrix** — Clear documentation of persona availability

### Previous Changes (preserved):

- All V2.6 features (hotfix, spike, thinking modes, sub-agents)
- All V2.5 features (context management, AI suggestions)
- All V2.4 features (unified format, English throughout)

---

## 15. Summary

The EPCI workflow (v2.7) provides:

1. **Structure** — 4 phases: Explore → Plan → Code → Inspect
2. **Flexibility** — 3 tiers: Micro (TINY), Soft (SMALL), Full (STANDARD/LARGE)
3. **Safety** — Phase A/B separation, guardrails, scope validation, safety flags
4. **Traceability** — Single Feature Document per feature
5. **Productivity** — Right-sized workflow for each task
6. **Consistency** — Unified formats, English throughout, standardized conventions
7. **Intelligence** — Thinking mode hierarchy for optimal analysis
8. **Efficiency** — Sub-agents pattern for context preservation
9. **Customization** — Universal flags for behavior modification
10. **Expertise** — Personas for specialized analysis

Start every task with `epci-discover` (if vague) or `epci-0-briefing` (if clear), follow the routing, and let EPCI guide you through a structured, documented development process.

**v2.7 brings:**
- Discovery mode for vague requests
- Universal flags for safety and efficiency
- Expert personas for specialized analysis
- Enhanced compatibility matrices

---

## 16. Related Documentation

| Document | Purpose |
|----------|---------|
| `epci-discover.md` | Pre-briefing discovery mode |
| `epci-flags.md` | Universal flags reference |
| `epci-personas.md` | Expert personas system |
| `epci-hotfix.md` | Emergency workflow |
| `epci-spike.md` | Exploration workflow |

---

*This guide can be stored as `docs/epci-workflow-guide.md` in your repository.*
