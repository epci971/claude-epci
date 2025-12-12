# Description Formulas - Triggering Patterns

> Master the art of writing descriptions that trigger reliably

---

## How Triggering Works

```
[User request]
        ↓
[Scan all Skills descriptions]
        ↓
[SEMANTIC matching (not keyword)]
        ↓
[0, 1 or multiple Skills match]
        ↓
[Progressive loading]
```

**Key point**: Claude performs **semantic** matching, not keyword matching. A vague description = unpredictable triggering.

---

## The Master Formula

```
[CAPABILITIES] + [USE CASES] + [TRIGGERS] + [BOUNDARIES]
```

| Component | Content | Example |
|-----------|---------|---------|
| **Capabilities** | Action verbs + objects | "Extract text, fill forms, merge PDFs" |
| **Use cases** | Usage contexts | "Use when working with PDF documents" |
| **Triggers** | User keywords | "forms, extraction, document merging" |
| **Boundaries** | Explicit exclusions | "Not for simple viewing or image PDFs" |

---

## Production-Ready Template

```yaml
description: >-
  [PRIMARY CAPABILITY in 1 sentence]. [SECONDARY CAPABILITIES].
  Provides [specific added value]. 
  Use when [context 1], [context 2], or [context 3].
  Not for [exclusion 1] or [exclusion 2].
```

---

## Elements to Include

### Action Verbs (Capabilities)
```
extract, analyze, create, generate, validate, review, audit,
merge, split, convert, fill, query, calculate, format,
summarize, optimize, refactor, transform, parse, lint
```

### File Types / Data Types
```
PDF, Excel, .xlsx, .csv, JSON, XML, SQL, Python, JavaScript,
markdown, .docx, images, logs, configurations, schemas,
database tables, API responses, reports
```

### Context Triggers ("Use when...")
```
- "Use when working with [file type]"
- "Use when analyzing [data type]"
- "Use when [action] is needed"
- "Use when user mentions [keywords]"
- "Use for [specific task]"
```

### Boundary Markers ("Not for...")
```
- "Not for [related but out-of-scope task]"
- "Does not handle [specific format/case]"
- "Not intended for [adjacent use case]"
- "Excludes [type of data/operation]"
```

---

## Comparative Examples

### ❌ Weak vs ✅ Strong

| ❌ Weak | ✅ Strong |
|---------|----------|
| `Helps with documents` | `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs or when user mentions forms, extraction, or document merging. Not for image-only PDFs.` |
| `For data analysis` | `Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with .xlsx files or analyzing tabular KPI data. Not for simple formatting changes.` |
| `Code helper` | `Review Python code for security vulnerabilities (OWASP) and performance. Use when auditing Python files or checking for SQLi, XSS. Not for general refactoring.` |
| `SQL stuff` | `Query ACME data warehouse for revenue, ARR, and customer metrics. Use when analyzing business data or building reports. Not for raw event logs or system monitoring.` |
| `Document processing` | `Convert Word documents to structured markdown with heading extraction and table preservation. Use when migrating documentation. Not for PDF or image files.` |

---

## Domain-Specific Patterns

### SQL / Data Analysis
```yaml
description: >-
  Comprehensive SQL analysis for [COMPANY] data warehouse. 
  Query [metric 1], [metric 2], and [metric 3]. 
  Provides table schemas, required filters, and metric definitions.
  Use when analyzing business data, building reports, or querying 
  financial metrics. Not for [excluded data type] or [excluded use].
```

### Code Review
```yaml
description: >-
  Review [LANGUAGE] code for [FOCUS AREAS]. 
  Identify [issue types] and suggest improvements.
  Use when reviewing code, auditing security, or checking quality.
  Not for [excluded task] or [excluded language].
```

### File Processing
```yaml
description: >-
  [ACTION] [FILE TYPE] files with [CAPABILITIES].
  Handles [specific features]. 
  Use when working with [file type] or when user needs [outcome].
  Not for [excluded format] or [excluded operation].
```

### Documentation
```yaml
description: >-
  Generate [DOC TYPE] documentation from [SOURCE].
  Includes [elements]. Follows [STANDARD] conventions.
  Use when creating docs, updating references, or documenting [subject].
  Not for [excluded doc type] or [excluded format].
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague description | Random triggering | Add specific capabilities and contexts |
| Too many generic keywords | Unwanted activation | Focus on domain-specific terms |
| No "Use when..." | Claude doesn't know WHEN | Add explicit usage contexts |
| No "Not for..." | Frequent false positives | Define clear boundaries |
| Description = repeated name | No useful info | Describe actual capabilities |
| Overlapping with other skills | Conflict | Differentiate triggers |

---

## Validation Checklist

Before finalizing description:

- [ ] ≤1024 characters
- [ ] Contains action verbs (what it DOES)
- [ ] Specifies file types / data types (what it works WITH)
- [ ] Includes "Use when..." (WHEN to trigger)
- [ ] Includes "Not for..." (WHEN NOT to trigger)
- [ ] No overlap with existing skills
- [ ] No tabs, proper YAML syntax
- [ ] Quotes around special characters (`:`, `"`, etc.)

---

## Character Count Tool

Quick estimation:
- Average word: 6 characters
- 1024 chars ≈ 170 words max
- Aim for 120-150 words for safety margin

```python
# Quick check
description = """your description here"""
print(f"Length: {len(description)} / 1024 chars")
print(f"OK" if len(description) <= 1024 else "TOO LONG")
```

---

## Testing Your Description

### Triggering Test Queries

For each skill, test with:

1. **Explicit trigger**: "Use the [skill-name] skill to [action]"
2. **Natural language**: User request without mentioning skill
3. **Edge case**: Similar but out-of-scope request
4. **Keywords only**: Just the trigger words

### Expected Results

| Query Type | Should Trigger? |
|------------|-----------------|
| Explicit request | ✅ Always |
| Natural language with keywords | ✅ Yes |
| Related but out-of-scope | ❌ No |
| Generic/vague request | ❌ No |
