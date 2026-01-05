# EPCI Commands Baseline Inventory — Pre-Optimization

> **Date**: 2026-01-05
> **Purpose**: Functional reference before command optimization
> **Total Commands**: 11

---

## 1. FLAGS INVENTORY

### Thinking Flags

| Flag | Commands | Auto-Trigger |
|------|----------|--------------|
| `--think` | epci, quick, debug, decompose | 3-10 files |
| `--think-hard` | epci, debug, brainstorm, decompose | >10 files, refactoring |
| `--ultrathink` | epci, decompose | Never (explicit) |

### Compression Flags

| Flag | Commands | Auto-Trigger |
|------|----------|--------------|
| `--uc` | epci, quick | context > 75% |
| `--verbose` | epci | Never |

### Workflow Flags

| Flag | Commands | Auto-Trigger |
|------|----------|--------------|
| `--safe` | epci, quick | Sensitive files |
| `--no-hooks` | epci, quick, commit | Never |
| `--continue` | epci | Never |

### Turbo Flag

| Flag | Commands | Effect |
|------|----------|--------|
| `--turbo` | brief, epci, quick, brainstorm, debug | Speed mode |

### Persona Flags (F09)

| Flag | Commands |
|------|----------|
| `--persona-architect` | All (via flags-system) |
| `--persona-frontend` | All |
| `--persona-backend` | All |
| `--persona-security` | All |
| `--persona-qa` | All |
| `--persona-doc` | All |

### MCP Flags (F12)

| Flag | Commands | Effect |
|------|----------|--------|
| `--c7` | brief, epci, brainstorm, debug, decompose, rules | Context7 |
| `--seq` | epci, brainstorm, debug | Sequential |
| `--magic` | epci | Magic (21st.dev) |
| `--play` | epci | Playwright |
| `--no-mcp` | All | Disable all MCP |

### Wave Flags

| Flag | Commands |
|------|----------|
| `--wave` | epci |
| `--wave-strategy` | epci |

### Quick Flags (F13)

| Flag | Commands |
|------|----------|
| `--autonomous` | quick |
| `--quick-turbo` | quick |
| `--no-bp` | quick (alias) |

### Command-Specific Flags

| Flag | Command | Effect |
|------|---------|--------|
| `--large` | epci | Alias --think-hard --wave |
| `--full` | debug | Force Complet mode |
| `--no-report` | debug | Skip Debug Report |
| `--commit` | debug | Generate commit context |
| `--context <path>` | debug | Link Feature Document |
| `--template <name>` | brainstorm | Force template |
| `--no-hmw` | brainstorm | Disable HMW questions |
| `--quick` | brainstorm | Fast mode (3 iter max) |
| `--no-security` | brainstorm | Skip @security-auditor |
| `--no-plan` | brainstorm | Skip @planner |
| `--force` | rules | Overwrite existing |
| `--validate-only` | rules | Only validate |
| `--dry-run` | rules, commit | Show without executing |
| `--stack <name>` | rules | Force stack detection |
| `--no-validate` | rules | Skip validation |
| `--skip-libs` | rules | Skip library rules |
| `--refresh-libs` | rules | Only refresh library rules |
| `--output <dir>` | decompose | Output directory |
| `--min-days <n>` | decompose | Min effort per sub-spec |
| `--max-days <n>` | decompose | Max effort per sub-spec |
| `--auto-commit` | commit | Skip breakpoint |
| `--amend` | commit | Amend last commit |

---

## 2. MCP SERVERS

| Server | Flag | Activation Conditions |
|--------|------|----------------------|
| Context7 | `--c7` | persona architect/backend/doc, import keywords |
| Sequential | `--seq` | `--think-hard`, persona architect/security |
| Magic | `--magic` | persona frontend, *.jsx/*.tsx files |
| Playwright | `--play` | persona frontend/qa, *.spec.ts files |

### Persona × MCP Matrix

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | **auto** | **auto** | - | - |
| frontend | **auto** | - | **auto** | **auto** |
| backend | **auto** | **auto** | - | - |
| security | - | **auto** | - | - |
| qa | - | - | - | **auto** |
| doc | **auto** | - | - | - |

---

## 3. SUBAGENTS INVENTORY

### Core Subagents

| Agent | Model | Commands Using | Condition |
|-------|-------|----------------|-----------|
| `@plan-validator` | opus | epci | Always P1 |
| `@code-reviewer` | opus | epci, debug | Always P2, Complet mode |
| `@security-auditor` | opus | epci, brainstorm, debug | auth/security files |
| `@qa-reviewer` | sonnet | epci | >5 test files |
| `@doc-generator` | sonnet | epci | Always P3 |
| `@decompose-validator` | opus | decompose | Always |
| `@rules-validator` | opus | rules | Always |

### Turbo Subagents

| Agent | Model | Commands Using | Role |
|-------|-------|----------------|------|
| `@clarifier` | haiku | brief, brainstorm (turbo) | Fast clarification |
| `@planner` | sonnet | epci, quick, brainstorm | Rapid planning |
| `@implementer` | sonnet | epci, quick | Code implementation |

### Exploration Agent

| Agent | Model | Commands Using |
|-------|-------|----------------|
| `@Explore` | haiku/sonnet | brief, brainstorm, debug, quick |

---

## 4. SKILLS INVENTORY

### Skills by Command

| Command | Skills Loaded |
|---------|---------------|
| brief | project-memory, epci-core, architecture-patterns, flags-system, mcp, personas, [stack] |
| epci P1 | project-memory, epci-core, architecture-patterns, flags-system, [stack] |
| epci P2 | testing-strategy, code-conventions, flags-system, [stack] |
| epci P3 | git-workflow |
| quick | project-memory, epci-core, code-conventions, flags-system, [stack] |
| brainstorm | brainstormer, project-memory, architecture-patterns, clarification-intelligente |
| debug | project-memory, debugging-strategy, mcp, [stack] |
| decompose | project-memory, architecture-patterns, flags-system, mcp |
| rules | rules-generator, project-memory, [stack] |
| commit | git-workflow |
| promptor | promptor |
| create | component-advisor, flags-system, [creator-skill] |
| memory | project-memory |

### All Skills Referenced

1. project-memory
2. epci-core
3. architecture-patterns
4. flags-system
5. mcp
6. personas
7. testing-strategy
8. code-conventions
9. git-workflow
10. brainstormer
11. clarification-intelligente
12. debugging-strategy
13. rules-generator
14. promptor
15. component-advisor
16. breakpoint-metrics
17. proactive-suggestions
18. learning-optimizer
19. [stack skills: php-symfony, javascript-react, python-django, java-springboot]

---

## 5. HOOKS INVENTORY

### Hook Points

| Hook | Commands Using |
|------|----------------|
| `pre-brief` | brief |
| `post-brief` | brief |
| `pre-phase-1` | epci |
| `post-phase-1` | epci |
| `pre-phase-2` | epci |
| `post-phase-2` | epci |
| `post-phase-3` | epci, quick |
| `on-breakpoint` | epci |
| `pre-agent` | epci |
| `post-agent` | epci |
| `pre-debug` | debug |
| `post-diagnostic` | debug |
| `post-debug` | debug |
| `pre-commit` | commit |
| `post-commit` | commit |

### Hook Execution Pattern

```bash
python3 src/hooks/runner.py <hook-type> --context '{...}'
```

---

## 6. BREAKPOINTS INVENTORY

| Command | Breakpoints | Skippable |
|---------|-------------|-----------|
| brief | 1 (Analysis Review) | No |
| epci | 3 (BP1, BP2, pre-commit) | --turbo reduces to 1 |
| quick | 1 (Lightweight 3s) | --autonomous |
| debug | 1 (Complet mode only) | --turbo |
| decompose | 1 (Validation) | No |
| brainstorm | Multiple (iterations) | --quick, --turbo |
| commit | 1 (pre-commit) | --auto-commit |
| rules | 0 | N/A |
| memory | 0 | N/A |
| promptor | 1 (multi-task checkpoint) | Single task |
| create | 0 (interactive) | N/A |

---

## 7. OUTPUT FILES INVENTORY

| Command | Output Files |
|---------|-------------|
| brief | `docs/features/<slug>.md` (Feature Document) |
| epci | Updates Feature Document §2, §3 |
| quick | `.project-memory/sessions/quick-{timestamp}.json`, `.epci-commit-context.json` |
| brainstorm | `./docs/briefs/[slug]/brief-*.md`, `./docs/briefs/[slug]/journal-*.md` |
| debug | `docs/debug/<slug>-<date>.md`, `.epci-commit-context.json` |
| decompose | `docs/specs/{slug}/INDEX.md`, `docs/specs/{slug}/S*.md` |
| rules | `.claude/CLAUDE.md`, `.claude/rules/*.md` |
| memory | `.project-memory/*` |
| commit | Cleans `.epci-commit-context.json` |
| promptor | Notion API export |
| create | `src/skills/*`, `src/commands/*`, `src/agents/*` |

---

## 8. TOOL PERMISSIONS

| Command | allowed-tools |
|---------|---------------|
| brief | Read, Write, Glob, Grep, Bash, Task |
| epci | Read, Write, Edit, Bash, Grep, Glob, Task |
| quick | Read, Write, Edit, Bash, Grep, Glob, Task |
| brainstorm | Read, Write, Bash, Glob, Grep, Task, WebFetch, WebSearch |
| debug | Read, Glob, Grep, Bash, Task, WebFetch, WebSearch, Write, Edit |
| decompose | Read, Write, Bash, Grep, Glob, Task, WebFetch |
| rules | Read, Write, Glob, Grep, Bash, Task |
| memory | Read, Write, Glob, Grep, Bash |
| commit | Read, Write, Bash, Glob |
| promptor | Read, Glob, Grep, Write, Bash |
| create | Read, Write, Glob, Bash |

---

## 9. COMMAND STATISTICS (Pre-Optimization)

| Command | Words | Lines | Est. Tokens |
|---------|-------|-------|-------------|
| epci.md | 3064 | 725 | ~6200 |
| quick.md | 2103 | 582 | ~4100 |
| memory.md | 2011 | 576 | ~4000 |
| brief.md | 2122 | 510 | ~3900 |
| decompose.md | 1766 | 529 | ~3500 |
| commit.md | 1180 | 398 | ~2900 |
| debug.md | 1493 | 455 | ~2800 |
| rules.md | 1425 | 418 | ~2700 |
| brainstorm.md | 2284 | 580 | ~2400 |
| promptor.md | 961 | 289 | ~1600 |
| create.md | 639 | 224 | ~1100 |
| **TOTAL** | **19048** | **5286** | **~35200** |

---

## 10. VALIDATION CHECKSUMS

To verify no functional regression after optimization, run:

```bash
# Extract all flags
grep -roh '\-\-[a-z-]*' src/commands/*.md | sort -u > /tmp/flags-after.txt

# Extract all agents
grep -roh '@[a-z-]*' src/commands/*.md | sort -u > /tmp/agents-after.txt

# Extract all skills
grep -roh '[a-z-]*-[a-z]*' src/commands/*.md | grep -E '^(project|epci|architecture|testing|git|code|debug|rules|brain|mcp|flag|persona|clarification|proactive|breakpoint|learning|component)' | sort -u > /tmp/skills-after.txt

# Extract all hooks
grep -roh "'\(pre\|post\|on\)-[a-z-]*'" src/commands/*.md | sort -u > /tmp/hooks-after.txt
```

Compare with baseline to ensure no elements are missing.

---

*Baseline inventory generated for optimization comparison*
