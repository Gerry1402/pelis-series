import os
from CLASSES.mkv import iso6392
from directorios import *
from varios import dividir_lista
from CLASSES.menu_seleccion import Menu





archivos = [os.path.join(carpeta_multiplexado.ruta, archivo) for archivo in os.listdir(carpeta_multiplexado.ruta) if os.path.splitext(archivo)[-1] == '.mkv']
n_archivos = len(archivos)
tamaño_total = sum(os.path.getsize(archivo) for archivo in archivos)


print(f'Para los idiomas utilizar la etiqueta iso-6392. Los idiomas que hay registrados son {', '.join(iso6392[:-1])} y {iso6392[-1]}\n')

pregunta = Menu(pregunta='¿Es un anime?', opciones=['Sí', 'No']).mostrar()

if pregunta == 'Sí':
    idioma_original = input('Idioma original (iso-6392) ("jpn" por defecto): ').replace(' ', '').lower() or 'jpn'
    orden_idiomas = ['cat', idioma_original, 'spa']
else:
    idioma_original = input('Idioma original (iso-6392) ("eng" por defecto): ').replace(' ', '').lower() or 'eng'
    orden_idiomas = [idioma_original, 'cat', 'spa']