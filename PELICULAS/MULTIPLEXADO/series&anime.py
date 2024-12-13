import os, sys
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva
from deep_translator import GoogleTranslator
from iso639 import languages

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import carpeta_multiplexado
from classes import MKV
from SERIES.titulos.titulos import nombres_titulos_episodios

# EDITAR SÓLO ESTA PARTE. SEGUIR INSRRUCCIONES. UTILIZAR ESPAÑOL.

idioma_original = 'Inglés'

audios =                {idioma_original: 1} | {'Catalán': 2, 'Español': 3}
subtitulos =            {idioma_original: 4} | {'Catalán': 5, 'Español': 6}
subtitulos_forzados =   {idioma_original: None} | {'Catalán': None, 'Español': None}

orden_audios = [idioma_original, 'Catalán', 'Español']
orden_subtitulos = [idioma_original, 'Catalán', 'Español']

##########################################################################

serie = input('Nombre de la serie: ')
temporadas = range(int(input('Temporada inicio: ')),int(input('Temporada final: '))+1)

orden_audios = orden_audios if idioma_original not in ['Catalán', 'Español'] else [idioma_original]
orden_subtitulos = orden_subtitulos if idioma_original not in ['Catalán', 'Español'] else [idioma_original]

if idioma_original == 'Japonés':
    orden_audios = ['Catalán', idioma_original]
    orden_subtitulos = ['Catalán', 'Español', idioma_original]

configuracion_inicial = [audios, subtitulos, subtitulos_forzados]

idiomas = {idioma: languages.get(name=GoogleTranslator(source='es', target='en').translate(idioma)) for idioma in list(set(orden_audios) | set(orden_subtitulos))}

os.makedirs(os.path.join(carpeta_multiplexado.ruta, "DONE"), exist_ok=True)

nombres_titulos = nombres_titulos_episodios(serie=serie, temporadas=temporadas)

if len(nombres_titulos) != len(["" for elemento in os.listdir(carpeta_multiplexado) if elemento.endswith('.mkv')]):
    exit(f'Los archivos en la carpeta {os.path.basename(carpeta_multiplexado)} y las temporadas {', '.join(sorted(list(temporadas))[:-1])} y {sorted(list(temporadas))[-1]} de "{serie}" no coinciden')

for i, (nombre, titulo) in enumerate(nombres_titulos.items()):

    print(f"    Multiplexando episodio {nombre}       ", end="\r")

    archivo_mkv = MKV(os.path.join(carpeta_multiplexado.ruta, f'{nombre}.mkv'))

    audios, subtitulos, subtitulos_forzados = configuracion_inicial

    """ Utilizar esta parte a conveniencia. Puede cambiar según la serie o la propia temporada.
        Si algun video tiene pistas de más, aquí puede dejar los cambios que modifican sólo a aquel archivo en concreto.
        Se pueden añadir tantos condicionales como se desee para ajustarse lo mejor posible a la situación.
        Si no se especifican todos los datos otra vez se perderán pistas en el multiplexado.

    if len(archivo_mkv.tracks) > 6:
        audios = {idioma_original: None} | {'Catalán': None, 'Español': None}
        subtitulos = {idioma_original: None} | {'Catalán': None, 'Español': None}
        subtitulos_forzados = {idioma_original: None} | {'Catalán': None, 'Español': None}
    """

    mkv = mkvf(title=titulo)

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

    mkv.mux(os.path.join(carpeta_multiplexado.ruta, "DONE", f'{nombre}.mkv'), silent=True)

    print(f"   Completado {i+1} de {len(nombres_titulos)}       ", end="\r")

print("Todos los episodios han sido procesados          ")