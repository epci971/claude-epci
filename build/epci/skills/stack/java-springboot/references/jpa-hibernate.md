# Spring Data JPA & Hibernate Reference

## Entity Patterns

### Basic Entity with Lombok

```java
@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false)
    private Boolean active = true;

    @Version
    private Long version;
}
```

### Equals and HashCode

```java
@Entity
@Getter
@Setter
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NaturalId
    @Column(nullable = false, unique = true)
    private String email;

    // Use business key (NaturalId) for equals/hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User other)) return false;
        return email != null && email.equals(other.getEmail());
    }

    @Override
    public int hashCode() {
        return Objects.hash(email);
    }
}
```

### Value Objects with @Embeddable

```java
@Embeddable
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class Address {
    private String street;
    private String city;
    private String zipCode;
    private String country;
}

@Entity
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Embedded
    private Address billingAddress;

    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name = "street", column = @Column(name = "shipping_street")),
        @AttributeOverride(name = "city", column = @Column(name = "shipping_city"))
    })
    private Address shippingAddress;
}
```

## Repository Patterns

### JpaRepository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived query methods
    Optional<User> findByEmail(String email);
    List<User> findByActiveTrue();
    List<User> findByNameContainingIgnoreCase(String name);
    boolean existsByEmail(String email);
    long countByActive(Boolean active);

    // Custom JPQL
    @Query("SELECT u FROM User u WHERE u.createdAt > :date")
    List<User> findRecentUsers(@Param("date") LocalDateTime date);

    // Native SQL
    @Query(value = "SELECT * FROM users WHERE email LIKE %:domain", nativeQuery = true)
    List<User> findByEmailDomain(@Param("domain") String domain);

    // Modifying queries
    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.lastLoginAt < :date")
    int deactivateInactiveUsers(@Param("date") LocalDateTime date);
}
```

### Pagination and Sorting

```java
public interface UserRepository extends JpaRepository<User, Long> {

    Page<User> findByActive(Boolean active, Pageable pageable);

    @Query("SELECT u FROM User u WHERE u.department = :dept")
    Slice<User> findByDepartment(@Param("dept") String department, Pageable pageable);
}

// Usage
Pageable pageable = PageRequest.of(0, 20, Sort.by("createdAt").descending());
Page<User> users = userRepository.findByActive(true, pageable);
```

### Specifications (Dynamic Queries)

```java
public class UserSpecifications {

    public static Specification<User> hasEmail(String email) {
        return (root, query, cb) ->
            email == null ? null : cb.equal(root.get("email"), email);
    }

    public static Specification<User> isActive() {
        return (root, query, cb) -> cb.isTrue(root.get("active"));
    }

    public static Specification<User> nameLike(String name) {
        return (root, query, cb) ->
            name == null ? null : cb.like(cb.lower(root.get("name")),
                "%" + name.toLowerCase() + "%");
    }

    public static Specification<User> createdAfter(LocalDateTime date) {
        return (root, query, cb) ->
            date == null ? null : cb.greaterThan(root.get("createdAt"), date);
    }
}

// Usage
Specification<User> spec = Specification
    .where(UserSpecifications.isActive())
    .and(UserSpecifications.nameLike("john"))
    .and(UserSpecifications.createdAfter(LocalDateTime.now().minusDays(30)));

List<User> users = userRepository.findAll(spec);
```

## Entity Relations

### OneToMany / ManyToOne

```java
@Entity
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines = new ArrayList<>();

    // Helper methods for bidirectional sync
    public void addLine(OrderLine line) {
        lines.add(line);
        line.setOrder(this);
    }

    public void removeLine(OrderLine line) {
        lines.remove(line);
        line.setOrder(null);
    }
}

@Entity
public class OrderLine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    private Integer quantity;
}
```

### Fetch Strategies

| Strategy | Default For | Use Case |
|----------|-------------|----------|
| EAGER | @ManyToOne, @OneToOne | Rarely recommended |
| LAZY | @OneToMany, @ManyToMany | Default choice |

```java
// Always use LAZY and fetch explicitly when needed
@ManyToOne(fetch = FetchType.LAZY)
private Customer customer;
```

## N+1 Prevention

### JOIN FETCH

```java
@Query("SELECT o FROM Order o " +
       "JOIN FETCH o.customer " +
       "JOIN FETCH o.lines l " +
       "JOIN FETCH l.product " +
       "WHERE o.id = :id")
Optional<Order> findByIdWithDetails(@Param("id") Long id);
```

### EntityGraph

```java
@Entity
@NamedEntityGraph(
    name = "Order.withDetails",
    attributeNodes = {
        @NamedAttributeNode("customer"),
        @NamedAttributeNode(value = "lines", subgraph = "lines-subgraph")
    },
    subgraphs = {
        @NamedSubgraph(name = "lines-subgraph",
            attributeNodes = @NamedAttributeNode("product"))
    }
)
public class Order { ... }

// Repository
@EntityGraph(value = "Order.withDetails", type = EntityGraph.EntityGraphType.FETCH)
Optional<Order> findById(Long id);

// Or dynamic
@EntityGraph(attributePaths = {"customer", "lines", "lines.product"})
List<Order> findByCustomerId(Long customerId);
```

### Batch Fetching

```yaml
# application.yml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 25
```

```java
// Or per-collection
@OneToMany(mappedBy = "order")
@BatchSize(size = 25)
private List<OrderLine> lines;
```

### Projection for Read-Only

```java
// Interface projection
public interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}

@Query("SELECT u.id as id, u.name as name, u.email as email FROM User u")
List<UserSummary> findAllSummaries();

// Record projection
public record UserDto(Long id, String name, String email) {}

@Query("SELECT new com.example.dto.UserDto(u.id, u.name, u.email) FROM User u")
List<UserDto> findAllDtos();
```

## Auditing

### Basic Auditing

```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {

    @Bean
    public AuditorAware<String> auditorProvider() {
        return () -> Optional.ofNullable(SecurityContextHolder.getContext())
                .map(SecurityContext::getAuthentication)
                .filter(Authentication::isAuthenticated)
                .map(Authentication::getName);
    }
}

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
@Getter
@Setter
public abstract class BaseEntity {

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String updatedBy;
}

@Entity
public class User extends BaseEntity {
    // Inherits audit fields
}
```

## Database Migrations

Use **Flyway** or **Liquibase** for version-controlled schema migrations:

```yaml
# Flyway configuration
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
```

Migration files: `V1__create_users.sql`, `V2__add_index.sql`

## Best Practices

| Practice | Do | Avoid |
|----------|-----|-------|
| Fetch | LAZY + explicit fetch | EAGER everywhere |
| Relations | Bidirectional helpers | Direct field access |
| Queries | Projections for reads | Full entity loads |
| IDs | Natural ID for equals | Generated ID in equals |
| Batch | Configure batch size | Default N+1 |
| Audit | @EntityListeners | Manual timestamps |
| Migrations | Flyway/Liquibase | hibernate.hbm2ddl.auto |

## Common Pitfalls

- **N+1**: Always use JOIN FETCH or EntityGraph for associations
- **equals/hashCode**: Use business key (email), not generated ID
