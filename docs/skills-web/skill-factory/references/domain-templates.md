# Domain Templates - Pre-Configured Skill Templates

> Ready-to-customize templates for common skill domains

---

## Available Domains

1. [SQL / Data Analytics](#1-sql--data-analytics)
2. [Code Review](#2-code-review)
3. [Documentation](#3-documentation)
4. [File Processing](#4-file-processing)
5. [Workflow Automation](#5-workflow-automation)
6. [API Integration](#6-api-integration)

---

## 1. SQL / Data Analytics

### Use Cases
- Data warehouse queries
- KPI analysis and reporting
- Customer segmentation
- Revenue metrics

### Template

```yaml
---
name: [company]-sql-analytics
description: >-
  Comprehensive SQL analysis toolkit for [COMPANY] data warehouse.
  Query [metric 1], [metric 2], [metric 3], and [metric 4].
  Provides table schemas, required filters, and metric definitions.
  Use when analyzing business data, building reports, or querying
  financial metrics. Not for [excluded data] or [excluded operation].
allowed-tools: Read, Grep, Glob
---

# [Company] SQL Analytics

## Overview

Query and analyze [COMPANY]'s data warehouse with proper filters and schema awareness. Ensures data quality with required exclusions and date filters.

## Quick Reference

| Metric | Table | Key Columns |
|--------|-------|-------------|
| Revenue | `fact_revenue` | amount, date, account_id |
| ARR | `dim_subscriptions` | mrr, start_date, status |
| Customers | `dim_customers` | segment, region, tier |

## Workflow

1. **Identify metric type** → Select appropriate table
2. **Apply required filters** → Exclude test accounts, incomplete periods
3. **Build query** → Use provided schemas
4. **Validate** → Run validation script
5. **Execute** → Return results with context

## Required Filters (ALWAYS APPLY)

```sql
-- Exclude test accounts
WHERE account_type != 'Test'
  AND account_name NOT LIKE '%Demo%'

-- Complete periods only
  AND date <= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day'
```

## Knowledge Base

- [Finance Schemas](references/finance.md)
- [Product Schemas](references/product.md)
- [Metric Definitions](references/metrics.md)

## Limitations

- Does NOT query: raw event logs, system monitoring, HR data
- Does NOT modify: any data (read-only)
```

### Typical References Structure

```
sql-analytics/
├── SKILL.md
├── references/
│   ├── finance.md          # Finance table schemas
│   ├── product.md          # Product usage schemas
│   ├── sales.md            # Sales pipeline schemas
│   ├── metrics.md          # Metric definitions
│   └── edge-cases.md       # Known data quirks
└── scripts/
    └── validate_query.py   # SQL validation
```

---

## 2. Code Review

### Use Cases
- Security audit (OWASP)
- Performance analysis
- Best practices check
- Code quality

### Template

```yaml
---
name: [language]-code-review
description: >-
  Review [LANGUAGE] code for [FOCUS AREAS].
  Identify security vulnerabilities, performance issues, and best practice violations.
  Provides actionable recommendations with code examples.
  Use when reviewing code, auditing security, or checking code quality.
  Not for [excluded task] or code generation.
allowed-tools: Read, Grep, Glob
---

# [Language] Code Review

## Overview

Systematic code review for [LANGUAGE] focusing on security, performance, and maintainability. Follows [STANDARD] guidelines.

## Review Checklist

### Security
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication/authorization
- [ ] Sensitive data handling

### Performance
- [ ] Algorithm complexity
- [ ] Database query optimization
- [ ] Memory management
- [ ] Caching opportunities

### Best Practices
- [ ] Code organization
- [ ] Error handling
- [ ] Logging
- [ ] Documentation
- [ ] Test coverage

## Workflow

1. **Read target files** → Understand structure
2. **Security scan** → Check for vulnerabilities
3. **Performance analysis** → Identify bottlenecks
4. **Best practices** → Compare against standards
5. **Report** → Prioritized findings with recommendations

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| 🔴 Critical | Security vulnerability | Fix immediately |
| 🟠 High | Performance/security concern | Fix before release |
| 🟡 Medium | Best practice violation | Plan to fix |
| 🟢 Low | Suggestion | Consider |

## Knowledge Base

- [Security Patterns](references/security.md)
- [Performance Guidelines](references/performance.md)
- [Style Guide](references/style-guide.md)

## Limitations

- Does NOT generate code (review only)
- Does NOT fix issues automatically
- Does NOT review [excluded languages]
```

---

## 3. Documentation

### Use Cases
- Technical documentation
- API reference
- User guides
- Release notes

### Template

```yaml
---
name: [project]-docs-generator
description: >-
  Generate [DOC TYPE] documentation for [PROJECT/SYSTEM].
  Produces structured markdown with [ELEMENTS].
  Follows [STANDARD] conventions and formatting.
  Use when creating docs, updating references, or documenting [subject].
  Not for [excluded doc type] or user-facing marketing content.
allowed-tools: Read, Write, Grep, Glob
---

# [Project] Documentation Generator

## Overview

Generate consistent, well-structured documentation following [STANDARD] conventions. Outputs ready-to-publish markdown.

## Document Types

| Type | Use When | Template |
|------|----------|----------|
| API Reference | Documenting endpoints | [api.md](templates/api.md) |
| User Guide | End-user instructions | [guide.md](templates/guide.md) |
| Technical Spec | Architecture decisions | [spec.md](templates/spec.md) |
| Release Notes | Version changelog | [release.md](templates/release.md) |

## Workflow

1. **Identify doc type** → Select appropriate template
2. **Gather source** → Code, specs, existing docs
3. **Extract structure** → Headings, sections
4. **Generate content** → Fill template
5. **Validate** → Check completeness
6. **Output** → Formatted markdown

## Style Guidelines

- Headings: Sentence case
- Code blocks: Always specify language
- Links: Relative paths preferred
- Tables: For structured data
- Lists: For sequential steps

## Knowledge Base

- [Style Guide](references/style-guide.md)
- [Templates](templates/)
- [Examples](references/examples.md)

## Limitations

- Does NOT create marketing content
- Does NOT translate (English only)
- Requires source material
```

---

## 4. File Processing

### Use Cases
- PDF manipulation
- Excel analysis
- CSV transformation
- Document conversion

### Template

```yaml
---
name: [filetype]-processor
description: >-
  Process [FILE TYPE] files with [CAPABILITIES].
  [ACTION 1], [ACTION 2], and [ACTION 3].
  Handles [specific features] and outputs [format].
  Use when working with [file type] files or when user needs [outcome].
  Not for [excluded format] or [excluded operation].
allowed-tools: Read, Write, Bash, Grep
---

# [FileType] Processor

## Overview

Process [FILE TYPE] files with support for [KEY FEATURES]. Handles common operations while preserving data integrity.

## Capabilities

| Operation | Input | Output |
|-----------|-------|--------|
| Extract | [file type] | Text/JSON |
| Transform | [file type] | [format] |
| Merge | Multiple files | Single file |
| Validate | [file type] | Report |

## Workflow

1. **Validate input** → Check file format
2. **Select operation** → Based on user request
3. **Process** → Apply transformation
4. **Validate output** → Ensure integrity
5. **Deliver** → Return result or save file

## Supported Formats

- ✅ [Format 1]
- ✅ [Format 2]
- ❌ [Unsupported format]

## Dependencies

```bash
pip install [required-packages]
```

## Knowledge Base

- [Format Specs](references/formats.md)
- [Edge Cases](references/edge-cases.md)

## Limitations

- Max file size: [limit]
- Does NOT handle: [excluded types]
- Requires: [dependencies]
```

---

## 5. Workflow Automation

### Use Cases
- Multi-step business processes
- Approval workflows
- Data pipelines
- Report generation

### Template

```yaml
---
name: [process]-workflow
description: >-
  Automate [PROCESS NAME] workflow with [STEPS COUNT] steps.
  Handles [input types] and produces [outputs].
  Includes validation, error handling, and status tracking.
  Use when [trigger conditions] or processing [data type].
  Not for [excluded scenarios] or manual interventions.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# [Process] Workflow

## Overview

Automated workflow for [PROCESS] ensuring consistency and traceability. Handles the complete flow from [start] to [end].

## Process Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Step 1  │ → │ Step 2  │ → │ Step 3  │ → │ Step 4  │
│ [name]  │    │ [name]  │    │ [name]  │    │ [name]  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## Steps Detail

### Step 1: [Name]
- **Input**: [input]
- **Action**: [action]
- **Output**: [output]
- **Validation**: [criteria]

### Step 2: [Name]
...

## Decision Points

| Condition | Action |
|-----------|--------|
| [condition 1] | [path A] |
| [condition 2] | [path B] |
| Error | [error handling] |

## Status Tracking

| Status | Meaning |
|--------|---------|
| 🔵 Pending | Not started |
| 🟡 In Progress | Processing |
| 🟢 Complete | Success |
| 🔴 Failed | Error occurred |

## Knowledge Base

- [Process Rules](references/rules.md)
- [Error Handling](references/errors.md)

## Limitations

- Sequential processing only
- Manual intervention for [cases]
- Does NOT handle [excluded scenarios]
```

---

## 6. API Integration

### Use Cases
- External API consumption
- Data synchronization
- Webhook handling
- Service orchestration

### Template

```yaml
---
name: [service]-api-client
description: >-
  Interact with [SERVICE] API for [OPERATIONS].
  Supports [endpoints/features]. Handles authentication and rate limiting.
  Use when querying [service], syncing data, or automating [tasks].
  Not for [excluded operations] or bulk data migration.
allowed-tools: Read, Bash, Grep
---

# [Service] API Client

## Overview

Interact with [SERVICE] API following best practices for authentication, error handling, and rate limiting.

## Available Operations

| Operation | Endpoint | Method |
|-----------|----------|--------|
| [Op 1] | `/api/v1/[resource]` | GET |
| [Op 2] | `/api/v1/[resource]` | POST |
| [Op 3] | `/api/v1/[resource]/{id}` | PUT |

## Authentication

```bash
# Set environment variable
export [SERVICE]_API_KEY="your-api-key"
```

## Workflow

1. **Authenticate** → Verify credentials
2. **Build request** → Construct payload
3. **Execute** → Call API with retry logic
4. **Handle response** → Parse and validate
5. **Return** → Formatted result

## Rate Limiting

- Limit: [X] requests per [period]
- Retry: Exponential backoff
- Headers: Check `X-RateLimit-*`

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Return data |
| 401 | Unauthorized | Check API key |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry with backoff |

## Knowledge Base

- [API Reference](references/api-reference.md)
- [Error Codes](references/errors.md)

## Limitations

- Read operations primarily
- No bulk operations (>100 items)
- Requires valid API credentials
```

---

## Template Selection Guide

| Your Need | Recommended Template |
|-----------|---------------------|
| Query business data | SQL / Data Analytics |
| Audit code quality | Code Review |
| Create technical docs | Documentation |
| Process files | File Processing |
| Automate processes | Workflow Automation |
| Connect to services | API Integration |
