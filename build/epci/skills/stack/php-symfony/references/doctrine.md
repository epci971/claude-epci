# Doctrine ORM Reference

## Entity Definition

### Best Practice Entity

```php
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Attribute\Groups;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'users')]
#[ORM\Index(columns: ['email'], name: 'idx_user_email')]
#[ORM\Index(columns: ['status', 'created_at'], name: 'idx_user_status_created')]
#[ORM\HasLifecycleCallbacks]
final class User
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    #[Groups(['user:read'])]
    private ?int $id = null;

    #[ORM\Column(length: 255, unique: true)]
    #[Groups(['user:read'])]
    private string $email;

    #[ORM\Column(length: 100)]
    #[Groups(['user:read'])]
    private string $name;

    #[ORM\Column(length: 20)]
    #[Groups(['user:read'])]
    private string $status = self::STATUS_PENDING;

    #[ORM\Column(type: Types::DATETIME_IMMUTABLE)]
    #[Groups(['user:read'])]
    private \DateTimeImmutable $createdAt;

    #[ORM\Column(type: Types::DATETIME_IMMUTABLE, nullable: true)]
    private ?\DateTimeImmutable $updatedAt = null;

    public const STATUS_PENDING = 'pending';
    public const STATUS_ACTIVE = 'active';
    public const STATUS_SUSPENDED = 'suspended';

    public function __construct(string $email, string $name)
    {
        $this->email = $email;
        $this->name = $name;
        $this->createdAt = new \DateTimeImmutable();
    }

    // Getters
    public function getId(): ?int
    {
        return $this->id;
    }

    public function getEmail(): string
    {
        return $this->email;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function getStatus(): string
    {
        return $this->status;
    }

    public function isActive(): bool
    {
        return $this->status === self::STATUS_ACTIVE;
    }

    // Business methods (no setters for protected properties)
    public function activate(): void
    {
        if ($this->status !== self::STATUS_PENDING) {
            throw new \DomainException('Only pending users can be activated');
        }
        $this->status = self::STATUS_ACTIVE;
    }

    public function suspend(): void
    {
        $this->status = self::STATUS_SUSPENDED;
    }

    public function updateName(string $name): void
    {
        $this->name = $name;
    }

    #[ORM\PreUpdate]
    public function onPreUpdate(): void
    {
        $this->updatedAt = new \DateTimeImmutable();
    }
}
```

### Relations

```php
<?php

declare(strict_types=1);

namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
final class Order
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    // ManyToOne - Eager loading by default
    #[ORM\ManyToOne(targetEntity: User::class)]
    #[ORM\JoinColumn(nullable: false)]
    private User $customer;

    // OneToMany with cascade and orphan removal
    #[ORM\OneToMany(
        targetEntity: OrderItem::class,
        mappedBy: 'order',
        cascade: ['persist', 'remove'],
        orphanRemoval: true,
    )]
    private Collection $items;

    // ManyToMany with join table
    #[ORM\ManyToMany(targetEntity: Tag::class)]
    #[ORM\JoinTable(name: 'order_tags')]
    private Collection $tags;

    public function __construct(User $customer)
    {
        $this->customer = $customer;
        $this->items = new ArrayCollection();
        $this->tags = new ArrayCollection();
    }

    public function addItem(OrderItem $item): self
    {
        if (!$this->items->contains($item)) {
            $this->items->add($item);
            $item->setOrder($this);
        }
        return $this;
    }

    public function removeItem(OrderItem $item): self
    {
        if ($this->items->removeElement($item)) {
            if ($item->getOrder() === $this) {
                $item->setOrder(null);
            }
        }
        return $this;
    }

    /**
     * @return Collection<int, OrderItem>
     */
    public function getItems(): Collection
    {
        return $this->items;
    }
}
```

## Repository Patterns

### Custom Repository

```php
<?php

declare(strict_types=1);

namespace App\Repository;

use App\Entity\User;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\ORM\QueryBuilder;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<User>
 */
final class UserRepository extends ServiceEntityRepository
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
            ->andWhere('u.status = :status')
            ->setParameter('status', User::STATUS_ACTIVE)
            ->orderBy('u.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }

    /**
     * @return User[]
     */
    public function findByFilters(array $filters, int $page = 1, int $limit = 20): array
    {
        $qb = $this->createActiveUsersQueryBuilder();

        if (!empty($filters['search'])) {
            $qb->andWhere('u.name LIKE :search OR u.email LIKE :search')
               ->setParameter('search', '%' . $filters['search'] . '%');
        }

        if (!empty($filters['status'])) {
            $qb->andWhere('u.status = :status')
               ->setParameter('status', $filters['status']);
        }

        return $qb
            ->setFirstResult(($page - 1) * $limit)
            ->setMaxResults($limit)
            ->getQuery()
            ->getResult();
    }

    public function countByStatus(string $status): int
    {
        return (int) $this->createQueryBuilder('u')
            ->select('COUNT(u.id)')
            ->andWhere('u.status = :status')
            ->setParameter('status', $status)
            ->getQuery()
            ->getSingleScalarResult();
    }

    private function createActiveUsersQueryBuilder(): QueryBuilder
    {
        return $this->createQueryBuilder('u')
            ->andWhere('u.status != :suspended')
            ->setParameter('suspended', User::STATUS_SUSPENDED);
    }
}
```

### N+1 Prevention

```php
<?php

// BAD - N+1 queries
$orders = $orderRepository->findAll();
foreach ($orders as $order) {
    echo $order->getCustomer()->getName(); // 1 query per order!
}

// GOOD - Eager loading with JOIN
public function findAllWithCustomer(): array
{
    return $this->createQueryBuilder('o')
        ->select('o', 'c')  // Select both
        ->join('o.customer', 'c')
        ->getQuery()
        ->getResult();
}

// GOOD - Explicit fetch join
public function findOrderWithItems(int $id): ?Order
{
    return $this->createQueryBuilder('o')
        ->select('o', 'i', 'p')
        ->leftJoin('o.items', 'i')
        ->leftJoin('i.product', 'p')
        ->andWhere('o.id = :id')
        ->setParameter('id', $id)
        ->getQuery()
        ->getOneOrNullResult();
}
```

### Batch Processing

```php
<?php

use Doctrine\ORM\EntityManagerInterface;

final class UserBatchProcessor
{
    private const BATCH_SIZE = 100;

    public function __construct(
        private readonly EntityManagerInterface $entityManager,
    ) {}

    public function processLargeDataset(iterable $items): int
    {
        $count = 0;

        foreach ($items as $item) {
            // Process item
            $user = new User($item['email'], $item['name']);
            $this->entityManager->persist($user);

            if (++$count % self::BATCH_SIZE === 0) {
                $this->entityManager->flush();
                $this->entityManager->clear(); // Detach all entities
            }
        }

        // Flush remaining
        $this->entityManager->flush();
        $this->entityManager->clear();

        return $count;
    }
}
```

## Migrations

### Creating Migrations

```bash
# Generate migration from entity changes
php bin/console make:migration

# Generate empty migration for manual SQL
php bin/console doctrine:migrations:generate

# Apply migrations
php bin/console doctrine:migrations:migrate

# Rollback
php bin/console doctrine:migrations:migrate prev

# Status
php bin/console doctrine:migrations:status
```

### Migration Example

```php
<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

final class Version20241201000000 extends AbstractMigration
{
    public function getDescription(): string
    {
        return 'Add status column to users table';
    }

    public function up(Schema $schema): void
    {
        $this->addSql("ALTER TABLE users ADD status VARCHAR(20) NOT NULL DEFAULT 'pending'");
        $this->addSql("UPDATE users SET status = 'active' WHERE is_active = true");
        $this->addSql('CREATE INDEX idx_user_status ON users (status)');
    }

    public function down(Schema $schema): void
    {
        $this->addSql('DROP INDEX idx_user_status');
        $this->addSql('ALTER TABLE users DROP COLUMN status');
    }
}
```

## Query Optimization

### Indexes

```php
#[ORM\Entity]
#[ORM\Table(name: 'orders')]
#[ORM\Index(columns: ['status'], name: 'idx_order_status')]
#[ORM\Index(columns: ['customer_id', 'created_at'], name: 'idx_order_customer_date')]
#[ORM\UniqueConstraint(columns: ['reference'], name: 'uniq_order_reference')]
final class Order
{
    // ...
}
```

### Partial Selects

```php
// Select only needed fields (for read-only operations)
public function findEmailsForNotification(): array
{
    return $this->createQueryBuilder('u')
        ->select('u.id', 'u.email', 'u.name')
        ->andWhere('u.status = :active')
        ->setParameter('active', User::STATUS_ACTIVE)
        ->getQuery()
        ->getArrayResult(); // Returns arrays, not entities
}
```

### Native Queries (Last Resort)

```php
// Use only when DQL is not sufficient
public function findComplexStats(): array
{
    $conn = $this->getEntityManager()->getConnection();

    $sql = '
        SELECT
            DATE_TRUNC(\'month\', created_at) as month,
            COUNT(*) as total,
            SUM(CASE WHEN status = :active THEN 1 ELSE 0 END) as active
        FROM users
        GROUP BY DATE_TRUNC(\'month\', created_at)
        ORDER BY month DESC
    ';

    return $conn->executeQuery($sql, [
        'active' => User::STATUS_ACTIVE,
    ])->fetchAllAssociative();
}
```

## doctrine.yaml Configuration

```yaml
# config/packages/doctrine.yaml
doctrine:
    dbal:
        url: '%env(resolve:DATABASE_URL)%'
        profiling_collect_backtrace: '%kernel.debug%'
        use_savepoints: true

    orm:
        auto_generate_proxy_classes: true
        enable_lazy_ghost_objects: true
        report_fields_where_declared: true
        validate_xml_mapping: true
        naming_strategy: doctrine.orm.naming_strategy.underscore_number_aware
        auto_mapping: true
        mappings:
            App:
                type: attribute
                is_bundle: false
                dir: '%kernel.project_dir%/src/Entity'
                prefix: 'App\Entity'
                alias: App

when@prod:
    doctrine:
        orm:
            auto_generate_proxy_classes: false
            proxy_dir: '%kernel.build_dir%/doctrine/orm/Proxies'
            query_cache_driver:
                type: pool
                pool: doctrine.system_cache_pool
            result_cache_driver:
                type: pool
                pool: doctrine.result_cache_pool
```
