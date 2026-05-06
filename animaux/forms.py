from django import forms
from .models import Animal, Adoption

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nom', 'espece', 'race', 'sexe', 'date_naissance_estimee', 
                  'statut', 'compatibilite_chats']
        widgets = {
            'date_naissance_estimee': forms.DateInput(attrs={'type': 'date'}),
        }

class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ['nom_adoptant', 'frais_participation']