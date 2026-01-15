# Workflow Chain Guide — Brainstorm → Decompose → Orchestrate

> **Version**: 1.0 | **Date**: Janvier 2025

## Overview

This guide explains the complete workflow chain for transforming vague ideas into executable specifications using the EPCI brainstorm, decompose, and orchestrate commands.

**Problem solved**: Users with vague ideas often don't know which EPCI command to start with and how to chain them effectively.

**Solution**: A guided workflow with automatic recommendations based on project size estimation.

---

## Visual Workflow Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         ENTRY POINTS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Vague Idea]    [Clear Brief]    [Structured PRD]            │
│       │               │                  │                      │
│       v               v                  v                      │
│  /brainstorm      /brief            /decompose                 │
│       │               │                  │                      │
└───────┼───────────────┼──────────────────┼──────────────────────┘
        │               │                  │
        v               │                  │
   [Brief.md]           │                  │
   + User Stories       │                  │
   + Complexité S/M/L   │                  │
        │               │                  │
        v               │                  │
   [Effort Calc]        │                  │
   Sum Must-have        │                  │
        │               │                  │
    ┌───┴───┬───────────┼──────────────────┘
    │       │           │
    v       v           v
  ≤2j    3-5j         >5j
 (TINY) (STD)       (LARGE)
    │       │           │
    │       │           v
    │       │      /decompose
    │       │           │
    │       │           v
    │       │      [INDEX.md]
    │       │      + S01-SNN.md
    │       │      + Dependencies
    │       │           │
    │       │       ┌───┴────┐
    │       │       v        v
    │       v   /orchestrate  Manual
    v      /brief    │       /brief @S01
  /brief      │      │            │
    │         │      v            │
    v         v   [Batch          │
 /quick   /quick   DAG Exec]      │
--autonomous  or                  │
              /epci                v
                              Sequential
                              Execution
```

---

## Decision Tree

### Step 1: Choose Entry Point

| You have... | Use... | Why |
|-------------|--------|-----|
| **Vague idea**, unclear scope | `/brainstorm` | Needs clarification, exploration, personas |
| **Clear brief**, know what to build | `/brief` | Direct to implementation workflow |
| **Structured PRD/CDC**, multi-phase | `/decompose` | Already structured, needs breakdown |
| **Native Claude Code plan** | `/epci --from-native-plan` | Reuse existing high-level plan |

### Step 2: Post-Brainstorm Decision

After `/brainstorm` completes, the command calculates effort:

```
Effort = Σ (Complexity of Must-have User Stories)

Where:
  S (Small)  = 1 day
  M (Medium) = 3 days
  L (Large)  = 5 days
```

**Automatic Recommendation:**

| Total Effort | Category | Recommended | Alternative |
|--------------|----------|-------------|-------------|
| ≤ 2 days | TINY | `/brief` → `/quick --autonomous` | None |
| 3-5 days | STANDARD | `/brief` → `/quick` or `/epci` | `/decompose` (for granular tracking) |
| > 5 days | LARGE | `/decompose` → `/orchestrate` | `/brief --large` (not recommended) |

### Step 3: Post-Decompose Decision

After `/decompose` generates sub-specs:

| Sub-specs Count | Recommended | Why |
|-----------------|-------------|-----|
| 1-3 specs | Manual `/brief @S0X` | Low overhead, full control |
| 4-9 specs | `/orchestrate` or Manual | User choice based on complexity |
| 10+ specs | `/orchestrate` | Batch execution with DAG saves time |

---

## Real-World Examples

### Example 1: TINY Project (≤2 days)

**Scenario**: Add a "Mark as favorite" button to existing product cards.

**User Flow:**

```bash
# Step 1: Brainstorm
$ /brainstorm "ajouter bouton favori sur cards produits"

# Brainstorm generates:
# - Brief with 2 User Stories (US1: S, US2: S)
# - Calculation: 1 + 1 = 2 days
# - Category: TINY

# Completion Summary shows:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BRAINSTORM COMPLETED | EMS: 82/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Project Estimation:
├── User Stories: 2 (2 Must-have)
├── Estimated Effort: 2 days
└── Complexity Category: TINY

🎯 RECOMMENDED NEXT STEPS:

  TINY project detected (≤2 days)

  → /brief @./docs/briefs/favori-cards/brief-favori-2025-01-12.md
    Claude will route automatically to /quick --autonomous
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Step 2: Execute recommended command
$ /brief @./docs/briefs/favori-cards/brief-favori-2025-01-12.md

# Brief automatically routes to /quick --autonomous
# → Explore, Plan, Code, Test, Commit (autonomous)
```

**Key takeaway**: TINY projects go straight from brainstorm → brief → quick (fully autonomous).

---

### Example 2: STANDARD Project (3-5 days)

**Scenario**: Add real-time notifications system with WebSocket and email fallback.

**User Flow:**

```bash
# Step 1: Brainstorm
$ /brainstorm "système notifications temps réel avec websocket et email fallback"

# Brainstorm generates:
# - Brief with 3 User Stories:
#   US1: WebSocket connection (M = 3j)
#   US2: Email fallback (S = 1j)
#   US3: Admin panel (S = 1j)
# - Calculation: 3 + 1 + 1 = 5 days
# - Category: STANDARD

# Completion Summary shows:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BRAINSTORM COMPLETED | EMS: 88/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Project Estimation:
├── User Stories: 3 (3 Must-have)
├── Estimated Effort: 5 days
└── Complexity Category: STANDARD

🎯 RECOMMENDED NEXT STEPS:

  STANDARD project (5 days)

  Option 1 (Recommended): Direct EPCI workflow
  → /brief @./docs/briefs/notif-temps-reel/brief-notif-2025-01-12.md

  Option 2: Decompose first (if you want granular tracking)
  → /decompose ./docs/briefs/notif-temps-reel/brief-notif-2025-01-12.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Step 2: Choose option (user decides)
# Most users choose Option 1 for 5-day projects

$ /brief @./docs/briefs/notif-temps-reel/brief-notif-2025-01-12.md

# Brief routes to /epci (3 phases)
# → Phase 1: Plan (2-15 min granularity, tests, validation)
# → Phase 2: Code (TDD, @code-reviewer)
# → Phase 3: Finalize (docs, commit)
```

**Key takeaway**: STANDARD projects (3-5 days) offer choice between direct `/epci` or `/decompose` for granular tracking.

---

### Example 3: LARGE Project (>5 days)

**Scenario**: Migrate entire Django app from monolith to microservices architecture.

**User Flow:**

```bash
# Step 1: Brainstorm
$ /brainstorm "migration architecture django monolithe vers microservices"

# Brainstorm generates:
# - Brief with 6 User Stories:
#   US1: Service extraction (L = 5j)
#   US2: API Gateway (M = 3j)
#   US3: Database split (L = 5j)
#   US4: Auth microservice (M = 3j)
#   US5: Migration ETL (M = 3j)
#   US6: Testing & docs (M = 3j)
# - Calculation: 5 + 3 + 5 + 3 + 3 + 3 = 22 days
# - Category: LARGE

# Completion Summary shows:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BRAINSTORM COMPLETED | EMS: 91/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Project Estimation:
├── User Stories: 6 (6 Must-have, 2 Should-have)
├── Estimated Effort: 22 days (Must-have only)
└── Complexity Category: LARGE

🎯 RECOMMENDED NEXT STEPS:

  ⚠️  LARGE project detected (22 days)

  Recommended: Decompose into manageable sub-specs
  → /decompose ./docs/briefs/migration-microservices/brief-migration-2025-01-12.md
     Breaks down into sub-specs of 1-5 days each
     Generates INDEX.md with dependency graph

  Then, choose execution strategy:

  Option A: Batch execution (recommended for 5+ sub-specs)
  → /orchestrate ./docs/specs/migration-microservices/
     Automatic DAG-based execution with priority handling

  Option B: Manual execution (for sequential control)
  → /brief @./docs/specs/migration-microservices/S01-{name}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Step 2: Decompose (mandatory for LARGE)
$ /decompose ./docs/briefs/migration-microservices/brief-migration-2025-01-12.md

# Decompose auto-detects brainstorm format:
# - Identifies "### US1 —" headers
# - Maps Complexité: S→1j, M→3j, L→5j
# - Maps Priorité: Must-have→1, Should-have→2
# - Infers dependencies from AC references

# Generates:
# ./docs/specs/migration-microservices/
# ├── INDEX.md (overview + Mermaid graphs)
# ├── S01-service-extraction.md (5j)
# ├── S02-api-gateway.md (3j, depends on S01)
# ├── S03-database-split.md (5j, depends on S01)
# ├── S04-auth-microservice.md (3j, depends on S02)
# ├── S05-migration-etl.md (3j, depends on S03)
# └── S06-testing-docs.md (3j, depends on S04, S05)

# Step 3: Execute (choose strategy)

# Option A: Batch execution (recommended)
$ /orchestrate ./docs/specs/migration-microservices/

# Orchestrate:
# - Analyzes dependency DAG
# - Identifies parallel opportunities:
#   - S02 and S03 can run parallel after S01
# - Auto-priority based on MoSCoW
# - Auto-retry on failure
# - Generates execution report

# Option B: Manual execution
$ /brief @./docs/specs/migration-microservices/S01-service-extraction.md
# ... wait for completion ...
$ /brief @./docs/specs/migration-microservices/S02-api-gateway.md
$ /brief @./docs/specs/migration-microservices/S03-database-split.md
# ... continue sequentially ...
```

**Key takeaway**: LARGE projects (>5 days) **must** use `/decompose` → `/orchestrate` for manageability.

---

## Workflow Comparison Table

| Workflow | Entry | Intermediate | Output | Duration | Best For |
|----------|-------|--------------|--------|----------|----------|
| **A (Standard)** | `/brief` | → `/quick` or `/epci` | Feature Document §1-3 | Direct | Clear brief, known scope |
| **B (Plan natif)** | `/epci --from-native-plan` | → Phase 1-3 | Feature Document §1-3 | 2-15 min planning + impl | Existing native plan |
| **D (Brainstorm TINY)** | `/brainstorm` → `/brief` | → `/quick --autonomous` | Inline brief + code | ~20-45 min + 30 min | Vague idea, simple feature |
| **E (Brainstorm STANDARD)** | `/brainstorm` → `/brief` | → `/quick` or `/epci` | Feature Document §1-3 | ~45-90 min + impl | Vague idea, medium feature |
| **F (Brainstorm LARGE)** | `/brainstorm` → `/decompose` | → `/orchestrate` or manual | INDEX + S01-SNN specs | ~60-120 min + batch | Vague idea, complex project |

---

## Common Questions

### Q1: When should I use `/decompose` instead of going straight to `/brief`?

**A:** Use `/decompose` when:
- Total estimated effort > 5 days (LARGE category)
- You have 5+ User Stories in Must-have
- You want granular tracking and parallel execution
- Project has clear phases with dependencies

**Skip `/decompose` when:**
- Total effort ≤ 5 days (TINY/STANDARD)
- Only 1-3 User Stories
- Project is simple and linear

### Q2: Can I use `/decompose` on a PRD that didn't come from `/brainstorm`?

**A:** Yes! `/decompose` auto-detects two formats:
1. **Brainstorm Brief**: `### US1 —` headers with `**Complexité**` and `**Priorité**`
2. **Standard PRD/CDC**: `## Phase X`, `### Step X.Y` headers

If your PRD has structured sections, `/decompose` will work.

### Q3: Is `/orchestrate` always recommended after `/decompose`?

**A:** No, it depends on sub-spec count:
- **1-3 sub-specs**: Manual `/brief @S0X` is fine (low overhead)
- **4-9 sub-specs**: User choice (orchestrate vs manual)
- **10+ sub-specs**: `/orchestrate` highly recommended (saves time, handles dependencies)

### Q4: What if I want to change the decomposition before execution?

**A:** `/decompose` shows a validation breakpoint before generating files:

```
⏸️  BREAKPOINT — VALIDATION DÉCOUPAGE

📋 DÉCOUPAGE PROPOSÉ: 6 sous-specs

| ID  | Title | Effort | Dependencies |
|-----|-------|--------|--------------|
| ... | ...   | ...    | ...          |

Options:
  [1] Valider → Générer les fichiers
  [2] Modifier → Ajuster le découpage
  [3] Annuler → Abandonner
```

Choose **[2] Modifier** to adjust before file generation.

### Q5: Can I pause and resume during `/orchestrate`?

**A:** Yes! `/orchestrate` saves state. If interrupted:
- Resume with: `/orchestrate ./docs/specs/{slug}/ --continue`
- View status: `/orchestrate ./docs/specs/{slug}/ --status`
- Retry failed: `/orchestrate ./docs/specs/{slug}/ --retry-failed`

---

## Integration with Project Memory

The workflow chain integrates with `.project-memory/` for learning:

**After `/brainstorm`:**
- Hook `post-brainstorm` saves:
  - Techniques applied
  - EMS scores
  - Duration, iterations
  - User Stories count and complexity

**After `/decompose`:**
- No dedicated hook (inherits from `/brief` or `/orchestrate`)

**After `/brief` on each sub-spec:**
- Hook `post-phase-3` saves:
  - Feature completed
  - Actual time vs estimated
  - Files modified
  - Commit status

**Learning over time:**
- Velocity calibration: Average actual time / estimated time
- Complexity patterns: S/M/L accuracy improves
- Stack-specific estimates: PHP projects vs React projects

---

## Troubleshooting

### Issue: `/decompose` doesn't detect my brainstorm brief

**Symptoms**: Error "No structure detected" or "PRD without clear structure"

**Causes:**
- User Stories missing `### US1 —` headers
- Complexité field missing or wrong format
- Brief generated with old template

**Solution:**
1. Check brief has `### USX — Title` format
2. Check `**Complexité**: S/M/L` exists for each story
3. Re-run `/brainstorm` if template is old (< v2.0)

### Issue: Effort calculation seems wrong

**Symptoms**: 3-day project marked as TINY, or 8-day marked as STANDARD

**Causes:**
- Only Must-have stories count toward calculation
- Should-have/Could-have are excluded

**Solution:**
- Review which stories are marked `**Priorité**: Must-have`
- Adjust priorities if MVP scope is wrong
- Re-run `/brainstorm` with correct prioritization

### Issue: `/orchestrate` runs sub-specs in wrong order

**Symptoms**: S03 executes before S01, causing errors

**Causes:**
- Dependency graph incorrect in INDEX.md
- Circular dependency not caught

**Solution:**
1. Check INDEX.md dependency graph
2. Run `/decompose` validation again
3. Manually edit INDEX.md dependencies if needed
4. Rerun `/orchestrate --continue`

---

## Cheat Sheet

```bash
# Vague idea → TINY project (≤2j)
/brainstorm "idea"
/brief @./docs/briefs/{slug}/brief-{slug}-{date}.md
# → Auto-routes to /quick --autonomous

# Vague idea → STANDARD project (3-5j)
/brainstorm "idea"
/brief @./docs/briefs/{slug}/brief-{slug}-{date}.md
# → Routes to /quick or /epci

# Vague idea → LARGE project (>5j)
/brainstorm "idea"
/decompose ./docs/briefs/{slug}/brief-{slug}-{date}.md
/orchestrate ./docs/specs/{slug}/
# → Batch DAG execution

# Clear brief → Direct execution
/brief "clear description"
# → Routes automatically based on complexity

# Existing PRD → Decompose
/decompose ./docs/prd/migration-plan.md
/orchestrate ./docs/specs/{slug}/

# Native plan → Refine
/epci --from-native-plan ~/.claude/plans/plan.md --slug {name}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-12 | Initial guide with examples and decision tree |

---

*This guide is part of the EPCI Plugin v4.9+ brainstormer skill.*
*For technical details, see: `src/commands/brainstorm.md`, `src/commands/decompose.md`, `src/commands/orchestrate.md`*
