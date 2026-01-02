# Domain Templates - Pre-configured Skill Patterns

> Ready-to-use templates for common skill categories

---

## Template Selection Guide

| Domain | Use When | Key Features |
|--------|----------|--------------|
| **SQL/Data** | Business metrics, data warehouse queries | Schemas, filters, metrics |
| **Code Review** | Security audit, quality check | Checklists, severity levels |
| **Documentation** | API docs, guides, changelogs | Style rules, templates |
| **File Processing** | PDF, Excel, CSV manipulation | Input/output specs |
| **Workflow Automation** | Multi-step business processes | Decision trees, status |
| **API Integration** | External service consumption | Auth, error handling |

---

## 1. SQL / Data Analytics Template

```yaml
---
name: {{company}}-data-analytics
description: >-
  Query {{company}} data warehouse for {{metrics}}.
  Provides table schemas, required filters, and metric definitions.
  Use when analyzing business data, building reports, or querying metrics.
  Not for raw event logs or system monitoring data.
---
```

### SKILL.md Structure

```markdown
# {{Company}} Data Analytics

## Overview
SQL analysis toolkit for {{company}} data warehouse. Query revenue,
customer metrics, and business KPIs with proper filters.

## Quick Start
1. Identify the metric needed
2. Check table schemas in [schemas.md](references/schemas.md)
3. Apply MANDATORY filters (see Critical Rules)
4. Build and validate query

## Critical Rules
**ALWAYS APPLY these filters:**
- `WHERE account_type != 'Test'`
- `WHERE period <= CURRENT_DATE - INTERVAL '1 day'`
- `WHERE status = 'Active'`

## Available Metrics
| Metric | Table | Reference |
|--------|-------|-----------|
| ARR | revenue_monthly | [arr.md](references/arr.md) |
| Churn | customer_events | [churn.md](references/churn.md) |

## Limitations
- No access to PII data
- No raw event logs
- Historical data limited to 24 months
```

---

## 2. Code Review Template

```yaml
---
name: {{language}}-code-reviewer
description: >-
  Review {{language}} code for {{focus-areas}}.
  Identify security vulnerabilities, performance issues, and code quality.
  Use when auditing code, reviewing PRs, or checking quality.
  Not for refactoring or code generation.
---
```

### SKILL.md Structure

```markdown
# {{Language}} Code Reviewer

## Overview
Code review assistant for {{language}} projects. Focuses on
{{focus-areas}} with severity-based reporting.

## Severity Levels
| Level | Criteria | Action |
|-------|----------|--------|
| CRITICAL | Security vulnerability, data loss risk | Block merge |
| HIGH | Performance issue, major bug | Fix required |
| MEDIUM | Code smell, maintainability | Should fix |
| LOW | Style, minor improvement | Optional |

## Review Checklist
### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention

### Performance
- [ ] No N+1 queries
- [ ] Proper indexing
- [ ] Memory management

### Quality
- [ ] Single responsibility
- [ ] Proper error handling
- [ ] Test coverage adequate

## Output Format
```markdown
## Code Review Report

### CRITICAL Issues
- [file:line] Description

### HIGH Issues
- [file:line] Description
```

## Limitations
- Does not execute code
- Cannot check runtime behavior
- Limited to static analysis
```

---

## 3. Documentation Template

```yaml
---
name: {{project}}-doc-generator
description: >-
  Generate {{doc-type}} documentation for {{project}}.
  Follows {{standard}} conventions with {{elements}}.
  Use when creating docs, updating references, or documenting APIs.
  Not for code comments or inline documentation.
---
```

### SKILL.md Structure

```markdown
# {{Project}} Documentation Generator

## Overview
Generate standardized documentation following {{standard}} conventions.
Produces consistent, well-structured documentation.

## Document Types
| Type | Template | Use When |
|------|----------|----------|
| API Reference | [api-template.md](templates/api.md) | New endpoint |
| User Guide | [guide-template.md](templates/guide.md) | Feature docs |
| Changelog | [changelog-template.md](templates/changelog.md) | Release |

## Style Guide
- Use active voice
- Keep sentences under 25 words
- Use code blocks for examples
- Include prerequisites

## Required Sections
1. **Title** - Clear, descriptive
2. **Overview** - 2-3 sentences
3. **Prerequisites** - What's needed
4. **Steps** - Numbered, actionable
5. **Examples** - At least one
6. **Troubleshooting** - Common issues

## Limitations
- English only
- No image generation
- No video content
```

---

## 4. File Processing Template

```yaml
---
name: {{filetype}}-processor
description: >-
  {{action}} {{filetype}} files with {{capabilities}}.
  Handles {{specific-features}}. Outputs {{output-format}}.
  Use when working with {{filetype}} files or when user needs {{outcome}}.
  Not for {{excluded-format}} or {{excluded-operation}}.
---
```

### SKILL.md Structure

```markdown
# {{FileType}} Processor

## Overview
Process {{filetype}} files: {{capabilities}}.
Outputs structured data in {{output-format}}.

## Supported Operations
| Operation | Description | Example |
|-----------|-------------|---------|
| Extract | Pull data from file | Text, tables |
| Transform | Convert format | JSON output |
| Merge | Combine multiple files | Single output |

## Input Requirements
- Format: {{accepted-formats}}
- Max size: {{size-limit}}
- Encoding: UTF-8

## Output Format
```json
{
  "status": "success",
  "data": {...},
  "metadata": {
    "source": "filename",
    "processed_at": "timestamp"
  }
}
```

## Error Handling
| Error | Cause | Resolution |
|-------|-------|------------|
| FORMAT_ERROR | Invalid file | Check file format |
| SIZE_EXCEEDED | File too large | Split file |
| ENCODING_ERROR | Non-UTF8 | Convert encoding |

## Limitations
- No encrypted files
- No password-protected files
- Single file at a time
```

---

## 5. Workflow Automation Template

```yaml
---
name: {{workflow}}-automation
description: >-
  Automate {{workflow}} with {{steps}} steps.
  Handles {{features}} with proper validation.
  Use when executing {{workflow}} or automating {{process}}.
  Not for {{excluded-workflow}} or manual operations.
---
```

### SKILL.md Structure

```markdown
# {{Workflow}} Automation

## Overview
Automated {{workflow}} with validation and status tracking.
Handles {{features}} with proper error recovery.

## Workflow Steps

```
[Start] -> [Step 1] -> [Decision] -> [Step 2] -> [End]
                          |
                          v
                      [Error Handler]
```

## Decision Points
| Point | Condition | Action |
|-------|-----------|--------|
| D1 | Valid input | Continue |
| D1 | Invalid input | Request correction |
| D2 | Approval granted | Proceed |
| D2 | Rejected | Notify and stop |

## Status Codes
| Code | Meaning | Next Action |
|------|---------|-------------|
| PENDING | Awaiting input | Provide data |
| IN_PROGRESS | Processing | Wait |
| COMPLETED | Success | Done |
| FAILED | Error | Review logs |

## Rollback Procedure
1. Identify failure point
2. Reverse completed steps
3. Restore initial state
4. Log rollback reason

## Limitations
- Sequential execution only
- No parallel workflows
- Manual approval required at {{approval-points}}
```

---

## Template Customization

### Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{company}}` | Organization name | `acme` |
| `{{language}}` | Programming language | `python` |
| `{{project}}` | Project name | `my-api` |
| `{{filetype}}` | File type | `pdf` |
| `{{workflow}}` | Process name | `onboarding` |
| `{{metrics}}` | Metrics tracked | `ARR, MRR, churn` |
| `{{focus-areas}}` | Review focus | `security, performance` |
