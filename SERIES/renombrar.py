import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *
from varios import lista_carpetas, lista_archivos

def renombrar_serie(serie):
    for video in lista_archivos(serie, extension='.mkv'):
        a=1