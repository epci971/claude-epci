# Brief Template — Major Feature

> Template for complex features (8h estimated)

---

## Detection Criteria

| Criterion | Value |
|-----------|-------|
| Word count | > 200 words |
| Verb type | Architectural (concevoir, architecturer, refondre) |
| Scope | Complex, multi-faceted |
| Components | 3+ |
| OR | External integrations |
| OR | Database schema changes |
| OR | Auth/security changes |

---

## Template Structure

```markdown
# {Action Verb} {Feature Description}

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: {HIGH|MEDIUM|LOW}

## Objectif

{3-4 sentences on purpose, benefit, and strategic importance}

## Description

{2-3 paragraphs on context, functioning, and key considerations}

## Exigences fonctionnelles

- {FR1: Detailed observable behavior}
- {FR2: Detailed observable behavior}
- {FR3: Detailed observable behavior}
- {FR4: Detailed observable behavior}

## Exigences non-fonctionnelles

- {NFR1: Performance/security/reliability}
- {NFR2: Scalability/maintainability}

## Contraintes techniques

- {Technical stack constraints}
- {External system constraints}
- {Data format/storage constraints}

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
   - [ ] Async tasks

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

- {Important pending decisions}
- {Risks or dependencies}
- {Future evolution considerations}
```

---

## Field Guidelines

### Title

**Format**: `{Verb} {Feature} {Qualifier/Context}`

**Architectural verbs**:
- Concevoir, Architecturer, Implémenter (complexe)
- Refondre, Migrer, Transformer
- Intégrer (système externe)

**Good examples**:
- "Implémenter le calcul TCB automatique avec synchronisation laboratoire"
- "Concevoir le système de notifications multi-canal"
- "Refondre l'architecture d'authentification SSO"
- "Intégrer le système de paiement Stripe"

### Objectif

3-4 sentences covering:
1. What the feature does (functional)
2. Why it's strategically important (business)
3. Who benefits and how (impact)
4. (Optional) What it replaces/improves

**Template**:
> {Verbe infinitif} {quoi} en {comment}. Cette fonctionnalité {bénéfice stratégique}. Elle permettra {à qui} de {faire quoi}, remplaçant {ancien processus si applicable}.

### Description

2-3 paragraphs covering:
- Integration context and dependencies
- High-level architecture decisions
- Key flows and interactions
- Edge cases and error handling considerations

### Exigences fonctionnelles

4-6 detailed FR:
- More specific than Standard
- Include edge cases if mentioned
- Group by functional area if many

### Exigences non-fonctionnelles

**Always include for Major** even if extrapolated from context:

| Category | Examples |
|----------|----------|
| Performance | Temps de réponse, throughput |
| Reliability | Disponibilité, failover |
| Security | Auth, chiffrement, audit |
| Scalability | Charge utilisateurs, volume données |
| Maintainability | Monitoring, logs, documentation |

If not explicitly mentioned, add reasonable defaults:
```markdown
## Exigences non-fonctionnelles

- Temps de réponse < 2 secondes pour les opérations utilisateur
- Logs structurés pour faciliter le debugging en production
```

### Contraintes techniques

Include all mentioned:
- Stack requirements (specific versions if mentioned)
- External systems (APIs, services)
- Data constraints (formats, volumes, retention)
- Infrastructure (servers, deployment)

### Plan d'implémentation

5-6 phases for Major:

1. **Architecture & Préparation** — Models, migrations, interfaces
2. **Backend — Core** — Main service, business logic
3. **Backend — Integration** — External APIs, async, queues
4. **Frontend — Main** — User-facing views
5. **Frontend — Admin** — Configuration, monitoring
6. **Finalisation** — Tests, docs

**Note**: Adapt phases to actual task. Skip "Admin" if no admin UI needed, etc.

### Notes

For Major, always include:
- Pending decisions (things to clarify)
- Dependencies (other systems, teams)
- Risks identified
- Future evolution path

---

## Complete Example

```markdown
# Implémenter le calcul TCB automatique avec synchronisation laboratoire

📦 **Feature majeure** | ⏱️ 8h | 🎯 Confidence: MEDIUM

## Objectif

Automatiser le calcul du TCB (Taux de Canne Broyée) en intégrant les données laboratoire en temps réel. Cette fonctionnalité remplace le processus manuel actuel par une solution fiable, traçable et conforme aux exigences réglementaires. Elle permettra aux opérateurs de suivre la production en continu et aux responsables d'accéder à des données fiables pour le pilotage.

## Description

Le module TCB s'intègre au workflow de production de l'usine Gardel. Il récupère automatiquement les mesures laboratoire (Brix, Pol, Pureté) via l'API existante, applique les formules de calcul officielles, et génère les rapports réglementaires.

Le système doit gérer les cas de mesures manquantes ou aberrantes. Un système d'alertes prévient les opérateurs pour intervention manuelle si nécessaire. L'historique complet est conservé pour audit et analyse de tendances.

La synchronisation s'effectue toutes les 15 minutes pendant les heures de production. Un mode manuel permet des calculs à la demande pour les tests ou corrections.

## Exigences fonctionnelles

- Le système récupère les mesures laboratoire automatiquement toutes les 15 minutes
- Le système calcule le TCB selon la formule officielle : `TCB = (Pol × Pureté) / Brix × Coefficient`
- Le système détecte les valeurs aberrantes (hors plage min/max configurable)
- Le système génère une alerte si données manquantes pendant plus de 30 minutes
- L'utilisateur peut consulter l'historique des calculs avec graphiques de tendance
- L'utilisateur peut exporter les données au format réglementaire (CSV structuré)
- Le système conserve un audit trail de toutes les modifications de paramètres

## Exigences non-fonctionnelles

- Temps de calcul < 2 secondes par batch de mesures
- Disponibilité 99.5% pendant les heures de production (6h-22h)
- Données conservées 10 ans minimum (contrainte réglementaire)
- Logs détaillés de chaque synchronisation pour debugging

## Contraintes techniques

- Intégration avec l'API laboratoire REST existante (authentification JWT)
- Stack Django 4.x existant
- Base PostgreSQL avec partitionnement pour l'historique volumineux
- Celery pour les tâches asynchrones de synchronisation

## Plan d'implémentation

1. **Architecture & Préparation**
   - [ ] Définir les modèles `CalculTCB`, `MesureLabo`, `AlerteTCB`, `ConfigTCB`
   - [ ] Créer les migrations Django avec index optimisés
   - [ ] Documenter les interfaces API internes et externes
   - [ ] Valider la formule de calcul avec le responsable production

2. **Backend — Service de calcul**
   - [ ] Créer le service `TCBCalculator` avec la logique métier
   - [ ] Implémenter la validation des mesures (plages, cohérence inter-mesures)
   - [ ] Créer le système de détection d'anomalies avec seuils configurables
   - [ ] Ajouter les endpoints API CRUD pour les calculs et configurations

3. **Backend — Synchronisation**
   - [ ] Créer la tâche Celery de récupération périodique des mesures
   - [ ] Implémenter le client API laboratoire avec retry et circuit breaker
   - [ ] Configurer les alertes (email + notification in-app)
   - [ ] Gérer le mode manuel pour calculs à la demande

4. **Frontend — Dashboard**
   - [ ] Créer le composant `TCBDashboard` avec graphiques temps réel (Recharts)
   - [ ] Implémenter la vue historique avec filtres date/période
   - [ ] Ajouter les indicateurs d'état (OK/Warning/Error) avec couleurs
   - [ ] Implémenter l'export CSV depuis l'interface

5. **Frontend — Administration**
   - [ ] Interface de configuration des seuils d'alerte
   - [ ] Gestion des coefficients de calcul par période
   - [ ] Visualisation des logs de synchronisation
   - [ ] Gestion des alertes (acquittement, historique)

6. **Finalisation**
   - [ ] Tests unitaires service calcul (coverage > 80%)
   - [ ] Tests d'intégration API laboratoire (mocks)
   - [ ] Tests de charge synchronisation (100 mesures/batch)
   - [ ] Documentation technique (architecture, API)
   - [ ] Documentation utilisateur (guide opérateur)
   - [ ] Plan de déploiement avec rollback

## Notes

- La formule de calcul exacte doit être validée avec M. Dupont (resp. production) avant développement
- Prévoir une phase de double-run (manuel + auto) pendant 2 semaines pour validation
- Dépendance : l'API laboratoire doit être stable (vérifier SLA avec équipe labo)
- Risque : volume de données historiques peut nécessiter optimisation requêtes
- Évolution future : intégration avec le système de reporting corporate
```

---

## Variation: Integration-Heavy

For features primarily about external integration:

```markdown
## Plan d'implémentation

1. **Analyse & Préparation**
   - [ ] Analyser la documentation API externe
   - [ ] Obtenir les credentials de test/staging
   - [ ] Définir le mapping de données entrant/sortant

2. **Client API**
   - [ ] Créer le client HTTP avec configuration
   - [ ] Implémenter l'authentification (OAuth/JWT/API Key)
   - [ ] Mapper les modèles de données

3. **Robustesse**
   - [ ] Implémenter retry avec exponential backoff
   - [ ] Ajouter circuit breaker pour pannes externes
   - [ ] Logging détaillé des échanges
   - [ ] Alerting sur erreurs répétées

4. **Intégration métier**
   - [ ] Connecter au workflow existant
   - [ ] Gérer les cas de données incohérentes
   - [ ] Implémenter les webhooks si bidirectionnel

5. **Frontend** (si applicable)
   - [ ] Interface de configuration connexion
   - [ ] Status de synchronisation visible
   - [ ] Historique des échanges

6. **Finalisation**
   - [ ] Tests avec sandbox externe
   - [ ] Tests de résilience (coupure réseau simulée)
   - [ ] Documentation d'intégration
   - [ ] Runbook pour incidents
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip NFR for Major | Always include NFR |
| Use < 5 phases | Use 5-6 detailed phases |
| Generic subtasks | Highly specific subtasks |
| Skip Architecture phase | Start with Architecture |
| Forget Finalisation | Always end with tests+docs |
| Empty Notes | Include decisions/risks/dependencies |
