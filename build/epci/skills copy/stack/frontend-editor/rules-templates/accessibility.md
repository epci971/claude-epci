---
paths:
  - frontend/**/*.tsx
  - frontend/**/*.jsx
  - frontend/**/*.html
---

# Accessibility Rules (WCAG 2.1 AA)

> Conventions accessibilite pour le frontend.

## 🔴 CRITICAL

1. **Contraste couleurs**: 4.5:1 texte, 3:1 elements UI
2. **Focus visible**: Toujours visible sur elements interactifs
3. **Touch targets**: Minimum 44x44px
4. **Alt text**: Toutes les images informatives

## 🟡 CONVENTIONS

### Focus Pattern

```css
/* Applied to all interactive elements */
.interactive {
  @apply focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}
```

### Semantic HTML

```tsx
// Correct structure
<main>
  <h1>Page Title</h1>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
  <article>
    <h2>Section Title</h2>
    <p>Content</p>
  </article>
</main>
```

### Form Labels

```tsx
// Always associate labels
<label htmlFor="email">Email</label>
<input id="email" type="email" aria-describedby="email-help" />
<span id="email-help">We'll never share your email</span>

// Or use aria-label for icon buttons
<button aria-label="Close dialog">
  <XIcon />
</button>
```

### Screen Reader

```tsx
// Visually hidden but screen reader accessible
<span className="sr-only">Description for screen readers</span>

// Skip link
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

## 🟢 PREFERENCES

- Utiliser Radix UI pour composants accessibles
- Tester avec VoiceOver/NVDA
- Aria-live pour contenu dynamique

## Quick Reference

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| Color contrast | 4.5:1 text | Verified tokens |
| Focus visible | Always | `focus:ring-2` |
| Touch targets | >= 44px | Size variants |
| Keyboard nav | Full | Semantic HTML |
| Alt text | Informative images | `alt="description"` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Skip link | `sr-only focus:not-sr-only` | Keyboard nav |
| Live regions | `aria-live="polite"` | Dynamic content |
| Modal focus trap | `@radix-ui/react-dialog` | Keyboard support |
| Disclosure | `@radix-ui/react-disclosure` | Screen reader |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| `div` as button | No keyboard | `<button>` |
| No focus styles | Can't navigate | `focus:ring-2` |
| Color only info | Color blind users | Icons + text |
| Auto-playing media | Disorienting | User control |
| Tiny touch targets | Hard to tap | Min 44px |

## Examples

### Correct

```tsx
// Accessible button
<button
  className={cn(
    "px-4 py-2 min-h-[44px] min-w-[44px]",  // Touch target
    "focus:outline-none focus:ring-2 focus:ring-offset-2",  // Focus
    "bg-primary-600 text-white"  // Contrast verified
  )}
  aria-label={iconOnly ? "Close" : undefined}
>
  {iconOnly ? <XIcon aria-hidden="true" /> : "Close"}
</button>

// Accessible form
<form aria-labelledby="form-title">
  <h2 id="form-title">Contact Form</h2>

  <div>
    <label htmlFor="name">Name *</label>
    <input
      id="name"
      required
      aria-required="true"
      aria-invalid={errors.name ? "true" : undefined}
      aria-describedby={errors.name ? "name-error" : undefined}
    />
    {errors.name && (
      <span id="name-error" role="alert">
        {errors.name}
      </span>
    )}
  </div>
</form>

// Accessible modal
<Dialog>
  <DialogTrigger asChild>
    <Button>Open Modal</Button>
  </DialogTrigger>
  <DialogContent aria-labelledby="dialog-title">
    <DialogTitle id="dialog-title">Edit Profile</DialogTitle>
    <DialogDescription>
      Make changes to your profile here.
    </DialogDescription>
    {/* Focus trapped inside automatically */}
  </DialogContent>
</Dialog>
```

### Incorrect

```tsx
// DON'T DO THIS
<div onClick={handleClick}>  {/* div not focusable! */}
  Click me
</div>

<img src="chart.png" />  {/* Missing alt! */}

<button>  {/* No focus styles! */}
  <XIcon />  {/* No label for icon button! */}
</button>

<span style={{ color: '#999' }}>  {/* Low contrast! */}
  Important info
</span>
```
