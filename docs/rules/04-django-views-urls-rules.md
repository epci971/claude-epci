# Django Views & URLs Rules

## URL Structure

### Root URLs (`config/urls.py`)

Only aggregates app URLs - no business logic:

```python
# config/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # HTML routes (backoffice)
    path("taxe/", include("apps.taxe_sejour.urls", namespace="taxe_sejour")),
    path("labo/", include("apps.labo.urls", namespace="labo")),
    path("comptes/", include("apps.comptes.urls", namespace="comptes")),
    
    # API routes (DRF)
    path("api/taxe/", include("apps.taxe_sejour.api.routers")),
    path("api/labo/", include("apps.labo.api.routers")),
    
    # Monitoring
    path("healthz/", include("apps.monitoring.urls")),
]

# Error handlers
handler400 = "apps.core.views.bad_request"
handler403 = "apps.core.views.permission_denied"
handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"

# Debug only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
```

### App URLs (`apps/<app>/urls.py`)

```python
# apps/taxe_sejour/urls.py
from django.urls import path
from .views import backoffice

app_name = "taxe_sejour"  # Required for namespacing

urlpatterns = [
    path("", backoffice.TaxeListView.as_view(), name="liste"),
    path("nouvelle/", backoffice.TaxeCreateView.as_view(), name="creer"),
    path("<uuid:pk>/", backoffice.TaxeDetailView.as_view(), name="detail"),
    path("<uuid:pk>/modifier/", backoffice.TaxeUpdateView.as_view(), name="modifier"),
    path("<uuid:pk>/supprimer/", backoffice.TaxeDeleteView.as_view(), name="supprimer"),
    # Custom actions
    path("<uuid:pk>/generer-pdf/", backoffice.GenererPDFView.as_view(), name="generer_pdf"),
]
```

### DRF Routers (`apps/<app>/api/routers.py`)

```python
# apps/taxe_sejour/api/routers.py
from rest_framework.routers import DefaultRouter
from .viewsets.taxe import TaxeSejourViewSet

router = DefaultRouter()
router.register("taxes", TaxeSejourViewSet, basename="taxe")

urlpatterns = router.urls
```

## URL Conventions

### Path Style

```
/taxe/                      → liste
/taxe/nouvelle/             → creer
/taxe/<uuid:pk>/            → detail
/taxe/<uuid:pk>/modifier/   → modifier
/taxe/<uuid:pk>/supprimer/  → supprimer
/taxe/<uuid:pk>/action/     → custom action (verb)
```

### Name Conventions

| Action | Name |
|--------|------|
| List | `liste` |
| Detail | `detail` |
| Create | `creer` |
| Update | `modifier` |
| Delete | `supprimer` |
| Custom | verb (`generer_pdf`, `clore_periode`, `exporter_csv`) |

### Path Converters

```python
path("<int:pk>/", ...)      # Auto-increment IDs (non-sensitive)
path("<uuid:pk>/", ...)     # UUIDs (sensitive data: payments, taxes)
path("<slug:slug>/", ...)   # Public-facing URLs
```

## Views Structure

### Module Organization

```
apps/<domain>/views/
├── __init__.py
├── backoffice.py      # Internal/admin screens
├── public.py          # Public-facing views (if any)
└── exports.py         # CSV, Excel, PDF exports
```

### Class-Based Views for CRUD

```python
# apps/sejour/views/backoffice.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class SejourListView(LoginRequiredMixin, ListView):
    model = Sejour
    template_name = "sejour/liste.html"
    context_object_name = "sejours"
    paginate_by = 25
    
    def get_queryset(self):
        return Sejour.objects.actifs().select_related("logement", "commune")

class SejourDetailView(LoginRequiredMixin, DetailView):
    model = Sejour
    template_name = "sejour/detail.html"
    
    def get_queryset(self):
        return Sejour.objects.select_related("logement", "commune")

class SejourCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Sejour
    form_class = SejourForm
    template_name = "sejour/form.html"
    permission_required = "sejour.add_sejour"
    success_url = reverse_lazy("sejour:liste")

class SejourUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Sejour
    form_class = SejourForm
    template_name = "sejour/form.html"
    permission_required = "sejour.change_sejour"

class SejourDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Sejour
    template_name = "sejour/confirm_delete.html"
    permission_required = "sejour.delete_sejour"
    success_url = reverse_lazy("sejour:liste")
```

### Views Calling Services

```python
# apps/taxe_sejour/views/backoffice.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from ..services.usecases.calculer_taxe import calculer_taxe_sejour
from ..exceptions import TaxeDejaCalculeeError

class CalculerTaxeView(LoginRequiredMixin, View):
    """View is thin - delegates to service."""
    
    def post(self, request, sejour_id):
        try:
            result = calculer_taxe_sejour(
                sejour_id=sejour_id,
                user=request.user,
            )
            messages.success(request, f"Taxe calculée: {result.montant}€")
            return redirect("taxe_sejour:detail", pk=result.taxe_id)
        
        except TaxeDejaCalculeeError:
            messages.error(request, "Taxe déjà calculée pour ce séjour")
            return redirect("sejour:detail", pk=sejour_id)
```

### Function-Based Views (Simple Cases)

```python
# apps/monitoring/views.py
from django.http import JsonResponse

def health_check(request):
    """Simple healthcheck - FBV is fine."""
    return JsonResponse({"status": "ok"})

def ready_check(request):
    """Kubernetes readiness probe."""
    # Check DB connection
    from django.db import connection
    connection.ensure_connection()
    return JsonResponse({"status": "ready"})
```

## Navigation & URLs

### Always Use reverse() or {% url %}

```python
# In Python
from django.urls import reverse

url = reverse("taxe_sejour:detail", kwargs={"pk": taxe.id})
return redirect("taxe_sejour:liste")
```

```html
<!-- In templates -->
<a href="{% url 'taxe_sejour:detail' pk=taxe.id %}">View</a>
<form action="{% url 'taxe_sejour:creer' %}" method="post">
```

## DO ✅

```python
# ✅ Use generic CBVs for CRUD
class SejourListView(LoginRequiredMixin, ListView):
    model = Sejour
    paginate_by = 25

# ✅ Always optimize queries in get_queryset()
def get_queryset(self):
    return Sejour.objects.select_related("logement").prefetch_related("taxes")

# ✅ LoginRequiredMixin on all sensitive views
class TaxeDetailView(LoginRequiredMixin, DetailView):
    ...

# ✅ Delegate to services for business logic
def post(self, request, pk):
    result = process_payment(pk, request.user)  # Service call
    return redirect(...)

# ✅ Use namespaces
path("taxe/", include("apps.taxe_sejour.urls", namespace="taxe_sejour"))

# ✅ app_name in every urls.py
app_name = "taxe_sejour"

# ✅ Pagination for lists
paginate_by = 25
```

## DON'T ❌

```python
# ❌ Business logic in views
class TaxeView(View):
    def post(self, request):
        sejour = Sejour.objects.get(pk=request.POST["id"])
        montant = sejour.nb_nuits * sejour.taux  # BAD - logic in view
        TaxeSejour.objects.create(montant=montant)  # BAD

# ❌ Hardcoded URLs
return redirect("/taxe/123/")  # BAD
return HttpResponseRedirect(f"/taxe/{taxe.id}/")  # BAD

# ❌ Logic in config/urls.py
# config/urls.py
def my_view(request):  # BAD - put in app views
    ...
urlpatterns = [path("x/", my_view)]

# ❌ Missing select_related (N+1 queries)
def get_queryset(self):
    return Sejour.objects.all()  # BAD if template accesses sejour.logement

# ❌ No pagination on lists
class SejourListView(ListView):
    model = Sejour  # BAD - no paginate_by

# ❌ Missing LoginRequiredMixin
class TaxeDetailView(DetailView):  # BAD - no auth check
    model = TaxeSejour

# ❌ Missing app_name
# urls.py
urlpatterns = [...]  # BAD - no app_name = "..."

# ❌ Transactions in views (should be in services)
def post(self, request):
    with transaction.atomic():  # BAD - put in service
        ...
```

## Security

```python
# Always use mixins for auth/perms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class TaxeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "taxe_sejour.view_taxesejour"
    
class TaxeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "taxe_sejour.add_taxesejour"

# Pass user to services for audit/authorization
def post(self, request, pk):
    result = delete_sejour(pk, user=request.user)  # Always pass user
```

## Checklist

### URL Structure
- [ ] `config/urls.py` only includes app URLs via `include()` - no logic
- [ ] Each app has `urls.py` with `app_name` defined
- [ ] URLs are namespaced (`namespace="taxe_sejour"`)
- [ ] Routes have names (`name="detail"`, `name="liste"`)
- [ ] Consistent naming: `liste`, `detail`, `creer`, `modifier`, `supprimer`
- [ ] Path converters used consistently (`uuid` for sensitive, `int` for refs)

### Views Organization
- [ ] Views in `views/backoffice.py`, `views/public.py`, `views/exports.py`
- [ ] CRUD uses generic CBVs (ListView, DetailView, CreateView, etc.)
- [ ] FBV only for simple cases (healthcheck, redirects)

### Views Behavior
- [ ] NO business logic in views - delegate to services
- [ ] `LoginRequiredMixin` on all sensitive views
- [ ] `PermissionRequiredMixin` where needed
- [ ] `get_queryset()` uses `select_related`/`prefetch_related`
- [ ] Lists have `paginate_by`

### Service Integration
- [ ] Use cases called from views, not inline logic
- [ ] `request.user` passed to services for security/audit
- [ ] Transactions managed in services, not views
- [ ] Service exceptions caught and converted to user messages

### Navigation
- [ ] No hardcoded URLs - always `reverse()` or `{% url %}`
- [ ] Custom error handlers defined (400, 403, 404, 500)
