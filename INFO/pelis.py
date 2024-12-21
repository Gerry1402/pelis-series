from tmdbv3api import TMDb, Movie, TV
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar TMDb con tu API Key
tmdb = TMDb()
tmdb.api_key = os.getenv('API_KEY_TMDB')
tmdb.language = 'es'  # Idioma de los resultados (español)

movie = Movie()

search = movie.search("Inception")

for result in search:
    print(f"Título: {result.title}")
    print(f"Resumen: {result.overview}")
    print(f"Fecha de lanzamiento: {result.release_date}")
    print("-" * 30)