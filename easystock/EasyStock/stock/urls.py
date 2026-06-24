from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategorieViewSet, FournisseurViewSet,
    ProduitViewSet, MouvementStockViewSet,
    dashboard_stats, login_view, logout_view
)

router = DefaultRouter()
router.register(r'categories', CategorieViewSet)
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'mouvements', MouvementStockViewSet, basename='mouvement')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', dashboard_stats, name='stats'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]