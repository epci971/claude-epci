# Feature Document — Brainstorm v4.2 S01 Core

## §1 — Functional Brief

### Context

Le brainstormer EPCI v4.1 necessite des ameliorations pour gerer les sessions longues et
ameliorer l'experience utilisateur:
- **Pas de persistence** : Sessions perdues si interruption
- **Navigation limitee** : Impossible de revenir en arriere
- **Fatigue cognitive** : Pas de checkpoints pour gerer l'energie
- **Format questions** : Une question a la fois peut etre lent

### Objective

Implementer les fondations v4.2:
1. **Session continuation** : Sauvegarder/reprendre les sessions brainstorm
2. **Navigation back** : Revenir a l'iteration precedente
3. **Energy checkpoints** : Points de controle pour gerer la fatigue
4. **Format 3-5 questions** : Plusieurs questions par iteration avec A/B/C
5. **Confirmation agents** : Prompt [Y/n] avant @planner/@security

### Source Specifications

- **Spec file**: `docs/briefs/brainstorm-v4/specs/S01-core.md`
- **Brief file**: `docs/briefs/brainstorm-v4/brief-brainstorm-v4.2-2026-01-06.md`

### Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC1 | Session save/restore | Save session, close, resume → state identical |
| AC2 | Auto-detect session | Launch /brainstorm with existing session → resume prompt |
| AC3 | Back command | Execute back → EMS and questions from previous iteration |
| AC4 | Energy check at EMS 50 | Reach EMS 50 → checkpoint displayed |
| AC5 | Energy check at EMS 75 | Reach EMS 75 → checkpoint displayed |
| AC6 | Format 3-5 questions | Each iteration shows 3-5 questions with A/B/C |
| AC7 | Confirmation @planner | EMS >=70 → confirmation prompt before launch |
| AC8 | Valid session YAML | Generated .yaml file conforms to documented format |

### Files Identified

| File | Action | Description |
|------|--------|-------------|
| `src/commands/brainstorm.md` | Modify | Add commands, format, session logic |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Reference session-format.md, update instructions |
| `src/skills/core/brainstormer/references/session-format.md` | Create | Document session YAML format |

### Constraints

- Ne pas casser la retrocompatibilite v4.1
- Sessions stockees dans `.project-memory/brainstorm-sessions/`
- Format YAML pour les sessions (lisibilite)
- Commande `back` limitee a 1 step (simplicite)

### Complexity

**Category**: STANDARD
**Estimated effort**: 4.5 days
**Files**: 3 (2 modifications, 1 creation)

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | LOC Est. |
|------|--------|------|----------|
| `src/skills/core/brainstormer/references/session-format.md` | Create | Low | ~100 |
| `src/commands/brainstorm.md` | Modify | Medium | ~200 |
| `src/skills/core/brainstormer/SKILL.md` | Modify | Low | ~50 |

### Tasks

1. [ ] **Create session-format.md** (15 min)
   - File: `src/skills/core/brainstormer/references/session-format.md`
   - Document YAML structure for sessions
   - Include examples and field descriptions

2. [ ] **Add session commands to brainstorm.md** (20 min)
   - Add `save` command with session serialization logic
   - Add auto-detect session logic at startup
   - Add resume prompt "[1] Reprendre [2] Nouvelle"
   - Define storage path `.project-memory/brainstorm-sessions/`

3. [ ] **Implement back command** (15 min)
   - Add `back` command to brainstorm.md
   - Implement state restoration (EMS, questions, phase)
   - Use session history for rollback
   - Limit to 1 step back

4. [ ] **Implement energy checkpoints** (20 min)
   - Define 4 triggers in brainstorm.md:
     - EMS reaches 50
     - EMS reaches 75
     - Iteration >= 7 without user command
     - Phase change Divergent → Convergent
   - Implement hybrid format (CLI + human)
   - Add `energy` command for forced check

5. [ ] **Implement 3-5 questions format** (25 min)
   - Modify breakpoint format in brainstorm.md
   - Update question generation logic
   - Keep A/B/C format with suggestions
   - Adapt iteration logic for batch questions

6. [ ] **Implement agent confirmation** (10 min)
   - Modify @planner trigger (EMS >=70) for confirmation
   - Modify @security-auditor trigger for confirmation
   - Format: `Lancer @planner? [Y/n]`

7. [ ] **Update SKILL.md references** (10 min)
   - Add reference to session-format.md
   - Update command list
   - Add session section

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking v4.1 compatibility | Low | High | Careful command additions, no removals |
| Session format evolution | Medium | Medium | Document format version in YAML |
| Complex state restoration | Low | Medium | Simple 1-step back, history array |

### Validation

- **@plan-validator**: APPROVED
  - Completeness: OK - All 8 acceptance criteria covered
  - Consistency: OK - Task ordering respects dependencies
  - Feasibility: OK - Risks identified with mitigations
  - Quality: OK - Tasks atomic, descriptions clear

**Recommendations integrated**:
1. Add `format_version: "1.0"` in session YAML schema
2. Reconcile One-at-a-Time vs 3-5 questions documentation
3. Ensure `energy` command added to commands table

---

## §3 — Implementation & Finalization

### Progress

- [x] Task 1 — Create session-format.md
- [x] Task 2 — Add session commands to brainstorm.md
- [x] Task 3 — Implement back command
- [x] Task 4 — Implement energy checkpoints
- [x] Task 5 — Implement 3-5 questions format
- [x] Task 6 — Implement agent confirmation
- [x] Task 7 — Update SKILL.md references

### Files Modified

| File | Action | Lines Changed |
|------|--------|---------------|
| `src/skills/core/brainstormer/references/session-format.md` | Created | ~150 |
| `src/commands/brainstorm.md` | Modified | ~200 |
| `src/skills/core/brainstormer/SKILL.md` | Modified | ~50 |

### Reviews

- **@code-reviewer**: APPROVED after fixes
  - Fixed: Question format contradiction (line 131)
  - Fixed: Section-by-Section version label
  - Fixed: Breakpoint format in SKILL.md

### Deviations

| Task | Deviation | Justification |
|------|-----------|---------------|
| - | None | Implementation matches plan |

### Additional Changes (by external modification)

- `technique [x]` command added (S02 scope, pre-integrated)
- Techniques reference section added to SKILL.md

### Documentation

- **Feature Document**: Updated with implementation details
- **session-format.md**: Complete YAML schema documentation
- **brainstorm.md**: v4.2 commands and features documented
- **SKILL.md**: References and commands updated

### PR Ready

- Branch: `feature/brainstorm-v42-s01-core`
- Files: 3 modified/created
- Tests: N/A (documentation-only changes)
- Docs: Up to date
