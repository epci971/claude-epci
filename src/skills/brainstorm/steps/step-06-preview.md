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

@../references/breakpoint-formats.md

| Reference | Purpose |
|-----------|---------|
| breakpoint-formats.md | Preview implementation box (section #preview-implementation-box) |

## Protocol

### 1. Generate Preview via Agent planner

LANCE l'agent planner pour générer un preview de l'implémentation:

```
Task({
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
```

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

  Task({
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

AFFICHE la boîte Preview Implementation (section #preview-implementation-box de breakpoint-formats.md importé ci-dessus):

```
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
│ [P1] Complexité {level} → recommande {skill}                        │
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
```

Remplis les variables:
- `{complexity}`, `{tasks_count}`, `{risks_count}` depuis planner results
- `{title_1}`, `{complexity_1}`, `{title_2}`, `{complexity_2}` depuis tasks_preview
- `{triggered}`, `{risk_level}`, `{concerns}` depuis security_audit
- `{routing}`, `{routing_reason}` depuis routing recommendation
- Suggestions proactives P1/P2/P3 basées sur résultats

APPELLE AskUserQuestion:
```json
{
  "question": "Procéder à la génération du brief?",
  "header": "Preview",
  "multiSelect": false,
  "options": [
    { "label": "Générer brief (Recommended)", "description": "Créer outputs finaux" },
    { "label": "Ajuster scope", "description": "Modifier selon preview" },
    { "label": "Ajouter notes sécurité", "description": "Inclure recommandations sécurité" }
  ]
}
```

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
