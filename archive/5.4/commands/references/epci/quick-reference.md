# EPCI Quick Reference

> Summary tables for `/epci` command

---

## Workflow Summary

```
/brief → Feature Document §1
  ↓
/epci (Phase 1) → §2 Implementation Plan → BP1
  ↓
/epci (Phase 2) → TDD + Reviews → §3 Part 1 → BP2
  ↓
/epci (Phase 3) → Commit + Docs → §3 Part 2 → Complete
```

---

## Key Agents

| Agent | Phase | Model | Role |
|-------|-------|-------|------|
| @plan-validator | P1 | opus | Gate-keeper validation |
| @code-reviewer | P2 | opus | Quality review (mandatory) |
| @security-auditor | P2 | opus | Security audit (conditional) |
| @qa-reviewer | P2 | sonnet | Test review (conditional) |
| @doc-generator | P3 | sonnet | Documentation generation |

---

## Breakpoints

| BP | Phase | Required Action |
|----|-------|-----------------|
| BP1 | After Phase 1 | Approve implementation plan |
| BP2 | After Phase 2 | Approve code before finalization |

---

## Common Flag Combinations

| Use Case | Flags |
|----------|-------|
| Fast standard feature | `--turbo` |
| Fast with quality gate | `--turbo --safe` |
| Large refactoring | `--large` or `--think-hard --wave` |
| Security-sensitive | `--safe --think-hard` |
| CI/CD pipeline | `--no-hooks --uc` |

---

## --large Mode

The `--large` flag is an alias for `--think-hard --wave`.

| Aspect | Standard | Large |
|--------|----------|-------|
| Thinking P1 | `think` | `think hard` |
| Thinking P2 | `think` | `think hard` |
| @security-auditor | Conditional | Conditional |
| @qa-reviewer | Conditional | Conditional |
| Wave orchestration | Off | Enabled |

**Note:** For v2.7 behavior with all subagents mandatory:
```
/epci --large --safe
```

---

## Flag Compatibility Matrix

| Combination | Result |
|-------------|--------|
| `--think` + `--think-hard` | `--think-hard` wins |
| `--uc` + `--verbose` | Explicit wins |
| `--large` + `--ultrathink` | `--ultrathink` wins |
| `--wave` + `--safe` | Both active |
| `--no-hooks` + any | Both active |

---

## See Also

- Full flags: `src/settings/flags.md`
- Breakpoint metrics: `src/skills/core/breakpoint-metrics/SKILL.md`
- MCP servers: `src/skills/mcp/SKILL.md`
- Feature templates: @references/epci/feature-document-templates.md

---

*Quick Reference for epci.md*
