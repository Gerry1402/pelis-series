import os, ffmpeg, subprocess, re
from typing import Union, List, Dict
from rich.progress import Progress
from datetime import datetime, timedelta

audio_codecs = {
    "mp3": "libmp3lame",
    "aac": "aac",
    "opus": "libopus",
    "ogg": "libvorbis",
    "wav": "pcm_s16le",
    "flac": "flac",
    "alac": "alac",
    "ac3": "ac3",
    "eac3": "eac3",
    "wma": "wmav2",
    "amr-nb": "libopencore_amrnb",
    "amr-wb": "libopencore_amrwb",
    "dts": "dca",
    "g722": "g722",
    "g711": "pcm_alaw",
    "truehd": "mlp",
    "adpcm": "adpcm_ms",
    "mp2": "mp2",
    "speex": "libspeex",
}

class Audio:
    def __init__(self, ruta_audio):
        self.ruta = ruta_audio
        self.nombre = os.path.splitext(os.path.basename(ruta_audio))[0]
        self.extension = os.path.splitext(os.path.basename(ruta_audio))[-1][1:]
        self.stream = ffmpeg.input(ruta_audio)
        self.informacion = ffmpeg.probe(ruta_audio)
        self.extension_final = None
        self.acelerador = None
        self.recortada = None
        self.repetidor = None
        self.tiempo = round(float(ffmpeg.probe(ruta_audio)['format']['duration']), 2)
        self.outputs = {}
        self.filters = {}
        self.inputs = {}
    
    def convertir (self, extension: str):
        """Método para la conversión del archivo.  El códec se elige automáticamente.

        Args:
            extension (str): Extensión a especificar.
        """
        self.extension_final = extension.lower()

    def bitrate (self, bitrate: int):
        """Método para ajustar la cantidad de bitrate.

        Args:
            bitrate (int): Cantidad a especificar.
        """
        self.outputs['audio_bitrate'] = f'{bitrate}k'

    def recortar (self, duracion: int, inicio: int = 0, final: bool = False):
        """Método para recortar.

        Args:
            duracion (int): Duración del archivo recortado en milisegundos. Por defecto recortará a partir del segundo 0.
            inicio (int): Especificar el milisegundo en el que empezará a recortar. Por defecto es 0.
            final (bool, optional): Si se activa, se tomará el final como punto de referencia (ignorando lo que hay en inicio).
        """
        self.tiempo = duracion
        start = str(((self.tiempo-duracion) if final else inicio)/1000)
        
        self.tiempo = duracion
        self.inputs['ss'] = start
        self.inputs['t'] = str(duracion/1000)

    def velocidad (self, velocidad: float = None, segundos: int = None):

        """Adjusts the playback speed of audio. Sets the tempo filter for audio processing.

This method modifies the playback speed by updating the 'atempo' filter with a rounded velocity value. The speed is controlled through an acceleration parameter.

Args:
    velocidad (float): The desired playback speed, which will be rounded to one decimal place.

Examples:
    # Set audio playback to half speed
    audio_instance.velocidad(0.5)
    
    # Set audio playback to double speed
    audio_instance.velocidad(2.0)

        """
        self.acelerador = velocidad or segundos/self.tiempo
        self.filters['atempo'] = str(velocidad)

    def bucle (self, iteraciones: int = -1, duracion: int = None):
        self.tiempo = duracion or self.tiempo*iteraciones
        self.inputs['stream_loop'] = iteraciones
        if duracion:
            self.inputs['t'] = f'{round(duracion/1000, 2)}'
    
    def crear(self, carpeta: str = None):
        """Creates and processes an audio file with optional configuration. Generates an audio output with specified parameters and provides progress tracking.

This method handles audio file creation by setting up codec, directory, and applying filters. It uses ffmpeg to process the audio, supports custom output folder, and yields progress percentage during conversion.

Args:
    carpeta (str, optional): Destination folder for the output audio file. Defaults to None.

Yields:
    float: Progress percentage of audio file conversion.

Examples:
    # Create audio file in default directory
    for progress in audio_instance.crear():
        print(f"Progress: {progress}%")
    
    # Create audio file in specific directory
    for progress in audio_instance.crear(carpeta='/path/to/output'):
        print(f"Progress: {progress}%")
        """
        print('holaaa')
        extension = self.extension_final or self.extension
        self.outputs['acodec'] = audio_codecs[extension]

        carpeta = carpeta or os.path.join(os.path.dirname(self.ruta), self.nombre)
        os.makedirs(carpeta, exist_ok=True)

        self.tiempo = int(self.tiempo / self.acelerador) if self.acelerador else int(self.tiempo)

        stream = ffmpeg.input(self.ruta, **self.inputs)
        for filter_name, filter in self.filters.items():
            if type(filter) == dict:
                stream = stream.filter(filter_name, **filter)
            else:
                stream = stream.filter(filter_name, filter)
        stream_1 = ffmpeg.output(stream, os.path.join(carpeta, f'{self.nombre}.{extension}'), **self.outputs)
        if '-map' not in stream_1.compile():
            stream = ffmpeg.output(stream, os.path.join(carpeta, f'{self.nombre}.{extension}'), map = '0:a:0', **self.outputs)
        else:
            stream = stream_1

        # ffmpeg.run(stream)

        comando = stream.compile()

        process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in process.stderr:
            # Buscar el porcentaje de progreso
            if match := re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d+)", line):
                yield (
                    (
                        int(
                            (
                                int(match[1]) * 3600
                                + int(match[2]) * 60
                                + int(match[3])
                                + int(match[4]) / 100
                            )
                        )
                        / self.tiempo
                    )
                    * 100
                )
    
    def __str__(self):
        return self.nombre
    
    def __call__(self):
        return self.nombre

audio = Audio('D:\\Gerard\\Videos\\mkvmerge python\\merge\\audios\\quantumania.ac3')
audio.velocidad(segundos = 2*3600+4*60+34)
audio.crear('D:\\Gerard\\Videos\\mkvmerge python\\merge\\audios\\dONE')