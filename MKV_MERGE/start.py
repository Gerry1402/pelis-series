import os
from CLASSES.mkv import *
from directorios import *
from CLASSES.menu_seleccion import Menu,MultiSelectMenu
from rich import print



audios = [os.path.join(carpeta_merge.audios.done, audio) for audio in os.listdir(carpeta_merge.audios.done)] or [os.path.join(str(carpeta_merge.audios), audio) for audio in os.listdir(str(carpeta_merge.audios))]
subtitulos = [os.path.join(carpeta_merge.subtitulos.done, subtitulo) for subtitulo in os.listdir(carpeta_merge.subtitulos.done)] or [os.path.join(str(carpeta_merge.subtitulos), audio) for audio in os.listdir(str(carpeta_merge.subtitulos))]
videos = [os.path.join(carpeta_merge.videos, video) for video in os.listdir(carpeta_merge.videos)]
n_archivos = len(videos)
tamaño_videos = sum(os.path.getsize(video) for video in videos)
tamaño_total = tamaño_videos

iso6392 = [info_idiomas[idioma]['iso639-2'] for idioma in idiomas]

audios_subtitulos = MultiSelectMenu(enunciado='Opciones para hacer merge (Seleccionar uno o dos)', opciones=['Audios', 'Subtítulos']).mostrar()
hacer_audios = 'Audios' in audios_subtitulos
if hacer_audios:
    if len(audios) != n_archivos:
        exit("  ¡¡   El numero de videos y de audios no coinciden   !!")
    tamaño_total += sum(os.path.getsize(audio) for audio in audios)
    idioma_audios = info_idiomas[Menu(enunciado='Seleccionar idioma audios', opciones=idiomas, subtitulos=iso6392, columnas=4, limite=4, nombre_limite='... Más idiomas').mostrar()]['iso639-2']
hacer_subtitulos = 'Subtítulos' in audios_subtitulos
if hacer_subtitulos:
    if len(subtitulos) != n_archivos:
        exit("  ¡¡   El numero de videos y de subtitulos no coinciden   !!")
    tamaño_total += sum(os.path.getsize(subtitulo) for subtitulo in subtitulos)
    idioma_subtitulos = info_idiomas[Menu(enunciado='Seleccionar idioma subtitulos', opciones=idiomas, subtitulos=iso6392, columnas=4, limite=4, nombre_limite='... Más idiomas').mostrar()]['iso639-2']


delay_audios_subtitulos = MultiSelectMenu(enunciado = '¿Añadir delay?', opciones=audios_subtitulos).mostrar()
delay_audio = int(input('Delay para los audios: ')) if 'Audios' in delay_audios_subtitulos else 0
delay_subtitulos = int(input('Delay para los subtitulos: ')) if 'Subtítulos' in delay_audios_subtitulos else 0

print('\n')