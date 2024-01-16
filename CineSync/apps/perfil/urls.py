from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('perfil/', views.mostrar_perfil, name='mostrar_perfil'),
]