# Symfony Security Reference

## Security Configuration

### security.yaml

```yaml
# config/packages/security.yaml
security:
    # Password hashing
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface:
            algorithm: auto  # Uses Argon2i if available, bcrypt otherwise

    # User providers
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email

    # Firewalls
    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false

        api:
            pattern: ^/api
            stateless: true
            provider: app_user_provider
            jwt: ~  # Using lexik/jwt-authentication-bundle

        main:
            lazy: true
            provider: app_user_provider
            form_login:
                login_path: app_login
                check_path: app_login
                enable_csrf: true
            logout:
                path: app_logout
            remember_me:
                secret: '%kernel.secret%'
                lifetime: 604800  # 1 week

    # Role hierarchy
    role_hierarchy:
        ROLE_ADMIN: ROLE_USER
        ROLE_SUPER_ADMIN: [ROLE_ADMIN, ROLE_ALLOWED_TO_SWITCH]

    # Access control
    access_control:
        - { path: ^/login$, roles: PUBLIC_ACCESS }
        - { path: ^/register, roles: PUBLIC_ACCESS }
        - { path: ^/api/login, roles: PUBLIC_ACCESS }
        - { path: ^/api/docs, roles: PUBLIC_ACCESS }
        - { path: ^/admin, roles: ROLE_ADMIN }
        - { path: ^/api, roles: ROLE_USER }
        - { path: ^/, roles: ROLE_USER }
```

## User Entity

```php
<?php

declare(strict_types=1);

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
final class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255, unique: true)]
    private string $email;

    #[ORM\Column]
    private string $password;

    /** @var array<string> */
    #[ORM\Column(type: 'json')]
    private array $roles = [];

    public function getUserIdentifier(): string
    {
        return $this->email;
    }

    /**
     * @return array<string>
     */
    public function getRoles(): array
    {
        $roles = $this->roles;
        $roles[] = 'ROLE_USER';  // Guarantee every user has ROLE_USER

        return array_unique($roles);
    }

    public function getPassword(): string
    {
        return $this->password;
    }

    public function setPassword(string $hashedPassword): void
    {
        $this->password = $hashedPassword;
    }

    public function eraseCredentials(): void
    {
        // Clear any temporary sensitive data
    }
}
```

## Voters (Fine-Grained Authorization)

```php
<?php

declare(strict_types=1);

namespace App\Security\Voter;

use App\Entity\Post;
use App\Entity\User;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\Voter\Voter;

final class PostVoter extends Voter
{
    public const VIEW = 'POST_VIEW';
    public const EDIT = 'POST_EDIT';
    public const DELETE = 'POST_DELETE';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::VIEW, self::EDIT, self::DELETE])
            && $subject instanceof Post;
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();

        // Visitors can view published posts
        if ($attribute === self::VIEW && $subject->isPublished()) {
            return true;
        }

        // Other actions require authentication
        if (!$user instanceof User) {
            return false;
        }

        /** @var Post $post */
        $post = $subject;

        return match ($attribute) {
            self::VIEW => $this->canView($post, $user),
            self::EDIT => $this->canEdit($post, $user),
            self::DELETE => $this->canDelete($post, $user),
            default => false,
        };
    }

    private function canView(Post $post, User $user): bool
    {
        // User can view their own posts
        return $post->getAuthor() === $user || $post->isPublished();
    }

    private function canEdit(Post $post, User $user): bool
    {
        // Only author can edit
        return $post->getAuthor() === $user;
    }

    private function canDelete(Post $post, User $user): bool
    {
        // Author or admin can delete
        return $post->getAuthor() === $user
            || in_array('ROLE_ADMIN', $user->getRoles());
    }
}
```

## Controller Authorization

```php
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Post;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/posts')]
final class PostController extends AbstractController
{
    // Method-level authorization
    #[Route('/{id}/edit', methods: ['GET', 'POST'])]
    #[IsGranted('POST_EDIT', subject: 'post')]
    public function edit(Post $post): Response
    {
        // User is guaranteed to have POST_EDIT permission
        return $this->render('post/edit.html.twig', [
            'post' => $post,
        ]);
    }

    // Programmatic check
    #[Route('/{id}/delete', methods: ['POST'])]
    public function delete(Post $post): Response
    {
        $this->denyAccessUnlessGranted('POST_DELETE', $post);

        // Proceed with deletion
        return $this->redirectToRoute('post_index');
    }

    // Role-based
    #[Route('/admin/all')]
    #[IsGranted('ROLE_ADMIN')]
    public function adminList(): Response
    {
        return $this->render('post/admin_list.html.twig');
    }

    // Expression-based
    #[IsGranted(new Expression('is_granted("ROLE_ADMIN") or object.getAuthor() == user'))]
    public function conditionalAccess(Post $post): Response
    {
        // ...
    }
}
```

## CSRF Protection

### In Forms

```php
<?php

// Form type - CSRF enabled by default
final class PostType extends AbstractType
{
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Post::class,
            'csrf_protection' => true,  // Default
            'csrf_field_name' => '_token',
            'csrf_token_id' => 'post_item',
        ]);
    }
}
```

### In Controllers (Non-Form Actions)

```php
<?php

use Symfony\Component\Security\Http\Attribute\IsCsrfTokenValid;

final class PostController extends AbstractController
{
    // Using attribute (Symfony 7.1+)
    #[Route('/{id}/delete', methods: ['POST'])]
    #[IsCsrfTokenValid('delete-post', tokenKey: '_token')]
    public function delete(Post $post): Response
    {
        // Token already validated
        $this->entityManager->remove($post);
        $this->entityManager->flush();

        return $this->redirectToRoute('post_index');
    }

    // Manual validation
    #[Route('/{id}/archive', methods: ['POST'])]
    public function archive(Post $post, Request $request): Response
    {
        $token = $request->request->get('_token');

        if (!$this->isCsrfTokenValid('archive-' . $post->getId(), $token)) {
            throw $this->createAccessDeniedException('Invalid CSRF token');
        }

        // Proceed
    }
}
```

### In Twig Templates

```twig
{# For forms #}
{{ form_start(form) }}
    {# CSRF token automatically included #}
{{ form_end(form) }}

{# For non-form actions #}
<form action="{{ path('post_delete', {id: post.id}) }}" method="POST">
    <input type="hidden" name="_token" value="{{ csrf_token('delete-post') }}">
    <button type="submit">Delete</button>
</form>
```

## Password Hashing

```php
<?php

use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

final class UserService
{
    public function __construct(
        private readonly UserPasswordHasherInterface $passwordHasher,
        private readonly EntityManagerInterface $entityManager,
    ) {}

    public function createUser(string email, string $plainPassword): User
    {
        $user = new User();
        $user->setEmail($email);

        // Hash password
        $hashedPassword = $this->passwordHasher->hashPassword(
            $user,
            $plainPassword,
        );
        $user->setPassword($hashedPassword);

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        return $user;
    }

    public function changePassword(User $user, string $newPassword): void
    {
        $hashedPassword = $this->passwordHasher->hashPassword(
            $user,
            $newPassword,
        );
        $user->setPassword($hashedPassword);

        $this->entityManager->flush();
    }
}
```

## JWT Authentication (API)

```yaml
# config/packages/lexik_jwt_authentication.yaml
lexik_jwt_authentication:
    secret_key: '%env(resolve:JWT_SECRET_KEY)%'
    public_key: '%env(resolve:JWT_PUBLIC_KEY)%'
    pass_phrase: '%env(JWT_PASSPHRASE)%'
    token_ttl: 3600  # 1 hour
```

```php
<?php

#[Route('/api/login', name: 'api_login', methods: ['POST'])]
public function login(#[CurrentUser] ?User $user): JsonResponse
{
    if (null === $user) {
        return $this->json([
            'message' => 'Missing credentials',
        ], Response::HTTP_UNAUTHORIZED);
    }

    // Return JWT token (handled by lexik/jwt-authentication-bundle)
    return $this->json([
        'user' => $user->getUserIdentifier(),
    ]);
}
```

## Security Headers

```yaml
# config/packages/nelmio_security.yaml
nelmio_security:
    content_type:
        nosniff: true
    xss_protection:
        enabled: true
        mode_block: true
    forced_ssl:
        enabled: true
        hsts_max_age: 31536000  # 1 year
        hsts_subdomains: true
    csp:
        enabled: true
        hosts: []
        content_types: []
        enforce:
            default-src: ['self']
            script-src: ['self']
            style-src: ['self', 'unsafe-inline']
            img-src: ['self', 'data:', 'https:']
```

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Password storage | Use `password_hashers` | Store plain text |
| Authorization | Use Voters | Check roles manually |
| CSRF | Enable for all forms | Disable without reason |
| Secrets | Environment variables | Hardcode in config |
| Sessions | HTTPS only | HTTP cookies |
| User input | Validate and sanitize | Trust user data |
