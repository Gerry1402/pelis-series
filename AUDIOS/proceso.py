from CLASSES.audio import Audio
from .start import *

idiomas_extra = []

def proceso(archivo):
    audio = Audio(archivo)

    ######
    
    audio.bucle(3)

    ######
    for progreso in audio.crear(os.path.join(carpeta_audios.done)):
        yield progreso


def proceso_consola(archivo, progress, task_id):
    for progreso in proceso(archivo):
        progress.update(task_id, advance=progreso)