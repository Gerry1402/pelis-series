import os, sys, shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *
from varios import *

def caratulas_series (serie):

    for capitulo in lista_archivos(os.path.join(carpeta_series.ruta, serie), extension='.mkv'):
        temporada=capitulo.split('x')[0]
        os.makedirs(temporada, exist_ok=True)
        shutil.move(capitulo,temporada)
        if not os.path.isfile(os.path.join(carpeta_series.ruta, serie, temporada, "cover.bat")):
            shutil.copy(os.path.join(carpeta_caratulas.cover), os.path.join(temporada, "cover.bat"))
            shutil.copy(os.path.join(carpeta_caratulas.series, serie, temporada, f'{temporada}.jpg'),os.path.join(temporada, "cover.jpg"))

def sacar_capitulos_de_carpetas ():

    lista_series=os.listdir(carpeta_series.ruta)

    for serie in lista_series:
        temporadas=os.listdir(os.path.join(carpeta_series.ruta, serie))
        for temporada in temporadas:
            if os.path.isdir(os.path.join(carpeta_series.ruta, serie, temporada)):
                os.chdir(os.path.join(carpeta_series.ruta, serie, temporada))
                capitulos=os.listdir(os.path.join(carpeta_series.ruta, serie, temporada))
                for capitulo in capitulos:
                    if capitulo.endswith('.mkv'):
                        shutil.move(capitulo, os.path.join(carpeta_series.ruta, serie))