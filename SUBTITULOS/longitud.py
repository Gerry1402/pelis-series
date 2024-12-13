import os, shutil
from .varios import sub_ass, sub_srt


carpeta_fuente = os.path.join('D:\\','Users','paula','Downloads','One Piece ESP SUB')
carpeta_fuente = os.path.join('D:\\','Gerard','Desktop','Repositorios GitHub','pelis-series', 'PRUEBAS')

maximo_lineas = 100

def len_ass(ruta_subtitulo):
    subtitulos = sub_ass(ruta_subtitulo)
    return len([subtitulo for subtitulo in subtitulos if subtitulo.effect == ''])

def len_srt(ruta_subtitulo):
    subtitulos = sub_srt(ruta_subtitulo)
    return len(subtitulos)


carpeta_destino = os.path.join(carpeta_fuente, 'dONE')
os.makedirs(carpeta_destino, exist_ok=True)

extensiones = {'.ass': len_ass, '.srt':len_srt}

lista_subtitulos = [archivo for archivo in os.listdir(carpeta_fuente) if os.path.splitext(archivo)[1] in extensiones]

for i, nombre_subtitulo in enumerate(lista_subtitulos, start=1):

    ruta_subtitulo = os.path.join(carpeta_fuente, nombre_subtitulo)
    extension_inicio = os.path.splitext(ruta_subtitulo)[-1]

    numero_linias = extensiones[extension_inicio](ruta_subtitulo)

    if numero_linias <= maximo_lineas:
        shutil.move(ruta_subtitulo, os.path.join(carpeta_destino, nombre_subtitulo))

    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_subtitulos)}       ',end='\r')