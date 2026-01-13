# Intégration des sources hétérogènes

## Types de sources supportés

| Type | Identification | Extraction | Métadonnées |
|------|---------------|------------|-------------|
| **Transcript YouTube** | Timecodes [00:00], mention chaîne | Parsing direct | Titre, chaîne, durée |
| **Transcript réunion** | Noms + ":", "réunion", "call" | Parsing structuré | Participants, date |
| **PDF** | Fichier .pdf uploadé | Extraction texte | Titre, auteur, pages |
| **URL Article** | http(s):// | web_fetch | Titre, auteur, date, site |
| **URL Doc** | docs.*, readme | web_fetch | Version, dernière màj |
| **Notes brutes** | Aucun pattern | Parsing libre | — |
| **CR existant** | Structure markdown | Parsing structuré | Date, participants |

---

## Workflow d'intégration

```
1. RÉCEPTION
   └── Identifier type de chaque source

2. NORMALISATION
   └── Convertir en structure commune

3. INDEXATION
   └── Extraire thèmes et entités
   └── Construire index croisé

4. FUSION
   └── Merger par thème
   └── Gérer contradictions

5. GÉNÉRATION
   └── Rapport unifié avec traçabilité
```

---

## Phase 1 : Identification automatique

### Règles de détection

```yaml
Transcript YouTube:
  patterns:
    - Timecodes: "[00:00]" ou "(00:00)" ou "00:00 -"
    - Mots-clés: "YouTube", nom de chaîne connu
    - Structure: dialoguée sans noms formels
  
Transcript réunion:
  patterns:
    - Format: "Nom:" ou "Nom :"
    - Mots-clés: "réunion", "call", "meeting", "point"
    - Contenu: actions, décisions identifiables

PDF uploadé:
  patterns:
    - Extension: .pdf détectée
    - Contenu: texte extrait structuré

URL:
  patterns:
    - Commence par: http:// ou https://
    - Domaine: détectable et accessible

Notes brutes:
  patterns:
    - Aucun des patterns ci-dessus
    - Texte non structuré
```

---

## Phase 2 : Normalisation

### Structure intermédiaire commune

```yaml
Source:
  id: "SRC_001"
  type: "youtube | reunion | pdf | url | notes"
  
  metadata:
    titre: "..."
    auteur: "..." # ou null
    date: "2025-01-13" # ou null  
    url: "..." # si applicable
    duree: "45min" # si applicable
    fiabilite: 4 # score 1-5
  
  contenu:
    texte_brut: "..."
    sections:
      - titre: "Introduction"
        contenu: "..."
        position: "0-500" # chars ou timecode
    
  entites:
    personnes: ["Jean", "Marie"]
    outils: ["Claude Code", "React"]
    concepts: ["API", "workflow"]
    dates: ["vendredi", "Q1 2025"]
    
  themes:
    - nom: "Installation"
      poids: 0.8
      extraits: ["...", "..."]
```

### Traitement par type

| Type | Normalisation spécifique |
|------|-------------------------|
| YouTube | Nettoyer timecodes, regrouper par segments, détecter changements de sujet |
| Réunion | Parser interventions, extraire actions/décisions existantes |
| PDF | Conserver structure (titres), garder pagination pour références |
| URL | Extraire contenu principal, ignorer navigation/pubs |
| Notes | Détecter listes/bullets, structurer si possible |

---

## Phase 3 : Indexation thématique

### Construction de l'index

```
Source 1 ──┬── Thème A ──┬── Source 1
           ├── Thème B ──┼── Source 2
           └── Thème C ──┴── Source 3
                         
Source 2 ──┬── Thème B
           ├── Thème D
           └── Thème E
                         
Source 3 ──┬── Thème A
           ├── Thème C
           └── Thème F
```

### Structure de l'index

```yaml
Index:
  themes:
    - nom: "Installation Claude Code"
      sources:
        - id: "SRC_001"
          extraits: ["Pour installer...", "npm install..."]
          position: "03:45-05:20"
        - id: "SRC_002"  
          extraits: ["Chapter 2: Setup"]
          position: "pages 12-15"
      couverture: "2/3 sources (66%)"
      contradictions: false
      
    - nom: "Limitations"
      sources:
        - id: "SRC_001"
          extraits: ["Limite à 100k tokens"]
        - id: "SRC_003"
          extraits: ["Limite à 200k tokens"]
      couverture: "2/3 sources"
      contradictions: true
      resolution: "Vérifier source officielle"
```

---

## Phase 4 : Fusion intelligente

### Règles de priorité

| Situation | Règle |
|-----------|-------|
| Information unique | Inclure avec [N] |
| Information concordante | Citer source la plus fiable |
| Information contradictoire | Documenter les deux, chercher primaire |
| Information datée différemment | Prioriser la plus récente |
| Information partielle | Combiner, tracer chaque fragment |

### Algorithme de fusion

```
POUR chaque thème :
  1. Collecter extraits de toutes sources
  2. Trier par fiabilité (⭐)
  3. Trier par date (récent prioritaire)
  4. SI contradiction :
     a. Chercher source primaire (web si besoin)
     b. OU documenter les deux positions
  5. Fusionner avec traçabilité [1][2]
  6. Calculer score de confiance
```

### Gestion des contradictions

| Type | Action |
|------|--------|
| Factuelle | Chercher source primaire, adopter si trouvée |
| Opinion | Documenter les deux positions |
| Temporelle | Prioriser la plus récente, mentionner évolution |
| Incertaine | Marquer "⚠️ non vérifié" |

---

## Phase 5 : Génération du rapport

### Ordre de présentation

1. Informations concordantes multi-sources (haute confiance)
2. Informations source unique fiable (⭐⭐⭐⭐+)
3. Informations source unique moins fiable (avec mention)
4. Informations contradictoires (avec analyse)
5. Lacunes identifiées

### Tableau de sources (obligatoire niveau ≥3)

```markdown
## 📚 Sources analysées

| # | Type | Source | Fiabilité | Thèmes | Date |
|---|------|--------|-----------|--------|------|
| [1] | 🎬 | YouTube "Tutorial" | ⭐⭐⭐⭐ | Install, Usage | 2025-01 |
| [2] | 📄 | Doc PDF v2 | ⭐⭐⭐⭐⭐ | Install, API | 2025-01 |
| [3] | 💬 | CR Réunion 12/01 | ⭐⭐⭐ | Retours, Bugs | 2025-01 |

### Couverture thématique

| Thème | Sources | Confiance |
|-------|---------|-----------|
| Installation | [1][2] | ⭐⭐⭐⭐⭐ |
| Utilisation | [1][3] | ⭐⭐⭐⭐ |
| Limitations | [2][3] ⚠️ | ⭐⭐⭐ |
```

### Exemple de paragraphe fusionné

```markdown
L'installation de Claude Code se fait via npm [1] ou depuis le site 
Anthropic [2]. Le processus prend environ 5 minutes [1] et nécessite 
Node.js 18+ [2][🌐1].

> ⚠️ **Note** : La source [1] mentionne Node 16+, mais la documentation 
> officielle [🌐1] indique Node 18+. Version officielle retenue.
```
