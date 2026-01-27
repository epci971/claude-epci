# Code Smells Catalog

> Detection rules for common code smells (based on Fowler's taxonomy).

## Detection Approach

Use hybrid detection: Claude analysis + static rules.

```
DETECTION_PRIORITY:
1. Static rules (fast, objective)
2. Claude analysis (nuanced, context-aware)
3. Combined confidence scoring
```

---

## Bloaters

### Long Method

**Definition**: Method too long to understand at a glance.

**Detection Rules**:
| Metric | Threshold | Severity |
|--------|-----------|----------|
| Lines | > 20 | Medium |
| Lines | > 50 | High |
| Cyclomatic Complexity | > 10 | Medium |
| Cyclomatic Complexity | > 15 | High |

**Claude Hints**:
- Multiple levels of abstraction in one method
- Comments explaining "sections" of code
- Scroll required to see full method

**Refactoring**: Extract Method

---

### Large Class

**Definition**: Class trying to do too much.

**Detection Rules**:
| Metric | Threshold | Severity |
|--------|-----------|----------|
| Lines | > 300 | Medium |
| Lines | > 500 | High |
| Methods | > 20 | Medium |
| Methods | > 30 | High |
| Fields | > 15 | Medium |

**Claude Hints**:
- Multiple unrelated groups of methods
- "And" in class name (UserAndOrderManager)
- Difficult to summarize purpose in one sentence

**Refactoring**: Extract Class

---

### Long Parameter List

**Definition**: Method requires too many parameters.

**Detection Rules**:
| Metric | Threshold | Severity |
|--------|-----------|----------|
| Parameters | > 4 | Medium |
| Parameters | > 6 | High |

**Claude Hints**:
- Many parameters often passed together
- Boolean flags controlling behavior
- Null frequently passed for optional params

**Refactoring**: Introduce Parameter Object, Replace Parameter with Method

---

### Primitive Obsession

**Definition**: Using primitives instead of small objects.

**Detection Rules**:
- Multiple fields always used together (address: street, city, zip)
- String manipulation for structured data (phone formatting)
- Magic numbers/strings

**Claude Hints**:
- Validation logic scattered for same concept
- Type-specific behavior on primitives

**Refactoring**: Replace Primitive with Object, Extract Class

---

## Object-Orientation Abusers

### Feature Envy

**Definition**: Method more interested in another class's data.

**Detection Rules**:
| Metric | Threshold | Severity |
|--------|-----------|----------|
| Calls to another class | > 3 | Low |
| Calls to another class | > 5 | Medium |
| Getters from another class | > 4 | Medium |

**Claude Hints**:
- Method accesses many fields of single other object
- Could be static if moved to that class
- "ask, don't tell" violation

**Refactoring**: Move Method

---

### Switch Statements (Repeated)

**Definition**: Same switch/case on type appearing multiple times.

**Detection Rules**:
- Same enum/type in multiple switch statements
- Parallel conditionals on same variable

**Claude Hints**:
- Adding new type requires changes in multiple places
- Switch cases have similar structure

**Refactoring**: Replace Conditional with Polymorphism

---

### Refused Bequest

**Definition**: Subclass doesn't use inherited behavior.

**Detection Rules**:
- Override to throw NotImplementedError
- Override with empty implementation
- < 50% of inherited methods used

**Claude Hints**:
- Inheritance for code reuse, not is-a relationship
- Methods not applicable to subclass

**Refactoring**: Replace Inheritance with Delegation

---

## Change Preventers

### Divergent Change

**Definition**: Class changed for multiple unrelated reasons.

**Detection Rules**:
- Git history shows changes for different features
- Multiple "areas of concern" in one class

**Claude Hints**:
- "If X changes, modify methods A,B; if Y changes, modify C,D"
- Single class, multiple responsibilities

**Refactoring**: Extract Class

---

### Shotgun Surgery

**Definition**: Single change requires many small edits.

**Detection Rules**:
- Same concept scattered across many files
- Adding feature touches 5+ files minimally

**Claude Hints**:
- Difficult to find all places to change
- Risk of missing one location

**Refactoring**: Move Method, Inline Class (consolidate)

---

## Dispensables

### Dead Code

**Definition**: Code that is never executed.

**Detection Rules**:
- Unreachable code after return/throw
- Unused private methods
- Unused parameters
- Commented-out code

**Tools**:
- Python: vulture, pylint
- JavaScript: eslint (no-unused-vars)
- IDE inspections

**Refactoring**: Remove (Inline with nothing)

---

### Duplicated Code

**Definition**: Same code structure in multiple places.

**Detection Rules**:
| Metric | Threshold | Severity |
|--------|-----------|----------|
| Identical lines | > 6 | Medium |
| Similar structure | > 10 | Medium |
| Copy-paste (fuzzy) | > 15 | High |

**Tools**:
- Python: pylint (duplicate-code)
- Generic: PMD CPD, jscpd

**Claude Hints**:
- "Copy and modify" pattern visible
- Bug fixes need to be applied multiple times

**Refactoring**: Extract Method, Extract Module

---

### Speculative Generality

**Definition**: Code created "just in case" but never used.

**Detection Rules**:
- Abstract classes with single concrete implementation
- Parameters/methods never called
- Hooks that are never hooked

**Claude Hints**:
- "We might need this later"
- Over-engineered for current requirements

**Refactoring**: Collapse Hierarchy, Inline Class, Remove

---

## Couplers

### Inappropriate Intimacy

**Definition**: Classes too tightly coupled.

**Detection Rules**:
- Class accesses private/protected members of another
- Bidirectional associations
- Inner class accessing many outer fields

**Refactoring**: Move Method, Extract Class, Replace Inheritance with Delegation

---

### Message Chains

**Definition**: Client depends on navigation structure.

**Detection Rules**:
```python
# Pattern: a.getB().getC().getD().getValue()
chain_length > 3  # Suspicious
chain_length > 4  # Definite smell
```

**Refactoring**: Hide Delegate, Extract Method

---

### Middle Man

**Definition**: Class that only delegates to another.

**Detection Rules**:
- > 50% of methods just call another object's method
- No added value in delegation

**Refactoring**: Remove Middle Man, Inline Method

---

## Severity Classification

| Severity | Impact | Action |
|----------|--------|--------|
| **High** | Significantly harms maintainability | Address in this refactoring |
| **Medium** | Moderate impact, technical debt | Consider addressing |
| **Low** | Minor issue, code style | Optional, document if skipped |

---

## Detection Output Format

```json
{
  "code_smells": [
    {
      "type": "Long Method",
      "severity": "high",
      "location": {
        "file": "auth.py",
        "method": "authenticate",
        "start_line": 45,
        "end_line": 130
      },
      "metrics": {
        "lines": 85,
        "cyclomatic_complexity": 15
      },
      "suggested_refactoring": "extract-method",
      "confidence": 0.95
    }
  ]
}
```
