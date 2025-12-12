Voici le **Guide n°11 – Tests & qualité logicielle – Gardel 2025**.

Objectif : définir une stratégie claire, réaliste et industrialisable de tests pour le projet Gardel (Django + DRF + ETL + React), utilisable :

- par l’équipe de dev (back / front),
    
- dans la CI (Gardel Git / Docker),
    
- par tes agents IA / IDE (Cursor, etc.) comme règles de génération / refactor.
    

---

# 1. Rôle des tests dans l’architecture Gardel

## 1.1. Ce que les tests doivent couvrir

Dans le contexte Gardel, on doit sécuriser :

- les **règles métier** (services d’application, calcul taxe, règles labo, etc.),
    
- les **intégrations** (DRF, ETL, imports/exports, tâches async),
    
- les **contrats d’API** (schémas, statuts, permissions),
    
- les **interfaces backoffice** critiques (flux principaux),
    
- la **non-régression** lors des montées de version (Django, DRF, libs).
    

## 1.2. Pyramide de tests adaptée à Gardel

Pyramide recommandée (inspirée des bonnes pratiques courantes) :

- **60–70 %** : tests unitaires / “service layer”
    
    - services d’application, services ETL, utils, validation métier.
        
- **20–30 %** : tests d’intégration
    
    - ORM (requêtes complexes), DRF, permissions, tâches Celery, commandes de management.
        
- **10 %** : tests end-to-end / UI
    
    - scénarios métier représentatifs (via API, éventuellement Cypress/Playwright côté front).
        

Idée clé :  
On ne teste **pas tout par l’UI**. On verrouille surtout la **couche service + API**, qui est le cœur du système.

---

# 2. Stack de test recommandée

## 2.1. Outils de base (backend)

Back Django/Gardel :

- **pytest** + **pytest-django** : framework de test moderne, concis, largement adopté
    
- **Django TestCase** via pytest-django (fixtures DB, client test Django),
    
- **rest_framework.test.APIClient** pour les tests DRF (API)
    
- **coverage.py** pour mesurer la couverture de tests
    

Ce combo est devenu un standard de facto pour les projets Django sérieux.

## 2.2. Outils front (optionnel dans ce guide)

Front React :

- tests unitaires/composants avec **Vitest** / Jest + Testing Library,
    
- tests E2E possibles avec Cypress/Playwright.
    

On pourra faire un guide dédié front si besoin. Ici, on cadre surtout le **backend Python/Django/DRF/ETL**.

---

# 3. Organisation des tests dans l’arborescence

## 3.1. Structure par app

On suit la logique déjà posée (guides précédents) et on ajoute des dossiers `tests/` par app :

```text
apps/
  taxe_sejour/
    models/
    services/
    api/
    forms/
    views/
    tests/
      __init__.py
      test_models.py
      test_services.py
      test_api.py
      test_forms.py
      test_tasks.py

  labo/
    services/
    api/
    tests/
      test_etl_import.py
      test_api_labo.py

shared/
  services/
    tests/
      test_utils.py
```

Principes :

- **un `tests/` par app**, jamais un gros dossier `tests/` global fourre-tout.
    
- séparation par type de test :
    
    - `test_models.py`,
        
    - `test_services.py`,
        
    - `test_api.py`,
        
    - `test_forms.py`,
        
    - `test_tasks.py`, etc.
        

## 3.2. Types de tests par couche

- **Models** : intégrité du modèle, contraintes, méthodes custom simples.
    
- **Services** : logique métier, agrégations, ETL “pure logique”.
    
- **API/DRF** : statuts HTTP, schéma minimal, permissions, pagination, filtres.
    
- **Forms** : validation, messages d’erreur, cohérence champs.
    
- **Tasks/ETL** : comportement des services ETL et des tâches Celery/commands.
    

---

# 4. Tests unitaires : services, utils, règles métier

Cible principale : **services d’application** (guide n°3) et services ETL (guide n°10).

## 4.1. Exemple : service métier taxe de séjour

```python
# apps/taxe_sejour/services/usecases/calculer_taxe_sejour.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TaxeResultat:
    montant: Decimal
    devise: str
    statut: str

def calculer_taxe_sejour(sejour, parametres) -> TaxeResultat:
    # logique métier pure
    ...
```

Test unitaire :

```python
# apps/taxe_sejour/tests/test_services.py
import pytest
from decimal import Decimal
from apps.taxe_sejour.services.usecases.calculer_taxe_sejour import (
    calculer_taxe_sejour,
    TaxeResultat,
)

@pytest.mark.django_db
def test_calculer_taxe_sejour_cas_simple(sejour_factory, parametre_taxe_commune):
    sejour = sejour_factory(
        duree_nuits=3,
        nb_occupants=2,
        commune=parametre_taxe_commune.commune,
    )

    resultat = calculer_taxe_sejour(sejour, parametre_taxe_commune)

    assert isinstance(resultat, TaxeResultat)
    assert resultat.montant == Decimal("...")  # attendu métier
    assert resultat.devise == "EUR"
    assert resultat.statut == "OK"
```

Points clés :

- on privilégie des **services purs** autant que possible, pour faciliter les tests.
    
- `pytest.mark.django_db` est utilisé si le service touche l’ORM (création/lecture d’objets).
    
- les fixtures (`sejour_factory`, `parametre_taxe_commune`) sont définies dans `conftest.py`.
    

## 4.2. Factories & fixtures

On conseille :

- **factory_boy** ou **model_bakery** pour créer des instances de modèles rapidement
    

Exemple (factory_boy) :

```python
# apps/taxe_sejour/tests/factories.py
import factory
from apps.taxe_sejour.models import Sejour, Commune

class CommuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Commune

    nom = "Lamentin"
    code_insee = "97120"

class SejourFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sejour

    commune = factory.SubFactory(CommuneFactory)
    # autres champs...
```

---

# 5. Tests d’intégration : ORM, DRF, formulaires, ETL

## 5.1. Tests DRF (API)

On utilise `APIClient` de DRF pour tester les endpoints

```python
# apps/taxe_sejour/tests/test_api.py
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_list_taxes_needs_auth():
    client = APIClient()
    response = client.get("/api/v1/taxe/taxes/")
    assert response.status_code == 401  # non authentifié

@pytest.mark.django_db
def test_list_taxes_ok(user_factory, taxe_factory):
    user = user_factory()
    taxe_factory()
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/taxe/taxes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1  # selon pagination
```

On teste :

- les statuts HTTP,
    
- l’application des **permissions**,
    
- la structure minimale du payload (ex. présence de `results`, `count`, etc. pour la pagination DRF).
    

## 5.2. Tests de formulaires

Tests typiques sur la validation (guide n°7) :

```python
# apps/sejour/tests/test_forms.py
from apps.sejour.forms.sejour_forms import SejourCreateForm

def test_sejour_form_dates_invalides():
    form = SejourCreateForm(
        data={
            "date_debut": "2025-08-10",
            "date_fin": "2025-08-05",
            "montant_total": 100,
        }
    )
    assert not form.is_valid()
    assert "__all__" in form.errors  # non_field_errors
```

## 5.3. Tests ETL & commandes

Pour un service ETL (guide n°10) :

```python
# apps/labo/tests/test_etl_import.py
from pathlib import Path
from apps.labo.services.etl.import_fichier import importer_fichier_labo

def test_importer_fichier_labo_minimal(tmp_path, sample_labo_file_factory):
    path = sample_labo_file_factory(tmp_path)  # crée un fichier CSV/XLSX minimal

    result = importer_fichier_labo(path)

    assert result.nb_lignes_lues > 0
    assert result.nb_erreurs == 0
```

Pour une **commande de management** :

```python
from django.core.management import call_command

def test_labo_import_daily_command(mocker):
    mock_import = mocker.patch(
        "apps.labo.management.commands.labo_import_daily.importer_fichier_labo"
    )

    call_command("labo_import_daily")

    mock_import.assert_called_once()
```

---

# 6. Tests des tâches async (Celery)

## 6.1. Tâches Celery testées comme des fonctions

Les bonnes pratiques Celery recommandent de **tester la logique métier en tant que fonctions** (services ETL) et de tester la tâche Celery comme un wrapper très mince

Exemple :

```python
# apps/taxe_sejour/tasks/taxe_etl_tasks.py
from celery import shared_task
from apps.taxe_sejour.services.etl.import_taxe import import_taxe

@shared_task
def import_taxe_async(source_url: str, user_id: int):
    return import_taxe(source_url=source_url, user_id=user_id)
```

Test :

```python
from apps.taxe_sejour.tasks.taxe_etl_tasks import import_taxe_async

def test_import_taxe_async_calls_service(mocker):
    mock_import = mocker.patch(
        "apps.taxe_sejour.tasks.taxe_etl_tasks.import_taxe"
    )

    import_taxe_async("http://exemple", 1)

    mock_import.assert_called_once_with(source_url="http://exemple", user_id=1)
```

Pour tester le **workflow Celery** (exécution dans la queue), on peut utiliser des configurations Celery “eager” dans les settings de test, mais cela reste secondaire par rapport au test du service lui-même.

---

# 7. Qualité globale : lint, format, type checking

## 7.1. Lint & format

Stratégie recommandée :

- **ruff** pour le linting (PEP8, import, détecter les erreurs courantes),
    
- **black** pour le formatage automatique,
    
- éventuellement **isort** si non géré par ruff.
    

Ces outils sont aujourd’hui largement adoptés pour Python et compatibles Django.

Pipeline typique :

```bash
ruff check .
black --check .
pytest --maxfail=1
coverage run -m pytest
coverage report
```

## 7.2. Typage (optionnel mais conseillé)

- Utiliser progressivement les **annotations de type** Python (déjà présentes dans les exemples : `TaxeResultat`, `ImportLaboResult`, etc.).
    
- Option : **mypy** pour vérifier les types sur les services / utils (moins prioritaire sur les vues).
    

---

# 8. Couverture & stratégie de non-régression

## 8.1. Couverture minimale

Avec `coverage.py`, on peut :

- mesurer la couverture,
    
- exclure certains fichiers (settings, `manage.py`, migrations).
    

Objectif réaliste Gardel :

- **> 80 % de couverture sur les services métier & ETL**,
    
- couverture globale projet autour de **60–70 %** (les views HTML étant souvent moins testées).
    

## 8.2. Ce qu’on doit impérativement couvrir

Priorité haute :

- services métier critiques :
    
    - calculs de taxe,
        
    - agrégations labo,
        
    - paramètres de commune / logement,
        
- API DRF :
    
    - endpoints exposés à l’extérieur,
        
    - endpoints utilisés par les écrans principaux (backoffice, React),
        
- ETL :
    
    - imports/exports récurrents,
        
    - tâches planifiées.
        

---

# 9. Intégration CI/CD

## 9.1. Pipeline minimal

Dans la CI (GitLab CI, GitHub Actions, autre), pipeline recommandé :

1. **Lint** : ruff + black (check).
    
2. **Tests unitaires & intégration** : `pytest`.
    
3. **Couverture** : `coverage run -m pytest`, `coverage report`.
    
4. **Checks Django** : `python manage.py check`, éventuellement `check --deploy` sur un settings de type prod.
    

## 9.2. Conditions de validation

- pipeline **rouge** si :
    
    - tests échouent,
        
    - linters échouent,
        
    - couverture sous un seuil minimal pour les services critiques (optionnelle mais conseillée).
        

---

# 10. Checklist “Tests & qualité – Gardel”

À utiliser comme règle d’équipe et pour la configuration des agents IA / IDE.

### 10.1. Organisation

-  Chaque app possède un dossier `tests/` avec des fichiers par type (`test_models.py`, `test_services.py`, `test_api.py`, …).
    
-  Les services métier & ETL ont des tests unitaires dédiés.
    
-  Les fixtures / factories sont centralisées proprement (`conftest.py`, `factories.py`).
    

### 10.2. Backend

-  `pytest` / `pytest-django` utilisés pour les tests.
    
-  `APIClient` DRF utilisé pour tester les endpoints API.
    
-  Les formulaires sont testés sur leurs validations critiques (dates, montants, champs obligatoires).
    
-  Les commandes de management ETL sont testées (au moins un test happy path).
    

### 10.3. Async & ETL

-  Les tâches Celery sont de simples wrappers autour de services testés.
    
-  Les services ETL sont idempotents et testés sur des fichiers d’exemple.
    
-  Les jobs planifiés critiques ont des tests (au moins ceux de leurs services sous-jacents).
    

### 10.4. Qualité globale

-  Lint (ruff) et format (black) intégrés dans la CI.
    
-  Couverture mesurée avec coverage, avec une cible minimale sur les services métier.
    
-  `manage.py check` (et idéalement `check --deploy`) exécuté régulièrement.
    

---

Si tu veux, on peut enchaîner sur le **Guide n°12 – Performance & scalabilité** en reprenant :

- les patterns d’optimisation ORM,
    
- le cache (par vue, par fragment, global),
    
- l’impact sur les ETL et l’API,
    
- et la façon d’intégrer ça dans la démarche qualité (tests de perf, alertes).