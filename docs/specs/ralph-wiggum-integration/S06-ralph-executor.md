# Specification — S06: Subagent @ralph-executor

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S06
> **Estimated effort**: 3 day(s)
> **Dependencies**: S01, S04
> **Blocks**: S07

---

## 1. Context

This sub-spec implements the **@ralph-executor** subagent, which encapsulates the logic for executing individual stories. It routes through `/brief` and then to `/quick` or `/epci` based on complexity, generating minimal Feature Documents for traceability.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US4

---

## 2. Scope

### Included

- @ralph-executor subagent definition
- Integration with `/brief` for story analysis
- Routing to `/quick --autonomous` (TINY/SMALL)
- Routing to `/epci --autonomous` (STANDARD+)
- Minimal Feature Document generation
- `ralph-analyzer` skill for response analysis

### Excluded

- Circuit Breaker (S02)
- Response Analyzer library (S03) — but uses its concepts
- ralph_loop.sh (S04) — calls this agent
- /ralph command (S07)

---

## 3. Tasks

- [ ] Create `src/agents/ralph-executor.md`
  - [ ] Define agent metadata (model: sonnet, description)
  - [ ] Define input schema (story object from prd.json)
  - [ ] Define output schema (status, feature_doc_path, commit_hash)
  - [ ] Implement story execution flow:
    - [ ] Load parent spec context
    - [ ] Call `/brief` with story description
    - [ ] Route based on complexity result
    - [ ] Execute `/quick --autonomous` or `/epci --autonomous`
    - [ ] Generate minimal Feature Document
    - [ ] Return execution result

- [ ] Create `src/skills/core/ralph-analyzer/SKILL.md`
  - [ ] Analyze story execution results
  - [ ] Detect success/failure/blocked states
  - [ ] Extract relevant metrics (files changed, tests status)
  - [ ] Format output for ralph_loop.sh consumption

- [ ] Implement `/brief` integration:
  - [ ] Pass story context and parent spec
  - [ ] Capture complexity assessment
  - [ ] Handle exploration if needed

- [ ] Implement routing logic:
  - [ ] TINY/SMALL → `/quick --autonomous`
  - [ ] STANDARD/LARGE → `/epci --autonomous`
  - [ ] Pass `--no-breakpoints` for fully autonomous execution

- [ ] Implement Feature Document generation:
  - [ ] Minimal format (title, story ref, result, commit)
  - [ ] Store in `.ralph-docs/` directory
  - [ ] Link to parent spec

- [ ] Implement error handling:
  - [ ] Retry logic (max 3 retries)
  - [ ] Mark story as "failed" after max retries
  - [ ] Capture error details for diagnostics

- [ ] Write tests for @ralph-executor

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S06-AC1 | Given story to execute, When @ralph-executor invoked, Then /brief called with context | Integration test |
| S06-AC2 | Given /brief result TINY/SMALL, When routing, Then /quick --autonomous called | Routing test |
| S06-AC3 | Given /brief result STANDARD+, When routing, Then /epci --autonomous called | Routing test |
| S06-AC4 | Given execution complete and tests pass, When finished, Then minimal Feature Document generated | Doc generation test |
| S06-AC5 | Given story US-005 in S02, When @ralph-executor runs, Then S02.md loaded as context | Context loading test |
| S06-AC6 | Given story fails 3 times, When max retries reached, Then marked as "failed" | Retry test |

---

## 5. Technical Notes

### Agent Definition

```yaml
# src/agents/ralph-executor.md
name: ralph-executor
model: sonnet
description: Execute single Ralph story via /brief → /quick or /epci routing

input:
  story:
    id: string          # US-001
    title: string       # Story title
    parent_spec: string # S02-circuit-breaker.md
    estimated_minutes: number

output:
  status: success | failed | blocked
  feature_doc_path: string | null
  commit_hash: string | null
  error_message: string | null
```

### Execution Flow

```
@ralph-executor
    │
    ├── Load story from input
    │
    ├── Load parent spec context
    │   └── Read {parent_spec} file
    │
    ├── Call /brief with story
    │   └── Get complexity assessment
    │
    ├── Route based on complexity
    │   ├── TINY/SMALL → /quick --autonomous
    │   └── STANDARD+ → /epci --autonomous
    │
    ├── Execute workflow
    │   └── Wait for completion
    │
    ├── Generate Feature Document
    │   └── Minimal format in .ralph-docs/
    │
    └── Return result
        └── {status, feature_doc_path, commit_hash}
```

### Feature Document (Minimal)

```markdown
# Ralph Story — US-001

> **Story**: US-001 - Implement cb_init function
> **Parent Spec**: S02-circuit-breaker.md
> **Executed**: 2025-01-14T03:45:00Z
> **Status**: success

## Result

- Files modified: 2
- Tests: PASSING
- Commit: abc1234

## Details

[Link to parent spec](../S02-circuit-breaker.md)
```

### Autonomous Flags

```bash
# /quick autonomous mode
/quick --autonomous --no-breakpoints

# /epci autonomous mode
/epci --autonomous --no-breakpoints
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US4 — Subagent @ralph-executor**

- Given une story à exécuter, When @ralph-executor est invoqué, Then il appelle /brief avec le contexte
- Given le résultat de /brief, When la complexité est TINY/SMALL, Then /quick --autonomous est appelé
- Given le résultat de /brief, When la complexité est STANDARD+, Then /epci --autonomous est appelé
- Given l'exécution terminée, When les tests passent, Then un Feature Document minimal est généré

**Notes:**
- Encapsule la logique /brief → /quick ou /epci
- Permet le fresh context en mode script
- Génère des Feature Documents pour traçabilité EPCI

---

*Generated by /decompose — Project: ralph-wiggum-integration*
