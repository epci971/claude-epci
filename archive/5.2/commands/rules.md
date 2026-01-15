---
description: >-
  Generate .claude/rules/ structure for a project. Performs 3-level detection
  (stack, architecture, conventions), generates CLAUDE.md and contextual rules,
  then validates via @rules-validator. Also supports incremental rule addition
  via auto-detection or --add flag.
argument-hint: "[--force] [--validate-only] [--dry-run] [--stack <name>] [--add] [\"rule text\"]"
allowed-tools: [Read, Write, Glob, Grep, Bash, Task]
---

# EPCI Rules — Rules Generator

## Overview

This command generates the `.claude/rules/` structure for a project.
It detects the technology stack, analyzes architecture, and creates
contextual rules files tailored to the project.

## Configuration

| Element       | Value                                                    |
| ------------- | -------------------------------------------------------- |
| **Thinking**  | `think` (default) / `think hard` (complex monorepo)      |
| **Skills**    | rules-generator, project-memory, [stack-skill detected]  |
| **Subagents** | @Explore (quick), @rules-validator, @rule-clarifier      |

## Arguments

| Argument          | Description                                      |
| ----------------- | ------------------------------------------------ |
| `--force`         | Overwrite existing `.claude/` directory          |
| `--validate-only` | Only validate existing rules, no generation      |
| `--dry-run`       | Show what would be generated without writing     |
| `--stack <name>`  | Force stack detection (django, symfony, react, springboot, frontend-editor) |
| `--no-validate`   | Skip validation step after generation            |
| `--add`           | Force incremental rule addition mode (auto-detected otherwise) |

## Process

### Step 0: Input Classification & Routing

**Reference**: `rules-generator/references/rule-classifier.md`

1. **Parse input and flags**
   - If `--add` flag present → **Mode ADD** (see `references/rules-add-mode.md`)
   - If explicit flags (`--force`, `--validate-only`, `--dry-run`, `--stack`) → **Mode GENERATE** (Step 1)
   - Else → Classify input text

2. **Auto-detect rule input** (if no explicit flags)

   Score the input for rule indicators:

   | Indicator | Score |
   |-----------|-------|
   | "always", "never", "must", "do not" | +0.2 each |
   | "should", "prefer", "avoid", "convention" | +0.2 each |
   | Structure [context] + [action] | +0.2 |
   | "?" at end (question) | -0.3 |

   **Routing**:
   - Score >= 0.7 → **Mode ADD** (see `references/rules-add-mode.md`)
   - Score 0.4-0.7 → Ask for confirmation
   - Score < 0.4 → **Mode GENERATE** (Step 1)

3. **Pre-checks (Mode GENERATE only)**
   - If `.claude/` exists and `--force` not provided:
     ```
     .claude/ already exists. Use --force to overwrite.
     ```
   - If `--validate-only`: Skip to Step 4 (Validation)

4. **Load project memory** (if `.project-memory/` exists)
   - Extract project name, conventions, patterns

---

### Mode ADD: Incremental Rule Addition

**Full details:** See `references/rules-add-mode.md`

Quick summary of steps:
- **A1**: Clarity assessment (score)
- **A2**: Clarification via @rule-clarifier (if needed)
- **A3**: Reformulation & user validation
- **A4**: Placement decision (CLAUDE.md vs rules/*.md)
- **A5**: Integration
- **A6**: Validation & completion

---

### Step 1: Stack Detection (3 Levels)

**Skill**: `rules-generator`

#### Level 1 — Technology Stack

Detect primary stack by analyzing project files:

| Stack         | Detection Pattern                                       |
| ------------- | ------------------------------------------------------- |
| Python/Django | `requirements.txt` OR `pyproject.toml` + django         |
| PHP/Symfony   | `composer.json` + symfony/*                             |
| JS/React      | `package.json` + react                                  |
| Java/Spring   | `pom.xml` OR `build.gradle` + spring-boot               |
| Frontend      | `tailwind.config.*` OR postcss + tailwind               |

**Monorepo detection:**
```
IF backend/ AND frontend/:
   → Detect both stacks
   → Generate combined rules
```

#### Level 2 — Architecture

Analyze project structure:

| Pattern       | Detection                              | Impact           |
| ------------- | -------------------------------------- | ---------------- |
| Clean Arch    | `domain/`, `application/`, `infra/`    | Layer rules      |
| Hexagonal     | `ports/`, `adapters/`                  | Port/adapter rules |
| MVC           | `controllers/`, `views/`, `models/`    | MVC rules        |
| DDD           | `aggregates/`, `valueobjects/`         | DDD rules        |
| Modular       | Multiple independent modules           | Module boundaries |

#### Level 3 — Conventions (AST)

For each detected stack, run AST analysis:

**Python:**
```bash
# Detect naming conventions, decorators, type hints
grep -r "def [a-z_]*(" backend/ | head -20
grep -r "@dataclass\|@validator" backend/ | head -10
```

**TypeScript/React:**
```bash
# Detect component patterns, hooks usage
grep -r "export (default |const )" frontend/src/ | head -20
grep -r "use[A-Z][a-zA-Z]*" frontend/src/ | head -10
```

---

### Step 2: Template Selection

Based on detection, select templates from skill stack folders:

| Detection                | Templates to Use                                            |
| ------------------------ | ----------------------------------------------------------- |
| Django                   | `python-django/rules-templates/backend-django.md`, etc.     |
| Symfony                  | `php-symfony/rules-templates/backend-symfony.md`, etc.      |
| React                    | `javascript-react/rules-templates/frontend-react.md`, etc.  |
| SpringBoot               | `java-springboot/rules-templates/backend-spring.md`, etc.   |
| Frontend (Tailwind)      | `frontend-editor/rules-templates/styling-tailwind.md`, etc. |
| Monorepo (Django+React)  | Django templates + React templates + Frontend templates     |

**Template paths:**
```
src/skills/stack/<stack>/rules-templates/
src/skills/core/rules-generator/templates/  (global templates)
```

---

### Step 3: Generation

Generate `.claude/` structure:

#### 3.1 Create Directory Structure

```bash
mkdir -p .claude/rules
```

#### 3.2 Generate CLAUDE.md

Use template from `src/skills/core/rules-generator/templates/claude-md.md`

**Variables to substitute:**
- `{{project_name}}` → From `.project-memory/context.json` or directory name
- `{{stack}}` → Detected stack(s)
- `{{architecture}}` → Detected patterns
- `{{generated_date}}` → Current date

**Content focus (>50 lines):**
- Project overview
- Architecture decisions
- Development workflow
- Key commands
- Testing strategy
- Deployment notes

#### 3.3 Generate Rules Files

For each selected template:

1. **Read template** from skill folder
2. **Adapt paths** for project structure
3. **Substitute variables** (project name, date, stack)
4. **Write to `.claude/rules/`**

**File naming:**
```
Template: backend-django.md → Output: .claude/rules/backend-django.md
Template: testing-pytest.md → Output: .claude/rules/testing-pytest.md
```

#### 3.4 Generate Global Rules

From `src/skills/core/rules-generator/templates/`:
- `global-quality.md` → `.claude/rules/global-quality.md`
- `global-git-workflow.md` → `.claude/rules/global-git-workflow.md`
- `domain-glossary.md` → `.claude/rules/domain-glossary.md` (if domain terms detected)

---

### Step 4: Validation

**Subagent**: `@rules-validator`

Invoke @rules-validator to validate generated structure:

```
Task: Validate .claude/rules/ structure
Input: Path to .claude/ directory
Expected: VALID | VALID_WITH_WARNINGS | INVALID
```

**If INVALID:**
- Display issues
- Suggest fixes
- Option to regenerate

**If VALID_WITH_WARNINGS:**
- Display warnings
- Continue with completion

---

### Step 5: Completion

Display summary:

```
+---------------------------------------------------------------------+
| RULES GENERATED                                                      |
+---------------------------------------------------------------------+
|                                                                     |
| STRUCTURE CREATED                                                   |
| ├── .claude/CLAUDE.md (850 tokens)                                  |
| └── .claude/rules/                                                  |
|     ├── backend-django.md (1200 tokens)                             |
|     ├── testing-pytest.md (980 tokens)                              |
|     ├── api-drf.md (750 tokens)                                     |
|     ├── global-quality.md (600 tokens)                              |
|     └── global-git-workflow.md (450 tokens)                         |
|                                                                     |
| DETECTION                                                           |
| ├── Stack: Python/Django + JavaScript/React                         |
| ├── Architecture: Clean Architecture                                |
| └── Conventions: snake_case, type hints, functional components      |
|                                                                     |
| VALIDATION: VALID                                                   |
|                                                                     |
| Rules will be auto-activated based on edited files                  |
|                                                                     |
+---------------------------------------------------------------------+
```

---

## Integration with Brief

When `/brief` is called on a project without `.claude/`:

1. **Suggest rules generation:**
   ```
   No project rules detected. Would you like to generate .claude/rules/?
      → Run /rules to create project conventions
   ```

2. **Auto-suggest after Feature completion:**
   - After `/epci` Phase 3, if no `.claude/` exists, suggest `/rules`

---

## Hook Integration

**Post-rules-init hook** (`hooks/active/post-rules-init.py`):
- Log rules generation
- Update `.project-memory/settings.json` with `rules_initialized: true`
- Optional: Notify team (webhook)

---

## Examples

### Basic Usage (Mode GENERATE)

```bash
# Detect stack and generate rules
/epci:rules

# Force regeneration
/epci:rules --force

# Validate existing rules only
/epci:rules --validate-only

# Preview without writing
/epci:rules --dry-run
```

### Incremental Addition (Mode ADD)

```bash
# Auto-detected as rule (high confidence)
/epci:rules "Always use type hints in Python code"
→ Direct reformulation, validation, addition

# Auto-detected as rule (needs clarification)
/epci:rules "Be careful with SQL injections"
→ @rule-clarifier asks: scope? severity?

# Force add mode explicitly
/epci:rules --add "Prefer functional components in React"

# Clear rule with explicit scope
/epci:rules "Files in backend/ must have docstrings"
→ Scope: backend/**/*.py, Severity: CRITICAL (must)
```

### Force Specific Stack

```bash
# Force Django detection (when auto-detection fails)
/epci:rules --stack django

# Force multiple stacks for monorepo
/epci:rules --stack django --stack react
```

---

## Error Handling

| Error                        | Message                                      | Solution                  |
| ---------------------------- | -------------------------------------------- | ------------------------- |
| No stack detected            | "No recognized stack"                        | Use `--stack` flag        |
| .claude/ exists              | ".claude/ already exists"                    | Use `--force`             |
| Template not found           | "Missing template: {name}"                   | Check skill installation  |
| Validation failed            | "Invalid rules"                              | Fix issues, regenerate    |
| Permission denied            | "Cannot create .claude/"                     | Check directory perms     |

---

## Validation Script Integration

Use the validation script for CI/CD:

```bash
# Validate rules after generation
python3 src/scripts/validate_rules.py .claude/rules/ --verbose

# Expected output:
# [OK] CLAUDE.md: Valid structure
# [OK] rules/backend-django.md: Valid frontmatter, 1200 tokens
# [OK] rules/testing-pytest.md: Valid frontmatter, 980 tokens
# VALIDATION REPORT: PASSED (5/5 files valid)
```
