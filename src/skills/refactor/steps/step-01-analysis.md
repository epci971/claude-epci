# Step 01: Analysis

> Collect metrics BEFORE, detect code smells, build dependency graph.

## Trigger

- Previous step: `step-00-init.md` completed

## Inputs

| Input | Source |
|-------|--------|
| Target files | From step-00 |
| Stack context | From step-00 |
| @Explore results | Background task |

## Protocol

### 1. Collect Metrics BEFORE

Use stack-appropriate tools with Claude fallback:

#### Python (radon/xenon)

```bash
# Cyclomatic Complexity
radon cc <target> -a -s

# Maintainability Index
radon mi <target> -s

# Lines of Code
radon raw <target> -s
```

#### PHP (phploc)

```bash
phploc <target>
```

#### JavaScript/Java (lizard)

```bash
lizard <target> --CCN 10
```

#### Fallback (Claude Estimation)

If tools unavailable, estimate:
- **LOC**: Count lines (excluding blanks/comments)
- **CC**: Count decision points (if, for, while, case, &&, ||)
- **Methods**: Count function/method definitions

### 2. Store Metrics

```json
{
  "metrics_before": {
    "files": [
      {
        "path": "src/services/auth.py",
        "loc": 450,
        "cyclomatic_complexity": 25,
        "maintainability_index": 45,
        "methods_count": 18,
        "avg_method_length": 25
      }
    ],
    "totals": {
      "loc": 450,
      "avg_cc": 25,
      "avg_mi": 45
    },
    "tool_used": "radon|phploc|lizard|claude-estimation"
  }
}
```

### 3. Detect Code Smells

Use hybrid detection (Claude + rules):

| Smell | Rule | Threshold |
|-------|------|-----------|
| Long Method | Lines or CC | > 20 lines OR CC > 10 |
| Large Class | Lines or methods | > 300 lines OR > 20 methods |
| Duplicated Code | Similar blocks | > 6 similar lines |
| Feature Envy | External calls | > 5 calls to same external class |
| God Class | Responsibilities | > 5 distinct concerns |
| Dead Code | Unused | No references |
| Deep Nesting | Indentation | > 4 levels |
| Long Parameter List | Parameters | > 5 parameters |

@../references/code-smells-catalog.md

See code-smells-catalog.md (imported above).

### 4. Build Dependency Graph

```
For each target file:
  → List imports (internal)
  → List exports (public API)
  → Identify dependents (files importing this)
  → Identify dependencies (files this imports)
```

Output format:

```json
{
  "dependency_graph": {
    "nodes": [
      {"id": "auth.py", "type": "target"},
      {"id": "user.py", "type": "dependency"},
      {"id": "session.py", "type": "dependent"}
    ],
    "edges": [
      {"from": "auth.py", "to": "user.py", "type": "imports"},
      {"from": "session.py", "to": "auth.py", "type": "imports"}
    ]
  }
}
```

### 5. Summarize Analysis

Present to user:

```
## Analysis Results

**Target**: src/services/auth.py
**Scope**: module (3 files affected)
**Stack**: python-django

### Metrics Before
| File | LOC | CC | MI |
|------|-----|----|----|
| auth.py | 450 | 25 | 45 |

### Code Smells Detected
1. **Long Method** (HIGH): `authenticate()` - 85 lines, CC=15
2. **Feature Envy** (MEDIUM): `validate_token()` - 8 calls to UserModel
3. **Deep Nesting** (LOW): `refresh_session()` - 5 levels

### Dependencies
- Imports: user.py, config.py
- Dependents: session.py, middleware.py, views/login.py
```

## Outputs

| Output | Destination |
|--------|-------------|
| `metrics_before` | State |
| `code_smells` | State |
| `dependency_graph` | State |
| Analysis summary | User display |

## Next Step

→ `step-02-planning.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Metrics tool fails | Fallback to Claude estimation |
| Circular dependency detected | Flag for Mikado Method in planning |
| No code smells found | Proceed (user requested refactoring) |
