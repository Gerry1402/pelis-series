import os
from classes import MKV, iso6392
from directorios import *


archivos = [archivo for archivo in os.listdir(carpeta_multiplexado.ruta) if os.path.splitext(archivo)[-1] == '.mkv']

print(f'Para los idiomas utilizar la etiqueta iso-6392. Los idiomas que hay registrados son {', '.join(iso6392)[:-1]} y {iso6392[-1]}\n')
idioma_original = 'jpn' or input('Idioma original (iso-6392) ("jpn" por defecto): ').replace(' ', '').lower()



for archivo in archivos:
    mkv = MKV(os.path.join(carpeta_multiplexado.ruta, archivo))
    #mkv.idiomas(idiom={}, forz=[])
    #mkv.eliminar(tracks=[])
    mkv.renombrar(titulo='', auto=True)
    mkv.reordenar(idiomas=['cat', idioma_original, 'spa'])
    #mkv.sincronizar(tiempo=350, audios = [], subtitulos = [], forz={})
    #mkv.recortar(inicio=True, frames=361)
    mkv.multiplexar(output=os.path.join(carpeta_multiplexado.done))
