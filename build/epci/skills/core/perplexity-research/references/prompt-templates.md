# Prompt Templates — Perplexity Research

> Templates de prompts optimisés pour Perplexity Pro par catégorie de recherche.

---

## Structure Générale

Tous les prompts suivent cette structure pour maximiser la qualité des résultats Perplexity :

```
[Contexte]: {domaine technique et situation}
[Question]: {question précise et ciblée}
[Contraintes]: {stack, versions, limitations}
[Format attendu]: {type de réponse souhaité}
```

---

## Template: library_unknown

**Usage :** Package/librairie non documenté dans Context7

```markdown
[Contexte]: Je travaille sur un projet {stack} et j'ai besoin d'intégrer {library_name} (version {version}).

[Question]: Quelles sont les best practices pour intégrer {library_name} dans une application {framework} ? Notamment :
- Configuration initiale recommandée
- Patterns d'utilisation courants
- Pièges à éviter
- Exemples de code concrets

[Contraintes]:
- Stack: {detected_stack}
- Version: {library_version}
- Environnement: {dev_environment}

[Format attendu]: Liste structurée avec exemples de code
```

**Variables :**
- `{library_name}` : Nom du package (ex: "@tanstack/query")
- `{version}` : Version détectée
- `{stack}` : Stack technique (ex: "React 18 + TypeScript")
- `{framework}` : Framework principal
- `{detected_stack}` : Stack complet détecté par @Explore
- `{dev_environment}` : Environnement (Node, browser, etc.)

---

## Template: bug_complex

**Usage :** Erreur rare ou complexe avec peu de résultats web

```markdown
[Erreur]: {error_message}

[Stack trace] (si disponible):
```
{stack_trace}
```

[Contexte]:
- Framework: {framework} {framework_version}
- Environnement: {environment}
- Fréquence: {frequency}
- Derniers changements: {recent_changes}

[Question]: Quelles sont les causes possibles de cette erreur et les solutions recommandées ? J'ai besoin de :
1. Les root causes les plus probables (classées par probabilité)
2. Les solutions pour chaque cause
3. Comment diagnostiquer laquelle s'applique à mon cas

[Format attendu]: Liste classée par probabilité avec solutions détaillées
```

**Variables :**
- `{error_message}` : Message d'erreur complet
- `{stack_trace}` : Stack trace si disponible
- `{framework}` : Framework (ex: "Next.js")
- `{framework_version}` : Version (ex: "14.2.0")
- `{environment}` : OS, Node version, etc.
- `{frequency}` : Always / Sometimes / Rare
- `{recent_changes}` : Changements récents potentiellement liés

---

## Template: architecture

**Usage :** Décisions architecturales, patterns distribués

```markdown
[Contexte]: Je conçois l'architecture pour {project_description}.

[Besoins]:
- {requirement_1}
- {requirement_2}
- {requirement_3}

[Contraintes]:
- Scale attendu: {scale}
- Budget infrastructure: {budget_level}
- Équipe: {team_size} développeurs
- Stack existant: {existing_stack}

[Question]: Quelle architecture recommandez-vous ? Comparez les options principales avec leurs trade-offs :
- Performance
- Scalabilité
- Complexité d'implémentation
- Coût opérationnel
- Maintenabilité

[Format attendu]: Tableau comparatif avec recommandation finale et justification
```

**Variables :**
- `{project_description}` : Description du projet/feature
- `{requirement_N}` : Besoins fonctionnels/non-fonctionnels
- `{scale}` : Ex: "1000 users", "100K requests/day"
- `{budget_level}` : Low / Medium / High
- `{team_size}` : Taille de l'équipe
- `{existing_stack}` : Technologies déjà en place

---

## Template: best_practices

**Usage :** Framework récent, nouvelles conventions

```markdown
[Framework]: {framework} {version}

[Contexte]: Je travaille sur {feature_description} dans un projet {project_type}.

[Question]: Quelles sont les best practices actuelles (2024-2025) pour {topic} avec {framework} {version} ?

Points spécifiques :
- Patterns recommandés vs patterns dépréciés
- Configuration optimale
- Erreurs courantes à éviter
- Évolutions récentes par rapport aux versions précédentes

[Contraintes]:
- TypeScript: {typescript_version} (si applicable)
- Autres dépendances: {dependencies}

[Format attendu]: Checklist avec exemples de code pour chaque point
```

**Variables :**
- `{framework}` : Nom du framework
- `{version}` : Version spécifique
- `{feature_description}` : Ce que vous construisez
- `{project_type}` : Type de projet (SaaS, e-commerce, etc.)
- `{topic}` : Sujet spécifique (authentication, state management, etc.)
- `{typescript_version}` : Version TypeScript si utilisé
- `{dependencies}` : Dépendances clés

---

## Template: market

**Usage :** Analyse concurrentielle, solutions existantes

```markdown
[Domaine]: {domain}

[Contexte]: Je développe {product_description} et j'ai besoin d'analyser le marché existant.

[Question]: Quelles sont les solutions existantes pour {domain} ? Pour chaque solution :
1. Fonctionnalités principales
2. Pricing model
3. Points forts / Points faibles
4. Stack technique (si connu)
5. Type de clients cibles

[Critères de comparaison]:
- {criterion_1}
- {criterion_2}
- {criterion_3}

[Format attendu]: Tableau comparatif des 5-7 solutions principales avec analyse des gaps et opportunités
```

**Variables :**
- `{domain}` : Domaine fonctionnel (ex: "notifications temps réel")
- `{product_description}` : Description du produit à développer
- `{criterion_N}` : Critères importants pour la comparaison

---

## Template: targeted

**Usage :** Recherche ciblée sur axe EMS faible en brainstorm

```markdown
[Contexte]: {brainstorm_context}

[Axe à améliorer]: {weak_axis}
Score actuel: {axis_score}/100

[Ce qui a déjà été couvert]:
- {covered_1}
- {covered_2}

[Question]: Comment puis-je améliorer l'axe "{weak_axis}" pour cette feature ? Donnez-moi :
{axis_specific_questions}

[Contraintes]:
- Stack: {stack}
- Temps disponible: {time_budget}

[Format attendu]: Suggestions actionables avec niveau de priorité
```

**Variables par axe :**

| Axe | Questions spécifiques |
|-----|----------------------|
| **Clarté** | "- Définitions manquantes<br>- Ambiguïtés à lever<br>- Terminologie à préciser" |
| **Profondeur** | "- Détails techniques à approfondir<br>- Edge cases à considérer<br>- Implications non évidentes" |
| **Couverture** | "- Perspectives stakeholders manquantes<br>- Cas d'usage non couverts<br>- Scénarios edge case" |
| **Décisions** | "- Décisions à prendre<br>- Trade-offs à évaluer<br>- Options à considérer" |
| **Actionnabilité** | "- Patterns d'implémentation<br>- Tâches concrètes<br>- Critères de succès mesurables" |

---

## Examples Complets

### Example 1: library_unknown

```markdown
[Contexte]: Je travaille sur un projet React 18 + TypeScript et j'ai besoin d'intégrer @tanstack/query (version 5.0.0).

[Question]: Quelles sont les best practices pour intégrer @tanstack/query dans une application React ? Notamment :
- Configuration initiale recommandée
- Patterns d'utilisation courants
- Pièges à éviter
- Exemples de code concrets

[Contraintes]:
- Stack: React 18.2, TypeScript 5.3, Vite
- Version: @tanstack/query 5.0.0
- Environnement: Browser SPA

[Format attendu]: Liste structurée avec exemples de code
```

### Example 2: bug_complex

```markdown
[Erreur]: EPERM: operation not permitted, symlink 'C:\...' -> 'C:\...'

[Stack trace]:
```
Error: EPERM: operation not permitted, symlink
    at Object.symlinkSync (node:fs:1234:3)
    at createSymlink (node_modules/...
```

[Contexte]:
- Framework: Next.js 14.2.0
- Environnement: Windows 11 WSL2, Node 20.10
- Fréquence: Always (sur npm install)
- Derniers changements: Migration vers pnpm

[Question]: Quelles sont les causes possibles de cette erreur et les solutions recommandées ? J'ai besoin de :
1. Les root causes les plus probables (classées par probabilité)
2. Les solutions pour chaque cause
3. Comment diagnostiquer laquelle s'applique à mon cas

[Format attendu]: Liste classée par probabilité avec solutions détaillées
```

### Example 3: market

```markdown
[Domaine]: Notifications temps réel pour applications SaaS

[Contexte]: Je développe un système de notifications pour une plateforme SaaS B2B et j'ai besoin d'analyser le marché existant.

[Question]: Quelles sont les solutions existantes pour les notifications temps réel ? Pour chaque solution :
1. Fonctionnalités principales
2. Pricing model
3. Points forts / Points faibles
4. Stack technique (si connu)
5. Type de clients cibles

[Critères de comparaison]:
- Support multi-canal (push, email, in-app)
- Pricing par message vs pricing flat
- Self-hosted vs SaaS
- API developer experience

[Format attendu]: Tableau comparatif des 5-7 solutions principales avec analyse des gaps et opportunités
```

---

## Formatting Guidelines

### Pour Perplexity Standard

- Prompts concis (< 300 mots)
- Une question principale claire
- Format attendu simple

### Pour Perplexity Deep Research

- Prompts détaillés (300-500 mots)
- Contexte riche
- Multiple sous-questions
- Demande de synthèse/comparaison

---

## Tips for Better Results

1. **Spécifier les versions** : Toujours inclure versions exactes
2. **Être précis sur le format** : "Tableau", "Liste classée", "Checklist"
3. **Limiter le scope** : Une question principale, pas 10
4. **Donner du contexte** : Le "pourquoi" aide Perplexity à mieux répondre
5. **Exclure l'obsolète** : "Solutions 2024-2025" pour éviter vieux résultats
