from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Categorie, Fournisseur, Produit, MouvementStock
from .serializers import (
    CategorieSerializer, FournisseurSerializer,
    ProduitSerializer, MouvementStockSerializer
)


# ─────────────────────────────────────────────
#  PAGINATION
# ─────────────────────────────────────────────

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ─────────────────────────────────────────────
#  AUTHENTIFICATION
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username et password sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        if not user.is_active:
            return Response({'error': 'Ce compte est désactivé.'}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })
    return Response({'error': 'Identifiants incorrects.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Token refresh requis.'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Token invalide.'}, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    total_produits = Produit.objects.count()
    total_categories = Categorie.objects.count()
    total_fournisseurs = Fournisseur.objects.count()
    valeur_stock = Produit.objects.aggregate(total=Sum('prix'))['total'] or 0
    produits_stock_faible = Produit.objects.filter(quantite__lt=5, quantite__gt=0).count()
    produits_rupture = Produit.objects.filter(quantite=0).count()
    il_y_a_7_jours = timezone.now() - timedelta(days=7)
    mouvements_recents = MouvementStock.objects.filter(date__gte=il_y_a_7_jours).count()
    top_produits = list(Produit.objects.order_by('-quantite')[:5].values('nom', 'quantite'))
    repartition = list(Categorie.objects.annotate(nb_produits=Count('produits')).values('nom', 'nb_produits'))

    return Response({
        "total_produits": total_produits,
        "total_categories": total_categories,
        "total_fournisseurs": total_fournisseurs,
        "valeur_totale_stock": float(valeur_stock),
        "produits_stock_faible": produits_stock_faible,
        "produits_rupture": produits_rupture,
        "mouvements_7_derniers_jours": mouvements_recents,
        "top_produits_en_stock": top_produits,
        "repartition_par_categorie": repartition,
    })


# ─────────────────────────────────────────────
#  VIEWSETS CRUD
# ─────────────────────────────────────────────

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        """GET /api/categories/{id}/produits/"""
        categorie = self.get_object()
        produits = categorie.produits.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)


class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        """GET /api/fournisseurs/{id}/produits/"""
        fournisseur = self.get_object()
        produits = fournisseur.produits.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)


class MouvementStockViewSet(viewsets.ModelViewSet):
    serializer_class = MouvementStockSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = MouvementStock.objects.select_related('produit', 'utilisateur').all()
        produit_id = self.request.query_params.get('produit')
        if produit_id:
            queryset = queryset.filter(produit__id=produit_id)
        type_mouvement = self.request.query_params.get('type')
        if type_mouvement:
            queryset = queryset.filter(type_mouvement=type_mouvement)
        date_debut = self.request.query_params.get('date_debut')
        if date_debut:
            queryset = queryset.filter(date__gte=date_debut)
        date_fin = self.request.query_params.get('date_fin')
        if date_fin:
            queryset = queryset.filter(date__lte=date_fin)
        return queryset


class ProduitViewSet(viewsets.ModelViewSet):
    serializer_class = ProduitSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = Produit.objects.select_related('categorie', 'fournisseur').all()

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(nom__icontains=search)

        categorie_id = self.request.query_params.get('categorie')
        if categorie_id:
            queryset = queryset.filter(categorie__id=categorie_id)

        fournisseur_id = self.request.query_params.get('fournisseur')
        if fournisseur_id:
            queryset = queryset.filter(fournisseur__id=fournisseur_id)

        prix_min = self.request.query_params.get('prix_min')
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)

        prix_max = self.request.query_params.get('prix_max')
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)

        ordering = self.request.query_params.get('ordering')
        allowed = ['prix', '-prix', 'nom', '-nom', 'quantite', '-quantite', 'date_ajout', '-date_ajout']
        if ordering in allowed:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        produit = serializer.save()
        if produit.quantite > 0:
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='ajout',
                quantite=produit.quantite,
                note="Stock initial à la création du produit",
                utilisateur=self.request.user if self.request.user.is_authenticated else None
            )

    def perform_update(self, serializer):
        ancienne_quantite = self.get_object().quantite
        produit = serializer.save()
        nouvelle_quantite = produit.quantite
        if nouvelle_quantite != ancienne_quantite:
            diff = nouvelle_quantite - ancienne_quantite
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='ajout' if diff > 0 else 'retrait',
                quantite=abs(diff),
                note=f"Modification : {ancienne_quantite} → {nouvelle_quantite}",
                utilisateur=self.request.user if self.request.user.is_authenticated else None
            )

    def destroy(self, request, *args, **kwargs):
        produit = self.get_object()
        nom = produit.nom
        produit.delete()
        return Response({'message': f'Produit "{nom}" supprimé avec succès.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stock_faible(self, request):
        """GET /api/produits/stock_faible/ — quantité entre 1 et 4"""
        produits = Produit.objects.filter(quantite__gt=0, quantite__lt=5)
        serializer = self.get_serializer(produits, many=True)
        return Response({'count': produits.count(), 'produits': serializer.data})

    @action(detail=False, methods=['get'])
    def rupture_stock(self, request):
        """GET /api/produits/rupture_stock/ — quantité = 0"""
        produits = Produit.objects.filter(quantite=0)
        serializer = self.get_serializer(produits, many=True)
        return Response({'count': produits.count(), 'produits': serializer.data})

    @action(detail=True, methods=['get'])
    def historique(self, request, pk=None):
        """GET /api/produits/{id}/historique/ — historique d'un produit"""
        produit = self.get_object()
        mouvements = MouvementStock.objects.filter(produit=produit)
        serializer = MouvementStockSerializer(mouvements, many=True)
        return Response({
            'produit': produit.nom,
            'total_mouvements': mouvements.count(),
            'historique': serializer.data
        })