# Phase 1: Planning — Detailed Process

> Reference for `/epci` Phase 1 detailed workflow

---

## Process Steps

**Execute `pre-phase-1` hooks** (if configured)

### Step 1: Read Feature Document

- Read `docs/features/<slug>.md` (created by `/brief` or Step 0.5)
- Verify §1 is complete (if incomplete → error, suggest `/brief` first)
- Extract from §1: identified files, stack, constraints, acceptance criteria
- **Check if native plan exists** in §2 under "Plan Original (Natif)" section

### Step 2: Planning (conditional approach)

**IF native plan exists in §2:**
- Read the native plan from "Plan Original (Natif)" section
- Use it as the high-level base structure
- **Refine** the native plan by:
  - Breaking down high-level tasks into atomic tasks (2-15 min each)
  - Adding specific file references from §1
  - Adding test planning for each atomic task
  - Ordering by dependencies
  - Adding risk assessments
- Update "Plan Raffiné & Validé" section with refined plan

**ELSE (standard workflow):**
- Use the files already identified in §1
- Break down into atomic tasks (2-15 min each)
- Order by dependencies
- Plan a test for each task
- Create new §2 from scratch

### Step 3: Validation (via @plan-validator)

- Submit plan to validator
- If NEEDS_REVISION → correct and resubmit
- If APPROVED → proceed to breakpoint

---

## Output §2 Format

**Use Edit tool** (NOT EnterPlanMode) to update Feature Document.

**Path:** `docs/features/<slug>.md` — **NOT** `~/.claude/plans/`

**Two scenarios:**
- **Scenario A** (Native plan): Update "Plan Raffiné & Validé" section with atomic tasks
- **Scenario B** (Standard): Create complete §2 from scratch

**Required elements:**
- Impacted files list
- Atomic tasks (2-15 min each)
- Dependencies between tasks
- Test plan for each task
- Risk assessment
- @plan-validator verdict

**Templates:** See @references/epci/feature-document-templates.md

---

## Post-Phase Hooks

```bash
python3 hooks/runner.py post-phase-1 --context '{
  "phase": "phase-1",
  "feature_slug": "<slug>",
  "complexity": "<complexity>"
}'
```

---

## Breakpoint BP1

**MANDATORY:** Display breakpoint and WAIT for user confirmation.

**Template:** Use `breakpoint-metrics/templates/bp1-template.md`

**Variables:** Plan, tasks, risks, @plan-validator verdict

**User options:**
- "Continuer" — Proceed to Phase 2
- "Modifier le plan" — Edit plan
- "Voir détails" — Show full details
- "Annuler" — Abort workflow

**Execute `on-breakpoint` hooks** (if configured)

---

*Reference for epci.md Phase 1*
