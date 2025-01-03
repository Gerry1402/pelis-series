from .start import *

def proceso(index):

    ######
    mkv = MKV(videos[index])
    mkv.archivo.add_track(mkvt(file_path = audios[index], language = idioma_audios, sync = delay_audio))  if hacer_audios else None
    mkv.archivo.add_track(mkvt(file_path = subtitulos[index], language=idioma_subtitulos, sync = delay_subtitulos))  if hacer_subtitulos else None

    ######
    yield from mkv.multiplexar(output=os.path.join(carpeta_merge.resultado))