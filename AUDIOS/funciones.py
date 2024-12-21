from pydub import AudioSegment
import os

def recortar(ruta_audio: str, carpeta_salida: str, extension_final: str, corte_inicio: int = 0, corte_final: int = 0):
    extension_inicio = os.path.splitext(ruta_audio)[-1].replace('.', '')
    nombre_audio = os.path.basename(ruta_audio)
    nombre_final = f'{os.path.splitext(nombre_audio)[0]}.{extension_final}'
    audio = AudioSegment.from_file(ruta_audio, format=extension_inicio)
    audio_recortado = audio[corte_inicio:corte_final*(-1)-1]
    audio_recortado.export(os.path.join(carpeta_salida, nombre_final), format=extension_final)