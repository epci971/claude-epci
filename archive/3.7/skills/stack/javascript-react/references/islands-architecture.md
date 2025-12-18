# React Islands Architecture Reference

## Philosophy

**Core Principle**: Django renders pages, React enhances interactive zones.

This is NOT a Single Page Application (SPA). React components are "islands" of interactivity within server-rendered Django pages.

### Benefits

| Benefit | Description |
|---------|-------------|
| Single deployment | One Docker, one CI/CD, one domain |
| Django handles auth | Sessions, permissions, CSRF - all Django |
| No CORS issues | Same origin for API calls |
| SEO-friendly | Server-rendered HTML |
| Progressive enhancement | Works without JS, React adds interactivity |
| Isolated bundles | Each island has independent lifecycle |

### Architecture Diagram

```
Django Template (Server-Rendered HTML)
├── Header (static HTML)
├── Navigation (static HTML or HTMX)
├── [React Island: DataTable] ← Interactive component
├── Content (static HTML)
├── [React Island: Chart] ← Interactive component
└── Footer (static HTML)
```

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx              # Entry point with component registry
│   ├── components/
│   │   ├── ui/               # Base components (Button, Modal, Input)
│   │   └── features/         # Business components (DataTable, KpiChart)
│   ├── hooks/                # Custom hooks
│   ├── api/                  # API client, React Query setup
│   ├── stores/               # Zustand stores
│   ├── utils/                # Utilities
│   └── types/                # TypeScript definitions
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── package.json

backend/
├── static/
│   └── assets/               # Vite output directory
├── templates/
│   └── <app>/
│       └── page.html         # Django templates with React mounting points
```

## Vite Configuration

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],

  // Critical: Match Django's STATIC_URL
  base: '/static/assets/',

  build: {
    // Output to Django's static directory
    outDir: '../backend/static/assets',
    emptyOutDir: true,

    // Generate manifest for django-vite
    manifest: true,

    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/main.tsx'),
      },
      output: {
        // Consistent naming for cache busting
        entryFileNames: '[name]-[hash].js',
        chunkFileNames: '[name]-[hash].js',
        assetFileNames: '[name]-[hash].[ext]',
      },
    },
  },

  server: {
    port: 5173,
    // Proxy API calls to Django in development
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
```

## Component Mounting Pattern

### Django Template Side

```html
<!-- templates/production/dashboard.html -->
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1>Production Dashboard</h1>

    <!-- React Island: DataTable -->
    <div
        data-react-component="DataTable"
        data-react-props='{"endpoint": "/api/v1/lots/", "columns": ["code", "quantite", "status"]}'
    ></div>

    <!-- React Island: Chart with initial data from Django -->
    <div
        data-react-component="KpiChart"
        data-react-props='{{ chart_data|safe }}'
    ></div>

    <!-- Load React bundle -->
    <script type="module" src="{% static 'assets/main.js' %}"></script>
</body>
</html>
```

### Django View (passing data)

```python
# apps/production/views.py
import json
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'production/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prepare data for React component
        chart_data = {
            'labels': ['Jan', 'Feb', 'Mar'],
            'values': [100, 150, 200],
            'title': 'Production mensuelle',
        }
        context['chart_data'] = json.dumps(chart_data)

        return context
```

### React Entry Point (Component Registry)

```tsx
// frontend/src/main.tsx
import { createRoot } from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Import all mountable components
import { DataTable } from './components/features/DataTable';
import { KpiChart } from './components/features/KpiChart';
import { LotForm } from './components/features/LotForm';

// Component registry - add all components that can be mounted
const COMPONENTS: Record<string, React.ComponentType<any>> = {
  DataTable,
  KpiChart,
  LotForm,
};

// React Query client (shared across all islands)
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Mount all React components on page load
function mountComponents() {
  const elements = document.querySelectorAll('[data-react-component]');

  elements.forEach((element) => {
    const componentName = element.getAttribute('data-react-component');
    const propsJson = element.getAttribute('data-react-props') || '{}';

    if (!componentName) return;

    const Component = COMPONENTS[componentName];
    if (!Component) {
      console.warn(`Unknown component: ${componentName}`);
      return;
    }

    try {
      const props = JSON.parse(propsJson);

      createRoot(element).render(
        <QueryClientProvider client={queryClient}>
          <Component {...props} />
        </QueryClientProvider>
      );
    } catch (error) {
      console.error(`Failed to mount ${componentName}:`, error);
    }
  });
}

// Mount on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mountComponents);
} else {
  mountComponents();
}
```

## Props Passing Patterns

### Pattern 1: Inline JSON (simple data)

```html
<div
    data-react-component="StatusBadge"
    data-react-props='{"status": "active", "label": "En cours"}'
></div>
```

### Pattern 2: Django template variable (dynamic data)

```html
<!-- In Django view: context['lot_data'] = json.dumps(lot_dict) -->
<div
    data-react-component="LotCard"
    data-react-props='{{ lot_data|safe }}'
></div>
```

### Pattern 3: API endpoint (lazy loading)

```html
<div
    data-react-component="DataTable"
    data-react-props='{"endpoint": "/api/v1/lots/", "pageSize": 25}'
></div>
```

```tsx
// Component fetches data via React Query
function DataTable({ endpoint, pageSize }: Props) {
  const { data, isLoading } = useQuery({
    queryKey: ['table-data', endpoint],
    queryFn: () => fetch(endpoint).then(r => r.json()),
  });

  // ...
}
```

### Pattern 4: Hidden input for forms

```html
<form>
    {% csrf_token %}
    <input type="hidden" name="initial_data" value='{{ form_data|safe }}' />

    <div
        data-react-component="ComplexForm"
        data-react-props='{}'
    ></div>
</form>
```

```tsx
// Component reads from hidden input
function ComplexForm() {
  const initialData = useMemo(() => {
    const input = document.querySelector('input[name="initial_data"]');
    return input ? JSON.parse(input.value) : {};
  }, []);

  // ...
}
```

## Development Workflow

### Terminal 1: Django backend

```bash
cd backend
python manage.py runserver
```

### Terminal 2: Vite dev server (HMR)

```bash
cd frontend
npm run dev
```

### Production Build

```bash
cd frontend
npm run build

cd ../backend
python manage.py collectstatic --noinput
```

## Django-Vite Integration (Optional)

For more sophisticated integration with manifest parsing:

```python
# pip install django-vite

# settings.py
INSTALLED_APPS += ['django_vite']

DJANGO_VITE = {
    'default': {
        'dev_mode': DEBUG,
        'dev_server_port': 5173,
        'manifest_path': BASE_DIR / 'static' / 'assets' / 'manifest.json',
    }
}
```

```html
{% load django_vite %}

<!DOCTYPE html>
<html>
<head>
    {% vite_hmr_client %}
    {% vite_asset 'src/main.tsx' %}
</head>
<!-- ... -->
</html>
```

## Zone Separation: HTMX vs React

**Critical Rule**: Never mix HTMX and React on the same element.

```html
<!-- GOOD: Separate zones -->
<div id="htmx-zone" hx-get="/partials/notifications" hx-trigger="every 30s">
    <!-- HTMX handles this zone -->
</div>

<div data-react-component="DataTable" data-react-props="{}">
    <!-- React handles this zone -->
</div>

<!-- BAD: Mixed zones -->
<div
    hx-get="/something"
    data-react-component="Something"
>
    <!-- CONFLICT! -->
</div>
```

### Decision Matrix: HTMX vs React

| Use Case | Choose |
|----------|--------|
| Simple form submission | HTMX |
| Server-rendered partials | HTMX |
| Notifications/toasts | HTMX |
| Complex interactive table | React |
| Real-time charts | React |
| Multi-step wizard | React |
| Drag-and-drop | React |
