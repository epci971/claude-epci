# React Testing Reference

## Test Setup

### Vitest Configuration

```typescript
// frontend/vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
    coverage: {
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
});
```

### Test Setup File

```typescript
// frontend/src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

## Component Testing

### Basic Component Test

```tsx
// frontend/src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>);

    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows loading spinner when loading', () => {
    render(<Button loading>Submit</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });

  it('applies variant classes', () => {
    render(<Button variant="danger">Delete</Button>);

    expect(screen.getByRole('button')).toHaveClass('bg-red-600');
  });
});
```

### Testing with User Events

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { SearchInput } from './SearchInput';

describe('SearchInput', () => {
  it('calls onSearch when user types and submits', async () => {
    const user = userEvent.setup();
    const onSearch = vi.fn();

    render(<SearchInput onSearch={onSearch} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'test query');
    await user.keyboard('{Enter}');

    expect(onSearch).toHaveBeenCalledWith('test query');
  });

  it('clears input when clear button is clicked', async () => {
    const user = userEvent.setup();
    render(<SearchInput onSearch={vi.fn()} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'some text');

    expect(input).toHaveValue('some text');

    await user.click(screen.getByRole('button', { name: /clear/i }));

    expect(input).toHaveValue('');
  });
});
```

## Hook Testing

### Custom Hook Test

```tsx
// frontend/src/hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

### Hook with React Query

```tsx
// frontend/src/hooks/useLots.test.tsx
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useLots } from './useLots';

// Wrapper with QueryClient
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

describe('useLots', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('fetches lots successfully', async () => {
    const mockLots = {
      count: 2,
      results: [
        { id: 1, code: 'LOT-001' },
        { id: 2, code: 'LOT-002' },
      ],
    };

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockLots),
    });

    const { result } = renderHook(() => useLots(), {
      wrapper: createWrapper(),
    });

    // Initially loading
    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual(mockLots);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    });

    const { result } = renderHook(() => useLots(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toBeDefined();
  });
});
```

## Mocking

### Mocking Modules

```tsx
// Mock entire module
vi.mock('./api/client', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

// Mock specific export
vi.mock('./utils/csrf', () => ({
  getCsrfToken: vi.fn(() => 'mock-token'),
}));
```

### Mocking Fetch

```tsx
describe('API calls', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('posts data with CSRF token', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: 1 }),
    });

    await createLot({ code: 'LOT-001' });

    expect(global.fetch).toHaveBeenCalledWith('/api/v1/lots/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': expect.any(String),
      },
      credentials: 'same-origin',
      body: JSON.stringify({ code: 'LOT-001' }),
    });
  });
});
```

### Mocking Zustand Store

```tsx
import { create } from 'zustand';

// Create mock store for testing
const createMockStore = (initialState = {}) =>
  create(() => ({
    selectedLots: [],
    selectLot: vi.fn(),
    deselectLot: vi.fn(),
    ...initialState,
  }));

// In test
vi.mock('../stores/lotStore', () => ({
  useLotStore: createMockStore({ selectedLots: [{ id: 1 }] }),
}));
```

## Integration Tests

### Form Submission Flow

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi } from 'vitest';
import { LotForm } from './LotForm';

describe('LotForm integration', () => {
  it('submits form and shows success message', async () => {
    const user = userEvent.setup();
    const queryClient = new QueryClient();

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: 1, code: 'LOT-001' }),
    });

    render(
      <QueryClientProvider client={queryClient}>
        <LotForm />
      </QueryClientProvider>
    );

    // Fill form
    await user.type(screen.getByLabelText(/code/i), 'LOT-001');
    await user.type(screen.getByLabelText(/quantité/i), '100');

    // Submit
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Wait for success
    await waitFor(() => {
      expect(screen.getByText(/created successfully/i)).toBeInTheDocument();
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();
    const queryClient = new QueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <LotForm />
      </QueryClientProvider>
    );

    // Submit empty form
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText(/code is required/i)).toBeInTheDocument();
    });
  });
});
```

## Test Utilities

### Custom Render with Providers

```tsx
// frontend/src/test/utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

interface WrapperProps {
  children: React.ReactNode;
}

function AllProviders({ children }: WrapperProps) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

function customRender(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

### Accessibility Testing

```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { describe, it, expect } from 'vitest';
import { Button } from './Button';

expect.extend(toHaveNoViolations);

describe('Button accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);

    const results = await axe(container);

    expect(results).toHaveNoViolations();
  });
});
```

## Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific file
npm test -- Button.test.tsx

# Run tests matching pattern
npm test -- --grep "submits form"
```

## Test Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Queries | `getByRole`, `getByLabelText` | `getByTestId` (last resort) |
| User actions | `userEvent.setup()` | `fireEvent` (for simple cases only) |
| Assertions | Specific (`toHaveTextContent`) | Generic (`toBeTruthy`) |
| Async | `waitFor`, `findBy*` | Manual `setTimeout` |
| Mocks | Minimal, reset between tests | Leaking state |
| Coverage | Critical paths, edge cases | 100% coverage |
