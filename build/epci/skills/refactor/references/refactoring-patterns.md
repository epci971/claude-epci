# Refactoring Patterns Catalog

> Reference for supported refactoring patterns based on Fowler's catalog.

## Classic Patterns

### Extract Method

**When to use**: Long method, duplicated code, comments explaining code blocks.

**Before**:
```python
def process_order(self, order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Calculate discount
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1
    elif order.total > 100:
        discount = order.total * 0.05

    # Apply discount and save
    order.final_total = order.total - discount
    self.db.save(order)
```

**After**:
```python
def process_order(self, order):
    self._validate_order(order)
    discount = self._calculate_discount(order)
    order.final_total = order.total - discount
    self.db.save(order)

def _validate_order(self, order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def _calculate_discount(self, order):
    if order.customer.is_premium:
        return order.total * 0.1
    elif order.total > 100:
        return order.total * 0.05
    return 0
```

---

### Extract Class

**When to use**: Large class, class with multiple responsibilities, group of fields that go together.

**Before**:
```python
class User:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.street = ""
        self.city = ""
        self.zip_code = ""
        self.country = ""

    def get_full_address(self):
        return f"{self.street}, {self.city} {self.zip_code}, {self.country}"

    def validate_address(self):
        return bool(self.street and self.city and self.zip_code)
```

**After**:
```python
class Address:
    def __init__(self, street="", city="", zip_code="", country=""):
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def get_full(self):
        return f"{self.street}, {self.city} {self.zip_code}, {self.country}"

    def is_valid(self):
        return bool(self.street and self.city and self.zip_code)

class User:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.address = Address()
```

---

### Inline Method/Class

**When to use**: Method body is as clear as the name, over-delegation.

**Before**:
```python
def get_rating(self):
    return self._more_than_five_late_deliveries()

def _more_than_five_late_deliveries(self):
    return self.late_deliveries > 5
```

**After**:
```python
def get_rating(self):
    return self.late_deliveries > 5
```

---

### Encapsulate Field/Collection

**When to use**: Direct field access, mutable collections exposed.

**Before**:
```python
class Order:
    def __init__(self):
        self.items = []  # Direct access
```

**After**:
```python
class Order:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return tuple(self._items)  # Immutable copy

    def add_item(self, item):
        self._items.append(item)

    def remove_item(self, item):
        self._items.remove(item)
```

---

### Rename (Method/Variable/Class)

**When to use**: Name doesn't communicate intent, inconsistent naming.

**Guidelines**:
- Methods: verb + noun (e.g., `calculateTotal`, `validateUser`)
- Variables: descriptive nouns (e.g., `customerEmail` not `ce`)
- Classes: noun phrases (e.g., `OrderProcessor` not `ProcessOrder`)
- Booleans: `is_`, `has_`, `can_` prefix

---

### Move Method/Field

**When to use**: Feature envy, method uses more of another class.

**Indicators**:
- Method calls many getters of another class
- Method could be static if moved
- Data and behavior are separated

---

## Legacy Patterns

### Strangler Fig

**When to use**: Large legacy system, gradual replacement needed.

**Strategy**:
```
1. Identify component to replace
2. Create new implementation alongside old
3. Route traffic gradually:
   - Start: 0% new, 100% old
   - Phase 1: 10% new, 90% old
   - Phase 2: 50% new, 50% old
   - Phase 3: 90% new, 10% old
   - Final: 100% new, 0% old
4. Remove old implementation
```

**Example**:
```python
# Feature flag routing
class AuthRouter:
    def authenticate(self, credentials):
        if feature_flags.is_enabled("new_auth", user_id=credentials.user_id):
            return NewAuthService().authenticate(credentials)
        else:
            return LegacyAuthService().authenticate(credentials)
```

---

### Branch by Abstraction

**When to use**: Replace implementation without feature flags.

**Strategy**:
```
1. Create abstraction (interface) for component
2. Make old implementation implement interface
3. Switch all clients to use interface
4. Create new implementation of interface
5. Gradually switch to new implementation
6. Remove old implementation
```

**Example**:
```python
# Step 1-2: Create interface, adapt old
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, payment): pass

class LegacyPaymentProcessor(PaymentProcessor):
    def process(self, payment):
        # Old implementation
        pass

# Step 4: New implementation
class ModernPaymentProcessor(PaymentProcessor):
    def process(self, payment):
        # New implementation
        pass

# Step 5: Switch via dependency injection
container.register(PaymentProcessor, ModernPaymentProcessor)
```

---

### Parallel Change (Expand-Contract)

**When to use**: API migration, backward compatibility needed.

**Strategy**:
```
1. EXPAND: Add new API alongside old
2. MIGRATE: Move clients to new API
3. CONTRACT: Remove old API
```

**Example**:
```python
# Phase 1: EXPAND
class UserService:
    def get_user(self, user_id):  # Old
        return self._fetch_user(user_id)

    def get_user_by_id(self, user_id):  # New (more explicit)
        return self._fetch_user(user_id)

# Phase 2: MIGRATE (update all callers)
# user_service.get_user(id) → user_service.get_user_by_id(id)

# Phase 3: CONTRACT
class UserService:
    def get_user_by_id(self, user_id):  # Only new remains
        return self._fetch_user(user_id)
```

---

## Architecture Patterns

### Mikado Method

**When to use**: Complex dependency graph, unclear impact.

**Full guide**: See [mikado-method.md](mikado-method.md)

**Summary**:
1. Define GOAL
2. Try to reach goal directly
3. On failure, identify prerequisite
4. Add prerequisite as sub-goal
5. Revert changes
6. Repeat until leaf goals identified
7. Execute leaf to root

---

## Pattern Selection Matrix

| Code Smell | Suggested Pattern(s) |
|------------|---------------------|
| Long Method | Extract Method |
| Large Class | Extract Class |
| Duplicated Code | Extract Method, Extract Module |
| Feature Envy | Move Method |
| Data Clumps | Extract Class (for data) |
| Primitive Obsession | Encapsulate Field |
| Long Parameter List | Introduce Parameter Object |
| Divergent Change | Split Class |
| Shotgun Surgery | Move Method, Inline Class |
| Parallel Inheritance | Collapse Hierarchy |
| Comments | Extract Method (name explains) |
| Dead Code | Inline (remove) |
| Speculative Generality | Inline, Remove |

---

## Safety Rules

1. **Run tests before each transformation**
2. **Run tests after each transformation**
3. **Revert immediately if tests fail**
4. **One transformation at a time**
5. **Commit after each successful transformation (if --atomic)**
6. **Never change behavior (external API must remain identical)**
