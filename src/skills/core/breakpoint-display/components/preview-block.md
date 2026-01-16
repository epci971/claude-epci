# Component: Preview Block

## Overview

Composant réutilisable pour afficher preview des tâches de la prochaine phase.

**Usage:** `plan-review`

## Input Structure

```typescript
{
  phase_name: "{NAME}",
  tasks: [
    {title: "{TITLE}", time: "{TIME}"},
    ...
  ],
  remaining_tasks: {number}
}
```

## Display Format

```
│ 📋 PREVIEW {PHASE_NAME}                                             │
│ ├── Tâche 1: {task_1_title} ({task_1_time})                       │
│ ├── Tâche 2: {task_2_title} ({task_2_time})                       │
│ ├── Tâche 3: {task_3_title} ({task_3_time})                       │
│ └── ... ({remaining_tasks} tâches restantes)                       │
```

## Example: Phase 2 Preview

```typescript
Input:
{
  phase_name: "PHASE 2",
  tasks: [
    {title: "Create User entity", time: "30min"},
    {title: "Implement auth service", time: "1h"},
    {title: "Add tests", time: "45min"}
  ],
  remaining_tasks: 5
}

Output:
│ 📋 PREVIEW PHASE 2                                                  │
│ ├── Tâche 1: Create User entity (30min)                           │
│ ├── Tâche 2: Implement auth service (1h)                          │
│ ├── Tâche 3: Add tests (45min)                                    │
│ └── ... (5 tâches restantes)                                       │
```

## Example: Phase 3 Preview

```typescript
Input:
{
  phase_name: "PHASE 3",
  tasks: [
    {title: "Commit structuré", time: "5min"},
    {title: "Génération documentation", time: "10min"},
    {title: "Préparation PR", time: "5min"}
  ],
  remaining_tasks: 0
}

Output:
│ 📋 PREVIEW PHASE 3                                                  │
│ ├── Tâche 1: Commit structuré (5min)                              │
│ ├── Tâche 2: Génération documentation (10min)                     │
│ └── Tâche 3: Préparation PR (5min)                                │
```

## Variation: Show Top N Tasks

If more than 5 tasks, show only first 3 + remaining count:

```
│ 📋 PREVIEW PHASE 2                                                  │
│ ├── Tâche 1: {task_1} ({time})                                    │
│ ├── Tâche 2: {task_2} ({time})                                    │
│ ├── Tâche 3: {task_3} ({time})                                    │
│ └── ... (12 tâches restantes)                                      │
```
