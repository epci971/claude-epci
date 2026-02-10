# Domain Mapping Reference

Reference for detecting technology domains from file extensions in the implementation plan.
Used by step-03b-team.md to determine if team mode should activate.

## File Extension → Domain Mapping

| Extension(s) | Domain | Stack Skill |
|---------------|--------|-------------|
| `*.py` | `backend` | python-django |
| `*.php` | `backend` | php-symfony |
| `*.java` | `backend` | java-springboot |
| `*.tsx`, `*.jsx` | `frontend` | javascript-react |
| `*.ts`, `*.js` | `frontend` | javascript-react |
| `*.css`, `*.scss`, `*.html` | `styling` | frontend-editor |
| `*.md` | `docs` | - |
| `*.json`, `*.yaml`, `*.yml` | `config` | - |
| `*.sql` | `database` | - |
| `*.sh`, `*.bash` | `infra` | - |

## Domain Grouping

Domains that count as **distinct** for team mode threshold:

| Domain | Counts as distinct | Reason |
|--------|-------------------|--------|
| `backend` | Yes | Requires stack-specific patterns |
| `frontend` | Yes | Requires stack-specific patterns |
| `styling` | No (merged with `frontend`) | Same review context as frontend |
| `docs` | No | Documentation only, no code review |
| `config` | No | Configuration, reviewed with associated domain |
| `database` | Yes | Distinct review expertise |
| `infra` | No | Scripts, reviewed with associated domain |

**Effective distinct domains**: `backend`, `frontend` (+styling), `database`

## Detection Algorithm

```
INPUT: List of files from approved plan (step-02)

1. EXTRACT file extensions from all planned files
2. MAP each extension to its domain using table above
3. MERGE styling into frontend
4. IGNORE docs, config, infra domains
5. COUNT distinct remaining domains
6. RETURN { domains: [...], count: N, files_per_domain: {...} }
```

## Threshold Logic

```
team_mode_active = (
  (complexity >= STANDARD AND distinct_domains >= 2)
  OR flag_team == true
) AND flag_no_team != true
```

## Examples

### Example 1: Multi-domain (team mode = YES)
```
Plan files: auth_service.py, auth_views.py, LoginForm.tsx, login.css
Domains: backend(2), frontend(1), styling(1)
Distinct: backend, frontend (styling merged)
Count: 2 → Team mode activates
```

### Example 2: Single-domain (team mode = NO)
```
Plan files: models.py, views.py, serializers.py, tests.py
Domains: backend(4)
Distinct: backend
Count: 1 → Classic mode
```

### Example 3: Docs only (team mode = NO)
```
Plan files: README.md, CHANGELOG.md, api-docs.md
Domains: docs(3)
Distinct: none (docs excluded)
Count: 0 → Classic mode
```
