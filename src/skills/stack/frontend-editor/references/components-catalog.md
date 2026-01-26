# Component Catalog Reference

## Button Variants

### Full Implementation

```typescript
// components/Button.tsx
import { cn } from '@/lib/utils';

const buttonVariants = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
  secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
  success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
  warning: 'bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
  outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500',
};

const sizeVariants = {
  sm: 'px-3 py-1.5 text-sm min-h-[32px]',
  md: 'px-4 py-2 text-base min-h-[40px]',
  lg: 'px-6 py-3 text-lg min-h-[48px]',
};

const baseClasses = cn(
  'inline-flex items-center justify-center',
  'rounded-md font-medium',
  'transition-colors duration-200',
  'focus:outline-none focus:ring-2 focus:ring-offset-2',
  'disabled:opacity-50 disabled:cursor-not-allowed'
);

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof sizeVariants;
  loading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  className,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        baseClasses,
        buttonVariants[variant],
        sizeVariants[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Spinner className="mr-2 h-4 w-4" />}
      {children}
    </button>
  );
}
```

## Form Components

### Input

```typescript
// components/Input.tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, className, id, ...props }: InputProps) {
  const inputId = id || `input-${Math.random().toString(36).slice(2)}`;

  return (
    <div className="space-y-1">
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={cn(
          'block w-full rounded-md px-3 py-2',
          'border shadow-sm',
          'focus:outline-none focus:ring-2 focus:ring-offset-0',
          'disabled:bg-gray-50 disabled:text-gray-500',
          error
            ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
            : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
          className
        )}
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-sm text-gray-500">{hint}</p>
      )}
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-red-600" role="alert">{error}</p>
      )}
    </div>
  );
}
```

### Select

```typescript
// components/Select.tsx
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { value: string; label: string }[];
}

export function Select({ label, error, options, className, id, ...props }: SelectProps) {
  const selectId = id || `select-${Math.random().toString(36).slice(2)}`;

  return (
    <div className="space-y-1">
      {label && (
        <label htmlFor={selectId} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <select
        id={selectId}
        className={cn(
          'block w-full rounded-md px-3 py-2',
          'border shadow-sm',
          'focus:outline-none focus:ring-2 focus:ring-offset-0',
          error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300 focus:ring-primary-500',
          className
        )}
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={error ? `${selectId}-error` : undefined}
        {...props}
      >
        {options.map(({ value, label }) => (
          <option key={value} value={value}>{label}</option>
        ))}
      </select>
      {error && (
        <p id={`${selectId}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

### Checkbox

```typescript
// components/Checkbox.tsx
interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export function Checkbox({ label, className, ...props }: CheckboxProps) {
  return (
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        className={cn(
          'h-4 w-4 rounded',
          'border-gray-300 text-primary-600',
          'focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
          className
        )}
        {...props}
      />
      <span className="text-sm text-gray-700">{label}</span>
    </label>
  );
}
```

## Card Components

### Basic Card

```typescript
// components/Card.tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn('bg-white rounded-lg shadow', className)}>
      {children}
    </div>
  );
}

Card.Header = function CardHeader({ children, className }: CardProps) {
  return (
    <div className={cn('px-4 py-3 border-b border-gray-200', className)}>
      {children}
    </div>
  );
};

Card.Body = function CardBody({ children, className }: CardProps) {
  return <div className={cn('p-4', className)}>{children}</div>;
};

Card.Footer = function CardFooter({ children, className }: CardProps) {
  return (
    <div className={cn('px-4 py-3 border-t border-gray-200 bg-gray-50 rounded-b-lg', className)}>
      {children}
    </div>
  );
};
```

## Layout Patterns

### Grid System

```typescript
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id}>{item.content}</Card>)}
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-4">
  {items.map(item => <Card key={item.id}>{item.content}</Card>)}
</div>
```

### Stack Layout

```typescript
// Vertical stack with gap
<div className="flex flex-col gap-4">
  <Component />
  <Component />
</div>

// Horizontal stack with gap
<div className="flex flex-row gap-2 items-center">
  <Icon />
  <Text />
</div>
```

## State Variants

| State | Classes | Usage |
|-------|---------|-------|
| Default | Base classes | Normal state |
| Hover | `hover:bg-gray-50` | Mouse over |
| Focus | `focus:ring-2 focus:ring-offset-2` | Keyboard focus |
| Active | `active:bg-gray-100` | Being clicked |
| Disabled | `disabled:opacity-50 disabled:cursor-not-allowed` | Not interactive |
| Loading | `opacity-75 cursor-wait` | Async operation |
| Error | `border-red-500 text-red-600` | Validation error |
| Success | `border-green-500 text-green-600` | Confirmation |

## Compound Components Pattern

```typescript
// Usage example
<Card>
  <Card.Header>
    <h3 className="text-lg font-semibold">Title</h3>
  </Card.Header>
  <Card.Body>
    <p>Content goes here</p>
  </Card.Body>
  <Card.Footer>
    <Button variant="primary">Action</Button>
  </Card.Footer>
</Card>
```

---

*Component Catalog v1.0 — Frontend Editor Reference*
