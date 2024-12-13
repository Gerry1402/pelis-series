import os, ffmpeg
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva
from typing import Union, List

class MKV: #Clase para archivos MKV

    def __init__(self, archivo_mkv:str):
        self.dir = archivo_mkv
        self.nombre = os.path.splitext(os.path.basename(self.dir))[0]
        self.carpeta = os.path.join(os.path.dirname(self.dir), self.nombre)
        self.resolucion = str(ffmpeg.probe(self.dir).get('streams')[0].get('width'))+'x'+str(ffmpeg.probe(self.dir).get('streams')[0].get('height'))
        self.archivo = mkvf(self.dir)

    def detalles(self, type: Union[str, List[str]] = None) -> List[dict]:
        """Esta funcion permite obtener los detalles de las pistas de un archivo mkv de manera fácil y organizada.

        Args:
            type (str or list[str]], optional): Tipos de archivo que se quieran analizar. Las opciones son 'video', 'audio' y 'subtitles'

        Returns:
            list[dict]: El resultado es una lista ordenada en la que aparecen las categrías 'id', 'name', 'type' y 'codec'.
            Dependiendo del tipo de pista, se añaden 'language' y/o 'forced'
        """
        detalles_tracks = []

        for track in self.archivo.tracks:

            if not type:
                if isinstance(type, str):
                    if track.track_type != type:
                        continue
                elif isinstance(type, list):
                    if track.track_type not in type:
                        continue

            info_track = {'id': track.track_id, 'name': track.track_name, 'type': track.track_type, 'codec': track.track_codec}
            if track.track_type == 'audio' or track.track_type == 'subtitles':
                info_track.update({'language': track.language, 'default': track.default_track})
                if track.track_type == 'subtitles':
                    info_track.update({'forced': track.forced_track})
            detalles_tracks.append(info_track)

        return detalles_tracks

    def renombrar(self, dict_id_nombre: dict):

        for id, nombre in dict_id_nombre.items():
            track = mkvt(self.dir, track_id=id, track_name=nombre)
            self.archivo.replace_track(id, track)

    def prioridad(self, audio=None, subtitulos=None, forzado=False):

        for track in self.archivo.tracks:
            if track.track_type == 'subtitles' and subtitulos:
                track.default_track = track.language == subtitulos and track.forced_track == forzado
            elif track.track_type == 'audio' and audio:
                track.default_track = track.language == audio
            self.archivo.replace_track(track.track_id, track)
    
    def multiplexar(self, output:str = None):
        """ Función para muxear el archivo final.
            Si no se especifica una carpeta, se una con el mismo nombre del archivo en la ruta de este y se pone ahí el resultado.

        Args:
            output (str, optional): _description_. Defaults to None.
        """

        if not output:
            os.makedirs(self.carpeta, exist_ok=True)
            output = self.carpeta

        output = os.path.join(output, f'{self.nombre}.mkv')

        self.archivo.mux(output_path=output, silent=True)

    def __str__(self):
        return self.nombre

archivo = MKV(r"D:\Gerard\Videos\La Lista De Schindler\La Lista De Schindler.mkv")
[print(detalle) for detalle in archivo.detalles()]
#archivo.renombrar(numero_track=0, nombre=f"HEVC {archivo.resolucion}")
#archivo.prioridad(audio='spa', subtitulos='eng')
