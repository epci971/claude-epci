---
paths:
  - backend/**/api/**/*.py
  - backend/**/serializers.py
  - backend/**/viewsets.py
---

# Django REST Framework Rules

> Conventions pour les APIs REST avec DRF.

## 🔴 CRITICAL

1. **Jamais d'entites dans les reponses**: Toujours utiliser des Serializers
2. **Validation dans serializers**: Pas dans les views
3. **Permissions explicites**: `permission_classes` sur chaque ViewSet

## 🟡 CONVENTIONS

### Serializers Read/Write

```python
class OrderReadSerializer(serializers.ModelSerializer):
    """Pour GET - relations expandees."""
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total', 'status']


class OrderWriteSerializer(serializers.ModelSerializer):
    """Pour POST/PUT - IDs uniquement."""
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user'
    )

    class Meta:
        model = Order
        fields = ['user_id', 'items']
```

### ViewSet Pattern

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderWriteSerializer
        return OrderReadSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('user')
```

### URL Structure

```
/api/v1/orders/           # List, Create
/api/v1/orders/{id}/      # Retrieve, Update, Delete
/api/v1/orders/{id}/items/ # Nested resource
```

## 🟢 PREFERENCES

- Utiliser `@action` pour actions custom
- Pagination par defaut (PageNumberPagination)
- Filtres via django-filter

## Quick Reference

| Task | Pattern |
|------|---------|
| Read serializer | Expand relations, read_only |
| Write serializer | PrimaryKeyRelatedField |
| Permissions | `permission_classes = [...]` |
| Filters | `filterset_class = OrderFilter` |
| Custom action | `@action(detail=True, methods=['post'])` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Read/Write split | Separate serializers | Clean API |
| Nested routes | drf-nested-routers | REST compliant |
| Bulk operations | Custom action | Performance |
| Versioning | URL prefix `/api/v1/` | Backward compat |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Model in response | Coupling, security | Serializers |
| No pagination | Memory issues | Default pagination |
| Permissions in view logic | Scattered | permission_classes |
| N+1 in serializers | Slow API | select_related in queryset |

## Examples

### Correct

```python
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrderOwner]
    filterset_class = OrderFilter
    pagination_class = StandardPagination

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).select_related('user').prefetch_related('items')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderWriteSerializer
        return OrderReadSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        cancel_order(order.id)
        return Response({'status': 'cancelled'})
```

### Incorrect

```python
# DON'T DO THIS
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # No filtering!
    serializer_class = OrderSerializer  # Same for read/write!
    # No permissions!

    def create(self, request):
        # Validation in view - BAD
        if not request.data.get('items'):
            return Response({'error': 'No items'}, status=400)
        # ...
```
