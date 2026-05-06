from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Animal, Espece, Adoption
from .forms import AnimalForm, AdoptionForm

def accueil(request):
    total_animaux = Animal.objects.count()
    disponibles = Animal.objects.filter(statut='DISP').count()
    adoptes = Animal.objects.filter(statut='ADOP').count()
    en_soin = Animal.objects.filter(statut='SOIN').count()
    en_famille = Animal.objects.filter(statut='FAMILLE').count()
    derniers_arrives = Animal.objects.all().order_by('-date_arrivee')[:5]
    
    context = {
        'total_animaux': total_animaux,
        'disponibles': disponibles,
        'adoptes': adoptes,
        'en_soin': en_soin,
        'en_famille': en_famille,
        'derniers_arrives': derniers_arrives,
    }
    return render(request, 'home.html', context)

def liste_animaux(request):
    animaux = Animal.objects.all()
    especes = Espece.objects.all()
    
    espece_id = request.GET.get('espece')
    sexe = request.GET.get('sexe')
    statut = request.GET.get('statut')
    compatibilite = request.GET.get('compatibilite')
    
    if espece_id:
        animaux = animaux.filter(espece_id=espece_id)
    if sexe:
        animaux = animaux.filter(sexe=sexe)
    if statut:
        animaux = animaux.filter(statut=statut)
    if compatibilite:
        animaux = animaux.filter(compatibilite_chats=True)
    
    context = {
        'animaux': animaux,
        'especes': especes,
    }
    return render(request, 'animaux/liste_animaux.html', context)

def fiche_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    adoption = Adoption.objects.filter(animal=animal).first()
    return render(request, 'animaux/fiche_animal.html', {'animal': animal, 'adoption': adoption})

def ajouter_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal ajouté avec succès!')
            return redirect('liste_animaux')
    else:
        form = AnimalForm()
    return render(request, 'animaux/ajouter_animal.html', {'form': form})

def modifier_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal modifié avec succès!')
            return redirect('fiche_animal', pk=animal.pk)
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'animaux/modifier_animal.html', {'form': form, 'animal': animal})

def adopter_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    
    if animal.statut == 'ADOP':
        messages.error(request, 'Cet animal est déjà adopté!')
        return redirect('fiche_animal', pk=animal.pk)
    
    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.animal = animal
            adoption.save()
            animal.statut = 'ADOP'
            animal.save()
            messages.success(request, f'Adoption de {animal.nom} enregistrée!')
            return redirect('fiche_animal', pk=animal.pk)
    else:
        form = AdoptionForm()
    
    return render(request, 'animaux/adopter_animal.html', {'form': form, 'animal': animal})

def recherche_animaux(request):
    query = request.GET.get('q', '')
    animaux = Animal.objects.filter(
        Q(nom__icontains=query) |
        Q(race__icontains=query)
    )
    return render(request, 'animaux/liste_animaux.html', {'animaux': animaux, 'query': query})