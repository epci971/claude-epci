# Django Security & Compliance Rules

## Defense in Depth Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Secure Configuration                          │
│  └── Settings, deployment, check --deploy               │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Authentication & Sessions                     │
│  └── Django auth, DRF auth, password policies           │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Authorization & Access Control                │
│  └── Permissions, roles, domain policies                │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Input Validation & Output Encoding            │
│  └── CSRF, XSS prevention, SQL injection protection     │
├─────────────────────────────────────────────────────────┤
│  Layer 5: Logging & Audit                               │
│  └── Security events, action trails, monitoring         │
└─────────────────────────────────────────────────────────┘
```

## OWASP Top 10 Coverage

| OWASP Risk | Django Protection |
|------------|-------------------|
| A01: Broken Access Control | Permissions, decorators, policies |
| A02: Cryptographic Failures | Secure cookies, HTTPS, hashing |
| A03: Injection | ORM parameterization, template escaping |
| A05: Security Misconfiguration | check --deploy, secure defaults |
| A07: XSS | Auto-escaping, no `\|safe` on user input |

## Production Settings Checklist

```python
# config/settings/prod.py
DEBUG = False
ALLOWED_HOSTS = ["app.example.com"]
SECRET_KEY = env("DJANGO_SECRET_KEY")  # From environment

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF
CSRF_TRUSTED_ORIGINS = ["https://app.example.com"]
```

### Deployment Verification
```bash
# Run before EVERY production deployment
python manage.py check --deploy --settings=config.settings.prod
```

## Authentication

### Django Auth (Backoffice)
```python
# config/settings/base.py
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
```

### DRF Authentication
```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

## Authorization & Permissions

### Domain Permission Policy
```python
# apps/items/permissions.py
def can_view_item(user, item) -> bool:
    if user.is_superuser:
        return True
    return item.organization_id == user.organization_id

def can_edit_item(user, item) -> bool:
    if not can_view_item(user, item):
        return False
    return user.has_perm("items.change_item")

def can_delete_item(user, item) -> bool:
    if not can_view_item(user, item):
        return False
    return user.has_perm("items.delete_item") or item.created_by_id == user.id
```

### DRF Permission Class
```python
# apps/items/api/permissions.py
from rest_framework.permissions import BasePermission
from apps.items.permissions import can_view_item, can_edit_item

class ItemObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return can_view_item(request.user, obj)
        return can_edit_item(request.user, obj)
```

### View-Level Protection
```python
# Django CBV
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "items.change_item"
    model = Item
    
    def get_queryset(self):
        # Filter to user's organization
        return super().get_queryset().filter(
            organization=self.request.user.organization
        )
```

## Throttling (Rate Limiting)

```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}
```

### Custom Throttle for Sensitive Endpoints
```python
from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    rate = "5/minute"

class ExportRateThrottle(UserRateThrottle):
    rate = "10/hour"
```

## CSRF Protection

### Templates (Required)
```django
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Submit</button>
</form>
```

### AJAX/HTMX Requests
```javascript
// Include CSRF token in AJAX headers
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
});
```

### HTMX Configuration
```django
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

## SQL Injection Prevention

### ✅ Safe: Use ORM
```python
# Parameterized queries - SAFE
Item.objects.filter(name=user_input)
Item.objects.filter(Q(name__icontains=search_term))
Item.objects.annotate(total=Sum("amount"))
```

### ❌ Dangerous: Raw SQL
```python
# NEVER do this
Item.objects.raw(f"SELECT * FROM items WHERE name = '{user_input}'")

# If raw SQL is absolutely necessary, use params
Item.objects.raw("SELECT * FROM items WHERE name = %s", [user_input])
```

## XSS Prevention

### Templates - Auto-Escaping (Default)
```django
{# Safe - auto-escaped #}
{{ user_comment }}

{# Output: &lt;script&gt;alert('xss')&lt;/script&gt; #}
```

### ❌ Dangerous: `|safe` Filter
```django
{# NEVER on user input #}
{{ user_comment|safe }}  {# XSS vulnerability! #}

{# Only for trusted, sanitized content #}
{{ sanitized_html|safe }}
```

### React - Avoid dangerouslySetInnerHTML
```tsx
// AVOID - XSS risk
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// SAFE - escaped by default
<div>{userContent}</div>
```

## Sensitive Data Handling

### Password Storage (Automatic)
```python
# Django handles hashing automatically
user.set_password("plaintext_password")  # Stored as hash
user.check_password("plaintext_password")  # Verified against hash
```

### API Tokens & Secrets
```python
# NEVER store in code or database
API_KEY = env("EXTERNAL_API_KEY")  # From environment

# If must store, use encryption
from cryptography.fernet import Fernet
cipher = Fernet(env("ENCRYPTION_KEY"))
encrypted = cipher.encrypt(sensitive_data.encode())
```

### Minimize Data Collection
```python
# Collect only necessary fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Only store what's needed
    timezone = models.CharField(max_length=50)
    # DON'T store: SSN, full DOB, etc. unless required
```

## Logging & Audit

### Security Logger Configuration
```python
# config/settings/base.py
LOGGING = {
    "version": 1,
    "handlers": {
        "security": {
            "class": "logging.FileHandler",
            "filename": "/var/log/app/security.log",
            "formatter": "json",
        },
    },
    "loggers": {
        "apps.security": {
            "handlers": ["security"],
            "level": "INFO",
        },
    },
}
```

### Security Event Logging
```python
# apps/accounts/views.py
import logging

security_logger = logging.getLogger("apps.security")

def login_view(request):
    if form.is_valid():
        user = authenticate(...)
        if user:
            login(request, user)
            security_logger.info(
                "login_success",
                extra={"user_id": user.id, "ip": get_client_ip(request)}
            )
        else:
            security_logger.warning(
                "login_failed",
                extra={"username": form.cleaned_data["username"], "ip": get_client_ip(request)}
            )
```

### Audit Trail for Sensitive Actions
```python
# apps/items/services/usecases/delete_item.py
import logging

audit_logger = logging.getLogger("apps.audit")

def delete_item(item_id: int, user) -> None:
    item = Item.objects.get(id=item_id)
    
    audit_logger.info(
        "item_deleted",
        extra={
            "item_id": item.id,
            "item_name": item.name,
            "user_id": user.id,
            "user_email": user.email,
        }
    )
    
    item.delete()
```

## CORS Configuration

```python
# config/settings/prod.py
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

# Strict origin list - no wildcards
CORS_ALLOWED_ORIGINS = [
    "https://frontend.example.com",
]

# Or for same-origin only
CORS_ALLOW_ALL_ORIGINS = False
```

---

## ✅ DO

- ✅ Run `check --deploy` before every production deployment
- ✅ Enable all security headers in production
- ✅ Use environment variables for all secrets
- ✅ Centralize permissions in domain policy functions
- ✅ Use `{% csrf_token %}` in all POST forms
- ✅ Use ORM for all database queries (parameterized)
- ✅ Let Django auto-escape template variables
- ✅ Implement rate limiting for authentication endpoints
- ✅ Log security events (login success/failure, sensitive actions)
- ✅ Keep dependencies updated (security patches)

---

## ❌ DON'T

- ❌ **No DEBUG=True in production**
- ❌ **No secrets in Git** - environment variables only
- ❌ **No @csrf_exempt on backoffice views**
- ❌ **No raw SQL with string concatenation**
- ❌ **No `|safe` on user input** - XSS vulnerability
- ❌ **No wildcard CORS origins (`*`) in production**
- ❌ **No disabled CsrfViewMiddleware**
- ❌ **No public endpoints without explicit throttling**
- ❌ **No storing plain-text passwords or tokens**

---

## Checklist

### Configuration & Deployment
- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] `SECRET_KEY` from environment, not in Git
- [ ] Secure cookies enabled (SESSION/CSRF)
- [ ] HSTS configured with appropriate duration
- [ ] `python manage.py check --deploy` passes
- [ ] `check --deploy` integrated in CI/CD pipeline

### Authentication & Sessions
- [ ] Django auth for backoffice
- [ ] DRF auth configured (Session and/or JWT)
- [ ] `DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]`
- [ ] Password validators configured
- [ ] Login throttling implemented

### Authorization
- [ ] Domain permissions centralized in `apps/<app>/permissions.py`
- [ ] Permissions reused in DRF via wrapper classes
- [ ] Object-level permissions for multi-tenant data
- [ ] Queryset filtering by user scope

### Input/Output Protection
- [ ] All POST forms include `{% csrf_token %}`
- [ ] No `|safe` on user-controlled data
- [ ] ORM used for all queries (no raw SQL concatenation)
- [ ] CORS strictly configured (no wildcards)

### Data & Compliance
- [ ] Sensitive data identified and documented
- [ ] Secrets stored in environment/secrets manager
- [ ] Data retention policy defined
- [ ] Anonymization capability for GDPR if needed

### Logging & Monitoring
- [ ] Security events logged (login, permission denied)
- [ ] Audit trail for sensitive operations
- [ ] Log format suitable for aggregation (JSON)
- [ ] Dependencies monitored for vulnerabilities
