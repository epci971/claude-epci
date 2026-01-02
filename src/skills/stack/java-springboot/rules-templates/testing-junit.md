---
paths:
  - backend/**/test/**/*.java
  - backend/**/*Test.java
  - backend/**/*IT.java
---

# JUnit 5 Testing Rules

> Conventions pour les tests Java avec JUnit 5.

## 🔴 CRITICAL

1. **Tests isoles**: Chaque test independant
2. **Nommage descriptif**: `test_action_expectedResult`
3. **Mocks pour dependances**: Isolation avec Mockito

## 🟡 CONVENTIONS

### Structure

```
src/test/java/com/example/app/
├── controller/
│   └── UserControllerTest.java      # @WebMvcTest
├── service/
│   └── UserServiceTest.java         # Unit test
├── repository/
│   └── UserRepositoryTest.java      # @DataJpaTest
└── integration/
    └── UserIntegrationTest.java     # @SpringBootTest
```

### Naming

| Type | Suffix | Exemple |
|------|--------|---------|
| Unit test | `*Test` | `UserServiceTest` |
| Integration | `*IT` | `UserControllerIT` |
| Method | descriptif | `createUser_success` |

### Unit Test Pattern

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_shouldReturnUser_whenEmailNotExists() {
        // Given
        var request = CreateUserRequest.builder()
                .email("test@example.com")
                .build();
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.save(any())).thenAnswer(i -> i.getArgument(0));

        // When
        var result = userService.createUser(request);

        // Then
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }
}
```

## 🟢 PREFERENCES

- AssertJ pour assertions fluides
- `@Nested` pour grouper les tests
- TestContainers pour integration DB

## Quick Reference

| Task | Pattern |
|------|---------|
| Unit test | `@ExtendWith(MockitoExtension.class)` |
| Mock | `@Mock` + `@InjectMocks` |
| Web test | `@WebMvcTest(Controller.class)` |
| DB test | `@DataJpaTest` |
| Full test | `@SpringBootTest` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Given-When-Then | Comments + structure | Clarity |
| AssertJ | `assertThat().isEqualTo()` | Fluent |
| Nested classes | `@Nested` | Organization |
| TestContainers | `@Container` | Real DB tests |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| No assertions | Useless | Assert something |
| Test order | Fragile | Isolated tests |
| Real DB in unit | Slow | Mocks |
| Too many mocks | Complexity | Integration test |

## Examples

### Correct

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock UserRepository userRepository;
    @Mock PasswordEncoder passwordEncoder;
    @InjectMocks UserService userService;

    @Nested
    class CreateUser {
        @Test
        void shouldCreateUser_whenValidRequest() {
            // Given
            var request = validRequest();
            when(userRepository.existsByEmail(any())).thenReturn(false);
            when(passwordEncoder.encode(any())).thenReturn("hashed");
            when(userRepository.save(any())).thenAnswer(i -> {
                User u = i.getArgument(0);
                u.setId(1L);
                return u;
            });

            // When
            var result = userService.createUser(request);

            // Then
            assertThat(result.getId()).isEqualTo(1L);
            assertThat(result.getEmail()).isEqualTo(request.getEmail());
        }

        @Test
        void shouldThrow_whenEmailExists() {
            when(userRepository.existsByEmail(any())).thenReturn(true);

            assertThatThrownBy(() -> userService.createUser(validRequest()))
                    .isInstanceOf(UserAlreadyExistsException.class);
        }
    }

    private CreateUserRequest validRequest() {
        return CreateUserRequest.builder()
                .email("test@example.com")
                .password("password")
                .build();
    }
}
```

### Incorrect

```java
// DON'T DO THIS
class UserServiceTest {
    @Autowired  // Real beans in unit test!
    UserService userService;

    @Test
    void test() {  // Vague name!
        userService.createUser(new CreateUserRequest());
        // No assertion!
    }
}
```
