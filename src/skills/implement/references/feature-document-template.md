# Feature Document Template

Reference template for the Feature Document created at `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md`.

Each step in the implement workflow fills its corresponding section using the **Edit tool**.

## Template

The Feature Document MUST be created using Write tool at step-00-init with the following structure:

---

# Feature: {feature-slug}

## §0 — Metadata

| Champ | Valeur |
|-------|--------|
| Slug | {feature-slug} |
| Complexite | {STANDARD/LARGE} |
| Date debut | {YYYY-MM-DD HH:mm} |
| Branche | feature/{feature-slug} |
| Spec source | {spec-path or "none"} |
| Status | IN_PROGRESS |

## §1 — Contexte & Objectif

### Objectif
{description of what the feature must accomplish}

### Contexte technique
{stack, dependencies, constraints}

### Criteres d'acceptation
- [ ] {criterion 1}
- [ ] {criterion 2}

## §2 — Plan d'implementation
> Section remplie par step-02-plan [P]

*En attente de la phase Planning...*

## §3 — Implementation
> Section remplie progressivement par step-03-code [C]

*En attente de la phase Code...*

### Team Mode (if activated by step-03b-team)

| Aspect | Value |
|--------|-------|
| Mode | {subagents/agent_teams} |
| Domains | {domain_list} |
| Parallel agents | {agent_list} |
| Background tasks | {task_ids} |

*Section ajoutee par step-03b-team si team mode actif. Absente en mode classique.*

## §4 — Revue & Validation
> Section remplie par step-04-review [I]

*En attente de la phase Inspect...*

## §5 — Finalisation
> Section remplie par step-05-document / step-06-finish

*En attente de la phase Finalization...*

---

## Section Ownership

| Section | Filled by | Tool | When |
|---------|-----------|------|------|
| §0 Metadata | step-00-init | Write | At creation |
| §1 Contexte | step-00-init | Write | At creation (from spec or input) |
| §2 Plan | step-02-plan | Edit | After plan validation |
| §3 Implementation | step-03-code | Edit | After each component (incremental) |
| §3 Team Mode | step-03b-team | Edit | If team mode activated (optional) |
| §4 Revue | step-04-review | Edit | After code review |
| §5 Finalisation | step-05-document | Edit | After documentation phase |

## Rules

- The Feature Document path MUST be stored in `artifacts.feature_doc` in state.json
- The path MUST follow the format: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md`
- Each step MUST use Edit tool to update its section (replacing the placeholder text)
- The document MUST NOT be overwritten — only appended/edited section by section
