from moviepy import VideoFileClip
import cv2, os

# Función para recortar el video con precisión en decimales (milisegundos)
def recortar_video_segundos(video, carpeta, start_time_sec=0, end_time_sec=None):

    cap = cv2.VideoCapture(video)

    # Verificar si el video se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir el archivo de video.")
        return

    # Obtener el número total de fotogramas del video
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Obtener la tasa de fotogramas (FPS) del video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calcular la duración del video en segundos
    duracion_segundos = end_time_sec or total_frames / fps

    # Cargar el video
    video = VideoFileClip(video)
    
    # Recortar el video entre start_time_sec y end_time_sec (en segundos con decimales)
    video_recortado = video.subclip(start_time_sec, duracion_segundos)
    
    # Guardar el video recortado
    video_recortado.write_videofile(os.path.join(carpeta, os.path.basename(video)), codec="libx264", audio_codec="aac")


# Función para recortar el video con precisión en decimales (milisegundos)
def recortar_video_frames(ruta_video, carpeta, frame_inicio:int=0, frame_final:int=None):

    cap = cv2.VideoCapture(ruta_video)

    # Verificar si el video se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir el archivo de video.")
        return

    # Obtener el número total de fotogramas del video
    frame_final = frame_final or cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Obtener la tasa de fotogramas (FPS) del video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calcular la duración del video en segundos
    duracion_segundos = frame_final / fps

    start_time_sec = frame_inicio / fps

    # Cargar el video
    video = VideoFileClip(ruta_video)
    
    # Recortar el video entre start_time_sec y end_time_sec (en segundos con decimales)
    video_recortado = video.subclipped(start_time_sec, duracion_segundos)
    
    # Guardar el video recortado
    video_recortado.write_videofile(os.path.join(carpeta, os.path.basename(ruta_video)), codec="libx264", audio_codec="aac")

# Parámetros: tiempos con decimales para milisegundos
input_video = "D:\\Gerard\\Videos\\[Judas] One Piece - 432.mkv"  # Ruta del video original
carpeta = "D:\\Gerard\\Videos\\Frames 1"  # Ruta para guardar el video recortado
start_time_sec = 30.123  # El tiempo de inicio en segundos (30 segundos y 123 milisegundos)
end_time_sec = 90.456    # El tiempo de fin en segundos (90 segundos y 456 milisegundos)

recortar_video_frames(input_video, carpeta=carpeta, frame_inicio=531)