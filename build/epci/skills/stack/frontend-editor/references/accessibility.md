# Accessibility Reference — WCAG 2.1 AA

## Color Contrast

### Requirements

| Element | Ratio | Example |
|---------|-------|---------|
| Normal text (<18px) | 4.5:1 | `text-gray-700` on white: 5.3:1 |
| Large text (>=18px bold, >=24px) | 3:1 | `text-gray-500` on white: 4.6:1 |
| UI components | 3:1 | Borders, icons, focus rings |
| Disabled elements | N/A | No requirement |

### Verified Color Tokens

```javascript
// All pass WCAG AA on white background
primary-600: '#2563eb' // 4.52:1 ✓
gray-700: '#374151'    // 5.3:1 ✓
red-600: '#dc2626'     // 4.53:1 ✓
green-700: '#15803d'   // 4.87:1 ✓
```

### Testing

```bash
# Use contrast checker tools
npx @axe-core/cli https://localhost:3000

# Or browser DevTools
# Chrome: Lighthouse > Accessibility
# Firefox: Accessibility Inspector
```

## Focus Management

### Focus Indicators

Every interactive element must have visible focus:

```css
/* Standard focus ring pattern */
.focusable {
  @apply focus:outline-none;
  @apply focus:ring-2;
  @apply focus:ring-offset-2;
  @apply focus:ring-primary-500;
}

/* Focus-visible for keyboard only */
.keyboard-focus {
  @apply focus:outline-none;
  @apply focus-visible:ring-2;
  @apply focus-visible:ring-offset-2;
  @apply focus-visible:ring-primary-500;
}
```

### Skip Links

```html
<!-- First element in body -->
<a
  href="#main-content"
  class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:p-4 focus:bg-white"
>
  Skip to main content
</a>

<!-- Main content target -->
<main id="main-content" tabindex="-1">
  <!-- Page content -->
</main>
```

### Focus Trap (Modals)

```typescript
// Use @radix-ui/react-dialog or similar
// Focus automatically trapped within modal
// Escape key closes modal
// Focus returns to trigger on close
```

## Keyboard Navigation

### Required Support

| Element | Keys | Behavior |
|---------|------|----------|
| Button | Enter, Space | Activate |
| Link | Enter | Navigate |
| Checkbox | Space | Toggle |
| Radio | Arrows | Select option |
| Select | Arrows, Enter | Open/select |
| Modal | Escape | Close |
| Dropdown | Arrows, Enter, Escape | Navigate/select/close |
| Tabs | Arrows | Switch tabs |

### Implementation

```typescript
// Button with keyboard support (native)
<button onClick={handleClick}>
  Click me
</button>

// Custom interactive element
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Custom button
</div>
```

### Tab Order

```html
<!-- Natural order (preferred) -->
<button>First</button>
<button>Second</button>
<button>Third</button>

<!-- Skip element (use sparingly) -->
<button tabindex="-1">Not in tab order</button>

<!-- Never use positive tabindex -->
<!-- tabindex="1" is an anti-pattern -->
```

## ARIA Patterns

### Semantic HTML First

```html
<!-- GOOD: Native semantics -->
<button>Submit</button>
<nav><ul><li><a href="/">Home</a></li></ul></nav>
<main><article><h1>Title</h1></article></main>

<!-- BAD: Divs with ARIA -->
<div role="button" tabindex="0">Submit</div>
<div role="navigation">...</div>
```

### Common ARIA Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-label` | Accessible name | `<button aria-label="Close">X</button>` |
| `aria-labelledby` | Reference label | `<div aria-labelledby="title-id">` |
| `aria-describedby` | Additional description | `<input aria-describedby="hint-id">` |
| `aria-expanded` | Expandable state | `<button aria-expanded={isOpen}>` |
| `aria-hidden` | Hide from AT | `<span aria-hidden="true">*</span>` |
| `aria-live` | Dynamic updates | `<div aria-live="polite">` |
| `aria-invalid` | Validation state | `<input aria-invalid={hasError}>` |
| `aria-disabled` | Disabled state | `<button aria-disabled={true}>` |

### Live Regions

```html
<!-- Polite: Announces when idle -->
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

<!-- Assertive: Interrupts immediately -->
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

## Screen Reader Classes

### Visually Hidden

```css
/* Tailwind's sr-only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Visible on focus */
.sr-only.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Usage

```html
<!-- Icon-only button with accessible name -->
<button aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>

<!-- Or with sr-only -->
<button>
  <TrashIcon aria-hidden="true" />
  <span class="sr-only">Delete item</span>
</button>

<!-- Table with context -->
<td>
  $99.00
  <span class="sr-only">per month</span>
</td>
```

## Form Accessibility

### Labels

```html
<!-- Explicit label (preferred) -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- Implicit label -->
<label>
  Email
  <input type="email" />
</label>

<!-- aria-label for icon inputs -->
<input type="search" aria-label="Search" />
```

### Error Messages

```html
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<p id="email-error" role="alert" class="text-red-600">
  Please enter a valid email address
</p>
```

### Required Fields

```html
<label for="name">
  Name <span aria-hidden="true" class="text-red-500">*</span>
</label>
<input id="name" required aria-required="true" />
```

## Testing Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus visible on all elements
- [ ] Color contrast passes WCAG AA
- [ ] Images have alt text
- [ ] Form fields have labels
- [ ] Error messages linked to inputs
- [ ] Skip links functional
- [ ] Page has single h1
- [ ] Heading hierarchy correct
- [ ] Modal focus trapped
- [ ] Dynamic content announced

---

*Accessibility Reference v1.0 — Frontend Editor Reference*
