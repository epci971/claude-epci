# Suggestion Examples - Component Opportunity Templates

> Real-world examples of component opportunity suggestions by type

---

## Skill Suggestion Examples

### Example 1: New Stack Skill

**Detected Pattern**: Svelte project setup repeated 3 times with manual research

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Skill

**Identified pattern:**
Svelte/SvelteKit development patterns researched and applied manually.
Same component structure, store patterns, and routing conventions applied.

**Occurrences:**
- Session 1: SvelteKit routing setup with manual documentation lookup
- Session 2: Svelte store implementation following same pattern
- Session 3: Component structure matching previous implementations

**Evidence:**
- WebFetch calls to svelte.dev: 8 times
- Similar component structure: 5 files
- Store pattern copied: 3 instances

**Estimated benefits:**
- Auto-detection of Svelte projects via `svelte.config.js`
- Standardized component, store, and routing patterns
- Reduced documentation lookup time (~15 min/session)

**Proposal:**
```
/epci:create skill svelte-sveltekit
```

**Confidence score:** 8/10

---
*Automatic suggestion - Ignore if not relevant*
```

### Example 2: Architecture Pattern Skill

**Detected Pattern**: Clean Architecture principles applied manually

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Skill

**Identified pattern:**
Clean Architecture / Hexagonal Architecture patterns applied across
multiple projects with similar structure but manual setup.

**Occurrences:**
- Project A: Created domain/, application/, infrastructure/ structure
- Project B: Same layered structure with ports/adapters
- Project C: Identical folder organization with dependency rules

**Evidence:**
- Folder structure repeated: 3 projects
- Same dependency direction enforced: 3 times
- Similar interface patterns: 12 files

**Estimated benefits:**
- Standardized architecture templates
- Automatic layer validation
- Dependency direction enforcement
- Reduced architecture setup time

**Proposal:**
```
/epci:create skill clean-architecture
```

**Confidence score:** 7/10

---
*Automatic suggestion - Ignore if not relevant*
```

---

## Command Suggestion Examples

### Example 3: CI Pipeline Command

**Detected Pattern**: Same sequence before every commit

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Command

**Identified pattern:**
Repeated manual sequence before each commit:
lint → type-check → test → build

**Occurrences:**
- Commit 1: Ran eslint, tsc, jest, webpack manually
- Commit 2: Same 4-step sequence
- Commit 3: Same sequence, forgot type-check initially
- Commit 4: Complete sequence again

**Sequence detected:**
```
1. npm run lint
2. npm run type-check
3. npm run test
4. npm run build
```

**Estimated benefits:**
- One command instead of 4
- No forgotten steps
- Consistent pre-commit validation
- Time savings: ~5 min/commit

**Proposal:**
```
/epci:create command pre-commit-check
```

**Confidence score:** 9/10

---
*Automatic suggestion - Ignore if not relevant*
```

### Example 4: Database Migration Command

**Detected Pattern**: Multi-step database workflow

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Command

**Identified pattern:**
Database migration workflow executed manually with same steps:
backup → migrate → seed → verify

**Occurrences:**
- Migration 1: Full sequence with manual verification
- Migration 2: Same steps, added rollback mid-way
- Migration 3: Complete workflow with verification

**Workflow detected:**
```
1. Create database backup
2. Run pending migrations
3. Seed reference data
4. Verify data integrity
5. [BREAKPOINT: User confirmation]
6. Commit or rollback
```

**Estimated benefits:**
- Automated backup before changes
- Verification built-in
- Rollback capability
- Audit trail

**Proposal:**
```
/epci:create command db-migrate-safe
```

**Confidence score:** 8/10

---
*Automatic suggestion - Ignore if not relevant*
```

---

## Subagent Suggestion Examples

### Example 5: Accessibility Auditor

**Detected Pattern**: Same a11y checklist applied repeatedly

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Subagent

**Identified pattern:**
Accessibility audit checklist applied manually to UI components
with same criteria and report format.

**Occurrences:**
- Component 1: Modal - WCAG checks + keyboard navigation
- Component 2: Form - Same checklist + ARIA labels
- Component 3: Navigation - Same pattern + focus management
- Component 4: Button group - Same criteria applied

**Checklist detected:**
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation
- [ ] Focus management
- [ ] Color contrast (4.5:1)
- [ ] Screen reader compatibility

**Report format detected:**
```markdown
## Accessibility Audit
### Summary: X issues found
### Issues by severity
### Remediation steps
### Verdict: PASS/FAIL
```

**Estimated benefits:**
- Consistent accessibility checks
- No missed criteria
- Standardized remediation guidance
- Compliance documentation

**Proposal:**
```
/epci:create agent a11y-auditor
```

**Confidence score:** 9/10

---
*Automatic suggestion - Ignore if not relevant*
```

### Example 6: API Contract Validator

**Detected Pattern**: API response validation repeated

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Subagent

**Identified pattern:**
API contract validation performed manually with same checks
across multiple endpoints.

**Occurrences:**
- Endpoint /users: Schema validation + error handling check
- Endpoint /orders: Same validation pattern
- Endpoint /products: Identical contract checks
- Endpoint /auth: Same structure validation

**Validation criteria detected:**
- [ ] Response matches OpenAPI schema
- [ ] Error responses follow standard format
- [ ] Status codes are appropriate
- [ ] Headers include required fields
- [ ] Pagination follows convention

**Estimated benefits:**
- Automated contract validation
- Consistency across APIs
- Early detection of breaking changes
- Documentation compliance

**Proposal:**
```
/epci:create agent api-contract-validator
```

**Confidence score:** 8/10

---
*Automatic suggestion - Ignore if not relevant*
```

---

## Low Confidence Examples

### Example 7: Borderline Suggestion

**Detected Pattern**: Pattern only observed twice

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: Skill

**Identified pattern:**
GraphQL schema design patterns applied manually.

**Occurrences:**
- Project A: GraphQL schema with similar resolver structure
- Project B: Same query/mutation organization

**Note:** Only 2 occurrences detected. Consider creating skill
if pattern continues.

**Estimated benefits:**
- Standardized schema structure
- Resolver patterns

**Proposal:**
```
/epci:create skill graphql-patterns
```

**Confidence score:** 5/10

---
*Suggestion based on emerging pattern - May need more evidence*
```

---

## Suggestion Formatting Guidelines

### Required Elements

| Element | Description |
|---------|-------------|
| Type | Skill, Command, or Subagent |
| Pattern | Clear description of detected pattern |
| Occurrences | 3+ specific instances |
| Evidence | Concrete proof (counts, files, etc.) |
| Benefits | Tangible advantages |
| Proposal | Ready-to-use command |
| Confidence | Score out of 10 |

### Tone Guidelines

| Confidence | Tone |
|------------|------|
| 5-6 | Tentative: "You might consider..." |
| 7-8 | Confident: "Consider creating..." |
| 9-10 | Strong: "Strongly recommend creating..." |

### Dismissal Handling

```markdown
---
*Automatic suggestion - Ignore if not relevant*

To suppress similar suggestions, respond with:
- "Not needed" - Won't suggest this type again this session
- "Maybe later" - Will remind at end of session
- "Show me how" - Proceed with creation
```

---

## Quick Reference

```
+------------------------------------------+
|      SUGGESTION TEMPLATE STRUCTURE        |
+------------------------------------------+
| 💡 COMPONENT OPPORTUNITY DETECTED         |
|                                           |
| ### Suggested Type: [Skill|Command|Agent] |
|                                           |
| **Identified pattern:**                   |
| [Clear description]                       |
|                                           |
| **Occurrences:**                          |
| - [Instance 1]                            |
| - [Instance 2]                            |
| - [Instance 3]                            |
|                                           |
| **Estimated benefits:**                   |
| - [Benefit 1]                             |
| - [Benefit 2]                             |
|                                           |
| **Proposal:**                             |
| /epci:create [type] [name]                |
|                                           |
| **Confidence score:** X/10                |
+------------------------------------------+
```
