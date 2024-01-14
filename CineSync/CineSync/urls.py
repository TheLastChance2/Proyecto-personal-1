from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_colores),
    path('home/', views.mostrar_home, name='mostrar_home'),
    path('home/<int:pagina>/', views.mostrar_home, name='mostrar_home_pagina'),
    path('detalles/', views.mostrar_detalles),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', views.mostrar_registro),
]
