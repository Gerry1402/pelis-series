import os, datetime
from .varios import extensiones, lista_subtitulos
from directorios import carpeta_subtitulos

desplazamiento = 15500 # Tiempo en milisegundos (positivo o negativo)

for i, nombre_subtitulo in enumerate(lista_subtitulos, start=1):

    ruta_subtitulo = os.path.join(carpeta_subtitulos, nombre_subtitulo)
    extension_inicio = os.path.splitext(ruta_subtitulo)[-1]

    abrir = extensiones.get(extension_inicio).get('open')
    guardar = extensiones.get(extension_inicio).get('save')

    subtitulos = abrir(ruta_subtitulo)

    if extension_inicio == '.ass':
        desplazamiento_final = datetime.timedelta(milliseconds = desplazamiento)
        for linia in subtitulos.events:
            linia.start += desplazamiento_final
            linia.end += desplazamiento_final
    elif extension_inicio == '.srt':
        desplazamiento_final = desplazamiento
        for linia in subtitulos:
            linia.start += desplazamiento_final
            linia.end += desplazamiento_final

    guardar(subtitulos, os.path.join(carpeta_subtitulos.done, nombre_subtitulo))

    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_subtitulos)}       ',end='\r')