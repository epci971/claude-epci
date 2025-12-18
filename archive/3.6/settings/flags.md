# EPCI Flags Reference

> **Version**: 3.1.0
> **Date**: 2025-12-16

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

Control execution safety and speed.

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--safe` | Maximum validations, extra confirmations | Sensitive files detected |
| `--fast` | Skip optional validations | Never |
| `--dry-run` | Simulation only, no modifications | Never |

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

# Fast iteration in development
/epci-quick --fast

# Preview what would happen
/epci --dry-run
```

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
2. **Safety over speed**: `--safe` > `--fast`
3. **Higher thinking wins**: `--ultrathink` > `--think-hard` > `--think`
4. **Explicit verbosity wins**: `--verbose` overrides auto `--uc`
5. **Implicit wave**: `--think-hard` + LARGE implies `--wave`

### Conflict Resolution

| Flag A | Flag B | Result |
|--------|--------|--------|
| `--safe` | `--fast` | **Error** (incompatible) |
| `--uc` | `--verbose` | `--verbose` wins (if explicit) |
| `--think` | `--think-hard` | `--think-hard` wins |
| `--think-hard` | `--ultrathink` | `--ultrathink` wins |
| `--wave` | `--safe` | Both active (compatible) |
| `--dry-run` | Any | Both active (always compatible) |

### Error Messages

```
ERROR: Flags --safe and --fast are incompatible.
       --safe enforces all validations
       --fast skips optional validations

       Choose one or omit both for default behavior.
```

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

## Quick Reference

### All Flags

| Category | Flags |
|----------|-------|
| Thinking | `--think`, `--think-hard`, `--ultrathink` |
| Compression | `--uc`, `--verbose` |
| Workflow | `--safe`, `--fast`, `--dry-run` |
| Wave | `--wave`, `--wave-strategy` |
| Legacy | `--large` (alias), `--continue` |

### Common Combinations

| Use Case | Flags |
|----------|-------|
| Large refactoring | `--think-hard --wave` or `--large` |
| Security feature | `--think-hard --safe` |
| Quick fix in dev | `--fast` |
| Major architecture | `--ultrathink --wave --safe` |
| Preview changes | `--dry-run` |

---

*Document generated for EPCI v3.1*
