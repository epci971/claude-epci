---
paths:
  - frontend/**/*.tsx
  - frontend/**/*.jsx
  - "!frontend/**/*.test.tsx"
  - "!frontend/**/*.test.ts"
  - "!frontend/node_modules/**"
---

# React Frontend Rules

> Conventions pour le developpement React/TypeScript.

## 🔴 CRITICAL

1. **Jamais `any`**: Typer explicitement, utiliser `unknown` si necessaire
2. **Composants fonctionnels**: Pas de classes
3. **Keys uniques**: Jamais d'index comme key dans les listes dynamiques
4. **CSRF sur mutations**: Toujours inclure le token CSRF

## 🟡 CONVENTIONS

### Structure

```
frontend/
├── src/
│   ├── components/        # Composants reutilisables
│   │   ├── ui/           # Primitives (Button, Input)
│   │   └── features/     # Composants metier
│   ├── hooks/            # Custom hooks
│   ├── stores/           # Zustand stores
│   ├── utils/            # Utilitaires
│   ├── types/            # Types TypeScript
│   └── main.tsx          # Entry point
```

### Naming

| Element | Convention | Exemple |
|---------|------------|---------|
| Composants | PascalCase | `UserCard.tsx` |
| Hooks | camelCase, use* | `useAuth.ts` |
| Utils | camelCase | `formatDate.ts` |
| Types | PascalCase | `User.ts` |
| Stores | camelCase, *Store | `userStore.ts` |

### Component Structure

```tsx
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
  // 1. Hooks en premier
  const [isExpanded, setIsExpanded] = useState(false);

  // 2. Handlers
  const handleClick = useCallback(() => {
    onSelect?.(user);
  }, [user, onSelect]);

  // 3. Render
  return (
    <div onClick={handleClick}>
      {user.name}
    </div>
  );
}
```

## 🟢 PREFERENCES

- Preferer `useCallback` pour handlers passes en props
- Utiliser `React.memo` pour composants lourds
- Destructurer les props dans la signature

## Quick Reference

| Task | Pattern |
|------|---------|
| State local | `useState`, `useReducer` |
| State global | Zustand store |
| Server state | React Query |
| Forms | react-hook-form + zod |
| Styling | Tailwind + cn() |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Component registry | `const COMPONENTS = {...}` | Dynamic mounting |
| Error boundary | `<ErrorBoundary>` wrapper | Graceful errors |
| Loading states | `{ isLoading ? <Spinner /> : <Content /> }` | UX |
| Optimistic updates | React Query `onMutate` | Responsive UI |

## Anti-patterns

| Anti-pattern | Probleme | Alternative |
|--------------|----------|-------------|
| `any` type | No type safety | Explicit types |
| Index as key | Reconciliation bugs | Unique IDs |
| Inline styles | Hard to maintain | Tailwind |
| Prop drilling | Verbose, fragile | Context or Zustand |
| Direct DOM | React conflicts | useRef |

## Examples

### Correct

```tsx
interface DataTableProps {
  endpoint: string;
}

export function DataTable({ endpoint }: DataTableProps) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['data', endpoint],
    queryFn: () => fetch(endpoint).then(r => r.json()),
  });

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <table>
      {data.map((item: DataItem) => (
        <tr key={item.id}>{item.name}</tr>
      ))}
    </table>
  );
}
```

### Incorrect

```tsx
// DON'T DO THIS
export function DataTable({ endpoint }: any) {  // any!
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(endpoint).then(r => r.json()).then(setData);
  }, []);  // Missing dependency!

  return (
    <table>
      {data.map((item, index) => (
        <tr key={index}>{item.name}</tr>  // Index as key!
      ))}
    </table>
  );
}
```
