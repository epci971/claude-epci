# EPCI Plugin for Claude Code

## Description

Plugin Claude Code implementant le workflow EPCI (Explore, Plan, Code, Inspect).
Systeme de gestion du developpement avec skills, subagents et hooks.

## Architecture

- **Pattern**: Plugin modulaire
- **Structure**: Monorepo avec src/ organise par fonction
- **Backend**: Python 3 (scripts, orchestration, hooks)
- **Content**: Markdown (skills, agents)

## Stack Technique

| Couche | Technologie | Notes |
|--------|-------------|-------|
| Scripts | Python 3 | validation, orchestration, hooks |
| Content | Markdown | skills, agents |
| Config | JSON/YAML | settings, plugin manifest |
| Tests | pytest | src/scripts/, src/project-memory/tests/ |

## Structure du Projet

```
src/
├── agents/           # 15 subagents (validateurs, reviewers, turbo, brainstorm)
├── hooks/            # Systeme hooks (runner.py)
├── mcp/              # MCP Integration (config, activation)
├── orchestration/    # Wave orchestration
├── project-memory/   # Gestion memoire projet (Python)
├── scripts/          # Validation scripts (Python)
├── settings/         # Configuration
└── skills/           # 30 skills
    ├── core/         # 18 skills fondamentaux
    ├── stack/        # 5 skills technologie
    ├── factory/      # 4 skills creation composants
    ├── personas/     # Systeme personas
    ├── mcp/          # MCP skill
    └── promptor/     # Voice-to-brief
```

## Commandes Essentielles

```bash
# Validation complete
python src/scripts/validate_all.py

# Validation par type
python src/scripts/validate_skill.py src/skills/core/epci-core/
python src/scripts/validate_subagent.py src/agents/code-reviewer.md

# Tests orchestration
python src/scripts/test_orchestration.py

# Hooks
python src/hooks/runner.py post-phase-3 --context '{...}'
```

## Conventions

Les conventions techniques detaillees sont dans `.claude/rules/`:

| Domaine | Fichier | Scope |
|---------|---------|-------|
| Python | `rules/python-scripts.md` | `src/**/*.py` |
| Plugin | `rules/plugin-content.md` | `src/**/*.md` |
| Qualite | `rules/global-quality.md` | Tout le projet |
| Git | `rules/global-git-workflow.md` | Commits/branches |

-> Voir `.claude/rules/` pour les details techniques
