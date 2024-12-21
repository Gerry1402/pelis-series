import os
from CLASSES.mkv import MKV
from directorios import *
from .start import *

for archivo in archivos:
    mkv = MKV(os.path.join(carpeta_multiplexado, archivo))
    #mkv.idiomas(idiom={}, forz=[])
    #mkv.eliminar(tracks=[])
    mkv.renombrar(titulo='', auto=True)
    mkv.reordenar(idiomas=orden_idiomas)
    #mkv.sincronizar(tiempo=350, audios = [], subtitulos = [], forz={})
    #mkv.recortar(inicio=True, frames=361)
    mkv.multiplexar(output=os.path.join(carpeta_multiplexado.done))