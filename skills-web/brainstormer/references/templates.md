# Startup Templates

> Pre-configured brainstorming templates for common use cases

---

## Template Overview

| Template | Use Case | Default Frameworks | Typical Duration |
|----------|----------|-------------------|------------------|
| `feature` | New functionality for an application | MoSCoW, Impact/Effort | 30-45 min |
| `audit` | Analysis of existing state | SWOT, Weighted Criteria | 45-60 min |
| `project` | New project from scratch | 5 Whys, Six Hats | 45-60 min |
| `research` | Technical exploration, benchmarking | Comparative Matrix, Scoring | 30-45 min |

---

## Template: `feature`

### Description
For brainstorming new features on an existing application. Balances user needs, technical feasibility, and business value.

### Default Configuration
| Setting | Value |
|---------|-------|
| Primary type | Technical |
| Secondary type | Business |
| Mandatory framework | MoSCoW (before finish) |
| Suggested framework | Impact/Effort |
| Typical iterations | 3-5 |

### Framing Questions (Phase 1)

**Context** (ask first):
1. What application/product is this for?
2. What's the current state of this area in the app?

**User Need** (ask second):
3. Who will use this feature? (persona/role)
4. What problem does it solve for them?
5. How do they currently work around not having this?

**Constraints** (ask third):
6. Any technical stack limitations?
7. Timeline or budget constraints?
8. Dependencies on other systems/teams?

**Success** (ask last):
9. How will we measure if this feature succeeds?

### Startup Brief Format

```markdown
## 📋 Feature Brainstorm Brief

**Application**: [Name]
**Feature area**: [Area/module]

**Target user**: [Persona]
**Problem solved**: [Core problem]
**Current workaround**: [How users cope today]

**Constraints**:
- Technical: [Stack, integrations]
- Timeline: [If any]
- Dependencies: [If any]

**Success metric**: [How we'll know it worked]

**Type**: Technical + Business
**Template**: feature
**Frameworks**: MoSCoW (mandatory), Impact/Effort (suggested)

→ Validate to start iterations?
```

### Report Emphasis
- Clear specification of the feature scope
- Prioritized requirements (MoSCoW breakdown)
- Technical considerations and constraints
- Implementation roadmap with phases
- Success metrics and validation approach

---

## Template: `audit`

### Description
For analyzing existing systems, contracts, processes, or situations. Focus on objective evaluation with actionable recommendations.

### Default Configuration
| Setting | Value |
|---------|-------|
| Primary type | Analytical |
| Secondary type | (varies by subject) |
| Mandatory framework | SWOT or Weighted Criteria |
| Suggested framework | Comparative Matrix |
| Typical iterations | 4-6 |

### Framing Questions (Phase 1)

**Scope** (ask first):
1. What exactly are we auditing? (system, contract, process, etc.)
2. What's explicitly in scope?
3. What's explicitly out of scope?

**Criteria** (ask second):
4. What criteria matter most for this evaluation?
5. How should criteria be weighted? (equal or prioritized)
6. Are there compliance requirements or standards to meet?

**Context** (ask third):
7. Why is this audit being done now?
8. What decisions will depend on the results?
9. Who are the stakeholders for the findings?

**Baseline** (ask last):
10. What data/documentation do we have?
11. What's the expected standard or benchmark?

### Startup Brief Format

```markdown
## 📋 Audit Brainstorm Brief

**Subject**: [What's being audited]
**Scope**: 
- In: [Included elements]
- Out: [Excluded elements]

**Evaluation criteria**:
1. [Criterion 1] — Weight: [X%]
2. [Criterion 2] — Weight: [X%]
3. [Criterion 3] — Weight: [X%]

**Context**: [Why now, what decision depends on this]
**Stakeholders**: [Who needs the results]
**Baseline/Standard**: [What we're comparing against]

**Type**: Analytical
**Template**: audit
**Frameworks**: SWOT or Weighted Criteria (mandatory)

→ Validate to start iterations?
```

### Report Emphasis
- Clear evaluation methodology documented
- Findings organized by criteria
- Severity/priority ranking of issues
- Actionable recommendations with rationale
- Risk assessment for each finding

---

## Template: `project`

### Description
For brainstorming new projects from scratch. Focuses on vision clarity, constraint identification, and roadmap development.

### Default Configuration
| Setting | Value |
|---------|-------|
| Primary type | Business |
| Secondary type | Creative |
| Mandatory framework | 5 Whys (for problem clarity) |
| Suggested framework | Six Hats, MoSCoW |
| Typical iterations | 4-6 |

### Framing Questions (Phase 1)

**Vision** (ask first):
1. What's the ultimate goal of this project?
2. What does success look like in concrete terms?
3. Why does this project matter? (to you, to users, to the organization)

**Stakeholders** (ask second):
4. Who is this project for? (end users, clients, internal)
5. Who needs to be involved in making it happen?
6. Who could block or derail this project?

**Constraints** (ask third):
7. What's the budget range? (order of magnitude)
8. What's the timeline expectation?
9. What resources are available? (team, tools, etc.)
10. What technical or organizational constraints exist?

**Risks** (ask last):
11. What could derail this project?
12. What dependencies exist?
13. What's unknown that we need to figure out?

### Startup Brief Format

```markdown
## 📋 Project Brainstorm Brief

**Project name/concept**: [Name]
**Vision**: [Ultimate goal in one sentence]
**Success looks like**: [Concrete outcomes]

**For whom**: [Target beneficiaries]
**Involved**: [Key people/teams]
**Potential blockers**: [Who could derail]

**Constraints**:
- Budget: [Range]
- Timeline: [Expectation]
- Resources: [Available]
- Other: [Technical, organizational]

**Key risks**: [Top 3 concerns]
**Key unknowns**: [What we need to discover]

**Type**: Business + Creative
**Template**: project
**Frameworks**: 5 Whys (mandatory), Six Hats (suggested)

→ Validate to start iterations?
```

### Report Emphasis
- Clear project vision and objectives
- Stakeholder map with roles
- Constraint summary and trade-offs
- Phased roadmap with milestones
- Risk register with mitigations
- MVP definition (what's in v1 vs later)

---

## Template: `research`

### Description
For technical research, vendor evaluation, or benchmarking. Focus on evidence-based comparison and clear recommendation.

### Default Configuration
| Setting | Value |
|---------|-------|
| Primary type | Technical |
| Secondary type | Analytical |
| Mandatory framework | Comparative Matrix |
| Suggested framework | Weighted Criteria, Scoring |
| Typical iterations | 3-5 |

### Framing Questions (Phase 1)

**Objective** (ask first):
1. What question are we trying to answer?
2. What decision will this research inform?

**Options** (ask second):
3. What options/alternatives are we considering? (or should we discover them?)
4. Are there any options already ruled out? Why?

**Criteria** (ask third):
5. What features/capabilities matter most?
6. What are deal-breakers (must-haves)?
7. How should we weight different criteria?

**Context** (ask last):
8. What's our current solution (if any)?
9. What constraints apply? (budget, integration, team skills)
10. How recent must the information be?

### Startup Brief Format

```markdown
## 📋 Research Brainstorm Brief

**Research question**: [Core question to answer]
**Decision it informs**: [What we'll decide based on this]

**Options to evaluate**:
1. [Option A]
2. [Option B]
3. [Option C]
(or: "Discover options during research")

**Evaluation criteria**:
- Must-have: [Deal-breakers]
- Important: [Key factors]
- Nice-to-have: [Bonus points]

**Current state**: [Existing solution if any]
**Constraints**: [Budget, integration, skills]
**Recency requirement**: [How current must info be]

**Type**: Technical + Analytical
**Template**: research
**Frameworks**: Comparative Matrix (mandatory), Scoring (suggested)

→ Validate to start iterations?
```

### Report Emphasis
- Research methodology documented
- Options discovered and evaluated
- Comparative analysis (matrix format)
- Scoring and ranking with rationale
- Clear recommendation with justification
- Implementation considerations for top choice

---

## Template Detection Logic

```
IF input mentions:
    "feature", "functionality", "add to app", "enhancement",
    "new capability", "user story", "implement"
    → Suggest: feature (confidence: high)

IF input mentions:
    "audit", "analyze", "evaluate", "review", "assess",
    "contract", "insurance", "compliance", "due diligence"
    → Suggest: audit (confidence: high)

IF input mentions:
    "new project", "start from scratch", "build from zero",
    "initiative", "launch", "create new", "greenfield"
    → Suggest: project (confidence: high)

IF input mentions:
    "research", "compare", "benchmark", "evaluate options",
    "which tool", "vendor selection", "technology choice",
    "alternatives", "what's best"
    → Suggest: research (confidence: high)

IF signals are mixed or weak:
    → Ask user: "This could be approached as [X] or [Y]. 
       Which feels more appropriate for what you need?"
    
IF no clear match:
    → Proceed without template (freeform brainstorming)
    → Offer templates as options after first iteration
```

---

## Template Customization

Users can request modifications at brief stage:

| Request | Action |
|---------|--------|
| "Focus more on UX" | Add UX-specific questions, suggest Creative type |
| "Add legal considerations" | Add compliance criteria, adjust frameworks |
| "Skip the business stuff" | Reduce Business questions, focus on Technical |
| "Make it faster" | Reduce questions to essentials, enable quick-mode behaviors |

Templates are starting points. Always adapt based on user's actual needs.

---

## Quick Mode Template Behavior

In `--quick` mode, templates are simplified:

| Aspect | Standard | Quick |
|--------|----------|-------|
| Framing questions | All (7-10) | Essential only (3-4) |
| Mandatory frameworks | As specified | Simplified or skipped |
| Brief detail | Full | Condensed |
| Iterations suggested | 4-6 | 2-3 |

**Quick mode framing questions** (all templates):
1. What's the core goal?
2. What are the key constraints?
3. How will you know it succeeded?

---

## Template Checklists (for Report Validation)

### Feature Template Checklist
- [ ] Application context identified
- [ ] User need clearly articulated
- [ ] Technical constraints captured
- [ ] Success metrics defined
- [ ] MoSCoW prioritization completed
- [ ] Implementation path outlined

### Audit Template Checklist
- [ ] Scope clearly defined (in/out)
- [ ] Evaluation criteria established and weighted
- [ ] Data/evidence gathered or identified
- [ ] SWOT or scoring framework applied
- [ ] Findings severity-ranked
- [ ] Recommendations are actionable

### Project Template Checklist
- [ ] Vision statement is clear and compelling
- [ ] Stakeholders identified with roles
- [ ] Constraints documented realistically
- [ ] Key risks identified with mitigations
- [ ] MVP scope defined
- [ ] Roadmap has concrete phases

### Research Template Checklist
- [ ] Research question is precise
- [ ] Options comprehensively identified
- [ ] Criteria defined and weighted
- [ ] Sources consulted and documented
- [ ] Comparison matrix completed
- [ ] Recommendation clearly justified
