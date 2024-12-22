import os
from CLASSES.mkv import iso6392
from directorios import *


archivos = [os.path.join(carpeta_multiplexado.ruta, archivo) for archivo in os.listdir(carpeta_multiplexado.ruta) if os.path.splitext(archivo)[-1] == '.mkv']
tamaño_analizado = 0
tiempos_totales = 0
n_archivos = len(archivos)
tamaño_total = 0
for archivo in archivos:
    tamaño_total += os.path.getsize(archivo)