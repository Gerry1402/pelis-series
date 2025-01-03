from .start import *

def proceso(index):

    ######
    mkv = MKV(videos[index-1])
    mkv.archivo.add_track(mkvt(file_path = audios[index-1], language = idioma_audios, sync = delay_audio))  if hacer_audios else None
    mkv.archivo.add_track(mkvt(file_path = subtitulos[index-1], language=idioma_subtitulos, sync = delay_subtitulos))  if hacer_subtitulos else None

    ######
    yield from mkv.multiplexar(output=os.path.join(carpeta_merge.resultado))