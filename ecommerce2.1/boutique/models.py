from django.utils import timezone
from datetime import timedelta, datetime
from django.db import models
from django.utils.text import slugify
from ecommerce.settings import AUTH_USER_MODEL

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Product(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    nom = models.CharField(max_length=40)
    slug = models.SlugField(blank= True, editable=False)
    prixDachat = models.IntegerField( verbose_name="Prix d'achat", default=0)
    prixDeVente = models.IntegerField( verbose_name="Prix de vente", blank=True)
    quantite = models.IntegerField(default=1)
    detail = models.TextField()
    image = models.ImageField(upload_to='poduits', blank=False, null=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nom}")
        if not self.prixDeVente:
            pv = int(self.prixDachat + self.prixDachat * 10 / 100)
            self.prixDeVente = self.arrondir(pv)
        super(Product, self).save(*args, **kwargs)

    def arrondir(self, prix):
        a = list(str(prix))
        if len(a) < 5:
            unite = int(a[-2] + a[-1])
            prix = prix - unite
            if unite == 0:
                pass
            elif unite < 51:
                unite = 50
            elif unite < 100:
                unite = 100
        elif len(a) == 5:
            unite = int(a[-2] + a[-1])
            prix = prix - unite
            if unite == 0:
                pass
            elif unite < 21:
                unite = 0
            elif unite < 100:
                unite = 100
        elif len(a) == 6:
            unite = int(a[-3] + a[-2] + a[-1])
            prix = prix - unite
            if unite == 0:
                pass
            elif unite < 501:
                unite = 500
            elif unite < 1000:
                unite = 1000

        return prix + unite

    def benefice(self):
        return self.prixDeVente - self.prixDachat
    def beneficeTotal(self):
        return self.benefice() * self.quantite
    def __str__(self):
        return self.nom

class Commande(models.Model):
    client = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE )
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    date_commande = models.DateTimeField(verbose_name="Commande", default=timezone.now)
    date_fin = models.DateTimeField(verbose_name="Expiration", default=lambda : timezone.now() + timedelta(hours=1))

    def __str__(self):
        return f"{self.client.username} | {self.produit.nom}"

    def expiration(self):
        if self.date_fin >= timezone.now():
            return False
        return True

class Panier(models.Model):
    client = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    commandes = models.ManyToManyField(Commande)

    def __str__(self):
        return f"Panier de { self.client.username }"

