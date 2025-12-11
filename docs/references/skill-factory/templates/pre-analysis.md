# Pre-Creation Analysis Template

> Complete this analysis before creating a new skill

---

## 1. Problem Definition

### Problem Statement
**What problem does this skill solve?** (1 sentence)

> _[Your answer here]_

### Current Pain Points
**What's painful about the current approach?**

- [ ] Manual repetition
- [ ] Inconsistent results
- [ ] Knowledge not documented
- [ ] Slow execution
- [ ] Error-prone process
- [ ] Other: _________________

### Value Proposition
**What value will this skill provide?**

> _[Your answer here]_

---

## 2. Frequency & Usage

### Historical Usage
**How many times has this task been performed in the past?**

| Period | Count |
|--------|-------|
| Last week | ___ |
| Last month | ___ |
| Last quarter | ___ |
| Total (estimated) | ___ |

**Threshold check**: ≥5 times in the past? ☐ Yes ☐ No

### Projected Usage
**How many times will this task be performed in the future?**

| Period | Expected Count |
|--------|----------------|
| Per week | ___ |
| Per month | ___ |
| Per quarter | ___ |

**Threshold check**: ≥10 times expected? ☐ Yes ☐ No

### Users
**Who will use this skill?**

| Role | Count | Frequency |
|------|-------|-----------|
| _[Role 1]_ | ___ | _/week_ |
| _[Role 2]_ | ___ | _/week_ |
| _[Role 3]_ | ___ | _/week_ |

---

## 3. Target Persona

### Primary User
**Describe the primary user of this skill**

- **Role**: _________________
- **Technical level**: ☐ Beginner ☐ Intermediate ☐ Advanced
- **Domain expertise**: ☐ Low ☐ Medium ☐ High
- **Familiarity with Claude**: ☐ New ☐ Regular ☐ Power user

### User Goals
**What does the user want to achieve?**

1. _[Goal 1]_
2. _[Goal 2]_
3. _[Goal 3]_

### User Constraints
**What limitations does the user have?**

- Time: _________________
- Access: _________________
- Skills: _________________

---

## 4. Trigger Analysis

### Expected Trigger Words
**What words/phrases will users employ?**

| Category | Keywords |
|----------|----------|
| Actions | _[e.g., analyze, extract, generate]_ |
| Objects | _[e.g., report, data, code]_ |
| Domains | _[e.g., revenue, security, documentation]_ |
| File types | _[e.g., PDF, Excel, Python]_ |

### Natural Language Requests
**How will users naturally phrase their requests?**

1. "_[Example request 1]_"
2. "_[Example request 2]_"
3. "_[Example request 3]_"

### Trigger Uniqueness
**Are these triggers unique or shared with other skills?**

| Trigger | Unique? | Competing Skill |
|---------|---------|-----------------|
| _[trigger 1]_ | ☐ Yes ☐ No | _[skill name]_ |
| _[trigger 2]_ | ☐ Yes ☐ No | _[skill name]_ |

---

## 5. Success Criteria

### Output Definition
**What does the skill produce?**

| Output | Format | Example |
|--------|--------|---------|
| _[Output 1]_ | _[format]_ | _[example]_ |
| _[Output 2]_ | _[format]_ | _[example]_ |

### Quality Criteria
**How do we know the output is good?**

- [ ] Criterion 1: _________________
- [ ] Criterion 2: _________________
- [ ] Criterion 3: _________________

### Measurable Success
**What metrics indicate success?**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Accuracy | ___% | _[how to measure]_ |
| Completeness | ___% | _[how to measure]_ |
| Time saved | ___ min | _[comparison]_ |

---

## 6. Scope Definition

### In Scope ✅
**What this skill DOES**

1. _[Capability 1]_
2. _[Capability 2]_
3. _[Capability 3]_
4. _[Capability 4]_

### Out of Scope ❌
**What this skill does NOT do**

1. _[Exclusion 1]_
2. _[Exclusion 2]_
3. _[Exclusion 3]_

### Boundary Conditions
**Edge cases and limitations**

| Scenario | Behavior |
|----------|----------|
| _[Edge case 1]_ | _[how handled]_ |
| _[Edge case 2]_ | _[how handled]_ |
| _[Invalid input]_ | _[error handling]_ |

---

## 7. Technical Requirements

### Platform Target
- [ ] Claude.ai
- [ ] Claude Code
- [ ] Both

### Dependencies
**External tools or packages needed**

| Dependency | Purpose | Required? |
|------------|---------|-----------|
| _[dep 1]_ | _[purpose]_ | ☐ Yes ☐ No |
| _[dep 2]_ | _[purpose]_ | ☐ Yes ☐ No |

### Data Access
**What data does the skill need?**

| Data Source | Access Method | Sensitivity |
|-------------|---------------|-------------|
| _[source 1]_ | _[method]_ | ☐ Public ☐ Internal ☐ Confidential |
| _[source 2]_ | _[method]_ | ☐ Public ☐ Internal ☐ Confidential |

---

## 8. Stability Assessment

### Procedure Stability
**How stable is the underlying procedure?**

- [ ] Very stable (changes <1x/year)
- [ ] Stable (changes 1-2x/year)
- [ ] Moderate (changes quarterly)
- [ ] Volatile (changes monthly or more) ⚠️

### Knowledge Stability
**How stable is the domain knowledge?**

- [ ] Static (rarely changes)
- [ ] Evolving slowly
- [ ] Rapidly changing ⚠️

### Risk Assessment
**What could cause this skill to become outdated?**

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| _[risk 1]_ | _L/M/H_ | _L/M/H_ | _[mitigation]_ |
| _[risk 2]_ | _L/M/H_ | _L/M/H_ | _[mitigation]_ |

---

## 9. Decision Gate

### Checklist Summary

| Criterion | Met? |
|-----------|------|
| Recurring task (≥5 past, ≥10 future) | ☐ |
| Clear problem definition | ☐ |
| Defined success criteria | ☐ |
| Stable procedures | ☐ |
| Unique triggers (no overlap) | ☐ |
| Clear scope boundaries | ☐ |
| Technical feasibility | ☐ |

### Recommendation

Based on this analysis:

- [ ] ✅ **PROCEED** - Create the skill
- [ ] ⚠️ **REFINE** - Narrow scope or clarify requirements
- [ ] ❌ **STOP** - Not a good skill candidate

### Reason
> _[Explain the recommendation]_

---

## 10. Next Steps

If proceeding:

1. [ ] Define skill name (kebab-case)
2. [ ] Draft description (triggering)
3. [ ] Design workflow
4. [ ] Identify reference content
5. [ ] Plan test cases

---

## Metadata

| Field | Value |
|-------|-------|
| **Analyst** | _[name]_ |
| **Date** | _[YYYY-MM-DD]_ |
| **Version** | 1.0 |
| **Status** | ☐ Draft ☐ Review ☐ Approved |
