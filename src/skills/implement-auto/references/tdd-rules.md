# TDD Rules (Self-Contained)

> Standalone TDD workflow for implement-auto. No dependency on epci:tdd-enforcer.

## Cycle

```
RED -> GREEN -> REFACTOR -> VERIFY
```

## Phase 1: RED (Write Failing Test)

| Rule | Description |
|------|-------------|
| NEVER skip | Always write test before implementation |
| One at a time | One test per cycle |
| Verify failure reason | Must fail for missing implementation, not syntax error |

### Process
1. Identify the next behavior to implement
2. Write a test that defines expected behavior
3. Run the test — confirm it fails
4. Verify failure message indicates missing implementation

## Phase 2: GREEN (Make Test Pass)

| Rule | Description |
|------|-------------|
| Minimal code | Write only what's needed to pass |
| No optimization | Resist improvements during GREEN |
| Run all tests | Verify no regressions |

### Process
1. Write simplest code that makes the test pass
2. Run test — confirm it passes
3. Verify all other tests still pass

## Phase 3: REFACTOR (Improve Code)

| Rule | Description |
|------|-------------|
| No behavior change | Keep tests green |
| One change at a time | Incremental improvements |
| Apply patterns | Follow project conventions from CLAUDE.md/rules/ |

### Process
1. Identify improvement opportunities
2. Make one refactoring change
3. Run tests — confirm still passing

## Phase 4: VERIFY (Final Check)

| Rule | Description |
|------|-------------|
| Full suite | Run all tests, not just current |
| Coverage check | Verify coverage meets target |
| Integration | Confirm feature works end-to-end |

## Coverage Target

For implement-auto, all tasks are pre-qualified STANDARD:

| Metric | Target |
|--------|--------|
| Line coverage | >= 70% |
| Branch coverage | >= 60% |
| TDD mode | guided |

## Test Detection

The skill auto-detects the project's test framework:

| Indicator | Framework | Run Command |
|-----------|-----------|-------------|
| `pytest.ini` or `conftest.py` | pytest | `pytest {file} -v` |
| `jest.config.*` | Jest | `npx jest {file}` |
| `vitest.config.*` | Vitest | `npx vitest run {file}` |
| `phpunit.xml*` | PHPUnit | `./vendor/bin/phpunit --filter {test}` |
| `build.gradle*` with junit | JUnit | `./gradlew test --tests "{TestClass}"` |

If no test framework detected: warn in JSON output, continue without strict TDD.

## Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| Test after code | Always RED first |
| Testing implementation details | Test behavior |
| Shared mutable state | Isolate each test |
| Over-mocking | Mock at boundaries only |
| Skipping REFACTOR | Always clean up |
