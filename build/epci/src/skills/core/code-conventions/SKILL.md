---
name: code-conventions
description: >-
  Generic code conventions and best practices. Naming, file structure,
  comments, error handling. Use when: Phase 2 implementation, code review.
  Not for: stack-specific conventions (→ stack skills).
---

# Code Conventions

## Overview

Universal code conventions for readable and maintainable code.

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `UserService` |
| Methods | camelCase | `getUserById()` |
| Variables | camelCase | `$userName` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Files | kebab-case or PascalCase | `user-service.ts` |
| Databases | snake_case | `user_accounts` |

### Naming Rules

| Rule | Good | Bad |
|------|------|-----|
| Explicit | `getUserEmailById` | `get` |
| No abbreviations | `configuration` | `cfg` |
| Verbs for actions | `calculateTotal()` | `total()` |
| Nouns for data | `userCount` | `countUser` |
| Booleans with is/has | `isActive`, `hasPermission` | `active`, `permission` |

## File Structure

### Order in a Class

```
1. Constants
2. Static properties
3. Instance properties
4. Constructor
5. Public methods
6. Protected methods
7. Private methods
```

### Size Limits

| Element | Ideal | Maximum |
|---------|-------|---------|
| Function | < 20 lines | 50 lines |
| Class | < 200 lines | 400 lines |
| File | < 300 lines | 500 lines |
| Parameters | ≤ 3 | 5 |
| Indentation levels | ≤ 3 | 4 |

## Error Handling

### DO ✅

```
- Fail fast (validate at entry)
- Typed and specific exceptions
- Explicit error messages with context
- Structured error logging
- Recovery strategy when possible
```

### DON'T ❌

```
- Empty catch (swallow exceptions)
- Generic exception everywhere
- Return null for errors
- Ignore errors
- Log without context
```

### Handling Pattern

```
try {
    // Risky code
} catch (SpecificException $e) {
    // Log with context
    $this->logger->error('Operation failed', [
        'operation' => 'create_user',
        'error' => $e->getMessage(),
        'context' => $context
    ]);
    // Rethrow or recover
    throw new DomainException('User creation failed', 0, $e);
}
```

## Comments

| Type | When | Format |
|------|------|--------|
| Doc | Public API | `/** @param ... @return ... */` |
| TODO | Future improvement | `// TODO: [ticket] description` |
| FIXME | Known bug | `// FIXME: [ticket] description` |
| Inline | Complex logic only | `// Explanation of why` |

### Comment Rules

- **Comment the WHY**, not the WHAT
- Avoid obvious comments
- Update comments with the code
- Prefer self-documenting code

## DRY, KISS, YAGNI Principles

| Principle | Meaning | Check |
|-----------|---------|-------|
| **DRY** | Don't Repeat Yourself | No copy-paste |
| **KISS** | Keep It Simple, Stupid | Simplest solution |
| **YAGNI** | You Aren't Gonna Need It | No "just in case" code |

## Quick Reference Checklist

| Rule | ✅ Check |
|------|---------|
| Explicit naming | No `x`, `data`, `temp` |
| Single responsibility | Function = 1 thing |
| No magic numbers | Named constants |
| No duplication | Factor if > 2 occurrences |
| Error handling | No empty catch |
| Reasonable size | Functions < 50 lines |
| Limited indentation | Max 4 levels |

## Code Smells to Avoid

| Smell | Symptom | Solution |
|-------|---------|----------|
| Long Method | > 50 lines | Extract Method |
| Large Class | > 400 lines | Extract Class |
| Feature Envy | Uses another class too much | Move Method |
| Data Clumps | Same params repeated | Extract Class/DTO |
| Primitive Obsession | Too many primitives | Value Objects |
| Switch Statements | Switch on types | Polymorphism |
