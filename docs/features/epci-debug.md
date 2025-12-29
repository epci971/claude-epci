# Feature Document — `/epci-debug` Command

> **Slug**: `epci-debug`
> **Category**: STANDARD
> **Date**: 2025-12-29

---

## §1 — Functional Brief

### Context

Création d'une commande de debugging intégrée au workflow EPCI, adaptée de Debuggor v4.11 (Cursor IDE) vers Claude Code. La commande exploite les primitives natives (skills, subagents, MCP, web search) avec un pipeline adaptatif unique qui détermine le mode (Quick/Complet) après la phase de diagnostic.

### Detected Stack

- **Framework**: Claude Code Plugin (EPCI v3.9.5)
- **Language**: Markdown (commands, skills) + Python (hooks, scripts)
- **Patterns**:
  - Command pattern (epci-spike.md template)
  - Skill with references/ (brainstormer pattern)
  - Conditional subagent invocation
  - Hook integration points

### Acceptance Criteria

- [ ] **AC1**: Commande `/epci-debug` créée avec pipeline adaptatif
- [ ] **AC2**: Skill `debugging-strategy` avec 3 fichiers references/
- [ ] **AC3**: Thought tree fonctionnel avec % confidence
- [ ] **AC4**: Scoring solutions 1-100 avec justification
- [ ] **AC5**: Intégration web search automatique
- [ ] **AC6**: Context7 MCP avec fallback gracieux
- [ ] **AC7**: Routing automatique (trivial/quick/complet) post-diagnostic
- [ ] **AC8**: Debug Report généré pour mode Complet
- [ ] **AC9**: Validation scripts passent (validate_skill.py, validate_command.py)

### Constraints

- SKILL.md < 3000 tokens (logique externalisée dans references/)
- Commande < 5000 tokens
- Nommage kebab-case obligatoire
- YAML frontmatter complet requis
- Pas de nouveau subagent (réutiliser @code-reviewer)

### Out of Scope

- Debugging multi-repo
- Intégration IDE (VS Code, Cursor)
- Replay de sessions de debug
- Analyse de logs en temps réel (tail -f)
- Extensions par stack (php-debug, react-debug) → v2

### Evaluation

- **Category**: STANDARD
- **Estimated files**: 6
- **Estimated LOC**: ~800-1000
- **Risk**: Medium (nouvelle intégration MCP/web search)
- **Justification**: 6 fichiers à créer, logique complexe (pipeline adaptatif), intégrations externes (MCP, web)

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think` | auto | 6 fichiers impactés |

### Memory Summary

- **Project**: tools-claude-code-epci
- **Stack**: claude-code-plugin (Python/Markdown)
- **Plugin Version**: 3.9.5
- **Features Completed**: 8
- **Conventions**: kebab-case files, SKILL.md pattern, validate_*.py scripts
- **Patterns**: epci-spike (command template), brainstormer (skill+refs)

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | Est. LOC |
|------|--------|------|----------|
| `build/epci/skills/core/debugging-strategy/SKILL.md` | Create | Low | ~180 |
| `build/epci/skills/core/debugging-strategy/references/thought-tree.md` | Create | Low | ~120 |
| `build/epci/skills/core/debugging-strategy/references/scoring.md` | Create | Low | ~100 |
| `build/epci/skills/core/debugging-strategy/references/thresholds.md` | Create | Low | ~100 |
| `build/epci/commands/epci-debug.md` | Create | Medium | ~350 |
| `docs/debug/` | Create (dir) | Low | — |

**Total estimated**: ~850 LOC across 5 files + 1 directory

### Tasks

1. [ ] **Create skill directory structure** (2 min)
   - Create `build/epci/skills/core/debugging-strategy/`
   - Create `build/epci/skills/core/debugging-strategy/references/`
   - Test: Directories exist

2. [ ] **Create references/thought-tree.md** (10 min)
   - File: `build/epci/skills/core/debugging-strategy/references/thought-tree.md`
   - Content: Format thought tree, confidence %, evidence structure, examples
   - Test: File readable, format documented

3. [ ] **Create references/scoring.md** (10 min)
   - File: `build/epci/skills/core/debugging-strategy/references/scoring.md`
   - Content: Scoring formula (simplicité 30%, risque 25%, temps 20%, maintenabilité 25%)
   - Test: File readable, formula with examples

4. [ ] **Create references/thresholds.md** (10 min)
   - File: `build/epci/skills/core/debugging-strategy/references/thresholds.md`
   - Content: Routing thresholds (trivial/quick/complet), quality gates
   - Test: File readable, thresholds table

5. [ ] **Create SKILL.md** (15 min)
   - File: `build/epci/skills/core/debugging-strategy/SKILL.md`
   - Content: YAML frontmatter + Overview + Reference links + Workflow + MCP fallback + Quick reference
   - Pattern: brainstormer SKILL.md (~180 lines, < 3000 tokens)
   - Test: validate_skill.py passes, references accessible

6. [ ] **Create epci-debug.md command** (15 min)
   - File: `build/epci/commands/epci-debug.md`
   - Content: YAML frontmatter + Overview + Arguments + Process (Diagnostic → Routing → Fix) + Output + Examples
   - Pattern: epci-spike.md structure (~350 lines, < 5000 tokens)
   - Test: validate_command.py passes

7. [ ] **Run validation & integration tests** (5 min)
   - Run: `python3 build/epci/scripts/validate_skill.py build/epci/skills/core/debugging-strategy/`
   - Run: `python3 build/epci/scripts/validate_command.py build/epci/commands/epci-debug.md`
   - Verify: All references linked in SKILL.md exist
   - Verify: MCP fallback documented
   - Test: Both scripts return exit code 0

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Token limit exceeded | Medium | Externalize details to references/, validate with script |
| MCP integration unclear | Low | Document fallback to web search in skill |
| Routing logic complex | Medium | Clear thresholds table in references/thresholds.md |
| Broken reference links | Low | Create references before SKILL.md |

### Validation

- **@plan-validator**: APPROVED (after revision)
  - Completeness: ✓
  - Consistency: ✓ (revised dependency order)
  - Feasibility: ✓
  - Quality: ✓

---

## §3 — Implementation & Finalization

### Progress

- [x] Task 1 — Create skill directory structure
- [x] Task 2 — Create references/thought-tree.md (121 lines)
- [x] Task 3 — Create references/scoring.md (147 lines)
- [x] Task 4 — Create references/thresholds.md (177 lines)
- [x] Task 5 — Create SKILL.md (233 lines)
- [x] Task 6 — Create epci-debug.md command (396 lines)
- [x] Task 7 — Run validation & integration tests

**Total**: 1,074 lines across 5 files

### Tests

```bash
$ python3 src/scripts/validate_skill.py src/skills/core/debugging-strategy/
RESULT: PASSED (6/6 checks)

$ python3 src/scripts/validate_command.py src/commands/epci-debug.md
RESULT: PASSED (5/5 checks)
```

### Reviews

- **@code-reviewer**: APPROVED_WITH_FIXES (3 Minor issues fixed)
  - Fixed: Formula × → * for compatibility
  - Fixed: Stack skills reference clarified
- **@security-auditor**: N/A (no security-sensitive files)
- **@qa-reviewer**: N/A (documentation only)

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| Location | `src/` instead of `build/` | User correction, follows conventions.json |
| LOC | 1,074 vs ~850 estimated | Reference files more detailed (+27%) |

### Commit Message (Prepared)

```
feat(debug): add /epci-debug command with debugging-strategy skill

- Create debugging-strategy skill with thought tree analysis
- Add solution scoring framework (simplicity, risk, time, maintainability)
- Implement adaptive routing (trivial/quick/complet modes)
- Include 3 reference docs: thought-tree, scoring, thresholds
- Support Context7 MCP with web search fallback

Refs: docs/features/epci-debug.md
```

### Documentation

- Feature Document: `docs/features/epci-debug.md`
- Brief: `docs/briefs/epci-debug/brief-epci-debug-2025-12-29.md`
- Journal: `docs/briefs/epci-debug/journal-epci-debug-2025-12-29.md`

### PR Ready

- Branch: `master` (direct commit)
- Tests: ✅ Validations passed
- Lint: ✅ YAML valid
- Docs: ✅ Feature Document complete
- Commit: ⏸️ Pending (manual commit requested)
