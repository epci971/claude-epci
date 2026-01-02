# Brief Template — Major Feature

> Template for complex features (8h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | > 200 words |
| Verb type | Architectural (concevoir, refondre) |
| Scope | Complex, multi-faceted |
| Components | 3+ OR external integrations |

---

## Template

```markdown
# {Action Verb} {Feature Description}

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: {HIGH|MEDIUM|LOW}

## Objectif

{3-4 sentences on purpose, benefit, strategic importance}

## Description

{2-3 paragraphs on context, functioning, key considerations}

## Exigences fonctionnelles

- {FR1: Detailed behavior}
- {FR2: Detailed behavior}
- {FR3: Detailed behavior}
- {FR4: Detailed behavior}

## Exigences non-fonctionnelles

- {NFR1: Performance/security/reliability}
- {NFR2: Scalability/maintainability}

## Contraintes techniques

- {Technical stack constraints}
- {External system constraints}
- {Data format constraints}

## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Définir modèles de données
   - [ ] Créer migrations
   - [ ] Documenter interfaces

2. **Backend — Core Logic**
   - [ ] Créer service principal
   - [ ] Implémenter règles métier
   - [ ] Ajouter validation

3. **Backend — Integration**
   - [ ] Client API externe
   - [ ] Gestion erreurs et retry
   - [ ] Tâches asynchrones

4. **Frontend — Main Views**
   - [ ] Composant principal
   - [ ] Formulaires et interactions
   - [ ] États loading/error

5. **Finalisation**
   - [ ] Tests unitaires (coverage >80%)
   - [ ] Tests intégration
   - [ ] Documentation technique
   - [ ] Documentation utilisateur

## Notes

- {Pending decisions}
- {Risks or dependencies}
- {Future evolution}
```

---

## Example

```markdown
# Implémenter le calcul TCB automatique avec synchronisation laboratoire

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: MEDIUM

## Objectif

Automatiser le calcul du TCB en intégrant les données laboratoire en temps réel.
Cette fonctionnalité remplace le processus manuel par une solution fiable et traçable.
Elle permettra aux opérateurs de suivre la production en continu.

## Description

Le module TCB récupère automatiquement les mesures laboratoire (Brix, Pol, Pureté),
applique les formules de calcul officielles, et génère les rapports réglementaires.

Le système gère les cas de mesures manquantes ou aberrantes avec alertes.
L'historique complet est conservé pour audit.

## Exigences fonctionnelles

- Le système récupère les mesures toutes les 15 minutes
- Le système calcule le TCB selon la formule officielle
- Le système détecte les valeurs aberrantes
- L'utilisateur peut consulter l'historique avec graphiques

## Exigences non-fonctionnelles

- Temps de calcul < 2 secondes par batch
- Disponibilité 99.5% pendant production

## Contraintes techniques

- Intégration API laboratoire REST (JWT)
- Stack Django 4.x existant
- PostgreSQL avec partitionnement

## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Définir modèles CalculTCB, MesureLabo, AlerteTCB
   - [ ] Créer migrations avec index
   - [ ] Documenter interfaces API

2. **Backend — Service de calcul**
   - [ ] Créer TCBCalculator
   - [ ] Implémenter validation mesures
   - [ ] Système détection anomalies

3. **Backend — Synchronisation**
   - [ ] Tâche Celery récupération
   - [ ] Client API avec retry
   - [ ] Alertes email + notification

4. **Frontend — Dashboard**
   - [ ] Composant TCBDashboard
   - [ ] Vue historique avec filtres
   - [ ] Indicateurs d'état

5. **Finalisation**
   - [ ] Tests unitaires (>80%)
   - [ ] Tests intégration API
   - [ ] Documentation technique

## Notes

- Formule à valider avec responsable production
- Prévoir double-run pendant 2 semaines
- Risque : volume de données historiques
```

---

## Characteristics

- 5-6 detailed phases
- ~400-500 words total
- NFR section mandatory
- Notes with decisions/risks
