# Agents Catalog

> Reference for Factory to recommend appropriate agents based on skill type and context.

## Agent Categories

### Validators (Quality Gates)

| Agent | Model | Trigger | Recommend if skill... |
|-------|-------|---------|----------------------|
| `plan-validator` | Opus | After Phase 1 | contains workflow/planification |
| `code-reviewer` | Opus | After implementation | generates code |
| `rules-validator` | Opus | After /rules | generates rules |
| `decompose-validator` | Opus | After /decompose | does PRD decomposition |

### Reviewers (Specialized Review)

| Agent | Model | Trigger | Recommend if skill... |
|-------|-------|---------|----------------------|
| `security-auditor` | Opus | auth/security files | touches auth, token, password, credentials |
| `qa-reviewer` | Sonnet | > 5 test files | generates tests or test patterns |

### Executors (Task Execution)

| Agent | Model | Trigger | Recommend if skill... |
|-------|-------|---------|----------------------|
| `implementer` | Sonnet | Phase 2 turbo | executes TDD tasks |
| `planner` | Sonnet | Phase 1 turbo | plans implementation tasks |
| `doc-generator` | Sonnet | Phase 3 | generates documentation |

### Brainstorm (Exploration)

| Agent | Model | Trigger | Recommend if skill... |
|-------|-------|---------|----------------------|
| `expert-panel` | Sonnet | `panel` command | is brainstorm type |
| `party-orchestrator` | Sonnet | `party` command | is brainstorm type |
| `ems-evaluator` | Haiku | Each brainstorm iteration | is brainstorm type |
| `technique-advisor` | Haiku | Weak EMS axes | is brainstorm type |
| `clarifier` | Haiku | Turbo mode | uses clarification engine |

### Utilities (Support)

| Agent | Model | Trigger | Recommend if skill... |
|-------|-------|---------|----------------------|
| `rule-clarifier` | Haiku | Ambiguous rules input | generates rules |
| `statusline-setup` | Haiku | @statusline-setup | DevX configuration |

## Recommendation Logic

### By Skill Type

```
user-invocable: true
├── Generates code? → code-reviewer
├── Touches auth/security? → security-auditor
├── Generates tests? → qa-reviewer
├── Generates documentation? → doc-generator
└── Uses planning workflow? → plan-validator

user-invocable: false (core skill)
├── Brainstorm type? → expert-panel, ems-evaluator, technique-advisor
├── Turbo execution? → implementer, planner, clarifier
├── Rules generation? → rules-validator, rule-clarifier
└── Decomposition? → decompose-validator
```

### By Domain Keywords

| Keywords in skill | Suggested agents |
|-------------------|------------------|
| `auth`, `login`, `token`, `password`, `credential` | security-auditor |
| `test`, `spec`, `coverage`, `mock` | qa-reviewer |
| `plan`, `phase`, `workflow`, `step` | plan-validator |
| `doc`, `readme`, `guide`, `tutorial` | doc-generator |
| `brainstorm`, `explore`, `ideate`, `panel` | expert-panel, ems-evaluator |
| `turbo`, `fast`, `quick`, `parallel` | implementer, planner, clarifier |
| `rule`, `convention`, `standard` | rules-validator, rule-clarifier |
| `decompose`, `prd`, `task`, `breakdown` | decompose-validator |

## Output Format for Factory

```
SUGGESTED AGENTS:
- code-reviewer (skill generates code)
- security-auditor (auth domain detected)

RATIONALE:
Based on skill type (user-invocable) and detected keywords (login, token).
```
