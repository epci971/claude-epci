# EPCT Workflow — Detail des phases

> Reference pour `/quick` — Phases detaillees du workflow EPCT

---

## [E] EXPLORE Phase (5-10s)

**Modele:** Haiku (TINY et SMALL)

**Objectif:** Collecte rapide du contexte et verification de la complexite.

### Processus

1. **Reception du Brief** depuis `/brief`
   - Extraire: fichiers cibles, stack detectee, mode, criteres d'acceptation
   - SI brief absent → Suggerer `/brief` d'abord

2. **Scan Rapide** (SMALL uniquement)
   - Invoquer @Explore (Haiku) via Task tool:
     ```
     Task tool avec subagent_type="Explore", model="haiku"
     Focus: Identification fichiers, detection patterns
     Ignorer: Analyse approfondie (reporter a l'implementation)
     ```

3. **Verification Ambiguite** (SMALL+ uniquement)
   - SI ambiguite detectee → Invoquer @clarifier (Haiku)
   - Maximum 1-2 questions de clarification

4. **Garde-fou Complexite**
   - SI complexite > SMALL detectee → Escalader vers `/epci`
   ```
   ⚠️ **ESCALADE REQUISE**

   Complexite depasse le seuil SMALL:
   - [Raison: ex., >3 fichiers, tests integration necessaires]

   → Basculement vers `/epci` pour workflow structure.
   ```

### Sortie (Interne)
- Mode confirme (TINY/SMALL)
- Liste des fichiers cibles
- Stack/patterns detectes
- Pret pour phase Plan

---

## [P] PLAN Phase (10-15s)

**Modele:** Haiku (TINY) | Sonnet + `think` (SMALL)

**Objectif:** Generer un decoupage atomique des taches.

### Processus

1. **Generation des Taches**
   - TINY: 1-2 taches maximum
   - SMALL: 3-5 taches atomiques (2-10 min chacune)

2. **Planification Complexe** (SMALL+ uniquement)
   - SI proche limite SMALL → Invoquer @planner (Sonnet):
     ```
     Task tool avec subagent_type="epci:planner", model="sonnet"
     Entree: Brief + fichiers identifies
     Sortie: Liste ordonnee de taches avec dependances
     ```

3. **Initialisation Session**
   - Creer fichier session: `.project-memory/sessions/quick-{timestamp}.json`
   - Enregistrer: timestamp, description, complexite, taches du plan

### Breakpoint Leger (SI --confirm)

**⚠️ SI `--confirm` actif, afficher ce breakpoint et attendre validation.**

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 PLAN: {N} taches | ~{LOC} LOC | {FILE_COUNT} fichier(s)          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [1] {Description tache 1}                                          │
│ [2] {Description tache 2}                                          │
│ [3] {Description tache 3}                                          │
│                                                                     │
│ Entree=continuer, M=modifier, Echap=annuler                        │
└─────────────────────────────────────────────────────────────────────┘
```

**Comportement:**
- **Defaut (pas de --confirm):** Pas de breakpoint, continuer directement
- **Flag `--confirm`:** Afficher breakpoint, attendre input utilisateur
- **Entree pressee:** Continuer vers phase Code
- **M pressee:** Modifier le plan
- **Echap pressee:** Annuler le workflow

---

## [C] CODE Phase (variable)

**Modele:** Haiku (TINY) | Sonnet (SMALL)

**Objectif:** Executer les taches d'implementation.

### Processus

1. **Execution des Taches**
   - TINY: Implementation directe (pas de subagent)
   - SMALL: Invoquer @implementer (Sonnet):
     ```
     Task tool avec subagent_type="epci:implementer", model="sonnet"
     Entree: Une tache du plan
     Sortie: Code implemente
     ```

2. **Pour Chaque Tache:**
   ```
   a. Lire le fichier cible
   b. Appliquer le changement (outil Edit)
   c. Micro-validation (verification syntaxe)
   d. Marquer la tache complete dans la session
   ```

3. **Auto-Correction**
   - Executer lint/format sur les fichiers modifies
   - Appliquer les corrections automatiques

4. **Gestion des Erreurs**
   - SI erreur: Activer mode `think`
   - Reessayer avec meme modele (max 1x)
   - SI echec persistant: Escalader modele (Haiku→Sonnet, Sonnet→Opus)
   - Apres 2 reessais: Arreter et demander intervention

   ```
   ⚠️ **IMPLEMENTATION BLOQUEE**

   Erreur persistante apres 2 reessais:
   - [Description erreur]

   Veuillez examiner et fournir des indications.
   ```

### Sortie (Interne)
- Liste des fichiers modifies
- Changements LOC (+/-)
- Erreurs rencontrees (si applicable)

---

## [T] TEST Phase (5-10s)

**Modele:** Haiku (validation) | Sonnet + `think hard` (si correction necessaire)

**Objectif:** Verifier la correction de l'implementation.

### Processus

1. **Executer les Tests Existants**
   ```bash
   # Detecter le runner de tests et executer
   npm test / pytest / php bin/phpunit / etc.
   ```

2. **Verification Lint/Format**
   ```bash
   # Executer le linter du projet
   eslint / flake8 / phpcs / etc.
   ```

3. **Verification Coherence**
   - Verifier que les imports sont valides
   - Confirmer absence d'erreurs de syntaxe
   - Confirmer que les changements correspondent aux criteres d'acceptation

4. **En Cas d'Echec Tests:**
   - Activer mode `think hard`
   - Tenter auto-correction (modele Sonnet)
   - SI correction echoue → Rapporter et arreter

### Sortie (Interne)
- Resultats tests (nombre pass/fail)
- Statut lint (propre/problemes)
- Pret pour resume final

---

## Mode Plan Natif (Fast Path)

Quand `/quick` recoit un argument `@docs/plans/...` ou un fichier avec frontmatter `saved_at`:

### Comportement

| Phase | Standard | Plan Natif |
|-------|----------|------------|
| [PRE] | Non applicable | Detection + extraction taches |
| [E] | Execute | **SKIP** |
| [P] | Execute | **SKIP** |
| [C] | Taches de [P] | Taches du plan |
| [T] | Execute | Execute |

### Pourquoi SMALL par defaut ?

Un plan natif implique que:
1. L'utilisateur a pris le temps de planifier
2. La feature a une complexite minimale necessitant un plan
3. TINY serait trop limite pour un plan formalise

→ Donc: Utiliser Sonnet (SMALL) pour garantir la qualite d'execution.

### Extraction des taches

Le systeme supporte plusieurs formats:
- Checkboxes: `- [ ] Task description`
- Listes numerotees: `1. Task description`
- Headers: `## Task 1: Description`
- Bullets sous section "Tasks:" ou "Plan:"

Si aucun format detecte → Fallback: une tache unique basee sur le titre.

### Detection automatique

```python
def is_native_plan(file_path):
    # Critere 1: Chemin dans docs/plans/
    if "docs/plans/" in file_path:
        return True
    # Critere 2: Frontmatter avec saved_at
    frontmatter = parse_yaml_frontmatter(read_file(file_path))
    if frontmatter and "saved_at" in frontmatter:
        return True
    return False
```

---

## Session Persistence

**Emplacement:** `.project-memory/sessions/quick-{timestamp}.json`

**Schema:**
```json
{
  "timestamp": "2025-12-31T14:30:22Z",
  "description": "correction typo dans README",
  "complexity": "TINY",
  "plan": [
    {"task": "Corriger typo ligne 42", "status": "completed"}
  ],
  "files_modified": ["README.md"],
  "duration_seconds": 45,
  "models_used": {
    "explore": "haiku",
    "plan": "haiku",
    "code": "haiku",
    "test": "haiku"
  },
  "retries": 0,
  "flags": ["--autonomous"]
}
```

**Gestion Session:**
- Creee au debut de la phase Plan
- Mise a jour apres chaque phase completee
- Permet la reprise si workflow interrompu
- Utilisee pour calibration des metriques

---

*Reference EPCT Workflow — /quick command*
