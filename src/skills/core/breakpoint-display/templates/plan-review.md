# Template: Plan Review Breakpoint

## Overview

Breakpoint pour revue de plan avec métriques, validations agents, et preview prochaine phase.

**Usage:** `/epci` BP1 (Phase 1), `/epci` BP2 (Phase 2)

## Data Structure

```typescript
{
  type: "plan-review",
  title: "{TITLE}",
  data: {
    flags: {
      // Active flags with sources
      active: ["--think", "--uc"],
      sources: {
        "--think": "auto: 12 files",
        "--uc": "auto: context 78%"
      }
    },
    metrics: {
      complexity: "{CATEGORY}",
      complexity_score: {number},
      files_impacted: {number},
      time_estimate: "{TIME}",
      risk_level: "{LEVEL}",
      risk_description: "{TEXT}"
    },
    validations: {
      // Agent validations
      plan_validator: {
        verdict: "{VERDICT}",
        completeness: "{STATUS}",
        consistency: "{STATUS}",
        feasibility: "{STATUS}",
        quality: "{STATUS}"
      },
      code_reviewer: {
        verdict: "{VERDICT}",
        summary: "{TEXT}"
      },
      security_auditor: {
        verdict: "{VERDICT}"
      },
      qa_reviewer: {
        verdict: "{VERDICT}"
      }
    },
    skills_loaded: ["{skill1}", "{skill2}", ...],
    preview_next_phase: {
      phase_name: "{NAME}",
      tasks: [
        {title: "{TASK}", time: "{TIME}"},
        ...
      ],
      remaining_tasks: {number}
    },
    feature_doc_path: "{PATH}",
    // For Phase 2 only:
    implementation_metrics: {
      tasks_completed: {number},
      tasks_total: {number},
      tests_count: {number},
      tests_status: "{STATUS}",
      coverage: {number},
      deviations: "{STATUS}"
    }
  },
  ask: {
    question: "{QUESTION}",
    header: "{HEADER}",
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
}
```

## Display Format

Uses reusable components:
- @components/flags-block.md (if flags present)
- @components/metrics-block.md
- @components/validations-block.md
- @components/preview-block.md

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  {TITLE}                                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [FLAGS BLOCK - if present]                                          │
│                                                                     │
│ [METRICS BLOCK]                                                     │
│                                                                     │
│ [VALIDATIONS BLOCK]                                                 │
│                                                                     │
│ [PREVIEW BLOCK]                                                     │
│                                                                     │
│ 🔗 Feature Document: {path}                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Then invoke `AskUserQuestion` with options.

## Example: Phase 1 Breakpoint (/epci BP1)

```typescript
{
  type: "plan-review",
  title: "PHASE 1 — Plan Validé",
  data: {
    flags: {
      active: ["--think", "--uc"],
      sources: {
        "--think": "auto: 12 files",
        "--uc": "auto: context 78%"
      }
    },
    metrics: {
      complexity: "STANDARD",
      complexity_score: 6.2,
      files_impacted: 12,
      time_estimate: "2-3h",
      risk_level: "MEDIUM",
      risk_description: "Auth changes require careful testing"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "OK",
        consistency: "OK",
        feasibility: "OK",
        quality: "OK"
      }
    },
    skills_loaded: ["testing-strategy", "php-symfony", "security-patterns"],
    preview_next_phase: {
      phase_name: "Phase 2: Implementation",
      tasks: [
        {title: "Create User entity", time: "30min"},
        {title: "Implement auth service", time: "1h"},
        {title: "Add tests", time: "45min"}
      ],
      remaining_tasks: 5
    },
    feature_doc_path: "docs/features/auth-oauth.md"
  },
  ask: {
    question: "Comment souhaitez-vous procéder ?",
    header: "🚀 Phase 2",
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 2 Implémentation"},
      {label: "Modifier plan", description: "Réviser plan avant implémentation"},
      {label: "Voir détails", description: "Afficher Feature Document complet"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
}
```

## Example: Phase 2 Breakpoint (/epci BP2)

```typescript
{
  type: "plan-review",
  title: "PHASE 2 — Code Implémenté",
  data: {
    metrics: {
      complexity: "STANDARD",
      complexity_score: 6.2,
      files_impacted: 12,
      time_estimate: "2-3h (actual: 2h15)",
      risk_level: "MEDIUM",
      risk_description: "All tests passing"
    },
    implementation_metrics: {
      tasks_completed: 8,
      tasks_total: 8,
      tests_count: 24,
      tests_status: "PASSING",
      coverage: 87,
      deviations: "NONE"
    },
    validations: {
      code_reviewer: {
        verdict: "APPROVED",
        summary: "Code quality excellent, naming conventions respected"
      },
      security_auditor: {
        verdict: "APPROVED"
      },
      qa_reviewer: {
        verdict: "APPROVED"
      }
    },
    preview_next_phase: {
      phase_name: "Phase 3: Finalization",
      tasks: [
        {title: "Commit structuré", time: "5min"},
        {title: "Génération documentation", time: "10min"},
        {title: "Préparation PR", time: "5min"}
      ],
      remaining_tasks: 0
    },
    feature_doc_path: "docs/features/auth-oauth.md"
  },
  ask: {
    question: "Comment souhaitez-vous procéder ?",
    header: "🚀 Phase 3",
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 3 Finalization"},
      {label: "Revoir code", description: "Examiner implémentation en détail"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
}
```

## Token Savings

**Avant:** ~350 tokens (ASCII box + validations + preview)
**Après:** ~90 tokens (skill invocation)
**Gain:** 74%
