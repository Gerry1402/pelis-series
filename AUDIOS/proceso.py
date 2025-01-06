from CLASSES.audio import Audio
from .start import *

idiomas_extra = []

def proceso(archivo):
    audio = Audio(archivo)

    ######

    audio.velocidad(segundos=74474)

    ######
    yield from audio.crear(os.path.join(carpeta_audios.done))