import os, requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

with open (os.path.join(os.path.dirname(__file__), '00_urls.txt'), 'r', encoding='utf-8') as w:
    urls = [line.strip() for line in w if line.strip() != ""]

class Episodios_Anime:
    
    def __init__(self, url):
        self.enlace = unquote(url)
    
    def nombre(self):
        if 'wikipedia' in self.enlace:
            nombre = self.enlace.split('/')[-1].split('#')[0].split('_')
            nombre = ' '.join(nombre[3:]) if nombre[2] == 'de' else ' '.join([nombre[2][2:]]+nombre[3:])
            nombre = nombre.split('(')[0][:-1] if '(' in nombre else nombre
            return nombre
    
    def wikipedia(self, reinicio=None):

        soup = BeautifulSoup(requests.get(self.enlace).text, 'html.parser')
        if 'Conan' in self.enlace:
            print(soup)
        if not reinicio:
            ep1=False
            soup_temporadas = []
            for temporada in soup.find_all(class_='wikitable'):
                if temporada.find(class_='vevent'):
                    comprobacion = temporada.find(class_='vevent').find('th') or temporada.find(class_='vevent').find('td')
                    if comprobacion.has_attr('id'):
                        if comprobacion['id'] == "ep1" and not ep1:
                            ep1 = not ep1
                        elif (comprobacion['id'] == "ep1" and ep1) or (comprobacion['id'] != "ep1" and not ep1):
                            continue
                        soup_temporadas.append(temporada)
        else:
            soup_temporadas = soup.find_all(class_='wikitable')

        soup_episodios = []

        for temporada in soup_temporadas:
            soup_episodios += [episodio for episodio in temporada.find_all(class_='vevent') if (episodio.find('th') or episodio.find('td'))['id'][2:].isdigit()]

        if soup_episodios == []:
            for temporada in soup_temporadas[:-1]:
                soup_episodios += [episodio.find('td') for episodio in temporada if episodio.find('td')]

        episodios = []

        for episodio in soup_episodios:
            nombre = episodio.find(class_='resumen') or episodio.find(class_='summary') or episodio
            episodios += [nombre.find('b').text]
        
        return episodios
    
    # Resultado debe ser formato: "[Episodio 1, Episodio 2, ...]"

    def seleccion(self):
        if 'wikipedia' in self.enlace:
            return self.wikipedia()
    
    def archivo(self):

        nombre = self.nombre()
        episodios = self.seleccion()
        cifras_episodios = len(str(len(episodios)))
        linias = []

        for i, episodio in enumerate(episodios):
            linias += [f'{str(i+1).zfill(cifras_episodios)} - {episodio}']

        with open (os.path.join(os.path.dirname(__file__), 'comprobar', f'{nombre}.txt'), 'w', encoding='utf-8') as w:
            w.write('\n'.join(linias))

for url in urls:
    Episodios_Anime(url).archivo()

