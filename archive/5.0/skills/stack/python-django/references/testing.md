# Django Testing Reference

## Test Organization

```
apps/<domain>/tests/
├── __init__.py
├── conftest.py         # Fixtures for this app
├── factories.py        # factory_boy factories
├── test_models.py      # Model unit tests
├── test_services.py    # Service layer tests
├── test_api.py         # API integration tests
└── test_views.py       # View tests (if applicable)
```

## pytest Configuration

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

```python
# config/settings/test.py
from .base import *

DEBUG = False

# Fast password hashing for tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# In-memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Faster email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

## Fixtures with factory_boy

### Factory Definitions

```python
# apps/production/tests/factories.py
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.production.models import Campagne, Lot
from django.contrib.auth import get_user_model

fake = Faker('fr_FR')

class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class CampagneFactory(DjangoModelFactory):
    class Meta:
        model = Campagne

    nom = factory.LazyFunction(lambda: f"Campagne {fake.word()}")
    status = 'EN_COURS'
    responsable = factory.SubFactory(UserFactory)

    # Traits for different states
    class Params:
        terminee = factory.Trait(status='TERMINE')
        brouillon = factory.Trait(status='BROUILLON')

class LotFactory(DjangoModelFactory):
    class Meta:
        model = Lot

    code = factory.Sequence(lambda n: f'LOT-{n:05d}')
    quantite = factory.LazyFunction(lambda: fake.pydecimal(min_value=1, max_value=1000))
    campagne = factory.SubFactory(CampagneFactory)
    operateur = factory.SubFactory(UserFactory)
    status = 'BROUILLON'
```

### conftest.py (Shared Fixtures)

```python
# apps/production/tests/conftest.py
import pytest
from rest_framework.test import APIClient

from .factories import UserFactory, CampagneFactory, LotFactory

@pytest.fixture
def user(db):
    """Create a regular user."""
    return UserFactory()

@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return UserFactory(is_staff=True, is_superuser=True)

@pytest.fixture
def campagne(db):
    """Create a campaign."""
    return CampagneFactory()

@pytest.fixture
def campagne_terminee(db):
    """Create a closed campaign."""
    return CampagneFactory(terminee=True)

@pytest.fixture
def lot(db, campagne):
    """Create a lot in default campaign."""
    return LotFactory(campagne=campagne)

@pytest.fixture
def lot_factory(db):
    """Return factory for creating lots."""
    return LotFactory

@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client
```

## Model Tests

```python
# apps/production/tests/test_models.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.production.models import Lot
from .factories import LotFactory, CampagneFactory

@pytest.mark.django_db
class TestLotModel:

    def test_create_lot(self, campagne):
        """Test basic lot creation."""
        lot = Lot.objects.create(
            code='LOT-001',
            quantite=Decimal('100.50'),
            campagne=campagne,
        )

        assert lot.id is not None
        assert lot.code == 'LOT-001'
        assert lot.quantite == Decimal('100.50')
        assert lot.status == 'BROUILLON'

    def test_code_unique_constraint(self, campagne):
        """Test unique code per campaign."""
        LotFactory(code='LOT-001', campagne=campagne)

        with pytest.raises(IntegrityError):
            LotFactory(code='LOT-001', campagne=campagne)

    def test_quantite_must_be_positive(self, campagne):
        """Test positive quantity constraint."""
        lot = Lot(
            code='LOT-001',
            quantite=Decimal('-10'),
            campagne=campagne,
        )

        with pytest.raises(ValidationError):
            lot.full_clean()

    def test_est_conforme_property(self, lot):
        """Test conformity computed property."""
        # No analyses = conforme
        assert lot.est_conforme is True

        # Add failing analysis
        lot.analyses.create(conforme=False, type='VISUEL')
        assert lot.est_conforme is False

    def test_manager_actifs(self, campagne):
        """Test active lots manager."""
        LotFactory.create_batch(3, campagne=campagne, status='BROUILLON')
        LotFactory.create_batch(2, campagne=campagne, status='ARCHIVE')

        assert Lot.objects.actifs().count() == 3

    def test_queryset_avec_relations(self, campagne, user):
        """Test optimized queryset doesn't cause N+1."""
        LotFactory.create_batch(5, campagne=campagne, operateur=user)

        # Should be 1 query (with JOINs)
        lots = list(Lot.objects.avec_relations())

        # Accessing relations should not trigger queries
        for lot in lots:
            _ = lot.campagne.nom
            _ = lot.operateur.email
```

## Service Tests

```python
# apps/production/tests/test_services.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError, PermissionDenied

from apps.production.services.usecases import cloturer_campagne
from apps.production.services.domain.calculs import calculer_bilan
from .factories import CampagneFactory, LotFactory, UserFactory

@pytest.mark.django_db
class TestCloturerCampagne:

    def test_cloturer_campagne_success(self, user):
        """Test successful campaign closure."""
        campagne = CampagneFactory(responsable=user)
        LotFactory.create_batch(3, campagne=campagne, status='VALIDE')

        # Grant permission
        user.user_permissions.add(
            Permission.objects.get(codename='cloturer_campagne')
        )

        result = cloturer_campagne(campagne_id=campagne.id, user=user)

        assert result.campagne.status == 'TERMINE'
        assert result.bilan is not None

    def test_cloturer_campagne_without_permission(self, user):
        """Test closure without permission."""
        campagne = CampagneFactory()

        with pytest.raises(PermissionDenied):
            cloturer_campagne(campagne_id=campagne.id, user=user)

    def test_cloturer_campagne_already_closed(self, user):
        """Test closure of already closed campaign."""
        campagne = CampagneFactory(terminee=True)

        with pytest.raises(ValidationError):
            cloturer_campagne(campagne_id=campagne.id, user=user)

class TestCalculerBilan:
    """Domain service tests - no database needed."""

    def test_calculer_bilan_empty(self):
        """Test bilan with no lots."""
        # Mock campagne with empty lots
        mock_campagne = type('Campagne', (), {
            'lots': type('Manager', (), {'all': lambda: []})()
        })()

        result = calculer_bilan(mock_campagne)

        assert result['quantite_totale'] == Decimal('0')
        assert result['taux_conformite'] == Decimal('0')

    def test_calculer_bilan_mixed(self):
        """Test bilan with conforming and non-conforming lots."""
        lots = [
            type('Lot', (), {'quantite': Decimal('100'), 'est_conforme': True})(),
            type('Lot', (), {'quantite': Decimal('200'), 'est_conforme': True})(),
            type('Lot', (), {'quantite': Decimal('50'), 'est_conforme': False})(),
        ]
        mock_campagne = type('Campagne', (), {
            'lots': type('Manager', (), {'all': lambda: lots})()
        })()

        result = calculer_bilan(mock_campagne)

        assert result['quantite_totale'] == Decimal('350')
        assert result['taux_conformite'] == Decimal('66.67')  # 2/3
```

## API Tests

```python
# apps/production/tests/test_api.py
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .factories import LotFactory, CampagneFactory

@pytest.mark.django_db
class TestLotAPI:

    def test_list_requires_authentication(self, api_client):
        """Test that list endpoint requires auth."""
        response = api_client.get('/api/v1/lots/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_lots_paginated(self, authenticated_client, lot_factory):
        """Test paginated list."""
        lot_factory.create_batch(100)

        response = authenticated_client.get('/api/v1/lots/')

        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.data
        assert 'next' in response.data
        assert response.data['count'] == 100
        assert len(response.data['results']) == 50  # PAGE_SIZE

    def test_list_filter_by_status(self, authenticated_client, lot_factory):
        """Test filtering by status."""
        lot_factory.create_batch(3, status='BROUILLON')
        lot_factory.create_batch(2, status='VALIDE')

        response = authenticated_client.get('/api/v1/lots/?status=VALIDE')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_create_lot(self, authenticated_client, campagne):
        """Test lot creation."""
        data = {
            'code': 'LOT-001',
            'quantite': '100.50',
            'campagne_id': campagne.id,
        }

        response = authenticated_client.post('/api/v1/lots/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['code'] == 'LOT-001'

    def test_create_lot_invalid_code(self, authenticated_client, campagne):
        """Test validation error."""
        data = {
            'code': 'INVALID',  # Must start with LOT-
            'quantite': '100',
            'campagne_id': campagne.id,
        }

        response = authenticated_client.post('/api/v1/lots/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'code' in response.data

    def test_update_lot(self, authenticated_client, lot):
        """Test lot update."""
        response = authenticated_client.patch(
            f'/api/v1/lots/{lot.id}/',
            {'quantite': '200.00'}
        )

        assert response.status_code == status.HTTP_200_OK
        lot.refresh_from_db()
        assert lot.quantite == Decimal('200.00')

    def test_delete_lot(self, authenticated_client, lot):
        """Test lot deletion."""
        response = authenticated_client.delete(f'/api/v1/lots/{lot.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Lot.objects.filter(id=lot.id).exists()

    def test_custom_action_cloturer(self, authenticated_client, lot):
        """Test custom action."""
        response = authenticated_client.post(
            f'/api/v1/lots/{lot.id}/cloturer/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
```

## Coverage Configuration

```ini
# .coveragerc
[run]
source = apps
omit =
    */migrations/*
    */tests/*
    */__pycache__/*
    */management/commands/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:

fail_under = 70
show_missing = True
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app
pytest apps/production/

# Run specific test file
pytest apps/production/tests/test_services.py

# Run specific test
pytest apps/production/tests/test_services.py::TestCloturerCampagne::test_success

# Run marked tests
pytest -m slow
pytest -m "not slow"

# Parallel execution
pytest -n auto

# Verbose with output
pytest -v -s
```

## Test Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Fixtures | Use factory_boy | Manual object creation |
| Database | Use `@pytest.mark.django_db` | TestCase classes |
| Isolation | Clean state per test | Shared mutable state |
| Assertions | Specific assertions | Generic `assert True` |
| Naming | `test_<action>_<condition>` | Vague names |
| Coverage | Focus on services (80%+) | 100% coverage everywhere |
