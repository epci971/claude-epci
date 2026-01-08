# Detection Patterns - Component Opportunity Analysis

> Detailed patterns and scoring criteria for automatic component detection

---

## Detection Algorithm

### Core Process

```
Observe User Actions
        │
        ▼
Pattern Recognition
        │
        ▼
Score Calculation
        │
        ▼
Threshold Check (≥4)
        │
   ┌────┴────┐
   ▼         ▼
Below      Above
Threshold  Threshold
   │         │
   ▼         ▼
Continue   Generate
Observing  Suggestion
```

---

## Skill Detection Patterns

### Pattern Categories

| Category | Weight | Description |
|----------|--------|-------------|
| **Repetition** | High | Same pattern appears multiple times |
| **Domain Gap** | Medium | Technical area not covered by existing skills |
| **Knowledge Demand** | Medium | Frequent documentation/research on topic |
| **Convention Application** | Low | Manual application of guidelines |

### Detailed Scoring Matrix

| Signal | Score | Detection Method | Example |
|--------|-------|------------------|---------|
| Pattern repeated 3+ times | +3 | Count identical sequences | Same API pattern in 3 files |
| Pattern repeated 5+ times | +4 | Count identical sequences | Same validation logic everywhere |
| Technical domain not covered | +2 | Check against existing skills | Rust project, no Rust skill |
| New framework detected | +2 | Package/config analysis | Svelte in package.json |
| Documentation consulted 3+ times | +2 | Track WebFetch/research | Same library docs fetched |
| Copy-paste of guidelines | +1 | Detect similar code blocks | Convention applied manually |
| Explicit user request | +3 | Keyword detection | "I need a skill for..." |

### Skill Type Inference

| Detected Pattern | Suggested Skill Type |
|------------------|---------------------|
| New framework/library | Stack skill |
| Architecture patterns | Core skill |
| Testing patterns | Testing skill |
| Conventions/formatting | Conventions skill |
| External service integration | Integration skill |

---

## Command Detection Patterns

### Pattern Categories

| Category | Weight | Description |
|----------|--------|-------------|
| **Sequence Repetition** | High | Same tool sequence repeated |
| **Workflow Gap** | Medium | Manual process could be automated |
| **Skill Combination** | Medium | Same skills used together |
| **User Request** | High | Explicit automation request |

### Detailed Scoring Matrix

| Signal | Score | Detection Method | Example |
|--------|-------|------------------|---------|
| Repeated action sequence | +3 | Track tool call patterns | lint → test → build repeated |
| Same sequence 3+ times | +4 | Count repetitions | CI sequence manual each time |
| Frequent skill combination | +2 | Track skill loading | Always testing + security skills |
| Documented but manual process | +2 | Guide reference + manual steps | Following deployment guide |
| Explicit user request | +3 | Keyword detection | "I'd like a command for..." |
| Multi-step with breakpoints | +2 | Detect pause patterns | User confirms between steps |

### Command Type Inference

| Detected Pattern | Suggested Command Type |
|------------------|----------------------|
| Linear tool sequence | Simple command |
| Sequence with conditions | Branching command |
| Sequence with user pauses | Interactive command |
| Cross-project workflow | Orchestration command |

---

## Subagent Detection Patterns

### Pattern Categories

| Category | Weight | Description |
|----------|--------|-------------|
| **Specialized Validation** | High | Same validation applied repeatedly |
| **Review Pattern** | Medium | Checklist-based review |
| **Domain Expertise** | Medium | Narrow specialized knowledge |
| **Report Generation** | Low | Standardized output format |

### Detailed Scoring Matrix

| Signal | Score | Detection Method | Example |
|--------|-------|------------------|---------|
| Repeated specialized validation | +3 | Track validation patterns | Same security check 3+ times |
| Same checklist applied | +3 | Detect checklist usage | Accessibility audit checklist |
| Recurring manual review | +2 | Track review sessions | Code review with same criteria |
| Narrow domain expertise | +2 | Analyze knowledge scope | Only API design expertise needed |
| Standardized report format | +1 | Detect report templates | Same report structure |
| Explicit validation need | +3 | Keyword detection | "Need to validate..." |

### Subagent Type Inference

| Detected Pattern | Suggested Subagent Type |
|------------------|------------------------|
| Security checks | Security auditor |
| Code quality review | Code reviewer |
| Test coverage analysis | QA reviewer |
| Documentation gaps | Doc checker |
| Performance analysis | Performance auditor |
| Accessibility check | A11y auditor |

---

## Multi-Signal Combinations

### Skill Combinations

| Signals | Combined Score | Confidence |
|---------|---------------|------------|
| Repetition + Domain Gap | 5+ | High |
| Knowledge Demand + Convention | 3+ | Medium |
| User Request + Domain Gap | 5+ | High |

### Command Combinations

| Signals | Combined Score | Confidence |
|---------|---------------|------------|
| Sequence + Skill Combo | 5+ | High |
| Manual Process + Repetition | 5+ | High |
| User Request alone | 3+ | Medium |

### Subagent Combinations

| Signals | Combined Score | Confidence |
|---------|---------------|------------|
| Validation + Report | 4+ | High |
| Review + Domain Expertise | 4+ | High |
| Checklist + Repetition | 4+ | High |

---

## Confidence Scoring

### Score to Confidence Mapping

| Score Range | Confidence Level | Suggestion Style |
|-------------|-----------------|------------------|
| 4-5 | Medium (6/10) | "You might benefit from..." |
| 6-7 | High (8/10) | "Consider creating..." |
| 8+ | Very High (9/10) | "Strongly recommend creating..." |

### Confidence Adjustments

| Factor | Adjustment |
|--------|------------|
| User explicitly requested | +2 |
| Pattern consistent across sessions | +1 |
| Similar component exists | -2 |
| Low variation in pattern | -1 |

---

## False Positive Prevention

### Exclusion Criteria

| Scenario | Action |
|----------|--------|
| Existing skill covers domain | Suppress suggestion |
| Pattern only 2 occurrences | Wait for more |
| User dismissed similar suggestion | Reduce score by 2 |
| One-time project setup | Mark as non-recurring |

### Validation Before Suggestion

```
Before suggesting:
1. Check existing skills/commands/agents
2. Verify pattern recurrence (not one-time)
3. Confirm automation benefit
4. Assess implementation complexity
```

---

## Monitoring Points

### Where to Detect

| Monitoring Point | What to Track |
|------------------|---------------|
| Tool invocations | Repeated sequences |
| Skill loading | Combination patterns |
| User prompts | Explicit requests |
| WebFetch calls | Knowledge demands |
| Code patterns | Convention application |
| Review sessions | Validation patterns |

### Session Tracking

```yaml
session_metrics:
  tool_sequences: []
  skill_combinations: []
  research_topics: []
  code_patterns: []
  review_checklists: []
  user_requests: []
```

---

## Quick Reference

```
+------------------------------------------+
|         DETECTION THRESHOLDS              |
+------------------------------------------+
| SKILL:    Score ≥ 4                       |
|   Repetition: +3, Domain: +2, Docs: +2   |
+------------------------------------------+
| COMMAND:  Score ≥ 4                       |
|   Sequence: +3, Combo: +2, Request: +3   |
+------------------------------------------+
| SUBAGENT: Score ≥ 4                       |
|   Validation: +3, Review: +2, Report: +1 |
+------------------------------------------+
| CONFIDENCE:                               |
|   4-5 = Medium | 6-7 = High | 8+ = V.High|
+------------------------------------------+
```
