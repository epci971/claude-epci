# Spring WebFlux & Reactive Reference

## Overview

Spring WebFlux provides reactive programming support for non-blocking, asynchronous web applications.

| Aspect | Spring MVC | Spring WebFlux |
|--------|------------|----------------|
| Programming model | Imperative | Reactive |
| Threading | Thread-per-request | Event loop |
| Blocking I/O | Yes | No |
| Use case | Traditional apps | High concurrency, streaming |

## Reactive Types

### Mono and Flux

```java
// Mono: 0 or 1 element
Mono<User> user = userRepository.findById(id);
Mono<Void> empty = Mono.empty();
Mono<String> just = Mono.just("value");

// Flux: 0 to N elements
Flux<User> users = userRepository.findAll();
Flux<Integer> range = Flux.range(1, 10);
Flux<String> stream = Flux.fromIterable(List.of("a", "b", "c"));
```

### Basic Operators

```java
// Transform
Mono<UserDto> dto = userMono.map(user -> mapper.toDto(user));

// FlatMap (async transformation)
Mono<Order> order = userMono.flatMap(user -> orderRepository.findByUser(user));

// Filter
Flux<User> active = usersFlux.filter(User::isActive);

// Combine
Mono<Tuple2<User, Profile>> combined = Mono.zip(userMono, profileMono);

// Default value
Mono<User> withDefault = userMono.defaultIfEmpty(User.anonymous());

// Error handling
Mono<User> safe = userMono
    .onErrorResume(NotFoundException.class, e -> Mono.empty())
    .onErrorMap(e -> new ServiceException("Failed", e));
```

## WebFlux Controllers

### Annotated Controller

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public Flux<UserResponse> getAllUsers() {
        return userService.findAll()
                .map(this::toResponse);
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<UserResponse>> getUser(@PathVariable Long id) {
        return userService.findById(id)
                .map(user -> ResponseEntity.ok(toResponse(user)))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> createUser(@Valid @RequestBody Mono<CreateUserRequest> request) {
        return request
                .flatMap(userService::create)
                .map(this::toResponse);
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> deleteUser(@PathVariable Long id) {
        return userService.deleteById(id)
                .then(Mono.just(ResponseEntity.noContent().<Void>build()))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }
}
```

### Functional Endpoints (RouterFunctions)

```java
@Configuration
public class RouterConfig {

    @Bean
    public RouterFunction<ServerResponse> userRoutes(UserHandler handler) {
        return RouterFunctions.route()
                .path("/api/users", builder -> builder
                        .GET("", handler::getAllUsers)
                        .GET("/{id}", handler::getUserById)
                        .POST("", handler::createUser)
                        .DELETE("/{id}", handler::deleteUser))
                .build();
    }
}

@Component
@RequiredArgsConstructor
public class UserHandler {

    private final UserService userService;

    public Mono<ServerResponse> getAllUsers(ServerRequest request) {
        return ServerResponse.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .body(userService.findAll(), User.class);
    }

    public Mono<ServerResponse> getUserById(ServerRequest request) {
        Long id = Long.parseLong(request.pathVariable("id"));
        return userService.findById(id)
                .flatMap(user -> ServerResponse.ok()
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(user))
                .switchIfEmpty(ServerResponse.notFound().build());
    }

    public Mono<ServerResponse> createUser(ServerRequest request) {
        return request.bodyToMono(CreateUserRequest.class)
                .flatMap(userService::create)
                .flatMap(user -> ServerResponse.created(
                        URI.create("/api/users/" + user.getId()))
                        .bodyValue(user));
    }
}
```

## R2DBC (Reactive Database)

### Configuration

```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/mydb
    username: user
    password: password
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-r2dbc</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>r2dbc-postgresql</artifactId>
</dependency>
```

### Entity and Repository

```java
@Table("users")
public class User {

    @Id
    private Long id;
    private String email;
    private String name;
    private Boolean active;
    private LocalDateTime createdAt;
}

@Repository
public interface UserRepository extends ReactiveCrudRepository<User, Long> {

    Mono<User> findByEmail(String email);

    Flux<User> findByActiveTrue();

    @Query("SELECT * FROM users WHERE name LIKE :pattern")
    Flux<User> searchByName(String pattern);

    @Modifying
    @Query("UPDATE users SET active = false WHERE id = :id")
    Mono<Integer> deactivate(Long id);
}
```

### Service Layer

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public Flux<User> findAll() {
        return userRepository.findAll();
    }

    public Mono<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public Mono<User> create(CreateUserRequest request) {
        return userRepository.findByEmail(request.email())
                .flatMap(existing -> Mono.<User>error(
                        new UserAlreadyExistsException(request.email())))
                .switchIfEmpty(Mono.defer(() -> {
                    User user = new User();
                    user.setEmail(request.email());
                    user.setName(request.name());
                    user.setActive(true);
                    return userRepository.save(user);
                }));
    }

    @Transactional
    public Mono<Void> deleteById(Long id) {
        return userRepository.deleteById(id);
    }
}
```

## Backpressure

### Handling Backpressure

```java
// Buffering
Flux<Data> buffered = dataFlux
    .onBackpressureBuffer(1000);

// Drop oldest
Flux<Data> dropOldest = dataFlux
    .onBackpressureBuffer(100, BufferOverflowStrategy.DROP_OLDEST);

// Drop newest
Flux<Data> dropLatest = dataFlux
    .onBackpressureDrop(dropped -> log.warn("Dropped: {}", dropped));

// Latest only
Flux<Data> latest = dataFlux
    .onBackpressureLatest();

// Request control
Flux<Data> controlled = dataFlux
    .limitRate(100); // Request 100 at a time
```

## Server-Sent Events (SSE)

```java
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> streamEvents() {
    return Flux.interval(Duration.ofSeconds(1))
            .map(seq -> ServerSentEvent.<String>builder()
                    .id(String.valueOf(seq))
                    .event("message")
                    .data("Event #" + seq)
                    .build());
}

// Simple streaming
@GetMapping(value = "/users/stream", produces = MediaType.APPLICATION_NDJSON_VALUE)
public Flux<User> streamUsers() {
    return userService.findAll()
            .delayElements(Duration.ofMillis(100));
}
```

## WebClient (Reactive HTTP Client)

```java
@Configuration
public class WebClientConfig {

    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl("https://api.example.com")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
}

@Service
@RequiredArgsConstructor
public class ExternalApiService {

    private final WebClient webClient;

    public Mono<ExternalUser> getUser(String id) {
        return webClient.get()
                .uri("/users/{id}", id)
                .retrieve()
                .onStatus(HttpStatusCode::is4xxClientError,
                        response -> Mono.error(new NotFoundException()))
                .bodyToMono(ExternalUser.class)
                .timeout(Duration.ofSeconds(5))
                .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)));
    }

    public Flux<ExternalUser> getAllUsers() {
        return webClient.get()
                .uri("/users")
                .retrieve()
                .bodyToFlux(ExternalUser.class);
    }

    public Mono<ExternalUser> createUser(CreateUserRequest request) {
        return webClient.post()
                .uri("/users")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ExternalUser.class);
    }
}
```

## Testing Reactive Code

```java
@WebFluxTest(UserController.class)
class UserControllerTest {

    @Autowired
    private WebTestClient webClient;

    @MockBean
    private UserService userService;

    @Test
    void getAllUsers_shouldReturnFlux() {
        when(userService.findAll()).thenReturn(Flux.just(
                new User(1L, "a@test.com", "A"),
                new User(2L, "b@test.com", "B")));

        webClient.get()
                .uri("/api/users")
                .exchange()
                .expectStatus().isOk()
                .expectBodyList(User.class)
                .hasSize(2);
    }

    @Test
    void getUser_notFound_shouldReturn404() {
        when(userService.findById(999L)).thenReturn(Mono.empty());

        webClient.get()
                .uri("/api/users/999")
                .exchange()
                .expectStatus().isNotFound();
    }
}

// StepVerifier for service tests
@Test
void findById_shouldReturnUser() {
    Mono<User> result = userService.findById(1L);

    StepVerifier.create(result)
            .expectNextMatches(user -> user.getEmail().equals("test@example.com"))
            .verifyComplete();
}

@Test
void findAll_shouldReturnMultipleUsers() {
    Flux<User> result = userService.findAll();

    StepVerifier.create(result)
            .expectNextCount(3)
            .verifyComplete();
}
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Blocking | Never block in reactive chain | `block()`, `Thread.sleep()` |
| Errors | Handle with `onError*` operators | Throwing in map/flatMap |
| Resources | Use `using()` for cleanup | Manual resource management |
| Testing | StepVerifier | `block()` in tests |
| Subscriptions | Let framework subscribe | Manual `subscribe()` |
