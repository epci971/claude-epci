# Specification — S08: Polish & Migration

> **Parent project**: ralph-wiggum-integration
> **Spec ID**: S08
> **Estimated effort**: 2 day(s)
> **Dependencies**: S07
> **Blocks**: —

---

## 1. Context

This sub-spec handles the final polish: configurable security levels, `/orchestrate` deprecation, rate limiting, and intelligent mode selection. These are "Should-have" features that complete the Ralph integration.

**Source**: `PRD-ralph-wiggum-integration-2025-01-13.md` — US7, US8, US12, US16

---

## 2. Scope

### Included

- Security levels (minimal, moderate, strict)
- `/orchestrate` deprecation with migration guide
- Rate limiting (100 calls/hour default)
- Intelligent mode selection algorithm
- Documentation updates
- CLAUDE.md updates for v5.1.0

### Excluded

- Core functionality (all previous specs)
- tmux monitoring (v1.1)
- Notifications Slack/Email (v1.1)
- Dashboard web (v2)

---

## 3. Tasks

- [ ] Implement security levels (US7):
  - [ ] `--safety-level minimal`: Only max-iterations check
  - [ ] `--safety-level moderate` (default): Warning if no sandbox
  - [ ] `--safety-level strict`: Generate secure .claude/settings.json
  - [ ] Document security implications

- [ ] Implement rate limiting (US12):
  - [ ] `MAX_CALLS_PER_HOUR` environment variable (default: 100)
  - [ ] `--calls N` flag override
  - [ ] Countdown display when limit reached
  - [ ] Reset counter on new hour
  - [ ] Handle Anthropic 5h API limit:
    - [ ] Detect rate limit error
    - [ ] Prompt: [1] Wait 60min [2] Stop

- [ ] Implement intelligent mode selection (US16):
  - [ ] Algorithm based on:
    - [ ] Story count (< 10 → hook, >= 10 → script)
    - [ ] Estimated duration (< 2h → hook, >= 2h → script)
    - [ ] --overnight flag → script
    - [ ] --interactive flag → hook
  - [ ] Display recommendation with reason
  - [ ] Allow explicit --mode override

- [ ] Deprecate /orchestrate (US8):
  - [ ] Add deprecation warning to orchestrate.md
  - [ ] Display warning when command executed
  - [ ] Suggest `/ralph` alternative
  - [ ] Create migration guide in docs/

- [ ] Update documentation:
  - [ ] Update CLAUDE.md with v5.1.0 features
  - [ ] Add Ralph section to CLAUDE.md
  - [ ] Create docs/ralph-guide.md
  - [ ] Update docs/briefs/ template

- [ ] Update hooks documentation:
  - [ ] Document ralph-stop-hook.sh
  - [ ] Document ralph-session hooks

- [ ] Write integration tests for polish features

---

## 4. Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| S08-AC1 | Given `--safety-level minimal`, When Ralph runs, Then only max-iterations checked | Security test |
| S08-AC2 | Given `--safety-level moderate`, When no sandbox, Then warning displayed | Warning test |
| S08-AC3 | Given `--safety-level strict`, When Ralph runs, Then secure settings.json generated | Settings test |
| S08-AC4 | Given user launches /orchestrate, When executed, Then deprecation warning shown | Deprecation test |
| S08-AC5 | Given deprecation warning, When displayed, Then suggests /ralph alternative | Migration test |
| S08-AC6 | Given MAX_CALLS_PER_HOUR=100, When limit reached, Then countdown until reset | Rate limit test |
| S08-AC7 | Given Anthropic 5h limit reached, When detected, Then prompt wait/stop options | API limit test |
| S08-AC8 | Given `/ralph` without --mode, When < 10 stories, Then hook mode recommended | Auto-select test |
| S08-AC9 | Given `/ralph --overnight`, When executed, Then script mode selected | Overnight test |
| S08-AC10 | Given recommendation shown, When displayed, Then explains why mode suggested | Explanation test |

---

## 5. Technical Notes

### Security Levels

| Level | Checks | Actions |
|-------|--------|---------|
| minimal | max-iterations | None |
| moderate | max-iterations, sandbox | Warning if no sandbox |
| strict | max-iterations, sandbox, settings | Generate secure settings.json |

### Secure Settings (strict mode)

```json
{
  "permissions": {
    "allow_bash": false,
    "allow_write": ["src/", "tests/"],
    "deny_paths": [".env", "credentials/"]
  },
  "ralph": {
    "max_iterations": 50,
    "rate_limit": 100,
    "circuit_breaker": true
  }
}
```

### Rate Limiting Display

```
⏱️ Rate limit reached (100/100 calls this hour)
   Next reset in: 23 minutes

   Waiting... [████████░░░░░░░░░░░░] 23:45
```

### Anthropic API Limit Handling

```
⚠️ Anthropic API rate limit reached (5h limit)

This is the provider's rate limit, not Ralph's.

Options:
  [1] Wait 60 minutes and continue
  [2] Stop execution (can resume with --continue)

Your choice:
```

### Mode Selection Algorithm

```python
def recommend_mode(stories, flags):
    if flags.get('--mode'):
        return flags['--mode']  # Explicit override

    if flags.get('--overnight'):
        return 'script'  # Robust for overnight

    if flags.get('--interactive'):
        return 'hook'  # Context preservation

    story_count = len(stories)
    estimated_hours = sum(s['estimated_minutes'] for s in stories) / 60

    if story_count < 10 and estimated_hours < 2:
        return 'hook'
    else:
        return 'script'
```

### Deprecation Warning

```
⚠️ DEPRECATION WARNING

/orchestrate is deprecated and will be removed in v6.0.

Please use /ralph instead:
  /ralph docs/specs/project/ --max-iterations 50

Migration guide: docs/migration/orchestrate-to-ralph.md
```

---

## 6. Source Reference

> Extract from `PRD-ralph-wiggum-integration-2025-01-13.md`

**US7 — Sécurité configurable**

- Given `--safety-level minimal`, When Ralph s'exécute, Then seul max-iterations est vérifié
- Given `--safety-level moderate`, When Ralph s'exécute, Then un warning s'affiche si pas de sandbox
- Given `--safety-level strict`, When Ralph s'exécute, Then .claude/settings.json sécurisé est généré

**US8 — Dépréciation /orchestrate**

- Given un utilisateur qui lance /orchestrate, When la commande s'exécute, Then un warning de dépréciation s'affiche
- Given le warning, When il s'affiche, Then il suggère d'utiliser /ralph à la place
- Given la documentation, When elle est mise à jour, Then /orchestrate est marqué deprecated

**US12 — Rate Limiting**

- Given MAX_CALLS_PER_HOUR=100, When la limite est atteinte, Then countdown jusqu'au reset horaire
- Given limite API 5h Anthropic atteinte, When détectée, Then proposer: [1] Attendre 60min [2] Arrêter
- Given flag `--calls 50`, When passé à /ralph, Then limite horaire ajustée

**US16 — Sélection de mode intelligent**

- Given `/ralph` sans flag mode, When durée estimée < 2h, Then mode hook par défaut
- Given `/ralph` sans flag mode, When durée estimée > 2h ou --overnight, Then mode script par défaut
- Given recommandation de mode, When affichée, Then explique pourquoi ce mode est suggéré

---

*Generated by /decompose — Project: ralph-wiggum-integration*
