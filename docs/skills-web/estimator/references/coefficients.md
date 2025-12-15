# Coefficients — Estimator

> Detailed grids and formulas for automatic coefficient calculation

---

## Effort Coefficient (coeff_effort)

### Auto-Detection Grid

| Client Type | Specs Clarity | coeff_effort | Rationale |
|-------------|---------------|--------------|-----------|
| Known | Clear | 0.85 | Optimal conditions, predictable |
| Known | Partial | 0.90 | Some unknowns, manageable |
| New | Clear | 0.90 | Client unknown but scope clear |
| New | Unclear | 0.95 | High uncertainty, buffer needed |

### Detection Logic

```
coeff_effort = BASE_COEFF

IF client is known (previous projects)
    BASE_COEFF = 0.85
ELSE
    BASE_COEFF = 0.90

IF specs are partial (missing details)
    coeff_effort += 0.05

IF specs are unclear (vague requirements)
    coeff_effort += 0.10

CLAMP(coeff_effort, 0.60, 1.00)
```

### Manual Override

User can force coefficient via:
- Flag at launch: `--coeff 0.80`
- Command during session: `modifier coeff 0.80`

---

## Risk Coefficient (coeff_risk)

### Auto-Detection Grid

| Risk Level | Conditions | coeff_risk | Buffer |
|------------|------------|------------|--------|
| Low | Known client + clear specs | 1.05 | +5% |
| Medium | Known client OR clear specs | 1.10 | +10% |
| High | New client + unclear specs | 1.15 | +15% |
| Critical | New client + unclear + tight deadline | 1.20 | +20% |

### Detection Logic

```
coeff_risk = 1.00

IF client is new
    coeff_risk += 0.05

IF specs are partial
    coeff_risk += 0.05

IF specs are unclear
    coeff_risk += 0.10

IF deadline is tight (< 2 months for > 100 JH)
    coeff_risk += 0.05

IF external dependencies (APIs, third parties)
    coeff_risk += 0.05

CLAMP(coeff_risk, 1.00, 1.30)
```

---

## Recette Rate by Project Type

| Project Type | recette_rate | Rationale |
|--------------|--------------|-----------|
| dev | 0.15 (15%) | Standard acceptance testing |
| refonte | 0.20 (20%) | Regression testing required |
| tma | 0.10 (10%) | Non-regression tests only |
| audit | 0.00 (0%) | No recette, deliverable is report |

### Recette Calculation

```
recette_jh = (sum_jh_lots_2_to_8) × recette_rate × coeff_effort × coeff_risk

# Lots 2-8 = Architecture, Backend, Frontend, Integrations, Conformité, Reprise, Tests
# Excludes: Cadrage (1), Recette (9), Formation (10), Documentation (11), Production (12)
```

---

## JH Range Calculations

### Base Formulas

```
JH_Low = sum(task_estimates) × 0.80
JH_Mid = sum(task_estimates) × coeff_effort
JH_High = sum(task_estimates) × 1.30
```

### Example Calculation

Given:
- Task estimates sum: 100 JH
- coeff_effort: 0.85
- coeff_risk: 1.10

```
JH_Low = 100 × 0.80 = 80 JH
JH_Mid = 100 × 0.85 = 85 JH
JH_High = 100 × 1.30 = 130 JH

# Add recette (15% for dev)
recette_base = (lots 2-8 sum, e.g., 70 JH)
recette_jh = 70 × 0.15 × 0.85 × 1.10 = 9.8 JH ≈ 10 JH

# Final totals
Total_Low = 80 + 8 = 88 JH
Total_Mid = 85 + 10 = 95 JH
Total_High = 130 + 13 = 143 JH
```

---

## Budget Scenarios

### Scenario Definitions

| Scenario | JH Base | Multiplier | Usage |
|----------|---------|------------|-------|
| Light | JH_Low | × 0.70 | MVP réduit, optionnel |
| Low | JH_Low | × 1.00 | Minimum viable |
| **Mid** | JH_Mid | × 1.00 | **Recommended** |
| High | JH_High | × 1.00 | Secured, risk-averse |

### Budget Calculation

```
budget_scenario = jh_scenario × tjm

# Example with TJM = 450€
budget_light = 88 × 0.70 × 450 = 27,720 €
budget_low = 88 × 450 = 39,600 €
budget_mid = 95 × 450 = 42,750 €
budget_high = 143 × 450 = 64,350 €
```

---

## Granularity Thresholds

| Total JH Estimate | Granularity | Precision |
|-------------------|-------------|-----------|
| < 30 JH | Macro | ±30% |
| 30-200 JH | Standard | ±20% |
| > 200 JH | Detailed | ±10% |

### Auto-Detection

```
# Estimate total from brief analysis (rough)
estimated_total = count_features × avg_jh_per_feature

IF estimated_total < 30
    granularity = "macro"
    lots_structure = "4_lots_merged"
ELSE IF estimated_total > 200
    granularity = "detailed"
    lots_structure = "12_lots_with_submodules"
ELSE
    granularity = "standard"
    lots_structure = "12_lots_standard"
```

---

## Adjustment Triggers

### When to Increase Coefficients

| Trigger | Adjustment |
|---------|------------|
| Complex integrations (>3 external APIs) | coeff_effort += 0.05 |
| Legacy code migration | coeff_risk += 0.10 |
| Tight deadline (< calculated duration × 0.7) | coeff_risk += 0.05 |
| New technology for team | coeff_effort += 0.05 |
| Regulatory requirements (RGPD, etc.) | coeff_risk += 0.05 |

### When to Decrease Coefficients

| Trigger | Adjustment |
|---------|------------|
| Reusable code available | coeff_effort -= 0.05 |
| Very clear mockups/specs | coeff_effort -= 0.05 |
| Similar project done recently | coeff_risk -= 0.05 |

---

## Coefficient Summary Table

For quick reference during estimation:

| Context | coeff_effort | coeff_risk | Combined Effect |
|---------|--------------|------------|-----------------|
| Best case (known + clear) | 0.85 | 1.05 | +5% buffer |
| Average case | 0.90 | 1.10 | +15% buffer |
| Worst case (new + unclear) | 0.95 | 1.20 | +30% buffer |
