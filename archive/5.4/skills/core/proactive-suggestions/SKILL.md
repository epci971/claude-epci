---
name: proactive-suggestions
description: >-
  Generates and manages proactive suggestions during EPCI workflow.
  Auto-invoke when: /epci reaches BP2 (post-Phase 2), code review findings
  need transformation, or /brainstorm uses --suggest flag (Discovery Mode).
  Do NOT load for: /quick (no formal breakpoints), or when suggestions
  are explicitly disabled via learning preferences.
---

# Proactive Suggestions (F06)

## Overview

Transforms code review findings and pattern detection results into prioritized,
actionable suggestions that learn from user preferences.

## Integration Points

| Phase | Trigger | Suggestion Types |
|-------|---------|------------------|
| BP1 (Post-Plan) | Plan validated | Architecture patterns, documentation |
| BP2 (Post-Code) | Code reviewed | Security, performance, quality |

## Suggestion Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│  Findings   │────▶│  Suggestion  │────▶│   Breakpoint   │
│  (Sources)  │     │   Engine     │     │    Display     │
└─────────────┘     └──────────────┘     └────────────────┘
      │                    │                     │
      ▼                    ▼                     ▼
 @code-reviewer      Score & Filter        💡 Section
 @security-auditor   Learning prefs        [Actions]
 @qa-reviewer        Prioritize P1>P2>P3
 PatternDetector
```

## Priority Levels

| Priority | Icon | Category | Examples |
|----------|------|----------|----------|
| **P1** | 🔒 | Security | Input validation, SQL injection, XSS |
| **P2** | ⚡/🧹 | Performance/Quality | N+1 query, god class, long method |
| **P3** | 🧹 | Style/Optimization | Magic numbers, dead code |

## Pattern Catalog

### Security (P1) - Critical
- `input-not-validated` - User input without validation
- `sql-injection` - SQL string concatenation
- `xss-vulnerability` - Unescaped output
- `csrf-missing` - Form without CSRF token
- `auth-missing` - Endpoint without auth check

### Performance (P2) - Important
- `n-plus-one-query` - Query in loop
- `missing-index` - Query on non-indexed column
- `large-payload` - Response without pagination
- `no-cache` - Repeated query without cache

### Quality (P2-P3) - Normal/Minor
- `god-class` - Class > 500 LOC
- `long-method` - Method > 50 LOC
- `magic-numbers` - Hardcoded constants
- `dead-code` - Unreachable code
- `duplicate-code` - Similar blocks > 20 LOC

## Scoring Algorithm

```python
score = base_score * impact_multiplier * preference_multiplier

where:
  base_score = PRIORITY_WEIGHTS[priority] / 100  # P1=1.0, P2=0.7, P3=0.5
  impact_multiplier = SEVERITY_IMPACT[severity]  # critical=1.5, minor=0.7
  preference_multiplier = 0.5 + (learning_score * 0.5)  # Range: 0.5-1.0
```

Suggestions with score < 0.3 are filtered out.

## User Actions

| Action | Effect | Learning Impact |
|--------|--------|-----------------|
| **[Accepter]** | Apply suggestion (if auto-fixable) | +1 preference |
| **[Voir détails]** | Show full explanation | Neutral |
| **[Ignorer]** | Skip for this session | Neutral |
| **[Ne plus suggérer]** | Disable pattern permanently | -∞ (blocklist) |

## Breakpoint Display Format

### Full Format (default)

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ ├── [P1] 🔒 Input non validé (path:line)                           │
│ │   └── Suggestion: Ajouter validation                             │
│ ├── [P2] ⚡ N+1 Query (path:line)                                   │
│ │   └── Suggestion: JOIN FETCH                                      │
│ └── [P3] 🧹 Magic number (path:line)                               │
│     └── Actions: [Accepter tout] [Voir détails] [Ignorer]          │
```

### Compact Format (token optimization)

```
💡 Suggestions: [P1] 🔒 Input validation | [P2] ⚡ N+1 query | [P3] 🧹 Magic num
```

## Learning Integration (F08)

Preferences stored in `.project-memory/learning/preferences.json`:

```json
{
  "suggestion_feedback": {
    "input-not-validated": {
      "accepted": 5,
      "rejected": 1,
      "acceptance_rate": 0.83
    }
  },
  "disabled_suggestions": ["magic-numbers"],
  "settings": {
    "suggestion_threshold": 0.3,
    "max_suggestions_per_breakpoint": 5
  }
}
```

## Hook Integration

The `post-phase-2-suggestions.py` hook automatically:
1. Collects findings from subagent reviews
2. Runs PatternDetector on changed files
3. Generates scored suggestions
4. Returns formatted output for breakpoint

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `suggestion_threshold` | 0.3 | Minimum score to display |
| `max_suggestions_per_breakpoint` | 5 | Max suggestions shown |
| `learning_enabled` | true | Enable preference learning |

## Usage Example

```python
from project_memory.suggestion_engine import SuggestionEngine, Finding

engine = SuggestionEngine(memory_dir=".project-memory")

findings = [
    Finding(
        pattern_id="input-not-validated",
        file_path="src/Controller/UserController.php",
        line_number=42,
        severity="critical",
    )
]

suggestions = engine.generate_suggestions(findings)
output = engine.format_for_breakpoint(suggestions)
print(output)
```

## Dependencies

- **F04 Project Memory** - Pattern and preference storage
- **F08 Continuous Learning** - Preference scoring and adaptation
- **F03 Enriched Breakpoints** - Display templates

---

## Discovery Mode (v5.3.7)

Mode spécialisé pour `/brainstorm` activé via le flag `--suggest`.
Génère des suggestions proactives pendant la phase de découverte de features.

### Activation

```bash
/brainstorm "feature description" --suggest
# Active les suggestions proactives durant le brainstorm
```

### Integration Points

| Point | Phase | Trigger | Suggestion Type |
|-------|-------|---------|-----------------|
| **Architecture Patterns** | Phase 1 | Après @Explore | Patterns architecture recommandés |
| **Weak-Axes Patterns** | Phase 2 | weak_axes[] non-vide | Techniques pour renforcer axes faibles |
| **Pivot Strategies** | Phase 2 | delta < 3 sur 2 itérations | Stratégies de pivot |
| **Convergence Strategies** | Phase 2 | EMS = 50 | Frameworks de décision (MoSCoW, RICE) |
| **Brief Quality** | Phase 2/3 | EMS ≥ 70 | Validation complétude brief |
| **Intelligent Questions** | Phase 2 | Génération questions | Questions basées sur historique |
| **Security Patterns** | Phase 2 | Keywords (auth, payment) | Patterns OWASP préventifs |
| **Effort Estimation** | Phase 3 | Calcul effort | Calibration basée historique |
| **Brief Validation** | Phase 3 | Après génération brief | Validation structure PRD |

### Discovery Pattern Catalog

| Pattern ID | Trigger | Suggestion | Priority |
|------------|---------|------------|----------|
| `arch-microservices` | files > 10 + distributed keywords | "Consider microservices architecture" | P2 |
| `arch-modular` | files > 5, single domain | "Consider modular monolith" | P2 |
| `security-early` | auth/payment/PII keywords | "Flag for @security-auditor review" | P1 |
| `scope-large` | complexity L/XL | "Consider phased approach via /decompose" | P2 |
| `scope-vague` | EMS clarity < 40 | "Add concrete success criteria" | P1 |
| `ems-stagnant` | delta < 3 × 2 iter | "Try pivot: reframe problem" | P2 |
| `coverage-low` | Coverage axis < 40 | "Use Six Hats for perspectives" | P2 |
| `decisions-pending` | Decisions axis < 40 | "Apply MoSCoW prioritization" | P2 |
| `actionability-low` | Actionability axis < 40 | "Break into smaller user stories" | P2 |
| `similar-feature` | Feature match > 0.7 | "Reuse patterns from {feature}" | P3 |
| `api-integration` | API/integration keywords | "Document contract early" | P2 |
| `data-migration` | migration/data keywords | "Plan rollback strategy" | P1 |

### Suggestion Format for Breakpoints

**Champ `suggestions[]` ajouté aux types de breakpoint:**

```yaml
@skill:breakpoint-display
  type: ems-status
  data:
    # ... existing fields ...
    suggestions:
      - pattern: "coverage-low"
        text: "Coverage à 35% — essayez Six Hats pour explorer les perspectives stakeholders"
        priority: P2
        action: "technique six-hats"
      - pattern: "security-early"
        text: "Patterns auth détectés — considérez @security-auditor preview"
        priority: P1
        action: "security-check"
```

**Pour type `plan-review` (transition EMS=50):**

```yaml
@skill:breakpoint-display
  type: plan-review
  data:
    # ... existing fields ...
    suggestions:
      - pattern: "convergence-framework"
        text: "Utilisez MoSCoW pour prioriser les User Stories"
        priority: P2
        action: "technique moscow"
      - pattern: "scope-large"
        text: "Projet estimé LARGE — considérez /decompose après brief"
        priority: P2
        action: null  # Information only
```

### Discovery Priority Levels

| Priority | Icon | Category | Display |
|----------|------|----------|---------|
| **P1** | 🔴 | Critical | Affiché en premier, recommandé fortement |
| **P2** | 🟡 | Important | Suggestion visible, optionnelle |
| **P3** | 🟢 | Nice-to-have | Affiché si peu de suggestions |

### Invocation

```python
from project_memory.suggestion_engine import SuggestionEngine

engine = SuggestionEngine(memory_dir=".project-memory", mode="discovery")

# For brainstorm context
discovery_suggestions = engine.generate_discovery_suggestions(
    ems_scores={"clarity": 80, "depth": 60, "coverage": 35, "decisions": 75, "actionability": 70},
    weak_axes=["coverage"],
    keywords=["auth", "api"],
    similar_features=["auth-oauth"]
)

# Output: List[DiscoverySuggestion]
```

### Learning Integration

**Données collectées en mode Discovery:**

| Donnée | Source | Usage |
|--------|--------|-------|
| Acceptation suggestions | User feedback | Calibrer score suggestions futures |
| Efficacité techniques | EMS delta post-technique | Recommander techniques efficaces |
| Patterns acceptés | Session history | Personnaliser suggestions futures |
| Feature similarity hits | Reuse tracking | Améliorer matching |

**Storage:**

```yaml
# .project-memory/learning/discovery_feedback.yaml
sessions:
  - session_id: "brainstorm-auth-2025-01-16"
    suggestions_shown: 4
    suggestions_accepted: 2
    patterns_accepted: ["security-early", "coverage-low"]
    patterns_ignored: ["scope-large", "similar-feature"]
    ems_improvement: 28
```

### Configuration

Via `.project-memory/settings.yaml`:

```yaml
suggestions:
  discovery:
    enabled: true
    max_suggestions_per_breakpoint: 3
    min_priority: P2  # P1, P2, P3
    show_actions: true
    learn_from_feedback: true
```

### Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Too many suggestions | Cognitive overload | Max 3 per breakpoint |
| Low-priority spam | Noise | Filter by min_priority |
| Ignoring context | Irrelevant | Use EMS axes for targeting |
| No learning | Static | Track acceptance rate |
