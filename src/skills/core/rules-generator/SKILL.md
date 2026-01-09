---
name: rules-generator
description: >-
  Generates .claude/rules/ structure for projects. Performs 3-level detection
  (stack, architecture, conventions) and creates CLAUDE.md + rules files.
  Also supports incremental rule addition via auto-detection or --add flag.
  Use when: /epci:rules command invoked, project needs conventions setup,
  or user wants to add a single rule incrementally.
  Not for: Linter configuration, IDE settings.
---

# Rules Generator

## Overview

This skill generates a complete `.claude/rules/` structure for any project by:
1. Detecting stack and frameworks (Level 1)
2. Analyzing architecture patterns (Level 2)
3. Extracting naming conventions (Level 3)
4. Selecting and customizing templates

## Auto-detection

Triggered by:
- `/epci:rules init` command
- `/brief` auto-suggestion when `.claude/` absent

## Detection Process

### Level 1 — Stack Detection

Analyze configuration files to identify frameworks:

| File | Detects |
|------|---------|
| `composer.json` + symfony | `php-symfony` |
| `package.json` + react | `javascript-react` |
| `requirements.txt` + django | `python-django` |
| `pom.xml` + spring-boot | `java-springboot` |
| `tailwind.config.*` | `frontend-editor` |

```python
def detect_stack(root: Path) -> dict:
    stack = {}

    # Python/Django
    for req_file in ["requirements.txt", "pyproject.toml"]:
        if (root / req_file).exists():
            content = (root / req_file).read_text()
            if "django" in content.lower():
                stack["backend"] = "python-django"

    # PHP/Symfony
    if (root / "composer.json").exists():
        data = json.load(open(root / "composer.json"))
        if "symfony/framework-bundle" in str(data.get("require", {})):
            stack["backend"] = "php-symfony"

    # React
    if (root / "package.json").exists():
        data = json.load(open(root / "package.json"))
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "react" in deps:
            stack["frontend"] = "javascript-react"
        if "tailwindcss" in deps:
            stack["styling"] = "frontend-editor"

    # Java/Spring Boot
    for build_file in ["pom.xml", "build.gradle"]:
        if (root / build_file).exists():
            content = (root / build_file).read_text()
            if "spring-boot" in content.lower():
                stack["backend"] = "java-springboot"

    return stack
```

-> See `references/detection-levels.md` for complete logic

### Level 2 — Architecture Detection

Analyze directory structure:

| Pattern | Indicators |
|---------|------------|
| Monorepo | `backend/` + `frontend/` dirs |
| MVC | `controllers/`, `models/`, `views/` |
| DDD | `domain/`, `application/`, `infrastructure/` |
| Service Layer | `services/`, `handlers/` |

### Level 3 — Convention Detection

Analyze code for patterns:

| Aspect | Method |
|--------|--------|
| Naming | Regex on class/function names |
| Imports | Parse import statements |
| Typing | Detect type hints usage |
| Docstrings | Check format (Google, NumPy) |

---

## Generation Process

### Step 1: Create Directory Structure

```bash
mkdir -p .claude/rules/{_global,backend,frontend,testing,domain}
```

### Step 2: Generate CLAUDE.md

Use `templates/claude-md.md` with variable substitution:

| Variable | Source |
|----------|--------|
| `{{project_name}}` | Directory name or package.json |
| `{{backend_framework}}` | Level 1 detection |
| `{{frontend_framework}}` | Level 1 detection |
| `{{dev_command}}` | Detected from scripts |

### Step 3: Select Templates

Based on detection results:

```python
def select_templates(stack: dict) -> list[str]:
    templates = [
        "global-quality",
        "global-git-workflow",
        "global-commands"
    ]

    if stack.get("backend") == "python-django":
        templates.extend([
            "backend-django",
            "testing-pytest",
            "api-drf"
        ])
    elif stack.get("backend") == "php-symfony":
        templates.extend([
            "backend-symfony",
            "testing-phpunit",
            "security-symfony"
        ])
    # ... other stacks

    if stack.get("frontend") == "javascript-react":
        templates.extend([
            "frontend-react",
            "state-management",
            "testing-vitest"
        ])

    if stack.get("styling") == "frontend-editor":
        templates.extend([
            "styling-tailwind",
            "accessibility"
        ])

    return templates
```

-> See `references/stack-templates.md` for template index

### Step 4: Customize Templates

Apply project-specific values:

```python
def customize_template(template: str, context: dict) -> str:
    # Replace variables
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))

    # Adjust paths for monorepo
    if context.get("structure") == "monorepo":
        template = template.replace("src/**", "backend/**")

    return template
```

### Step 5: Validate Generated Files

Invoke `validate_rules.py`:

```bash
python src/scripts/validate_rules.py .claude/
```

---

## Output Structure

```
.claude/
├── CLAUDE.md                    # Project overview
└── rules/
    ├── _global/
    │   ├── quality.md           # Quality standards
    │   ├── git-workflow.md      # Git conventions
    │   └── commands.md          # Common commands
    ├── backend/
    │   ├── {framework}.md       # Backend rules
    │   └── api-{framework}.md   # API rules (if DRF/API Platform)
    ├── frontend/
    │   ├── react.md             # React patterns
    │   ├── state.md             # State management
    │   ├── tailwind.md          # Tailwind conventions
    │   └── accessibility.md     # WCAG rules
    ├── testing/
    │   ├── {test-framework}.md  # Testing patterns
    └── domain/
        └── glossary.md          # Business terms
```

---

## Actions

### `init`

Generate complete structure from scratch.

```
/epci:rules init [--force] [--dry-run]

--force    Overwrite existing files
--dry-run  Preview without creating files
```

**Process:**
1. Detect stack (Levels 1-3)
2. Show detection results
3. Confirm with user
4. Generate files
5. Validate
6. Report

### `add` (Incremental)

Add a single rule incrementally. Auto-detected or forced with `--add`.

```
/epci:rules "rule text"           # Auto-detected
/epci:rules --add "rule text"     # Explicit mode
```

**Process:**
1. Classify input (is it a rule?)
2. Assess clarity (scope, severity, wording)
3. Clarify if needed (@rule-clarifier)
4. Reformulate and confirm
5. Determine placement (CLAUDE.md or rules/*.md)
6. Integrate rule in correct section
7. Validate

**Auto-detection indicators:**
- Keywords: "toujours", "jamais", "doit", "préférer", "éviter"
- Structure: [contexte] + [action/contrainte]

-> See `references/rule-classifier.md` for classification logic

### `validate`

Check rules against codebase for drift.

```
/epci:rules validate [--fix]

--fix  Propose corrections for violations
```

**Checks:**
- Rules match actual code patterns
- No references to non-existent files
- Paths patterns are valid

### `update`

Detect new patterns and propose additions.

```
/epci:rules update
```

**Process:**
1. Analyze new code since last update
2. Detect new patterns
3. Propose rule additions
4. Apply with confirmation

---

## Integration Points

### With `/brief`

Auto-suggestion when `.claude/` absent:

```
⚠️ No .claude/rules/ found.
Run /epci:rules init to generate conventions.
```

### With `@rules-validator`

Agent validates generated structure:

```
Invoke @rules-validator with paths:
  - .claude/CLAUDE.md
  - .claude/rules/**/*.md
```

### With Hook

`post-rules-init` saves to project memory:

```python
{
    "timestamp": "2026-01-02T14:30:00Z",
    "stacks_detected": ["python-django", "javascript-react"],
    "files_created": [".claude/CLAUDE.md", "..."],
    "validation_verdict": "APPROVED"
}
```

---

## Quick Reference

| Task | Method |
|------|--------|
| Detect stack | Check config files (composer.json, package.json...) |
| Detect architecture | Analyze directory structure |
| Detect conventions | Parse code samples |
| Select templates | Based on detected stacks |
| Generate files | Apply templates with substitution |
| Validate | Run validate_rules.py |

## Error Handling

| Error | Recovery |
|-------|----------|
| Detection fails | Fallback to generic templates |
| Template missing | Skip with warning |
| Validation fails | Report issues, don't abort |
| File exists | Ask confirmation (unless --force) |

---

## References

- `references/detection-levels.md` — Detection algorithm details
- `references/rules-format.md` — File format specification
- `references/stack-templates.md` — Template index
- `references/rule-classifier.md` — Incremental add classification logic

---

*Rules Generator v1.1 — EPCI Plugin Integration*
