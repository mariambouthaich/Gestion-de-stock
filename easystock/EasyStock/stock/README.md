# Backend — Gestion de Stock

## Technologies
- Python 3.x
- Django
- Django REST Framework
- SQLite

## Installation

git clone <lien_du_projet>
cd backend
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## API Endpoints

### Produits
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /api/produits/ | Liste tous les produits |
| POST | /api/produits/ | Créer un produit |
| GET | /api/produits/{id}/ | Détail d'un produit |
| PUT | /api/produits/{id}/ | Modifier un produit |
| DELETE | /api/produits/{id}/ | Supprimer un produit |
| GET | /api/produits/?search=nom | Recherche par nom |
| GET | /api/produits/?categorie=1 | Filtrer par catégorie |
| GET | /api/produits/stock_faible/ | Produits quantité < 5 |

### Catégories
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /api/categories/ | Liste toutes les catégories |
| POST | /api/categories/ | Créer une catégorie |
| GET | /api/categories/{id}/ | Détail d'une catégorie |
| PUT | /api/categories/{id}/ | Modifier une catégorie |
| DELETE | /api/categories/{id}/ | Supprimer une catégorie |

### Statistiques
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /api/stats/ | Statistiques globales du stock |

## Format JSON — Produit
{
    "id": 1,
    "nom": "Clavier",
    "description": "Clavier mécanique",
    "prix": "150.00",
    "quantite": 10,
    "categorie": 1,
    "categorie_nom": "Informatique",
    "date_ajout": "2026-05-07T18:48:00Z",
    "date_modification": "2026-05-07T18:48:00Z"
}