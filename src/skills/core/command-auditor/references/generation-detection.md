# Generation Detection Rules — DG-001 to DG-010

> Rules for detecting when commands need decomposition or new components

---

## Overview

Generation detection rules identify when a command should:
- Extract logic to a dedicated skill
- Create a new subagent for delegation
- Split content into reference files
- Generate supporting scripts or hooks

These are **SUGGESTION** severity (non-blocking) unless they indicate
structural problems (**ERREUR**).

---

## Rules Detail

### DG-001: Détecter besoin de skill

**Severity**: SUGGESTION

**Check**: Section contains > 500 tokens of reusable logic

**Detection Criteria**:
- Code block > 50 lines with business logic
- Algorithm description > 500 words
- Repeated pattern across commands

**Trigger Example**:
```markdown
## Validation Algorithm

[500+ tokens of detailed validation logic that could be reused]
```

**Suggestion**:
```
💡 DG-001: Section "Validation Algorithm" contains ~600 tokens of logic.
Consider extracting to skill: `validation-algorithm/SKILL.md`
```

---

### DG-002: Détecter besoin de subagent

**Severity**: SUGGESTION

**Check**: Explicit delegation pattern detected

**Detection Patterns**:
- "Delegate to..."
- "Invoke ... to handle..."
- "Let ... process..."
- "Use Task tool to spawn..."

**Trigger Example**:
```markdown
Delegate the validation to a specialized validator that checks
all 95 rules and returns a structured report.
```

**Suggestion**:
```
💡 DG-002: Delegation detected at line 45.
Consider creating subagent: `@command-validator`
```

---

### DG-003: Détecter besoin de référence

**Severity**: SUGGESTION

**Check**: Section exceeds 100 lines

**Detection**: Count lines between section headers

**Trigger Example**:
```markdown
## Rules Detail

[150 lines of detailed rule explanations]
```

**Suggestion**:
```
💡 DG-003: Section "Rules Detail" is 150 lines.
Consider extracting to: `references/rules-detail.md`
```

---

### DG-004: Détecter pattern répété

**Severity**: ERREUR

**Check**: Significant text block appears multiple times

**Detection**:
- Find text sequences > 50 chars appearing 2+ times
- Exclude common patterns (table headers, code syntax)

**Trigger Example**:
```markdown
## Step 1
IF frontmatter missing → mark FM-001 BLOQUANT and continue

## Step 3
IF frontmatter missing → mark FM-001 BLOQUANT and continue
```

**Error**:
```
❌ DG-004: Duplicate content detected (52 chars, 2 occurrences)
Lines: 45, 89
Fix: Extract to shared section or reference once
```

---

### DG-005: Détecter template candidat

**Severity**: SUGGESTION

**Check**: Output format described in detail → candidate for template file

**Detection Patterns**:
- Output format section with markdown structure
- Report format with placeholders
- Response template with `{variables}`

**Trigger Example**:
```markdown
## Output Format

```markdown
# Report — {name}

| Metric | Value |
|--------|-------|
| Score | {score}/100 |
...
```
```

**Suggestion**:
```
💡 DG-005: Output template detected.
Consider extracting to: `templates/report-template.md`
```

---

### DG-006: Détecter hook candidat

**Severity**: SUGGESTION

**Check**: Pre/post action pattern → candidate for hook script

**Detection Patterns**:
- "Before executing..."
- "After completion..."
- "On success/failure..."
- Side effects (logging, notifications)

**Trigger Example**:
```markdown
After successful audit:
1. Log result to `.project-memory/audits/`
2. Update metrics in `metrics.json`
3. Notify if score < 70
```

**Suggestion**:
```
💡 DG-006: Post-action pattern detected.
Consider creating hook: `hooks/active/post-audit.py`
```

---

### DG-007: Détecter script candidat

**Severity**: SUGGESTION

**Check**: Deterministic logic that could be a script

**Detection Criteria**:
- Pure computation (no LLM judgment needed)
- Input → Output transformation
- Validation with fixed rules
- File manipulation patterns

**Trigger Example**:
```markdown
## Token Estimation

Estimate tokens: `len(content) // 4`
If > 5000, mark as BLOQUANT.
```

**Suggestion**:
```
💡 DG-007: Deterministic logic detected.
Consider extracting to script: `scripts/estimate_tokens.py`
```

---

### DG-008: Suggérer décomposition si > 300 lignes

**Severity**: SUGGESTION

**Check**: Total command length > 300 lines

**Rationale**: Long commands are harder to maintain and understand

**Thresholds**:
- 300-500 lines: Suggest decomposition
- > 500 lines: ERREUR (ST-012)

**Suggestion**:
```
💡 DG-008: Command is 350 lines.
Consider decomposing:
  - Extract validation logic to skill
  - Move detailed rules to references/
  - Create subagent for complex processing
```

---

### DG-009: Suggérer references/ si contenu dense

**Severity**: SUGGESTION

**Check**: High information density (many tables, lists, code blocks)

**Detection**:
- > 5 tables in document
- > 10 code blocks
- > 20 list items in single section

**Trigger Example**:
```markdown
[Document with 8 tables, 15 code blocks, 50+ list items]
```

**Suggestion**:
```
💡 DG-009: High density content detected.
Consider organizing into references/:
  - references/rules-tables.md
  - references/code-examples.md
  - references/quick-reference.md
```

---

### DG-010: Détecter overlap avec commandes existantes

**Severity**: ERREUR

**Check**: Command functionality overlaps with existing command

**Detection**:
- Similar description keywords
- Same output format
- Overlapping trigger conditions

**Existing Commands** (14 total):
```
brief, epci, quick, ralph-exec, orchestrate, commit,
rules, brainstorm, debug, decompose, memory, promptor,
create, save-plan
```

**Trigger Example**:
```markdown
---
description: Generate project rules and conventions
---
```

**Error**:
```
❌ DG-010: Overlap detected with existing command.
Command: /rules (rules.md)
Similarity: 85% (description, output format)
Action: Merge functionality or differentiate clearly
```

---

## Detection Algorithm

```python
def detect_generation_needs(content: str, existing_commands: list) -> list[Suggestion]:
    suggestions = []

    # DG-001: Skill candidate
    sections = split_by_headers(content)
    for section_name, section_content in sections.items():
        tokens = len(section_content) // 4
        if tokens > 500 and has_logic_patterns(section_content):
            suggestions.append(Suggestion(
                'DG-001',
                f'Section "{section_name}" has ~{tokens} tokens of logic',
                f'Extract to skill: `{slugify(section_name)}/SKILL.md`'
            ))

    # DG-002: Subagent candidate
    delegation_patterns = [
        r'[Dd]elegate to',
        r'[Ii]nvoke .* to handle',
        r'[Uu]se Task tool',
        r'[Ss]pawn .* agent'
    ]
    for pattern in delegation_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line = content[:match.start()].count('\n') + 1
            suggestions.append(Suggestion(
                'DG-002',
                f'Delegation pattern at line {line}',
                'Consider creating dedicated subagent'
            ))

    # DG-004: Duplicate detection
    duplicates = find_duplicates(content, min_length=50)
    for dup_text, locations in duplicates.items():
        if len(locations) >= 2:
            suggestions.append(Suggestion(
                'DG-004',
                f'Duplicate content ({len(dup_text)} chars) at lines {locations}',
                'Consolidate to single location',
                severity='ERREUR'
            ))

    # DG-010: Overlap detection
    command_desc = extract_description(content)
    for existing in existing_commands:
        similarity = calculate_similarity(command_desc, existing.description)
        if similarity > 0.7:
            suggestions.append(Suggestion(
                'DG-010',
                f'Overlap with {existing.name}: {similarity:.0%} similar',
                'Differentiate or merge functionality',
                severity='ERREUR'
            ))

    return suggestions
```

---

## Generation Actions

When suggestions are accepted, generate:

| Detection | Generated Component |
|-----------|---------------------|
| DG-001 | `skills/{category}/{name}/SKILL.md` |
| DG-002 | `agents/{name}.md` |
| DG-003 | `{command}/references/{name}.md` |
| DG-005 | `{command}/templates/{name}.md` |
| DG-006 | `hooks/active/{hook-name}.py` |
| DG-007 | `scripts/{script-name}.py` |

---

*Generation Detection Rules v1.0.0 — Command Auditor*
