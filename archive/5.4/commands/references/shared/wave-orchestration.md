# Wave Orchestration — Multi-Agent DAG

> Shared reference for `--wave` flag behavior across commands

---

## Overview

When `--wave` flag is enabled, agents are executed using the DAG-based orchestrator
for parallel execution of independent agents.

---

## Orchestration Modes

| Mode | Description | Flag |
|------|-------------|------|
| Sequential | One agent at a time | `--sequential` |
| DAG | Respect dependencies, parallelize when possible | default with `--wave` |
| Parallel | All agents simultaneously (use with caution) | `--parallel` |

---

## DAG Structure (EPCI)

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

**Independent agents** (can run in parallel):
- @code-reviewer
- @security-auditor
- @qa-reviewer

**Sequential dependencies:**
- @plan-validator must complete before reviews
- @doc-generator runs after all reviews complete

---

## Performance

Parallel execution of independent agents reduces validation time by **30-50%** for LARGE features.

| Feature Size | Sequential | DAG (--wave) | Savings |
|--------------|------------|--------------|---------|
| STANDARD | ~5 min | ~4 min | 20% |
| LARGE | ~15 min | ~8 min | 47% |

---

## Configuration

**Default DAG:** `config/dag-default.yaml`

**Project-specific overrides:** `.project-memory/orchestration.yaml`

**Example override:**
```yaml
# Force sequential for debugging
orchestration:
  mode: sequential

# Custom agent order
dag:
  - @plan-validator
  - @code-reviewer
  - @security-auditor  # Run after code-reviewer
  - @qa-reviewer
  - @doc-generator
```

---

## Usage

```bash
# Enable wave orchestration
/epci --wave

# Large mode (includes --wave)
/epci --large

# Force sequential (debug)
/epci --wave --sequential
```

---

## Commands Using Wave

| Command | Default | With --wave |
|---------|---------|-------------|
| `/epci` | Sequential | DAG parallel |
| `/quick` | Sequential | Not supported |
| `/orchestrate` | DAG | Always DAG |

---

*Shared reference for wave orchestration*
