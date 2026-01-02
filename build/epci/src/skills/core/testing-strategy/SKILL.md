---
name: testing-strategy
description: >-
  Testing strategies and patterns. Test pyramid, TDD, mocking, fixtures.
  Use when: Phase 2 implementation, defining test strategy, QA review.
  Not for: stack-specific tools (→ stack skills).
---

# Testing Strategy

## Overview

Guide to testing strategies for reliable and maintainable code.

## Test Pyramid

```
         /\
        /E2E\        Few, slow, expensive
       /──────\
      /Integra-\     Some, moderate
     /──tion────\
    /────────────\
   /    Unit      \  Many, fast, cheap
  /────────────────\
```

| Level | Quantity | Speed | Cost | Focus |
|-------|----------|-------|------|-------|
| Unit | 70% | < 10ms | Low | Isolated logic |
| Integration | 20% | < 1s | Medium | Components together |
| E2E | 10% | > 1s | High | User flows |

## Test-Driven Development (TDD)

### RED-GREEN-REFACTOR Cycle

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│   RED   │────►│  GREEN  │────►│REFACTOR │
│(test    │     │(minimal │     │(improve)│
│ fails)  │     │ code)   │     │         │
└─────────┘     └─────────┘     └────┬────┘
     ▲                               │
     └───────────────────────────────┘
```

### TDD Rules

1. **Test BEFORE code** — Always
2. **One test at a time** — Focus
3. **Minimal code** — Just enough to pass the test
4. **Refactor when green** — Never on red

## Test Patterns

### Arrange-Act-Assert (AAA)

```php
public function testUserValidation(): void
{
    // Arrange - Setup
    $user = new User('test@example.com');

    // Act - Execute
    $result = $user->validate();

    // Assert - Verify
    $this->assertTrue($result);
}
```

### Given-When-Then (BDD)

```gherkin
Given a user with valid email
When I validate the user
Then validation succeeds
```

## Test Coverage

### What to Test

| Priority | Type | Example |
|----------|------|---------|
| High | Happy path | Successful creation |
| High | Edge cases | Limits, null, empty |
| High | Error cases | Expected exceptions |
| Medium | Boundary | Min, max, overflow |
| Low | Corner cases | Rare combinations |

### Coverage Matrix

```
                    Input
                 Valid  Invalid
              ┌───────┬────────┐
Output  OK    │   ✅  │   ❌   │
              ├───────┼────────┤
        Error │   ❌  │   ✅   │
              └───────┴────────┘
```

## Mocking

### When to Mock ✅

- External dependencies (API, DB, filesystem)
- Slow or expensive behaviors
- Hard to reproduce cases (network errors)
- Uncontrollable third-party services

### When NOT to Mock ❌

- The code being tested (SUT)
- Value objects
- Simple logic
- Stable internal dependencies

### Types of Test Doubles

| Type | Usage | Example |
|------|-------|---------|
| Dummy | Fills parameter | `new NullLogger()` |
| Stub | Returns fixed value | `$mock->willReturn(42)` |
| Spy | Records calls | `$mock->expects($this->once())` |
| Mock | Verifies behavior | `$mock->expects(...)->with(...)` |
| Fake | Simplified implementation | `InMemoryRepository` |

## Fixtures and Factories

### Fixtures

```php
// Static, predictable data
$user = $this->fixtures->getReference('user-admin');
```

### Factories

```php
// Dynamic, flexible data
$user = UserFactory::new()
    ->admin()
    ->verified()
    ->create();
```

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Mock testing | Tests implementation | Test behavior |
| Flaky test | Passes/fails randomly | Eliminate time dependencies |
| Coupled test | Depends on other tests | Isolated tests |
| Slow test | Suite > 10 min | More unit, less E2E |
| Fragile test | Breaks for nothing | Test contracts, not implementation |
| Over-mocking | Mocks everything | Prefer simple real objects |

## Checklist Before Merge

- [ ] Tests for happy path
- [ ] Tests for edge cases
- [ ] Tests for expected errors
- [ ] No tests depending on other tests
- [ ] No flaky tests
- [ ] All tests pass
- [ ] Acceptable coverage (>80% for critical code)
