import os, shutil, pysrt, ass


carpeta_fuente = os.path.join('D:\\','Users','paula','Downloads','One Piece ESP SUB')

desplazamiento = 15500 # Tiempo en milisegundos (positivo o negativo)

maximo_lineas = 100



carpeta_destino = os.path.join(carpeta_fuente, 'dONE')
os.makedirs(carpeta_destino, exist_ok=True)

extensiones = {'.ass': ass.parse, '.srt':pysrt.open}

lista_subtitulos = [archivo for archivo in os.listdir(carpeta_fuente) if os.path.splitext(archivo)[1] in extensiones]

for i, nombre_subtitulo in enumerate(lista_subtitulos, start=1):

    ruta_subtitulo = os.path.join(carpeta_fuente, nombre_subtitulo)
    extension_inicio = os.path.splitext(ruta_subtitulo)[-1]

    subtitulos = extensiones[extension_inicio](ruta_subtitulo)

    numero_linias = len([subtitulo for subtitulo in subtitulos if subtitulo.effect == ''])

    if numero_linias <= maximo_lineas:
        shutil.move(ruta_subtitulo, os.path.join(carpeta_destino, nombre_subtitulo))

    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_subtitulos)}       ',end='\r')