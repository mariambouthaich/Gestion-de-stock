import django_filters
from .models import Produit, MouvementStock


class ProduitFilter(django_filters.FilterSet):
    # Recherche par nom (insensible à la casse)
    nom = django_filters.CharFilter(lookup_expr='icontains')

    # Recherche par description
    description = django_filters.CharFilter(lookup_expr='icontains')

    # Filtrer par prix entre deux valeurs
    prix_min = django_filters.NumberFilter(field_name='prix', lookup_expr='gte')
    prix_max = django_filters.NumberFilter(field_name='prix', lookup_expr='lte')

    # Filtrer par quantité
    quantite_min = django_filters.NumberFilter(field_name='quantite', lookup_expr='gte')
    quantite_max = django_filters.NumberFilter(field_name='quantite', lookup_expr='lte')

    # Filtrer par catégorie (par nom)
    categorie_nom = django_filters.CharFilter(
        field_name='categorie__nom',
        lookup_expr='icontains'
    )

    # Filtrer par fournisseur (par nom)
    fournisseur_nom = django_filters.CharFilter(
        field_name='fournisseur__nom',
        lookup_expr='icontains'
    )

    # Filtrer produits en stock faible
    stock_faible = django_filters.BooleanFilter(method='filter_stock_faible')

    def filter_stock_faible(self, queryset, name, value):
        if value:
            return queryset.filter(quantite__lt=5)
        return queryset.filter(quantite__gte=5)

    class Meta:
        model = Produit
        fields = [
            'nom', 'description', 'categorie', 'fournisseur',
            'prix_min', 'prix_max', 'quantite_min', 'quantite_max',
            'categorie_nom', 'fournisseur_nom', 'stock_faible'
        ]


class MouvementStockFilter(django_filters.FilterSet):
    # Filtrer par date
    date_debut = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_fin = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte')

    # Filtrer par produit (par nom)
    produit_nom = django_filters.CharFilter(
        field_name='produit__nom',
        lookup_expr='icontains'
    )

    class Meta:
        model = MouvementStock
        fields = ['type_mouvement', 'produit', 'date_debut', 'date_fin', 'produit_nom']