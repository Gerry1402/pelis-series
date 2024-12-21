import os, time
from CLASSES.mkv import MKV
from directorios import *
from .start import *


idiomas_extra = []
tiempos_totales = 0
tamaño_analizado = 0
n_archivos = len(archivos)
tiempo_base = time.time()

for i, archivo in enumerate(archivos, start=1):

    mkv = MKV(archivo)
    #mkv.idiomas(idiom={}, forz=[])
    #mkv.eliminar(tracks=[])
    mkv.conservar(idiomas = orden_idiomas + idiomas_extra)
    mkv.renombrar(titulo='', auto=True)
    mkv.reordenar(idiomas=orden_idiomas)
    mkv.predeterminar(subtitulo='spa', forzado=False)
    #mkv.sincronizar(tiempo=350, audios = [], subtitulos = [], forz={})
    #mkv.recortar(inicio=True, frames=361)
    mkv.multiplexar(output=os.path.join(carpeta_multiplexado.done))

    tamaño_analizado += os.path.getsize(archivo)
    porcentaje = tamaño_analizado/tamaño_total
    tiempo = int(time.time()-tiempo_base)
    print(f'Multiplexar: {i}/{n_archivos}   {round(porcentaje*100, 2)}%.   {int(porcentaje * tiempo)-tiempo} segundos restantes         ',end='\n')