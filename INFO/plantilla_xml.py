from typing import Union, List, Dict

def json_series(temporada:int, fecha_temporada: int, numero_episodio:int, titulo_episodio:str, numero_temporadas:int = None, serie:str = ''):

    json = {
        'collection':{
            'TITLE': serie,
        },
        'season':{
            'PART_NUMBER': str(temporada),
            'DATE_RELEASED': str(fecha_temporada)
        },
        'episode':{
            'TITLE': titulo_episodio,
            'PART_NUMBER': str(numero_episodio),
            'EPISODE': '',
        }
    }