---
paths:
  - src/**/test_*.py
  - src/**/tests/**/*.py
  - src/project-memory/tests/**/*.py
---

# Python Testing Conventions

> Conventions pour les tests Python du plugin EPCI.

## 🔴 CRITICAL

1. **Nommage test_**: Prefixe `test_` pour fichiers et fonctions
2. **Assertions explicites**: Un assert par comportement teste
3. **Pas de side effects**: Tests independants et idempotents
4. **Fixtures pour setup**: Utiliser pytest fixtures

## 🟡 CONVENTIONS

### Structure fichiers

```
src/
├── module/
│   ├── __init__.py
│   └── feature.py
└── scripts/
    └── test_module.py    # Tests du module
```

Ou pattern alternatif:
```
src/
└── project-memory/
    ├── manager.py
    └── tests/
        ├── conftest.py   # Fixtures partagees
        └── test_manager.py
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Fichier | `test_{module}.py` | `test_validation.py` |
| Fonction | `test_{action}_{scenario}` | `test_validate_returns_errors_on_invalid_yaml` |
| Fixture | `{resource}_fixture` | `sample_skill_fixture` |

### Structure test

```python
def test_function_does_something_specific():
    # Arrange
    input_data = create_test_data()

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result.is_valid
    assert len(result.errors) == 0
```

## 🟢 PREFERENCES

- pytest plutot que unittest
- parametrize pour cas multiples
- tmp_path pour fichiers temporaires
- monkeypatch pour mocks simples

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `@pytest.fixture` | Setup reutilisable |
| `@pytest.mark.parametrize` | Cas multiples |
| `tmp_path` | Fichiers temporaires |
| `monkeypatch` | Mock simple |
| `capsys` | Capture stdout/stderr |

## Common Patterns

### Fixture partagee

```python
# conftest.py
@pytest.fixture
def sample_skill_content() -> str:
    return '''---
name: test-skill
description: Test skill for validation
---

# Test Skill

## Overview
Test content.
'''
```

### Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("valid_content", True),
    ("missing_frontmatter", False),
    ("invalid_yaml", False),
])
def test_validate_handles_cases(input: str, expected: bool):
    result = validate(FIXTURES[input])
    assert result.is_valid == expected
```

### Fichiers temporaires

```python
def test_writes_output_file(tmp_path: Path):
    output = tmp_path / "output.json"
    generate_output(output)
    assert output.exists()
    data = json.loads(output.read_text())
    assert "result" in data
```

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Tests dependants | Ordre important | Fixtures independantes |
| Assertions multiples | Echec opaque | Un assert par test |
| Mock excessif | Tests fragiles | Integration quand possible |
| Sleep dans tests | Lent, flaky | Events, conditions |

## Examples

### Correct

```python
import pytest
from pathlib import Path
from src.scripts.validate_skill import validate_skill


@pytest.fixture
def valid_skill_path(tmp_path: Path) -> Path:
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text('''---
name: test-skill
description: A test skill
---

# Test Skill
''')
    return skill_dir


def test_validate_skill_accepts_valid_structure(valid_skill_path: Path):
    is_valid, errors = validate_skill(valid_skill_path)
    assert is_valid
    assert errors == []


def test_validate_skill_rejects_missing_frontmatter(tmp_path: Path):
    skill_dir = tmp_path / "bad-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# No frontmatter")

    is_valid, errors = validate_skill(skill_dir)
    assert not is_valid
    assert "frontmatter" in errors[0].lower()
```

### Incorrect

```python
# Bad - multiple concerns, no fixtures, vague assertions
def test_stuff():
    # Setup mixed with test
    with open("test.md", "w") as f:
        f.write("content")

    result = validate("test.md")
    assert result  # Vague

    # Cleanup in test
    os.remove("test.md")
```
