from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from boutique.form import ProductAddForm
from boutique.models import Product, Categorie, Panier, Commande
from compte.models import Client

def index(request):
    Products = Product.objects.all()
    Categories = []

    for product in Products:
        categorie = product.categorie
        if categorie not in Categories:
            Categories.append(categorie)

    context = {
        'Products': Products,
        'Categories': Categories,
        'Client': Client
    }
    return render(request, 'boutique/index.html', context)

def detailCategorie(request, slugCat):
    categorie = get_object_or_404(Categorie, slug=slugCat)
    Products = Product.objects.all()
    return render(request, 'boutique/categorie.html', context={"categorie": categorie, 'Products': Products})

def detailProduit(request, slugCat, slugPro):
    product = get_object_or_404(Product, slug=slugPro)
    return render(request, 'boutique/produit.html', context={"product": product})

def ajouter_au_panier(request, slugCat, slugPro):
    if request.method == "POST":
        client = request.user
        quantite = int(request.POST.get("quantite"))
        product = get_object_or_404(Product, slug=slugPro)
        panier, _ = Panier.objects.get_or_create(client=client)
        commande, cree = Commande.objects.get_or_create(client=client, produit = product)

        if cree:
            commande.quantite = quantite
            commande.save()
            panier.commandes.add(commande)
            product.quantite -= quantite
            product.save()
            panier.save()
        else:
            commande.quantite += quantite
            product.quantite -= quantite
            product.save()
            commande.save()
    return redirect(reverse("detailProduit", kwargs={"slugPro": slugPro, "slugCat": slugCat}))

def statistique(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        liste_qart = []
        liste_bart = []
        for product in products:
            liste_qart.append(product.quantite)
            liste_bart.append(product.benefice()*product.quantite)
        categories = Categorie.objects.all()
        nbr_produit = len(products)
        nbr_article = sum(liste_qart)
        Benefice_T = sum(liste_bart)
        proprietes = {}

        def pourcentage(portion, total):
            if total == 0:
                return 0
            prctg = (portion / total) * 100
            return int(prctg)

        for categorie in categories:
            propriete_cat = {}
            nbr_pro = 0
            nbr_art = 0
            prix_pro_vente = 0
            prix_pro_achat = 0
            benefice = 0
            for product in products:
                if categorie.nom == product.categorie.nom:
                    nbr_pro += 1
                    nbr_art += product.quantite
                    prix_pro_vente += product.prixDeVente * product.quantite
                    prix_pro_achat += product.prixDachat * product.quantite
                    benefice = prix_pro_vente - prix_pro_achat



            propriete_cat["Prix total d'achat"] = prix_pro_achat
            propriete_cat['Prix total de vente'] = prix_pro_vente
            propriete_cat['Benefice total'] = benefice
            propriete_cat["Nombre d'atricles"] = nbr_art
            propriete_cat['Nombre de model'] = nbr_pro
            propriete_cat["Pourcentage en nombre de modele"] = pourcentage(nbr_pro, nbr_produit)
            propriete_cat["Pourcentage en nombre d'articles"] = pourcentage(nbr_art, nbr_article)
            propriete_cat["Pourcentage en benefice"] = pourcentage(benefice, Benefice_T)
            proprietes[categorie] = propriete_cat


            Prix_T_achat = 0
            for element in proprietes.values():
                Prix_T_achat += element["Prix total d'achat"]

            Prix_T_vente = 0
            for element in proprietes.values():
                Prix_T_vente += element["Prix total de vente"]

        context = {
            'proprietes': proprietes,
            'nombre_produit': nbr_produit,
            'nombre_article': nbr_article,
            'Benefice_T': Benefice_T,
            'Prix_T_achat': Prix_T_achat,
            'Prix_T_vente': Prix_T_vente
        }
        return render(request, 'boutique/statistique.html', context=context)
    else:
        return redirect('index')

def ajouter_article(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = ProductAddForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.save()
                return redirect(reverse("detailCategorie", kwargs={"slugCat": product.categorie.slug}))
        else:
            form = ProductAddForm()
        return render(request, 'boutique/ajout.html', {"form": form })
    else:
        return redirect('index')

def panier(request):
    panier = get_object_or_404(Panier, client=request.user)
    commandes = panier.commandes.all()
    commandes_valide = []
    prix_total = 0
    for commande in commandes:
        if commande.expiration() == True:
            restorer(commande)
        else:
            commandes_valide.append(commande)
            prix_total += commande.produit.prixDeVente * commande.quantite
    return render(request, 'boutique/panier.html', context={"commandes": commandes_valide, "prixTotal": prix_total})

def restorer(commande):
    produits = Product.objects.all()
    for produit in produits:
        if produit.nom == commande.produit.nom:
            produit.quantite += commande.quantite
            produit.save()
            commande.delete()

def vider_panier(request):
    panier = get_object_or_404(Panier, client=request.user)
    commandes = panier.commandes.all()
    for commande in commandes:
        restorer(commande)
    return redirect('index')