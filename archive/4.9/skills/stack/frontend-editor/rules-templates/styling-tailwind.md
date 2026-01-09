---
paths:
  - frontend/**/*.css
  - frontend/**/*.scss
  - "**/tailwind.config.*"
  - "!frontend/node_modules/**"
---

# Tailwind CSS Rules

> Conventions pour le styling avec Tailwind CSS.

## 🔴 CRITICAL

1. **Pas de styles inline**: Utiliser les classes Tailwind
2. **Pas d'!important**: Utiliser le layer system
3. **Design tokens**: Couleurs dans tailwind.config, pas hardcodees
4. **Focus visible**: Toujours `focus:ring-2 focus:ring-offset-2`

## 🟡 CONVENTIONS

### Design Tokens

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        // secondary, success, warning, danger
      },
    },
  },
};
```

### Component Variants

| Variant | Classes | Usage |
|---------|---------|-------|
| `primary` | `bg-primary-600 text-white hover:bg-primary-700` | Actions principales |
| `secondary` | `bg-gray-200 text-gray-900 hover:bg-gray-300` | Actions secondaires |
| `danger` | `bg-red-600 text-white hover:bg-red-700` | Actions destructives |
| `ghost` | `text-gray-700 hover:bg-gray-100` | Actions subtiles |
| `outline` | `border border-gray-300 hover:bg-gray-50` | Emphasis bordure |

### Utility Function

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<button className={cn(
  "px-4 py-2 rounded-md",
  variant === "primary" && "bg-primary-600 text-white",
  className
)}>
```

## 🟢 PREFERENCES

- Mobile-first: classes de base pour mobile, `md:` pour tablette
- Spacing scale: utiliser l'echelle Tailwind (4, 8, 16...)
- Dark mode: `dark:` prefix pour theming

## Quick Reference

| Task | Pattern |
|------|---------|
| Merge classes | `cn(base, variant, className)` |
| Responsive | `md:flex lg:grid` |
| Dark mode | `dark:bg-gray-900` |
| Focus | `focus:ring-2 focus:ring-offset-2` |
| Hover | `hover:bg-primary-700` |
| Transition | `transition-colors duration-200` |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| cn() utility | clsx + tailwind-merge | Safe merging |
| Variant objects | Map of class strings | Type-safe |
| Responsive grid | `grid grid-cols-1 md:grid-cols-2` | Fluid |
| Token system | CSS variables | Runtime theming |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| Inline styles | Hard to maintain | Tailwind classes |
| `!important` | Specificity wars | Layer system |
| Random colors | Inconsistent | Design tokens |
| Skip focus | Accessibility fail | Always include |
| Fixed px | Not responsive | Tailwind scale |

## Examples

### Correct

```tsx
// Button with variants
const buttonVariants = {
  primary: "bg-primary-600 text-white hover:bg-primary-700",
  secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
  danger: "bg-red-600 text-white hover:bg-red-700",
};

const sizeVariants = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg",
};

export function Button({ variant = "primary", size = "md", className, ...props }) {
  return (
    <button
      className={cn(
        "rounded-md font-medium transition-colors",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500",
        buttonVariants[variant],
        sizeVariants[size],
        className
      )}
      {...props}
    />
  );
}
```

### Incorrect

```tsx
// DON'T DO THIS
<button
  style={{ backgroundColor: '#3b82f6', padding: '8px 16px' }}  // Inline!
  className="text-white !important"  // !important!
>
  Click
</button>

// No focus styles - accessibility fail!
<button className="bg-blue-500 text-white px-4 py-2">
  Click
</button>
```
