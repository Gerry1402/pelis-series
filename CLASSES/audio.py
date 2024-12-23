import os, ffmpeg, subprocess, re
from typing import Union, List, Dict
from rich.progress import Progress

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
        self.tiempo = round(float(ffmpeg.probe(ruta_audio)['format']['duration']), 2)
        self.outputs = {}
        self.filters = {}
        self.inputs = {}
    
    def convertir (self, extension):
        self.extension_final = extension.lower()

    def bitrate (self, bitrate):
        self.outputs['audio_bitrate'] = f'{bitrate}k'

    def recortar (self, inicio: int, duracion: int):
        self.tiempo = duracion
        self.inputs['ss'] = str(inicio/1000)
        self.inputs['t'] = str(duracion/1000)

    def velocidad (self, velocidad):
        self.filters['atempo'] = str(round(float(velocidad),1))

    def bucle (self, iteraciones: int = -1, duracion: int = None):
        self.tiempo = duracion or self.tiempo*iteraciones
        self.inputs['stream_loop'] = iteraciones
        if duracion:
            self.inputs['t'] = f'{round(duracion/1000, 2)}'
    
    def crear(self, carpeta: str = None):
        extension = self.extension_final or self.extension
        self.outputs['acodec'] = audio_codecs[extension]
        carpeta = carpeta or os.path.join(os.path.dirname(self.ruta), self.nombre)
        os.makedirs(carpeta, exist_ok=True)
        stream = ffmpeg.input(self.ruta, **self.inputs)
        for filter_name, filter in self.filters.items():
            stream = stream.filter(filter_name, filter)
        stream_1 = ffmpeg.output(stream, os.path.join(carpeta, f'{self.nombre}.{extension}'), **self.outputs)
        if '-map' not in stream_1.compile():
            stream = ffmpeg.output(stream, os.path.join(carpeta, f'{self.nombre}.{extension}'), map = '0:a:0', **self.outputs)
        else:
            stream = stream_1
        
        #ffmpeg.run(stream)

        comando = stream.compile()

        process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stderr:
            # Buscar el porcentaje de progreso
            match = re.search(r'speed=\s*([\d.]+)x', line)
            if match:
                yield int(float(match.group(1))//1)
    
    def __str__(self):
        return self.nombre
    
    def __call__(self):
        return self.nombre

# audio = Audio("Z:\\Música\\Música clásica\\Amadeus Quartet\\A Tribute to Norbert Brainin (Amadeus Quartet)\\02-03-Verdi String Quartet in E Minor - III. Prestissimo.flac")

# audio.bucle(5)

# audio.convertir('mp3')

# for speed in audio.crear("D:\\Gerard\\Videos\\mkvmerge python\\merge\\audios\\dONE"):
#     print(speed)