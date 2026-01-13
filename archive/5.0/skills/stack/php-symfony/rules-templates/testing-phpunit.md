---
paths:
  - backend/tests/**/*.php
  - "!backend/tests/bootstrap.php"
---

# PHPUnit Testing Rules

> Conventions pour les tests PHP avec PHPUnit.

## 🔴 CRITICAL

1. **Tests isoles**: Chaque test independant
2. **Pas de donnees de prod**: Utiliser fixtures ou factories
3. **Rollback transactions**: Tests fonctionnels dans transaction

## 🟡 CONVENTIONS

### Structure

```
tests/
├── Unit/
│   ├── Service/
│   │   └── UserServiceTest.php
│   └── Entity/
│       └── UserTest.php
├── Functional/
│   └── Controller/
│       └── UserControllerTest.php
└── fixtures/
    └── users.yaml
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Classe | `*Test` | `UserServiceTest` |
| Methode | `test*` ou `@test` | `testCreateUser` |
| DataProvider | `provide*Data` | `provideInvalidEmails` |

### Pattern AAA

```php
public function testCreateUserSuccess(): void
{
    // Arrange
    $dto = new CreateUserDto('test@example.com', 'Test');

    // Act
    $user = $this->userService->createUser($dto);

    // Assert
    $this->assertNotNull($user->getId());
    $this->assertEquals('test@example.com', $user->getEmail());
}
```

## 🟢 PREFERENCES

- Utiliser `@dataProvider` pour cas multiples
- Mocker les services externes avec Prophecy ou PHPUnit mocks
- Utiliser `WebTestCase` pour tests API

## Quick Reference

| Task | Pattern |
|------|---------|
| Unit test | `extends TestCase` |
| Functional | `extends WebTestCase` |
| Mock | `$this->createMock(Service::class)` |
| DataProvider | `@dataProvider provideData` |
| Exception | `$this->expectException(Exception::class)` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| WebTestCase | `static::createClient()` | Full stack test |
| Fixtures | Alice ou DoctrineFixtures | Donnees reproductibles |
| DataProvider | `@dataProvider` | DRY tests |
| Mock | `createMock()` | Isolation |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| No assertions | Test inutile | Assert something |
| Test order | Fragile | Isolated tests |
| External calls | Slow, flaky | Mocks |
| Hardcoded IDs | Fragile | Fixtures/Factories |

## Examples

### Correct

```php
final class UserServiceTest extends TestCase
{
    private UserService $userService;
    private UserRepository&MockObject $userRepository;

    protected function setUp(): void
    {
        $this->userRepository = $this->createMock(UserRepository::class);
        $this->userService = new UserService($this->userRepository);
    }

    public function testCreateUserSuccess(): void
    {
        $dto = new CreateUserDto('test@example.com', 'Test');

        $this->userRepository
            ->expects($this->once())
            ->method('save')
            ->willReturnCallback(fn(User $user) => $user);

        $user = $this->userService->createUser($dto);

        $this->assertEquals('test@example.com', $user->getEmail());
    }

    /**
     * @dataProvider provideInvalidEmails
     */
    public function testCreateUserWithInvalidEmail(string $email): void
    {
        $this->expectException(ValidationException::class);
        $this->userService->createUser(new CreateUserDto($email, 'Test'));
    }

    public static function provideInvalidEmails(): array
    {
        return [
            'empty' => [''],
            'no at' => ['invalidemail'],
            'no domain' => ['test@'],
        ];
    }
}
```

### Incorrect

```php
// DON'T DO THIS
class UserTest extends TestCase
{
    public function testUser(): void
    {
        $user = new User();
        $user->setEmail('test@example.com');
        // No assertion!
    }
}
```
