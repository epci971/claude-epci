# Coverage Rules

Reference for test coverage requirements and test quality standards in EPCI.

---

## Coverage by Complexity

| Complexity | Line Coverage | Branch Coverage | TDD Mode |
|------------|---------------|-----------------|----------|
| TINY | Optional | Optional | `optional` |
| SMALL | >= 50% | >= 40% | `guided` |
| STANDARD | >= 70% | >= 60% | `guided` |
| LARGE | >= 80% | >= 70% | `strict` |

### Mode Definitions

| Mode | Behavior |
|------|----------|
| `optional` | Suggest tests, no enforcement |
| `guided` | Remind and prompt, allow skip with confirmation |
| `strict` | Block progress without passing tests |

---

## Test Categories

### Unit Tests

| Aspect | Requirement |
|--------|-------------|
| Scope | Single component in isolation |
| Dependencies | Mocked external dependencies |
| Execution | Fast (< 100ms each) |
| Coverage | Primary coverage target |

**When to use:** All business logic, utilities, services.

### Integration Tests

| Aspect | Requirement |
|--------|-------------|
| Scope | Component interactions |
| Dependencies | Real where practical |
| Execution | Slower but realistic |
| Coverage | Data flow, API contracts |

**When to use:** API endpoints, database operations, external services.

### E2E Tests (If Applicable)

| Aspect | Requirement |
|--------|-------------|
| Scope | Full user workflows |
| Environment | Production-like |
| Focus | Critical paths only |
| Role | Complement, not replace unit tests |

**When to use:** Critical user journeys, smoke tests.

---

## Coverage Exclusions

Files/patterns to exclude from coverage requirements:

| Category | Examples |
|----------|----------|
| Configuration | `*.config.js`, `*.config.ts` |
| Generated code | `*.generated.*`, `dist/` |
| Type definitions | `*.d.ts`, `types/` |
| Simple wrappers | Pass-through functions |
| Test files | `*.test.*`, `*.spec.*` |
| Mocks | `__mocks__/`, `*.mock.*` |

### Configuration Example

```json
{
  "collectCoverageFrom": [
    "src/**/*.{ts,tsx}",
    "!src/**/*.d.ts",
    "!src/**/*.config.*",
    "!src/**/types/**",
    "!src/**/__mocks__/**"
  ]
}
```

---

## Test Quality Checklist

### Structure (AAA Pattern)

```
- [ ] Arrange: Set up test data and conditions
- [ ] Act: Execute the code under test
- [ ] Assert: Verify expected outcomes
```

**Example:**
```typescript
it('should calculate total with discount', () => {
  // Arrange
  const cart = new Cart();
  cart.add({ price: 100, quantity: 2 });
  const discount = 0.1;

  // Act
  const total = cart.calculateTotal(discount);

  // Assert
  expect(total).toBe(180);
});
```

### Naming Conventions

```
- [ ] Describes expected behavior
- [ ] Uses "should" or "when/then" format
- [ ] Specific about conditions and outcomes
```

**Good names:**
- `should return empty array when no items match`
- `should throw ValidationError when email is invalid`
- `when user is admin, should allow delete operation`

**Bad names:**
- `test1`
- `works correctly`
- `handles edge case`

### Test Independence

```
- [ ] No dependency on other tests
- [ ] No shared mutable state
- [ ] Can run in any order
- [ ] Self-contained setup and teardown
```

### Readability

```
- [ ] Clear setup and expectations
- [ ] Minimal test-specific logic
- [ ] Obvious what's being tested
- [ ] No magic numbers without context
```

---

## Strategies by Complexity

### TINY (Optional TDD)

- Write tests if behavior is non-trivial
- Focus on happy path
- No coverage requirement

### SMALL (Guided TDD)

- Write tests for all public functions
- Cover happy path + one error case
- Target 50% line coverage

### STANDARD (Guided TDD)

- Full TDD cycle for each feature
- Cover happy path + error cases + edge cases
- Target 70% line coverage, 60% branch

### LARGE (Strict TDD)

- Mandatory TDD, no exceptions
- Comprehensive test suite
- Target 80% line coverage, 70% branch
- Include integration tests

---

## Coverage Commands

| Stack | Coverage Command |
|-------|------------------|
| Node.js (Jest) | `npm run test -- --coverage` |
| Node.js (Vitest) | `npm run test -- --coverage` |
| Python (pytest) | `pytest --cov=src --cov-report=term` |
| Java (Gradle) | `./gradlew test jacocoTestReport` |
| PHP (PHPUnit) | `./vendor/bin/phpunit --coverage-text` |

---

## Coverage Reports

### Minimum Report Contents

| Metric | Description |
|--------|-------------|
| Line coverage | Percentage of lines executed |
| Branch coverage | Percentage of branches taken |
| Function coverage | Percentage of functions called |
| Uncovered lines | List of untested lines |

### Interpreting Results

| Coverage | Interpretation |
|----------|----------------|
| < 50% | Insufficient, high risk |
| 50-70% | Acceptable for small tasks |
| 70-80% | Good, standard requirement |
| > 80% | Excellent, large task requirement |
| 100% | Suspicious, may test implementation |

---

## Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Low branch coverage | Conditionals untested | Add tests for else/catch paths |
| Inflated coverage | High % but bugs exist | Test behavior, not lines |
| Flaky coverage | Results vary | Remove randomness, fix timing |
| Slow tests | Coverage takes forever | Parallelize, mock heavy I/O |
