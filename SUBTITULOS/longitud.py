import os, shutil
from .varios import extensiones, lista_subtitulos
from directorios import carpeta_subtitulos

maximo_lineas = 100

for i, nombre_subtitulo in enumerate(lista_subtitulos, start=1):

    ruta_subtitulo = os.path.join(carpeta_subtitulos, nombre_subtitulo)
    extension = os.path.splitext(ruta_subtitulo)[-1]

    numero_linias = extensiones[extension]['len'](ruta_subtitulo)

    if numero_linias <= maximo_lineas:
        shutil.move(ruta_subtitulo, os.path.join(carpeta_subtitulos.done, nombre_subtitulo))

    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_subtitulos)}       ',end='\r')