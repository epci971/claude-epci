Voici le **Guide n°12 – Performance & scalabilité – Gardel 2025**.

Objectif : définir comment garder l’application Gardel **rapide, robuste et scalable**, en production comme en montée en charge, en cohérence avec :

- l’architecture Django/DRF + ETL définie dans les guides précédents,
    
- PostgreSQL comme base principale,
    
- Celery + Redis pour les tâches async,
    
- les contraintes métier (labo, production, taxe de séjour, BI).
    

---

# 1. Principes généraux de performance dans Gardel

## 1.1. Ce que l’on cherche à optimiser

Trois familles de performances :

1. **Performances interactives**
    
    - Latence des vues HTML (backoffice) et des endpoints DRF (API).
        
    - Fluidité des filtres, listes, formulaires, dashboards React.
        
2. **Performances batch / ETL**
    
    - Temps de traitement des imports labo / production, agrégats, exports fiscaux.
        
    - Capacité à rejouer / replanifier sans saturer la base.
        
3. **Scalabilité globale**
    
    - Capacité à monter en charge (plus d’utilisateurs, plus de données) en ajoutant des ressources de manière contrôlée.
        

## 1.2. Règles de base

Quelques règles structurantes :

- **Mesurer avant d’optimiser** : logs, métriques, profiling (cf. Guide 13 Logging & observabilité, à venir).
    
- **Réduire le travail inutile** :
    
    - requêtes ORM superflues,
        
    - champs non nécessaires dans les sérialisations,
        
    - calculs répétitifs non mis en cache.
        
- **Désynchroniser** les traitements lourds :
    
    - ETL et calculs massifs → Celery / jobs planifiés (cf. Guide 10).
        
- **Déplacer les bonnes responsabilités au bon endroit** :
    
    - logique métier dans les services,
        
    - agrégations complexes éventuellement dans la base (SQL, index, vues matérialisées si besoin).
        

---

# 2. Optimisation ORM & base de données

Django ORM offre déjà un niveau de protection et d’optimisation raisonnable, à condition d’être utilisé correctement. La doc Django insiste notamment sur les points suivants : `select_related`, `prefetch_related`, `only/defer`, indexation, transactions, et éviter les N+1 queries.

## 2.1. Requêtes N+1 & chargement des relations

Pattern classique à éviter :

```python
# Vue naïve
sejours = Sejour.objects.all()
for sejour in sejours:
    commune = sejour.commune  # déclenche une requête par sejour
```

Solution :

- `select_related` pour les FK “one-to-one / many-to-one”,
    
- `prefetch_related` pour les relations “many-to-many / reverse FK”.
    

```python
sejours = Sejour.objects.select_related("commune").all()
```

Pour les listes exposées via DRF, appliquer `select_related/prefetch_related` dans le `queryset` du ViewSet :

```python
class SejourViewSet(ModelViewSet):
    queryset = (
        Sejour.objects
        .select_related("commune", "logement")
        .prefetch_related("occupants")
    )
```

À intégrer systématiquement dans les endpoints liste / export.

## 2.2. Champs ramenés : `only` / `defer`

Pour les tables volumineuses, ne pas ramener tous les champs si on n’en affiche que quelques-uns :

```python
Sejour.objects.only("id", "date_debut", "date_fin", "commune_id")
```

À utiliser avec parcimonie, notamment quand :

- les modèles ont des champs JSON ou des blobs lourds,
    
- l’API n’expose qu’un sous-ensemble de champs.
    

## 2.3. Indexation & migrations

Rappel du Guide Modèles :

- Indexer les champs utilisés dans les filtres, joins et ordres fréquents (dates, commune, statut, etc.).
    
- Ajouter des index composés si les requêtes filtrent souvent sur plusieurs colonnes (ex : `(commune_id, periode)`).
    

Exemples :

```python
class Meta:
    indexes = [
        models.Index(fields=["commune", "periode"]),
        models.Index(fields=["statut", "periode"]),
    ]
```

Sur PostgreSQL, utiliser aussi :

- `GIN` / `GIST` pour champs JSONB ou recherches full-text,
    
- `partial index` pour des cas ciblés (ex. `statut='EN_COURS'`).
    

Ces décisions doivent être basées sur l’observation des requêtes (EXPLAIN ANALYZE) et des stats de production.

## 2.4. Transactions & verrous

Pour les ETL et updates massifs :

- regrouper les opérations cohérentes dans une **transaction atomique** (`transaction.atomic()`),
    
- éviter de garder une transaction ouverte longtemps (risque de verrous longs côté PostgreSQL),
    
- privilégier des opérations batch (update / insert multiples) au lieu de boucles Python + `save()` individuels.
    

---

# 3. Performance API & DRF

## 3.1. Pagination obligatoire sur les listes

Toutes les listes non triviales (DRF) doivent être paginées :

- `PageNumberPagination` ou `LimitOffsetPagination` par défaut,
    
- `CursorPagination` pour les très grosses tables (ETL logs, historiques).
    

Côté config :

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}
```

Règles :

- ne jamais renvoyer plusieurs milliers de lignes en une seule réponse,
    
- documenter la pagination pour les consommateurs API (front, BI, etc.).
    

## 3.2. Filtres, recherche & ordering

Les filtres DRF/django-filter permettent de limiter le volume renvoyé :

- `DjangoFilterBackend` pour les filtres explicites,
    
- `SearchFilter` pour la recherche texte (sur champs ciblés),
    
- `OrderingFilter` avec liste blanche des champs autorisés.
    

Veiller à :

- ne pas laisser `ordering_fields = "__all__"`,
    
- ne pas autoriser l’ordering sur des champs non indexés en production,
    
- limiter la recherche full-text sur des champs raisonnables.
    

## 3.3. Sérialisation & champs calculés

Les serializers DRF peuvent devenir un goulot d’étranglement si :

- beaucoup de champs calculés par objet,
    
- appels à d’autres services dans `to_representation`.
    

Bonne pratique :

- garder les serializers **minces**,
    
- pré-calculer les agrégats en base (annotate) ou via services en amont,
    
- éviter les boucles Python sur de gros QuerySets (préférer `annotate`, `aggregate`).
    

---

# 4. Cache : niveaux & stratégies

Django propose plusieurs mécanismes de cache (cache global, par vue, par fragment, per-site). Nous les utilisons en complément de l’optimisation ORM.

## 4.1. Caches techniques

- `locmem` en dev,
    
- **Redis** en prod (déjà présent pour Celery) :
    
    - cache global,
        
    - caches par vue,
        
    - éventuellement caches applicatifs (services).
        

Configuration type (rappel Guide Settings) :

```python
CACHES = {
    "default": env.cache(
        "DJANGO_CACHE_URL",
        default="locmem://",
    )
}
```

## 4.2. Cache par vue / endpoint

Pour les vues DRF ou HTML peu changeantes, on peut utiliser :

- `@cache_page(timeout)` sur la vue,
    
- ou un mixin côté DRF.
    

Attention :

- à bien **invalider** ou limiter le timeout si les données changent fréquemment,
    
- à ne pas cacher des vues dépendant de droits utilisateurs sans prudence.
    

## 4.3. Cache applicatif (services)

Pour certains calculs coûteux :

- utiliser le cache Django dans les services :
    

```python
from django.core.cache import cache

def get_parametre_taxe(commune_id):
    key = f"parametre_taxe:{commune_id}"
    param = cache.get(key)
    if param is None:
        param = ParamTaxe.objects.get(commune_id=commune_id)
        cache.set(key, param, 300)  # 5 minutes
    return param
```

À utiliser pour les paramètres et référentiels peu changeants, consultés très fréquemment.

---

# 5. ETL & performance batch

## 5.1. Découpage & granularité

Pour les jobs ETL (labo, production, taxe) :

- découper les traitements en **lots** raisonnables (batchs),
    
- éviter les “gros monolithes” de plusieurs centaines de milliers de lignes en une seule transaction.
    

Patrons :

- lecture fichier / source en streaming ou chunk (pandas avec `chunksize`, par exemple, si utilisé),
    
- insertion par lot (bulk_create, upserts, etc.),
    
- journalisation des progressions (nb lignes traitées, %).
    

## 5.2. Bulk operations

Utiliser :

- `bulk_create` / `bulk_update` lorsque c’est possible,
    
- ou des `INSERT ... ON CONFLICT` côté PostgreSQL via ORM ou SQL brut maîtrisé, si besoin d’upsert massif.
    

Attention :

- `bulk_create` ne déclenche pas les signaux de modèle (`save`, `post_save`, etc.), ce qui est généralement souhaitable pour des ETL (logique explicite dans les services plutôt que dans les signaux).
    

## 5.3. Désynchronisation & ordonnancement

Comme défini au Guide 10 :

- les traitements lourds doivent passer par Celery,
    
- les jobs planifiés doivent être distribués dans le temps (pas tout à 02h00 du matin),
    
- il peut être utile de :
    
    - prioriser certaines queues,
        
    - limiter le nombre de workers sur certains jobs sensibles.
        

---

# 6. Scalabilité de l’application Django

## 6.1. Scalabilité horizontale

Django est stateless par conception (sessions en base/cache, pas en mémoire du process), ce qui permet :

- d’ajouter plusieurs containers / instances derrière un load balancer,
    
- d’augmenter la capacité en ajoutant des workers WSGI/ASGI.
    

Conditions :

- les **sessions** ne doivent pas être stockées uniquement en mémoire (utiliser DB ou cache partagé),
    
- les fichiers uploadés doivent être en stockage partagé ou externalisé (S3, équivalent, ou volume partagé).
    

## 6.2. Base de données

Le principal goulot d’étranglement est souvent la **base de données** :

- optimiser les requêtes (cf. §2),
    
- ajouter de la capacité (CPU/RAM, disques rapides),
    
- considérer des index adaptés,
    
- potentiellement utiliser :
    
    - des **réplicas en lecture** (si très gros volume de lecture),
        
    - des mécanismes de sharding uniquement si la volumétrie le justifie (probablement pas dans une première phase Gardel).
        

## 6.3. Workers Celery

Scalabilité côté tâches :

- augmenter le nombre de workers,
    
- distribuer les tâches sur plusieurs machines,
    
- segmenter les queues :
    
    - `high_priority` (petits jobs critiques),
        
    - `etl_heavy` (ETL lourds),
        
    - `notifications`, etc.
        

---

# 7. Performance front / UX (backoffice + React)

Même si ce guide est centré backend, quelques points :

- pagination et filtres côté serveur (DRF) plutôt que chargement massif côté front,
    
- éviter les tableaux gigantesques en backoffice ; prévoir :
    
    - pagination,
        
    - filtres,
        
    - exports CSV/Excel pour analyses lourdes (via ETL / jobs dédiés),
        
- côté React, privilégier :
    
    - requêtes ciblées,
        
    - affichage progressif (skeletons, loaders),
        
    - mémorisation (memoization) de certaines données partagées.
        

---

# 8. Stratégie de test de performance & monitoring

## 8.1. Tests de performance

Pour les cas critiques :

- tests de montée en charge (locust, k6, JMeter, etc.) sur les endpoints API les plus sollicités,
    
- tests de durée des jobs ETL sur des jeux de données représentatifs,
    
- définition de **SLOs** (objectifs de temps de réponse, temps de traitement).
    

## 8.2. Monitoring

Lié au Guide 13 Logging & observabilité, mais à anticiper :

- métriques :
    
    - temps moyen de réponse par endpoint,
        
    - nombre de requêtes,
        
    - taux d’erreur,
        
    - temps de traitement des jobs Celery,
        
- dashboards (Prometheus/Grafana, autre),
    
- alertes sur :
    
    - latence anormalement élevée,
        
    - files Celery qui s’allongent,
        
    - saturation DB.
        

---

# 9. Checklist “Performance & scalabilité – Gardel”

À utiliser comme grille de contrôle lors des revues et des déploiements.

### 9.1. ORM & DB

-  Les listes (vues / API) utilisent `select_related` / `prefetch_related` pour les relations fréquentes.
    
-  Les champs filtrés / ordonnés sont indexés (simple ou composé).
    
-  Pas de boucles Python avec `obj.related_set.all()` dans des listes volumineuses.
    

### 9.2. API & DRF

-  Toutes les listes API sont paginées (taille raisonnable, ex. 50).
    
-  Les endpoints critiques ont des filtres ciblés, pas de “tout renvoyer”.
    
-  Les serializers ne réalisent pas de gros calculs par objet ; les agrégats sont pré-calculés (annotate, services).
    

### 9.3. Cache

-  Un backend cache approprié est configuré (Redis en prod).
    
-  Les paramètres / référentiels souvent consultés sont mis en cache.
    
-  Les vues peu changeantes peuvent être cachées avec des timeouts adaptés.
    

### 9.4. ETL & async

-  Les jobs ETL sont découpés en lots raisonnables.
    
-  Les traitements lourds sont exécutés via Celery (et non dans le thread HTTP).
    
-  Les ETL importants utilisent des opérations bulk lorsque c’est pertinent.
    

### 9.5. Scalabilité

-  L’application est stateless (sessions en DB/cache, fichiers sur stockage partagé).
    
-  La stack permet d’ajouter des instances web / workers sans modification de code.
    
-  Des queues Celery distinctes existent pour séparer les charges (priorités, types de jobs).
    

### 9.6. Monitoring & tests de perf

-  Des métriques de base sont collectées (latence, erreurs, files Celery).
    
-  Des tests de charge ont été effectués sur les endpoints critiques.
    
-  Les jobs ETL critiques sont surveillés (durée, échecs, backlog).
    

---

Si tu veux, on peut enchaîner avec le **Guide n°13 – Logging & observabilité**, qui viendra compléter ce guide en détaillant :

- la configuration `LOGGING` Django,
    
- la structuration des logs applicatifs,
    
- les métriques à collecter,
    
- et la façon d’utiliser ces informations pour piloter la performance Gardel.