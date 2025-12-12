# Django Forms & Validation Rules

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  User (Backoffice HTML)                                 │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Django Views (FBV/CBV)                                 │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Django Forms (Form / ModelForm)                        │
│  └── Input validation, field definition, normalization  │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Services (usecases/, domain/)                          │
│  └── Business rules, transactions, integrations         │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Models & ORM                                           │
│  └── Structural constraints, DB integrity               │
└─────────────────────────────────────────────────────────┘
```

## Forms Directory Structure

```
apps/
  <app_name>/
    forms/
      __init__.py           # Re-export public forms
      item_forms.py         # Item-related forms
      order_forms.py        # Order-related forms
      import_forms.py       # File upload forms
    views/
    services/
    tests/
      test_forms.py
```

## Validation Levels Distribution

| Level | What to Validate | Example |
|-------|------------------|---------|
| **Database** | Structural integrity | NOT NULL, UNIQUE, FK, CHECK |
| **Model** | Field-level invariants | `clean()` for cross-field model rules |
| **Form** | Input-specific rules | Required fields, format, local coherence |
| **Service** | Business rules | Overlap checks, permissions, calculations |

**Rule**: Validation that applies to ALL entry points (HTML, API, ETL) → Model/DB  
**Rule**: Validation specific to a UI form → Form  
**Rule**: Complex business rules → Service

## Form Types

### ModelForm (CRUD)
```python
# apps/items/forms/item_forms.py
from django import forms
from apps.items.models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "amount", "description"]
        
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount
```

### Form (Use Case DTO)
```python
# apps/items/forms/item_forms.py
class ItemSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date must be before end date.")
        
        return cleaned_data
```

## Form Lifecycle

```python
# View handling form
def item_create_view(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            # Delegate to service
            item = create_item_with_defaults(
                payload=form.cleaned_data,
                user=request.user,
            )
            return redirect("items:detail", pk=item.pk)
    else:
        form = ItemForm()  # Unbound form
    
    return render(request, "items/form.html", {"form": form})
```

### Using commit=False
```python
if form.is_valid():
    instance = form.save(commit=False)
    # Enrich before saving
    instance.created_by = request.user
    instance.save()
    form.save_m2m()  # Don't forget for M2M fields
```

## Field Validation

### Single Field Validation
```python
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["quantity", "delivery_date"]
    
    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity > 1000:
            raise forms.ValidationError("Maximum quantity is 1000.")
        return quantity
    
    def clean_delivery_date(self):
        delivery_date = self.cleaned_data["delivery_date"]
        if delivery_date < date.today():
            raise forms.ValidationError("Delivery date cannot be in the past.")
        return delivery_date
```

### Cross-Field Validation
```python
class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        
        if start and end:
            if start > end:
                raise forms.ValidationError("Start date must be before end date.")
            if (end - start).days > 365:
                self.add_error("end_date", "Range cannot exceed 1 year.")
        
        return cleaned_data
```

## Integration with Services

```python
# apps/orders/forms/order_forms.py
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "items", "delivery_date"]

# apps/orders/views/backoffice.py
from apps.orders.services.usecases import create_order_and_notify

def order_create_view(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Service handles business logic + transaction
            order = create_order_and_notify(
                payload=form.cleaned_data,
                user=request.user,
            )
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderCreateForm()
    
    return render(request, "orders/form.html", {"form": form})
```

```python
# apps/orders/services/usecases/create_order.py
from django.db import transaction

@transaction.atomic
def create_order_and_notify(payload: dict, user) -> Order:
    order = Order.objects.create(**payload, created_by=user)
    calculate_order_totals(order)
    send_order_notification(order)
    return order
```

## Formsets

### Basic Formset
```python
from django.forms import formset_factory

class LineItemForm(forms.Form):
    product = forms.CharField(max_length=100)
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(max_digits=10, decimal_places=2)

LineItemFormSet = formset_factory(
    LineItemForm,
    extra=3,
    can_delete=True,
)
```

### Inline Formset (Parent-Child)
```python
from django.forms import inlineformset_factory
from apps.orders.models import Order, OrderLine

OrderLineFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderLine,
    fields=["product", "quantity", "price"],
    extra=1,
    can_delete=True,
)
```

### View with Formset
```python
def order_edit_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderLineFormSet(request.POST, instance=order)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderLineFormSet(instance=order)
    
    return render(request, "orders/edit.html", {
        "form": form,
        "formset": formset,
    })
```

## File Upload

```python
# Form
class ImportForm(forms.Form):
    file = forms.FileField()
    overwrite = forms.BooleanField(required=False)

# View
def import_view(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)  # Note: request.FILES
        if form.is_valid():
            file = form.cleaned_data["file"]
            # Delegate to ETL service
            result = import_data_from_file(file, request.user)
            messages.success(request, f"Imported {result.count} records.")
            return redirect("items:list")
    else:
        form = ImportForm()
    
    return render(request, "items/import.html", {"form": form})
```

### Template for File Upload
```django
<form method="post" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Import</button>
</form>
```

## Security

### CSRF Protection
```django
{# Always include in POST forms #}
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Submit</button>
</form>
```

### XSS Prevention
```django
{# Safe - auto-escaped #}
{{ user_input }}

{# DANGEROUS - only for trusted content #}
{{ trusted_html|safe }}
```

---

## ✅ DO

- ✅ Use `ModelForm` for simple CRUD operations
- ✅ Use `Form` for use cases not mapping 1:1 to models
- ✅ Validate field-specific rules in `clean_<field>()`
- ✅ Validate cross-field rules in `clean()`
- ✅ Always call `is_valid()` before accessing `cleaned_data`
- ✅ Delegate business logic to services after validation
- ✅ Use `commit=False` for pre-save modifications
- ✅ Include `{% csrf_token %}` in all POST forms
- ✅ Use `enctype="multipart/form-data"` for file uploads
- ✅ Pass `request.FILES` to form constructor

---

## ❌ DON'T

- ❌ **No business logic in forms** - delegate to services
- ❌ **No transactions in forms** - handle in services
- ❌ **No heavy `save()` overrides** - use services
- ❌ **No ORM queries in forms** - compute in views/services
- ❌ **No `|safe` on user input** - XSS vulnerability
- ❌ **No missing `{% csrf_token %}`** - CSRF vulnerability
- ❌ **No `@csrf_exempt` on backoffice views**
- ❌ **No formsets for simple single-object forms**

---

## Checklist

### Organization & Structure
- [ ] Each app has `forms/` directory with context-based files
- [ ] `forms/` contains only form logic (no services, no ETL)
- [ ] Shared forms in `shared/forms/` if needed (rare)

### Form Types
- [ ] Simple CRUD → `ModelForm`
- [ ] Use case specific → `Form` + service
- [ ] `ModelForm.save()` not overloaded with business logic

### Validation
- [ ] Simple field validation in `clean_<field>()`
- [ ] Cross-field validation in `clean()`
- [ ] Structural invariants in models + DB constraints
- [ ] Business rules in services
- [ ] `is_valid()` always called before using `cleaned_data`

### Security & UX
- [ ] All POST forms include `{% csrf_token %}`
- [ ] No `|safe` on uncontrolled user data
- [ ] Clear error messages (field-specific vs non-field)

### Multiple Items & Files
- [ ] Formsets used only when UX requires multiple objects
- [ ] File uploads use `FileField` + ETL service for processing
- [ ] `enctype="multipart/form-data"` on upload forms
