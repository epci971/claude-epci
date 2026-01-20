# Phase 2: Implementation — Detailed Process

> Reference for `/epci` Phase 2 detailed workflow

---

## TDD Cycle

**Execute `pre-phase-2` hooks** (if configured)

For each task in the plan:

```
1. RED — Write the failing test
2. Execute → confirm failure
3. GREEN — Implement minimal code
4. Execute → confirm passing
5. REFACTOR — Improve if necessary
6. Check off the task
```

---

## Post-Implementation Reviews

After all tasks complete:

1. Run complete test suite
2. Invoke @code-reviewer (mandatory)
3. Invoke @security-auditor (if applicable)
4. Invoke @qa-reviewer (if applicable)
5. Fix Critical/Important issues
6. Generate proactive suggestions (F06)

---

## Proactive Suggestions (F06)

After code review, the `proactive-suggestions` skill generates suggestions.

**Sources:**
- Subagent findings (@code-reviewer, @security-auditor, @qa-reviewer)
- PatternDetector analysis on changed files

**Priority Order:** P1 (Security) > P2 (Performance/Quality) > P3 (Style)

**Display in BP2:** Up to 5 suggestions with actions:
- `[Accepter tout]` — Apply auto-fixable suggestions
- `[Voir détails]` — Show full details
- `[Ignorer]` — Skip for this session

User feedback is recorded for learning (F08).

---

## Output §3 Part 1 Format

**Use Edit tool** (NOT EnterPlanMode) to update Feature Document.

**Path:** `docs/features/<slug>.md`

```markdown
## §3 — Implementation & Finalization

### Progress
- [x] Task 1 — Create entity Y
- [x] Task 2 — Modify service X
- [x] Task 3 — Add validation

### Tests
```bash
$ php bin/phpunit
OK (47 tests, 156 assertions)
```

### Reviews
- **@code-reviewer**: APPROVED (0 Critical, 2 Minor)
- **@security-auditor**: APPROVED
- **@qa-reviewer**: N/A

### Deviations
| Task | Deviation | Justification |
|------|-----------|---------------|
| #3 | +1 file | Helper extraction |
```

---

## Post-Phase Hooks

```bash
python3 hooks/runner.py post-phase-2 --context '{
  "phase": "phase-2",
  "feature_slug": "<slug>",
  "files_modified": [...],
  "test_results": {...}
}'
```

---

## Breakpoint BP2

**MANDATORY:** Display breakpoint and WAIT for user confirmation.

**Template:** Use `breakpoint-metrics/templates/bp2-template.md`

**Variables:** Tasks completed, test results, review verdicts, proactive suggestions

**Conditional agents:**
- @security-auditor if auth/security files detected
- @qa-reviewer if 5+ test files
- In `--safe` mode: all mandatory

**User options:**
- "Continuer" — Proceed to Phase 3
- "Corriger issues" — Fix reported issues
- "Voir rapports" — Show full reports
- "Annuler" — Abort workflow

**Execute `on-breakpoint` hooks** (if configured)

---

*Reference for epci.md Phase 2*
