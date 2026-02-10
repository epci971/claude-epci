# Feature: agent-team-implement

## §0 — Metadata

| Champ | Valeur |
|-------|--------|
| Slug | agent-team-implement |
| Complexite | STANDARD |
| Date debut | 2026-02-10 15:00 |
| Branche | feature/agent-team-implement |
| Spec source | docs/briefs/agent-team-implement/brief-agent-team-implement-20260210.md |
| Status | COMPLETED |

## §1 — Contexte & Objectif

### Objectif
Integrer l'orchestration multi-agents dans la commande /implement pour paralleliser la phase Code (C) et Inspect (I). Phase 1 MVP : Code Reviewer en background parallele via subagents, avec detection dynamique des domaines et flags --team/--no-team.

### Contexte technique
- Stack: Plugin EPCI (Markdown skills + Python scripts)
- Mecanisme: Task tool avec run_in_background pour subagents paralleles
- Scope: Phases C+I uniquement, E et P inchangees
- Pattern: Nouveau step-03b-team.md additif (zero modification des steps existants)

### Criteres d'acceptation
- [ ] Feature STANDARD avec >=2 domaines s'execute avec agents paralleles sans intervention manuelle
- [ ] Code Reviewer tourne en parallele du code ou en fin de phase C
- [ ] Features simples (TINY/SMALL) continuent de fonctionner sans changement
- [ ] step-03b-team.md s'integre sans modifier les step files existants
- [ ] Flags --team/--no-team permettent override du seuil auto-detect

## §2 — Plan d'implementation
> Rempli par step-02-plan [P]

### Taches atomiques
| # | Tache | Estimation | Dependances | Status |
|---|-------|-----------|-------------|--------|
| T1 | Create domain-mapping.md reference | 10min | - | PENDING |
| T2 | Create step-03b-team.md skeleton | 15min | - | PENDING |
| T3 | Add --team/--no-team flag parsing | 10min | - | PENDING |
| T4 | Implement domain detection | 15min | T1,T2 | PENDING |
| T5 | Implement team activation breakpoint | 10min | T4 | PENDING |
| T6 | Implement parallel Code Reviewer | 15min | T5 | PENDING |
| T7 | Update step-04-review.md aggregation | 15min | T6 | PENDING |
| T8 | Add parallel Security + QA support | 15min | T6 | PENDING |
| T9 | Update step-04b/04c pre-computed | 10min | T8 | PENDING |
| T10 | Add Agent Teams (TeammateTool) | 15min | T6 | PENDING |
| T11 | Add auto-detect routing | 10min | T10 | PENDING |
| T12 | Update SKILL.md | 15min | All | PENDING |
| T13 | Update feature-document-template.md | 10min | T7 | PENDING |
| T14 | Run validate_skill.py | 5min | T12 | PENDING |

### Strategie de test
- Validation structurelle: `python src/scripts/validate_skill.py src/skills/implement/`
- Frontmatter: Chaine prev_step/next_step integre
- Token limits: steps < 5000, references < 5000
- Cross-references: Tous les @file resolvables

### Phases
| Phase | Tasks | Focus | Est. |
|-------|-------|-------|------|
| 1. Foundation | T1-T3 | Domain mapping, skeleton, flags | 35min |
| 2. Core Team | T4-T7 | Detection + parallel Code Reviewer | 55min |
| 3. Extended Reviews | T8-T9 | Security + QA parallel | 25min |
| 4. Agent Teams | T10-T11 | TeammateTool + auto-routing | 25min |
| 5. Integration | T12-T14 | SKILL.md, template, validation | 30min |

## §3 — Implementation
> Rempli progressivement par step-03-code [C]

### Composants implementes
| Composant | Fichier | Tests | Status |
|-----------|---------|-------|--------|
| Domain mapping reference | references/domain-mapping.md | validate.py PASS | DONE |
| Step-03b-team orchestrator | steps/step-03b-team.md | validate.py PASS | DONE |
| Flag parsing (--team/--no-team) | steps/step-00-init.md | validate.py PASS | DONE |
| Parallel review aggregation | steps/step-04-review.md | validate.py PASS | DONE |
| Security pre-computed results | steps/step-04b-security.md | validate.py PASS | DONE |
| QA pre-computed results | steps/step-04c-qa.md | validate.py PASS | DONE |
| Background reviewer in coding | steps/step-03-code.md | validate.py PASS | DONE |
| SKILL.md workflow update | SKILL.md | validate.py PASS | DONE |
| Feature template team sections | references/feature-document-template.md | validate.py PASS | DONE |
| Step chain update (plan→team→code) | steps/step-02-plan.md, step-03-code.md | validate.py PASS | DONE |

### Deviations du plan
- T4-T6, T8, T10-T11 merged into single step-03b-team.md write (more efficient, same result)

### Coverage
- Validation: PASS (0 errors, 6 warnings — 5 pre-existing + 1 cosmetic)
- Step chain: Verified (step-02 → step-03b → step-03 → step-04)

## §4 — Revue & Validation
> Rempli par step-04-review [I]

### @code-reviewer
- Verdict: APPROVED_WITH_FIXES
- Issues critiques: 0
- Issues importantes: 3 (all resolved)
  1. step-02-plan NEXT STEP TRIGGER text → fixed
  2. Inline domain mapping inconsistency → fixed (removed duplicate, rely on reference)
  3. Duplicate Code Reviewer launch block → fixed (kept only in step-03-code)
- Issues mineures: 5 (cosmetic, acceptable)
- Resume: Implementation architecturally sound, retrocompatible, all brief requirements addressed

### @security-auditor
- N/A - non invoque (no auth/security code modified)

### @qa-reviewer
- N/A - non invoque (Markdown content, no executable code)

## §5 — Finalisation
> Rempli par step-05-document / step-06-finish

### Resume
Added agent team orchestration to /implement skill with step-03b-team.md for multi-domain parallel execution, --team/--no-team flags, parallel Code Reviewer, conditional Security/QA reviewers, and experimental Agent Teams support.

### Fichiers modifies
- src/skills/implement/steps/step-03b-team.md (NEW)
- src/skills/implement/references/domain-mapping.md (NEW)
- src/skills/implement/SKILL.md
- src/skills/implement/steps/step-00-init.md
- src/skills/implement/steps/step-02-plan.md
- src/skills/implement/steps/step-03-code.md
- src/skills/implement/steps/step-04-review.md
- src/skills/implement/steps/step-04b-security.md
- src/skills/implement/steps/step-04c-qa.md
- src/skills/implement/references/feature-document-template.md

### Tests ajoutes : 0
(Markdown content, validation via validate.py: PASS with 0 errors)

### Documentation mise a jour
- SKILL.md: Workflow diagram, step table, decision tree, flags, Team Mode section
- feature-document-template.md: Team Mode sub-section in §3

### Prochaines etapes
- [ ] Commit changes in worktree
- [ ] Merge to master or create PR
- [ ] Deploy (build process)
- [ ] Test on a STANDARD multi-domain feature
