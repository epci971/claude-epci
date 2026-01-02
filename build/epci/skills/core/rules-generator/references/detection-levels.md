# Detection Levels Reference

## Overview

The rules-generator skill uses a 3-level detection system to analyze projects
and generate appropriate rules. Each level provides increasingly detailed insights.

## Level 1 — Stack Detection

**Purpose**: Identify frameworks, languages, and major dependencies.

### Detection Sources

| File | Detects |
|------|---------|
| `composer.json` | PHP, Symfony, Laravel, packages |
| `package.json` | Node, React, Vue, TypeScript |
| `requirements.txt` | Python, Django, FastAPI |
| `pyproject.toml` | Python, Poetry, modern tooling |
| `pom.xml` | Java, Spring Boot, Maven |
| `build.gradle` | Java, Kotlin, Gradle |
| `go.mod` | Go modules |
| `Cargo.toml` | Rust crates |

### Detection Logic

```python
def detect_stack(project_root: Path) -> dict:
    stack = {"backend": None, "frontend": None, "database": None}

    if (project_root / "composer.json").exists():
        data = json.load(open(project_root / "composer.json"))
        if "symfony/framework-bundle" in data.get("require", {}):
            stack["backend"] = "php-symfony"

    if (project_root / "package.json").exists():
        data = json.load(open(project_root / "package.json"))
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "react" in deps:
            stack["frontend"] = "javascript-react"
        if "tailwindcss" in deps:
            stack["styling"] = "frontend-editor"

    # ... similar for other stacks
    return stack
```

### Output

```json
{
  "level": 1,
  "backend": "python-django",
  "frontend": "javascript-react",
  "styling": "frontend-editor",
  "database": "postgresql",
  "versions": {
    "python": "3.11",
    "django": "5.0",
    "react": "18.2",
    "node": "20.x"
  }
}
```

---

## Level 2 — Architecture Detection

**Purpose**: Identify structural patterns and project organization.

### Detection Patterns

| Pattern | Indicators | Result |
|---------|------------|--------|
| **Monorepo** | `backend/`, `frontend/` dirs | `structure: monorepo` |
| **MVC** | `controllers/`, `models/`, `views/` | `pattern: mvc` |
| **DDD** | `domain/`, `application/`, `infrastructure/` | `pattern: ddd` |
| **Clean Architecture** | `entities/`, `usecases/`, `adapters/` | `pattern: clean` |
| **Hexagonal** | `ports/`, `adapters/` | `pattern: hexagonal` |
| **Service Layer** | `services/`, `handlers/` | `layer: service` |

### Detection Logic

```python
def detect_architecture(project_root: Path) -> dict:
    arch = {"structure": "standard", "pattern": None, "layers": []}

    # Monorepo detection
    if (project_root / "backend").is_dir() and (project_root / "frontend").is_dir():
        arch["structure"] = "monorepo"

    # Pattern detection (backend)
    backend_root = project_root / "backend" if arch["structure"] == "monorepo" else project_root

    if (backend_root / "src" / "Domain").is_dir():
        arch["pattern"] = "ddd"
    elif (backend_root / "apps").is_dir():
        arch["pattern"] = "django-apps"

    # Layer detection
    if any((backend_root / d).is_dir() for d in ["services", "Service"]):
        arch["layers"].append("service")
    if any((backend_root / d).is_dir() for d in ["repositories", "Repository"]):
        arch["layers"].append("repository")

    return arch
```

### Output

```json
{
  "level": 2,
  "structure": "monorepo",
  "pattern": "service-layer",
  "layers": ["controller", "service", "repository"],
  "has_api": true,
  "has_async": true,
  "test_location": "tests/"
}
```

---

## Level 3 — Convention Detection

**Purpose**: Analyze code to extract naming conventions and recurring patterns.

### Detection Areas

| Area | Analysis Method | Examples |
|------|-----------------|----------|
| **Naming** | Regex on class/function names | `snake_case`, `camelCase`, `PascalCase` |
| **Imports** | Parse import statements | stdlib first, third-party, local |
| **Docstrings** | Check presence and format | Google, NumPy, Sphinx |
| **Type hints** | Detect typing usage | Full, partial, none |
| **Error handling** | Exception patterns | Custom exceptions, error codes |

### Detection Logic

```python
def detect_conventions(project_root: Path, stack: dict) -> dict:
    conventions = {
        "naming": {},
        "imports": {},
        "documentation": {},
        "typing": {},
        "patterns": []
    }

    # Sample files for analysis
    py_files = list(project_root.glob("**/*.py"))[:20]  # Limit for performance

    for file in py_files:
        content = file.read_text()

        # Naming detection
        class_names = re.findall(r"class\s+(\w+)", content)
        func_names = re.findall(r"def\s+(\w+)", content)

        # Infer style
        if all(is_pascal_case(n) for n in class_names):
            conventions["naming"]["classes"] = "PascalCase"
        if all(is_snake_case(n) for n in func_names):
            conventions["naming"]["functions"] = "snake_case"

        # Type hints detection
        if "from typing import" in content or ": " in content:
            conventions["typing"]["enabled"] = True

    return conventions
```

### Output

```json
{
  "level": 3,
  "naming": {
    "classes": "PascalCase",
    "functions": "snake_case",
    "constants": "UPPER_SNAKE_CASE",
    "files": "snake_case"
  },
  "imports": {
    "order": ["stdlib", "third_party", "local"],
    "style": "absolute"
  },
  "documentation": {
    "docstrings": "google",
    "coverage": 0.7
  },
  "typing": {
    "enabled": true,
    "coverage": 0.85
  },
  "patterns": [
    "repository_pattern",
    "service_layer",
    "dto_usage"
  ]
}
```

---

## Fallback Strategy

If detection fails at a higher level, fall back gracefully:

```
Level 3 fails → Use Level 2 defaults
Level 2 fails → Use Level 1 defaults
Level 1 fails → Use generic templates
```

### Warning Messages

```python
if not level_3_success:
    warnings.append("Convention detection incomplete. Using stack defaults.")
if not level_2_success:
    warnings.append("Architecture detection failed. Using standard structure.")
if not level_1_success:
    warnings.append("Stack detection failed. Generating generic rules.")
```

---

## Integration with Rules Generation

The detection results feed into template selection:

```python
def select_templates(detection: dict) -> list[str]:
    templates = ["global-quality", "global-git-workflow"]

    if detection["backend"]:
        templates.append(f"backend-{detection['backend']}")
    if detection["frontend"]:
        templates.append(f"frontend-{detection['frontend']}")
    if detection.get("styling"):
        templates.append(f"styling-{detection['styling']}")

    return templates
```
