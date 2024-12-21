from pydub import AudioSegment
import os


carpeta_fuente = os.path.join('D:\\','Users','paula','Downloads','One Piece AAC')

corte_inicio = 15500 # Tiempo en milisegundos

corte_final = 0 # Tiempo en milisegundos

extension_final = 'mp3'



carpeta_destino = os.path.join(carpeta_fuente, 'dONE')
os.makedirs(carpeta_destino, exist_ok=True)

extensiones = ['.aac', '.mp3', '.opus', '.ac3', '.wav', '.m4a', '.mka', '.ogg', '.mp2', '.amr', '.ape', '.au', '.m4r', '.m4b', '.aiff', '.wma']

if f'.{extension_final}' not in extensiones:
    quit('La extension final no coincide con ninguna de las registradas en la lista')

lista_audios = [archivo for archivo in os.listdir(carpeta_fuente) if os.path.splitext(archivo)[1] in extensiones]

for i, nombre_audio in enumerate(lista_audios, start=1):

    ruta_audio = os.path.join(carpeta_fuente, nombre_audio)
    extension_inicio = os.path.splitext(ruta_audio)[-1].replace('.', '')
    nombre_final = f'{os.path.splitext(nombre_audio)[0]}.{extension_final}'

    audio = AudioSegment.from_file(ruta_audio, format=extension_inicio)

    audio_recortado = audio[corte_inicio:corte_final*(-1)-1]

    audio_recortado.export(os.path.join(carpeta_destino, nombre_final), format=extension_final)
    print(f'{'Hecho' if i==1 else 'Hechos'} {i} de {len(lista_audios)}       ',end='\r')