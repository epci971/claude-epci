---
name: javascript-react
description: >-
  Patterns and conventions for JavaScript/React. Includes hooks, TypeScript,
  state management, testing with Jest/RTL. Use when: React development,
  package.json with react detected. Not for: Vue, Angular, Node backend.
---

# JavaScript/React Development Patterns

## Overview

Patterns and conventions for modern React development with TypeScript.

## Auto-detection

Automatically loaded if detection of:
- `package.json` containing `react`
- Files `*.tsx`, `*.jsx`
- Structure `src/components/`, `src/hooks/`

## React Architecture

### Standard Structure

```
project/
├── src/
│   ├── components/        # Reusable components
│   │   ├── ui/           # Basic UI components
│   │   └── features/     # Feature-specific components
│   ├── hooks/            # Custom hooks
│   ├── contexts/         # React contexts
│   ├── services/         # API calls, external services
│   ├── utils/            # Helpers, utilities
│   ├── types/            # TypeScript types
│   └── pages/            # Page components (if routing)
├── tests/
│   ├── __mocks__/
│   └── setup.ts
├── public/
└── package.json
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | `use*` | `useAuth.ts` |
| Contexts | `*Context` | `AuthContext.tsx` |
| Utils | camelCase | `formatDate.ts` |
| Types | PascalCase | `User.ts` |
| Tests | `*.test.tsx` | `UserCard.test.tsx` |

## Component Patterns

### Functional Component with TypeScript

```tsx
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
  className?: string;
}

export function UserCard({ user, onSelect, className }: UserCardProps) {
  const handleClick = () => {
    onSelect?.(user);
  };

  return (
    <div className={cn('user-card', className)} onClick={handleClick}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

### Component with Local State

```tsx
interface CounterProps {
  initialValue?: number;
  onChange?: (value: number) => void;
}

export function Counter({ initialValue = 0, onChange }: CounterProps) {
  const [count, setCount] = useState(initialValue);

  const increment = () => {
    const newValue = count + 1;
    setCount(newValue);
    onChange?.(newValue);
  };

  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
    </div>
  );
}
```

## Hooks Patterns

### Custom Hook

```tsx
interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useApi<T>(url: string): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(url);
      const json = await response.json();
      setData(json);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
```

### Hook with Context

```tsx
const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

## State Management Patterns

### useReducer for Complex State

```tsx
type State = {
  items: Item[];
  loading: boolean;
  error: string | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Item[] }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'ADD_ITEM'; payload: Item };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, loading: false, items: action.payload };
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload };
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };
    default:
      return state;
  }
}
```

## Testing Patterns (Jest + RTL)

### Component Test

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = { id: '1', name: 'John', email: 'john@example.com' };

  it('renders user information', () => {
    render(<UserCard user={mockUser} />);

    expect(screen.getByText('John')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const onSelect = jest.fn();
    render(<UserCard user={mockUser} onSelect={onSelect} />);

    fireEvent.click(screen.getByText('John'));

    expect(onSelect).toHaveBeenCalledWith(mockUser);
  });
});
```

### Hook Test

```tsx
import { renderHook, act, waitFor } from '@testing-library/react';
import { useApi } from './useApi';

describe('useApi', () => {
  it('fetches data successfully', async () => {
    const mockData = { id: 1, name: 'Test' };
    global.fetch = jest.fn().mockResolvedValue({
      json: () => Promise.resolve(mockData),
    });

    const { result } = renderHook(() => useApi('/api/data'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toEqual(mockData);
    expect(result.current.error).toBeNull();
  });
});
```

## Useful Commands

```bash
# Development
npm run dev
npm run build
npm run lint
npm run type-check

# Tests
npm test
npm test -- --watch
npm test -- --coverage
npm test -- UserCard.test.tsx

# Dependencies
npm install <package>
npm install -D <package>  # dev dependency
```

## React Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| State | useState/useReducer | Class state |
| Effects | useEffect with cleanup | componentDidMount |
| Memoization | useMemo/useCallback if needed | Memoize everything |
| Props | Destructuring | `props.xxx` |
| Types | TypeScript strict | `any` |
| Keys | Unique IDs | Index as key |

## Performance

```tsx
// Component memoization
const MemoizedComponent = memo(ExpensiveComponent);

// Value memoization
const sortedItems = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Callback memoization
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// Lazy loading
const LazyComponent = lazy(() => import('./HeavyComponent'));
```

## Accessibility

```tsx
// ARIA labels
<button aria-label="Close dialog" onClick={onClose}>×</button>

// Semantic HTML
<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// Focus management
useEffect(() => {
  if (isOpen) {
    dialogRef.current?.focus();
  }
}, [isOpen]);
```
