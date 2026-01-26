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

## Protocol

### 1. Generate @planner Preview

```python
@agent:planner (Sonnet)
  input: {
    brief: brief_v0,
    decisions: decisions,
    codebase_context: codebase_analysis,
    mode: "preview"  # Don't create full plan, just breakdown
  }
  output: {
    tasks_preview: [
      {title: "...", complexity: "SMALL", description: "..."},
      {title: "...", complexity: "STANDARD", description: "..."}
    ],
    estimated_complexity: "STANDARD",
    dependencies: [...],
    risks: [...]
  }
```

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

### 4. Run @security-auditor (if triggered)

```python
IF trigger_security_audit:
  @agent:security-auditor (Opus)
    input: {
      brief: brief_v0,
      decisions: decisions,
      codebase_security: codebase_analysis.security_patterns,
      mode: "preventive"  # Pre-implementation audit
    }
    output: {
      risk_level: "LOW|MEDIUM|HIGH",
      concerns: [...],
      recommendations: [...],
      owasp_relevant: [...]
    }
```

### 5. BREAKPOINT: Preview Results (if preview requested)

```typescript
@skill:epci:breakpoint-system
  type: plan-review
  title: "Implementation Preview"
  data: {
    metrics: {
      complexity: "{estimated}",
      tasks_count: {count},
      risks_count: {risks.length}
    },
    tasks_preview: [...],
    security_audit: {
      triggered: {true|false},
      risk_level: "{level}",
      concerns: [...]
    },
    routing: {
      recommended: "{/implement|/quick}",
      reason: "{complexity-based reasoning}"
    }
  }
  ask: {
    question: "Proceed with brief generation?",
    header: "Preview",
    options: [
      {label: "Generate brief (Recommended)", description: "Create final outputs"},
      {label: "Adjust scope", description: "Modify based on preview"},
      {label: "Add security notes", description: "Include security recommendations"}
    ]
  }
  suggestions: [
    {pattern: "complexity", text: "Complexity {level} -> recommend {skill}", priority: "P1"},
    {pattern: "security", text: "{concern} - will be noted in brief", priority: "P2"},
    {pattern: "risk", text: "Consider {mitigation} for {risk}", priority: "P3"}
  ]
```

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
