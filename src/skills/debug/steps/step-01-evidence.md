---
name: step-01-evidence
description: Gather diagnostic evidence from multiple sources
prev_step: steps/step-00-clarify.md
next_step: steps/step-02-research.md
---

# Step 01: Evidence

## MANDATORY EXECUTION RULES (READ FIRST):

- :red_circle: NEVER proceed without at least error message OR reproduction steps
- :red_circle: NEVER skip project-memory recall
- :white_check_mark: ALWAYS detect and load stack skill
- :white_check_mark: ALWAYS check recent git commits
- :white_check_mark: ALWAYS search for similar past bugs
- :thought_balloon: FOCUS on gathering observable facts, not assumptions

## EXECUTION PROTOCOLS:

### 1. Detect Stack Skill

Run stack detection (same as /quick):

```
STACK DETECTION ORDER:
1. Check for manage.py → python-django
2. Check package.json for react → javascript-react
3. Check pom.xml/build.gradle for spring-boot → java-springboot
4. Check composer.json for symfony → php-symfony
5. Check tailwind.config.* → frontend-editor
```

Load detected stack skill for debug patterns.

### 2. Extract Error Information

Parse from input:

| Data | Source | Required |
|------|--------|----------|
| Error message | User input | Yes |
| Error type/code | Parsed from message | Yes |
| Stack trace | User input | Preferred |
| File:line | Stack trace | If available |
| Timestamp | User input or logs | Optional |

### 3. Gather Reproduction Information

Document:

```
REPRODUCTION:
- Frequency: [Always | Sometimes (X%) | Rare | Once]
- Environment: [dev | staging | prod | all]
- User type: [all | specific role | specific user]
- Trigger: [specific action | random | scheduled]
- Steps:
  1. {step 1}
  2. {step 2}
  3. {step 3 - error occurs}
```

### 4. Check Recent Changes

Query git for recent commits:

```bash
git log --since="1 week" --oneline --all -- {relevant_paths}
```

Look for:
- Config changes
- Dependency updates
- Code changes in error area
- Recent merges

### 5. Recall Similar Bugs (project-memory)

```
similar_bugs = project_memory.recall_bugs([
  error_pattern,
  affected_files,
  error_type
])
```

For each match, extract:
- Previous root cause
- Applied solution
- Files involved
- Keywords that matched

### 6. Read Relevant Files

Based on stack trace and error location:

```
FILES TO READ:
1. {file from stack trace} - error location
2. {config file} - if config-related error
3. {test file} - existing tests for context
4. {related service} - dependencies
```

### 7. Collect Environment Info

If relevant:

| Info | Command | When |
|------|---------|------|
| Node version | `node -v` | JS errors |
| Python version | `python --version` | Python errors |
| Dependencies | `package.json` / `requirements.txt` | Dependency errors |
| Env variables | Check if referenced | Config errors |

## CONTEXT BOUNDARIES:

- This step expects: Clarified bug description
- This step produces: Evidence packet with all gathered information

## OUTPUT FORMAT:

```
## Evidence Gathered

### Error Information
- **Message**: {exact error message}
- **Type**: {error type/category}
- **Location**: {file:line}
- **Stack Trace**:
  ```
  {formatted stack trace}
  ```

### Reproduction
- **Frequency**: {Always | Sometimes | Rare}
- **Environment**: {env}
- **Steps**:
  1. {step}
  2. {step}
  3. {error occurs}

### Recent Changes
| Commit | Date | Author | Message | Relevant |
|--------|------|--------|---------|----------|
| {sha} | {date} | {author} | {msg} | {Yes/No} |

### Similar Bugs (from project-memory)
{If found}:
- **Bug #{id}**: {description}
  - Root cause: {cause}
  - Solution: {fix}
  - Similarity: {high | medium}

{If none}: No similar bugs found in project history.

### Stack Detected
- **Stack**: {stack-name | none}
- **Debug patterns loaded**: {Yes | No}

### Files Analyzed
- `{path1}` - {purpose}
- `{path2}` - {purpose}

Ready for research phase.
```

## ESCALATION TRIGGER:

If cannot gather minimum evidence:

```
+---------------------------------------------------------------------+
| [EVIDENCE GAP] Cannot Proceed                                        |
+---------------------------------------------------------------------+
| Missing: {error message | reproduction steps | both}                  |
|                                                                      |
| Please provide:                                                      |
| 1. Exact error message or behavior                                   |
| 2. Steps to reproduce                                                |
|                                                                      |
| Without this information, debugging cannot proceed systematically.   |
+---------------------------------------------------------------------+
```

## NEXT STEP TRIGGER:

Proceed to step-02-research.md when:
- At minimum: error message OR reproduction steps available
- Stack skill loaded (or marked as none)
- Recent changes checked
- project-memory queried
