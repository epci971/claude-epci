# Brief Template — Standard

> Template for standard features (4h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | 50-200 words |
| Verb type | Creative (créer, ajouter, implémenter) |
| Scope | Clear, well-defined |

---

## Template

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

## Example

```markdown
# Implémenter l'export PDF des rapports d'analyses

📦 **Standard** | ⏱️ 4h | 🎯 Confidence: HIGH

## Objectif

Permettre aux utilisateurs d'exporter les rapports au format PDF pour archivage.
Cette fonctionnalité répond au besoin de traçabilité documentaire.

## Description

La fonctionnalité s'intègre au module rapports existant. Un bouton "Exporter PDF"
sera ajouté sur la page de détail. Le PDF reprend la mise en forme actuelle
avec en-tête laboratoire et pied de page légal.

## Exigences fonctionnelles

- Le système génère un PDF à partir des données du rapport
- Le PDF inclut l'en-tête avec logo et informations laboratoire
- L'utilisateur télécharge le fichier directement via le navigateur

## Contraintes techniques

- Utiliser la librairie wkhtmltopdf existante
- Respecter la charte graphique définie

## Plan d'implémentation

1. **Backend — Service PDF**
   - [ ] Créer le service `RapportPdfGenerator`
   - [ ] Configurer le template HTML
   - [ ] Ajouter l'endpoint API `/api/rapports/{id}/pdf`

2. **Frontend — Interface**
   - [ ] Ajouter le bouton "Exporter PDF"
   - [ ] Gérer l'état de chargement
   - [ ] Déclencher le téléchargement

3. **Finalisation**
   - [ ] Tests avec différents formats
   - [ ] Vérifier multi-navigateurs

## Notes

- Évolution future : export batch de plusieurs rapports
```

---

## Characteristics

- 2-3 phases with checkboxes
- ~200-300 words total
- Always end with Finalisation
