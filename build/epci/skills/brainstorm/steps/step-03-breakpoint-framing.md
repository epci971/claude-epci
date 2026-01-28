# Step 03: Breakpoint Framing

> Validate framing before entering iteration loop.

## Trigger

- Previous step: `step-02-framing.md` completed
- Template, HMW, and EMS baseline established

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `brief_v0` | From step-01 | Yes |
| `template` | From step-02 | Yes |
| `hmw_questions` | From step-02 | No |
| `ems` | From step-02 | Yes |
| `codebase_analysis` | From step-02 | No |
| `--quick` flag | From step-00 | No |

## Reference Files Used

| Reference | Purpose |
|-----------|---------|
| [breakpoint-formats.md](../references/breakpoint-formats.md#framing-validation-box) | Framing validation ASCII box template |
| [iteration-rules.md](../references/iteration-rules.md#quick-mode-adjustments) | Quick mode question limits |

## Protocol

### 1. Prepare Framing Summary

Compile all framing information:

```markdown
## Session Framing

**Topic**: {idea_refined}
**Template**: {template}
**Initial EMS**: {ems.global}/100

### Brief Summary
{brief_v0 condensed}

### Codebase Context
- Stack: {detected stack}
- Related modules: {list}
- Patterns found: {list}

### HMW Questions
1. {hmw_1}
2. {hmw_2}
3. {hmw_3}
```

### 2. Generate Framing Questions (3 max)

Target critical missing information:

| Category | Question Type |
|----------|---------------|
| **Target** | "Who exactly will use this?" |
| **Constraints** | "Any technical limits we should know?" |
| **Timeline** | "Is there a deadline or milestone?" |
| **Dependencies** | "Does this depend on other work?" |
| **Priority** | "What's the most critical aspect?" |

Apply [quick mode adjustments](../references/iteration-rules.md#quick-mode-adjustments): limit to 2 questions (Target + Priority) if `--quick` flag active.

### 3. BREAKPOINT: Framing Validation (OBLIGATOIRE)

AFFICHE le format Framing Validation depuis [references/breakpoint-formats.md](../references/breakpoint-formats.md#framing-validation-box).

Remplis les variables:
- `{template}`, `{ems_initial}`, `{hmw_count}`
- `{brief_v0_condensed}`
- Questions de cadrage avec suggestions

APPELLE AskUserQuestion avec les options depuis la référence.

⏸️ ATTENDS la réponse utilisateur avant de continuer.

### 4. Integrate Responses

```
IF framing questions answered:
  → Update brief with new information
  → Recalculate EMS clarity axis
  → Store decisions made

IF "Adjust framing" selected:
  → Allow template change
  → Allow brief modification
  → Return to this breakpoint

IF "Add context" selected:
  → Open-ended input
  → Process and integrate
  → Return to this breakpoint
```

### 5. Finalize Iteration Setup

```json
{
  "iteration": 1,
  "phase": "DIVERGENT",
  "persona": "architecte",
  "exploration_ready": true,
  "framing_complete": true
}
```

## Outputs

| Output | Destination |
|--------|-------------|
| `framing_complete` | Session state |
| `exploration_ready` | Session state |
| Updated `brief_v0` | Session state |
| Updated `ems` | Session state |

## Next Step

| Condition | Next Step |
|-----------|-----------|
| Framing validated | → `step-04-iteration.md` |
| Adjust framing | → `step-03-breakpoint-framing.md` (loop) |
| Cancel session | → Exit with summary |

## Error Handling

| Error | Resolution |
|-------|------------|
| User wants to restart | → `step-01-clarify.md` |
| Template mismatch | Allow template change |
| Missing critical info | Generate additional questions |
