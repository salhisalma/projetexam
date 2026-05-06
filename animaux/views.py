from django.shortcuts import render, redirect
from .models import Animal, Espece, Adoption
from .forms import AnimalForm, AdoptionForm

# Create your views here.

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
    animal = Animal.objects.get(id=pk)
    adoption = None
    try:
        adoption = Adoption.objects.get(animal=animal)
    except Adoption.DoesNotExist:
        pass
    return render(request, 'animaux/fiche_animal.html', {'animal': animal, 'adoption': adoption})

def ajouter_animal(request):
    form = AnimalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_animaux')
    context = {'form': form}
    return render(request, 'animaux/ajouter_animal.html', context)

def modifier_animal(request, pk):
    animal = Animal.objects.get(id=pk)
    form = AnimalForm(request.POST or None, instance=animal)
    if form.is_valid():
        form.save()
        return redirect('fiche_animal', pk=animal.id)
    context = {'form': form, 'animal': animal}
    return render(request, 'animaux/modifier_animal.html', context)

def adopter_animal(request, pk):
    animal = Animal.objects.get(id=pk)
    
    if animal.statut == 'ADOP':
        return redirect('fiche_animal', pk=animal.id)
    
    form = AdoptionForm(request.POST or None)
    if form.is_valid():
        adoption = form.save(commit=False)
        adoption.animal = animal
        adoption.save()
        animal.statut = 'ADOP'
        animal.save()
        return redirect('fiche_animal', pk=animal.id)
    
    context = {'form': form, 'animal': animal}
    return render(request, 'animaux/adopter_animal.html', context)

def recherche_animaux(request):
    query = request.GET.get('q', '')
    animaux = Animal.objects.filter(nom__icontains=query) | Animal.objects.filter(race__icontains=query)
    context = {'animaux': animaux, 'query': query}
    return render(request, 'animaux/liste_animaux.html', context)