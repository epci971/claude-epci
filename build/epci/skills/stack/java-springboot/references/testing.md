# Spring Boot Testing Reference

## JUnit 5 Fundamentals

### Basic Test Structure

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @BeforeEach
    void setUp() {
        // Setup before each test
    }

    @Test
    @DisplayName("Should create user when email is unique")
    void createUser_whenEmailUnique_shouldSucceed() {
        // Given
        CreateUserRequest request = new CreateUserRequest("test@example.com", "Test");
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenAnswer(i -> {
            User u = i.getArgument(0);
            u.setId(1L);
            return u;
        });

        // When
        User result = userService.createUser(request);

        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }

    @Test
    void createUser_whenEmailExists_shouldThrowException() {
        // Given
        CreateUserRequest request = new CreateUserRequest("existing@example.com", "Test");
        when(userRepository.existsByEmail(anyString())).thenReturn(true);

        // When/Then
        assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(UserAlreadyExistsException.class)
                .hasMessageContaining("existing@example.com");

        verify(userRepository, never()).save(any());
    }
}
```

### Nested Tests

```java
@DisplayName("UserService")
class UserServiceTest {

    @Nested
    @DisplayName("createUser")
    class CreateUser {

        @Test
        @DisplayName("should create user with valid data")
        void withValidData_shouldSucceed() { }

        @Test
        @DisplayName("should throw when email exists")
        void withExistingEmail_shouldThrow() { }

        @Nested
        @DisplayName("when user is admin")
        class WhenAdmin {

            @Test
            void shouldBypassEmailVerification() { }
        }
    }

    @Nested
    @DisplayName("deleteUser")
    class DeleteUser {

        @Test
        void shouldSoftDeleteUser() { }
    }
}
```

### Parameterized Tests

```java
class ValidationTest {

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "   "})
    void shouldRejectBlankEmail(String email) {
        assertThat(validator.isValidEmail(email)).isFalse();
    }

    @ParameterizedTest
    @CsvSource({"test@example.com, true", "invalid, false"})
    void shouldValidateEmails(String email, boolean expected) {
        assertThat(validator.isValidEmail(email)).isEqualTo(expected);
    }

    @ParameterizedTest
    @EnumSource(value = UserStatus.class, names = {"ACTIVE", "PENDING"})
    void shouldAllowLogin(UserStatus status) {
        assertThat(authService.canLogin(status)).isTrue();
    }
}
```

## Mockito

### Stubbing

```java
// Return value
when(repository.findById(1L)).thenReturn(Optional.of(user));

// Throw exception
when(repository.findById(999L)).thenThrow(new NotFoundException());

// Answer with argument
when(repository.save(any(User.class))).thenAnswer(invocation -> {
    User arg = invocation.getArgument(0);
    arg.setId(1L);
    return arg;
});

// Consecutive calls
when(service.getStatus())
    .thenReturn("PENDING")
    .thenReturn("PROCESSING")
    .thenReturn("COMPLETED");

// Void methods
doNothing().when(service).sendNotification(any());
doThrow(new RuntimeException()).when(service).delete(any());
```

### Verification

```java
// Called once
verify(repository).save(user);

// Called specific times
verify(repository, times(2)).findById(anyLong());
verify(repository, never()).delete(any());
verify(repository, atLeastOnce()).findAll();

// With argument capture
ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
verify(repository).save(captor.capture());
User savedUser = captor.getValue();
assertThat(savedUser.getEmail()).isEqualTo("test@example.com");

// Ordered verification
InOrder inOrder = inOrder(repository, eventPublisher);
inOrder.verify(repository).save(any(User.class));
inOrder.verify(eventPublisher).publishEvent(any(UserCreatedEvent.class));

// No more interactions
verifyNoMoreInteractions(repository);
```

## Spring Boot Test Slices

### @WebMvcTest (Controller Layer)

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void getUser_shouldReturnUser() throws Exception {
        User user = new User(1L, "test@example.com", "Test");
        when(userService.findById(1L)).thenReturn(user);

        mockMvc.perform(get("/api/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    void createUser_withValidData_shouldReturn201() throws Exception {
        CreateUserRequest request = new CreateUserRequest("new@example.com", "New");
        User created = new User(1L, "new@example.com", "New");
        when(userService.createUser(any())).thenReturn(created);

        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists());
    }

    @Test
    void createUser_withInvalidEmail_shouldReturn400() throws Exception {
        CreateUserRequest request = new CreateUserRequest("invalid", "Test");

        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors").isArray());
    }
}
```

### @DataJpaTest (Repository Layer)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void findByEmail_shouldReturnUser() {
        // Given
        User user = new User(null, "test@example.com", "Test", true);
        entityManager.persistAndFlush(user);

        // When
        Optional<User> found = userRepository.findByEmail("test@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Test");
    }

    @Test
    void findByActiveTrue_shouldReturnOnlyActiveUsers() {
        entityManager.persist(new User(null, "active@test.com", "Active", true));
        entityManager.persist(new User(null, "inactive@test.com", "Inactive", false));
        entityManager.flush();

        List<User> activeUsers = userRepository.findByActiveTrue();

        assertThat(activeUsers).hasSize(1);
        assertThat(activeUsers.get(0).getEmail()).isEqualTo("active@test.com");
    }
}
```

### @SpringBootTest (Integration)

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Transactional
class UserIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @LocalServerPort
    private int port;

    @Autowired
    private UserRepository userRepository;

    @Test
    void createAndRetrieveUser() {
        // Create
        CreateUserRequest request = new CreateUserRequest("int@test.com", "Integration");
        ResponseEntity<UserResponse> createResponse = restTemplate.postForEntity(
                "/api/users", request, UserResponse.class);

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        Long userId = createResponse.getBody().getId();

        // Retrieve
        ResponseEntity<UserResponse> getResponse = restTemplate.getForEntity(
                "/api/users/" + userId, UserResponse.class);

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().getEmail()).isEqualTo("int@test.com");
    }
}
```

## TestContainers

### Setup

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

### PostgreSQL Container

```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldPersistUser() {
        User user = new User(null, "test@example.com", "Test", true);
        User saved = userRepository.save(user);

        assertThat(saved.getId()).isNotNull();
        assertThat(userRepository.findByEmail("test@example.com")).isPresent();
    }
}
```

## ArchUnit

Use ArchUnit (`archunit-junit5`) for architecture validation:

```java
@AnalyzeClasses(packages = "com.example.app")
class ArchitectureTest {
    @ArchTest
    static final ArchRule layer_dependencies =
        layeredArchitecture()
            .layer("Controller").definedBy("..controller..")
            .layer("Service").definedBy("..service..")
            .layer("Repository").definedBy("..repository..")
            .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller", "Service")
            .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");
}
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Naming | `methodName_condition_expectedResult` | Generic names |
| Structure | Given/When/Then or Arrange/Act/Assert | Mixed steps |
| Mocking | Mock dependencies, not SUT | Over-mocking |
| Assertions | AssertJ fluent assertions | JUnit basic |
| Data | Builder pattern, test fixtures | Hardcoded values |
| DB tests | @Transactional for rollback | Manual cleanup |
| Integration | TestContainers for real DB | H2 differences |

## Test Organization

Organize tests by type: `unit/`, `integration/`, `architecture/`, `fixtures/`
