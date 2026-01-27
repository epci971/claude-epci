# Validation Checklist

Complete 12-point checklist for skill validation before generation.

## Required Checks (1-9)

### 1. Name Uniqueness

```bash
# Check no existing skill with same name
grep -r "^name: {skill-name}" skills/
```

**Pass**: No matches found
**Fail**: Name already exists → choose different name

### 2. Name Format

**Rules**:
- Lowercase only
- Hyphens allowed (no underscores)
- Max 64 characters
- No special characters

**Examples**:
- ✅ `api-generator`
- ✅ `code-review`
- ❌ `API_Generator` (uppercase, underscore)
- ❌ `code.review` (dot)

### 3. Description Specificity

**Vague indicators** (fail if present):
- "helper"
- "utility"
- "tool"
- "misc"
- Single word descriptions

**Specific indicators** (pass):
- Action verbs
- Concrete use cases
- Named triggers

### 4. Description Length

```python
len(description) < 1024  # characters
# Optimal: 50-150 words
```

### 5. Trigger Words Present

Description must include at least 3:
- "Use when:"
- "Triggers:"
- Natural invocation phrases
- Action scenarios

**Example check**:
```
✅ "Use when: reviewing PRs, checking code quality"
✅ "Triggers: code review, PR review, review changes"
❌ "A code review tool" (no triggers)
```

### 6. SKILL.md Line Count

```bash
wc -l SKILL.md
# Must be < 500 lines
```

**If over 500 lines**:
- Extract sections to references/
- Keep SKILL.md as overview
- Link to detailed files

### 7. Referenced Files Exist

For each `[text](path)` in SKILL.md:
- File must exist at that path
- Path must be relative to SKILL.md

```bash
# Extract and check all links
grep -oP '\[.*?\]\(\K[^)]+' SKILL.md | while read path; do
  test -f "$path" || echo "Missing: $path"
done
```

### 8. Allowed-Tools Appropriate

| Skill Type | Recommended Tools |
|------------|-------------------|
| Read-only | `Read, Glob, Grep` |
| Modifications | `Read, Write, Edit` |
| Interactive | `AskUserQuestion` |
| Execution | `Bash` (with restrictions) |

**Warning signs**:
- `Bash` without restrictions for read-only skill
- Missing `AskUserQuestion` for interactive skill
- Too permissive for skill's purpose

### 9. Workflow Steps Numbered

SKILL.md must contain numbered workflow:

```markdown
## Workflow

1. Step one
2. Step two
3. Step three
```

**Check**: At least 3 numbered steps present

---

## Recommended Checks (10-12)

### 10. Examples Included

SKILL.md should have:
- Input example
- Output example
- Usage example

```markdown
## Examples

### Input
/skill-name arg1 arg2

### Output
Expected result...
```

### 11. Error Handling Defined

Document what happens on:
- Invalid input
- Missing prerequisites
- Execution failures

```markdown
## Error Handling

- Invalid input → Show usage help
- Missing file → Ask for correct path
- Command fails → Report error details
```

### 12. Limitations Documented

Clear "does NOT" section:

```markdown
## Limitations

This skill does NOT:
- Handle edge case X
- Support format Y
- Work with Z
```

### 13. Task Tool Documentation (MANDATORY for complex)

**Rule**: Multi-phase workflows with agent delegation MUST document Task invocations

**Validation**:
- [ ] Delegated phases show `Task(subagent_type: ...)` syntax
- [ ] Not just "@agent-name" descriptions
- [ ] Context passed to agent is documented

**Severity**: ERROR for workflows with 4+ phases

**Check**:
```bash
# Verify Task invocations present for agent references
grep -r "subagent_type:" steps/
# Should match each @agent reference
```

---

## Validation Report Template

```
┌─────────────────────────────────────────────────────┐
│ SKILL VALIDATION REPORT                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Skill: {name}                                       │
│ Type: {user | core}                                 │
│                                                      │
│ REQUIRED CHECKS                                      │
│ [✓] 1. Name unique                                  │
│ [✓] 2. Name format valid                            │
│ [✓] 3. Description specific                         │
│ [✓] 4. Description < 1024 chars                     │
│ [✓] 5. Trigger words present                        │
│ [✓] 6. SKILL.md < 500 lines                         │
│ [✓] 7. All references exist                         │
│ [✓] 8. Allowed-tools appropriate                    │
│ [✓] 9. Workflow numbered                            │
│                                                      │
│ RECOMMENDED CHECKS                                   │
│ [✓] 10. Examples included                           │
│ [✓] 11. Error handling defined                      │
│ [✓] 12. Limitations documented                      │
│ [✓] 13. Task tool documented (if delegating)        │
│                                                      │
│ Result: PASS (13/13)                                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Quick Validation Commands

```bash
# 1. Check name uniqueness
grep -r "^name: my-skill" skills/

# 2. Check description length
head -20 SKILL.md | grep -A5 "description:" | wc -c

# 3. Count lines
wc -l SKILL.md

# 4. Check references exist
grep -oP '\]\(\K[^)]+\.md' SKILL.md | xargs -I{} test -f {} && echo "OK" || echo "MISSING"

# 5. Check numbered steps
grep -cE "^[0-9]+\." SKILL.md
```
