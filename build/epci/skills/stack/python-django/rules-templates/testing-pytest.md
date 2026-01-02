---
paths:
  - backend/**/tests/**/*.py
  - backend/**/test_*.py
  - backend/**/*_test.py
---

# Pytest Testing Rules

> Conventions pour les tests Python avec pytest.

## 🔴 CRITICAL

1. **Marker django_db obligatoire**: `@pytest.mark.django_db` pour acces DB
2. **Pas de donnees de prod**: Utiliser factories, jamais de vraies donnees
3. **Tests isoles**: Chaque test independant, pas d'ordre requis

## 🟡 CONVENTIONS

### Structure

```
backend/
└── apps/
    └── orders/
        └── tests/
            ├── conftest.py      # Fixtures locales
            ├── test_models.py
            ├── test_services.py
            ├── test_api.py
            └── factories.py     # Factory Boy
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Fichiers | `test_*.py` | `test_orders.py` |
| Classes | `Test*` | `TestOrderService` |
| Methodes | `test_*` | `test_create_order_success` |
| Fixtures | snake_case | `authenticated_client` |

### Pattern AAA

```python
def test_create_order_success(user, order_data):
    # Arrange
    service = OrderService()

    # Act
    order = service.create(user, order_data)

    # Assert
    assert order.status == 'pending'
    assert order.user == user
```

## 🟢 PREFERENCES

- Preferer `pytest.raises` a try/except
- Utiliser `freezegun` pour les dates
- Mocker les services externes

## Quick Reference

| Task | Pattern |
|------|---------|
| Test avec DB | `@pytest.mark.django_db` |
| Factory | `OrderFactory.create()` |
| API client | `api_client.post('/api/...')` |
| Mock external | `@patch('apps.orders.services.external_api')` |
| Parametrize | `@pytest.mark.parametrize('input,expected', [...])` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Factory Boy | `OrderFactory.create(status='paid')` | Donnees realistes |
| Fixtures | `@pytest.fixture` in conftest.py | Reutilisation |
| Parametrize | `@pytest.mark.parametrize` | Coverage exhaustive |
| Freeze time | `@freeze_time('2024-01-01')` | Tests deterministes |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Hardcoded IDs | Fragile | Factories |
| Sleep in tests | Slow, flaky | Mock time |
| Test order dependency | Fragile | Isolated tests |
| No assertions | Useless test | Assert something |

## Examples

### Correct

```python
@pytest.mark.django_db
class TestOrderService:
    def test_create_order_success(self, user):
        # Arrange
        items = [{"product_id": 1, "quantity": 2}]

        # Act
        order = create_order(user.id, items)

        # Assert
        assert order.status == 'pending'
        assert order.items.count() == 1

    def test_create_order_empty_items_fails(self, user):
        with pytest.raises(ValidationError):
            create_order(user.id, [])
```

### Incorrect

```python
# DON'T DO THIS
def test_order():
    user = User.objects.get(id=1)  # Hardcoded ID!
    order = Order.objects.create(user=user)
    # No assertion!
```
