# CDC Commande — /document

> **Version** : 1.0.0  
> **Date** : 2025-12-15  
> **Type** : Commande EPCI  
> **Skill associé** : `documentor`

---

## 1. Frontmatter

```yaml
---
description: >-
  Documentation generator for projects. Creates and maintains technical docs,
  user guides, README, and changelog. Analyzes source code to generate accurate,
  contextual documentation. Supports incremental updates with custom content preservation.
argument-hint: <target> [sub-argument] [--flags]
allowed-tools: [Read, Write, Glob, Grep, LS, Bash]
---
```

---

## 2. Overview

Commande principale pour générer et maintenir la documentation d'un projet.
Route toutes les requêtes vers le skill `documentor` qui gère la logique métier.

---

## 3. Usage

```bash
/document <target> [sub-argument] [flags]
```

| Élément | Description | Obligatoire |
|---------|-------------|-------------|
| `target` | Type de documentation à générer | ✅ Oui |
| `sub-argument` | Précision du scope (module, composant) | ❌ Non |
| `flags` | Options de comportement | ❌ Non |

---

## 4. Targets

| Target | Description | Fichier(s) généré(s) |
|--------|-------------|---------------------|
| `init` | Initialise la structure docs/ | `docs/`, `.documentor.yml` |
| `readme` | Documentation principale projet | `README.md` |
| `architecture` | Architecture technique | `docs/technical/architecture.md` |
| `api` | Documentation API/routes | `docs/technical/api/*.md` |
| `database` | Schéma base de données | `docs/technical/database.md` |
| `components` | Composants frontend | `docs/technical/components/*.md` |
| `guide` | Guides utilisateur/admin | `docs/guides/*.md` |
| `contributing` | Guide de contribution | `docs/contributing/CONTRIBUTING.md` |
| `changelog` | Historique des versions | `CHANGELOG.md` |
| `all` | Génération complète | Tous les fichiers |

---

## 5. Sous-arguments

| Target | Sous-argument | Exemple | Effet |
|--------|---------------|---------|-------|
| `api` | `[module]` | `/document api users` | Doc API module users uniquement |
| `api` | `--all` | `/document api --all` | Doc toutes les routes API |
| `components` | `[name]` | `/document components Button` | Doc composant Button |
| `components` | `--all` | `/document components --all` | Doc tous les composants |
| `guide` | `user` | `/document guide user` | Guide utilisateur |
| `guide` | `admin` | `/document guide admin` | Guide administrateur |
| `changelog` | `[version]` | `/document changelog 1.2.0` | Entrée version spécifique |

---

## 6. Flags

| Flag | Court | Effet |
|------|-------|-------|
| `--force` | `-f` | Regénère les blocs AUTO même si identiques |
| `--verbose` | `-v` | Affiche le détail des fichiers analysés |
| `--no-checkpoint` | `-y` | Skip le checkpoint, génère directement |

---

## 7. Routing

Tous les targets routent vers le même skill :

```
/document <any-target>
    │
    └──► Skill: documentor
         └──► Méthode selon target
```

---

## 8. Process

### 8.1 Validation des arguments

```
Si target manquant:
    → Erreur + liste des targets disponibles

Si target inconnu:
    → Erreur + suggestion (fuzzy match)

Si sub-argument invalide pour le target:
    → Erreur + sub-arguments valides pour ce target
```

### 8.2 Dispatch au skill

```
1. Valider arguments
2. Charger config .documentor.yml si présente
3. Invoquer skill `documentor` avec:
   - target
   - sub_argument (optionnel)
   - flags
   - config (optionnel)
4. Le skill gère le reste (analyse, checkpoint, génération)
```

---

## 9. Exemples

### Initialiser la documentation

```bash
> /document init

→ Invoque documentor
→ Crée structure docs/
→ Génère .documentor.yml interactif
→ Crée fichiers de base avec marqueurs

✅ Documentation initialisée

Fichiers créés:
- docs/.documentor.yml
- docs/technical/.gitkeep
- docs/guides/.gitkeep
- docs/contributing/.gitkeep

Prochaine étape: /document readme
```

### Générer le README

```bash
> /document readme

📍 Checkpoint — Génération README

Fichiers analysés:
- package.json (nom, version, scripts)
- composer.json (dépendances PHP)
- src/ (structure projet)

Fichier à générer:
- README.md (création)

Sections prévues:
- Présentation
- Prérequis
- Installation
- Configuration
- Usage
- Tests
- Contribution
- Licence

→ valider | modifier | annuler

> valider

✅ README.md généré (127 lignes)
```

### Documenter une API spécifique

```bash
> /document api users

📍 Checkpoint — Documentation API Users

Fichiers analysés:
- src/Controller/Api/UserController.php (8 endpoints)
- src/Entity/User.php (12 champs)
- src/DTO/UserRequest.php

Fichier à générer:
- docs/technical/api/users.md (création)

Endpoints détectés:
- GET    /api/users
- GET    /api/users/{id}
- POST   /api/users
- PUT    /api/users/{id}
- DELETE /api/users/{id}
- POST   /api/users/{id}/activate
- POST   /api/users/{id}/deactivate
- GET    /api/users/{id}/permissions

→ valider | modifier | annuler

> valider

✅ docs/technical/api/users.md généré (234 lignes)
```

### Mettre à jour avec contenu custom préservé

```bash
> /document api users

📍 Checkpoint — Documentation API Users

Fichier existant: docs/technical/api/users.md
- Dernière modification: 2025-12-10
- Sections AUTO: 5 (à regénérer)
- Sections CUSTOM: 2 (préservées)

Sections CUSTOM préservées:
- "Notes d'implémentation" (lignes 45-67)
- "Cas particuliers" (lignes 120-145)

Changements détectés:
- +1 endpoint: PATCH /api/users/{id}
- Modifié: POST /api/users (nouveau champ 'role')

→ valider | modifier | annuler

> valider

✅ docs/technical/api/users.md mis à jour
   - 5 sections regénérées
   - 2 sections custom préservées
   - +1 endpoint documenté
```

### Génération complète

```bash
> /document all

📍 Checkpoint — Génération complète

Projet: mon-application (Symfony 7 + React 18)

Fichiers à générer:
| Fichier | Action | Estimation |
|---------|--------|------------|
| README.md | Création | ~120 lignes |
| CHANGELOG.md | Création | ~30 lignes |
| docs/technical/architecture.md | Création | ~200 lignes |
| docs/technical/database.md | Création | ~150 lignes |
| docs/technical/api/users.md | Création | ~180 lignes |
| docs/technical/api/auth.md | Création | ~120 lignes |
| docs/technical/components/Button.md | Création | ~80 lignes |
| docs/guides/user-guide.md | Création | ~100 lignes |
| docs/contributing/CONTRIBUTING.md | Création | ~90 lignes |

Total: 9 fichiers, ~1070 lignes

⚠️ Génération complète peut prendre plusieurs minutes.

→ valider | modifier | annuler

> valider

Génération en cours...

✅ Documentation complète générée

Fichiers créés: 9
Lignes générées: 1047
Temps: 2m 34s
```

---

## 10. Erreurs courantes

### Target manquant

```
❌ Target manquant.

Usage: /document <target> [sub-argument] [flags]

Targets disponibles:
- init          Initialise la structure docs/
- readme        Documentation principale
- architecture  Architecture technique
- api           Documentation API
- database      Schéma base de données
- components    Composants frontend
- guide         Guides utilisateur
- contributing  Guide de contribution
- changelog     Historique versions
- all           Génération complète

Exemple: /document readme
```

### Target inconnu

```
❌ Target 'readme.md' inconnu.

Vouliez-vous dire: readme ?

Usage: /document readme
```

### Sub-argument invalide

```
❌ Sub-argument 'Button' invalide pour target 'api'.

Sub-arguments valides pour 'api':
- [module]  Nom du module (ex: users, auth, products)
- --all     Toutes les routes API

Exemple: /document api users
```

### Pas de structure docs/

```
⚠️ Structure docs/ non trouvée.

Initialisez d'abord avec:
/document init

Ou créez manuellement:
mkdir -p docs/technical docs/guides docs/contributing
```

---

## 11. Output standard

### Succès

```
✅ **DOCUMENTATION GÉNÉRÉE**

Target: [target]
Fichier: [chemin]
Action: [Création | Mise à jour]
Lignes: [nombre]

Sections:
- [section 1] ✅
- [section 2] ✅
- [section custom] 🔒 (préservée)

Prochaine étape suggérée:
→ /document [suggestion]
```

### Avec avertissements

```
⚠️ **DOCUMENTATION GÉNÉRÉE AVEC AVERTISSEMENTS**

Target: api
Fichier: docs/technical/api/users.md

Avertissements:
- 2 endpoints sans annotations détectés
- Schéma de réponse incomplet pour GET /users/{id}

Suggestion:
Ajoutez des annotations PHPDoc pour améliorer la documentation.
```

---

## 12. Configuration

La commande charge automatiquement `docs/.documentor.yml` si présent.

Voir skill `documentor` pour le schéma complet de configuration.

---

## 13. Skills chargés

| Skill | Rôle |
|-------|------|
| `documentor` | Logique métier, analyse, génération |

---

## 14. Voir aussi

- Skill `documentor` — Logique de génération
- `/document init` — Initialisation projet
- `docs/.documentor.yml` — Configuration

---

*CDC Commande — Pattern EPCI v1.0*
