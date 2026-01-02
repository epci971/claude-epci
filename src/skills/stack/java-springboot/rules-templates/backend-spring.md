---
paths:
  - backend/**/*.java
  - "!backend/**/test/**"
---

# Spring Boot Backend Rules

> Conventions pour le developpement Java/Spring Boot.

## 🔴 CRITICAL

1. **Injection constructeur**: Jamais `@Autowired` sur fields
2. **Transactions sur services**: Jamais sur controllers
3. **DTOs pour API**: Jamais d'entites directement
4. **Validation avec @Valid**: Sur tous les @RequestBody

## 🟡 CONVENTIONS

### Architecture

```
src/main/java/com/example/app/
├── Application.java
├── config/               # Configuration beans
├── controller/           # REST controllers
├── service/              # Business logic
├── repository/           # Data access
├── entity/               # JPA entities
├── dto/                  # Request/Response DTOs
├── exception/            # Custom exceptions
└── security/             # Security config
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Controllers | `*Controller` | `UserController` |
| Services | `*Service` | `UserService` |
| Repositories | `*Repository` | `UserRepository` |
| Entities | Singular, PascalCase | `User` |
| DTOs | `*Request`, `*Response` | `CreateUserRequest` |

### Service Pattern

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public User createUser(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException(request.getEmail());
        }

        User user = User.builder()
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();

        return userRepository.save(user);
    }

    @Transactional(readOnly = true)
    public User getById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

## 🟢 PREFERENCES

- Utiliser Lombok `@RequiredArgsConstructor`
- `@Transactional(readOnly = true)` pour les reads
- Builder pattern pour entities et DTOs

## Quick Reference

| Task | Pattern |
|------|---------|
| Injection | `@RequiredArgsConstructor` + `private final` |
| Transaction | `@Transactional` on service methods |
| Validation | `@Valid @RequestBody` |
| Exception | `@RestControllerAdvice` global handler |
| Logging | `@Slf4j` + `log.info()` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| DTO mapping | MapStruct ou manual | Separation |
| Global exception | `@RestControllerAdvice` | Consistent errors |
| Pagination | `Pageable` parameter | Standard paging |
| Specifications | `Specification<T>` | Dynamic queries |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Field injection | Untestable | Constructor |
| Transaction on controller | Wrong layer | Service |
| Entity in response | Coupling | DTOs |
| Business in controller | SRP | Service layer |

## Examples

### Correct

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;
    private final UserMapper userMapper;

    @PostMapping
    public ResponseEntity<UserResponse> create(
            @Valid @RequestBody CreateUserRequest request) {
        User user = userService.createUser(request);
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(userMapper.toResponse(user));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getById(@PathVariable Long id) {
        User user = userService.getById(id);
        return ResponseEntity.ok(userMapper.toResponse(user));
    }
}
```

### Incorrect

```java
// DON'T DO THIS
@RestController
public class UserController {
    @Autowired  // Field injection!
    private UserRepository userRepository;

    @PostMapping("/users")
    @Transactional  // Transaction on controller!
    public User create(@RequestBody User user) {  // Entity as DTO!
        return userRepository.save(user);  // No validation!
    }
}
```
