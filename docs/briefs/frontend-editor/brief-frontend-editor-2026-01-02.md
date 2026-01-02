# Brief Fonctionnel — Skill `frontend-editor`

> **Version**: 1.0 | **Date**: 2026-01-02 | **EMS Final**: 88/100

---

## 1. Contexte

Le projet EPCI dispose d'un skill `javascript-react` orienté comportement et interactivité. Il manque un skill dédié à la **couche présentation** (HTML/CSS/Tailwind) pour compléter l'écosystème.

## 2. Objectif

Créer un skill `frontend-editor` spécialisé dans :
- L'intégration HTML avec conventions UX/UI
- Les bonnes pratiques Tailwind CSS
- L'orchestration automatique des MCP Magic et Context7
- La génération de composants UI accessibles

## 3. Scope

### Inclus
- Composants UI complets : Button, Input, Select, Checkbox, Radio, Card, Modal, Dropdown, Tabs, Table, Form, Navigation, Toast, Alert
- Variants Tailwind : primary, secondary, success, warning, danger, ghost, outline
- Sizes : sm, md, lg
- States : default, hover, focus, disabled, loading, error
- Accessibilité WCAG 2.1 intégrée (ARIA, focus rings, contraste)
- Responsive design par défaut

### Exclus
- Comportement JavaScript/React (délégué à `javascript-react`)
- Bootstrap (Tailwind only)
- Vue/Svelte (React uniquement, extensible plus tard)

## 4. Spécifications Techniques

### 4.1 Structure du Skill

```
src/skills/stack/frontend-editor/
├── SKILL.md                          # Skill principal (<5000 tokens)
└── references/
    ├── tailwind-conventions.md       # Règles et patterns Tailwind
    ├── components-catalog.md         # Templates composants complets
    └── accessibility.md              # Patterns WCAG 2.1
```

### 4.2 Auto-détection

```python
'frontend-editor': {
    'files': ['package.json', 'tailwind.config.js', 'tailwind.config.ts'],
    'patterns': [
        ('package.json', r'"tailwindcss"'),
        ('tailwind.config', r'content:\s*\['),
    ],
    'dirs': ['src/components', 'src/ui'],
}
```

### 4.3 Triggers d'Auto-activation

| Type | Valeurs |
|------|---------|
| **Keywords** | `button, input, form, modal, card, table, layout, responsive, tailwind, css, style, ui, ux, component, présentation, design, intégration` |
| **Files** | `*.css`, `*.scss`, `**/components/**/*.tsx`, `**/ui/**/*.tsx` |
| **Contexte** | Tâches mentionnant "présentation", "design", "intégration HTML" |

### 4.4 MCP Integration

| Server | Usage | Auto-activation |
|--------|-------|-----------------|
| **Magic** (21st.dev) | Patterns UI, composants de référence | Oui - via keywords UI |
| **Context7** | Documentation Tailwind, règles CSS | Oui - via keywords Tailwind |

### 4.5 Ordre de Chargement

```
/epci ou /quick avec tâche UI
    │
    ├── 1. frontend-editor (présentation HTML/CSS)
    │
    └── 2. javascript-react (comportement/interactivité)
```

## 5. Composants Catalog

### 5.1 Composants de Base
- **Button** : variants, sizes, icons, loading state
- **Input** : text, email, password, search, avec validation
- **Select** : native, custom dropdown
- **Checkbox** / **Radio** : avec labels accessibles
- **Textarea** : auto-resize optional

### 5.2 Composants Layout
- **Card** : header, body, footer, variants
- **Modal** : dialog accessible, backdrop, animations
- **Dropdown** : menu, submenu, keyboard navigation
- **Tabs** : horizontal, vertical, avec panels

### 5.3 Composants Data
- **Table** : sortable, pagination, responsive
- **Form** : validation, error states, field groups

### 5.4 Composants Feedback
- **Toast** : success, error, warning, info, auto-dismiss
- **Alert** : inline, dismissible
- **Navigation** : navbar, sidebar, breadcrumbs

## 6. Conventions Tailwind

### 6.1 Utility Function

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 6.2 Pattern Composant

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  className?: string;
  children: React.ReactNode;
}

const variantStyles = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
  // ...
};

const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};
```

### 6.3 Accessibilité Obligatoire

- Focus visible : `focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`
- ARIA labels sur éléments interactifs
- Contraste minimum WCAG AA (4.5:1 texte, 3:1 UI)
- Navigation clavier complète

## 7. Intégration EPCI

### 7.1 Dans /epci et /quick

Le skill `frontend-editor` s'active automatiquement quand :
1. La tâche contient des keywords UI/UX/CSS
2. Les fichiers modifiés sont dans `components/` ou `ui/`
3. Le brief mentionne "présentation", "intégration", "design"

### 7.2 Workflow Type

```
Brief: "Créer un formulaire de contact responsive"
    │
    ├── frontend-editor active
    │   ├── MCP Magic → patterns formulaire
    │   ├── MCP Context7 → docs Tailwind forms
    │   └── Génère HTML/Tailwind avec a11y
    │
    └── javascript-react active (si comportement requis)
        └── Ajoute validation, submit handler
```

## 8. Critères de Succès

- [ ] Skill `frontend-editor` créé avec structure complète
- [ ] Auto-détection fonctionnelle (Tailwind dans package.json)
- [ ] MCP Magic et Context7 s'activent sur keywords UI
- [ ] Composants catalog documentés avec exemples
- [ ] Accessibilité WCAG 2.1 dans chaque template
- [ ] Intégration /epci et /quick validée

## 9. Estimation

| Aspect | Valeur |
|--------|--------|
| **Complexité** | STANDARD |
| **Fichiers** | 4 (SKILL.md + 3 references) |
| **Dépendances** | javascript-react (complémentaire) |
| **Risques** | Faible - Pattern existant à suivre |

---

## Exploration Summary

| Élément | Découverte |
|---------|------------|
| **Stack** | React + Tailwind CSS |
| **Pattern modèle** | `src/skills/stack/javascript-react/` |
| **MCP existant** | Magic (21st.dev) + Context7 (docs) |
| **Persona** | Frontend (auto-activate Magic + Playwright) |
| **Fichiers candidats** | Nouveau skill à créer |

---

*Brief généré par /brainstorm — Prêt pour /brief puis /epci*
