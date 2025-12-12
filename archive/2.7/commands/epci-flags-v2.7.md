# epci-flags — Universal Flags Reference (v2.7)

> **EPCI Enhancement** — Control behavior across all commands
>
> Flags are universal modifiers that change how EPCI commands behave.
> They provide safety controls, output formatting, and debugging capabilities.

---

## Critical Rules

- ⚠️ Flags are OPTIONAL — all commands work without flags
- ⚠️ Flags can be COMBINED (e.g., `--preview --uc`)
- ⚠️ Some flags are INCOMPATIBLE with certain commands (see matrix)
- ⚠️ `--persona-*` flags are documented separately in `epci-personas.md`

---

## 1. Overview

### 1.1 Flag Categories

| Category | Flags | Purpose |
|----------|-------|---------|
| **Safety** | `--preview`, `--safe-mode` | Prevent unintended changes |
| **Output** | `--uc`, `--verbose` | Control output verbosity |
| **Debug** | `--introspect` | Transparency into reasoning |
| **Quality** | `--validate` | Automatic verification |
| **Expertise** | `--persona-*` | Specialized expert mode |

### 1.2 Quick Reference

| Flag | Short | Description |
|------|-------|-------------|
| `--preview` | `-p` | Show what would happen without executing |
| `--safe-mode` | `-s` | Require confirmation before each file change |
| `--uc` | — | Ultra-compressed output (~70% smaller) |
| `--verbose` | `-v` | Detailed, expanded output |
| `--introspect` | `-i` | Show internal reasoning process |
| `--validate` | — | Run automatic verification after execution |
| `--persona-*` | — | Activate specialized persona (see epci-personas.md) |

---

## 2. Safety Flags

### 2.1 `--preview` (alias: `-p`)

**Purpose**: Show what would be done without actually doing it.

**Behavior**:
- Analyzes the task completely
- Lists all files that WOULD be modified/created/deleted
- Shows estimated LOC changes
- Does NOT write any files
- Does NOT execute any code

**Use Cases**:
- Review impact before committing to changes
- Estimate scope of a task
- Verify understanding before execution
- Safe exploration of "what if" scenarios

**Example**:

```bash
epci-2-code --preview
FEATURE_SLUG=user-authentication

# Output:
## Preview Mode — No Changes Made

### Files That Would Be Modified
| File | Action | Est. LOC |
|------|--------|----------|
| src/Security/Authenticator.php | modify | +45, -12 |
| src/Entity/User.php | modify | +8, -0 |
| config/security.yaml | modify | +15, -3 |

### Files That Would Be Created
| File | Est. LOC |
|------|----------|
| src/Security/JwtTokenManager.php | ~120 |
| tests/Security/AuthenticatorTest.php | ~80 |

### Summary
- Total files: 5
- Estimated changes: +268, -15 LOC
- Risk assessment: Medium

To execute these changes, run without --preview flag.
```

**Compatible Commands**: All except `epci-hotfix`, `epci-discover`

---

### 2.2 `--safe-mode` (alias: `-s`)

**Purpose**: Require explicit confirmation before each file modification.

**Behavior**:
- Pauses before EACH file write
- Shows exactly what will be written
- Waits for user confirmation (y/n)
- Allows skipping individual files
- Creates checkpoint after each confirmed change

**Use Cases**:
- Critical production code changes
- Learning/understanding what Claude does
- High-risk modifications
- Compliance requirements (audit trail)

**Example**:

```bash
epci-2-code --safe-mode
FEATURE_SLUG=payment-processing

# Output:
## Safe Mode Active — Confirmation Required

### File 1/4: src/Payment/PaymentProcessor.php

Action: MODIFY
Changes:
```diff
+ public function processRefund(Payment $payment): RefundResult
+ {
+     // ... 25 lines of new code
+ }
```

Confirm this change? [y/n/skip/abort]: y
✅ File modified.

### File 2/4: src/Entity/Payment.php
...
```

**Confirmation Options**:
- `y` / `yes` — Apply this change
- `n` / `no` — Skip this file, continue to next
- `skip` — Skip this file, continue to next
- `abort` — Stop completely, rollback all changes in this session

**Compatible Commands**: `epci-2-code`, `epci-3-finalize`, `epci-soft`, `epci-micro`

---

## 3. Output Flags

### 3.1 `--uc` (Ultra-Compressed)

**Purpose**: Reduce output verbosity by ~70% while preserving essential information.

**Behavior**:
- Removes explanatory prose
- Uses abbreviations and compact formats
- Preserves all critical information
- Ideal for experienced users
- Saves context window space

**Use Cases**:
- Long conversations approaching context limits
- Experienced users who don't need explanations
- Scripted/automated workflows
- Quick iterations

**Example**:

**Standard Output:**
```markdown
## 2. Explore — Context & Impact

### 2.1 Modules & components involved

After analyzing the codebase, I've identified the following key modules 
and components that will be involved in this feature implementation:

- `src/Domain/Booking/BookingValidator.php` — This is the main validation 
  service that handles all booking-related validations. We'll need to add 
  our new validation logic here.
- `src/Application/Booking/BookingService.php` — The application service 
  that orchestrates booking operations. This will need to call our new 
  validation method.
- `templates/booking/form.html.twig` — The frontend template that displays 
  validation errors to users.

### 2.2 Existing behaviour (before)

Currently, the system does not impose any limit on booking duration...
[... 500 more words ...]
```

**With `--uc`:**
```markdown
## Explore

**Files:** BookingValidator.php (modify), BookingService.php (modify), form.html.twig (modify)

**Current:** No stay limit. **Target:** Max 30 days, error msg on violation.

**Risks:** Edge case 30 days (accept), premium rentals (exclude)
```

**Compression Techniques**:
- Tables instead of prose
- Bullet points instead of paragraphs
- Abbreviations (Est., Config., Impl.)
- No introductory phrases
- Direct statements only

**Compatible Commands**: All commands

---

### 3.2 `--verbose` (alias: `-v`)

**Purpose**: Expanded, detailed output with extra explanations.

**Behavior**:
- Includes reasoning for decisions
- Adds context and background
- Shows alternative approaches considered
- Includes more examples
- Better for learning/documentation

**Use Cases**:
- New team members learning the codebase
- Documentation purposes
- Complex decisions needing justification
- Training/educational contexts

**Example**:

```bash
epci-1-analyse --verbose
FEATURE_SLUG=cache-invalidation

# Output includes additional sections:

### Why This Approach?

I considered three approaches for cache invalidation:

1. **Time-based TTL** — Simple but may serve stale data
2. **Event-based invalidation** — Complex but precise
3. **Hybrid approach** — Balance of both

I recommend option 3 because:
- Your data changes infrequently (TTL works for most cases)
- But financial data needs immediate consistency (events for critical paths)
- This matches the pattern used in your OrderService (see line 145)

### Alternative Approaches Rejected

| Approach | Reason for Rejection |
|----------|---------------------|
| Redis pub/sub | Infrastructure overhead not justified |
| Database triggers | Tight coupling, harder to test |
```

**Compatible Commands**: All commands

**Note**: `--verbose` and `--uc` are mutually exclusive. If both specified, `--uc` takes precedence.

---

## 4. Debug Flags

### 4.1 `--introspect` (alias: `-i`)

**Purpose**: Show internal reasoning and decision-making process.

**Behavior**:
- Displays decision logic with emoji markers
- Shows what triggers were detected
- Explains routing decisions
- Reveals confidence levels
- Shows alternatives considered

**Use Cases**:
- Understanding why Claude made certain choices
- Debugging unexpected behavior
- Learning how EPCI routing works
- Validating Claude's understanding

**Output Markers**:

| Marker | Meaning |
|--------|---------|
| 🎯 | Decision made |
| 🔍 | Analysis performed |
| 🔄 | Alternative considered |
| 📊 | Metric/score calculated |
| ⚠️ | Warning/concern noted |
| 💡 | Insight/recommendation |
| ✅ | Validation passed |
| ❌ | Validation failed |

**Example**:

```bash
epci-0-briefing --introspect
$ARGUMENTS=<brief about user authentication>

# Output includes introspection block:

---
### 🔍 Introspection

🔍 **Keyword Analysis**
   Detected: "authentication" (security), "JWT" (security), "login" (security)
   Security score: 0.85

🎯 **Persona Decision**
   Auto-activating: `--persona-security`
   Reason: 3+ security keywords detected

📊 **Complexity Assessment**
   - Files estimate: 5-8 (STANDARD range)
   - LOC estimate: 300-500 (STANDARD range)
   - Risk factors: auth = high sensitivity
   - Final: STANDARD (confidence: 82%)

🔄 **Routing Alternatives Considered**
   - epci-soft: Rejected (> 3 files expected)
   - epci-micro: Rejected (new business logic)
   - epci-1-analyse: ✅ Selected

💡 **Recommendations**
   - Consider `--persona-security` for EPCI-2
   - Suggest security review before merge
---
```

**Compatible Commands**: `epci-0-briefing`, `epci-1-analyse`, `epci-2-code`, `epci-3-finalize`, `epci-soft`, `epci-spike`

---

## 5. Quality Flags

### 5.1 `--validate`

**Purpose**: Run automatic verification checks after execution.

**Behavior**:
- Runs after main command completes
- Executes relevant validation checks
- Reports pass/fail status
- Suggests fixes for failures
- Does not block (informational)

**Validation Checks by Command**:

| Command | Validations Run |
|---------|-----------------|
| `epci-2-code` | Syntax check, test run, lint |
| `epci-3-finalize` | Plan vs implementation audit, doc completeness |
| `epci-soft` | Syntax check, basic tests |
| `epci-micro` | Syntax check |
| `epci-hotfix` | Syntax check, smoke test |

**Example**:

```bash
epci-2-code --validate
FEATURE_SLUG=order-processing

# After implementation, runs validation:

---
## Validation Results

### Syntax Check
✅ All files pass syntax validation

### Test Execution
```bash
php bin/phpunit tests/Unit/Order/
```
✅ 12 tests, 24 assertions, 0 failures

### Lint Check
⚠️ 2 warnings found:
- src/Order/OrderProcessor.php:45 — Line exceeds 120 characters
- src/Order/OrderProcessor.php:89 — Missing docblock

### Overall: ✅ PASS (with warnings)

Suggestions:
- Consider fixing lint warnings before commit
- Run full test suite: `php bin/phpunit`
---
```

**Compatible Commands**: `epci-2-code`, `epci-3-finalize`, `epci-soft`, `epci-micro`, `epci-hotfix`

---

## 6. Combining Flags

### 6.1 Valid Combinations

Flags can be combined for enhanced behavior:

```bash
# Preview with compressed output
epci-2-code --preview --uc

# Safe mode with validation
epci-2-code --safe-mode --validate

# Introspection with verbose output
epci-1-analyse --introspect --verbose

# Full safety stack
epci-2-code --preview --safe-mode --validate
```

### 6.2 Combination Effects

| Combination | Effect |
|-------------|--------|
| `--preview --uc` | Compact preview summary |
| `--preview --verbose` | Detailed impact analysis |
| `--safe-mode --validate` | Confirm each change, then validate all |
| `--introspect --uc` | Compact reasoning display |
| `--preview --safe-mode` | Preview only (safe-mode ignored in preview) |

### 6.3 Invalid/Ignored Combinations

| Combination | Behavior |
|-------------|----------|
| `--uc --verbose` | `--uc` wins (mutually exclusive) |
| `--preview --safe-mode` | `--safe-mode` ignored (nothing to confirm in preview) |

---

## 7. Compatibility Matrix

### 7.1 Full Matrix

| Flag | epci-0 | epci-1 | epci-2 | epci-3 | soft | micro | hotfix | spike | discover |
|------|--------|--------|--------|--------|------|-------|--------|-------|----------|
| `--preview` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `--safe-mode` | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| `--uc` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--verbose` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| `--introspect` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| `--validate` | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `--persona-*` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

### 7.2 Why Some Flags Are Incompatible

| Flag | Incompatible With | Reason |
|------|-------------------|--------|
| `--preview` | `epci-hotfix` | Emergency mode needs immediate action |
| `--preview` | `epci-discover` | Discovery is already non-destructive |
| `--safe-mode` | `epci-0`, `epci-1` | No file modifications to confirm |
| `--safe-mode` | `epci-hotfix` | Emergency mode needs speed |
| `--introspect` | `epci-micro` | Too lightweight for introspection overhead |
| `--introspect` | `epci-hotfix` | Emergency mode focuses on fix, not reasoning |
| `--verbose` | `epci-hotfix` | Emergency mode needs brevity |
| `--validate` | `epci-0`, `epci-1` | No code to validate |
| `--validate` | `epci-spike` | Spike code is throwaway |
| `--persona-*` | `epci-micro` | Too lightweight for personas |
| `--persona-*` | `epci-hotfix` | Emergency needs focus, not perspectives |

---

## 8. Default Behaviors

### 8.1 When No Flags Specified

| Aspect | Default |
|--------|---------|
| Preview | OFF — Changes are applied |
| Safe mode | OFF — No confirmation prompts |
| Output | Standard verbosity |
| Introspection | OFF — Reasoning hidden |
| Validation | OFF — No auto-validation |
| Persona | None or auto-detected |

### 8.2 Recommended Defaults by Context

| Context | Recommended Flags |
|---------|-------------------|
| **Learning EPCI** | `--verbose --introspect` |
| **Production code** | `--safe-mode --validate` |
| **Quick iteration** | `--uc` |
| **Impact assessment** | `--preview` |
| **Debugging issues** | `--introspect --verbose` |
| **Long conversations** | `--uc` |

---

## 9. Usage Examples

### 9.1 Cautious Workflow

```bash
# Step 1: Preview what would happen
epci-1-analyse --preview
FEATURE_SLUG=payment-refund

# Step 2: Execute with full analysis
epci-1-analyse --verbose
FEATURE_SLUG=payment-refund

# Step 3: Implement with safety
epci-2-code --safe-mode --validate
FEATURE_SLUG=payment-refund

# Step 4: Finalize with validation
epci-3-finalize --validate
FEATURE_SLUG=payment-refund
```

### 9.2 Fast Iteration Workflow

```bash
# Compressed output throughout
epci-0-briefing --uc
$ARGUMENTS=<brief>

epci-soft --uc
FEATURE_SLUG=quick-fix
```

### 9.3 Learning/Documentation Workflow

```bash
# Maximum detail and transparency
epci-1-analyse --verbose --introspect
FEATURE_SLUG=complex-feature
```

### 9.4 Security-Critical Workflow

```bash
# Full safety + security persona
epci-1-analyse --persona-security --verbose
FEATURE_SLUG=auth-upgrade

epci-2-code --safe-mode --validate --persona-security
FEATURE_SLUG=auth-upgrade
```

---

## 10. Flag Syntax

### 10.1 Long Form (Recommended)

```bash
epci-2-code --preview --safe-mode --validate
```

### 10.2 Short Form (Where Available)

```bash
epci-2-code -p -s     # --preview --safe-mode
epci-1-analyse -v -i  # --verbose --introspect
```

### 10.3 Placement

Flags can appear:
- After command name: `epci-2-code --preview`
- Before arguments: `epci-2-code --preview FEATURE_SLUG=...`
- Mixed with arguments: `epci-2-code FEATURE_SLUG=... --preview`

All placements are equivalent.

---

## 11. Summary

EPCI Flags provide:

1. **Safety controls** — `--preview` and `--safe-mode` prevent accidents
2. **Output control** — `--uc` and `--verbose` for different verbosity needs
3. **Debugging** — `--introspect` reveals internal reasoning
4. **Quality assurance** — `--validate` runs automatic checks
5. **Flexibility** — Combine flags for customized behavior

Use flags to adapt EPCI commands to your specific needs and risk tolerance.

---

## 12. Related Documentation

- **Personas**: See `epci-personas.md` for `--persona-*` flags
- **Workflow Guide**: See `epci-workflow-guide.md` for overall workflow
- **Individual Commands**: Each command file documents its specific flag support

---

*This document is part of the EPCI v2.7 workflow system.*
