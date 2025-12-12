# Django Code Conventions & IDE Rules

## Core Principles

1. **Readability > Cleverness**: Clear code over one-liners
2. **Separation of Concerns**: Models → Services → Views/API
3. **Tests by Default**: New code = new tests
4. **Predictable Structure**: AI/IDE-friendly organization

## Python Style (PEP 8)

### Naming Conventions
```python
# Variables and functions: snake_case
user_count = 10
def calculate_total():
    pass

# Classes: PascalCase
class OrderService:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_PAGE_SIZE = 50

# Private: leading underscore
def _internal_helper():
    pass
```

### Line Length & Formatting
```python
# Max line length: 88 characters (Black default)
# Indentation: 4 spaces (no tabs)

# Tools
# - ruff: linting
# - black: formatting
# - isort: import sorting (or ruff)
```

## Import Order

```python
# 1. Standard library
import logging
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

# 2. Third-party packages
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

# 3. Local application
from apps.orders.models import Order
from apps.orders.services.usecases import create_order
from shared.utils import format_currency
```

**Rules**:
- No `from module import *`
- Group imports with blank lines
- Alphabetical within groups

## Project Structure

```
backend/
  src/
    config/
      settings/
        base.py
        dev.py
        test.py
        prod.py
      urls.py
      celery.py
      wsgi.py
    apps/
      <app_name>/
        models/
        services/
          usecases/
          domain/
          etl/
        api/
          serializers.py
          viewsets.py
          routers.py
          filters.py
        views/
        forms/
        tasks/
        management/commands/
        tests/
        permissions.py
    shared/
      models/
      services/
      utils/
```

## Model Conventions

```python
# apps/orders/models/order.py
from django.db import models
from shared.models.mixins import TimeStampedMixin

class Order(TimeStampedMixin, models.Model):
    """Order placed by a customer."""
    
    # ForeignKey with explicit related_name
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    
    # Fields: explicit verbose_name
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Order Status",
    )
    
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total Amount",
    )
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
    
    def __str__(self):
        return f"Order {self.id} - {self.customer}"
```

### Naming
- Model names: **singular PascalCase** (`Order`, `Customer`)
- Table names: auto-generated (or explicit `db_table`)
- FK fields: singular noun (`customer`, not `customer_id`)

## Service Conventions

```python
# apps/orders/services/usecases/create_order.py
import logging
from dataclasses import dataclass
from decimal import Decimal
from django.db import transaction

logger = logging.getLogger("apps.orders.usecases")

@dataclass
class CreateOrderResult:
    """Result DTO for order creation."""
    order_id: int
    total: Decimal
    status: str

def create_order(
    customer_id: int,
    items: list[dict],
    user_id: int,
) -> CreateOrderResult:
    """
    Create a new order with items.
    
    Args:
        customer_id: The customer placing the order
        items: List of {product_id, quantity}
        user_id: User performing the action
    
    Returns:
        CreateOrderResult with order details
    
    Raises:
        CustomerNotFoundError: If customer doesn't exist
        InsufficientStockError: If product stock is insufficient
    """
    logger.info("Creating order", extra={"customer_id": customer_id})
    
    with transaction.atomic():
        # Business logic here
        pass
    
    return CreateOrderResult(
        order_id=order.id,
        total=order.total,
        status=order.status,
    )
```

### Rules
- One function per file (for complex use cases)
- Return dataclasses, not dicts
- No `request` object in services
- No HTTP/Response objects in services
- Document with docstrings

## DRF Conventions

### ViewSet
```python
# apps/orders/api/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from apps.orders.services.usecases import create_order
from .serializers import OrderSerializer, OrderCreateSerializer
from .permissions import CanViewOrder

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations.
    
    list: List user's orders
    retrieve: Get order details
    create: Create new order
    """
    queryset = Order.objects.select_related("customer")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CanViewOrder]
    
    def get_queryset(self):
        """Filter to user's orders."""
        return super().get_queryset().filter(
            customer__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel an order."""
        order = self.get_object()
        # Delegate to service
        result = cancel_order(order.id, request.user.id)
        return Response({"status": result.status})
```

### Serializer
```python
# apps/orders/api/serializers.py
from rest_framework import serializers
from apps.orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order read operations."""
    
    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True,
    )
    
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "status",
            "total",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for order creation (use case DTO)."""
    
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
    )
    
    def validate_items(self, value):
        # Validation logic
        return value
```

### Naming
- `<Model>ViewSet`, `<Model>Serializer`
- Multiple serializers: `<Model>ListSerializer`, `<Model>DetailSerializer`, `<Model>CreateSerializer`

## Test Conventions

```python
# apps/orders/tests/test_services.py
import pytest
from decimal import Decimal

from apps.orders.services.usecases.create_order import (
    create_order,
    CreateOrderResult,
)

class TestCreateOrder:
    """Tests for create_order use case."""
    
    @pytest.mark.django_db
    def test_create_order_success(self, customer_factory, product_factory):
        """Should create order with correct total."""
        customer = customer_factory()
        product = product_factory(price=Decimal("10.00"))
        
        result = create_order(
            customer_id=customer.id,
            items=[{"product_id": product.id, "quantity": 2}],
            user_id=1,
        )
        
        assert isinstance(result, CreateOrderResult)
        assert result.total == Decimal("20.00")
    
    @pytest.mark.django_db
    def test_create_order_invalid_customer(self):
        """Should raise error for non-existent customer."""
        with pytest.raises(CustomerNotFoundError):
            create_order(
                customer_id=99999,
                items=[],
                user_id=1,
            )
```

### Naming
- Files: `test_<module>.py`
- Functions: `test_<function>_<scenario>`
- Classes (optional): `Test<Feature>`

## Celery Task Conventions

```python
# apps/orders/tasks/notification_tasks.py
import logging
from celery import shared_task

from apps.orders.services.notifications import send_order_email

logger = logging.getLogger("apps.orders.tasks")

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def send_order_confirmation_task(self, order_id: int):
    """
    Send order confirmation email.
    
    Thin wrapper - delegates to service.
    """
    logger.info("Sending confirmation", extra={"order_id": order_id})
    
    try:
        send_order_email(order_id)
    except Exception as exc:
        logger.error("Failed to send", exc_info=True)
        raise self.retry(exc=exc)
```

### Rules
- Tasks are **thin wrappers**
- Business logic in services
- Use `bind=True` for retry support
- Log start/error

## Permission Conventions

```python
# apps/orders/permissions.py
"""Domain permission policies for orders."""

def can_view_order(user, order) -> bool:
    """Check if user can view this order."""
    if user.is_superuser:
        return True
    return order.customer.user_id == user.id

def can_cancel_order(user, order) -> bool:
    """Check if user can cancel this order."""
    if not can_view_order(user, order):
        return False
    return order.status in ["pending", "confirmed"]
```

```python
# apps/orders/api/permissions.py
"""DRF permission classes wrapping domain policies."""

from rest_framework.permissions import BasePermission
from apps.orders.permissions import can_view_order

class CanViewOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        return can_view_order(request.user, obj)
```

## IDE/Agent Rules Summary

### Where to Create New Code

| Type | Location |
|------|----------|
| Model | `apps/<app>/models/<model>.py` |
| Service (use case) | `apps/<app>/services/usecases/<action>.py` |
| ETL Service | `apps/<app>/services/etl/<job>.py` |
| API Serializer | `apps/<app>/api/serializers.py` |
| API ViewSet | `apps/<app>/api/viewsets.py` |
| Form | `apps/<app>/forms/<context>_forms.py` |
| Celery Task | `apps/<app>/tasks/<domain>_tasks.py` |
| Management Command | `apps/<app>/management/commands/<name>.py` |
| Test | `apps/<app>/tests/test_<module>.py` |

### Never Create Business Logic In

- `config/` (settings, URLs, WSGI only)
- Serializers (validation only)
- Views/ViewSets (I/O orchestration only)
- Celery tasks (thin wrappers only)
- Templates (presentation only)

---

## ✅ DO

- ✅ Follow PEP 8 (enforced by ruff/black)
- ✅ Use type hints in services
- ✅ Document services with docstrings
- ✅ Return dataclasses from services
- ✅ Name loggers as `apps.<app>.<module>`
- ✅ Create tests with every new service
- ✅ Use factories for test data
- ✅ Keep tasks thin (delegate to services)

---

## ❌ DON'T

- ❌ **No business logic in views/serializers**
- ❌ **No `request` in services**
- ❌ **No HTTP responses from services**
- ❌ **No `import *`**
- ❌ **No global `tests/` folder** - tests per app
- ❌ **No mixing concerns** - separate layers
- ❌ **No code without tests** (for services)

---

## Quick Reference for AI Agents

```yaml
Stack: Django 5, DRF, PostgreSQL, Celery, Redis, pytest

Structure:
  - apps/<app>/models/
  - apps/<app>/services/{usecases,domain,etl}/
  - apps/<app>/api/{serializers,viewsets,routers}.py
  - apps/<app>/tasks/
  - apps/<app>/tests/

Conventions:
  - snake_case: functions, variables
  - PascalCase: classes
  - Services: pure logic, return dataclasses
  - Tasks: thin wrappers calling services
  - DRF: IsAuthenticated by default
  - Tests: pytest, one tests/ per app

Tools:
  - ruff: linting
  - black: formatting
  - pytest: testing
  - coverage: code coverage
```
