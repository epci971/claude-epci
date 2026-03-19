# Domain Mapping Reference

Reference for detecting technology domains from file extensions.
Used by step-03-code-auto for stack skill loading and step-04-review-auto for security pattern detection.

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

## Stack Skill Loading

For each component file, load the corresponding stack skill ONCE per type:

```
stack_cache = {}

FOR each component in plan:
  ext = get_extension(component.file)
  stack = extension_to_stack(ext)
  IF stack AND stack NOT IN stack_cache:
    Read(src/skills/stack/{stack}/SKILL.md)
    Read(src/skills/stack/{stack}/references/*.md)
    stack_cache[stack] = true
  Apply stack patterns for implementation and tests
```

## Security Pattern Detection

Used by step-04-review-auto to trigger @security-auditor:

```
Path patterns: **/auth/**, **/security/**, **/middleware/**
Keywords: password, jwt, oauth, encrypt, decrypt, token, session, cookie, csrf, cors, authenticate, authorize
File names: auth.*, security.*, middleware.*, permissions.*
```
