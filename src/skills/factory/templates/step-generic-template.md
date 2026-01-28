# Step Generic Template

> Template for generating intermediate step files (step-01 through step-98) in new skills.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{step_number}}` | Step number (2 digits) | `01`, `02` |
| `{{step_name}}` | Step name (kebab-case) | `analyze`, `execute` |
| `{{step_title}}` | Step title (Title Case) | `Analyze`, `Execute` |
| `{{step_description}}` | One-line description | `Analyze input and gather context` |
| `{{prev_step}}` | Previous step file | `step-00-init.md` |
| `{{next_step}}` | Next step file | `step-02-plan.md` |
| `{{protocols}}` | List of protocol steps | `[{verb: "Analyze", description: "..."}]` |
| `{{has_breakpoint}}` | Whether step has breakpoint | `true/false` |
| `{{breakpoint_type}}` | Breakpoint type | `validation`, `plan-review` |
| `{{reference_files}}` | List of referenced files | `[{name, filename, purpose}]` |

---

## Template Content

```markdown
# Step {{step_number}}: {{step_title}}

> {{step_description}}

## Trigger

- Completion of {{prev_step}}

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | From previous step | Yes |
| {additional inputs} | {source} | {Yes/No} |

## Protocol

> **DECLARATIVE STYLE**: Each action describes WHAT to do.
> For detailed schemas/templates, link to references/.

{{#each protocols}}
### {{@index}}. {{this.verb}}

{{this.description}}

{{#if this.code}}
```
{{this.code}}
```
{{/if}}
{{/each}}

## Reference Files Used

{{#if reference_files}}
| Reference | Purpose |
|-----------|---------|
{{#each reference_files}}
| [{{this.name}}](../references/{{this.filename}}) | {{this.purpose}} |
{{/each}}

> **Note**: Apply formats/rules from references, don't duplicate inline.
{{else}}
*No external references required for this step.*
{{/if}}

{{#if has_breakpoint}}
### X. BREAKPOINT: {{step_title}} Validation (OBLIGATOIRE)

AFFICHE le format approprié depuis references/breakpoint-formats.md (si disponible).

Remplis les variables requises pour ce breakpoint:
- Step-specific data placeholders
- Proactive suggestions (P1/P2/P3)

APPELLE AskUserQuestion avec:
```
AskUserQuestion({
  questions: [{
    question: "How would you like to proceed?",
    header: "Action",
    multiSelect: false,
    options: [
      { label: "Continuer (Recommended)", description: "Proceed to next step" },
      { label: "Modifier", description: "Adjust current step" },
      { label: "Annuler", description: "Stop workflow" }
    ]
  }]
})
```

⏸️ ATTENDS la réponse utilisateur avant de continuer.

> **Alternative**: Use `@skill:epci:breakpoint-system` if interactive with type `{{breakpoint_type}}`.
{{/if}}

## Outputs

| Output | Destination |
|--------|-------------|
| {output 1} | Session state |
| {output 2} | For next step |

## Next Step

{{#if conditional_next}}
| Condition | Next Step |
|-----------|-----------|
{{#each conditional_next}}
| `{{this.condition}}` | → `{{this.step}}` |
{{/each}}
| Default | → `{{next_step}}` |
{{else}}
→ `{{next_step}}`
{{/if}}

## Error Handling

| Error | Resolution |
|-------|------------|
| {error 1} | {resolution} |
| {error 2} | {resolution} |
```

---

## Usage

When Factory generates intermediate steps:

1. Set step number and name from workflow design
2. Link prev_step and next_step correctly
3. Fill in protocols from phase description
4. Add breakpoint if phase requires user validation
5. Define outputs that next step needs
