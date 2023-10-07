from django.contrib.auth import get_user_model, login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from compte.form import AddClient

def inscription(request):
    if request.method == "POST":
        form = AddClient(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data["password"]
            client = form.save(commit=False)
            client.set_password(password)
            client.save()
            return redirect('connexion')
    else:
        form = AddClient()
    return render(request, 'compte/inscription.html', {"form": form })

def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'compte/connexion.html')

def modifier_mdp(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        user = authenticate(username=username, password=password)
        if user:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                login(request, user)
                return redirect('index')
    return render(request, 'compte/modifierMdp.html')

def deconnexion(request):
    logout(request)
    return redirect('index')
