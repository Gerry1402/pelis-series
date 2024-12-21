from tmdbv3api import TMDb, Movie, TV, Season
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar TMDb con tu API Key
tmdb = TMDb()
tmdb.api_key = os.getenv('API_KEY_TMDB')
tmdb.language = 'en'  # Idioma de los resultados (español)

# Buscar una serie
tv = TV()
search_series = tv.search("Breaking Bad")

if search_series:
    detalles = tv.details(search_series[0].id)

    print("Título:", detalles.name)
    print("Descripción:", detalles.overview)
    print("Fecha de estreno:", detalles.first_air_date)
    print("Número de temporadas:", detalles.number_of_seasons)
    print("Número de episodios:", detalles.number_of_episodes)
    print("Géneros:", [genre['name'] for genre in detalles.genres])
    print("Página oficial:", detalles.homepage)
    