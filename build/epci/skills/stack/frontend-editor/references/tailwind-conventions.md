# Tailwind Conventions Reference

## Design Tokens

### Color System

Full semantic color palette with 10 shades each:

```javascript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',   // Default
          700: '#1d4ed8',   // Hover
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f9fafb',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
        },
        success: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        },
        danger: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
        },
      },
    },
  },
};
```

### Spacing Scale

| Token | Value | CSS Variable | Use Case |
|-------|-------|--------------|----------|
| 0.5 | 2px | `--spacing-0-5` | Borders, fine adjustments |
| 1 | 4px | `--spacing-1` | Tight gaps |
| 2 | 8px | `--spacing-2` | Icon gaps, small padding |
| 3 | 12px | `--spacing-3` | Button padding |
| 4 | 16px | `--spacing-4` | Standard padding |
| 6 | 24px | `--spacing-6` | Card padding |
| 8 | 32px | `--spacing-8` | Section gaps |
| 12 | 48px | `--spacing-12` | Large sections |
| 16 | 64px | `--spacing-16` | Page margins |

### Typography Scale

| Class | Size | Line Height | Weight | Use Case |
|-------|------|-------------|--------|----------|
| `text-xs` | 0.75rem (12px) | 1rem | 400 | Labels, captions |
| `text-sm` | 0.875rem (14px) | 1.25rem | 400 | Body small, help text |
| `text-base` | 1rem (16px) | 1.5rem | 400 | Body default |
| `text-lg` | 1.125rem (18px) | 1.75rem | 500 | Subheadings |
| `text-xl` | 1.25rem (20px) | 1.75rem | 600 | Section titles |
| `text-2xl` | 1.5rem (24px) | 2rem | 700 | Page headings |
| `text-3xl` | 1.875rem (30px) | 2.25rem | 700 | Hero headings |

## Configuration Patterns

### Content Paths

```javascript
// tailwind.config.ts
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    // Django templates (if hybrid project)
    '../backend/templates/**/*.html',
    // Component library
    './node_modules/@your-org/ui/**/*.js',
  ],
  // ...
};
```

### Plugins

```javascript
plugins: [
  require('@tailwindcss/forms'),        // Form styling reset
  require('@tailwindcss/typography'),   // Prose content
  require('@tailwindcss/aspect-ratio'), // Aspect ratios
  require('@tailwindcss/container-queries'), // Container queries
]
```

### Dark Mode

```javascript
// Class-based (recommended for control)
darkMode: 'class',

// Or media-based (follows system)
darkMode: 'media',
```

### Custom Utilities

```javascript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      // Custom animations
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
};
```

## Class Merging with cn()

### Installation

```bash
npm install clsx tailwind-merge
```

### Implementation

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Usage Patterns

```typescript
// Basic merging
cn('px-4 py-2', 'text-sm')
// => 'px-4 py-2 text-sm'

// Conditional classes
cn('base-class', isActive && 'active-class')
// => 'base-class active-class' (if isActive)

// Object syntax
cn('base', { 'text-red-500': hasError, 'text-green-500': isSuccess })
// => 'base text-red-500' (if hasError)

// Override conflicts (tailwind-merge handles this)
cn('px-4', 'px-6')
// => 'px-6' (later wins)

// Allow className prop override
cn(baseClasses, variantClasses, className)
// => Consumer can override
```

## Layer System

### CSS Layers

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Reset and base styles */
  html {
    @apply antialiased;
  }
}

@layer components {
  /* Reusable component classes */
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }
}

@layer utilities {
  /* Custom utilities */
  .text-balance {
    text-wrap: balance;
  }
}
```

## Best Practices

### Do

```html
<!-- Use semantic tokens -->
<button class="bg-primary-600 hover:bg-primary-700">

<!-- Use spacing scale -->
<div class="p-4 space-y-2">

<!-- Use cn() for dynamic classes -->
<div className={cn('base', variant && variants[variant])}>
```

### Don't

```html
<!-- Avoid arbitrary values when tokens exist -->
<button class="bg-[#2563eb]">  <!-- Use bg-primary-600 -->

<!-- Avoid inline styles -->
<div style="padding: 16px">  <!-- Use p-4 -->

<!-- Avoid !important -->
<div class="!mt-0">  <!-- Fix specificity instead -->
```

---

*Tailwind Conventions v1.0 — Frontend Editor Reference*
