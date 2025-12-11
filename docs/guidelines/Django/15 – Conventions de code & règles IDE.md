Voici le **Guide n°15 – Conventions de code & règles IDE – Gardel 2025**.

Objectif : définir un cadre **clair, stable et exploitable par les outils** (Cursor, IDE, agents IA) pour :

- homogénéiser le code Python/Django/DRF/ETL,
    
- faciliter les revues, la maintenance et le refactor,
    
- donner des règles explicites aux agents IA / assistants de code.
    

Ce guide s’appuie sur les conventions Python/Django (PEP 8, modèles de projet Django, bonnes pratiques DRF) et les outils modernes (ruff, black, pytest).

---

# 1. Principes généraux

## 1.1. Philosophie Gardel

Conventions gardées en tête pour tout le code :

1. **Lisibilité > astuce**  
    On préfère un code légèrement plus verbeux mais clair, aux one-liners obscurs.
    
2. **Séparation des responsabilités**
    
    - modèles = persistance,
        
    - services = logique métier,
        
    - vues / viewsets = orchestration I/O,
        
    - tâches = déclencheurs async (Celery),
        
    - forms/serializers = validation.
        
3. **Tests & refactor par défaut**  
    Tout nouveau code significatif doit être accompagnée de tests (au moins niveau service).
    
4. **Prédictibilité pour les outils IA / IDE**
    
    - arborescence stable,
        
    - noms cohérents,
        
    - conventions explicites → pour que Cursor & co puissent retrouver les bonnes zones et générer “au bon endroit”.
        

---

# 2. Style Python (PEP8, imports, formatage)

## 2.1. PEP 8, ruff, black

Référentiel :

- PEP 8 (conventions de code Python),
    
- ruff pour le lint,
    
- black pour le formatage.
    

Règles :

- indentation : 4 espaces, pas de tabulations,
    
- lignes ≤ 88 caractères (config black par défaut),
    
- noms :
    
    - variables, fonctions : `snake_case`,
        
    - classes : `PascalCase`,
        
    - constantes : `UPPER_SNAKE_CASE`.
        

## 2.2. Imports

Ordre des imports :

1. standard library,
    
2. package tiers (`django`, `rest_framework`, etc.),
    
3. packages internes (`apps.*`, `shared.*`).
    

Exemple :

```python
import logging
from dataclasses import dataclass
from datetime import date

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.taxe_sejour.models import Sejour
from apps.taxe_sejour.services.usecases.calculer_taxe_sejour import calculer_taxe_sejour
from apps.taxe_sejour.serializers import SejourSerializer
```

Pas d’`import *`.

Utiliser des alias seulement pour les cas classiques (`import logging`, `import decimal as dec` si vraiment justifié).

---

# 3. Conventions spécifiques Django

## 3.1. Modèles

- un fichier `models.py` par app **ou** (si volumineux) un package `models/` avec `__init__.py` qui agrège.
    
- nommage des modèles en **singulier** : `Sejour`, `Commune`, `TaxeSejour`, `ParamTaxe`.
    

Attributs :

- `created_at` / `updated_at` si traçabilité standard,
    
- pour les clés étrangères : `commune = models.ForeignKey("Commune", ...)` (nom clair, pas d’abréviation inutile),
    
- `related_name` explicite sur les relations inverses.
    

Meta :

```python
class Sejour(models.Model):
    ...

    class Meta:
        verbose_name = "Séjour"
        verbose_name_plural = "Séjours"
        ordering = ["-date_debut"]
        indexes = [
            models.Index(fields=["commune", "date_debut"]),
        ]
```

## 3.2. Vues Django (HTML) & URLs

- vues **class-based** par défaut (CBV), sauf cas ultra-simple,
    
- conventions :
    
    - `apps/<app>/views/<feature>_views.py`
        
    - `apps/<app>/urls.py` pour l’app, inclus dans `config/urls.py`.
        

URL naming :

- noms explicites : `"taxe_sejour:liste_sejours"`, `"taxe_sejour:detail_sejour"`.
    

---

# 4. Conventions DRF (API)

## 4.1. Organisation

Par app :

```text
apps/taxe_sejour/
  api/
    viewsets.py
    serializers.py
    filters.py     # si besoin
    urls.py
```

- `viewsets.py` : classes DRF (ViewSet, ModelViewSet, APIView).
    
- `serializers.py` : serializers DRF.
    
- `urls.py` : router + paths.
    

## 4.2. ViewSets

Convention :

- pour un CRUD standard : `ModelViewSet`,
    
- pour des endpoints métiers (actions custom) : ViewSet ou APIView dédiée.
    

Noms :

```python
class SejourViewSet(ModelViewSet):
    queryset = (
        Sejour.objects
        .select_related("commune", "logement")
        .prefetch_related("occupants")
    )
    serializer_class = SejourSerializer
    permission_classes = [IsAuthenticated, CanVoirSejourPermission]
```

Actions custom :

```python
from rest_framework.decorators import action

class SejourViewSet(ModelViewSet):
    ...

    @action(detail=True, methods=["post"])
    def recalculer_taxe(self, request, pk=None):
        ...
```

On respecte les conventions DRF pour les actions (`detail=True/False`, `methods=[...]`).

## 4.3. Serializers

Conventions :

- un serializer par use-case métier si besoin (ex: `SejourListSerializer`, `SejourDetailSerializer`, `SejourCreateSerializer`),
    
- pas de logique métier lourde dans les serializers (juste validation I/O).
    

Noms :

```python
class SejourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sejour
        fields = [
            "id",
            "date_debut",
            "date_fin",
            "montant_total",
            "commune",
            "logement",
        ]
```

---

# 5. Conventions services & couche applicative

Le **Guide n°3** définit la structure des services métier ; ici on fixe les conventions de code.

## 5.1. Organisation

Par app :

```text
apps/taxe_sejour/
  services/
    __init__.py
    usecases/
      __init__.py
      calculer_taxe_sejour.py
      generer_declaration_mensuelle.py
    queries/
      __init__.py
      sejours_par_commune.py
    etl/
      import_taxe.py
      export_collectivites.py
```

Principes :

- `usecases` → logique métier orchestrée (grands cas d’usage),
    
- `queries` → requêtes de lecture complexes (rapports, listings),
    
- `etl` → traitements d’import/export (cf. Guide 10).
    

## 5.2. Style de code dans les services

- fonctions orientées domaine,
    
- usage possible de `@dataclass` pour les DTO / résultats.
    

Exemple :

```python
# apps/taxe_sejour/services/usecases/calculer_taxe_sejour.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TaxeResultat:
    montant: Decimal
    devise: str
    statut: str  # OK / WARNING / ERROR
    message: str | None = None

def calculer_taxe_sejour(sejour, parametres) -> TaxeResultat:
    # 1. Validation
    # 2. Calcul
    # 3. Retour structuré
    ...
```

Conventions :

- pas d’accès direct à `request` dans les services,
    
- pas de référence aux vues / serializers,
    
- idéalement pas d’accès direct à la couche HTTP (pas de `Response`).
    

---

# 6. Conventions ETL & tâches async

## 6.1. ETL

Code ETL dans `services/etl/` suit les règles suivantes :

- une fonction principale par job (ex. `importer_fichier_labo`, `calculer_taxe_daily`),
    
- signature explicite (ne pas passer un dictionnaire flou),
    
- retour via dataclass si besoin de rapport.
    

## 6.2. Tâches Celery

Dans `apps/<app>/tasks/` :

```python
# apps/labo/tasks/labo_etl_tasks.py
from celery import shared_task
from apps.labo.services.etl.import_fichier import importer_fichier_labo

@shared_task
def importer_labo_fichier_task(path_str: str, user_id: int | None = None):
    ...
```

Règles :

- **tâche mince** qui appelle un service,
    
- pas de logique métier lourde dans le corps de la tâche,
    
- gestion des retries et log des erreurs dans la tâche (mais pas le cœur métier).
    

---

# 7. Conventions tests

## 7.1. Nom des fichiers & des fonctions

Fichiers :

- `test_models.py`,
    
- `test_services.py`,
    
- `test_api.py`,
    
- `test_etl.py`,
    
- `test_tasks.py`.
    

Fonctions :

- `test_<fonctionnalité>_<cas>` :
    

```python
def test_calculer_taxe_sejour_cas_simple(...): ...
def test_calculer_taxe_sejour_dates_invalides(...): ...
```

## 7.2. Usage de pytest

- marquage `@pytest.mark.django_db` lorsque l’accès DB est nécessaire,
    
- fixtures dans `conftest.py` ou fichiers dédiés.
    

---

# 8. Nommage & conventions métier

## 8.1. Domaines Gardel

On standardise les noms de domaines dans le code :

- `labo` (laboratoire),
    
- `production`,
    
- `taxe_sejour`,
    
- `sejour`,
    
- `logement`,
    
- `commune`,
    
- `parametre` / `parametre_taxe`,
    
- `referentiels` (si app transversale).
    

Ces noms se retrouvent partout :

- noms d’apps,
    
- noms de modèles,
    
- noms de services,
    
- noms de permissions.
    

## 8.2. Permissions & rôles

Pour les permissions DRF / Django :

- noms explicites : `can_voir_taxe`, `can_modifier_taxe`, `can_lancer_import_labo`,
    
- groupe de fonctions dans `apps/<app>/permissions.py` ou `domain/permissions.py`.
    

---

# 9. Règles IDE & agents IA (Cursor, etc.)

## 9.1. Dossier `.cursor` / config IDE

Objectif : fournir à Cursor/IDE un “contrat” clair :

- dossier `.cursor/` ou équivalent avec :
    
    - règles globales,
        
    - chemins importants (`apps`, `shared`, `config`),
        
    - conventions (ex. où créer un nouveau service, où créer un test, etc.).
        

Lignes directrices :

- **création de nouvelles fonctionnalités** :
    
    - modèle → `apps/<app>/models.py`,
        
    - service métier → `apps/<app>/services/usecases/`,
        
    - serializer → `apps/<app>/api/serializers.py`,
        
    - viewset → `apps/<app>/api/viewsets.py`,
        
    - test de service → `apps/<app>/tests/test_services.py`,
        
    - test API → `apps/<app>/tests/test_api.py`.
        
- **jamais créer de code métier dans `config/`**, uniquement :
    
    - settings,
        
    - urls racine,
        
    - asgi/wsgi,
        
    - celery config.
        

## 9.2. “Rules” pour les agents IA

Règles clés à intégrer dans les prompts d’agents :

1. **Toujours respecter l’architecture par app**
    
    - ne pas mélanger les domaines,
        
    - ne pas créer de services dans `views.py`.
        
2. **Toujours créer les tests avec le code**
    
    - au moins un test pour chaque nouveau service métier,
        
    - au moins un test API pour chaque nouvel endpoint DRF.
        
3. **Ne pas inventer de stack**
    
    - rester dans Django/DRF/PostgreSQL/Celery/Redis.
        
4. **Respecter les conventions de nommage**
    
    - `SejourViewSet`, `SejourSerializer`, `calculer_taxe_sejour`, etc.
        
5. **Respecter les guides précédents**
    
    - settings modulaires,
        
    - sécurité (`IsAuthenticated` par défaut),
        
    - ETL via services + tâches Celery minces,
        
    - logging via `logging.getLogger("apps.<app>...")`.
        

---

# 10. Règles spécifiques pour refactor & review

## 10.1. Refactor

Lors de refactors (humain ou IA) :

- **ne pas casser la structure** (ne pas fusionner services et vues),
    
- **isoler la logique métier** dans des services testables,
    
- ajouter ou adapter les tests existants,
    
- vérifier les imports (supprimer ceux non utilisés, garder l’ordre).
    

## 10.2. Code review

Liste de contrôle :

- la nouvelle fonctionnalité suit-elle la structure `models → services → API/tests` ?
    
- les noms sont-ils cohérents (FR, domaine Gardel) ?
    
- y a-t-il des “odeurs” :
    
    - logique métier dans des serializers,
        
    - grosses fonctions non découpées,
        
    - duplication de code évidente,
        
    - absence de tests ?
        

---

# 11. Résumé pour agents & IDE

Pour utilisation directe dans un outil (résumé ultra-condensé) :

- **Stack** : Django 5, DRF, PostgreSQL, Celery, Redis, pytest, ruff, black.
    
- **Structure** :
    
    - `apps/<app>/models.py`
        
    - `apps/<app>/services/{usecases,queries,etl}/`
        
    - `apps/<app>/api/{viewsets.py,serializers.py,urls.py}`
        
    - `apps/<app>/tasks/`
        
    - `apps/<app>/tests/{test_services.py,test_api.py,...}`
        
- **Conventions** :
    
    - noms en snake_case pour fonctions, PascalCase pour classes,
        
    - services = logique métier pure, réutilisable,
        
    - tasks Celery = wrappers minces,
        
    - DRF : `IsAuthenticated` par défaut, permissions métier custom,
        
    - tests partout, avec pytest.
        

---

Si tu veux, on peut encore ajouter un **Guide n°16 (optionnel) – Front React/Vite dédié** pour cadrer la partie front si tu pars sur un front séparé de Django, avec les mêmes niveaux de rigueur (naming, architecture, intégration API).