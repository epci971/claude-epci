# Magic MCP Server (21st.dev)

## Overview

Magic provides modern UI component generation using 21st.dev's component library.

| Attribute | Value |
|-----------|-------|
| **Function** | UI component generation |
| **Tools** | `21st_magic_component_builder`, `logo_search`, `21st_magic_component_inspiration`, `21st_magic_component_refiner` |
| **Timeout** | 20 seconds |
| **Fallback** | Basic component generation |

## When to Use

- Creating new React/Vue components
- Building accessible UI elements
- Modern design patterns
- Responsive layouts

## Auto-Triggers

### Keywords
`component`, `button`, `form`, `modal`, `table`, `ui`, `interface`, `design`, `layout`, `widget`

### Files
`*.jsx`, `*.tsx`, `*.vue`, `*.svelte`, `**/components/**`, `**/ui/**`

### Personas
- **frontend** (primary)

## Available Tools

### 21st_magic_component_builder
Build new UI components from specifications.

### logo_search
Find company logos in JSX/TSX/SVG format.

### 21st_magic_component_inspiration
Browse existing component designs for inspiration.

### 21st_magic_component_refiner
Improve and refine existing components.

## Workflow

```
1. Analyze UI requirement from brief
2. Search for similar components on 21st.dev
3. Generate component with:
   - Accessibility (WCAG 2.1)
   - Responsive design
   - Modern patterns
4. Include variants (loading, empty, error states)
```

## Example Usage

**Brief**: "Create a reusable DataTable component"
**Persona**: `--persona-frontend`

```
 Magic activated (auto: frontend)
 Searching 21st.dev for DataTable patterns
 Generating component with:
   ✓ Sorting
   ✓ Filtering
   ✓ Pagination
   ✓ WCAG 2.1 accessibility
   ✓ Responsive breakpoints
   ✓ Loading/empty/error states
```

## Component Features

Generated components include:

- **Accessibility**: ARIA labels, keyboard navigation, focus management
- **Responsiveness**: Mobile-first, breakpoint variants
- **States**: Loading, empty, error, success
- **Theming**: CSS variables, dark mode support
- **TypeScript**: Full type definitions

## Fallback

If Magic is unavailable:

```
 [MCP] Magic unavailable, using basic generation
```

Generates functional components without 21st.dev patterns.

## Best Practices

1. **Provide context** — Describe use case and requirements
2. **Specify variants** — List needed states upfront
3. **Include accessibility** — Always request WCAG compliance
4. **Review output** — Verify generated code quality

## Configuration

```json
{
  "magic": {
    "enabled": true,
    "auto_activate": true,
    "timeout_seconds": 20
  }
}
```

---

*Magic Reference — F12 MCP Integration*
