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

def mostrar_home(request, pagina=1):

    """ -------------------------------------------------------------------------------------------------------------------
        
        * Convocamos la URL y los headers brindados por la API, las cuales dan especificaciones a python de cómo se almacena y muestra la información.

        * Solicitamos los datos mediante la función requests y haciendo uso del metodo GET de HTTP.

        * Le damos un valor predeterminado a la variable que almacenará los datos recibidos de la API en forma de lista.

        * Definimos la pagina de peliculas-series mostradas. 

    ------------------------------------------------------------------------------------------------------------------- """

    try:
        pagina = int(pagina)
    except ValueError:
        pagina = 1

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

    """ -------------------------------------------------------------------------------------------------------------------

        ?El código de estado HTTP 200 es un estándar que indica una respuesta exitosa a una solicitud. 
        
        *En este if se almacena la información en las variables 'datos_peliculas' y datos_series luego de confirmar que la solicitud fue exitosa.
        *Esto se hace mediante el método 'json()', el cuál pasa los datos recibidos de formato JSON (Como esta almacenado en la API) al formato de una estructura de datos de python.

        En las estructuras for se importan las imagenes 'cover' que se encuentran en urls diferentes a la de los datos 
        anteriores. Se importan solo las versiones de calidad w500 para evitar lentitud en la carga de la pagina

    ------------------------------------------------------------------------------------------------------------------- """

    if solicitud_peliculas.status_code == 200:
        datos_peliculas = solicitud_peliculas.json().get('results', [])

    if solicitud_series.status_code == 200:
        datos_series = solicitud_series.json().get('results', [])
    
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

    """ -------------------------------------------------------------------------------------------------------------------

        Devolemos la plantilla de HTML junto a un diccionario de clave única que sirve como nombre que se utilizará
        para llamar a los datos en la estructura HTML, tanto de las series como de las peliculas y también el de la 
        pagina por si se requiere mostrarlo. 

    ------------------------------------------------------------------------------------------------------------------- """

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