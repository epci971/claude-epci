---
description: >-
  Sauvegarde les plans natifs Claude Code depuis ~/.claude/plans/ vers le projet
  local docs/plans/. Auto-detecte le dernier plan ET genere un slug intelligent
  base sur le contexte. Zero configuration requise.
argument-hint: "[--source <file>] [--slug <name>] [--dry-run]"
allowed-tools: [Read, Write, Bash, Glob]
---

# EPCI Save-Plan — Plan Archiver

## Overview

Sauvegarde les plans natifs Claude Code dans le projet pour versioning et collaboration.

**Zero argument requis** - la commande fonctionne en tapant simplement `/save-plan`

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | None (simple command) |
| **Skills** | breakpoint-display |
| **Subagents** | None |

## Arguments (tous optionnels)

| Argument | Description |
|----------|-------------|
| `--source <file>` | Specifier un fichier plan different (override auto-detection) |
| `--slug <name>` | Forcer un slug specifique (override auto-generation) |
| `--dry-run` | Afficher ce qui serait fait sans sauvegarder |

## Output

- **Dossier**: `docs/plans/`
- **Format**: `<slug>-<YYYYMMDD-HHmmss>.md`
- **Exemple**: `docs/plans/auth-oauth-20260115-143052.md`

---

## Process

### Step 1: Determiner le fichier source

**Si `--source <file>` fourni:**
- Utiliser le fichier specifie
- Resoudre `~` vers `$HOME` si necessaire

**Sinon (auto-detection):**

Utiliser Glob pour lister les fichiers dans `~/.claude/plans/`:

```bash
ls -t ~/.claude/plans/*.md 2>/dev/null | head -1
```

**Si aucun fichier trouve:**

Afficher erreur et arreter:

```
+----------------------------------------------------------+
| ERROR                                                     |
+----------------------------------------------------------+
|                                                          |
| No plan files found in ~/.claude/plans/                  |
|                                                          |
| Create a plan using Claude Code's native planning mode   |
| first, then run /save-plan again.                        |
|                                                          |
+----------------------------------------------------------+
```

**STOP** - Ne pas continuer.

---

### Step 2: Lire le contenu source

Utiliser Read tool pour lire le fichier plan detecte.

Stocker:
- `source_path`: chemin complet du fichier source
- `source_content`: contenu du fichier
- `original_filename`: nom du fichier (basename)

**Si fichier vide:** Continuer avec warning (plan vide est valide).

**Si fichier introuvable:**

```
+----------------------------------------------------------+
| ERROR                                                     |
+----------------------------------------------------------+
|                                                          |
| Source file not found: {source_path}                     |
|                                                          |
| Check the path and try again.                            |
|                                                          |
+----------------------------------------------------------+
```

**STOP** - Ne pas continuer.

---

### Step 3: Generer le slug (auto-detection intelligente)

**Si `--slug <name>` fourni:**
- Utiliser le slug specifie directement
- Marquer `auto_detected: false` dans le frontmatter

**Sinon (auto-generation):**

Analyser le contenu du plan avec cet algorithme:

#### 3.1 Chercher un titre explicite

Scanner les 20 premieres lignes pour un pattern de titre:

```
/^#\s*(Plan|Feature|Implementation|Objectif):\s*(.+)/i
```

**Si trouve:** Extraire le texte apres le `:` et slugifier.

**Exemples:**
- `# Plan: Commande save-plan` → `commande-save-plan`
- `# Feature: Authentication OAuth` → `authentication-oauth`

#### 3.2 Chercher dans le contenu structure

Si pas de titre explicite, chercher une section `## Objectif`:

```markdown
## Objectif
Creer une nouvelle commande pour sauvegarder les plans
```

Extraire la premiere phrase et prendre les 4 premiers mots significatifs.

#### 3.3 Fallback: premiers mots significatifs

Si aucune structure trouvee:
1. Prendre les 500 premiers caracteres
2. Extraire les mots significatifs (filtrer stopwords)
3. Prendre les 3 premiers mots
4. Slugifier

#### Fonction slugify

```
1. Convertir en minuscules
2. Supprimer les accents (e→e, a→a, etc.)
3. Remplacer espaces par tirets
4. Supprimer caracteres non-alphanumeriques (sauf tirets)
5. Fusionner tirets multiples
6. Limiter a 50 caracteres max
```

#### Stopwords a filtrer

Francais: le, la, les, de, du, un, une, et, ou, pour, avec, dans, sur, qui, que, ce, cette, ces, son, sa, ses, leur, leurs, nous, vous, ils, elles, par, en, au, aux

Anglais: the, a, an, to, for, of, in, on, at, by, with, from, is, are, was, were, be, been, being, have, has, had, do, does, did, will, would, could, should, may, might, must, can

---

### Step 4: Breakpoint de confirmation

**OBLIGATOIRE** - Afficher le breakpoint via `@skill:breakpoint-display` et attendre confirmation.

**Skill**: `breakpoint-display`

```yaml
@skill:breakpoint-display
  type: validation
  title: "SAVE PLAN — Confirmation"
  data:
    source_detected: "{source_path}"
    slug_generated: "{slug}"
    destination: "docs/plans/{slug}-{timestamp}.md"
    auto_detected: {true|false}
  ask:
    question: "Souhaitez-vous sauvegarder ce plan ?"
    header: "💾 Save Plan"
    options:
      - {label: "Confirmer (Recommended)", description: "Sauvegarder le plan"}
      - {label: "Modifier slug", description: "Changer le slug généré"}
      - {label: "Annuler", description: "Ne pas sauvegarder"}
```

**Attendre la reponse utilisateur.**

**Si "Confirmer":** Continuer vers Step 5.

**Si "Modifier slug":** Demander le nouveau slug via AskUserQuestion, puis continuer.

**Si "Annuler":** Afficher message d'annulation et **STOP**.

**Si `--dry-run`:** Afficher ce qui serait fait (source, slug, destination, frontmatter) et **STOP**.

---

### Step 5: Generer et ecrire la sortie

#### 5.1 Creer le dossier si necessaire

```bash
mkdir -p docs/plans
```

#### 5.2 Generer le timestamp

Format: `YYYYMMDD-HHmmss`

Exemple: `20260115-143052`

#### 5.3 Construire le chemin de destination

```
docs/plans/{slug}-{timestamp}.md
```

#### 5.4 Construire le frontmatter

```yaml
---
saved_at: "2026-01-15T14:30:52Z"
source: "~/.claude/plans/graceful-noodling-dragonfly.md"
slug: "commande-save-plan"
original_filename: "graceful-noodling-dragonfly.md"
auto_detected: true
---
```

**Notes:**
- `saved_at`: Format ISO 8601 avec timezone Z (UTC)
- `source`: Garder le `~` pour lisibilite
- `auto_detected`: `true` si slug genere automatiquement, `false` si fourni via `--slug`

#### 5.5 Combiner et ecrire

Combiner frontmatter + contenu original:

```markdown
---
saved_at: "..."
source: "..."
slug: "..."
original_filename: "..."
auto_detected: true
---

[Contenu original du plan ici]
```

Utiliser Write tool pour creer le fichier.

---

### Step 6: Afficher le resume

```
+----------------------------------------------------------+
| PLAN SAVED                                                |
+----------------------------------------------------------+
|                                                          |
| Source: {source_path}                                    |
| Destination: {destination_path}                          |
|                                                          |
| Metadata added:                                           |
|   saved_at: {timestamp}                                  |
|   slug: {slug}                                           |
|   auto_detected: {true|false}                            |
|                                                          |
| Next steps:                                               |
|   /epci --from-native-plan {destination_path} --slug {slug} |
|                                                          |
+----------------------------------------------------------+
```

---

## Error Handling

| Erreur | Message | Action |
|--------|---------|--------|
| Aucun plan dans ~/.claude/plans/ | `No plan files found in ~/.claude/plans/` | Stop |
| Fichier source introuvable | `Source file not found: {path}` | Stop |
| Impossible de generer slug | `Could not auto-detect slug` | Demander via breakpoint |
| Dossier docs/plans/ non creatable | `Cannot create directory: docs/plans/` | Stop |
| Fichier destination non writable | `Cannot write to: {path}` | Stop |

---

## Examples

```bash
# Tout auto-detecte (cas le plus courant)
/save-plan

# Preview sans sauvegarder
/save-plan --dry-run

# Forcer un slug specifique
/save-plan --slug my-custom-feature

# Specifier un fichier source different
/save-plan --source ~/.claude/plans/specific-plan.md

# Combiner les deux
/save-plan --source ~/.claude/plans/old-plan.md --slug legacy-feature
```

---

## Integration with EPCI Workflow

```bash
# Workflow typique
<mode plan natif Claude Code>
# Genere ~/.claude/plans/random-name.md

/save-plan
# Auto-detecte + genere slug
# Breakpoint de confirmation
# Sauvegarde dans docs/plans/auth-oauth-20260115-143052.md

/epci --from-native-plan docs/plans/auth-oauth-20260115-143052.md --slug auth-oauth
# Utilise le plan sauvegarde pour implementation
```

---

## Technical Notes

- **Encoding:** UTF-8 pour supporter les caracteres speciaux
- **Line endings:** Preserver les line endings du fichier source
- **Permissions:** Le fichier cree herite des permissions par defaut du systeme
- **Collisions:** Le timestamp avec secondes (HHmmss) evite les collisions
