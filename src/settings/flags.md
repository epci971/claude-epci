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
/epci-brief "Add user authentication endpoint"
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

## Quick Reference

### All Flags

| Category | Flags |
|----------|-------|
| Thinking | `--think`, `--think-hard`, `--ultrathink` |
| Compression | `--uc`, `--verbose` |
| Workflow | `--safe`, `--no-hooks` |
| Persona | `--persona-architect`, `--persona-frontend`, `--persona-backend`, `--persona-security`, `--persona-qa`, `--persona-doc` |
| MCP | `--c7`, `--seq`, `--magic`, `--play`, `--no-mcp` |
| Wave | `--wave`, `--wave-strategy` |
| Legacy | `--large` (alias), `--continue` |

### Common Combinations

| Use Case | Flags |
|----------|-------|
| Large refactoring | `--think-hard --wave` or `--large` |
| Security feature | `--think-hard --safe --persona-security` |
| Major architecture | `--ultrathink --wave --persona-architect` |
| API development | `--think-hard --persona-backend` |
| Testing without hooks | `--no-hooks` |
| CI/CD pipeline | `--no-hooks --uc` |

---

*Document generated for EPCI v3.1*
