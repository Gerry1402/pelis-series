import os, time
from CLASSES.mkv import MKV
from directorios import *
from .start import *


idiomas_extra = []
tiempos_totales = 0
tamaño_analizado = 0
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
    print(f'Multiplexar: {i}/{len(archivos)}   {round(i/len(archivos)*100, 2)}%.   {int(tamaño_analizado/tamaño_total * (time.time()-tiempo_base))} segundos restantes         ',end='\r')