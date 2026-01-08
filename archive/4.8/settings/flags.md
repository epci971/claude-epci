# EPCI Flags Reference

> **Version**: 3.2.0
> **Date**: 2025-12-29

This document provides the complete reference for EPCI universal flags.

---

## Overview

EPCI flags provide fine-grained control over workflow behavior. They can be:
1. **Explicitly specified** by the user
2. **Auto-activated** based on context
3. **Combined** following precedence rules

---

## Thinking Flags

Control the depth of analysis and reasoning.

| Flag | Tokens | Auto-Trigger | Usage |
|------|--------|--------------|-------|
| `--think` | ~4K | 3-10 files impacted | Standard multi-file analysis |
| `--think-hard` | ~10K | >10 files OR refactoring OR migration | Deep system analysis |
| `--ultrathink` | ~32K | Never (explicit only) | Critical decisions, major refactoring |

### Examples

```bash
# Standard analysis for medium complexity
/epci --think

# Deep analysis for large refactoring
/epci --think-hard

# Critical architectural decision
/epci --ultrathink
```

---

## Compression Flags

Manage token usage and output verbosity.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--uc` | Ultra-compressed output (30-50% token reduction) | context > 75% used |
| `--verbose` | Full detailed output | Never |

### `--uc` Compression Techniques

When `--uc` is active:
- Use symbols: `✓` / `✗` / `⚠️` instead of words
- Use abbreviations: `impl` for implementation, `cfg` for configuration
- Omit optional explanations
- Compact table formats

### Examples

```bash
# Force compressed output
/epci --uc

# Force verbose output (overrides auto-uc)
/epci --verbose
```

---

## Reformulation Flags

Control brief reformulation for fuzzy/voice-dictated inputs.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--rephrase` | Force reformulation of brief before analysis | Never (explicit only) |
| `--no-rephrase` | Skip reformulation even if brief is fuzzy | Never (explicit only) |

### Fuzziness Score Auto-Trigger

Reformulation is auto-triggered based on a **fuzziness score** (0-100%):

```
Fuzziness Score = (
    (1 - domain_confidence) × 35% +
    (gap_count / 8) × 25% +
    (1 - scope_clarity) × 20% +
    hesitation_density × 20%
)

Thresholds:
- > 60%  → Auto-trigger reformulation
- 40-60% → Suggest reformulation
- < 40%  → Skip reformulation
```

### Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Domain confidence | 35% | Low domain detection = fuzzy |
| Gap count | 25% | Many high-priority gaps = fuzzy |
| Scope clarity | 20% | Vague terms + short brief = fuzzy |
| Hesitation density | 20% | Voice artifacts (euh, um...) detected |

### Voice Artifact Detection

Hesitations and fillers that increase fuzziness score:

| Type | French | English |
|------|--------|---------|
| Hesitations | euh, heu, hum, hmm, bah, ben | uh, um, er, erm, ah |
| Fillers | tu vois, genre, quoi, voilà, en fait | you know, like, actually, so |

### Reformulation Output

When triggered, the brief is restructured into:

```
**Objectif**: [What to achieve]
**Contexte**: [Technical context from exploration]
**Contraintes**: [Identified constraints]
**Critères de succès**: [Success criteria based on template type]
```

### --turbo Mode Behavior

| Aspect | Standard | Turbo |
|--------|----------|-------|
| Auto-trigger threshold | > 60% | > 70% |
| Auto-accept reformulation | Never | If confidence > 80% |
| Breakpoint format | Full | Compact |

### Examples

```bash
# Force reformulation for voice-dictated brief
/brief --rephrase "euh faudrait un truc pour gérer les users"

# Skip reformulation even if detected as fuzzy
/brief --no-rephrase "quick dirty fix asap"

# Combined with turbo (higher threshold)
/brief --turbo --rephrase "add auth feature"
```

### Precedence

| Flag Combination | Result |
|------------------|--------|
| `--rephrase` + `--no-rephrase` | `--no-rephrase` wins (explicit skip) |
| `--rephrase` + `--turbo` | Rephrase with turbo thresholds (70%) |
| `--no-rephrase` + high fuzziness | Skip reformulation (explicit override) |

---

## Workflow Flags

Control execution safety and hooks.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--safe` | Maximum validations, extra confirmations | Sensitive files detected |
| `--no-hooks` | Disable all hook execution | Never |

### Sensitive File Patterns (trigger `--safe`)

```
**/auth/**
**/security/**
**/payment/**
**/password/**
**/api/v*/admin/**
```

### Examples

```bash
# Safe mode for security-sensitive changes
/epci --safe

# Disable hooks for testing or CI/CD
/epci --no-hooks
```

---

## Turbo Flag

**Speed-optimized mode** that reduces workflow time by 30-50% for experienced projects.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--turbo` | Speed mode: adaptive models, parallel reviews, reduced breakpoints | `.project-memory/` exists AND category != LARGE |

### What `--turbo` Changes

| Aspect | Standard | Turbo |
|--------|----------|-------|
| **Clarification** | Full questions | @clarifier (Haiku) — 2-3 targeted questions |
| **Exploration** | Thorough @Explore | @Explore (Haiku) — Quick scan |
| **Planning** | Manual breakdown | @planner (Sonnet) — Rapid task generation |
| **Implementation** | Manual coding | @implementer (Sonnet) — Task-by-task execution |
| **Reviews** | Sequential | Parallel (all agents in single Task call) |
| **Breakpoints** | 3 (BP1, BP2, pre-commit) | 1 (pre-commit only) |
| **Suggestions** | Manual approval | Auto-accept if confidence > 0.7 |

### Turbo Agent Model Distribution

| Agent | Model | Role |
|-------|-------|------|
| @clarifier | **haiku** | Fast clarification questions |
| @planner | **sonnet** | Rapid task breakdown |
| @implementer | **sonnet** | Code implementation |
| @plan-validator | **opus** | Critical validation (unchanged) |
| @code-reviewer | **opus** | Quality validation (unchanged) |
| @security-auditor | **opus** | Security validation (unchanged) |
| @qa-reviewer | **sonnet** | Test review |
| @doc-generator | **sonnet** | Documentation |

### Auto-Activation

`--turbo` is **auto-suggested** (not auto-activated) when:

```
IF .project-memory/ exists AND category != LARGE:
   Display: "💡 --turbo recommandé (projet connu)"
   Include --turbo in FLAGS suggestion
```

**Why not auto-activated?** Turbo mode trades some depth for speed. User should opt-in.

### Command Compatibility

| Command | Turbo Effect |
|---------|--------------|
| `/brainstorm` | @clarifier (Haiku), max 3 iter, auto-accept EMS > 60 |
| `/brief` | @Explore (Haiku), 2 questions max, auto-suggest --turbo |
| `/epci` | @planner + @implementer, parallel reviews, 1 breakpoint |
| `/quick` | @implementer for SMALL, auto-commit, skip review |
| `/debug` | Haiku diagnostic, auto-apply best solution |

### Examples

```bash
# Explicit turbo mode
/epci --turbo

# Combined with other flags
/epci --turbo --safe           # Turbo with extra safety
/epci --turbo --persona-backend # Turbo with backend focus

# Not recommended
/epci --turbo --large          # Conflicting: large needs depth, turbo speeds
```

### Precedence

| Flag Combination | Result |
|------------------|--------|
| `--turbo` + `--large` | Warning: conflicting flags, `--large` takes precedence |
| `--turbo` + `--ultrathink` | `--ultrathink` overrides turbo thinking reduction |
| `--turbo` + `--safe` | Both active (safe + speed = quality-gated speed) |

---

## Persona Flags (F09)

Control global thinking modes that influence the entire workflow.

| Flag | Focus | Auto-Trigger |
|------|-------|--------------|
| `--persona-architect` | System thinking, patterns, scalability | architecture/design keywords |
| `--persona-frontend` | UI/UX, accessibility, Core Web Vitals | component/UI keywords |
| `--persona-backend` | APIs, data integrity, reliability | API/database keywords |
| `--persona-security` | Threat modeling, OWASP, compliance | auth/security keywords |
| `--persona-qa` | Tests, edge cases, coverage | test/quality keywords |
| `--persona-doc` | Documentation, clarity, examples | document/README keywords |

### Auto-Activation Scoring

```
Score = (keywords × 0.4) + (files × 0.4) + (stack × 0.2)

Thresholds:
- > 0.6  → Auto-activate
- 0.4-0.6 → Suggest to user
- < 0.4  → No activation
```

### Precedence

1. **Explicit persona** always wins over auto-activation
2. Only **one persona** can be active at a time
3. If multiple personas score > 0.6, highest score wins

### Examples

```bash
# Explicit persona for API development
/epci --persona-backend

# Combined with thinking flags
/epci --persona-security --think-hard

# Auto-activated based on brief content
/brief "Add user authentication endpoint"
# → --persona-backend auto-activated (score: 0.68)
```

### Display

```
FLAGS: --think-hard (auto) | --persona-backend (auto: 0.72)
```

→ See `src/skills/personas/SKILL.md` for full documentation.

---

## Wave Flags

Control multi-wave orchestration for large features.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--wave` | Enable wave-based execution | complexity score > 0.7 |
| `--wave-strategy progressive` | Iterative with validation between waves | Default with --wave |
| `--wave-strategy systematic` | Complete analysis then execution | Explicit only |

### Examples

```bash
# Enable wave orchestration
/epci --wave

# Systematic approach for complex migrations
/epci --wave --wave-strategy systematic
```

---

## Auto-Activation Rules

### Conditions

| Flag | Condition | Threshold |
|------|-----------|-----------|
| `--think` | Files impacted | 3-10 files |
| `--think-hard` | Files OR refactoring | >10 files OR migration detected |
| `--uc` | Context window usage | > 75% |
| `--safe` | Sensitive file patterns | Any match |
| `--wave` | Complexity score | > 0.7 |

### Algorithm

```
1. Evaluate context (files, patterns, complexity)
2. Check auto-activation conditions
3. Apply explicit flags (override auto)
4. Resolve conflicts using precedence rules
5. Display active flags
```

---

## Precedence Rules

### Priority Order

1. **Explicit flags** always override auto-activation
2. **Higher thinking wins**: `--ultrathink` > `--think-hard` > `--think`
3. **Explicit verbosity wins**: `--verbose` overrides auto `--uc`
4. **Implicit wave**: `--think-hard` + LARGE implies `--wave`

### Conflict Resolution

| Flag A | Flag B | Result |
|--------|--------|--------|
| `--uc` | `--verbose` | `--verbose` wins (if explicit) |
| `--think` | `--think-hard` | `--think-hard` wins |
| `--think-hard` | `--ultrathink` | `--ultrathink` wins |
| `--wave` | `--safe` | Both active (compatible) |
| `--no-hooks` | Any | Both active (always compatible) |

---

## Migration from `--large`

The `--large` flag is maintained for backward compatibility.

| Old | New Equivalent |
|-----|----------------|
| `--large` | `--think-hard --wave` |

When `--large` is used:
1. Internally mapped to `--think-hard --wave`
2. Deprecation notice displayed (optional)
3. Full backward compatibility maintained

---

## Flag Display

Active flags are displayed at the start of each command:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🚀 EPCI Workflow — feature-name                                     │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: --think-hard (auto) | --safe (auto) | --wave (explicit)     │
└─────────────────────────────────────────────────────────────────────┘
```

Legend:
- `(auto)` — Flag was auto-activated based on context
- `(explicit)` — Flag was explicitly specified by user
- No suffix — Default behavior

---

## MCP Flags (F12)

Control Model Context Protocol server activation.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--c7` | Enable Context7 (library docs) | persona architect/backend/doc, import keywords |
| `--seq` | Enable Sequential (multi-step reasoning) | `--think-hard`, persona architect/security |
| `--magic` | Enable Magic (UI generation) | persona frontend, *.jsx/*.tsx files |
| `--play` | Enable Playwright (E2E tests) | persona frontend/qa, *.spec.ts files |
| `--no-mcp` | Disable all MCP servers | Never |

### MCP Auto-Activation

MCPs are auto-activated based on:
1. **Persona activation**: Each persona has preferred MCPs (see matrix below)
2. **Keyword triggers**: Specific keywords in brief trigger MCPs
3. **File triggers**: File patterns trigger MCPs
4. **Flag triggers**: `--think-hard` triggers Sequential

### Persona × MCP Matrix

| Persona | Context7 | Sequential | Magic | Playwright |
|---------|:--------:|:----------:|:-----:|:----------:|
| architect | **auto** | **auto** | - | - |
| frontend | **auto** | - | **auto** | **auto** |
| backend | **auto** | **auto** | - | - |
| security | - | **auto** | - | - |
| qa | - | - | - | **auto** |
| doc | **auto** | - | - | - |

### MCP Precedence

1. **Explicit flags** (`--c7`, `--no-mcp`) always override auto-activation
2. **`--no-mcp`** disables all MCP servers
3. **Multiple MCPs** can be active simultaneously

### Examples

```bash
# Enable specific MCP
/epci --c7                 # Context7 only
/epci --seq --magic        # Sequential + Magic

# Disable all MCP
/epci --no-mcp

# Combined with persona (auto-activates preferred MCPs)
/epci --persona-frontend   # Auto: Magic + Playwright
```

→ See `src/skills/mcp/SKILL.md` for complete MCP documentation.

---

## Quick Workflow Flags (F13)

Control `/quick` command behavior for TINY and SMALL features.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--autonomous` | Skip plan breakpoint, continuous execution | TINY detected by `/brief` |
| `--quick-turbo` | Force Haiku model everywhere (TINY only) | Never (explicit only) |
| `--no-bp` | Alias for `--autonomous` | - |

### `--autonomous` Mode

When `--autonomous` is active:
- Skip the lightweight 3s breakpoint at Plan phase
- Execute all EPCT phases without interruption
- Session still persisted for tracking

**Auto-Activation:**
```
IF complexity == TINY:
   /brief routes to `/quick --autonomous`
   Display: "Mode TINY → exécution autonome"
```

### `--quick-turbo` Mode

Forces Haiku model on ALL phases (Explore, Plan, Code, Test).

**Constraints:**
- Only valid for TINY features
- If SMALL detected: Error + suggest removing flag
- Maximum speed, suitable for trivial changes

**Error on SMALL:**
```
⚠️ **FLAG INCOMPATIBLE**

--quick-turbo requires TINY complexity.
Detected: SMALL ({file_count} files, ~{loc} LOC)

Options:
1. Remove --quick-turbo and retry
2. Switch to /epci for larger features
```

### Flag Interactions

| Combination | Result |
|-------------|--------|
| `--autonomous` only | Skip plan BP, continue EPCT |
| `--quick-turbo` only | Haiku everywhere (TINY required) |
| `--autonomous --quick-turbo` | Both active (fastest possible) |
| `--turbo --autonomous` | `--turbo` precedence (legacy turbo mode) |
| `--safe --autonomous` | `--safe` wins (breakpoints maintained) |
| `--quick-turbo` + SMALL | Error, flag rejected |

### Examples

```bash
# Automatic for TINY (routed by /brief)
/quick --autonomous

# Maximum speed for trivial fix
/quick --autonomous --quick-turbo

# Explicit breakpoint for SMALL
/quick

# Combined with compression
/quick --autonomous --uc
```

---

## Quick Reference

### All Flags

| Category | Flags |
|----------|-------|
| Thinking | `--think`, `--think-hard`, `--ultrathink` |
| Compression | `--uc`, `--verbose` |
| **Reformulation** | **`--rephrase`**, **`--no-rephrase`** |
| Workflow | `--safe`, `--no-hooks` |
| **Speed** | **`--turbo`** |
| **Quick (F13)** | **`--autonomous`**, **`--quick-turbo`**, `--no-bp` |
| Persona | `--persona-architect`, `--persona-frontend`, `--persona-backend`, `--persona-security`, `--persona-qa`, `--persona-doc` |
| MCP | `--c7`, `--seq`, `--magic`, `--play`, `--no-mcp` |
| Wave | `--wave`, `--wave-strategy` |
| Legacy | `--large` (alias), `--continue` |

### Common Combinations

| Use Case | Flags |
|----------|-------|
| **Fast standard feature** | **`--turbo`** |
| **Fast with quality gate** | **`--turbo --safe`** |
| Large refactoring | `--think-hard --wave` or `--large` |
| Security feature | `--think-hard --safe --persona-security` |
| Major architecture | `--ultrathink --wave --persona-architect` |
| API development | `--think-hard --persona-backend` |
| Testing without hooks | `--no-hooks` |
| CI/CD pipeline | `--no-hooks --uc` |

---

*Document generated for EPCI v4.0.0*
