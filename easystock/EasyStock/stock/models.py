from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Catégories"


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Fournisseurs"


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField(default=0)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produits'
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produits'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['-date_ajout']

    @property
    def stock_faible(self):
        return self.quantite < 5


class MouvementStock(models.Model):
    TYPES = [
        ('ajout', 'Ajout de stock'),
        ('retrait', 'Retrait de stock'),
        ('modification', 'Modification'),
    ]
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='mouvements'
    )
    type_mouvement = models.CharField(max_length=20, choices=TYPES)
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.date})"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Mouvements de stock"