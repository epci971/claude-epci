---

# **Documentation — Intégration de React dans un projet Django (modèle “React dans les templates Django”)**

## **1. Objectif du document**

Ce guide présente la méthode moderne (2025) permettant d’intégrer **React** au sein d’un projet **Django monolithique**, sans créer une application frontend distincte.

Dans cette approche :

- Django reste **responsable du rendu des pages HTML**.
- React est utilisé pour **des composants interactifs locaux**, intégrés dans ces pages.
- L’ensemble est compilé par **Vite**, un bundler rapide, moderne et simple à intégrer.

Ce modèle combine les forces de Django (templates, sécurité, permissions, admin, simplicité) avec la puissance de React (composants dynamiques, UX moderne).

---

# **2. Pourquoi intégrer React dans Django ?**

Cette architecture hybride est idéale dans des projets métiers complexes (ex : Gardel), car elle permet :

### **2.1. Un monolithe Django simple à maintenir**

- Pas de duplication backend/API.
- Pas de complexité SPA (CORS, tokens, déploiement séparé…).
- Un seul Docker, un seul CI/CD.

### **2.2. Un enrichissement progressif**

On ajoute React **seulement là où c’est utile** :

- tableaux riches,
- graphiques,
- formulaires avancés,
- interactions complexes,
- filtres,
- sélecteurs dynamiques,
- widget de cartographie,
- timeline métier…

### **2.3. Une UX moderne, sans refonte complète**

Les pages restent rendues par Django, et React apporte une couche d’interactivité supplémentaire.

---

# **3. Architecture technique recommandée**

```
project/
│
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── apps/
│   ├── templates/
│   └── static/
│
└── frontend/
    ├── index.html (optionnel)
    ├── src/
    │     ├── main.jsx
    │     └── components/
    ├── vite.config.js
    ├── package.json
    └── dist/  (généré par Vite lors du build)

```

### **Rôle des dossiers :**

- `backend/` → Django (routes, templates, API, logique métier)
- `frontend/` → code React + Vite
- `dist/` → bundles compilés, servis par Django via `collectstatic`

---

# **4. Fonctionnement général : React dans une page Django**

1. Django rend une page HTML classique via un template.
2. À l’intérieur, on inclut :
    - **un conteneur** `<div id="mon-composant">`
    - **le bundle JS/React généré par Vite**
3. React monte un composant dans ce conteneur.

Exemple côté template :

```html
<!-- templates/labo/detail.html -->
<div id="react-kpi-tendance" data-initial="{{ donnees|safe }}"></div>

<script type="module" src="{% static 'assets/main.js' %}"></script>

```

Exemple côté React :

```jsx
import React from "react";
import { createRoot } from "react-dom/client";
import KpiTendance from "./components/KpiTendance.jsx";

const el = document.getElementById("react-kpi-tendance");
if (el) {
    const data = JSON.parse(el.dataset.initial);
    createRoot(el).render(<KpiTendance initialData={data} />);
}

```

---

# **5. Installation et configuration étape par étape**

## **5.1. Installation du dossier frontend React + Vite**

Dans le dossier `frontend/` :

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install

```

Cela crée une structure de base React (React 18/19, JSX, HMR…).

---

## **5.2. Configuration de Vite**

Créer un fichier `vite.config.js` :

```jsx
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
    plugins: [react()],
    base: '/static/assets/',      // Django servira ici
    build: {
        outDir: '../backend/static/assets',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'src/main.jsx'),
            },
        }
    },
})

```

---

## **5.3. Compilation des assets**

Développement :

```bash
npm run dev

```

Production :

```bash
npm run build

```

Vite compile les bundles dans `backend/static/assets/`.

Django pourra les servir via `collectstatic`.

---

# **6. Intégrer un composant React dans un template Django**

## **6.1. Placer un conteneur dans la page Django**

```html
<!-- templates/production/dashboard.html -->
<div id="react-tableau-production"
     data-json="{{ tableau_json|safe }}">
</div>

<script type="module" src="{% static 'assets/main.js' %}"></script>

```

**Bonnes pratiques :**

- Toujours utiliser `data-*` pour passer des données simples.
- Toujours utiliser `|safe` lorsque JSON est valide.
- Ne pas mettre de logique JS dans le template (React s'en occupe).

---

## **6.2. Récupérer le conteneur et monter le composant**

`src/main.jsx` :

```jsx
import React from "react";
import { createRoot } from "react-dom/client";
import TableauProduction from "./components/TableauProduction.jsx";

const id = "react-tableau-production";
const el = document.getElementById(id);

if (el) {
    const data = JSON.parse(el.dataset.json);
    createRoot(el).render(<TableauProduction initialData={data} />);
}

```

---

# **7. Communication Django ↔ React**

## **7.1. Données injectées depuis Django**

Utiliser la technique :

```html
data-json="{{ data|safe }}"

```

→ Pas besoin d’appel AJAX pour initialiser le composant.

---

## **7.2. Communication API (Django REST Framework)**

Pour les interactions dynamiques :

```jsx
fetch("/api/production/kpi/")
  .then(r => r.json())
  .then(setKpis);

```

Versions sécurisées via session/cookie (csrftoken auto).

---

# **8. Organisation du code React pour Django**

Organisation recommandée :

```
frontend/src/
    main.jsx              # point d'entrée, montage conditionnel
    utils/
    hooks/
    components/
        TableauProduction.jsx
        GraphiqueQualite.jsx
        UploadFichier.jsx

```

Principe :

- **1 composant React = 1 zone interactive dans un template Django**
- Ne jamais faire une SPA cachée
- Montages conditionnels (`if (document.getElementById('...'))`)

---

# **9. Avantages pour un projet industriel (comme Gardel)**

### ✔ Monolithe Django intact

Permissions, sécurité, DRF, logique métier inchangée.

### ✔ UX moderne

Sans réécrire tout le site.

### ✔ Contrôle fin

On active React uniquement sur certaines pages.

### ✔ Déploiement simple

1 seul Docker, 1 seul Nginx, 1 seul CI/CD.

### ✔ Compatible avec le rythme industriel

Pas besoin d’une équipe dédiée frontend.

---

# **10. Bonnes pratiques**

### **10.1. Côté Django**

- Centraliser les templates dans des apps dédiées.
- Utiliser DRF pour les endpoints JSON.
- Ne pas inclure de JS inline non contrôlé.
- Charger les bundles via `{% static %}`.

### **10.2. Côté React**

- Un composant par zone interactive.
- Respecter la logique "islands architecture".
- Préférer React 19 + Server Components **uniquement si nécessaire**.
- Préférer les libraries légères (Recharts, Zustand, etc.).

### **10.3. Côté Vite**

- Toujours utiliser un output dans `/static/assets/`.
- Toujours utiliser `base: '/static/assets/'`.
- Utiliser HMR en dev via un proxy Django si besoin.

---

# **11. Exemple complet : création d'un composant React et intégration**

## **Étape 1 — Créer le composant**

`frontend/src/components/KpiBar.jsx` :

```jsx
export default function KpiBar({ value }) {
    return (
        <div className="kpi-bar">
            <div className="kpi-value">{value}%</div>
        </div>
    );
}

```

## **Étape 2 — Ajouter le conteneur dans un template Django**

```html
<div id="kpi-bar" data-value="{{ kpi }}"></div>
<script type="module" src="{% static 'assets/main.js' %}"></script>

```

## **Étape 3 — Monter le composant**

`src/main.jsx` :

```jsx
import { createRoot } from "react-dom/client";
import KpiBar from "./components/KpiBar";

const el = document.getElementById("kpi-bar");
if (el) {
    const value = parseFloat(el.dataset.value);
    createRoot(el).render(<KpiBar value={value} />);
}

```

---

# **12. Check-list rapide**

### **Pour intégrer React dans Django :**

- [x] Créer un dossier `frontend/` séparé
- [x] Installer Vite + React
- [x] Configurer l’output vers `backend/static/`
- [x] Appeler le bundle dans les templates Django
- [x] Monter les composants via `createRoot()`
- [x] Injecter les données via `data-*` ou API DRF
- [x] Tester en dev avec `npm run dev`
- [x] Compiler en prod avec `npm run build`
- [x] Utiliser `collectstatic` pour diffuser les assets

---

# **13. Conclusion**

Ce modèle “**React dans Django**” est **la meilleure pratique moderne** pour un projet monolithique nécessitant :

- une UI enrichie par endroits,
- un backend robuste et centralisé,
- une maintenance simple,
- une montée en compétence rapide des développeurs.

Il offre le meilleur équilibre entre simplicité Django et puissance de React.

---