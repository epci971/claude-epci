# Feature Document — Skill `frontend-editor`

> **Slug**: `frontend-editor`
> **Category**: STANDARD
> **Date**: 2026-01-02

---

## §1 — Functional Brief

### Context

Le projet EPCI dispose d'un skill `javascript-react` orienté comportement et interactivité. Il manque un skill dédié à la **couche présentation** (HTML/CSS/Tailwind) pour compléter l'écosystème et orchestrer automatiquement les MCP Magic et Context7.

### Detected Stack

- **Framework**: EPCI Plugin System v3.5.0
- **Language**: Markdown + TypeScript examples
- **Patterns**: skill-stack (modèle: javascript-react)

### Acceptance Criteria

- [ ] SKILL.md créé avec front matter YAML valide
- [ ] 3 fichiers references créés (tailwind, components, accessibility)
- [ ] Auto-détection sur tailwind.config.* + optionnel shadcn/radix
- [ ] MCP Magic et Context7 triggers documentés
- [ ] Variants complets: primary, secondary, success, warning, danger, ghost, outline
- [ ] Accessibilité WCAG 2.1 AA intégrée dans chaque pattern
- [ ] Validation script passe: `python src/scripts/validate_skill.py`

### Constraints

- SKILL.md < 5000 tokens (viser ~2500)
- Description YAML ≤ 1024 caractères
- Format "Use when: ... Not for: ..." obligatoire
- Chaque reference < 3000 tokens

### Out of Scope

- Comportement JavaScript/React (délégué à `javascript-react`)
- Support Vue/Svelte (extensible plus tard)
- Bootstrap (Tailwind only)

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 4
- **Estimated LOC**: ~700
- **Risk**: Low (pattern existant à suivre)
- **Justification**: Création de skill suivant un pattern établi, pas de risque architectural

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 4 fichiers à créer |
| `--persona-frontend` | auto | Skill UI/UX |
| `--c7` | auto | Documentation Tailwind |
| `--magic` | auto | Patterns composants |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin
- **Conventions**: kebab-case/SKILL.md, src/skills/
- **Velocity**: 10 features completed

---

## §2 — Implementation Plan

### Impacted Files
| File | Action | Risk |
|------|--------|------|
| src/skills/stack/frontend-editor/SKILL.md | Create | Low |
| src/skills/stack/frontend-editor/references/tailwind-conventions.md | Create | Low |
| src/skills/stack/frontend-editor/references/components-catalog.md | Create | Low |
| src/skills/stack/frontend-editor/references/accessibility.md | Create | Low |

### Tasks
1. [x] **Create skill structure** (5 min)
   - Directory: `src/skills/stack/frontend-editor/`
   - Subdirectory: `references/`

2. [ ] **Write SKILL.md** (45 min)
   - Front matter YAML valide
   - Auto-detection sur tailwind.config.*
   - Component variants (7 types)
   - MCP integration (Magic + Context7)
   - Quick reference table

3. [ ] **Write tailwind-conventions.md** (30 min)
   - Design tokens (colors, spacing, typography)
   - Configuration patterns
   - cn() utility pattern

4. [ ] **Write components-catalog.md** (40 min)
   - Button variants (primary, secondary, success, warning, danger, ghost, outline)
   - Form components (input, select)
   - Card & layout patterns
   - State variants

5. [ ] **Write accessibility.md** (30 min)
   - WCAG 2.1 AA checklist
   - Color contrast requirements
   - Keyboard navigation patterns
   - ARIA patterns

6. [ ] **Validate skill** (10 min)
   - Run: `python src/scripts/validate_skill.py`

### Risks
| Risk | Probability | Mitigation |
|------|-------------|------------|
| Token overflow SKILL.md | Low | Target ~2500 tokens, delegate to refs |
| Incomplete variants | Low | Checklist for all 7 variants |

### Validation
- **@plan-validator**: APPROVED (turbo mode - implicit)

---

## §3 — Implementation & Finalization

### Progress
- [x] Task 1 — Create skill structure
- [x] Task 2 — Write SKILL.md (255 lines, ~1718 tokens)
- [x] Task 3 — Write tailwind-conventions.md (256 lines)
- [x] Task 4 — Write components-catalog.md (286 lines)
- [x] Task 5 — Write accessibility.md (291 lines)
- [x] Task 6 — Validate skill (6/6 checks passed)

### Validation
```bash
$ python src/scripts/validate_skill.py src/skills/stack/frontend-editor/
[OK] Structure: Valid
[OK] YAML syntax: Valid
[OK] Name format: 'frontend-editor' (15 chars)
[OK] Description: 376 chars
[OK] Token count: ~1718 tokens
[OK] References: Checked
RESULT: PASSED (6/6 checks)
```

### Reviews
- **@code-reviewer**: APPROVED_WITH_FIXES (0 Critical, 2 Important auto-fixed, 5 Minor)
- **@security-auditor**: N/A (no security files)
- **@qa-reviewer**: N/A (no tests)

### Auto-fixes Applied
| Issue | File | Fix |
|-------|------|-----|
| Select missing id/htmlFor | components-catalog.md | Added id generation + htmlFor binding |
| Select missing aria-describedby | components-catalog.md | Added aria-invalid + aria-describedby |

### Files Created
| File | Lines | Tokens |
|------|-------|--------|
| `src/skills/stack/frontend-editor/SKILL.md` | 255 | ~1718 |
| `src/skills/stack/frontend-editor/references/tailwind-conventions.md` | 256 | ~1500 |
| `src/skills/stack/frontend-editor/references/components-catalog.md` | 298 | ~1800 |
| `src/skills/stack/frontend-editor/references/accessibility.md` | 291 | ~1800 |
| **Total** | **1100** | **~6818** |

### PR Ready
- Branch: `master` (direct)
- Validation: PASSED
- Lint: N/A (Markdown)
- Docs: Self-documenting skill
