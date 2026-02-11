# BRIEF TECHNIQUE — Pipeline de Développement Semi-Automatisé V3

> **Notion → OpenClaw → Claude Code → GitHub PR**

---

| Champ | Valeur |
|-------|--------|
| Projet | Pipeline de dev semi-automatisé V3 |
| Auteur | Edouard — Auto-entrepreneur fullstack |
| Date | 11 février 2026 |
| Version | 1.0 — Brief initial |
| Statut | Spécification (brainstorm finalisé) |
| Stack cible | Django/Python, Symfony/React (multi-projet) |
| Infra | VPS Linux (Ubuntu 24), OpenClaw, Claude Code CLI |

---


```mermaid
flowchart TD
    %% ============================================================
    %% OPENCLAW — Pipeline Autonome de Développement
    %% Notion → OpenClaw → Claude Code → Git/PR
    %% ============================================================

    %% --- STYLES ---
    classDef notion fill:#2d2d2d,stroke:#e6e6e6,color:#fff,stroke-width:2px
    classDef cron fill:#1a1a2e,stroke:#16213e,color:#e6e6e6,stroke-width:2px
    classDef process fill:#0f3460,stroke:#533483,color:#fff,stroke-width:2px
    classDef decision fill:#533483,stroke:#e94560,color:#fff,stroke-width:2px
    classDef success fill:#1b5e20,stroke:#4caf50,color:#fff,stroke-width:2px
    classDef failure fill:#b71c1c,stroke:#ef5350,color:#fff,stroke-width:2px
    classDef claude fill:#d4a574,stroke:#8b6914,color:#1a1a1a,stroke-width:2px
    classDef telegram fill:#0088cc,stroke:#005f8a,color:#fff,stroke-width:2px
    classDef guardrail fill:#e65100,stroke:#ff9800,color:#fff,stroke-width:2px

    %% ================================================================
    %% BLOC 1 — NOTION (Source de vérité)
    %% ================================================================
    subgraph NOTION["📋 NOTION — Source de vérité"]
        direction TB
        N_DB[("Base 'Dev Tasks'<br/>─────────────<br/>• Titre (title)<br/>• Spec PRD (rich_text)<br/>• Projet (relation)<br/>• Priorité (P0/P1/P2)<br/>• Complexité (simple/moyenne/complexe)<br/>• Statut (select)<br/>• Branch (auto-filled)<br/>• PR URL (auto-filled)<br/>• Coût tokens (auto-filled)<br/>• Logs (commentaires)")]
        N_STATUTS["Cycle de statuts<br/>─────────────<br/>À faire → En cours<br/>→ En review → Terminé<br/>↘ Échoué"]
    end

    %% ================================================================
    %% BLOC 2 — CRON TRIGGER
    %% ================================================================
    CRON{{"⏰ Cron OpenClaw<br/>(10min – 1h configurable)"}}

    %% ================================================================
    %% BLOC 3 — PIPELINE RUNNER
    %% ================================================================
    subgraph PIPELINE["⚙️ OPENCLAW — Orchestrateur VPS Linux"]
        direction TB

        P_START([pipeline-runner.sh])
        P_QUERY["1️⃣ Query Notion API<br/>Tâches 'À faire'<br/>triées par priorité"]
        P_HAS_TASKS{Tâches<br/>disponibles ?}
        P_NO_TASKS([Fin — Rien à traiter])

        %% --- Boucle par tâche ---
        subgraph TASK_LOOP["🔄 Pour chaque tâche (séquentiel)"]
            direction TB

            T_QUOTA["2a. Check quota<br/>Claude Code /status"]
            T_THROTTLE{Throttle ?}
            T_PAUSE["⏸️ Pause 30min<br/>puis retry"]

            T_UPDATE_ENCOURS["2c. Update Notion<br/>→ 'En cours'"]
            T_NOTIF_START["2d. 📱 Telegram<br/>'🚀 Tâche #X démarrée'"]

            T_WORKTREE["2e. Créer Git worktree<br/>feature/{task-id}"]
            T_PROMPT["2f. Construire<br/>prompt EPCI"]

            %% --- Claude Code ---
            subgraph CLAUDE_EXEC["🤖 CLAUDE CODE — Exécuteur"]
                direction TB

                C_LAUNCH["2g. Lancer Claude Code<br/>──────────────<br/>claude -p prompt.md<br/>--model sonnet<br/>--allowedTools Bash,Read,Write,Edit<br/>--permission-mode bypassPermissions<br/>--output-format json"]

                subgraph EPCI["📐 Workflow EPCI"]
                    direction LR
                    E_EXPLORE["🔍 EXPLORE<br/>Identifier fichiers<br/>pertinents"]
                    E_PLAN["📝 PLAN<br/>Proposer plan<br/>d'implémentation"]
                    E_CODE["💻 CODE<br/>Implémenter<br/>selon le plan"]
                    E_INSPECT["🔎 INSPECT<br/>Tests, lint,<br/>typecheck"]

                    E_EXPLORE --> E_PLAN --> E_CODE --> E_INSPECT
                end

                C_LAUNCH --> EPCI
                C_SKILLS["📁 Skills .claude/<br/>chargés automatiquement<br/>(worktree du projet)"]
            end

            %% --- Validation ---
            T_VALIDATE["2h. Validation<br/>──────────────<br/>• Tests (PHPUnit/Jest)<br/>• Lint (ESLint/PSR)<br/>• Typecheck (TS)"]
            T_RESULT{Tests OK ?}

            %% --- Succès ---
            T_PUSH["2i. ✅ Push branch<br/>+ Créer PR"]
            T_NOTION_OK["Update Notion<br/>→ 'En review'<br/>+ Branch + PR URL"]
            T_NOTIF_OK["📱 Telegram<br/>'✅ Tâche #X terminée'"]
            T_TOKENS_OK["📊 Log coût tokens<br/>dans Notion"]

            %% --- Échec ---
            T_RETRY{Retry<br/>disponible ?<br/> max 1}
            T_DIAG["🔧 Enrichir diagnostic<br/>+ log erreur"]
            T_RETRY_EXEC["Relancer Claude Code<br/>avec contexte enrichi"]
            T_NOTION_KO["Update Notion<br/>→ 'Échoué'<br/>+ logs erreur"]
            T_NOTIF_KO["📱 Telegram<br/>'❌ Tâche #X échouée'"]

            %% --- Cleanup ---
            T_CLEANUP["2k. Cleanup worktree<br/>si merged"]

            %% --- Connexions internes ---
            T_QUOTA --> T_THROTTLE
            T_THROTTLE -->|Oui| T_PAUSE
            T_PAUSE -->|Retry| T_QUOTA
            T_THROTTLE -->|Non| T_UPDATE_ENCOURS
            T_UPDATE_ENCOURS --> T_NOTIF_START
            T_NOTIF_START --> T_WORKTREE
            T_WORKTREE --> T_PROMPT
            T_PROMPT --> CLAUDE_EXEC
            CLAUDE_EXEC --> T_VALIDATE
            T_VALIDATE --> T_RESULT

            T_RESULT -->|✅ OK| T_PUSH
            T_PUSH --> T_NOTION_OK
            T_NOTION_OK --> T_TOKENS_OK
            T_TOKENS_OK --> T_NOTIF_OK
            T_NOTIF_OK --> T_CLEANUP

            T_RESULT -->|❌ KO| T_RETRY
            T_RETRY -->|Oui, 1ère fois| T_DIAG
            T_DIAG --> T_RETRY_EXEC
            T_RETRY_EXEC --> T_VALIDATE
            T_RETRY -->|Non, déjà retry| T_NOTION_KO
            T_NOTION_KO --> T_NOTIF_KO
            T_NOTIF_KO --> T_CLEANUP
        end

        %% --- Garde-fous ---
        subgraph GUARDRAILS["🛡️ Garde-fous"]
            direction TB
            G_TIMEOUT["⏱️ Timeout 20min<br/>par tâche"]
            G_BUDGET["💰 Budget tracker<br/>tokens cumulés/session"]
            G_CONSECUTIVE{"3 échecs<br/>consécutifs ?"}
            G_AUTO_PAUSE["⛔ Pause automatique<br/>+ alerte Telegram"]
        end

        P_START --> P_QUERY
        P_QUERY --> P_HAS_TASKS
        P_HAS_TASKS -->|Non| P_NO_TASKS
        P_HAS_TASKS -->|Oui| TASK_LOOP
        T_CLEANUP -->|Tâche suivante| P_HAS_TASKS
    end

    %% ================================================================
    %% BLOC 4 — TELEGRAM KILL SWITCH
    %% ================================================================
    subgraph TELEGRAM["📱 TELEGRAM — Contrôle à distance"]
        direction TB
        TG_COMMANDS["Commandes disponibles<br/>──────────────<br/>/pause — Suspendre le pipeline<br/>/resume — Reprendre<br/>/stop — Arrêter complètement<br/>/status — État actuel + stats"]
        TG_NOTIFS["Notifications reçues<br/>──────────────<br/>🚀 Tâche démarrée<br/>✅ Tâche terminée<br/>❌ Tâche échouée<br/>⛔ Pipeline en pause<br/>📊 Résumé session"]
    end

    %% ================================================================
    %% BLOC 5 — GIT / GITHUB
    %% ================================================================
    subgraph GIT["🔀 GIT / GITHUB"]
        direction TB
        GIT_WORKTREE["Git Worktrees<br/>feature/{task-id}"]
        GIT_PR["Pull Requests<br/>auto-générées"]
        GIT_REVIEW["👁️ Code Review<br/>(manuelle par Edouard)"]
        GIT_MERGE["Merge → main"]

        GIT_WORKTREE --> GIT_PR
        GIT_PR --> GIT_REVIEW
        GIT_REVIEW --> GIT_MERGE
    end

    %% ================================================================
    %% CONNEXIONS INTER-BLOCS
    %% ================================================================
    NOTION -->|"Cron déclenche<br/>le pipeline"| CRON
    CRON --> P_START
    PIPELINE <-->|"Read/Write<br/>statuts, logs, tokens"| NOTION
    PIPELINE <-->|"Notifications &<br/>Kill switch"| TELEGRAM
    PIPELINE -->|"Push & PR"| GIT
    GIT -->|"Merge déclenche<br/>cleanup worktree"| PIPELINE

    G_CONSECUTIVE -->|Oui| G_AUTO_PAUSE
    G_CONSECUTIVE -->|Non| TASK_LOOP

    %% ================================================================
    %% APPLICATION DES STYLES
    %% ================================================================
    class N_DB,N_STATUTS notion
    class CRON cron
    class P_START,P_QUERY,P_HAS_TASKS,P_NO_TASKS process
    class T_QUOTA,T_UPDATE_ENCOURS,T_WORKTREE,T_PROMPT,T_VALIDATE,T_CLEANUP process
    class T_THROTTLE,T_RESULT,T_RETRY decision
    class T_PAUSE guardrail
    class T_PUSH,T_NOTION_OK,T_TOKENS_OK success
    class T_DIAG,T_RETRY_EXEC,T_NOTION_KO failure
    class T_NOTIF_START,T_NOTIF_OK,T_NOTIF_KO,G_AUTO_PAUSE telegram
    class C_LAUNCH,C_SKILLS claude
    class E_EXPLORE,E_PLAN,E_CODE,E_INSPECT claude
    class G_TIMEOUT,G_BUDGET,G_CONSECUTIVE guardrail
    class GIT_WORKTREE,GIT_PR,GIT_REVIEW,GIT_MERGE process
    class TG_COMMANDS,TG_NOTIFS telegram
```


## 1. Résumé Exécutif

Ce document spécifie un **pipeline de développement semi-automatisé** qui transforme un backlog de tâches Notion en Pull Requests GitHub, sans intervention humaine pendant l'exécution. Le pipeline est conçu pour tourner en batch pendant les weekends et soirées, libérant du temps de développement productif.

Le flux est : **Notion** (backlog qualifié) → **OpenClaw** (orchestration cron) → **Claude Code** (exécution EPCI headless via skill implement-auto) → **GitHub** (push + PR avec Feature Document). L'humain intervient uniquement pour la review des PRs le lundi matin.

Le pipeline traite les tâches séquentiellement, avec une cible de **15–30 tâches standard par weekend**, en exploitant un abonnement Claude Max (plan 5x). Chaque tâche consomme ~60–75K tokens Sonnet, avec des options premium (Opus review) pour les tâches critiques.

### Documents liés

| Réf. | Composant | Complexité | Priorité |
|------|-----------|------------|----------|
| SPEC-01 | Skill implement-auto | LARGE | P0 — Critique |
| SPEC-02 | Script orchestrateur | STANDARD | P0 — Critique |
| SPEC-03 | Schéma Notion + export brainstorm | SMALL | P1 — Important |
| SPEC-04 | Notifications + kill switch | SMALL | P1 — Important |

---

## 2. Contexte & Problème

### 2.1 Situation actuelle

Le workflow EPCI (Explore → Plan → Code → Inspect) est opérationnel en mode interactif via le skill **implement**. Chaque tâche nécessite ~20–45 minutes de présence active du développeur pour valider les 8 breakpoints (transition entre phases, validation du plan, choix worktree/team mode, etc.). Ce modèle fonctionne bien en journée de travail.

Le problème : le backlog contient souvent 30+ tâches pré-qualifiées (spec claire, complexité STANDARD) qui ne nécessitent pas de décision humaine intermédiaire. Exécuter ces tâches manuellement prend 2-3 jours pleins. Le temps de review inter-phase est essentiellement du temps perdu.

### 2.2 Opportunité

L'abonnement Claude Max (plan 5x) offre un quota significatif, et les soirées/weekends représentent ~60% du temps calendaire non exploité. En automatisant l'exécution des tâches pré-qualifiées, on peut :

- **Multiplier le throughput par 3-5x** : 15-30 tâches/weekend au lieu de 5-8 manuellement
- **Récupérer le temps développeur** : le lundi matin se résume à une review de PRs, pas à de l'exécution
- **Maintenir la qualité** : TDD enforced, self-review automatique, Feature Document pour traçabilité
- **Fail graceful** : une tâche en échec n'impacte pas les suivantes, et le développeur a les logs complets

### 2.3 Contraintes

1. **Quota Claude Max** : fenêtre glissante de 5h, ~45 sessions Sonnet estimées. Pas d'API de consultation directe du quota.
2. **Mode headless** : Claude Code via `claude -p` ne supporte pas l'interaction. Le skill doit être 100% autonome.
3. **Sécurité** : pas d'exécution de code non validé en production. Tout passe par PR + review humaine.
4. **Multi-projet** : le pipeline doit supporter Django (Gardel) et Symfony/React (autres projets) via le CLAUDE.md de chaque projet.
5. **Infrastructure VPS** : Ubuntu 24, user non-root dédié, résilience aux reboots maintenance.

---

## 3. Architecture Générale

### 3.1 Vue d'ensemble

Le flux s'exécute en séquentiel strict (une tâche à la fois). Le cron OpenClaw déclenche un cycle toutes les 30 minutes. Chaque cycle exécute jusqu'à 5 tâches (configurable), avec des gardes sur le quota et les échecs consécutifs.

```
Cron OpenClaw (toutes les 30 min)
    │
    ▼
pipeline-runner.sh
    │
    ├── 1. Health check (recovery post-crash)
    │   └── Détecter tâches "En cours" sans processus actif → marquer "Échoué"
    │
    ├── 2. Query Notion : tâches "À faire", triées par priorité puis complexité
    │
    ├── 3. Pour chaque tâche (séquentiel) :
    │   │
    │   ├── 3a. quota-checker.sh → suffisant ?
    │   │   ├── Oui → continuer
    │   │   └── Non → arrêter le cycle
    │   │
    │   ├── 3b. Update Notion → "En cours" + notif 🚀
    │   │
    │   ├── 3c. run-task.sh (worktree → Claude Code → parse JSON)
    │   │
    │   └── 3d. Traitement résultat :
    │       ├── SUCCESS → push + PR + Notion "En review" + notif ✅
    │       ├── PARTIAL → push + PR draft + Notion "En review (partiel)" + notif ⚠️
    │       └── FAILED  → cleanup + Notion "Échoué" + notif ❌
    │
    ├── 4. Heartbeat notification (résumé progression)
    │
    └── 5. Fin du cycle
```

**Flux nominal** : Notion (« À faire ») → OpenClaw poll → quota check → Notion (« En cours ») → notif démarrage → Claude Code (implement-auto EPCI complet) → parse JSON résultat → git push + PR → Notion (« En review ») → notif succès

**Flux d'échec** : ... → Claude Code (implement-auto) → échec détecté (timeout, test failures, hallucination) → cleanup worktree → Notion (« Échoué ») → notif erreur avec logs

### 3.2 Décisions d'architecture

**Exécution séquentielle (pas de parallélisme).** Le quota Claude Max est une ressource partagée. Deux tâches parallèles doubleraient la consommation et risqueraient le throttle. V2 pourra explorer le parallélisme si le quota le permet.

**Fan-out depuis main (pas de chainage de branches).** Chaque tâche crée son worktree depuis `origin/main`. Si deux tâches modifient le même fichier, le conflit est détecté au merge de la PR. Alternative rejetée : chaîner les branches (task-2 depuis task-1), trop fragile si task-1 échoue.

**Self-review par défaut (pas de subagent Opus).** Le skill implement-auto utilise une checklist de self-review au lieu d'invoquer un Code Reviewer Opus coûteux. Option `--with-review` pour les tâches critiques flaggées dans Notion. La vraie review reste humaine via la PR.

**JSON structuré comme contrat d'interface.** Le skill implement-auto produit un fichier JSON standardisé (status, métriques, erreurs, warnings). L'orchestrateur parse ce JSON pour décider des actions post-tâche. Pas de parsing de texte libre.

**Notion comme source de vérité unique.** Toutes les tâches, leur statut, les logs, les liens PR sont dans Notion. L'orchestrateur lit et écrit dans Notion. Pas de base de données séparée.

### 3.3 Contrat JSON de sortie (implement-auto → orchestrateur)

```json
{
  "status": "SUCCESS | PARTIAL | FAILED",
  "feature_slug": "auth-login",
  "branch": "feature/auth-login",
  "worktree_finalized": true,
  "feature_doc": "docs/features/auth-login-20260215.md",
  "metrics": {
    "files_created": 5,
    "files_modified": 3,
    "tests_added": 12,
    "tests_passing": 12,
    "coverage_percent": 87,
    "duration_seconds": 540,
    "components_total": 5,
    "components_succeeded": 5,
    "components_failed": 0
  },
  "phases_completed": ["init", "explore", "plan", "code", "review", "document", "memory"],
  "phases_failed": [],
  "checks": {
    "tests": "pass",
    "lint": "pass",
    "typecheck": "pass"
  },
  "errors": [],
  "warnings": []
}
```

Signification des statuts :
- **SUCCESS** : toutes les phases complètes, tous les checks passent
- **PARTIAL** : phases complètes mais certains composants en échec ou checks en warning
- **FAILED** : une phase a échoué (explore_hallucination, plan_validation_failed, code_repeated_failures, timeout, etc.)

---

## 4. Budget Tokens

Estimations basées sur le plan Claude Max 5x, modèle Sonnet par défaut. Les chiffres sont conservateurs et devront être affinés après les premiers runs réels.

| Phase | Tokens (Sonnet) | Subagents | Notes |
|-------|-----------------|-----------|-------|
| Init | ~2K | Aucun | Parse + worktree + Feature Doc |
| Explore | ~8K | Haiku (Task) | Subagent économique |
| Plan | ~12K | Sonnet (Task) | +15K si `--validate-plan` (Opus) |
| Code (TDD) | ~25-40K | Aucun | Variable selon composants |
| Review | ~5K | Aucun | +20K si `--with-review` (Opus) |
| Document + Finish | ~5K | Aucun | Feature Doc + vérifications |
| Memory + JSON | ~3K | Aucun | index.json + output structuré |
| **TOTAL (défaut)** | **~60-75K** | | **Sans flags optionnels** |
| **TOTAL (full)** | **~95-110K** | | **Avec --validate-plan + --with-review** |

**Projection weekend** : 30 tâches × 70K tokens = ~2.1M tokens. Sur une fenêtre de 48h avec renouvellement toutes les 5h, c'est faisable en théorie. Le quota checker (G1) empêchera le dépassement.

---

## 5. Analyse Premortem

Sept scénarios d'échec ont été identifiés et analysés. Chaque scénario a généré un ou plusieurs gaps (spécifications manquantes), intégrés dans les 4 specs détaillées.

### S1 — Quota épuisé après 12 tâches

Les tâches consomment 120K+ tokens au lieu de 55-70K estimés (retry, code complexe). La fenêtre 5h s'épuise après 4-5 tâches. Le pipeline ne traite que 40% du backlog weekend.

**Mitigation** : G1 (quota checker avant chaque tâche) + G2 (tri par complexité, simples d'abord).

### S2 — Boucle infinie, 40% du budget brûlé

Une tâche échoue au step Code, retry échoue aussi. Claude Code fait des retry internes (corrige, relance tests, recorrige) → 200K tokens avant le timeout de 20 minutes.

**Mitigation** : G3 (monitoring tokens temps réel) + circuit breaker interne au skill (max 2 retries par composant, abort après 3 échecs consécutifs).

### S3 — Conflits worktree entre tâches

Tâche 15 modifie `models.py`, tâche 18 aussi. Les deux créent leur worktree depuis `origin/main`. Tâche 18 ne voit pas les changements de tâche 15 → conflit au merge de la PR.

**Mitigation** : G4 (stratégie fan-out depuis main, conflits détectés à la PR, l'humain décide l'ordre de merge).

### S4 — Feature Document inutilisable le lundi

Les sections §2-§5 sont remplies avec des données correctes mais sans synthèse. Le lundi matin, impossible de comprendre le travail sans relire le diff complet.

**Mitigation** : G5 (résumé exécutif en haut du Feature Document : quoi, pourquoi, fichiers clés, décisions, warnings).

### S5 — Hallucination API dans Explore

Le subagent Haiku interprète mal un pattern. Le planner Sonnet planifie sur une mauvaise base. Le code implémente un appel à une méthode inexistante. Tests échouent, retry échoue → "Échoué".

**Mitigation** : G6 (sanity check automatique entre Explore et Plan, vérification que les fichiers/méthodes référencés existent réellement via Glob/Grep).

### S6 — VPS reboot pendant la nuit

Reboot maintenance 3h. OpenClaw redémarre mais la tâche interrompue laisse un worktree en état sale (fichiers modifiés non commités). La tâche suivante démarre, le state.json est incohérent.

**Mitigation** : G7 (health check au démarrage de chaque cycle cron, détecte les tâches "En cours" sans processus actif, marque "Échoué", cleanup worktree, notifie).

### S7 — Notifications silencieuses

Le bot Telegram rate-limite ou son token expire. Les 10 dernières tâches tournent sans notification. L'utilisateur ne sait pas que 5 ont échoué.

**Mitigation** : G8 (heartbeat toutes les heures + alarme si pas de heartbeat depuis 2h).

---

## 6. Gaps Identifiés

Le premortem a révélé 10 gaps dans la spécification initiale. Chaque gap est traité dans la spec correspondante.

| # | Gap identifié | Criticité | Spec cible |
|---|---------------|-----------|------------|
| G1 | Quota checker avant chaque tâche | 🔴 Critique | SPEC-02 |
| G2 | Tri tâches par complexité estimée | 🟢 Nice-to-have | SPEC-02 |
| G3 | Monitoring tokens temps réel | 🟠 Important | SPEC-02 |
| G4 | Stratégie base branch (conflits) | 🔴 Critique | SPEC-01 / SPEC-02 |
| G5 | Résumé exécutif Feature Document | 🟡 Important | SPEC-01 |
| G6 | Sanity check Explore→Plan | 🟠 Important | SPEC-01 |
| G7 | Health check post-crash / recovery | 🟠 Important | SPEC-02 |
| G8 | Heartbeat notifications | 🟢 Nice-to-have | SPEC-04 |
| G9 | Auth Claude Code (session expirée) | 🟠 Important | SPEC-02 |
| G10 | Rollback tâche échouée (cleanup) | 🟠 Important | SPEC-02 |

---

## 7. Vue d'ensemble par composant

### 7.1 SPEC-01 — Skill implement-auto

Adaptation du skill `implement` existant pour une exécution headless complète. Supprime les 8 breakpoints, les boîtes ASCII, et l'outil `AskUserQuestion`. Ajoute un JSON de sortie structuré, un sanity check post-explore (G6), un circuit breaker sur les composants en échec, et un résumé exécutif dans le Feature Document (G5).

**Différences clés avec implement :**

| Aspect | implement | implement-auto |
|--------|----------|----------------|
| Breakpoints | 8 (AskUserQuestion) | **Aucun** — interdit |
| Routing complexité | TINY→quick, STANDARD→EPCI | **Toujours STANDARD** (pré-qualifié) |
| Team mode | Auto-detect + confirmation | **Désactivé** par défaut |
| Worktree | Opt-in au breakpoint | **Toujours créé** automatiquement |
| Plan validator | Opus, obligatoire | **Optionnel** (flag `--validate-plan`) |
| Code reviewer | Subagent Opus | **Self-review** checklist |
| Output | Boîtes ASCII + suggestions | **JSON structuré** uniquement |

**Steps** : 00-init-auto → 01-explore-auto (+ sanity check) → 02-plan-auto (± validator) → 03-code-auto (TDD, circuit breaker) → 04-review-auto (self-review) → 05-document-auto (+ résumé) → 06-finish-auto → 07-memory-auto (JSON output)

**Flags** : `--validate-plan` (Plan Validator Opus), `--with-review` (Code Reviewer Opus). Désactivés par défaut.

### 7.2 SPEC-02 — Script orchestrateur

Trois scripts Bash + jq :

- **pipeline-runner.sh** : boucle principale avec health check, tri, guards (quota, échecs consécutifs), heartbeat
- **run-task.sh** : exécution d'une tâche (worktree → Claude Code → parse JSON → push → PR)
- **quota-checker.sh** : tracking interne + détection de throttle réactive dans les logs Claude Code

Fonctions clés : verrou anti-concurrence (lockfile + trap), health check post-crash (G7), tri priorité + complexité (G2), circuit breaker 3 échecs consécutifs, génération automatique du body PR avec métriques, vérification auth Claude Code (G9), cleanup worktree sur échec (G10).

### 7.3 SPEC-03 — Schéma Notion + export brainstorm

Base de données Notion « Dev Tasks » avec les propriétés :

- **Titre** (title) — Nom de la tâche / feature slug
- **Spec PRD** (rich text) — Contenu de la spec, structuré pour Claude Code
- **Projet** (select) — gardel, projet-symfony, etc.
- **Priorité** (select) — P0, P1, P2, P3
- **Complexité** (select + score numérique) — Simple (1), Moyenne (2), Complexe (3)
- **Statut** (select) — À faire, En cours, En review, En review (partiel), Échoué, Terminé
- **Branch** (text) — Nom de la branche Git
- **PR URL** (url) — Lien vers la Pull Request GitHub
- **Coût tokens** (number) — Tokens consommés
- **Logs** (rich text) — Logs d'exécution pipeline
- **Flags** (multi-select) — validate_plan, with_review

Inclut un mécanisme d'export depuis brainstorm : après une session brainstormer, générer automatiquement les tâches qualifiées dans Notion avec leur spec PRD structurée.

### 7.4 SPEC-04 — Notifications + kill switch

Bot Telegram (ou Discord) pour :

- **Notifications par tâche** : démarrage (🚀), succès (✅ avec lien PR), échec (❌ avec phase + erreur)
- **Heartbeat** toutes les heures : « Pipeline alive, X/Y tâches, Z échecs »
- **Alarme** si pas de heartbeat depuis 2h
- **Kill switch** : commande Telegram `/kill` pour arrêter le pipeline immédiatement (crée un fichier sentinelle `/tmp/pipeline-kill` vérifié par le runner avant chaque tâche)
- **Logs structurés** JSON pour parsing et debugging

---

## 8. Planning d'implémentation

Ordre basé sur les dépendances entre composants :

1. **SPEC-03 (Notion)** — Créer la base de données et les vues. Prérequis pour tout le reste. ~0.5 jour.
2. **SPEC-01 (implement-auto)** — Adapter le skill. Testable en isolation avec `claude -p`. ~2-3 jours.
3. **SPEC-02 (orchestrateur)** — Écrire les scripts. Connecte Notion + implement-auto + GitHub. ~1-2 jours.
4. **SPEC-04 (notifications)** — Bot Telegram + heartbeat + kill switch. ~0.5-1 jour.
5. **Intégration + test end-to-end** — Run complet avec 3-5 tâches test. Ajuster les seuils quota. ~1 jour.

**Total estimé : 5-7 jours** de travail effectif (pas nécessairement consécutifs). Première utilisation réelle ciblée sur un weekend test avec ~10 tâches du projet Gardel.

---

## 9. Hors scope V1

- **Parallélisme** : V1 est strictement séquentiel. Exploration repoussée à V2.
- **Auto-merge** : toutes les PRs nécessitent une review humaine. Pas de merge automatique.
- **Tâches LARGE/EPIC** : seules les tâches pré-qualifiées STANDARD passent par le pipeline. Les tâches complexes restent en interactif.
- **Déploiement continu** : le pipeline s'arrête à la PR. Le déploiement reste un processus manuel séparé.
- **Dashboard web** : la visibilité se fait via Notion et les notifications Telegram. Pas d'interface web dédiée en V1.

---

## 10. Glossaire

- **EPCI** — Explore → Plan → Code → Inspect. Méthodologie de développement assisté par IA, structurée en phases avec breakpoints de validation.
- **implement** — Skill Claude Code existant (interactif, avec breakpoints).
- **implement-auto** — Nouvelle variante autonome (headless, sans breakpoints).
- **OpenClaw** — Orchestrateur/scheduler open source utilisé pour déclencher les tâches cron.
- **Feature Document** — Document de traçabilité généré par le skill implement, documentant chaque phase.
- **Worktree** — Copie de travail Git isolée (`git worktree`), une par tâche pour éviter les conflits.
- **Fan-out** — Stratégie où chaque branche est créée depuis main (pas depuis la branche précédente).
- **Kill switch** — Mécanisme pour arrêter le pipeline immédiatement via commande Telegram.
- **Heartbeat** — Notification périodique confirmant que le pipeline est actif et fonctionne.
- **Circuit breaker** — Mécanisme d'arrêt automatique après N échecs consécutifs (au niveau composant dans implement-auto, au niveau tâche dans l'orchestrateur).
