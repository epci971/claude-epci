# TDD Rules

Reference for Test-Driven Development workflow in EPCI implementation.

---

## TDD Cycle: RED → GREEN → REFACTOR

### RED Phase (Write Failing Test)

#### Rules
- :red_circle: NEVER skip writing the test first
- :red_circle: NEVER write implementation before test
- :white_check_mark: ALWAYS write one test at a time
- :white_check_mark: ALWAYS verify test fails for the right reason
- :white_check_mark: ALWAYS keep test focused on one behavior

#### Process
1. Identify the next behavior to implement
2. Write a test that defines expected behavior
3. Run the test to confirm it fails
4. Verify failure message indicates missing implementation (not syntax error)

#### Example
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

---

### GREEN Phase (Make Test Pass)

#### Rules
- :red_circle: NEVER write more code than needed to pass
- :red_circle: NEVER optimize during GREEN phase
- :white_check_mark: ALWAYS write minimal implementation
- :white_check_mark: ALWAYS run test after each change
- :white_check_mark: ALWAYS verify no other tests broken

#### Process
1. Write the simplest code that makes the test pass
2. Run the test to confirm it passes
3. Verify all other tests still pass
4. Resist urge to add "obvious" improvements

#### Example
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

---

### REFACTOR Phase (Improve Code)

#### Rules
- :red_circle: NEVER change behavior during refactor
- :red_circle: NEVER skip running tests after refactor
- :white_check_mark: ALWAYS keep tests green during refactor
- :white_check_mark: ALWAYS improve one thing at a time
- :white_check_mark: ALWAYS apply identified patterns

#### Process
1. Identify improvement opportunities
2. Make one refactoring change
3. Run tests to confirm still passing
4. Repeat until satisfied with code quality

#### Refactoring Opportunities
- Extract methods for repeated code
- Rename for clarity
- Apply design patterns
- Remove duplication
- Improve error handling

---

## Test Categories

### Unit Tests
- Test single component in isolation
- Mock external dependencies
- Fast execution (< 100ms each)
- High coverage (70%+ lines)

### Integration Tests
- Test component interactions
- Use real dependencies where practical
- Test data flow between components
- Slower but more realistic

### E2E Tests (if applicable)
- Test full user workflows
- Use production-like environment
- Focus on critical paths
- Complement, not replace unit tests

---

## Test Quality Checklist

```
### Structure (AAA Pattern)
- [ ] Arrange: Set up test data and conditions
- [ ] Act: Execute the code under test
- [ ] Assert: Verify expected outcomes

### Naming
- [ ] Describes expected behavior
- [ ] Uses "should" or "when" format
- [ ] Specific about conditions and outcomes

### Independence
- [ ] No dependency on other tests
- [ ] No shared mutable state
- [ ] Can run in any order

### Readability
- [ ] Clear setup and expectations
- [ ] Minimal test-specific logic
- [ ] Obvious what's being tested
```

---

## Coverage Requirements

| Complexity | Line Coverage | Branch Coverage |
|------------|---------------|-----------------|
| STANDARD | >= 70% | >= 60% |
| LARGE | >= 80% | >= 70% |

### Coverage Exclusions
- Configuration files
- Generated code
- Pure type definitions
- External library wrappers (simple pass-through)

---

## Common Patterns

### Testing Async Code
```typescript
it('should handle async operation', async () => {
  const result = await asyncFunction();
  expect(result).toBeDefined();
});
```

### Testing Errors
```typescript
it('should throw on invalid input', async () => {
  await expect(asyncFunction(null)).rejects.toThrow('Invalid input');
});
```

### Testing with Mocks
```typescript
it('should call dependency', async () => {
  const mockDep = jest.fn().mockResolvedValue('result');
  const service = new Service(mockDep);

  await service.execute();

  expect(mockDep).toHaveBeenCalledTimes(1);
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Test after code | Misses edge cases | Write test first |
| Multiple assertions per behavior | Hard to debug | One assertion per test |
| Testing implementation | Brittle tests | Test behavior |
| Shared state | Flaky tests | Isolate each test |
| Over-mocking | False confidence | Mock at boundaries |
| Skipping refactor | Technical debt | Always refactor |
