---
name: javascript-react
description: >-
  Patterns et conventions pour JavaScript/React. Inclut hooks, TypeScript,
  state management, testing avec Jest/RTL. Use when: développement React,
  package.json avec react détecté. Not for: Vue, Angular, Node backend.
---

# JavaScript/React Development Patterns

## Overview

Patterns et conventions pour le développement React moderne avec TypeScript.

## Auto-détection

Chargé automatiquement si détection de :
- `package.json` contenant `react`
- Fichiers `*.tsx`, `*.jsx`
- Structure `src/components/`, `src/hooks/`

## Architecture React

### Structure standard

```
project/
├── src/
│   ├── components/        # Composants réutilisables
│   │   ├── ui/           # Composants UI basiques
│   │   └── features/     # Composants feature-specific
│   ├── hooks/            # Custom hooks
│   ├── contexts/         # React contexts
│   ├── services/         # API calls, external services
│   ├── utils/            # Helpers, utilities
│   ├── types/            # TypeScript types
│   └── pages/            # Page components (si routing)
├── tests/
│   ├── __mocks__/
│   └── setup.ts
├── public/
└── package.json
```

### Conventions de nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | `use*` | `useAuth.ts` |
| Contexts | `*Context` | `AuthContext.tsx` |
| Utils | camelCase | `formatDate.ts` |
| Types | PascalCase | `User.ts` |
| Tests | `*.test.tsx` | `UserCard.test.tsx` |

## Component Patterns

### Functional Component avec TypeScript

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

### Component avec état local

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

### Hook avec contexte

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

### useReducer pour état complexe

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

## Commandes utiles

```bash
# Développement
npm run dev
npm run build
npm run lint
npm run type-check

# Tests
npm test
npm test -- --watch
npm test -- --coverage
npm test -- UserCard.test.tsx

# Dépendances
npm install <package>
npm install -D <package>  # dev dependency
```

## Bonnes pratiques React

| Pratique | Faire | Éviter |
|----------|-------|--------|
| State | useState/useReducer | Class state |
| Effects | useEffect avec cleanup | componentDidMount |
| Memoization | useMemo/useCallback si besoin | Memoize tout |
| Props | Destructuring | `props.xxx` |
| Types | TypeScript strict | `any` |
| Keys | IDs uniques | Index comme key |

## Performance

```tsx
// Memoization de composant
const MemoizedComponent = memo(ExpensiveComponent);

// Memoization de valeur
const sortedItems = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Memoization de callback
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// Lazy loading
const LazyComponent = lazy(() => import('./HeavyComponent'));
```

## Accessibilité

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
