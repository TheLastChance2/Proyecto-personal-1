from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('colores/', views.mostrar_colores),
    path('', views.mostrar_cargando),
    path('home/', views.mostrar_home, name='mostrar_home'),
    path('home/<int:pagina>/', views.mostrar_home, name='mostrar_home_pagina'),
    path('detalles/<int:pelicula_id>/', views.mostrar_detalles, name='detalles_pelicula'),
    path('detalles_serie/<int:serie_id>/', views.mostrar_detalles_serie, name='detalles_serie'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', views.mostrar_registro),
    path('base/', views.mostrar_base),
    path('', include('apps.perfil.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('preparando/', views.mostrar_cargando),
    path('categorias/', views.mostrar_categorias),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
