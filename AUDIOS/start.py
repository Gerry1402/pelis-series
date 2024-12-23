import os
from CLASSES.audio import audio_codecs
from directorios import *


archivos = [os.path.join(carpeta_audios.ruta, archivo) for archivo in os.listdir(carpeta_audios.ruta) if os.path.splitext(archivo)[-1][1:] in audio_codecs]
n_archivos = len(archivos)
tamaño_total = 0
for archivo in archivos:
    tamaño_total += os.path.getsize(archivo)