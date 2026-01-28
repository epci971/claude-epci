# Stack Guidelines

> Technology-specific conventions and patterns for spec generation.

## Overview

This reference contains stack detection rules and guidelines for each supported technology stack. Used by step-03 for PROMPT.md generation and by templates for conditional content.

---

## Stack Detection Matrix

| Stack | Detection Files | Framework | Language | Test Framework |
|-------|-----------------|-----------|----------|----------------|
| Django | `manage.py` + `requirements.txt`/`pyproject.toml` with django | Django | Python | pytest |
| React | `package.json` with react | React | TypeScript | vitest |
| Spring | `pom.xml` or `build.gradle` with spring-boot | Spring Boot | Java | JUnit 5 |
| Symfony | `composer.json` with symfony | Symfony | PHP | PHPUnit |
| Generic | No specific markers | - | - | Project-specific |

### Detection Priority

1. Check for Django markers first (manage.py is definitive)
2. Check for Spring markers (pom.xml/build.gradle with spring)
3. Check for Symfony markers (composer.json with symfony)
4. Check for React markers (package.json with react)
5. Default to Generic if no matches

### Secondary Markers

| Stack | Additional Markers |
|-------|-------------------|
| Django | `urls.py`, `settings.py`, `wsgi.py` |
| React | `src/components/`, `.tsx` files, `vite.config.*` |
| Spring | `@SpringBootApplication`, `src/main/java/` |
| Symfony | `bin/console`, `src/Controller/`, `config/bundles.php` |

---

## Django Guidelines

### Architecture Patterns

- **Service layer pattern**: Forms -> Services -> Models (avoid fat models/views)
- **Repository pattern**: For complex queries, use managers or repositories
- **Type hints**: Required on all public functions (mypy compatible)

### Testing

- **Framework**: pytest with pytest-django
- **Fixtures**: Factory Boy for model factories
- **Coverage**: Target 80%+ on service layer
- **Mocking**: pytest-mock for external services

### Conventions

```python
# Service layer example
class UserService:
    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password."""
        # Business logic here
        return User.objects.create(email=email, password=make_password(password))
```

### Tools

| Purpose | Tool |
|---------|------|
| API | Django REST Framework |
| Async tasks | Celery |
| Admin | Django Admin (customized) |
| Forms | Django Forms / DRF Serializers |

### Commit Format

```
feat({feature}): {description}
fix({feature}): {description}
test({feature}): {description}
refactor({feature}): {description}
```

---

## React Guidelines

### Architecture Patterns

- **Functional components only**: No class components
- **Hooks**: Custom hooks for reusable logic
- **State management**: Zustand for global state (if needed)
- **Data fetching**: React Query / TanStack Query

### Testing

- **Framework**: Vitest + React Testing Library
- **Strategy**: Test behavior, not implementation
- **Coverage**: Target 70%+ on components
- **E2E**: Playwright for critical flows

### Conventions

```tsx
// Component example
interface UserCardProps {
  user: User;
  onEdit: (id: string) => void;
}

export function UserCard({ user, onEdit }: UserCardProps) {
  return (
    <div className="card">
      <h3>{user.name}</h3>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}
```

### Tools

| Purpose | Tool |
|---------|------|
| Styling | Tailwind CSS |
| Build | Vite |
| Types | TypeScript strict mode |
| Forms | React Hook Form |

### Commit Format

```
feat({feature}): {description}
fix({feature}): {description}
test({feature}): {description}
style({feature}): {description}
```

---

## Spring Boot Guidelines

### Architecture Patterns

- **Service layer pattern**: Controllers -> Services -> Repositories
- **Interface-based services**: Define interfaces for services
- **Constructor injection**: Never use field injection
- **DTO pattern**: Separate API models from entities

### Testing

- **Framework**: JUnit 5 + Mockito
- **Slices**: @WebMvcTest, @DataJpaTest for focused tests
- **Coverage**: Target 80%+ on services
- **Integration**: @SpringBootTest for full context

### Conventions

```java
// Service example
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;

    @Override
    public User createUser(CreateUserRequest request) {
        // Business logic here
        return userRepository.save(User.from(request));
    }
}
```

### Tools

| Purpose | Tool |
|---------|------|
| ORM | Spring Data JPA |
| Security | Spring Security |
| Validation | Jakarta Validation |
| Boilerplate | Lombok |

### Commit Format

```
feat({feature}): {description}
fix({feature}): {description}
test({feature}): {description}
refactor({feature}): {description}
```

---

## Symfony Guidelines

### Architecture Patterns

- **Service layer pattern**: Controllers -> Services -> Repositories
- **Dependency injection**: Autowiring preferred
- **Voters**: For authorization logic
- **Events**: For decoupled side effects

### Testing

- **Framework**: PHPUnit + Prophecy
- **Functional**: WebTestCase for controllers
- **Coverage**: Target 80%+ on services
- **Fixtures**: Doctrine Fixtures for test data

### Conventions

```php
// Service example
class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly UserPasswordHasherInterface $hasher
    ) {}

    public function createUser(CreateUserRequest $request): User
    {
        // Business logic here
        $user = new User();
        $user->setEmail($request->email);
        $user->setPassword($this->hasher->hashPassword($user, $request->password));

        $this->userRepository->save($user, true);
        return $user;
    }
}
```

### Tools

| Purpose | Tool |
|---------|------|
| ORM | Doctrine |
| Async | Messenger |
| Security | Security Bundle + Voters |
| Validation | Validator Component |

### Commit Format

```
feat({feature}): {description}
fix({feature}): {description}
test({feature}): {description}
refactor({feature}): {description}
```

---

## Generic Guidelines

When no specific stack is detected, apply these universal conventions.

### Principles

- Follow existing project conventions
- Write comprehensive tests for all code
- Document non-obvious decisions
- Use existing patterns and utilities
- Maintain consistent code style

### Testing

- Use project's existing test framework
- Match existing test patterns
- Target reasonable coverage (60%+)
- Focus on critical paths

### Commit Format

```
feat({feature}): {description}
fix({feature}): {description}
test({feature}): {description}
docs({feature}): {description}
```

---

## Test Framework Quick Reference

| Stack | Unit Tests | Integration | E2E |
|-------|-----------|-------------|-----|
| Django | pytest | pytest-django | Playwright |
| React | Vitest | Vitest | Playwright |
| Spring | JUnit 5 | @SpringBootTest | - |
| Symfony | PHPUnit | WebTestCase | Panther |
| Generic | Project-specific | - | - |

---

## Usage

### In step-03-generate-ralph.md

```markdown
1. Detect stack using detection matrix
2. Load appropriate guidelines section
3. Inject into PROMPT.md {{STACK_GUIDELINES}} placeholder
```

### In prompt.md.template

The template uses conditional blocks:
- `{{#if STACK_DJANGO}}` ... `{{/if}}`
- `{{#if STACK_REACT}}` ... `{{/if}}`
- etc.

Step-03 sets the appropriate flag based on detection.
