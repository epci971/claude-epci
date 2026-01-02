---
paths:
  - backend/**/security/**/*.java
  - backend/**/config/SecurityConfig.java
---

# Spring Security Rules

> Conventions securite pour Spring Boot.

## 🔴 CRITICAL

1. **CSRF actif pour sessions**: Desactiver uniquement pour APIs stateless
2. **Passwords hashes**: Toujours BCrypt via PasswordEncoder
3. **Pas de secrets dans le code**: application.yml avec env vars
4. **Authorization explicite**: Configurer chaque endpoint

## 🟡 CONVENTIONS

### Security Configuration

```java
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final JwtAuthFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(csrf -> csrf.disable())  // OK for stateless API
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/public/**").permitAll()
                        .requestMatchers("/api/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated())
                .sessionManagement(session ->
                        session.sessionCreationPolicy(STATELESS))
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
                .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### JWT Filter Pattern

```java
@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {
    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain chain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            chain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7);
        String username = jwtService.extractUsername(token);

        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);
            if (jwtService.isTokenValid(token, userDetails)) {
                var authToken = new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        chain.doFilter(request, response);
    }
}
```

## 🟢 PREFERENCES

- Utiliser `@PreAuthorize` pour methode-level security
- Centraliser les roles dans enum
- Logger les echecs d'auth

## Quick Reference

| Task | Pattern |
|------|---------|
| Public endpoint | `.requestMatchers("/public/**").permitAll()` |
| Role required | `.hasRole("ADMIN")` |
| Method security | `@PreAuthorize("hasRole('ADMIN')")` |
| Current user | `@AuthenticationPrincipal` |
| Hash password | `passwordEncoder.encode(raw)` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| JWT stateless | Custom filter | Scalable |
| Role hierarchy | RoleHierarchy bean | DRY roles |
| Method security | `@EnableMethodSecurity` | Granular |
| Audit | Spring Data JPA Auditing | Traceability |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| CSRF off + session | Vulnerable | Keep CSRF |
| Plain password | Security breach | BCrypt |
| permitAll default | Wide open | Authenticated default |
| Secrets in code | Exposure | Environment vars |

## Examples

### Correct

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/me")
    public ResponseEntity<UserResponse> getCurrentUser(
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(
                userService.getByEmail(userDetails.getUsername())
        );
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or #id == principal.id")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}

// Password handling
public User register(RegisterRequest request) {
    String hashedPassword = passwordEncoder.encode(request.getPassword());
    return userRepository.save(
            User.builder()
                    .email(request.getEmail())
                    .password(hashedPassword)
                    .build()
    );
}
```

### Incorrect

```java
// DON'T DO THIS
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .authorizeHttpRequests(auth -> auth
                        .anyRequest().permitAll())  // Wide open!
                .build();
    }
}

// Plain password storage
user.setPassword(request.getPassword());  // Not hashed!
```
