# Feature Document — EPCI Rules Generator

> **Slug**: `epci-rules`
> **Category**: STANDARD
> **Date**: 2026-01-02

---

## §1 — Functional Brief

### Context

Créer une commande `/epci:rules` qui analyse automatiquement un projet pour générer une structure `.claude/rules/` optimisée. Cette commande maintient la cohérence entre le fichier `CLAUDE.md` (vision fonctionnelle/projet) et les rules (conventions techniques par stack).

Le besoin est issu de l'absence de conventions documentées dans les projets, l'incohérence entre le code et les bonnes pratiques, et le temps perdu à redécouvrir les patterns à chaque session.

### Detected Stack

- **Framework**: EPCI Plugin v4.4
- **Language**: Markdown (commands, skills, agents) + Python (scripts, hooks)
- **Patterns**: Command+Skill+Agent, Factory (templates), Hooks (post-action), Validation scripts

### Target Stacks for Templates

| Stack | Backend | Frontend | Priority |
|-------|---------|----------|----------|
| Python Django | `backend/**/*.py` | — | P1 |
| PHP Symfony | `backend/**/*.php` | — | P1 |
| JavaScript React | — | `frontend/**/*.tsx` | P1 |
| Java SpringBoot | `backend/**/*.java` | — | P1 |
| Frontend Editor | — | `frontend/**/*.css` | P1 |

### Acceptance Criteria

- [ ] `/epci:rules init` génère CLAUDE.md + rules/ pour un projet multi-stack
- [ ] `/epci:rules validate` détecte le drift entre code et rules
- [ ] Les paths patterns s'auto-activent correctement (tous stacks)
- [ ] @rules-validator valide la structure générée
- [ ] Hook post-rules-init sauvegarde dans .project-memory/
- [ ] Script validate_rules.py passe pour les rules générées
- [ ] Tous les stacks ont leurs templates (Django, Symfony, React, SpringBoot, Tailwind)

### Constraints

- Limite 5000 tokens par skill/command
- Limite 2000 tokens par agent
- Scripts Python sans dépendances externes (stdlib only)
- Compatibilité avec structure EPCI v4.4 existante

### Out of Scope

- Action `sync` (import linters) — différé v1.1
- Support autres stacks (Vue, Angular, FastAPI, Laravel)
- UI/Dashboard de gestion des rules

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 32 (27 créés + 5 modifiés)
- **Estimated LOC**: ~6000
- **Risk**: Medium (intégration skills existants, détection Niveau 3)
- **Justification**: Multi-composants (command, skill, agent, scripts, templates), mais patterns existants à suivre

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think-hard` | auto | >10 files impacted |

### Memory Summary

- **Project**: EPCI Plugin v4.4
- **Stack**: Markdown + Python
- **Conventions**: kebab-case, YAML frontmatter, <5000 tokens
- **Features completed**: 5+ (f07-orchestration, f09-personas, frontend-editor)
- **Patterns**: Factory skills, validation scripts, hooks system

---

## §2 — Implementation Plan

### Niveaux de Détection

| Niveau | Analyse | Méthode |
|--------|---------|---------|
| 1 | Stack | composer.json, package.json, requirements.txt |
| 2 | Architecture | Dossiers (backend/, frontend/, DDD, MVC) |
| 3 | Conventions | Nommage classes/fonctions, patterns récurrents |

### Impacted Files (32 total)

#### À Créer (27 fichiers)

| # | File | Action | Risk |
|---|------|--------|------|
| 1 | `src/skills/core/rules-generator/SKILL.md` | Create | Low |
| 2 | `src/skills/core/rules-generator/references/detection-levels.md` | Create | Low |
| 3 | `src/skills/core/rules-generator/references/rules-format.md` | Create | Low |
| 4 | `src/skills/core/rules-generator/references/stack-templates.md` | Create | Low |
| 5 | `src/agents/rules-validator.md` | Create | Low |
| 6 | `src/commands/rules.md` | Create | Medium |
| 7 | `src/scripts/validate_rules.py` | Create | Medium |
| 8 | `src/hooks/active/post-rules-init.py` | Create | Low |
| 9-11 | `src/skills/stack/python-django/rules-templates/*.md` (3) | Create | Low |
| 12-14 | `src/skills/stack/php-symfony/rules-templates/*.md` (3) | Create | Low |
| 15-17 | `src/skills/stack/javascript-react/rules-templates/*.md` (3) | Create | Low |
| 18-20 | `src/skills/stack/java-springboot/rules-templates/*.md` (3) | Create | Low |
| 21-22 | `src/skills/stack/frontend-editor/rules-templates/*.md` (2) | Create | Low |
| 23-27 | `src/skills/core/rules-generator/templates/*.md` (5) | Create | Low |

#### À Modifier (5 fichiers)

| # | File | Action | Risk |
|---|------|--------|------|
| 28 | `src/commands/brief.md` | Modify (+15 LOC) | Low |
| 29 | `src/commands/epci.md` | Modify (+5 LOC) | Low |
| 30 | `src/scripts/validate_all.py` | Modify (+5 LOC) | Low |
| 31 | `src/skills/core/project-memory/SKILL.md` | Modify (+15 LOC) | Low |
| 32 | `CLAUDE.md` | Modify (+10 LOC) | Low |

### Tasks

#### Wave 0 — Prérequis (5 min)

1. [ ] **Setup directories** (5 min)
   - Create: `src/skills/core/rules-generator/{references,templates}`
   - Create: `src/skills/stack/*/rules-templates/`
   - Test: `ls -la` directories exist

#### Wave 1 — Fondations (parallélisable, 20 min)

2. [ ] **Create skill references** (15 min)
   - Files: #2, #3, #4
   - Test: Content accessible, markdown valid

3. [ ] **Create global templates** (10 min)
   - Files: #23-#27
   - Test: YAML frontmatter valid

4. [ ] **Create validate_rules.py** (20 min)
   - File: #7
   - Test: `python validate_rules.py --help`

#### Wave 2 — Core Skill (25 min)

5. [ ] **Create rules-generator SKILL.md** (25 min)
   - File: #1
   - Depends: Wave 1
   - Test: `validate_skill.py` passes

#### Wave 3 — Templates Stack (parallélisable, 10 min)

6. [ ] **Templates Python Django** (10 min)
   - Files: #9, #10, #11
   - Test: YAML parse, paths `backend/**/*.py`

7. [ ] **Templates PHP Symfony** (10 min)
   - Files: #12, #13, #14
   - Test: YAML parse, paths `backend/**/*.php`

8. [ ] **Templates JavaScript React** (10 min)
   - Files: #15, #16, #17
   - Test: YAML parse, paths `frontend/**/*.tsx`

9. [ ] **Templates Java SpringBoot** (10 min)
   - Files: #18, #19, #20
   - Test: YAML parse, paths `backend/**/*.java`

10. [ ] **Templates Frontend Editor** (10 min)
    - Files: #21, #22
    - Test: YAML parse, paths `**/*.css`, `**/tailwind.config.*`

#### Wave 4 — Agent (15 min)

11. [ ] **Create rules-validator agent** (15 min)
    - File: #5
    - Depends: Wave 2
    - Test: `validate_subagent.py` passes

#### Wave 5 — Command (25 min)

12. [ ] **Create rules command** (25 min)
    - File: #6
    - Depends: Waves 2, 3, 4
    - Test: `validate_command.py` passes

#### Wave 6 — Intégration (25 min)

13. [ ] **Create hook post-rules-init** (15 min)
    - File: #8
    - Test: Mock execution creates rules-history.json

14. [ ] **Modify existing files** (10 min)
    - Files: #28-#32
    - Test: `validate_all.py` passes
    - Rollback: `git stash` before

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Détection Niveau 3 imprécise | Medium | Fallback Niveau 2, warning |
| Paths patterns frontend-editor | Low | Tests spécifiques CSS/Tailwind |
| Limite tokens skill (5000) | Low | Externaliser en références |
| Conflit CLAUDE.md | Low | Backup avant modification |

### Validation

- **@plan-validator**: APPROVED
- **Completeness**: 32/32 files covered
- **Dependencies**: All waves properly sequenced
- **Tests**: Defined for each task

### Time Estimate

| Mode | Time |
|------|------|
| Sequential | 3h10 |
| Parallel (Waves 1, 3) | ~2h |

---

## §3 — Implementation & Finalization

### Progress

- [x] Wave 0 — Setup directories
- [x] Wave 1 — Fondations (références, templates globaux, validate_rules.py)
- [x] Wave 2 — Core Skill rules-generator
- [x] Wave 3 — Templates Stack (5 stacks: Django, Symfony, React, SpringBoot, Frontend-Editor)
- [x] Wave 4 — Agent @rules-validator
- [x] Wave 5 — Command rules.md
- [x] Wave 6 — Intégration (hook + modifications)

### Tests

```bash
$ python3 src/scripts/validate_all.py
Skills:      26 passed, 0 failed
Commands:    11 passed, 0 failed
Agents:      10 passed, 0 failed
Flags:       passed
Rules:       passed

RESULT: ✅ CORE VALIDATIONS PASSED
```

### Reviews

- **@code-reviewer**: APPROVED_WITH_FIXES (0 Critical, 4 Important, 6 Minor)
  - All Critical/Important issues fixed:
    - Added clarification comment to `claude-md.md` template
    - Documented empty `paths: []` behavior in global templates
    - Added `--verbose` flag to `validate_rules.py`
- **@security-auditor**: N/A (no auth/security files involved)
- **@qa-reviewer**: N/A

### Files Created (27)

| Category | Files |
|----------|-------|
| Skill | `src/skills/core/rules-generator/SKILL.md` |
| References | `references/detection-levels.md`, `rules-format.md`, `stack-templates.md` |
| Global Templates | `templates/claude-md.md`, `global-quality.md`, `global-git-workflow.md`, `global-commands.md`, `domain-glossary.md` |
| Django Templates | `backend-django.md`, `testing-pytest.md`, `api-drf.md` |
| Symfony Templates | `backend-symfony.md`, `testing-phpunit.md`, `security-symfony.md` |
| React Templates | `frontend-react.md`, `state-management.md`, `testing-vitest.md` |
| SpringBoot Templates | `backend-spring.md`, `testing-junit.md`, `security-spring.md` |
| Frontend-Editor | `styling-tailwind.md`, `accessibility.md` |
| Script | `src/scripts/validate_rules.py` |
| Agent | `src/agents/rules-validator.md` |
| Command | `src/commands/rules.md` |
| Hook | `src/hooks/active/post-rules-init.py` |

### Files Modified (5)

- `src/commands/brief.md` — Added Step 7: Rules Suggestion
- `src/commands/epci.md` — Added /rules suggestion after Phase 3
- `src/scripts/validate_all.py` — Added rules validation section
- `src/skills/core/project-memory/SKILL.md` — Added rules_initialized tracking
- `CLAUDE.md` — Added /rules command (11), @rules-validator agent (10), rules-generator skill (25)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| None | - | Implementation followed plan |

### Documentation

- `/rules` command fully documented in `src/commands/rules.md`
- Skill documentation in `SKILL.md` with references
- CLAUDE.md updated with new counts

### PR Ready

- Branch: `master` (direct implementation)
- Tests: ✅ All core validations passing
- Lint: ✅ Python scripts clean
- Docs: ✅ Up to date
