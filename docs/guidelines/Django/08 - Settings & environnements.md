Voici le **Guide n°8 – Settings & environnements (Django, projet Gardel, 2025)**.

Objectif : fournir un cadre clair, industrialisable et sécurisé pour la configuration Django (settings) du projet Gardel, utilisable :

- par les développeurs (mise en place locale, debug),
- par le chef de projet / architecte (validation des environnements),
- par l’ops / infra (déploiement Docker, CI/CD),
- comme “rules” pour tes agents IA / IDE.

Le guide s’appuie sur :

- la doc officielle Django sur les settings, la sécurité et la checklist de déploiement ([Django Project](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com))
- les bonnes pratiques 12-Factor (config par variables d’environnement) ([Twelve-Factor App](https://12factor.net/config?utm_source=chatgpt.com))
- les guides récents sur l’architecture des settings Django (settings modulaires, multi-environnements) ([Django Stars](https://djangostars.com/blog/configuring-django-settings-best-practices/?utm_source=chatgpt.com))
- l’architecture projet déjà définie dans le **Guide n°1** (config/settings/base-dev-test-prod)

Contexte Gardel : monolithe Django 5.x, PostgreSQL, API DRF, ETL, front React/Vite, déployé en environnements **dev / test / prod** (Docker).

---

# 1. Rappels fondamentaux & objectifs

## 1.1. Rôle des settings dans Django

Dans Django, le **module de settings** porte la configuration globale du projet : bases de données, middleware, apps installées, sécurité, caches, etc. ([Django Project](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com))

Formellement :

- un projet Django est défini **principalement par un module de settings** et un module d’URL racine ([Django Project](https://docs.djangoproject.com/en/5.2/ref/applications/?utm_source=chatgpt.com))
- un settings file est **un module Python** contenant des variables en majuscules (DEBUG, DATABASES, etc.) ([Django Project](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com))

Dans Gardel, les settings doivent :

- être **modulaires** (base + variantes par environnement),
- respecter les contraintes **sécurité / performance** en prod (checklist Django),
- être compatibles avec une configuration **Dockerisée** (variables d’environnement pilotées par `docker-compose` / orchestrateur),
- rester **lisibles** pour les développeurs (pas de “[settings.py](http://settings.py) monolithique” de 1000 lignes).

## 1.2. Enjeux spécifiques Gardel

Contexte métier / technique :

- plusieurs **apps métier** (labo, production, taxe_sejour, etc.) + **ETL** + **API DRF**
- **PostgreSQL** comme base principale (volumétrie, contraintes avancées, JSONB) ([Django Project](https://docs.djangoproject.com/en/5.2/ref/databases/?utm_source=chatgpt.com))
- **environnements multiples** :
    - dev local (DEBUG, outils de debug, DB locale),
    - test / CI (tests automatisés, DB éphémère),
    - prod (sécurisée, variables d’environnement, scaling).

Objectifs Gardel :

- respecter le principe **“config ≠ code”** (12-Factor) : les valeurs spécifiques à l’environnement (mots de passe, URLs, clés) ne sont pas dans le Git ([Twelve-Factor App](https://12factor.net/config?utm_source=chatgpt.com))
- rendre les settings **exploitables par les agents IA** (structure prévisible, limites par environnement),
- simplifier la commande `manage.py check --deploy` en prod (checklist sécurité) ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

---

# 2. Architecture des settings dans Gardel

## 2.1. Arborescence cible

On reprend et précise l’architecture posée dans le Guide n°1

```bash
backend/
  src/
    config/
      __init__.py
      settings/
        __init__.py
        base.py      # commun : apps, middleware, DRF, PostgreSQL...
        dev.py       # dev local / intégration
        test.py      # tests / CI
        prod.py      # prod Gardel
      urls.py
      asgi.py
      wsgi.py

```

Principe :

- `base.py` contient **tout ce qui est commun** à tous les environnements,
- chaque fichier d’environnement fait simplement :

```python
# dev.py / test.py / prod.py
from .base import *

# puis surcharge uniquement ce qui est spécifique
DEBUG = True  # ou False
DATABASES["default"]["HOST"] = env("DB_HOST", default="db")
...

```

Ce schéma (base + dev/prod/test) est un pattern recommandé depuis longtemps et encore d’actualité en 2025 ([Stack Overflow](https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings?utm_source=chatgpt.com))

## 2.2. Sélection de l’environnement

La sélection du module de settings se fait via la variable d’environnement **`DJANGO_SETTINGS_MODULE`** ([Django Project](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com))

Exemples :

- dev local :

```bash
export DJANGO_SETTINGS_MODULE="config.settings.dev"

```

- tests (CI) :

```bash
export DJANGO_SETTINGS_MODULE="config.settings.test"

```

- prod (Docker / serveur) :

```bash
export DJANGO_SETTINGS_MODULE="config.settings.prod"

```

Dans Docker, cela passe typiquement par :

```yaml
services:
  backend:
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}

```

---

# 3. Gestion des secrets & variables d’environnement

## 3.1. Règle absolue : aucun secret dans le dépôt

Rappel du Guide n°1 : **jamais** de `SECRET_KEY`, mots de passe ou tokens en dur dans Git

On s’aligne sur :

- la doc Django sécurité,
- la checklist de déploiement,
- la méthodologie 12-Factor (config dans l’environnement, pas dans le code) ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

**Conséquences pratiques :**

- tous les secrets (clé Django, mot de passe DB, credentials SMTP, tokens API) viennent de l’OS / Docker / orchestrateur,
- les fichiers `.env` sont **ignorés par Git** (`.gitignore`),
- les settings ne contiennent que :
    - des **valeurs par défaut non sensibles**, ou
    - des appels à `env("...")` avec fallback raisonnable en dev.

## 3.2. Utilisation de `django-environ` (recommandée)

`django-environ` permet de **parser les variables d’environnement** (bool, int, URLs de BDD, listes, etc.) et d’appliquer les principes 12-Factor proprement ([Django Environ](https://django-environ.readthedocs.io/?utm_source=chatgpt.com))

Patron dans `config/settings/base.py` :

```python
# config/settings/base.py
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)

# Optionnel : lecture d'un .env uniquement en dev/local
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)

DEBUG = env("DEBUG", default=False)

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-insecure-key-change-me")

```

Avantages :

- un seul point d’entrée pour les variables d’environnement,
- support natif de `DATABASE_URL`, `CACHES`, `EMAIL_URL`, etc. via des URLs ([Django Environ](https://django-environ.readthedocs.io/?utm_source=chatgpt.com))
- cohérent avec la philosophie Gardel de centraliser la configuration applicative.

---

# 4. Paramètres globaux dans `base.py`

L’idée : `base.py` contient **le socle stable du projet**. Chaque environnement ne change que ce qui est strictement nécessaire.

## 4.1. Noyau Django

Exemples de paramètres structurants (à figer dans `base.py`) ([Django Project](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com))

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps tierces
    "rest_framework",
    # Apps Gardel
    "apps.labo",
    "apps.production",
    "apps.taxe_sejour",
    "apps.referentiels",
    "apps.comptes",
    # ...
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

```

**Recommandations Gardel :**

- garder `INSTALLED_APPS` **structuré par blocs** (Django core / tierces / Gardel),
- documenter les apps “sensibles” (auth, comptes, ETL) dans un commentaire,
- ne pas multiplier les middlewares exotiques sans justification → impact perf & debug.

## 4.2. Langue, fuseau horaire, formats

Gardel est en Guadeloupe, mais les données peuvent recouper des fuseaux / normes différentes. On fixe néanmoins des conventions cohérentes :

```python
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "America/Guadeloupe"  # cohérent avec l’infra
USE_I18N = True
USE_L10N = True
USE_TZ = True

```

Remarque : Django recommande l’usage de `USE_TZ=True` pour éviter les problèmes de conversions horaires en prod ([Django Project](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com))

## 4.3. Base de données (PostgreSQL)

Deux options possibles :

1. via `DATABASE_URL` (recommandé, plus simple pour Docker / cloud),
2. via structure explicite `DATABASES['default']`.

Patron via URL :

```python
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://gardel:gardel@localhost:5432/gardel_dev",
    )
}

```

C’est aligné avec les recommandations 12-Factor et les guides `django-environ` pour la configuration BD ([Django Environ](https://django-environ.readthedocs.io/?utm_source=chatgpt.com))

Pour prod, seul l’URL change (gestion par l’infra).

---

# 5. Environnements : dev, test, prod

## 5.1. Dev (`dev.py`)

Objectif : confort développeur, **sans compromettre la sécurité** si la config fuit.

Exemple :

```python
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Ex : toolbar de debug uniquement en dev
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ["127.0.0.1"]

```

Règles Gardel :

- pas de données sensibles “trop réalistes” en dev (mots de passe de prod, etc.),
- possibilité de pointer sur une DB clone de prod → à gérer via `DATABASE_URL` local, pas dans le code,
- les outils de debug (Django Debug Toolbar, etc.) sont **strictement cantonnés** à `dev.py`.

## 5.2. Test / CI (`test.py`)

Objectif : exécuter les tests (unitaires, intégration) dans un environnement contrôlé.

```python
from .base import *

DEBUG = False  # on teste le comportement proche prod

# Base de tests : en mémoire / DB dédiée
DATABASES["default"] = env.db(
    "TEST_DATABASE_URL",
    default="postgres://gardel_test:gardel_test@localhost:5433/gardel_test",
)

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",  # plus rapide en tests
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

```

Règles Gardel :

- les tests ne doivent **jamais** impacter les données réelles,
- si on utilise Docker pour la CI, `TEST_DATABASE_URL` pointe vers un conteneur Postgres dédié.

## 5.3. Prod (`prod.py`)

Objectif : **sécurité, performance, robustesse**.

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["gardel.example.com"])

# Sécurité renforcée
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proxy SSL (si Nginx/Traefik en front)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

```

Ces réglages sont explicitement recommandés dans la doc Django (security topic + deployment checklist) et les guides de bonnes pratiques sécurité ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

---

# 6. Thématisation des settings (optionnel mais conseillé)

Pour les gros projets, certains auteurs recommandent de **segmenter les settings par thème** (database, cache, logging, DRF, etc.) pour éviter un `base.py` indigeste ([Medium](https://medium.com/django-unleashed/breaking-up-with-settings-py-a-smarter-django-settings-structure-not-env-based-4175d266bb25?utm_source=chatgpt.com))

Pattern possible dans Gardel :

```bash
config/settings/
  components/
    database.py
    cache.py
    security.py
    static_media.py
    logging.py
    drf.py
    email.py
  base.py
  dev.py
  test.py
  prod.py

```

Exemple dans `base.py` :

```python
from .components.database import DATABASES
from .components.cache import CACHES
from .components.static_media import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from .components.drf import REST_FRAMEWORK
from .components.logging import LOGGING

```

**Règle Gardel :**

- ok pour découper tant que :
    - les composants sont **bien nommés**,
    - on évite les imports circulaires,
    - un nouveau développeur peut retrouver facilement où se trouve un paramètre.

---

# 7. Static, media, caches & e-mail

## 7.1. Fichiers statiques & media

Paramètres typiques dans `base.py` + surcharges éventuelles :

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "assets",  # si besoin
]

```

En prod :

- servir les fichiers statiques via Nginx / proxy,
- éventuellement utiliser WhiteNoise ou un équivalent si on veut servir les statiques directement depuis l’app ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

## 7.2. Caches

Django supporte différents backends (locmem, Redis, etc.) ([Django Project](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com))

Pattern :

```python
CACHES = {
    "default": env.cache(
        "DJANGO_CACHE_URL",
        default="locmem://",
    )
}

```

- en dev : `locmem://` suffit,
- en prod : `redis://redis:6379/1` ou équivalent, piloté par `DJANGO_CACHE_URL`.

## 7.3. E-mails

```python
DEFAULT_FROM_EMAIL = "no-reply@gardel.local"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = True

```

- en dev : surcharger dans `dev.py` avec le backend console,
- en test : backend `locmem`.

---

# 8. Sécurité & conformité : settings à ne pas négliger

Synthèse des réglages “sensibles” listés dans la doc Django et les ressources sécurité ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

À activer / vérifier en **prod** :

- `DEBUG = False`
- `ALLOWED_HOSTS` correctement renseigné,
- `SECRET_KEY` robuste, venant d’une env var, non versionné,
- `SECURE_SSL_REDIRECT = True` (si HTTPS partout),
- `SESSION_COOKIE_SECURE = True`,
- `CSRF_COOKIE_SECURE = True`,
- `SECURE_HSTS_SECONDS > 0` (HSTS),
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` selon politique,
- `SECURE_PROXY_SSL_HEADER` si on est derrière un proxy,
- `X_FRAME_OPTIONS = "DENY"` (ou `SAMEORIGIN` selon besoin),
- `CSRF_TRUSTED_ORIGINS` si l’app est servie sur des domaines spécifiques.

Commande à intégrer dans le pipeline de déploiement :

```bash
python manage.py check --deploy --tag=security

```

---

# 9. Intégration Docker, CI/CD & environnements Gardel

## 9.1. Docker & `docker-compose`

Dans `docker-compose.yml` (exemple simplifié) :

```yaml
services:
  backend:
    build: ./backend
    env_file:
      - .env.prod
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=gardel
      - POSTGRES_USER=gardel
      - POSTGRES_PASSWORD=${DB_PASSWORD}

```

Le fichier `.env.prod` (non versionné) contient uniquement :

```
DJANGO_SECRET_KEY=...
DATABASE_URL=postgres://gardel:${DB_PASSWORD}@db:5432/gardel
DJANGO_ALLOWED_HOSTS=gardel.example.com
DJANGO_CACHE_URL=redis://redis:6379/1

```

## 9.2. CI/CD

Dans la CI :

- exécuter les tests avec `DJANGO_SETTINGS_MODULE=config.settings.test`,
- vérifier que les migrations passent (`manage.py migrate --check` peut être intégré),
- lancer `manage.py check --deploy` sur une config proche prod.

---

# 10. Checklist “Settings & environnements Gardel”

À utiliser en **revue de code** ou avant un déploiement.

### 10.1. Structure & modularisation

- [ ] Arborescence `config/settings/` présente avec `base.py`, `dev.py`, `test.py`, `prod.py`.
- [ ] `DJANGO_SETTINGS_MODULE` correctement renseigné pour chaque environnement.
- [ ] Pas de `settings.py` monolithique unique.

### 10.2. Secrets & variables d’environnement

- [ ] Aucun `SECRET_KEY` / mot de passe en clair dans Git.
- [ ] `.env*` dans `.gitignore`.
- [ ] `django-environ` (ou équivalent) utilisé proprement dans `base.py`. ([Django Environ](https://django-environ.readthedocs.io/?utm_source=chatgpt.com))
- [ ] `DATABASE_URL`, `DJANGO_CACHE_URL`, `EMAIL_*` fournis par l’environnement.

### 10.3. Distinction dev / test / prod

- [ ] `dev.py` : `DEBUG=True`, outils de debug activés uniquement ici.
- [ ] `test.py` : DB de test dédiée, backend mail mémoire, hashers rapides.
- [ ] `prod.py` : `DEBUG=False`, sécurité renforcée (cookies secure, HSTS, proxy SSL, etc.). ([Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com))

### 10.4. Sécurité

- [ ] `ALLOWED_HOSTS` correctement renseigné en prod.
- [ ] `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` = True en prod.
- [ ] `SECURE_SSL_REDIRECT` actif si HTTPS.
- [ ] `SECURE_HSTS_SECONDS` configuré.
- [ ] `python manage.py check --deploy --tag=security` OK.

### 10.5. Infra & CI/CD

- [ ] Docker / orchestrateur fournit toutes les env vars nécessaires.
- [ ] La CI utilise `config.settings.test`.
- [ ] Les scripts de déploiement exécutent :
    - migrations,
    - collectstatic,
    - `check --deploy`.

---

Si tu veux, on pourra ensuite décliner ce guide en un **exemple concret Gardel** (`base.py`, `dev.py`, `prod.py` complets, alignés avec ta stack Docker) ou le spécialiser pour l’intégration DRF / Celery / ETL (caches, queues, etc.).