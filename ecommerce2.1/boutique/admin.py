from django.contrib import admin
from boutique.models import Product, Categorie, Commande, Panier


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3

class CategorieAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ["nom", ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["nom", 'categorie', "prixDachat", "prixDeVente", "quantite", "beneficeTotal" ]
    ordering = ["quantite"]
    list_filter = ['categorie']
    search_fields = ["nom"]

class CommandedAdmin(admin.ModelAdmin):
    list_display = ["client", 'produit', "quantite", "date_commande", "date_fin", "expiration"]
    ordering = ["date_commande"]
    list_filter = ['produit__categorie', "date_commande"]
    search_fields = ["produit"]


admin.site.register(Panier)
admin.site.register(Commande, CommandedAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Categorie, CategorieAdmin)
