import os
from CLASSES.mkv import iso6392
from directorios import *
from varios import dividir_lista


numero_archivos_conjunto = 3
tamaños_conjuntos = []

archivos = [os.path.join(carpeta_multiplexado.ruta, archivo) for archivo in os.listdir(carpeta_multiplexado.ruta) if os.path.splitext(archivo)[-1] == '.mkv']
tamaño_analizado = 0
tamaño_total = 0
for i, archivo in enumerate(archivos, start=1):
    tamaño_total += os.path.getsize(archivo)
    if i % numero_archivos_conjunto == 0 or archivo == archivos[-1]:
        tamaños_conjuntos.append(tamaño_total-sum(tamaños_conjuntos))

archivos_separados = dividir_lista(archivos, numero_archivos_conjunto)



print(f'Para los idiomas utilizar la etiqueta iso-6392. Los idiomas que hay registrados son {', '.join(iso6392[:-1])} y {iso6392[-1]}\n')

pregunta = input('Es un anime? [S/N]: ')

if pregunta.lower() == 's':
    idioma_original = input('Idioma original (iso-6392) ("jpn" por defecto): ').replace(' ', '').lower() or 'jpn'
    orden_idiomas = ['cat', idioma_original, 'spa']
else:
    idioma_original = input('Idioma original (iso-6392) ("eng" por defecto): ').replace(' ', '').lower() or 'eng'
    orden_idiomas = [idioma_original, 'cat', 'spa']