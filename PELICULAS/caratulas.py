import os, sys, shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *
from varios import *

def caratulas_peliculas():
    for nombre in lista_archivos(carpeta_peliculas, extension='.mkv'):
        os.path.join(carpeta_peliculas, f'{nombre}.mkv')
        os.makedirs(nombre, exist_ok=True)
        shutil.move(os.path.join(carpeta_peliculas, f'{nombre}.mkv'), os.path.join(carpeta_peliculas, nombre))
        shutil.copy(carpeta_caratulas.cover, os.path.join(carpeta_peliculas, nombre))
        shutil.copy(os.path.join(carpeta_caratulas.peliculas, f'{nombre}.jpg'), os.path.join(nombre, 'cover.jpg'))

def sacar_peliculas_de_carpetas():
    for nombre in lista_carpetas(carpeta_peliculas):
        pelicula = os.path.join(carpeta_peliculas, nombre, f'{nombre}.mkv')
        if os.path.isfile(pelicula):
            shutil.move(pelicula, carpeta_peliculas)