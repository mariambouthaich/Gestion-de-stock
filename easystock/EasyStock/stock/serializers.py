from rest_framework import serializers
from .models import Categorie, Fournisseur, Produit, MouvementStock


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


class MouvementStockSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)

    class Meta:
        model = MouvementStock
        fields = [
            'id', 'produit', 'produit_nom',
            'type_mouvement', 'quantite',
            'date', 'note', 'utilisateur', 'utilisateur_nom'
        ]


class ProduitSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    stock_faible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Produit
        fields = [
            'id', 'nom', 'description', 'prix', 'quantite',
            'categorie', 'categorie_nom',
            'fournisseur', 'fournisseur_nom',
            'stock_faible', 'date_ajout', 'date_modification'
        ]

    def validate_prix(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être supérieur à 0.")
        return value

    def validate_quantite(self, value):
        if value < 0:
            raise serializers.ValidationError("La quantité ne peut pas être négative.")
        return value

    def validate_nom(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Le nom doit avoir au moins 2 caractères.")
        return value