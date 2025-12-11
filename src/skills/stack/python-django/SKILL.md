---
name: python-django
description: >-
  Patterns and conventions for Python/Django. Includes Django REST Framework,
  pytest, models, views, serializers. Use when: Django development,
  requirements.txt with django detected. Not for: Flask, FastAPI, plain Python.
---

# Python/Django Development Patterns

## Overview

Patterns and conventions for modern Django development.

## Auto-detection

Automatically loaded if detection of:
- `requirements.txt` or `pyproject.toml` containing `django`
- Files `manage.py`, `settings.py`
- Structure `apps/`, `models.py`, `views.py`

## Django Architecture

### Standard Structure

```
project/
├── config/                # Project configuration
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                  # Django applications
│   └── users/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
│       ├── admin.py
│       └── tests/
│           ├── test_models.py
│           └── test_views.py
├── core/                  # Shared code
│   ├── models.py         # Base models
│   └── permissions.py
├── tests/
├── manage.py
├── requirements.txt
└── pyproject.toml
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Apps | snake_case, plural | `users`, `blog_posts` |
| Models | PascalCase, singular | `User`, `BlogPost` |
| Views | `*View` or `*ViewSet` | `UserDetailView` |
| Serializers | `*Serializer` | `UserSerializer` |
| URLs | kebab-case | `user-detail` |
| Tests | `test_*.py` | `test_models.py` |

## Model Patterns

### Base Model

```python
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampedModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email

    @property
    def display_name(self) -> str:
        return self.name or self.email.split('@')[0]
```

### Manager and QuerySet

```python
class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def by_email(self, email: str):
        return self.filter(email__iexact=email)


class UserManager(models.Manager):
    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def create_user(self, email: str, password: str, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
```

## Django REST Framework Patterns

### Serializer

```python
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'display_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
```

### ViewSet

```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        return User.objects.active()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### URLs

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

## Testing Patterns (pytest)

### Model Test

```python
import pytest
from django.core.exceptions import ValidationError
from apps.users.models import User


@pytest.mark.django_db
class TestUser:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='securepassword'
        )

        assert user.email == 'test@example.com'
        assert user.check_password('securepassword')
        assert user.is_active

    def test_email_must_be_unique(self):
        User.objects.create_user(email='test@example.com', password='pass')

        with pytest.raises(Exception):
            User.objects.create_user(email='test@example.com', password='pass')

    def test_display_name_returns_name_if_set(self):
        user = User(email='test@example.com', name='John Doe')
        assert user.display_name == 'John Doe'

    def test_display_name_returns_email_prefix_if_no_name(self):
        user = User(email='test@example.com')
        assert user.display_name == 'test'
```

### API Test

```python
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestUserAPI:
    def test_list_users_requires_auth(self, api_client):
        response = api_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_authenticated(self, authenticated_client):
        response = authenticated_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self, api_client):
        data = {
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'securepass123'
        }
        response = api_client.post('/api/v1/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'new@example.com'
```

### Fixtures (conftest.py)

```python
import pytest
from apps.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpassword',
        name='Test User'
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword'
    )
```

## Useful Commands

```bash
# Development
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Shell and debug
python manage.py shell_plus  # django-extensions
python manage.py dbshell

# Tests
pytest
pytest -v
pytest --cov=apps
pytest apps/users/tests/test_models.py

# Quality
ruff check .
mypy .
black .
```

## Django Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Models | Fat models, thin views | Logic in views |
| Queries | select_related/prefetch | N+1 queries |
| Settings | Environment variables | Hardcoded secrets |
| Tests | pytest + factories | Verbose setUp |
| Serializers | Separate per action | Single serializer |

## Django Security

```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# DRF Permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```

## pytest Configuration

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_*.py
addopts = -v --tb=short
```
