import os, sys
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva
from deep_translator import GoogleTranslator
from iso639 import languages

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PELICULAS.info import titulos_peliculas
from directorios import *
from classes import MKV

##### EDITAR SÓLO ESTA PARTE. SEGUIR INSRRUCCIONES. UTILIZAR ESPAÑOL. ######

pelicula = input('Nombre del archivo mkv (sin la extensión): ')
idioma_original = 'Inglés'

audios =                {idioma_original: 1} | {'Catalán': 2, 'Español': 3}
subtitulos =            {idioma_original: 4} | {'Catalán': 5, 'Español': 6}
subtitulos_forzados =   {idioma_original: None} | {'Catalán': None, 'Español': None}

orden_audios = [idioma_original, 'Catalán', 'Español']
orden_subtitulos = [idioma_original, 'Catalán', 'Español']

##########################################################################

if pelicula not in titulos_peliculas:
    exit('Falta la carátula de la película')

orden_audios = orden_audios if idioma_original not in ['Catalán', 'Español'] else [idioma_original]
orden_subtitulos = orden_subtitulos if idioma_original not in ['Catalán', 'Español'] else [idioma_original]

if idioma_original == 'Japonés':
    orden_audios = ['Catalán', idioma_original]
    orden_subtitulos = ['Catalán', 'Español', idioma_original]

idiomas = {idioma: languages.get(name=GoogleTranslator(source='es', target='en').translate(idioma)) for idioma in list(set(orden_audios) | set(orden_subtitulos))}

os.makedirs(os.path.join(carpeta_multiplexado.ruta, "DONE"), exist_ok=True)

archivo_mkv = MKV(os.path.join(carpeta_multiplexado.pelis, f'{pelicula}.mkv'))

mkv = mkvf(title=titulos_peliculas[pelicula])

HEVC = mkvt(archivo_mkv.dir, track_id=0, track_name=f"HEVC {archivo_mkv.resolucion}", language='und')
mkv.add_track(HEVC)

for idioma_audio in orden_audios:
    if audios[idioma_audio]:
        audio = mkvt(archivo_mkv.dir, track_id=audios[idioma_audio], track_name="AAC", language=idiomas[idioma_audio].bibliographic, default_track=idioma_audio == idioma_original, forced_track=False)
        mkv.add_track(audio)

for idioma_subtitulo in orden_subtitulos:
    
    if subtitulos_forzados[idioma_subtitulo]:
        subtitulo_forzado = mkvt(archivo_mkv.dir, track_id=subtitulos_forzados[idioma_subtitulo], track_name=GoogleTranslator(source='es', target=idiomas[idioma_original].alpha2).translate('Subtítulos forzados'), language=idiomas[idioma_audio].bibliographic, default_track=idioma_audio == idioma_original, forced_track=True)
        mkv.add_track(subtitulo_forzado)

    if subtitulos[idioma_subtitulo]:
        subtitulo = mkvt(archivo_mkv.dir, track_id=subtitulos[idioma_audio], track_name=GoogleTranslator(source='es', target=idiomas[idioma_original].alpha2).translate('Subtítulos'), language=idiomas[idioma_audio].bibliographic, default_track=False, forced_track=False)
        mkv.add_track(subtitulo)

mkv.mux(os.path.join(carpeta_multiplexado.ruta, "DONE", f'{pelicula}.mkv'), silent=True)