from django import forms
from boutique.models import Product

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["categorie", "nom", "prixDachat", "prixDeVente", "quantite", "detail", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantite'].label = "Quantité d'article"

        self.fields['prixDeVente'].widget.attrs.update({
            'placeholder': 'Champ non obligatoire, veleur par défaut = prix de vente + 10%',
        })
        for element in self.fields:
            self.fields[element].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })