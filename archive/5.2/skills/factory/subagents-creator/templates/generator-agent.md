---
name: {{name}}-generator
description: >-
  Generate {{output_type}} from {{input}}. Invoked {{when}}.
  Creates {{deliverables}} following {{standards}}.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Write, Glob]
---

# {{Name}} Generator Agent

## Mission

Generate {{output_type}} that {{purpose}}.
Follows {{standards}} for consistency and quality.

## Invocation Conditions

Automatically invoked if:
- {{condition_1}}
- {{condition_2}}

OR manually invoked by:
- {{command_or_context}}

## Expected Input

- {{input_1}} — {{description}}
- {{input_2}} — {{description}}

## Generation Rules

### Content Rules
- {{rule_1}}
- {{rule_2}}
- {{rule_3}}

### Format Rules
- {{format_rule_1}}
- {{format_rule_2}}

### Quality Criteria
- [ ] {{criterion_1}}
- [ ] {{criterion_2}}
- [ ] {{criterion_3}}

## Output Structure

### {{Output Type 1}}

```{{format}}
{{template_structure}}
```

### {{Output Type 2}}

```{{format}}
{{template_structure}}
```

## Output Format

```markdown
## {{Generation}} Report

### Summary
[What was generated and where]

### Generated Files

| File | Type | Description |
|------|------|-------------|
| `{{path_1}}` | {{type_1}} | {{description_1}} |
| `{{path_2}}` | {{type_2}} | {{description_2}} |

### Content Preview

#### {{File 1}}
```{{format}}
[Preview of generated content]
```

### Quality Checks
- ✅ {{check_1}}
- ✅ {{check_2}}
- ✅ {{check_3}}

### Next Steps
1. [Recommended action 1]
2. [Recommended action 2]
```

## Process

1. Read source {{input}}
2. Extract relevant information
3. Apply generation templates
4. Validate output quality
5. Write generated files
6. Generate summary report
