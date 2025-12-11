# Django Templates & Frontend Integration Rules

## Architecture Overview

```
Server-Side First Architecture:
┌─────────────────────────────────────────────────────────┐
│  Browser (HTML + JS)                                    │
│  ├── Django Templates (base HTML)                       │
│  ├── HTMX (AJAX interactions, partial updates)          │
│  └── React Islands (rich components, dashboards)        │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Django Backend                                         │
│  ├── Views → Template Engine → HTML Response            │
│  ├── Services → Business Logic                          │
│  └── Models → ORM                                       │
└─────────────────────────────────────────────────────────┘
```

## Template Directory Structure

### Global Templates (Project Level)
```
backend/
  templates/
    base.html                    # Root layout
    base_backoffice.html         # Admin/backoffice layout
    base_public.html             # Public-facing layout
    partials/
      _navbar.html               # Shared navigation
      _messages.html             # Flash messages
      _pagination.html           # Pagination component
    react/
      vite_entry.html            # Vite bundle loader helper
      _react_mount.html          # Generic React root template
```

### App-Level Templates
```
apps/
  <app_name>/
    templates/
      <app_name>/                # Namespaced folder (required)
        liste.html               # List view
        detail.html              # Detail view
        form.html                # Create/edit form
        partials/
          _table_items.html      # HTMX table partial
          _row_item.html         # HTMX row partial
```

## Template Settings Configuration

```python
# config/settings/base.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",  # Global templates
        ],
        "APP_DIRS": True,            # Enable app templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

## Template Inheritance Pattern

### Base Layout
```django
{# templates/base_backoffice.html #}
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}App{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
  {% block extra_head %}{% endblock %}
</head>
<body hx-boost="true">
  {% include "partials/_navbar.html" %}
  <main id="main-content">
    {% include "partials/_messages.html" %}
    {% block content %}{% endblock %}
  </main>
  <script src="{% static 'js/htmx.min.js' %}" defer></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template
```django
{% extends "base_backoffice.html" %}

{% block title %}Item List{% endblock %}

{% block content %}
  <h1>Items</h1>
  <table>
    {% for item in items %}
      <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.created_at|date:"Y-m-d" }}</td>
      </tr>
    {% empty %}
      <tr><td colspan="2">No items found.</td></tr>
    {% endfor %}
  </table>
{% endblock %}
```

## HTMX Integration

### Filter Form with Partial Update
```django
{# Full page template #}
<form
  id="filter-form"
  hx-get="{% url 'app:list' %}"
  hx-target="#table-container"
  hx-push-url="true"
>
  <select name="status">...</select>
  <button type="submit">Filter</button>
</form>

<div id="table-container">
  {% include "app/partials/_table.html" %}
</div>
```

### View with HTMX Detection
```python
# apps/<app>/views/backoffice.py
def item_list(request):
    items = Item.objects.filter(...)
    context = {"items": items}
    
    if request.htmx:
        # Return partial for HTMX requests
        return render(request, "app/partials/_table.html", context)
    
    # Return full page for standard requests
    return render(request, "app/list.html", context)
```

### HTMX Redirect After Action
```python
from django_htmx.http import HttpResponseClientRedirect

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return HttpResponseClientRedirect(reverse("app:list"))
```

## React Islands Integration

### Template with React Mount Point
```django
{% extends "base_backoffice.html" %}

{% block content %}
  <h1>Dashboard</h1>
  
  <div
    id="dashboard-root"
    data-item-id="{{ item.id }}"
    data-user="{{ request.user.username }}"
  ></div>
{% endblock %}

{% block extra_js %}
  {% include "react/vite_entry.html" with entry="apps/dashboard/main.tsx" %}
{% endblock %}
```

### React Entry Point
```tsx
// frontend/apps/dashboard/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { Dashboard } from "./Dashboard";

const root = document.getElementById("dashboard-root");
if (root) {
  const props = {
    itemId: root.dataset.itemId,
    user: root.dataset.user,
  };
  
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <Dashboard {...props} />
    </React.StrictMode>
  );
}
```

## Zone Separation: HTMX vs React

```django
{# Correct: Separate zones #}
<div class="layout">
  <!-- HTMX Zone -->
  <section id="htmx-zone" hx-target="#table-container">
    <form hx-get="{% url 'app:list' %}">...</form>
    <div id="table-container">
      {% include "app/partials/_table.html" %}
    </div>
  </section>

  <!-- React Zone (never touched by HTMX) -->
  <section id="react-zone">
    <div id="chart-root" data-config='{{ chart_config|escapejs }}'></div>
  </section>
</div>
```

---

## ✅ DO

- ✅ Use template inheritance (`{% extends %}`) for all pages
- ✅ Namespace app templates: `apps/<app>/templates/<app>/`
- ✅ Prefix partials with `_` or put in `partials/` folder
- ✅ Use `{% url 'app:name' %}` for all URL references
- ✅ Use `{% static 'path' %}` for all static files
- ✅ Check `request.htmx` to return appropriate response
- ✅ Keep template logic minimal: `if`, `for`, `with`, `include`
- ✅ Use filters for display formatting: `|date`, `|default`
- ✅ Pass data to React via `data-*` attributes
- ✅ One React root per functional zone
- ✅ React consumes JSON API, HTMX consumes HTML partials

---

## ❌ DON'T

- ❌ **No ORM calls in templates** - compute in views/services
- ❌ **No business logic in templates** - presentation only
- ❌ **No hardcoded URLs** - always use `{% url %}`
- ❌ **No `|safe` on user input** - XSS vulnerability
- ❌ **No HTMX targeting React roots** - breaks React DOM
- ❌ **No React inside HTMX swap targets** - unmounts components
- ❌ **No mixed zones** - one technology per DOM section
- ❌ **No complex calculations** - delegate to services
- ❌ **No duplicate template namespaces** - causes conflicts

---

## Checklist

### Template Structure
- [ ] `TEMPLATES` config uses `DIRS` + `APP_DIRS=True`
- [ ] Global templates in `backend/templates/`
- [ ] App templates in `apps/<app>/templates/<app>/`
- [ ] Partials clearly identified (`_` prefix or `partials/` folder)
- [ ] All pages extend a base layout

### Template Quality
- [ ] No direct ORM access in templates
- [ ] Logic limited to control tags only
- [ ] Filters used for presentation formatting
- [ ] URLs generated with `{% url %}` tag

### HTMX
- [ ] HTMX script loaded in base layout
- [ ] `hx-boost="true"` for navigation where appropriate
- [ ] HTMX endpoints return partials (not full pages)
- [ ] Views detect `request.htmx` for response type
- [ ] `hx-target` avoids React zones

### React Islands
- [ ] React roots defined via `<div id="...">` elements
- [ ] Props passed via `data-*` attributes
- [ ] Bundles included via Vite helper
- [ ] React consumes API endpoints (not HTML)
- [ ] React zones not manipulated by HTMX

### i18n & Accessibility
- [ ] `{% trans %}` used for translatable strings
- [ ] `aria-live` regions for HTMX updates
- [ ] Loading indicators for async operations
