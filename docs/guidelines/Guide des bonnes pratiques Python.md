# Guide des Bonnes Pratiques Django/DRF (2025) pour un Projet Industriel

## Contexte et Stack Technique

Dans le cadre d’un projet industriel de type _Gardel_, il est crucial de mettre en place une stack technique robuste et sécurisée en 2025. La stack recommandée comprend :

- **Django 4.x+ (Python)** – Framework web backend principal, réputé pour sa fiabilité et sa rapidité de développement. Django 4 apporte des améliorations de performance et supporte les versions récentes de Python (3.10+), tout en conservant sa philosophie "_batteries included_".
- **Django REST Framework (DRF)** – Extension de Django pour construire facilement des API REST. Permet de structurer des endpoints JSON pour alimenter des frontends ou services tiers.
- **PostgreSQL** – Base de données relationnelle robuste et riche en fonctionnalités (types JSON, index géospatiaux, etc.), parfaitement supportée par l’ORM de Django. PostgreSQL est le choix de prédilection pour les applications Django en production.
- **Frontend React** – Framework JavaScript moderne pour l’interface utilisateur. Le frontend est découplé du backend, communiquant via les APIs DRF (JSON). Cela implique de configurer les CORS correctement côté Django si le front est servi sur un domaine distinct.
- **Scripts Python de traitement de données (ETL)** – Pour les tâches d’import/export et de transformation de données (fichiers Excel, CSV, logs industriels), des scripts ou commandes Django dédiés seront utilisés (voir plus loin les _management commands_). Cela permet d’utiliser l’ORM Django et la logique métier existante lors des traitements hors requêtes web.
- **Docker** – Conteneurisation de l’application pour garantir un environnement cohérent entre développement, tests et production. Chaque composant (Django, base de données, etc.) tourne dans un conteneur isolé, facilitant le déploiement sur l’infrastructure cible.
- **Hébergement Cloud Privé** – Le déploiement se fait sur un cloud interne ou on-premise sécurisé. On peut utiliser une plateforme type OpenStack, Kubernetes on-premise, ou des VMs internes. Le choix impose de respecter les normes de sécurité de l’entreprise (LDAP interne, politique de patching, etc.) et d’assurer la portabilité (grâce aux conteneurs Docker notamment).

**Exigences industrielles particulières :** Ce type de projet gère probablement des **campagnes industrielles** (par exemple des campagnes de production journalières dans une usine). Cela induit des besoins spécifiques de **règles métiers par jour**, d’**historisation** des données de production, de **recalcul** en cas de corrections, et de génération de **bilans** en fin de campagne. Ces considérations influenceront la manière de concevoir les modèles, la base de données et les traitements batch pour garantir la traçabilité et la reproductibilité des calculs (voir section dédiée).

## Architecture du Projet et Organisation du Code

### Structure modulaire par applications Django

Une bonne pratique Django est de structurer le code en **applications (apps) modulaires** correspondant aux domaines métiers du projet. Plutôt que de tout mettre dans une seule app, on crée une app par fonctionnalité ou sous-domaine (par ex. `production`, `qualite`, `utilisateurs`, etc.). Chaque app contient ses modèles, vues, serializers, tests, etc., ce qui clarifie les responsabilités. Un tel découpage évite l’effet "_god app_" monolithique difficile à maintenir. Il est conseillé de regrouper toutes les apps dans un répertoire central (ex: `apps/`) pour garder le répertoire racine propre.

Par exemple, une arborescence de projet pourrait ressembler à :

```
myproject/
├── manage.py
├── config/                # Configurations globales
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py        # Paramètres communs
│   │   ├── dev.py         # Paramètres dev
│   │   └── prod.py        # Paramètres prod
│   ├── urls.py            # URL globales du projet
│   └── wsgi.py            # WSGI application
├── apps/
│   ├── production/        # App domaine "Production"
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services.py    # Logique métier spécifique
│   │   ├── tests.py
│   │   └── management/commands/  # Commandes custom (import, etc.)
│   ├── qualite/           # App domaine "Qualité"
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   └── utilisateurs/      # App pour gestion utilisateurs (auth, LDAP sync)
│       └── ...
├── common/                # Code réutilisable (utilitaires, mixins…)
│   ├── __init__.py
│   └── utils.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

```

Dans cette organisation :

- **`config/`** contient les réglages Django et la configuration du projet (urls globales, WSGI). On y sépare les **paramètres** par environnement (voir plus bas).
- **`apps/`** contient chaque app métier. Les noms d’apps reflètent des domaines fonctionnels. Chaque app a son propre `urls.py` inclus dans le routeur principal, ce qui cloisonne les routes.
- **`common/`** peut héberger des utilitaires partagés entre apps (plutôt que dupliquer du code ou créer des dépendances cycliques entre apps). Par exemple, des fonctions d’aide, mixins génériques, classes de base.
- On maintient `manage.py` à la racine pour exécuter les commandes Django. Les tests unitaires sont idéalement placés à côté du code qu’ils testent (par exemple dans chaque app, un fichier `tests.py` ou un package `tests/`), de sorte qu’en cas de faille, on localise vite l’origine.

Cette structure facilite **l’onboarding** des développeurs : elle reste proche du layout Django par défaut (pas de surprise pour trouver les settings, l’entrypoint `manage.py`, etc.) tout en étant organisée pour un projet de grande envergure.

### Paramètres de configuration (12-factor app)

La gestion des **settings** Django doit suivre le principe _12-factor_, séparant clairement le code de la configuration. On évite de tout mettre dans un seul `settings.py` monolithique. À la place, on peut :

- Créer un package `settings/` contenant par exemple `base.py` (valeurs par défaut communes), `development.py`, `production.py` etc. pour chaque environnement. On sélectionne le fichier approprié via la variable d’environnement `DJANGO_SETTINGS_MODULE` lors du déploiement.
- **Ne pas inclure les secrets ou données sensibles** (SECRET_KEY, mots de passe BD, clés API…) en clair dans le code versionné. Ces valeurs seront chargées depuis l’environnement (variables d’env ou fichiers de config séparés). Par exemple, utiliser la librairie **django-environ** ou **python-decouple** pour lire un fichier `.env` ou les variables d’env système. Ainsi, les mots de passe et clés ne fuitent pas dans le dépôt git, réduisant les risques de compromission.
- Versionner uniquement les paramètres génériques. Les différences (DEBUG on/off, paramètres de cache, email, etc.) sont gérées par les fichiers de settings spécifiques ou par des variables d’environnement.

Cette approche rend le projet conforme aux standards d’applications cloud-native. Elle facilite le **déploiement dans Docker et sur n’importe quel hébergement** : en isolant la config, il est plus aisé de packager l’app en conteneur et de la déployer sur divers environnements (VPS, Kubernetes, etc.). En outre, cela permet de **basculer d’une architecture monolithique à microservices** plus aisément si nécessaire, puisque chaque service peut consommer ses variables d’env sans dépendre d’un fichier de config unique.

**Bonnes pratiques supplémentaires sur les settings :** activer l’option `ALLOWED_HOSTS` en prod, désactiver `DEBUG`, configurer correctement la timezone et locale, utiliser `logging` configuré (voir plus loin), etc. Les valeurs sensibles (SECRET_KEY...) seront approvisionnées via le mécanisme sécurisé du cloud privé (vault interne ou variables protégées dans GitLab CI/CD).

### Qualité du code, tests et outils

Pour un projet industriel, la **maintenabilité** est primordiale. Adopter une discipline de code propre dès le départ facilite les évolutions futures :

- Suivre les conventions PEP8 et les standards Django. On peut intégrer des outils comme **flake8** et **black** pour le linting et le formatage automatique du code.
- Écrire des **tests automatisés** dès que possible (tests unitaires sur les utils et modèles, tests d’intégration sur les vues/API, tests fonctionnels si nécessaire). La couverture de tests doit idéalement être élevée et surveillée en CI. En 2025, une couverture complète est souvent _non négociable_ dans les projets pros. Des outils comme `pytest` (avec pytest-django) peuvent simplifier l’écriture des tests, et des librairies comme **factory_boy** aident à créer des données de test cohérentes.
- Inclure les tests dans le cycle de développement, par exemple en les exécutant automatiquement à chaque _commit_ via l’intégration continue (voir section CI/CD). Cela garantit qu’aucune régression n’est introduite sans être détectée rapidement.
- Exploiter les **abstract base models** de Django pour factoriser des champs communs. Par exemple, définir un modèle de base `TimeStampedModel` (avec champs `created_at`, `updated_at`) dont héritent les autres modèles métier, au lieu de répéter ces champs partout. De même pour d’autres patterns communs (ex: un champ `auteur_modification`, etc.).
- Documenter le code en utilisant des docstrings et éventuellement maintenir une documentation technique (avec Sphinx ou dans un `README.md` détaillé) décrivant l’architecture, les commandes disponibles, les conventions du projet, etc. Ceci est d’autant plus utile dans un contexte industriel où l’on peut avoir du turnover ou des intervenants externes.

## Composants Django : Modèles, Vues, Sérializers, Formulaires, Commandes, Services

Dans cette section, nous détaillons les bonnes pratiques pour chaque type de composant de l’application Django.

### Modèles et ORM Django

Les **modèles Django** représentent le cœur des données de l’application. Bonnes pratiques :

- **Concevoir des modèles en accord avec le domaine** : chaque table (modèle) doit correspondre à un objet métier identifiable (ex: _Campagne_, _LotProduction_, _AnalyseLaboratoire_, etc.). Profitez de la puissance de l’ORM Django pour exprimer les relations entre modèles (OneToOne, ForeignKey, ManyToMany) de manière claire.
- **Éviter les modèles anémiques** : on peut inclure dans les modèles certaines **logiques métier simples** liées aux données (méthodes d’instance ou de classe). Par exemple, une méthode `lot.calcul_indicateur()` calculant un indicateur à partir des champs du lot. Django encourage souvent des modèles « riches » en logique associée aux données elles-mêmes. Toutefois, pour les traitements complexes impliquant plusieurs modèles, il vaut mieux externaliser la logique dans des services (voir plus loin).
- **Managers et QuerySets personnalisés** : Utiliser des custom managers ou querysets pour factoriser des requêtes complexes ou fréquemment utilisées. Par exemple, un manager `Production.objects.en_cours()` qui filtre les productions actives. Cela rend le code plus lisible (on interroge via `Production.objects.en_cours()`) et évite de dupliquer du filtrage un peu partout.
- **Indexes et performances** : Bien analyser les besoins de requêtes pour ajouter des index sur les champs fréquemment filtrés. Des champs de recherche, de date ou clés étrangères souvent utilisées dans des filtres/tri bénéficieront d’un index pour accélérer les requêtes. Attention à ne pas sur-indexer inutilement : chaque index a un coût en écriture, donc ne les ajouter que s’ils apportent un gain en lecture avéré.
- **Éviter le piège du N+1** : En ORM, le problème N+1 survient lorsqu’on itère sur un queryset et charge à chaque tour une relation en déclenchant une requête séparée. Utilisez systématiquement `select_related` pour pré-charger les relations _one-to-one_ ou _foreign key_, et `prefetch_related` pour les relations _many-to-many_ ou _one-to-many_, lorsque vous accédez à ces relations dans du code itératif. Par exemple, `Lot.objects.select_related('campagne').all()` va charger en une requête chaque lot et sa campagne associée au lieu d’une requête par lot.
- **Migrations** : Conservez des migrations **propres et à jour**. Chaque modification de modèle doit s’accompagner d’une migration créée via `makemigrations` et versionnée. En revue de code, vérifiez que les migrations reflètent bien les changements voulus et rien de plus (par ex, éviter des migrations inutiles de type _rename_ accidentel). En production, appliquer les migrations dans un ordre contrôlé, tester sur un environnement de staging les migrations qui modifient beaucoup de données. Pensez à _squasher_ les migrations au bout d’un certain nombre si l’application vit longtemps, afin d’éviter un historique pléthorique (ex: squasher les migrations de l’app utilisateurs après X années). Toujours tester la migration (appliquée puis rollback si possible) avant de l’exécuter en prod.

Enfin, pour les _campagnes industrielles_, la conception de modèles doit permettre l’**historisation**. Par exemple, plutôt que d’écraser les valeurs d’indicateurs calculés, on peut stocker ces résultats dans un modèle _Journalier_ lié à la campagne et indexé par date, de sorte à garder une trace de chaque jour de production. Si un recalcul est nécessaire (suite à correction d’une donnée brute), on génèrera une nouvelle entrée de résultat (ou on mettra à jour l’entrée du jour en gardant les anciennes valeurs ailleurs pour audit). Les modèles doivent comporter des champs de **timestamp** ou version pour suivre l’évolution dans le temps.

### Sérializers (Django REST Framework)

Les **sérialiseurs DRF** transforment les modèles Django en données JSON (et inversement) pour exposer une API. Conseils de bonnes pratiques :

- **Utiliser des ModelSerializer** lorsque possible pour réduire le code boilerplate. Un `ModelSerializer` génère automatiquement des champs basés sur le modèle. On peut le customiser (champs en plus/moins, validation spécifique) via la classe Meta ou en redéfinissant des méthodes de validation.
- **Séparer les serializers de lecture et d’écriture** lorsque les besoins divergent. Par exemple, en lecture (GET), vous souhaitez peut-être renvoyer des champs calculés ou des relations détaillées (nids d’objets), tandis qu’en écriture (POST/PUT) vous attendez un format plus simple (des IDs de relation au lieu d’objets complets). Dans ce cas, définissez deux serializers distincts – par convention, nommés _XxxReadSerializer_ et _XxxWriteSerializer_ – et configurez vos vues DRF pour utiliser l’un ou l’autre selon l’action. Cette séparation évite d’avoir un seul serializer surchargé gérant tous les cas. C’est un pattern courant pour maintenir la **clarté** et la sécurité (les champs en lecture seule ne sont pas acceptés en écriture, par ex). Un moyen est de surcharger `get_serializer_class()` dans vos ViewSets pour renvoyer le serializer approprié en fonction de `self.action` (DRF ViewSet actions).
- **Valider les données métier dans le serializer** (ou le modèle). Le serializer DRF offre des méthodes `validate_<field>` et `validate` pour les validations _cross-field_. Profitez-en pour implémenter des règles d’intégrité métier (par ex: vérifier qu’une date de fin est postérieure à la date de début, etc.). Cela garantit que même si l’API est appelée en dehors de l’interface (client API externe), les règles sont appliquées. Pour des validations complexes multi-modèles, le serializer peut appeler des services métiers (voir section Services).
- **Pagination et filtrage** : Par défaut, **activez la pagination** des listes d’objets dans l’API pour éviter des réponses JSON énormes. DRF propose plusieurs classes de pagination (PageNumberPagination, LimitOffsetPagination, etc.) faciles à configurer. De même, implémentez un filtrage clair des résultats via des query params explicites (par ex `GET /api/lots?campagne_id=5`). Intégrez **django-filter** avec DRF pour un filtrage déclaratif sur certains champs autorisés. Il est recommandé de **documenter les paramètres de filtrage disponibles** pour chaque endpoint. En 2025, on encourage à rendre le filtrage **explicite et contrôlé** plutôt que d’exposer tous les champs sans discernement.
- **Performance** : Si un endpoint liste doit retourner beaucoup de données agrégées, envisagez d’optimiser la sérialisation (utilisation de `SerializerMethodField` calculés de manière performante, pré-chargement des relations comme mentionné plus haut). Dans certains cas extrêmes, il peut être plus efficace de recourir à des requêtes SQL brutes ou à des vues matérialisées en base pour alimenter l’API (selon les SLA de temps de réponse).
- **Sécurité des données** : Faites attention aux informations sensibles. Ne sérialisez pas par erreur des champs confidentiels (mot de passe, token, données personnelles) vers l’extérieur. DRF ne sérialise pas les champs déclarés comme `PasswordField` ou marqués _write_only_ en lecture, donc utilisez ces mécanismes pour protéger les données sensibles. Pensez également aux permissions au niveau des vues API (voir sections Authentification et Permissions plus loin).

### Vues Django et Routing (URLs)

Les **vues** sont le code qui reçoit une requête et renvoie une réponse. Dans un projet avec API REST et frontend séparé, on aura surtout des vues API (ViewSets DRF) et possiblement quelques vues classiques (par ex. pour le back-office Django admin, ou des pages d’aide). Recommandations :

- **Vues basées sur les classes (CBV)** : Django offre des _class-based views_ génériques (ListView, DetailView, CreateView…) et DRF fournit aussi des APIView et ViewSet classes. Privilégiez les CBV lorsque la factorisation ou la réutilisation le justifie. Par exemple, un ListView générique peut couvrir beaucoup de cas de listing d’objets avec très peu de code. De même, les **ViewSets de DRF** permettent de décrire en une classe l’ensemble des opérations CRUD sur un modèle, ce qui est concis et cohérent. En 2025, la tendance est d’utiliser les CBV pour les fonctionnalités complexes et structurées, et de recourir éventuellement aux vues fonctionnelles (FBV) pour de toutes petites actions très simples. Les CBV rendent le code plus modulaire et extensible grâce à l’héritage et aux mixins Django.
- **Routing explicite par app** : Chaque app Django devrait avoir son `urls.py` qui définit ses routes locales. Le `urls.py` principal (dans `config/urls.py`) inclura ces routes avec un préfixe. Par exemple, `path('production/', include('apps.production.urls'))`. Cela rend l’URL scheme clair et l’isolement des modules facile. En Symfony, on a des routes via annotations ou YAML par bundle; en Django tout est du code Python, ce qui apporte la flexibilité des expressions régulières ou converters pour les paramètres dans les URLs.
- **Nommer les routes** avec le paramètre `name=` dans `path()` afin de pouvoir y référer ailleurs (notamment dans les templates Django ou pour faire du reverse). Ex: `path('lot/<int:id>/edit/', edit_lot_view, name='lot_edit')`. Ainsi dans un template on peut faire `{% url 'lot_edit' lot.id %}` pour générer l’URL.
- **Vues légères** : Appliquez la philosophie "_thin views, fat models/services_". La vue (qu’elle soit fonction ou classe) devrait idéalement contenir peu de logique métier impérative. Elle orchestre l’appel aux bonnes méthodes (services, ORM) et renvoie la réponse HTTP appropriée. Ceci améliore la lisibilité et la testabilité (on peut tester la logique métier séparément de la vue).
- **Gestion des erreurs dans les vues** : Assurez-vous de gérer les cas d’erreurs ou d’objets non trouvés proprement dans les vues. Utilisez les exceptions Django (`Http404`, `PermissionDenied`) ou DRF (exceptions API) pour que les réponses HTTP soient adaptées (404, 403, 400...). Par exemple, dans une vue Django classique on attrapera `MyModel.DoesNotExist` pour lever `Http404`, comme illustré dans la documentation.
- **Middleware éventuels** : Si certaines préoccupations sont transverses (par ex, journaliser toutes les requêtes API entrantes, ou imposer un header particulier), envisagez d’écrire un middleware plutôt que de le coder dans chaque vue. Par exemple un middleware d’audit qui logge l’utilisateur et l’URL appelée peut contribuer à la traçabilité.

### Formulaires Django

Dans la mesure où le frontend est développé en React et utilise l’API REST, l’utilisation des formulaires HTML Django classiques sera sans doute limitée (peut-être pour l’interface admin ou quelques écrans internes). Néanmoins, Django dispose d’un puissant système de **forms** et **model forms** qui peut être utile pour des interfaces d’administration personnalisées ou des scripts.

- **Django Forms vs Symfony Forms** : À titre de comparaison, Symfony utilise un composant Form distinct (FormType classes) où l’on définit chaque champ et validation, puis le contrôleur construit le form et le passe à la vue Twig. Django simplifie grandement cela : il suffit de définir une classe qui hérite de `forms.Form` ou `forms.ModelForm` et Django génère les champs automatiquement pour un modèle donné. On peut ensuite exploiter ce formulaire dans une vue Django classique et le rendre dans un template. Par exemple, en Django :
    
    ```python
    # forms.py
    from django import forms
    from .models import Customer
    
    class CustomerForm(forms.ModelForm):
        class Meta:
            model = Customer
            fields = ['name', 'surnames', 'address']
    
    ```
    
    Ce form génère automatiquement des champs pour `name, surnames, address` basés sur le modèle Customer, sans qu’on ait à écrire de HTML. Dans la vue on pourra faire :
    
    ```python
    def edit_customer(request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerForm(request.POST or None, instance=customer)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('customer_detail', pk=pk)
        return render(request, 'customer_edit.html', {'form': form})
    
    ```
    
    Cette simplicité est un atout de Django. Si de tels formulaires sont utilisés (par exemple pour des écrans d’administration ou des outils internes non couverts par l’admin Django), tirez-en profit pour accélérer le développement. Le formulaire gère la validation et l’affichage des erreurs automatiquement dans le template.
    
- **Validations et nettoyage** : Utilisez les méthodes `clean()` ou `clean_fieldname()` des formulaires pour implémenter des validations côté serveur additionnelles. Par exemple, s’assurer qu’un champ numérique est positif, etc. Même si le frontend React a sa propre validation, il faut toujours valider côté serveur également.
    
- **Sécurité** : Les formulaires Django offrent une protection CSRF intégrée via le token `{% csrf_token %}` à inclure dans les formulaires HTML. Ne pas oublier de l’utiliser si vous créez des templates de formulaire, afin de se prémunir des attaques CSRF.
    
- **Limites** : Pour un projet full API, on pourrait se passer de formulaires Django pour la partie publique/React. Cependant, connaître leur existence permet d’éventuellement créer rapidement un outil d’administration additionnel si le besoin se présente, sans devoir tout recoder en JS (par ex, un simple formulaire d’import manuel de fichier via l’interface d’admin pourrait être fait avec un ModelForm + view).
    

### Commandes de Management (scripts & batchs)

Les **management commands** Django (commande `manage.py <nom>` que l’on peut créer) sont l’outil approprié pour les tâches batch, les imports/exports de fichiers, ou les traitements périodiques. Plutôt que d’écrire des scripts Python isolés, tirer parti de Django pour ces tâches apporte plusieurs avantages : accès direct aux modèles/ORM, configuration Django déjà chargée, et intégration dans les outils de l’app.

**Bonnes pratiques pour les commandes custom** :

- **Organisation** : Créer un package `management/commands` dans l’app concernée (par ex, dans `apps/production/management/commands/`). Chaque module Python dans ce dossier correspondra à une commande exécutable. Django détectera automatiquement ces commandes si l’app est dans `INSTALLED_APPS`. Exemple : un fichier `import_donnees.py` dans ce dossier permettra d’exécuter `python manage.py import_donnees`.
- **Utilisation typique** : Les commandes Django sont particulièrement utiles pour lancer des scripts _standalone_ ou des tâches périodiques via CRON ou un planificateur Windows. Dans notre contexte industriel, on peut imaginer une commande `import_logs_journaliers` qui va chercher des fichiers de log ou CSV déposés chaque jour et les ingérer.
- **Structure** : Une classe Command héritant de `BaseCommand` doit être définie, avec au minimum une méthode `handle()` qui contient la logique. On peut définir des arguments via `add_arguments()` pour rendre la commande paramétrable (par ex, `-date=YYYYMMDD` pour traiter un jour spécifique).
- **Sortie et logging** : Utiliser `self.stdout` et `self.stderr` pour toute sortie console plutôt que `print()`. Cela permettra de contrôler la verbosité via l’option `-verbosity` et de mieux tester la commande (on peut capturer stdout dans les tests). Structurer la sortie (messages de début/fin, compteurs d’éléments traités, etc.) pour faciliter la supervision. En cas d’erreur non-récupérable, lever `CommandError` pour que Django affiche un message d’erreur clair et retourne un code de sortie non nul.
- **Transactions** : Si la commande effectue des changements importants en base, envisager d’encapsuler dans une transaction (via `transaction.atomic()` ou le décorateur `@transaction.atomic`) afin d’assurer l’intégrité en cas d’échec en milieu de traitement. Attention toutefois à ne pas tout faire en une transaction si des milliers de lignes sont insérées (risque de lourdeur sur la base) – parfois il vaut mieux traiter par lots.
- **Planification** : Pour exécuter ces commandes régulièrement, deux approches : (1) utiliser une crontab/scheduler du système hôte qui appelle `docker exec <container> python manage.py ma_commande` à l’heure voulue, ou (2) intégrer un outil comme **Celery Beat** si on utilise Celery (voir ci-dessous). Dans un contexte on-premise, un CRON interne peut suffire si le scheduling n’est pas trop complexe. Assurez-vous dans tous les cas de surveiller l’exécution (logs).
- **Exemple** : une commande `import_mesures` pourrait ouvrir un fichier CSV de mesures industrielles et créer des objets Django en base pour chaque ligne. On veillera à gérer les exceptions fichier (fichier manquant, format invalide) proprement et à journaliser l’opération (nombre de lignes importées, etc.). Ce type de commande peut être déclenché chaque nuit après la réception des fichiers du jour.

Si certaines tâches sont très longues ou intensives, il peut être pertinent d’utiliser **Celery** (avec un broker type Redis) pour les exécuter de façon asynchrone, surtout si on doit les déclencher depuis une requête web. Par exemple, l’utilisateur upload un fichier sur le site : au lieu de l’importer synchrone et bloquer la requête, on peut lancer une tâche Celery en background et immédiatement répondre à l’utilisateur (puis notifier quand c’est fini). Celery s’intègre bien avec Django et est un standard en traitement asynchrone Python. Il nécessite toutefois de déployer un worker séparé.

### Services Métier (logique métier découpée)

Dans les projets Django de grande taille, il est souvent bénéfique d’introduire une couche de **services métier** pour structurer la logique applicative complexe. L’idée est de ne pas mettre toute la logique dans les vues ou les modèles, afin de **séparer les préoccupations**. Un _service_ est typiquement une fonction ou classe Python (pouvant être regroupée dans un module `services.py` par app) qui réalise une action métier complète en orchestrant éventuellement plusieurs modèles.

**Pourquoi une couche de services ?**

- **Lisibilité et réutilisation** : Une vue API DRF peut appeler un service métier (par ex `CalculBilanService.calculer_bilan(campagne)`), ce qui clarifie le rôle de la vue (elle gère la requête HTTP, pas le calcul lui-même). Le même service peut être réutilisé ailleurs (dans une commande management, un script, etc.) sans dupliquer la logique.
- **Testabilité** : On peut tester les services comme des unités de logique indépendantes, sans avoir à simuler une requête HTTP. Cela facilite l’écriture de tests unitaires sur les règles métier pures.
- **Transactions centralisées** : Dans un service, on peut encapsuler plusieurs opérations de BDD dans une transaction atomique pour assurer la cohérence globale. Par exemple, un service qui crée un objet principal et plusieurs objets associés pourra utiliser `transaction.atomic()` pour s’assurer que soit tout est créé, soit rien (en cas d’erreur).
- **Organisation du code** : En adoptant ce pattern, l’équipe sait que _« toute la logique de calcul de production se trouve dans services.production_service »_, _« la vue ne fait qu’appeler ce service »_. Cela donne un repère clair dans la base de code, ce qui améliore la maintenabilité et limite l’enchevêtrement de code dans les vues.

**Mise en place** : Concrètement, on crée par exemple un fichier `services.py` dans chaque app ou un package `services/` avec plusieurs modules par domaine. À l’intérieur, définir soit des classes statiques, soit simplement des fonctions. Par exemple :

```python
# apps/production/services.py
from django.db import transaction
from .models import Lot, Bilan

def cloturer_campagne(campagne):
    """Clôture une campagne: calculer le bilan final et marquer la campagne comme terminée."""
    with transaction.atomic():
        campagne.status = 'TERMINE'
        campagne.save()
        # Calcul du bilan en agrégeant les lots
        total_qty = Lot.objects.filter(campagne=campagne).aggregate_sum('quantite')
        # ... autres calculs
        bilan = Bilan.objects.create(campagne=campagne, quantite_totale=total_qty, ...)
        return bilan

```

Ensuite la vue qui gère l’endpoint `POST /api/campagnes/{id}/cloture` peut faire :

```python
@api_view(['POST'])
def cloture_campagne_view(request, pk):
    campagne = get_object_or_404(Campagne, pk=pk)
    if not request.user.has_perm('production.cloturer_campagne', campagne):
        return Response(status=403)
    bilan = services.cloturer_campagne(campagne)
    return Response(BilanSerializer(bilan).data)

```

Ici la vue est concise et compréhensible, toute la logique lourde est déléguée.

**Attention** : Certains puristes Django estiment qu’une couche de service est parfois superflue si les modèles sont bien conçus (on pourrait mettre `cloture()` en méthode du modèle Campagne par ex.). Ce débat existe, mais dès que la logique fait intervenir plusieurs modèles ou des appels externes (autre API, envoi d’email, etc.), une fonction de service dédiée est judicieuse. Le tout est d’éviter la **surgénéralisation** pour des opérations triviales – pas besoin d’une couche service pour un simple CRUD standard (sinon on ajoute de la complexité pour rien). Il faut l’introduire de manière pragmatique, quand la complexité le justifie. Dans un contexte industriel, il y aura vraisemblablement de nombreuses règles métier complexes, donc la couche service prendra tout son sens pour isoler ces règles.

En synthèse, adoptez une architecture logique MVT+Services : **Modèles** pour le stockage et la logique centrée sur un seul objet, **Vues** pour l’interface (HTTP/API) et autorisations, **Services** pour le métier multi-objets. Cette séparation suit le principe "_Separation of Concerns_" et améliore la modularité et l’évolutivité du projet.

## API REST avec Django REST Framework

Pour servir le frontend React et éventuellement d’autres consommateurs (applications mobiles, partenaires, etc.), une API REST bien conçue est essentielle. Voici les lignes directrices pour structurer l’API avec DRF :

- **ViewSets et routeurs** : Utilisez les **ViewSets** de DRF pour regrouper les opérations CRUD d’une ressource dans une même classe. Par exemple un `LotViewSet` avec les méthodes `list`, `retrieve`, `create`, etc. Puis exposez-le via un **DefaultRouter** ou **SimpleRouter** DRF dans `urls.py` (par ex: `router.register('lots', LotViewSet)`). Cela génère automatiquement des routes RESTful (`/api/lots/`, `/api/lots/123/`, etc.) et est cohérent avec les standards REST. Vous pouvez ajouter des actions personnalisées via les décorateurs `@action` de DRF si nécessaire (ex: `/api/lots/123/valider/` pour une action métier).
- **Versionnage de l’API** : Pensez à versionner vos URLs d’API dès le début, par exemple préfixer par `/api/v1/...`. Ainsi, si l’API évolue de façon rétro-incompatible, vous pourrez exposer `/api/v2/` en parallèle sans casser les anciens consommateurs. DRF propose aussi des mécanismes de versioning interne plus sophistiqués, mais un simple namespace d’URL est souvent suffisant.
- **Documentation de l’API** : Prévoir une documentation de l’API pour les développeurs front ou clients tiers. On peut utiliser **drf-yasg** ou **drf-spectacular** pour générer un **Swagger/OpenAPI** interactif. Cela permet d’exposer automatiquement les schémas des endpoints, les modèles de données attendus, etc. Cette doc peut être auto-hébergée (une route `/api/docs/`). A minima, utiliser la fonctionnalité de **Schema** DRF pour décrire les champs, et fournir un fichier OpenAPI à jour.
- **Auth de l’API** : Pour un frontend React servant la même application, on peut utiliser l’authentification par session (via cookie) combinée au mécanisme CSRF de Django si le domaine est le même. Toutefois, dans un contexte client SPA, on privilégie souvent un système **token JWT** plus découplé. L’implémentation standard en 2025 est le package **djangorestframework-simplejwt** qui offre des endpoints de login générant un JWT (et refresh token). Ces JWT peuvent encapsuler les informations de l’utilisateur (id, roles) et sont envoyés dans les headers Authorization. Nous détaillons plus loin la mise en place, mais au niveau API DRF, cela se traduit par l’ajout de `JWTAuthentication` dans les classes de permission DRF, et possiblement la mise en place d’un _permission class_ custom pour vérifier les rôles/scopes dans le payload du JWT.
- **Permissions DRF** : DRF fournit des classes de permission réutilisables (IsAuthenticated, IsAdminUser, DjangoModelPermissions, etc.). Choisissez la stratégie adaptée par vue. Par exemple, les endpoints lecture seule peuvent être ouverts à de simples utilisateurs authentifiés, tandis que les endpoints de modification nécessitent un rôle plus élevé (on peut créer une classe custom comme `IsManagerUser` qui vérifie un attribut du User ou son groupe). Les permissions DRF fonctionnent par vue, mais pour du filtrage par objet (_object-level permission_), il faut surcharger la méthode `get_queryset` pour restreindre aux objets autorisés. Ex: dans `LotViewSet.get_queryset`, retourner `Lot.objects.filter(site__in=request.user.sites_autorises)` pour n’exposer que les lots du site auquel l’utilisateur a accès. Cela doit idéalement être couplé avec les règles de base de données ou au moins les vérifications dans les services côté backend pour être sûr qu’on ne serve pas de données non autorisées même en cas de bug de l’API.
- **Throttling & Rate limiting** : Si l’API est exposée à des clients variés (ex: partenaires) ou sur internet, envisagez d’activer les mécanismes de throttle de DRF pour prévenir les abus (ex: X requêtes par minute par IP ou par utilisateur). Pour un usage interne (intranet industriel), c’est moins critique, mais en cas d’intégration avec d’autres systèmes ça peut éviter de saturer le backend.
- **Retour d’erreurs** : DRF fournit un format de réponse uniforme pour les erreurs (codes HTTP, réponse JSON avec `detail` ou les messages de validation). Assurez-vous de bien utiliser les exceptions DRF (ValidationError, NotAuthenticated, PermissionDenied, etc.) afin que les consommateurs de l’API reçoivent des codes HTTP cohérents (400, 401, 403, 404, 500). Personnalisez les messages d’erreur si nécessaire, et loggez côté serveur les détails pour faciliter le debugging.
- **Tests d’API** : Rédigez des tests automatisés pour les endpoints critiques (par ex. tester qu’un utilisateur avec tel rôle peut/tout pas accéder à tel endpoint, que les validations renvoient bien une 400 avec tel message si input invalide, etc.). On peut utiliser la **APIClient** de DRF dans les tests ou des outils externes (comme _pytest-django_ avec des appels API).

En suivant ces pratiques, on obtient une API REST cohérente, maintenable et sécurisée, qui pourra évoluer avec les besoins (nouvelles versions) tout en assurant un service fiable au frontend et aux éventuels autres clients.

## Traitements de Données, Fichiers et Journalisation

Les projets industriels manipulent souvent des **fichiers de données** (mesures CSV, rapports Excel, logs machines) qu’il faut ingérer, transformer et stocker. De plus, une bonne gestion des **logs applicatifs** et des **erreurs** est nécessaire pour le support en production.

### Collecte et transformation des fichiers (ETL)

Pour les tâches de type ETL (Extract-Transform-Load) sur des fichiers, voici les bonnes pratiques :

- **Emplacement et accès** : Si l’application reçoit des fichiers (par ex via un upload ou déposés dans un répertoire surveillé), définissez un endroit centralisé pour les stocker temporairement. Vous pouvez configurer le **FileStorage** de Django pour pointer vers un répertoire sur le serveur ou un volume monté (dans Docker, on peut monter un volume pour stocker ces fichiers entrants). Une fois traités, déplacez ou archivez les fichiers pour éviter de retraiter les mêmes.
- **Parsing efficace** : Pour lire des gros CSV, évitez de tout charger en mémoire brute. Utilisez des itérateurs ou des bibliothèques optimisées. Le module Python natif `csv` permet de streamer ligne par ligne. Si les fichiers sont très volumineux et que les performances sont un enjeu, la bibliothèque **pandas** peut être utilisée pour des transformations complexes, mais attention à la conso mémoire (pandas charge tout en RAM). Pour des fichiers Excel, utiliser **openpyxl** ou **xlrd**. Assurez-vous de bien gérer les encodages (UTF-8, etc.) et les séparateurs décimaux/csv (selon si c’est un CSV point-virgule par ex).
- **Validation des données** : Intégrez des contrôles lors de l’import. Par exemple, vérifier que les colonnes attendues sont présentes, que les valeurs numériques sont dans des plages plausibles, etc. En cas d’anomalie, loggez un message clair avec l’emplacement (ligne/colonne) pour faciliter le diagnostic. Vous pouvez compter les lignes réussies et celles en erreur pour un bilan d’import.
- **Transactionnalité** : Si vous importez des données en base via Django, envisagez de _batcher_ les insertions. Par exemple accumuler 500 objets puis faire un `MyModel.objects.bulk_create(liste)` au lieu d’insérer ligne par ligne (bien plus efficace). Toutefois, attention avec bulk_create, il ne déclenche pas les signaux Django ni l’enregistrement historique (si vous utilisez django-simple-history) par défaut. Alternative : utiliser une transaction englobant l’ensemble, de sorte à rollback complet en cas d’échec. Tout dépend du contexte : pour un import quotidien, peut-être vaut-il mieux insérer ce qui est valide et ignorer les lignes invalides plutôt que tout rejeter.
- **Outil d’import** : Si l’application est amenée à faire beaucoup d’import/export, il existe des libs Django dédiées (par ex **django-import-export** pour importer des fichiers via l’admin, ou **petl** pour ETL). Dans un contexte sur mesure, écrire vos commandes management (comme discuté) est souvent suffisant et plus flexible.

### Journaux et logs

La **journalisation** doit être prise en compte dès le développement, afin de faciliter la maintenance en production :

- **Configuration du logging** : Utilisez le module `logging` de Python configuré via Django settings. En mode debug, console suffira, mais en production, préférez un format structuré (JSON par ex) et un envoi des logs vers un fichier ou une sortie standard (si Docker, la stdout du container sera collectée par la plateforme d’hébergement). On peut définir plusieurs loggers : par ex un logger `django` pour les messages framework, un logger `myapp` pour vos messages métier. Ajustez les niveaux (INFO, WARNING, ERROR) pour n’avoir ni trop peu ni trop de verbosité.
- **Logs des actions utilisateur** : Dans une optique de traçabilité, loggez les actions sensibles. Par exemple, lorsqu’un utilisateur lance le recalcul d’un bilan, écrivez un log INFO ou AUDIT du style _"[user X] initiated recalculation for campaign Y"_. Si possible, incluez un identifiant de requête ou d’opération pour lier les logs entre eux. Ces logs peuvent être centralisés plus tard dans un SIEM ou un outil de suivi.
- **Rotation/Retenue** : Mettez en place une rotation des logs si vous écrivez dans des fichiers, pour éviter qu’ils ne grossissent indéfiniment. Django peut le faire via TimedRotatingFileHandler, ou utilisez la rotation du système/d’outils externes.
- **Analyses** : Considérez l’utilisation de la stack **ELK (Elasticsearch, Logstash, Kibana)** ou équivalent pour collecter et analyser les logs applicatifs, surtout si vous avez plusieurs instances ou de gros volumes de logs. Étant on-premise, vous pouvez déployer un Graylog ou un ELK interne. Cela vous permettra de rechercher des erreurs survenues, de faire des tableaux de bord (ex: nombre d’imports réussis vs échoués par jour, etc.).
- **Logs des erreurs** : Configurez Django pour envoyer un email aux admins (`ADMINS` dans settings) en cas d’erreur 500 non gérée en prod. Mieux, intégrez un outil comme **Sentry** (peut être self-hébergé ou on-prem) pour capturer et agréger les exceptions non gérées. Sentry s’intègre facilement et enverra une stacktrace détaillée quand un bug survient, ce qui est très précieux.

### Gestion des erreurs et tolérance aux pannes

- **Erreurs applicatives** : Adoptez le principe _fail fast_ pendant le dev (remonter vite les exceptions), mais en production, attrapez les exceptions prévues et gérez-les proprement pour éviter des crashs brutaux. Par exemple, si un import de fichier échoue pour une ligne, loggez l’erreur et continuez sur les autres lignes (sauf si l’erreur remet en cause tout le fichier).
- **Résilience** : Si l’application dépend de ressources externes (webservices, API tierces, etc.), implémentez des mécanismes de retry ou de retour en arrière en cas d’échec, surtout pour les tâches batch. Par exemple, si l’ETL doit appeler une API pour chaque enregistrement, prévoir que l’API puisse être indisponible et soit retenter plus tard sans bloquer toute la chaîne.
- **Monitoring technique** : (voir section Maintenabilité plus loin pour plus de détails) En bref, surveillez vos tâches: un outil de monitoring ou au minimum des métriques (durée des imports, taux d’erreurs, etc.) vous aideront à anticiper les problèmes de performance ou de données corrompues.

En appliquant ces pratiques, le traitement de données sera plus fiable et transparent. La collecte de fichiers industriels souvent bruts gagnera en robustesse, et l’équipe pourra facilement auditer ce qui a été fait via les logs et historiques.

## Intégration Continue et Déploiement (CI/CD)

Mettre en place une pipeline **CI/CD** est indispensable pour un projet professionnel. Avec GitLab comme forge, on utilisera **GitLab CI** pour automatiser les tests, la construction des images Docker et le déploiement. Voici les bonnes pratiques :

- **Pipeline découpé en étapes** : Séparer les jobs en stages logiques : `tests` -> `build` -> `deploy`. Par exemple, un stage _tests_ qui exécute les tests unitaires et de lint, un stage _build_ qui construit et push l’image Docker, puis un stage _deploy_ (optionnel) qui déploie sur l’environnement de staging/production. L’automatisation garantit que l’application est testée et déployée de manière cohérente à chaque changement.
- **Automatisation des tests** : Un job _test_ lancera `pytest` ou `./manage.py test` et pourra calculer la **couverture de code**. GitLab CI peut récupérer un rapport de couverture (Cobertura, etc.) et afficher une statistique. Vous pouvez même fixer un seuil de couverture minimum à atteindre, pour obliger l’équipe à écrire des tests pour chaque fonctionnalité.
- **Linting et analyse statique** : Intégrez dans la CI un job pour _flake8/pylint_ et éventuellement _mypy_ (vérification de type statique) afin d’attraper en amont les problèmes de style ou de typage.
- **Construction Docker** : Dans le stage _build_, utilisez un **Dockerfile optimisé** (voir plus loin). Le job fera par ex `docker build -t registry.intra/gardel/app:$CI_COMMIT_SHA .` puis `docker push ...`. GitLab runner doit avoir accès au daemon Docker (soit runner docker privileged, soit Kaniko etc. sur K8s). Utilisez le **GitLab Container Registry** interne pour stocker les images versionnées (taguées par commit ou version). Cela permet de déployer précisément une image donnée en prod.
- **Docker multi-stage** : Le Dockerfile devrait utiliser une build multi-stage afin de produire une image finale légère. Par ex, une première stage qui construit les dépendances (peut-être sur une image Python slim puis pip install), puis copie le code dans une seconde stage (basée sur une image Python slim ou Alpine) pour exécuter. Ceci permet de réduire la taille de l’image ~de 70% et d’éliminer les dépendances de build inutiles en production.
- **Variables et secrets CI** : Configurez les secrets (credentials DB, SECRET_KEY, etc.) dans GitLab CI/CD (Variables protégées) pour qu’ils soient injectés au déploiement sans être exposés dans le code. Par exemple, la commande de déploiement peut utiliser `docker run -e SECRET_KEY=$SECRET_KEY ...`.
- **Déploiement continu** : Selon votre infra, le stage de déploiement peut simplement consister à copier l’image sur un serveur et la lancer via Docker Compose, ou déclencher un déploiement Kubernetes. Dans un contexte on-prem, on peut imaginer un runner GitLab sur le réseau interne capable de se connecter aux serveurs cibles. Par exemple, utiliser **SSH** pour exécuter `docker pull && docker-compose up -d` sur le serveur de prod. Veillez à ce que seuls les commits sur la branche `main` ou les tags de version déclenchent le déploiement en production, pour éviter tout déploiement intempestif.
- **Environnements multiples** : Mettez en place un environnement de **recette/staging** identique à la prod où déployer d’abord pour valider. La CI peut déployer sur une instance de test à chaque merge (ou via des _Review Apps_), permettant à l’équipe métier de valider les changements avant la mise en prod.
- **Suivi et alertes** : Intégrez la CI/CD à votre flux de travail. Par exemple, que GitLab envoie des notifications en cas d’échec de pipeline. Examinez les rapports de test et de couverture à chaque merge request pour maintenir la qualité.

Un fichier `.gitlab-ci.yml` minimal pourrait ressembler à :

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: "$CI_REGISTRY_IMAGE/app"

test:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest --junitxml=report.xml --cov=.
  artifacts:
    reports:
      junit: report.xml
    coverage_report:
      coverage_format: cobertura
      path: coverage.xml

build:
  stage: build
  image: docker:24.0.2
  services:
    - docker:24.0.2-dind
  variables:
    DOCKER_DRIVER: overlay2
  script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
    - docker build -t "$DOCKER_IMAGE:$CI_COMMIT_SHORT_SHA" .
    - docker push "$DOCKER_IMAGE:$CI_COMMIT_SHORT_SHA"
    - docker tag "$DOCKER_IMAGE:$CI_COMMIT_SHORT_SHA" "$DOCKER_IMAGE:latest"
    - docker push "$DOCKER_IMAGE:latest"

deploy_prod:
  stage: deploy
  environment: production
  only:
    - main
  script:
    - ssh user@server.prod "docker pull $DOCKER_IMAGE:latest && docker-compose -f /path/docker-compose.yml up -d"

```

_(Cet exemple est simplifié : en pratique on sécurisera la connexion SSH par clé, etc.)_

Grâce à la CI/CD, on obtient un processus de livraison **fiable et reproductible**. Chaque modification passe par les tests automatiques et la revue de code, puis est déployée via Docker. On réduit drastiquement les erreurs humaines et on peut livrer des nouvelles versions plus fréquemment et en toute confiance.

## Sécurité, Authentification et Traçabilité

La sécurité de l’application et des données est un aspect critique, surtout en environnement industriel sensible. Django offre un socle sûr, mais il convient de respecter les bonnes pratiques suivantes :

### Sécurité Applicative Générale

- **Mises à jour** : Maintenez Django et les packages à jour aux dernières versions stables, pour bénéficier des correctifs de sécurité. Surveillez les annonces de sécurité du DSF et planifiez des montées de version régulières (Django sort des LTS, etc.).
- **Paramètres Django** : Tirez parti des protections intégrées de Django : CSRF Middleware activé (par défaut) pour toutes les vues non-API, protection XSS via l’échappement automatique dans les templates, protection anti-clickjacking (envoyer le header X-Frame-Options via `X_FRAME_OPTIONS` = DENY), etc. Vérifiez que ces protections sont bien en place en production (pas désactivées par mégarde).
- **En-têtes HTTP de sécurité** : Configurez le serveur web frontal (Nginx, etc.) ou Django pour ajouter les en-têtes HTTP Security essentiels : `Content-Security-Policy` (pour limiter les sources de scripts, particulièrement si React est servi du même domaine), `Strict-Transport-Security` (HSTS pour imposer HTTPS), `X-Content-Type-Options: nosniff`, etc.
- **Conteneurs** : Si Docker est utilisé, minimisez la surface d’attaque de l’image : privilégiez les images _slim_ ou _alpine_, n’incluez pas d’outils inutiles. Appliquez les principes de moindre privilège : l’application dans le container ne devrait pas tourner en root (utiliser un USER non privilégié dans le Dockerfile). De plus, utilisez des scans d’images (Trivy, etc.) en CI pour détecter des vulnérabilités dans l’image déployée.
- **Accès réseau** : En cloud privé, s’assurer que la base de données n’est pas exposée publiquement (firewall interne). Utiliser des connexions chiffrées (TLS) pour les communications internes si nécessaire, notamment si des données sensibles circulent.
- **Audit du code** : Faire des revues de code focalisées sur la sécurité pour les parties critiques. Envisager des tests d’intrusion / pentest une fois l’application en place pour valider la robustesse (injection SQL – bien que Django ORM y soit peu vulnérable si bien utilisé, XSS, IDOR – contrôle d’accès aux objets, etc.).

### Authentification (LDAP, JWT, Sessions)

**Authentification LDAP (Annuaire d’Entreprise)** : Dans un contexte industriel, l’entreprise peut avoir un annuaire LDAP ou Active Directory centralisé pour gérer les utilisateurs. Intégrer Django avec LDAP permet aux utilisateurs de se connecter avec leurs identifiants habituels et d’appliquer des politiques de sécurité uniformes.

- Utilisez la bibliothèque **django-auth-ldap** (maintenue officiellement) pour brancher Django sur le serveur LDAP. Ce backend d’auth remplace ou complète le backend classique. Il suffit de le configurer dans les settings (URL du serveur, DN de base, mapping des attributs vers User Django, etc.). Une fois en place, un utilisateur LDAP pourra s’authentifier sur le site Django. On peut prévoir de **synchroniser** certains attributs LDAP dans le modèle User Django (nom, email, etc.) à la première connexion.
- Vous pouvez également associer les **groupes LDAP** avec des groupes Django pour les permissions (ex: un groupe LDAP "Gardel_Admin" pourrait être mappé sur un groupe Django "Administrateurs" ayant certains droits). Django-auth-ldap permet de faire ce mapping automatiquement via des règles (ex: tous les membres de telle OU LDAP -> tel Group Django).
- Prévoir un mécanisme de **fallback** pour l’admin principal : souvent on garde un superuser local Django au cas où le LDAP est indisponible, pour pouvoir se connecter quand même (en créant un user admin en base avec mot de passe).
- Niveau sécurité, assurez-vous que la connexion LDAP se fait via LDAPS (LDAP sur SSL) ou StartTLS pour chiffrer les identifiants sur le réseau.

**Authentification par sessions** : C’est le mécanisme par défaut de Django (identification via cookie de session). Si l’application est utilisée majoritairement via l’API et un client JS, on utilisera plutôt JWT, mais il peut y avoir des cas (par ex l’interface d’admin Django, ou un module d’UI interne) où la session traditionnelle est utilisée.

- Activez la durée d’expiration des sessions selon la politique de l’entreprise (paramètre `SESSION_COOKIE_AGE`). Eventuellement utilisez `SESSION_EXPIRE_AT_BROWSER_CLOSE` si requis (pour forcer reconnexion après fermeture navigateur).
- Le cookie de session doit être `Secure` (seulement transmis en HTTPS) et `HttpOnly` pour éviter qu’un JS ne puisse y accéder.
- Django prend en charge la rotation de session en cas de changement de mot de passe ou de login sur une autre compte (via SESSION_SECURITY, etc.), utilisez ces features si pertinent.

**Authentification JWT (JSON Web Token)** : Recommandée pour l’API consommée par le frontend React, surtout si le domaine du frontend est distinct ou qu’une appli mobile doit consommer l’API.

- Utilisez **djangorestframework-simplejwt** ou **django-rest-knox** (des solutions courantes). SimpleJWT fournit des endpoints `/api/token/` et `/api/token/refresh/` par défaut. Lorsqu’un utilisateur fournit ses identifiants (qui peuvent être vérifiés via LDAP backend couplé), on renvoie un access token JWT signé contenant son identité et un refresh token.
- Le JWT est ensuite envoyé par le client dans le header `Authorization: Bearer <token>` à chaque requête. Côté DRF, il suffit d’ajouter `REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = ("rest_framework_simplejwt.authentication.JWTAuthentication", ...)`.
- Pensez à la durée de vie courte pour le access token (par ex 5 minutes) et plus longue pour le refresh (quelques jours) pour limiter l’impact si vol de token. Implémentez le refresh rotation (fourni par la lib).
- **Scopes JWT** : On peut inclure dans le JWT des informations de rôle ou de permissions (via les _claims_). Par exemple, ajouter un champ `"roles": ["lecteur", "editeur"]` dans le payload. Le frontend peut l’utiliser pour conditionner l’affichage, mais attention, tout ce qui est autorisation serveur ne doit pas se fier uniquement à ce claim (il peut être falsifié côté client si la clé privée était compromise, etc.). Mieux vaut recalculer les permissions côté serveur pour chaque requête, en utilisant le JWT seulement pour l’authentification de base.
- **Révocation** : JWT étant stateless, la révocation d’un token avant expiration n’est pas triviale. SimpleJWT propose un blacklist optionnel (stocker les tokens invalidés). Si le risque est faible, on peut s’en passer (les tokens expirent vite). Sinon, activez ce mécanisme (stocke en base les identifiants de token révoqués).

### Autorisation et Gestion des Droits par Profil

Au-delà de l’authentification, il faut gérer les **permissions** : qui a le droit de faire quoi. Django propose un système de permissions intégré (sur les modèles, via `User`, `Group` et `Permission`) qui peut servir de base.

**Rôles et Groupes** : La recommandation est de **ne jamais assigner individuellement des permissions aux utilisateurs**, mais de passer par des groupes (rôles). Par exemple, définir des groupes _Lecteur_, _Éditeur_, _Validateur_, _Admin_, etc. Chaque groupe se voit attribuer un ensemble de permissions (par ex le groupe _Lecteur_ a les perms de voir les objets, _Éditeur_ peut en plus créer/éditer, _Validateur_ peut valider/clos, etc.). On assigne ensuite les utilisateurs aux groupes appropriés selon leur profil réel. Cela facilite grandement la maintenance : pour changer un droit, on le modifie au niveau groupe, pas pour chaque personne.

**Permissions par modèle vs personnalisées** : Django crée par défaut des perms add/change/delete sur chaque modèle. On peut ajouter des permissions spécifiques via `Meta.permissions` dans le modèle. Par ex, `permissions = [("valider_bilan", "Peut valider un bilan de production")]`. Ces permissions seront en base et assignables aux groupes. Dans le code, on utilisera `user.has_perm('app_label.valider_bilan')` pour vérifier.

**Implémentation dans l’UI** :

- Côté Django (si on a des templates admin), on peut utiliser les decorateurs @permission_required ou vérifier request.user.has_perm dans la vue.
- Côté DRF, on peut créer une classe de permission custom. Par ex, `class HasBilanValidationPerm(permissions.BasePermission)` qui dans `has_permission` fait `return request.user.has_perm('app.valider_bilan')`. Puis l’attacher aux vues correspondantes (permission_classes = [HasBilanValidationPerm]).
- Côté React, prévoir que l’API renvoie un 403 si l’action n’est pas permise, et gérer cela (message "Access interdit"). On pourrait aussi exposer dans un endpoint le profil/les perms de l’utilisateur pour que le frontend adapte l’UX (griser des boutons non autorisés).

**Portée des permissions (scopes métiers)** : Dans un contexte industriel, les droits peuvent dépendre du **périmètre** (par ex, un responsable de site A ne voit que les données du site A). Pour cela, combiner le système de permissions avec du filtrage par objets :

- Soit en implémentant des **object permissions** avec un package comme **django-guardian** qui permet d’assigner des perms par objet (mais ça peut devenir lourd si beaucoup d’objets).
- Soit plus simplement via la logique applicative : inclure dans les modèles les champs nécessaires (ex: chaque Lot a un champ `site`) et restreindre les QuerySets en fonction du site de l’utilisateur (ex: user profil contient un champ site rattaché).
- Vous pouvez également coder une couche de _Scope_ manuellement. Par ex, avoir une table de correspondance Utilisateur -> Sites accessibles, et toujours filtrer selon ça.
- L’important est de centraliser ce genre de règle pour ne pas l’oublier. Une façon est d’utiliser un **Mixin** sur les ViewSets qui filtre le queryset en fonction d’un attribut du user (par ex, son site ou ses groupes).
- Dans les campagnes industrielles, peut-être que certaines règles sont temporaires ou journalières (ex: tel jour seul un superviseur peut modifier certaines données). Ce genre de règle peut être géré via des flags en base (un modèle de calendrier des droits, etc.) ou plus simplement dans le code en vérifiant la date courante.

**Traçabilité des actions utilisateur** : Liée aux permissions, la traçabilité vise à enregistrer _qui a fait quelle action quand_. Pour cela:

- Activez le **AdminLog** Django si vous utilisez l’admin – Django loggue automatiquement les ajouts/modifs/suppressions faites via le site admin.
- Pour l’application custom, envisagez d’utiliser une app comme **django-simple-history** qui garde l’historique de chaque modification sur les modèles importants. Ce plugin stocke l’état d’un objet à chaque create/update/delete, et peut en plus enregistrer quel utilisateur a effectué le changement (via un middleware ou en passant explicitement l’utilisateur). Ainsi, on peut auditer les changements de valeurs, ce qui est souvent vital en contexte industriel (traçabilité des corrections).
- Vous pouvez aussi implémenter une journalisation manuelle pour certaines actions critiques. Ex: lorsqu’un bilan est validé, créer un enregistrement dans une table `AuditAction` avec user, timestamp, type d’action ("VALIDATION_BILAN"), id de l’objet concerné. Cette table peut servir à générer des rapports d’audit.
- La traçabilité passe aussi par les logs évoqués précédemment (loguer les actions importantes). Avoir à la fois un log technique et un stockage en base éventuellement plus pérenne (si on a besoin de requêter qui a fait quoi plus facilement que de parser des logs).

En somme, utilisez le système de permissions Django couplé à des groupes pour gérer les rôles (RBAC) et n’hésitez pas à développer des contrôles additionnels pour les spécificités métier. Ainsi on garantit que chaque utilisateur n’a accès qu’aux fonctionnalités et données conformes à son rôle, et que chaque action peut être attribuée à quelqu’un en cas de besoin.

## Maintenabilité, Évolutivité, Documentation et Supervision

Concevoir l’application avec la **maintenabilité** et l’**évolution** à l’esprit permet d’assurer sa pérennité sur le long terme, d’autant qu’un projet industriel peut vivre de nombreuses années et voir ses exigences changer.

### Maintenabilité du Code

- **Qualité du code** : Comme déjà mentionné, faites respecter les standards de code. Des revues de code systématiques aident à garder une base cohérente. Utilisez des outils d’analyse statique (flake8, SonarQube si disponible) pour détecter du code mort, des complexités cyclomatiques élevées, etc.
- **Refactorisation continue** : Ne pas hésiter à refactorer des portions de code lorsque des motifs de duplication apparaissent ou que la complexité augmente trop. Par exemple, extraire une fonction utilitaire commune plutôt que copier-coller du code entre deux vues.
- **Convention de nommage et architecture** : Documentez et faites respecter les conventions (nomenclature des modèles, des champs, structure des dossiers). Par ex, tous les fichiers serializers s’appellent `serializers.py` pour qu’on les trouve facilement, nom des apps en minuscules singulier, etc.
- **Isolation des dépendances** : Si certaines parties du code sont susceptibles d’être réutilisées ailleurs ou d’évoluer séparément, isolez-les. Par ex, une logique de calcul générique pourrait aller dans un module séparé, éventuellement publié en package interne pip si besoin. Cela favorise la réutilisation et l’indépendance.

### Évolutivité et Performance

- **Scalabilité horizontale** : Grâce à Docker, l’application peut théoriquement tourner sur plusieurs instances derrière un load balancer. Assurez-vous qu’elle est **stateless** autant que possible : pas de fichier écrit localement (utilisez un stockage partagé ou base pour stocker les uploads, ou un volume monté commun), sessions stockées en base ou cache partagé si vous scalez plusieurs containers, tâches planifiées uniques (ou avoir un mécanisme pour éviter doublons si plusieurs instances, ex: un seul worker Celery distinct). En 2025, il est courant de déployer Django sur Kubernetes pour profiter du scaling et de la résilience.
- **Cache** : Identifiez les éléments qui pourraient bénéficier de cache. Django offre un framework de cache pouvant utiliser Memcached ou Redis. On peut cacher au niveau page (peu utile pour une API JSON), au niveau vue (decorateur `@cache_page` pour des GET très coûteux), ou au niveau fragment de template. Pour l’API, on peut implémenter un cache des réponses GET si les données changent peu fréquemment (attention à l’invalidation). Un cache peut énormément soulager la base de données sur des endpoints lourds. De plus, l’usage de Redis pour stocker du cache partagé est courant en déploiement dockerisé.
- **Optimisation base de données** : Monitorer les requêtes (via l’outil Django debug toolbar en dev, ou via les logs en prod) pour ajouter des index ou optimiser des requêtes lentes. Parfois, passer par du SQL brut pour les gros agrégats peut être valable. Par exemple, pour un bilan global, un `SELECT SUM(x) FROM ... GROUP BY ...` en SQL pourra être plus efficace que de charger toutes les instances en Python.
- **Tâches asynchrones** : Pour l’évolutivité, décorréler les tâches lourdes du cycle web synchrone. On a mentionné Celery. Celery permet aussi de planifier périodiquement (via beat) et de paralléliser des traitements s’il y a beaucoup à faire (plusieurs workers). Cela peut être utile si, par exemple, chaque nuit il faut recalculer tous les indicateurs de toutes les campagnes – on pourrait paralléliser par site ou par type d’indicateur.
- **Tests de charge** : Avant la mise en production (et après chaque changement majeur), effectuez des tests de performance / charge pour voir comment l’application tient. Simulez des appels API massifs, l’import de fichiers volumineux, etc. Cela permettra de détecter des goulots d’étranglement (peut-être la mémoire, ou telle requête SQL trop lente) et de dimensionner l’infra en conséquence (CPU, RAM, tuning Postgres).

### Documentation et Connaissance

- **Documentation utilisateur** : En plus de la doc technique, prévoir une doc fonctionnelle ou au moins une aide pour les utilisateurs finaux (par ex, un wiki interne ou un manuel expliquant le flux de campagne, comment interpréter tel écran de bilan, etc.). Ce n’est pas directement lié à Django, mais un projet industriel s’accompagne souvent d’une passation vers les équipes métiers utilisatrices.
- **Documentation technique** : Rédiger un document d’architecture technique décrivant les choix faits (frameworks, structure du projet, schéma base de données simplifié, intégrations externes, etc.). Ceci aide toute personne arrivant sur le projet à en avoir une vision globale sans lire tout le code. Inclure également comment lancer l’app en local, comment déployer, etc. (souvent dans le README).
- **Commentaires dans le code** : Encouragez l’ajout de commentaires lorsqu’une logique n’est pas évidente ou repose sur une règle métier pointue. Il vaut mieux écrire _"// Ce coefficient est calculé selon la formule X fournie par l’ingénieur procédés"_ que de laisser un calcul magique inexpliqué.

### Supervision et Monitoring

Pour assurer la disponibilité et détecter les anomalies en production :

- **Monitoring de l’application** : Mettez en place un système de supervision de l’app Django elle-même. Par exemple, un **heartbeat** endpoint (`/health/`) que l’outil de monitoring peut appeler pour vérifier que l’app répond (et éventuellement vérifier la connexion DB). Sur Kubernetes, utilisez des probes readiness/liveness. Sur VMs, un outil comme Zabbix, Centreon ou Prometheus peut faire un check HTTP.
- **APM (Application Performance Monitoring)** : Considérez l’usage d’un APM pour avoir des métriques de performance détaillées (temps de réponse par endpoint, requêtes SQL lentes, taux d’erreurs…). Des solutions comme **New Relic, Dynatrace** existent (coûteuses), mais on peut opter pour du open-source avec **Elastic APM** ou **OpenTelemetry**. OpenTelemetry est un standard émergent en 2025 pour instrumenter le code et envoyer traces/metrics vers, par exemple, un stack ELK ou Grafana. Cela vous aidera à identifier les bottlenecks et surveiller l’expérience utilisateur.
- **Alerting** : Configurez des alertes sur les métriques importantes. Exemples : alerte si le taux d’erreur 5xx dépasse X%, si le temps de réponse moyen dépasse Y, si l’utilisation CPU/RAM du container est > Z, ou si une tâche planifiée n’a pas tourné à l’heure prévue. Des outils comme Prometheus + Alertmanager ou les alertes Cloud interne peuvent être utilisés.
- **Logs centralisés et analytiques** : Comme dit, agrégerez les logs et utilisez Kibana ou autre pour rechercher en cas de problème. Avoir des tableaux de bord (ex: nombre de campagnes clôturées par semaine, nombre d’erreurs d’import, etc.) peut fournir de la proactivité.

En investissant dans ces aspects, on s’assure que le projet sera **soutenable sur la durée**. La combinaison d’un code de qualité, bien testé, et d’un monitoring efficace permet de dormir sur ses deux oreilles ou du moins de réagir vite aux incidents inévitables.

## Spécificités des Campagnes Industrielles : Règles Journalières, Historisation, Recalculs, Bilans

Les campagnes industrielles, comme évoqué précédemment, apportent leur lot de contraintes métier qu’il faut bien gérer dans l’application Django.

### Règles par jour et variables

Dans une campagne (par ex une campagne sucrière, métallurgique, etc.), il peut y avoir des **règles métiers variant selon le jour** ou la période :

- **Planning intégré** : Intégrez dans votre modèle de données la notion de calendrier de campagne. Par exemple, une table _CalendrierCampagne_ avec un enregistrement par jour contenant des infos telles que "jour férié", "arrêt technique", "objectif de production du jour", etc. Cela permet d’avoir dans l’app les données nécessaires pour appliquer des règles particulières à certains jours.
- **Règles configurables** : Si les règles changent d’une campagne à l’autre, il peut être utile de les rendre configurables via l’UI (par ex, stockées en base) plutôt que codées en dur. Par exemple, un pourcentage de tolérance sur un écart de production journalier pourrait être un paramètre. Vous pouvez prévoir un écran d’administration pour saisir ces paramètres en début de campagne.
- **Application des règles** : Dans le code de calcul (services métier par ex), prenez en compte ces variations. Par ex, _"si jour férié, alors la règle de calcul de rendement est différente"_ pourrait se traduire par une condition dans le service de calcul ou par l’utilisation d’un coefficient venant d’une table config.
- **Documentation** : Ces règles spécifiques doivent être bien documentées car elles ne sont pas triviales. Mettez des commentaires dans le code pour renvoyer à la documentation métier correspondante ou expliquer la raison de ces exceptions.

### Historisation des données de campagne

L’historisation est cruciale pour pouvoir auditer le passé et aussi comparer les performances d’une campagne à l’autre :

- **Pas de perte de données** : Ne jamais supprimer ou écraser définitivement des données de production. Si un recalcul est fait, conservez soit l’ancienne valeur quelque part (champ séparé "valeur_initiale" ou dans un historique), soit au moins logguez l’ancien résultat. Idéalement, optez pour un modèle de versionnement.
- **django-simple-history** : Comme mentionné, cette lib peut garder l’historique de chaque instance de modèle. Par exemple, chaque objet _BilanJournalier_ aurait ses versions successives enregistrées, avec date et utilisateur. Ainsi, on peut remonter l’évolution jour par jour si des corrections ont eu lieu.
- **Modèles d’historique manuels** : Alternativement, créez des modèles _History_ séparés. Ex : un modèle _LotProductionHistory_ qui stocke les mêmes champs qu’un Lot, plus un champ `historique_date` et `lot_reference`. A chaque modification majeure, insérez-y une copie. C’est plus lourd à maintenir que la librairie, mais peut offrir un contrôle total (par ex ne stocker que certaines infos).
- **Périmètre de l’historique** : Décidez ce qui doit être historisé. Peut-être que toutes les données brutes journalières sont immuables (mesures capteurs par ex ne changent pas) – pas besoin d’historiser. Par contre, les résultats calculés ou validations peuvent changer suite à corrections – c’est là qu’il faut historiser.
- **Purge** : Attention, historiser signifie accumuler beaucoup de données au fil des ans. Prévoyez une politique d’archivage/purge si nécessaire (ex: ne garder l’historique détaillé que des 10 dernières années, etc.), en accord avec les contraintes légales ou métier.

### Recalculs et corrections

Il est courant en industrie qu’après coup, on doive **recalculer** certains indicateurs (ex: un capteur était mal calibré, on corrige ses données -> il faut recalculer le rendement des jours impactés).

- **Conserver les données brutes** : Toujours stocker les données sources brutes initiales (par ex les relevés capteurs originaux). Les calculs doivent idéalement se faire sur ces données brutes, en appliquant des formules. Ainsi, si on change une formule ou qu’on corrige une donnée brute, on peut relancer le calcul sur la période et obtenir les nouvelles valeurs.
- **Fonctions idempotentes** : Concevez les fonctions de calcul de sorte qu’elles puissent être appelées à tout moment pour recalculer à l’identique un résultat, sans effets de bord (idempotence). Par ex, `calculer_bilan(jour)` lit toutes les données du jour et recalcule, au lieu de faire un incrément ou un delta. Ça évite les erreurs d’accumulation.
- **Outils de recalcul** : Fournissez peut-être dans l’UI un moyen de déclencher un recalcul. Par ex, un bouton "Recalculer la journée du 12/11 suite à correction". Celui-ci peut appeler un endpoint API qui exécute le service de recalcul pour ce jour. Journalisez ces actions comme dit (qui a recalculé).
- **Performance du recalcul** : Si recalculer une campagne entière prend du temps (plusieurs minutes), envisagez de faire ces calculs en tâche arrière-plan (Celery) ou au moins de manière asynchrone vis-à-vis de l’UI (avec feedback à l’utilisateur quand terminé).
- **Verrouillage** : Pendant un recalcul, s’assurer que personne d’autre ne modifie les mêmes données. On peut par exemple mettre un lock applicatif (un champ "calcul_en_cours" dans Campagne, ou un verrou Redis/Celery worker) pour éviter deux recalculs concurrents.
- **Comparaison pré/post** : Idéalement, fournir un diff des résultats avant/après recalcul pour validation. Cela peut être dans un rapport ou logué.

### Bilans de fin de campagne

En fin de campagne (ou périodiquement), des **bilans** sont générés (rapports de production, de qualité, etc.) :

- **Automatisation** : Ces bilans peuvent être générés automatiquement par l’application. Par exemple, une commande `genere_bilan_campagne` qui compile toutes les données en fin de campagne et sort un PDF ou un ensemble de chiffres. Automatisez un maximum pour éviter les erreurs manuelles. Vous pouvez utiliser libraries comme **ReportLab** pour PDF, ou même générer un Excel de synthèse via OpenPyXL si c’est l’attendu.
- **Traçabilité des bilans** : Stockez en base le fait qu’un bilan a été validé/généré à telle date par tel utilisateur. Cela recoupe la traçabilité.
- **Historisation des bilans** : Conserver les bilans finaux (ex: fichier PDF archivé, ou snapshot des indicateurs en base). Ainsi, même si on recalcule plus tard, on garde la trace de ce qui avait été présenté à l’époque.
- **Comparaison multi-campagnes** : Il peut être utile de développer des vues comparatives (ex: bilan campagne 2024 vs 2023). Pour cela, la base doit garder les données par campagne de manière distincte et accessible. Par ex, un modèle _Campagne_ parent de _Lot_ ou _Jour_, permettant de filtrer par campagne. On évite de mélanger les données de différentes campagnes sans référence, sinon on ne s’en sort plus.

En résumé, le système doit être pensé pour **évoluer dans le temps** : plusieurs campagnes se succèdent, chacune potentiellement avec des règles ajustées, des corrections a posteriori, et des bilans finaux. En codant de façon modulaire (règles externalisées, calculs recomposables) et en stockant toutes les informations intermédiaires, on se donne la possibilité de faire face aux aléas industriels (et ils sont nombreux).

## Comparaison Django vs Symfony sur les Grands Patterns

Pour conclure, faisons une **analogie des concepts** entre Django (Python) et Symfony (PHP) afin de situer les équivalences et différences clés :

|**Aspect**|**Django (Python)**|**Symfony (PHP)**|
|---|---|---|
|**Modèles / ORM**|Modèles Django définis en Python (classes héritant de `models.Model`) avec ORM intégré de type Active Record. Les objets comportent directement des méthodes d'accès (ex: `obj.save()`). Pas de getters/setters explicites, l'ORM gère l'accès aux champs. Migrations gérées par Django (`makemigrations/migrate`).|Entités Doctrine (classes PHP) généralement avec propriétés privées et getters/setters. ORM Doctrine de type Data Mapper où on passe par un EntityManager pour persister (`$em->persist($entity); $em->flush();`). Doctrine offre plus de customisation (mapping XML/YAML possible, hooks). Migrations gérées par Doctrine (commands diff/migrate).|
|**Logique Métier**|Par défaut intégrée soit dans les modèles (méthodes de modèle, managers) soit dans les vues. Possibilité de créer une couche _services_ Python pour isoler la logique métier complexe, mais Django n'impose rien. On peut utiliser des modules de services ou utilitaires, sans container d'injection.|Symfony encourage une séparation nette : contrôleurs le plus simples possible, logique dans des services (classes métiers). Symfony fournit un **container d'injection de dépendances** puissant pour gérer les services et leur lifecyle. On définit les services dans YAML/PHP, et on les injecte dans les contrôleurs. Cette approche est plus formelle qu'avec Django, qui est moins structuré à ce niveau.|
|**Vues / Contrôleurs**|Django utilise le pattern MVT : les _views_ Django correspondent aux contrôleurs en MVC. Ce sont des fonctions ou classes qui reçoivent `request` et retournent `response`. Django propose des vues génériques. Le routing se fait via du code Python ([urls.py](http://urls.py)) en associant une URL regex/path à une vue.|Symfony utilise des _Controllers_ en PHP, souvent organisés par _Bundle_. Le routing peut se faire par annotations dans le contrôleur ou via des fichiers YAML de routes. Les contrôleurs Symfony sont généralement plus verbeux (il faut instancier la réponse, etc.), mais le framework fournit des abstractions (par ex, `$this->render()` pour retourner une vue Twig).|
|**Templates**|Django a son moteur de templates intégré (syntaxe avec `{% %}` et `{{ }}`). Il est volontairement limité en logique pour forcer la séparation présentation/métier. Les templates Django sont généralement rendus côté serveur (mais ici le front est React, donc usage limité aux emails ou à l'admin).|Symfony utilise **Twig** comme moteur de templates, à la syntaxe très proche de Django template (double accolades, etc.) – la transition est facile. Twig est puissant et extensible. En Symfony on rend beaucoup de vues Twig côté serveur pour les applis traditionnelles. Dans un contexte API + React, Symfony servirait surtout JSON et peu de Twig également.|
|**Formulaires**|Django Forms, y compris ModelForm, permettent de générer facilement des formulaires HTML côté serveur et de valider les données. C'est très automatisé (on définit la classe form et Django fait le reste dans le template avec quelques balises). Moins utilisé dans un contexte API, mais très pratique en admin ou appli classique.|Symfony Forms (FormType classes) sont plus verbeuses : on crée une classe qui construit le formulaire champ par champ et configure les options. Dans le contrôleur, on crée une instance du form et on le passe à la vue Twig qui le rend. Système très flexible (beaucoup de types de champs, possibilité d’embarquer des collections de formulaires), mais plus de code à écrire qu'en Django.|
|**Commandes CLI**|Django a `manage.py` avec les **management commands** extensibles. On crée un fichier Python dans `management/commands`, la commande est automatiquement disponible. Très simple à implémenter et intégrer (utilise l'environnement Django directement).|Symfony utilise le composant **Console**. On crée une classe qui étend `Command` et on l’enregistre comme service (ou via autoconfigure). On exécute via `bin/console <commande>`. C'est assez similaire en concept, un peu plus verbeux en code (il faut définir configure() et execute()). Le résultat est le même : permettre d'écrire des scripts CLI faisant appel au code de l'appli.|
|**API / Webservices**|Django n'a pas d'API REST par défaut dans le core, on utilise Django REST Framework (ou alternative comme Django Ninja). DRF est un ajout puissant mais optionnel. On écrit explicitement les ViewSets/Serializers. Pas de magie, on contrôle précisément les endpoints et la sérialisation.|Symfony nativement ne fournit pas d'API REST clé en main, mais l'écosystème propose **API Platform** qui s'intègre à Symfony. API Platform peut auto-générer des endpoints CRUD pour les entités Doctrine en quelques config, et inclut pagination, filtres, docs OpenAPI out-of-the-box. Sinon, on peut utiliser les contrôleurs Symfony classiques pour retourner du JSON manuellement ou via serializer (JMS Serializer par ex). L'approche Symfony peut être plus "automatisée" avec API Platform, là où Django/DRF est un peu plus manuel mais très configurable.|

_(Tableau : Comparaison des approches Django vs Symfony)_

En synthèse, **Django** se distingue par son intégration “tout-en-un” (ORM, template, forms, admin) et une philosophie pragmatique qui mise sur la **simplicité et la rapidité de développement**, avec une structure de projet minimaliste. **Symfony**, lui, s’appuie sur une architecture plus **configurable et découpée**, avec un moteur d’injection de dépendances, une séparation plus formelle des couches et un écosystème de bundles/outils riche pour ajouter des fonctionnalités (au prix d’une courbe d’apprentissage plus élevée). A performance comparable, le choix entre les deux dépend souvent du langage maîtrisé par l’équipe (Python vs PHP) et des préférences en termes de structure. Dans notre contexte industriel, Django offre un développement rapide et une robustesse éprouvée, notamment grâce à son ORM et son écosystème scientifique Python (utile pour des calculs complexes), tandis que les analogies avec Symfony permettent de rassurer sur le fait que tous les grands concepts existent de part et d’autre (modèles, vues/contrôleurs, forms, CLI, etc.), simplement implémentés différemment.

## Conclusion

Ce guide a présenté les meilleures pratiques pour mener à bien un projet Django 4.x couplé à Django REST Framework dans un contexte industriel exigeant. En résumé, il convient de :

- **Structurer proprement le projet** en applications modulaires, avec une configuration souple par environnement et un code organisé (services métiers, tests, utilitaires partagés).
- **Exploiter pleinement Django et DRF** en suivant leurs conventions : modèles bien pensés (et indexés), vues légères, serializers sécurisés et efficaces, API documentée et paginée, formulaires et commandes mis à profit pour les besoins d’interactions hors web.
- **Mettre en place une chaîne CI/CD** fiable (tests automatiques, qualité du code, containerisation Docker, déploiement orchestré) pour livrer fréquemment en gardant la qualité.
- **Sécuriser l’application** à tous les niveaux : de l’infrastructure (Docker, réseau) aux contrôles applicatifs (auth LDAP/JWT, permissions fines, protections CSRF/XSS) en passant par la surveillance active (logs, monitoring, APM).
- **Prendre en compte les spécificités métier** dès la conception : l’historisation des données, la capacité de recalcul et d’audit, la gestion de règles évolutives, afin que l’outil accompagne réellement le processus industriel sans le brider.
- **Prévoir la maintenance sur le long terme** via documentation, tests, monitoring et une base de code propre et extensible, pour que l’application puisse évoluer avec les besoins futurs (nouvelles campagnes, changements de réglementation, etc.).

En appliquant ces bonnes pratiques, le projet bénéficiera d’une architecture solide, d’une qualité logicielle élevée et d’une confiance accrue de la part des utilisateurs finaux. Django est particulièrement adapté aux applications métier durables et complexes, et couplé avec une stack moderne (React, Docker, CI/CD), il permet de concilier **rapidité de développement** et **fiabilité en production**, ce qui est un atout majeur pour un projet industriel ambitieux tel que celui de Gardel en 2025.

**Sources :**

- Meilleures pratiques de structure et configuration Django
- Recommandations code Django (modularité, tests, sécurité)
- Intégration CI/CD et monitoring
- Concepts de couche service et logique métier
- Historisation et traçabilité des données
- Gestion des permissions et rôles dans Django
- Comparatif Django vs Symfony (structures MVC, ORM, forms)