# Django REST Framework Reference

## API Structure

```
apps/<domain>/api/
├── __init__.py
├── serializers.py    # All serializers
├── viewsets.py       # All viewsets
├── routers.py        # Router configuration
├── filters.py        # Custom filters
├── permissions.py    # API permissions
└── urls.py           # API URL patterns
```

## Serializer Patterns

### Read/Write Separation

```python
# apps/production/api/serializers.py
from rest_framework import serializers
from apps.production.models import Lot, Campagne

# READ serializer - rich, nested data
class LotReadSerializer(serializers.ModelSerializer):
    """Serializer for reading lot data (list/retrieve)."""

    campagne = CampagneMinimalSerializer(read_only=True)
    operateur = UserMinimalSerializer(read_only=True)
    est_conforme = serializers.BooleanField(read_only=True)

    class Meta:
        model = Lot
        fields = [
            'id', 'code', 'quantite', 'status',
            'campagne', 'operateur', 'est_conforme',
            'created_at', 'updated_at',
        ]

# WRITE serializer - flat, IDs only
class LotWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating lots."""

    campagne_id = serializers.PrimaryKeyRelatedField(
        queryset=Campagne.objects.actives(),
        source='campagne',
    )

    class Meta:
        model = Lot
        fields = ['code', 'quantite', 'campagne_id']

    def validate_code(self, value):
        """Custom field validation."""
        if not value.startswith('LOT-'):
            raise serializers.ValidationError(
                "Code must start with 'LOT-'"
            )
        return value

    def validate(self, attrs):
        """Cross-field validation."""
        campagne = attrs.get('campagne')
        if campagne and campagne.status == 'TERMINE':
            raise serializers.ValidationError(
                "Cannot add lots to closed campaigns"
            )
        return attrs
```

### Nested Serializers

```python
# Minimal serializers for nesting (avoid circular imports)
class CampagneMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagne
        fields = ['id', 'nom', 'status']

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Deep nested for detailed views
class CampagneDetailSerializer(serializers.ModelSerializer):
    lots = LotReadSerializer(many=True, read_only=True)
    responsable = UserMinimalSerializer(read_only=True)

    # Computed fields via annotations
    nombre_lots = serializers.IntegerField(read_only=True)
    quantite_totale = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Campagne
        fields = [
            'id', 'nom', 'status', 'responsable',
            'lots', 'nombre_lots', 'quantite_totale',
            'created_at', 'updated_at',
        ]
```

### Use Case Serializers (Non-Model)

```python
# For service layer DTOs
class CloturerCampagneInputSerializer(serializers.Serializer):
    """Input for cloturer_campagne use case."""

    commentaire = serializers.CharField(required=False, allow_blank=True)
    forcer = serializers.BooleanField(default=False)

class CloturerCampagneOutputSerializer(serializers.Serializer):
    """Output from cloturer_campagne use case."""

    campagne_id = serializers.IntegerField()
    bilan_id = serializers.IntegerField()
    message = serializers.CharField()
```

## ViewSet Patterns

### Standard ModelViewSet

```python
# apps/production/api/viewsets.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.production.models import Lot
from apps.production.api.serializers import (
    LotReadSerializer, LotWriteSerializer
)
from apps.production.api.filters import LotFilter
from apps.production.services.usecases import cloturer_lot

class LotViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lots.

    list: List all lots (paginated)
    retrieve: Get single lot
    create: Create new lot
    update: Full update
    partial_update: Partial update
    destroy: Delete lot
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = LotFilter
    ordering_fields = ['created_at', 'code', 'quantite']
    ordering = ['-created_at']

    def get_queryset(self):
        """Optimized queryset with relations."""
        return Lot.objects.select_related('campagne', 'operateur')\
                          .prefetch_related('analyses')

    def get_serializer_class(self):
        """Different serializers for read/write."""
        if self.action in ['create', 'update', 'partial_update']:
            return LotWriteSerializer
        return LotReadSerializer

    def perform_create(self, serializer):
        """Set operateur on creation."""
        serializer.save(operateur=self.request.user)

    # Custom actions
    @action(detail=True, methods=['post'])
    def cloturer(self, request, pk=None):
        """Close a lot (custom action)."""
        lot = self.get_object()

        try:
            result = cloturer_lot(lot_id=lot.id, user=request.user)
            return Response({
                'status': 'success',
                'message': f'Lot {lot.code} closed',
            })
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Get lot statistics (list action)."""
        qs = self.get_queryset()
        stats = {
            'total': qs.count(),
            'par_status': dict(
                qs.values('status').annotate(count=Count('id'))
            ),
        }
        return Response(stats)
```

### Read-Only ViewSet

```python
class CampagnePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only access to campaigns."""

    queryset = Campagne.objects.filter(public=True)
    serializer_class = CampagneMinimalSerializer
    permission_classes = [permissions.AllowAny]
```

## Filtering & Pagination

### Custom Filters

```python
# apps/production/api/filters.py
import django_filters
from apps.production.models import Lot

class LotFilter(django_filters.FilterSet):
    """Filter for Lot API."""

    # Range filters
    quantite_min = django_filters.NumberFilter(
        field_name='quantite', lookup_expr='gte'
    )
    quantite_max = django_filters.NumberFilter(
        field_name='quantite', lookup_expr='lte'
    )

    # Date filters
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    # Related field filter
    campagne = django_filters.NumberFilter(field_name='campagne_id')

    # Search
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Lot
        fields = ['status', 'campagne']

    def filter_search(self, queryset, name, value):
        """Full-text search on code."""
        return queryset.filter(code__icontains=value)
```

### Pagination

```python
# config/settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# Custom pagination
# apps/production/api/pagination.py
from rest_framework.pagination import PageNumberPagination

class LargePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500

# Usage in ViewSet
class LotViewSet(viewsets.ModelViewSet):
    pagination_class = LargePagination
```

## Permissions

### Custom Permissions

```python
# apps/production/api/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission: owner can edit, others read-only."""

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner
        return obj.operateur == request.user

class CanCloseCampaign(permissions.BasePermission):
    """Check Django permission for closing campaigns."""

    def has_permission(self, request, view):
        return request.user.has_perm('production.cloturer_campagne')

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('production.cloturer_campagne', obj)
```

### Permission in ViewSet

```python
class LotViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        """Different permissions per action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        if self.action == 'cloturer':
            return [CanCloseLot()]
        return [permissions.IsAuthenticated()]
```

## Router Configuration

```python
# apps/production/api/routers.py
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'lots', viewsets.LotViewSet, basename='lot')
router.register(r'campagnes', viewsets.CampagneViewSet, basename='campagne')

# apps/production/api/urls.py
from django.urls import path, include
from .routers import router

urlpatterns = [
    path('', include(router.urls)),
]
```

## Authentication

### JWT Configuration

```python
# config/settings/base.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

### Auth URLs

```python
# config/urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Error Handling

```python
# apps/shared/api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler with logging."""

    response = exception_handler(exc, context)

    if response is None:
        # Unhandled exception
        logger.exception("Unhandled API exception", exc_info=exc)
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Add error code for frontend
    response.data['error_code'] = exc.__class__.__name__

    return response
```

## API Versioning

```python
# config/urls.py
urlpatterns = [
    path('api/v1/', include('apps.production.api.urls')),
    path('api/v2/', include('apps.production.api.v2.urls')),  # Future version
]
```

## Testing APIs

```python
# apps/production/tests/test_api.py
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
class TestLotAPI:

    def test_list_requires_auth(self, api_client):
        response = api_client.get('/api/v1/lots/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_lots(self, authenticated_client, lot_factory):
        lot_factory.create_batch(5)

        response = authenticated_client.get('/api/v1/lots/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 5

    def test_create_lot(self, authenticated_client, campagne):
        data = {
            'code': 'LOT-001',
            'quantite': '100.50',
            'campagne_id': campagne.id,
        }

        response = authenticated_client.post('/api/v1/lots/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['code'] == 'LOT-001'

    def test_cloturer_action(self, authenticated_client, lot):
        response = authenticated_client.post(
            f'/api/v1/lots/{lot.id}/cloturer/'
        )

        assert response.status_code == status.HTTP_200_OK
```
