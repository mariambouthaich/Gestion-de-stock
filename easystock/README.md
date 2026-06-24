# EasyStock — Système de Gestion des Stocks

Application full-stack de gestion d'inventaire avec **Vue 3** (frontend) + **Django REST Framework** (backend).

---

## 🗂 Structure du projet

```
easystock/
├── EasyStock/              # Backend Django
│   ├── backend/            # Configuration Django (settings, urls, wsgi)
│   ├── stock/              # App principale (models, views, serializers, urls)
│   ├── db.sqlite3          # Base de données SQLite
│   ├── manage.py
│   └── requirements.txt
├── src/                    # Frontend Vue 3
│   ├── components/
│   │   ├── DashboardLayout.vue   # Layout principal avec sidebar
│   │   └── ui/                   # Composants réutilisables
│   │       ├── LoadingSpinner.vue
│   │       ├── ConfirmModal.vue
│   │       ├── Pagination.vue
│   │       └── EmptyState.vue
│   ├── router/index.js           # Vue Router (toutes les routes)
│   ├── services/                 # Couche API (Axios)
│   │   ├── api.js                # Instance Axios + intercepteurs
│   │   ├── auth.js               # Login / Logout / JWT
│   │   ├── categories.js
│   │   ├── products.js
│   │   ├── suppliers.js
│   │   ├── stockMovements.js
│   │   └── stats.js
│   ├── views/
│   │   ├── Home.vue              # Landing page
│   │   ├── Login.vue             # Page de connexion
│   │   ├── Dashboard.vue         # Vue d'ensemble (KPIs)
│   │   ├── ProductsAdmin.vue     # CRUD Produits
│   │   ├── Categories.vue        # CRUD Catégories
│   │   ├── Suppliers.vue         # CRUD Fournisseurs
│   │   ├── Stock.vue             # Historique mouvements
│   │   ├── Users.vue             # Lien vers Django Admin
│   │   └── Settings.vue          # Paramètres & statut API
│   ├── App.vue
│   ├── main.js
│   └── styles.css                # Design system (CSS variables + classes)
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── .env
```

---

## 🚀 Lancement

### 1. Backend Django

```bash
cd EasyStock

# Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# (Optionnel) Charger les données initiales
python manage.py loaddata stock/fixtures/donnees_initiales.json

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

Le backend sera disponible sur **http://127.0.0.1:8000**

### 2. Frontend Vue 3

```bash
# À la racine du projet (là où est package.json)
npm install
npm run dev
```

Le frontend sera disponible sur **http://localhost:5173**

---

## 🔑 API Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/login/` | Obtenir un token JWT |
| GET | `/api/stats/` | KPIs du dashboard |
| GET/POST | `/api/produits/` | Liste & créer produits |
| GET/PUT/DELETE | `/api/produits/{id}/` | Détail, modifier, supprimer |
| GET | `/api/produits/stock_faible/` | Produits stock < 5 |
| GET | `/api/produits/rupture_stock/` | Produits stock = 0 |
| GET/POST | `/api/categories/` | Liste & créer catégories |
| GET/PUT/DELETE | `/api/categories/{id}/` | Détail, modifier, supprimer |
| GET/POST | `/api/fournisseurs/` | Liste & créer fournisseurs |
| GET/PUT/DELETE | `/api/fournisseurs/{id}/` | Détail, modifier, supprimer |
| GET | `/api/mouvements/` | Historique des mouvements |

---

## ✅ Fonctionnalités

- **Authentification JWT** : login sécurisé, token stocké en localStorage
- **Dashboard** : 7 KPIs, top produits, répartition par catégorie, alertes stock
- **Produits** : CRUD complet avec filtres (nom, catégorie, fournisseur), badges de stock
- **Catégories** : CRUD avec recherche et pagination
- **Fournisseurs** : CRUD avec tous les champs (nom, email, téléphone, adresse)
- **Mouvements de stock** : liste filtrée (type, date début/fin) avec pagination
- **Sidebar** : collapsible, navigation claire, indicateur de page active
- **UI** : design system cohérent (dark theme, CSS variables, composants réutilisables)
- **Responsive** : sidebar mobile, menu hamburger

---

## 🛠 Stack technique

| Couche | Technologie |
|--------|-------------|
| Frontend | Vue 3 (Composition API) |
| Routing | Vue Router 4 |
| HTTP | Axios |
| Styles | Tailwind CSS 3 + CSS custom |
| Backend | Django 5 + DRF |
| Auth | SimpleJWT |
| DB | SQLite (dev) |
