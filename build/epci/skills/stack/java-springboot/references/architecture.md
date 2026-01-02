# Spring Boot Architecture Reference

## Project Structure

### Standard Maven Layout

```
project/
├── src/
│   ├── main/
│   │   ├── java/com/example/app/
│   │   │   ├── Application.java
│   │   │   ├── config/
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── entity/
│   │   │   ├── dto/
│   │   │   └── exception/
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       └── application-prod.yml
│   └── test/
│       └── java/com/example/app/
├── pom.xml
└── README.md
```

### Gradle Layout

```
project/
├── src/main/java/
├── src/main/resources/
├── src/test/java/
├── build.gradle.kts
├── settings.gradle.kts
└── gradle/
    └── wrapper/
```

## Layered Architecture

### Layer Responsibilities

| Layer | Package | Responsibility |
|-------|---------|----------------|
| Controller | `controller/` | HTTP handling, validation, response mapping |
| Service | `service/` | Business logic, transactions, orchestration |
| Repository | `repository/` | Data access, queries |
| Entity | `entity/` | Domain model, JPA mappings |
| DTO | `dto/` | Data transfer, API contracts |

### Controller Layer

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(userMapper.toResponse(user));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(userMapper.toEntity(request));
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(userMapper.toResponse(user));
    }
}
```

### Service Layer

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public User create(User user) {
        log.info("Creating user: {}", user.getEmail());
        User saved = userRepository.save(user);
        eventPublisher.publishEvent(new UserCreatedEvent(saved));
        return saved;
    }

    @Transactional(readOnly = true)
    public User findById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

## Clean Architecture

### Ports and Adapters Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Infrastructure                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │                   Application                      │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │                  Domain                      │  │  │
│  │  │  ┌─────────────────────────────────────┐    │  │  │
│  │  │  │           Entity                     │    │  │  │
│  │  │  └─────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Package Structure

```
com.example.app/
├── domain/
│   ├── model/
│   │   └── User.java              # Domain entity
│   ├── port/
│   │   ├── in/
│   │   │   └── UserUseCase.java   # Input port (interface)
│   │   └── out/
│   │       └── UserPort.java      # Output port (interface)
│   └── service/
│       └── UserDomainService.java # Domain logic
├── application/
│   └── service/
│       └── UserApplicationService.java  # Use case impl
└── infrastructure/
    ├── adapter/
    │   ├── in/
    │   │   └── web/
    │   │       └── UserController.java  # REST adapter
    │   └── out/
    │       └── persistence/
    │           ├── UserJpaEntity.java
    │           ├── UserJpaRepository.java
    │           └── UserPersistenceAdapter.java
    └── config/
        └── BeanConfig.java
```

### Port Interfaces

```java
// Input Port
public interface CreateUserUseCase {
    User createUser(CreateUserCommand command);
}

// Output Port
public interface LoadUserPort {
    Optional<User> loadById(Long id);
}

public interface SaveUserPort {
    User save(User user);
}
```

### Adapter Implementation

```java
@Component
@RequiredArgsConstructor
public class UserPersistenceAdapter implements LoadUserPort, SaveUserPort {

    private final UserJpaRepository repository;
    private final UserPersistenceMapper mapper;

    @Override
    public Optional<User> loadById(Long id) {
        return repository.findById(id)
                .map(mapper::toDomain);
    }

    @Override
    public User save(User user) {
        UserJpaEntity entity = mapper.toJpaEntity(user);
        UserJpaEntity saved = repository.save(entity);
        return mapper.toDomain(saved);
    }
}
```

## Hexagonal Architecture with Spring

### Domain Module

```java
// Domain Entity - No Spring annotations
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private List<OrderLine> lines;
    private OrderStatus status;

    public Money calculateTotal() {
        return lines.stream()
                .map(OrderLine::getSubtotal)
                .reduce(Money.ZERO, Money::add);
    }

    public void confirm() {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Order already confirmed");
        }
        this.status = OrderStatus.CONFIRMED;
    }
}
```

### Application Service

```java
@Service
@RequiredArgsConstructor
public class OrderApplicationService implements CreateOrderUseCase {

    private final LoadCustomerPort loadCustomerPort;
    private final SaveOrderPort saveOrderPort;
    private final OrderDomainService orderDomainService;

    @Override
    @Transactional
    public Order createOrder(CreateOrderCommand command) {
        Customer customer = loadCustomerPort.loadById(command.customerId())
                .orElseThrow(() -> new CustomerNotFoundException(command.customerId()));

        Order order = orderDomainService.createOrder(customer, command.items());
        return saveOrderPort.save(order);
    }
}
```

### Configuration

```java
@Configuration
public class DomainConfig {

    @Bean
    public OrderDomainService orderDomainService() {
        return new OrderDomainService();
    }
}
```

## Modular Monolith

### Multi-Module Maven Structure

```
parent/
├── pom.xml                    # Parent POM
├── common/
│   └── pom.xml               # Shared utilities
├── user-module/
│   ├── pom.xml
│   └── src/main/java/
│       └── com/example/user/
│           ├── api/          # Public interfaces
│           ├── internal/     # Package-private impl
│           └── UserModuleConfig.java
├── order-module/
│   ├── pom.xml
│   └── src/main/java/
│       └── com/example/order/
└── app/
    └── pom.xml               # Main application
```

### Module API

```java
// Public API exposed by module
public interface UserApi {
    UserDto findById(Long id);
    boolean exists(Long id);
}

// Internal implementation
@Service
class UserApiImpl implements UserApi {

    private final UserRepository repository;
    private final UserMapper mapper;

    @Override
    public UserDto findById(Long id) {
        return repository.findById(id)
                .map(mapper::toDto)
                .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

### Module Configuration

```java
@Configuration
@ComponentScan(basePackageClasses = UserModuleConfig.class)
@EntityScan(basePackageClasses = UserModuleConfig.class)
@EnableJpaRepositories(basePackageClasses = UserModuleConfig.class)
public class UserModuleConfig {
}
```

### Inter-Module Communication

```java
// Via Spring Events
@Component
@RequiredArgsConstructor
public class OrderEventListener {

    private final UserApi userApi;

    @EventListener
    @Async
    public void onOrderCreated(OrderCreatedEvent event) {
        UserDto user = userApi.findById(event.customerId());
        // Process...
    }
}
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Dependencies | Constructor injection | Field injection |
| Transactions | Service layer | Controller layer |
| Validation | DTOs at controller | Entities directly |
| Mapping | Dedicated mappers | Manual in controller |
| Logging | SLF4J with params | String concatenation |
| Configuration | @ConfigurationProperties | Raw @Value everywhere |

## Package Dependencies

```
controller → service → repository
     ↓          ↓          ↓
    dto      entity     entity
```

**Rule**: Lower layers should not depend on upper layers.
