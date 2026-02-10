---
name: step-05-document
description: Documentation update phase
prev_step: steps/step-04-review.md
next_step: steps/step-06-finish.md
---

# Step 05: Document

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER skip Feature Document update
- 🔴 NEVER leave outdated documentation
- ✅ ALWAYS complete Feature Document
- ✅ ALWAYS update related docs if affected
- ✅ ALWAYS document breaking changes
- 🔵 YOU ARE A DOCUMENTOR ensuring future maintainability
- 💭 FOCUS on what the next developer needs to know

## EXECUTION PROTOCOLS:

1. **Complete** Feature Document
   - Update status to COMPLETED
   - Add final implementation details
   - Record test coverage achieved
   - Document any deviations from plan

2. **Update** related documentation
   - API docs if endpoints changed
   - README if usage changed
   - CHANGELOG if significant
   - Architecture docs if structure changed

3. **Document** breaking changes
   - Migration steps if needed
   - Deprecated code notices
   - Compatibility notes

4. **Review** documentation quality
   - Clear and concise
   - Code examples where helpful
   - No outdated references

5. **Complete** Feature Document §5

**MANDATORY**: Use **Edit tool** to fill §5 in the Feature Document.

Path: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md` (from `artifacts.feature_doc`)

EXECUTE Edit({
  file_path: "{feature_doc_path}",
  old_string: "## §5 — Finalisation\n> Section remplie par step-05-document / step-06-finish\n\n*En attente de la phase Finalization...*",
  new_string: "## §5 — Finalisation\n> Rempli par step-05-document / step-06-finish\n\n### Resume\n{1-2 sentence summary}\n\n### Fichiers modifies\n{list of modified files with - prefix}\n\n### Tests ajoutes : {test_count}\n\n### Documentation mise a jour\n{list of updated docs}\n\n### Prochaines etapes\n- [ ] Commit\n- [ ] PR\n- [ ] Deploiement"
})

## CONTEXT BOUNDARIES:

- This step expects: Reviewed and approved code, feature_doc_path (from step-00)
- This step produces: Feature Document §5 filled, related docs updated

## FEATURE DOCUMENT REFERENCE:

The Feature Document template is defined in `@../references/feature-document-template.md`.
This step fills §5 (Finalisation) using Edit tool. The document was created at step-00-init.

## OUTPUT FORMAT:

```
## Documentation Complete

### Feature Document
- Location: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md`
- Status: COMPLETED

### Updated Docs
- {doc 1}: {changes}
- {doc 2}: {changes}

### Breaking Changes
{none | list of changes with migration steps}
```

## NEXT STEP TRIGGER:

When documentation is complete, proceed to `step-06-finish.md`.
