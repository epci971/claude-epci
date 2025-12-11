# Meilleures Pratiques React 2025 dans un Projet Django Intégré

## Introduction

Dans un projet Django **multi-pages** tel que _Gardel_, il est courant d’intégrer ponctuellement des composants **React** directement dans les templates Django, afin d’enrichir certaines pages par des tableaux interactifs, formulaires dynamiques ou visualisations graphiques. Contrairement à une application **SPA** autonome, ici React cohabite avec le rendu côté serveur de Django : chaque page est principalement rendue par Django (HTML statique), puis React vient « améliorer » des portions ciblées. Ce rapport passe en revue les **meilleures pratiques en 2025** pour réussir cette intégration hybride, en couvrant l’architecture front-end, l’outillage (Vite, Webpack), l’écosystème (Tailwind, librairies UI), la gestion d’état, les appels API, l’organisation du code, ainsi que les aspects d’animation, d’accessibilité et d’amélioration progressive. Un guide de démarrage concret est proposé en fin de document pour aider un développeur Django à intégrer un build React modulaire via **Vite + Tailwind** dans un template Django.

## Architecture Front-End Intégrée (2025)

**En 2025**, les bonnes pratiques d’architecture pour des composants React embarqués favorisent une approche modulaire et progressive. Plutôt que de transformer l’application en single-page app, on recommande de n’utiliser React que pour les **composants interactifs ciblés**, tout en laissant Django générer le contenu statique principal. Concrètement, chaque composant React est monté dans un conteneur `<div>` spécifique du template (éventuellement avec des attributs de données), et React se charge uniquement de cette portion du DOM. Cette approche présente plusieurs avantages :

- **Isolation des composants** : chaque widget React fonctionne indépendamment (avec son propre état local ou contexte), ce qui évite de mêler logiques front et back de façon trop complexe.
- **Chargement conditionnel** : grâce au bundler (voir section suivante), on peut charger le code React **seulement sur les pages qui en ont besoin**. On utilise le **code splitting** et le **lazy loading** de React pour s’assurer que seuls les composants présents sur la page sont effectivement chargés côté client, sans alourdir inutilement les autres pages.
- **Pas de duplication de routage** : Django continue de gérer le routage global et le rendu initial. React n’intervient que pour la logique dynamique fine (par exemple la validation en temps réel d’un formulaire, les filtres d’un tableau, etc.), ce qui évite d’avoir à dupliquer les règles de navigation ou de sécurité côté front.

En suivant ce modèle, on obtient une architecture _« progressivement améliorée »_ : la page se charge initialement comme n’importe quelle page Django classique, puis les **fragments React** se **montent** et enrichissent l’UI. Dans ce contexte, il n’est généralement pas nécessaire d’implémenter un router côté React (sauf éventuellement pour une sous-section très dynamique), ni d’avoir une architecture Redux lourde globale – chaque composant peut gérer son état local ou utiliser un petit store dédié si besoin.

## Intégration de React avec Django via Vite

Pour intégrer React de manière optimale, on utilise en 2025 des bundlers modernes comme **Vite** (plutôt que Webpack, plus lourd). Vite offre un développement rapide (HMR efficace) et une excellente optimisation en production. Les bonnes pratiques d’intégration Django+Vite incluent :

- **Configuration du bundler avec manifest** : Configurer _vite.config.js_ pour générer un `manifest.json` d’assets, pointer le `base` sur le répertoire static de Django, et définir des **entry points** adaptés. Par exemple, on peut avoir une entrée principale `main.jsx` (ou `.tsx`) qui importe React et monte les composants nécessaires. L’option `build.manifest: true` est essentielle pour que Django sache quels fichiers inclure.
- **Inclusion conditionnelle des assets** : En mode dev, on peut utiliser le dev server de Vite pour charger les modules avec HMR. En production, on utilisera le manifest pour inclure les fichiers compilés (JS et CSS) dans les templates Django. Le paquet _django-vite_ facilite cela : il fournit la templatetag `{% vite_asset 'chemin/vers/entry.js' %}` qui injecte une balise `<script type="module">` pointant vers le bundle correct, et ajoute automatiquement les fichiers CSS liés. On peut appeler cette templatetag uniquement dans les pages concernées (ou dans le layout de base si l’entrée est unique mais légère).
- **Injection des composants React** : Dans le template Django, à l’endroit où l’on veut le composant interactif, on insère un conteneur vide. Par exemple : `{% load react_tags %} <div id="react-MyComp"></div> {% static '...' %}`. Une approche élégante consiste à utiliser des _data attributes_ pour indiquer quel composant monter et avec quelles props. Par exemple, `<div data-react-component="NomDuComposant" data-react-props='{"clé": "valeur"}'></div>`. Au chargement, le script principal React peut balayer le DOM, détecter ces attributs et créer un root React pour chaque élément, en y rendant le composant indiqué avec les props fournies. Ce mécanisme a été démontré dans de récents guides : on initialise React sur chaque `<div data-react-component>` présent, ce qui permet de monter plusieurs composants indépendants sur une même page. **Seuls les modules réellement utilisés sont chargés** grâce au _dynamic import/lazy_, évitant de surcharger la page.
- **Bundle léger et performant** : Vite permet de configurer facilement un split du bundle _vendor_ (React, React-DOM, etc.) distinct du code applicatif. Ainsi, le poids initial par page est réduit et les librairies communes peuvent être mises en cache sur le long terme par le navigateur. En production, on active aussi la minification et le tree-shaking par défaut. Les fichiers générés comportent un hash pour le cache-busting.

En somme, l’intégration via Vite consiste à **automatiser la pipeline front** : on développe les composants en React/TypeScript dans un dossier dédié (par ex. `frontend/`), Vite se charge de compiler le tout (incluant Tailwind, voir plus bas) vers des fichiers statiques dans `static/`, et Django inclut ces fichiers statiques dans les pages. On peut recourir soit à une solution _maison_ (script de génération de tags, tag custom `{% RC %}`, etc. comme dans certains tutoriels), soit à une librairie prête à l’emploi comme _django-vite_. Quoi qu’il en soit, on obtient un flux de travail fluide : **`npm run dev`** pour lancer Vite en HMR pendant que `runserver` tourne, puis **`npm run build`** et `collectstatic` pour la production.

## Design System : Tailwind CSS et Librairies de Composants

**Tailwind CSS** s’est imposé comme une base de design efficace en 2025, y compris dans un contexte Django/React intégré. Tailwind offre une approche utilitaire qui permet de conserver le style au plus près du markup, et de faciliter la cohérence visuelle entre les composants React et les pages Django statiques. Les meilleures pratiques incluent : configurer Tailwind en mode JIT (Just-in-Time) pour ne garder que les classes utilisées (via la purge), définir dans _tailwind.config.js_ le chemin des templates Django et des fichiers React (afin que toutes les classes utilisées soient bien détectées), et utiliser des variables de thème (couleurs, spacing) partagées pour que les éléments React s’intègrent harmonieusement au reste du site.

En complément de Tailwind, de nombreuses **librairies de composants** compatibles existent. L’état de l’art en 2025 privilégie des bibliothèques **headless** ou non-intrusives, qui fournissent des composants accessibles tout en laissant la main sur le style (pour pouvoir utiliser Tailwind). Parmi les plus en vue :

- **shadcn/ui** : une collection open-source de composants préconstruits, combinant Tailwind CSS et les primitives de Radix UI. La particularité est que l’on **importe le code source des composants dans son projet** (plutôt qu’une dépendance npm figée), ce qui donne un contrôle total sur le style et le comportement, sans risque de _lock-in_. Cette approche « copy-paste » offre des composants accessibles et personnalisables, tout en évitant les dépendances cachées. En d’autres termes, _shadcn/ui_ sert de base pour construire son _design system_ interne, en permettant d’éjecter le code de chaque composant (boutons, formulaires, dialogues, etc.) dans son propre codebase.
- **Radix UI** : une librairie **headless** populaire qui fournit des primitives non stylées mais entièrement accessibles. Radix offre des composants bas niveau (menu, dialog, popover, tabs, etc.) gérant pour vous toute la logique d’accessibilité (ARIA, clavier, focus). On l’utilise en combo avec Tailwind : on obtient ainsi la structure et le comportement d’un composant accessible, et on applique nos classes Tailwind pour le style visuel. Radix est apprécié pour sa robustesse et sa compatibilité SSR, et sert souvent de fondation (il est par exemple utilisé par shadcn/ui en coulisses).
- **Headless UI** : développé par l’équipe Tailwind, c’est une autre librairie de composants non stylés et accessibles, conçus pour s’intégrer parfaitement avec Tailwind CSS. Comme le dit la documentation officielle, il s’agit de composants « entièrement non stylés et pleinement accessibles, conçus pour s’intégrer à Tailwind CSS ». Headless UI propose notamment des `<Menu>`, `<Listbox>`, `<Dialog>` (modal), `<Popover>`, etc., couvrant les besoins courants d’UI interactive sans imposer de styles. Par rapport à Radix, le catalogue est plus restreint, mais l’intégration avec Tailwind est immédiate (les exemples fournis utilisent directement des classes Tailwind).

En plus de ces solutions, citons **Tailwind UI**, la bibliothèque commerciale officielle de composants pré-stylés par les créateurs de Tailwind, qui peut accélérer la mise en page (mais les composants sont fournis en HTML/CSS, à adapter en React le cas échéant). Des kits gratuits comme **DaisyUI** existent également, ajoutant une couche de composants sur Tailwind. Toutefois, la tendance en 2025 est de s’appuyer sur des _headless components_ pour construire une bibliothèque maison de composants, garantissant à la fois l’accessibilité et la personnalisation visuelle. Cela s’inscrit dans une philosophie de _Design System_ modulable : **utiliser Tailwind comme base** de style, et **composer des composants réutilisables** à partir de briques accessibles (Radix/HeadlessUI) éventuellement combinées à du code source custom (shadcn/ui).

## Comparatif des Solutions de Gestion d’État (Zustand, Jotai, Redux Toolkit)

La gestion d’état globale ou partagée entre composants est un enjeu clé en React. En 2025, trois bibliothèques ressortent souvent : **Redux Toolkit**, **Zustand** et **Jotai**. Chacune a ses atouts, et le choix dépend des cas d’usage. Pour un projet comme Gardel (formulaires complexes, tableaux de données _datamart_, validations, chargements progressifs, etc.), on peut formuler les recommandations suivantes :

- **Redux Toolkit** : C’est la version moderne et simplifiée de Redux, fournie officiellement. Elle **structure l’état global de manière prédictible** (un store unique avec des _slices_ d’état immutables) et convient bien aux **grandes applications complexes** nécessitant un suivi d’état centralisé et rigoureux. Redux Toolkit apporte des outils comme `configureStore` et `createSlice` qui réduisent le boilerplate et intègrent Immer (mise à jour immuable facilitée). On le recommande si l’application front-end intégrée devient vraiment conséquente ou si l’équipe est déjà familière de Redux. En revanche, pour un usage ponctuel dans quelques widgets isolés, Redux peut être surdimensionné (taille du bundle, verbosité).
- **Zustand** : Un **petit store léger** et rapide, basé sur des hooks. Zustand est sans boilerplate : on définit un store via une fonction `create()` en quelques lignes, puis on utilise directement les hooks générés (`useStore`) dans les composants. Il est adapté aux **applications de taille moyenne** ou aux fonctionnalités isolées qui ont besoin d’un état global minimal (ex : partager quelques valeurs entre plusieurs composants sur une page). Sa simplicité le rend idéal pour du prototypage rapide, ou pour remplacer un contexte React un peu trop complexe. Par exemple, pour un formulaire multi-étapes où plusieurs sous-composants doivent accéder aux mêmes données temporairement, Zustand offre une solution plus ergonomique qu’un Redux complet.
- **Jotai** : Une approche différente, basée sur des **atomes d’état**. Jotai permet de gérer l’état sous forme de petites unités (atoms) que l’on combine, avec une mise à jour très fine (un composant abonné à un atom ne se re-rendera qu’en cas de changement de celui-ci). C’est excellent pour optimiser les re-rendus et avoir un **contrôle granulaire** sur le flux d’état. Jotai s’appuie sur le Context API en interne mais expose un usage plus simple. On le recommande lorsque l’application nécessite de nombreuses petites sources d’état indépendantes, ou pour des cas où la performance de rendu est critique (par ex, un gros formulaire où chaque champ pourrait être un atom, évitant qu’une maj d’un champ ne rerender tous les autres). Il convient aussi si l’on veut isoler logiquement différentes parties de l’état : par exemple une atom pour les filtres d’un tableau, une autre pour la pagination, etc., sans tout centraliser.

En résumé, **le choix dépend de l’échelle et des besoins** : _Redux Toolkit_ reste la solution puissante pour un **état global complexe** et quand on a besoin d’outils comme le devtools Redux ou d’intégrer des middlewares (utile si beaucoup de logique métier côté client). _Zustand_ est souvent suffisant pour la plupart des besoins d’un projet Django+React **modulaire**, car on a rarement besoin d’un énorme store global – on peut créer un petit store par composant ou fonctionnalité. _Jotai_ se positionne entre les deux : plus structuré que Zustand quand l’app grandit, tout en évitant la lourdeur de Redux, et très efficace pour éviter les re-rendus superflus. Notons qu’il existe aussi d’autres solutions (par ex. **Redux Toolkit Query** pour gérer le cache API, ou **Recoil** de Facebook), mais Zustand et Jotai ont gagné en popularité pour leur simplicité. Enfin, ne pas oublier que **React Context et les hooks d’état natifs** (`useState`, `useReducer`) suffisent parfois : pour un formulaire isolé, on peut très bien se passer d’une librairie externe et garder l’état localement ou via un contexte englobant quelques composants. La règle d’or : _commencer simple_, puis introduire une librairie de state management seulement si le partage d’état devient trop complexe à gérer avec les outils de base.

## Requêtes API : React Query vs SWR

Les composants React de Gardel communiquent probablement avec une API (par ex une Django REST API) pour charger des données ou soumettre des formulaires. Deux outils modernes se distinguent pour gérer ces interactions réseau côté front : **React Query (TanStack Query)** et **SWR** (stale-while-revalidate). Ces bibliothèques facilitent les appels API en offrant le caching, le suivi du statut de requête (loading, error, success) et la synchronisation des données. Voici un comparatif et des bonnes pratiques :

- **React Query** : C’est une solution complète de gestion de l’**état serveur** (données issues d’API). On définit des _queries_ avec une clé et une fonction de fetch, et React Query s’occupe de la lancer au montage du composant, de mettre en cache le résultat, de le rafraîchir au besoin, etc. Ses points forts : une **grande richesse de fonctionnalités** (par ex. invalidation manuelle de cache, refetch automatique au focus de la fenêtre, gestion fine des _stale times_), un support natif des **mutations** (POST/PUT/DELETE) avec possibilité d’**updates optimistes** et rollbacks, ainsi que des devtools très pratiques pour voir l’état du cache en temps réel. React Query brille dans les applications complexes où l’on a beaucoup de points de données différents et des interactions utilisateur modifiant ces données. Par exemple, dans Gardel, s’il y a des tableaux de bord avec données paginées ou éditables, React Query permettra de mettre à jour localement une ligne dès que l’utilisateur la modifie (optimistic update) et de synchroniser avec le serveur en arrière-plan. Côté performances, React Query peut **regrouper/batcher** les requêtes et optimiser les re-renders, ce qui lui donne un avantage dans les applications à données complexes. En somme, on choisira React Query si l’application implique **de nombreuses mutations de données, un besoin pointu de contrôle du cache et des revalidations**, et qu’on souhaite un éventail complet d’options pour gérer les états de chargement/erreur et les rafraîchissements.
- **SWR** : Créé par Vercel, SWR propose une API plus simple et légère pour le data fetching. Son nom vient de _stale-while-revalidate_ : la philosophie est de **retourner d’abord les données en cache (stales) puis de déclencher en arrière-plan la requête pour avoir les données fraîches**, ce qui donne une UI très réactive. SWR est souvent jugé **très facile à prendre en main** – un simple hook `useSWR(key, fetcher)` – et il convient bien aux applications modestes ou aux pages où les besoins de caching sont simples. Il gère aussi le refetch on focus, la reconnexion réseau, etc., de manière automatique comme React Query. Cependant, SWR a moins de fonctionnalités avancées par défaut : par exemple la gestion des mutations n’est pas aussi complète (on peut faire `mutate()` pour mettre à jour le cache, mais l’API est moins structurée que le `useMutation` de React Query). De même, il n’y a pas d’outil officiel de devtool pour visualiser le cache SWR (ceci dit, la simplicité de SWR fait que ce n’est pas forcément nécessaire). **Quand choisir SWR ?** Essentiellement lorsque **l’application est simple ou de taille moyenne**, avec des besoins de data fetching modérés, et qu’on veut minimiser le code et le poids des dépendances. Par exemple, pour quelques appels API ponctuels sur une page sans logique complexe de cache, SWR fera très bien l’affaire avec moins de configuration. L’objectif peut aussi être la **taille du bundle** : SWR étant un peu plus léger, si on cherche à réduire l’empreinte front et qu’on n’a pas besoin des extras de React Query, c’est un bon choix.

**Bonnes pratiques communes** : Quel que soit l’outil choisi, on veillera à **structurer les clés de cache** de façon cohérente (souvent par ressource ou par identifiant d’objet) afin de pouvoir invalider ou refetch les données au bon moment. Penser à définir des **stratégies de rafraîchissement** : par ex, utiliser un _stale time_ adapté (si les données changent rarement, on peut éviter de refetch trop souvent), ou au contraire mettre en place un polling si besoin de données temps réel. Il est recommandé d’encapsuler les appels dans des hooks custom (ex: `useFetchUsers()` qui utilise `useQuery` ou `useSWR` en interne) pour centraliser la logique et pouvoir réutiliser facilement. En cas d’erreur de requête, offrir une UX appropriée : on peut exploiter le champ `error` retourné pour afficher un message dans le composant, et éventuellement utiliser un _Error Boundary_ React global pour capter les erreurs fatales d’appel API. Les deux librairies permettent une **gestion fine des erreurs** – par exemple SWR offre un contrôle granulaire pour afficher les erreurs aux endroits appropriés. Enfin, pour améliorer la perception de rapidité, on peut **précharger/préféter** certaines données _avant_ que l’utilisateur n’en ait besoin (par ex, React Query propose une méthode `queryClient.prefetchQuery` qu’on peut appeler lors du rendu serveur Django pour inclure déjà des données, ou au survol d’un lien pour charger à l’avance la page suivante). De même, exploiter le **cache global** pour éviter des requêtes redondantes : par exemple si plusieurs composants ont besoin de la même liste de références, utiliser une même query key afin de mutualiser le résultat.

En somme, _SWR_ et _React Query_ ont des forces comparables sur la gestion de cache et la revalidation. **Pour une application simple (quelques endpoints)**, SWR peut suffire et apporter une solution rapide. **Pour une application plus complexe**, React Query est généralement le choix privilégié pour ses **fonctionnalités riches et son contrôle accru**, même au prix d’un peu plus de complexité initiale.

## Organisation des Composants et Code (Projet Multi-lots)

Dans un projet multi-lots (plusieurs modules ou fonctionnalités distinctes), il est crucial d’organiser le code front de manière propre et **isolée par domaine** afin de faciliter la maintenance et le travail en parallèle des équipes. Voici les bonnes pratiques recommandées :

- **Structure modulaire des dossiers** : Séparer le code par « lot » fonctionnel. Par exemple, on peut avoir un répertoire `frontend/src/` avec des sous-dossiers pour chaque module (ex: `tableaux/`, `formulaires/`, `dashboard/`, etc.), chacun contenant ses composants spécifiques. En complément, prévoir des dossiers communs pour les éléments réutilisables globalement : `components/` (composants UI génériques, ex: Button, Modal), `hooks/` (hooks custom), `utils/` (fonctions utilitaires), `styles/` (fichiers CSS/Tailwind si besoin), `store/` (états globaux éventuels), etc. Une arborescence type issue d’un projet réel pourrait ressembler à ceci :

```
src/
├── api/        (logique d'API, ex: fonctions fetch ou configuration React Query)
├── common/     (composants ou utils communs)
├── components/ (composants UI génériques)
├── context.tsx (fournisseurs de contexte globaux si nécessaires)
├── helpers/    (fonctions helper)
├── hooks/      (hooks personnalisés)
├── pages/      (composants de pages entières ou points d'entrée de modules)
├── [module1]/  (ex: jobs/, un lot spécifique avec ses composants)
├── [module2]/  (autre module)
├── styles/     (fichiers CSS, ex: index.css qui importe Tailwind)
└── utils.tsx   (utilitaire global)

```

Chaque module/lot peut ainsi avoir son propre espace, et idéalement son **point d’entrée** si on décide de faire des bundles séparés. En effet, Vite permet de définir plusieurs entrées (multi-page app) pour générer des fichiers JS distincts par section. On pourrait avoir par exemple `tableaux.tsx` qui bundle tout le nécessaire pour les pages de tableaux, et `formulaires.tsx` pour les pages de formulaires, etc., afin d’éviter de charger du code inutile sur certaines pages. Cette séparation se refléterait dans le manifest Vite et permettrait d’inclure dans Django uniquement le bundle requis par page (via `{% vite_asset 'tableaux.tsx' %}` par exemple). Même si on ne va pas jusqu’à un build par module, le fait de structurer par dossier aide à clarifier les responsabilités.

- **Isolation logique et évitement du couplage** : Chaque lot ou composant complexe devrait idéalement **ne pas dépendre directement du code des autres lots**. S’il y a des interactions, passer par des abstractions communes (par ex. un service API central commun, ou un petit store global pour partager juste ce qu’il faut). L’objectif est de pouvoir faire évoluer un module sans craindre de casser un autre. Comme le souligne un guide récent, cette approche multi-apps permet une **isolation de chaque bundle React** avec son propre cycle de vie, son déploiement et même son versioning indépendant. On obtient ainsi une séparation claire des préoccupations, ce qui est idéal pour la scalabilité. Gardel pourrait par exemple avoir un module React pour la partie « visualisation de données » et un autre pour la partie « formulaires dynamiques », chacun évoluant séparément.
- **Réutilisation et bibliothèque interne** : Regrouper les composants réutilisables (boutons, inputs stylés, etc.) dans un dossier commun ou même un package interne (si le projet est très grand, on peut imaginer un monorepo avec un package npm interne pour les composants UI partagés). Cela évite la duplication et garantit la cohérence (tous les modules utilisent le même composant de sélection date, par ex.). Avec Tailwind, on peut créer des _components_ ou _partials_ CSS pour factoriser certains styles si besoin, ou utiliser des outils comme `@apply`.
- **TypeScript strict** : En 2025, il est fortement conseillé d’utiliser **TypeScript** pour tout le code React. Définir précisément les types de _props_ de chaque composant, les formats de données venant de l’API (éventuellement générer des types à partir du schéma ou des serializers Django), et activer les options strictes de TS. Le typage contribue grandement à la maintenabilité en évitant des bugs d’intégration (par ex, passer la mauvaise prop à un composant) et en facilitant le refactoring (on trouve immédiatement toutes les utilisations d’un type).
- **Hooks personnalisés pour la logique métier** : Une bonne pratique est d’extraire la logique complexe des composants React en dehors du JSX, via des hooks ou des fonctions pures. Par exemple, si un composant gère un formulaire avec plusieurs étapes et règles de validation, on peut créer un hook `useMultiStepForm(initialValues)` qui encapsule l’état interne et expose des méthodes (`nextStep`, `validateStep`, etc.). Le composant de présentation utilise ce hook, ce qui clarifie son JSX et permet de tester la logique du hook séparément. De même pour les appels API : un hook `useFetchData(id)` peut englober un appel React Query et ne retourner que `data` et `error`, ce qui simplifie le composant. Cette **isolation de la logique** améliore la lisibilité et le test unitaire du code.
- **Conventions de code et qualité** : Adoptez une convention de nommage consistante (par ex. PascalCase pour les composants, camelCase pour les fonctions, SCREAMING_SNAKE_CASE pour les constantes partagées, etc.). Mettez en place des outils de linting (_ESLint_) et de formattage (_Prettier_) intégrés au processus (éventuellement via un pre-commit hook) pour assurer une homogénéité du code écrite par différentes personnes. Ecrivez des tests unitaires pour les utilitaires et les hooks critiques (par ex. tester qu’un hook de validation retourne bien les erreurs attendues). Tout cela contribue à une **écriture maintenable** sur le long terme.

Enfin, soulignons l’avantage d’une approche multi-bundle dans Django : on peut tout à fait avoir **plusieurs applications React au sein d’un même projet Django**. Chaque « lot » important pourrait être compilé en un bundle séparé et inclus via une templatetag dédiée. Cela offre une véritable **scalabilité** car on limite la taille des JS par page et on cloisonne les évolutions de chaque partie. Cette approche modulaire est alignée avec le concept de micro-frontend (_sans introduire de complexité excessive non plus_). L’essentiel est de trouver le bon découpage pour Gardel : par exemple, si Gardel comporte un lot 1 “Bilan laboratoire” et un lot 2 “Suivi IPE” (hypothétiquement), et qu’ils n’ont pas de rapport entre eux, chacun peut avoir son code React indépendant.

## Animations et Expérience Utilisateur

L’ajout d’animations subtiles peut grandement améliorer l’expérience utilisateur, à condition de rester performant et accessible. En 2025, la référence pour les animations en React est **Framer Motion** (récemment renommé _Motion_). C’est un _framework_ d’animations _production-ready_, qui permet de créer des interactions fluides et complexes avec une API déclarative intuitive. Motion est **open-source, performant, et de niveau professionnel**, prenant en charge aussi bien les transitions simples que des gestes complexes ou des enchaînements d’animations orchestrés. Quelques conseils d’utilisation :

- Utilisez Framer Motion pour les animations d’entrées/sorties de composants (par ex. un panneau latéral qui slide, un modal qui fade in/out). Le composant `<AnimatePresence>` de Motion facilite l’animation lors du montage/démontage conditionnel d’éléments. Plutôt que de jouer avec des classes CSS et des setTimeout, on bénéficie d’une API qui gère le cycle de vie des éléments sortants proprement.
- Exploitez les _gestures_ (drag, hover, tap) fournies par Motion pour des interactions avancées (glisser-déposer réactif, boutons avec effet de pression, etc.). Ces interactions sont optimisées pour paraître natives et fluides. Par exemple, si une fonctionnalité de Gardel nécessite de réordonner des éléments par glisser, Motion peut détecter le drag et animer les cartes lors du réarrangement.
- Veillez toutefois à ne pas surcharger l’interface d’animations inutiles. Privilégiez les animations qui **servent le sens ou le feedback utilisateur** (un champ qui tremble en rouge en cas d’erreur de saisie, un loader qui tourne pendant un chargement, un volet de détails qui se déploie). Des animations trop nombreuses ou trop longues peuvent distraire ou ralentir la perception. Restez dans la subtilité et la cohérence du design system (ex: utilisez les mêmes durées et courbes d’accélération définies dans le thème Tailwind pour toutes les animations).
- Côté performance, Framer Motion est efficace (il utilise sous le capot le _browser_ **Web Animations API** quand possible, pour bénéficier de l’accélération GPU). Néanmoins, surveillez le coût de certaines animations sur des pages très lourdes en données. Par exemple, animer une liste de 1000 éléments n’est pas souhaitable. Réservez les animations aux éléments de niveau interface. Vous pouvez aussi combiner Tailwind pour des transitions simples (Tailwind propose des classes utilitaires pour certains effets CSS). Par exemple, pour un simple _hover effect_, inutile d’aller chercher Framer Motion : une classe `transition duration-150 ease-in` sur le CSS peut suffire. En revanche, pour un enchaînement plus complexe (comme un **stagger** où des éléments apparaissent l’un après l’autre en cascade), Motion offre un outil prêt à l’emploi (_variants_ et _staggerChildren_).

En somme, **Framer Motion** (Motion) est recommandé pour des animations **riches et maintenables** dans React. Son API _déclarative_ s’intègre bien avec React (on décrit _quoi_ animer, pas comment l’animer étape par étape). Cela permet d’avoir du code d’animation lisible et centralisé, plutôt que de gérer manuellement des classes CSS dans le composant. De plus, c’est compatible avec Tailwind – on peut utiliser les deux ensemble (par ex. un composant `<motion.div>` avec des classes Tailwind pour le style statique, et des props Motion pour l’animation). En complément, pensez à toujours vérifier l’**accessibilité** des animations : éviter les effets qui pourraient gêner les personnes sensibles (flashs, mouvements trop rapides). Respectez le réglage « _prefers-reduced-motion_» du système : CSS et Framer Motion permettent de désactiver ou réduire les animations pour les utilisateurs qui ont activé cette préférence.

## Accessibilité et Bonnes Pratiques de Code

**Accessibilité (a11y)** : L’accessibilité doit être considérée dès la conception de vos composants React. Dans un contexte Django+React, il faut veiller à ce que les portions enrichies par React restent utilisables par tous les usagers (lecteurs d’écran, navigation clavier, etc.). Quelques bonnes pratiques :

- **Utiliser du HTML sémantique** autant que possible. Par exemple, si un composant React affiche une liste de résultats, assurez-vous d’utiliser une liste `<ul><li>` plutôt que des `<div>` arbitraires. De même, les boutons doivent être de vrais `<button>` avec un label explicite (pas seulement des icônes cliquables sans texte). Django fournit souvent déjà du HTML correct, donc vos composants insérés doivent s’aligner sur ces standards.
- **Aria et roles** : Si vous créez un composant personnalisé (par ex. un composant d’autocomplete ou un menu déroulant), suivez les patterns ARIA recommandés. Des librairies comme Radix ou Headless UI gèrent en interne beaucoup de ces attributs pour vous, c’est un atout majeur. Par exemple, Radix UI garantit que son `<DropdownMenu>` aura tous les roles/menuitem et attributs ARIA nécessaires, alignés sur les pratiques WAI-ARIA. Si vous implémentez vous-même, il faut penser à des aspects comme : focus trap dans une modal, annoncer via `aria-live` les mises à jour dynamiques, mettre `aria-invalid="true"` sur un champ invalide, etc.
- **Navigation clavier** : Tout ce qui est faisable à la souris doit l’être au clavier. Testez que vos composants React peuvent être atteints par Tab, activés par Entrée/Espace si ce sont des boutons, etc. Par exemple, un composant custom de sélection doit gérer les flèches, l’ouverture du menu par Alt+↓, etc., ou s’appuyer sur un composant headless qui le fait. Ne _cassez_ pas le focus visuel fourni par le navigateur (Tailwind a une classe `focus:outline-none` souvent utilisée, mais veillez à remplacer par un style de focus personnalisé plutôt que de le supprimer complètement).
- **Couleurs et contrastes** : Si vous utilisez Tailwind, définissez votre palette de couleurs en respectant les contrastes AA/AAA pour le texte. Par exemple, des composants React dynamiques comme un tag ou un badge de statut doivent conserver un ratio de contraste suffisant sur fond coloré. Vous pouvez utiliser des utilitaires ou Stylelint avec un plugin a11y pour vérifier les contrastes.

En résumé, l’utilisation de composants accessibles (via Radix, Headless UI, etc.) vous met déjà sur la bonne voie en 2025, car beaucoup de bonnes pratiques sont intégrées. Mais cela ne dispense pas de tester manuellement avec un lecteur d’écran (NVDA, VoiceOver) et en mode navigation clavier pure, pour s’assurer que l’expérience est complète.

**Écriture de code maintenable** : La maintenabilité du code React est primordiale dans un projet qui va vivre (Gardel semble être un projet continu). Au-delà de l’architecture modulaire déjà évoquée, voici d’autres points à surveiller :

- **Lisibilité** : Préférez des composants clairs et courts. Il vaut mieux découper un gros composant en plusieurs sous-composants fonctionnels que d’avoir un monolithe de 500 lignes mêlant logique et présentation. Une règle empirique : si un composant dépasse ~200 lignes ou a trop de responsabilités, envisagez de le scinder. Utilisez des noms explicites pour vos composants et fonctions (ex: `UserTable` plutôt que `Table`, `useFetchUserData` plutôt que `useThing`).
- **Documentation interne** : N’hésitez pas à ajouter des commentaires JSDoc pour vos hooks ou fonctions complexes, spécifiant leur usage. Par exemple, documenter qu’un hook `useValidation()` renvoie tel objet et comment il doit être utilisé. Cela aidera vos collègues (et vous-même après quelques mois) à comprendre l’intention du code.
- **Gestion des erreurs et cas limites** : Rendez vos composants robustes en prévoyant les cas où les données sont manquantes ou invalides. Par exemple, un composant d’affichage de graphique devrait gérer le cas où les données ne sont pas encore là (afficher un loader ou un message), ou un composant de formulaire devrait vérifier que toutes les props nécessaires sont passées (en TypeScript, marquer certaines props comme obligatoires). Évitez de faire planter le composant pour une raison triviale (propriété undefined non gérée). L’utilisation de TypeScript vous aide ici, mais il faut tout de même penser aux null/undefined et aux erreurs d’API.
- **Optimisation** : Bien que la performance ne semble pas le point central, un code maintenable passe aussi par éviter les pièges de performance qui rendraient le debugging pénible plus tard. Par exemple, utilisez `React.memo` pour mémoriser des composants purement visuels qui reçoivent souvent les mêmes props (pour éviter des rerenders inutiles), ou utilisez des hooks comme `useMemo`/`useCallback` à bon escient pour éviter de recréer des objets/fonctions à chaque rendu si cela cause des rerenders profonds. Toutefois, n’optimisez pas prématurément : ne mettez ces mémoizations que si vous constatez un souci ou dans des endroits critiques (listes longues, etc.).
- **Tests** : Enfin, écrire quelques tests (avec Jest/RTL ou Vitest) assure la non-régression lors des évolutions. Par exemple, tester qu’un composant de calcul de KPI affiche bien le bon total selon les props, ou qu’un hook `useFormValidation` retourne une erreur quand un champ requis est vide. Cela renforce la confiance dans le code et sert de documentation vivante.

En suivant ces pratiques, on obtient un code base front **fiable, lisible et évolutif**. La combinaison de TypeScript (pour éviter les erreurs), de lintage auto, de composantisation poussée, et de tests là où c’est pertinent, permet d’absorber les nouvelles fonctionnalités sans transformer le projet en spaghetti.

## Amélioration Progressive et Rendu SSR/Hydratation

L’approche progressive (_Progressive Enhancement_) consiste à faire en sorte que les pages soient d’abord pleinement utilisables sans JavaScript, puis d’y ajouter des améliorations React si le JS est activé. Dans un projet Django, cela signifie que pour chaque fonctionnalité interactive, on devrait idéalement avoir un **fallback serveur**. Par exemple, un formulaire qui a une validation en direct côté React devrait aussi pouvoir être soumis de façon classique (requête HTTP) et validé côté serveur, afin que l’utilisateur puisse l’utiliser même sans JS (avec un retour d’erreur via une nouvelle page ou un rechargement). De même, une table de données filtrable côté client devrait présenter une liste par défaut et offrir un moyen de filtrer sans JS (par ex. un paramètre de requête via un lien ou un formulaire qui cause un refresh).

En pratique, tout n’est pas toujours implémenté en double – surtout si l’audience est captive (intranet par ex.) et utilisera majoritairement un navigateur moderne avec JS. Néanmoins, suivre les principes de l’amélioration progressive assure une meilleure robustesse générale de l’application. Voici comment concilier cela avec React :

- **Server-side rendering (SSR)** vs **CSR** : Pour qu’un composant React soit _totalement_ transparent en termes de SEO ou de non-JS, il faudrait le rendre côté serveur (générer son HTML initial) puis l’hydrater côté client. Or, Django ne peut pas rendre du React nativement. On pourrait imaginer un service Node.js côté serveur qui pré-rend les composants (via `react-dom/server`), ou utiliser un framework comme Next.js. Cependant, cela ajoute une complexité élevée pour un gain modéré si les composants ne sont qu’une partie de la page. Une réponse sur StackOverflow confirme qu’en effet _« il faut une forme de rendu côté serveur pour faire de la progressive enhancement avec React »_, l’idée étant de servir du HTML statique que React viendra hydrater ensuite. Toutefois, sans mettre en place Next.js, on peut s’approcher du concept d’amélioration progressive en combinant Django et un peu de logique front : Django sert du HTML pour la structure de base, puis **le front détecte et hydrate/enrichit les éléments dynamiques**. Comme l’explique le même post, si on rend le HTML via Django, on peut quand même faire du progressive enhancement en laissant le front React _trouver les éléments à améliorer et faire un `createRoot` dessus_*. C’est exactement notre approche avec les `data-react-component` : on a du HTML statique (peut-être simplifié) que React vient activer.
- **Exemple d’amélioration progressive** : Imaginons une page Django qui liste des items avec un bouton « Détails » à côté de chaque. En pur Django, ce bouton mène à une autre page ou ouvre un collapse via un peu de JS de base. En React, on pourrait au lieu de ça, au clic, charger dynamiquement les détails et les afficher sans recharger la page. Pour garder une amélioration progressive, on ferait en sorte que le bouton soit un lien classique `<a href="/item/42/details">` (ciblant une page de détails serveurs), mais qu’en JS on **intercepte le clic** et empêche la navigation pour plutôt déclencher le composant React d’affichage inline des détails. Ainsi, avec JS on a l’expérience améliorée (détail en ligne), sans JS le lien fonctionne et amène à une page séparée – l’utilisateur peut accéder à l’information malgré tout. Ce pattern est idéal car il concilie les deux mondes.
- **Hydratation partielle** : Comme évoqué, on n’a généralement pas de SSR React dans Django, donc on ne fait pas d’hydratation au sens classique (qui suppose que le même HTML a été généré par React côté serveur). En revanche, on peut parler d’« hydratation partielle » ou d’insertion de **composants îlots (islands)**. Notre page Django peut être vue comme une page _îlots_ où certaines divs seront occupées par des « îlots React ». Cette architecture en îlots est tendance pour améliorer les performances : seuls les îlots comportent du JS, le reste de la page reste statique. Dans notre cas, grâce au chargement conditionnel, on n’envoie du JS que pour ces îlots. Cela évite de **surcharger les pages** inutiles – par exemple, si une page ne contient aucun composant React, elle ne subira pas le coût de React (ni CSS additionnel, ni JS). Même si une page contient 3 composants React, chacun est monté indépendamment et ne fait rien tant qu’il n’est pas utilisé.
- **Limitations** : L’une des limites de ce genre d’intégration est le **flash de contenu** potentiel ou l’attente du bundle. Si un composant React doit remplacer du contenu existant, l’utilisateur pourrait voir ce contenu statique puis son remplacement. Pour minimiser cela, on peut soit essayer de **styler le contenu statique comme le final**, soit afficher un spinner/squelette à l’emplacement en attendant la montée du composant. Par ailleurs, plus il y a de composants React sur une page, plus le poids du bundle initial peut augmenter (même si on code-split, il y a le runtime React commun ~30kB gzip + chaque composant asynchrone). Il faut donc trouver un juste équilibre et éventuellement regrouper certains composants liés ensemble dans un même chunk pour éviter de multiplier les petits fetchs de code.

En pratique, les **solutions modernes** pour injecter des fragments React sans surcharger la page passent par l’optimisation du bundler et une utilisation judicieuse de React. Nous en avons déjà cité plusieurs : _lazy loading_, _code splitting_, multiple entrées Vite par page, utilisation d’attributs data pour rendre le bootstrap JS plus intelligent. On peut également mentionner des approches plus expérimentales comme **Astro** ou **Qwik** qui implémentent le concept d’îlots et de résumabilité, mais celles-ci nécessitent de sortir du cadre Django. Pour Gardel, une solution pragmatique est celle que nous avons décrite : Django génère le squelette HTML, et les composants React sont intégrés en douceur, de façon **progressive** et ciblée, sans chercher à tout rendre universellement en double. L’important est de **veiller aux performances** : tester les pages sur des navigateurs modestes, voir si le chargement du JS n’empêche pas l’interactivité initiale de la page (utiliser par ex. `defer` sur les scripts ou les charger en fin de body comme dans l’exemple avec `{% addtoblock "js" %}`). De plus, grâce à l’invalidation de cache avec le manifest, les fichiers ne seront téléchargés qu’une fois puis mis en cache par le navigateur.

En résumé, les limitations inhérentes à cette intégration (pas de SSR React natif, hydratation manuelle, dépendance au JS pour ces features) se contournent par une **bonne stratégie d’amélioration progressive**. Là où SEO ou no-JS sont critiques, on fournira une solution de repli serveur. Là où la performance compte, on fragmentera le JS et on ne l’injectera que si nécessaire. Cette approche vise à tirer le meilleur des deux mondes sans alourdir inutilement Django.

## Guide de Démarrage : Django + React Modulaire avec Vite & Tailwind

Pour un développeur Django qui souhaite intégrer React de manière modulaire dans un projet existant, voici un guide pas-à-pas pour bien démarrer, en adoptant Vite et Tailwind CSS :

**1. Installer et initialiser le projet React** – Dans le répertoire du projet Django, créer un dossier pour le frontend (par ex. `frontend/` à la racine du projet). Naviguez dans ce dossier et initialisez un projet Vite + React :

```bash
npm create vite@latest frontend-react -- --template react-ts

```

Ceci crée un template React TypeScript. Vous pouvez aussi configurer manuellement Vite dans un dossier existant. Assurez-vous d’avoir **@vitejs/plugin-react** installé pour la prise en charge de React et JSX/TSX.

**2. Configurer Vite pour Django** – Ouvrez le fichier `vite.config.ts` généré et ajustez les options de build :

- Définissez `base: "/static/"` (en supposant que `STATIC_URL = '/static/'` dans Django). Ainsi, Vite saura générer des chemins relatifs corrects pour les assets.
- Définissez `build.outDir` vers un dossier accessible par Django pour les fichiers compilés, par ex. `../static/frontend` (ou un chemin dans `STATICFILES_DIRS`). On peut choisir `outDir: "dist"` puis configurer Django pour lire `frontend/dist`.
- Activez `build.manifest: true` pour obtenir un fichier manifest.json.
- Spécifiez les entrées. Si vous n’avez qu’un seul point d’entrée (ex: `main.tsx`), Vite le prendra par défaut. Pour plusieurs entrées, utiliser `rollupOptions.input` pour lister par nom vos fichiers principaux (ex: `{ dashboard: "./src/dashboard.tsx", formulaire: "./src/formulaire.tsx" }`). Chaque entrée produira un bundle séparé.
- Optionnellement, incluez le plugin de manifest Django si vous en utilisez un (il existe par ex. un plugin custom dans certains tutos, mais on peut s’en passer avec django-vite).

Exemple simplifié de configuration :

```tsx
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/static/',
  plugins: [react()],
  build: {
    outDir: 'dist',
    manifest: true,
    rollupOptions: {
      input: {
        main: './src/main.tsx'
      }
    }
  }
});

```

**3. Installer et configurer Tailwind CSS** – Depuis le dossier frontend, installez Tailwind et ses dépendances :

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p   # génère tailwind.config.js et postcss.config.js

```

Dans `tailwind.config.js`, configurez le _content_ pour qu’il pointe sur **vos fichiers React** et **vos templates Django**. Par exemple :

```jsx
content: [
  "./index.html",
  "./src/**/*.{js,jsx,ts,tsx}",
  "../templates/**/*.html"
],

```

Cela permet à Tailwind de purger les classes non utilisées en production en scannant ces emplacements. Adaptez le chemin des templates selon votre structure (ici on suppose que `templates/` Django est adjacent au dossier frontend). Vous pouvez personnaliser le thème (couleurs, etc.) à ce stade si nécessaire.

Dans `postcss.config.js`, assurez-vous que Tailwind et autoprefixer sont bien inclus (le template `-p` l’a fait normalement). Dans votre code, créez un fichier CSS principal (ex: `src/index.css`) où vous importez les directives Tailwind de base :

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

```

Importez ce fichier `index.css` dans votre point d’entrée React (par ex, dans `main.tsx`), afin que Tailwind soit appliqué.

**4. Préparer le point d’entrée React** – Le fichier `main.tsx` (ou `index.tsx`) va initialiser vos composants. Comme discuté, on peut adopter le pattern du _data-react-component_. Vous pouvez coder quelque chose comme suit :

```tsx
import { createRoot } from 'react-dom/client';
import componentMap from './components/componentMap';  // un mapping nom -> composant React

const elements = document.querySelectorAll('[data-react-component]');
elements.forEach(el => {
  const name = el.getAttribute('data-react-component');
  const Component = componentMap[name];
  if (Component) {
    const propsData = el.getAttribute('data-react-props');
    const props = propsData ? JSON.parse(propsData) : {};
    createRoot(el).render(<Component {...props} />);
  }
});

```

Dans cet exemple, on suppose que vous avez un `componentMap.ts` qui exporte un objet associant un nom de composant (string) à l’import du composant réel. On peut utiliser `React.lazy` pour importer les composants de manière asynchrone (lazy loading), ce qui est recommandé pour que le bundle initial reste léger et que chaque composant devienne un chunk séparé. Notez qu’il faudra alors englober le rendu dans un `<Suspense>` éventuellement pour gérer l’attente de chargement.

Alternativement, pour un démarrage plus simple, si vous n’avez qu’un ou deux points de montage, vous pouvez explicitement cibler un ID. Par exemple :

```tsx
import MyWidget from './components/MyWidget';
const container = document.getElementById('my-widget-container');
if (container) {
  createRoot(container).render(<MyWidget />);
}

```

Mais la méthode data-attribute est plus évolutive pour de multiples composants et permet de passer des props facilement via le HTML.

**5. Configurer Django** – Côté Django, il faut maintenant indiquer où sont les fichiers statiques et les templates du frontend :

- Dans **[settings.py](http://settings.py)**, ajoutez le chemin du build Vite aux `STATICFILES_DIRS`. Si vous avez mis `outDir: "dist"`, et que ce dossier se trouve dans `frontend/dist`, faites :

```python
STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "dist",   # inclure les fichiers de build de Vite
    # ... autres dossiers static éventuels
]

```

Ainsi, `collectstatic` prendra en compte les fichiers générés.

- Toujours dans settings, vous pouvez ajouter le dossier des templates React si vous en avez (par ex, dans l’exemple Medium ils génèrent un `scripts.html` dans `react-components/templates`). Mais ce n’est pas obligatoire : vous pouvez tout aussi bien inclure directement les tags dans les templates Django existants.
- Si vous utilisez **django-vite** (installable via pip), configurez-le :

Dans vos templates de base, chargez les tags `{% load django_vite %}` puis utilisez `{% vite_asset 'main.tsx' %}` ou autre, comme indiqué dans la doc. En dev, cela inclura le script depuis le dev server avec HMR, en prod, cela lira le manifest et inclura les `<script>` et `<link>` appropriés.

````
```python
INSTALLED_APPS = [..., 'django_vite']
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend" / "dist"
DJANGO_VITE_DEV_MODE = DEBUG  # pour qu’en mode DEBUG on utilise le dev server

```
````

**6. Inclure les scripts et styles dans le template Django** – Ouvrez par exemple votre `base.html` (template parent commun). Dans le `<head>`, incluez la CSS compilée et le JS du frontend. Si vous utilisez django-vite, cela se résume à :

```
{% load django_vite %}
<!DOCTYPE html>
<html lang="en">
<head>
  ...
  {% vite_asset 'main.tsx' %}
  {% vite_hmr_client %}
  {% vite_react_refresh %}
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>

```

Ici, on suppose un seul entry point `main.tsx` qui gère tous les composants. La balise `{% vite_hmr_client %}` injecte le client HMR en dev, et `{% vite_react_refresh %}` ajoute le support Fast Refresh pour React en dev – ces deux-là ne sortent rien en production. Si vous n’utilisez pas django-vite, vous pouvez à la place inclure manuellement les tags générés. Par exemple, après un build, ouvrez le `manifest.json` pour trouver le nom du fichier principal (ex: `main.abcdef.js`) et son éventuel CSS. Puis dans `base.html` :

```
{% load static %}
<link rel="stylesheet" href="{% static 'main.abcdef.css' %}" />
<script type="module" src="{% static 'main.abcdef.js' %}"></script>

```

C’est moins automatique mais fonctionnel (il faudrait mettre à jour ces noms après chaque build, d’où l’intérêt de l’automatisation via un include ou django-vite).

**7. Insérer un composant React dans une page** – Dans un template Django où vous voulez ajouter de l’interactivité, utilisez le conteneur prévu. Par exemple, dans `ma_page.html` :

```
{% extends "base.html" %}
{% load static django_vite react_tags %}
{% block content %}
  <h1>Données de capteurs</h1>
  <p>Voici un aperçu des mesures :</p>
  {% RC "ChartComponent" data=mesures_json %}
{% endblock %}

```

Ici on utilise le templatetag custom `{% RC %}` provenant d’une librairie de tags `react_tags` (à créer) qui insère la `<div>` avec les bons data-attributes. Par exemple, `react_tags.py` pourrait contenir :

```python
@register.simple_tag
def RC(component_name, **props):
    props_json = json.dumps(props)
    return mark_safe(f"<div data-react-component='{component_name}' data-react-props='{props_json}'></div>")

```

Ainsi `{% RC "ChartComponent" data=mesures_json %}` produira `<div data-react-component="ChartComponent" data-react-props="{\\"data\\": [...]}"></div>`. Notre script React le détectera et montera le composant `ChartComponent` en lui passant la prop `data` (contenant les mesures). Dans cet exemple, `mesures_json` serait une variable de contexte Django contenant les données sous forme de JSON (on peut utiliser `|json_script` ou `json.dumps` dans la vue pour l’obtenir).

Si on ne veut pas créer de templatetag, on peut écrire le HTML à la main dans le template Django :

```
<div id="chart1" data-react-component="ChartComponent" data-react-props='{{ mesures_json|safe }}'></div>

```

(en s’assurant que `mesures_json` est déjà une chaîne JSON échappée correctement). L’utilisation d’un templatetag _safe_ simplifie en évitant les problèmes d’échappement.

**8. Lancer en développement** – Démarrez le serveur Django : `python manage.py runserver`. Puis, dans un autre terminal, lancez Vite en mode dev : `npm run dev` (dans le dossier frontend). Grâce à django-vite ou à vos inclusions, le template va charger le script depuis le dev server (généralement `http://localhost:5173`) au lieu du fichier statique. Vous devriez voir vos composants React se charger sur la page. Modifiez un composant React, la HMR de Vite devrait mettre à jour la page sans rechargement complet. C’est un gros avantage de Vite : un cycle de développement très rapide. Si HMR ne fonctionne pas, vérifiez que `{% vite_hmr_client %}` est bien présent et que `DJANGO_VITE_DEV_MODE` est True.

**9. Construire pour la production** – Lorsque vous êtes prêt à déployer, générez le build optimisé : `npm run build`. Ceci produit le dossier `dist` avec les fichiers minifiés et hashés, et le manifest.json. Exécutez ensuite `collectstatic` pour rassembler les fichiers statiques (si vous utilisez whitenoise ou un serveur web). Django servira alors les fichiers statiques compilés. Vos templates, grâce aux templatetags, pointeront automatiquement vers les bons noms de fichiers. Par exemple, django-vite lit le manifest et insère le `<script>` adéquat avec son hash. Vérifiez en prod que tout fonctionne : les composants devraient se monter de la même manière (il peut être utile de tester sans le dev server, en mettant `DJANGO_VITE_DEV_MODE=False` en local).

**10. Convention et next steps** – Vous avez maintenant un setup de base fonctionnel. À partir de là, vous pouvez étoffer votre projet : ajouter d’autres composants React de manière progressive sur d’autres pages Django en répétant la méthode (mettre un `<div data-react-component="X">` + passer les données nécessaires). Si les composants ont besoin d’appeler l’API, configurez par exemple Axios ou utilisez fetch directement, ou mieux intégrez React Query/SWR comme discuté plus haut. N’oubliez pas d’intégrer la gestion d’authentification (ex: en envoyant le token CSRF via les fetch, ou utiliser les cookies HttpOnly). Pour Tailwind, exploitez les plugins si besoin (forms, typography, etc.) pour styler les éléments générés par Django (par ex. le plugin `@tailwindcss/forms` pour harmoniser les champs de formulaire par défaut).

En termes de conventions, définissez dès le départ le style de code (par ex. fonction fléchée pour les composants, ou fonction nommée, etc.), et comment les composants React interagissent avec Django. Par exemple, si un composant doit envoyer des données à Django, va-t-il appeler directement une API REST ou soumettre un `<form>` invisible ? Ces choix doivent être cohérents à travers le projet. Souvent, le plus simple est de créer des **endpoints API JSON** dans Django (via Django REST Framework ou des vues JSON) que les composants React consomment via fetch. Cela sépare bien les responsabilités : Django d’un côté rend la page initiale + fournit des API, React de l’autre gère l’UX dynamique.

Enfin, documentez pour l’équipe la façon d’ajouter un nouveau composant React sur une page Django (comme nous venons de le faire). Vous pouvez par exemple créer un composant minimal "HelloReact" pour démontrer l’intégration, ce qui servira de modèle aux autres développeurs.

## Conclusion

Intégrer React dans un projet Django multi-pages en 2025 permet de bénéficier du meilleur des deux mondes : la robustesse et le SEO du rendu serveur, combinés à la richesse interactive de React pour des composants spécifiques. Les meilleures pratiques mises en avant – architecture modulaire, utilisation de Vite pour un bundling efficace, Tailwind CSS pour un design cohérent, librairies modernes pour l’état (Zustand/Jotai) et les data fetch (React Query/SWR), attention portée à l’accessibilité et à la maintenabilité – visent à garantir un développement **fluide, évolutif et performant**. Gardel, en adoptant ces recommandations, pourra enrichir son interface utilisateur tout en conservant la fiabilité de sa base Django. En suivant le guide de démarrage fourni, un développeur peut rapidement mettre en place l’infrastructure nécessaire et commencer à coder des composants React modulaires intégrés dans Django, ouvrant la voie à une application **plus dynamique** sans sacrifier les acquis du serveur. Bonne programmation !

**Sources :** Les informations et conseils ci-dessus s’appuient sur des retours d’expérience et ressources récentes, notamment sur l’intégration de Vite avec Django, l’utilisation de Tailwind CSS et de composants headless, le comparatif des outils de gestion d’état, les recommandations pour React Query vs SWR, l’organisation multi-applications React dans Django, ainsi que sur les discussions autour de l’amélioration progressive avec React. Ces sources soulignent l’importance d’une approche progressive, performante et bien structurée pour intégrer React dans un contexte Django en 2025, et ont été librement adaptées en français dans ce rapport.