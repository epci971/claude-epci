# Output Format — Estimator

> Complete template for the estimation document

---

## Document Structure Overview

```
Estimation — [Project Name]
├── 1. Context and Scope
│   ├── 1.1 Need Description
│   ├── 1.2 Scope
│   └── 1.3 Project Type
├── 2. Functional Breakdown
├── 3. Technical Stack
├── 4. Detailed Estimation
│   ├── 4.1 Lot 1 — Cadrage
│   ├── 4.2 Lot 2 — Backend
│   └── ... (per lot)
├── 5. Charge Summary
├── 6. Financial Valorization
│   ├── 6.1 Parameters
│   └── 6.2 Budget Scenarios
├── 7. Identified Risks
├── 8. Technical Registry
│   ├── 8.1 Assumptions
│   ├── 8.2 Stack Choices
│   └── 8.3 Out of Scope
└── 9. Conditions
```

---

## Complete Template

```markdown
# Estimation — [Project Name]

> Generated on [date] — Version 1.0
> Granularity: [Macro/Standard/Detailed]
> Reference: EST-[YYYY]-[NNN]

---

## 1. Context and Scope

### 1.1 Need Description

[Reformulation of the need in 3-5 lines, focusing on business objectives]

### 1.2 Scope

**Included**:
- [Element 1]
- [Element 2]
- [Element N]

**Excluded**:
- [Element 1]
- [Element 2]

**Assumptions**:
- [Assumption 1]
- [Assumption 2]

### 1.3 Project Type

- **Type**: [dev / refonte / tma / audit]
- **Granularity**: [macro / standard / detailed]
- **Client**: [Known / New]
- **Specs clarity**: [Clear / Partial / Unclear]

---

## 2. Functional Breakdown

| ID | Feature | Description | Priority | Module | Dependencies |
|----|---------|-------------|----------|--------|--------------|
| FCT-001 | [Name] | [Description] | MVP | [Module] | — |
| FCT-002 | [Name] | [Description] | MVP | [Module] | FCT-001 |
| FCT-003 | [Name] | [Description] | Should | [Module] | FCT-001, FCT-002 |
| ... | ... | ... | ... | ... | ... |

**Summary**:
- Total features: [N]
- MVP features: [N]
- Should features: [N]
- Could features: [N]

---

## 3. Technical Stack

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| Backend | Symfony | 7.x LTS | Robust, mature ecosystem, team expertise |
| Frontend | React | 18.x | Flexible, performant, wide adoption |
| Database | PostgreSQL | 16.x | Reliability, advanced features |
| Cache | Redis | 7.x | Performance, sessions |
| Infra | Docker | Latest | Portability, consistency |
| CI/CD | GitLab CI | — | Integrated with repo |

### Stack Justification

**Backend choice**: [Detailed justification for main backend choice]

**Frontend choice**: [Detailed justification for main frontend choice]

**Infrastructure**: [Justification for infrastructure choices]

---

## 4. Detailed Estimation

### 4.1 Lot 1 — Cadrage

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type | Criticality |
|------|-------------|--------|--------|---------|---------|------|-------------|
| Kick-off | Launch meeting | 0.5 | 1 | 1.5 | — | PO | Medium |
| Specs | Functional specs | 3 | 5 | 8 | — | PO | High |
| Validation | Sign-off | 1 | 2 | 3 | — | PO | High |
| **Subtotal** | | **4.5** | **8** | **12.5** | | | |

### 4.2 Lot 2 — Architecture

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type | Criticality |
|------|-------------|--------|--------|---------|---------|------|-------------|
| Analysis | Technical study | 2 | 3 | 5 | — | Back | High |
| DB Model | Schema design | 2 | 3 | 5 | — | Back | High |
| Setup | Environment setup | 2 | 3 | 4 | — | DevOps | Medium |
| **Subtotal** | | **6** | **9** | **14** | | | |

### 4.3 Lot 3 — Backend

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type | Criticality |
|------|-------------|--------|--------|---------|---------|------|-------------|
| Auth API | Authentication endpoints | 3 | 5 | 8 | FCT-001 | Back | High |
| [Module] API | [Description] | X | X | X | FCT-XXX | Back | [Level] |
| ... | ... | ... | ... | ... | ... | ... | ... |
| **Subtotal** | | **X** | **X** | **X** | | | |

[Continue for all lots...]

### 4.9 Lot 9 — Recette (Automatic)

| Task | Description | JH Low | JH Mid | JH High | FCT Ref | Type | Criticality |
|------|-------------|--------|--------|---------|---------|------|-------------|
| Preparation | Scenarios, environment | 2 | 3 | 4 | — | QA | Medium |
| Client testing | Testing support | 3 | 5 | 8 | — | QA | High |
| Bug fixes | Corrections | 4 | 6 | 10 | — | Back | High |
| Sign-off | Final acceptance | 1 | 2 | 2 | — | PO | High |
| **Subtotal** | | **10** | **16** | **24** | | | |

**Calculation**: 15% of lots 2-8 = [X] JH × coeff_effort × coeff_risk

---

## 5. Charge Summary

<!-- ESTIMATOR_DATA_START -->
| Lot | JH Low | JH Mid | JH High |
|-----|--------|--------|---------|
| 1. Cadrage | X | X | X |
| 2. Architecture | X | X | X |
| 3. Backend | X | X | X |
| 4. Frontend | X | X | X |
| 5. Intégrations | X | X | X |
| 6. Conformité | X | X | X |
| 7. Reprise | X | X | X |
| 8. Tests | X | X | X |
| 9. Recette | X | X | X |
| 10. Formation | X | X | X |
| 11. Documentation | X | X | X |
| 12. Production | X | X | X |
| **TOTAL** | **X** | **X** | **X** |
<!-- ESTIMATOR_DATA_END -->

---

## 6. Financial Valorization

### 6.1 Parameters

- **Applied TJM**: [XXX] €
- **Effort coefficient**: [0.XX] (client [known/new], specs [clear/partial/unclear])
- **Risk coefficient**: [1.XX]
- **Recette rate**: [XX]% ([project type])

### 6.2 Budget Scenarios

<!-- ESTIMATOR_BUDGET_START -->
| Scenario | JH | Amount HT | Context |
|----------|-----|-----------|---------|
| Light (option) | X | XX XXX € | Reduced MVP |
| Low | X | XX XXX € | Minimum viable |
| **Mid** | **X** | **XX XXX €** | **Recommended** |
| High | X | XX XXX € | Secured |
<!-- ESTIMATOR_BUDGET_END -->

**Recommendation**: Mid scenario — **XX XXX € HT**

### 6.3 Budget Distribution

```
Cadrage        ████░░░░░░ 10%
Architecture   ███░░░░░░░  8%
Backend        ████████░░ 30%
Frontend       ██████░░░░ 25%
Intégrations   ███░░░░░░░  8%
Recette        ████░░░░░░ 15%
Other          ██░░░░░░░░  4%
```

---

## 7. Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Medium | +X JH | [Mitigation action] |
| [Risk 2] | Low | +X JH | [Mitigation action] |
| [Risk 3] | High | +X JH | [Mitigation action] |

### Risk Analysis

- **Highest risk**: [Description and why]
- **Total buffer included**: [X] JH via coefficients

---

## 8. Technical Registry

### 8.1 Assumptions

- [Assumption 1]: [Detail]
- [Assumption 2]: [Detail]
- [Assumption 3]: [Detail]

### 8.2 Stack Choices Justified

| Choice | Alternative Considered | Reason for Selection |
|--------|------------------------|---------------------|
| Symfony | Django, Spring | Team expertise, ecosystem |
| PostgreSQL | MySQL | Advanced features needed |
| Docker | PaaS | Portability, cost control |

### 8.3 Explicitly Out of Scope

- [Element 1]: [Reason]
- [Element 2]: [Reason]
- [Element 3]: Will be addressed in phase 2

---

## 9. Conditions

### 9.1 Validity

This estimation is valid for **30 days** from the generation date.

### 9.2 Reference Documents

- [Document 1]: Brief client
- [Document 2]: Meeting notes
- [Document 3]: Brainstorm report

### 9.3 Revision Triggers

This estimation should be revised if:
- Scope changes significantly
- New constraints are identified
- More than 30 days have passed
- Client requirements clarified

---

## Appendix: Calculation Details

### Coefficient Application

```
Base JH sum: [X]
× coeff_effort ([0.XX]): [X]
× coeff_risk ([1.XX]): [X]
+ Recette ([XX]%): [X]
= Final JH: [X]

× TJM ([XXX] €): [XX XXX] €
```

### Scenario Calculations

```
Light: [X] JH × 0.70 × [TJM] = [XX XXX] €
Low:   [X] JH × 1.00 × [TJM] = [XX XXX] €
Mid:   [X] JH × 1.00 × [TJM] = [XX XXX] €
High:  [X] JH × 1.00 × [TJM] = [XX XXX] €
```

---

*Document generated by Estimator v1.0 — Ready for Propositor*
```

---

## Parseable Tags Reference

### Data Tags

| Tag | Content | Consumer |
|-----|---------|----------|
| `<!-- ESTIMATOR_DATA_START/END -->` | Charge summary table | Propositor |
| `<!-- ESTIMATOR_BUDGET_START/END -->` | Budget scenarios table | Propositor |

### Parsing Example (for Propositor)

```python
import re

def extract_estimator_data(markdown_content):
    # Extract charge data
    data_pattern = r'<!-- ESTIMATOR_DATA_START -->(.*?)<!-- ESTIMATOR_DATA_END -->'
    data_match = re.search(data_pattern, markdown_content, re.DOTALL)
    
    # Extract budget data
    budget_pattern = r'<!-- ESTIMATOR_BUDGET_START -->(.*?)<!-- ESTIMATOR_BUDGET_END -->'
    budget_match = re.search(budget_pattern, markdown_content, re.DOTALL)
    
    return {
        'charge_table': data_match.group(1) if data_match else None,
        'budget_table': budget_match.group(1) if budget_match else None
    }
```

---

## Output Language

The document is generated in the **user's input language**:

| User Language | Output Language | Headers Example |
|---------------|-----------------|-----------------|
| French | French | "Estimation", "Contexte", "Synthèse" |
| English | English | "Estimation", "Context", "Summary" |

### French Headers Reference

| English | French |
|---------|--------|
| Context and Scope | Contexte et périmètre |
| Need Description | Description du besoin |
| Functional Breakdown | Découpage fonctionnel |
| Technical Stack | Stack technique |
| Detailed Estimation | Estimation détaillée |
| Charge Summary | Synthèse de la charge |
| Financial Valorization | Valorisation financière |
| Identified Risks | Risques identifiés |
| Technical Registry | Registre technique |
| Conditions | Conditions |
