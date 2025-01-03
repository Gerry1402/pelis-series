import os, ffmpeg, subprocess
from pycdlib import PyCdlib


iso = PyCdlib()
iso.new(interchange_level=3, rock_ridge='1.09', joliet=3)
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

class VideoTs:

    def __init__(self, ruta_carpeta_videots:str):
        self.dir: str = ruta_carpeta_videots
        self.archivo = iso
        self.vobs = [os.path.join(ruta_carpeta_videots, vob) for vob in os.listdir(ruta_carpeta_videots) if os.path.basename(vob).startswith('VTS_01_') and os.path.splitext(vob)[-1] == '.VOB']
        self.info = [ffmpeg.probe(vob) for vob in self.vobs]
        self.codecs_audios = [track['codec_name'] for track in ffmpeg.probe(self.vobs[0])['streams'] if track['codec_type'] == 'audio']

    def crear_iso(self, ruta_iso):
        for vob in self.vobs:
            self.archivo.add_file_from_filesystem(
                vob,
                f'/{os.path.relpath(vob, self.dir).replace(os.sep, "/")};1'
            )
        self.archivo.write(ruta_iso)
        self.archivo.close()
        self.archivo = iso

    def extraer_audio(self, ruta_audio, maps: list = None):
        os.makedirs(ruta_audio, exist_ok=True)
        comando = ['ffmpeg']
        for vob in self.vobs:
            comando += ['-i', vob]
        comando += ['-filter_complex']
        for i, codec in enumerate(self.codecs_audios, start = 1):
            copia_comando = comando.copy()
            if maps:
                copia_comando += [''.join([f'[{j}:a:{track}]' for j, track in enumerate(maps)])+f'concat=n={len(self.vobs)}:v=0:a=1']
            else:
                copia_comando += [''.join([f'[{j}:a:{i}]' for j in range(len(self.vobs))])+f'concat=n={len(self.vobs)}:v=0:a=1']
            # copia_comando += ['-map', '"[out]"']
            copia_comando += [os.path.join(ruta_audio, f'audio_{i}.{codec}')]
            # print(copia_comando)
            subprocess.run(copia_comando)
            if maps:
                break



videots = VideoTs("Z:\\[TEMP]\\ANT-MAN AND THE WASP QUANTUMANIA\\VIDEO_TS")

videots.extraer_audio("D:\\Gerard\\Videos\\mkvmerge python\\merge\\audios\\dONE", [3,2,2,3,2,2,3,2])