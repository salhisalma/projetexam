from django.db import models
from datetime import date

class Espece(models.Model):
    nom_espece = models.CharField(max_length=50)
    besoins_specifiques = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom_espece

class Animal(models.Model):
    STATUT_CHOICES = [
        ('DISP', 'Disponible'),
        ('SOIN', 'En soin'),
        ('ADOP', 'Adopté'),
        ('FAMILLE', 'En famille d\'accueil'),
    ]
    
    SEXE_CHOICES = [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]
    
    nom = models.CharField(max_length=100)
    race = models.CharField(max_length=100, blank=True)
    date_naissance_estimee = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='DISP')
    date_arrivee = models.DateField(auto_now_add=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    compatibilite_chats = models.BooleanField(default=False)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom} - {self.espece.nom_espece}"
    
    def get_statut_display_fr(self):
        return dict(self.STATUT_CHOICES).get(self.statut, self.statut)
    
    def get_badge_color(self):
        colors = {
            'DISP': 'primary',
            'SOIN': 'secondary',
            'ADOP': 'danger',
            'FAMILLE': 'warning'
        }
        return colors.get(self.statut, 'secondary')

class Adoption(models.Model):
    nom_adoptant = models.CharField(max_length=200)
    date_adoption = models.DateField(auto_now_add=True)
    frais_participation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.animal.nom} adopté par {self.nom_adoptant}"