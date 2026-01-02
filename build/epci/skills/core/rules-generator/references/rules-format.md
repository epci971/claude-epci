# Rules File Format Reference

## Overview

Rules files follow a specific format with YAML frontmatter and structured markdown content.
This ensures consistent parsing and auto-activation based on file paths.

---

## File Structure

```markdown
---
paths:
  - pattern/to/match/**/*.ext
  - "!pattern/to/exclude/**"
---

# Rule Title

> Brief description of the rule scope

## 🔴 CRITICAL (Ne jamais violer)

1. **Rule name**: Explanation
2. **Another rule**: Explanation

## 🟡 CONVENTIONS (Standard du projet)

- Convention 1: detail
- Convention 2: detail

## 🟢 PREFERENCES (Quand applicable)

- Preference 1
- Preference 2

## Quick Reference

| Task | Pattern |
|------|---------|
| Task 1 | Solution |
| Task 2 | Solution |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Pattern 1 | How to implement | Why use it |

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Bad practice | Why it's bad | What to do instead |

## Examples

### Correct

```{lang}
// Good code example
```

### Incorrect

```{lang}
// Bad code example - avoid this
```
```

---

## YAML Frontmatter

### Required Fields

#### `paths`

List of glob patterns for auto-activation.

```yaml
paths:
  - src/**/*.py           # Include all Python files in src/
  - "!src/**/migrations/**" # Exclude migrations
  - backend/**/*.php      # Include PHP files in backend/
```

**Pattern Syntax:**
- `*` — Match any characters except `/`
- `**` — Match any characters including `/`
- `!` — Exclude pattern (must be quoted: `"!pattern"`)
- `{}` — Alternatives: `*.{ts,tsx}`

### Optional Fields

#### `tags`

Categorization for filtering.

```yaml
tags: [architecture, security, performance]
```

#### `priority`

Order when multiple rules match.

```yaml
priority: 1  # Lower = higher priority
```

#### `applies_to`

Specific sub-frameworks.

```yaml
applies_to: [django, drf, celery]
```

---

## Markdown Sections

### Section Hierarchy

| Level | Section | Purpose |
|-------|---------|---------|
| 🔴 | CRITICAL | Rules that must never be violated |
| 🟡 | CONVENTIONS | Standard practices for the project |
| 🟢 | PREFERENCES | Optional but recommended |

### Required Sections

1. **Title** (`# Rule Title`)
2. **At least one level** (🔴, 🟡, or 🟢)

### Recommended Sections

- **Quick Reference** — Cheatsheet table
- **Common Patterns** — Frequent use cases
- **Anti-patterns** — What to avoid
- **Examples** — Code samples (Correct/Incorrect)

---

## Path Patterns by Stack

### Python Django

```yaml
paths:
  - backend/**/*.py
  - "!backend/**/migrations/**"
  - "!backend/**/tests/**"
```

### PHP Symfony

```yaml
paths:
  - backend/**/*.php
  - config/**/*.yaml
  - "!backend/var/**"
  - "!backend/vendor/**"
```

### JavaScript React

```yaml
paths:
  - frontend/**/*.tsx
  - frontend/**/*.ts
  - "!frontend/**/*.test.ts"
  - "!frontend/**/*.test.tsx"
  - "!frontend/node_modules/**"
```

### Java Spring Boot

```yaml
paths:
  - backend/**/*.java
  - "!backend/**/test/**"
```

### Frontend Editor (Tailwind)

```yaml
paths:
  - frontend/**/*.css
  - frontend/**/*.scss
  - "**/tailwind.config.*"
  - "!frontend/node_modules/**"
```

---

## Validation Rules

### Frontmatter Validation

```python
def validate_frontmatter(content: str) -> tuple[bool, list[str]]:
    errors = []

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        errors.append("Missing YAML frontmatter")
        return False, errors

    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return False, errors

    # Required fields
    if "paths" not in data:
        errors.append("Missing required field: paths")
    elif not isinstance(data["paths"], list):
        errors.append("paths must be a list")

    return len(errors) == 0, errors
```

### Content Validation

```python
def validate_content(content: str) -> tuple[bool, list[str]]:
    errors = []
    warnings = []

    # Must have title
    if not re.search(r'^# .+', content, re.MULTILINE):
        errors.append("Missing title (# heading)")

    # Must have at least one level
    levels = ["🔴", "🟡", "🟢"]
    if not any(level in content for level in levels):
        errors.append("Must have at least one section (🔴, 🟡, or 🟢)")

    # Warnings for missing recommended sections
    if "Quick Reference" not in content:
        warnings.append("Missing recommended section: Quick Reference")
    if "Anti-pattern" not in content:
        warnings.append("Missing recommended section: Anti-patterns")

    return len(errors) == 0, errors + warnings
```

---

## Examples

### Minimal Valid Rule

```markdown
---
paths:
  - src/**/*.py
---

# Python Conventions

## 🟡 CONVENTIONS

- Use snake_case for functions
- Use PascalCase for classes
```

### Complete Rule

```markdown
---
paths:
  - backend/**/*.py
  - "!backend/**/migrations/**"
tags: [backend, django, architecture]
priority: 1
applies_to: [django, drf]
---

# Django Backend Rules

> Conventions for Python/Django development in this project.

## 🔴 CRITICAL

1. **No logic in views**: Views delegate to services
2. **No N+1 queries**: Always use select_related/prefetch_related

## 🟡 CONVENTIONS

- Services in `services/` directory
- One model per file in `models/`
- Serializers mirror model structure

## 🟢 PREFERENCES

- Prefer class-based views for CRUD
- Use `@transaction.atomic` for multi-model operations

## Quick Reference

| Task | Pattern |
|------|---------|
| Business logic | `services/usecases/` |
| FK access | `select_related()` |
| M2M access | `prefetch_related()` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Service Layer | `services/domain.py` | Testable, reusable |
| Repository | Custom QuerySet | Encapsulated queries |

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Fat models | Hard to test | Domain services |
| Logic in views | SRP violation | Service layer |

## Examples

### Correct

```python
# services/usecases/create_user.py
@transaction.atomic
def create_user(email: str, name: str) -> User:
    user = User.objects.create(email=email, name=name)
    send_welcome_email.delay(user.id)
    return user
```

### Incorrect

```python
# views.py - DON'T DO THIS
class UserViewSet(ViewSet):
    def create(self, request):
        # Business logic in view - BAD
        user = User.objects.create(**request.data)
        send_mail(...)  # Side effect in view - BAD
        return Response(...)
```
```

---

## Token Limits

| Component | Max Tokens | Approximate Lines |
|-----------|------------|-------------------|
| Single rule file | 2000 | ~400 lines |
| CLAUDE.md | 500 | ~100 lines |
| All rules combined | 10000 | ~2000 lines |

**Best Practice**: Keep rules focused. Split large rules into multiple files.
