from CLASSES.mkv import MKV
from .start import *

idiomas_extra = []

def proceso(archivo):
    mkv = MKV(archivo)

    ######
    
    #mkv.idiomas(idiom={}, forz=[])
    #mkv.eliminar(tracks=[])
    mkv.conservar(idiomas = orden_idiomas + idiomas_extra)
    mkv.renombrar(titulo='', auto=True)
    mkv.reordenar(idiomas=orden_idiomas)
    mkv.predeterminar(subtitulo='spa', forzado=False)
    #mkv.sincronizar(tiempo=350, audios = [], subtitulos = [], forz={})
    #mkv.recortar(inicio=True, frames=361)
    mkv.redimensionar(3840, 1000)

    ######
    for progreso in mkv.multiplexar(output=os.path.join(carpeta_multiplexado.done)):
        yield progreso


def proceso_consola(archivo, progress, task_id):
    for progreso in proceso(archivo):
        progress.update(task_id, completed=progreso)