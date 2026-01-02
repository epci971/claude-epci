---
paths:
  - src/**/*.py
  - "!src/**/tests/**"
  - "!src/project-memory/tests/**"
---

# Python Scripts Conventions

> Conventions pour le code Python du plugin (scripts, hooks, orchestration).

## 🔴 CRITICAL

1. **Type hints obligatoires**: Toute fonction publique doit avoir des types
2. **Docstrings Google style**: Pour fonctions et classes publiques
3. **Pas d'import ***: Imports explicites uniquement
4. **Pas de print() en production**: Utiliser logging

## 🟡 CONVENTIONS

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Fichiers | snake_case | `validate_skill.py` |
| Classes | PascalCase | `WaveOrchestrator` |
| Fonctions | snake_case | `detect_stack()` |
| Constantes | UPPER_SNAKE | `MAX_TOKENS` |

### Structure fichiers

```python
"""Module docstring."""

# Standard library
import json
import re
from pathlib import Path

# Third party (si applicable)
import yaml

# Local imports
from ..orchestration import WavePlanner

# Constants
MAX_TOKENS = 5000

# Classes/Functions
```

### Fonctions

- Max 30 lignes par fonction
- Early return pour lisibilite
- Arguments nommes pour > 3 params

## 🟢 PREFERENCES

- f-strings preferes a .format()
- pathlib.Path plutot que os.path
- dataclasses pour DTOs simples
- List comprehensions quand lisibles

## Quick Reference

| Task | Pattern |
|------|---------|
| Lire JSON | `json.loads(Path(f).read_text())` |
| Lire YAML | `yaml.safe_load(Path(f).read_text())` |
| Glob fichiers | `Path(root).glob("**/*.py")` |
| Regex | `re.search(pattern, text)` |

## Common Patterns

| Pattern | Implementation |
|---------|----------------|
| Validation | Return `tuple[bool, list[str]]` (valid, errors) |
| Detection | Dict avec categories detectees |
| Config | JSON/YAML en `.project-memory/` |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Bare except | Masque erreurs | `except SpecificError` |
| Mutable defaults | Bug subtil | `None` puis assign |
| Global state | Tests difficiles | Injection dependances |

## Examples

### Correct

```python
def validate_frontmatter(content: str) -> tuple[bool, list[str]]:
    """Validate YAML frontmatter in markdown file.

    Args:
        content: Raw markdown content with frontmatter.

    Returns:
        Tuple of (is_valid, list_of_errors).
    """
    errors: list[str] = []

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, ["Missing YAML frontmatter"]

    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML: {e}"]

    if "paths" not in data:
        errors.append("Missing required field: paths")

    return len(errors) == 0, errors
```

### Incorrect

```python
# Bad - no types, no docstring, bare except
def validate(c):
    try:
        d = yaml.load(c)  # unsafe load
        if d.get('paths'):
            return True
    except:  # bare except
        pass
    return False
```
