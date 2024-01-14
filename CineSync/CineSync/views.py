from django.shortcuts import render
import requests

def mostrar_colores(request):
    return render(request, 'colores.html')

def mostrar_home(request, pagina=1):

    """ -------------------------------------------------------------------------------------------------------------------
        
        * Convocamos la URL y los headers brindados por la API, las cuales dan especificaciones a python de cómo se almacena y muestra la información.

        * Solicitamos los datos mediante la función requests y haciendo uso del metodo GET de HTTP.

        * Le damos un valor predeterminado a la variable que almacenará los datos recibidos de la API en forma de lista. 

    ------------------------------------------------------------------------------------------------------------------- """

    try:
        pagina = int(pagina)
    except ValueError:
        # En caso de que no sea un entero válido, usa el valor predeterminado (1)
        pagina = 1

    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={pagina}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZGNhYmMwNjA0YzVkZWE5NTBjYzNiYzM3MmIzZmRkZSIsInN1YiI6IjY1OTRkOGQ0MGU2NGFmMTJlMjhjMWIwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbbbluAx9E1p9aQ5ID93hGxzKwLmYuXID_g0J_Ww2tk"
    }

    solicitud_de_datos = requests.get(url, headers=headers) 
    
    datos_peliculas = [] 

    """ -------------------------------------------------------------------------------------------------------------------

        ?El código de estado HTTP 200 es un estándar que indica una respuesta exitosa a una solicitud. 
        
        * En este if se almacena la información en la variable 'datos_peliculas' luego de confirmar que la solicitud fue exitosa.
        * Esto se hace mediante el método 'json()', el cuál pasa los datos recibidos de formato JSON (Como esta almacenado en la API) al 
        * formato de una estructura de datos de python.

    ------------------------------------------------------------------------------------------------------------------- """

    if solicitud_de_datos.status_code == 200:
        datos_peliculas = solicitud_de_datos.json()

    """ -------------------------------------------------------------------------------------------------------------------

        Devolemos la plantilla de HTML junto a un diccionario de clave única que sirve como nombre que se utilizará
        para llamar a los datos en la estructura HTML. 

        ! Notese que la función 'get' utilizada en datos_pelculas no es la misma del protocolo HTTP, sino que es un 
        ! metodo propio de los diccionarios en python que nos devolverá un valor en caso de que el mismo exista o
        ! nos devolverá un espacio en blanco en caso de que no haya película para mostrar. 

    ------------------------------------------------------------------------------------------------------------------- """

    return render(request, 'home.html', {'peliculas': datos_peliculas.get('results', []), 'pagina_actual': pagina})



def mostrar_detalles(request):
    return render(request, 'pelicula_detalle.html')
