from django.shortcuts import render
import requests

def mostrar_colores(request):
    return render(request, 'colores.html')

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

    url_peliculas = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={pagina}&sort_by=popularity.desc"
    url_series = f"https://api.themoviedb.org/3/discover/tv?include_adult=false&include_video=false&language=es-ES&page={pagina}&sort_by=popularity.desc"


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


def mostrar_detalles(request):
    return render(request, 'pelicula_detalle.html')
