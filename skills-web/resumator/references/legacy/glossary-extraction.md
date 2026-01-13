# Glossary Extraction Reference

> Rules for automatic term extraction and definition

---

## Purpose

The glossary:
1. Documents jargon for future readers
2. Standardizes project terminology
3. Creates onboarding reference
4. Clarifies ambiguous acronyms

---

## Term Categories

### 1. Acronyms

Abbreviations from initial letters.

**Examples**: ETL, API, MCD, ORM, CLI, BDD, CRUD, MCP

**Rule**: Include ALL acronyms in transcription, even common ones.

---

### 2. Technical Terms

Domain-specific vocabulary.

**Examples**: DataFrame, orchestrator, middleware, endpoint, migration, decorator

**Rule**: Include if:
- Appears 2+ times, OR
- Central to discussion, OR
- Unclear to non-technical reader

---

### 3. Tools & Libraries

Specific software, frameworks, packages.

**Examples**: Pandas, Django, OpenPyXL, Celery, React, Symfony

**Rule**: Include ALL tools mentioned, with purpose in context.

---

### 4. Domain-Specific Terms

Business/industry terminology specific to context.

**Examples**: Jour de broyage, campagne, indicateur brut, tâche cron

**Rule**: Include terms with special meaning in project context.

---

## Extraction Process

### Step 1: Scan for Candidates

Look for:
- ALL CAPS words (acronyms)
- CamelCase / snake_case (technical)
- Words with explanations ("X, which is...")
- Foreign words in native text
- Quoted terms
- Tool/product names

### Step 2: Filter

**Include if ANY**:
- Appears 2+ times
- Central to decision/action
- Defined in transcription
- Would be unclear outside project
- Is a tool/library name

**Exclude if ALL**:
- Appears once only
- Tangential to main topics
- Universally understood
- Common word without special meaning

### Step 3: Generate Definitions

For each term:
- Concise definition (1-2 sentences)
- Context if project-specific
- Relation to other terms if applicable

---

## Definition Guidelines

### Format

```markdown
| Term | Definition |
|------|------------|
| **ETL** | Extract-Transform-Load; data integration pattern for moving data |
| **DataFrame** | Pandas tabular structure; used here for Excel manipulation |
| **Jour de broyage** | 24h production period at sugar factory, 5am to 5am |
```

### Writing Style

**DO**:
- Start with expansion for acronyms
- Keep to 1-2 sentences
- Include context when specific
- Use semicolons to separate parts

**DON'T**:
- Write encyclopedia entries
- Include usage examples
- Repeat other sections
- Use overly technical definitions

### Examples

**Good**:
```markdown
| **ETL** | Extract-Transform-Load; pipeline pattern for Excel-to-database integration |
```

**Bad** (too long):
```markdown
| **ETL** | Extract-Transform-Load is a pattern involving extracting from sources, transforming per business rules, and loading into targets. Used here for Excel processing... |
```

**Good**:
```markdown
| **Jour de broyage** | Production day at sugar factory; runs 5am to 5am, not midnight |
```

**Bad** (missing context):
```markdown
| **Jour de broyage** | A day of crushing |
```

---

## Handling Ambiguity

### Same Acronym, Multiple Meanings

Specify which applies:

```markdown
| **BDD** | Base de Données (Database); here refers to PostgreSQL warehouse |
```

### Project-Specific Meaning

When common term has special meaning:

```markdown
| **Indicateur** | In this project: calculated metric from lab measurements (Brix, pH) |
```

### Uncertain Terms

If definition unclear:

```markdown
| **ALM** | Albioma (energy company); provides production data via Excel |
```

---

## Ordering

**Default**: Alphabetical by term

**If >10 terms**: Group by category then alphabetical:

```markdown
## 📚 Glossary

### Acronyms
| Term | Definition |
|------|------------|
| **API** | ... |
| **ETL** | ... |

### Technical Terms
| Term | Definition |
|------|------------|
| **DataFrame** | ... |

### Tools & Libraries
| Term | Definition |
|------|------------|
| **Pandas** | ... |

### Domain Terms
| Term | Definition |
|------|------------|
| **Campagne** | ... |
```

---

## Minimum Glossary

Even for simple meetings:
- All acronyms used
- All tool/product names
- Any term explained in meeting

**If none**:
```markdown
## 📚 Glossary

[No technical terms requiring definition]
```

---

## Web Research

If term needs clarification:

1. Search authoritative definition
2. Adapt to project context
3. Mark source

```markdown
| **Context7** | MCP server for up-to-date docs — 🌐 GitHub |
```

---

## Quality Checklist

- [ ] All acronyms expanded
- [ ] All tools identified
- [ ] Definitions ≤2 sentences
- [ ] Project meanings noted
- [ ] Consistent ordering
- [ ] No duplicates
- [ ] No overly obvious terms
