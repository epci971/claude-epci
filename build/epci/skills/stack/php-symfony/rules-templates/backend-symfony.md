---
paths:
  - backend/**/*.php
  - config/**/*.yaml
  - "!backend/var/**"
  - "!backend/vendor/**"
---

# Symfony Backend Rules

> Conventions pour le developpement PHP/Symfony.

## 🔴 CRITICAL

1. **Controllers thin**: Max 20 lignes par action, deleguer aux services
2. **Injection constructeur**: Jamais `$container->get()`, toujours autowiring
3. **Pas d'entites dans les reponses API**: Utiliser des DTOs
4. **Declare strict_types**: `declare(strict_types=1);` en premiere ligne

## 🟡 CONVENTIONS

### Architecture

```
src/
├── Controller/            # Thin HTTP controllers
├── Command/               # Console commands
├── Entity/                # Doctrine entities
├── Repository/            # Doctrine repositories
├── Service/               # Business logic (final classes)
├── Dto/                   # Data Transfer Objects
├── Handler/               # Use-case handlers
├── Message/               # Messenger messages
├── MessageHandler/        # Async handlers
├── Event/                 # Domain events
├── Security/Voter/        # Authorization voters
└── Validator/Constraint/  # Custom validation
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Controller | `*Controller`, final | `UserController` |
| Entity | Singular, PascalCase, final | `User` |
| Repository | `*Repository`, final | `UserRepository` |
| Service | Descriptive, final | `EmailNotifier` |
| DTO | `*Dto`, readonly | `CreateUserDto` |
| Message | `*Message`, readonly | `SendEmailMessage` |

### Services

```php
<?php
declare(strict_types=1);

final class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly EntityManagerInterface $entityManager,
    ) {}

    public function createUser(CreateUserDto $dto): User
    {
        $user = new User($dto->email, $dto->name);
        $this->entityManager->persist($user);
        $this->entityManager->flush();
        return $user;
    }
}
```

## 🟢 PREFERENCES

- Utiliser les attributs PHP 8+ pour routing et validation
- Preferer `#[MapRequestPayload]` pour deserialisation
- Events via `EventDispatcherInterface`

## Quick Reference

| Task | Pattern |
|------|---------|
| Route | `#[Route('/api/users', methods: ['GET'])]` |
| Validation | `#[Assert\NotBlank]` sur DTO |
| Auth | `#[IsGranted('ROLE_USER')]` |
| Async | Messenger avec `#[AsMessageHandler]` |
| Cache | Symfony Cache avec tags |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Thin Controller | Delegate to service | Testable |
| Final Services | `final class` | No inheritance issues |
| DTO Validation | `#[MapRequestPayload]` + Assert | Clean validation |
| Voters | `#[IsGranted]` attribute | Centralized auth |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Fat controller | SRP viole | Extract to service |
| `$container->get()` | Service locator | Constructor injection |
| Public setters | Mutable state | Business methods |
| Hardcoded config | Environment-specific | `%env(VAR)%` |

## Examples

### Correct

```php
<?php
declare(strict_types=1);

#[Route('/api/users', name: 'api_users_')]
final class UserController extends AbstractController
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    #[Route('', name: 'create', methods: ['POST'])]
    public function create(
        #[MapRequestPayload] CreateUserDto $dto
    ): JsonResponse {
        $user = $this->userService->createUser($dto);
        return $this->json($user, Response::HTTP_CREATED, [], [
            'groups' => ['user:read']
        ]);
    }
}
```

### Incorrect

```php
// DON'T DO THIS
class UserController extends AbstractController
{
    public function create(Request $request): Response
    {
        // Business logic in controller - BAD
        $user = new User();
        $user->setEmail($request->get('email'));
        $this->getDoctrine()->getManager()->persist($user);
        $this->getDoctrine()->getManager()->flush();
        // Direct entity in response - BAD
        return $this->json($user);
    }
}
```
