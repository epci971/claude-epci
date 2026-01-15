---
paths:
  - backend/src/Security/**/*.php
  - backend/config/packages/security.yaml
---

# Symfony Security Rules

> Conventions securite pour Symfony.

## 🔴 CRITICAL

1. **CSRF obligatoire**: Toujours actif sur les forms
2. **Voters pour autorisation**: Jamais de role checks dans le code
3. **Pas de secrets dans le code**: Utiliser secrets:set ou env vars
4. **Hashage passwords**: Toujours via UserPasswordHasherInterface

## 🟡 CONVENTIONS

### Voters

```php
<?php
declare(strict_types=1);

final class PostVoter extends Voter
{
    public const EDIT = 'POST_EDIT';
    public const DELETE = 'POST_DELETE';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::EDIT, self::DELETE])
            && $subject instanceof Post;
    }

    protected function voteOnAttribute(
        string $attribute,
        mixed $subject,
        TokenInterface $token
    ): bool {
        $user = $token->getUser();
        if (!$user instanceof User) {
            return false;
        }

        return match ($attribute) {
            self::EDIT => $subject->getAuthor() === $user,
            self::DELETE => $subject->getAuthor() === $user || $user->isAdmin(),
            default => false,
        };
    }
}
```

### Usage Controller

```php
#[IsGranted('POST_EDIT', subject: 'post')]
public function edit(Post $post): Response
{
    // User can edit
}
```

### CSRF Protection

```php
// Forms - automatic
// Non-form actions
#[IsCsrfTokenValid('delete-post', tokenKey: '_token')]
public function delete(Post $post): Response
{
    // CSRF validated
}
```

## 🟢 PREFERENCES

- Utiliser attributs `#[IsGranted]` plutot que `denyAccessUnlessGranted()`
- Centraliser les roles dans une enum
- Logger les echecs d'authentification

## Quick Reference

| Task | Pattern |
|------|---------|
| Check permission | `#[IsGranted('ROLE_X')]` |
| Voter | `Voter::supports()` + `voteOnAttribute()` |
| CSRF | `#[IsCsrfTokenValid('action', '_token')]` |
| Hash password | `$hasher->hashPassword($user, $plain)` |
| Current user | `$this->getUser()` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Voters | Per-entity authorization | Granular access |
| Role hierarchy | security.yaml | DRY roles |
| Remember me | security.yaml | UX |
| API tokens | Custom authenticator | Stateless API |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Role in code | Scattered, hard to audit | Voters |
| Plain password | Security breach | Always hash |
| CSRF disabled | CSRF attacks | Keep enabled |
| Hardcoded secrets | Exposure risk | env vars / secrets |

## Examples

### Correct

```php
// Voter-based authorization
#[Route('/posts/{id}/edit')]
#[IsGranted('POST_EDIT', subject: 'post')]
public function edit(Post $post): Response
{
    // Authorization already checked
}

// Password handling
public function register(CreateUserDto $dto): User
{
    $user = new User($dto->email);
    $hashedPassword = $this->passwordHasher->hashPassword(
        $user,
        $dto->plainPassword
    );
    $user->setPassword($hashedPassword);
    return $user;
}
```

### Incorrect

```php
// DON'T DO THIS
public function edit(Post $post): Response
{
    // Manual role check - BAD
    if (!$this->getUser()->hasRole('ROLE_EDITOR')) {
        throw new AccessDeniedHttpException();
    }

    // Checking ownership manually - should be in Voter
    if ($post->getAuthor() !== $this->getUser()) {
        throw new AccessDeniedHttpException();
    }
}
```
