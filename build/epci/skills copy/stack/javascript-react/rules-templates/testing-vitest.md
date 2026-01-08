---
paths:
  - frontend/**/*.test.ts
  - frontend/**/*.test.tsx
  - frontend/**/*.spec.ts
  - frontend/**/*.spec.tsx
---

# Vitest Testing Rules

> Conventions pour les tests React avec Vitest.

## 🔴 CRITICAL

1. **Tester le comportement, pas l'implementation**: User-centric testing
2. **Queries accessibles en priorite**: `getByRole` > `getByTestId`
3. **Async/await pour interactions**: Toujours attendre les updates

## 🟡 CONVENTIONS

### Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Button/
│   │       ├── Button.tsx
│   │       └── Button.test.tsx  # Co-located
│   └── hooks/
│       └── useAuth.test.ts
└── vitest.config.ts
```

### Queries Priority

| Priority | Query | Use Case |
|----------|-------|----------|
| 1 | `getByRole` | Buttons, links, inputs |
| 2 | `getByLabelText` | Form fields |
| 3 | `getByPlaceholderText` | Inputs sans label |
| 4 | `getByText` | Non-interactive text |
| Last | `getByTestId` | Dernier recours |

### Pattern AAA

```tsx
describe('Button', () => {
  it('calls onClick when clicked', async () => {
    // Arrange
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click me</Button>);

    // Act
    await userEvent.click(screen.getByRole('button'));

    // Assert
    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

## 🟢 PREFERENCES

- Utiliser `userEvent` plutot que `fireEvent`
- Wrapper les tests React Query avec `QueryClientProvider`
- Mock les API avec MSW

## Quick Reference

| Task | Pattern |
|------|---------|
| Render | `render(<Component />)` |
| Find element | `screen.getByRole('button')` |
| Click | `await userEvent.click(element)` |
| Type | `await userEvent.type(input, 'text')` |
| Assert | `expect(element).toBeInTheDocument()` |
| Mock | `vi.fn()`, `vi.mock()` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Render with providers | Custom render function | DRY setup |
| MSW | Mock API responses | Realistic tests |
| userEvent | `userEvent.setup()` | Accurate events |
| waitFor | `await waitFor(() => ...)` | Async assertions |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| `getByTestId` first | Bad accessibility | `getByRole` |
| Snapshot overuse | Brittle, noisy | Specific assertions |
| Implementation details | Fragile | Behavior testing |
| Missing await | Flaky tests | Always await |

## Examples

### Correct

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('UserList', () => {
  it('displays users after loading', async () => {
    render(<UserList />, { wrapper: createWrapper() });

    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Assert content
    expect(screen.getByRole('list')).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });

  it('filters users by search', async () => {
    const user = userEvent.setup();
    render(<UserList />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByRole('searchbox')).toBeInTheDocument();
    });

    await user.type(screen.getByRole('searchbox'), 'John');

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.queryByText('Jane Doe')).not.toBeInTheDocument();
  });
});
```

### Incorrect

```tsx
// DON'T DO THIS
it('works', () => {
  const { container } = render(<UserList />);

  // Implementation detail
  expect(container.querySelector('.user-list')).toBeTruthy();

  // No await for async
  fireEvent.click(screen.getByTestId('load-btn'));

  // Immediate assertion after async action
  expect(screen.getByText('Users')).toBeInTheDocument();
});
```
