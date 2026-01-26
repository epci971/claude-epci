# Stacks Catalog

> Reference for Factory to auto-detect and recommend relevant stack skills.

## Available Stack Skills

| Stack | Target | Skill Path |
|-------|--------|------------|
| `python-django` | Django/DRF backend | `src/skills/stack/python-django/` |
| `javascript-react` | React islands/SPA | `src/skills/stack/javascript-react/` |
| `java-springboot` | Spring Boot backend | `src/skills/stack/java-springboot/` |
| `php-symfony` | Symfony 7/8 backend | `src/skills/stack/php-symfony/` |
| `frontend-editor` | Tailwind/a11y styling | `src/skills/stack/frontend-editor/` |

## Auto-Detection Rules

### python-django

**Detect if ANY of:**
- `manage.py` exists at project root
- `requirements.txt` contains `django`
- `pyproject.toml` contains `django`
- `settings.py` exists in any subdirectory
- Files match `**/views.py`, `**/models.py`, `**/urls.py` pattern

**Confidence levels:**
- HIGH: `manage.py` + `django` in dependencies
- MEDIUM: `django` in dependencies only
- LOW: Django-like file patterns only

### javascript-react

**Detect if ANY of:**
- `package.json` contains `react` or `react-dom`
- Files with `.tsx` or `.jsx` extension exist
- `next.config.*` or `vite.config.*` exists
- Import statements contain `from 'react'`

**Confidence levels:**
- HIGH: `react` in package.json + `.tsx` files
- MEDIUM: `.tsx/.jsx` files only
- LOW: JSX-like syntax detected

### java-springboot

**Detect if ANY of:**
- `pom.xml` contains `spring-boot`
- `build.gradle` contains `spring-boot`
- Files match `**/Application.java` with `@SpringBootApplication`
- `application.yml` or `application.properties` exists

**Confidence levels:**
- HIGH: `spring-boot` in pom.xml/build.gradle
- MEDIUM: Spring annotations detected
- LOW: Java project structure only

### php-symfony

**Detect if ANY of:**
- `composer.json` contains `symfony/`
- `bin/console` exists
- `config/bundles.php` exists
- Files in `src/Controller/`, `src/Entity/`

**Confidence levels:**
- HIGH: `symfony/framework-bundle` in composer.json
- MEDIUM: Symfony file structure
- LOW: PHP project with MVC pattern

### frontend-editor

**Detect if ANY of:**
- `tailwind.config.js` or `tailwind.config.ts` exists
- `postcss.config.*` with tailwind plugin
- CSS files contain `@tailwind` directive
- `*.css` files with utility class patterns

**Confidence levels:**
- HIGH: `tailwind.config.*` exists
- MEDIUM: Tailwind directives in CSS
- LOW: Utility-first CSS patterns

## Detection Priority

When multiple stacks detected, prioritize by:

1. **Primary stack** (highest confidence backend): django/springboot/symfony
2. **Frontend stack** (if React detected): javascript-react
3. **Styling stack** (if Tailwind detected): frontend-editor

## Output Format for Factory

```
DETECTED STACK:
- php-symfony (HIGH: composer.json + symfony/framework-bundle)
- frontend-editor (HIGH: tailwind.config.ts)

RECOMMENDED REFERENCES:
- Stack php-symfony provides: architecture, doctrine, security, testing, messenger
- Stack frontend-editor provides: tailwind-conventions, accessibility, components-catalog
```

## Stack Combinations

Common combinations and their implications:

| Backend | Frontend | Styling | Pattern |
|---------|----------|---------|---------|
| python-django | javascript-react | frontend-editor | Full-stack SPA |
| php-symfony | javascript-react | frontend-editor | Symfony + React islands |
| java-springboot | javascript-react | frontend-editor | Enterprise full-stack |
| php-symfony | - | frontend-editor | Symfony + Twig + Tailwind |
| python-django | - | - | Django templates (traditional) |
