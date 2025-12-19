# Prompt d'Audit EPCI — Prêt pour Claude Code

> **Usage** : Copier le contenu entre les balises `--- DÉBUT ---` et `--- FIN ---` directement dans Claude Code

---

## --- DÉBUT DU PROMPT À COPIER ---

```markdown
# 🔍 MISSION : Audit Complet du Plugin EPCI

## Contexte

Tu es missionné pour effectuer un **audit exhaustif d'intégrité** du plugin EPCI. L'objectif est de vérifier que toutes les fonctionnalités documentées sont bien implémentées, fonctionnelles et conformes aux spécifications.

## Document de Référence

**Inventaire des fonctionnalités à auditer** :
→ Fichier : `epci-inventaire-fonctionnalites.md` (dans le projet ou fourni ci-après)

Cet inventaire contient ~255 fonctionnalités réparties en 10 catégories :
- 9 Commandes (86 fonctionnalités)
- 6 Subagents (35 fonctionnalités)
- 12 Skills Core (52 fonctionnalités)
- 4 Skills Stack (16 fonctionnalités)
- 4 Skills Factory (18 fonctionnalités)
- Système de Hooks (10 fonctionnalités)
- Project Memory (12 fonctionnalités)
- Système de Flags (4 fonctionnalités)
- 7 Scripts de validation
- Brainstormer (15 fonctionnalités à vérifier si implémentées)

## Méthodologie d'Audit

### Phase 1 — Audit Structurel
```
Pour chaque composant listé dans l'inventaire :
1. Vérifier l'existence du fichier
2. Valider le frontmatter YAML (description, allowed-tools, etc.)
3. Vérifier les références internes (skills, agents référencés existent)
4. Contrôler la structure attendue
```

### Phase 2 — Audit de Validation
```
Exécuter les scripts de validation :
1. python scripts/validate_all.py
2. python scripts/validate_skill.py (sur chaque skill)
3. python scripts/validate_command.py (sur chaque commande)
4. python scripts/validate_subagent.py (sur chaque agent)
5. python scripts/test_triggering.py
6. python hooks/runner.py --list
```

### Phase 3 — Audit Fonctionnel (Échantillonnage)
```
Tester les workflows critiques :
1. /epci-memory init (ou status si déjà initialisé)
2. /epci-learn status
3. Vérifier un hook actif
4. Valider la structure Project Memory
```

## Livrables Attendus

### Livrable Principal : Rapport d'Audit (CDC/Specs)

Génère un fichier **`docs/audits/AUDIT-EPCI-COMPLET-[DATE].md`** avec la structure suivante :

---

# Cahier des Charges — Audit d'Intégrité Plugin EPCI

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Document** | Rapport d'Audit EPCI |
| **Version** | 1.0 |
| **Date** | [DATE_AUDIT] |
| **Auditeur** | Claude Code |
| **Périmètre** | Plugin EPCI v3.x complet |
| **Référentiel** | epci-inventaire-fonctionnalites.md |

---

## 1. Résumé Exécutif

### 1.1 Verdict Global

**[✅ CONFORME | ⚠️ PARTIELLEMENT CONFORME | ❌ NON CONFORME]**

### 1.2 Indicateurs Clés

| Indicateur | Valeur | Cible | Status |
|------------|--------|-------|--------|
| Composants présents | X/Y | 100% | ✅/❌ |
| Validations passées | X/Y | 100% | ✅/❌ |
| Erreurs critiques | X | 0 | ✅/❌ |
| Warnings | X | <10 | ✅/❌ |
| Couverture fonctionnelle | X% | >90% | ✅/❌ |

### 1.3 Synthèse des Écarts

| Priorité | Nombre | Description |
|----------|--------|-------------|
| 🔴 Critique | X | Bloque le fonctionnement |
| 🟠 Majeur | X | Fonctionnalité dégradée |
| 🟡 Mineur | X | Amélioration possible |
| 🔵 Info | X | Observation |

---

## 2. Spécifications de Conformité

### 2.1 Commandes

#### 2.1.1 /epci-brief

| ID | Fonctionnalité | Spécification | Résultat | Écart |
|----|----------------|---------------|----------|-------|
| CMD-BRIEF-01 | Chargement Project Memory | Le skill project-memory-loader doit être invoqué | ✅/❌ | [Détail] |
| CMD-BRIEF-02 | Exploration @Explore | Subagent @Explore invoqué via Task tool | ✅/❌ | [Détail] |
| CMD-BRIEF-03 | Détection de stack | Stack technique identifié automatiquement | ✅/❌ | [Détail] |
| ... | ... | ... | ... | ... |

**Taux de conformité : X/11 (X%)**

#### 2.1.2 /epci

| ID | Fonctionnalité | Spécification | Résultat | Écart |
|----|----------------|---------------|----------|-------|
| CMD-EPCI-01 | Pré-workflow Memory | Contexte chargé avant Phase 1 | ✅/❌ | [Détail] |
| ... | ... | ... | ... | ... |

**Taux de conformité : X/26 (X%)**

[Répéter pour chaque commande : /epci-quick, /epci-spike, /epci-decompose, /epci-memory, /epci-learn, /epci:create]

---

### 2.2 Subagents

#### 2.2.1 @plan-validator

| ID | Fonctionnalité | Spécification | Résultat | Écart |
|----|----------------|---------------|----------|-------|
| AGT-PLAN-01 | Check Completeness | Vérifie stories, fichiers, tests, dépendances | ✅/❌ | [Détail] |
| ... | ... | ... | ... | ... |

**Taux de conformité : X/7 (X%)**

[Répéter pour : @code-reviewer, @security-auditor, @qa-reviewer, @doc-generator, @decompose-validator]

---

### 2.3 Skills Core

| Skill | Fichier | YAML | Tokens | Refs | Status |
|-------|---------|------|--------|------|--------|
| epci-core | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| architecture-patterns | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| breakpoint-metrics | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| clarification-intelligente | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| flags-system | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| proactive-suggestions | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| learning-optimizer | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| project-memory | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| project-memory-loader | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| code-conventions | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| testing-strategy | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| git-workflow | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

**Légende** : Fichier=existe, YAML=frontmatter valide, Tokens=<5000, Refs=références OK

---

### 2.4 Skills Stack

| Skill | Fichier | YAML | Auto-détection | Références |
|-------|---------|------|----------------|------------|
| php-symfony | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| javascript-react | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| python-django | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| java-springboot | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

---

### 2.5 Skills Factory

| Skill | Fichier | Templates | Validation Script |
|-------|---------|-----------|-------------------|
| skills-creator | ✅/❌ | ✅/❌ | ✅/❌ |
| commands-creator | ✅/❌ | ✅/❌ | ✅/❌ |
| subagents-creator | ✅/❌ | ✅/❌ | ✅/❌ |
| component-advisor | ✅/❌ | ✅/❌ | N/A |

---

### 2.6 Système de Hooks

| Hook | Type | Fichier | Exécutable | Syntaxe |
|------|------|---------|------------|---------|
| pre-phase-2-lint.sh | pre-phase-2 | ✅/❌ | ✅/❌ | ✅/❌ |
| post-phase-2-suggestions.py | post-phase-2 | ✅/❌ | ✅/❌ | ✅/❌ |
| post-phase-3-memory-update.py | post-phase-3 | ✅/❌ | ✅/❌ | ✅/❌ |
| on-breakpoint-memory-context.py | on-breakpoint | ✅/❌ | ✅/❌ | ✅/❌ |

**runner.py** : ✅/❌ Fonctionnel

---

### 2.7 Project Memory

| Module/Fichier | Existe | Valide | Fonctionnel |
|----------------|--------|--------|-------------|
| manager.py | ✅/❌ | ✅/❌ | ✅/❌ |
| detector.py | ✅/❌ | ✅/❌ | ✅/❌ |
| calibration.py | ✅/❌ | ✅/❌ | ✅/❌ |
| clarification_analyzer.py | ✅/❌ | ✅/❌ | ✅/❌ |
| similarity_matcher.py | ✅/❌ | ✅/❌ | ✅/❌ |
| question_generator.py | ✅/❌ | ✅/❌ | ✅/❌ |
| suggestion_engine.py | ✅/❌ | ✅/❌ | ✅/❌ |
| learning_analyzer.py | ✅/❌ | ✅/❌ | ✅/❌ |
| pattern_catalog.py | ✅/❌ | ✅/❌ | ✅/❌ |
| schemas/*.json | ✅/❌ | ✅/❌ | N/A |
| templates/*.json | ✅/❌ | ✅/❌ | N/A |
| tests/test_*.py | ✅/❌ | ✅/❌ | ✅/❌ |

---

### 2.8 Scripts de Validation

| Script | Existe | Exécutable | Résultat |
|--------|--------|------------|----------|
| validate_all.py | ✅/❌ | ✅/❌ | [Output] |
| validate_skill.py | ✅/❌ | ✅/❌ | [Output] |
| validate_command.py | ✅/❌ | ✅/❌ | [Output] |
| validate_subagent.py | ✅/❌ | ✅/❌ | [Output] |
| validate_flags.py | ✅/❌ | ✅/❌ | [Output] |
| validate_memory.py | ✅/❌ | ✅/❌ | [Output] |
| test_triggering.py | ✅/❌ | ✅/❌ | [Output] |

---

### 2.9 Brainstormer (si implémenté)

| ID | Fonctionnalité | Implémenté | Fonctionnel |
|----|----------------|------------|-------------|
| BRAIN-01 | Commande /brainstorm | ✅/❌/🚧 | ✅/❌ |
| BRAIN-02 | Phase Init | ✅/❌/🚧 | ✅/❌ |
| ... | ... | ... | ... |

**Status** : ✅ Implémenté / ❌ Absent / 🚧 En cours

---

## 3. Résultats des Validations Automatisées

### 3.1 validate_all.py

```
[Coller l'output complet ici]
```

**Résumé** :
- Total composants : X
- Validés : X
- Erreurs : X
- Warnings : X

### 3.2 test_triggering.py

```
[Coller l'output complet ici]
```

**Résumé** :
- Skills testés : X
- Triggers OK : X
- Triggers KO : X

### 3.3 hooks/runner.py --list

```
[Coller l'output complet ici]
```

---

## 4. Tests Fonctionnels

### 4.1 Test /epci-memory status

**Commande exécutée** : `/epci-memory status`

**Résultat attendu** : Dashboard avec project name, stack, metrics

**Résultat obtenu** :
```
[Output]
```

**Verdict** : ✅/❌

### 4.2 Test /epci-learn status

**Commande exécutée** : `/epci-learn status`

**Résultat attendu** : Dashboard calibration avec factors, samples, confidence

**Résultat obtenu** :
```
[Output]
```

**Verdict** : ✅/❌

---

## 5. Registre des Écarts

### 5.1 Écarts Critiques (🔴)

| ID | Composant | Écart | Impact | Action Requise |
|----|-----------|-------|--------|----------------|
| EC-001 | [Composant] | [Description] | [Impact] | [Action] |
| ... | ... | ... | ... | ... |

### 5.2 Écarts Majeurs (🟠)

| ID | Composant | Écart | Impact | Action Recommandée |
|----|-----------|-------|--------|-------------------|
| EM-001 | [Composant] | [Description] | [Impact] | [Action] |
| ... | ... | ... | ... | ... |

### 5.3 Écarts Mineurs (🟡)

| ID | Composant | Écart | Recommandation |
|----|-----------|-------|----------------|
| Em-001 | [Composant] | [Description] | [Recommandation] |
| ... | ... | ... | ... |

---

## 6. Plan de Remédiation

### 6.1 Actions Immédiates (Critiques)

| Priorité | Action | Responsable | Délai |
|----------|--------|-------------|-------|
| 1 | [Action] | Dev | Immédiat |
| 2 | [Action] | Dev | 24h |

### 6.2 Actions Court Terme (Majeures)

| Priorité | Action | Responsable | Délai |
|----------|--------|-------------|-------|
| 1 | [Action] | Dev | 1 semaine |
| 2 | [Action] | Dev | 1 semaine |

### 6.3 Améliorations (Mineures)

| Action | Bénéfice | Effort |
|--------|----------|--------|
| [Action] | [Bénéfice] | Faible/Moyen/Élevé |

---

## 7. Annexes

### A. Arborescence Vérifiée

```
epci-plugin/
├── commands/
│   ├── epci-brief.md      [✅/❌]
│   ├── epci.md            [✅/❌]
│   ├── epci-quick.md      [✅/❌]
│   ├── epci-spike.md      [✅/❌]
│   ├── epci-decompose.md  [✅/❌]
│   ├── epci-memory.md     [✅/❌]
│   ├── epci-learn.md      [✅/❌]
│   └── create.md          [✅/❌]
├── agents/
│   ├── plan-validator.md  [✅/❌]
│   ├── code-reviewer.md   [✅/❌]
│   ├── security-auditor.md[✅/❌]
│   ├── qa-reviewer.md     [✅/❌]
│   ├── doc-generator.md   [✅/❌]
│   └── decompose-validator.md [✅/❌]
├── skills/
│   ├── core/              [X/12 ✅]
│   ├── stack/             [X/4 ✅]
│   └── factory/           [X/4 ✅]
├── hooks/
│   ├── runner.py          [✅/❌]
│   ├── active/            [X hooks]
│   └── examples/          [X hooks]
├── project-memory/
│   ├── *.py               [X/9 ✅]
│   ├── schemas/           [✅/❌]
│   ├── templates/         [✅/❌]
│   └── tests/             [✅/❌]
├── scripts/
│   └── *.py               [X/7 ✅]
└── settings/
    └── flags.md           [✅/❌]
```

### B. Logs Complets

[Inclure les logs pertinents si nécessaire]

### C. Fichiers Manquants

| Fichier Attendu | Status | Action |
|-----------------|--------|--------|
| [Fichier] | Manquant | Créer |

---

## 8. Signatures

| Rôle | Nom | Date |
|------|-----|------|
| Auditeur | Claude Code | [DATE] |
| Validation | [À compléter] | |

---

*Document généré automatiquement — Audit EPCI v3.x*

---

## Instructions de Génération

1. **Crée le dossier** `docs/audits/` s'il n'existe pas
2. **Nomme le fichier** : `AUDIT-EPCI-COMPLET-YYYYMMDD.md`
3. **Parcours systématiquement** chaque élément de l'inventaire
4. **Exécute tous les scripts** de validation disponibles
5. **Documente chaque écart** avec son ID unique
6. **Propose des actions** pour chaque écart identifié

## Confirmation Finale

À la fin de l'audit, affiche :

```
═══════════════════════════════════════════════════════════════
✅ AUDIT TERMINÉ

📄 Rapport généré : docs/audits/AUDIT-EPCI-COMPLET-[DATE].md

📊 Résumé :
   • Verdict : [CONFORME/PARTIELLEMENT CONFORME/NON CONFORME]
   • Composants audités : X/Y
   • Écarts critiques : X
   • Écarts majeurs : X
   • Écarts mineurs : X

⏭️ Prochaine étape : Revue du rapport et plan de remédiation
═══════════════════════════════════════════════════════════════
```
```

## --- FIN DU PROMPT À COPIER ---

---

## Instructions d'utilisation

### Prérequis

1. Le fichier `epci-inventaire-fonctionnalites.md` doit être présent dans ton projet
2. Tu dois être dans le répertoire racine du plugin EPCI

### Étapes

1. **Ouvre Claude Code** dans ton projet EPCI
2. **Copie tout le contenu** entre `--- DÉBUT ---` et `--- FIN ---`
3. **Colle dans Claude Code**
4. **Attends la génération** du rapport (10-20 min selon la taille)
5. **Récupère le rapport** dans `docs/audits/`

### Alternative : Avec fichier inventaire inline

Si tu préfères inclure l'inventaire directement dans le prompt, ajoute après la ligne `→ Fichier : epci-inventaire-fonctionnalites.md` :

```
<inventaire>
[Coller ici le contenu complet de epci-inventaire-fonctionnalites.md]
</inventaire>
```
