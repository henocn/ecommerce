
from django.urls import path
from boutique.views import ajouter_article, vider_panier
from boutique.views import index, detailCategorie, detailProduit, statistique, panier, ajouter_au_panier


urlpatterns = [
    path('', index, name="index"),
    path("ajouter/", ajouter_article, name="ajouter_article"),
    path('stat/', statistique, name="statistique"),
    path('panier/', panier, name="panier"),
    path('panier/supprimer/', vider_panier, name="vider_panier"),
    path('panier/ajouter/<str:slugCat>/<str:slugPro>/', ajouter_au_panier , name="ajouter_au_panier"),
    path('<str:slugCat>/', detailCategorie, name="detailCategorie"),
    path('<str:slugCat>/<str:slugPro>/', detailProduit, name="detailProduit")
]