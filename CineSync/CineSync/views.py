from django.shortcuts import render, redirect, get_object_or_404
import requests
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
import asyncio
from asgiref.sync import async_to_sync
import concurrent.futures
from django.views.decorators.cache import cache_page


def mostrar_colores(request):
    return render(request, 'colores.html')

def mostrar_base(request):
    return render(request, 'base.html')

def mostrar_cargando(request):
    return render(request,'cargando.html')

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


def obtener_imagenes_adicionales(tmdb_id, tipo, base_url_imagen, headers, cantidad=1):
    url = f'https://api.themoviedb.org/3/{tipo}/{tmdb_id}/images?api_key=fZd8qW3Bpej0Zea4Rz2OxSS6XLSNRGJW'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        images_data = response.json()
        return [f"{base_url_imagen}{img['file_path']}" for img in images_data.get('backdrops', [])[:cantidad]]
    else:
        return []

def obtener_imagenes_adicionales_paralelo(ids, tipo, base_url_imagen, headers, cantidad=1):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Lanzar solicitudes en paralelo
        resultados = list(executor.map(lambda tmdb_id: obtener_imagenes_adicionales(tmdb_id, tipo, base_url_imagen, headers, cantidad), ids))

    return resultados

#@cache_page(60 * 15)
def mostrar_home(request, pagina=1):

    try:
        pagina = int(pagina)
    except ValueError:
        pagina = 1

    base_url_imagen = "https://image.tmdb.org/t/p/"
    base_url_imagen_w342 = f"{base_url_imagen}w342"
    base_url_imagen_w780 = f"{base_url_imagen}w780"

    url_peliculas = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=es-ES&page={pagina}&sort_by=popularity.desc"
    url_series = f"https://api.themoviedb.org/3/discover/tv?include_adult=true&include_video=false&language=es-ES&page={pagina}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }

    solicitud_peliculas = requests.get(url_peliculas, headers=headers)
    solicitud_series = requests.get(url_series, headers=headers)

    datos_peliculas = solicitud_peliculas.json().get('results', [])[:20] if solicitud_peliculas.status_code == 200 else []
    datos_series = solicitud_series.json().get('results', [])[:20] if solicitud_series.status_code == 200 else []

    # Obtener todos los IDs de películas y series
    ids_peliculas = [pelicula.get('id') for pelicula in datos_peliculas[:20]]
    ids_series = [serie.get('id') for serie in datos_series[:20]]

    for i, pelicula in enumerate(datos_peliculas):
        pelicula['imagen_url'] = f"{base_url_imagen_w342}{pelicula.get('poster_path', '')}"

    for i, serie in enumerate(datos_series):
        serie['imagen_url'] = f"{base_url_imagen_w342}{serie.get('poster_path', '')}"

    # Asignar las imágenes adicionales a cada película y serie

    if pagina == 1:
        # Utilizar carga paralela para obtener imágenes adicionales de películas
        imagenes_adicionales_peliculas = obtener_imagenes_adicionales_paralelo(ids_peliculas[:3], 'movie', base_url_imagen_w780, headers, cantidad=1)
        for i, pelicula in enumerate(datos_peliculas[:3]):
            pelicula['imagenes_adicionales'] = imagenes_adicionales_peliculas[i]

        # Utilizar carga paralela para obtener imágenes adicionales de series
        imagenes_adicionales_series = obtener_imagenes_adicionales_paralelo(ids_series[:3], 'tv', base_url_imagen_w780, headers, cantidad=1)
        for i, serie in enumerate(datos_series[:3]):
            serie['imagenes_adicionales'] = imagenes_adicionales_series[i]

    return render(request, 'home.html', {'peliculas': datos_peliculas, 'series': datos_series, 'pagina_actual': pagina})

def mostrar_detalles(request, pelicula_id):
    url_info = f"https://api.themoviedb.org/3/movie/{pelicula_id}?language=es-ES"
    url_imagenes = f"https://api.themoviedb.org/3/movie/{pelicula_id}/images"
    url_reparto = f"https://api.themoviedb.org/3/movie/{pelicula_id}/credits"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }

    api_key = 'fdcabc0604c5dea950cc3bc372b3fdde'

    # Obtener información de la película
    respuesta_info = requests.get(url_info, headers=headers)
    pelicula_info = respuesta_info.json() if respuesta_info.status_code == 200 else None

    # Obtener todas las imágenes de la película
    respuesta_imagenes = requests.get(url_imagenes, headers=headers)
    todas_las_imagenes = respuesta_imagenes.json().get('backdrops', [])[:5]  if respuesta_imagenes.status_code == 200 else []

    # Limitar a las primeras 5 imágenes
    imagenes = todas_las_imagenes

    if pelicula_info and 'poster_path' in pelicula_info:
        base_url_imagen = "https://image.tmdb.org/t/p/original"
        pelicula_info['imagen_url'] = f"{base_url_imagen}{pelicula_info['poster_path']}"
    else:
        pelicula_info['imagen_url'] = None

    respuesta_reparto = requests.get(url_reparto, headers=headers)
    reparto_data = respuesta_reparto.json().get('cast', []) if respuesta_reparto.status_code == 200 else []

    # Limitar a un máximo de 10 miembros del reparto
    reparto = reparto_data

    # Utilizar la etiqueta específica 'w300_and_h450_bestv2' para las imágenes de perfil de los actores
    base_image_url = "https://image.tmdb.org/t/p/"
    for actor in reparto:
        # Verificar si hay una foto del actor
        if actor['profile_path']:
            actor['profile_image'] = f"{base_image_url}w300_and_h450_bestv2{actor['profile_path']}"
        else:
            # Si no hay foto del actor, usar la imagen predeterminada
            actor['profile_image'] = '/static/img/predeterminado_actores.jpg'

    genres_url = f'https://api.themoviedb.org/3/movie/{pelicula_id}?api_key={api_key}&language=es-ES'
    genres_response = requests.get(genres_url)

    if genres_response.status_code == 200:
        genres_data = genres_response.json()
        if 'genres' in genres_data:
            pelicula_info['genres'] = genres_data['genres']
        else:
            pelicula_info['genres'] = []
    else:
        pelicula_info['genres'] = []


    return render(request, 'pelicula_detalle.html', {'pelicula': pelicula_info, 'imagenes': imagenes, 'reparto': reparto})
    
    
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

def mostrar_categorias(request):
    return render(request, 'categorias.html')