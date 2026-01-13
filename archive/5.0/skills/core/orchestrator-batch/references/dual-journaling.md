# Dual Journaling

## Overview

The orchestrator maintains two journal formats:
- **Markdown** for human readability
- **JSON** for tooling and automation

Both are updated in real-time during execution.

## Markdown Journal

**File**: `{specs-dir}/orchestration-journal.md`

```markdown
# Orchestration Journal — 2026-01-09T22:15:00

## Configuration
- Source: ./docs/specs/my-project/
- Specs: 5 (S01, S02, S03, S04, S05)
- Mode: sequential
- Max retries: 3

---

## S01-core
- Started: 22:15:00
- Routing: /epci (STANDARD)
- Phase 1: OK 3min
- Phase 2: OK 12min (1 retry - test fix)
- Phase 3: OK 2min
- Commit: abc1234 "feat(core): implement session logic"
- Duration: 17min
- Status: SUCCESS

## S02-techniques
- Started: 22:32:00
- Routing: /quick (SMALL)
- EPCT: OK 8min
- Commit: def5678 "feat(techniques): add library"
- Duration: 8min
- Status: SUCCESS

## S03-integration
- Started: 22:40:00
- Routing: /epci (STANDARD)
- Phase 1: OK 2min
- Phase 2: FAILED
- Retry 1/3: FAILED
- Retry 2/3: FAILED
- Retry 3/3: FAILED
- Duration: 25min
- Status: FAILED
- Error: Integration test timeout

## S04-dependent
- Status: SKIPPED
- Reason: Depends on failed S03

## S05-independent
- Started: 23:05:00
- Routing: /quick (TINY)
- EPCT: OK 5min
- Commit: ghi9012 "fix(config): update defaults"
- Duration: 5min
- Status: SUCCESS

---

## Summary
- Total: 5 specs
- Succeeded: 3 (60%)
- Failed: 1 (20%)
- Skipped: 1 (20%)
- Duration: 55min
- Commits: 3
- Retries used: 4
```

## JSON Journal

**File**: `{specs-dir}/orchestration-journal.json`

```json
{
  "orchestration_id": "orch-2026-01-09-221500",
  "started_at": "2026-01-09T22:15:00Z",
  "completed_at": "2026-01-09T23:10:00Z",
  "source_dir": "./docs/specs/my-project/",
  "config": {
    "mode": "sequential",
    "max_retries": 3,
    "auto_commit": true
  },
  "specs": [
    {
      "id": "S01",
      "title": "Core logic",
      "started_at": "2026-01-09T22:15:00Z",
      "completed_at": "2026-01-09T22:32:00Z",
      "routing": "epci",
      "complexity": "STANDARD",
      "phases": {
        "phase1": {"status": "success", "duration_sec": 180},
        "phase2": {"status": "success", "duration_sec": 720, "retries": 1},
        "phase3": {"status": "success", "duration_sec": 120}
      },
      "commit": {
        "sha": "abc1234",
        "message": "feat(core): implement session logic"
      },
      "duration_sec": 1020,
      "status": "success",
      "retries": 1
    }
  ],
  "summary": {
    "total_specs": 5,
    "succeeded": 3,
    "failed": 1,
    "skipped": 1,
    "total_duration_sec": 3300,
    "total_retries": 4,
    "commits": ["abc1234", "def5678", "ghi9012"]
  }
}
```

## Real-Time Updates

Both journals are updated after each spec:

```python
def update_journals(spec_result):
    # Append to markdown
    with open(md_journal, 'a') as f:
        f.write(format_spec_md(spec_result))

    # Update JSON (read, modify, write)
    journal = load_json(json_journal)
    journal['specs'].append(spec_result)
    save_json(json_journal, journal)

    # Update INDEX.md progress
    update_index_progress(spec_result)
```

## INDEX.md Progress

The orchestrator updates the Status column in real-time:

```markdown
| ID | Title | Effort | Priority | Dependencies | Status |
|----|-------|--------|----------|--------------|--------|
| S01 | Core | 4h | - | - | SUCCESS |
| S02 | Tech | 2h | 1 | - | SUCCESS |
| S03 | Int | 3h | - | S01, S02 | FAILED |
| S04 | Dep | 2h | - | S03 | SKIPPED |
| S05 | Ind | 1h | - | - | RUNNING |
```

## Final Report

After completion, a summary report is generated:

**File**: `{specs-dir}/orchestration-report.md`

See command documentation for full report template.
