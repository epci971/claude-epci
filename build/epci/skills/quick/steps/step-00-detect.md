---
name: step-00-detect
description: Detect input type, stack skills, and validate complexity
prev_step: null
next_step: steps/step-01-mini-explore.md
conditional_next:
  - condition: "input starts with @"
    step: steps/step-03-code.md
  - condition: "complexity == STANDARD or complexity == LARGE"
    step: null
    action: "suggest /implement and abort"
---

# Step 00: Detection

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER proceed if complexity > SMALL
- :red_circle: NEVER skip stack detection
- :white_check_mark: ALWAYS parse input first (@ prefix = plan path)
- :white_check_mark: ALWAYS validate plan file exists if @path provided
- :white_check_mark: ALWAYS invoke complexity-calculator
- :thought_balloon: FOCUS on correct routing: plan-first vs full workflow

## EXECUTION PROTOCOLS:

### 1. Parse Input

```
INPUT FORMAT:
├── @path → Plan-first workflow
│   └─ Examples: @.claude/plans/fix.md, @docs/plans/feature.md
│
└── "text" → Full workflow (mini E-P first)
    └─ Examples: "fix login button", "add email validation"
```

**Actions:**
- Extract input type (plan vs text)
- If @path: verify file exists, load content
- If text: extract key terms for complexity analysis

### 2. Detect Native Plan (if @path)

Check if file is a native Claude Code plan:

```python
def is_native_plan(file_path: str) -> bool:
    # Pattern 1: Conventional path
    if ".claude/plans/" in file_path or "docs/plans/" in file_path:
        return True

    # Pattern 2: Frontmatter with saved_at
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter and "saved_at" in frontmatter:
        return True

    return False
```

**If native plan:**
- Extract objective from plan
- Extract target files from plan
- Extract completion criteria
- Skip to step-03-code.md

### 3. Detect Stack Skills

Run stack detection algorithm (see [references/stack-detection.md](../references/stack-detection.md)):

```
STACK DETECTION ORDER:
1. Check root directory for signature files
2. Check dependency manifests (package.json, requirements.txt, etc.)
3. Check directory structure
4. Score confidence and select best match
```

**Detected stack → Load stack skill for context:**
- `python-django`: Django patterns, pytest conventions
- `javascript-react`: React patterns, Jest/Vitest
- `java-springboot`: Spring patterns, JUnit
- `php-symfony`: Symfony patterns, PHPUnit
- `frontend-editor`: Tailwind patterns, a11y

### 4. Validate Complexity

Invoke `complexity-calculator`:

```python
result = complexity.calculate(input_description)
# Returns: { category, confidence, factors, recommended_workflow }
```

**Routing Decision:**

| Complexity | Action |
|------------|--------|
| TINY | Continue → step-01 or step-03 |
| SMALL | Continue → step-01 or step-03 |
| STANDARD | ABORT → Suggest /implement |
| LARGE | ABORT → Suggest /implement |

### 5. Initialize State (Minimal)

If proceeding, create minimal state entry:

```json
{
  "id": "{generated-slug}",
  "status": "in_progress",
  "current_phase": "detect",
  "complexity": "{TINY|SMALL}",
  "created_at": "{ISO-8601}",
  "created_by": "/quick",
  "input_type": "{plan|text}",
  "detected_stack": "{stack-name|null}"
}
```

## CONTEXT BOUNDARIES:

- This step expects: User input (text or @plan-path)
- This step produces: Routing decision, stack context, complexity validation

## OUTPUT FORMAT:

```
## Detection Complete

Input Type: {plan | text}
Stack Detected: {stack-name | none}
Complexity: {TINY | SMALL}
Confidence: {0.0-1.0}

Routing: {step-01-mini-explore | step-03-code}
```

## ESCALATION TRIGGER:

If complexity == STANDARD or LARGE:

```
┌─────────────────────────────────────────────────────────────────┐
│ [ESCALATION] Task Too Complex for /quick                         │
├─────────────────────────────────────────────────────────────────┤
│ Detected Complexity: {STANDARD | LARGE}                          │
│ Estimated: ~{loc} LOC across {files} files                       │
│                                                                  │
│ This task exceeds /quick limits (max SMALL: 200 LOC, 3 files)   │
│                                                                  │
│ Recommended: /implement {feature-slug}                           │
└─────────────────────────────────────────────────────────────────┘
```

## NEXT STEP TRIGGER:

- If @plan provided and valid → step-03-code.md (skip E-P)
- If text description → step-01-mini-explore.md
- If STANDARD/LARGE → Abort with /implement suggestion
