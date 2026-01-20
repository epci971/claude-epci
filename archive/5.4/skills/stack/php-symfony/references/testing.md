# Symfony Testing Reference

## Test Organization

```
tests/
├── Unit/                          # Pure unit tests (no kernel)
│   ├── Entity/
│   ├── Service/
│   └── Validator/
├── Functional/                    # Integration tests (with kernel)
│   ├── Controller/
│   ├── Repository/
│   └── Command/
├── E2E/                          # End-to-end tests (browser)
│   └── Feature/
├── Fixtures/                      # Test data
│   └── UserFixtures.php
└── bootstrap.php
```

## PHPUnit Configuration

```xml
<!-- phpunit.xml.dist -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/10.5/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         cacheResultFile=".phpunit.cache/test-results"
         executionOrder="depends,defects"
         shortenArraysForExportThreshold="10"
         requireCoverageMetadata="false"
         beStrictAboutOutputDuringTests="true"
         failOnRisky="true"
         failOnWarning="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Functional">
            <directory>tests/Functional</directory>
        </testsuite>
    </testsuites>

    <coverage includeUncoveredFiles="true">
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <exclude>
            <directory>src/Kernel.php</directory>
        </exclude>
        <report>
            <html outputDirectory="coverage"/>
            <text outputFile="coverage/coverage.txt"/>
        </report>
    </coverage>

    <php>
        <ini name="display_errors" value="1"/>
        <ini name="error_reporting" value="-1"/>
        <server name="APP_ENV" value="test" force="true"/>
        <server name="SHELL_VERBOSITY" value="-1"/>
        <server name="SYMFONY_PHPUNIT_REMOVE" value=""/>
        <server name="SYMFONY_PHPUNIT_VERSION" value="10.5"/>
    </php>
</phpunit>
```

## Unit Tests

### Entity Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Entity;

use App\Entity\User;
use PHPUnit\Framework\TestCase;

final class UserTest extends TestCase
{
    public function testCreateUser(): void
    {
        // Arrange
        $email = 'test@example.com';
        $name = 'John Doe';

        // Act
        $user = new User($email, $name);

        // Assert
        $this->assertEquals($email, $user->getEmail());
        $this->assertEquals($name, $user->getName());
        $this->assertEquals(User::STATUS_PENDING, $user->getStatus());
        $this->assertFalse($user->isActive());
    }

    public function testActivateUser(): void
    {
        $user = new User('test@example.com', 'John');

        $user->activate();

        $this->assertTrue($user->isActive());
        $this->assertEquals(User::STATUS_ACTIVE, $user->getStatus());
    }

    public function testCannotActivateAlreadyActiveUser(): void
    {
        $user = new User('test@example.com', 'John');
        $user->activate();

        $this->expectException(\DomainException::class);
        $this->expectExceptionMessage('Only pending users can be activated');

        $user->activate();
    }
}
```

### Service Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Service;

use App\Entity\User;
use App\Repository\UserRepository;
use App\Service\UserService;
use Doctrine\ORM\EntityManagerInterface;
use PHPUnit\Framework\TestCase;
use Psr\EventDispatcher\EventDispatcherInterface;

final class UserServiceTest extends TestCase
{
    private UserService $service;
    private UserRepository $repository;
    private EntityManagerInterface $entityManager;
    private EventDispatcherInterface $eventDispatcher;

    protected function setUp(): void
    {
        $this->repository = $this->createMock(UserRepository::class);
        $this->entityManager = $this->createMock(EntityManagerInterface::class);
        $this->eventDispatcher = $this->createMock(EventDispatcherInterface::class);

        $this->service = new UserService(
            $this->repository,
            $this->entityManager,
            $this->eventDispatcher,
        );
    }

    public function testCreateUser(): void
    {
        // Arrange
        $this->entityManager
            ->expects($this->once())
            ->method('persist')
            ->with($this->isInstanceOf(User::class));

        $this->entityManager
            ->expects($this->once())
            ->method('flush');

        $this->eventDispatcher
            ->expects($this->once())
            ->method('dispatch');

        // Act
        $user = $this->service->createUser('test@example.com', 'John');

        // Assert
        $this->assertEquals('test@example.com', $user->getEmail());
        $this->assertEquals('John', $user->getName());
    }

    public function testActivateUserThrowsExceptionIfAlreadyActive(): void
    {
        $user = new User('test@example.com', 'John');
        $user->activate();

        $this->expectException(\DomainException::class);

        $this->service->activateUser($user);
    }
}
```

## Functional Tests

### Controller Test (WebTestCase)

```php
<?php

declare(strict_types=1);

namespace App\Tests\Functional\Controller;

use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\KernelBrowser;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use Symfony\Component\HttpFoundation\Response;

final class UserControllerTest extends WebTestCase
{
    private KernelBrowser $client;
    private EntityManagerInterface $entityManager;

    protected function setUp(): void
    {
        $this->client = static::createClient();
        $this->entityManager = static::getContainer()->get(EntityManagerInterface::class);
    }

    public function testListUsers(): void
    {
        // Create test data
        $user = $this->createUser('test@example.com');

        // Make request
        $this->client->request('GET', '/api/users');

        // Assert response
        $this->assertResponseIsSuccessful();
        $this->assertResponseHeaderSame('Content-Type', 'application/json');

        $data = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertIsArray($data);
        $this->assertNotEmpty($data);
    }

    public function testCreateUser(): void
    {
        $payload = [
            'email' => 'new@example.com',
            'name' => 'New User',
            'password' => 'password123',
        ];

        $this->client->request(
            'POST',
            '/api/users',
            [],
            [],
            ['CONTENT_TYPE' => 'application/json'],
            json_encode($payload),
        );

        $this->assertResponseStatusCodeSame(Response::HTTP_CREATED);

        $data = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('new@example.com', $data['email']);
    }

    public function testCreateUserWithInvalidEmail(): void
    {
        $payload = [
            'email' => 'invalid-email',
            'name' => 'Test',
            'password' => 'password123',
        ];

        $this->client->request(
            'POST',
            '/api/users',
            [],
            [],
            ['CONTENT_TYPE' => 'application/json'],
            json_encode($payload),
        );

        $this->assertResponseStatusCodeSame(Response::HTTP_UNPROCESSABLE_ENTITY);
    }

    public function testShowUserNotFound(): void
    {
        $this->client->request('GET', '/api/users/99999');

        $this->assertResponseStatusCodeSame(Response::HTTP_NOT_FOUND);
    }

    private function createUser(string $email): User
    {
        $user = new User($email, 'Test User');
        $this->entityManager->persist($user);
        $this->entityManager->flush();

        return $user;
    }

    protected function tearDown(): void
    {
        // Clean up test data
        $this->entityManager->createQuery('DELETE FROM App\Entity\User')->execute();
        parent::tearDown();
    }
}
```

### Authenticated Requests

```php
<?php

final class AdminControllerTest extends WebTestCase
{
    public function testAdminAccessRequiresAuthentication(): void
    {
        $client = static::createClient();
        $client->request('GET', '/admin/users');

        $this->assertResponseRedirects('/login');
    }

    public function testAdminCanAccessAdminArea(): void
    {
        $client = static::createClient();

        // Create admin user
        $userRepository = static::getContainer()->get(UserRepository::class);
        $admin = $userRepository->findOneBy(['email' => 'admin@example.com']);

        // Login as admin
        $client->loginUser($admin);

        $client->request('GET', '/admin/users');

        $this->assertResponseIsSuccessful();
    }

    public function testRegularUserCannotAccessAdminArea(): void
    {
        $client = static::createClient();

        $user = new User('user@example.com', 'Regular User');
        // No ROLE_ADMIN

        $client->loginUser($user);
        $client->request('GET', '/admin/users');

        $this->assertResponseStatusCodeSame(Response::HTTP_FORBIDDEN);
    }
}
```

### Repository Test

```php
<?php

declare(strict_types=1);

namespace App\Tests\Functional\Repository;

use App\Entity\User;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

final class UserRepositoryTest extends KernelTestCase
{
    private UserRepository $repository;
    private EntityManagerInterface $entityManager;

    protected function setUp(): void
    {
        self::bootKernel();
        $this->repository = static::getContainer()->get(UserRepository::class);
        $this->entityManager = static::getContainer()->get(EntityManagerInterface::class);
    }

    public function testFindActiveUsers(): void
    {
        // Arrange
        $activeUser = $this->createUser('active@example.com', User::STATUS_ACTIVE);
        $pendingUser = $this->createUser('pending@example.com', User::STATUS_PENDING);

        // Act
        $activeUsers = $this->repository->findActiveUsers();

        // Assert
        $this->assertCount(1, $activeUsers);
        $this->assertEquals('active@example.com', $activeUsers[0]->getEmail());
    }

    public function testFindByEmail(): void
    {
        $user = $this->createUser('find-me@example.com');

        $found = $this->repository->findByEmail('find-me@example.com');

        $this->assertNotNull($found);
        $this->assertEquals($user->getId(), $found->getId());
    }

    public function testFindByEmailReturnsNullWhenNotFound(): void
    {
        $found = $this->repository->findByEmail('nonexistent@example.com');

        $this->assertNull($found);
    }

    private function createUser(string $email, string $status = User::STATUS_PENDING): User
    {
        $user = new User($email, 'Test');

        if ($status === User::STATUS_ACTIVE) {
            $user->activate();
        }

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        return $user;
    }

    protected function tearDown(): void
    {
        $this->entityManager->createQuery('DELETE FROM App\Entity\User')->execute();
        parent::tearDown();
    }
}
```

## Fixtures (doctrine/doctrine-fixtures-bundle)

```php
<?php

declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\User;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

final class UserFixtures extends Fixture
{
    public const ADMIN_USER_REFERENCE = 'admin-user';
    public const REGULAR_USER_REFERENCE = 'regular-user';

    public function __construct(
        private readonly UserPasswordHasherInterface $passwordHasher,
    ) {}

    public function load(ObjectManager $manager): void
    {
        // Admin user
        $admin = new User('admin@example.com', 'Admin User');
        $admin->setPassword($this->passwordHasher->hashPassword($admin, 'admin123'));
        $admin->setRoles(['ROLE_ADMIN']);
        $admin->activate();
        $manager->persist($admin);
        $this->addReference(self::ADMIN_USER_REFERENCE, $admin);

        // Regular user
        $user = new User('user@example.com', 'Regular User');
        $user->setPassword($this->passwordHasher->hashPassword($user, 'user123'));
        $user->activate();
        $manager->persist($user);
        $this->addReference(self::REGULAR_USER_REFERENCE, $user);

        $manager->flush();
    }
}
```

```bash
# Load fixtures
php bin/console doctrine:fixtures:load --env=test

# Load specific group
php bin/console doctrine:fixtures:load --group=test
```

## Commands

```bash
# Run all tests
php bin/phpunit

# Run specific test file
php bin/phpunit tests/Unit/Entity/UserTest.php

# Run specific test method
php bin/phpunit --filter testCreateUser

# Run with coverage
php bin/phpunit --coverage-html coverage/

# Run unit tests only
php bin/phpunit --testsuite Unit

# Run functional tests only
php bin/phpunit --testsuite Functional

# Stop on first failure
php bin/phpunit --stop-on-failure
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Structure | AAA (Arrange-Act-Assert) | Mixed logic |
| Isolation | Independent tests | Shared state |
| Naming | Descriptive test names | `test1`, `testA` |
| Fixtures | Use fixtures bundle | Manual data creation |
| Mocking | Mock external services | Mock everything |
| Coverage | Focus on services (80%+) | 100% coverage |
| Speed | Unit > Functional > E2E | Slow tests |
