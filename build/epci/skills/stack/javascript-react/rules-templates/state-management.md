---
paths:
  - frontend/**/stores/**/*.ts
  - frontend/**/hooks/**/*.ts
  - frontend/**/*Store.ts
  - frontend/**/*Query.ts
---

# State Management Rules

> Conventions pour la gestion d'etat React.

## 🔴 CRITICAL

1. **Separer client/server state**: Zustand pour client, React Query pour server
2. **Pas de state global pour UI locale**: useState suffit
3. **Toujours CSRF sur mutations**: Header X-CSRFToken

## 🟡 CONVENTIONS

### Decision Matrix

| Scope | Solution |
|-------|----------|
| Component local | `useState` |
| Complex local | `useReducer` |
| Shared between components | React Context |
| Cross-feature | **Zustand** |
| Server data | **React Query** |

### Zustand Store

```typescript
import { create } from 'zustand';

interface UserState {
  selectedUsers: User[];
  selectUser: (user: User) => void;
  clearSelection: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  selectedUsers: [],
  selectUser: (user) => set((state) => ({
    selectedUsers: [...state.selectedUsers, user]
  })),
  clearSelection: () => set({ selectedUsers: [] }),
}));
```

### React Query Pattern

```typescript
// Fetching
const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then(r => r.json()),
});

// Mutation with CSRF
const mutation = useMutation({
  mutationFn: (data: CreateUserDto) => fetch('/api/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify(data),
  }),
  onSuccess: () => queryClient.invalidateQueries(['users']),
});
```

### CSRF Token

```typescript
// utils/csrf.ts
export function getCsrfToken(): string {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}
```

## 🟢 PREFERENCES

- Zustand avec immer pour updates complexes
- React Query avec staleTime pour cache
- Selectors Zustand pour performance

## Quick Reference

| Task | Pattern |
|------|---------|
| Client state | `useUserStore()` |
| Server state | `useQuery({ queryKey, queryFn })` |
| Mutation | `useMutation({ mutationFn, onSuccess })` |
| CSRF | `'X-CSRFToken': getCsrfToken()` |
| Invalidate | `queryClient.invalidateQueries()` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Optimistic update | `onMutate` + rollback | Fast UX |
| Infinite scroll | `useInfiniteQuery` | Pagination |
| Polling | `refetchInterval` | Real-time |
| Prefetch | `queryClient.prefetchQuery` | Fast navigation |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Redux for all | Overkill | Zustand + RQ |
| Fetch in useEffect | Manual caching | React Query |
| Global for local | Complexity | useState |
| Missing CSRF | 403 errors | Always include |

## Examples

### Correct

```typescript
// Store for client state
export const useCartStore = create<CartState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({
    items: [...state.items, item]
  })),
  total: 0,
}));

// Query for server state
export function useProducts(categoryId: string) {
  return useQuery({
    queryKey: ['products', categoryId],
    queryFn: () => fetchProducts(categoryId),
    staleTime: 5 * 60 * 1000, // 5 min cache
  });
}

// Mutation with optimistic update
export function useAddToCart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: addToCartApi,
    onMutate: async (newItem) => {
      await queryClient.cancelQueries(['cart']);
      const previous = queryClient.getQueryData(['cart']);
      queryClient.setQueryData(['cart'], (old: Cart) => ({
        ...old,
        items: [...old.items, newItem],
      }));
      return { previous };
    },
    onError: (err, newItem, context) => {
      queryClient.setQueryData(['cart'], context?.previous);
    },
  });
}
```

### Incorrect

```typescript
// DON'T DO THIS
const [products, setProducts] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetch('/api/products')  // No CSRF!
    .then(r => r.json())
    .then(data => {
      setProducts(data);
      setLoading(false);
    });
}, []);  // Manual state management - use React Query!
```
