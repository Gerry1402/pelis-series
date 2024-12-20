import os, datetime
from .varios import extensiones


carpeta_fuente = os.path.join('D:\\','Users','paula','Downloads','One Piece ESP SUB')
carpeta_fuente = os.path.join('D:\\','Gerard','Desktop','Repositorios GitHub','pelis-series', 'PRUEBAS')

desplazamiento = 15500 # Tiempo en milisegundos (positivo o negativo)



carpeta_destino = os.path.join(carpeta_fuente, 'dONE')
os.makedirs(carpeta_destino, exist_ok=True)

lista_subtitulos = [archivo for archivo in os.listdir(carpeta_fuente) if os.path.splitext(archivo)[1] in extensiones]

for i, nombre_subtitulo in enumerate(lista_subtitulos, start=1):

    ruta_subtitulo = os.path.join(carpeta_fuente, nombre_subtitulo)
    extension_inicio = os.path.splitext(ruta_subtitulo)[-1]

    abrir = extensiones.get(extension_inicio).get('open')
    guardar = extensiones.get(extension_inicio).get('save')

    subtitulos = abrir(ruta_subtitulo)

    if extension_inicio == '.ass':
        desplazamiento_final = datetime.timedelta(milliseconds=desplazamiento)
        for linia in subtitulos.events:
            linia.start += desplazamiento_final
            linia.end += desplazamiento_final
    elif extension_inicio == '.srt':
        desplazamiento_final = desplazamiento
        for linia in subtitulos:
            linia.start += desplazamiento_final
            linia.end += desplazamiento_final

    guardar(subtitulos, os.path.join(carpeta_destino, nombre_subtitulo))

    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_subtitulos)}       ',end='\r')