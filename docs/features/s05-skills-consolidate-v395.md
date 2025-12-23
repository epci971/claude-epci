# Feature Document — S05: Skills Consolidation + Version 3.9.5

> **Slug**: `s05-skills-consolidate-v395`
> **Category**: STANDARD
> **Date**: 2025-12-23

---

## §1 — Functional Brief

### Context
This feature consolidates the `project-memory-loader` skill into `project-memory` to eliminate redundancy and confusion. Additionally, it aligns all version numbers across the codebase to v3.9.5.

Currently:
- Two skills exist: `project-memory` (manager) and `project-memory-loader` (loader)
- Version inconsistencies: plugin.json (3.9.1), README.md (3.8), hooks/README.md (v3.7)

### Detected Stack
- **Framework**: Claude Code Plugin
- **Language**: Python3, Markdown
- **Patterns**: YAML frontmatter, kebab-case files

### Memory Summary
- Project: tools-claude-code-epci
- Plugin version target: 3.9.5
- Skills count: 20 → 19 after consolidation

### Identified Files

| File | Action | Risk |
|------|--------|------|
| `src/skills/core/project-memory/SKILL.md` | Modify (merge) | High |
| `src/skills/core/project-memory-loader/` | Delete | Medium |
| `src/commands/epci-brief.md` | Modify | Low |
| `src/commands/epci.md` | Modify | Low |
| `src/commands/epci-quick.md` | Modify | Low |
| `src/commands/epci-spike.md` | Modify | Low |
| `src/commands/brainstorm.md` | Modify | Low |
| `src/commands/epci-decompose.md` | Modify | Low |
| `src/.claude-plugin/plugin.json` | Modify | Medium |
| `src/README.md` | Modify | Low |
| `src/hooks/README.md` | Modify | Low |
| `CLAUDE.md` | Modify | Low |

### Acceptance Criteria
- [ ] S05-AC1: Single `project-memory` skill exists with merged capabilities
- [ ] S05-AC2: `project-memory-loader/` directory deleted
- [ ] S05-AC3: All 6 commands reference `project-memory` (not loader)
- [ ] S05-AC4: plugin.json version = 3.9.5, skill removed
- [ ] S05-AC5: src/README.md version = 3.9.5
- [ ] S05-AC6: src/hooks/README.md version = 3.9.5
- [ ] S05-AC7: CLAUDE.md skill count updated (20 → 19)
- [ ] S05-AC8: `grep -r "project-memory-loader" src/` returns 0 results

### Constraints
- Must preserve all functionality from both skills
- Must not break existing workflows

### Out of Scope
- Skill caching implementation
- Lazy-load skills implementation
- Changes to other skills

### Evaluation
- **Category**: STANDARD
- **Estimated files**: 12
- **Estimated LOC**: ~400
- **Risk**: Medium
- **Justification**: Multi-file refactoring with skill deletion

### Suggested Flags

| Flag | Source | Reason |
|------|--------|--------|
| `--think-hard` | auto | 12 files impacted |

---

## §2 — Implementation Plan

### Impacted Files

| File | Action | Risk | LOC Est. |
|------|--------|------|----------|
| `src/skills/core/project-memory/SKILL.md` | Modify (merge) | High | +150 |
| `src/skills/core/project-memory-loader/` | Delete | Medium | -257 |
| `src/commands/epci-brief.md` | Modify | Low | ~3 |
| `src/commands/epci.md` | Modify | Low | ~3 |
| `src/commands/epci-quick.md` | Modify | Low | ~3 |
| `src/commands/epci-spike.md` | Modify | Low | ~3 |
| `src/commands/brainstorm.md` | Modify | Low | ~3 |
| `src/commands/epci-decompose.md` | Modify | Low | ~3 |
| `src/.claude-plugin/plugin.json` | Modify | Medium | ~3 |
| `src/README.md` | Modify | Low | ~2 |
| `src/hooks/README.md` | Modify | Low | ~2 |
| `CLAUDE.md` | Modify | Low | ~5 |

### Tasks

1. [ ] **Merge project-memory-loader into project-memory** (15 min)
   - Add "When to Load" section from loader
   - Add "Loading Process" section from loader
   - Add "Context Application Matrix" from loader
   - Add "Memory Status Display" from loader
   - Add "Error Handling" section from loader
   - Update description in frontmatter to include loading capability
   - Add `allowed-tools: [Read, Glob, Write]`

2. [ ] **Update epci-brief.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

3. [ ] **Update epci.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

4. [ ] **Update epci-quick.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

5. [ ] **Update epci-spike.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

6. [ ] **Update brainstorm.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

7. [ ] **Update epci-decompose.md** (3 min)
   - Replace `project-memory-loader` → `project-memory` in Skills list

8. [ ] **Update plugin.json** (5 min)
   - Remove `"./skills/core/project-memory-loader/SKILL.md"` from skills array
   - Update version: `"3.9.1"` → `"3.9.5"`

9. [ ] **Update src/README.md version** (2 min)
   - Change header: `# EPCI Plugin v3.8` → `# EPCI Plugin v3.9.5`

10. [ ] **Update src/hooks/README.md version** (2 min)
    - Change header: `> **Version**: 1.1.0 (EPCI v3.7)` → `> **Version**: 1.2.0 (EPCI v3.9.5)`

11. [ ] **Update CLAUDE.md** (5 min)
    - Update skill count references (20 → 19)
    - Update version references if present

12. [ ] **Pre-deletion verification** (3 min)
    - Run `grep -r "project-memory-loader" src/` → expect only SKILL.md result
    - Verify all command references updated

13. [ ] **Delete project-memory-loader directory** (2 min)
    - Remove `src/skills/core/project-memory-loader/` directory

14. [ ] **Post-deletion verification** (2 min)
    - Run `grep -r "project-memory-loader" src/` → expect 0 results
    - Verify skill count in plugin.json = 19

### Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Lost functionality during merge | Medium | Preserve all loader sections in merged skill |
| Broken references to old skill | Medium | grep verification after deletion |
| Claude Code not finding merged skill | Low | Test with `/epci-brief` after changes |

### Validation
- **@plan-validator**: APPROVED (after revision of skill count 20→19 and task ordering)

---

## §3 — Implementation & Finalization

### Progress
- [x] Task 1 — Merge project-memory-loader into project-memory
- [x] Task 2 — Update epci-brief.md
- [x] Task 3 — Update epci.md
- [x] Task 4 — Update epci-quick.md
- [x] Task 5 — Update epci-spike.md
- [x] Task 6 — Update brainstorm.md
- [x] Task 7 — Update epci-decompose.md
- [x] Task 8 — Update plugin.json (version + remove skill)
- [x] Task 9 — Update src/README.md version
- [x] Task 10 — Update src/hooks/README.md version
- [x] Task 11 — Update CLAUDE.md skill count
- [x] Task 12 — Pre-deletion verification (found 3 extra references, fixed)
- [x] Task 13 — Delete project-memory-loader directory
- [x] Task 14 — Post-deletion verification

### Verification Results
```bash
$ grep -r "project-memory-loader" src/
✅ No references found

$ plugin.json skills count
Skills count: 19
```

### Files Modified
| File | Changes |
|------|---------|
| `src/skills/core/project-memory/SKILL.md` | +170 LOC (merged loader content) |
| `src/commands/epci-brief.md` | Replaced loader → memory |
| `src/commands/epci.md` | Replaced loader → memory (3 occurrences) |
| `src/commands/epci-quick.md` | Replaced loader → memory (2 occurrences) |
| `src/commands/epci-spike.md` | Replaced loader → memory (2 occurrences) |
| `src/commands/brainstorm.md` | Replaced loader → memory |
| `src/commands/epci-decompose.md` | Replaced loader → memory |
| `src/.claude-plugin/plugin.json` | Version 3.9.1→3.9.5, removed loader skill |
| `src/README.md` | Version 3.8→3.9.5, removed loader references |
| `src/hooks/README.md` | Version 1.1.0 (v3.7)→1.2.0 (v3.9.5) |
| `CLAUDE.md` | Skills count 14→19 |
| `src/skills/core/brainstormer/SKILL.md` | Fixed loader reference |

### Reviews
- **@code-reviewer**: APPROVED
  - Merger complete and well-structured
  - All 19 skills properly listed in plugin.json
  - Version consistency verified (3.9.5)
  - No references to project-memory-loader in src/
  - Legacy references in docs/archive are acceptable (historical)

### Commit
```
5a30630 feat(skills): consolidate project-memory skills + version 3.9.5

S05 Skills Consolidation implementation:
- Merge project-memory-loader skill into project-memory
- Delete project-memory-loader directory (20 → 19 skills)
- Update all commands to reference project-memory
- Align versions to v3.9.5 across plugin.json, README.md, hooks/README.md
- Update CLAUDE.md skill count (14 → 19)
- Update brainstormer skill reference
- Add Feature Document for S05

Refs: docs/features/s05-skills-consolidate-v395.md
```

### PR Ready
- Branch: `master`
- Tests: ✅ Grep verification passed (0 references to project-memory-loader)
- Skill count: ✅ 19 skills in plugin.json
- Docs: ✅ Feature Document complete
