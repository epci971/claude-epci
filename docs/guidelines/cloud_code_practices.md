# Étude Exhaustive : Meilleures Pratiques pour le Développement de Plugins Cloud Code

**Version:** 1.0  
**Date:** Janvier 2026  
**Couverture:** Commands, Skills, Agents et évolutions récentes (Skills auto-invoqués)

---

## Table des Matières

1. [Principes Fondamentaux](#principes-fondamentaux)
2. [Architecture & Structure](#architecture--structure)
3. [Meilleures Pratiques pour les Commands](#meilleures-pratiques-pour-les-commands)
4. [Meilleures Pratiques pour les Skills](#meilleures-pratiques-pour-les-skills)
5. [Meilleures Pratiques pour les Agents](#meilleures-pratiques-pour-les-agents)
6. [Sécurité & Isolation](#sécurité--isolation)
7. [Testing & Validation](#testing--validation)
8. [Performance & Optimisation](#performance--optimisation)
9. [Gestion du Contexte](#gestion-du-contexte)
10. [Matrice de Conformité](#matrice-de-conformité)

---

## Principes Fondamentaux

### 1.1 - Progressive Context Loading (PCL)
**Principe:** Charger uniquement le contexte nécessaire au moment opportun.

**Critères de conformité:**
- [ ] La description du skill/commande est disponible sans charger tout le contenu
- [ ] Le contenu complet se charge uniquement lors de l'invocation
- [ ] Les fichiers référencés se chargent progressivement et à la demande
- [ ] Les dépendances sont déclarées explicitement

**Exemple conforme:**
```
Chargement initial: Métadonnées + description (100-200 caractères)
À l'invocation: Contenu complet + dépendances
```

### 1.2 - Responsabilité Unique (SRP)
**Principe:** Chaque skill/command/agent a une seule raison de changer.

**Critères de conformité:**
- [ ] Une command = une tâche spécifique
- [ ] Un skill = une expertise métier distinct
- [ ] Un agent = un rôle clairement défini
- [ ] Pas de dépendances circulaires
- [ ] Composition plutôt que héritage

### 1.3 - Idempotence
**Principe:** Exécuter la même opération plusieurs fois produit le même résultat.

**Critères de conformité:**
- [ ] Les opérations sont reproductibles
- [ ] Pas d'état global modifié
- [ ] Les résultats sont déterministes
- [ ] Les effets secondaires sont documentés
- [ ] Les commandes idempotentes sont marquées `idempotent: true`

### 1.4 - Portabilité
**Principe:** Les skills et commands peuvent être partagés entre projets.

**Critères de conformité:**
- [ ] Aucun chemin absolu
- [ ] Aucune dépendance au contexte global
- [ ] Configuration externalisée
- [ ] Variables d'environnement utilisées pour les secrets
- [ ] Tests sans dépendances externes

---

## Architecture & Structure

### 2.1 - Structure des Répertoires

**Structure recommandée:**
```
mon-plugin/
├── .claude/
│   ├── commands/
│   │   ├── analyze-code/
│   │   │   ├── command.md
│   │   │   ├── analyze.js
│   │   │   └── utils.js
│   │   └── generate-tests/
│   │       └── command.md
│   ├── skills/
│   │   ├── code-analyzer/
│   │   │   ├── skill.md
│   │   │   ├── analyzer.js
│   │   │   └── rules/
│   │   │       └── patterns.json
│   │   └── test-generator/
│   │       └── skill.md
│   ├── agents/
│   │   ├── code-reviewer/
│   │   │   └── agent.md
│   │   └── security-checker/
│   │       └── agent.md
│   └── settings.json
├── CLAUDE.md
├── tests/
│   ├── commands.test.js
│   ├── skills.test.js
│   └── agents.test.js
└── package.json
```

**Critères de conformité:**
- [ ] Séparation claire entre commands, skills, agents
- [ ] Structure cohérente et prévisible
- [ ] Documentation colocalisée avec le code
- [ ] Fichiers de configuration centralisés
- [ ] Hiérarchie claire et lisible

### 2.2 - Fichier CLAUDE.md (Contexte d'Exécution)

**Contenu obligatoire:**
```markdown
# CLAUDE.md - Contexte de Développement

## Pile Technologique
- Node.js 18+
- Framework: [votre framework]
- Versions clés: [spécifier]

## Repo Map
- `/commands` → Commandes disponibles
- `/skills` → Skills (auto-invoquées)
- `/agents` → Agents spécialisés

## Commandes Standard
- `npm test` → Lancer tous les tests
- `npm run lint` → Vérifier style et conformité
- `npm run validate` → Valider la structure

## Style & Conventions
- ES Modules (import/export)
- Destructuration obligatoire
- Nommage: camelCase (JS), kebab-case (fichiers)
- Commentaires JSDoc pour APIs publiques

## Zones "Ne Pas Toucher"
- [Lister fichiers critiques]

## Sécurité & Compliance
- Pas de secrets en dur
- Variables d'env: `.env.example`
- Audit trail obligatoire
```

**Critères de conformité:**
- [ ] CLAUDE.md existe et est à jour
- [ ] Toutes les règles importantes sont documentées
- [ ] Zones protégées clairement identifiées
- [ ] Instructions de test présentes
- [ ] Secrets et sensibilités explicitement mentionnés

---

## Meilleures Pratiques pour les Commands

### 3.1 - Frontmatter & Métadonnées

**Structure obligatoire:**
```markdown
---
name: analyze-code-quality
description: Analyse la qualité du code et identifie les problèmes
argument-hint: [file-path] [options]
type: prompt
user-invocable: true
disable-model-invocation: false
idempotent: false
category: code-analysis
version: "1.0"
author: plugin-name
dependencies: [eslint, prettier]
timeout: 30000
---

# Implementation
...
```

**Critères de conformité:**
- [ ] `name`: kebab-case, unique dans le plugin
- [ ] `description`: <200 caractères, claire et actionnable
- [ ] `argument-hint`: indique le format attendu
- [ ] `type`: "prompt", "code", ou "workflow"
- [ ] `user-invocable` & `disable-model-invocation` explicites
- [ ] `idempotent`: true si la commande est idempotente
- [ ] `timeout`: spécifié pour les opérations longues
- [ ] `dependencies`: listées et versionées
- [ ] `version`: suit SemVer

### 3.2 - Contenu de la Command

**Structure recommandée:**
```markdown
---
name: validate-plugin
description: Valide la structure et la conformité du plugin
---

# Validation de Plugin

## Étapes
1. Vérifier structure des répertoires
2. Valider tous les frontmatter
3. Exécuter tests unitaires
4. Vérifier absence de secrets
5. Générer rapport de conformité

## Utilisation
\`/validate-plugin\` [--strict] [--report]

## Résultats
- ✅ Plugin conforme
- ⚠️ Avertissements (non-bloquants)
- ❌ Erreurs (blocage)
```

**Critères de conformité:**
- [ ] Étapes clairement numérotées
- [ ] Résultats déterministes
- [ ] Messages d'erreur explicites
- [ ] Format de sortie bien défini
- [ ] Exemples d'utilisation fournis
- [ ] Conditions de succès/échec claires

### 3.3 - Gestion des Erreurs

**Pattern obligatoire:**
```javascript
// Toujours retourner objet structuré
const result = {
  success: boolean,
  errorCode: string | null,
  errorMessage: string | null,
  data: any,
  metadata: {
    executionTime: number,
    timestamp: ISO8601,
    commandVersion: string
  }
};

// Codes d'erreur standardisés
const ERROR_CODES = {
  INVALID_ARGS: 'CMD_INVALID_ARGS',
  FILE_NOT_FOUND: 'CMD_FILE_NOT_FOUND',
  PERMISSION_DENIED: 'CMD_PERMISSION_DENIED',
  EXECUTION_TIMEOUT: 'CMD_EXEC_TIMEOUT',
  VALIDATION_FAILED: 'CMD_VALIDATION_FAILED'
};
```

**Critères de conformité:**
- [ ] Tous les erreurs retournent structure standardisée
- [ ] Codes d'erreur constants et documentés
- [ ] Messages d'erreur explicites (>10 caractères)
- [ ] Stack trace loggée (non exposée au user)
- [ ] Métadonnées d'exécution incluses
- [ ] Pas de console.log (utiliser logger)

### 3.4 - Input Validation

**Obligatoire pour chaque paramètre:**
```javascript
function validateInput(args) {
  const schema = {
    filePath: { type: 'string', required: true, pattern: /^[^\0]*$/ },
    options: { type: 'object', required: false, strict: true },
    verbosity: { type: 'enum', values: ['low', 'medium', 'high'] }
  };
  
  for (const [key, rules] of Object.entries(schema)) {
    if (rules.required && !args[key]) {
      throw new ValidationError(`Missing required: ${key}`);
    }
    // Valider type
    // Valider pattern/enum
    // Valider taille/limites
  }
}
```

**Critères de conformité:**
- [ ] Schéma de validation défini
- [ ] Type-checking obligatoire
- [ ] Regex pour chaînes (injection prevention)
- [ ] Limites de taille (fichiers, nombre, etc.)
- [ ] Énumérés pour valeurs discrètes
- [ ] Messages d'erreur de validation clairs

### 3.5 - Composition de Commands

**Pattern pour commands complexes:**
```markdown
---
name: code-review-full
dependencies: [analyze-code-quality, security-scan, test-coverage]
---

# Full Code Review

Cette commande orchestre plusieurs commandes spécialisées.

## Flux
1. Lancer `analyze-code-quality`
2. Lancer `security-scan` en parallèle
3. Lancer `test-coverage` en parallèle
4. Synthétiser résultats
5. Générer rapport unifié
```

**Critères de conformité:**
- [ ] Dépendances déclarées et versionnées
- [ ] Exécution parallèle quand possible
- [ ] Fusion cohérente des résultats
- [ ] Pas d'invocation circulaire
- [ ] Timeout parent = max(timeouts enfants)

---

## Meilleures Pratiques pour les Skills

### 4.1 - Anatomie d'un Skill (Frontmatter)

**Structure complète:**
```yaml
---
name: code-refactor
description: Refactorise le code pour améliorer maintenabilité
type: prompt
user-invocable: true
disable-model-invocation: false
when-to-use: Quand du code répété doit être restructuré
expertise-domain: code-quality
complexity-level: medium
icon: ♻️
---
```

**Champs obligatoires:**
- [ ] `name`: unique, kebab-case
- [ ] `description`: claire, <200 caractères
- [ ] `type`: "prompt" (pour skills Claude Code)
- [ ] `user-invocable`: vrai par défaut
- [ ] `disable-model-invocation`: faux par défaut
- [ ] `expertise-domain`: catégorie métier
- [ ] `complexity-level`: low, medium, high

### 4.2 - Auto-Invocation (Skills Auto-Invoqués)

**Concept clé:** Claude décide automatiquement d'utiliser le skill si la description match le contexte.

**Pour ACTIVER l'auto-invocation:**
```yaml
---
name: test-generator
disable-model-invocation: false  # ← CLÉ
description: Génère tests unitaires basés sur le code existant. Utilisé quand du code sans tests doit être couvert.
---
```

**Pour DÉSACTIVER l'auto-invocation:**
```yaml
---
name: dangerous-refactor
disable-model-invocation: true  # ← Invocation manuelle seulement via /dangerous-refactor
user-invocable: true
description: Utilisé uniquement quand explicitement invoqué.
---
```

**Critères de conformité pour skills auto-invoqués:**
- [ ] Description contient mots-clés pour trigger (ex: "Générer tests", "Refactoriser")
- [ ] Pas d'effets secondaires dangereux
- [ ] Opération réversible (ou checkpoints recommandés)
- [ ] Timeout spécifié
- [ ] Permissions explicites
- [ ] Pas de modification de fichiers critiques sans consentement

### 4.3 - Structure du Contenu Skill

**Exemple complet:**
```markdown
---
name: analyze-dependencies
description: Analyse les dépendances et identifie vulnérabilités, obsolescence
type: prompt
disable-model-invocation: false
---

# Analyser les Dépendances du Projet

## Quand utiliser
- Lors d'audit de sécurité
- Pour mise à jour de dépendances
- Pour identifier tech debt

## Ce que fait ce skill
1. Parse package.json et yarn.lock/pnpm-lock
2. Vérifie versions contre latest
3. Scanne vulnérabilités connues
4. Identifie dépendances inutilisées
5. Propose plan de mise à jour

## Instructions pour Claude

Quand invoqué pour analyser les dépendances:

1. **Charger dépendances actuelles**
   - Lire package.json
   - Identifier versions directes

2. **Audit de sécurité**
   - Vérifier CVE database
   - Relever vulnerabilités critiques
   - Proposer patches

3. **Obsolescence**
   - Comparer avec latest
   - Identifier breaking changes
   - Évaluer impact de mise à jour

4. **Recommandations**
   - Hiérarchiser par risque
   - Suggérer version stables
   - Avertir sur breaking changes

## Output format
\`\`\`json
{
  "vulnerabilities": [{...}],
  "updates": [{...}],
  "unused": [...],
  "recommendations": [...]
}
\`\`\`
```

**Critères de conformité:**
- [ ] Section "Quand utiliser" présente
- [ ] Instructions pas à pas
- [ ] Format de sortie défini
- [ ] Exemples concrets fournis
- [ ] Limitations documentées
- [ ] Fallback en cas d'erreur

### 4.4 - Progressive Loading de Skills

**Architecture correcte:**
```
Contexte initial:
├── Métadonnées skill (10 lignes)
└── Description (1-2 lignes)

À l'invocation:
├── Contenu complet du skill
├── Fichiers référencés (parser.js, rules.json)
└── Dépendances associées
```

**Critères de conformité:**
- [ ] Métadonnées chargées systématiquement
- [ ] Contenu complet chargé lazy
- [ ] Fichiers supportants déterminés dynamiquement
- [ ] Pas de sur-chargement du contexte
- [ ] Temps de réponse initial <1s

### 4.5 - Permissions et Scope

**Déclarer explicitement:**
```yaml
---
name: file-modifier
permissions:
  - "read:workspace"      # lecture fichiers
  - "write:current-file"  # écriture fichier courant seulement
  - "no:network"          # aucun accès réseau
  - "no:shell"           # pas de shell commands
---
```

**Critères de conformité:**
- [ ] Permissions minimales (principle of least privilege)
- [ ] Fichiers critiques explicitement exclus
- [ ] Réseau/shell restreint si possible
- [ ] Permissions documentées en frontmatter
- [ ] Pas de privilèges demandés mais inutilisés

---

## Meilleures Pratiques pour les Agents

### 5.1 - Définition d'un Agent

**Structure de base:**
```markdown
---
name: code-reviewer
role: "Spécialiste en revue de code"
instructions: |
  Tu es un expert en revue de code avec 10+ ans d'expérience.
  Tu te focuses sur:
  - Clarté et lisibilité
  - Patterns et anti-patterns
  - Performance
  - Sécurité
  
  Tu fournis du feedback constructif et actionnable.

skills: [code-analyzer, security-scanner]
subordinates: []
model: claude-opus  # optional: modèle spécifique
context-limit: 100000
---
```

**Critères de conformité:**
- [ ] `role` clairement défini
- [ ] `instructions` détaillées et spécifiques
- [ ] `skills` assignés pertinents
- [ ] Pas de sous-agents de même rôle (prevent loops)
- [ ] `context-limit` respecté

### 5.2 - Multi-Agent Orchestration

**Pattern recommandé:**
```
Flux d'orchestration:

1. SOFTWARE ENGINEER AGENT
   ├─ Skills: test-generator, code-creator
   └─ Output: code + tests

2. CODE REVIEWER AGENT (parallèle ou séquentiel)
   ├─ Skills: code-analyzer, best-practices-checker
   └─ Output: feedback, suggestions

3. SECURITY AGENT (parallèle ou séquentiel)
   ├─ Skills: security-scanner, vulnerability-detector
   └─ Output: security findings

4. SYNTHESIS
   ├─ Aggréger tous les résultats
   ├─ Générer rapport unifié
   └─ Proposer PR finale
```

**Critères de conformité:**
- [ ] Agents spécialisés par domaine
- [ ] Pas de chevauchement de responsabilité
- [ ] Communication explicite entre agents
- [ ] Exécution parallèle quand possible
- [ ] Synthèse des résultats centralisée
- [ ] Pas de context pollution entre agents

### 5.3 - Sub-Agents vs Agents

**Sub-Agents:** Agents invoqués depuis le contexte courant (utiles pour tâches secondaires)

**Agents Indépendants:** Agents avec contexte isolé (pour tâches principales)

**Critères de sélection:**
- [ ] Sub-agent si: tâche mineure, même contexte utilisable
- [ ] Agent indépendant si: tâche majeure, contexte isolé utile
- [ ] Pas de chaînes >3 levels d'agents

### 5.4 - Checkpoints et Contrôle

**Pattern obligatoire:**
```javascript
// Pour chaque étape majeure
checkpoint({
  name: "post-code-generation",
  description: "Code généré avant revue",
  canRevert: true,
  branchName: "feature/auto-generated"
});

// Avant changements destructifs
if (!userApproved()) {
  return {
    status: "AWAITING_APPROVAL",
    changes: [...],
    reviewUrl: ".../pr/123"
  };
}
```

**Critères de conformité:**
- [ ] Checkpoints après chaque batch de changements
- [ ] Revert possible pour chaque checkpoint
- [ ] Approbation utilisateur avant changements destructifs
- [ ] Audit trail complet loggé
- [ ] Rollback automatique sur erreur

### 5.5 - Agent Communication Protocol

**Format standardisé:**
```javascript
// Message inter-agent
{
  from: "software-engineer-agent",
  to: "code-reviewer-agent",
  type: "request-review",
  payload: {
    files: [...],
    context: "Feature X implementation",
    priority: "high"
  },
  metadata: {
    timestamp: ISO8601,
    requestId: UUID,
    priority: 0-10
  }
}

// Response
{
  to: "software-engineer-agent",
  from: "code-reviewer-agent",
  type: "review-complete",
  payload: {
    status: "approved" | "needs-changes" | "rejected",
    findings: [],
    suggestions: []
  }
}
```

**Critères de conformité:**
- [ ] Format de message standardisé
- [ ] Métadonnées incluant timestamp et ID de requête
- [ ] Statut de réponse explicite
- [ ] Pas de communication implicite
- [ ] Audit trail des messages

---

## Sécurité & Isolation

### 6.1 - Isolation par Projet

**Règle d'or:** Plugins du même projet partagent sandbox → problème de sécurité.

**Solution - Séparation stricte:**
```json
// settings.json
{
  "projectId": "project-prod",
  "security": {
    "isolate": true,
    "compartments": [
      {
        "name": "financial-operations",
        "projectId": "project-financial-separate"
      },
      {
        "name": "user-data-processing",
        "projectId": "project-data-separate"
      }
    ]
  }
}
```

**Critères de conformité:**
- [ ] Workloads sensibles en projets séparés
- [ ] Permissions par compartiment
- [ ] Zero trust entre compartiments
- [ ] Chaque compartiment audit trail distinct

### 6.2 - Gestion des Secrets

**Obligatoire - Jamais en dur:**
```javascript
// ❌ MAUVAIS
const API_KEY = "sk-1234567890abcdef";

// ✅ BON
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error("API_KEY not set");

// .env.example (commité)
API_KEY=<your-key-here>
DATABASE_URL=<database-url>
```

**Critères de conformité:**
- [ ] Aucun secret dans code ou git
- [ ] Variables d'env préfixées (`PLUGIN_*`)
- [ ] `.env.example` avec placeholders
- [ ] `.env` dans `.gitignore`
- [ ] Audit log pour accès secrets
- [ ] Rotation de secrets documentée

### 6.3 - Input Sanitization

**Obligatoire partout:**
```javascript
function sanitizeInput(input, type = 'string') {
  switch(type) {
    case 'string':
      // Prevent injection
      return input
        .replace(/[<>]/g, '')  // HTML entities
        .trim()
        .slice(0, 1000);  // Limite taille
    
    case 'filepath':
      // Prevent path traversal
      if (input.includes('..') || input.startsWith('/')) {
        throw new SecurityError('Invalid path');
      }
      return input;
    
    case 'json':
      try {
        return JSON.parse(input);
      } catch (e) {
        throw new ValidationError('Invalid JSON');
      }
  }
}
```

**Critères de conformité:**
- [ ] Sanitization pour strings, paths, JSON
- [ ] Limites de taille appliquées
- [ ] Caractères dangereux filtrés
- [ ] Validation stricte des enums
- [ ] Pas de eval() ou functions dynamiques

### 6.4 - Audit Trail

**Obligatoire pour actions sensibles:**
```javascript
async function logAction(action, details, userId) {
  const auditEntry = {
    timestamp: new Date().toISOString(),
    action,
    userId,
    details,
    changes: {
      before: details.before,
      after: details.after
    },
    ipAddress: getClientIP(),
    userAgent: getUserAgent()
  };
  
  await auditLog.write(auditEntry);
  // Ne JAMAIS logger secrets, passwords
}

// Actions à logger:
// - Création/modification/suppression fichiers
// - Changements de permissions
// - Exécution de commands sensibles
// - Approbations utilisateur
```

**Critères de conformité:**
- [ ] Log pour toute action modifiant l'état
- [ ] Timestamp inclus
- [ ] Utilisateur identifié
- [ ] Before/after dans diffs
- [ ] Pas de données sensibles loggées
- [ ] Logs immuables (append-only)

### 6.5 - Permission Model

**Principe: Least Privilege**
```yaml
permissions:
  read:
    - workspace: true
    - specific-files: [package.json, CLAUDE.md]
  write:
    - current-file: true
    - workspace: false
    - append-logs: true
  execute:
    - npm-scripts: [test, lint]
    - shell: false
    - network: false
  resources:
    - max-memory: 512MB
    - max-cpu: 50%
    - max-execution-time: 30s
```

**Critères de conformité:**
- [ ] Permissions minimales nécessaires
- [ ] Ressources limitées (CPU, RAM, temps)
- [ ] Réseau restreint par défaut
- [ ] Shell désactivé à moins qu'explicite
- [ ] Permissions revue lors de chaque mise à jour

---

## Testing & Validation

### 7.1 - Structure de Tests

**Obligatoire - Couvrir tous les niveaux:**
```javascript
// tests/commands.test.js
describe('Commands', () => {
  describe('analyze-code-quality', () => {
    it('should validate input file path', async () => {
      // Test validation
    });
    
    it('should return standardized error on invalid file', async () => {
      // Test error handling
    });
    
    it('should be idempotent', async () => {
      // Run twice, compare results
    });
    
    it('should timeout after 30s', async () => {
      // Timeout test
    });
    
    it('should not expose secrets in output', async () => {
      // Security test
    });
  });
});

// tests/skills.test.js
describe('Skills', () => {
  describe('code-refactor', () => {
    it('should have valid frontmatter', () => {
      // Validate YAML
    });
    
    it('should describe auto-invocation criteria', () => {
      // Check description contains trigger words
    });
    
    it('should load progressively', async () => {
      // Verify lazy loading
    });
    
    it('should not break on missing dependencies', () => {
      // Fallback behavior
    });
  });
});

// tests/agents.test.js
describe('Agents', () => {
  describe('code-reviewer-agent', () => {
    it('should initialize with correct role', () => {
      // Verify metadata
    });
    
    it('should communicate with other agents', async () => {
      // Test message passing
    });
    
    it('should checkpoint after major changes', async () => {
      // Verify checkpoint creation
    });
  });
});
```

**Critères de conformité:**
- [ ] Suite de tests pour chaque command
- [ ] Suite de tests pour chaque skill
- [ ] Suite de tests pour chaque agent
- [ ] Tests d'intégration multi-agents
- [ ] Tests de sécurité/input validation
- [ ] Tests de performance/timeout
- [ ] >80% code coverage

### 7.2 - Test-Driven Development (TDD) Workflow

**Processus obligatoire:**
```
1. ÉCRIRE TESTS
   - Décrire comportement attendu
   - Définir input/output pairs
   - Tester cas d'erreur
   ✅ Confirmation: Tous les tests échouent

2. COMMITER TESTS
   - Sauvegarder tests
   - Ne PAS modifier après ça

3. IMPLÉMENTER CODE
   - Écrire code pour passer les tests
   - Ne PAS modifier les tests
   - Itérer jusqu'à succès
   ✅ Confirmation: Tous les tests passent

4. COMMITER CODE
   - Sauvegarder implémentation
```

**Critères de conformité:**
- [ ] Tests écrits AVANT code
- [ ] Tests ne sont JAMAIS modifiés pour passer
- [ ] Code itère jusqu'à succès
- [ ] Chaque commit est atomique
- [ ] History montre progression claire

### 7.3 - Validation de Conformité

**Checklist automatisée (npm run validate):**
```javascript
// validate.js
const validations = {
  structure: [
    'checkDirectoryStructure',
    'checkFilesExist',
    'checkNoEmptyDirs'
  ],
  
  metadata: [
    'validateAllFrontmatter',
    'validateNames',
    'validateDescriptions',
    'validateVersions'
  ],
  
  code: [
    'lintWithEslint',
    'typeCheckWithTypeScript',
    'runAllTests',
    'checkCodeCoverage'
  ],
  
  security: [
    'scanForSecrets',
    'checkForVulnerabilities',
    'validateInputSanitization',
    'checkForInsecurePatterns'
  ],
  
  performance: [
    'checkContextSize',
    'validateTimeouts',
    'checkMemoryUsage'
  ]
};
```

**Critères de conformité:**
- [ ] npm run validate = exit 0 (succès)
- [ ] npm run validate --strict = fail sur warnings
- [ ] Rapport généré avec détails
- [ ] Historique de validations gardé
- [ ] CI/CD bloque si validation échoue

### 7.4 - Test-Specific Commands

**Créer commands de test:**
```markdown
---
name: run-conformity-tests
description: Lance tous les tests de conformité du plugin
---

## Conformity Test Suite

Lance:
1. Tests structurels
2. Tests de validation métadonnées
3. Tests de sécurité
4. Tests de performance
5. Rapport final de couverture

Sortie: Pass/Fail + détails

---
name: test-coverage-report
description: Génère et affiche rapport de couverture de code
---
```

**Critères de conformité:**
- [ ] Commands de test bien documentées
- [ ] Report format parseable
- [ ] Metrics collectées (coverage %, time, etc.)
- [ ] Historique de trends accessible

---

## Performance & Optimisation

### 8.1 - Context Size Management

**Règles strictes:**
```javascript
// Chaque élement en contexte doit être compté
const contextBudget = 100_000; // tokens

const contextUsage = {
  systemPrompt: 2_000,
  skillDescriptions: 5_000,  // Lazy loaded
  commandDescriptions: 3_000,  // Lazy loaded
  agentDefinitions: 2_000,
  userQuery: 500,
  // Total au démarrage: ~12.5k
  // Budgeté: jusqu'à 87.5k pour content
};
```

**Critères de conformité:**
- [ ] Context initial <15% du budget
- [ ] Métadonnées chargées systématiquement
- [ ] Contenu chargé lazy
- [ ] Pas d'over-loading
- [ ] Monitoring du contexte réel
- [ ] Alertes si >80% utilisé

### 8.2 - Progressive Loading Details

**Implémentation requise:**
```javascript
class SkillLoader {
  // Phase 1: Load metadata only
  async loadMetadata(skillName) {
    return await fs.readFile(`skills/${skillName}/skill.md`, 'utf8')
      .split('---')[1]  // YAML frontmatter seulement
      .parseAsYAML();
  }
  
  // Phase 2: Load content on demand
  async loadFull(skillName) {
    const metadata = await this.loadMetadata(skillName);
    const content = await fs.readFile(`skills/${skillName}/skill.md`, 'utf8');
    return { metadata, content };
  }
  
  // Phase 3: Load dependencies progressively
  async loadDependencies(skillName) {
    const metadata = await this.loadMetadata(skillName);
    return await Promise.all(
      metadata.dependencies?.map(dep => this.loadFull(dep)) || []
    );
  }
}
```

**Critères de conformité:**
- [ ] 3 phases de chargement clairement définies
- [ ] Phase 1 <1s de latence
- [ ] Phase 2 & 3 parallélisées
- [ ] Dépendances chaînées correctement
- [ ] Caching des métadonnées

### 8.3 - Timeout Management

**Spécification obligatoire:**
```yaml
---
name: code-analyzer
timeout: 30000  # 30 secondes
soft-timeout: 25000  # Alert après 25s
max-retries: 2

# Par étape interne:
steps:
  - parse-files: 5000ms
  - analyze-patterns: 15000ms
  - generate-report: 5000ms
  - cleanup: 1000ms
---
```

**Critères de conformité:**
- [ ] Timeout spécifié pour chaque command/skill
- [ ] Soft-timeout pour logs d'alerte
- [ ] Étapes discrètes avec timeouts propres
- [ ] Cleanup garanti même en timeout
- [ ] Pas de orphaned processes
- [ ] Logs de timeout détaillés

### 8.4 - Resource Limits

**Configuration:**
```json
{
  "resourceLimits": {
    "memory": {
      "perExecution": "512MB",
      "perProject": "2GB"
    },
    "cpu": {
      "perExecution": "50%",
      "cores": 2
    },
    "disk": {
      "tempFiles": "1GB",
      "logs": "500MB"
    },
    "network": {
      "bandwidthPerMin": "100MB",
      "connectionsPerExecution": 5
    }
  }
}
```

**Critères de conformité:**
- [ ] Limites définies par resource
- [ ] Monitoring en temps réel
- [ ] Alertes à 80% d'usage
- [ ] Cleanup automatique des temp files
- [ ] Pas de resource exhaustion possible

---

## Gestion du Contexte

### 9.1 - CLAUDE.md - Contexte Complet

**Contenu obligatoire pour projet:**
```markdown
# CLAUDE.md - Contexte d'Exécution du Plugin

## 1. Vue d'Ensemble du Projet
- **Nom:** plugin-cloud-code-suite
- **Description:** Suite de tools pour cloud development
- **Version:** 1.0.0
- **Mainteneur:** [contact]

## 2. Architecture
- Plugins cloud code avec commands, skills, agents
- Progressive context loading
- Multi-agent orchestration
- Test-driven development

## 3. Stack Technologique
- **Runtime:** Node.js 18+
- **Langage:** JavaScript (ES modules)
- **Frameworks:** Claude SDK, Testing: Jest
- **Dépendances clés:** [lister]

## 4. Structure des Répertoires
\`\`\`
.claude/
├── commands/  → Commandes Claude invoquées par user
├── skills/    → Skills auto-invoqués ou manuels
└── agents/    → Agents spécialisés

tests/
├── commands.test.js
├── skills.test.js
└── agents.test.js
\`\`\`

## 5. Commandes Standard
\`\`\`bash
npm test              # Tests (Jest)
npm run lint          # ESLint + Prettier
npm run validate      # Conformité globale
npm run coverage      # Coverage report
\`\`\`

## 6. Conventions de Code
- **Modules:** ES Modules (import/export)
- **Style:** ESLint config .eslintrc.json
- **Nommage:**
  - camelCase pour fonctions/variables
  - kebab-case pour fichiers/commands
  - PascalCase pour classes
- **Commentaires:** JSDoc pour APIs publiques
- **Destructuration:** Obligatoire quand possible

## 7. Style Guide Personnalisé
- [Détails propres au projet]

## 8. Zones Protégées (Ne Pas Toucher)
- `package.json` → Versions des dépendances
- `.claude/settings.json` → Configuration système
- `tests/` → Structure des tests (content peut évoluer)

## 9. Sécurité & Secrets
- **Pas de secrets en dur:** Utiliser variables d'env
- **Template:** `.env.example` pour secrets
- **Audit:** Logs obligatoires pour actions sensibles
- **Permissions:** Least privilege strictement appliqué

## 10. Workflow de Développement
1. Lire cette CLAUDE.md d'abord
2. TDD: Écrire tests → Implémenter → Commit
3. Lancer npm run validate avant chaque commit
4. Checkout sur feature branch
5. PR avec description complète

## 11. Dépannage Courant
- **Test échoue:** Voir messages d'erreur, utiliser --verbose
- **Validation échoue:** npm run validate --details
- **Imports cassés:** Vérifier chemins relatifs (ES modules)

## 12. Ressources & Docs
- Claude Code Docs: https://code.claude.com/docs
- Plugin Best Practices: ./BEST_PRACTICES.md
- Architecture Decision Log: ./ADR.md
```

**Critères de conformité:**
- [ ] CLAUDE.md existe et est complet
- [ ] Mis à jour à chaque changement majeur
- [ ] Lisible et actionnable pour Claude
- [ ] Inclut zones protégées
- [ ] Exemples concrets fournis
- [ ] Dépannage courant couvert

### 9.2 - Context Injection Pattern

**Injection cohérente:**
```javascript
// Ordre de chargement:
const context = {
  // Phase 1: Métadonnées (toujours)
  metadata: await loadMetadata(),
  
  // Phase 2: Contenu (lazy)
  commands: {} ,  // Descriptions seulement
  skills: {},     // Descriptions seulement
  agents: {},     // Definitions seulement
  
  // Phase 3: Dépendances (on demand)
  dependencies: {}, // Chargé dynamiquement
  
  // Phase 4: Historique (optional)
  recentActions: [], // Si pertinent
};
```

**Critères de conformité:**
- [ ] Métadonnées systématiquement chargées
- [ ] Contenu lazy-loaded
- [ ] Dépendances déterminées à l'exécution
- [ ] Aucun sur-chargement
- [ ] Pas d'ordre magique (explicite)

---

## Matrice de Conformité

### Checklist Complète (10 Categories)

| Catégorie | Critère | Status | Notes |
|-----------|---------|--------|-------|
| **PRINCIPES FONDAMENTAUX** | Progressive Context Loading | [ ] | |
| | Responsabilité Unique (SRP) | [ ] | |
| | Idempotence (si applicable) | [ ] | |
| | Portabilité | [ ] | |
| **ARCHITECTURE** | Structure répertoires conforme | [ ] | |
| | CLAUDE.md complet | [ ] | |
| | Fichiers de config centralisés | [ ] | |
| **COMMANDS** | Frontmatter valide | [ ] | |
| | Input validation | [ ] | |
| | Error handling standardisé | [ ] | |
| | Composition multi-level | [ ] | |
| **SKILLS** | Frontmatter complet | [ ] | |
| | Auto-invocation controllée | [ ] | |
| | Description claire | [ ] | |
| | Progressive loading | [ ] | |
| | Permissions minimales | [ ] | |
| **AGENTS** | Rôle clairement défini | [ ] | |
| | Instructions détaillées | [ ] | |
| | Skills assignés pertinents | [ ] | |
| | Orchestration multi-agent | [ ] | |
| | Communication standar | [ ] | |
| | Checkpoints obligatoires | [ ] | |
| **SÉCURITÉ** | Isolation par projet | [ ] | |
| | Pas de secrets en dur | [ ] | |
| | Input sanitization | [ ] | |
| | Audit trail complet | [ ] | |
| | Permission model strict | [ ] | |
| **TESTING** | Tests unitaires >80% | [ ] | |
| | Tests intégration multi-level | [ ] | |
| | Tests sécurité | [ ] | |
| | TDD workflow suivi | [ ] | |
| | Validation automatisée | [ ] | |
| **PERFORMANCE** | Context <15% initial | [ ] | |
| | Progressive loading | [ ] | |
| | Timeouts spécifiés | [ ] | |
| | Resource limits définis | [ ] | |
| **CONTEXTE** | CLAUDE.md complet | [ ] | |
| | Context injection pattern | [ ] | |
| | Documentation actualisée | [ ] | |
| **DOCUMENTATION** | README complet | [ ] | |
| | Exemples concrets | [ ] | |
| | ADR (Architecture Decisions) | [ ] | |
| | Changelog maintenu | [ ] | |

### Critères par Niveaux

**Niveau 1 - Fondations (OBLIGATOIRE)**
- [ ] Structure répertoires conforme
- [ ] CLAUDE.md existe
- [ ] Frontmatter valide sur tous les elements
- [ ] Input validation présente
- [ ] Pas de secrets en dur
- [ ] Tests unitaires écrits

**Niveau 2 - Qualité (RECOMMANDÉ)**
- [ ] >80% code coverage
- [ ] Tests d'intégration
- [ ] Audit trail complète
- [ ] Progressive loading
- [ ] Checkpoints pour agents
- [ ] Monitoring/logging

**Niveau 3 - Excellence (AVANCÉ)**
- [ ] Multi-agent orchestration fluide
- [ ] Self-healing capabilities
- [ ] Performance optimized
- [ ] Exhaustive documentation
- [ ] Security hardening
- [ ] Continuous validation

---

## Conclusion

Cette étude exhaustive couvre les meilleures pratiques 2025-2026 pour plugins cloud code couvrant:

✅ **Commands** - Invocation, validation, composition  
✅ **Skills** - Auto-invocation, progressive loading, permissions  
✅ **Agents** - Rôles, orchestration, communication  
✅ **Sécurité** - Isolation, secrets, audit  
✅ **Testing** - TDD, validation, coverage  
✅ **Performance** - Context management, timeouts, resources  

**Prochaines étapes:**
1. Implémenter checklist de conformité
2. Créer tests unitaires pour chaque catégorie
3. Automatiser validation (npm run validate)
4. Mettre en place CI/CD gates
5. Monitorer conformité continue
