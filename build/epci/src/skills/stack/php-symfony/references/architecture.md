# Symfony Architecture Reference

## Project Structure

```
project/
├── bin/
│   └── console                    # CLI entry point
├── config/
│   ├── packages/                  # Bundle configuration
│   │   ├── doctrine.yaml
│   │   ├── framework.yaml
│   │   ├── messenger.yaml
│   │   ├── security.yaml
│   │   └── twig.yaml
│   ├── routes/                    # Route definitions
│   │   └── annotations.yaml
│   ├── bundles.php
│   ├── routes.yaml
│   └── services.yaml              # DI configuration
├── public/
│   └── index.php                  # Front controller
├── src/
│   ├── Controller/                # HTTP controllers
│   ├── Command/                   # Console commands
│   ├── Entity/                    # Doctrine entities
│   ├── Repository/                # Doctrine repositories
│   ├── Service/                   # Business logic services
│   ├── Dto/                       # Data Transfer Objects
│   ├── Handler/                   # Use-case handlers (CQRS)
│   ├── Message/                   # Messenger messages
│   ├── MessageHandler/            # Messenger handlers
│   ├── Event/                     # Domain events
│   ├── EventListener/             # Single event listeners
│   ├── EventSubscriber/           # Multi-event subscribers
│   ├── Form/                      # Form types
│   ├── Validator/                 # Custom constraints
│   │   └── Constraint/
│   ├── Security/
│   │   └── Voter/                 # Authorization voters
│   ├── Bridge/                    # Third-party integrations
│   ├── Factory/                   # Object factories
│   ├── Normalizer/                # Serialization
│   ├── Twig/
│   │   └── Extension/             # Twig extensions
│   └── Kernel.php
├── templates/                     # Twig templates
│   ├── base.html.twig
│   └── <feature>/
├── tests/
│   ├── Unit/
│   ├── Functional/
│   └── bootstrap.php
├── translations/                  # i18n files
│   ├── messages.fr.yaml
│   └── validators.fr.yaml
├── var/
│   ├── cache/
│   └── log/
├── vendor/
├── composer.json
└── symfony.lock
```

## Service Layer Architecture

### Layer Responsibilities

| Layer | Purpose | Contains |
|-------|---------|----------|
| Controller | HTTP handling | Route, validation, response |
| Service | Business logic | Domain rules, orchestration |
| Repository | Data access | Queries, persistence |
| Handler | Use case execution | CQRS command/query handling |

### Service Pattern

```php
<?php

declare(strict_types=1);

namespace App\Service;

use App\Entity\User;
use App\Repository\UserRepository;
use App\Event\UserCreatedEvent;
use Doctrine\ORM\EntityManagerInterface;
use Psr\EventDispatcher\EventDispatcherInterface;

final class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $entityManager,
        private readonly EventDispatcherInterface $eventDispatcher,
    ) {}

    public function createUser(string $email, string $name): User
    {
        // Business logic here
        $user = new User($email, $name);

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $this->eventDispatcher->dispatch(new UserCreatedEvent($user));

        return $user;
    }

    public function activateUser(User $user): void
    {
        if ($user->isActive()) {
            throw new \DomainException('User already active');
        }

        $user->activate();
        $this->entityManager->flush();
    }
}
```

### Handler Pattern (CQRS)

```php
<?php

declare(strict_types=1);

namespace App\Handler;

use App\Message\CreateUserCommand;
use App\Entity\User;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final class CreateUserHandler
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $entityManager,
    ) {}

    public function __invoke(CreateUserCommand $command): User
    {
        // Check business rules
        if ($this->userRepository->findByEmail($command->email)) {
            throw new \DomainException('Email already exists');
        }

        $user = new User($command->email, $command->name);

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        return $user;
    }
}
```

## Dependency Injection Configuration

### services.yaml

```yaml
# config/services.yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true
        public: false  # Services are private by default

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'

    # Controller configuration
    App\Controller\:
        resource: '../src/Controller/'
        tags: ['controller.service_arguments']

    # Explicit service configuration
    App\Service\ExternalApiClient:
        arguments:
            $apiUrl: '%env(API_URL)%'
            $apiKey: '%env(API_KEY)%'
            $timeout: '%env(int:API_TIMEOUT)%'

    # Service with interface binding
    App\Contract\PaymentGatewayInterface:
        class: App\Service\StripePaymentGateway

    # Tagged services
    App\EventListener\AuditListener:
        tags:
            - { name: doctrine.event_listener, event: postPersist }
            - { name: doctrine.event_listener, event: postUpdate }
```

### Environment Variables

```yaml
# .env
APP_ENV=dev
APP_SECRET=your-secret-key
DATABASE_URL="postgresql://user:pass@localhost:5432/db?serverVersion=15"
MESSENGER_TRANSPORT_DSN=doctrine://default?auto_setup=0
REDIS_URL=redis://localhost:6379
MAILER_DSN=smtp://localhost:1025
```

```php
// Access in services
#[Autowire('%env(API_KEY)%')]
private readonly string $apiKey;

// Or in constructor
public function __construct(
    #[Autowire('%env(DATABASE_URL)%')]
    private readonly string $databaseUrl,
) {}
```

## Controller Architecture

### Thin Controller Pattern

```php
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Dto\CreateUserDto;
use App\Service\UserService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\MapRequestPayload;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/api/users', name: 'api_users_')]
final class UserController extends AbstractController
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    #[Route('', name: 'create', methods: ['POST'])]
    #[IsGranted('ROLE_ADMIN')]
    public function create(
        #[MapRequestPayload] CreateUserDto $dto,
    ): JsonResponse {
        // Controller is thin: delegate to service
        $user = $this->userService->createUser(
            $dto->email,
            $dto->name,
        );

        return $this->json($user, Response::HTTP_CREATED, [], [
            'groups' => ['user:read'],
        ]);
    }

    #[Route('/{id}', name: 'show', methods: ['GET'])]
    public function show(User $user): JsonResponse
    {
        // Automatic entity resolution via ParamConverter
        return $this->json($user, Response::HTTP_OK, [], [
            'groups' => ['user:read', 'user:details'],
        ]);
    }
}
```

### DTO Pattern

```php
<?php

declare(strict_types=1);

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

final readonly class CreateUserDto
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Email]
        public string $email,

        #[Assert\NotBlank]
        #[Assert\Length(min: 2, max: 100)]
        public string $name,

        #[Assert\NotBlank]
        #[Assert\Length(min: 8)]
        public string $password,
    ) {}
}
```

## Directory Organization Rules

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `UserController`, `OrderService` |
| Methods | camelCase | `findActiveUsers()`, `createOrder()` |
| Properties | camelCase | `$createdAt`, `$isActive` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Folders | PascalCase | `Controller/`, `EventListener/` |
| Config files | kebab-case | `doctrine.yaml`, `security.yaml` |

### File Limits

| Metric | Limit |
|--------|-------|
| Lines per function | Max 30 |
| Parameters per function | Max 5 |
| Lines per file | Max 300 |
| Files per directory | Max 10 (split into subdirs) |

## Advanced Patterns

### Factory Pattern

```php
<?php

declare(strict_types=1);

namespace App\Factory;

use App\Entity\Order;
use App\Entity\OrderItem;
use App\Dto\CreateOrderDto;

final class OrderFactory
{
    public function createFromDto(CreateOrderDto $dto): Order
    {
        $order = new Order($dto->customerId);

        foreach ($dto->items as $itemDto) {
            $item = new OrderItem(
                $itemDto->productId,
                $itemDto->quantity,
                $itemDto->price,
            );
            $order->addItem($item);
        }

        return $order;
    }
}
```

### Bridge Pattern (Third-Party Integration)

```php
<?php

declare(strict_types=1);

namespace App\Bridge\Stripe;

use App\Contract\PaymentGatewayInterface;
use App\Entity\Payment;
use Stripe\StripeClient;

final class StripePaymentGateway implements PaymentGatewayInterface
{
    public function __construct(
        private readonly StripeClient $client,
        private readonly string $webhookSecret,
    ) {}

    public function createPayment(int $amount, string $currency): Payment
    {
        $intent = $this->client->paymentIntents->create([
            'amount' => $amount,
            'currency' => $currency,
        ]);

        return new Payment($intent->id, $amount, $currency);
    }
}
```
