---
name: step-06-preview
description: Generate implementation preview and optional security audit
prev_step: steps/step-05-breakpoint-finish.md
next_step: steps/step-07-validate.md
conditional_next:
  - condition: "Adjust scope"
    step: steps/step-04-iteration.md
  - condition: "Cancel"
    step: null
---

# Step 06: Preview

> Generate implementation preview and optional security audit.

## Trigger

- Previous step: `step-05-breakpoint-finish.md` completed
- User selected "Generate outputs" or "Preview first"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | Session state | Yes |
| `decisions[]` | Session state | Yes |
| `ems` | Session state | Yes |
| `codebase_analysis` | Session state | No |
| `preview_requested` | Session state | No |
| `--no-security` flag | From step-00 | No |

## Reference Files

*(Breakpoint templates are inline in this file)*

## Protocol

### 1. Generate Preview via Agent planner

LANCE l'agent planner pour générer un preview de l'implémentation:

LANCE Task({
  subagent_type: "planner",
  model: "sonnet",
  prompt: "Génère un preview d'implémentation pour ce brainstorm.
    Brief: {brief_v0}
    Décisions: {decisions}
    Contexte codebase: {codebase_analysis}
    Mode: preview (pas de plan complet, juste découpage)

    Retourne JSON:
    {
      tasks_preview: [
        {title: '...', complexity: 'SMALL', description: '...'},
        {title: '...', complexity: 'STANDARD', description: '...'}
      ],
      estimated_complexity: 'STANDARD',
      dependencies: [...],
      risks: [...]
    }"
})

ATTENDS le résultat avant de continuer.

### 2. Display Preview (if requested)

```markdown
## Implementation Preview

**Estimated Complexity**: {TINY|SMALL|STANDARD|LARGE}

### Tasks Breakdown
| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | {title} | {complexity} | - |
| 2 | {title} | {complexity} | T1 |
| 3 | {title} | {complexity} | T1, T2 |

### Identified Risks
- {risk_1}
- {risk_2}

### Recommended Approach
{routing recommendation: /implement or /quick}
```

### 3. Check Security Audit Trigger

```
security_patterns = [
  "**/auth/**",
  "**/security/**",
  "**/permissions/**",
  "login", "password", "token", "jwt", "oauth",
  "session", "csrf", "xss", "injection"
]

IF NOT --no-security flag:
  IF brief contains security_patterns OR codebase_analysis.security_patterns:
    trigger_security_audit = true
```

### 4. Run Security Audit via Agent (if triggered)

```
IF trigger_security_audit:
  LANCE l'agent security-auditor:

  LANCE Task({
    subagent_type: "security-auditor",
    model: "opus",
    prompt: "Effectue un audit de sécurité préventif pour ce brainstorm.
      Brief: {brief_v0}
      Décisions: {decisions}
      Patterns sécurité codebase: {codebase_analysis.security_patterns}
      Mode: preventive (audit pré-implémentation)

      Retourne JSON:
      {
        risk_level: 'LOW|MEDIUM|HIGH',
        concerns: [...],
        recommendations: [...],
        owasp_relevant: [...]
      }"
  })

  ATTENDS le résultat avant de continuer.
```

### 5. BREAKPOINT: Preview Results (OBLIGATOIRE si preview demandé)

AFFICHE cette boîte:

┌─────────────────────────────────────────────────────────────────────┐
│ 👁️ PREVIEW IMPLÉMENTATION                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ MÉTRIQUES                                                           │
│ • Complexité estimée: {complexity}                                  │
│ • Nombre de tâches: {tasks_count}                                   │
│ • Risques identifiés: {risks_count}                                 │
│                                                                     │
│ DÉCOUPAGE TÂCHES                                                    │
│ | # | Tâche | Complexité | Dépendances |                            │
│ |---|-------|------------|-------------|                            │
│ | 1 | {title_1} | {complexity_1} | - |                              │
│ | 2 | {title_2} | {complexity_2} | T1 |                             │
│                                                                     │
│ AUDIT SÉCURITÉ                                                      │
│ • Déclenché: {triggered}                                            │
│ • Niveau risque: {risk_level}                                       │
│ • Préoccupations: {concerns}                                        │
│                                                                     │
│ ROUTING RECOMMANDÉ                                                  │
│ → {routing}                                                         │
│ → Raison: {routing_reason}                                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTIONS PROACTIVES                                              │
│ [P1] Complexité {complexity} → recommande {skill}                   │
│ [P2] {concern} — sera noté dans le brief                            │
│ [P3] Considère {mitigation} pour {risk}                             │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─ Options ──────────────────────────────────────────────────────┐ │
│ │  [A] Générer brief (Recommended) — Créer outputs finaux        │ │
│ │  [B] Ajuster scope — Modifier selon preview                    │ │
│ │  [C] Ajouter notes sécurité — Inclure recommandations          │ │
│ │  [?] Autre réponse...                                          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

Remplis les variables:
- `{complexity}`: Estimated overall complexity (`STANDARD`, etc.)
- `{tasks_count}`: Number of tasks in breakdown
- `{risks_count}`: Number of identified risks
- `{title_1}`, `{complexity_1}`: First task title and complexity
- `{title_2}`, `{complexity_2}`: Second task title and complexity
- `{triggered}`: Security audit triggered (`Yes` or `No`)
- `{risk_level}`: Security risk level (`LOW`, `MEDIUM`, `HIGH`)
- `{concerns}`: Security concerns list
- `{routing}`: Recommended skill (`/implement` or `/quick`)
- `{routing_reason}`: Routing justification
- `{skill}`: Recommended skill for P1
- `{concern}`: Specific concern for P2
- `{mitigation}`, `{risk}`: Mitigation suggestion for P3

APPELLE AskUserQuestion({
  questions: [{
    question: "Procéder à la génération du brief?",
    header: "Preview",
    multiSelect: false,
    options: [
      { label: "Générer brief (Recommended)", description: "Créer outputs finaux" },
      { label: "Ajuster scope", description: "Modifier selon preview" },
      { label: "Ajouter notes sécurité", description: "Inclure recommandations sécurité" }
    ]
  }]
})

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 6. Update Brief with Preview Insights

```
IF preview insights available:
  - Add complexity estimate to brief
  - Add security notes if audit triggered
  - Add risks section
  - Add routing recommendation
```

### 7. Prepare Validation Context

```json
{
  "preview_complete": true,
  "complexity_estimate": "{TINY|SMALL|STANDARD|LARGE}",
  "security_audit": {
    "triggered": true,
    "risk_level": "MEDIUM",
    "recommendations": [...]
  },
  "routing_recommendation": "{/implement|/quick}",
  "tasks_preview": [...]
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `preview_complete` | Session state |
| `complexity_estimate` | Session state |
| `security_audit` | Session state |
| `routing_recommendation` | Session state |
| `tasks_preview` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Continue to validation | → `step-07-validate.md` |
| Adjust scope | → `step-04-iteration.md` |
| Cancel | → Exit with summary |

## Error Handling

| Error | Resolution |
|-------|------------|
| @planner unavailable | Generate basic breakdown |
| @security-auditor unavailable | Note in brief, proceed |
| Preview timeout | Proceed without full preview |
