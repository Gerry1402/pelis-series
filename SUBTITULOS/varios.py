import pysrt, ass, os
from directorios import carpeta_subtitulos

def sub_ass(ruta_subtitulo):
    with open(ruta_subtitulo, 'r', encoding='utf_8_sig') as f:
        return ass.parse(f)

def save_ass(variable, ruta_subtitulo):
    with open(ruta_subtitulo, "w", encoding='utf_8_sig') as f:
        variable.dump_file(f)

def len_ass(ruta_subtitulo):
    subtitulos = sub_ass(ruta_subtitulo)
    return len([subtitulo for subtitulo in subtitulos if subtitulo.effect == ''])

ext_ass = {'open': sub_ass, 'save': save_ass, 'len': len_ass}

def sub_srt(ruta_subtitulo):
    return pysrt.open(ruta_subtitulo)

def save_srt(variable, ruta_subtitulo):
    variable.save(ruta_subtitulo, encoding='utf-8')

def len_srt(ruta_subtitulo):
    subtitulos = sub_srt(ruta_subtitulo)
    return len(subtitulos)

ext_srt = {'open': sub_srt, 'save': save_srt, 'len': len_srt}

extensiones = {'.ass': ext_ass, '.srt': ext_srt}

lista_subtitulos = [archivo for archivo in os.listdir(carpeta_subtitulos) if os.path.splitext(archivo)[1] in extensiones]