import os
from CLASSES.mkv import MKV
from directorios import *
from .start import *

idiomas_extra = []

for archivo in archivos:
    mkv = MKV(os.path.join(carpeta_multiplexado.ruta, archivo))
    #mkv.idiomas(idiom={}, forz=[])
    #mkv.eliminar(tracks=[])
    mkv.conservar(idiomas = orden_idiomas + idiomas_extra)
    mkv.renombrar(titulo='', auto=True)
    mkv.reordenar(idiomas=orden_idiomas)
    mkv.predeterminar(subtitulo='spa', forzado=False)
    #mkv.sincronizar(tiempo=350, audios = [], subtitulos = [], forz={})
    #mkv.recortar(inicio=True, frames=361)
    mkv.multiplexar(output=os.path.join(carpeta_multiplexado.done))