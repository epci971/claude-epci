# Processus de Reformulation

> Logique de reformulation du brief (Step 1)

---

## Pré-étape: Clarification Input (Conditionnelle)

**Skill**: `input-clarifier`

Avant reformulation, vérifier si l'input nécessite clarification (artefacts vocaux détectés).

```
IF flag --no-clarify:
   → Ignorer clarification, procéder aux checks de reformulation

ELSE:
   → Calculer score clarté via skill input-clarifier
   → IF score < 0.6: Afficher prompt reformulation (depuis input-clarifier)
   → Utiliser input nettoyé pour reformulation suivante
```

> **Note**: Utilise le skill centralisé `input-clarifier` pour détection cohérente des artefacts.

---

## Conditions de SKIP (rares)

| Condition | Comment détecter | Action |
|-----------|------------------|--------|
| **Flag `--no-rephrase`** | Utilisateur a explicitement ignoré | SKIP — aller au Step 2 |
| **Brief déjà structuré** | Contient headers "## Objectif", "## Context", "## Critères" | SKIP — déjà depuis /brainstorm |

**Si condition SKIP rencontrée**: Afficher brief tel quel avec breakpoint validation, puis Step 2.

---

## Conditions de DÉCLENCHEMENT (si UNE est vraie → DOIT reformuler)

| Condition | Comment détecter |
|-----------|------------------|
| **Flag `--rephrase`** | Utilisateur a explicitement demandé |
| **Score clarté < 0.6** | Détecté par skill input-clarifier (artefacts vocaux, auto-corrections) |
| **Brief vague/incomplet** | < 30 mots ET contient termes vagues: `système`, `améliorer`, `ajouter`, `truc`, `chose`, `something` |
| **Pas de verbe d'action clair** | Manque: `implémenter`, `créer`, `ajouter`, `corriger`, `fixer`, `add`, `create`, `fix`, `implement` |

---

## ACTION: Processus de Reformulation

**Si déclenché, OBLIGATOIRE:**

### 1. Utiliser input nettoyé

Depuis input-clarifier (si clarification déclenchée):
- Artefacts déjà supprimés par le skill
- Auto-corrections déjà résolues

### 2. Détecter type de template

| Type | Keywords détectés |
|------|-------------------|
| **FEATURE** | `ajouter`, `créer`, `implémenter`, `nouveau`, `add`, `create` |
| **PROBLEM** | `bug`, `erreur`, `fixer`, `corriger`, `cassé`, `fix`, `broken` |
| **DECISION** | `choisir`, `quelle`, `comment`, `stratégie`, `which`, `how` |

### 3. Restructurer en format

```
**Objectif**: [Verbe action] + [quoi] + [but]
**Contexte**: [Domaine détecté] | [Compréhension initiale]
**Contraintes**: [Extraites du brief OU "À définir"]
**Critères de succès**: [Basés sur type template]
```
