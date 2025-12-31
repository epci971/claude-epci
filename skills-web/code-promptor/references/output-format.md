# Output Format — Brief Structure Reference

> Complete specification for Code-Promptor brief output

---

## Overview

Code-Promptor produces briefs in 3 formats based on detected complexity. All formats follow the same core principles:
- **Title**: Notion-ready (Action verb + Object)
- **Self-contained**: Readable without source transcript
- **Actionable**: Ready for development workflow

---

## Complexity Detection

### Criteria Matrix

| Level | Word Count | Verb Type | Scope | Components |
|-------|------------|-----------|-------|------------|
| **Quick fix** | < 50 | Corrective | Very limited | 1 |
| **Standard** | 50-200 | Creative | Clear | 1-2 |
| **Major** | > 200 | Architectural | Complex | 3+ |

### Verb Classification

| Level | Verbs |
|-------|-------|
| Quick fix | corriger, fixer, débugger, réparer, ajuster, résoudre |
| Standard | créer, ajouter, implémenter, développer, intégrer |
| Major | concevoir, architecturer, refondre, migrer, transformer |

### Override Triggers

Force **Major** regardless of word count:
- Multiple external integrations mentioned
- Database schema changes
- Authentication/security changes
- Multiple domains (backend + frontend + devops)

---

## Common Header

All briefs start with:

```markdown
# [Title — Action Verb + Object]

📦 **[Complexity]** | ⏱️ [Time] | 🎯 Confidence: [HIGH|MEDIUM|LOW]
```

### Title Rules

| Rule | Example ✅ | Counter-example ❌ |
|------|-----------|-------------------|
| Start with action verb | "Implémenter le calcul TCB" | "Calcul TCB" |
| 5-12 words max | "Créer l'export PDF rapports" | "Créer un système complet d'export PDF pour tous les rapports avec filtres" |
| No person references | "Développer l'API auth" | "Ce que Pierre veut pour l'auth" |
| Specific | "Intégrer Stripe pour paiements" | "Faire les paiements" |

### Confidence Levels

| Level | Criteria |
|-------|----------|
| 🟢 HIGH | Clear intent, explicit requirements, no contradictions |
| 🟡 MEDIUM | Clear intent, some gaps in FR/NFR |
| 🔴 LOW | Vague intent, major gaps, unresolved ambiguities |

---

## Format 1: Quick Fix (1h)

### Structure

```markdown
# [Title]

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: [LEVEL]

## Objectif

[2-3 sentences describing the fix purpose]

## Contexte

[Brief context where the issue occurs]

## Correction attendue

- [Action 1]
- [Action 2]
- [Verification step]

## Notes

- [Additional notes or "Aucune note complémentaire."]
```

### Characteristics

- No implementation plan (too simple)
- "Correction attendue" instead of formal FR
- Short and actionable
- ~100-150 words total

### Example

```markdown
# Corriger l'affichage des dates format FR

📦 **Quick fix** | ⏱️ 1h | 🎯 Confidence: HIGH

## Objectif

Corriger l'affichage incorrect des dates dans le module laboratoire qui montre le format US (MM/DD/YYYY) au lieu du format français (DD/MM/YYYY).

## Contexte

Le problème apparaît sur la page de résultats d'analyses. Toutes les dates de prélèvement s'affichent en format américain.

## Correction attendue

- Identifier le composant DateDisplay utilisé dans la vue
- Appliquer le formateur avec pattern `d/m/Y`
- Vérifier la cohérence sur les autres vues du module

## Notes

- Aucune note complémentaire.
```

---

## Format 2: Standard (4h)

### Structure

```markdown
# [Title]

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: [LEVEL]

## Objectif

[2-4 sentences describing purpose and benefit]

## Description

[1-2 paragraphs on context and high-level functioning]

## Exigences fonctionnelles

- [FR1] [Observable behavior]
- [FR2] [Observable behavior]
- [FR3] [Observable behavior]

## Contraintes techniques

- [Constraint 1]
- [Constraint 2]
- [Or: "Aucune contrainte explicitement mentionnée."]

## Plan d'implémentation

1. **[Phase 1 Name]**
   - [ ] Subtask 1
   - [ ] Subtask 2

2. **[Phase 2 Name]**
   - [ ] Subtask 1
   - [ ] Subtask 2

3. **Finalisation**
   - [ ] Tests
   - [ ] Documentation

## Notes

- [Secondary considerations or "Aucune note complémentaire."]
```

### Characteristics

- Implementation plan with subtasks grouped by phase
- Subtasks auto-generated based on type/domain
- ~200-300 words total
- Balance between detail and concision

### Example

```markdown
# Implémenter l'export PDF des rapports d'analyses

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: HIGH

## Objectif

Permettre aux utilisateurs d'exporter les rapports d'analyses au format PDF pour archivage et partage externe. Cette fonctionnalité répond au besoin de traçabilité documentaire.

## Description

La fonctionnalité s'intègre au module rapports existant. Un bouton "Exporter PDF" sera ajouté sur la page de détail. Le PDF généré reprend la mise en forme actuelle avec en-tête laboratoire et pied de page légal.

## Exigences fonctionnelles

- Le système génère un PDF à partir des données du rapport affiché
- Le PDF inclut l'en-tête avec logo et informations laboratoire
- Le PDF inclut un pied de page avec mentions légales et date
- L'utilisateur télécharge le fichier directement via le navigateur

## Contraintes techniques

- Utiliser la librairie PDF existante (wkhtmltopdf)
- Respecter la charte graphique définie

## Plan d'implémentation

1. **Backend — Service PDF**
   - [ ] Créer le service `RapportPdfGenerator`
   - [ ] Configurer le template HTML de conversion
   - [ ] Ajouter l'endpoint API `/api/rapports/{id}/pdf`

2. **Frontend — Interface**
   - [ ] Ajouter le bouton "Exporter PDF" sur `RapportDetail`
   - [ ] Gérer l'état de chargement pendant génération
   - [ ] Déclencher le téléchargement automatique

3. **Finalisation**
   - [ ] Tests avec différents formats de rapports
   - [ ] Vérifier le rendu multi-navigateurs

## Notes

- Évolution future possible : export batch de plusieurs rapports
```

---

## Format 3: Major (8h)

### Structure

```markdown
# [Title]

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: [LEVEL]

## Objectif

[3-4 sentences on purpose, benefit, and strategic importance]

## Description

[2-3 paragraphs on context, functioning, and key considerations]

## Exigences fonctionnelles

- [FR1] [Detailed observable behavior]
- [FR2] [Detailed observable behavior]
- [FR3] [Detailed observable behavior]
- [FR4] [Detailed observable behavior]

## Exigences non-fonctionnelles

- [NFR1] Performance/security/reliability requirement
- [NFR2] Scalability/maintainability requirement

## Contraintes techniques

- [Technical stack constraints]
- [External system constraints]
- [Data format constraints]

## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Define data models
   - [ ] Create migrations
   - [ ] Document interfaces

2. **Backend — Core Logic**
   - [ ] Create main service
   - [ ] Implement business rules
   - [ ] Add validation

3. **Backend — Integration**
   - [ ] External API client
   - [ ] Error handling & retry
   - [ ] Async tasks if needed

4. **Frontend — Main Views**
   - [ ] Dashboard/main component
   - [ ] Forms and interactions
   - [ ] Loading/error states

5. **Frontend — Administration**
   - [ ] Configuration interface
   - [ ] Monitoring views

6. **Finalisation**
   - [ ] Unit tests (coverage >80%)
   - [ ] Integration tests
   - [ ] Technical documentation
   - [ ] User documentation

## Notes

- [Important decisions pending]
- [Risks or dependencies]
- [Future evolution considerations]
```

### Characteristics

- NFR section included
- Detailed plan with 5-6 phases
- Specific subtasks for each phase
- ~400-500 words total

---

## Multi-Brief Separator

When generating multiple briefs:

```markdown
═══════════════════════════════════════════════════════════════════
📋 TÂCHE 1/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 1 content]

═══════════════════════════════════════════════════════════════════
📋 TÂCHE 2/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 2 content]

═══════════════════════════════════════════════════════════════════
📋 TÂCHE 3/3 — Copier dans Notion
═══════════════════════════════════════════════════════════════════

[Brief 3 content]

═══════════════════════════════════════════════════════════════════
✅ 3 briefs générés — Prêts pour Notion
═══════════════════════════════════════════════════════════════════
```

---

## Dependencies Section

When `ref [n]` command is used:

```markdown
## Dépendances

- ⚠️ Requiert : [Tâche N — Title](notion_link)
```

---

## Absence Markers

Use these exact phrases when information is missing:

| Section | Marker |
|---------|--------|
| FR | "Aucun FR explicitement mentionné dans la source." |
| NFR | "Aucun NFR explicitement mentionné dans la source." |
| Constraints | "Aucune contrainte technique explicitement mentionnée." |
| Notes | "Aucune note complémentaire." |

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| "Le transcript mentionne..." | References source | Self-contained content |
| "L'utilisateur souhaite..." | References person | "La fonctionnalité vise à..." |
| Inventing FR | Scope creep | Mark as absent |
| Generic subtasks | Not actionable | Context-specific subtasks |
| No verb in title | Not actionable | Start with action verb |
