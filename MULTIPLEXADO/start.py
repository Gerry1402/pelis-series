import os
from CLASSES.mkv import *
from directorios import *
from CLASSES.menu_seleccion import Menu
from rich import print




archivos = [os.path.join(carpeta_multiplexado.ruta, archivo) for archivo in os.listdir(carpeta_multiplexado.ruta) if os.path.splitext(archivo)[-1] == '.mkv']
n_archivos = len(archivos)
tamaño_total = sum(os.path.getsize(archivo) for archivo in archivos)

iso6392 = [info_idiomas[idioma]['iso639-2'] for idioma in idiomas]

priorizar = Menu(enunciado='¿Priorizar idioma original?', opciones=['Sí', 'No']).mostrar()=='Sí'
idioma_original = Menu(enunciado='Seleccionar idioma original', opciones=idiomas, subtitulos=iso6392, columnas=4, limite=4, nombre_limite='... Más idiomas').mostrar()
print('\n')
idioma_original_iso = info_idiomas[idioma_original]['iso639-2']
orden_idiomas = [idioma_original, 'cat', 'spa'] if priorizar else ['cat', idioma_original, 'spa']