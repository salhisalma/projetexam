from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('animaux/', views.liste_animaux, name='liste_animaux'),
    path('animal/<int:pk>/', views.fiche_animal, name='fiche_animal'),
    path('animal/ajouter/', views.ajouter_animal, name='ajouter_animal'),
    path('animal/<int:pk>/modifier/', views.modifier_animal, name='modifier_animal'),
    path('animal/<int:pk>/adopter/', views.adopter_animal, name='adopter_animal'),
    path('recherche/', views.recherche_animaux, name='recherche'),
]