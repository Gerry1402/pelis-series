from dotenv import load_dotenv
import os, requests
import tmdbsimple as tmdb


serie = input('Nombre de la serie: ')

load_dotenv()

# Configurar TMDb con tu API Key

tmdb.API_KEY = os.getenv('API_KEY_TMDB')

tmdb.REQUESTS_TIMEOUT = 5

busqueda = tmdb.Search()

busqueda.tv(query=serie)


if len(busqueda.results) > 1:
    for i, result in enumerate(busqueda.results):
        info_season = tmdb.TV(result['id']).info()
        print(f'{i}: ', result['name'], f'({result['first_air_date'].split('-')[0]})')

resultado = busqueda.results[int(input('Seleccionar serie (Numero): ')) if len(busqueda.results)>1 else 0]

informacion = tmdb.TV(resultado['id']).info()

#['adult', 'backdrop_path', 'created_by', 'episode_run_time', 'first_air_date', 'genres', 'homepage', 'id',
# 'in_production', 'languages', 'last_air_date', 'last_episode_to_air', 'name', 'next_episode_to_air', 'networks', 'number_of_episodes',
# 'number_of_seasons', 'origin_country', 'original_language', 'original_name', 'overview', 'popularity', 'poster_path', 'production_companies',
# 'production_countries', 'seasons', 'spoken_languages', 'status', 'tagline', 'type', 'vote_average', 'vote_count']

estado = informacion['status']
id_serie = informacion['id']

titulo = informacion['original_name'] # TITLE (Collection)
subtitulo = informacion['tagline'] # TITLE (Collection)
generos_serie = informacion['genres'] # TITLE (Collection)
numero_temporadas = informacion['number_of_seasons'] # TITLE (Collection)
fecha_serie = informacion['first_air_date'] # TITLE (Collection)
sinopsis_serie = informacion['overview'] # TITLE (Collection)
idioma = informacion['languages']

for temporada in informacion['seasons']:
    temporada = tmdb.TV_Seasons(id_serie, temporada['season_number']).info()
    # ['_id', 'air_date', 'episodes', 'name', 'overview', 'id', 'poster_path', 'season_number', 'vote_average']
    fecha_temporada = temporada['air_date'] # TITLE (Season)
    sinopsis_temporada = temporada['episodes'] # TITLE (Season)
    numero_temporada = temporada['overview'] # TITLE (Season)
    numero_episodios = max(episodio['episode_number'] for episodio in temporada['episodes']) # TITLE (Season)
    for episodio in temporada['episodes']:
        fecha_episodio = episodio['air_date']
        numero_temporada = temporada['season_number']
        print(numero_temporada)
        for person in episodio['crew']:
            print(f'{person['name']}\t{person['job']}')

        roles = {   
                    'Director': 'DIRECTOR',
                    'First Assistant Director': 'ASSISTANT_DIRECTOR',
                    'Second Assistant Director': 'ASSISTANT_DIRECTOR',
                    'Producer': 'PRODUCER',
                    'Co-Producer': 'COPRODUCER',
                    'Writer': 'WRITTEN BY',
                    'Director of Photography': 'DIRECTOR_OF_PHOTOGRAPHY',
                    'Sound Re-Recording Mixer': 'SOUND_ENGINEER',
                    # 'Script Supervisor',
                    # 'Costume Supervisor',
                    # 'Co-Executive Producer',
                    # 'Casting Associate',
                    # 'Consulting Producer',
                    # 'Key Makeup Artist',
                    # 'Makeup Artist',
                    # 'Associate Producer',
                    # 'Production Coordinator',
                    # 'Property Master',
                    # 'Transportation Coordinator',
                    # 'Hairstylist',
                    # 'Digital Colorist',
                    # 'Executive Consultant',
                    # 'Unit Production Manager'
                }
        quit()

print(estado)
