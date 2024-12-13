import pysrt, ass


def sub_ass(ruta_subtitulo):
    with open(ruta_subtitulo, 'r', encoding='utf_8_sig') as f:
        return ass.parse(f)

def save_ass(variable, ruta_subtitulo):
    with open(ruta_subtitulo, "w", encoding='utf_8_sig') as f:
        variable.dump_file(f)

ext_ass = {'open': sub_ass, 'save': save_ass}

def sub_srt(ruta_subtitulo):
    return pysrt.open(ruta_subtitulo)

def save_srt(variable, ruta_subtitulo):
    variable.save(ruta_subtitulo, encoding='utf-8')

ext_srt = {'open': sub_srt, 'save': save_srt}

extensiones = {'.ass': ext_ass, '.srt': ext_srt}