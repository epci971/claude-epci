---
name: step-05-document-auto
description: Complete Feature Document and generate executive summary
prev_step: steps/step-04-review-auto.md
next_step: steps/step-06-finish-auto.md
---

# Step 05: Document (Auto)

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion
- ALWAYS complete the Feature Document
- ALWAYS generate an executive summary

## EXECUTION PROTOCOLS:

### 1. Generate Executive Summary

Write a 2-3 paragraph summary covering:

- **What was implemented**: Components, files created/modified
- **Technical decisions**: Patterns followed, architecture choices
- **Test coverage**: Number of tests, coverage metrics
- **Limitations**: Known issues, components that failed (if PARTIAL)

### 2. Update Feature Document §5

Use Edit tool to update the Resume Executif section in the Feature Document:

```
## Resume Executif

{generated executive summary}

### Metriques

| Metrique | Valeur |
|----------|--------|
| Fichiers crees | {files_created} |
| Fichiers modifies | {files_modified} |
| Tests ajoutes | {tests_added} |
| Tests passants | {tests_passing} |
| Tests echoues | {tests_failing} |
| Composants reussis | {success_count}/{total_components} |
```

### 3. Update Acceptance Criteria

In the Feature Document, check off acceptance criteria that were met:

```
- [x] Criterion that was met
- [ ] Criterion not yet met
```

### 4. Update JSON Output

Update `.implement-auto-output.json`:
- `phases.completed` += "document"
- `phases.current` = "finish"
- `feature_doc` = path to Feature Document

## CONTEXT BOUNDARIES:

- This step expects: Implementation results, review findings, Feature Document
- This step produces: Completed Feature Document, updated JSON

## NEXT STEP TRIGGER:

Always proceed to step-06-finish-auto.md.
