from dotenv import load_dotenv
import os, requests
import tmdbsimple as tmdb


load_dotenv()

# Configurar TMDb con tu API Key

tmdb.API_KEY = os.getenv('API_KEY_TMDB')

tmdb.REQUESTS_TIMEOUT = 5

movie = tmdb.Movies(603)
response = movie.info()
print(response.keys())