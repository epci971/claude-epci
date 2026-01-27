# Journal Format - Exploration History

> Complete iteration history and EMS progression for brainstorm sessions.

## Overview

The journal captures the complete thinking process of a brainstorm session. Unlike the brief (synthesis), the journal is exhaustive.

**Filename**: `journal-{slug}-{date}.md`
**Location**: `docs/briefs/{slug}/`
**Audience**: The brainstorm participant for personal reference and traceability.
**Principle**: Complete history - nothing omitted.
**Note**: Not generated in Quick Mode.

## Template

```markdown
# Exploration Journal - [Topic]

> Generated on [date] - [N] iterations

---

## Session Metadata

| Attribute | Value |
|-----------|-------|
| **Initial topic** | [Original formulation] |
| **Detected type** | [Technical/Business/Creative/Analytical] |
| **Template used** | [feature/audit/project/research/decision/problem/strategy] |
| **Frameworks applied** | [List] |
| **Challenge mode** | Active/Inactive |
| **Quick Mode** | Yes/No |
| **Total iterations** | [N] |
| **Deep dives** | [Count] |
| **Pivots** | [Count] |
| **Bias alerts** | [Count] |
| **Final EMS** | [Score]/100 |
| **Dominant Persona** | [Maieuticien/Sparring/Architecte/Pragmatique] |
| **Phase shifts** | [Divergent->Convergent at iteration X] |
| **Session duration** | [X minutes] |

---

## Initialization Phase

### Input Clarification

| Attribute | Value |
|-----------|-------|
| Original input | "[raw user input]" |
| Clarity score | [X.XX] |
| Reformulated | "[cleaned input]" |
| User accepted | Yes/No |

### HMW Questions Generated

| # | Question | Selected |
|---|----------|----------|
| 1 | [HMW question 1] | Yes/No |
| 2 | [HMW question 2] | Yes/No |
| 3 | [HMW question 3] | Yes/No |
| 4 | [HMW question 4] | Yes/No |
| 5 | [HMW question 5] | Yes/No |

### Perplexity Research Prompts

| # | Category | Mode | Prompt | Injected |
|---|----------|------|--------|----------|
| R1 | [Category] | Standard/Deep | "[Prompt]" | Yes/No/Skipped |
| R2 | [Category] | Standard/Deep | "[Prompt]" | Yes/No/Skipped |
| R3 | [Category] | Standard/Deep | "[Prompt]" | Yes/No/Skipped |

### Startup Brief (Validated)

[Complete validated brief from Phase 1]

### Codebase Analysis (@Explore)

| Attribute | Value |
|-----------|-------|
| Stack detected | [e.g., React/TypeScript/Node] |
| Patterns | [List of detected patterns] |
| Conventions | [Naming, structure, etc.] |
| Related files | [If relevant] |

### Sources Analyzed

| Source | Type | Key Insights |
|--------|------|--------------|
| [Source 1] | URL/Document | [Summary] |
| [Source 2] | URL/Document | [Summary] |

### Project Memory Recall

| Type | Item | Relevance |
|------|------|-----------|
| Feature | [Past feature] | [How it relates] |
| Pattern | [Detected pattern] | [Application] |
| Preference | [User preference] | [Consideration] |

---

## Iteration History

### Iteration 1

**Phase**: Divergent
**Persona**: [#] Architecte
**EMS**: [Score] (+[Delta])

**Theme explored**: [Main theme of this iteration]

**Questions asked**:
1. [Question 1] - [Tag: Critical/Important/Info]
2. [Question 2] - [Tag]
3. [Question 3] - [Tag]

**User responses summary**:
[Brief summary of key points from user responses]

**Explored**:
- [Point 1]
- [Point 2]
- [Point 3]

**Decided**:
- [Decision if any]

**Opened**:
- [New thread 1]
- [New thread 2]

**Persona notes**:
[If persona change occurred, explain why]

---

### Iteration 2

**Phase**: Divergent
**Persona**: [?] Maieuticien
**EMS**: [Score] (+[Delta])

[Same structure...]

---

### Iteration [N] (Final)

**Phase**: Convergent
**Persona**: [>] Pragmatique
**EMS**: [Score] (+[Delta])

**Theme explored**: [Main theme]

**Questions asked**:
1. [Final questions]

**User responses summary**:
[Summary]

**Explored**:
- [Points]

**Decided**:
- [Final decisions]

**Opened**:
- [Remaining threads if any]

**Final recommendations**:
- [If any EMS-based recommendations were given]

---

## Phase History

| Iteration | Phase | Trigger |
|-----------|-------|---------|
| 1-3 | Divergent | Session start |
| 4 | Convergent | User command `converge` |
| 5-N | Convergent | Continued |

---

## Persona History

| Iteration | Persona | Trigger |
|-----------|---------|---------|
| 1 | [#] Architecte | Default |
| 2 | [?] Maieuticien | User uncertainty detected |
| 3 | [!] Sparring | Overconfidence detected ("obviously") |
| 4 | [>] Pragmatique | Stagnation (EMS < 5 pts x 2 iter) |
| N | [>] Pragmatique | Finish command |

---

## EMS Progression

| Iteration | Clarity | Depth | Coverage | Decisions | Action. | Total | Delta |
|-----------|---------|-------|----------|-----------|---------|-------|-------|
| Init | [X] | [X] | [X] | [X] | [X] | [X] | - |
| It.1 | [X] | [X] | [X] | [X] | [X] | [X] | +[Y] |
| It.2 | [X] | [X] | [X] | [X] | [X] | [X] | +[Y] |
| ... | ... | ... | ... | ... | ... | ... | ... |
| Final | [X] | [X] | [X] | [X] | [X] | [X] | +[Y] |

### EMS Graph

```
EMS Score
100 |
 90 | . . . . . . . . . . . . . . . . . . .
 80 |                              *--* [Final]
 70 | . . . . . . . . . . . . . *--+ . . .
 60 |                      *--+
 50 | . . . . . . . . . *-+ . . . . . . .
 40 |              *--+
 30 | . . . . *--+ . . . . . . . . . . . .
 20 |    *--+
 10 |
  0 +---+----+----+----+----+----+----+----
    Init It.1 It.2 It.3 It.4 It.5 It.6 End
```

---

## Key Decisions Made

| Decision | Iteration | Confidence | Rationale |
|----------|-----------|------------|-----------|
| [Decision 1] | [N] | High/Med/Low | [Brief why] |
| [Decision 2] | [N] | High/Med/Low | [Brief why] |
| [Decision 3] | [N] | High/Med/Low | [Brief why] |

---

## Open Threads

| Thread | Opened at | Priority | Status | Notes |
|--------|-----------|----------|--------|-------|
| [Thread 1] | Iteration [N] | High/Med/Low | Open/Closed | [Context] |
| [Thread 2] | Iteration [N] | High/Med/Low | Open/Closed | [Context] |

---

## Deep Dives

| Topic | Iteration | Duration | Key Findings |
|-------|-----------|----------|--------------|
| [Topic 1] | [N] | [X] questions | [Summary] |

---

## Pivots

| Original | New Direction | Iteration | Trigger |
|----------|---------------|-----------|---------|
| [Original topic] | [New topic] | [N] | [Why pivot occurred] |

---

## Frameworks Applied

| Framework | Iteration | Input | Output Summary |
|-----------|-----------|-------|----------------|
| [5 Whys] | [N] | [Starting question] | [Root cause found] |
| [Six Hats] | [N] | [Topic] | [Key perspectives] |
| [MoSCoW] | [N] | [Features] | [Prioritization] |
| [Pre-mortem] | [N] | [Plan] | [Identified risks] |

---

## Bias Alerts

| Bias Type | Iteration | Context | User Response |
|-----------|-----------|---------|---------------|
| [Confirmation bias] | [N] | [What triggered] | [Acknowledged/Dismissed/Explained] |
| [Sunk cost fallacy] | [N] | [What triggered] | [Response] |

---

## Techniques Suggested

| Technique | Iteration | For Axis | Applied | Outcome |
|-----------|-----------|----------|---------|---------|
| [5 Whys] | [N] | Depth | Yes/No | [If applied, what happened] |
| [Six Hats] | [N] | Coverage | Yes/No | [Outcome] |

---

## Perplexity Results Summary

### R1 - [Category]

**Prompt**: "[The prompt]"
**Mode**: Standard/Deep Research
**Status**: Injected/Skipped

**Key findings**:
- [Finding 1]
- [Finding 2]

**Impact on exploration**:
[How this influenced the brainstorm]

---

## Session Events Timeline

| Time | Event |
|------|-------|
| 00:00 | Session started |
| 00:02 | Brief validated |
| 00:05 | HMW generated |
| 00:08 | Perplexity prompts generated |
| 00:15 | Iteration 1 complete (EMS: 35) |
| 00:25 | Iteration 2 complete (EMS: 48) |
| ... | ... |
| XX:XX | `finish` command |
| XX:XX | Brief generated |
| XX:XX | Session complete |

---

## Post-Session Metrics

| Metric | Value |
|--------|-------|
| Total duration | [X] minutes |
| Iterations | [N] |
| Questions asked | [Total] |
| Decisions made | [Count] |
| Threads opened | [Count] |
| Threads closed | [Count] |
| Frameworks used | [Count] |
| Personas used | [List] |
| Phase changes | [Count] |
| EMS improvement | [Start] -> [End] (+[Total]) |

---

*Journal generated by Brainstorm v6.0*
```

## Section Guidelines

### Session Metadata
- Capture all configuration at session start
- Helps reproduce or understand session context
- Include dominant persona and phase shifts

### Initialization Phase
- Capture all Phase 1 activities
- HMW questions with selection status
- Perplexity prompts with injection status
- Codebase analysis results

### Iteration History
- One section per iteration
- Include all questions asked
- Summarize user responses (don't copy verbatim)
- Track persona and phase per iteration
- Note EMS with delta

### EMS Progression
- Complete table of all axes per iteration
- Visual graph for quick understanding
- Helps identify patterns and stagnation

### Decisions
- All decisions with full context
- When made and confidence level
- Enables future review of reasoning

### Open Threads
- Track what was started but not finished
- Helps future exploration
- Include priority for follow-up

### Deep Dives & Pivots
- Document significant exploration detours
- Capture what was learned
- Track direction changes

### Frameworks
- What was applied and when
- Input given and output received
- Helps evaluate framework effectiveness

### Bias Alerts
- Document all bias alerts raised
- How user responded
- Useful for learning and pattern recognition

### Timeline
- Chronological event log
- Helps understand session flow
- Useful for optimization

---

*Journal Format v1.0 - EPCI Brainstorm v6.0*
