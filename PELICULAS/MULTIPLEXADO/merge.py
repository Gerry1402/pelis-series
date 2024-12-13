import os, cv2, sys
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *

# EDITAR SÓLO ESTA PARTE. SEGUIR INSRRUCCIONES. UTILIZAR ESPAÑOL.

Film = False
ISO_6392_HEVC = 'und'
delay_HEVC = 0

Audio = False
ISO_6392_AAC = 'eng'
delay_AAC = 0

Subtitulos = False
ISO_6392_ASS = 'spa'
delay_ASS = 0

################## FUNCIONES AUXILIARES. NO TOCAR.#############################################################

exit("  ¡¡   El numero de videos y de films no coinciden   !!") if Film and len(os.listdir(carpeta_mkvmerge.films)) != len(os.listdir(carpeta_mkvmerge.videos)) else None
exit("  ¡¡   El numero de videos y de audios no coinciden   !!") if Audio and len(os.listdir(carpeta_mkvmerge.audios)) != len(os.listdir(carpeta_mkvmerge.videos)) else None
exit("  ¡¡   El numero de videos y de subtitulos no coinciden   !!") if Subtitulos and len(os.listdir(carpeta_mkvmerge.subtitulos)) != len(os.listdir(carpeta_mkvmerge.videos)) else None

###############################################################################################################

if not Film and not Audio and not Subtitulos:
    exit("¿¿Pero que quieres que haga Pereira?? Que quieres que haga???")
for i, video in enumerate(carpeta_mkvmerge.videos):
    nombre, extension = os.path.splitext(os.path.basename(video))
    os.makedirs(carpeta_mkvmerge.resultado, exist_ok=True)
    print(f"Multiplexando episodio {nombre}")
    mkv = mkvf(file_path = video)

    mkv.add_track(mkvt(file_path = os.path.join(carpeta_mkvmerge.films, os.listdir(carpeta_mkvmerge.films)[i]), language = ISO_6392_HEVC, sync = delay_HEVC)) if Film else None
    mkv.add_track(mkvt(file_path = os.path.join(carpeta_mkvmerge.audios, os.listdir(carpeta_mkvmerge.audios)[i]), language = ISO_6392_AAC, sync = delay_AAC))  if Audio else None
    mkv.add_track(mkvt(file_path = os.path.join(carpeta_mkvmerge.subtitulos, os.listdir(carpeta_mkvmerge.subtitulos)[i]), language=ISO_6392_ASS, sync = delay_ASS))  if Subtitulos else None
    mkv.mux(os.path.join(carpeta_mkvmerge.resultado, f'{nombre}{extension}'), silent = True)
    print(f"Completado {i+1} de {len(os.listdir(carpeta_mkvmerge.videos))}")
print("Todos los episodios han sido procesados")
