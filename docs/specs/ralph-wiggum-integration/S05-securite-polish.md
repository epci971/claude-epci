# Specification — S05: Security & Polish

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S05
> **Estimated effort**: 2 day(s)
> **Dependencies**: S04
> **Blocks**: -

---

## 1. Context

This sub-spec implements security features, deprecation of /orchestrate, rate limiting, and intelligent mode selection. It polishes the Ralph integration for production readiness.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US7, US8, US12, US16

---

## 2. Scope

### Included

- US7: Configurable Security (--safety-level)
  - minimal: only max-iterations check
  - moderate: sandbox warning
  - strict: generate .claude/settings.json

- US8: /orchestrate Deprecation
  - Deprecation warning on usage
  - Migration guide documentation
  - Suggestion to use /ralph

- US12: Rate Limiting
  - MAX_CALLS_PER_HOUR (default 100)
  - Countdown on limit reached
  - API 5h limit detection and prompt
  - --calls flag for custom limit

- US16: Intelligent Mode Selection
  - Auto-detect best mode based on context
  - Display recommendation with reasoning
  - <10 stories + <2h → hook
  - >=10 stories OR >=2h → script
  - --overnight → script

### Excluded

- Core implementation — see S01-S04 (already done)
- v1.1 features (tmux, notifications, dashboard)

---

## 3. Tasks

### Security (US7)

- [ ] Implement --safety-level flag in /ralph
  - [ ] minimal: basic iteration check only
  - [ ] moderate: log warning if no sandbox detected
  - [ ] strict: generate secure .claude/settings.json

- [ ] Create security settings template
  - [ ] Sandbox configuration
  - [ ] Allowed/denied commands
  - [ ] Safe defaults

### Deprecation /orchestrate (US8)

- [ ] Modify `src/commands/orchestrate.md`
  - [ ] Add deprecation notice at top
  - [ ] Display warning on execution
  - [ ] Suggest /ralph alternative

- [ ] Update documentation
  - [ ] CLAUDE.md reference
  - [ ] Migration guide section

### Rate Limiting (US12)

- [ ] Implement in ralph_loop.sh / ralph-stop-hook.sh
  - [ ] Track calls per hour
  - [ ] Countdown display on limit
  - [ ] API 5h limit detection (error message pattern)
  - [ ] User prompt: [1] Wait 60min [2] Stop
  - [ ] --calls N flag

- [ ] Add to configuration
  - [ ] Default MAX_CALLS_PER_HOUR=100
  - [ ] Environment variable override

### Mode Selection (US16)

- [ ] Implement auto-selection logic in /ralph
  - [ ] Count stories from prd.json
  - [ ] Estimate duration from complexity
  - [ ] Apply selection rules
  - [ ] Display recommendation message

- [ ] Add reasoning display
  - [ ] Explain why mode was selected
  - [ ] Show override options

### Final Polish

- [ ] Update CLAUDE.md with Ralph documentation
- [ ] Create example project in docs/examples/ralph-demo/
- [ ] End-to-end integration test

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S05-AC1 | --safety-level minimal only checks max-iterations | Manual test |
| S05-AC2 | --safety-level moderate shows sandbox warning | Manual test |
| S05-AC3 | --safety-level strict generates settings.json | File check |
| S05-AC4 | /orchestrate shows deprecation warning | Manual test |
| S05-AC5 | Warning suggests /ralph as alternative | Message check |
| S05-AC6 | Documentation marks /orchestrate deprecated | Doc check |
| S05-AC7 | 100 calls/hour triggers countdown | Manual test |
| S05-AC8 | API 5h limit prompts user choice | Manual test |
| S05-AC9 | --calls 50 adjusts hourly limit | Manual test |
| S05-AC10 | <10 stories, <2h → mode hook auto-selected | Logic test |
| S05-AC11 | >=10 stories → mode script auto-selected | Logic test |
| S05-AC12 | --overnight forces script mode | Manual test |
| S05-AC13 | Mode selection shows reasoning message | Message check |

---

## 5. Technical Notes

### Safety Level Settings

```json
// .claude/settings.json (--safety-level strict)
{
  "sandbox": {
    "enabled": true,
    "allowed_commands": ["npm", "node", "git", "python", "pip"],
    "denied_patterns": ["rm -rf", "sudo", "curl | bash"]
  },
  "ralph": {
    "max_iterations": 50,
    "require_tests": true,
    "auto_commit": true
  }
}
```

### Rate Limiting Logic

```bash
check_rate_limit() {
  local current_hour=$(date +%H)
  local calls_this_hour=$(get_calls_count "$current_hour")

  if [ "$calls_this_hour" -ge "$MAX_CALLS_PER_HOUR" ]; then
    local minutes_until_reset=$((60 - $(date +%M)))
    echo "Rate limit reached. Reset in ${minutes_until_reset}m"
    countdown "$minutes_until_reset"
  fi
}

check_api_5h_limit() {
  if grep -q "rate_limit_exceeded" "$last_response"; then
    echo "API 5h limit detected."
    echo "[1] Wait 60 minutes"
    echo "[2] Stop execution"
    read -p "Choice: " choice
    # handle choice
  fi
}
```

### Mode Selection Rules

| Condition | Mode | Reason |
|-----------|------|--------|
| stories < 10 AND duration < 2h | hook | Context preserved, simpler |
| stories >= 10 OR duration >= 2h | script | Fresh context, robustness |
| --overnight flag | script | Crash recovery, rate limiting |
| --interactive flag | hook | Context preserved |

### Files to Modify/Create

| File | Action | Lines (est.) |
|------|--------|--------------|
| `src/commands/ralph.md` | Modify | +100 |
| `src/commands/orchestrate.md` | Modify | +20 |
| `src/scripts/ralph_loop.sh` | Modify | +80 |
| `src/hooks/ralph-stop-hook.sh` | Modify | +50 |
| `docs/examples/ralph-demo/` | Create | ~200 |

---

*Generated by /decompose — Project: ralph-wiggum-integration*
