from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_colores),
    path('home/', views.mostrar_home, name='mostrar_home'),
    path('home/<int:pagina>/', views.mostrar_home, name='mostrar_home_pagina'),
    path('detalles/<int:pelicula_id>/', views.mostrar_detalles, name='detalles_pelicula'),
    path('detalles_serie/<int:serie_id>/', views.mostrar_detalles_serie, name='detalles_serie'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', views.mostrar_registro),
    path('base/', views.mostrar_base),
    path('', include('apps.perfil.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
