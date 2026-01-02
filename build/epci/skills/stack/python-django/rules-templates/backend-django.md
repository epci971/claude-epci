---
paths:
  - backend/**/*.py
  - "!backend/**/migrations/**"
  - "!backend/**/tests/**"
---

# Django Backend Rules

> Conventions pour le developpement Python/Django.

## 🔴 CRITICAL

1. **Pas de logique dans les views**: Les views delegent aux services
2. **Pas de N+1 queries**: Toujours utiliser `select_related`/`prefetch_related`
3. **Pas de secrets hardcodes**: Utiliser `env('SECRET')` ou django-environ
4. **Migrations versionnees**: Jamais de `--fake`, toujours commiter

## 🟡 CONVENTIONS

### Architecture

- Services dans `services/` (usecases, domain, integrations)
- Un model par fichier dans `models/`
- Serializers miroir des models
- Permissions dans `permissions.py` par app

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Models | Singular, PascalCase | `User`, `Order` |
| Views | Descriptive + View/ViewSet | `UserViewSet` |
| Services | Action + Service | `CreateOrderService` |
| Serializers | Model + Serializer | `OrderSerializer` |

### Imports

```python
# Order: stdlib, django, third-party, local
from datetime import datetime

from django.db import models
from rest_framework import serializers

from apps.core.models import BaseModel
```

## 🟢 PREFERENCES

- Preferer les class-based views pour CRUD
- Utiliser `@transaction.atomic` pour multi-model ops
- Type hints sur toutes les fonctions publiques

## Quick Reference

| Task | Pattern |
|------|---------|
| Business logic | `services/usecases/` |
| Pure calculations | `services/domain/` |
| External APIs | `services/integrations/` |
| FK access | `select_related()` |
| M2M/Reverse FK | `prefetch_related()` |
| Bulk insert | `bulk_create(batch_size=1000)` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Service Layer | `services/usecases/action.py` | Testable, reutilisable |
| Repository | Custom QuerySet methods | Queries encapsulees |
| DTO | Dataclass ou Pydantic | Validation typee |
| Events | Django signals sparingly | Decouplage |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Fat views | SRP viole, hard to test | Service layer |
| Fat models | Coupling, testing issues | Domain services |
| N+1 queries | Performance disaster | select/prefetch_related |
| FloatField for money | Precision loss | DecimalField |
| Logic in signals | Hard to debug | Explicit service calls |

## Examples

### Correct

```python
# services/usecases/create_order.py
from django.db import transaction

@transaction.atomic
def create_order(user_id: int, items: list[dict]) -> Order:
    """Use case: create order with items."""
    user = User.objects.get(id=user_id)
    order = Order.objects.create(user=user, status='pending')

    OrderItem.objects.bulk_create([
        OrderItem(order=order, **item) for item in items
    ])

    notify_order_created.delay(order.id)
    return order
```

### Incorrect

```python
# views.py - DON'T DO THIS
class OrderViewSet(ViewSet):
    def create(self, request):
        # Business logic in view - BAD
        order = Order.objects.create(user=request.user)
        for item in request.data['items']:
            OrderItem.objects.create(order=order, **item)  # N+1!
        send_email(...)  # Side effect in view - BAD
        return Response(OrderSerializer(order).data)
```
