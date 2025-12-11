# React Frontend Rules (Django Integration)

## Architecture: Islands Pattern

```
┌─────────────────────────────────────────────────────────┐
│  Django Template (Server-Rendered HTML)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ React Island│  │ React Island│  │ Static HTML │      │
│  │ (DataTable) │  │ (Chart)     │  │ (Content)   │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

**Principle**: Django renders pages, React enhances specific interactive zones.

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx              # Entry point, mounts components
│   ├── components/           # Reusable UI components
│   │   ├── ui/               # Base UI (Button, Modal, Input)
│   │   └── features/         # Feature components (DataTable, Chart)
│   ├── hooks/                # Custom hooks
│   ├── api/                  # API calls (React Query, fetch)
│   ├── stores/               # State management (Zustand)
│   ├── utils/                # Utilities
│   └── types/                # TypeScript types
├── vite.config.ts
├── tailwind.config.js
├── package.json
└── tsconfig.json
```

## Component Mounting Pattern

### Entry Point
```tsx
// src/main.tsx
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import DataTable from "./components/features/DataTable";
import KpiChart from "./components/features/KpiChart";

const queryClient = new QueryClient();

// Component registry
const components: Record<string, React.ComponentType<any>> = {
  DataTable,
  KpiChart,
};

// Mount all React islands on page
document.querySelectorAll("[data-react-component]").forEach((el) => {
  const componentName = el.getAttribute("data-react-component");
  const propsJson = el.getAttribute("data-react-props") || "{}";
  
  if (componentName && components[componentName]) {
    const Component = components[componentName];
    const props = JSON.parse(propsJson);
    
    createRoot(el).render(
      <QueryClientProvider client={queryClient}>
        <Component {...props} />
      </QueryClientProvider>
    );
  }
});
```

### Component Example
```tsx
// src/components/features/DataTable.tsx
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

interface DataTableProps {
  endpoint: string;
  columns: string[];
}

export default function DataTable({ endpoint, columns }: DataTableProps) {
  const [page, setPage] = useState(1);
  
  const { data, isLoading, error } = useQuery({
    queryKey: ["table-data", endpoint, page],
    queryFn: () => fetch(`${endpoint}?page=${page}`).then(r => r.json()),
  });
  
  if (isLoading) return <div className="animate-pulse">Loading...</div>;
  if (error) return <div className="text-red-500">Error loading data</div>;
  
  return (
    <table className="min-w-full divide-y divide-gray-200">
      {/* Table content */}
    </table>
  );
}
```

## State Management

### Zustand (Recommended for Islands)
```tsx
// src/stores/filterStore.ts
import { create } from "zustand";

interface FilterState {
  search: string;
  status: string | null;
  setSearch: (search: string) => void;
  setStatus: (status: string | null) => void;
  reset: () => void;
}

export const useFilterStore = create<FilterState>((set) => ({
  search: "",
  status: null,
  setSearch: (search) => set({ search }),
  setStatus: (status) => set({ status }),
  reset: () => set({ search: "", status: null }),
}));
```

### When to Use What

| Solution | Use Case |
|----------|----------|
| `useState` | Single component local state |
| `useReducer` | Complex local state logic |
| React Context | Shared state within one island |
| **Zustand** | Shared state across components, simple API |
| Jotai | Fine-grained reactivity, many atoms |
| Redux Toolkit | Large app with complex global state |

## API Data Fetching

### React Query (Recommended)
```tsx
// src/api/orders.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API_BASE = "/api/v1";

export function useOrders(page: number) {
  return useQuery({
    queryKey: ["orders", page],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/orders/?page=${page}`);
      if (!res.ok) throw new Error("Failed to fetch orders");
      return res.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: CreateOrderData) => {
      const res = await fetch(`${API_BASE}/orders/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("Failed to create order");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });
}

function getCsrfToken(): string {
  return document.querySelector<HTMLInputElement>(
    "[name=csrfmiddlewaretoken]"
  )?.value || "";
}
```

### SWR Alternative
```tsx
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function useOrders(page: number) {
  return useSWR(`/api/v1/orders/?page=${page}`, fetcher, {
    revalidateOnFocus: false,
  });
}
```

## UI Libraries

### Recommended Stack
```
Tailwind CSS          → Utility-first styling
shadcn/ui             → Copy-paste accessible components
Radix UI              → Headless primitives (used by shadcn)
Lucide React          → Icons
Recharts              → Charts and graphs
```

### Tailwind Configuration
```js
// tailwind.config.js
export default {
  content: [
    "./src/**/*.{ts,tsx}",
    "../backend/templates/**/*.html",  // Include Django templates
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1e40af",
        secondary: "#64748b",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
};
```

### Component Example with shadcn/ui
```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export function CreateOrderDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>New Order</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Order</DialogTitle>
        </DialogHeader>
        <form className="space-y-4">
          <Input placeholder="Customer name" />
          <Button type="submit">Create</Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## TypeScript Patterns

### Props Types
```tsx
interface DataTableProps {
  endpoint: string;
  columns: Column[];
  initialPage?: number;
  onRowClick?: (row: Row) => void;
}

interface Column {
  key: string;
  label: string;
  sortable?: boolean;
}
```

### API Response Types
```tsx
interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

interface Order {
  id: number;
  reference: string;
  status: "pending" | "confirmed" | "shipped";
  total: string;
  created_at: string;
}
```

## Accessibility (a11y)

```tsx
// Use semantic HTML
<button> instead of <div onClick>
<nav>, <main>, <article>, <section>

// ARIA when needed
<button aria-label="Close dialog" aria-expanded={isOpen}>

// Keyboard navigation
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === "Escape") onClose();
  if (e.key === "Enter") onSubmit();
};

// Focus management
useEffect(() => {
  if (isOpen) inputRef.current?.focus();
}, [isOpen]);
```

## Performance

### Code Splitting
```tsx
import { lazy, Suspense } from "react";

const HeavyChart = lazy(() => import("./components/HeavyChart"));

function Dashboard() {
  return (
    <Suspense fallback={<div>Loading chart...</div>}>
      <HeavyChart data={data} />
    </Suspense>
  );
}
```

### Memoization
```tsx
import { memo, useMemo, useCallback } from "react";

// Memoize component
const TableRow = memo(function TableRow({ row }: { row: Row }) {
  return <tr>{/* ... */}</tr>;
});

// Memoize expensive computation
const sortedData = useMemo(
  () => data.sort((a, b) => a.name.localeCompare(b.name)),
  [data]
);

// Memoize callback
const handleClick = useCallback((id: number) => {
  setSelected(id);
}, []);
```

---

## ✅ DO

- ✅ Use TypeScript for type safety
- ✅ Mount components conditionally (`if (el)`)
- ✅ Use React Query/SWR for API data
- ✅ Use Zustand for simple shared state
- ✅ Use Tailwind + headless components (shadcn/ui, Radix)
- ✅ Include CSRF token in mutations
- ✅ Lazy load heavy components
- ✅ Structure by feature, not by type
- ✅ Use semantic HTML and ARIA

---

## ❌ DON'T

- ❌ **No SPA routing** - Django handles navigation
- ❌ **No global Redux for simple islands** - overkill
- ❌ **No inline styles** - use Tailwind classes
- ❌ **No `any` types** - use proper TypeScript
- ❌ **No direct DOM manipulation** - use React state
- ❌ **No fetch without error handling**
- ❌ **No mixing HTMX zones with React roots**

---

## Checklist

### Setup
- [ ] Vite configured with React + TypeScript
- [ ] Tailwind CSS configured (including Django templates in content)
- [ ] React Query/SWR for data fetching
- [ ] Component registry in main.tsx

### Components
- [ ] Props typed with interfaces
- [ ] Loading and error states handled
- [ ] Accessible (keyboard, ARIA)
- [ ] Memoized when needed

### State
- [ ] Local state for single component
- [ ] Zustand/Jotai for shared state
- [ ] React Query cache for server state

### API
- [ ] CSRF token included in mutations
- [ ] Error handling with user feedback
- [ ] Proper cache invalidation
