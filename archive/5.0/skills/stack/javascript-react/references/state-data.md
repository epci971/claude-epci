# State Management & Data Fetching Reference

## CSRF Token Handling (Critical)

**All POST/PUT/DELETE requests to Django MUST include the CSRF token.**

### CSRF Utility

```typescript
// frontend/src/utils/csrf.ts

/**
 * Get CSRF token from cookie or hidden input.
 * Django sets this in the csrftoken cookie.
 */
export function getCsrfToken(): string {
  // Try cookie first
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (cookieValue) return cookieValue;

  // Fallback to hidden input
  const input = document.querySelector<HTMLInputElement>(
    'input[name="csrfmiddlewaretoken"]'
  );

  return input?.value || '';
}

/**
 * Headers for fetch requests that modify data.
 */
export function getMutationHeaders(): HeadersInit {
  return {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken(),
  };
}
```

### Usage with Fetch

```typescript
// Simple fetch with CSRF
async function createLot(data: LotInput): Promise<Lot> {
  const response = await fetch('/api/v1/lots/', {
    method: 'POST',
    headers: getMutationHeaders(),
    credentials: 'same-origin', // Important for cookies
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}
```

### Usage with React Query

```typescript
// frontend/src/api/lots.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { getMutationHeaders } from '../utils/csrf';

export function useCreateLot() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: LotInput) => {
      const response = await fetch('/api/v1/lots/', {
        method: 'POST',
        headers: getMutationHeaders(),
        credentials: 'same-origin',
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Creation failed');
      }

      return response.json();
    },

    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['lots'] });
    },
  });
}
```

## State Management Decision Matrix

| Scope | Solution | When to Use |
|-------|----------|-------------|
| Component local | `useState` | Single component, simple state |
| Complex local | `useReducer` | Multiple related state values |
| Island shared | React Context | State shared within one island |
| Cross-component | **Zustand** | Shared across components, simple API |
| Server state | **React Query** | Data from API, caching needed |
| Large app | Redux Toolkit | Complex global state (rare for islands) |

### Recommendation for Islands: Zustand + React Query

- **Zustand**: Simple, small bundle, no boilerplate, perfect for islands
- **React Query**: Handles server state, caching, refetching automatically

## Zustand Patterns

### Basic Store

```typescript
// frontend/src/stores/lotStore.ts
import { create } from 'zustand';

interface Lot {
  id: number;
  code: string;
  quantite: number;
}

interface LotStore {
  selectedLots: Lot[];
  isSelecting: boolean;

  // Actions
  selectLot: (lot: Lot) => void;
  deselectLot: (id: number) => void;
  clearSelection: () => void;
  toggleSelecting: () => void;
}

export const useLotStore = create<LotStore>((set) => ({
  selectedLots: [],
  isSelecting: false,

  selectLot: (lot) =>
    set((state) => ({
      selectedLots: [...state.selectedLots, lot],
    })),

  deselectLot: (id) =>
    set((state) => ({
      selectedLots: state.selectedLots.filter((l) => l.id !== id),
    })),

  clearSelection: () => set({ selectedLots: [] }),

  toggleSelecting: () =>
    set((state) => ({ isSelecting: !state.isSelecting })),
}));
```

### Usage in Components

```tsx
function LotTable() {
  const { selectedLots, selectLot, deselectLot } = useLotStore();

  return (
    <table>
      {lots.map((lot) => (
        <tr key={lot.id}>
          <td>
            <input
              type="checkbox"
              checked={selectedLots.some((l) => l.id === lot.id)}
              onChange={(e) =>
                e.target.checked
                  ? selectLot(lot)
                  : deselectLot(lot.id)
              }
            />
          </td>
          <td>{lot.code}</td>
        </tr>
      ))}
    </table>
  );
}

function SelectionActions() {
  const { selectedLots, clearSelection } = useLotStore();

  if (selectedLots.length === 0) return null;

  return (
    <div>
      <span>{selectedLots.length} selected</span>
      <button onClick={clearSelection}>Clear</button>
    </div>
  );
}
```

### Zustand with Persistence

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const usePreferencesStore = create(
  persist<PreferencesStore>(
    (set) => ({
      theme: 'light',
      pageSize: 25,
      setTheme: (theme) => set({ theme }),
      setPageSize: (size) => set({ pageSize: size }),
    }),
    {
      name: 'user-preferences', // localStorage key
    }
  )
);
```

## React Query Patterns

### Query Client Setup

```typescript
// frontend/src/api/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});
```

### Fetching Data

```typescript
// frontend/src/api/lots.ts
import { useQuery } from '@tanstack/react-query';

interface LotsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Lot[];
}

export function useLots(page = 1, filters?: LotFilters) {
  return useQuery({
    queryKey: ['lots', page, filters],
    queryFn: async (): Promise<LotsResponse> => {
      const params = new URLSearchParams({
        page: String(page),
        ...filters,
      });

      const response = await fetch(`/api/v1/lots/?${params}`);

      if (!response.ok) {
        throw new Error('Failed to fetch lots');
      }

      return response.json();
    },
  });
}

// Usage
function LotList() {
  const [page, setPage] = useState(1);
  const { data, isLoading, error } = useLots(page);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <>
      {data.results.map((lot) => (
        <LotCard key={lot.id} lot={lot} />
      ))}
      <Pagination
        page={page}
        hasNext={!!data.next}
        onPageChange={setPage}
      />
    </>
  );
}
```

### Mutations with Optimistic Updates

```typescript
export function useUpdateLot() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Lot> }) => {
      const response = await fetch(`/api/v1/lots/${id}/`, {
        method: 'PATCH',
        headers: getMutationHeaders(),
        credentials: 'same-origin',
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Update failed');
      return response.json();
    },

    // Optimistic update
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: ['lots'] });

      const previousLots = queryClient.getQueryData(['lots']);

      queryClient.setQueryData(['lots'], (old: any) => ({
        ...old,
        results: old.results.map((lot: Lot) =>
          lot.id === id ? { ...lot, ...data } : lot
        ),
      }));

      return { previousLots };
    },

    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousLots) {
        queryClient.setQueryData(['lots'], context.previousLots);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['lots'] });
    },
  });
}
```

### Prefetching

```typescript
function LotListItem({ lot }: { lot: Lot }) {
  const queryClient = useQueryClient();

  // Prefetch on hover
  const prefetchDetails = () => {
    queryClient.prefetchQuery({
      queryKey: ['lot', lot.id],
      queryFn: () => fetch(`/api/v1/lots/${lot.id}/`).then(r => r.json()),
    });
  };

  return (
    <div onMouseEnter={prefetchDetails}>
      <Link to={`/lots/${lot.id}`}>{lot.code}</Link>
    </div>
  );
}
```

## API Client Pattern

```typescript
// frontend/src/api/client.ts
import { getMutationHeaders } from '../utils/csrf';

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new ApiError(
      data.detail || `HTTP ${response.status}`,
      response.status,
      data
    );
  }
  return response.json();
}

export const api = {
  get: async <T>(url: string): Promise<T> => {
    const response = await fetch(url, {
      credentials: 'same-origin',
    });
    return handleResponse<T>(response);
  },

  post: async <T>(url: string, data: unknown): Promise<T> => {
    const response = await fetch(url, {
      method: 'POST',
      headers: getMutationHeaders(),
      credentials: 'same-origin',
      body: JSON.stringify(data),
    });
    return handleResponse<T>(response);
  },

  patch: async <T>(url: string, data: unknown): Promise<T> => {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: getMutationHeaders(),
      credentials: 'same-origin',
      body: JSON.stringify(data),
    });
    return handleResponse<T>(response);
  },

  delete: async (url: string): Promise<void> => {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: getMutationHeaders(),
      credentials: 'same-origin',
    });
    if (!response.ok) {
      throw new ApiError(`HTTP ${response.status}`, response.status);
    }
  },
};
```

## Error Handling

```tsx
// Error boundary for React Query
import { QueryErrorResetBoundary } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div>
              <p>Something went wrong: {error.message}</p>
              <button onClick={resetErrorBoundary}>Try again</button>
            </div>
          )}
        >
          <DataTable />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
```
