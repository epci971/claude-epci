# Brief Template — Standard

> Template for standard features (4h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | 50-200 words |
| Verb type | Creative (créer, ajouter, implémenter) |
| Scope | Clear, well-defined |
| Components | 1-2 |

---

## Template Structure

```markdown
# {Action Verb} {Feature Description}

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: {HIGH|MEDIUM|LOW}

## Objectif

{2-4 sentences describing purpose and benefit}

## Description

{1-2 paragraphs on context and high-level functioning}

## Exigences fonctionnelles

- {FR1: Observable behavior}
- {FR2: Observable behavior}
- {FR3: Observable behavior}

## Contraintes techniques

- {Constraint 1}
- {Constraint 2}
- {Or: "Aucune contrainte technique explicitement mentionnée."}

## Plan d'implémentation

1. **{Phase 1 Name}**
   - [ ] {Subtask 1}
   - [ ] {Subtask 2}

2. **{Phase 2 Name}**
   - [ ] {Subtask 1}
   - [ ] {Subtask 2}

3. **Finalisation**
   - [ ] Tests
   - [ ] Documentation

## Notes

- {Notes or "Aucune note complémentaire."}
```

---

## Field Guidelines

### Title

**Format**: `{Verb} {Feature} {Context/Qualifier}`

**Good examples**:
- "Implémenter l'export PDF des rapports d'analyses"
- "Créer le composant de sélection de dates"
- "Ajouter la synchronisation automatique avec l'API"
- "Développer le dashboard KPIs temps réel"

### Objective

2-4 sentences covering:
1. What the feature does
2. Why it's needed (business value)
3. Who benefits

**Template**:
> Permettre {à qui} de {faire quoi}. Cette fonctionnalité {bénéfice 1} et {bénéfice 2}. Le besoin principal est de {core need}.

### Description

1-2 paragraphs covering:
- Integration context (where it fits)
- High-level functioning
- Key interactions

**Note**: Don't repeat FR here — describe the "how it works" at high level.

### Exigences fonctionnelles

Observable behaviors, testable:
- Use "Le système..." or "L'utilisateur peut..."
- Each FR should be verifiable
- Don't invent — mark absent if not mentioned

**Template per FR**:
> Le système {verbe} {objet} {condition/précision}

### Contraintes techniques

Only if explicitly mentioned:
- Technology stack requirements
- External system constraints
- Data format requirements
- Performance requirements

If none mentioned:
> - Aucune contrainte technique explicitement mentionnée.

### Plan d'implémentation

2-3 phases with checkboxes:
- Group by domain (Backend, Frontend) or logical phase
- 2-4 subtasks per phase
- Always end with "Finalisation"

**Subtask generation**: Use templates from [subtask-templates.md](../references/subtask-templates.md)

### Notes

Secondary considerations:
- Future evolutions mentioned
- Open questions
- Dependencies
- Or "Aucune note complémentaire."

---

## Complete Example

```markdown
# Implémenter l'export PDF des rapports d'analyses

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: HIGH

## Objectif

Permettre aux utilisateurs d'exporter les rapports d'analyses au format PDF pour archivage et partage externe. Cette fonctionnalité répond au besoin de traçabilité documentaire et facilite la communication avec les partenaires externes.

## Description

La fonctionnalité s'intègre au module rapports existant. Un bouton "Exporter PDF" sera ajouté sur la page de détail d'un rapport. Le PDF généré reprend la mise en forme actuelle avec en-tête laboratoire (logo, coordonnées) et pied de page légal (mentions obligatoires, date de génération).

Le processus de génération est synchrone pour les rapports standards. L'utilisateur clique sur le bouton, le PDF est généré côté serveur, puis téléchargé automatiquement.

## Exigences fonctionnelles

- Le système génère un PDF à partir des données du rapport affiché
- Le PDF inclut l'en-tête avec logo et informations laboratoire
- Le PDF inclut un pied de page avec mentions légales et date de génération
- L'utilisateur peut télécharger le fichier directement via le navigateur
- Le nom du fichier suit le format `rapport_{id}_{date}.pdf`

## Contraintes techniques

- Utiliser la librairie wkhtmltopdf déjà configurée sur le serveur
- Respecter la charte graphique définie dans le design system
- Le PDF ne doit pas dépasser 10 Mo

## Plan d'implémentation

1. **Backend — Service PDF**
   - [ ] Créer le service `RapportPdfGenerator`
   - [ ] Configurer le template HTML de conversion
   - [ ] Ajouter l'endpoint API `GET /api/rapports/{id}/pdf`
   - [ ] Configurer les headers de réponse (Content-Type, Content-Disposition)

2. **Frontend — Interface**
   - [ ] Ajouter le bouton "Exporter PDF" sur le composant `RapportDetail`
   - [ ] Implémenter l'état de chargement pendant la génération
   - [ ] Déclencher le téléchargement automatique à la réception

3. **Finalisation**
   - [ ] Tests avec différents formats de rapports
   - [ ] Test de performance avec rapports volumineux
   - [ ] Documentation de l'endpoint API

## Notes

- Évolution future envisagée : export batch de plusieurs rapports
- Vérifier la compatibilité des polices sur le serveur de production
```

---

## Variation: Multi-Domain (Backend + Frontend)

When task spans both domains, structure phases accordingly:

```markdown
## Plan d'implémentation

1. **Backend — API**
   - [ ] Créer l'endpoint
   - [ ] Implémenter la logique
   - [ ] Valider les entrées

2. **Backend — Service**
   - [ ] Créer le service métier
   - [ ] Gérer les cas d'erreur

3. **Frontend — Composant**
   - [ ] Créer le composant UI
   - [ ] Connecter à l'API
   - [ ] Gérer les états

4. **Finalisation**
   - [ ] Tests backend
   - [ ] Tests frontend
   - [ ] Documentation
```

---

## Variation: Frontend-Only

```markdown
## Plan d'implémentation

1. **Composant — Structure**
   - [ ] Créer le composant principal
   - [ ] Définir les props et types
   - [ ] Implémenter le rendu de base

2. **Composant — Logique**
   - [ ] Ajouter la gestion d'état
   - [ ] Implémenter les interactions
   - [ ] Connecter aux données

3. **Finalisation**
   - [ ] Tests Jest/RTL
   - [ ] Vérifier responsive
   - [ ] Documentation storybook
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Invent FR not mentioned | Mark as absent |
| Skip plan for Standard | Always include plan |
| Use > 6 phases | Keep to 2-3 phases |
| Generic subtasks | Context-specific subtasks |
| Repeat Description in FR | Each section is distinct |
