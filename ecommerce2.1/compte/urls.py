from django.urls import path
from compte.views import inscription, connexion, deconnexion, modifier_mdp

urlpatterns = [
    path("inscription/", inscription, name = "inscription"),
    path("connexion/", connexion, name = "connexion"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("modifier/", modifier_mdp, name="modifier")
]