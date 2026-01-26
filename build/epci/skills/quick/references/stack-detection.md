# Stack Detection Reference

Algorithme de détection automatique des stack skills pour `/quick`.

## Objectif

Détecter le stack technique du projet pour charger le skill approprié et obtenir les conventions/patterns.

## Stacks Supportés

| Stack | Skill | Fournit |
|-------|-------|---------|
| Django | `python-django` | Patterns Django, pytest, DRF |
| React | `javascript-react` | Patterns React, Jest/Vitest, TypeScript |
| Spring Boot | `java-springboot` | Patterns Spring, JUnit, Lombok |
| Symfony | `php-symfony` | Patterns Symfony, PHPUnit, Doctrine |
| Tailwind | `frontend-editor` | Patterns CSS, a11y, composants |

## Algorithme de Scoring

### Étape 1: Définir les Signatures

```python
STACK_SIGNATURES = {
    "python-django": {
        "files": ["manage.py", "settings.py", "wsgi.py"],
        "deps": {
            "requirements.txt": ["django"],
            "pyproject.toml": ["django"],
            "Pipfile": ["django"]
        },
        "dirs": ["templates/", "static/"],
        "confidence_base": 0.9
    },
    "javascript-react": {
        "files": ["package.json"],
        "deps": {
            "package.json": ["react", "react-dom"]
        },
        "dirs": ["src/components/", "src/pages/"],
        "extensions": [".tsx", ".jsx"],
        "confidence_base": 0.85
    },
    "java-springboot": {
        "files": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "deps": {
            "pom.xml": ["spring-boot"],
            "build.gradle": ["org.springframework.boot"]
        },
        "dirs": ["src/main/java/"],
        "confidence_base": 0.9
    },
    "php-symfony": {
        "files": ["composer.json", "bin/console", "symfony.lock"],
        "deps": {
            "composer.json": ["symfony/framework-bundle"]
        },
        "dirs": ["src/Controller/", "src/Entity/"],
        "confidence_base": 0.9
    },
    "frontend-editor": {
        "files": ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.mjs"],
        "deps": {
            "package.json": ["tailwindcss"]
        },
        "confidence_base": 0.8
    }
}
```

### Étape 2: Calculer le Score

```python
def detect_stack(root: str) -> list[StackResult]:
    """Détecte les stacks avec scoring de confidence."""
    results = []

    for stack_name, signatures in STACK_SIGNATURES.items():
        score = 0
        evidence = []

        # Check files (30 points each)
        for file in signatures.get("files", []):
            if exists(join(root, file)):
                score += 30
                evidence.append(f"file:{file}")

        # Check deps in manifests (25 points each)
        for manifest, deps in signatures.get("deps", {}).items():
            manifest_path = join(root, manifest)
            if exists(manifest_path):
                content = read_file(manifest_path)
                for dep in deps:
                    if dep in content:
                        score += 25
                        evidence.append(f"dep:{dep}")

        # Check dirs (15 points each)
        for dir_path in signatures.get("dirs", []):
            if isdir(join(root, dir_path)):
                score += 15
                evidence.append(f"dir:{dir_path}")

        # Threshold: minimum 30 points to be considered
        if score >= 30:
            confidence = min(1.0, score / 100 * signatures["confidence_base"])
            results.append(StackResult(
                name=stack_name,
                confidence=confidence,
                evidence=evidence
            ))

    # Sort by confidence descending
    return sorted(results, key=lambda r: r.confidence, reverse=True)
```

### Étape 3: Sélectionner le Meilleur Match

```python
def select_stack(results: list[StackResult]) -> StackResult | None:
    """Sélectionne le stack avec la meilleure confidence."""
    if not results:
        return None

    best = results[0]

    # Confidence threshold: 0.5 minimum
    if best.confidence < 0.5:
        return None

    return best
```

## Ordre de Priorité

1. **Fichiers de signature** (manage.py, package.json, etc.) - 30 pts
2. **Dépendances dans manifests** (django, react, etc.) - 25 pts
3. **Structure de répertoires** (src/components/, etc.) - 15 pts

## Exemples de Détection

### Projet Django

```
project/
├── manage.py                 → +30 (file:manage.py)
├── requirements.txt
│   └── contains "django"     → +25 (dep:django)
├── myapp/
│   └── settings.py          → +30 (file:settings.py)
└── templates/                → +15 (dir:templates/)

Score: 100 → Confidence: 0.9
Result: python-django
```

### Projet React + Tailwind

```
project/
├── package.json              → +30 (file:package.json)
│   ├── "react"               → +25 (dep:react)
│   ├── "react-dom"           → +25 (dep:react-dom)
│   └── "tailwindcss"         → +25 (dep:tailwindcss)
├── tailwind.config.js        → +30 (file:tailwind.config.js)
└── src/components/           → +15 (dir:src/components/)

React Score: 95 → Confidence: 0.81
Tailwind Score: 85 → Confidence: 0.68
Result: [javascript-react, frontend-editor] (both loaded)
```

## Multi-Stack Support

Un projet peut avoir plusieurs stacks (ex: React + Tailwind).

```python
def get_all_relevant_stacks(results: list[StackResult]) -> list[str]:
    """Retourne tous les stacks avec confidence > 0.5."""
    return [r.name for r in results if r.confidence >= 0.5]
```

## Output

```python
@dataclass
class StackResult:
    name: str           # "python-django"
    confidence: float   # 0.0 - 1.0
    evidence: list[str] # ["file:manage.py", "dep:django"]
```

## Cas Spéciaux

### Aucun Stack Détecté

Si aucun stack n'atteint le threshold :

```python
if not stacks:
    # Continue sans stack skill
    # Utiliser patterns génériques
    pass
```

### Stack Ambigu

Si plusieurs stacks ont des scores proches :

```python
if len(stacks) > 1 and stacks[0].confidence - stacks[1].confidence < 0.1:
    # Charger les deux stacks
    # Prioriser celui avec le meilleur match pour les fichiers cibles
    pass
```
