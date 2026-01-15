# Brainstorm Completion Summary Reference

> Reference pour le format de completion du brainstorm (Phase 3, Steps 8-10).

---

## Project Estimation (Step 8)

Calculate total estimated effort from User Stories to determine project category:

```python
# Sum complexity from Must-have stories
total_effort = sum(
    1 if story.complexite == "S" else
    3 if story.complexite == "M" else
    5 for story in must_have_stories
)

# Determine category
if total_effort <= 2:
    category = "TINY"
elif total_effort <= 5:
    category = "SMALL/STANDARD"
else:
    category = "LARGE"
```

---

## Completion Summary Format (Step 10)

Display structured summary with next steps recommendation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BRAINSTORM COMPLETED | EMS: {score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files Generated:
├── Brief: ./docs/briefs/{slug}/brief-{slug}-{date}.md
└── Journal: ./docs/briefs/{slug}/journal-{slug}-{date}.md

📊 Project Estimation:
├── User Stories: {total_count} ({must_count} Must-have, {should_count} Should-have, {could_count} Could-have)
├── Estimated Effort: {total_effort} days ({must_effort}j Must-have + {should_effort}j Should-have)
└── Complexity Category: {TINY|SMALL|STANDARD|LARGE}

🎯 RECOMMENDED NEXT STEPS:

{if category == "TINY"}
  TINY project detected (≤2 days)

  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md
    Claude will route automatically to /quick --autonomous

{else if category == "SMALL/STANDARD" and total_effort <= 5}
  SMALL/STANDARD project ({total_effort} days)

  Option 1 (Recommended): Direct EPCI workflow
  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md

  Option 2: Decompose first (if you want granular tracking)
  → /decompose ./docs/briefs/{slug}/brief-{slug}-{date}.md

{else if category == "LARGE"}
  ⚠️  LARGE project detected ({total_effort} days)

  Recommended: Decompose into manageable sub-specs
  → /decompose ./docs/briefs/{slug}/brief-{slug}-{date}.md
     Breaks down into sub-specs of 1-5 days each
     Generates INDEX.md with dependency graph

  Then, choose execution strategy:

  Option A: Batch execution (recommended for 5+ sub-specs)
  → /orchestrate ./docs/specs/{slug}/
     Automatic DAG-based execution with priority handling

  Option B: Manual execution (for sequential control)
  → /brief @./docs/specs/{slug}/S01-{name}.md
     Execute each sub-spec individually as needed

  Alternative: Direct workflow (not recommended for >10 days)
  → /brief @./docs/briefs/{slug}/brief-{slug}-{date}.md --large
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Session Metrics:
├── Techniques applied: {techniques_list}
├── Duration: ~{duration} min
├── Iterations: {count}
└── Phase transitions: {phase_transitions}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Effort Calculation Examples

| User Stories | Complexity | Calculated Effort | Category | Recommended Command |
|--------------|------------|-------------------|----------|---------------------|
| US1, US2 | S, S | 1 + 1 = 2j | TINY | `/brief` → `/quick --autonomous` |
| US1, US2, US3 | S, M, M | 1 + 3 + 3 = 7j | LARGE | `/decompose` |
| US1, US2 | M, M | 3 + 3 = 6j | LARGE | `/decompose` |
| US1, US2, US3 | S, S, M | 1 + 1 + 3 = 5j | STANDARD | `/brief` (or `/decompose` for tracking) |

---

## Important Notes

- Only Must-have stories count toward MVP effort
- Should-have and Could-have are mentioned but don't trigger LARGE category
- If total effort > 5 days from Must-have alone → Always recommend `/decompose`
- If 3-5 days → Present both options, let user decide
- If ≤2 days → Direct to `/brief` (will auto-route to `/quick`)
