import os
from directorios import carpeta_multiplexado

def parsear_series_anime (serie, temporada, episodio)

def titulos_series_animes (serie):
    series = [s for s in os.listdir(carpeta_multiplexado.titulos) if os.path.splitext(s)[-1]=='.txt']
    if f'{serie}.txt' not in series:
        quit('La serie o anime no esta dentro de los títulos hechos')
    
