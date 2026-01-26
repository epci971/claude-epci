---
id: task-006
title: Create New References
slug: new-references
feature: skill-implement
complexity: M
estimated_minutes: 90
dependencies:
  - task-002
  - task-003
  - task-004
  - task-005
files_affected:
  - path: src/skills/implement/references/stack-integration.md
    action: create
  - path: src/skills/implement/references/multi-agent-review.md
    action: create
  - path: src/skills/implement/references/turbo-mode.md
    action: create
test_approach: Manual
---

# Task 006: Create New References

## Objective

Create three new reference files that provide detailed documentation for stack integration, multi-agent review architecture, and turbo mode workflow. These files supplement the SKILL.md and steps with in-depth technical details.

---

## Context

Reference files in EPCI skills serve as detailed documentation that goes beyond what fits in SKILL.md or step files. They are loaded on-demand when specific topics need elaboration.

The three files cover:
1. Stack integration details (detection, injection, transmission)
2. Multi-agent review architecture (parallel, synthesis, severity)
3. Turbo mode workflow (differences, flags, shortcuts)

---

## Acceptance Criteria

### AC1: stack-integration.md Complete

- **Given**: The new references/ directory
- **When**: stack-integration.md is created
- **Then**: Contains detection patterns, rules-templates mapping, injection protocol, and agent transmission details

### AC2: multi-agent-review.md Complete

- **Given**: The new references/ directory
- **When**: multi-agent-review.md is created
- **Then**: Contains parallel execution pattern, agent selection matrix, synthesis algorithm, and severity handling

### AC3: turbo-mode.md Complete

- **Given**: The new references/ directory
- **When**: turbo-mode.md is created
- **Then**: Contains flag documentation, workflow differences table, skipped steps, and use cases

### AC4: Cross-References Added

- **Given**: All three reference files
- **When**: Reviewed for completeness
- **Then**: Files reference each other and link back to SKILL.md sections

---

## Steps

### Step 1: Create stack-integration.md (30 min)

**Input**: Brief section 4, stack skills SKILL.md files

**Actions**:
1. Create file with standard reference header
2. Add "## Detection Patterns" section with detailed patterns per stack:
   - python-django: manage.py, pyproject.toml with django, requirements*.txt with Django
   - javascript-react: package.json with react dependency, .tsx files
   - php-symfony: composer.json with symfony/*, bin/console
   - java-springboot: pom.xml or build.gradle with spring-boot-starter
   - frontend-editor: tailwind.config.js/ts, postcss.config.*
3. Add "## Rules Templates Mapping" table
4. Add "## Injection Protocol" with step-by-step process
5. Add "## Agent Context Transmission" explaining how stack context flows to agents
6. Add examples and code snippets

**Output**: Complete stack-integration.md

**Validation**: All 5 stacks fully documented with detection and rules

---

### Step 2: Create multi-agent-review.md (30 min)

**Input**: Brief section 5, Perplexity research on multi-agent patterns

**Actions**:
1. Create file with standard reference header
2. Add "## Architecture Overview" with parallel fan-out diagram
3. Add "## Agent Selection Matrix" table:
   - @code-reviewer: Always, Opus, full codebase
   - @security-auditor: Conditional, Opus, security focus
   - @qa-reviewer: Conditional, Sonnet, test quality
4. Add "## Parallel Execution" with Task tool pattern
5. Add "## Critic Synthesis Algorithm":
   - Collect, Parse, Dedupe, Classify, Report
6. Add "## Severity Handling" with Critical/Important/Minor definitions
7. Add "## Auto-Fix Rules" with decision tree
8. Include examples of review report format

**Output**: Complete multi-agent-review.md

**Validation**: Parallel pattern and synthesis clearly documented

---

### Step 3: Create turbo-mode.md (20 min)

**Input**: Brief section 8, decision D9

**Actions**:
1. Create file with standard reference header
2. Add "## Overview" explaining turbo mode purpose
3. Add "## Activation" with --turbo flag documentation
4. Add "## Workflow Differences" table:
   | Aspect | Standard | Turbo |
   | Breakpoints | 4 | 1 |
   | Reviews | Sequential→Parallel | All Parallel |
   | Explore phase | Full | Skip if @plan |
   | Plan validation | @plan-validator | Skip |
   | Auto-fix | Minor only | Minor + Important |
5. Add "## Use Cases":
   - Frequent commits on stable codebase
   - Hotfixes with time pressure
   - Features with existing tests
6. Add "## Limitations" and when NOT to use turbo

**Output**: Complete turbo-mode.md

**Validation**: Clear comparison table and use cases documented

---

### Step 4: Add Cross-References (10 min)

**Input**: All three new reference files, SKILL.md, step files

**Actions**:
1. Add "## See Also" section to each reference file
2. Link to related SKILL.md sections
3. Link to relevant step files
4. Cross-link between reference files where appropriate
5. Verify all links are relative and correct

**Output**: Cross-referenced documentation

**Validation**: All links work, documentation is connected

---

## Files

| Path | Action | Description |
|------|--------|-------------|
| `src/skills/implement/references/stack-integration.md` | create | Stack detection and injection details |
| `src/skills/implement/references/multi-agent-review.md` | create | Parallel review architecture details |
| `src/skills/implement/references/turbo-mode.md` | create | Turbo mode workflow documentation |

---

## Test Approach

- **Type**: Manual
- **Framework**: Documentation review
- **Location**: N/A (manual review)
- **Coverage Target**: N/A

### Test Cases

| # | Description | Type | Priority |
|---|-------------|------|----------|
| 1 | stack-integration.md has all 5 stacks | Manual | High |
| 2 | multi-agent-review.md has parallel pattern | Manual | High |
| 3 | turbo-mode.md has comparison table | Manual | High |
| 4 | All cross-references link correctly | Manual | Medium |
| 5 | No broken relative links | Manual | Medium |

---

## Dependencies

### Requires (blockedBy)

- **task-002**: Stack & Core section in SKILL.md defines what references detail
- **task-003**: step-00-init references stack detection
- **task-004**: step-03-code references TDD rules
- **task-005**: step-04-review references multi-agent architecture

### Blocks

*No other tasks depend on this one*

---

## Notes

- Reference files should be standalone (readable without SKILL.md context)
- Keep each file under 300 lines for readability
- Use consistent formatting across all three files
- Include practical examples where helpful
- Run validation script after creation

---

*Task specification generated by /spec v1.0 — EPCI v6.0*
