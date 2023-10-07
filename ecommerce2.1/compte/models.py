from django.contrib.auth.models import AbstractUser
from django.db import models

class Client(AbstractUser):
    choix = [
        ("Togo", "Togo"), ("Ghana", "Ghana"), ("Benin", "Benin"), ("Côte d'ivoire", "Côte d'ivoire"),
        ("Sénégal", "Sénégal"), ("Mali", "Mali"), ("Caméroun", "Cameroun"), ("Guinée Bisseau", "Guinée Bisseau"),
        ("Cap-vert", "Cap-vert"), ("Niger", "Niger"), ("Nigeria", "Nigeria"), ("Congo", "Congo"),
        ("Tchad", "Tchad"), ("Soudan", "Soudan")
    ]
    pays = models.CharField(max_length=40, choices=choix)
    profil = models.ImageField(upload_to='profils', blank=False, null=False)