import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from directorios import *
from varios import lista_archivos

with open(os.path.join(os.path.dirname(__file__),'titulos.txt'), 'r', encoding='utf8') as f1:
    titulos_peliculas = {line.split('\t')[0]: line.split('\t')[1].strip() for line in f1}

with open(os.path.join(os.path.dirname(__file__),'links.txt'), 'r', encoding='utf8') as f2:
    links_imdb_peliculas = {line.split('\t')[0]: line.split('\t')[1].strip() for line in f2}

caratulas_peliculas = lista_archivos(carpeta_caratulas.peliculas)
xml_peliculas = lista_archivos(carpeta_xml.peliculas)


