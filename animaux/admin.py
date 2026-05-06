from django.contrib import admin
from .models import Espece, Animal, Adoption

@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_espece', 'besoins_specifiques')
    search_fields = ('nom_espece',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'espece', 'race', 'sexe', 'statut', 'date_arrivee')
    list_filter = ('statut', 'espece', 'sexe')
    search_fields = ('nom', 'race')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'nom_adoptant', 'date_adoption', 'frais_participation')
    search_fields = ('nom_adoptant', 'animal__nom')