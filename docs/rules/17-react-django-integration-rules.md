# React + Django Integration Rules (Vite)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Django Monolith                                        │
│  ├── Templates (HTML) ──────────────────────────────┐   │
│  │   └── React mount points (<div data-react-*>)    │   │
│  ├── Views (render pages)                           │   │
│  └── DRF API (JSON endpoints)                       │   │
└─────────────────────────────────────────────────────────┘
         │                                        ▲
         │ includes <script>                      │ fetch/API
         ▼                                        │
┌─────────────────────────────────────────────────────────┐
│  Vite Build                                             │
│  └── React bundles → /static/assets/                    │
└─────────────────────────────────────────────────────────┘
```

**Benefits**:
- Single deployment (one Docker, one CI/CD)
- Django handles auth, permissions, routing
- React enhances specific interactive zones
- No CORS issues (same origin)

## Project Structure

```
project/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings/
│   │   └── urls.py
│   ├── apps/
│   ├── templates/
│   │   ├── base.html
│   │   └── dashboard/
│   │       └── index.html
│   └── static/
│       └── assets/          # ← Vite build output
│
└── frontend/
    ├── src/
    │   ├── main.tsx
    │   └── components/
    ├── vite.config.ts
    ├── tailwind.config.js
    └── package.json
```

## Vite Configuration

### vite.config.ts
```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  
  // Static URL path in Django
  base: "/static/assets/",
  
  build: {
    // Output to Django static folder
    outDir: "../backend/static/assets",
    emptyOutDir: true,
    
    // Generate manifest for django-vite
    manifest: true,
    
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main.tsx"),
      },
    },
  },
  
  server: {
    // Dev server for HMR
    port: 5173,
    strictPort: true,
  },
});
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

## Django Template Integration

### Base Template
```html
<!-- templates/base.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}App{% endblock %}</title>
    
    <!-- Tailwind CSS (from Vite build) -->
    <link rel="stylesheet" href="{% static 'assets/main.css' %}">
</head>
<body>
    {% block content %}{% endblock %}
    
    <!-- React bundle -->
    {% block scripts %}
    <script type="module" src="{% static 'assets/main.js' %}"></script>
    {% endblock %}
</body>
</html>
```

### Page with React Component
```html
<!-- templates/dashboard/index.html -->
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
    
    <!-- Static Django content -->
    <p>Welcome, {{ user.username }}</p>
    
    <!-- React mount point with data -->
    <div 
        id="kpi-chart"
        data-react-component="KpiChart"
        data-react-props='{{ chart_data|safe }}'
    ></div>
    
    <!-- Another React component -->
    <div 
        id="data-table"
        data-react-component="DataTable"
        data-react-props='{"endpoint": "/api/v1/orders/", "columns": ["id", "status", "total"]}'
    ></div>
</div>
{% endblock %}
```

### Django View
```python
# apps/dashboard/views.py
import json
from django.shortcuts import render

def dashboard_view(request):
    # Prepare data for React component
    chart_data = json.dumps({
        "title": "Monthly KPIs",
        "data": [
            {"month": "Jan", "value": 100},
            {"month": "Feb", "value": 150},
        ],
    })
    
    return render(request, "dashboard/index.html", {
        "chart_data": chart_data,
    })
```

## React Entry Point

### Component Registry & Mounting
```tsx
// frontend/src/main.tsx
import "./index.css";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Import all components
import KpiChart from "./components/KpiChart";
import DataTable from "./components/DataTable";
import FilterForm from "./components/FilterForm";

// Component registry
const COMPONENTS: Record<string, React.ComponentType<any>> = {
  KpiChart,
  DataTable,
  FilterForm,
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 1,
    },
  },
});

// Mount all React components on the page
function mountComponents() {
  const elements = document.querySelectorAll("[data-react-component]");
  
  elements.forEach((el) => {
    const name = el.getAttribute("data-react-component");
    const propsJson = el.getAttribute("data-react-props") || "{}";
    
    if (!name || !COMPONENTS[name]) {
      console.warn(`Unknown component: ${name}`);
      return;
    }
    
    try {
      const Component = COMPONENTS[name];
      const props = JSON.parse(propsJson);
      
      createRoot(el).render(
        <QueryClientProvider client={queryClient}>
          <Component {...props} />
        </QueryClientProvider>
      );
    } catch (error) {
      console.error(`Failed to mount ${name}:`, error);
    }
  });
}

// Mount when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", mountComponents);
} else {
  mountComponents();
}
```

## Data Passing Patterns

### Pattern 1: Initial Data via data-* Attributes
```html
<!-- Django template -->
<div 
    data-react-component="OrderList"
    data-react-props='{{ orders_json|safe }}'
></div>
```

```tsx
// React component receives props directly
interface OrderListProps {
  orders: Order[];
}

function OrderList({ orders }: OrderListProps) {
  return <ul>{orders.map(o => <li key={o.id}>{o.name}</li>)}</ul>;
}
```

### Pattern 2: API Endpoint for Dynamic Data
```html
<!-- Django template -->
<div 
    data-react-component="OrderTable"
    data-react-props='{"endpoint": "/api/v1/orders/"}'
></div>
```

```tsx
// React component fetches data
function OrderTable({ endpoint }: { endpoint: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ["orders"],
    queryFn: () => fetch(endpoint).then(r => r.json()),
  });
  
  if (isLoading) return <Skeleton />;
  return <Table data={data.results} />;
}
```

### Pattern 3: Django Template Tag (Optional)
```python
# templatetags/react_tags.py
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.simple_tag
def react_component(name, **props):
    props_json = json.dumps(props)
    return mark_safe(
        f'<div data-react-component="{name}" '
        f'data-react-props=\'{props_json}\'></div>'
    )
```

```html
{% load react_tags %}
{% react_component "KpiChart" data=chart_data title="Monthly KPIs" %}
```

## API Communication

### CSRF Token Handling
```tsx
// src/utils/api.ts
export function getCsrfToken(): string {
  // From cookie
  const cookie = document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="));
  if (cookie) return cookie.split("=")[1];
  
  // From hidden input
  const input = document.querySelector<HTMLInputElement>(
    "[name=csrfmiddlewaretoken]"
  );
  return input?.value || "";
}

export async function apiPost<T>(url: string, data: unknown): Promise<T> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    credentials: "same-origin",
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}
```

### React Query with CSRF
```tsx
// src/api/mutations.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiPost } from "../utils/api";

export function useCreateOrder() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateOrderInput) => 
      apiPost("/api/v1/orders/", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });
}
```

## Development Workflow

### Running Both Servers
```bash
# Terminal 1: Django
cd backend
python manage.py runserver

# Terminal 2: Vite (HMR)
cd frontend
npm run dev
```

### Development with HMR (Optional: django-vite)
```python
# settings/dev.py
DJANGO_VITE = {
    "default": {
        "dev_mode": True,
        "dev_server_port": 5173,
    }
}
```

```html
<!-- With django-vite -->
{% load django_vite %}
{% vite_hmr_client %}
{% vite_asset 'src/main.tsx' %}
```

### Production Build
```bash
# Build React
cd frontend
npm run build

# Collect static files
cd ../backend
python manage.py collectstatic --noinput
```

## Zone Separation: HTMX vs React

```html
<!-- ⚠️ NEVER mix HTMX and React on same element -->

<!-- HTMX zone (server-rendered updates) -->
<div id="notifications" hx-get="/notifications/" hx-trigger="every 30s">
    {% include "partials/notifications.html" %}
</div>

<!-- React zone (client-side interactivity) -->
<div data-react-component="DataTable" data-react-props='...'></div>

<!-- Static Django content -->
<div class="content">
    {{ article.body|safe }}
</div>
```

---

## ✅ DO

- ✅ Use `data-react-component` and `data-react-props` pattern
- ✅ Configure Vite output to Django static folder
- ✅ Include CSRF token in all POST/PUT/DELETE requests
- ✅ Use `|safe` filter for JSON props (ensure data is valid JSON)
- ✅ Mount components conditionally (check element exists)
- ✅ Use React Query for API data fetching
- ✅ Keep React islands independent
- ✅ Let Django handle routing and auth

---

## ❌ DON'T

- ❌ **No React Router** - Django handles navigation
- ❌ **No mixing HTMX targets with React roots**
- ❌ **No inline JS in templates** - use React components
- ❌ **No hardcoded API URLs** - pass via props
- ❌ **No forgetting CSRF** on mutations
- ❌ **No global React state for page data** - get from Django

---

## Build Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server (HMR) |
| `npm run build` | Build for production |
| `collectstatic` | Gather static files for Django |

## Files to Gitignore

```gitignore
# Frontend
frontend/node_modules/
frontend/dist/

# Generated assets in Django
backend/static/assets/

# Keep manifest if using django-vite
!backend/static/assets/.vite/manifest.json
```

---

## Checklist

### Vite Setup
- [ ] `vite.config.ts` with correct `base` and `outDir`
- [ ] Manifest generation enabled
- [ ] React plugin configured

### Django Setup
- [ ] Static files configured for Vite output
- [ ] Base template includes React bundle
- [ ] CSRF token available for API calls

### Component Integration
- [ ] `data-react-component` attributes on mount points
- [ ] Props passed as JSON via `data-react-props`
- [ ] Component registry in main.tsx
- [ ] Error boundaries for component failures

### Development
- [ ] Both servers running (Django + Vite)
- [ ] HMR working for React changes
- [ ] API calls working with CSRF

### Production
- [ ] `npm run build` generates assets
- [ ] `collectstatic` includes built assets
- [ ] No dev dependencies in production
