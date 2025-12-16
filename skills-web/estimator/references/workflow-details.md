# Workflow Details — Estimator

> Complete specifications for each phase and checkpoint format

---

## Phase 1: Qualification

### Objective
Understand the project context and calibrate estimation parameters.

### Input Analysis

Estimator accepts inputs from:

| Source | Priority | Data Extracted |
|--------|----------|----------------|
| `brainstormer` output | ⭐ Ideal | Context, decisions, features |
| `code-promptor` output | ⭐ Ideal | Technical specs, constraints |
| `resumator` output | Good | Requirements from meetings |
| Client specifications | Good | Formal requirements |
| Free text brief | Acceptable | To be structured |

### Clarification Questions

Ask maximum 3 questions if brief is clear. Standard questions:

1. **Project type**: New development / Evolution / Refonte / TMA / Audit?
2. **Technical context**: Existing stack? Specific constraints?
3. **Client profile**: Known or new? Specs clarity level?

### Auto-Detection Logic

```
IF brief mentions "migration" OR "refonte" OR "legacy"
    → type = refonte
    → coeff_risk += 0.05

IF brief mentions "maintenance" OR "TMA" OR "support"
    → type = tma
    → recette_rate = 0.10

IF brief mentions "audit" OR "review" OR "diagnostic"
    → type = audit
    → recette_rate = 0.00

IF total_jh_estimate < 30
    → granularity = macro
ELSE IF total_jh_estimate > 200
    → granularity = detailed
ELSE
    → granularity = standard
```

### Checkpoint 1 Format

```markdown
📍 Checkpoint 1 — Project Understanding

**My understanding**:
[Brief reformulation in 3-5 lines]

**Detected parameters**:
- Project type: [dev/refonte/tma/audit]
- Granularity: [macro/standard/detailed]
- Effort coefficient: [0.xx] (client [known/new], specs [clear/partial/unclear])
- Risk coefficient: [1.xx]

**Identified constraints**:
- [Constraint 1]
- [Constraint 2]

**Options:**
→ `valider` — Proceed to functional breakdown
→ `modifier [parameter]` — Adjust a parameter
→ `question [topic]` — Clarify a point
```

---

## Phase 2: Functional Breakdown

### Objective
Identify ALL features — explicit from brief AND implicit from best practices.

### Feature Extraction Process

1. **Explicit features**: Directly mentioned in brief
2. **Implicit features**: Standard components often forgotten
   - Authentication & authorization
   - User management
   - Logging & monitoring
   - Error handling
   - Admin interface
   - Data export
   - Notifications
   - Search functionality

### Feature Table Format

| ID | Feature | Description | Priority | Module | Dependencies |
|----|---------|-------------|----------|--------|--------------|
| FCT-001 | Authentication | OAuth2 secure login | MVP | Auth | — |
| FCT-002 | Dashboard | User dashboard | MVP | Core | FCT-001 |
| FCT-003 | PDF Export | Report generation | Should | Reports | FCT-002 |

### Priority Definitions

| Priority | Meaning | Inclusion |
|----------|---------|-----------|
| **MVP** | Essential for launch | Always included |
| **Should** | Important but not blocking | Included in standard scenario |
| **Could** | Nice to have | Included in high scenario only |

### AI Suggestions Format

```markdown
💡 **AI Suggestions**:
- Have you considered [implicit feature]?
- Module [X] might require [external dependency]
- [Feature Y] often needs [related feature Z]

❓ **Pending questions**:
- Is [feature] mandatory or optional?
- What's the expected user volume?
```

### Checkpoint 2 Format

```markdown
📍 Checkpoint 2 — Functional Breakdown

I identified [N] features across [X] modules:

| ID | Feature | Priority | Module |
|----|---------|----------|--------|
| FCT-001 | ... | MVP | ... |
| FCT-002 | ... | MVP | ... |
| ... | ... | ... | ... |

**Module summary**:
- [Module 1]: [N] features
- [Module 2]: [N] features

💡 **AI Suggestions**:
- [Suggestion 1]
- [Suggestion 2]

❓ **Pending questions**:
- [Question 1]?
- [Question 2]?

**Options:**
→ `valider` — Proceed to task evaluation
→ `ajouter [feature]` — Add a feature
→ `modifier FCT-xxx` — Edit a feature
→ `supprimer FCT-xxx` — Remove a feature
→ `question [topic]` — Clarify before validating
```

---

## Phase 3: Task Evaluation

### Objective
Estimate each task with Low/Mid/High ranges.

### Lot Structure Selection

| Granularity | Lots | Structure |
|-------------|------|-----------|
| **Macro** | 4 | Cadrage, Développement, Recette, Déploiement |
| **Standard** | 12 | Full 12-lot structure |
| **Detailed** | 12+ | 12 lots + Backend/Frontend sub-modules |

### Task Table Format

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type | Criticality |
|------|-------------|--------|--------|---------|---------|------|-------------|
| Setup | Init repo, CI/CD | 2 | 3 | 4 | — | DevOps | Medium |
| API Auth | Auth endpoints | 3 | 4 | 6 | FCT-001 | Back | High |

### Calculation Formulas

```
JH_Low = Sum(tasks) × 0.8
JH_Mid = Sum(tasks) × coeff_effort
JH_High = Sum(tasks) × 1.3

Recette_JH = (JH lots 2-8) × recette_rate × coeff_effort × coeff_risk
```

### Recette Rates by Project Type

| Type | Rate | Justification |
|------|------|---------------|
| dev | 15% | Standard |
| refonte | 20% | Regression risks |
| tma | 10% | Non-regression tests |
| audit | 0% | Deliverable = report |

### Checkpoint 3 Format

```markdown
📍 Checkpoint 3 — Detailed Estimation

**Summary by lot**:

| Lot | JH Low | JH Mid | JH High |
|-----|--------|--------|---------|
| Cadrage | X | X | X |
| Backend | X | X | X |
| Frontend | X | X | X |
| ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** |

**Applied coefficients**:
- Effort: [0.xx]
- Risk: [1.xx]

⚠️ **Attention points**:
- [Task X]: High uncertainty, wide range
- [Lot Y]: External dependency not confirmed

**Options:**
→ `valider` — Proceed to valorization
→ `ajuster-jh [ID] [value]` — Modify a JH
→ `recalculer` — Recalculate after modifications
→ `détailler [lot]` — View lot details
```

---

## Phase 4: Valorization & Synthesis

### Objective
Convert JH to budget and document all assumptions.

### TJM Grid

| Profile | TJM | Usage |
|---------|-----|-------|
| Junior Dev | 350-400€ | Simple tasks |
| Confirmed Dev | 450€ (default) | Standard development |
| Senior Dev | 550-650€ | Architecture, complex |
| Project Manager | 500-600€ | Coordination |

### Budget Scenarios

| Scenario | Calculation | Usage |
|----------|-------------|-------|
| Light | JH_Low × 0.7 × TJM | Reduced MVP (optional) |
| Low | JH_Low × TJM | Minimum viable |
| **Mid** | JH_Mid × TJM | **Recommended** |
| High | JH_High × TJM | Secured |

### Technical Registry Contents

1. **Assumptions made**
   - [Assumption 1]
   - [Assumption 2]

2. **Identified risks**
   - [Risk 1]: Impact +X JH, Mitigation: [action]
   - [Risk 2]: Impact +X JH, Mitigation: [action]

3. **Stack choices justified**
   - Backend: [Technology] — [Reason]
   - Frontend: [Technology] — [Reason]

4. **Explicitly out of scope**
   - [Element 1]
   - [Element 2]

### Final Checkpoint Format

```markdown
📍 Final Checkpoint — Complete Estimation

## Budget Summary

| Scenario | JH | Amount HT |
|----------|-----|-----------|
| Light (option) | X | XX XXX € |
| Low | X | XX XXX € |
| **Mid** | **X** | **XX XXX €** |
| High | X | XX XXX € |

**Recommendation**: Mid scenario — **XX XXX € HT**

## Technical Registry
[Assumptions, risks, stack choices summary]

## Validity
- Valid for: 30 days
- Revision if: Scope change

**Options:**
→ `exporter` — Generate final document
→ `modifier [section]` — Return to a section
→ `propositor` — Chain to commercial proposal
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Incomplete brief | Ask clarification questions |
| Missing feature references | Alert and offer to add |
| Incoherent totals | Recalculate and alert |
| User inactive | Gentle reminder after 2 messages |
| Conflicting requirements | Present for user arbitration |
