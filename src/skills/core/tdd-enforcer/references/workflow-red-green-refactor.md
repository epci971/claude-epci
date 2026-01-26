# TDD Workflow: RED-GREEN-REFACTOR-VERIFY

Reference for the complete Test-Driven Development cycle in EPCI implementations.

---

## Cycle Overview

```
RED → GREEN → REFACTOR → VERIFY
 │      │         │         │
 │      │         │         └─ All tests pass, coverage met
 │      │         └─ Clean up code, maintain green
 │      └─ Minimal code to pass test
 └─ Write failing test first
```

---

## Phase 1: RED (Write Failing Test)

### Rules

| Icon | Rule |
|------|------|
| :no_entry: | NEVER skip writing the test first |
| :no_entry: | NEVER write implementation before test |
| :white_check_mark: | ALWAYS write one test at a time |
| :white_check_mark: | ALWAYS verify test fails for the right reason |
| :white_check_mark: | ALWAYS keep test focused on one behavior |

### Process

1. Identify the next behavior to implement
2. Write a test that defines expected behavior
3. Run the test to confirm it fails
4. Verify failure message indicates missing implementation (not syntax error)

### Example

```typescript
// RED: Test that should fail
describe('UserService', () => {
  it('should create a user with valid data', async () => {
    const service = new UserService();
    const user = await service.create({ name: 'John', email: 'john@example.com' });

    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
    expect(user.email).toBe('john@example.com');
  });
});
```

### Validation Criteria

- Test execution returns exit code 1
- Failure is due to missing/incomplete implementation
- No syntax errors or import failures

---

## Phase 2: GREEN (Make Test Pass)

### Rules

| Icon | Rule |
|------|------|
| :no_entry: | NEVER write more code than needed to pass |
| :no_entry: | NEVER optimize during GREEN phase |
| :white_check_mark: | ALWAYS write minimal implementation |
| :white_check_mark: | ALWAYS run test after each change |
| :white_check_mark: | ALWAYS verify no other tests broken |

### Process

1. Write the simplest code that makes the test pass
2. Run the test to confirm it passes
3. Verify all other tests still pass
4. Resist urge to add "obvious" improvements

### Example

```typescript
// GREEN: Minimal implementation to pass
class UserService {
  async create(data: { name: string; email: string }) {
    return {
      id: crypto.randomUUID(),
      name: data.name,
      email: data.email,
    };
  }
}
```

### Validation Criteria

- Test execution returns exit code 0
- No regression in existing tests
- Implementation is minimal (no extra features)

---

## Phase 3: REFACTOR (Improve Code)

### Rules

| Icon | Rule |
|------|------|
| :no_entry: | NEVER change behavior during refactor |
| :no_entry: | NEVER skip running tests after refactor |
| :white_check_mark: | ALWAYS keep tests green during refactor |
| :white_check_mark: | ALWAYS improve one thing at a time |
| :white_check_mark: | ALWAYS apply identified patterns |

### Process

1. Identify improvement opportunities
2. Make one refactoring change
3. Run tests to confirm still passing
4. Repeat until satisfied with code quality

### Refactoring Opportunities

| Category | Examples |
|----------|----------|
| Structure | Extract methods, split classes |
| Naming | Rename for clarity, consistent terminology |
| Patterns | Apply design patterns where appropriate |
| Duplication | DRY principle, extract shared logic |
| Errors | Improve error handling, messages |

### Validation Criteria

- All tests still pass after each change
- No new features added
- Code quality improved (readability, maintainability)

---

## Phase 4: VERIFY (Final Verification)

### Rules

| Icon | Rule |
|------|------|
| :no_entry: | NEVER skip final verification |
| :no_entry: | NEVER ignore coverage requirements |
| :white_check_mark: | ALWAYS run full test suite |
| :white_check_mark: | ALWAYS check coverage thresholds |
| :white_check_mark: | ALWAYS verify integration points |

### Process

1. Run complete test suite
2. Check coverage meets requirements
3. Verify no flaky tests
4. Confirm feature works end-to-end

### Validation Criteria

- All tests pass (exit code 0)
- Coverage meets complexity threshold
- No flaky or intermittent failures

---

## Common Patterns

### Testing Async Code

```typescript
it('should handle async operation', async () => {
  // Arrange
  const service = new DataService();

  // Act
  const result = await service.fetchData();

  // Assert
  expect(result).toBeDefined();
  expect(result.status).toBe('success');
});
```

### Testing Errors

```typescript
it('should throw on invalid input', async () => {
  const service = new ValidationService();

  await expect(service.validate(null))
    .rejects.toThrow('Invalid input');
});

it('should throw specific error type', async () => {
  const service = new AuthService();

  await expect(service.login('', ''))
    .rejects.toBeInstanceOf(AuthenticationError);
});
```

### Testing with Mocks

```typescript
it('should call dependency correctly', async () => {
  // Arrange
  const mockRepository = {
    save: jest.fn().mockResolvedValue({ id: '123' }),
  };
  const service = new UserService(mockRepository);

  // Act
  await service.createUser({ name: 'John' });

  // Assert
  expect(mockRepository.save).toHaveBeenCalledTimes(1);
  expect(mockRepository.save).toHaveBeenCalledWith(
    expect.objectContaining({ name: 'John' })
  );
});
```

### Testing Edge Cases

```typescript
describe('edge cases', () => {
  it('should handle empty array', () => {
    expect(calculateAverage([])).toBe(0);
  });

  it('should handle single element', () => {
    expect(calculateAverage([5])).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(calculateAverage([-1, -2, -3])).toBe(-2);
  });
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Test after code | Misses edge cases, tests confirm bugs | Write test first, always |
| Multiple assertions per behavior | Hard to debug, unclear failures | One assertion per test |
| Testing implementation | Brittle tests, break on refactor | Test behavior, not internals |
| Shared state | Flaky tests, order-dependent | Isolate each test completely |
| Over-mocking | False confidence, miss integration bugs | Mock at boundaries only |
| Skipping refactor | Technical debt accumulates | Always refactor phase |
| Gold-plating in GREEN | Scope creep, over-engineering | Minimal code to pass only |
| Ignoring failure reason | False green, hidden bugs | Verify failure message |

---

## Phase Transitions

### RED → GREEN

**Allowed when:**
- Test fails for correct reason (missing implementation)
- No syntax or import errors

**Not allowed when:**
- Test passes (already implemented)
- Test fails for wrong reason (setup issue)

### GREEN → REFACTOR

**Allowed when:**
- Current test passes
- All other tests pass

**Not allowed when:**
- Any test failing
- Untested code paths remain

### REFACTOR → VERIFY

**Allowed when:**
- Refactoring complete
- All tests still pass

**Not allowed when:**
- Tests broken by refactor
- Code changes behavior

### VERIFY → Next Cycle

**Allowed when:**
- All tests pass
- Coverage thresholds met
- No flaky tests

**Not allowed when:**
- Coverage below threshold
- Integration issues detected
