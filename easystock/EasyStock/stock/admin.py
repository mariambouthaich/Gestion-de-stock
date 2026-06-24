from django.contrib import admin
from .models import Categorie, Fournisseur, Produit, MouvementStock


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'telephone', 'adresse']
    search_fields = ['nom', 'email']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'quantite', 'categorie', 'fournisseur', 'stock_faible', 'date_ajout']
    list_filter = ['categorie', 'fournisseur']
    search_fields = ['nom', 'description']
    readonly_fields = ['date_ajout', 'date_modification']

    def stock_faible(self, obj):
        return obj.stock_faible
    stock_faible.boolean = True
    stock_faible.short_description = 'Stock faible ?'


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['produit', 'type_mouvement', 'quantite', 'date', 'utilisateur']
    list_filter = ['type_mouvement']
    search_fields = ['produit__nom']
    readonly_fields = ['date']