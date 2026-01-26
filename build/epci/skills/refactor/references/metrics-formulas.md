# Metrics Formulas

> Reference for code quality metrics used in refactoring analysis.

## Core Metrics

### Lines of Code (LOC)

**Definition**: Count of executable lines (excluding blanks and comments).

**Variants**:
| Metric | Definition |
|--------|------------|
| LOC | Total lines |
| SLOC | Source lines (no blanks) |
| LLOC | Logical lines (statements) |
| CLOC | Comment lines |

**Calculation**:
```python
def count_loc(code):
    lines = code.split('\n')
    loc = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            loc += 1
    return loc
```

**Thresholds**:
| Context | Good | Warning | Bad |
|---------|------|---------|-----|
| Method | < 20 | 20-50 | > 50 |
| Class | < 200 | 200-400 | > 400 |
| Module | < 500 | 500-1000 | > 1000 |

---

### Cyclomatic Complexity (CC)

**Definition**: Number of linearly independent paths through code.

**Formula**:
```
CC = E - N + 2P

Where:
  E = number of edges in control flow graph
  N = number of nodes
  P = number of connected components (usually 1)
```

**Simplified Calculation**:
```python
def calculate_cc(code):
    cc = 1  # Base complexity

    # Add 1 for each decision point
    decision_points = ['if', 'elif', 'for', 'while', 'except', 'case', 'and', 'or', '?']

    for point in decision_points:
        cc += code.count(point)

    return cc
```

**Thresholds** (per method):
| CC | Risk Level | Recommendation |
|----|------------|----------------|
| 1-10 | Low | Simple, easy to test |
| 11-20 | Moderate | More complex, needs attention |
| 21-50 | High | Difficult to test, refactor |
| > 50 | Very High | Untestable, must refactor |

---

### Maintainability Index (MI)

**Definition**: Composite metric indicating ease of maintenance.

**Formula (SEI variant)**:
```
MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)

Where:
  HV = Halstead Volume
  CC = Cyclomatic Complexity
  LOC = Lines of Code
```

**Microsoft variant** (scales 0-100):
```
MI = max(0, (171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)) * 100 / 171)
```

**Thresholds**:
| MI | Rating | Color |
|----|--------|-------|
| 80-100 | Highly maintainable | Green |
| 60-79 | Moderately maintainable | Yellow |
| 40-59 | Difficult to maintain | Orange |
| 0-39 | Very difficult | Red |

---

### Halstead Metrics

**Operators and Operands**:
```
n1 = number of distinct operators
n2 = number of distinct operands
N1 = total number of operators
N2 = total number of operands
```

**Derived Metrics**:
```
Program Length:       N = N1 + N2
Vocabulary:           n = n1 + n2
Volume:               V = N * log2(n)
Difficulty:           D = (n1/2) * (N2/n2)
Effort:               E = D * V
Time to Program:      T = E / 18 (seconds)
Bugs Delivered:       B = V / 3000
```

**Example**:
```python
# Code: x = (y + z) * 2
# Operators: =, +, *, ( )
# Operands: x, y, z, 2

n1 = 4  # =, +, *, ()
n2 = 4  # x, y, z, 2
N1 = 4
N2 = 4

N = 8
n = 8
V = 8 * log2(8) = 24
```

---

## Coupling Metrics

### Afferent Coupling (Ca)

**Definition**: Number of classes that depend on this class.

```
High Ca = many dependents = changes are risky
```

---

### Efferent Coupling (Ce)

**Definition**: Number of classes this class depends on.

```
High Ce = many dependencies = fragile, hard to test
```

---

### Instability (I)

**Formula**:
```
I = Ce / (Ca + Ce)

Where:
  I = 0: Maximally stable (many dependents, no dependencies)
  I = 1: Maximally unstable (no dependents, many dependencies)
```

**Guidance**: Stable packages should be abstract; unstable packages should be concrete.

---

## Dependency Metrics

### Depth of Inheritance Tree (DIT)

**Definition**: Maximum length from class to root of hierarchy.

**Thresholds**:
| DIT | Assessment |
|-----|------------|
| 0-2 | Normal |
| 3-4 | Moderate |
| > 4 | Deep hierarchy, consider flattening |

---

### Number of Children (NOC)

**Definition**: Number of immediate subclasses.

**Thresholds**:
| NOC | Assessment |
|-----|------------|
| 0-3 | Normal |
| 4-6 | Many subclasses |
| > 6 | Consider interface or composition |

---

## Tools by Language

### Python

```bash
# radon - CC, MI, Halstead, LOC
radon cc src/ -a -s          # Cyclomatic complexity
radon mi src/ -s             # Maintainability index
radon hal src/               # Halstead metrics
radon raw src/ -s            # Raw metrics (LOC)

# xenon - CI threshold checker
xenon --max-absolute B --max-modules A --max-average A src/

# mccabe - CC only
python -m mccabe --min 10 src/module.py
```

### PHP

```bash
# phploc - Comprehensive metrics
phploc src/

# Output includes:
# - LOC (various types)
# - Cyclomatic Complexity
# - Dependencies
# - Classes, Methods, Functions
```

### JavaScript/TypeScript

```bash
# lizard - Multi-language
lizard src/ --CCN 10

# escomplex - Detailed analysis
escomplex src/**/*.js

# complexity-report
cr src/
```

### Java

```bash
# lizard
lizard src/ --CCN 10

# checkstyle (with CyclomaticComplexity check)
checkstyle -c complexity-checks.xml src/

# pmd - CPD for duplication
pmd cpd --minimum-tokens 100 --files src/
```

---

## Claude Estimation Fallback

When tools unavailable, Claude estimates:

```markdown
## Estimation Approach

1. **LOC**: Count non-blank, non-comment lines
2. **CC**: Count decision points:
   - +1 base
   - +1 for each: if, elif, for, while, except, and, or, ?:
3. **MI**: Rough assessment:
   - Green (80+): Short methods, simple logic
   - Yellow (60-79): Medium methods, some nesting
   - Orange (40-59): Long methods, complex logic
   - Red (<40): Very long, deeply nested

**Confidence Level**: Estimation ±20% vs tools
```

---

## Delta Calculation

```python
def calculate_delta(before, after):
    return {
        "absolute": after - before,
        "percent": ((after - before) / before) * 100 if before != 0 else 0,
        "trend": "improved" if (
            # For metrics where lower is better
            (metric in ["loc", "cc"] and after < before) or
            # For metrics where higher is better
            (metric in ["mi"] and after > before)
        ) else "degraded" if before != after else "unchanged"
    }
```
