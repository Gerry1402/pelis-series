import os, sys
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *

# EDITAR SÓLO ESTA PARTE. SEGUIR INSRRUCCIONES. UTILIZAR ESPAÑOL.

Audio = False
ISO_6392_AAC = 'eng'
delay_AAC = 0

Subtitulos = False
ISO_6392_ASS = 'spa'
delay_ASS = 0

################## FUNCIONES AUXILIARES. NO TOCAR.#############################################################

exit("  ¡¡   El numero de videos y de audios no coinciden   !!") if Audio and len(os.listdir(carpeta_merge.audios)) != len(os.listdir(carpeta_merge.videos)) else None
exit("  ¡¡   El numero de videos y de subtitulos no coinciden   !!") if Subtitulos and len(os.listdir(carpeta_merge.subtitulos)) != len(os.listdir(carpeta_merge.videos)) else None

###############################################################################################################

if not Audio and not Subtitulos:
    exit("¿¿Pero que quieres que haga Pereira?? Que quieres que haga???")

audios = os.listdir(carpeta_merge.audios)
subtitulos = os.listdir(carpeta_merge.subtitulos)
n_totales = len(os.listdir(carpeta_merge.videos))

for i, video in enumerate(carpeta_merge.videos, start=1):
    nombre, extension = os.path.splitext(os.path.basename(video))
    os.makedirs(carpeta_merge.resultado, exist_ok=True)
    print(f"Multiplexando episodio {nombre}")
    mkv = mkvf(file_path = video)

    mkv.add_track(mkvt(file_path = os.path.join(carpeta_merge.audios, audios[i]), language = ISO_6392_AAC, sync = delay_AAC))  if Audio else None
    mkv.add_track(mkvt(file_path = os.path.join(carpeta_merge.subtitulos, subtitulos[i]), language=ISO_6392_ASS, sync = delay_ASS))  if Subtitulos else None
    mkv.mux(os.path.join(carpeta_merge.resultado, f'{nombre}{extension}'), silent = True)
    print(f"Completado{'s' if i!=1 else ''} {i} de {n_totales}           ", end='\r')
print("Todos los episodios han sido procesados                                 ")
