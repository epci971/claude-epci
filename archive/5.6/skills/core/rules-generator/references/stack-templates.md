# Stack Templates Index

## Overview

This document indexes all available rule templates organized by stack.
Templates are located in `skills/stack/{stack}/rules-templates/`.

---

## Template Registry

### Backend Stacks

| Stack | Template | Target Path | Description |
|-------|----------|-------------|-------------|
| `python-django` | `backend-django.md` | `rules/backend/django.md` | Django conventions, ORM, DRF |
| `python-django` | `testing-pytest.md` | `rules/testing/pytest.md` | pytest patterns, fixtures |
| `python-django` | `api-drf.md` | `rules/backend/api-drf.md` | Django REST Framework |
| `php-symfony` | `backend-symfony.md` | `rules/backend/symfony.md` | Symfony patterns, Doctrine |
| `php-symfony` | `testing-phpunit.md` | `rules/testing/phpunit.md` | PHPUnit testing |
| `php-symfony` | `security-symfony.md` | `rules/backend/security.md` | Voters, CSRF, auth |
| `java-springboot` | `backend-spring.md` | `rules/backend/spring.md` | Spring Boot patterns |
| `java-springboot` | `testing-junit.md` | `rules/testing/junit.md` | JUnit 5 testing |
| `java-springboot` | `security-spring.md` | `rules/backend/security.md` | Spring Security |

### Frontend Stacks

| Stack | Template | Target Path | Description |
|-------|----------|-------------|-------------|
| `javascript-react` | `frontend-react.md` | `rules/frontend/react.md` | React components, hooks |
| `javascript-react` | `state-management.md` | `rules/frontend/state.md` | Zustand, React Query |
| `javascript-react` | `testing-vitest.md` | `rules/testing/vitest.md` | Vitest, RTL |
| `frontend-editor` | `styling-tailwind.md` | `rules/frontend/tailwind.md` | Tailwind patterns |
| `frontend-editor` | `accessibility.md` | `rules/frontend/accessibility.md` | WCAG 2.1 AA |

### Global Templates

| Template | Target Path | Description |
|----------|-------------|-------------|
| `claude-md.md` | `.claude/CLAUDE.md` | Project overview template |
| `global-quality.md` | `rules/_global/quality.md` | Quality standards |
| `global-git-workflow.md` | `rules/_global/git-workflow.md` | Git conventions |
| `global-commands.md` | `rules/_global/commands.md` | Common commands |
| `domain-glossary.md` | `rules/domain/glossary.md` | Business terms |

---

## Template Selection Logic

```python
def select_templates(detection: dict) -> list[tuple[str, str]]:
    """
    Returns list of (template_path, target_path) tuples.
    """
    templates = []

    # Always include global templates
    templates.extend([
        ("templates/claude-md.md", ".claude/CLAUDE.md"),
        ("templates/global-quality.md", ".claude/rules/_global/quality.md"),
        ("templates/global-git-workflow.md", ".claude/rules/_global/git-workflow.md"),
    ])

    # Backend templates
    backend = detection.get("backend")
    if backend == "python-django":
        templates.extend([
            ("python-django/rules-templates/backend-django.md", ".claude/rules/backend/django.md"),
            ("python-django/rules-templates/testing-pytest.md", ".claude/rules/testing/pytest.md"),
            ("python-django/rules-templates/api-drf.md", ".claude/rules/backend/api-drf.md"),
        ])
    elif backend == "php-symfony":
        templates.extend([
            ("php-symfony/rules-templates/backend-symfony.md", ".claude/rules/backend/symfony.md"),
            ("php-symfony/rules-templates/testing-phpunit.md", ".claude/rules/testing/phpunit.md"),
            ("php-symfony/rules-templates/security-symfony.md", ".claude/rules/backend/security.md"),
        ])
    elif backend == "java-springboot":
        templates.extend([
            ("java-springboot/rules-templates/backend-spring.md", ".claude/rules/backend/spring.md"),
            ("java-springboot/rules-templates/testing-junit.md", ".claude/rules/testing/junit.md"),
            ("java-springboot/rules-templates/security-spring.md", ".claude/rules/backend/security.md"),
        ])

    # Frontend templates
    frontend = detection.get("frontend")
    if frontend == "javascript-react":
        templates.extend([
            ("javascript-react/rules-templates/frontend-react.md", ".claude/rules/frontend/react.md"),
            ("javascript-react/rules-templates/state-management.md", ".claude/rules/frontend/state.md"),
            ("javascript-react/rules-templates/testing-vitest.md", ".claude/rules/testing/vitest.md"),
        ])

    # Styling templates
    styling = detection.get("styling")
    if styling == "frontend-editor":
        templates.extend([
            ("frontend-editor/rules-templates/styling-tailwind.md", ".claude/rules/frontend/tailwind.md"),
            ("frontend-editor/rules-templates/accessibility.md", ".claude/rules/frontend/accessibility.md"),
        ])

    return templates
```

---

## Template Variables

Templates support variable substitution for project-specific values:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{project_name}}` | Project name | `my-awesome-app` |
| `{{backend_framework}}` | Backend framework | `Django 5.0` |
| `{{frontend_framework}}` | Frontend framework | `React 18` |
| `{{python_version}}` | Python version | `3.11` |
| `{{node_version}}` | Node version | `20.x` |
| `{{dev_command}}` | Dev server command | `python manage.py runserver` |
| `{{test_command}}` | Test command | `pytest` |
| `{{lint_command}}` | Lint command | `ruff check .` |

### Substitution Logic

```python
def substitute_variables(template: str, context: dict) -> str:
    """Replace template variables with actual values."""
    result = template
    for key, value in context.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result
```

---

## Multi-Stack Combinations

### Common Combinations

| Combination | Templates Generated |
|-------------|---------------------|
| Django + React + Tailwind | 9 files (3 backend + 3 frontend + 3 global) |
| Symfony + React + Tailwind | 9 files |
| Spring Boot + React + Tailwind | 9 files |
| Django only | 6 files (3 backend + 3 global) |
| React + Tailwind only | 7 files (3 frontend + 1 styling + 3 global) |

### Directory Structure Generated

```
.claude/
├── CLAUDE.md                    # From claude-md.md
└── rules/
    ├── _global/
    │   ├── quality.md           # From global-quality.md
    │   ├── git-workflow.md      # From global-git-workflow.md
    │   └── commands.md          # From global-commands.md
    ├── backend/
    │   ├── django.md            # From backend-django.md
    │   └── api-drf.md           # From api-drf.md
    ├── frontend/
    │   ├── react.md             # From frontend-react.md
    │   ├── state.md             # From state-management.md
    │   ├── tailwind.md          # From styling-tailwind.md
    │   └── accessibility.md     # From accessibility.md
    ├── testing/
    │   ├── pytest.md            # From testing-pytest.md
    │   └── vitest.md            # From testing-vitest.md
    └── domain/
        └── glossary.md          # From domain-glossary.md
```

---

## Adding New Templates

### 1. Create Template File

```bash
# Location: src/skills/stack/{stack}/rules-templates/{name}.md
touch src/skills/stack/python-fastapi/rules-templates/backend-fastapi.md
```

### 2. Follow Format

Use the format defined in `rules-format.md`:
- YAML frontmatter with `paths:`
- Sections: 🔴 CRITICAL, 🟡 CONVENTIONS, 🟢 PREFERENCES
- Quick Reference table
- Examples (Correct/Incorrect)

### 3. Register in This Index

Add entry to the appropriate section in this file.

### 4. Update Selection Logic

If new stack, update `select_templates()` function in the skill.
