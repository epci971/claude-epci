---
description: >-
  Time-boxed exploration for technical uncertainties. Generates a Spike Report
  with GO/NO-GO/MORE_RESEARCH verdict. No production code, focus on
  learning and uncertainty reduction.
argument-hint: "[duration] [question] [--think-hard] [--c7] [--seq]"
allowed-tools: [Read, Glob, Grep, Bash, Task, WebFetch, WebSearch]
---

# EPCI Spike — Time-boxed Exploration

## Overview

A spike is a time-limited exploration to reduce technical uncertainty.
**Objective: Learn, not produce code.**

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `duration` | Maximum time (e.g., 30min, 1h, 2h) | 1h |
| `question` | Technical question to resolve | Required |

## Supported Flags

| Flag | Effect | Auto-Trigger |
|------|--------|--------------|
| `--think-hard` | Deep analysis for complex spikes | Complex question detected |
| `--uc` | Compressed Spike Report | context > 75% |
| `--c7` | Enable Context7 for library docs | Auto with tech exploration |
| `--seq` | Enable Sequential for complex reasoning | With `--think-hard` |
| `--no-mcp` | Disable all MCP servers | Never |

**Note:** `--safe`, `--wave` flags are not applicable to spikes (exploration only).

## When to Use a Spike

- New unknown technology or framework
- Uncertain feasibility
- Multiple possible approaches with no clear preference
- Integration with undocumented external system
- Performance or scalability to validate

## Pre-Workflow: Load Project Memory

**Skill**: `project-memory`

Load project context from `.project-memory/` before exploration. The skill handles:
- Reading context, conventions, settings, patterns
- Finding similar past spikes or features for reference
- Applying project-specific patterns to suggestions

**If `.project-memory/` does not exist:** Continue with defaults.

---

## Process

**⚠️ IMPORTANT: Follow ALL steps in sequence. Do NOT skip the Spike Report generation.**

### 1. Framing (MANDATORY — 5 min)

**⚠️ DO NOT SKIP:** Display the Spike Setup to the user before proceeding.

Clearly define:
- **Question**: What uncertainty do we want to resolve?
- **Success criteria**: How will we know it's feasible?
- **Time-box**: Strict maximum duration
- **Scope**: What's included/excluded from exploration

```markdown
## Spike Setup

**Question:** [Precise technical question]

**Success criteria:**
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

**Time-box:** [Duration]

**Scope:**
- ✅ Included: [What we explore]
- ❌ Excluded: [What we don't explore]
```

### 2. Exploration (MANDATORY)

**⚠️ DO NOT SKIP:** Use Task tool with @Explore subagent.

**Invoke @Explore** (thorough level) to:
- Search for existing solutions
- Analyze code examples
- Identify applicable patterns

**Typical activities:**
- Read documentation
- Create throwaway prototypes
- Test hypotheses
- Evaluate alternatives

**Rules:**
- ⏱️ Strictly respect the time-box
- 🗑️ Produced code is throwaway (not production quality)
- 📝 Document discoveries as you go
- 🎯 Stay focused on the initial question

### 3. Synthesis (MANDATORY — 10 min)

**⚠️ DO NOT SKIP:** Synthesize findings before generating the report.

At the end of the time-box, synthesize:
- What was learned
- What works / doesn't work
- Identified risks
- Recommendation

## Output: Spike Report (USE WRITE TOOL — MANDATORY)

**⚠️ MANDATORY:** Use the **Write tool** to create the file `docs/spikes/<spike-slug>.md`

Create the directory if needed, then write the Spike Report:

```markdown
# Spike Report — [Title]

## Question
[The technical question explored]

## Executive Summary
[2-3 sentences on the main conclusion]

## Exploration Conducted

### Approaches Tested
| Approach | Result | Notes |
|----------|--------|-------|
| [Approach 1] | ✅ Works | [Details] |
| [Approach 2] | ❌ Fails | [Reason] |
| [Approach 3] | ⚠️ Partial | [Limitations] |

### Prototype Code
```[lang]
// Throwaway code - DO NOT use in production
[snippet demonstrating the concept]
```

### Discoveries
1. [Important discovery 1]
2. [Important discovery 2]
3. [Important discovery 3]

### Identified Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High | Elevated | [Solution] |
| [Risk 2] | Medium | Medium | [Solution] |

## Resources Consulted
- [Link 1] - [What we learned from it]
- [Link 2] - [What we learned from it]

## Verdict

### [GO | NO-GO | MORE_RESEARCH]

**Justification:**
[Explanation of the verdict]

### If GO
- **Recommended approach:** [Approach to follow]
- **Estimated effort:** [SMALL | STANDARD | LARGE]
- **Next step:** Launch `/brief` with this information

### If NO-GO
- **Reason:** [Why it's not feasible]
- **Suggested alternatives:** [Other options to consider]

### If MORE_RESEARCH
- **Remaining questions:** [What still needs exploration]
- **Suggested next spike:** [Proposed new spike]

## Time Spent
- Planned time-box: [Duration]
- Actual time: [Duration]
```

## Spike Examples

### Spike: External API Integration

```
Question: Can payment API X handle our volumes?
Time-box: 2h

Exploration:
- Read API documentation
- Test endpoints in sandbox
- Measure response times
- Calculate costs

Verdict: GO
- API supports 1000 req/s (our need: 100)
- Acceptable pricing
- PHP SDK available
```

### Spike: New Technology

```
Question: Is GraphQL suitable for our API?
Time-box: 4h

Exploration:
- Setup GraphQL server
- Implement basic query
- Compare with current REST
- Evaluate learning curve

Verdict: NO-GO
- Learning curve too steep for the team
- Insufficient benefits for our use case
- Recommendation: Stay with REST
```

## Skills Loaded

- `project-memory` (context and conventions)
- `architecture-patterns` (approach evaluation)
- `flags-system` (flag handling)
- `mcp` (Context7 for docs, Sequential for reasoning)
- `[stack-skill]` (auto-detected)

## Differences with Other Workflows

| Aspect | /spike | /epci | /quick |
|--------|-------------|-------|-------------|
| Objective | Learn | Produce | Produce |
| Code | Throwaway | Production | Production |
| Output | Spike Report | Feature Doc | Commit |
| Tests | No | Yes | Optional |
| Time-box | Strict | Flexible | Flexible |

## Post-Spike

After a GO spike:
1. Create a brief with spike information
2. Launch `/brief` for normal workflow
3. Reference Spike Report in Feature Document

```
📊 **SPIKE COMPLETE**

Spike Report generated: docs/spikes/<spike-slug>.md
Verdict: [GO | NO-GO | MORE_RESEARCH]

Next step: [Recommended action]
```
