from django.shortcuts import render, redirect, get_object_or_404
import requests
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def mostrar_colores(request):
    return render(request, 'colores.html')

def mostrar_base(request):
    return render(request, 'base.html')

def mostrar_registro(request):
	data = {
		'form': CustomUserCreationForm()
	}

	if request.method == 'POST':
		formulario = CustomUserCreationForm(data=request.POST)
		if formulario.is_valid():
			formulario.save()
			user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
			login(request,user)
			messages.success(request, "El registro se ha completado correctamente")
			return redirect(to="inicio")
	return render(request, 'registration/registro.html', data)

import requests
from django.shortcuts import render

def mostrar_home(request, pagina=1):

    try:
        pagina = int(pagina)
    except ValueError:
        pagina = 1

    # URLs sin per_page
    url_peliculas = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=es-ES&page={pagina}&sort_by=popularity.desc"
    url_series = f"https://api.themoviedb.org/3/discover/tv?include_adult=true&include_video=false&language=es-ES&page={pagina}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }

    solicitud_peliculas = requests.get(url_peliculas, headers=headers)
    solicitud_series = requests.get(url_series, headers=headers)

    datos_peliculas = []
    datos_series = []

    if solicitud_peliculas.status_code == 200:
        datos_peliculas = solicitud_peliculas.json().get('results', [])[:10]  

    if solicitud_series.status_code == 200:
        datos_series = solicitud_series.json().get('results', [])[:10]  
    
    base_url_imagen = "https://image.tmdb.org/t/p/w500"

    for dato in datos_peliculas:
        if 'poster_path' in dato:
            dato['imagen_url'] = f"{base_url_imagen}{dato['poster_path']}"
        else:
            dato['imagen_url'] = None

    for dato in datos_series:
        if 'poster_path' in dato:
            dato['imagen_url'] = f"{base_url_imagen}{dato['poster_path']}"
        else:
            dato['imagen_url'] = None

    base_url_imagen = "https://image.tmdb.org/t/p/w780"

    for pelicula in datos_peliculas:
        tmdb_id = pelicula.get('id', None)
        if tmdb_id:
            images_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key=fZd8qW3Bpej0Zea4Rz2OxSS6XLSNRGJW'
            images_response = requests.get(images_url, headers=headers)

            if images_response.status_code == 200:
                images_data = images_response.json()
                if 'backdrops' in images_data:
                    pelicula['imagenes_adicionales'] = [f"{base_url_imagen}{img['file_path']}" for img in images_data['backdrops'][:5]]
                else:
                    pelicula['imagenes_adicionales'] = []
            else:
                pelicula['imagenes_adicionales'] = []
        else:
            pelicula['imagenes_adicionales'] = []

    return render(request, 'home.html', {'peliculas': datos_peliculas, 'series': datos_series, 'pagina_actual': pagina})



def mostrar_detalles(request, pelicula_id):
    url_info = f"https://api.themoviedb.org/3/movie/{pelicula_id}?language=es-ES"
    url_imagenes = f"https://api.themoviedb.org/3/movie/{pelicula_id}/images"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }



    # Obtener información de la película
    respuesta_info = requests.get(url_info, headers=headers)
    pelicula_info = respuesta_info.json() if respuesta_info.status_code == 200 else None

    # Obtener imágenes de la película
    respuesta_imagenes = requests.get(url_imagenes, headers=headers)
    imagenes = respuesta_imagenes.json().get('backdrops', []) if respuesta_imagenes.status_code == 200 else []

    if pelicula_info and 'poster_path' in pelicula_info:
        base_url_imagen = "https://image.tmdb.org/t/p/original"
        pelicula_info['imagen_url'] = f"{base_url_imagen}{pelicula_info['poster_path']}"
    else:
        pelicula_info['imagen_url'] = None

    return render(request, 'pelicula_detalle.html', {'pelicula': pelicula_info, 'imagenes': imagenes})
    
    
def mostrar_detalles_serie(request, serie_id):
    url_info = f"https://api.themoviedb.org/3/tv/{serie_id}?language=es-ES"
    url_imagenes = f"https://api.themoviedb.org/3/tv/{serie_id}/images"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }

    # Obtener información de la serie
    respuesta_info = requests.get(url_info, headers=headers)
    serie_info = respuesta_info.json() if respuesta_info.status_code == 200 else None

    # Obtener imágenes de la serie
    respuesta_imagenes = requests.get(url_imagenes, headers=headers)
    imagenes = respuesta_imagenes.json().get('backdrops', []) if respuesta_imagenes.status_code == 200 else []

    if serie_info and 'poster_path' in serie_info:
        base_url_imagen = "https://image.tmdb.org/t/p/original"
        serie_info['imagen_url'] = f"{base_url_imagen}{serie_info['poster_path']}"
    else:
        serie_info['imagen_url'] = None

    return render(request, 'detalles_serie.html', {'serie': serie_info, 'imagenes': imagenes})