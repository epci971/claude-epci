# Django Tests & Software Quality Rules

## Test Pyramid

```
                    ┌─────────────┐
                    │   E2E/UI    │  ~10%
                    │  (Cypress)  │
                 ┌──┴─────────────┴──┐
                 │   Integration     │  ~20-30%
                 │  (API, ORM, ETL)  │
              ┌──┴───────────────────┴──┐
              │      Unit Tests         │  ~60-70%
              │  (Services, Utils)      │
              └─────────────────────────┘
```

**Focus**: Test services and API heavily. Don't test everything via UI.

## Test Stack

- **pytest** + **pytest-django**: Modern test framework
- **factory_boy** or **model_bakery**: Model factories
- **APIClient** (DRF): API endpoint testing
- **coverage.py**: Code coverage measurement
- **ruff** + **black**: Linting and formatting

## Test Directory Structure

```
apps/
  <app_name>/
    tests/
      __init__.py
      conftest.py           # Fixtures for this app
      factories.py          # Model factories
      test_models.py        # Model tests
      test_services.py      # Service/use case tests
      test_api.py           # DRF endpoint tests
      test_forms.py         # Form validation tests
      test_tasks.py         # Celery task tests
      test_etl.py           # ETL service tests

shared/
  tests/
    conftest.py             # Global fixtures
    test_utils.py
```

## Unit Tests: Services

### Service Test Example
```python
# apps/orders/tests/test_services.py
import pytest
from decimal import Decimal
from apps.orders.services.usecases.calculate_total import (
    calculate_order_total,
    OrderTotalResult,
)

@pytest.mark.django_db
def test_calculate_order_total_basic(order_factory, product_factory):
    product = product_factory(price=Decimal("10.00"))
    order = order_factory(items=[{"product": product, "quantity": 3}])
    
    result = calculate_order_total(order)
    
    assert isinstance(result, OrderTotalResult)
    assert result.subtotal == Decimal("30.00")
    assert result.tax == Decimal("6.00")  # 20% tax
    assert result.total == Decimal("36.00")


def test_calculate_order_total_empty_order():
    """Test without DB - pure logic."""
    from unittest.mock import Mock
    
    order = Mock()
    order.items.all.return_value = []
    
    result = calculate_order_total(order)
    
    assert result.total == Decimal("0.00")
```

## Integration Tests: API

### DRF API Test Example
```python
# apps/orders/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user


class TestOrderAPI:
    
    @pytest.mark.django_db
    def test_list_orders_requires_auth(self, api_client):
        response = api_client.get("/api/v1/orders/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.django_db
    def test_list_orders_returns_user_orders(
        self, authenticated_client, order_factory
    ):
        client, user = authenticated_client
        order = order_factory(user=user)
        order_factory()  # Other user's order
        
        response = client.get("/api/v1/orders/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["results"]) == 1
        assert response.json()["results"][0]["id"] == str(order.id)
    
    @pytest.mark.django_db
    def test_create_order_success(self, authenticated_client, product_factory):
        client, user = authenticated_client
        product = product_factory()
        
        response = client.post("/api/v1/orders/", {
            "items": [{"product_id": product.id, "quantity": 2}]
        }, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()
```

## Form Tests

```python
# apps/orders/tests/test_forms.py
from apps.orders.forms import OrderCreateForm

def test_order_form_invalid_dates():
    form = OrderCreateForm(data={
        "delivery_date": "2024-01-01",
        "order_date": "2024-01-15",  # After delivery
    })
    
    assert not form.is_valid()
    assert "__all__" in form.errors  # Non-field error


def test_order_form_valid():
    form = OrderCreateForm(data={
        "delivery_date": "2024-01-15",
        "order_date": "2024-01-01",
        "quantity": 5,
    })
    
    assert form.is_valid()
```

## ETL & Task Tests

### ETL Service Test
```python
# apps/labo/tests/test_etl.py
import pytest
from pathlib import Path
from apps.labo.services.etl.import_file import import_labo_file

@pytest.fixture
def sample_csv(tmp_path):
    csv_content = "id,name,value\n1,Test,100\n2,Test2,200"
    file_path = tmp_path / "sample.csv"
    file_path.write_text(csv_content)
    return file_path

@pytest.mark.django_db
def test_import_labo_file_success(sample_csv):
    result = import_labo_file(sample_csv)
    
    assert result.rows_read == 2
    assert result.rows_imported == 2
    assert result.errors == 0


@pytest.mark.django_db
def test_import_labo_file_idempotent(sample_csv):
    """Running twice should not duplicate data."""
    import_labo_file(sample_csv)
    result = import_labo_file(sample_csv)
    
    assert result.rows_imported == 2  # Updated, not duplicated
```

### Celery Task Test
```python
# apps/labo/tests/test_tasks.py
from unittest.mock import patch

def test_import_task_calls_service():
    with patch("apps.labo.tasks.etl_tasks.import_labo_file") as mock_import:
        mock_import.return_value = {"rows_imported": 10}
        
        from apps.labo.tasks.etl_tasks import import_labo_file_task
        result = import_labo_file_task("/path/to/file.csv", user_id=1)
        
        mock_import.assert_called_once_with(
            Path("/path/to/file.csv"), 1
        )
```

### Management Command Test
```python
# apps/labo/tests/test_commands.py
from django.core.management import call_command
from unittest.mock import patch

def test_import_daily_command(mocker):
    mock_import = mocker.patch(
        "apps.labo.management.commands.import_daily.import_labo_file"
    )
    
    call_command("import_daily", "--source=/data/file.csv", "--force")
    
    mock_import.assert_called_once()
```

## Factories (factory_boy)

```python
# apps/orders/tests/factories.py
import factory
from factory.django import DjangoModelFactory
from apps.orders.models import Order, OrderItem
from apps.accounts.tests.factories import UserFactory

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    status = "pending"
    
    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item_data in extracted:
                OrderItemFactory(order=self, **item_data)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem
    
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory("apps.products.tests.factories.ProductFactory")
    quantity = 1
```

## Coverage Configuration

```ini
# pyproject.toml or .coveragerc
[tool.coverage.run]
source = ["apps", "shared"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "config/*",
    "manage.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 70
```

## Quality Tools Configuration

### pyproject.toml
```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # Line length handled by black

[tool.black]
line-length = 88
target-version = ["py312"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-v --tb=short"
```

## CI Pipeline Commands

```bash
# Lint
ruff check .
black --check .

# Tests
pytest --maxfail=3 -q

# Coverage
coverage run -m pytest
coverage report --fail-under=70
coverage xml  # For CI integration

# Django checks
python manage.py check
python manage.py check --deploy --settings=config.settings.prod
```

---

## ✅ DO

- ✅ One `tests/` directory per app with files by type
- ✅ Test services with unit tests (mock DB when possible)
- ✅ Test API endpoints with `APIClient`
- ✅ Use `@pytest.mark.django_db` only when DB access needed
- ✅ Use factories for model creation (`factory_boy`)
- ✅ Test ETL services with sample files
- ✅ Test Celery tasks as function calls (mock the service)
- ✅ Measure coverage with targets: 80%+ on services
- ✅ Run `manage.py check` in CI

---

## ❌ DON'T

- ❌ **No single global tests folder** - tests per app
- ❌ **No testing everything via UI/E2E** - unit test services
- ❌ **No skipping tests for "simple" code**
- ❌ **No hardcoded test data** - use factories
- ❌ **No testing implementation details** - test behavior
- ❌ **No ignoring failing tests** - fix or remove

---

## Coverage Targets

| Layer | Target | Priority |
|-------|--------|----------|
| Services (usecases, domain) | **80%+** | High |
| ETL services | **80%+** | High |
| API endpoints | **70%+** | High |
| Forms | **60%+** | Medium |
| Views (HTML) | **50%+** | Low |
| Overall project | **70%+** | - |

---

## Checklist

### Organization
- [ ] Each app has `tests/` with `test_models.py`, `test_services.py`, `test_api.py`
- [ ] Business services and ETL have dedicated tests
- [ ] Fixtures/factories in `conftest.py` and `factories.py`

### Backend Tests
- [ ] `pytest` + `pytest-django` used
- [ ] `APIClient` for DRF endpoint tests
- [ ] Forms tested on validation rules
- [ ] Management commands tested (at least happy path)

### Async & ETL
- [ ] Celery tasks tested as thin wrappers
- [ ] ETL services tested with sample files
- [ ] Idempotency tested (run twice, no duplicates)

### Quality
- [ ] Lint (ruff) and format (black) in CI
- [ ] Coverage measured with minimum threshold
- [ ] `manage.py check` and `check --deploy` run regularly
