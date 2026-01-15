<!--
  Template: CLAUDE.md (project root)
  Note: This is NOT a rules file. No YAML frontmatter required.
  This template generates the project's main CLAUDE.md file.
  Variables: {{project_name}}, {{stack}}, etc. are substituted at generation time.
-->
# {{project_name}}

## Description

{{project_description}}

## Architecture

- **Pattern**: {{architecture_pattern}}
- **Structure**: {{structure_type}}
- **Backend**: {{backend_description}}
- **Frontend**: {{frontend_description}}

## Stack Technique

| Couche | Technologie | Version | Notes |
|--------|-------------|---------|-------|
| Backend | {{backend_framework}} | {{backend_version}} | {{backend_notes}} |
| Frontend | {{frontend_framework}} | {{frontend_version}} | {{frontend_notes}} |
| Styling | {{styling_framework}} | {{styling_version}} | Design tokens |
| Database | {{database}} | {{database_version}} | |
| Cache | {{cache}} | {{cache_version}} | Si applicable |

## Commandes Essentielles

```bash
# Installation
{{install_command}}

# Developpement
{{dev_backend_command}}      # Backend
{{dev_frontend_command}}     # Frontend

# Tests
{{test_command}}             # Tous les tests

# Qualite
{{lint_command}}             # Linting
{{format_command}}           # Formatting
```

## Conventions

Les conventions techniques detaillees sont dans `.claude/rules/`:

| Domaine | Fichier | Scope |
|---------|---------|-------|
| Backend | `rules/backend/{{backend_rule_file}}` | `backend/**/*` |
| Frontend | `rules/frontend/react.md` | `frontend/**/*.tsx` |
| Styling | `rules/frontend/tailwind.md` | `frontend/**/*.css` |
| Tests | `rules/testing/*.md` | `**/tests/**/*` |
| Qualite | `rules/_global/quality.md` | Tout le projet |

-> Voir `.claude/rules/` pour les details techniques
