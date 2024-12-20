import cv2
import os

# Función para separar un video en fotogramas
def extraer_fotogramas(ruta_video, ruta_carpeta, segundo_inicio=0, intervalo = 2):

    cap = cv2.VideoCapture(input_video)

    if not cap.isOpened():
        print("Error al abrir el archivo de video.")
        return

    frame_final = int(cap.get(cv2.CAP_PROP_FPS)*(segundo_inicio + intervalo))
    frame_inicio = int(cap.get(cv2.CAP_PROP_FPS)*segundo_inicio)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_inicio)
    
    for i, frame in enumerate(range(frame_inicio, frame_final+1), start=1):
        _, frame = cap.read()
        frame_filename = os.path.join(output_folder, f"frame_{i+frame_inicio}.png")
        cv2.imwrite(frame_filename, frame)
    
    cap.release()

# Parámetros
input_video = "D:\\Gerard\\Videos\\[Judas] One Piece - 433.mkv"  # Ruta del archivo de video
output_folder = "D:\\Gerard\\Videos\\Frames 2"        # Carpeta donde se guardarán las imágenes

# Llamar a la función para extraer los fotogramas
extraer_fotogramas(input_video, output_folder, segundo_inicio=14)