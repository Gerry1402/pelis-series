import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from directorios import *

def info_serie(serie):
    info = []
    if not serie:
        serie='00'
    with open(os.path.join(os.path.dirname(__file__), 'titulos', f'{serie}.txt'), 'r', encoding='utf8') as f:
        for linia in f:

            if linia.strip() == "":
                continue

            info_episodio = {}
            temporada_episodio, titulo = linia.strip().split(' - ', 1)

            temporada, episodio = temporada_episodio.split("x")
            info_episodio['temporada'], info_episodio['episodio'] = int(temporada), int(episodio)

            info_episodio['titulo'] = titulo.replace('! - ','! ').replace('? - ', '? ').replace(' - ', ': ')
            info_episodio['nombre'] = info_episodio['titulo'].replace(':','.').replace('?','.').replace('"','\'')

            info.append(info_episodio)

    return info

def episodios_temporada(serie, temporadas):
    return [capitulo for capitulo in info_serie(serie) if capitulo.get('temporada') == temporadas]

def crear_archivo_titulos(serie):
    with open (os.path.join(os.path.dirname(__file__), '00.txt'), 'r', encoding='utf-8') as r, open(os.path.join(os.path.dirname(__file__), f'{serie}.txt'), 'w', encoding='utf8') as w:
        temporadas = {}
        temporada = 0
        for line in r:
            episodio, nombre = line.split("\t")
            episodio, nombre = int(episodio), nombre.replace('«', '').replace('»','')
            if episodio == 1:
                temporada += 1
                temporadas[temporada] = []
            temporadas[temporada] += [nombre]
        
        cifras_temporada = len(str(len(temporadas)))

        for temporada in range(1, len(temporadas)+1):
            cifras_episodio = len(str(len(temporadas[temporada])))
            for numero, episodio in enumerate(temporadas[temporada]):
                w.write(f'{str(temporada).zfill(cifras_temporada)}x{str(numero+1).zfill(cifras_episodio)} - {episodio}')

crear_archivo_titulos('How I Met Your Mother')
