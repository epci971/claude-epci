---
name: php-symfony
description: >-
  Patterns et conventions pour PHP/Symfony. Inclut Doctrine ORM, PHPUnit,
  Twig, services et bundles. Use when: développement Symfony, composer.json
  avec symfony détecté. Not for: Laravel, plain PHP, autres frameworks.
---

# PHP/Symfony Development Patterns

## Overview

Patterns et conventions pour le développement Symfony moderne.

## Auto-détection

Chargé automatiquement si détection de :
- `composer.json` contenant `symfony/`
- Fichiers `config/packages/*.yaml`
- Structure `src/Controller/`, `src/Entity/`

## Architecture Symfony

### Structure standard

```
project/
├── config/
│   ├── packages/          # Configuration par bundle
│   ├── routes/            # Routes par context
│   └── services.yaml      # Services DI
├── src/
│   ├── Controller/        # HTTP controllers
│   ├── Entity/            # Doctrine entities
│   ├── Repository/        # Doctrine repositories
│   ├── Service/           # Business logic
│   ├── EventListener/     # Event subscribers
│   └── Command/           # Console commands
├── templates/             # Twig templates
├── tests/
│   ├── Unit/
│   └── Functional/
└── public/
    └── index.php          # Front controller
```

### Conventions de nommage Symfony

| Élément | Convention | Exemple |
|---------|------------|---------|
| Controller | `*Controller` | `UserController` |
| Entity | Singulier, PascalCase | `User`, `OrderItem` |
| Repository | `*Repository` | `UserRepository` |
| Service | Nom descriptif | `EmailNotifier` |
| Command | `app:*` | `app:user:create` |

## Doctrine Patterns

### Entity

```php
#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
class User
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255, unique: true)]
    private string $email;

    #[ORM\Column]
    private \DateTimeImmutable $createdAt;

    public function __construct(string $email)
    {
        $this->email = $email;
        $this->createdAt = new \DateTimeImmutable();
    }

    // Getters... (pas de setters publics si possible)
}
```

### Repository

```php
/**
 * @extends ServiceEntityRepository<User>
 */
class UserRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, User::class);
    }

    public function findByEmail(string $email): ?User
    {
        return $this->findOneBy(['email' => $email]);
    }

    /**
     * @return User[]
     */
    public function findActiveUsers(): array
    {
        return $this->createQueryBuilder('u')
            ->andWhere('u.active = :active')
            ->setParameter('active', true)
            ->orderBy('u.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }
}
```

## Controller Patterns

### RESTful Controller

```php
#[Route('/api/users', name: 'api_users_')]
class UserController extends AbstractController
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $em,
    ) {}

    #[Route('', name: 'list', methods: ['GET'])]
    public function list(): JsonResponse
    {
        $users = $this->userRepository->findAll();
        return $this->json($users, context: ['groups' => 'user:read']);
    }

    #[Route('/{id}', name: 'show', methods: ['GET'])]
    public function show(User $user): JsonResponse
    {
        return $this->json($user, context: ['groups' => 'user:read']);
    }

    #[Route('', name: 'create', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        // Validation et création
        return $this->json($user, Response::HTTP_CREATED);
    }
}
```

## Service Patterns

### Service avec injection

```php
class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $em,
        private readonly EventDispatcherInterface $dispatcher,
    ) {}

    public function createUser(string $email): User
    {
        $user = new User($email);

        $this->em->persist($user);
        $this->em->flush();

        $this->dispatcher->dispatch(new UserCreatedEvent($user));

        return $user;
    }
}
```

### Configuration services.yaml

```yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'

    # Services explicites si nécessaire
    App\Service\ExternalApiClient:
        arguments:
            $apiKey: '%env(API_KEY)%'
```

## Testing Patterns (PHPUnit)

### Unit Test

```php
class UserTest extends TestCase
{
    public function testCreateUserWithValidEmail(): void
    {
        $user = new User('test@example.com');

        $this->assertEquals('test@example.com', $user->getEmail());
        $this->assertNotNull($user->getCreatedAt());
    }

    public function testCreateUserWithInvalidEmailThrowsException(): void
    {
        $this->expectException(\InvalidArgumentException::class);

        new User('invalid-email');
    }
}
```

### Functional Test (WebTestCase)

```php
class UserControllerTest extends WebTestCase
{
    public function testListUsers(): void
    {
        $client = static::createClient();
        $client->request('GET', '/api/users');

        $this->assertResponseIsSuccessful();
        $this->assertResponseHeaderSame('Content-Type', 'application/json');
    }

    public function testCreateUser(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/users', [], [], [
            'CONTENT_TYPE' => 'application/json',
        ], json_encode(['email' => 'new@example.com']));

        $this->assertResponseStatusCodeSame(201);
    }
}
```

## Commandes utiles

```bash
# Développement
php bin/console make:entity
php bin/console make:controller
php bin/console make:migration
php bin/console doctrine:migrations:migrate

# Debug
php bin/console debug:router
php bin/console debug:container
php bin/console debug:autowiring

# Tests
php bin/phpunit
php bin/phpunit --filter UserTest
php bin/phpunit --coverage-html coverage/

# Cache
php bin/console cache:clear
```

## Bonnes pratiques Symfony

| Pratique | Faire | Éviter |
|----------|-------|--------|
| Injection | Constructor injection | `$container->get()` |
| Entities | Immutables si possible | Setters publics |
| Controllers | Thin, déléguer aux services | Logique métier |
| Config | Variables d'environnement | Valeurs en dur |
| Validation | Constraints + Validator | Validation manuelle |

## Sécurité Symfony

```php
// Voters pour l'autorisation
#[IsGranted('ROLE_USER')]
#[IsGranted(new Expression('is_granted("EDIT", object)'))]

// CSRF protection
$token = $this->isCsrfTokenValid('delete'.$user->getId(), $request->request->get('_token'));

// Password hashing
$hashedPassword = $passwordHasher->hashPassword($user, $plainPassword);
```
