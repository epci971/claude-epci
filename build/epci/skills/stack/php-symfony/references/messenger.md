# Symfony Messenger Reference

## Overview

Messenger provides async message handling with queues. Messages are dispatched to a bus and handled by handlers, either synchronously or asynchronously.

## Message Pattern

### Message Definition

```php
<?php

declare(strict_types=1);

namespace App\Message;

/**
 * Messages are simple data objects - no logic.
 * They will be serialized for queue storage.
 */
final readonly class SendWelcomeEmailMessage
{
    public function __construct(
        public int $userId,
        public string $email,
        public string $name,
    ) {}
}

// Command message (modifies state)
final readonly class CreateUserCommand
{
    public function __construct(
        public string $email,
        public string $name,
        public string $password,
    ) {}
}

// Query message (reads state)
final readonly class GetUserByIdQuery
{
    public function __construct(
        public int $userId,
    ) {}
}

// Event message (something happened)
final readonly class UserCreatedEvent
{
    public function __construct(
        public int $userId,
        public \DateTimeImmutable $createdAt,
    ) {}
}
```

### Message Handler

```php
<?php

declare(strict_types=1);

namespace App\MessageHandler;

use App\Message\SendWelcomeEmailMessage;
use App\Service\EmailService;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final class SendWelcomeEmailHandler
{
    public function __construct(
        private readonly EmailService $emailService,
    ) {}

    public function __invoke(SendWelcomeEmailMessage $message): void
    {
        $this->emailService->sendWelcomeEmail(
            $message->email,
            $message->name,
        );
    }
}

// Multiple handlers for same message
#[AsMessageHandler]
final class LogWelcomeEmailHandler
{
    public function __construct(
        private readonly LoggerInterface $logger,
    ) {}

    public function __invoke(SendWelcomeEmailMessage $message): void
    {
        $this->logger->info('Welcome email sent', [
            'userId' => $message->userId,
            'email' => $message->email,
        ]);
    }
}
```

## Configuration

### messenger.yaml

```yaml
# config/packages/messenger.yaml
framework:
    messenger:
        # Uncomment for failed messages handling
        failure_transport: failed

        transports:
            # Async transport using Doctrine
            async:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
                    queue_name: default
                retry_strategy:
                    max_retries: 3
                    delay: 1000
                    multiplier: 2
                    max_delay: 0

            # High priority queue
            async_priority_high:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
                    queue_name: high
                retry_strategy:
                    max_retries: 5
                    delay: 500

            # Failed messages storage
            failed:
                dsn: 'doctrine://default?queue_name=failed'

            # Sync transport for dev/testing
            sync: 'sync://'

        routing:
            # Route messages to transports
            'App\Message\SendWelcomeEmailMessage': async
            'App\Message\ProcessPaymentMessage': async_priority_high
            'App\Message\*': async  # Fallback for all App\Message\*

when@dev:
    framework:
        messenger:
            transports:
                async: 'sync://'  # Process synchronously in dev
                async_priority_high: 'sync://'

when@test:
    framework:
        messenger:
            transports:
                async: 'in-memory://'  # Store in memory for assertions
                async_priority_high: 'in-memory://'
```

### Redis Transport

```yaml
# For production with Redis
framework:
    messenger:
        transports:
            async:
                dsn: 'redis://localhost:6379/messages'
                options:
                    stream: 'symfony_messages'
                    group: 'symfony_consumers'
                    consumer: '%env(HOSTNAME)%'
```

### PostgreSQL Transport (LISTEN/NOTIFY)

```yaml
# Native PostgreSQL pub/sub - performant and transactional
framework:
    messenger:
        transports:
            async:
                dsn: 'doctrine://default?auto_setup=0'
                options:
                    table_name: messenger_messages
                    queue_name: default
```

## Dispatching Messages

### From Controller

```php
<?php

use Symfony\Component\Messenger\MessageBusInterface;
use Symfony\Component\Messenger\Stamp\DelayStamp;

final class UserController extends AbstractController
{
    public function __construct(
        private readonly MessageBusInterface $bus,
    ) {}

    #[Route('/users', methods: ['POST'])]
    public function create(#[MapRequestPayload] CreateUserDto $dto): JsonResponse
    {
        // Dispatch async message
        $this->bus->dispatch(new SendWelcomeEmailMessage(
            userId: $user->getId(),
            email: $user->getEmail(),
            name: $user->getName(),
        ));

        // Dispatch with delay (5 minutes)
        $this->bus->dispatch(
            new FollowUpEmailMessage($user->getId()),
            [new DelayStamp(5 * 60 * 1000)]  // milliseconds
        );

        return $this->json($user, Response::HTTP_CREATED);
    }
}
```

### From Service with Transaction Safety

```php
<?php

use Symfony\Component\Messenger\MessageBusInterface;
use Symfony\Component\Messenger\Stamp\DispatchAfterCurrentBusStamp;

final class UserService
{
    public function __construct(
        private readonly EntityManagerInterface $em,
        private readonly MessageBusInterface $bus,
    ) {}

    public function createUser(string $email): User
    {
        $user = new User($email);

        $this->em->persist($user);
        $this->em->flush();

        // Dispatch AFTER flush succeeds (transaction-safe)
        $this->bus->dispatch(
            new SendWelcomeEmailMessage($user->getId(), $email, $user->getName()),
            [new DispatchAfterCurrentBusStamp()]
        );

        return $user;
    }
}
```

## Worker Commands

```bash
# Consume messages from all transports
php bin/console messenger:consume async

# Consume from multiple transports with priority
php bin/console messenger:consume async_priority_high async

# Limit and memory management
php bin/console messenger:consume async \
    --limit=100 \
    --memory-limit=128M \
    --time-limit=3600

# Stop workers gracefully
php bin/console messenger:stop-workers

# Failed messages
php bin/console messenger:failed:show
php bin/console messenger:failed:retry
php bin/console messenger:failed:remove <id>
```

## Supervisor Configuration

```ini
# /etc/supervisor/conf.d/messenger-worker.conf
[program:messenger-consume]
command=php /var/www/app/bin/console messenger:consume async async_priority_high --time-limit=3600
user=www-data
numprocs=2
startsecs=0
autostart=true
autorestart=true
process_name=%(program_name)s_%(process_num)02d
stdout_logfile=/var/log/supervisor/messenger.log
stderr_logfile=/var/log/supervisor/messenger_error.log
```

## Testing Messages

```php
<?php

use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;
use Symfony\Component\Messenger\Transport\InMemoryTransport;

final class UserCreationTest extends KernelTestCase
{
    public function testWelcomeEmailIsDispatched(): void
    {
        self::bootKernel();

        $userService = self::getContainer()->get(UserService::class);
        $userService->createUser('test@example.com');

        /** @var InMemoryTransport $transport */
        $transport = self::getContainer()->get('messenger.transport.async');

        $this->assertCount(1, $transport->getSent());

        $envelope = $transport->getSent()[0];
        $message = $envelope->getMessage();

        $this->assertInstanceOf(SendWelcomeEmailMessage::class, $message);
        $this->assertEquals('test@example.com', $message->email);
    }
}
```

## Error Handling

### Custom Exception Handling

```php
<?php

use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Symfony\Component\Messenger\Exception\RecoverableMessageHandlingException;
use Symfony\Component\Messenger\Exception\UnrecoverableMessageHandlingException;

#[AsMessageHandler]
final class ProcessPaymentHandler
{
    public function __invoke(ProcessPaymentMessage $message): void
    {
        try {
            $this->paymentGateway->process($message->amount);
        } catch (TemporaryFailureException $e) {
            // Will be retried according to retry_strategy
            throw new RecoverableMessageHandlingException(
                'Payment gateway temporarily unavailable',
                previous: $e,
            );
        } catch (InvalidCardException $e) {
            // Will NOT be retried - goes directly to failed transport
            throw new UnrecoverableMessageHandlingException(
                'Invalid card',
                previous: $e,
            );
        }
    }
}
```

## CQRS Pattern with Messenger

```php
<?php

// Command Bus
final readonly class CommandBus
{
    public function __construct(
        #[Autowire('@messenger.bus.commands')]
        private MessageBusInterface $commandBus,
    ) {}

    public function dispatch(object $command): void
    {
        $this->commandBus->dispatch($command);
    }
}

// Query Bus (synchronous)
final readonly class QueryBus
{
    public function __construct(
        #[Autowire('@messenger.bus.queries')]
        private MessageBusInterface $queryBus,
    ) {}

    public function query(object $query): mixed
    {
        $envelope = $this->queryBus->dispatch($query);
        $handledStamp = $envelope->last(HandledStamp::class);

        return $handledStamp?->getResult();
    }
}
```

```yaml
# config/packages/messenger.yaml
framework:
    messenger:
        default_bus: messenger.bus.commands

        buses:
            messenger.bus.commands:
                middleware:
                    - doctrine_transaction

            messenger.bus.queries:
                middleware:
                    - validation
```
