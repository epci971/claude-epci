Voici le **Guide n°14 – CI/CD & déploiement – Gardel 2025**.

Objectif : définir un **pipeline complet** de CI/CD pour le projet Gardel (Django + DRF + Celery + ETL + Docker), cohérent avec les guides précédents (tests, sécurité, logging, ETL, performance) et **exploitable** :

- par l’équipe de dev,
    
- par l’ops / infra,
    
- par tes agents IA / IDE (règles de génération / refactor / vérification).
    

---

# 1. Cadrage : ce que doit faire la CI/CD Gardel

## 1.1. Rôles de la CI

La CI (Continuous Integration) doit, à chaque push / merge :

1. **Vérifier la qualité du code**
    
    - linting (ruff, black check),
        
    - style et erreurs courantes.
        
2. **Exécuter la batterie de tests**
    
    - tests unitaires et d’intégration Django/DRF,
        
    - tests ETL et tâches Celery (au moins les services),
        
    - mesurer la couverture.
        
3. **Contrôler la cohérence du projet**
    
    - `manage.py check`,
        
    - éventuellement `check --deploy` sur des settings proches prod,
        
    - vérification des migrations.
        

## 1.2. Rôles de la CD

La CD (Continuous Delivery / Deployment) doit permettre :

1. **Build reproductible des images Docker**
    
    - image backend Django/DRF,
        
    - image worker Celery, beat, etc. si séparées.
        
2. **Déploiement automatique ou semi-automatique**
    
    - sur un environnement de **recette / préprod**,
        
    - puis sur **prod** (idéalement via un mécanisme de promotion).
        
3. **Exécution des étapes de mise à niveau**
    
    - migrations Django,
        
    - collectstatic,
        
    - checks de sécurité,
        
    - redémarrage/rolling update des services.
        

---

# 2. Stack technique CI/CD (hypothèses)

Pour le guide, on part sur une stack générique, adaptable :

- **Git** (GitLab, GitHub, autre) avec runner CI,
    
- **Docker** / docker-compose pour l’orchestration simple,
    
- cibles possibles :
    
    - VPS (Docker + compose),
        
    - ou plus tard un orchestrateur (Swarm / Kubernetes).
        

L’essentiel du guide reste valable quel que soit l’outil (GitHub Actions, GitLab CI, etc.) : seules les syntaxes de pipeline changent.

---

# 3. Découpage du pipeline : phases

On structure la CI/CD en **4 grandes phases** :

1. **Phase 1 – Static checks (lint / style / sécurité de base)**
    
2. **Phase 2 – Tests & couverture**
    
3. **Phase 3 – Build & publish des images Docker**
    
4. **Phase 4 – Déploiement & post-checks**
    

Chaque phase peut être un “stage” du pipeline.

---

# 4. Phase 1 – Static checks

## 4.1. Lint & format

Commandes recommandées (backend) :

```bash
ruff check .
black --check .
```

Objectifs :

- rattraper les erreurs de style,
    
- détecter des problèmes simples (imports morts, code mort, etc.).
    

## 4.2. Autres checks statiques (optionnel)

- `mypy` sur les services et utils si tu souhaites du type-checking,
    
- scan de dépendances (ex. `pip-audit`, `safety`) pour détecter des vulnérabilités connues dans les libs.
    

---

# 5. Phase 2 – Tests & couverture

## 5.1. Commandes de test

Avec pytest :

```bash
pytest --maxfail=1 --disable-warnings -q
```

Avec couverture :

```bash
coverage run -m pytest
coverage report
# ou coverage xml pour l’intégration CI
```

## 5.2. Checks spécifiques Django

- `python manage.py check`
    
- éventuellement `python manage.py check --deploy` sur les settings de prod (attention aux env vars nécessaires).
    

Pour `check --deploy`, on peut :

```bash
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py check --deploy
```

en s’assurant que les variables (SECRET_KEY fictive, etc.) sont fournies par la CI.

## 5.3. Tests DB & Celery

En CI :

- base de tests PostgreSQL dédiée (conteneur Docker `postgres`),
    
- Celery peut être configuré en mode “eager” pour simplifier certains tests (tâches exécutées immédiatement dans le process de test), mais la **logique métier** reste testée au niveau service (cf. guide Tests).
    

---

# 6. Phase 3 – Build & publish Docker

## 6.1. Images à prévoir

Minimum :

- `gardel-backend` : Django/DRF + code,
    
- `gardel-worker` : Celery worker (peut partager Dockerfile et image, avec une commande différente),
    
- éventuellement `gardel-beat` : Celery beat (scheduler),
    
- `gardel-nginx` : reverse proxy (si tu en as un défini, cf. autre conversation).
    

Schéma possible de Dockerfile unique paramétré via `CMD` / `ENTRYPOINT` :

```Dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# deps système, etc.

COPY backend/pyproject.toml backend/poetry.lock ./  # si poetry
# ou requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src

ENV DJANGO_SETTINGS_MODULE=config.settings.prod

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Pour le worker :

```yaml
services:
  web:
    image: registry.example.com/gardel-backend:<sha>
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
  worker:
    image: registry.example.com/gardel-backend:<sha>
    command: celery -A config worker -l info
  beat:
    image: registry.example.com/gardel-backend:<sha>
    command: celery -A config beat -l info
```

## 6.2. Tagging & registry

Stratégie de tags :

- `<sha>` (SHA du commit) pour l’identifiant immuable,
    
- `latest` ou `prod` pour un alias.
    

Exemple :

- `registry.example.com/gardel-backend:abc1234`
    
- `registry.example.com/gardel-backend:prod`
    

Le pipeline :

1. build image,
    
2. push vers registry (privée ou publique),
    
3. déclenche (ou permet) le déploiement.
    

---

# 7. Phase 4 – Déploiement & post-checks

## 7.1. Déploiement sur un serveur Docker / compose

Sur un VPS (classique dans ton contexte), on peut utiliser :

- un repo Git cloné côté serveur,
    
- un `docker-compose.prod.yml`,
    
- un script de déploiement qui :
    
    - récupère la nouvelle image,
        
    - applique les migrations,
        
    - redémarre les services.
        

Exemple de `docker-compose.prod.yml` simplifié :

```yaml
version: "3.9"

services:
  web:
    image: registry.example.com/gardel-backend:${IMAGE_TAG}
    env_file: .env.prod
    depends_on:
      - db
      - redis

  worker:
    image: registry.example.com/gardel-backend:${IMAGE_TAG}
    env_file: .env.prod
    command: celery -A config worker -l info
    depends_on:
      - db
      - redis

  beat:
    image: registry.example.com/gardel-backend:${IMAGE_TAG}
    env_file: .env.prod
    command: celery -A config beat -l info
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    env_file: .env.db

  redis:
    image: redis:7
```

Script de déploiement (pseudo) :

```bash
#!/usr/bin/env bash
set -e

IMAGE_TAG=$1  # commit SHA ou tag

export IMAGE_TAG

docker compose -f docker-compose.prod.yml pull web worker beat

docker compose -f docker-compose.prod.yml run --rm web \
  python manage.py migrate --noinput

docker compose -f docker-compose.prod.yml run --rm web \
  python manage.py collectstatic --noinput

docker compose -f docker-compose.prod.yml up -d web worker beat
```

La CI peut :

- soit se connecter en SSH au serveur et exécuter ce script,
    
- soit pousser un événement vers un outil de déploiement (ArgoCD, etc. si K8s).
    

## 7.2. Post-checks & health checks

Après déploiement :

- endpoints de **health check** :
    
    - `/healthz` : simple (OK / status DB),
        
    - `/readiness` : pour les orchestrateurs.
        
- script/verif :
    
    - `curl https://gardel.example.com/healthz`
        
    - vérifier `HTTP 200` et contenu attendu.
        

En cas d’échec, le pipeline ou l’outil de déploiement doit :

- notifier (Slack/mail/Teams),
    
- éventuellement **roll back** à l’image précédente.
    

---

# 8. Environnements : dev / recette / prod

## 8.1. Dev / feature branches

Sur les branches de dev / feature :

- CI complète (lint, tests, coverage),
    
- possibilité de build d’image et de déploiement sur un environnement de **prévisualisation** (optionnel).
    

## 8.2. Recette / préprod

Sur `develop` ou une branche `staging` :

- build & push image,
    
- déploiement automatique sur un environnement de **recette**,
    
- base de données de test, jeu de données anonymisées ou approximatives.
    

## 8.3. Prod

Sur `main` / `master` :

- build & push image,
    
- déploiement **semi-automatique** (validation manuelle) ou automatique selon ta politique,
    
- check `--deploy`, healthchecks, logs.
    

---

# 9. Intégration des guides précédents dans la CI/CD

On recolle les briques des guides 8 à 13 dans le pipeline :

- **Guide 8 – Settings & environnements**
    
    - utilisation stricte de `DJANGO_SETTINGS_MODULE` par env,
        
    - secrets via env vars, **jamais** dans le repo.
        
- **Guide 9 – Sécurité & conformité**
    
    - `check --deploy` dans le pipeline,
        
    - vérification des settings sensibles (`DEBUG=False`, `ALLOWED_HOSTS`, cookies secure, etc.).
        
- **Guide 10 – ETL, tâches planifiées & async**
    
    - services ETL testés en CI,
        
    - worker & beat inclus dans la stack de déploiement.
        
- **Guide 11 – Tests & qualité**
    
    - pytest + coverage obligatoire,
        
    - seuils de couverture sur les services métier.
        
- **Guide 12 – Performance & scalabilité**
    
    - tests spécifiques de perf (en jobs séparés),
        
    - vérification de l’utilisation de select_related/prefetch dans les endpoints critiques (via review + tests).
        
- **Guide 13 – Logging & observabilité**
    
    - configuration LOGGING active en prod,
        
    - logs envoyés vers stdout et collectés par l’infra.
        

---

# 10. Exemple de pipeline (pseudo GitLab CI ou GitHub Actions)

## 10.1. GitLab CI (pseudo-yaml)

```yaml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DJANGO_SETTINGS_MODULE: config.settings.test

lint:
  stage: lint
  script:
    - pip install -r requirements-dev.txt
    - ruff check .
    - black --check .

test:
  stage: test
  script:
    - pip install -r requirements-dev.txt
    - pytest --maxfail=1 --disable-warnings -q
    - coverage run -m pytest
    - coverage report
    - python manage.py check

build:
  stage: build
  script:
    - docker build -t registry.example.com/gardel-backend:$CI_COMMIT_SHA backend
    - docker push registry.example.com/gardel-backend:$CI_COMMIT_SHA
  only:
    - main
    - develop

deploy_prod:
  stage: deploy
  script:
    - ssh user@server "cd /srv/gardel && ./deploy.sh $CI_COMMIT_SHA"
  when: manual
  only:
    - main
```

Même logique transposable en GitHub Actions avec des jobs et steps équivalents.

---

# 11. Checklist “CI/CD & déploiement – Gardel”

### 11.1. CI

-  Lint (ruff, black) exécutés à chaque pipeline.
    
-  Tests `pytest` + coverage exécutés.
    
-  `manage.py check` (et éventuellement `check --deploy`) exécuté régulièrement.
    
-  Base de test PostgreSQL / Redis configurée dans la CI (si nécessaire pour tests d’intégration).
    

### 11.2. Build Docker

-  Dockerfile unique (ou clairement structurés) pour backend/worker/beat.
    
-  Images taggées avec le SHA du commit.
    
-  Images poussées vers un registry privé.
    

### 11.3. Déploiement

-  `docker-compose.prod.yml` (ou manifestes K8s) maintenu dans le repo infra.
    
-  Script de déploiement gérant :
    
    - pull des images,
        
    - `migrate`,
        
    - `collectstatic`,
        
    - redémarrage des services.
        
-  Health checks mis en place (endpoints `/healthz` / `/readiness`).
    

### 11.4. Sécurité & qualité

-  Secrets uniquement via variables d’environnement (pas dans Git).
    
-  `DEBUG=False` en prod, `ALLOWED_HOSTS` configuré.
    
-  Logs envoyés vers stdout, centralisés par l’infra.
    
-  Monitoring (latence, erreurs, jobs Celery) branché sur l’environnement prod.
    

---

Si tu le souhaites, on peut terminer la collection avec le **Guide n°15 – Conventions de code & règles IDE**, qui servira directement de base pour tes agents Cursor / IA (règles d’auto-génération et de refactor Python/Django/DRF/ETL + intégration avec la stack Gardel).