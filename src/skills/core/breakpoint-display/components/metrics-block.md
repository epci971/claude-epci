# Component: Metrics Block

## Overview

Composant réutilisable pour afficher métriques de complexité, fichiers, temps, risque.

**Usage:** `plan-review`, `analysis`

## Input Structure

```typescript
{
  complexity: "{CATEGORY}",
  complexity_score: {number},
  files_impacted: {number},
  time_estimate: "{TIME}",
  risk_level: "{LOW|MEDIUM|HIGH}",
  risk_description: "{TEXT}"
}
```

## Display Format

```
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: {complexity} (score: {score})                      │
│ ├── Fichiers impactés: {files}                                     │
│ ├── Temps estimé: {time}                                           │
│ └── Risque: {risk_level} {risk_description}                        │
```

## Example

```typescript
Input:
{
  complexity: "STANDARD",
  complexity_score: 6.2,
  files_impacted: 12,
  time_estimate: "2-3h",
  risk_level: "MEDIUM",
  risk_description: "Auth changes require careful testing"
}

Output:
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: STANDARD (score: 6.2)                              │
│ ├── Fichiers impactés: 12                                          │
│ ├── Temps estimé: 2-3h                                             │
│ └── Risque: MEDIUM Auth changes require careful testing            │
```

## Variations

### With Implementation Metrics (Phase 2)

```typescript
{
  ...base_metrics,
  implementation_metrics: {
    tasks_completed: {number},
    tasks_total: {number},
    tests_count: {number},
    tests_status: "{STATUS}",
    coverage: {number},
    deviations: "{STATUS}"
  }
}
```

Display:
```
│ 📊 MÉTRIQUES                                                        │
│ ├── Complexité: STANDARD (score: 6.2)                              │
│ ├── Fichiers impactés: 12                                          │
│ ├── Temps estimé: 2-3h (actual: 2h15)                              │
│ ├── Risque: MEDIUM All tests passing                               │
│ │                                                                   │
│ ├── Tâches: 8/8 complétées                                         │
│ ├── Tests: 24 PASSING                                              │
│ ├── Coverage: 87%                                                  │
│ └── Déviations: NONE                                               │
```
