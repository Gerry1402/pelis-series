from tmdbv3api import TMDb, Movie, TV
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar TMDb con tu API Key
tmdb = TMDb()
tmdb.api_key = os.getenv('API_KEY_TMDB')
tmdb.language = 'es'  # Idioma de los resultados (español)

# Buscar una serie
tv = TV()
search_series = tv.search("Breaking Bad")

for result in search_series:
    print(f"Título: {result.name}")
    print(f"Resumen: {result.overview}")
    print(f"Primera emisión: {result.first_air_date}")
    print("-" * 30)