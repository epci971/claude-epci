# Existing Subagents Reference

Reference catalog of all existing EPCI subagents for consistency and inspiration.

## Native Subagents (Claude Code)

### @Explore
- **Model**: Haiku
- **Mode**: Read-only
- **Purpose**: Fast codebase analysis
- **Usage**: Initial exploration, file discovery

### @Plan
- **Model**: Sonnet
- **Mode**: Research
- **Purpose**: Research before planning
- **Usage**: Strategy development, architecture research

### General-purpose
- **Model**: Sonnet
- **Mode**: Read+Write
- **Purpose**: General implementation tasks
- **Usage**: Code generation, modifications

## Custom EPCI Subagents (5)

### @plan-validator
- **Purpose**: Validate implementation plan before Phase 2
- **Tools**: Read, Grep
- **Invoked by**: `/epci` Phase 1
- **Output**: APPROVED | NEEDS_REVISION
- **Checklist**: Task atomicity, dependencies, test coverage, risks

### @code-reviewer
- **Purpose**: Code quality and maintainability review
- **Tools**: Read, Grep, Glob
- **Invoked by**: `/epci` Phase 2, `/epci-quick`
- **Output**: Review report with severity levels
- **Checklist**: SOLID, DRY, KISS, naming, error handling

### @security-auditor
- **Purpose**: OWASP Top 10 security audit
- **Tools**: Read, Grep
- **Invoked by**: `/epci` Phase 2 (conditional)
- **Condition**: Files with auth, API, input handling
- **Output**: Security report with vulnerabilities
- **Checklist**: Injection, XSS, CSRF, auth bypass, data exposure

### @qa-reviewer
- **Purpose**: Test quality and coverage review
- **Tools**: Read, Grep, Bash
- **Invoked by**: `/epci` Phase 2 (conditional)
- **Condition**: STANDARD/LARGE with complex tests
- **Output**: QA report with recommendations
- **Checklist**: Coverage, edge cases, mocking, assertions

### @doc-generator
- **Purpose**: Generate technical documentation
- **Tools**: Read, Write, Glob
- **Invoked by**: `/epci` Phase 3
- **Output**: README updates, API docs, CHANGELOG entries

## Frontmatter Patterns

### Validator Subagent
```yaml
---
name: {{name}}-validator
description: >-
  Validate {{subject}} against {{criteria}}. Invoked {{when}}.
  Produces {{verdict_type}} verdict.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep]
---
```

### Reviewer Subagent
```yaml
---
name: {{name}}-reviewer
description: >-
  Review {{subject}} for {{quality_aspects}}. Invoked {{when}}.
  Reports issues by severity level.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Grep, Glob]
---
```

### Generator Subagent
```yaml
---
name: {{name}}-generator
description: >-
  Generate {{output_type}} from {{input}}. Invoked {{when}}.
  Creates {{deliverables}}.
model: claude-sonnet-4-20250514
allowed-tools: [Read, Write, Glob]
---
```

## Tool Guidelines

### Least Privilege Principle

| Mission Type | Minimum Tools |
|--------------|---------------|
| Read/Analysis | Read, Grep |
| Validation | Read, Grep |
| Review | Read, Grep, Glob |
| Generation | Read, Write |
| Execution | Read, Bash |

### Tools to Restrict

| Tool | Only If |
|------|---------|
| Write | Creates new files as output |
| Edit | Modifies existing files |
| Bash | Runs commands (tests, linters) |
| Glob | Needs file pattern matching |

## Output Patterns

### Verdict-Based Output
```markdown
## {{Report Title}}

### Summary
{{1-2 sentence summary}}

### Findings
{{structured findings}}

### Verdict
**{{APPROVED | NEEDS_FIXES | REJECTED}}**

**Reasoning:** {{justification}}
```

### Severity-Based Output
```markdown
## {{Review Title}}

### Summary
{{overview}}

### Issues

#### 🔴 Critical
{{critical issues}}

#### 🟠 Important
{{important issues}}

#### 🟡 Minor
{{minor issues}}

### Recommendations
{{actionable recommendations}}
```

## Checklist Patterns

### Quality Checklist
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Conditional Checklist
- [ ] If {{condition}}: Check {{criterion}}
- [ ] If {{condition}}: Check {{criterion}}
