---
paths: []
---

# Project Commands

> Commandes frequentes pour le developpement.

## 🟡 CONVENTIONS

### Development

```bash
# Backend ({{backend_framework}})
{{dev_backend_command}}

# Frontend ({{frontend_framework}})
{{dev_frontend_command}}

# Full stack (si docker-compose)
docker-compose up -d
```

### Testing

```bash
# All tests
{{test_command}}

# With coverage
{{test_coverage_command}}

# Single test
{{test_single_command}}
```

### Quality

```bash
# Linting
{{lint_command}}

# Formatting
{{format_command}}

# Type checking
{{typecheck_command}}
```

### Database

```bash
# Migrations
{{migration_create_command}}
{{migration_run_command}}

# Reset (dev only)
{{db_reset_command}}
```

### Build & Deploy

```bash
# Build production
{{build_command}}

# Deploy (si applicable)
{{deploy_command}}
```

## Quick Reference

| Task | Command |
|------|---------|
| Start dev | `{{dev_command}}` |
| Run tests | `{{test_command}}` |
| Lint | `{{lint_command}}` |
| Build | `{{build_command}}` |

## Environment Variables

```bash
# Required
{{required_env_vars}}

# Optional
{{optional_env_vars}}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port already in use | `lsof -i :PORT` then `kill PID` |
| Dependencies outdated | `{{install_command}}` |
| Database connection | Check `.env` and DB service status |
| Cache issues | `{{cache_clear_command}}` |
