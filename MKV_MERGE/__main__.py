import os, sys
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva
from CLASSES.mkv import MKV
from directorios import *

# EDITAR SÓLO ESTA PARTE. SEGUIR INSRRUCCIONES. UTILIZAR ESPAÑOL.

Audio = True
ISO_6392_AAC = 'eng'
delay_AAC = 0

Subtitulos = False
ISO_6392_ASS = 'spa'
delay_ASS = 0

################## FUNCIONES AUXILIARES. NO TOCAR.#############################################################


###############################################################################################################

if not Audio and not Subtitulos:
    exit("¿¿Pero que quieres que haga Pereira?? Que quieres que haga???")

audios = [os.path.join(carpeta_merge.audios.done, audio) for audio in os.listdir(carpeta_merge.audios.done)]
subtitulos = [os.path.join(carpeta_merge.subtitulos.done, subtitulo) for subtitulo in os.listdir(carpeta_merge.subtitulos.done)]
videos = [os.path.join(carpeta_merge.videos, video) for video in os.listdir(carpeta_merge.videos)]

exit("  ¡¡   El numero de videos y de audios no coinciden   !!") if Audio and len(audios) != len(videos) else None
exit("  ¡¡   El numero de videos y de subtitulos no coinciden   !!") if Subtitulos and len(subtitulos) != len(videos) else None

for i, video in enumerate(videos, start=1):
    nombre, extension = os.path.splitext(os.path.basename(video))
    os.makedirs(carpeta_merge.resultado, exist_ok=True)
    print(f"Multiplexando episodio {nombre}")
    mkv = MKV(video)

    mkv.archivo.add_track(mkvt(file_path = audios[i-1], language = ISO_6392_AAC, sync = delay_AAC))  if Audio else None
    mkv.archivo.add_track(mkvt(file_path = subtitulos[i-1], language=ISO_6392_ASS, sync = delay_ASS))  if Subtitulos else None
    [print(f'{r}    ', end='\r') for r in mkv.multiplexar(os.path.join(carpeta_merge.resultado))]
    print(f"Completado{'s' if i!=1 else ''} {i} de {videos}           ", end='\r')
print("Todos los episodios han sido procesados                                 ")
