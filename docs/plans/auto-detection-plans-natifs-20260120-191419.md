---
saved_at: "2026-01-20T19:14:19Z"
source: "~/.claude/plans/resilient-kindling-hanrahan.md"
slug: "auto-detection-plans-natifs"
original_filename: "resilient-kindling-hanrahan.md"
auto_detected: true
---

# Plan : Auto-Détection Plans Natifs (Sans Flag Explicite)

## Objectif

**Supprimer le flag `--from-native-plan`** et implémenter une détection automatique dans les 3 commandes :
- `/brief` — détecte et utilise comme contexte, route intelligemment
- `/epci` — détecte et intègre en §2 automatiquement
- `/quick` — détecte et utilise comme contexte pour phase [P]

**Principe** : Si le fichier passé est dans `docs/plans/`, c'est un plan natif → traitement automatique.

---

## Fichiers à modifier

| Fichier | Modification |
|---------|--------------|
| `src/commands/brief.md` | Step 0.5 (détection) + Step 6 (routing sans flag) |
| `src/commands/epci.md` | Supprimer flag + Step 0.5 auto-détection locale |
| `src/commands/quick.md` | Ajouter détection locale dans phase [E] |
| `src/commands/references/epci/native-plan-import.md` | Supprimer références au flag |
| `CLAUDE.md` | Mise à jour workflow (plus de flag) |

---

## Logique de détection (commune aux 3 commandes)

```python
def is_native_plan(file_path):
    """Détection automatique d'un plan natif sauvegardé."""
    # Critère 1: Chemin dans docs/plans/
    if "docs/plans/" in file_path:
        return True

    # Critère 2 (fallback): Frontmatter avec saved_at
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter and "saved_at" in frontmatter:
        return True

    return False

def extract_native_plan_metadata(file_path):
    """Extrait slug et contenu du plan natif."""
    content = read_file(file_path)
    frontmatter = parse_yaml_frontmatter(content)

    return {
        "slug": frontmatter.get("slug") or extract_slug_from_filename(file_path),
        "source": frontmatter.get("source", "unknown"),
        "content": content_after_frontmatter(content),
        "path": file_path
    }
```

---

## Implémentation par commande

### 1. `/brief` — Détection + Routing intelligent

**Fichier:** `src/commands/brief.md`

#### Step 0.5 — Détection Type Input (mise à jour)

```markdown
| Pattern | INPUT_TYPE | Traitement |
|---------|------------|------------|
| `docs/plans/*.md` | `native_plan` | Auto-détecté, extraire slug + contenu |
| `docs/briefs/*/*.md` | `brainstorm_output` | Workflow existant |
| Autre `.md` | `external_file` | Brief brut |
| Texte libre | `text` | Brief inline |

**SI fichier dans `docs/plans/` :**
1. `is_native_plan = true`
2. Extraire frontmatter (slug, source)
3. Stocker `native_plan_metadata` pour routing
4. Utiliser contenu du plan comme contexte pour @Explore
```

#### Step 6 — Routing (sans flag explicite)

```markdown
**SI INPUT_TYPE == "native_plan" :**

| Catégorie | Commande | Slug |
|-----------|----------|------|
| TINY | `/quick "{brief}" @{native_plan_path}` | Auto |
| SMALL | `/quick "{brief}" @{native_plan_path}` | Auto |
| STANDARD | `/epci {detected_slug} @{native_plan_path}` | Depuis metadata |
| LARGE | `/epci --large {detected_slug} @{native_plan_path}` | Depuis metadata |

**Note:** Le `@{path}` est passé comme argument de contexte, PAS comme flag.
Chaque commande cible fait sa propre détection locale.
```

---

### 2. `/epci` — Suppression flag + Détection locale

**Fichier:** `src/commands/epci.md`

#### Supprimer de argument-hint (ligne 6)

```yaml
# AVANT
argument-hint: "[--large] [--turbo] [--from-native-plan <file>] ..."

# APRÈS
argument-hint: "[--large] [--turbo] [--think|--think-hard|--ultrathink] ..."
```

#### Step 0.5 — Détection automatique (remplace condition flag)

```markdown
## Step 0.5: Détection Plan Natif (AUTO)

**Condition:** Argument de contexte `@<file>` fourni

1. Vérifier si `<file>` est dans `docs/plans/` OU a frontmatter `saved_at`
2. **SI plan natif détecté :**
   - Extraire slug depuis frontmatter ou filename
   - Extraire contenu du plan
   - Créer/mettre à jour Feature Document avec §2 "Plan Original (Natif)"
   - Vérifier §1 → lancer @Explore si manquant
3. **SINON :**
   - Traitement standard (fichier comme brief additionnel)

**Pas de flag nécessaire** — la détection est basée sur le chemin/frontmatter.
```

#### Supprimer documentation du flag

Supprimer la ligne du tableau des flags :
```markdown
| `--from-native-plan <file>` | ... |  ← SUPPRIMER
```

---

### 3. `/quick` — Ajouter détection locale

**Fichier:** `src/commands/quick.md`

#### Phase [E] EXPLORE — Ajouter détection

```markdown
### [E] EXPLORE Phase (5-10s)

**SI argument de contexte `@<file>` fourni :**
1. Vérifier si fichier est dans `docs/plans/` (auto-détection)
2. **SI plan natif :**
   - Extraire contenu comme contexte pour phase [P]
   - Stocker `native_plan_context` pour utilisation ultérieure
3. **SINON :**
   - Traiter comme contexte additionnel standard

**Suite normale :**
1. Collecter contexte via @Explore (quick mode)
2. Invoquer `@skill:complexity-calculator`
3. ...
```

#### Phase [P] PLAN — Utiliser contexte plan natif

```markdown
### [P] PLAN Phase (10-15s)

**SI `native_plan_context` existe :**
- Utiliser le plan natif comme base pour générer les tâches
- Affiner/adapter au contexte découvert en phase [E]
- Ne pas repartir de zéro

**SINON :**
- Génération standard des tâches
```

---

### 4. Mise à jour références

**Fichier:** `src/commands/references/epci/native-plan-import.md`

Renommer en `native-plan-detection.md` et mettre à jour :
- Supprimer toutes les références à `--from-native-plan`
- Documenter la détection automatique
- Exemples mis à jour

---

### 5. Mise à jour CLAUDE.md

**Section Workflow avec Plan Natif**

```markdown
### Workflow avec Plan Natif (v5.5.0+)

**Plus besoin de flag** — détection automatique basée sur `docs/plans/`.

\`\`\`bash
# 1. Créer plan en mode natif Claude Code
<mode plan natif>
# → ~/.claude/plans/random-name.md

# 2. Sauvegarder dans le projet
/save-plan
# → docs/plans/auth-oauth-20260120-143052.md

# 3. Utiliser directement (DÉTECTION AUTOMATIQUE)
/brief @docs/plans/auth-oauth-20260120-143052.md
# → Détecte plan natif automatiquement
# → Route vers /quick ou /epci avec contexte

# OU directement dans /epci
/epci auth-oauth @docs/plans/auth-oauth-20260120-143052.md
# → Détecte plan natif, intègre en §2

# OU directement dans /quick (si petit scope)
/quick "fix auth" @docs/plans/auth-oauth-20260120-143052.md
# → Utilise plan comme contexte pour phase [P]
\`\`\`
```

---

## Résumé des changements

| Commande | Avant | Après |
|----------|-------|-------|
| `/brief` | Ne gère pas les plans natifs | Détecte `docs/plans/`, route avec `@path` |
| `/epci` | Flag `--from-native-plan` requis | Détection auto via `@path` dans `docs/plans/` |
| `/quick` | Pas de support | Détection auto, utilise comme contexte [P] |

**Principe unifié :** Passage d'un fichier via `@<path>` + chemin dans `docs/plans/` = plan natif détecté automatiquement.

---

## Vérification

1. **Test détection `/brief`** :
   ```bash
   /brief @docs/plans/integration-perplexity-research-20260120-160914.md
   ```
   Attendu : détecte plan natif, route vers `/epci` avec contexte

2. **Test détection `/epci`** :
   ```bash
   /epci auth-feature @docs/plans/auth-20260120.md
   ```
   Attendu : détecte plan natif, intègre en §2 automatiquement

3. **Test détection `/quick`** :
   ```bash
   /quick "small fix" @docs/plans/fix-20260120.md
   ```
   Attendu : détecte plan natif, utilise comme contexte phase [P]

4. **Test rétrocompatibilité** :
   ```bash
   /epci feature-slug  # Sans @path → workflow standard
   /brief "texte"      # Sans @path → workflow standard
   ```

---

## Bump version

Après implémentation : `5.4.1` → `5.5.0` (changement de comportement majeur)

Fichiers à bumper :
- `CLAUDE.md` header
- `src/.claude-plugin/plugin.json`
- `build/epci/.claude-plugin/plugin.json`
